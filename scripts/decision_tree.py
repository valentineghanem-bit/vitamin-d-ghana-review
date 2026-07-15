"""Build the reproducible CART input matrix for the Vitamin D Ghana review.

This derives the study-level feature matrix from data/extracted_data.csv, writes
data/cart_feature_matrix.csv, and runs the exploratory CART model reported in
the manuscript. It does not use abandoned individual-level simulations.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.tree import DecisionTreeClassifier

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "extracted_data.csv"
MATRIX = ROOT / "data" / "cart_feature_matrix.csv"
RESULTS = ROOT / "outputs" / "data" / "cart_results.json"

POP_MAP = {
    "Healthy adults": 1,
    "Healthy donors": 1,
    "Pre-conception": 2,
    "Pregnant women": 3,
    "Pregnant (1st trimester)": 3,
    "T2DM": 4,
    "T2DM women": 4,
    "BPH patients": 5,
    "Psychiatric": 6,
    "RA patients": 7,
    "CLD patients": 8,
}
REGION_MAP = {
    "Ashanti": 1,
    "Greater Accra": 2,
    "Eastern": 3,
    "Western North": 4,
    "Volta": 5,
    "Multi-region": 6,
}
ASSAY_MAP = {"ELISA": 1, "LC-MS/MS": 2}


def quality_score(value: str) -> int:
    text = str(value)
    if text[:1].isdigit():
        return int(text[:1])
    if "Some concerns" in text:
        return 6
    return 6


def build_matrix() -> pd.DataFrame:
    df = pd.read_csv(DATA)
    matrix = pd.DataFrame(
        {
            "ref_id": df["ref_id"],
            "first_author_year": df["first_author_year"],
            "population_numeric": df["population"].map(POP_MAP).fillna(0).astype(int),
            "region_numeric": df["region"].map(REGION_MAP).fillna(0).astype(int),
            "assay_numeric": df["assay_method"].map(ASSAY_MAP).fillna(0).astype(int),
            "quality_score": df["quality_assessment"].map(quality_score),
            "sample_size": df["n"],
            "vdd_prevalence_pct": df["vdd_prevalence_pct"],
            "high_vdd": (df["vdd_prevalence_pct"] > 70).astype(int),
        }
    )
    MATRIX.parent.mkdir(parents=True, exist_ok=True)
    matrix.to_csv(MATRIX, index=False)
    return matrix


def run_cart(matrix: pd.DataFrame) -> dict:
    features = ["population_numeric", "region_numeric", "assay_numeric", "quality_score", "sample_size"]
    x = matrix[features]
    y = matrix["high_vdd"]
    clf = DecisionTreeClassifier(max_depth=3, min_samples_split=5, random_state=42, class_weight="balanced")
    loo = LeaveOneOut()
    pred = cross_val_predict(clf, x, y, cv=loo)
    prob = cross_val_predict(clf, x, y, cv=loo, method="predict_proba")[:, 1]
    clf.fit(x, y)
    result = {
        "n_studies": int(len(matrix)),
        "high_vdd_threshold_pct": 70,
        "accuracy": round(float(accuracy_score(y, pred)), 3),
        "auc": round(float(roc_auc_score(y, prob)), 3),
        "features": features,
        "source": "data/cart_feature_matrix.csv derived from data/extracted_data.csv",
    }
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(run_cart(build_matrix()), indent=2))
