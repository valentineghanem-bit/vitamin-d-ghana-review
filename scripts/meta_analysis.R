# ============================================================
# meta_analysis.R — Vitamin D Ghana Scoping Review
# Author: Valentine Golden Ghanem | ORCID: 0009-0002-8332-0220
# Date: April 2026
# Description: Random-effects meta-analysis, heterogeneity, meta-regression,
#              funnel plot with trim-and-fill, sensitivity analysis
# Packages: meta (>=6.5), metafor (>=4.4)
# Usage: Rscript scripts/meta_analysis.R
# ============================================================

suppressPackageStartupMessages({
  library(meta)
  library(metafor)
})

set.seed(42)

# ── 1. Load data ─────────────────────────────────────────────────────────────
cat("Loading data...\n")
dat <- tryCatch(
  read.csv("data/extracted_data.csv", stringsAsFactors = FALSE),
  error = function(e) {
    message("CSV not found — using embedded canonical data")
    data.frame(
      Study_ID = 1:17,
      Author_Year = c("Acquah 2017","Fondjo 2017a","Fondjo 2018","Fondjo 2019",
                      "Fondjo 2020","Fondjo 2021","Fondjo 2022","Fondjo 2023",
                      "Dzudzor 2023","Oppong 2022","Asante 2021","Acheampong 2020",
                      "Boachie 2021","Amponsah 2022","Kesse-Gyan 2023",
                      "Mensah 2024","Ayamah 2025"),
      N = c(200,200,272,180,170,300,185,210,450,500,1200,800,620,380,550,680,1748),
      Mean_25OHD = c(18.7,15.8,20.5,14.2,13.9,14.6,16.3,17.1,14.1,19.8,
                     21.4,22.3,17.8,20.9,16.9,23.1,NA),
      SD = c(7.2,6.1,8.3,5.8,5.1,5.9,6.4,6.8,5.4,8.1,9.2,9.8,7.3,8.6,6.7,10.2,NA),
      VDD_Prevalence = c(62.0,92.4,60.9,78.3,74.1,81.7,67.6,63.8,85.3,54.2,
                         47.3,44.8,65.2,52.6,71.3,41.5,88.1),
      Population_Category = c("General","T2DM","Pregnant","Preeclampsia","RA","General",
                               "CLD","BPH","Psychiatric","General","General","General",
                               "General","Pregnant","T2DM","General","General"),
      Population_Category_numeric = c(1,3,2,6,4,1,5,7,8,1,1,1,1,2,3,1,1),
      Assay = c("ELISA","ELISA","ELISA","ELISA","ELISA","ELISA","ELISA","ELISA",
                "CLIA","CLIA","CLIA","CLIA","ELISA","ELISA","LC-MS/MS","CLIA","ELISA"),
      Assay_numeric = c(1,1,1,1,1,1,1,1,2,2,2,2,1,1,3,2,1),
      NOS_Score = c(6,6,7,6,6,7,6,6,7,6,7,6,5,6,8,7,7),
      Publication_Year = c(2017,2017,2018,2019,2020,2021,2022,2023,2023,
                           2022,2021,2020,2021,2022,2023,2024,2025),
      Region_numeric = c(2,1,1,1,1,1,1,1,2,2,3,4,6,5,2,7,1)
    )
  }
)

cat(sprintf("Loaded %d studies (Total N = %s)\n", nrow(dat), format(sum(dat$N), big.mark=",")))

# ── 2. Random-effects meta-analysis — mean 25(OH)D ───────────────────────────
cat("\n--- Meta-Analysis: Mean Serum 25(OH)D ---\n")
dat_mean <- dat[\!is.na(dat$Mean_25OHD) & \!is.na(dat$SD), ]
cat(sprintf("Studies with mean+SD: %d\n", nrow(dat_mean)))

m1 <- metacont(
  n.e     = dat_mean$N,
  mean.e  = dat_mean$Mean_25OHD,
  sd.e    = dat_mean$SD,
  studlab = dat_mean$Author_Year,
  sm      = "MD",
  random  = TRUE,
  fixed   = FALSE,
  method.tau = "REML",
  hakn    = TRUE
)

cat(sprintf("Pooled mean 25(OH)D: %.1f ng/mL (95%% CI: %.1f-%.1f)\n",
            m1$TE.random, m1$lower.random, m1$upper.random))
cat(sprintf("I² = %.1f%% | Q = %.1f, df = %d, p = %.4f\n",
            m1$I2 * 100, m1$Q, m1$df.Q, m1$pval.Q))
cat(sprintf("tau² = %.4f | tau = %.4f\n", m1$tau^2, m1$tau))

# ── 3. VDD prevalence meta-analysis ──────────────────────────────────────────
cat("\n--- Meta-Analysis: VDD Prevalence ---\n")
dat_prev <- dat[\!is.na(dat$VDD_Prevalence), ]
events   <- round(dat_prev$VDD_Prevalence * dat_prev$N / 100)

m2 <- metaprop(
  event   = events,
  n       = dat_prev$N,
  studlab = dat_prev$Author_Year,
  sm      = "PLOGIT",
  random  = TRUE,
  fixed   = FALSE,
  method.tau = "PM",
  hakn    = TRUE
)

pooled_prev <- plogis(m2$TE.random) * 100
lower_prev  <- plogis(m2$lower.random) * 100
upper_prev  <- plogis(m2$upper.random) * 100
cat(sprintf("Pooled VDD prevalence: %.1f%% (95%% CI: %.1f%%-%-.1f%%)\n",
            pooled_prev, lower_prev, upper_prev))
cat(sprintf("I² = %.1f%% | Q = %.1f, p = %.4f\n",
            m2$I2 * 100, m2$Q, m2$pval.Q))

# ── 4. Publication bias ───────────────────────────────────────────────────────
cat("\n--- Publication Bias ---\n")
egger  <- metabias(m1, method.bias = "linreg")
cat(sprintf("Egger's test: t = %.3f, df = %d, p = %.3f\n",
            egger$statistic, egger$df, egger$p.value))

tf <- trimfill(m1)
tf_prev <- plogis(tf$TE.random) * 100
cat(sprintf("Trim-and-fill: imputed studies = %d, adjusted pooled = %.1f ng/mL\n",
            tf$k0, tf$TE.random))

# ── 5. Meta-regression ────────────────────────────────────────────────────────
cat("\n--- Meta-Regression ---\n")
dat_mr <- dat_mean
dat_mr$sei <- dat_mr$SD / sqrt(dat_mr$N)

mr1 <- rma(
  yi   = dat_mr$Mean_25OHD,
  sei  = dat_mr$sei,
  mods = ~ Population_Category_numeric + Assay_numeric +
            NOS_Score + Publication_Year + Region_numeric,
  data   = dat_mr,
  method = "REML"
)
cat("\nMeta-regression results:\n")
print(summary(mr1))
cat(sprintf("R² from moderators: %.1f%%\n",
            max(0, mr1$R2) * 100))

# ── 6. Subgroup analyses ──────────────────────────────────────────────────────
cat("\n--- Subgroup Analyses ---\n")
for (pop in unique(dat_prev$Population_Category)) {
  sub <- dat_prev[dat_prev$Population_Category == pop, ]
  if (nrow(sub) >= 2) {
    ev <- round(sub$VDD_Prevalence * sub$N / 100)
    ms <- metaprop(ev, sub$N, studlab=sub$Author_Year,
                   sm="PLOGIT", random=TRUE, fixed=FALSE,
                   method.tau="PM", hakn=TRUE)
    cat(sprintf("  %-14s: %.1f%% (95%% CI: %.1f%%–%.1f%%), k=%d\n",
                pop,
                plogis(ms$TE.random)*100,
                plogis(ms$lower.random)*100,
                plogis(ms$upper.random)*100,
                nrow(sub)))
  } else {
    ev <- round(sub$VDD_Prevalence * sub$N / 100)
    cat(sprintf("  %-14s: %.1f%% (single study, k=1)\n",
                pop, sub$VDD_Prevalence))
  }
}

# ── 7. Sensitivity: leave-one-out ────────────────────────────────────────────
cat("\n--- Sensitivity (Leave-One-Out) ---\n")
loo_res <- metainf(m1, pooled="random")
cat(sprintf("LOO range: %.1f – %.1f ng/mL\n",
            min(loo_res$lower), max(loo_res$upper)))

cat("\n=== META-ANALYSIS COMPLETE ===\n")
cat(sprintf("Key result: Pooled VDD = %.1f%% (95%% CI: %.1f%%–%.1f%%)\n",
            pooled_prev, lower_prev, upper_prev))
cat(sprintf("Key result: Pooled mean = %.1f ng/mL (95%% CI: %.1f–%.1f)\n",
            m1$TE.random, m1$lower.random, m1$upper.random))
cat(sprintf("Egger's p = %.3f | Trim-fill imputed k = %d\n", egger$p.value, tf$k0))
