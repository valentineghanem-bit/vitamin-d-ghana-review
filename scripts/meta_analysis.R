# meta_analysis.R -- analysis wrapper.

suppressPackageStartupMessages({
  library(meta)
})

csv_path <- "data/extracted_data.csv"
if (!file.exists(csv_path)) {
  stop("Missing data/extracted_data.csv; run from repository root.")
}

dat <- read.csv(csv_path, stringsAsFactors = FALSE)

required <- c("first_author_year", "analysis_n_vdd", "vdd_events",
              "vdd_prevalence_pct", "analysis_n_mean",
              "mean_25ohd_ngml", "sd_25ohd")
missing <- setdiff(required, names(dat))
if (length(missing) > 0) {
  stop(sprintf("Missing required columns: %s", paste(missing, collapse = ", ")))
}

dat_prev <- dat[!is.na(dat$analysis_n_vdd) & !is.na(dat$vdd_prevalence_pct), ]
cat(sprintf("VDD model rows: %d; analytic N = %s\n",
            nrow(dat_prev), format(sum(dat_prev$analysis_n_vdd), big.mark = ",")))

prev_model <- metaprop(
  event = dat_prev$vdd_events,
  n = dat_prev$analysis_n_vdd,
  studlab = dat_prev$first_author_year,
  sm = "PLOGIT",
  method.tau = "DL",
  random = TRUE,
  fixed = FALSE
)

cat(sprintf("Pooled VDD prevalence: %.1f%% (95%% CI %.1f-%.1f); I2 = %.1f%%\n",
            plogis(prev_model$TE.random) * 100,
            plogis(prev_model$lower.random) * 100,
            plogis(prev_model$upper.random) * 100,
            prev_model$I2 * 100))

dat_mean <- dat[!is.na(dat$analysis_n_mean) & !is.na(dat$mean_25ohd_ngml) & !is.na(dat$sd_25ohd), ]
cat(sprintf("Mean model rows with SD: %d; analytic N = %s\n",
            nrow(dat_mean), format(sum(dat_mean$analysis_n_mean), big.mark = ",")))

mean_model <- metamean(
  n = dat_mean$analysis_n_mean,
  mean = dat_mean$mean_25ohd_ngml,
  sd = dat_mean$sd_25ohd,
  studlab = dat_mean$first_author_year,
  sm = "MRAW",
  method.tau = "DL",
  random = TRUE,
  fixed = FALSE
)

cat(sprintf("Pooled mean 25(OH)D: %.1f ng/mL (95%% CI %.1f-%.1f); I2 = %.1f%%\n",
            mean_model$TE.random, mean_model$lower.random,
            mean_model$upper.random, mean_model$I2 * 100))
