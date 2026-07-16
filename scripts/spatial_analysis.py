"""Export regional evidence-coverage status.

Formal Moran's I and Gi* hotspot inference is not retained because only four
administrative regions have extractable region-specific VDD prevalence. This
script preserves a reproducible status
output without regenerating invalid spatial statistics.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REGIONAL_CSV = ROOT / "data" / "regional_aggregation.csv"
SPATIAL_JSON = ROOT / "outputs" / "data" / "spatial_results.json"


def export_spatial_status() -> dict:
    regional = pd.read_csv(REGIONAL_CSV)
    mapped = regional[regional["k"] > 0]["region"].tolist()
    result = {
        "analysis": "Spatial autocorrelation and hotspot inference not retained",
        "formal_spatial_autocorrelation_retained": False,
        "mapped_regions": int(len(mapped)),
        "regions_without_region_specific_prevalence_data": int((regional["k"] == 0).sum()),
        "mapped_regions_list": mapped,
        "reason": "Only four of Ghana's sixteen administrative regions had extractable region-specific VDD prevalence. Multi-region donor data were not assigned to a single administrative polygon. Moran's I, Gi* hotspot and north-south gradient claims are therefore not retained as defensible inferential findings.",
        "current_use": "Evidence-coverage mapping only.",
    }
    SPATIAL_JSON.parent.mkdir(parents=True, exist_ok=True)
    SPATIAL_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(export_spatial_status(), indent=2))
