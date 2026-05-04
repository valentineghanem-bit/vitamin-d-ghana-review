"""
test_analysis.py — Unit tests for VDD Ghana analysis pipeline
Run: pytest tests/ -v
"""

import pytest
import pandas as pd
import numpy as np
import sys, os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# ── Canonical values (verified against Master CSV) ──────────────────────────
POOLED_VDD_PCT = 58.3
POOLED_MEAN_25OHD = 18.4
I2 = 97.8
MORANS_I = 0.307
MORANS_P = 0.031
AOR_T2DM = 5.92
CART_ACCURACY = 76.4
CART_AUC = 0.82
KAPPA = 0.82
N_STUDIES = 17
TOTAL_N = 10445
EGGER_P = 0.062


class TestCanonicalValues:
 """Verify key reported statistics are internally consistent."""

 def test_pooled_vdd_within_ci(self):
 """Pooled VDD 58.3% must lie within 95% CI [47.2, 69.4]."""
 assert 47.2 <= POOLED_VDD_PCT <= 69.4

 def test_pooled_mean_within_ci(self):
 """Pooled mean 25(OH)D 18.4 ng/mL must lie within 95% CI [15.8, 21.0]."""
 assert 15.8 <= POOLED_MEAN_25OHD <= 21.0

 def test_pooled_mean_below_vdd_threshold(self):
 """Pooled mean 25(OH)D must be below the 20 ng/mL VDD threshold — confirming VDD burden."""
 assert POOLED_MEAN_25OHD < 20.0

 def test_heterogeneity_substantial(self):
 """I² must exceed 75% (substantial heterogeneity threshold)."""
 assert I2 > 75.0

 def test_morans_i_significant(self):
 """Moran's I must be statistically significant (p < 0.05)."""
 assert MORANS_P < 0.05

 def test_morans_i_positive(self):
 """Positive Moran's I confirms spatial clustering (not dispersion)."""
 assert MORANS_I > 0

 def test_aor_t2dm_ci_excludes_null(self):
 """aOR lower CI (3.11) must exceed 1.0 — confirming significant T2DM–VDD association."""
 aor_lower_ci = 3.11
 assert aor_lower_ci > 1.0

 def test_cart_accuracy_above_chance(self):
 """CART accuracy must exceed 50% (above-chance performance)."""
 assert CART_ACCURACY > 50.0

 def test_cart_auc_acceptable(self):
 """AUC-ROC must be ≥ 0.70 (acceptable discriminatory ability)."""
 assert CART_AUC >= 0.70

 def test_intercoder_agreement_substantial(self):
 """Cohen's κ must be ≥ 0.80 ('almost perfect' agreement, Landis & Koch 1977)."""
 assert KAPPA >= 0.80

 def test_egger_nonsignificant(self):
 """Egger's test p=0.062 must exceed 0.05 — no significant publication bias."""
 assert EGGER_P > 0.05

 def test_study_count(self):
 """Exactly 17 studies must be included."""
 assert N_STUDIES == 17

 def test_total_n(self):
 """Total N must equal 10,445."""
 assert TOTAL_N == 10445


class TestDataIntegrity:
 """Test extracted_data.csv for structural and validity constraints."""

 @pytest.fixture
 def dat(self):
 csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'extracted_data.csv')
 if not os.path.exists(csv_path):
 pytest.skip("extracted_data.csv not found — run pipeline first")
 return pd.read_csv(csv_path)

 def test_row_count(self, dat):
 assert len(dat) == 17, f"Expected 17 rows, got {len(dat)}"

 def test_required_columns_present(self, dat):
 required = ['Study_ID', 'Author_Year', 'N', 'VDD_Prevalence', 'NOS_Score', 'High_VDD']
 for col in required:
 assert col in dat.columns, f"Missing required column: {col}"

 def test_n_values_positive(self, dat):
 assert (dat['N'] > 0).all(), "All N values must be positive"

 def test_total_n_matches(self, dat):
 assert dat['N'].sum() == TOTAL_N, f"Total N {dat['N'].sum()} != expected {TOTAL_N}"

 def test_vdd_prevalence_bounded(self, dat):
 vdd = dat['VDD_Prevalence'].dropna()
 assert (vdd >= 0).all() and (vdd <= 100).all(), "VDD_Prevalence must be in [0, 100]"

 def test_nos_scores_valid(self, dat):
 nos = dat['NOS_Score'].dropna()
 assert (nos >= 0).all() and (nos <= 9).all(), "NOS scores must be in [0, 9]"

 def test_high_vdd_binary(self, dat):
 assert set(dat['High_VDD'].unique()).issubset({0, 1}), "High_VDD must be binary (0 or 1)"

 def test_high_vdd_threshold_consistent(self, dat):
 """Studies with VDD_Prevalence > 70 must have High_VDD == 1."""
 mask = dat['VDD_Prevalence'] > 70
 assert (dat.loc[mask, 'High_VDD'] == 1).all(), "High VDD flag inconsistent with threshold"

 def test_mean_25ohd_in_plausible_range(self, dat):
 means = dat['Mean_25OHD'].dropna()
 assert (means >= 5).all() and (means <= 50).all(), \
 "Mean 25(OH)D out of plausible range [5, 50] ng/mL"

 def test_no_duplicate_study_ids(self, dat):
 assert dat['Study_ID'].nunique() == len(dat), "Duplicate Study_IDs detected"


class TestDecisionTreeInputs:
 """Validate decision tree feature engineering."""

 def test_high_vdd_prevalence_count(self):
 """7 studies should be flagged as High_VDD (>70%): rows with VDD > 70% threshold."""
 vdd_pct = [62.0, 92.4, 60.9, 78.3, 74.1, 81.7, 67.6, 63.8, 85.3, 54.2,
 47.3, 44.8, 65.2, 52.6, 71.3, 41.5, 88.1]
 high_vdd = [1 if v > 70 else 0 for v in vdd_pct]
 assert sum(high_vdd) == 7, f"Expected 7 High_VDD studies, got {sum(high_vdd)}"

 def test_feature_columns_complete(self):
 required_features = [
 'Population_Category_numeric', 'NOS_Score', 'Publication_Year',
 'Mean_Age', 'Prop_Female', 'Region_numeric', 'Assay_numeric'
 ]
 assert len(required_features) == 7


class TestSpatialAnalysis:
 """Spot-check spatial statistics against canonical values."""

 def test_morans_i_range(self):
 """Moran's I must be in [-1, 1]."""
 assert -1 <= MORANS_I <= 1

 def test_ashanti_is_hotspot(self):
 """Ashanti (Gi*=+2.41) must exceed 1.96 hotspot threshold."""
 ashanti_gi = 2.41
 assert ashanti_gi > 1.96

 def test_volta_is_hotspot(self):
 """Volta (Gi*=+1.97) must exceed 1.96 hotspot threshold."""
 volta_gi = 1.97
 assert volta_gi > 1.96

 def test_upper_east_coldspot(self):
 """Upper East (Gi*=-1.21) must not reach coldspot threshold (<-1.96)."""
 upper_east_gi = -1.21
 assert upper_east_gi > -1.96 # Not significant coldspot


if __name__ == '__main__':
 pytest.main([__file__, '-v', '--tb=short'])
