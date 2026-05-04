# Data Dictionary — extracted_data.csv
**Study:** Vitamin D Status in Ghana: A Mixed-Methods Narrative Review 
**Author:** Valentine Golden Ghanem | OSF: 10.17605/OSF.IO/53GBT 
**Rows:** 17 (one per included study) | **N total:** 10,445

## Variable Definitions

| Column | Type | Units | Description | ICD-10 |
|--------|------|-------|-------------|--------|
| Study_ID | Integer | — | Sequential identifier 1–17 | — |
| Author_Year | String | — | First author surname + year | — |
| Region | String | — | Ghana region of study site | — |
| Region_numeric | Integer | — | 1=Ashanti, 2=Gr.Accra, 3=Eastern, 4=Western, 5=Brong-Ahafo, 6=Northern, 7=Volta, 8=Upper East, 9=Upper West, 10=Central | — |
| Design | String | — | CS=cross-sectional, CC=case-control, Cohort, RCT | — |
| Population_Category | String | — | Study population type | — |
| Population_Category_numeric | Integer | — | 1=General, 2=Pregnant, 3=T2DM, 4=RA, 5=CLD, 6=Preeclampsia, 7=BPH, 8=Psychiatric, 9=Men | — |
| N | Integer | participants | Total sample size | — |
| Mean_25OHD | Float | ng/mL | Mean serum 25-hydroxyvitamin D; harmonised from nmol/L ÷ 2.496 | E55.9 |
| SD | Float | ng/mL | Standard deviation of Mean_25OHD | E55.9 |
| VDD_Prevalence | Float | % | Proportion with 25(OH)D <20 ng/mL (<50 nmol/L) | E55.9 |
| Assay | String | — | ELISA / CLIA / LC-MS/MS | — |
| Assay_numeric | Integer | — | 1=ELISA, 2=CLIA, 3=LC-MS/MS | — |
| NOS_Score | Integer | 0–9 | Newcastle-Ottawa Scale quality score | — |
| Publication_Year | Integer | year | 4-digit year | — |
| Latitude | Float | decimal degrees | Study site centroid (WGS84) | — |
| Longitude | Float | decimal degrees | Study site centroid (WGS84) | — |
| Prop_Female | Float | % | Proportion female in sample | — |
| Mean_Age | Float | years | Mean participant age | — |
| High_VDD | Integer | binary | 1 if VDD_Prevalence >70%; 0 otherwise | E55.9 |
| DOI | String | — | Full https:// DOI URL | — |

## Missing Value Encoding
- All missing values encoded as `NA`
- No blanks, no zeros used as missing-value proxies
- Mean_25OHD and SD are `NA` for Ayamah 2025 [17] (prevalence-only study)

## Unit Conversion
Studies originally reporting in nmol/L were converted: **ng/mL = nmol/L ÷ 2.496** 
Affected studies: Fondjo 2017 [2] (cases: 2.45 nmol/L → 0.98 ng/mL — extreme outlier, handled in sensitivity), Dzudzor 2023 [9] (62.4 nmol/L → 25.0 ng/mL). 
Final harmonised values are those reported in manuscript Table 1.

## Population Category ICD-10 Codes
- General population: Healthy adults (no specific ICD-10)
- T2DM: E11 (Type 2 diabetes mellitus)
- RA: M05–M06 (Rheumatoid arthritis)
- CLD: K72–K74 (Chronic liver disease / cirrhosis)
- Preeclampsia: O14 (Pre-existing hypertension complicating pregnancy)
- BPH: N40 (Benign prostatic hyperplasia)
- Psychiatric: F20–F48 (Schizophrenia spectrum, mood, anxiety disorders)
- VDD (outcome): E55.9 (Vitamin D deficiency, unspecified)
