#!/usr/bin/env python3
"""The only entry point for datasets (CLAUDE.md Commands).

Gate-aware: refuses to run until PREDICTION.md is pinned (gate G1). Once
pinned, this script is where NANOGrav/EPTA/lensing/Lyman-alpha fetches get
implemented (EXECUTION_PLAN.md WP S3-01) — idempotent, checksummed, and
recorded in data/MANIFEST.md. Not implemented yet: the model has no pinned
observable to fetch data for.
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.gate import GateError, require_pinned_for_real_data  # noqa: E402


def main() -> int:
    try:
        require_pinned_for_real_data()
    except GateError as e:
        print(f"fetch_data.py refuses to run: {e}", file=sys.stderr)
        return 1

    # Reached only once PREDICTION.md is pinned (gate G1 open) — WP S3-01
    # (NANOGrav/EPTA/lensing/Lyman-alpha fetch + data/MANIFEST.md) goes here.
    print("Gate G1 is open but no dataset fetchers are implemented yet "
          "(WP S3-01 pending).", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
