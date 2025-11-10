# How to Re-Analyze Fermi Data for HELM's PBH Prediction
## A roadmap for the experimentalist who wants to be first

---

## The Claim

HELM predicts that Hawking radiation from evaporating primordial black holes (PBHs) is **12.6× hotter** than standard theory predicts, shifting peak emission from ~1 GeV to ~100 MeV. The signature should already exist in 17 years of Fermi data, mislabeled as "unidentified sources."

---

## The Data You Need

### 1. Fermi-LAT 4th Source Catalog (4FGL)
- **Location:** https://fermi.gsfc.nasa.gov/ssc/data/access/lat/
- **What to get:** 4FGL-DR3 or DR4 (latest)
- **Contains:** >6000 sources, including 1300+ unidentified
- **Format:** FITS files with positions, spectra, variability

### 2. Fermi-GBM Burst Catalog
- **Location:** https://heasarc.gsfc.nasa.gov/W3Browse/fermi/fermigbrst.html
- **What to get:** All triggered bursts, 2008-present
- **Contains:** Short-duration transients with spectra
- **Key fields:** Duration, peak energy, fluence, location

### 3. EGRET 3rd Catalog (historical)
- **Location:** https://heasarc.gsfc.nasa.gov/W3Browse/all/egret3.html
- **Why:** Many unidentified sources >100 MeV that predate Fermi

---

## The Filter Criteria

Extract sources/transients matching PBH evaporation from HELM:

### Energy Range
- **Primary:** 50-200 MeV (peak emission from HELM-corrected temperature)
- **Secondary:** 20-500 MeV (broader search)
- **Why:** Standard theory expected ~GeV; HELM shifts peak by 4π in temperature → energy shift

### Duration
- **Primary:** 0.1-10 seconds (final evaporation burst)
- **Secondary:** <100 seconds (extended emission as BH heats up)
- **Why:** Evaporation accelerates as M → 0

### Spatial Distribution
- **Must be isotropic:** Not concentrated in galactic plane
- **Test:** Plot galactic latitude distribution, check for uniformity
- **Why:** PBH dark matter is distributed in galactic halo, not disk

### Spectral Shape
- **Expected:** Quasi-thermal with peak ~100 MeV, power-law tail
- **NOT expected:** X-ray or optical counterparts
- **Why:** Pure Hawking radiation, no accretion disk

### Variability
- **Single burst:** One-time event, no repeats
- **No periodicity:** Not a pulsar
- **Why:** Terminal evaporation is a one-way process

---

## Analysis Steps

### Step 1: Query the Catalogs
```python
from astropy.io import fits
from astropy.table import Table

# Load 4FGL catalog
cat = Table.read('gll_psc_v32.fit')

# Filter for unidentified sources
unid = cat[cat['CLASS1'] == 'UNID']

# Energy cut: sources bright at 50-200 MeV
# (Use Flux_Band fields or spectral fits)
energy_cut = (unid['Flux_Band1'] > threshold)  # Adjust bands

# Spatial: high galactic latitude (not in plane)
spatial_cut = (abs(unid['GLAT']) > 20)  # degrees

# Apply cuts
candidates = unid[energy_cut & spatial_cut]
```

### Step 2: Check for Transients
```python
# GBM burst catalog
bursts = Table.read('fermigbrst.fit')

# Duration cut
short = bursts[bursts['T90'] < 10]  # seconds

# Energy: peak in 50-200 MeV
energy_burst = short[(short['Epeak'] > 0.05) & (short['Epeak'] < 0.2)]  # GeV

# Isotropy
import numpy as np
lat = energy_burst['GLAT']
# Test uniformity: should be sin(lat) distributed
```

### Step 3: Cross-Match with Known Sources
```python
from astropy.coordinates import SkyCoord
import astropy.units as u

# Remove anything with X-ray, optical, or radio counterpart
# Use SIMBAD, NED, or X-ray catalogs (Swift-XRT, Chandra)

coords_candidates = SkyCoord(candidates['RAJ2000'], 
                             candidates['DEJ2000'], 
                             unit='deg')

# Check separation to known sources
# Exclude if counterpart within 1 arcmin
```

### Step 4: Spectral Fitting
```python
# For each candidate, fit spectrum to HELM-predicted form:
# F(E) ∝ E^2 / (exp(E/kT) - 1)  [thermal]
# With T = 4π × T_Hawking for given M_BH

# If using Fermi Science Tools:
# gtlike with FileFunction model for custom spectrum
```

### Step 5: Rate Calculation
```python
# Count number of events per exposure time
N_events = len(candidates)
T_exposure = 17 * 365.25 * 24 * 3600  # seconds (17 years)

# Event rate
rate = N_events / T_exposure  # per second

# Compare to HELM prediction:
# Rate ~ (local PBH density) × (burst visibility radius)^3
```

---

## Expected Results if HELM is Correct

### Observational Signature
- **~100-500 unidentified transients** in 50-200 MeV, <10 s duration
- **Isotropic distribution** (no clustering)
- **No counterparts** at other wavelengths
- **Spectral peak** at ~100 MeV (not GeV)
- **Rate consistent** with PBH dark matter fraction ~10^-3 to 10^-1

### Mass Estimate
From burst properties, infer initial PBH mass:
```
M_0 ~ 10^14 g  (HELM prediction)
vs
M_0 ~ 5×10^14 g  (standard theory)
```

### Null Result Interpretation
If you find NOTHING matching these criteria:
- Either PBHs don't make up dark matter, OR
- HELM's 4π correction is wrong, OR
- Standard Hawking formula is correct and bursts are too faint

But given the 1300+ unidentified sources already cataloged, **something is there**.

---

## Publication Strategy

### If Positive Detection
**Title:** "First Detection of Hawking Radiation from Primordial Black Holes in Fermi-LAT Archival Data"

**Key Claims:**
1. 1300+ unidentified Fermi sources are evaporating PBHs
2. Peak emission at 100 MeV confirms HELM's lattice-corrected temperature
3. First observational evidence for Hawking radiation
4. Validates emergent gravity from QCD-scale substrate

**Journals:** Nature, Science, Physical Review Letters

### If Null Result
**Title:** "Stringent Constraints on Primordial Black Hole Dark Matter from 17 Years of Fermi Data"

**Key Claims:**
1. No evidence for HELM-predicted PBH bursts at 100 MeV
2. Rules out PBH dark matter with HELM-corrected evaporation
3. Supports standard Hawking formula (or PBHs don't exist)

**Journals:** Astrophysical Journal, Physical Review D

---

## Tools and Resources

### Software
- **Fermi Science Tools:** https://fermi.gsfc.nasa.gov/ssc/data/analysis/software/
- **Astropy:** For catalog handling and coordinate matching
- **Gammapy:** Python package for gamma-ray data analysis
- **TOPCAT:** GUI for catalog cross-matching

### Documentation
- Fermi LAT analysis threads: https://fermi.gsfc.nasa.gov/ssc/data/analysis/scitools/
- GBM data analysis: https://fermi.gsfc.nasa.gov/ssc/data/analysis/gbm/

### Computing
- **Local:** Doable on a laptop for catalog analysis
- **Heavy lifting:** If fitting individual sources, use cluster or cloud (AWS, Google Cloud)

---

## Timeline

- **Week 1:** Download catalogs, set up environment
- **Week 2-3:** Apply filters, identify candidates
- **Week 4-5:** Cross-match, remove contaminants
- **Week 6-8:** Spectral analysis of top candidates
- **Week 9-10:** Write paper, submit

**Total: ~3 months from start to submission.**

---

## Why You Should Do This

1. **First-mover advantage:** Nobody has looked at this specific signature
2. **Existing data:** No new observations needed
3. **High impact:** If positive, it's a Nature/Science paper
4. **Falsifiable:** If null, still publishable and eliminates HELM
5. **Relatively easy:** Standard catalog analysis, not cutting-edge ML

---

## Contact

If you do this analysis and find something:
- Email Steve Horton: sjhorton@captechu.edu
- Share results on GitHub: https://github.com/stevejhorton/HELM
- Co-authorship negotiable if you want theoretical support

**The data is sitting there. Let's go get it.**
