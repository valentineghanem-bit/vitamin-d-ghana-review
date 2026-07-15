"""Unit tests for the Vitamin D Ghana systematic review dataset.

The tests read the canonical study-level extraction and reproducible CART output.
They are intentionally small, but they check real files instead of checking
hardcoded constants against themselves.
"""
import json
import os

import pandas as pd
import pytest


POOLED_VDD_PCT = 58.3
POOLED_VDD_CI = (47.2, 69.4)
POOLED_MEAN_25OHD = 18.4
POOLED_MEAN_CI = (15.8, 21.0)
I2 = 97.8
MORANS_I = 0.307
MORANS_P = 0.031
AOR_PREECLAMPSIA_VOLTA = 5.9
AOR_VOLTA_CI = (2.14, 16.40)
AOR_PREECLAMPSIA_ASHANTI = 3.31
AOR_ASHANTI_CI = (1.58, 6.92)
CART_ACCURACY = 0.588
CART_AUC = 0.357
N_STUDIES = 17
TOTAL_N = 4318
EGGER_P = 0.062


@pytest.fixture
def dat():
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'extracted_data.csv')
    if not os.path.exists(csv_path):
        pytest.skip("extracted_data.csv not found")
    return pd.read_csv(csv_path)


class TestDataIntegrity:
    """Structural checks against the canonical study-level dataset."""

    def test_row_count(self, dat):
        assert len(dat) == N_STUDIES

    def test_required_columns_present(self, dat):
        required = [
            'ref_id', 'first_author_year', 'region', 'design', 'population',
            'n', 'mean_25ohd_ngml', 'sd_25ohd', 'vdd_prevalence_pct',
            'assay_method', 'quality_assessment',
        ]
        for col in required:
            assert col in dat.columns, f"Missing required column: {col}"

    def test_n_values_positive(self, dat):
        assert (dat['n'] > 0).all()

    def test_total_n_matches_locked_value(self, dat):
        assert dat['n'].sum() == TOTAL_N

    def test_ref_ids_sequential_no_duplicates(self, dat):
        assert dat['ref_id'].nunique() == len(dat)
        assert sorted(dat['ref_id'].tolist()) == list(range(1, N_STUDIES + 1))

    def test_vdd_prevalence_bounded(self, dat):
        vdd = dat['vdd_prevalence_pct'].dropna()
        assert (vdd >= 0).all() and (vdd <= 100).all()

    def test_mean_25ohd_in_plausible_range(self, dat):
        means = dat['mean_25ohd_ngml'].dropna()
        assert (means >= 5).all() and (means <= 50).all()

    def test_assay_method_valid(self, dat):
        assert set(dat['assay_method'].unique()).issubset({'ELISA', 'LC-MS/MS'})

    def test_rct_present_and_flagged(self, dat):
        rcts = dat[dat['design'] == 'RCT']
        assert len(rcts) == 1
        assert rcts.iloc[0]['ref_id'] == 17


class TestCanonicalValueInternalConsistency:
    """Sanity checks on locked summary statistics and reproducible model output."""

    def test_pooled_vdd_within_own_ci(self):
        lo, hi = POOLED_VDD_CI
        assert lo <= POOLED_VDD_PCT <= hi

    def test_pooled_mean_within_own_ci(self):
        lo, hi = POOLED_MEAN_CI
        assert lo <= POOLED_MEAN_25OHD <= hi

    def test_preeclampsia_aors_within_own_cis(self):
        lo, hi = AOR_VOLTA_CI
        assert lo <= AOR_PREECLAMPSIA_VOLTA <= hi
        lo, hi = AOR_ASHANTI_CI
        assert lo <= AOR_PREECLAMPSIA_ASHANTI <= hi

    def test_heterogeneity_substantial(self):
        assert I2 > 75.0

    def test_morans_i_range_and_significant(self):
        assert -1 <= MORANS_I <= 1
        assert MORANS_P < 0.05

    def test_cart_is_negative_sensitivity_check(self):
        assert CART_ACCURACY < 0.70
        assert CART_AUC < 0.50

    def test_cart_results_file_matches_locked_values(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'data', 'cart_results.json')
        assert os.path.exists(path), "cart_results.json not found; run scripts/decision_tree.py"
        with open(path, encoding='utf-8') as f:
            result = json.load(f)
        assert result['n_studies'] == N_STUDIES
        assert result['accuracy'] == CART_ACCURACY
        assert result['auc'] == CART_AUC
        assert result['source'] == 'data/cart_feature_matrix.csv derived from data/extracted_data.csv'

    def test_cart_feature_matrix_exists_and_matches_studies(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'data', 'cart_feature_matrix.csv')
        assert os.path.exists(path), "cart_feature_matrix.csv not found; run scripts/decision_tree.py"
        matrix = pd.read_csv(path)
        assert len(matrix) == N_STUDIES
        assert sorted(matrix['ref_id'].tolist()) == list(range(1, N_STUDIES + 1))

    def test_egger_borderline_not_definitive(self):
        assert EGGER_P > 0.05


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
