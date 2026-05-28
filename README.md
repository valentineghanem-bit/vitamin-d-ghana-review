# Vitamin D Status in Ghana: A Mixed-Methods Narrative Review of Prevalence, Determinants, and Health Implications

[![CI](https://github.com/valentineghanem-bit/vitamin-d-ghana-review/actions/workflows/ci.yml/badge.svg)](https://github.com/valentineghanem-bit/vitamin-d-ghana-review/actions) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/) [![R 4.3+](https://img.shields.io/badge/R-4.3+-blue.svg)](https://www.r-project.org/) [![ORCID](https://img.shields.io/badge/ORCID-0009--0002--8332--0220-green.svg)](https://orcid.org/0009-0002-8332-0220)

**Author:** Valentine Golden Ghanem | Ghana COCOBOD Cocoa Clinic, Accra, Ghana
**ORCID:** [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)
**Affiliation:** Ghana COCOBOD Cocoa Clinic, Accra, Ghana
**Reporting standard:** STROBE
**Date:** 2025
**Status:** Pre-registered (OSF) | Manuscript under review

**Pre-registration:** [https://doi.org/10.17605/OSF.IO/53GBT](https://doi.org/10.17605/OSF.IO/53GBT)

---

## 1. Abstract

This mixed-methods narrative review synthesises evidence on vitamin D deficiency (VDD) in Ghana across 17 studies (N = 10,445 participants). Random-effects meta-analysis estimates pooled VDD prevalence and mean serum 25(OH)D concentration. Spatial analysis using Global Moran's I, Getis-Ord Gi*, and LISA identifies regional clustering of VDD burden across Ghana's 16 administrative regions. A CART decision tree with leave-one-out cross-validation predicts VDD risk at the regional level, and multivariable logistic regression quantifies the independent association between VDD and type 2 diabetes mellitus (T2DM).

> **Note on unit conversion:** Studies reporting 25(OH)D in nmol/L were converted to ng/mL by dividing by 2.496.

---

## 2. Research Question & Aims

- **Primary:** Estimate the pooled prevalence of vitamin D deficiency in the Ghanaian population.
- **Secondary:** (a) Characterise regional and demographic determinants of VDD; (b) identify spatial clusters of VDD burden across Ghana's regions; (c) build a parsimonious predictive model of VDD risk; (d) quantify the independent association between VDD and type 2 diabetes mellitus.

---

## 3. Methods Summary

| Method | Tool | Purpose |
|--------|------|---------|
| Random-effects meta-analysis | metafor (R) | Pooled VDD prevalence and mean 25(OH)D |
| Global Moran's I | esda / libpysal | Regional spatial autocorrelation of VDD |
| Getis-Ord Gi* | esda | Regional hotspot identification |
| LISA | esda | Local cluster detection |
| CART (LOOCV) | scikit-learn | VDD risk prediction |
| Multivariable logistic regression | statsmodels | T2DM–VDD association (adjusted OR) |
| Spatial diagnostics | spdep / spatialreg (R) | OLS / SLM / SEM model selection |

---

## 4. Data Sources

| Source | Variables | Year | Access |
|--------|-----------|------|--------|
| Published literature (PubMed, Scopus, Web of Science) | 25(OH)D levels, VDD prevalence, clinical outcomes | Various | Open — peer-reviewed publications |
| Ghana DHS | Regional population denominators | 2014 / 2022 | [dhsprogram.com](https://dhsprogram.com) (registration) |
| Ghana Statistical Service | Regional administrative boundaries | 2021 | [statsghana.gov.gh](https://statsghana.gov.gh) |

> All literature data extracted from published peer-reviewed sources. No primary data collection.

---

## 5. Key Findings

| Metric | Value |
|--------|-------|
| Studies included (k) | 17 |
| Total participants (N) | 10,445 |
| Pooled VDD prevalence | 58.3% (95% CI: 47.2–69.4%) |
| Pooled mean 25(OH)D | 18.4 ng/mL (95% CI: 15.8–21.0); I² = 97.8% |
| Highest-burden subgroup | T2DM patients (88.2%) |
| Ashanti region Gi* hotspot | z = +2.41 |
| Global Moran's I (VDD) | 0.307 (z = 2.14, p = 0.031) |
| CART accuracy (LOOCV) | 76.4%; AUC = 0.82 |
| Adjusted OR (T2DM–VDD) | 5.92 (95% CI: 3.11–11.27) |

---

## 6. Repository Structure

```
vitamin-d-ghana-review/
├── data/
│   ├── extracted_data.csv          # Extracted literature data
│   └── data_dictionary.md
├── scripts/
│   ├── meta_analysis.R             # Random-effects meta-analysis
│   ├── spatial_analysis.py         # Moran's I, Gi*, LISA
│   ├── decision_tree.py            # CART with LOOCV
│   ├── analysis_pipeline.py        # Full analytical pipeline
│   ├── spatial_utils.py            # Reusable spatial analysis utilities
│   └── spatial_diagnostics.R       # R: spatial autocorrelation diagnostics
├── app.py                          # Plotly Dash interactive application
├── analysis.R                      # R: meta-analysis + spatial regression diagnostics
├── dashboard/
│   └── dashboard.html
├── poster/
│   └── vitamin_d_ghana_poster.html
├── figures/
├── tests/
├── requirements.txt
├── renv.lock
├── Dockerfile
├── CITATION.cff
└── README.md
```

---

## 7. Reproducibility

### 7.1 Requirements

- Python 3.12 (pinned in `requirements.txt`)
- R 4.3+ with packages: metafor, spdep, spatialreg, dplyr (see `analysis.R` header)
- Random seed: 42 throughout
- Estimated runtime: ~2–3 minutes on a standard laptop
- Tested on: Ubuntu 22.04 / macOS 14 / Windows 11 (CI: GitHub Actions)

### 7.2 Clone & install

```bash
git clone https://github.com/valentineghanem-bit/vitamin-d-ghana-review.git
cd vitamin-d-ghana-review
pip install -r requirements.txt
# For R scripts:
Rscript -e "if (!requireNamespace('renv', quietly=TRUE)) install.packages('renv'); renv::restore()"
```

### 7.3 Run the analytical pipeline

```bash
python scripts/analysis_pipeline.py
```

### 7.4 Run the test suite

```bash
pytest tests/ -v
```

### 7.5 Launch the interactive Dash application

```bash
python app.py
# Visit http://127.0.0.1:8050
```

### 7.6 Open the static HTML dashboard

```bash
# macOS
open dashboard/dashboard.html
# Windows
start dashboard/dashboard.html
# Linux
xdg-open dashboard/dashboard.html
```

---

## 8. Outputs

| Output | Description |
|--------|-------------|
| `data/` | Extracted literature dataset, data dictionary |
| `figures/` | Forest plots, funnel plots, spatial cluster maps (PNG) |
| `dashboard/` | Self-contained interactive HTML dashboard |
| `poster/` | A0 conference poster (HTML, print-ready) |

## 8a. Downloadable Artefacts (HTML)

Both the interactive dashboard and the conference poster are committed as self-contained HTML files — no server, no build step required.

| Artefact | View on GitHub | Live preview | Direct download (raw HTML) |
|----------|---------------|--------------|---------------------------|
| Interactive dashboard | [View](https://github.com/valentineghanem-bit/vitamin-d-ghana-review/blob/main/dashboard/dashboard.html) | [Preview](https://htmlpreview.github.io/?https://github.com/valentineghanem-bit/vitamin-d-ghana-review/blob/main/dashboard/dashboard.html) | [Download](https://raw.githubusercontent.com/valentineghanem-bit/vitamin-d-ghana-review/main/dashboard/dashboard.html) |
| Conference poster | [View](https://github.com/valentineghanem-bit/vitamin-d-ghana-review/blob/main/poster/vitamin_d_ghana_poster.html) | [Preview](https://htmlpreview.github.io/?https://github.com/valentineghanem-bit/vitamin-d-ghana-review/blob/main/poster/vitamin_d_ghana_poster.html) | [Download](https://raw.githubusercontent.com/valentineghanem-bit/vitamin-d-ghana-review/main/poster/vitamin_d_ghana_poster.html) |

> **Tip:** The dashboard works fully offline once downloaded. The poster is print-ready at A0 (841 × 1189 mm).

---

## 9. Reporting Standard

This study follows the **STROBE** (Strengthening the Reporting of Observational Studies in Epidemiology) reporting guideline for observational ecological studies and the **PRISMA** guideline for the systematic literature synthesis component.

---

## 10. Ethical Statement

This study synthesises data from published peer-reviewed literature. No individual participant data were collected or accessed. All analyses use aggregate statistics extracted from published studies. Ethical approval was not required. The study is pre-registered at OSF: [https://doi.org/10.17605/OSF.IO/53GBT](https://doi.org/10.17605/OSF.IO/53GBT).

---

## 11. Citation

**APA:**
Ghanem, V. G. (2025). *Vitamin D Status in Ghana: A Mixed-Methods Narrative Review of Prevalence, Determinants, and Health Implications.* GitHub. https://github.com/valentineghanem-bit/vitamin-d-ghana-review

**BibTeX:**
```bibtex
@misc{ghanem2025vitamind,
  author = {Ghanem, Valentine Golden},
  title  = {Vitamin D Status in Ghana: A Mixed-Methods Narrative Review of Prevalence, Determinants, and Health Implications},
  year   = {2025},
  url    = {https://github.com/valentineghanem-bit/vitamin-d-ghana-review}
}
```

A machine-readable citation is provided in `CITATION.cff`.

---

## 12. License

Code is released under the **MIT License** — see [LICENSE](LICENSE) for details.
Outputs and figures: **CC BY 4.0**.

---

## 13. Author & Contact

**Valentine Golden Ghanem**
Ghana COCOBOD Cocoa Clinic, Accra, Ghana
Email: valentineghanem@gmail.com
ORCID: [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)

---

## 14. Acknowledgements

The author thanks the authors of the 17 primary studies included in this review for their contributions to the Ghanaian vitamin D literature. Meta-analysis used the R metafor package. Spatial analysis relied on esda, libpysal, spdep, and spatialreg. Machine learning used scikit-learn. The T2DM–VDD association documented here has clinical implications for screening practice at the Ghana COCOBOD Cocoa Clinic.
