"""Integrity tests for the corrected Vitamin D Ghana dataset."""
import json
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs" / "data"

N_PAPERS = 17
PAPER_N = 4316
VDD_ROWS = 9
VDD_N = 1609
POOLED_VDD = 55.3
POOLED_VDD_CI = (35.5, 75.2)
MEAN_ROWS = 7
MEAN_N = 1153
POOLED_MEAN = 25.1
POOLED_MEAN_CI = (12.7, 37.5)


@pytest.fixture
def extracted():
    return pd.read_csv(DATA / "extracted_data.csv")


@pytest.fixture
def canonical():
    return pd.read_csv(DATA / "canonical_values.csv").iloc[0]


def row(df, study):
    match = df[df["first_author_year"] == study]
    assert len(match) == 1, f"{study} row missing or duplicated"
    return match.iloc[0]


class TestCorrectedExtraction:
    def test_review_count_and_paper_n(self, extracted):
        assert len(extracted) == N_PAPERS
        assert int(extracted["paper_n"].sum()) == PAPER_N

    def test_required_corrected_columns_present(self, extracted):
        required = {
            "paper_n",
            "analysis_n_vdd",
            "analysis_n_mean",
            "mean_statistic_type",
            "cohort_id",
            "analysis_role",
            "extraction_status",
            "extraction_note",
        }
        assert required.issubset(extracted.columns)

    def test_vdd_analysis_uses_only_verified_rows(self, extracted):
        vdd = extracted.dropna(subset=["analysis_n_vdd", "vdd_prevalence_pct"])
        assert len(vdd) == VDD_ROWS
        assert int(vdd["analysis_n_vdd"].sum()) == VDD_N
        assert vdd["extraction_status"].str.contains("extractable").all()

    def test_unsupported_old_vdd_values_are_removed(self, extracted):
        assert pd.isna(row(extracted, "Asare 2017")["vdd_prevalence_pct"])
        assert pd.isna(row(extracted, "Sakyi 2022")["vdd_prevalence_pct"])
        assert pd.isna(row(extracted, "Dzudzor 2023")["vdd_prevalence_pct"])

    def test_pooling_rows_match_eligibility_decisions(self, extracted):
        fondjo2017 = row(extracted, "Fondjo 2017")
        assert int(fondjo2017["paper_n"]) == 216
        assert int(fondjo2017["analysis_n_vdd"]) == 118
        assert fondjo2017["vdd_prevalence_pct"] == pytest.approx(92.4)
        assert pd.isna(fondjo2017["mean_25ohd_ngml"])

        fondjo2018 = row(extracted, "Fondjo 2018")
        assert fondjo2018["vdd_prevalence_pct"] == pytest.approx(60.9)
        assert fondjo2018["mean_25ohd_ngml"] == pytest.approx(8.38)

        fondjo2022 = row(extracted, "Fondjo 2022")
        assert fondjo2022["vdd_prevalence_pct"] == pytest.approx(39.5)
        assert pd.isna(fondjo2022["mean_25ohd_ngml"])
        assert "median/IQR" in fondjo2022["mean_statistic_type"]

    def test_mean_analysis_does_not_count_median_rows_as_means(self, extracted):
        mean = extracted.dropna(subset=["analysis_n_mean", "mean_25ohd_ngml"])
        assert len(mean) == MEAN_ROWS
        assert int(mean["analysis_n_mean"].sum()) == MEAN_N
        assert "Fondjo 2022" not in set(mean["first_author_year"])
        assert "Dzudzor 2023" not in set(mean["first_author_year"])


class TestCanonicalOutputs:
    def test_canonical_values_match_corrected_meta_analysis(self, canonical):
        assert int(canonical["Included papers (k)"]) == N_PAPERS
        assert int(canonical["Prevalence analytic rows (k)"]) == VDD_ROWS
        assert int(canonical["Prevalence analytic N"]) == VDD_N
        assert canonical["Random-effects VDD prevalence (%)"] == pytest.approx(POOLED_VDD)
        assert canonical["VDD 95% CI low"] == pytest.approx(POOLED_VDD_CI[0])
        assert canonical["VDD 95% CI high"] == pytest.approx(POOLED_VDD_CI[1])
        assert canonical["Random-effects mean 25(OH)D (ng/mL)"] == pytest.approx(POOLED_MEAN)
        assert canonical["Mean 25(OH)D 95% CI low"] == pytest.approx(POOLED_MEAN_CI[0])
        assert canonical["Mean 25(OH)D 95% CI high"] == pytest.approx(POOLED_MEAN_CI[1])

    def test_spatial_inference_is_withdrawn(self, canonical):
        assert int(canonical["Region-specific VDD mapped regions (k)"]) == 4
        assert int(canonical["Regions without region-specific VDD prevalence data"]) == 12
        assert canonical["Spatial autocorrelation retained"] == "No"

    def test_regional_aggregation_has_four_mapped_regions(self):
        regional = pd.read_csv(DATA / "regional_aggregation.csv")
        mapped = regional[regional["k"] > 0]
        assert set(mapped["region"]) == {"Ashanti", "Volta", "Eastern", "Western North"}
        assert len(regional[regional["k"] == 0]) == 12

    def test_cart_feature_matrix_is_verification_matrix_only(self):
        matrix = pd.read_csv(DATA / "cart_feature_matrix.csv")
        assert len(matrix) == VDD_ROWS
        assert set(matrix["ref_id"]) == {4, 5, 21, 23, 24, 26, 27, 28, 31}

    def test_withdrawn_model_json_outputs_are_not_inferential(self):
        with open(OUT / "cart_results.json", encoding="utf-8") as f:
            cart = json.load(f)
        assert cart["retained_as_inferential_model"] is False
        assert cart["n_rows"] == VDD_ROWS

        with open(OUT / "spatial_results.json", encoding="utf-8") as f:
            spatial = json.load(f)
        assert spatial["formal_spatial_autocorrelation_retained"] is False
        assert spatial["mapped_regions"] == 4
        assert spatial["regions_without_region_specific_prevalence_data"] == 12
