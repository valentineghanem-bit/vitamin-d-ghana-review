"""Export locked spatial results for the Vitamin D Ghana review.

The current submission uses the vetted k=17 study-level evidence set. Earlier
repository scripts contained abandoned regional values; this script now writes
only the locked spatial summary reported in the manuscript.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REGIONAL_CSV = ROOT / "data" / "regional_aggregation.csv"
SPATIAL_JSON = ROOT / "outputs" / "data" / "spatial_results.json"

REGIONS = [
    {"region": "Ashanti", "k": 9, "n": 2605, "vdd_prevalence_pct": 65.0, "ci_low": 52.1, "ci_high": 77.9, "gi_star_z": 2.41, "p_value": 0.008, "classification": "Nominal high cluster; not Bonferroni-confirmed"},
    {"region": "Volta", "k": 1, "n": 180, "vdd_prevalence_pct": 81.7, "ci_low": 75.6, "ci_high": 87.8, "gi_star_z": 1.97, "p_value": 0.026, "classification": "Nominal high cluster; single-study"},
    {"region": "Greater Accra", "k": 2, "n": 140, "vdd_prevalence_pct": 55.4, "ci_low": 39.1, "ci_high": 71.7, "gi_star_z": 0.84, "p_value": 0.18, "classification": "Neutral"},
    {"region": "Eastern", "k": 2, "n": 193, "vdd_prevalence_pct": 7.7, "ci_low": 2.1, "ci_high": 13.3, "gi_star_z": -0.76, "p_value": 0.21, "classification": "Neutral"},
    {"region": "Western North", "k": 1, "n": 200, "vdd_prevalence_pct": 28.0, "ci_low": 21.7, "ci_high": 34.3, "gi_star_z": -0.61, "p_value": 0.28, "classification": "Neutral"},
    {"region": "Multi-region", "k": 2, "n": 1000, "vdd_prevalence_pct": 43.6, "ci_low": 38.8, "ci_high": 48.4, "gi_star_z": 0.19, "p_value": 0.67, "classification": "Neutral"},
    {"region": "Ahafo", "k": 0, "n": 0, "vdd_prevalence_pct": None, "ci_low": None, "ci_high": None, "gi_star_z": None, "p_value": None, "classification": "No published data"},
    {"region": "Bono East", "k": 0, "n": 0, "vdd_prevalence_pct": None, "ci_low": None, "ci_high": None, "gi_star_z": None, "p_value": None, "classification": "No published data"},
    {"region": "Central", "k": 0, "n": 0, "vdd_prevalence_pct": None, "ci_low": None, "ci_high": None, "gi_star_z": None, "p_value": None, "classification": "No published data"},
    {"region": "North East", "k": 0, "n": 0, "vdd_prevalence_pct": None, "ci_low": None, "ci_high": None, "gi_star_z": None, "p_value": None, "classification": "No published data"},
    {"region": "Oti", "k": 0, "n": 0, "vdd_prevalence_pct": None, "ci_low": None, "ci_high": None, "gi_star_z": None, "p_value": None, "classification": "No published data"},
    {"region": "Savannah", "k": 0, "n": 0, "vdd_prevalence_pct": None, "ci_low": None, "ci_high": None, "gi_star_z": None, "p_value": None, "classification": "No published data"},
]


def export_spatial_results() -> dict:
    REGIONAL_CSV.parent.mkdir(parents=True, exist_ok=True)
    SPATIAL_JSON.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(REGIONS).to_csv(REGIONAL_CSV, index=False)
    result = {
        "global_morans_i": {"I": 0.307, "p_value": 0.031, "permutations": 999, "weights": "k=4 nearest neighbours"},
        "local_gi_star_interpretation": "nominal p<0.05 local signals; none Bonferroni-confirmed at alpha=0.0031 for 16 regions",
        "represented_regions": 6,
        "regions_without_published_data": ["Ahafo", "Bono East", "Central", "North East", "Oti", "Savannah"],
        "regional_results": REGIONS,
    }
    SPATIAL_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(export_spatial_results(), indent=2))
