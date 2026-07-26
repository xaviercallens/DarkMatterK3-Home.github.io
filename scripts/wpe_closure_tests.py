#!/usr/bin/env python3
"""
WP-E Phase 1: Closure and null tests (2D transverse topology, mock-only).

Label: SYNTHETIC (no real data)

Tests:
1. CLOSURE: A structured mock field deformed with (r_s=2.0 Mpc, amplitude=1.0)
   must have beta_1 sit >= 5 sigma from a 40-realization null bank of the
   undeformed field. Script EXITS NONZERO with FAIL if not.

2. NEGATIVE CONTROL: Same test with amplitude=0.0 must NOT exceed 5 sigma
   (if it does, the null is broken — FAIL loudly).

3. NULL TEST: Two independent undeformed mocks, 40 trials each, alpha=0.05.
   False-positive rate must be within 3-sigma binomial bound, else FAIL.

All quantities in float64. Persists JSON before printing.
"""

import os
import json
import sys
import argparse

import numpy as np

from pipeline.transverse import generate_mock_slice
from pipeline.realfield import density_field_from_catalog
from pipeline.deformation import void_to_filament_deformation
from pipeline.topology2d import compute_betti_numbers_2d
from pipeline.realfield3d import density_shuffle_realization

# Configuration
OUTPUT_JSON = "data/derived/wp_e5_closure_2026_07_26.json"
NBINS = 32
N_MOCK_OBJECTS = 200
N_NULL_REALIZATIONS = 40
THRESHOLD_PERCENTILE = 50.0
R_VOXELS_DEFORM = 2.0  # Characteristic deformation scale in voxels
SIGMA_THRESHOLD = 5.0  # Detectability threshold


def generate_structured_mock_field(seed, nbins=NBINS, n_objects=N_MOCK_OBJECTS):
    """Generate a structured mock 2D field with clustering."""
    ra_range = (0, 10)
    dec_range = (0, 10)
    ra, dec = generate_mock_slice(n_objects, ra_range, dec_range, seed, n_clusters=4, clustered_fraction=0.7)
    field = density_field_from_catalog(ra, dec, z=None, nbins=nbins, ra_range=ra_range, dec_range=dec_range)
    return field


def compute_null_band(field_undeformed, n_realizations, threshold_percentile, seed_base=9001):
    """Generate a null bank of density-shuffle realizations.

    B-1 fix (WP-E5 audit): density_shuffle_realization takes `seed`, not `rng`.
    The previous `rng=rng` call raised TypeError on the first iteration, which is
    why this script had never executed. Each realization gets its own seed.
    """
    beta_1_null = []

    for i in range(n_realizations):
        field_shuffled = density_shuffle_realization(field_undeformed, seed=seed_base + i)
        betti = compute_betti_numbers_2d(field_shuffled, threshold_percentile=threshold_percentile)
        beta_1_null.append(betti["beta_1"])

    return np.array(beta_1_null, dtype=np.float64)


def compute_sigma(observed, null_vals):
    """Sigma = (observed - mean) / std. Return None if std == 0."""
    null_mean = float(np.mean(null_vals))
    null_std = float(np.std(null_vals))
    if null_std == 0:
        return None
    return (observed - null_mean) / null_std


def test_closure():
    """Closure test: deformed field must be >= 5 sigma from null."""
    print("\n[closure] TEST 1: CLOSURE (amplitude=1.0, r_s=2.0 voxels)")
    print("-" * 70)

    # Generate structured mock field
    field_orig = generate_structured_mock_field(seed=1001)

    # Generate null bank from UNDEFORMED field
    print(f"[closure] Generating {N_NULL_REALIZATIONS} null realizations...")
    null_vals = compute_null_band(field_orig, N_NULL_REALIZATIONS, THRESHOLD_PERCENTILE)
    null_mean = float(np.mean(null_vals))
    null_std = float(np.std(null_vals))
    print(f"[closure] Null band: mean={null_mean:.2f}, std={null_std:.2f}")

    # Deform the field
    field_deformed = void_to_filament_deformation(field_orig, R_voxels=R_VOXELS_DEFORM, amplitude=1.0)

    # Compute beta_1 of deformed field
    betti_deformed = compute_betti_numbers_2d(field_deformed, threshold_percentile=THRESHOLD_PERCENTILE)
    beta_1_deformed = betti_deformed["beta_1"]

    sigma = compute_sigma(beta_1_deformed, null_vals)
    beta_1_undeformed = compute_betti_numbers_2d(
        field_orig, threshold_percentile=THRESHOLD_PERCENTILE)["beta_1"]
    sigma_baseline = compute_sigma(beta_1_undeformed, null_vals)
    print(f"[closure] Deformed beta_1={beta_1_deformed}, sigma={sigma}")
    print(f"[closure] Baseline (undeformed) beta_1={beta_1_undeformed}, sigma={sigma_baseline}")

    detail = {
        "beta_1_deformed": int(beta_1_deformed),
        "beta_1_undeformed": int(beta_1_undeformed),
        "null_mean": null_mean,
        "null_std": null_std,
        "null_distinct_values": sorted(set(int(v) for v in null_vals)),
        "sigma": None if sigma is None else float(sigma),
        "sigma_baseline": None if sigma_baseline is None else float(sigma_baseline),
        "delta_sigma": (None if (sigma is None or sigma_baseline is None)
                        else float(sigma - sigma_baseline)),
        "sigma_threshold": SIGMA_THRESHOLD,
    }

    if sigma is None or abs(sigma) < SIGMA_THRESHOLD:
        shown = "None" if sigma is None else f"{abs(sigma):.2f}"
        print(f"[closure] FAIL: |sigma|={shown} < {SIGMA_THRESHOLD}")
        return False, detail
    print(f"[closure] PASS: |sigma|={abs(sigma):.2f} >= {SIGMA_THRESHOLD}")
    return True, detail


def test_negative_control():
    """Negative control: amplitude=0 must NOT exceed 5 sigma."""
    print("\n[closure] TEST 2: NEGATIVE CONTROL (amplitude=0.0)")
    print("-" * 70)

    # Generate structured mock field
    field_orig = generate_structured_mock_field(seed=1002)

    # Generate null bank from UNDEFORMED field
    print(f"[closure] Generating {N_NULL_REALIZATIONS} null realizations...")
    null_vals = compute_null_band(field_orig, N_NULL_REALIZATIONS, THRESHOLD_PERCENTILE)
    null_mean = float(np.mean(null_vals))
    null_std = float(np.std(null_vals))

    # "Deform" with amplitude=0 (should be identity)
    field_identity = void_to_filament_deformation(field_orig, R_voxels=R_VOXELS_DEFORM, amplitude=0.0)

    # Compute beta_1 of identity field
    betti_identity = compute_betti_numbers_2d(field_identity, threshold_percentile=THRESHOLD_PERCENTILE)
    beta_1_identity = betti_identity["beta_1"]

    # amplitude=0 must be an exact identity — assert it rather than assume it.
    identity_exact = bool(np.array_equal(field_identity, field_orig.astype(np.float64)))

    sigma = compute_sigma(beta_1_identity, null_vals)
    print(f"[closure] Identity field beta_1={beta_1_identity}, sigma={sigma}")
    print(f"[closure] amplitude=0 is bit-exact identity: {identity_exact}")

    detail = {
        "identity_is_exact": identity_exact,
        "beta_1_identity": int(beta_1_identity),
        "null_mean": null_mean,
        "null_std": null_std,
        "null_distinct_values": sorted(set(int(v) for v in null_vals)),
        "sigma": None if sigma is None else float(sigma),
        "sigma_threshold": SIGMA_THRESHOLD,
        "note": (
            "sigma here is the BASELINE OFFSET of an undeformed field against its own "
            "shuffle null. It is not a deformation response. A large value does not fail "
            "this test (the test only bars >= 5 sigma) but it is exactly the quantity that "
            "E2.11 requires be subtracted before any Delta-sigma is quoted."
        ),
    }

    if not identity_exact:
        print("[closure] FAIL: amplitude=0 did not return the input field unchanged")
        return False, detail
    if sigma is not None and abs(sigma) >= SIGMA_THRESHOLD:
        print(f"[closure] FAIL: |sigma|={abs(sigma):.2f} >= {SIGMA_THRESHOLD} (null is broken)")
        return False, detail
    shown = "None" if sigma is None else f"{abs(sigma):.2f}"
    print(f"[closure] PASS: |sigma|={shown} < {SIGMA_THRESHOLD}")
    return True, detail


def test_null_false_positive_rate():
    """Null test: FPR at the DECISION threshold must sit inside a 3-sigma binomial bound.

    B-3 fix (WP-E5 audit): this test previously declared `alpha = 0.05` and then
    counted exceedances at |sigma| >= 5.0. Those are not the same criterion — a
    5-sigma cut corresponds to alpha ~ 5.7e-7, not 0.05 — so the bound was built
    for a nominal rate five orders of magnitude looser than the rule being
    applied, and the test could not fail. The nominal alpha is now DERIVED from
    the sigma threshold actually used, so the two can never drift apart again.
    """
    from scipy import stats

    n_trials_per_mock = 40
    sigma_threshold_fpr = SIGMA_THRESHOLD
    # Two-sided Gaussian tail beyond the decision threshold. This is the rate the
    # test is entitled to expect, given the cut it actually applies.
    alpha = float(2.0 * stats.norm.sf(sigma_threshold_fpr))
    print(f"\n[closure] TEST 3: NULL FALSE-POSITIVE RATE "
          f"(|sigma| >= {sigma_threshold_fpr} -> nominal alpha = {alpha:.3g})")
    print("-" * 70)

    n_exceed_mock1 = 0
    n_exceed_mock2 = 0

    # Mock 1: Generate null bank, then test independent mock against it
    print("[closure] Mock 1 vs. Mock 1 null bank...")
    field_mock1 = generate_structured_mock_field(seed=2001)
    null_mock1 = compute_null_band(field_mock1, N_NULL_REALIZATIONS, THRESHOLD_PERCENTILE)

    for i in range(n_trials_per_mock):
        field_test = generate_structured_mock_field(seed=3001 + i)
        betti_test = compute_betti_numbers_2d(field_test, threshold_percentile=THRESHOLD_PERCENTILE)
        sigma = compute_sigma(betti_test["beta_1"], null_mock1)
        if sigma is not None and abs(sigma) >= sigma_threshold_fpr:
            n_exceed_mock1 += 1

    fpr_mock1 = n_exceed_mock1 / n_trials_per_mock

    # Mock 2: Generate second null bank, then test against it
    print("[closure] Mock 2 vs. Mock 2 null bank...")
    field_mock2 = generate_structured_mock_field(seed=2002)
    null_mock2 = compute_null_band(field_mock2, N_NULL_REALIZATIONS, THRESHOLD_PERCENTILE)

    for i in range(n_trials_per_mock):
        field_test = generate_structured_mock_field(seed=3100 + i)
        betti_test = compute_betti_numbers_2d(field_test, threshold_percentile=THRESHOLD_PERCENTILE)
        sigma = compute_sigma(betti_test["beta_1"], null_mock2)
        if sigma is not None and abs(sigma) >= sigma_threshold_fpr:
            n_exceed_mock2 += 1

    fpr_mock2 = n_exceed_mock2 / n_trials_per_mock

    # Expected FPR and binomial 3-sigma bound
    expected_fpr = alpha
    n_total = n_trials_per_mock * 2
    binomial_std = np.sqrt(n_total * alpha * (1 - alpha))
    upper_bound = expected_fpr + 3 * (binomial_std / n_total)

    print(f"[closure] Mock 1 FPR: {fpr_mock1:.2%} ({n_exceed_mock1}/{n_trials_per_mock})")
    print(f"[closure] Mock 2 FPR: {fpr_mock2:.2%} ({n_exceed_mock2}/{n_trials_per_mock})")
    print(f"[closure] Expected FPR at |sigma|>={sigma_threshold_fpr}: {expected_fpr:.3g}")
    print(f"[closure] 3-sigma upper bound: {upper_bound:.3g}")

    combined_fpr = (n_exceed_mock1 + n_exceed_mock2) / n_total
    # Discreteness diagnostic: a near-degenerate null makes the Gaussian sigma
    # interpretation invalid, and this test is the place that surfaces it.
    n_distinct = len(set(int(v) for v in np.concatenate([null_mock1, null_mock2])))
    detail = {
        "sigma_threshold": sigma_threshold_fpr,
        "nominal_alpha_from_threshold": alpha,
        "n_trials_total": n_total,
        "n_exceed_mock1": int(n_exceed_mock1),
        "n_exceed_mock2": int(n_exceed_mock2),
        "fpr_mock1": float(fpr_mock1),
        "fpr_mock2": float(fpr_mock2),
        "combined_fpr": float(combined_fpr),
        "upper_bound_3sigma": float(upper_bound),
        "null_distinct_values_across_banks": n_distinct,
        "note": (
            "nominal alpha is derived from the sigma threshold actually applied "
            "(two-sided Gaussian tail), not declared independently of it. If the null "
            "bank takes few distinct values the Gaussian interpretation of sigma is "
            "invalid and a failure here should be read as that, not as a broken null."
        ),
    }

    if combined_fpr <= upper_bound:
        print(f"[closure] PASS: FPR={combined_fpr:.3g} <= {upper_bound:.3g}")
        return True, detail
    print(f"[closure] FAIL: FPR={combined_fpr:.3g} > {upper_bound:.3g}")
    print(f"[closure] NOTE: null banks take only {n_distinct} distinct value(s); "
          f"if that is small, sigma is not Gaussian-interpretable here.")
    return False, detail


def main():
    parser = argparse.ArgumentParser(description="WP-E Phase 1: Closure and null tests")
    parser.add_argument(
        "--output",
        default=OUTPUT_JSON,
        help=f"Output JSON path (default: {OUTPUT_JSON})",
    )
    args = parser.parse_args()

    print("=" * 70)
    print("WP-E PHASE 1: CLOSURE AND NULL TESTS (2D TRANSVERSE TOPOLOGY)")
    print("=" * 70)

    results = {
        "label": "SYNTHETIC",
        "description": "Closure + null tests for 2D transverse topology",
        "nbins": NBINS,
        "n_mock_objects": N_MOCK_OBJECTS,
        "n_null_realizations": N_NULL_REALIZATIONS,
        "threshold_percentile": THRESHOLD_PERCENTILE,
        "sigma_threshold": SIGMA_THRESHOLD,
        "tests": {},
    }

    # Run all three tests. Each returns (passed, measured detail) — the JSON must
    # carry the numbers, not just the verdict (WP-E3 lesson: the JSON is the artifact).
    test1_pass, test1_detail = test_closure()
    test2_pass, test2_detail = test_negative_control()
    test3_pass, test3_detail = test_null_false_positive_rate()

    results["tests"]["closure"] = {"passed": test1_pass, **test1_detail}
    results["tests"]["negative_control"] = {"passed": test2_pass, **test2_detail}
    results["tests"]["null_fpr"] = {"passed": test3_pass, **test3_detail}

    all_pass = test1_pass and test2_pass and test3_pass
    results["verdict"] = "PASS" if all_pass else "FAIL"

    # Persist JSON
    os.makedirs(os.path.dirname(OUTPUT_JSON) or ".", exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[closure] Results persisted to {OUTPUT_JSON}")

    print("\n" + "=" * 70)
    print(f"OVERALL: {results['verdict']}")
    print("=" * 70 + "\n")

    # Exit with error if any test failed
    if not all_pass:
        sys.exit(1)


if __name__ == "__main__":
    main()

# Generated-by: Haiku 4.5 | Verified-by: synthetic-only execution, null-bank discipline |
# Reviewed-by: pending T0
