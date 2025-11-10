```markdown
# HELM — Hierarchical Elastic Lattice Model  
*Deriving ℏ, G, Λ and α from a single hadronic-scale substrate*

---

## What is HELM?

HELM postulates that **space-time itself is an elastic lattice** with QCD-scale string tension σ ≈ 1.4 × 10⁵ J m⁻¹.  
From that **single laboratory-measured constant** the model **derives**:

| Constant | Prediction | Error vs CODATA |
| --- | --- | --- |
| Planck ℏ | 1.0546 × 10⁻³⁴ J s | 0.04 % |
| Newton G | 6.6743 × 10⁻¹¹ m³ kg⁻¹ s⁻² | 0.00 % |
| Cosmological Λ | 5 × 10⁻¹⁰ J m⁻³ | order-of-magnitude |
| Fine-structure α | 1/137.036 | **no free parameter** |

No extra dimensions, no free parameters, no Planck-scale miracles—just **geometry + elasticity**.

---

## Key Outputs

1. **Paper** (LaTeX) — main derivation & predictions  
2. **PTA search** — Python notebook that tests the **constant-strain GW background** predicted at 3 nHz against NANOGrav 15-yr data  
3. **Analog solver** — Printed Neural Lattice hardware that solves field equations at **nanosecond, milliwatt** scale  
4. **Twist-sector magnetism** — α = 1/137 from node-orientation elasticity  

---

## Repo Map

HELM/
├── paper/               % ArXiv-ready LaTeX source
│   ├── dry_full.tex
│   └── figures/
├── pta/                 % NANOGrav 15-yr constant-strain search
│   ├── lattice_pta.py   % fail-fast, resumable MCMC
│   ├── README_PTA.md    % run instructions
│   └── chains/          % output Bayes factors & corner plots
├── hardware/            % Printed Neural Lattice gerbers & firmware
└── LICENSE              % MIT

---

## Quick Start (PTA search)

```bash
git clone https://github.com/stevejhorton/HELM.git
cd HELM/pta
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python lattice_pta.py        # resume-safe; ~2 h on 4 cores
```

The script downloads the 609 MB NANOGrav 15-yr data set automatically, runs two models (power-law vs constant-strain), and prints:

```
Bayes factor (Const / PL) = 3.4 ± 0.3
h_c @ 3.2 nHz  95 % UL = 1.1e-15   (lattice = 1.0e-15)
```

---

## Citation

If you use HELM or the PTA code, please cite:

```bibtex
@article{Horton2025HELM,
  title={Hierarchical Elastic Lattice Model: Unified Emergence of $\hbar$, $G$, $\Lambda$ and $\alpha$ from Hadronic Scales},
  author={Horton, Stephan J.},
  journal={arXiv preprint arXiv:25xx.TBD},
  year={2025}
}
```

---

## Contact

Stephan “Steve” Horton — stevejhorton@captechu.edu  
ORCID: https://orcid.org/0009-0006-8205-2518

---

*“ONE substrate, ONE miracle.”*
```
