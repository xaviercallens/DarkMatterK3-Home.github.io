#!/usr/bin/env python3
"""
WP-E5 Phase 2/3: 2D transverse detectability sweep over (occupancy, r_s, amplitude).

Label: SYNTHETIC. Every density field in this script is a mock. The only external
number is the transverse extent of `euclid_z_edf_north`, taken from a committed
measurement (provenance in EXTENT_PROVENANCE below), not from a live catalogue
read — so this script performs no real-data access and emits no TEST/FIT label.

This is the rewrite mandated by docs/WP_E5_AUDIT_2026_07_26.md §3. The previous
version was quarantined for: never having run (A-1), never passing r_s to the
deformation (A-2), reporting raw sigma as Delta-sigma (A-3), a fabricated extent
(A-4), and a wrong label (A-5). Each is addressed here and guarded by an
assertion or a persisted diagnostic rather than by a comment.

What changed scientifically. Phase 0 returned NO-GO on real data and Phase 1
closure FAILED at the real field's occupancy (188 objects in a dz=0.20 slice):
the deformed and undeformed fields gave identical beta_1, so the pipeline could
not recover a signal it injected itself. The open question is therefore not
"which (r_s, alpha) does the real field exclude" — it excludes nothing — but
"how many objects would a field need before this statistic responds at all".
Occupancy is consequently a swept axis here, and it is the axis that matters.

Outputs (JSON persisted BEFORE any summary is printed):
  data/derived/wp_e5_sweep_2026_07_26.json
"""

import os
import sys
import json
import argparse

import numpy as np

from pipeline.transverse import generate_mock_slice, resolvable_2d
from pipeline.realfield import density_field_from_catalog
from pipeline.deformation import void_to_filament_deformation
from pipeline.topology2d import compute_betti_numbers_2d
from pipeline.realfield3d import density_shuffle_realization

OUTPUT_JSON = "data/derived/wp_e5_sweep_2026_07_26.json"

# Transverse extent of euclid_z_edf_north, in comoving Mpc.
# PROVENANCE (P1): docs/WP_E4_RESOLVABILITY_FLOOR_2026_07_26.md and
# docs/WP_E3_REALDATA_THIRD_SCHEME_2026_07_26.md §5.1 record voxel edges of
# 6.04 x 6.55 Mpc at nbins=8, hence extent = 8 * (6.04, 6.55) = (48.32, 52.40).
# This is a measured, committed quantity — not an estimate. Checked in-script.
EXTENT_MPC = (48.32, 52.40)
EXTENT_PROVENANCE = (
    "docs/WP_E4_RESOLVABILITY_FLOOR_2026_07_26.md; voxel 6.04 x 6.55 Mpc at nbins=8 "
    "=> extent = 8 * (6.04, 6.55) = (48.32, 52.40) Mpc"
)

NBINS = 32
N_NULL_REALIZATIONS = 40
THRESHOLD_PERCENTILE = 50.0

# Swept axes.
# Occupancy: 188 is the real dz=0.20 slice of edf_north (Phase 0). The rest ask
# how much more would be needed.
N_OBJECTS_GRID = [188, 500, 1000, 2000, 5000, 10000]
R_S_MPC = [0.27, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0]
ALPHA = [0.0, 0.01, 0.1, 0.5, 1.0, 2.0]

DELTA_SIGMA_DETECT = 3.0
DELTA_SIGMA_STRONG = 5.0

RA_RANGE = (0.0, 10.0)
DEC_RANGE = (0.0, 10.0)


def mpc_to_voxels(scale_mpc, extent_mpc, nbins):
    """Convert a physical scale in Mpc to Gaussian sigma in voxel units.

    A-2 fix: this conversion is what the quarantined version promised in its
    docstring and never implemented (it hardcoded R_voxels=2.0, so r_s never
    entered the physics and every row of the grid was bit-identical).
    """
    voxel_x = extent_mpc[0] / nbins
    voxel_y = extent_mpc[1] / nbins
    voxel_mean = 0.5 * (voxel_x + voxel_y)
    return scale_mpc / voxel_mean


def build_null_bank(field, n_realizations, seed_base):
    """Density-shuffle null bank for a given undeformed field."""
    vals = []
    for i in range(n_realizations):
        shuffled = density_shuffle_realization(field, seed=seed_base + i)
        vals.append(compute_betti_numbers_2d(
            shuffled, threshold_percentile=THRESHOLD_PERCENTILE)["beta_1"])
    return np.array(vals, dtype=np.float64)


def sigma_against(observed, null_vals):
    """(observed - null_mean) / null_std, or None when the null has no variance."""
    null_std = float(np.std(null_vals))
    if null_std == 0.0:
        return None
    return (float(observed) - float(np.mean(null_vals))) / null_std


def make_field(n_objects, seed):
    ra, dec = generate_mock_slice(
        n_objects, RA_RANGE, DEC_RANGE, seed, n_clusters=4, clustered_fraction=0.7)
    return density_field_from_catalog(
        ra, dec, z=None, nbins=NBINS, ra_range=RA_RANGE, dec_range=DEC_RANGE)


def classify(delta_sigma):
    """Zone from BASELINE-SUBTRACTED Delta-sigma (E2.11)."""
    if delta_sigma is None:
        return "ZONE_0_UNTESTABLE", "null has zero variance; sigma undefined"
    a = abs(delta_sigma)
    if a < DELTA_SIGMA_DETECT:
        return "ZONE_0_UNTESTABLE", f"|delta_sigma|={a:.2f} < {DELTA_SIGMA_DETECT}"
    if a < DELTA_SIGMA_STRONG:
        return "ZONE_1_DETECTABLE", (
            f"{DELTA_SIGMA_DETECT} <= |delta_sigma|={a:.2f} < {DELTA_SIGMA_STRONG}")
    return "ZONE_2_GENERIC_DEFORMATION_EXCLUDED", (
        f"|delta_sigma|={a:.2f} >= {DELTA_SIGMA_STRONG}; excludes THIS generic warp, "
        "not any vacuum or derived mechanism")


def main():
    ap = argparse.ArgumentParser(description="WP-E5 Phase 2/3 transverse sweep (synthetic)")
    ap.add_argument("--output", default=OUTPUT_JSON)
    args = ap.parse_args()

    # Guard the provenanced constant against silent drift.
    assert abs(EXTENT_MPC[0] - 8 * 6.04) < 1e-9 and abs(EXTENT_MPC[1] - 8 * 6.55) < 1e-9, \
        "EXTENT_MPC no longer matches its cited derivation from the nbins=8 voxel edges"

    voxel_mpc = (EXTENT_MPC[0] / NBINS, EXTENT_MPC[1] / NBINS)
    results = {
        "label": "SYNTHETIC",
        "description": (
            "WP-E5 Phase 2/3: 2D transverse detectability sweep over "
            "(n_objects, r_s, amplitude), baseline-subtracted per E2.11"),
        "nbins": NBINS,
        "extent_mpc": list(EXTENT_MPC),
        "extent_provenance": EXTENT_PROVENANCE,
        "voxel_mpc": list(voxel_mpc),
        "n_null_realizations": N_NULL_REALIZATIONS,
        "threshold_percentile": THRESHOLD_PERCENTILE,
        "n_objects_grid": N_OBJECTS_GRID,
        "r_s_mpc_grid": R_S_MPC,
        "alpha_grid": ALPHA,
        "zone_thresholds": {
            "detect": DELTA_SIGMA_DETECT, "strong": DELTA_SIGMA_STRONG},
        "statistic": "delta_sigma = sigma(alpha) - sigma(alpha=0), E2.11",
        "cells": [],
    }

    print("=" * 74)
    print("WP-E5 PHASE 2/3: TRANSVERSE DETECTABILITY SWEEP (SYNTHETIC)")
    print("=" * 74)
    print(f"extent {EXTENT_MPC} Mpc / nbins {NBINS} -> voxel "
          f"{voxel_mpc[0]:.3f} x {voxel_mpc[1]:.3f} Mpc")

    zone_counts = {}
    baseline_violations = []

    for n_obj in N_OBJECTS_GRID:
        field = make_field(n_obj, seed=1234)
        null_vals = build_null_bank(field, N_NULL_REALIZATIONS, seed_base=5001)
        null_distinct = sorted(set(int(v) for v in null_vals))

        # sigma at zero deformation: the baseline E2.11 requires be subtracted.
        beta_1_base = compute_betti_numbers_2d(
            field, threshold_percentile=THRESHOLD_PERCENTILE)["beta_1"]
        sigma_base = sigma_against(beta_1_base, null_vals)

        print(f"\n[n={n_obj}] null mean={np.mean(null_vals):.3f} "
              f"std={np.std(null_vals):.3f} distinct={null_distinct} | "
              f"beta_1(undeformed)={beta_1_base} sigma_baseline="
              f"{'None' if sigma_base is None else f'{sigma_base:+.2f}'}")

        for r_s in R_S_MPC:
            res = resolvable_2d(r_s, EXTENT_MPC, NBINS, min_voxels=1.0)
            R_voxels = mpc_to_voxels(r_s, EXTENT_MPC, NBINS)

            for alpha in ALPHA:
                cell = {
                    "n_objects": n_obj, "r_s_mpc": r_s, "alpha": alpha,
                    "R_voxels": float(R_voxels),
                    "resolvability_verdict": res["verdict"],
                    "null_mean": float(np.mean(null_vals)),
                    "null_std": float(np.std(null_vals)),
                    "null_distinct_values": null_distinct,
                    "beta_1_undeformed": int(beta_1_base),
                    "sigma_baseline": None if sigma_base is None else float(sigma_base),
                }

                # E2.16: resolvability is a PRECONDITION, checked before statistics.
                if res["verdict"] == "UNRESOLVABLE":
                    cell.update({
                        "zone": "ZONE_0_UNRESOLVABLE",
                        "reason": res["note"],
                        "delta_sigma": None,
                    })
                    results["cells"].append(cell)
                    zone_counts["ZONE_0_UNRESOLVABLE"] = \
                        zone_counts.get("ZONE_0_UNRESOLVABLE", 0) + 1
                    continue

                deformed = void_to_filament_deformation(
                    field, R_voxels=R_voxels, amplitude=alpha)
                beta_1_def = compute_betti_numbers_2d(
                    deformed, threshold_percentile=THRESHOLD_PERCENTILE)["beta_1"]
                sigma_def = sigma_against(beta_1_def, null_vals)

                if sigma_def is None or sigma_base is None:
                    delta_sigma = None
                else:
                    delta_sigma = float(sigma_def - sigma_base)

                # A-3 negative control, enforced not asserted-in-prose: alpha=0 is an
                # exact identity, so its baseline-subtracted Delta-sigma MUST be 0.
                if alpha == 0.0:
                    if not np.array_equal(deformed, field.astype(np.float64)):
                        baseline_violations.append(
                            {"n_objects": n_obj, "r_s_mpc": r_s,
                             "why": "amplitude=0 was not a bit-exact identity"})
                    if delta_sigma is not None and delta_sigma != 0.0:
                        baseline_violations.append(
                            {"n_objects": n_obj, "r_s_mpc": r_s,
                             "why": f"delta_sigma={delta_sigma} at alpha=0, expected 0"})

                zone, reason = classify(delta_sigma)
                cell.update({
                    "beta_1_deformed": int(beta_1_def),
                    "sigma_deformed": None if sigma_def is None else float(sigma_def),
                    "delta_sigma": delta_sigma,
                    "zone": zone, "reason": reason,
                })
                results["cells"].append(cell)
                zone_counts[zone] = zone_counts.get(zone, 0) + 1

    results["zone_summary"] = zone_counts
    results["baseline_control_violations"] = baseline_violations
    results["baseline_control_passed"] = (len(baseline_violations) == 0)

    # Persist BEFORE printing anything summary-shaped (WP-E3 lesson).
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[sweep] Results persisted to {args.output}")

    print("\n" + "=" * 74)
    print("ZONE SUMMARY")
    print("=" * 74)
    for zone in sorted(zone_counts):
        print(f"  {zone}: {zone_counts[zone]}")
    print(f"\n  alpha=0 baseline control: "
          f"{'PASS' if results['baseline_control_passed'] else 'FAIL'} "
          f"({len(baseline_violations)} violation(s))")

    # Detectability frontier: smallest occupancy at which anything is detectable.
    detect = [c for c in results["cells"]
              if c["zone"] in ("ZONE_1_DETECTABLE", "ZONE_2_GENERIC_DEFORMATION_EXCLUDED")]
    if detect:
        n_min = min(c["n_objects"] for c in detect)
        print(f"\n  Smallest occupancy with any detectable cell: n={n_min}")
    else:
        print("\n  No cell at any occupancy reached |delta_sigma| >= "
              f"{DELTA_SIGMA_DETECT}.")
    print("=" * 74 + "\n")

    if not results["baseline_control_passed"]:
        print("[sweep] ABORT-WORTHY: the alpha=0 negative control failed. "
              "Delta-sigma is not baseline-subtracted correctly.")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Generated-by: Claude Opus 5 (Stream 3) | Verified-by: rewrite of the quarantined
# version against docs/WP_E5_AUDIT_2026_07_26.md §3; r_s -> R_voxels conversion live
# (A-2), Delta-sigma baseline-subtracted per E2.11 with an enforced alpha=0 == 0
# negative control that exits nonzero (A-3), extent provenanced and assertion-checked
# (A-4), label SYNTHETIC (A-5), resolvability checked before statistics (E2.16) |
# Reviewed-by: pending T0
