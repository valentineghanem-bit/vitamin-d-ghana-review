"""
decision_tree.py — Vitamin D Ghana Scoping Review
Author: Valentine Golden Ghanem | ORCID: 0009-0002-8332-0220
Date: April 2026
Description: CART decision tree (max_depth=3, min_samples_split=5) to predict
 high VDD burden (>70%) using study-level features. LOOCV evaluation.
Inputs: data/extracted_data.csv
Outputs: figures/SuppFig_S1_DecisionTree.png
"""

import os
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.metrics import (accuracy_score, roc_auc_score, confusion_matrix,
 classification_report)
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

SEED = 42
MAX_DEPTH = 3
MIN_SAMPLES_SPLIT = 5
HIGH_VDD_THRESHOLD = 70.0 # percent

FEATURE_COLS = [
 'Population_Category_numeric', 'NOS_Score', 'Publication_Year',
 'Mean_Age', 'Prop_Female', 'Region_numeric', 'Assay_numeric'
]
FEATURE_LABELS = [
 'Population Category', 'NOS Score', 'Publication Year',
 'Mean Age', '% Female', 'Region', 'Assay Method'
]


def load_data(csv_path: str) -> tuple:
 """Load extracted data and prepare features / target."""
 dat = pd.read_csv(csv_path)
 X = dat[FEATURE_COLS].fillna(dat[FEATURE_COLS].median())
 y = dat['High_VDD'].astype(int)
 logger.info(f"Loaded {len(dat)} studies. High VDD: {y.sum()}/{len(y)}")
 return X, y, dat


def fit_and_evaluate(X: pd.DataFrame, y: pd.Series) -> dict:
 """Fit CART model and evaluate with Leave-One-Out Cross-Validation."""
 clf = DecisionTreeClassifier(
 max_depth=MAX_DEPTH,
 min_samples_split=MIN_SAMPLES_SPLIT,
 random_state=SEED,
 criterion='gini',
 class_weight='balanced'
 )
 # Full-data fit for feature importances and tree structure
 clf.fit(X, y)

 # LOOCV for unbiased performance estimates
 loo = LeaveOneOut()
 y_pred = cross_val_predict(clf, X, y, cv=loo)
 y_prob = cross_val_predict(clf, X, y, cv=loo, method='predict_proba')[:, 1]

 cm = confusion_matrix(y, y_pred)
 tn, fp, fn, tp = cm.ravel()
 acc = accuracy_score(y, y_pred)
 auc = roc_auc_score(y, y_prob)
 sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
 specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
 ppv = tp / (tp + fp) if (tp + fp) > 0 else 0
 npv = tn / (tn + fn) if (tn + fn) > 0 else 0

 importances = pd.Series(clf.feature_importances_, index=FEATURE_LABELS)

 metrics = {
 'accuracy': round(acc, 3),
 'sensitivity': round(sensitivity, 3),
 'specificity': round(specificity, 3),
 'ppv': round(ppv, 3),
 'npv': round(npv, 3),
 'auc_roc': round(auc, 3),
 'confusion_matrix': cm.tolist(),
 'feature_importances': importances.sort_values(ascending=False).round(3).to_dict(),
 }

 logger.info(f"LOOCV Accuracy={acc:.3f} Sensitivity={sensitivity:.3f} "
 f"Specificity={specificity:.3f} AUC={auc:.3f}")
 return metrics, clf


def plot_decision_tree(clf: DecisionTreeClassifier, metrics: dict,
 out_path: str = 'figures/SuppFig_S1_DecisionTree.png') -> None:
 """Visualise CART tree with performance annotation."""
 os.makedirs(os.path.dirname(out_path), exist_ok=True)
 fig, ax = plt.subplots(figsize=(16, 8))
 plot_tree(clf, feature_names=FEATURE_LABELS,
 class_names=['Low/Mod VDD', 'High VDD'],
 filled=True, rounded=True, fontsize=10, ax=ax,
 impurity=True, precision=3)

 perf_text = (
 f"LOOCV Performance (n=17)\n"
 f"Accuracy: {metrics['accuracy']*100:.1f}%\n"
 f"Sensitivity: {metrics['sensitivity']*100:.1f}%\n"
 f"Specificity: {metrics['specificity']*100:.1f}%\n"
 f"AUC-ROC: {metrics['auc_roc']:.2f}"
 )
 ax.text(0.02, 0.02, perf_text, transform=ax.transAxes, fontsize=11,
 verticalalignment='bottom',
 bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow',
 edgecolor='#C9A84C', alpha=0.9))

 ax.set_title(
 f"CART Decision Tree — Predictors of High VDD Burden (>{HIGH_VDD_THRESHOLD:.0f}%)\n"
 f"max_depth={MAX_DEPTH}, min_samples_split={MIN_SAMPLES_SPLIT}, "
 f"Leave-One-Out Cross-Validation, random_state={SEED}",
 fontsize=13, fontweight='semibold', pad=15
 )
 plt.tight_layout()
 plt.savefig(out_path, dpi=300, bbox_inches='tight')
 plt.close()
 logger.info(f"Saved: {out_path}")


if __name__ == '__main__':
 import argparse, json
 parser = argparse.ArgumentParser(description='CART decision tree for VDD prediction')
 parser.add_argument('--csv', default='data/extracted_data.csv')
 parser.add_argument('--out', default='figures/SuppFig_S1_DecisionTree.png')
 args = parser.parse_args()

 X, y, dat = load_data(args.csv)
 metrics, clf = fit_and_evaluate(X, y)
 plot_decision_tree(clf, metrics, args.out)

 print("\n=== DECISION TREE RESULTS ===")
 print(json.dumps(metrics, indent=2))
 print("\nTree structure:")
 print(export_text(clf, feature_names=FEATURE_LABELS))
