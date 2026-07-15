# meta_analysis.R -- canonical analysis wrapper for the Vitamin D Ghana review.
# Reads only data/extracted_data.csv. No embedded fallback datasets are allowed.

suppressPackageStartupMessages({
  library(meta)
  library(metafor)
})

csv_path <- "data/extracted_data.csv"
if (!file.exists(csv_path)) {
  stop("Missing data/extracted_data.csv; run from repository root.")
}

dat <- read.csv(csv_path, stringsAsFactors = FALSE)
names(dat) <- tolower(names(dat))

required <- c("ref_id", "first_author_year", "region", "design", "population",
              "n", "mean_25ohd_ngml", "sd_25ohd", "vdd_prevalence_pct",
              "assay_method", "quality_assessment")
missing <- setdiff(required, names(dat))
if (length(missing) > 0) {
  stop(sprintf("Missing required columns: %s", paste(missing, collapse = ", ")))
}

cat(sprintf("Loaded %d studies; total N = %s\n",
            nrow(dat), format(sum(dat$n), big.mark = ",")))

dat_prev <- dat[!is.na(dat$vdd_prevalence_pct), ]
events <- round(dat_prev$vdd_prevalence_pct * dat_prev$n / 100)

prev_model <- metaprop(
  event = events,
  n = dat_prev$n,
  studlab = dat_prev$first_author_year,
  sm = "PLOGIT",
  method.tau = "PM",
  random = TRUE,
  fixed = FALSE,
  hakn = TRUE
)

pooled_prev <- plogis(prev_model$TE.random) * 100
prev_low <- plogis(prev_model$lower.random) * 100
prev_high <- plogis(prev_model$upper.random) * 100

cat(sprintf("Pooled VDD prevalence: %.1f%% (95%% CI %.1f-%.1f); I2 = %.1f%%\n",
            pooled_prev, prev_low, prev_high, prev_model$I2 * 100))

dat_mean <- dat[!is.na(dat$mean_25ohd_ngml) & !is.na(dat$sd_25ohd), ]
mean_model <- metamean(
  n = dat_mean$n,
  mean = dat_mean$mean_25ohd_ngml,
  sd = dat_mean$sd_25ohd,
  studlab = dat_mean$first_author_year,
  sm = "MRAW",
  method.tau = "REML",
  random = TRUE,
  fixed = FALSE,
  hakn = TRUE
)

cat(sprintf("Pooled mean 25(OH)D: %.1f ng/mL (95%% CI %.1f-%.1f); I2 = %.1f%%\n",
            mean_model$TE.random, mean_model$lower.random,
            mean_model$upper.random, mean_model$I2 * 100))

egger <- metabias(mean_model, method.bias = "linreg")
cat(sprintf("Egger test p = %.3f\n", egger$p.value))

cat("Assay counts:\n")
print(table(dat$assay_method))
