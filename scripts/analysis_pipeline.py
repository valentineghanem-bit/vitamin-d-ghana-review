"""
analysis_pipeline.py — End-to-end orchestration
Author: Valentine Golden Ghanem | ORCID: 0009-0002-8332-0220
Date: April 2026
Usage:
 python scripts/analysis_pipeline.py --all
 python scripts/analysis_pipeline.py --step spatial
 python scripts/analysis_pipeline.py --step dt
"""

import argparse
import logging
import os
import subprocess
import sys
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

STEPS = {
 'spatial': {
 'label': 'Spatial analysis (Moran\'s I, Gi*, LISA)',
 'script': 'scripts/spatial_analysis.py',
 },
 'dt': {
 'label': 'CART decision tree (LOOCV)',
 'script': 'scripts/decision_tree.py',
 },
}


def run_step(name: str, config: dict) -> float:
 """Execute a single pipeline step and return elapsed seconds."""
 logger.info(f"{'='*60}")
 logger.info(f"STEP [{name}]: {config['label']}")
 logger.info(f"{'='*60}")
 t0 = time.time()
 result = subprocess.run(
 [sys.executable, config['script']],
 capture_output=False,
 env=os.environ.copy()
 )
 elapsed = time.time() - t0
 if result.returncode != 0:
 logger.error(f"STEP [{name}] FAILED (exit code {result.returncode})")
 sys.exit(result.returncode)
 logger.info(f"STEP [{name}] OK in {elapsed:.1f}s")
 return elapsed


def validate_outputs() -> bool:
 """Confirm all expected output figures were created."""
 expected = [
 'figures/SuppFig_S2_Spatial.png',
 'figures/SuppFig_S1_DecisionTree.png',
 ]
 all_ok = True
 for f in expected:
 exists = os.path.exists(f)
 status = 'OK' if exists else 'MISSING'
 logger.info(f" [{status}] {f}")
 if not exists:
 all_ok = False
 return all_ok


if __name__ == '__main__':
 parser = argparse.ArgumentParser(description='VDD Ghana analysis pipeline')
 parser.add_argument('--all', action='store_true', help='Run all steps')
 parser.add_argument('--step', choices=list(STEPS.keys()), help='Run single step')
 parser.add_argument('--validate-only', action='store_true', help='Only validate outputs')
 args = parser.parse_args()

 os.makedirs('figures', exist_ok=True)

 if args.validate_only:
 ok = validate_outputs()
 sys.exit(0 if ok else 1)

 steps_to_run = list(STEPS.keys()) if args.all else ([args.step] if args.step else [])
 if not steps_to_run:
 parser.print_help()
 sys.exit(0)

 total_start = time.time()
 timings = {}
 for name in steps_to_run:
 timings[name] = run_step(name, STEPS[name])

 total = time.time() - total_start
 logger.info(f"\n{'='*60}")
 logger.info("PIPELINE COMPLETE")
 for name, t in timings.items():
 logger.info(f" {name}: {t:.1f}s")
 logger.info(f" TOTAL: {total:.1f}s")
 logger.info(f"{'='*60}")

 ok = validate_outputs()
 if not ok:
 logger.error("Some expected outputs are missing\!")
 sys.exit(1)
