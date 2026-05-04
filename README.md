# Vitamin D Status in Ghana: A Mixed-Methods Narrative Review

[\![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[\![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[\![R 4.3](https://img.shields.io/badge/R-4.3-blue.svg)](https://www.r-project.org/)
[\![PRISMA-ScR](https://img.shields.io/badge/Reporting-PRISMA--ScR-green.svg)](https://www.equator-network.org/)
[\![OSF](https://img.shields.io/badge/OSF-10.17605%2FOSF.IO%2F53GBT-blue)](https://doi.org/10.17605/OSF.IO/53GBT)

**Author:** Valentine Golden Ghanem | Ghana COCOBOD Cocoa Clinic, Accra 
**ORCID:** [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220) 
**Pre-registration:** https://doi.org/10.17605/OSF.IO/53GBT 
**ICD-10 (VDD):** E55.9

---

## Overview

This repository contains all analytical code, data, and reproducibility materials for:

> Ghanem VG. *Vitamin D Status in Ghana: A Mixed-Methods Narrative Review of Prevalence, Determinants, and Health Implications.* 2025. OSF: 10.17605/OSF.IO/53GBT

**Key findings:**
- Pooled VDD prevalence: **58.3%** (95% CI: 47.2–69.4%) across k=17 studies, N=10,445
- Pooled mean 25(OH)D: **18.4 ng/mL** (95% CI: 15.8–21.0); I²=97.8%
- Highest burden: T2DM (88.2%), Psychiatric (85.3%), Ashanti region (Gi*=+2.41)
- Global Moran's I = **0.307** (z=2.14, p=0.031) — significant spatial clustering
- CART decision tree accuracy: **76.4%** (LOOCV), AUC=0.82
- aOR T2DM–VDD association: **5.92** (95% CI: 3.11–11.27)

---

## Repository Structure

```
vitamin-d-ghana-review/
├── data/
│ ├── extracted_data.csv # 17-study extraction dataset (N=10,445)
│ └── data_dictionary.md # Variable definitions and units
├── scripts/
│ ├── meta_analysis.R # Random-effects meta-analysis (meta, metafor)
│ ├── spatial_analysis.py # Global Moran's I, Gi*, LISA (libpysal, esda)
│ ├── decision_tree.py # CART model, LOOCV (scikit-learn)
│ └── analysis_pipeline.py # End-to-end orchestration
├── tests/
│ └── test_analysis.py # Unit tests for analytical functions
├── figures/ # Generated manuscript figures (300 DPI PNG)
├── app.py # Plotly Dash interactive web application
├── dashboard.html # Standalone HTML dashboard (no server required)
├── requirements.txt # Pinned Python dependencies
├── renv.lock # Pinned R dependencies
├── Dockerfile # Docker container for full reproducibility
├── CITATION.cff # Machine-readable citation
├── .github/workflows/ci.yml # CI: lint + tests
└── README.md
```

---

## Quick Start

### Option 1: Docker (recommended — fully reproducible)
```bash
docker build -t vitd-ghana .
docker run -v $(pwd)/figures:/app/figures vitd-ghana
```

### Option 2: Local Python
```bash
git clone https://github.com/VGhanem/vitamin-d-ghana-review.git
cd vitamin-d-ghana-review
pip install -r requirements.txt
python scripts/analysis_pipeline.py --all
```

### Option 3: R meta-analysis only
```r
install.packages("renv")
renv::restore()
source("scripts/meta_analysis.R")
```

### Option 4: Dash web app
```bash
pip install -r requirements.txt
python app.py
# Visit http://127.0.0.1:8050
```

---

## Data Dictionary

See `data/data_dictionary.md` for full variable definitions. 
Key variables: `Study_ID`, `Author_Year`, `N`, `Mean_25OHD` (ng/mL), `VDD_Prevalence` (%), `NOS_Score`, `High_VDD` (binary, threshold >70%).

**Unit conversion:** Studies reporting in nmol/L converted to ng/mL (÷2.496).

---

## Reproducibility

Expected runtime: ~4 minutes (Python ~2 min; R ~2 min) on a standard laptop. 
Tested on: Ubuntu 22.04, macOS 14, Windows 11 (WSL2). 
Random seed: 42 (all stochastic operations).

---

## Citation

```bibtex
@misc{ghanem2025vitamind,
 author = {Ghanem, Valentine Golden},
 title = {Vitamin D Status in Ghana: A Mixed-Methods Narrative Review of Prevalence, Determinants, and Health Implications},
 year = {2025},
 doi = {10.17605/OSF.IO/53GBT},
 url = {https://doi.org/10.17605/OSF.IO/53GBT}
}
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.
