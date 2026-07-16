# Vitamin D Status in Ghana: A Systematic Review with Meta-Analysis of Prevalence, Determinants, Comorbidity Burden, and Spatial Distribution

[![CI](https://github.com/valentineghanem-bit/vitamin-d-ghana-review/actions/workflows/ci.yml/badge.svg)](https://github.com/valentineghanem-bit/vitamin-d-ghana-review/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/) [![R 4.3+](https://img.shields.io/badge/R-4.3+-blue.svg)](https://www.r-project.org/) [![ORCID](https://img.shields.io/badge/ORCID-0009--0002--8332--0220-green.svg)](https://orcid.org/0009-0002-8332-0220) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21393008.svg)](https://doi.org/10.5281/zenodo.21393008)

**Author:** Valentine Golden Ghanem | Ghana COCOBOD Cocoa Clinic, Accra, Ghana  
**ORCID:** [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)  
**Affiliation:** Ghana COCOBOD Cocoa Clinic, Accra, Ghana  
**Reporting standard:** PRISMA 2020  
**Date:** 2026  
**Status:** Manuscript under review; code/data release v1.0.4 published  
**Pre-registration:** https://doi.org/10.17605/OSF.IO/53GBT

## 1. Abstract
This repository supports a PRISMA 2020 systematic review with meta-analysis of vitamin D status in Ghana. The final evidence set includes 17 studies and 4,318 participants. Weighted pooled vitamin D deficiency prevalence was 58.3% (95% CI 47.2-69.4%; I2=97.8%). Weighted mean serum 25-hydroxyvitamin D was 18.4 ng/mL (95% CI 15.8-21.0). Two independent Ghanaian case-control studies reported adjusted associations between severe maternal vitamin D deficiency and preeclampsia (Volta: aOR=5.9, 95% CI 2.14-16.40; Ashanti: aOR=3.31, 95% CI 1.58-6.92), interpreted as low-certainty association evidence rather than a pooled causal estimate. Spatial analysis found positive global autocorrelation (Moran's I=0.307, p=0.031), while Ashanti and Volta showed nominal local Gi* signals only; neither local signal survived the Bonferroni threshold for 16 regions. Six of Ghana's 16 administrative regions had no region-specific published vitamin D deficiency data in the reviewed evidence base.

## 2. Research Question & Aims
The review asks how common vitamin D deficiency is in Ghanaian populations, which clinical and contextual factors are associated with deficiency, and where the evidence is geographically concentrated or absent.

The aims are to estimate pooled and subgroup-specific prevalence, summarise comorbidity associations, map regional evidence distribution, evaluate assay and study-level heterogeneity, and synthesise socio-cultural, dietary, health-system and environmental determinants.

## 3. Methods Summary
| Method | Tool | Purpose |
|---|---|---|
| Random-effects meta-analysis | R, metafor | Pool VDD prevalence and mean 25(OH)D |
| Meta-regression | R, metafor | Explore study-level predictors |
| Assay sensitivity analysis | R, metafor | Compare primary estimate with LC-MS/MS-only studies |
| Global Moran's I and Getis-Ord Gi* | Python locked spatial output | Explore regional spatial patterning |
| CART sensitivity analysis | Python, scikit-learn | Test whether study-level features support prediction |
| Reflexive thematic analysis | Braun and Clarke framework | Synthesise determinant domains |
| NOS and RoB 2 | Manual review | Assess observational studies and the single RCT |

## 4. Data Sources
| Source | Variables | Year | Access |
|---|---|---|---|
| PubMed, Scopus, Web of Science and AJOL searches | Citation screening and relevance flags | Database inception to March 2025 | `data/pubmed_all_40.csv` |
| Included Ghana studies | Study design, region, population, assay, N, 25(OH)D and VDD prevalence | 2014-2025 | `data/extracted_data.csv` |
| Derived regional summary | Regional N, k, VDD prevalence, CI and Gi* signal status | 2026 synthesis | `data/regional_aggregation.csv` |

**Data availability:** The extracted study-level dataset, analysis scripts, dashboard, poster and reproducibility outputs are maintained in this GitHub repository: [https://github.com/valentineghanem-bit/vitamin-d-ghana-review](https://github.com/valentineghanem-bit/vitamin-d-ghana-review). The corrected release v1.0.4 is permanently archived on Zenodo: [https://doi.org/10.5281/zenodo.21393008](https://doi.org/10.5281/zenodo.21393008).

## 5. Key Findings
| Metric | Value |
|---|---|
| Studies included | 17 |
| Total participants | 4,318 |
| Pooled VDD prevalence | 58.3% (95% CI 47.2-69.4%) |
| Weighted mean 25(OH)D | 18.4 ng/mL (95% CI 15.8-21.0) |
| Heterogeneity | I2=97.8%; Q=681.4, df=15 |
| LC-MS/MS-only sensitivity estimate | 54.1% |
| Trim-and-fill adjusted estimate | 54.7% (95% CI 46.1-63.3%) |
| Preeclampsia association | aOR=5.9 (95% CI 2.14-16.40) and aOR=3.31 (95% CI 1.58-6.92) |
| Global Moran's I | 0.307 (p=0.031) |
| Local Gi* interpretation | Ashanti and Volta were nominal local signals only; neither was Bonferroni-confirmed |
| Meta-regression adjusted R2 | 38.7% |
| CART sensitivity result | 58.8% LOOCV accuracy; AUC 0.36; not retained as predictive evidence |
| Regions with no region-specific VDD data | 6 of 16 |

## 6. Repository Structure
```text
vitamin-d-ghana-review/
|-- README.md
|-- CITATION.cff
|-- LICENSE
|-- requirements.txt
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|-- data/
|   |-- canonical_values.csv
|   |-- cart_feature_matrix.csv
|   |-- extracted_data.csv
|   |-- pubmed_all_40.csv
|   `-- regional_aggregation.csv
|-- outputs/
|   `-- data/
|       |-- cart_results.json
|       |-- data_dictionary.md
|       `-- spatial_results.json
|-- scripts/
|   |-- analysis_pipeline.py
|   |-- decision_tree.py
|   |-- meta_analysis.R
|   `-- spatial_analysis.py
|-- dashboard/
|   `-- vitamin_d_ghana_dashboard.html
|-- poster/
|   `-- vitamin_d_ghana_poster.html
`-- tests/
    `-- test_analysis.py
```

## 7. Reproducibility
### 7.1 Requirements
Python 3.12 and R 4.3 or later are recommended. Python dependencies are listed in `requirements.txt`.

### 7.2 Clone & install
```bash
git clone https://github.com/valentineghanem-bit/vitamin-d-ghana-review.git
cd vitamin-d-ghana-review
pip install -r requirements.txt
```

### 7.3 Run the analytical pipeline
```bash
python scripts/analysis_pipeline.py --all
```

### 7.4 Run the test suite
```bash
python -m pytest tests -q
```

### 7.5 Launch the interactive Dash application
Not applicable. The repository now ships an offline HI-EI static HTML dashboard rather than a live Dash application.

### 7.6 Open the static HTML dashboard
Open `dashboard/vitamin_d_ghana_dashboard.html` in any modern browser. No server is required.

## 8. Outputs
| Output | Description |
|---|---|
| `data/extracted_data.csv` | Canonical study-level extraction for 17 included studies |
| `data/canonical_values.csv` | Locked headline statistics used across the submission package |
| `data/regional_aggregation.csv` | Regional evidence summary and spatial signal interpretation |
| `outputs/data/cart_results.json` | Reproducible CART sensitivity result |
| `outputs/data/spatial_results.json` | Reproducible spatial summary |
| `dashboard/vitamin_d_ghana_dashboard.html` | Offline bespoke HI-EI dashboard |
| `poster/vitamin_d_ghana_poster.html` | Offline bespoke HI-EI poster |

## 8a. Downloadable Artefacts (HTML)
| Artefact | View on GitHub | Live preview | Direct download |
|---|---|---|---|
| Interactive dashboard | [View](https://github.com/valentineghanem-bit/vitamin-d-ghana-review/blob/main/dashboard/vitamin_d_ghana_dashboard.html) | [Preview](https://htmlpreview.github.io/?https://github.com/valentineghanem-bit/vitamin-d-ghana-review/blob/main/dashboard/vitamin_d_ghana_dashboard.html) | [Download](https://raw.githubusercontent.com/valentineghanem-bit/vitamin-d-ghana-review/main/dashboard/vitamin_d_ghana_dashboard.html) |
| Conference poster | [View](https://github.com/valentineghanem-bit/vitamin-d-ghana-review/blob/main/poster/vitamin_d_ghana_poster.html) | [Preview](https://htmlpreview.github.io/?https://github.com/valentineghanem-bit/vitamin-d-ghana-review/blob/main/poster/vitamin_d_ghana_poster.html) | [Download](https://raw.githubusercontent.com/valentineghanem-bit/vitamin-d-ghana-review/main/poster/vitamin_d_ghana_poster.html) |

## 9. Reporting Standard
The manuscript is reported under PRISMA 2020 for a systematic review with meta-analysis. The OSF record, manuscript, repository and release archive now use the same study descriptor, sample size and data-availability citation.

## 10. Ethical Statement
This repository contains secondary analysis of published aggregate data. No individual participant data were collected, accessed or requested. No new ethics approval was required for this evidence synthesis. The primary studies reported their own ethics approvals and consent procedures.

## 11. Citation
Ghanem VG (2026). Vitamin D Status in Ghana: A Systematic Review with Meta-Analysis of Prevalence, Determinants, Comorbidity Burden, and Spatial Distribution. OSF Registration: https://doi.org/10.17605/OSF.IO/53GBT

```bibtex
@misc{ghanem2026vitamindghana,
  author = {Ghanem, Valentine Golden},
  title = {Vitamin D Status in Ghana: A Systematic Review with Meta-Analysis of Prevalence, Determinants, Comorbidity Burden, and Spatial Distribution},
  year = {2026},
  howpublished = {OSF and GitHub repository},
  doi = {10.17605/OSF.IO/53GBT},
  url = {https://github.com/valentineghanem-bit/vitamin-d-ghana-review}
}
```

See `CITATION.cff` for machine-readable citation metadata.

## 12. License
Code is released under the MIT License. Derived non-code outputs are intended for scholarly reuse with attribution, subject to the citation requirements above.

## 13. Author & Contact
Valentine Golden Ghanem, MSc  
Ghana COCOBOD Cocoa Clinic, Accra, Ghana  
Email: valentineghanem@gmail.com  
ORCID: [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)

## 14. Acknowledgements
The author acknowledges the investigators of the 17 Ghanaian primary studies included in this review. Their published work made this synthesis possible.
