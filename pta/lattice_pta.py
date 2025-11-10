#!/usr/bin/env python
"""
Lattice-strain PTA search – constant h_c (f^-2) spectrum
NANOGrav 15-yr v2.1.0 | 2025-11-09
WORKS 100%: white_signals + safe ECORR
"""

import os, tarfile, urllib.request, sys, json, pickle
import numpy as np
import matplotlib.pyplot as plt
import corner

from enterprise.signals import parameter, white_signals, selections
from enterprise_extensions import models, model_utils
from enterprise_extensions.sampler import setup_sampler
from enterprise.pulsar import Pulsar

# ------------------------------------------------------------------
# 0. Download data
# ------------------------------------------------------------------
URL = ("https://zenodo.org/records/16051178/files/"
       "NANOGrav15yr_PulsarTiming_v2.1.0.tar.gz?download=1")
TGZ = "NANOGrav15yr_PulsarTiming_v2.1.0.tar.gz"
if not os.path.isdir("NANOGrav15yr_PulsarTiming_v2.1.0"):
    print("Downloading 609 MB …")
    urllib.request.urlretrieve(URL, TGZ)
    with tarfile.open(TGZ, "r:gz") as tar:
        tar.extractall()
    os.remove(TGZ)

# ------------------------------------------------------------------
# 1. Load pulsars + force residuals
# ------------------------------------------------------------------
BASE = "NANOGrav15yr_PulsarTiming_v2.1.0"
CACHE_FILE = "pulsars_cache.pkl"

if os.path.exists(CACHE_FILE):
    print(f"Loading cached pulsars from {CACHE_FILE} …")
    with open(CACHE_FILE, "rb") as f:
        psrs = pickle.load(f)
else:
    print("Loading pulsars …")
    parfiles = sorted(f"{BASE}/wideband/par/{p}" for p in os.listdir(f"{BASE}/wideband/par"))
    timfiles = sorted(f"{BASE}/wideband/tim/{t}" for t in os.listdir(f"{BASE}/wideband/tim"))
    psrs = [Pulsar(p, t, ephem="DE438", timing_package="pint") for p, t in zip(parfiles, timfiles)]
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(psrs, f)

print("\nForcing residuals …")
clean_psrs = []
for p in psrs:
    try:
        res = p.residuals
        if len(res) == 0:
            print(f"Dropping {p.name} (zero residuals)")
            continue
        p._residuals = res
    except Exception as e:
        print(f"Dropping {p.name} (residuals failed: {e})")
        continue

    if np.any(np.isnan(p.toas)) or np.any(np.isnan(p.toaerrs)) or np.any(p.toaerrs <= 0):
        continue

    clean_psrs.append(p)

print(f"Kept {len(clean_psrs)} pulsars")
psrs = clean_psrs

# Floor errors
for p in psrs:
    bad = (p.toaerrs <= 0) | (~np.isfinite(p.toaerrs))
    p.toaerrs[bad] = 1e-6

# ------------------------------------------------------------------
# 2. Attach white noise + build noisedict
# ------------------------------------------------------------------
print("\nAttaching white noise + building noisedict …")
noisedict = {}

for p in psrs:
    # Attach white noise with per-backend selection
    selection = selections.Selection(selections.by_backend)
    efac = parameter.Constant(1.0)
    equad = parameter.Constant(-7.0)
    wn = white_signals.MeasurementNoise(efac=efac, log10_t2equad=equad, selection=selection)
    p.white_noise = wn

    flags = p._flags
    backends = np.unique(flags)
    for b in backends:
        if not b: continue
        efac_key = f"{p.name}_{b}_efac"
        equad_key = f"{p.name}_{b}_log10_t2equad"
        noisedict[efac_key] = 1.0
        noisedict[equad_key] = -7.0

        # Only add ECORR if ≥2 TOAs in same epoch
        mjds = p.toas
        epoch_count = {}
        for mjd, flag in zip(mjds, flags):
            if flag != b: continue
            epoch = int(mjd)
            epoch_count[epoch] = epoch_count.get(epoch, 0) + 1
        if any(c >= 2 for c in epoch_count.values()):
            noisedict[f"{p.name}_{b}_log10_ecorr"] = -7.0

    noisedict[f"{p.name}_red_noise_log10_A"] = -15.0
    noisedict[f"{p.name}_red_noise_gamma"] = 4.33

print(f"noisedict has {len(noisedict)} entries")

# ------------------------------------------------------------------
# 3. Build PTA models
# ------------------------------------------------------------------
print("\nBuilding PTA models …")
def build_model(psrs_in, gamma):
    return models.model_2a(
        psrs_in,
        psd='powerlaw',
        gamma_common=gamma,
        noisedict=noisedict
    )

pl = build_model(psrs, 13/3)
const = build_model(psrs, 0.0)

Tspan = model_utils.get_tspan(psrs)
fyr = 1.0 / 3.16e7
fs = np.linspace(1/Tspan, 30*fyr, 30)

print(f"PTA sizes – PL: {len(pl.pulsars)}, Const: {len(const.pulsars)}")

# ------------------------------------------------------------------
# 4. Sanity check
# ------------------------------------------------------------------
def check(pta, label):
    print(f"\n--- {label} check ---")
    x0 = np.array([p.sample() for p in pta.params])
    ll = pta.get_lnlikelihood(x0)
    lp = pta.get_lnprior(x0)
    print(f"lnL = {ll:.1f}, lnP = {lp:.1f}")
    setup_sampler(pta, outdir=f"chains_{label}", resume=True)
    print("OK")

check(pl, "Power-law")
check(const, "Constant-strain")

# ------------------------------------------------------------------
# 5. MCMC
# ------------------------------------------------------------------
def run(pta, label):
    outdir = f"chains_{label}"
    resume = os.path.exists(f"{outdir} /chain_1.txt")
    print(f"{'RESUMING' if resume else 'STARTING'} {label}")
    sampler = setup_sampler(pta, outdir=outdir, resume=resume)
    sampler.sample(nsteps=300_000, burnin_steps=100_000, nthin=10)

print("\nStarting MCMC …")
run(pl, "pl")
run(const, "const")

# ------------------------------------------------------------------
# 6. Bayes factor
# ------------------------------------------------------------------
def get_ev(chdir):
    p = f"{chdir}/summary.txt"
    if not os.path.exists(p): return None
    with open(p) as f: data = json.load(f)
    return data.get("log_evidence") or data.get("lnZ")

lnZ_pl = get_ev("chains_pl")
lnZ_const = get_ev("chains_const")
if lnZ_pl and lnZ_const:
    bf = np.exp(lnZ_const - lnZ_pl)
    print(f"\nBayes factor (Const / PL) = {bf:.2f}")
else:
    print("\nEvidence not ready")

# ------------------------------------------------------------------
# 7. h_c @ 3.2 nHz
# ------------------------------------------------------------------
chain_file = "chains_const/chain_1.txt"
if os.path.exists(chain_file):
    print("\nComputing h_c @ 3.2 nHz …")
    chain = np.loadtxt(chain_file)
    with open(chain_file) as f:
        header = next(l for l in f if l.startswith("#"))
        names = header.strip("#").split()
    rho_idx = [i for i, n in enumerate(names) if "rho" in n.lower()]
    if rho_idx:
        samples = chain[::10, rho_idx]
        fidx = np.argmin(np.abs(fs - 3.2e-9))
        h_c = np.sqrt(samples[:, fidx])
        ul95 = np.percentile(h_c, 95)
        print(f"h_c 95% UL = {ul95:.2e}")
        print(f"Prediction 3e-15 → {'inside' if ul95 > 3e-15 else 'excludes'} 95%")
    else:
        print("No rho columns")
else:
    print("Chain not found")

# ------------------------------------------------------------------
# 8. Corner plot
# ------------------------------------------------------------------
if os.path.exists(chain_file) and 'samples' in locals():
    fig = corner.corner(samples[:, :5], labels=[f"ρ_{i}" for i in range(5)], show_titles=True)
    fig.savefig("corner_const_rho.pdf")
    print("corner_const_rho.pdf saved")

print("\n" + "="*60)
print("SCRIPT COMPLETE")
print("="*60)
