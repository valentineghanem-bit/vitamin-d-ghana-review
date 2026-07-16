# analysis.R - corrected Vitamin D Ghana review wrapper.

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
  "ref_id", "first_author_year", "region", "design", "population", "paper_n",
  "analysis_n_vdd", "analysis_n_mean", "mean_25ohd_ngml", "sd_25ohd",
  "vdd_prevalence_pct", "vdd_events", "assay_method", "quality_assessment",
  "analysis_role", "extraction_status"
)
missing <- setdiff(required, names(dat))
if (length(missing) > 0) {
  stop(sprintf("Missing required columns: %s", paste(missing, collapse = ", ")))
}

paper_n <- sum(dat$paper_n, na.rm = TRUE)
prev <- dat |> filter(!is.na(analysis_n_vdd), !is.na(vdd_prevalence_pct))
mean_rows <- dat |> filter(!is.na(analysis_n_mean), !is.na(mean_25ohd_ngml))

cat(sprintf("Eligible papers: %d; review-level paper N = %s\n",
            nrow(dat), format(paper_n, big.mark = ",")))
cat(sprintf("Eligible VDD rows: %d; analytic N = %s\n",
            nrow(prev), format(sum(prev$analysis_n_vdd), big.mark = ",")))
cat(sprintf("Descriptive mean 25(OH)D rows: %d; analytic N = %s\n\n",
            nrow(mean_rows), format(sum(mean_rows$analysis_n_mean), big.mark = ",")))

if (nrow(dat) != 17 || paper_n != 4316 || nrow(prev) != 9 || sum(prev$analysis_n_vdd) != 1609) {
  stop("Dataset integrity check failed against corrected extraction values.")
}

subgroup <- prev |>
  group_by(population) |>
  summarise(
    k = n(),
    analytic_n = sum(analysis_n_vdd),
    events = sum(vdd_events),
    event_weighted_vdd_pct = round(events / analytic_n * 100, 1),
    .groups = "drop"
  ) |>
  arrange(desc(event_weighted_vdd_pct))

cat("VDD prevalence by verified population row\n")
print(subgroup)

regional <- read_csv("data/regional_aggregation.csv", show_col_types = FALSE)
cat("\nRegional evidence coverage\n")
print(regional |> select(region, k, n, vdd_prevalence_pct, classification))

cat("\nSpatial autocorrelation and CART prediction claims are withdrawn in the corrected package.\n")
