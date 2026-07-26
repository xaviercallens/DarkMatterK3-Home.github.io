#!/usr/bin/env python3
"""
WP-E5 Phase 2/3: 2D transverse detectability sweep over (occupancy, r_s, amplitude).

Label: SYNTHETIC. Every density field here is a mock. The only external quantity is
the transverse extent of `euclid_z_edf_north`, taken from a committed measurement
(EXTENT_PROVENANCE below) rather than a live catalogue read — so this performs no
real-data access and emits no TEST/FIT label.

Rewritten per docs/WP_E5_AUDIT_2026_07_26.md §3 (the previous version was
quarantined for never running, never passing r_s to the deformation, reporting raw
sigma as Delta-sigma, a fabricated extent, and a wrong label). Then revised again
after self-review; see §"Revision 2" below.

WHY OCCUPANCY IS THE SWEPT AXIS
Phase 0 returned NO-GO on real data and Phase 1 closure FAILED at the real field's
occupancy: deformed and undeformed fields gave identical beta_1, so the pipeline
could not recover a signal it injected itself. The live question is therefore not
"which (r_s, alpha) does the real field exclude" — it excludes nothing — but "how
much data would this statistic need before it responds at all".

STATISTIC
    Delta_sigma(alpha) = sigma(alpha) - sigma(0),  both against the SAME null bank.

Because both terms share one null bank, the null MEAN cancels exactly:
    Delta_sigma = (beta_1(alpha) - beta_1(0)) / sigma_null
This matters beyond tidiness. The open objection to E2.11 under Deep Think review
(briefs/DEEPTHINK_REVIEW_REQUEST_BASELINE_2026_07_26.md §4.1) is that differencing
two sigmas with DIFFERENT denominators is an artifact generator. That objection does
not reach this implementation: one denominator, and the baseline offset cancels
identically rather than approximately.

REVISION 2 (self-review, 2026-07-26) — three defects found in the first rewrite:
  1. Scalar R_voxels made the deformation anisotropic in Mpc (voxel is 1.510 x
     1.637 Mpc, an ~8% axis asymmetry). Now a per-axis sigma, isotropic in Mpc.
  2. One mock realization per occupancy meant the whole map was a single draw with
     no scatter. Now N_FIELD_REALIZATIONS per cell, with mean and std reported and
     classification on the mean.
  3. The 50th-percentile threshold does NOT deliver a 50% fill on a sparse counts
     field — ties at zero dominate, and the measured fill ran 8.4% (n=188) to 48.0%
     (n=2000). Occupancy was therefore confounded with mask geometry. Both threshold
     modes are now run: `percentile` (as before, for continuity) and `matched_fill`.
  4. At a FIXED threshold the deformation changes the mask SIZE, so beta_1 moved for
     a non-topological reason: measured fill at n=10000 ran 39.6% (undeformed) ->
     47.8% (alpha=0.01) -> 31.5% (alpha=2.0), via tie-breaking of the many cells
     sitting exactly at the percentile of a discrete counts field. That is the
     spurious +5.06 sigma at alpha=0.01. `matched_fill` holds the mask SIZE at the
     baseline's achieved fill, so a beta_1 difference reflects ARRANGEMENT.
  5. A null bank too degenerate to support a Gaussian sigma is now refused up front
     by pipeline.resolvability.null_degeneracy (ZONE_0_DEGENERATE_NULL) — the
     statistical sibling of the resolvability guard.

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
from pipeline.topology2d import compute_betti_numbers_2d, threshold_for_fill_fraction
from pipeline.realfield3d import density_shuffle_realization
from pipeline.resolvability import null_degeneracy

OUTPUT_JSON = "data/derived/wp_e5_sweep_2026_07_26.json"

# Transverse extent of euclid_z_edf_north, comoving Mpc.
# PROVENANCE (P1): docs/WP_E4_RESOLVABILITY_FLOOR_2026_07_26.md and
# docs/WP_E3_REALDATA_THIRD_SCHEME_2026_07_26.md §5.1 record voxel edges of
# 6.04 x 6.55 Mpc at nbins=8, hence extent = 8 * (6.04, 6.55). Asserted in main().
EXTENT_MPC = (48.32, 52.40)
EXTENT_PROVENANCE = (
    "docs/WP_E4_RESOLVABILITY_FLOOR_2026_07_26.md; voxel 6.04 x 6.55 Mpc at nbins=8 "
    "=> extent = 8 * (6.04, 6.55) = (48.32, 52.40) Mpc"
)

NBINS = 32
N_NULL_REALIZATIONS = 40
N_FIELD_REALIZATIONS = 5
FIELD_SEEDS = [1234, 2345, 3456, 4567, 5678]

THRESHOLD_PERCENTILE = 50.0

N_OBJECTS_GRID = [188, 500, 1000, 2000, 5000, 10000]
R_S_MPC = [0.27, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0]
ALPHA = [0.0, 0.01, 0.1, 0.5, 1.0, 2.0]

DELTA_SIGMA_DETECT = 3.0
DELTA_SIGMA_STRONG = 5.0

RA_RANGE = (0.0, 10.0)
DEC_RANGE = (0.0, 10.0)


def mpc_to_voxels_per_axis(scale_mpc, extent_mpc, nbins):
    """Physical scale (Mpc) -> per-axis Gaussian sigma in voxel units.

    Returns one sigma per array axis so the deformation is isotropic in Mpc rather
    than in voxels. The first array axis of the binned field corresponds to the
    first extent entry (see density_field_from_catalog's (ra, dec) binning order).
    """
    voxel_x = extent_mpc[0] / nbins
    voxel_y = extent_mpc[1] / nbins
    return (scale_mpc / voxel_x, scale_mpc / voxel_y)


def build_null_bank(field, threshold_value, n_realizations, seed_base):
    """Density-shuffle null bank at a FIXED threshold value.

    The threshold is passed explicitly rather than recomputed per realization: a
    shuffle preserves the value multiset exactly, so recomputing a percentile would
    give the same number anyway, but fixing it makes that independence explicit and
    keeps the null comparable to the observed field cell-for-cell.
    """
    vals = []
    for i in range(n_realizations):
        shuffled = density_shuffle_realization(field, seed=seed_base + i)
        vals.append(compute_betti_numbers_2d(
            shuffled, threshold_value=threshold_value)["beta_1"])
    return np.array(vals, dtype=np.float64)


def make_field(n_objects, seed):
    ra, dec = generate_mock_slice(
        n_objects, RA_RANGE, DEC_RANGE, seed, n_clusters=4, clustered_fraction=0.7)
    return density_field_from_catalog(
        ra, dec, z=None, nbins=NBINS, ra_range=RA_RANGE, dec_range=DEC_RANGE)


def pick_threshold(field, mode):
    """(threshold_value, achieved_fill) for the BASELINE field under a given mode."""
    if mode in ("percentile", "matched_fill"):
        t = float(np.percentile(field, THRESHOLD_PERCENTILE))
        return t, float((field > t).mean())
    raise ValueError(f"unknown threshold mode {mode!r}")


def threshold_for_deformed(deformed, mode, baseline_threshold, baseline_fill):
    """Threshold to apply to a DEFORMED field, and the fill it achieves.

    This choice is not cosmetic; it decides what the statistic measures.

    `percentile` keeps the baseline's threshold VALUE. The deformation then
    changes the mask SIZE, and beta_1 moves for a reason that has nothing to do
    with topology. Measured at n=10000: fill runs 39.6% (undeformed) -> 47.8%
    (alpha=0.01) -> 31.5% (alpha=2.0). The mechanism is tie-breaking — the binned
    counts field has many cells tied exactly at the percentile, and an arbitrarily
    small smooth perturbation pushes that whole tied block across a fixed
    threshold. That is the origin of the spurious +5.06 sigma at alpha=0.01, an
    amplitude far too small to restructure anything.

    `matched_fill` instead keeps the mask SIZE fixed at the baseline's achieved
    fill, so a beta_1 difference reflects the ARRANGEMENT of mass rather than how
    many cells happen to sit above a number. This is the comparison the sweep is
    actually trying to make.
    """
    if mode == "percentile":
        return baseline_threshold, float((deformed > baseline_threshold).mean())
    if mode == "matched_fill":
        return threshold_for_fill_fraction(deformed, baseline_fill)
    raise ValueError(f"unknown threshold mode {mode!r}")


def classify(delta_sigma):
    """Zone from BASELINE-SUBTRACTED Delta-sigma (E2.11)."""
    if delta_sigma is None or not np.isfinite(delta_sigma):
        return "ZONE_0_UNTESTABLE", "null has zero variance; sigma undefined"
    a = abs(delta_sigma)
    if a < DELTA_SIGMA_DETECT:
        return "ZONE_0_UNTESTABLE", f"|mean delta_sigma|={a:.2f} < {DELTA_SIGMA_DETECT}"
    if a < DELTA_SIGMA_STRONG:
        return "ZONE_1_DETECTABLE", (
            f"{DELTA_SIGMA_DETECT} <= |mean delta_sigma|={a:.2f} < {DELTA_SIGMA_STRONG}")
    return "ZONE_2_GENERIC_DEFORMATION_EXCLUDED", (
        f"|mean delta_sigma|={a:.2f} >= {DELTA_SIGMA_STRONG}; excludes THIS generic "
        "warp, not any vacuum or derived mechanism")


def run_mode(mode, results):
    """Sweep one thresholding mode. Returns (zone_counts, control_violations)."""
    zone_counts = {}
    violations = []
    cells = []
    per_occupancy = {}

    print(f"\n{'=' * 74}\nTHRESHOLD MODE: {mode}\n{'=' * 74}")

    for n_obj in N_OBJECTS_GRID:
        # Per-realization state, built once and reused across the (r_s, alpha) grid.
        realizations = []
        for seed in FIELD_SEEDS:
            field = make_field(n_obj, seed)
            thr, fill = pick_threshold(field, mode)
            null_vals = build_null_bank(field, thr, N_NULL_REALIZATIONS, seed_base=5001)
            null_std = float(np.std(null_vals))
            beta_1_base = compute_betti_numbers_2d(field, threshold_value=thr)["beta_1"]
            realizations.append({
                "seed": seed, "field": field, "threshold": thr, "fill": fill,
                "null_vals": null_vals, "null_std": null_std,
                "beta_1_base": int(beta_1_base),
                "null_distinct": len(set(int(v) for v in null_vals)),
                # Statistical precondition, checked alongside the spatial one.
                "null_verdict": null_degeneracy(null_vals),
            })

        fills = [r["fill"] for r in realizations]
        stds = [r["null_std"] for r in realizations]
        distincts = [r["null_distinct"] for r in realizations]
        per_occupancy[str(n_obj)] = {
            "mask_fill_mean": float(np.mean(fills)),
            "occupied_fraction_mean": float(np.mean(
                [(r["field"] > 0).mean() for r in realizations])),
            "null_std_mean": float(np.mean(stds)),
            "null_distinct_values_mean": float(np.mean(distincts)),
            "beta_1_baseline_per_realization": [r["beta_1_base"] for r in realizations],
        }
        print(f"[n={n_obj:>5}] fill={np.mean(fills):.1%} "
              f"occupied={per_occupancy[str(n_obj)]['occupied_fraction_mean']:.1%} "
              f"null_std={np.mean(stds):.2f} null_distinct={np.mean(distincts):.1f} "
              f"beta_1_base={[r['beta_1_base'] for r in realizations]}")

        for r_s in R_S_MPC:
            res = resolvable_2d(r_s, EXTENT_MPC, NBINS, min_voxels=1.0)
            sigma_vox = mpc_to_voxels_per_axis(r_s, EXTENT_MPC, NBINS)

            for alpha in ALPHA:
                cell = {
                    "threshold_mode": mode, "n_objects": n_obj, "r_s_mpc": r_s,
                    "alpha": alpha, "R_voxels_per_axis": list(sigma_vox),
                    "resolvability_verdict": res["verdict"],
                    "mask_fill_mean": float(np.mean(fills)),
                    "null_std_mean": float(np.mean(stds)),
                    "null_distinct_values_mean": float(np.mean(distincts)),
                }

                # E2.16: resolvability is a PRECONDITION, checked before statistics.
                if res["verdict"] == "UNRESOLVABLE":
                    cell.update({"zone": "ZONE_0_UNRESOLVABLE",
                                 "reason": res["note"],
                                 "delta_sigma_mean": None, "delta_sigma_std": None})
                    cells.append(cell)
                    zone_counts["ZONE_0_UNRESOLVABLE"] = \
                        zone_counts.get("ZONE_0_UNRESOLVABLE", 0) + 1
                    continue

                # Statistical precondition, same standing as the spatial one: if the
                # null cannot support a Gaussian sigma, no sigma computed against it
                # may be reported as a detection, however large it looks. This is the
                # mechanical fix for the artifact class that has appeared five times.
                n_degenerate = sum(r["null_verdict"]["degenerate"] for r in realizations)
                if n_degenerate > len(realizations) // 2:
                    cell.update({
                        "zone": "ZONE_0_DEGENERATE_NULL",
                        "reason": (f"{n_degenerate}/{len(realizations)} realizations have "
                                   f"a degenerate null: "
                                   f"{realizations[0]['null_verdict']['note']}"),
                        "delta_sigma_mean": None, "delta_sigma_std": None,
                        "n_realizations_degenerate_null": int(n_degenerate),
                    })
                    cells.append(cell)
                    zone_counts["ZONE_0_DEGENERATE_NULL"] = \
                        zone_counts.get("ZONE_0_DEGENERATE_NULL", 0) + 1
                    continue

                deltas = []
                deformed_fills = []
                for r in realizations:
                    deformed = void_to_filament_deformation(
                        r["field"], R_voxels=sigma_vox, amplitude=alpha)
                    thr_def, fill_def = threshold_for_deformed(
                        deformed, mode, r["threshold"], r["fill"])
                    deformed_fills.append(fill_def)
                    b_def = compute_betti_numbers_2d(
                        deformed, threshold_value=thr_def)["beta_1"]
                    # Null mean cancels: delta = (b_def - b_base) / null_std.
                    d = (None if r["null_std"] == 0.0
                         else (b_def - r["beta_1_base"]) / r["null_std"])
                    deltas.append(d)

                    if alpha == 0.0:
                        if not np.array_equal(deformed, r["field"].astype(np.float64)):
                            violations.append({
                                "mode": mode, "n_objects": n_obj, "r_s_mpc": r_s,
                                "seed": r["seed"],
                                "why": "amplitude=0 was not a bit-exact identity"})
                        if d is not None and d != 0.0:
                            violations.append({
                                "mode": mode, "n_objects": n_obj, "r_s_mpc": r_s,
                                "seed": r["seed"],
                                "why": f"delta_sigma={d} at alpha=0, expected exactly 0"})

                good = [d for d in deltas if d is not None]
                if not good:
                    d_mean, d_std, n_cross = None, None, 0
                else:
                    d_mean = float(np.mean(good))
                    d_std = float(np.std(good))
                    n_cross = int(sum(abs(d) >= DELTA_SIGMA_DETECT for d in good))

                zone, reason = classify(d_mean)
                cell.update({
                    "deformed_fill_mean": float(np.mean(deformed_fills)),
                    "fill_drift_from_baseline": float(
                        np.mean(deformed_fills) - np.mean(fills)),
                    "delta_sigma_per_realization": [
                        None if d is None else float(d) for d in deltas],
                    "delta_sigma_mean": d_mean,
                    "delta_sigma_std": d_std,
                    "n_realizations_crossing_3sigma": n_cross,
                    "n_realizations_valid": len(good),
                    "zone": zone, "reason": reason,
                })
                cells.append(cell)
                zone_counts[zone] = zone_counts.get(zone, 0) + 1

    results["cells"].extend(cells)
    results["per_occupancy"][mode] = per_occupancy
    return zone_counts, violations


def main():
    ap = argparse.ArgumentParser(description="WP-E5 Phase 2/3 transverse sweep (synthetic)")
    ap.add_argument("--output", default=OUTPUT_JSON)
    args = ap.parse_args()

    assert abs(EXTENT_MPC[0] - 8 * 6.04) < 1e-9 and abs(EXTENT_MPC[1] - 8 * 6.55) < 1e-9, \
        "EXTENT_MPC no longer matches its cited derivation from the nbins=8 voxel edges"

    voxel_mpc = (EXTENT_MPC[0] / NBINS, EXTENT_MPC[1] / NBINS)
    results = {
        "label": "SYNTHETIC",
        "description": (
            "WP-E5 Phase 2/3: 2D transverse detectability sweep over "
            "(n_objects, r_s, amplitude), baseline-subtracted per E2.11, "
            "two threshold modes, 5 field realizations per cell"),
        "nbins": NBINS,
        "extent_mpc": list(EXTENT_MPC),
        "extent_provenance": EXTENT_PROVENANCE,
        "voxel_mpc": list(voxel_mpc),
        "n_null_realizations": N_NULL_REALIZATIONS,
        "n_field_realizations": N_FIELD_REALIZATIONS,
        "field_seeds": FIELD_SEEDS,
        "threshold_modes": ["percentile", "matched_fill"],
        "threshold_percentile": THRESHOLD_PERCENTILE,
        "n_objects_grid": N_OBJECTS_GRID,
        "r_s_mpc_grid": R_S_MPC,
        "alpha_grid": ALPHA,
        "zone_thresholds": {"detect": DELTA_SIGMA_DETECT, "strong": DELTA_SIGMA_STRONG},
        "statistic": (
            "delta_sigma = sigma(alpha) - sigma(0) against a shared null bank; the "
            "null mean cancels identically, so delta_sigma = "
            "(beta_1(alpha) - beta_1(0)) / sigma_null"),
        "deformation_isotropy": (
            "per-axis Gaussian sigma so the warp is isotropic in Mpc, not in voxels"),
        "cells": [],
        "per_occupancy": {},
    }

    print("=" * 74)
    print("WP-E5 PHASE 2/3: TRANSVERSE DETECTABILITY SWEEP (SYNTHETIC)")
    print("=" * 74)
    print(f"extent {EXTENT_MPC} Mpc / nbins {NBINS} -> voxel "
          f"{voxel_mpc[0]:.3f} x {voxel_mpc[1]:.3f} Mpc | "
          f"{N_FIELD_REALIZATIONS} field realizations/cell")

    all_zone_counts = {}
    all_violations = []
    for mode in ("percentile", "matched_fill"):
        zc, viol = run_mode(mode, results)
        all_zone_counts[mode] = zc
        all_violations.extend(viol)

    results["zone_summary"] = all_zone_counts
    results["baseline_control_violations"] = all_violations
    results["baseline_control_passed"] = (len(all_violations) == 0)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[sweep] Results persisted to {args.output}")

    print("\n" + "=" * 74)
    print("ZONE SUMMARY")
    print("=" * 74)
    for mode in ("percentile", "matched_fill"):
        print(f"\n  [{mode}]")
        for zone in sorted(all_zone_counts[mode]):
            print(f"    {zone}: {all_zone_counts[mode][zone]}")
        det = [c for c in results["cells"]
               if c["threshold_mode"] == mode
               and c["zone"] in ("ZONE_1_DETECTABLE",
                                 "ZONE_2_GENERIC_DEFORMATION_EXCLUDED")]
        if det:
            print(f"    smallest occupancy with a detectable cell: "
                  f"n={min(c['n_objects'] for c in det)}")
            print(f"    smallest r_s with a detectable cell: "
                  f"{min(c['r_s_mpc'] for c in det)} Mpc")
        else:
            print(f"    no cell reached |mean delta_sigma| >= {DELTA_SIGMA_DETECT}")

    print(f"\n  alpha=0 baseline control: "
          f"{'PASS' if results['baseline_control_passed'] else 'FAIL'} "
          f"({len(all_violations)} violation(s))")
    print("=" * 74 + "\n")

    if not results["baseline_control_passed"]:
        print("[sweep] ABORT-WORTHY: the alpha=0 negative control failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Generated-by: Claude Opus 5 (Stream 3) | Verified-by: rewrite per
# docs/WP_E5_AUDIT_2026_07_26.md §3, then revised after self-review — per-axis sigma
# (physical isotropy), 5 field realizations with reported scatter, and a fixed-fill
# threshold mode that holds mask geometry constant while occupancy varies (the
# percentile threshold was measured to fill 8.4%-48.0% across the grid). alpha=0
# control enforced per realization and exits nonzero | Reviewed-by: pending T0
