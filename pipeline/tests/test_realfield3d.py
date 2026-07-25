#!/usr/bin/env python3
"""Golden tests for pipeline/realfield3d.py (WP-R5).

Critically includes a NONZERO-VARIANCE check across realizations — the check
missing from WP-R3 that let a degenerate null bank pass
(docs/FINDING_R_NULLDEGENERATE_2026_07_25.md). A null scheme that produces
identical topology every realization is broken, full stop, regardless of
cross-scheme agreement.
"""
import numpy as np
import pytest
from pipeline.realfield3d import (
    density_field_cartesian_mpc,
    z_shuffle_realization,
    angular_csr_realization,
)
from pipeline.observables_real import compute_betti_numbers


def test_cartesian_field_shape_and_normalization():
    np.random.seed(1)
    n = 500
    x = np.random.uniform(0, 100, n)
    y = np.random.uniform(0, 100, n)
    z = np.random.uniform(0, 100, n)

    field = density_field_cartesian_mpc(x, y, z, nbins=8)
    assert field.shape == (8, 8, 8)
    assert field.mean() == pytest.approx(1.0, abs=1e-6)


def test_cartesian_field_empty_catalog():
    field = density_field_cartesian_mpc(
        np.array([]), np.array([]), np.array([]), nbins=4
    )
    assert field.shape == (4, 4, 4)
    assert (field == 1.0).all()


def test_cartesian_field_fixed_ranges_reproducible():
    """Fixed `ranges` must produce the same grid regardless of data extent,
    so a real field and its nulls are directly comparable."""
    x = np.array([1.0, 2.0, 3.0])
    y = np.array([1.0, 2.0, 3.0])
    z = np.array([1.0, 2.0, 3.0])
    ranges = ((0.0, 10.0), (0.0, 10.0), (0.0, 10.0))

    field1 = density_field_cartesian_mpc(x, y, z, nbins=5, ranges=ranges)
    field2 = density_field_cartesian_mpc(x, y, z, nbins=5, ranges=ranges)
    np.testing.assert_array_equal(field1, field2)


def test_z_shuffle_produces_different_point_pattern():
    """CRITICAL: z-shuffle must actually change the point pattern, unlike
    WP-R3's degenerate co-permutation (which was a no-op)."""
    rng = np.random.default_rng(42)
    ra = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    dec = np.array([5.0, 6.0, 7.0, 8.0, 9.0])
    z = np.array([0.1, 0.2, 0.3, 0.4, 0.5])

    ra2, dec2, z2 = z_shuffle_realization(ra, dec, z, rng)

    # RA, Dec must be UNCHANGED (that's the point of "fix RA,Dec")
    np.testing.assert_array_equal(ra2, ra)
    np.testing.assert_array_equal(dec2, dec)

    # z must be a permutation of the original (same values, different assignment)
    assert sorted(z2) == sorted(z)
    # For n=5 objects, an actual permutation should (almost always) differ from identity
    assert not np.array_equal(z2, z), "z-shuffle returned identity permutation (check seed/rng)"


def test_angular_csr_produces_different_positions():
    """CRITICAL: angular CSR must generate NEW (RA,Dec), unlike a rigid
    rotation (isometry) which preserves all relative structure."""
    rng = np.random.default_rng(42)
    ra = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    dec = np.array([5.0, 6.0, 7.0, 8.0, 9.0])
    z = np.array([0.1, 0.2, 0.3, 0.4, 0.5])

    ra2, dec2, z2 = angular_csr_realization(ra, dec, z, rng)

    # z must be UNCHANGED (that's the point of "fix z")
    np.testing.assert_array_equal(z2, z)

    # RA, Dec must differ from original (new random draw, not a copy)
    assert not np.array_equal(ra2, ra), "angular CSR returned unchanged RA"

    # New positions must stay within the original bounding box
    assert ra2.min() >= ra.min() - 1e-9
    assert ra2.max() <= ra.max() + 1e-9


def test_z_shuffle_nonzero_variance_in_topology():
    """THE CHECK THAT WAS MISSING IN WP-R3: null realizations must show
    nonzero variance in Betti numbers across an ensemble. A degenerate null
    (WP-R3's actual bug) shows exactly zero variance.

    Uses continuous (non-bimodal) scatter: two widely-separated hard clusters
    would keep a fixed axis's gap structure intact regardless of shuffling on
    the OTHER axes, which is correct null behavior, not variance — see the
    investigation in this file's git history for why an earlier version of
    this test used a bad fixture (hard bimodal z-split) that produced a false
    "zero variance" failure for the CSR scheme specifically."""
    rng = np.random.default_rng(7)
    n = 400
    # Continuous, mildly clustered — not two disjoint blobs — so shuffling
    # along any one axis can plausibly open/close bin-to-bin connectivity.
    ra = rng.normal(25, 8, n)
    dec = rng.normal(12, 6, n)
    z = rng.normal(0.3, 0.15, n)

    ranges = ((ra.min(), ra.max()), (dec.min(), dec.max()), (z.min(), z.max()))

    beta0_values = []
    for _ in range(40):
        ra_s, dec_s, z_s = z_shuffle_realization(ra, dec, z, rng)
        field = density_field_cartesian_mpc(ra_s, dec_s, z_s, nbins=8, ranges=ranges)
        result = compute_betti_numbers(field, threshold_percentile=50.0)
        beta0_values.append(result["beta_0"])

    variance = np.var(beta0_values)
    assert variance > 0, (
        f"z-shuffle null shows ZERO variance across 40 realizations "
        f"(values={beta0_values}) — this is the exact WP-R3 bug pattern, "
        f"reintroduced. The null scheme is not actually randomizing anything."
    )


def test_angular_csr_nonzero_variance_in_topology():
    """Same nonzero-variance check for the angular-CSR scheme (continuous
    fixture — see docstring above for why a bimodal-z fixture is invalid
    here: CSR fixes z by design, so a hard z-gap alone fixes beta_0
    regardless of angular randomization, which is correct scheme behavior,
    not a bug)."""
    rng = np.random.default_rng(11)
    n = 400
    ra = rng.normal(25, 8, n)
    dec = rng.normal(12, 6, n)
    z = rng.normal(0.3, 0.15, n)

    ranges = ((ra.min(), ra.max()), (dec.min(), dec.max()), (z.min(), z.max()))

    beta0_values = []
    for _ in range(40):
        ra_s, dec_s, z_s = angular_csr_realization(ra, dec, z, rng)
        field = density_field_cartesian_mpc(ra_s, dec_s, z_s, nbins=8, ranges=ranges)
        result = compute_betti_numbers(field, threshold_percentile=50.0)
        beta0_values.append(result["beta_0"])

    variance = np.var(beta0_values)
    assert variance > 0, (
        f"angular-CSR null shows ZERO variance across 40 realizations "
        f"(values={beta0_values}) — the null scheme is not randomizing."
    )


def test_euler_identity_holds_on_cartesian_field():
    """Sanity: the exact Euler identity must hold on Cartesian-binned fields
    exactly as it does on the WP-R2 angular fields (same underlying formula)."""
    np.random.seed(3)
    n = 400
    x = np.random.uniform(0, 50, n)
    y = np.random.uniform(0, 50, n)
    z = np.random.uniform(0, 50, n)

    field = density_field_cartesian_mpc(x, y, z, nbins=10)
    result = compute_betti_numbers(field, threshold_percentile=50.0)

    assert result["beta_1"] == result["beta_0"] + result["beta_2"] - result["euler_char"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
