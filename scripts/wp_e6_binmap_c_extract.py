#!/usr/bin/env python3
"""WP-E6-BINMAP-C — Real DESI DR1 P1D covariance sub-block extraction runner.

Authority: `briefs/T1_DELEGATED_RULINGS_2026_07_31.md` R2 (executing T0-ratified
D1 `dbf1337`). ENGINEERING / DESIGN, DRAFT label (CLAUDE.md rule 3 — not TEST,
not FIT): this script performs no model comparison; it extracts and verifies
the survey's own published covariance.

One-command reproduction:
    python scripts/fetch_data.py            # fetch + SHA-256 hard gate
    python scripts/wp_e6_binmap_c_extract.py

Reads the hash-gated Zenodo FITS (data/raw/, gitignored), runs
pipeline.binmap.covariance_block() (which re-verifies the SHA-256 pin and the
three mandatory cross-checks), and writes the small derived artifacts to the
tracked data/derived/:
  - wp_e6_binmap_c_cov_member66_z4p2_2026_07_31.npy   (66x66 member-level block)
  - wp_e6_binmap_c_cov_z4p2_2026_07_31.json           (grouping, checks, spectrum)
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "pipeline"))
import binmap  # noqa: E402

DESI_CSV = REPO_ROOT / "data" / "literature" / "desi_dr1_lya_p1d_2026_07_27.csv"
FITS_PATH = (REPO_ROOT / "data" / "raw" / "desi_dr1_lya_p1d_zenodo"
             / binmap.COVARIANCE_FITS_NAME)
OUT_NPY = REPO_ROOT / "data" / "derived" / "wp_e6_binmap_c_cov_member66_z4p2_2026_07_31.npy"
OUT_JSON = REPO_ROOT / "data" / "derived" / "wp_e6_binmap_c_cov_z4p2_2026_07_31.json"


def main() -> int:
    if not FITS_PATH.exists():
        print(f"FITS not found: {FITS_PATH}\nRun: python scripts/fetch_data.py")
        return 1

    map_out = binmap.restriction_map(str(DESI_CSV), z_target=4.2)
    vres = binmap.verify_bins(map_out)
    if not vres["passes"]:
        print(f"verify_bins() FAILED: {vres}")
        return 1

    # covariance_block enforces the SHA-256 hard gate + 3 mandatory checks.
    result = binmap.covariance_block(map_out, covariance_fits_path=str(FITS_PATH))

    np.save(OUT_NPY, result["cov_member"])
    payload = {
        "label": "DRAFT (ENGINEERING/DESIGN — not TEST, not FIT)",
        "wp": "WP-E6-BINMAP-C",
        "authority": ("briefs/T1_DELEGATED_RULINGS_2026_07_31.md R2, executing "
                      "T0 ratification D1 (dbf1337)"),
        "generated": datetime.now(timezone.utc).isoformat(),
        "matrix_npy": OUT_NPY.name,
        "matrix_shape": list(result["cov_member"].shape),
        "member_csv_indices": result["member_csv_indices"],
        "grouping": result["grouping"],
        "checks": result["checks"],
        "eigenvalues": result["eigenvalues"],
        "condition_number": result["condition_number"],
        "aggregated_9x9": result["aggregated_9x9"],
        "aggregation_note": result["aggregation_note"],
        "provenance": result["provenance"],
        "binmap_verify_bins": vres,
    }
    with open(OUT_JSON, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {OUT_NPY} and {OUT_JSON}")
    print(f"checks: {result['checks']}")
    print(f"condition number: {result['condition_number']:.4f}")
    print(f"eigenvalue range: [{min(result['eigenvalues']):.6g}, "
          f"{max(result['eigenvalues']):.6g}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
