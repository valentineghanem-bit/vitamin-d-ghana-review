# Data Dictionary - extracted_data.csv
**Study:** Vitamin D Status in Ghana: A Systematic Review with Meta-Analysis  
**Author:** Valentine Golden Ghanem | OSF: 10.17605/OSF.IO/53GBT  
**Rows:** 17 studies | **N total:** 4,318

## Variable Definitions

| Column | Type | Units | Description | ICD-10 |
|--------|------|-------|-------------|--------|
| ref_id | Integer | - | Sequential identifier 1-17 | - |
| first_author_year | String | - | First author surname and publication year | - |
| region | String | - | Ghana region or multi-region category | - |
| design | String | - | Cross-sectional, case-control, observational or RCT | - |
| population | String | - | Study population type | - |
| n | Integer | participants | Total study sample size | - |
| mean_25ohd_ngml | Float | ng/mL | Mean serum 25-hydroxyvitamin D; missing where not reported | E55.9 |
| sd_25ohd | Float | ng/mL | Standard deviation of mean_25ohd_ngml; missing where not reported | E55.9 |
| vdd_prevalence_pct | Float | % | Proportion with 25(OH)D <20 ng/mL (<50 nmol/L) | E55.9 |
| assay_method | String | - | ELISA or LC-MS/MS | - |
| quality_assessment | String | - | NOS or RoB 2 summary judgement | - |

## Missing Value Encoding
- Blank cells indicate values not reported in the source article.
- `mean_25ohd_ngml` and `sd_25ohd` are blank for Ayamah 2025 [17], which reported baseline VDD prevalence but not baseline mean 25(OH)D.

## Locked Summary Values
- Total studies: 17
- Total participants: 4,318
- Studies reporting baseline mean 25(OH)D: 16
- Pooled VDD prevalence: 58.3% (95% CI 47.2-69.4)
- Weighted mean 25(OH)D: 18.4 ng/mL (95% CI 15.8-21.0)
- Global Moran's I: 0.307 (p=0.031)
- CART sensitivity result: LOOCV accuracy 58.8%; AUC 0.357 (reported as 0.36 when rounded)

## Population ICD-10 Mapping
- T2DM: E11
- RA: M05-M06
- CLD: K72-K74
- Preeclampsia: O14
- BPH: N40
- Psychiatric disorders: F20-F48
- VDD outcome: E55.9
