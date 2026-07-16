# analysis.R - Vitamin D Ghana systematic review with meta-analysis.
# Repository-level analysis wrapper. Reads only the canonical extracted dataset.

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

csv_path <- "data/extracted_data.csv"
if (!file.exists(csv_path)) {
  stop("Missing data/extracted_data.csv; run this script from the repository root.")
}

dat <- read_csv(csv_path, show_col_types = FALSE)
required <- c(
  "ref_id", "first_author_year", "region", "design", "population", "n",
  "mean_25ohd_ngml", "sd_25ohd", "vdd_prevalence_pct", "assay_method",
  "quality_assessment"
)
missing <- setdiff(required, names(dat))
if (length(missing) > 0) {
  stop(sprintf("Missing required columns: %s", paste(missing, collapse = ", ")))
}

cat(sprintf("Loaded %d studies; total N = %s\n",
            nrow(dat), format(sum(dat$n), big.mark = ",")))

if (nrow(dat) != 17 || sum(dat$n) != 4318) {
  stop("Dataset integrity check failed: expected k=17 and N=4,318.")
}

subgroup <- dat |>
  filter(!is.na(vdd_prevalence_pct)) |>
  group_by(population) |>
  summarise(
    k = n(),
    n = sum(n),
    weighted_vdd_pct = round(weighted.mean(vdd_prevalence_pct, n), 1),
    weighted_mean_25ohd = round(weighted.mean(mean_25ohd_ngml, n, na.rm = TRUE), 1),
    .groups = "drop"
  ) |>
  arrange(desc(weighted_vdd_pct))

cat("\nVDD prevalence by population subgroup\n")
print(subgroup)

by_region <- dat |>
  group_by(region) |>
  summarise(
    k = n(),
    n = sum(n),
    weighted_vdd_pct = round(weighted.mean(vdd_prevalence_pct, n, na.rm = TRUE), 1),
    weighted_mean_25ohd = round(weighted.mean(mean_25ohd_ngml, n, na.rm = TRUE), 1),
    .groups = "drop"
  ) |>
  arrange(desc(weighted_vdd_pct))

cat("\nRegional evidence summary\n")
print(by_region)

cat("\nUnit conversion check\n")
cat("Formula: ng/mL = nmol/L / 2.496\n")
cat("VDD threshold: <20 ng/mL (<50 nmol/L)\n")
cat("Insufficiency: 20-29 ng/mL (50-72 nmol/L)\n")
cat("Sufficiency: >=30 ng/mL (>=75 nmol/L)\n")
cat("\nAnalysis wrapper complete. Use scripts/meta_analysis.R for the primary meta-analysis.\n")
