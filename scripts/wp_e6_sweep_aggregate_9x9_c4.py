#!/usr/bin/env python3
"""WP-E6-SWEEP — 9×9 band aggregation under ruling C4(b): drop the members beyond the data provider's recommended k cut.

Authority (taken on T0's behalf, T0's instruction of 2026-10-10 "implement on my behalf"; see
`briefs/T0_RULING_SWEEP_C1_C5_EB_2026_10_10.md`, NOT YET PINNED until that file is merged and named by REAL_DATA_RULING_PIN):
  C4(b): "drop those 3 members and re-aggregate band 8 from 7 members" (T0_DECISION_REQUEST_SWEEP_THEORY_CORRECTIONS addendum).

The cut is the provider's own (arXiv:2505.07974 sec. 5.4 item 1): k < 0.5 π / R_z, R_z = c Δλ_DESI / ((1+z) λ_Lyα),
Δλ_DESI = 0.8 Å. It is COMPUTED here from those constants (z = 4.2), not typed. Everything else is the pinned v1 aggregation
(inverse-variance diagonal weights, full member covariance propagated; pipeline/binmap.aggregate_bands), unchanged: the only change
is the member set. The v1 artifacts are not modified; this writes NEW files with a `_c4_` tag.

This script performs no model comparison. It reads the hash-gated real covariance (as the v1 script did) and the published P1D
vector at z = 4.2; the vector is aggregated, never fitted here. Outputs feed the sweep only after the ruling is pinned.

    python3 scripts/wp_e6_sweep_aggregate_9x9_c4.py
Controls: checkers/tests/test_wp_e6_sweep_c4.py
Generated-by: Claude (Sonnet 5.5), Stream 3 support, 2026-10-10 | Reviewed-by: N
"""
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "pipeline"))
import binmap  # noqa: E402

DESI_CSV = REPO_ROOT / "data" / "literature" / "desi_dr1_lya_p1d_2026_07_27.csv"
FITS_PATH = REPO_ROOT / "data" / "raw" / "desi_dr1_lya_p1d_zenodo" / binmap.COVARIANCE_FITS_NAME
OUT_NPY = REPO_ROOT / "data" / "derived" / "wp_e6_sweep_cov_agg9_c4_z4p2_2026_10_10.npy"
OUT_JSON = REPO_ROOT / "data" / "derived" / "wp_e6_sweep_cov_agg9_c4_z4p2_2026_10_10.json"

C_KMS = 299792.458          # km/s
DELTA_LAMBDA_A = 0.8         # Å, DESI spectrograph (arXiv:2505.07974 sec. 5.4 item 1)
LAMBDA_LYA_A = 1215.67       # Å
Z = 4.2
EXPECTED_DROPPED = 3         # the count the decision request states (checked, not assumed)


def k_cut(z=Z):
    r_z = C_KMS * DELTA_LAMBDA_A / ((1.0 + z) * LAMBDA_LYA_A)      # km/s
    return 0.5 * math.pi / r_z, r_z


def apply_cut(map_out, k_max):
    """Return (filtered map_out, dropped) — members with k > k_max removed from whichever band holds them."""
    dropped = []
    for band in map_out["bands"]:
        keep = [i for i, k in enumerate(band["member_k_values"]) if k <= k_max]
        if len(keep) != len(band["members"]):
            for i, k in enumerate(band["member_k_values"]):
                if k > k_max:
                    dropped.append({"bin_index": band["bin_index"], "csv_row": band["members"][i], "k": k})
        band["members"] = [band["members"][i] for i in keep]
        band["member_k_values"] = [band["member_k_values"][i] for i in keep]
        band["member_log10k_values"] = [band["member_log10k_values"][i] for i in keep]
        band["member_count"] = len(keep)
        band["all_within_nyquist"] = True
    return map_out, dropped


def main():
    if not FITS_PATH.exists():
        print(f"FITS not found: {FITS_PATH}\nRun: python scripts/fetch_data.py")
        return 1
    kmax, r_z = k_cut()
    map_out = binmap.restriction_map(str(DESI_CSV), z_target=4.2)
    vres = binmap.verify_bins(map_out)
    if not vres["passes"]:
        print(f"verify_bins() FAILED before the cut: {vres}")
        return 1
    n_before = [len(b["members"]) for b in map_out["bands"]]
    map_out, dropped = apply_cut(map_out, kmax)
    n_after = [len(b["members"]) for b in map_out["bands"]]
    if len(dropped) != EXPECTED_DROPPED or {d["bin_index"] for d in dropped} != {8}:
        print(f"REFUSED: expected exactly {EXPECTED_DROPPED} members dropped, all in band 8; got {dropped}")
        return 2
    result = binmap.covariance_block(map_out, covariance_fits_path=str(FITS_PATH))
    agg = result["aggregation"]
    np.save(OUT_NPY, agg["cov_agg"])
    payload = {
        "label": "DRAFT (ENGINEERING/DESIGN — not TEST, not FIT); consuming comparisons: exclusion/FIT",
        "wp": "WP-E6-SWEEP (aggregation step, ruling C4(b))",
        "authority": ("T0's instruction 2026-10-10 'implement on my behalf' (briefs/T0_RULING_SWEEP_C1_C5_EB_2026_10_10.md); "
                      "pinned v1 rule otherwise unchanged (briefs/WP_E6_SWEEP_DESIGN_PINNED_2026_09_16.md Sec.1.2)"),
        "rule": agg["rule"],
        "k_cut": {"k_max_s_per_km": kmax, "R_z_kms": r_z, "source": "arXiv:2505.07974 sec. 5.4 item 1: k < 0.5*pi/R_z",
                  "constants": {"c_kms": C_KMS, "delta_lambda_A": DELTA_LAMBDA_A, "lambda_lya_A": LAMBDA_LYA_A, "z": Z}},
        "members_before": n_before, "members_after": n_after, "dropped": dropped,
        "generated": datetime.now(timezone.utc).isoformat(),
        "matrix_npy": OUT_NPY.name, "matrix_shape": list(agg["cov_agg"].shape),
        "member_csv_indices": result["member_csv_indices"], "grouping": result["grouping"],
        "weights_9xn": agg["weights"].tolist(), "row_sums": agg["weights"].sum(axis=1).tolist(),
        "data_agg_p1d_kms": agg["data_agg"].tolist(), "k_eff_s_per_km": agg["k_eff"].tolist(),
        "k_target_s_per_km": [g["k_target"] for g in agg["bands"]],
        "k_eff_over_k_target": agg["k_eff_over_k_target"].tolist(),
        "diag_if_uncorrelated": agg["diag_if_uncorrelated"].tolist(),
        "diag_actual": np.diag(agg["cov_agg"]).tolist(),
        "checks": agg["checks"], "member_checks": result["checks"],
        "eigenvalues": agg["eigenvalues"], "condition_number": agg["condition_number"],
        "hartlap": "none — survey-published covariance, not a mock sample covariance (design doc Sec.1.3)",
        "provenance": result["provenance"],
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2))
    print(f"k_max = {kmax:.6f} s/km (R_z = {r_z:.4f} km/s); dropped {len(dropped)} member(s) from band 8")
    print(f"members per band: {n_before} -> {n_after}")
    print(f"checks: {agg['checks']}; condition number {agg['condition_number']:.4f}")
    print(f"wrote {OUT_NPY.name} and {OUT_JSON.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
