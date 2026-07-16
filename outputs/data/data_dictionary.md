# Data Dictionary

This repository contains the extraction and summary files supporting the PRISMA 2020 systematic review of vitamin D status in Ghana.

## Canonical Summary

File: `data/canonical_values.csv`

| Field | Meaning |
|---|---|
| Included papers (k) | Number of eligible peer-reviewed papers in the review |
| Prevalence analytic rows (k) | Number of independent analytic rows used in the VDD prevalence meta-analysis |
| Prevalence analytic N | Total participants contributing to VDD prevalence synthesis |
| Mean 25(OH)D analytic rows (k) | Rows contributing descriptive mean 25(OH)D data |
| Mean 25(OH)D analytic N | Participants contributing descriptive mean 25(OH)D data |
| Random-effects VDD prevalence (%) | Pooled VDD prevalence estimate |
| VDD 95% CI low / high | Lower and upper 95% confidence limits |
| VDD I2 (%) | Heterogeneity statistic |
| Random-effects mean 25(OH)D (ng/mL) | Pooled mean among rows with usable SDs |
| Preeclampsia aOR Volta / Ashanti | Separate Ghanaian case-control association estimates |
| Region-specific VDD mapped regions (k) | Administrative regions with region-specific VDD prevalence data |
| Regions without region-specific VDD prevalence data | Administrative regions without region-specific VDD prevalence data |
| Spatial-cluster inference retained | Whether formal spatial-cluster inference is retained |

## Extracted Study Data

File: `data/extracted_data.csv`

| Column | Type | Unit | Description |
|---|---|---|---|
| `ref_id` | Integer | none | Internal row identifier |
| `first_author_year` | String | none | Study label |
| `region` | String | none | Ghana region or multi-region category |
| `design` | String | none | Study design |
| `population` | String | none | Population or analytic group |
| `paper_n` | Integer | participants | Study-level participant count reported for the paper or analytic sample |
| `analysis_n_vdd` | Integer | participants | Denominator used for VDD prevalence synthesis. Blank means no compatible VDD prevalence row. |
| `analysis_n_mean` | Integer | participants | Denominator used for descriptive mean 25(OH)D synthesis. Blank means no usable mean row. |
| `mean_25ohd_ngml` | Float | ng/mL | Mean 25(OH)D value after unit harmonisation where applicable |
| `sd_25ohd` | Float | ng/mL | Standard deviation used for mean modelling where available |
| `mean_statistic_type` | String | none | How the vitamin D statistic was reported or derived |
| `vdd_prevalence_pct` | Float | percent | Prevalence of VDD, generally 25(OH)D <20 ng/mL or <50 nmol/L when compatible |
| `vdd_events` | Integer | participants | Number of participants with VDD |
| `assay_method` | String | none | Reported vitamin D assay method |
| `quality_assessment` | String | none | NOS or RoB 2 summary |
| `cohort_id` | String | none | Cohort grouping used to avoid over-counting overlapping samples |
| `analysis_role` | String | none | How the row contributes to synthesis |
| `extraction_status` | String | none | Eligibility status for quantitative synthesis |
| `extraction_note` | String | none | Reason for inclusion or exclusion from specific pooled estimates |

## Key Compatibility Notes

- Asare 2017 reports vitamin D mean values but no VDD prevalence.
- Sakyi 2022 reports RA/control 25VD means with a printed pg/mL unit and no VDD prevalence.
- Dzudzor 2023 reports vitamin D as median/IQR values and no VDD prevalence.
- Fondjo 2022 contributes treatment-active psychiatric-patient VDD prevalence but not a mean/SD row.
- Median/IQR rows are not treated as mean/SD rows.
- Multi-region donor data are not assigned to a single administrative region.

## Regional Aggregation

File: `data/regional_aggregation.csv`

This file is an evidence-coverage table. It is not a spatial-autocorrelation result. Only Ashanti, Volta, Eastern and Western North have region-specific VDD prevalence data.

## CART and Spatial Status Outputs

Files:

- `outputs/data/cart_results.json`
- `outputs/data/spatial_results.json`

These files preserve reproducibility status only. Predictive performance claims and formal spatial-cluster interpretation are not retained because the compatible evidence layer is too sparse.
