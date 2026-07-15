# Vitamin D Status in Ghana: A Systematic Review with Meta-Analysis

[![CI](https://github.com/valentineghanem-bit/vitamin-d-ghana-review/actions/workflows/ci.yml/badge.svg)](https://github.com/valentineghanem-bit/vitamin-d-ghana-review/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/) [![R 4.3+](https://img.shields.io/badge/R-4.3+-blue.svg)](https://www.r-project.org/) [![ORCID](https://img.shields.io/badge/ORCID-0009--0002--8332--0220-green.svg)](https://orcid.org/0009-0002-8332-0220)

**Author:** Valentine Golden Ghanem | Ghana COCOBOD Cocoa Clinic, Accra, Ghana
**ORCID:** [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)
**Affiliation:** Ghana COCOBOD Cocoa Clinic, Accra, Ghana
**Reporting standard:** PRISMA 2020
**Date:** 2026
**Status:** Manuscript in preparation
**Pre-registration:** https://doi.org/10.17605/OSF.IO/53GBT

## 1. Abstract
This systematic review with meta-analysis pools 17 studies (N=4,318) measuring serum 25-hydroxyvitamin D [25(OH)D] in Ghanaian populations (database inception to March 2025). Weighted pooled vitamin D deficiency (VDD; 25(OH)D <20 ng/mL) prevalence was 58.3% (95% CI 47.2-69.4%; I2=97.8%). Severe maternal VDD was associated with preeclampsia in one case-control study (aOR=5.9, 95% CI 2.14-16.40), with a second case-control study reporting a smaller adjusted association (aOR=3.31, 95% CI 1.58-6.92). Spatial analysis found positive global autocorrelation (Moran's I=0.307, p=0.031) and nominal local high-prevalence Gi* signals in Ashanti (p=0.008) and Volta (p=0.026); neither local signal survives the OSF-specified Bonferroni threshold for 16 regions. Reflexive thematic analysis identified four determinant domains (socio-cultural, dietary, healthcare-system, environmental/policy). Six of Ghana's 16 administrative regions have no published VDD data.

## 2. Research Question & Aims
Estimate overall and subgroup-stratified VDD prevalence; characterise comorbidity burden and clinical associations; map geographic/spatial distribution across all 16 administrative regions; and synthesise socio-cultural and health-system determinants via reflexive thematic analysis.

## 3. Methods Summary
| Method | Tool | Purpose |
|---|---|---|
| Random-effects meta-analysis (inverse-variance) | metafor (R) | Pooled VDD prevalence and mean 25(OH)D |
| Meta-regression (backward elimination) | metafor (R) | Study-level predictors of prevalence |
| Global Moran's I / Getis-Ord Gi* | PySAL-style locked output | Spatial autocorrelation and local cluster exploration |
| CART sensitivity analysis (LOOCV) | scikit-learn | Exploratory study-level sensitivity check |
| Reflexive thematic analysis | Braun & Clarke (2021) | Qualitative determinant synthesis |
| Newcastle-Ottawa Scale + Cochrane RoB 2 | Manual | Risk-of-bias assessment (16 observational + 1 RCT) |

## 4. Data Sources
| Source | Variables | Year | Access |
|---|---|---|---|
| PubMed, Scopus, Web of Science, AJOL | Study-level 25(OH)D, VDD%, N, design, region, assay | Inception-March 2025 | Public (see `data/pubmed_all_40.csv`) |
| 17 included studies (Table 1) | Study-level extraction (`data/extracted_data.csv`) | 2014-2025 | Derived, this repository |

**Data availability:** The extracted study-level dataset, PRISMA materials, analysis scripts and reproducibility materials will be archived through Zenodo at `[ZENODO DOI/URL TO BE INSERTED AFTER RELEASE: https://zenodo.org/record/XXXXXXX]` and maintained in this GitHub repository at `[GITHUB REPOSITORY URL TO BE INSERTED/CONFIRMED: https://github.com/valentineghanem-bit/vitamin-d-ghana-review]`. The Zenodo DOI will be appended here after the GitHub release triggers the linked Zenodo integration.

## 5. Key Findings
| Metric | Value |
|---|---|
| Studies included (k) | 17 |
| Total participants (N) | 4,318 |
| Pooled VDD prevalence | 58.3% (95% CI 47.2-69.4%) |
| Weighted mean 25(OH)D | 18.4 ng/mL (95% CI 15.8-21.0) |
| Heterogeneity (I2) | 97.8% |
| Sensitivity: LC-MS/MS-only | 54.1% |
| Sensitivity: trim-and-fill adjusted | 54.7% (95% CI 46.1-63.3%) |
| Preeclampsia association | aOR=5.9 in Fondjo 2021; aOR=3.31 in Fondjo 2024 |
| Global Moran's I | 0.307 (p=0.031) |
| Local Gi* signals | Ashanti (Gi*=+2.41), Volta (Gi*=+1.97, nominal p<0.05; not Bonferroni-confirmed) |
| Meta-regression adjusted R2 | 38.7% |
| CART exploratory performance | 58.8% LOOCV accuracy (AUC 0.36; not retained as predictive evidence) |
| Regions with no published data | 6 of 16 |

## 6. Repository Structure
```
vitamin-d-ghana-review/
  README.md  CITATION.cff  LICENSE  requirements.txt
  .github/workflows/ci.yml
  data/            extracted_data.csv, pubmed_all_40.csv, canonical_values.csv
  outputs/data/    cart_results.json, spatial_results.json, data_dictionary.md
  scripts/         analysis_pipeline.py, decision_tree.py, meta_analysis.R, spatial_analysis.py
  dashboard/       vitamin_d_ghana_dashboard.html
  poster/          vitamin_d_ghana_poster.html
  tests/           test_analysis.py
```

## 7. Reproducibility
### 7.1 Requirements
Python 3.12, R 4.3+. See `requirements.txt`.
### 7.2 Clone & install
`git clone https://github.com/valentineghanem-bit/vitamin-d-ghana-review.git && cd vitamin-d-ghana-review && pip install -r requirements.txt`
### 7.3 Run the analytical pipeline
`python scripts/analysis_pipeline.py --all`
### 7.4 Run the test suite
`pytest tests/`
### 7.5 Launch the interactive Dash application
Not applicable. This project ships a static HTML dashboard, not a live Dash app.
### 7.6 Open the static HTML dashboard
Open `dashboard/vitamin_d_ghana_dashboard.html` directly in any browser.

## 8. Outputs
| Output | Description |
|---|---|
| `data/extracted_data.csv` | Canonical study-level dataset (k=17, N=4,318) |
| `data/cart_feature_matrix.csv` | Derived CART input matrix |
| `outputs/data/cart_results.json` | Reproducible CART sensitivity result |
| `outputs/data/spatial_results.json` | Locked spatial summary |
| `dashboard/vitamin_d_ghana_dashboard.html` | Interactive summary dashboard |
| `poster/vitamin_d_ghana_poster.html` | A0 conference poster |

## 8a. Downloadable Artefacts (HTML)
| Artefact | View on GitHub | Live preview | Direct download |
|---|---|---|---|
| Interactive dashboard | [View](https://github.com/valentineghanem-bit/vitamin-d-ghana-review/blob/main/dashboard/vitamin_d_ghana_dashboard.html) | [Preview](https://htmlpreview.github.io/?https://github.com/valentineghanem-bit/vitamin-d-ghana-review/blob/main/dashboard/vitamin_d_ghana_dashboard.html) | [Download](https://raw.githubusercontent.com/valentineghanem-bit/vitamin-d-ghana-review/main/dashboard/vitamin_d_ghana_dashboard.html) |
| Conference poster | [View](https://github.com/valentineghanem-bit/vitamin-d-ghana-review/blob/main/poster/vitamin_d_ghana_poster.html) | [Preview](https://htmlpreview.github.io/?https://github.com/valentineghanem-bit/vitamin-d-ghana-review/blob/main/poster/vitamin_d_ghana_poster.html) | [Download](https://raw.githubusercontent.com/valentineghanem-bit/vitamin-d-ghana-review/main/poster/vitamin_d_ghana_poster.html) |

## 9. Reporting Standard
PRISMA 2020 (systematic review with meta-analysis). Completed checklist is maintained in the manuscript submission folder, not in the public repository.

## 10. Ethical Statement
Secondary synthesis of previously published, de-identified aggregate data. No new human-participant data were collected; no separate ethics approval was required. All 17 primary studies reported their own ethics approval and informed consent per the Declaration of Helsinki.

## 11. Citation
Ghanem VG (2026). Vitamin D Status in Ghana: A Systematic Review with Meta-Analysis of Prevalence, Determinants, Comorbidity Burden, and Spatial Distribution. OSF Registration: https://doi.org/10.17605/OSF.IO/53GBT

```bibtex
@misc{ghanem2026vitamind,
  author = {Ghanem, Valentine Golden},
  title = {Vitamin D Status in Ghana: A Systematic Review with Meta-Analysis},
  year = {2026},
  howpublished = {OSF},
  doi = {10.17605/OSF.IO/53GBT}
}
```
See also `CITATION.cff`.

## 12. License
MIT (code) | CC BY 4.0 (derived non-code outputs)

## 13. Author & Contact
Valentine Golden Ghanem, MSc | Ghana COCOBOD Cocoa Clinic, Accra, Ghana | valentineghanem@gmail.com | [ORCID 0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)

## 14. Acknowledgements
The author thanks the authors of the 17 primary studies synthesised in this review.
