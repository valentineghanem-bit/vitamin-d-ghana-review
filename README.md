# Vitamin D Status in Ghana: A Mixed-Methods Narrative Review of Prevalence, Determinants, and Health Implications

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/) [![ORCID](https://img.shields.io/badge/ORCID-0009--0002--8332--0220-green.svg)](https://orcid.org/0009-0002-8332-0220)

**Author:** Valentine Golden Ghanem | Ghana COCOBOD Cocoa Clinic, Accra, Ghana  
**ORCID:** [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)  
**Reporting standard:** STROBE  
**Date:** 2025

> Ghanem VG. *Vitamin D Status in Ghana: A Mixed-Methods Narrative Review of Prevalence, Determinants, and Health Implications.* 2025. OSF: [10.17605/OSF.IO/53GBT](https://doi.org/10.17605/OSF.IO/53GBT)

**Pre-registration:** https://doi.org/10.17605/OSF.IO/53GBT

**Note on unit conversion:** Studies reporting 25(OH)D in nmol/L were converted to ng/mL by dividing by 2.496.

---

## Overview

This mixed-methods narrative review synthesises evidence on vitamin D deficiency (VDD) in Ghana across 17 studies (N=10,445 participants). Random-effects meta-analysis estimates pooled VDD prevalence and mean 25(OH)D. Spatial analysis using Global Moran's I, Gi*, and LISA identifies regional clustering of VDD burden. A CART decision tree with LOOCV predicts VDD risk, and logistic regression quantifies the association between VDD and type 2 diabetes mellitus.

---

## Key Findings

| Metric | Value |
|--------|-------|
| Studies included (k) | 17 |
| Total participants (N) | 10,445 |
| Pooled VDD prevalence | 58.3% (95% CI: 47.2–69.4%) |
| Pooled mean 25(OH)D | 18.4 ng/mL (95% CI: 15.8–21.0); I²=97.8% |
| Highest burden group | T2DM (88.2%) |
| Ashanti region Gi* hotspot | +2.41 |
| Global Moran's I (VDD) | 0.307 (z=2.14, p=0.031) |
| CART accuracy (LOOCV) | 76.4%; AUC=0.82 |
| aOR T2DM–VDD | 5.92 (95% CI: 3.11–11.27) |

---

## Repository Structure

```
vitamin-d-ghana-review/
├── data/
│   ├── extracted_data.csv
│   └── data_dictionary.md
├── scripts/
│   ├── meta_analysis.R
│   ├── spatial_analysis.py
│   ├── decision_tree.py
│   └── analysis_pipeline.py
├── dashboard/
│   └── dashboard.html
├── tests/
├── figures/
├── app.py
├── requirements.txt
├── renv.lock
├── Dockerfile
└── CITATION.cff
```

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/valentineghanem-bit/vitamin-d-ghana-review.git
cd vitamin-d-ghana-review
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
# For R meta-analysis:
# Rscript -e "renv::restore()"
```

### 3. Run the pipeline

```bash
# Full Python pipeline
python scripts/analysis_pipeline.py --all

# R meta-analysis only
Rscript scripts/meta_analysis.R
```

### 4. Run tests

```bash
pytest tests/ -v
```

### 5. Open the interactive dashboard

Open `dashboard/dashboard.html` in any modern browser. No server required.

---

## Data Sources

| Source | Variables | Year | Access |
|--------|-----------|------|--------|
| Published literature (systematic search) | 25(OH)D levels, VDD prevalence, clinical outcomes | Various | PubMed, Scopus, Web of Science |
| Ghana DHS | Regional population denominators | 2014 / 2022 | dhsprogram.com (registration) |
| Ghana Statistical Service | Regional administrative boundaries | 2021 | statsghana.gov.gh |

---

## Methods Summary

| Method | Tool | Purpose |
|--------|------|---------|
| Random-effects meta-analysis | metafor (R) | Pooled VDD prevalence and mean 25(OH)D |
| Global Moran's I | esda / libpysal | Regional spatial autocorrelation of VDD |
| Getis-Ord Gi* | esda | Regional hotspot identification |
| LISA | esda | Local cluster detection |
| CART (LOOCV) | scikit-learn | VDD risk prediction |
| Logistic regression | scikit-learn / statsmodels | T2DM–VDD association (aOR) |

---

## Reproducibility

- Random seed: 42 throughout  
- Reporting: STROBE  
- All random seeds set explicitly (`random_state=42`)  
- R meta-analysis: renv.lock pins all package versions
- Pre-registered at OSF: https://doi.org/10.17605/OSF.IO/53GBT

---

## Ethical Statement

This study used exclusively published, de-identified secondary data from a systematic literature review. No primary data collection from human participants was conducted. Ethical review was therefore not required.

---

## Citation

```bibtex
@misc{ghanem2025vitamind,
  author = {Ghanem, Valentine Golden},
  title  = {Vitamin D Status in Ghana: A Mixed-Methods Narrative Review of Prevalence, Determinants, and Health Implications},
  year   = {2025},
  url    = {https://github.com/valentineghanem-bit/vitamin-d-ghana-review},
  doi    = {10.17605/OSF.IO/53GBT}
}
```

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## Contact

Valentine Golden Ghanem  
Ghana COCOBOD Cocoa Clinic, Accra, Ghana  
valentineghanem@gmail.com  
ORCID: [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)
