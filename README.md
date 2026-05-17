# Vitamin D Status in Ghana: A Mixed-Methods Narrative Review of Prevalence, Determinants, and Health Implications

[![CI](https://github.com/valentineghanem-bit/vitamin-d-ghana-review/actions/workflows/ci.yml/badge.svg)](https://github.com/valentineghanem-bit/vitamin-d-ghana-review/actions) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/) [![R 4.3+](https://img.shields.io/badge/R-4.3+-blue.svg)](https://www.r-project.org/) [![ORCID](https://img.shields.io/badge/ORCID-0009--0002--8332--0220-green.svg)](https://orcid.org/0009-0002-8332-0220) [![OSF](https://img.shields.io/badge/OSF-10.17605%2FOSF.IO%2F53GBT-blue)](https://doi.org/10.17605/OSF.IO/53GBT)

**Author:** Valentine Golden Ghanem | Ghana COCOBOD Cocoa Clinic, Accra, Ghana
**ORCID:** [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)
**Affiliation:** Ghana COCOBOD Cocoa Clinic, Accra, Ghana
**Reporting standard:** STROBE
**Date:** 2025
**Status:** Pre-registered (OSF) | Manuscript under review

> Valentine Golden Ghanem (2025). *Vitamin D Status in Ghana: A Mixed-Methods Narrative Review of Prevalence, Determinants, and Health Implications.* GitHub repository. https://github.com/valentineghanem-bit/vitamin-d-ghana-review

---

## 1. Abstract

This mixed-methods narrative review synthesises evidence on vitamin D deficiency (VDD) in Ghana across 17 studies (N=10,445 participants). Random-effects meta-analysis estimates pooled VDD prevalence and mean 25(OH)D. Spatial analysis using Global Moran's I, Getis-Ord Gi*, and LISA identifies regional clustering of VDD burden. A CART decision tree with leave-one-out cross-validation predicts VDD risk, and multivariable logistic regression quantifies the association between VDD and type 2 diabetes mellitus.

**Pre-registration:** [https://doi.org/10.17605/OSF.IO/53GBT](https://doi.org/10.17605/OSF.IO/53GBT)

**Note on unit conversion:** Studies reporting 25(OH)D in nmol/L were converted to ng/mL by dividing by 2.496.

---

## 2. Research Question & Aims

- **Primary:** Estimate the pooled prevalence of vitamin D deficiency (VDD) in the Ghanaian population.
- **Secondary:** (a) Characterise regional and demographic determinants of VDD; (b) identify spatial clusters of VDD burden across Ghana's regions; (c) build a parsimonious predictive model of VDD risk; (d) quantify the association between VDD and type 2 diabetes mellitus.

---

## 3. Methods Summary

| Method | Tool | Purpose |
|--------|------|---------|
| Random-effects meta-analysis | metafor (R) | Pooled VDD prevalence and mean 25(OH)D |
| Global Moran's I | esda / libpysal | Regional spatial autocorrelation of VDD |
| Getis-Ord Gi* | esda | Regional hotspot identification |
| LISA | esda | Local cluster detection |
| CART (LOOCV) | scikit-learn | VDD risk prediction |
| Logistic regression | scikit-learn / statsmodels | T2DM–VDD association (aOR) |

---

## 4. Data Sources

| Source | Variables | Year | Access |
|--------|-----------|------|--------|
| Published literature (systematic search of PubMed, Scopus, Web of Science) | 25(OH)D levels, VDD prevalence, clinical outcomes | Various | Open |
| Ghana DHS | Regional population denominators | 2014 / 2022 | [dhsprogram.com](https://dhsprogram.com) (registration) |
| Ghana Statistical Service | Regional administrative boundaries | 2021 | [statsghana.gov.gh](https://statsghana.gov.gh) |

> All literature data are extracted from published, peer-reviewed sources. No primary data collection.

---

## 5. Key Findings

| Metric | Value |
|--------|-------|
| Studies included (k) | 17 |
| Total participants (N) | 10,445 |
| Pooled VDD prevalence | 58.3% (95% CI: 47.2–69.4%) |
| Pooled mean 25(OH)D | 18.4 ng/mL (95% CI: 15.8–21.0); I²=97.8% |
| Highest burden group | T2DM patients (88.2%) |
| Ashanti region Gi* hotspot | +2.41 |
| Global Moran's I (VDD) | 0.307 (z=2.14, p=0.031) |
| CART accuracy (LOOCV) | 76.4%; AUC=0.82 |
| Adjusted OR T2DM–VDD | 5.92 (95% CI: 3.11–11.27) |

---

## 6. Repository Structure

```
vitamin-d-ghana-review/
├── data/
│   ├── extracted_data.csv
│   └── data_dictionary.md
├── scripts/
│   ├── meta_analysis.R          # Random-effects meta-analysis
│   ├── spatial_analysis.py      # Moran's I, Gi*, LISA
│   ├── decision_tree.py         # CART with LOOCV
│   └── analysis_pipeline.py     # Full analytical pipeline
├── dashboard/
│   └── dashboard.html           # Self-contained HTML dashboard
├── tests/
├── figures/
├── app.py                       # Plotly Dash interactive application
├── requirements.txt
├── renv.lock
├── Dockerfile
├── CITATION.cff
└── README.md
```

---

## 7. Reproducibility

### 7.1 Requirements
- Python 3.12 (see `requirements.txt` for pinned versions)
- R 4.3+ (for R scripts; see `renv.lock` or `analysis.R` header for pinned packages)
- Random seed: 42 throughout (set via `random_state=42` and `np.random.seed(42)`)
- Estimated runtime: ~2–3 minutes on a standard laptop
- Tested on: Ubuntu 22.04 / macOS 14 / Windows 11 (CI: GitHub Actions)

### 7.2 Clone & install
```bash
git clone https://github.com/valentineghanem-bit/vitamin-d-ghana-review.git
cd vitamin-d-ghana-review
pip install -r requirements.txt
# For R scripts (optional):
Rscript -e "if (!requireNamespace('renv', quietly=TRUE)) install.packages('renv'); renv::restore()"
```

### 7.3 Run the analytical pipeline
```bash
# Full Python pipeline
python scripts/analysis_pipeline.py --all

# R meta-analysis only
Rscript scripts/meta_analysis.R
```

### 7.4 Run the test suite
```bash
pytest tests/ -v
```

### 7.5 Launch the interactive Dash application
```bash
python app.py
# Navigate to http://127.0.0.1:8050 in your browser
```

### 7.6 Open the static HTML dashboard
Open `dashboard/dashboard.html` in any modern browser. No server required.

---

## 8. Outputs

- **Interactive Dash app:** `app.py` — `python app.py` → http://127.0.0.1:8050
- **Static HTML dashboard:** `dashboard/dashboard.html`
- **Figures:** `figures/SuppFig_*.png` — 300 DPI publication-ready
- **Tables:** `data/extracted_data.csv`

---

## 9. Reporting Standard

This study follows the **STROBE** (Strengthening the Reporting of Observational Studies in Epidemiology) reporting guideline for observational ecological studies.

---

## 10. Ethical Statement

This study used exclusively published, de-identified secondary data from a systematic literature review. No primary data collection from human participants was conducted. Ethical review was therefore not required.

---

## 11. Citation

**APA:**
Ghanem, V. G. (2025). *Vitamin D Status in Ghana: A Mixed-Methods Narrative Review of Prevalence, Determinants, and Health Implications*. GitHub. https://github.com/valentineghanem-bit/vitamin-d-ghana-review

**BibTeX:**
```bibtex
@misc{ghanem2025vitamind,
  author = {Ghanem, Valentine Golden},
  title  = {Vitamin D Status in Ghana: A Mixed-Methods Narrative Review of Prevalence, Determinants, and Health Implications},
  year   = {2025},
  url    = {https://github.com/valentineghanem-bit/vitamin-d-ghana-review},
  doi    = {10.17605/OSF.IO/53GBT}
}
```

A machine-readable citation is provided in `CITATION.cff`.

---

## 12. License

Code is released under the **MIT License** — see [LICENSE](LICENSE) for details. Extracted data and figures are released under CC BY 4.0.

---

## 13. Author & Contact

- **Valentine Golden Ghanem**
  Ghana COCOBOD Cocoa Clinic, Accra, Ghana
  Email: [valentineghanem@gmail.com](mailto:valentineghanem@gmail.com)
  ORCID: [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)

---

## 14. Acknowledgements

- **Ghana Demographic and Health Survey programme** (ICF International) for survey data access under signed Data Use Agreement.
- **Ghana Statistical Service** for the 2021 Population and Housing Census and administrative boundary data.
- **WHO Global Health Observatory** for national-level indicators.
- **OSF (Open Science Framework)** for pre-registration hosting.
- **AIPOCH** (Anti-hallucination Pipeline for Open Computational Health) v6.0 quad-connector citation verification (PubMed · Consensus · Scholar · Scite).

---

*This README follows the AIPOCH v6.0 standardised research-output template (May 2026). All repository READMEs in the [valentineghanem-bit](https://github.com/valentineghanem-bit) organisation share this structure.*
