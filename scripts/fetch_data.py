#!/usr/bin/env python3
"""S3-01 — The only entry point for datasets (CLAUDE.md Commands).

Gate-aware: refuses to run until PREDICTION.md is pinned (gate G1). Once
pinned, this script fetches NANOGrav/EPTA (PTA observable P2), lensing (P1),
and Lyman-α constraints — idempotent, checksummed, and recorded in
data/MANIFEST.md. See scripts/data_fetchers.py for individual dataset
implementations.
"""
import logging
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.gate import GateError, require_pinned_for_real_data  # noqa: E402
from scripts.data_fetchers import fetch_all_datasets  # noqa: E402
from scripts.manifest import update_manifest  # noqa: E402

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> int:
    try:
        require_pinned_for_real_data()
    except GateError as e:
        logger.error(f"fetch_data.py refuses to run: {e}")
        return 1

    # Reached only once PREDICTION.md is pinned (gate G1 open) — WP S3-01
    logger.info("Gate G1 is open. Fetching datasets for S3 observables (P1, P2)...")

    try:
        results = fetch_all_datasets()
        update_manifest(results)
        logger.info("All datasets fetched and checksummed. data/MANIFEST.md updated.")
        return 0
    except Exception as e:
        logger.error(f"Dataset fetch failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
