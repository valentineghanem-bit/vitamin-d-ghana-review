# Vitamin D Status in Ghana: A Systematic Review with Meta-Analysis of Prevalence, Comorbidity Signals, and Evidence Gaps

[![CI](https://github.com/valentineghanem-bit/vitamin-d-ghana-review/actions/workflows/ci.yml/badge.svg)](https://github.com/valentineghanem-bit/vitamin-d-ghana-review/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/) [![R 4.3+](https://img.shields.io/badge/R-4.3+-blue.svg)](https://www.r-project.org/) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21400878.svg)](https://doi.org/10.5281/zenodo.21400878)

**Author:** Valentine Golden Ghanem  
**Affiliation:** Ghana COCOBOD Cocoa Clinic, Accra, Ghana  
**ORCID:** [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)  
**Reporting standard:** PRISMA 2020  
**OSF registration:** https://doi.org/10.17605/OSF.IO/53GBT  
**Release:** v1.1.0

## 1. What This Repository Contains
This repository supports a PRISMA 2020 systematic review with meta-analysis of vitamin D status in Ghana. The review includes 17 eligible peer-reviewed studies. VDD prevalence could be extracted from 9 independent analytic rows comprising 1,609 participants. Seven rows comprising 1,153 participants contributed descriptive mean 25(OH)D data.

The random-effects pooled VDD prevalence is **55.3%** (95% CI 35.5-75.2; I2=99.0%). The mean 25(OH)D estimate is **25.1 ng/mL** (95% CI 12.7-37.5) among rows with usable mean data.

## 2. Quantitative Synthesis Rules
The quantitative synthesis follows prespecified compatibility rules:

- Asare 2017 reports vitamin D mean values but no VDD prevalence.
- Sakyi 2022 reports RA/control 25VD means with a printed pg/mL unit and no VDD prevalence.
- Dzudzor 2023 reports chronic liver disease vitamin D as median/IQR and no VDD prevalence.
- Fondjo 2022 is treated as a median/IQR psychiatric-patient study with treatment-active VDD prevalence, not as a mean/SD row.
- Fondjo 2018 VDD prevalence is retained, but its 25(OH)D mean is converted from the source's nmol/L table rather than treated as ng/mL.

The repository therefore reports pooled estimates only where a compatible denominator, outcome definition and independent analytic row were available. Formal spatial-cluster inference and prediction modelling are outside the inferential scope of this evidence base.

## 3. Key Findings
| Metric | Value |
|---|---|
| Eligible studies | 17 |
| Eligible VDD prevalence rows | 9 |
| VDD prevalence analytic N | 1,609 |
| Random-effects VDD prevalence | 55.3% (95% CI 35.5-75.2) |
| VDD heterogeneity | I2=99.0%; Q=788.4, df=8 |
| Mean 25(OH)D rows | 7 descriptive rows; 5 model rows with SD |
| Random-effects mean 25(OH)D | 25.1 ng/mL (95% CI 12.7-37.5) |
| Preeclampsia association | Volta aOR=5.9; Ashanti aOR=3.31 |
| Mapped region-specific VDD evidence | 4 of 16 administrative regions |
| Regions without region-specific VDD prevalence data | 12 of 16 |
| Spatial inference | Evidence-coverage mapping only |

## 4. Repository Structure
```text
vitamin-d-ghana-review/
|-- README.md
|-- CITATION.cff
|-- LICENSE
|-- requirements.txt
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

## 5. Reproducibility
```bash
git clone https://github.com/valentineghanem-bit/vitamin-d-ghana-review.git
cd vitamin-d-ghana-review
pip install -r requirements.txt
python -m pytest tests -q
```

The dashboard and poster are offline HI-EI HTML artifacts. Open them directly in a browser:

- `dashboard/vitamin_d_ghana_dashboard.html`
- `poster/vitamin_d_ghana_poster.html`

## 6. Data Availability
The extraction dataset, scripts, dashboard, poster and reproducibility outputs are maintained in this GitHub repository and permanently archived on Zenodo:

- GitHub: [https://github.com/valentineghanem-bit/vitamin-d-ghana-review](https://github.com/valentineghanem-bit/vitamin-d-ghana-review)
- Zenodo (version of record, v1.1.0): [https://doi.org/10.5281/zenodo.21400878](https://doi.org/10.5281/zenodo.21400878)
- Zenodo (concept DOI, always resolves to the latest version): [https://doi.org/10.5281/zenodo.21383063](https://doi.org/10.5281/zenodo.21383063)

## 7. Citation
Ghanem VG (2026). Vitamin D Status in Ghana: A Systematic Review with Meta-Analysis of Prevalence, Comorbidity Signals, and Evidence Gaps. OSF registration: https://doi.org/10.17605/OSF.IO/53GBT. Zenodo: https://doi.org/10.5281/zenodo.21400878.

```bibtex
@misc{ghanem2026vitamindghana,
  author = {Ghanem, Valentine Golden},
  title = {Vitamin D Status in Ghana: A Systematic Review with Meta-Analysis of Prevalence, Comorbidity Signals, and Evidence Gaps},
  year = {2026},
  doi = {10.5281/zenodo.21400878},
  url = {https://github.com/valentineghanem-bit/vitamin-d-ghana-review}
}
```

## 8. License
Code is released under the MIT License. Scholarly outputs should be cited using the citation above.
