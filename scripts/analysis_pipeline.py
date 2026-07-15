"""End-to-end reproducibility wrapper for the Vitamin D Ghana repository."""
from __future__ import annotations

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
        'label': "Export locked spatial summary",
        'script': 'scripts/spatial_analysis.py',
    },
    'dt': {
        'label': 'CART sensitivity analysis',
        'script': 'scripts/decision_tree.py',
    },
}

EXPECTED_OUTPUTS = [
    'data/cart_feature_matrix.csv',
    'data/regional_aggregation.csv',
    'outputs/data/cart_results.json',
    'outputs/data/spatial_results.json',
]


def run_step(name: str, config: dict) -> float:
    """Execute a single pipeline step and return elapsed seconds."""
    logger.info("=" * 60)
    logger.info("STEP [%s]: %s", name, config['label'])
    logger.info("=" * 60)
    t0 = time.time()
    result = subprocess.run(
        [sys.executable, config['script']],
        capture_output=False,
        env=os.environ.copy(),
        check=False,
    )
    elapsed = time.time() - t0
    if result.returncode != 0:
        logger.error("STEP [%s] FAILED (exit code %s)", name, result.returncode)
        sys.exit(result.returncode)
    logger.info("STEP [%s] OK in %.1fs", name, elapsed)
    return elapsed


def validate_outputs() -> bool:
    """Confirm expected reproducibility outputs were created."""
    all_ok = True
    for path in EXPECTED_OUTPUTS:
        exists = os.path.exists(path)
        status = 'OK' if exists else 'MISSING'
        logger.info(" [%s] %s", status, path)
        if not exists:
            all_ok = False
    return all_ok


def main() -> int:
    parser = argparse.ArgumentParser(description='Vitamin D Ghana reproducibility pipeline')
    parser.add_argument('--all', action='store_true', help='Run all steps')
    parser.add_argument('--step', choices=list(STEPS.keys()), help='Run single step')
    parser.add_argument('--validate-only', action='store_true', help='Only validate outputs')
    args = parser.parse_args()

    if args.validate_only:
        return 0 if validate_outputs() else 1

    steps_to_run = list(STEPS.keys()) if args.all else ([args.step] if args.step else [])
    if not steps_to_run:
        parser.print_help()
        return 0

    total_start = time.time()
    timings = {}
    for name in steps_to_run:
        timings[name] = run_step(name, STEPS[name])

    total = time.time() - total_start
    logger.info("=" * 60)
    logger.info("PIPELINE COMPLETE")
    for name, elapsed in timings.items():
        logger.info(" %s: %.1fs", name, elapsed)
    logger.info(" TOTAL: %.1fs", total)
    logger.info("=" * 60)

    return 0 if validate_outputs() else 1


if __name__ == '__main__':
    sys.exit(main())
