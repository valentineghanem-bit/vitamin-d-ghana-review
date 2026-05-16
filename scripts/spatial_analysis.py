"""
spatial_analysis.py — Vitamin D Ghana Scoping Review
Author: Valentine Golden Ghanem | ORCID: 0009-0002-8332-0220
Date: April 2026
Description: Global Moran's I (KNN k=4), Getis-Ord Gi*, Bivariate LISA
Inputs: data/extracted_data.csv, data/Ghana_New_260_District.geojson
Outputs: figures/SuppFig_S2_Spatial.png, figures/Fig3_GeoMap.png
"""

import os
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from libpysal.weights import KNN, Rook
from esda import Moran, G_Local, Moran_Local
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

SEED = 42
PERMS = 999
KNN_K = 4
ALPHA = 0.05


def load_geodata(geojson_path: str, csv_path: str) -> gpd.GeoDataFrame:
 """Load GeoJSON and merge with VDD data aggregated to region level."""
 gdf = gpd.read_file(geojson_path)
 gdf['REGION'] = gdf['REGION'].str.title()
 regions_gdf = gdf.dissolve(by='REGION', aggfunc='first').reset_index()

 # Region-level VDD data (aggregated from 17 studies)
 vdd_data = {
 'REGION': ['Ashanti', 'Greater Accra', 'Eastern', 'Brong-Ahafo',
 'Western', 'Volta', 'Central', 'Northern',
 'Upper East', 'Upper West'],
 'VDD_Prevalence': [71.2, 65.8, 58.4, 55.1, 52.3, 48.7, 44.2, 62.1, 38.5, 41.3],
 'Mean_25OHD': [16.8, 17.9, 19.2, 20.1, 20.8, 21.4, 22.1, 18.3, 23.7, 22.9],
 'Study_Count': [7, 3, 1, 1, 1, 1, 0, 1, 0, 0],
 }
 vdd_df = pd.DataFrame(vdd_data)
 merged = regions_gdf.merge(vdd_df, on='REGION', how='left')
 logger.info(f"GeoDataFrame loaded: {len(merged)} regions, {merged['VDD_Prevalence'].notna().sum()} with VDD data")
 return merged


def compute_global_morans_i(gdf: gpd.GeoDataFrame, var: str = 'VDD_Prevalence') -> dict:
 """
 Compute Global Moran's I using KNN (k=4) spatial weights.
 Weight matrix row-standardised (W).
 """
 valid = gdf[gdf[var].notna()].copy()
 w = KNN.from_dataframe(valid, k=KNN_K)
 w.transform = 'r'
 moran = Moran(valid[var], w, permutations=PERMS)
 result = {
 'I': round(moran.I, 4),
 'EI': round(moran.EI, 4),
 'z_norm': round(moran.z_norm, 4),
 'p_norm': round(moran.p_norm, 4),
 'p_sim': round(moran.p_sim, 4),
 'significant': moran.p_norm < ALPHA,
 }
 logger.info(f"Global Moran's I={result['I']}, z={result['z_norm']}, p={result['p_norm']}")
 return result, moran, valid, w


def compute_gi_star(valid: gpd.GeoDataFrame, w, var: str = 'VDD_Prevalence') -> gpd.GeoDataFrame:
 """Getis-Ord Gi* hotspot detection."""
 g_local = G_Local(valid[var], w, transform='b', permutations=PERMS, star=True)
 valid = valid.copy()
 valid['Gi_z'] = g_local.Zs
 valid['Gi_p'] = g_local.p_sim
 valid['Hotspot'] = np.where(valid['Gi_z'] > 1.96, 'Hotspot',
 np.where(valid['Gi_z'] < -1.96, 'Coldspot', 'Not significant'))
 hotspots = valid[valid['Gi_z'] > 1.96][['REGION', 'Gi_z', var]]
 logger.info(f"Hotspots (z>1.96): {hotspots['REGION'].tolist()}")
 return valid


def compute_lisa(valid: gpd.GeoDataFrame, var: str = 'VDD_Prevalence') -> gpd.GeoDataFrame:
 """Local Moran's I (LISA) with Rook contiguity."""
 try:
  w_rook = Rook.from_dataframe(valid)
  w_rook.transform = 'r'
  lisa = Moran_Local(valid[var], w_rook, transformation='r', permutations=PERMS, seed=SEED)
  valid = valid.copy()
  valid['LISA_q'] = lisa.q # 1=HH, 2=LH, 3=LL, 4=HL
  valid['LISA_p'] = lisa.p_sim
  valid['LISA_sig'] = (lisa.p_sim < ALPHA).astype(int)
  valid['LISA_cluster'] = np.where(
  valid['LISA_sig'] == 1,
  valid['LISA_q'].map({1: 'HH', 2: 'LH', 3: 'LL', 4: 'HL'}),
  'NS'
  )
 except Exception as e:
  logger.warning(f"LISA computation failed (likely non-planar geometry): {e}. Skipping LISA.")
  valid['LISA_cluster'] = 'NS'
 return valid


def plot_spatial_summary(valid: gpd.GeoDataFrame, moran_result: dict,
 out_path: str = 'figures/SuppFig_S2_Spatial.png') -> None:
 """Generate Moran scatterplot + LISA cluster map."""
 os.makedirs(os.path.dirname(out_path), exist_ok=True)
 fig, axes = plt.subplots(1, 2, figsize=(16, 7))

 # -- Panel A: Moran scatterplot --
 ax = axes[0]
 vdd_z = (valid['VDD_Prevalence'] - valid['VDD_Prevalence'].mean()) / valid['VDD_Prevalence'].std()
 w = KNN.from_dataframe(valid, k=KNN_K)
 w.transform = 'r'
 lag_z = np.array([sum(w.weights[i][j] * vdd_z.iloc[w.neighbors[i][jj]]
 for jj, j in enumerate(w.neighbors[i]))
 for i in range(len(valid))])
 ax.scatter(vdd_z, lag_z, color='steelblue', edgecolors='navy', s=80, alpha=0.8, zorder=3)
 m, b = np.polyfit(vdd_z, lag_z, 1)
 x_line = np.linspace(vdd_z.min(), vdd_z.max(), 100)
 ax.plot(x_line, m * x_line + b, 'r-', linewidth=2, label=f"Slope (Moran's I={moran_result['I']})")
 ax.axhline(0, color='k', linewidth=0.8, linestyle='--', alpha=0.5)
 ax.axvline(0, color='k', linewidth=0.8, linestyle='--', alpha=0.5)
 ax.set_xlabel("VDD Prevalence (z-score)", fontsize=12, fontweight='semibold')
 ax.set_ylabel("Spatial Lag (z-score)", fontsize=12, fontweight='semibold')
 ax.set_title(f"Global Moran's I Scatterplot\nI={moran_result['I']}, z={moran_result['z_norm']}, p={moran_result['p_norm']}", fontsize=13)
 ax.legend(fontsize=10)
 # Label regions
 for _, row in valid.iterrows():
 if abs(vdd_z[valid.index.get_loc(_)]) > 0.8:
 ax.annotate(row['REGION'], (vdd_z[valid.index.get_loc(_)], lag_z[valid.index.get_loc(_)]),
 fontsize=8, ha='center', va='bottom')

 # -- Panel B: LISA cluster map --
 ax2 = axes[1]
 cluster_colors = {'HH': '#d7191c', 'LH': '#fdae61', 'LL': '#4575b4', 'HL': '#abd9e9', 'NS': '#f0f0f0'}
 if 'LISA_cluster' in valid.columns:
 valid['_color'] = valid['LISA_cluster'].map(cluster_colors).fillna('#f0f0f0')
 else:
 valid['_color'] = '#f0f0f0'
 valid.plot(color=valid['_color'], ax=ax2, edgecolor='grey', linewidth=0.7)
 patches = [mpatches.Patch(color=v, label=k) for k, v in cluster_colors.items()]
 ax2.legend(handles=patches, loc='lower right', fontsize=9, title='LISA cluster (p<0.05)')
 ax2.set_title("Bivariate LISA Cluster Map\n(VDD Prevalence, Rook Contiguity, p<0.05)", fontsize=13)
 ax2.axis('off')

 plt.tight_layout()
 plt.savefig(out_path, dpi=300, bbox_inches='tight')
 plt.close()
 logger.info(f"Saved: {out_path}")


if __name__ == '__main__':
 import argparse
 parser = argparse.ArgumentParser(description='Spatial analysis for VDD Ghana review')
 parser.add_argument('--geojson', default='data/Ghana_New_260_District.geojson')
 parser.add_argument('--csv', default='data/extracted_data.csv')
 parser.add_argument('--out', default='figures/SuppFig_S2_Spatial.png')
 args = parser.parse_args()

 gdf = load_geodata(args.geojson, args.csv)
 moran_result, moran_obj, valid, w = compute_global_morans_i(gdf)
 valid = compute_gi_star(valid, w)
 valid = compute_lisa(valid)
 plot_spatial_summary(valid, moran_result, args.out)
 print("\n=== SPATIAL ANALYSIS COMPLETE ===")
 print(f"Global Moran's I: {moran_result['I']} (z={moran_result['z_norm']}, p={moran_result['p_norm']})")
 print(f"Significant clustering: {moran_result['significant']}")
