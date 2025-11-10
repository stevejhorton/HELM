# HELM — Hierarchical Elastic Lattice Model  
*Deriving ℏ, G, Λ, and α from a single hadronic-scale substrate*

---

## Overview
##READ THE PAPERS - 
[HELM_Main Paper](paper/dry_full.pdf "HELM_Main")
[HELM_Sup Paper (for the real geeks)](paper/sup/HELM_Supplement.pdf "HELM_Sup")

[Visual](tree/main/paper/figures/3d_lattice.png "Lattice_Visual")
##

HELM proposes that **space-time is an elastic lattice** with QCD-scale string tension  
**σ ≈ 1.4 × 10⁵ J·m⁻¹**, measured in laboratory settings.  
From this single constant, the model **derives**:

| Constant         | Prediction                  | Error vs CODATA         |
|------------------|-----------------------------|--------------------------|
| Planck ℏ         | 1.0546 × 10⁻³⁴ J·s          | 0.04%                    |
| Newton G         | 6.6743 × 10⁻¹¹ m³·kg⁻¹·s⁻²  | 0.00%                    |
| Cosmological Λ   | 5 × 10⁻¹⁰ J·m⁻³             | Order-of-magnitude       |
| Fine-structure α | 1 / 137.036                 | No free parameter        |

No extra dimensions. No free parameters. No Planck-scale miracles.  
Just **geometry and elasticity**.

---

## Key Components

- **Paper (LaTeX):** Full derivation and predictions  
- **PTA Search:** Python notebook testing HELM’s constant-strain GW background at 3 nHz vs NANOGrav 15-year data    
- **Twist-Sector Magnetism:** α = 1/137 derived from node-orientation elasticity

---

## Repository Structure

```
HELM/
├── paper/               # ArXiv-ready LaTeX source
│   ├── dry_full.tex
│   └── figures/
├── pta/                 # NANOGrav 15-yr constant-strain search
│   ├── lattice_pta.py   # Fail-fast, resumable MCMC
│   ├── README_PTA.md    # Run instructions
│   └── chains/          # Output Bayes factors & corner plots
├── hardware/            # Printed Neural Lattice gerbers & firmware
└── LICENSE              # GNU
```

---

## Quick Start: PTA Search

```bash
git clone https://github.com/stevejhorton/HELM.git
cd HELM/pta
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python lattice_pta.py
```

- Downloads the 609 MB NANOGrav 15-year dataset
- Runs two models: power-law vs constant-strain
- Prints:

```
Bayes factor (Const / PL) = 3.4 ± 0.3
h_c @ 3.2 nHz  95% UL = 1.1e-15   (lattice = 1.0e-15)
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

**Stephan “Steve” Horton**  
📧 stevejhorton@captechu.edu  
🔗 ORCID: https://orcid.org/0009-0006-8205-2518

---

*“One substrate. One miracle.”*
