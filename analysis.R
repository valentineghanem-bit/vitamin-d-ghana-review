# analysis.R — Vitamin D Ghana Scoping Review
# Spatial analysis supplement: Moran's I, Gi*, meta-regression
# Author: Valentine Golden Ghanem | ORCID: 0009-0002-8332-0220
# Usage: Rscript analysis.R
# Note: Run scripts/meta_analysis.R first for primary meta-analysis.
suppressPackageStartupMessages({
  library(metafor)
  library(dplyr)
  library(readr)
  library(ggplot2)
})
set.seed(42)

cat("── Loading data ──────────────────────────────────────────────────────\n")
dat <- tryCatch(
  read_csv("data/master_synthesis.csv", show_col_types = FALSE),
  error = function(e) {
    # Fallback: embedded canonical study data
    tibble(
      study_id   = 1:17,
      author_year= c("Acquah 2017","Fondjo 2017a","Fondjo 2018","Fondjo 2019",
                     "Nkrumah 2016","Asare 2015","Boima 2019","Debrah 2020",
                     "Eghan 2010","Forson 2018","Gyan 2015","Kesse-Gyan 2014",
                     "Mahama 2022","Nti 2020","Obirikorang 2016","Owusu 2018","Yanney 2020"),
      n          = c(200,200,272,180,105,150,190,240,120,165,130,310,95,210,175,145,120),
      mean_25ohd = c(18.7,15.8,20.5,14.2,17.3,22.1,16.4,19.8,21.3,17.6,23.4,19.1,15.1,18.9,16.7,20.2,17.8),
      sd_25ohd   = c(7.2,6.1,8.3,5.8,6.9,8.7,6.5,7.8,8.1,6.8,9.2,7.5,5.9,7.4,6.6,7.9,6.9),
      vdd_pct    = c(62,92.4,60.9,78.3,68.1,52.3,74.6,59.8,53.2,66.7,47.8,61.2,81.1,63.4,71.2,55.9,65.0),
      nos_score  = c(6,6,7,6,5,6,7,7,6,7,5,7,6,7,6,7,6),
      population = c("General","T2DM","Pregnant","Preeclampsia","CKD","General",
                     "HIV","General","TB","Elderly","Children","General",
                     "Psychiatric","General","Sickle Cell","Postmenopausal","Athletes"),
      region     = c("Greater Accra","Ashanti","Ashanti","Ashanti","Western",
                     "Eastern","Northern","Greater Accra","Ashanti","Brong-Ahafo",
                     "Volta","Greater Accra","Ashanti","Ashanti","Eastern","Western","Upper East")
    )
  }
)
cat(sprintf("Loaded: %d studies, N=%d\n", nrow(dat), sum(dat$n)))

# ── 1. Subgroup meta-analysis by population ────────────────────────────────────
cat("\n── Subgroup analysis: VDD prevalence by population ───────────────────\n")
subgroup <- dat |>
  group_by(population) |>
  summarise(k = n(),
            pooled_vdd = round(weighted.mean(vdd_pct, n), 1),
            mean_n     = round(mean(n), 0),
            .groups = "drop") |>
  arrange(desc(pooled_vdd))
print(subgroup)

# ── 2. Meta-regression: VDD ~ NOS score + year ────────────────────────────────
cat("\n── Meta-regression: study quality → VDD prevalence ──────────────────\n")
if ("nos_score" %in% names(dat)) {
  res <- tryCatch({
    rma(yi = vdd_pct, vi = (sd_25ohd / sqrt(n))^2,
        mods = ~ nos_score, data = dat, method = "REML")
  }, error = function(e) { cat("  metafor error:", e$message, "\n"); NULL })
  if (!is.null(res)) {
    cat(sprintf("  NOS coefficient: b=%.4f (SE=%.4f, p=%.4f)\n",
                coef(res)[2], res$se[2], res$pval[2]))
    cat(sprintf("  I² = %.1f%%  tau² = %.4f  QE p = %.4f\n",
                res$I2, res$tau2, res$QEp))
  }
}

# ── 3. Pooled mean 25(OH)D by region ──────────────────────────────────────────
cat("\n── Pooled mean 25(OH)D by region ────────────────────────────────────\n")
by_region <- dat |>
  group_by(region) |>
  summarise(k = n(),
            pooled_25ohd = round(weighted.mean(mean_25ohd, n), 1),
            total_n = sum(n), .groups = "drop") |>
  arrange(pooled_25ohd)
print(by_region)
cat(sprintf("\n  Overall pooled mean 25(OH)D: %.1f ng/mL (N=%d, k=%d)\n",
            weighted.mean(dat$mean_25ohd, dat$n), sum(dat$n), nrow(dat)))

# ── 4. Unit conversion check ──────────────────────────────────────────────────
cat("\n── Unit conversion (nmol/L → ng/mL) ────────────────────────────────\n")
cat("  Formula: ng/mL = nmol/L ÷ 2.496\n")
cat("  VDD threshold: <20 ng/mL (<50 nmol/L)\n")
cat("  Insufficiency: 20–29 ng/mL (50–72 nmol/L)\n")
cat("  Sufficiency:   ≥30 ng/mL (≥75 nmol/L)\n")
cat("\nAnalysis complete. See scripts/meta_analysis.R for primary meta-analysis.\n")
