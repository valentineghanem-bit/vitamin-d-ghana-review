"""Export the prevalence-row matrix and CART status.

The evidence base has only nine eligible VDD prevalence
rows. That is not enough for a defensible predictive CART model. This script is
kept so the reproducibility pipeline remains stable, but it writes an eligibility
status rather than model performance claims.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "extracted_data.csv"
MATRIX = ROOT / "data" / "cart_feature_matrix.csv"
RESULTS = ROOT / "outputs" / "data" / "cart_results.json"


def build_matrix() -> pd.DataFrame:
    df = pd.read_csv(DATA)
    prev = df.dropna(subset=["analysis_n_vdd", "vdd_prevalence_pct"]).copy()
    prev["population_numeric"] = pd.Categorical(prev["population"]).codes + 1
    prev["region_numeric"] = pd.Categorical(prev["region"]).codes + 1
    prev["assay_numeric"] = pd.Categorical(prev["assay_method"]).codes + 1
    prev["quality_score"] = prev["quality_assessment"].str.extract(r"(\d+)").fillna(2).astype(int)
    prev["sample_size"] = prev["analysis_n_vdd"].astype(int)
    prev["high_vdd"] = (prev["vdd_prevalence_pct"] > 70).astype(int)
    cols = [
        "ref_id",
        "first_author_year",
        "population_numeric",
        "region_numeric",
        "assay_numeric",
        "quality_score",
        "sample_size",
        "vdd_prevalence_pct",
        "high_vdd",
    ]
    MATRIX.parent.mkdir(parents=True, exist_ok=True)
    prev[cols].to_csv(MATRIX, index=False)
    return prev[cols]


def write_status(matrix: pd.DataFrame) -> dict:
    result = {
        "analysis": "CART sensitivity output not retained for inferential use",
        "retained_as_inferential_model": False,
        "n_rows": int(len(matrix)),
        "source": "data/cart_feature_matrix.csv derived only from eligible VDD prevalence rows",
        "reason": "Only nine prevalence rows were eligible for pooling. This is too sparse for a defensible predictive model, and earlier CART accuracy/AUC claims were removed from the manuscript and repository narrative.",
        "current_use": "Reproducibility check only. The matrix confirms which rows entered the VDD prevalence synthesis.",
    }
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(write_status(build_matrix()), indent=2))
