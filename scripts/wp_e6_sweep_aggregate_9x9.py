#!/usr/bin/env python3
"""WP-E6-SWEEP — 9×9 band-aggregated DESI DR1 P1D covariance + observed vector.

Authority: T0 ruling A1 2026-09-16 (Option 1), pinned in
`briefs/WP_E6_SWEEP_DESIGN_PINNED_2026_09_16.md` §1 (pin commit 79c9444).
ENGINEERING / DESIGN, DRAFT label (CLAUDE.md rule 3): this script performs no
model comparison. Every comparison that consumes its output is exclusion/FIT
(design doc §1.4; TUNING_LOG.md row 2026-09-16).

One-command reproduction:
    python scripts/fetch_data.py                 # fetch + SHA-256 hard gate
    python scripts/wp_e6_sweep_aggregate_9x9.py

Reads the hash-gated Zenodo FITS (data/raw/, gitignored) through
pipeline.binmap.covariance_block() — which re-verifies the SHA-256 pin, the
three mandatory member-level cross-checks, and now applies the pinned
aggregation — and writes the tracked derived artifacts:
  - data/derived/wp_e6_sweep_cov_agg9_z4p2_2026_09_16.npy   (9×9 C_9)
  - data/derived/wp_e6_sweep_cov_agg9_z4p2_2026_09_16.json  (W, P_9, k_eff, checks)
The 2026-07-31 BINMAP-C member-level artifacts are not modified.
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
OUT_NPY = REPO_ROOT / "data" / "derived" / "wp_e6_sweep_cov_agg9_z4p2_2026_09_16.npy"
OUT_JSON = REPO_ROOT / "data" / "derived" / "wp_e6_sweep_cov_agg9_z4p2_2026_09_16.json"


def main() -> int:
    if not FITS_PATH.exists():
        print(f"FITS not found: {FITS_PATH}\nRun: python scripts/fetch_data.py")
        return 1

    map_out = binmap.restriction_map(str(DESI_CSV), z_target=4.2)
    vres = binmap.verify_bins(map_out)
    if not vres["passes"]:
        print(f"verify_bins() FAILED: {vres}")
        return 1

    result = binmap.covariance_block(map_out, covariance_fits_path=str(FITS_PATH))
    agg = result["aggregation"]

    np.save(OUT_NPY, agg["cov_agg"])
    payload = {
        "label": "DRAFT (ENGINEERING/DESIGN — not TEST, not FIT); consuming comparisons: exclusion/FIT",
        "wp": "WP-E6-SWEEP (aggregation step)",
        "authority": ("T0 ruling A1 2026-09-16, Option 1; pinned design "
                      "briefs/WP_E6_SWEEP_DESIGN_PINNED_2026_09_16.md Sec.1 (pin commit 79c9444)"),
        "rule": agg["rule"],
        "generated": datetime.now(timezone.utc).isoformat(),
        "matrix_npy": OUT_NPY.name,
        "matrix_shape": list(agg["cov_agg"].shape),
        "source_member_matrix": "wp_e6_binmap_c_cov_member66_z4p2_2026_07_31.npy (identical content re-extracted from the FITS this run)",
        "member_csv_indices": result["member_csv_indices"],
        "grouping": result["grouping"],
        "weights_9x66": agg["weights"].tolist(),
        "row_sums": agg["weights"].sum(axis=1).tolist(),
        "data_agg_p1d_kms": agg["data_agg"].tolist(),
        "k_eff_s_per_km": agg["k_eff"].tolist(),
        "k_target_s_per_km": [g["k_target"] for g in agg["bands"]],
        "k_eff_over_k_target": agg["k_eff_over_k_target"].tolist(),
        "diag_if_uncorrelated": agg["diag_if_uncorrelated"].tolist(),
        "diag_actual": np.diag(agg["cov_agg"]).tolist(),
        "checks": agg["checks"],
        "member_checks": result["checks"],
        "eigenvalues": agg["eigenvalues"],
        "condition_number": agg["condition_number"],
        "hartlap": "none — survey-published covariance, not a mock sample covariance (design doc Sec.1.3)",
        "provenance": result["provenance"],
        "binmap_verify_bins": vres,
    }
    with open(OUT_JSON, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {OUT_NPY} and {OUT_JSON}")
    print(f"checks: {agg['checks']}")
    print(f"condition number: {agg['condition_number']:.4f}")
    for b, (ke, kt, r) in enumerate(zip(agg["k_eff"], payload["k_target_s_per_km"],
                                        agg["k_eff_over_k_target"])):
        print(f"  band {b}: k_eff={ke:.6f} k_target={kt:.6f} ratio={r:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
