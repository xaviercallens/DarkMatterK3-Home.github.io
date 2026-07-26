#!/usr/bin/env python3
"""Tests for pipeline/transverse.py (2D transverse topology, WP-E revised protocol).

Validates slice selection, projection, extent measurement, resolvability, and mock generation.
All quantities in float64. Tests are closure and determinism gates.
"""
import numpy as np
import pytest
from pipeline.transverse import (
    select_slice,
    project_slice_2d,
    transverse_extent_mpc,
    resolvable_2d,
    generate_mock_slice,
)


def test_select_slice_basic():
    """Slice selection includes lower edge, excludes upper edge."""
    z = np.array([0.5, 1.0, 1.5, 2.0, 2.5])
    mask = select_slice(z, z_lo=1.0, dz=0.5)
    # [1.0, 1.5): includes 1.0 (lower inclusive), excludes 1.5 (upper exclusive)
    expected = np.array([False, True, False, False, False])
    np.testing.assert_array_equal(mask, expected)


def test_select_slice_edges():
    """Boundary conditions: z_lo inclusive, z_lo + dz exclusive."""
    z = np.array([1.0, 1.5, 2.0])
    mask = select_slice(z, z_lo=1.0, dz=1.0)
    # [1.0, 2.0): includes 1.0 and 1.5, excludes 2.0
    expected = np.array([True, True, False])
    np.testing.assert_array_equal(mask, expected)


def test_project_slice_2d_fixed_ranges():
    """Fixed ranges grid must be identical regardless of subset."""
    # Create a catalog with 100 objects uniformly distributed
    ra_full = np.linspace(10, 20, 100)
    dec_full = np.linspace(-5, 5, 100)

    # Define fixed ranges from full catalog
    ranges = ((10, 20), (-5, 5))

    # Create two different slices from the same catalog
    mask1 = np.arange(100) < 50
    mask2 = np.arange(100) >= 50

    field1 = project_slice_2d(ra_full, dec_full, mask1, nbins=16, ranges=ranges)
    field2 = project_slice_2d(ra_full, dec_full, mask2, nbins=16, ranges=ranges)

    # Both fields must have identical shape
    assert field1.shape == field2.shape == (16, 16)
    # Fields should differ (different objects)
    assert not np.allclose(field1, field2)


def test_project_slice_2d_empty_slice():
    """Projection of an empty slice returns a uniform field (mean = 1)."""
    ra = np.array([10, 11, 12])
    dec = np.array([0, 1, 2])
    mask = np.zeros(3, dtype=bool)  # All False

    field = project_slice_2d(ra, dec, mask, nbins=8)
    assert field.shape == (8, 8)
    assert np.allclose(field.mean(), 1.0)


def test_transverse_extent_mpc_basic():
    """Extent computation returns positive Mpc values."""
    # Simple case: a small region near the equator
    ra = np.array([0, 0.1, 0.1, 0])
    dec = np.array([0, 0, 0.1, 0.1])
    z_mid = 1.0

    extent_ra, extent_dec = transverse_extent_mpc(ra, dec, z_mid)

    # Both extents should be positive and of order ~0.1 deg * comoving_distance
    # At z=1, comoving distance ~ 1500 Mpc, so 0.1 deg ~ 0.0017 rad ~ 2.5 Mpc
    assert extent_ra > 0
    assert extent_dec > 0
    # Reasonable scale: order 1-5 Mpc for 0.1 deg at z=1
    assert 1 < extent_ra < 10
    assert 1 < extent_dec < 10


def test_resolvable_2d_unresolvable():
    """Small scale relative to voxel is unresolvable."""
    extent = (10.0, 10.0)  # 10 Mpc × 10 Mpc
    nbins = 10  # voxel_size = 1 Mpc per axis
    scale = 0.5  # 0.5 Mpc < 1 voxel

    result = resolvable_2d(scale, extent, nbins, min_voxels=1.0)

    assert result["verdict"] == "UNRESOLVABLE"
    assert not result["resolvable_per_axis"][0]
    assert not result["resolvable_per_axis"][1]


def test_resolvable_2d_resolvable():
    """Large scale relative to voxel is resolvable."""
    extent = (10.0, 10.0)
    nbins = 10  # voxel_size = 1 Mpc
    scale = 2.0  # 2 voxels on both axes

    result = resolvable_2d(scale, extent, nbins, min_voxels=1.0)

    assert result["verdict"] == "RESOLVABLE"
    assert result["resolvable_per_axis"][0]
    assert result["resolvable_per_axis"][1]


def test_resolvable_2d_partial():
    """Asymmetric extent can yield partial resolvability."""
    extent = (20.0, 5.0)  # 20 Mpc × 5 Mpc
    nbins = 10  # voxel_sizes: 2 Mpc (x), 0.5 Mpc (y)
    scale = 1.5  # 0.75 voxels on x, 3 voxels on y

    result = resolvable_2d(scale, extent, nbins, min_voxels=1.0)

    assert result["verdict"] == "PARTIALLY_RESOLVABLE"
    assert not result["resolvable_per_axis"][0]  # x unresolvable
    assert result["resolvable_per_axis"][1]  # y resolvable


def test_generate_mock_slice_determinism():
    """Same seed produces identical mocks."""
    ra_range = (10, 20)
    dec_range = (-5, 5)
    seed = 42

    ra1, dec1 = generate_mock_slice(100, ra_range, dec_range, seed)
    ra2, dec2 = generate_mock_slice(100, ra_range, dec_range, seed)

    np.testing.assert_array_equal(ra1, ra2)
    np.testing.assert_array_equal(dec1, dec2)


def test_generate_mock_slice_boundaries():
    """Mock objects stay within specified range."""
    ra_range = (10, 20)
    dec_range = (-5, 5)
    seed = 12345

    ra, dec = generate_mock_slice(500, ra_range, dec_range, seed)

    assert ra.shape == (500,)
    assert dec.shape == (500,)
    assert np.all(ra >= ra_range[0]) and np.all(ra <= ra_range[1])
    assert np.all(dec >= dec_range[0]) and np.all(dec <= dec_range[1])


def test_generate_mock_slice_nonzero_variance():
    """A structured mock field has nonzero variance in density statistics.

    This is the WP-R3 no-op guard: if a null scheme produces zero variance
    in the test statistic, the null is broken. A properly structured mock
    should show variance when shuffled (density_shuffle) or re-randomized.
    """
    from pipeline.realfield3d import density_shuffle_realization
    from pipeline.topology2d import compute_betti_numbers_2d

    # Generate a mock slice field
    ra, dec = generate_mock_slice(200, (10, 20), (-5, 5), seed=999)
    from pipeline.realfield import density_field_from_catalog
    field = density_field_from_catalog(ra, dec, z=None, nbins=32)

    # Compute beta_1 for the original field
    betti_orig = compute_betti_numbers_2d(field, threshold_percentile=50.0)
    beta_1_orig = betti_orig["beta_1"]

    # Apply density_shuffle 10 times and check that at least one differs
    betti_shuffled = []
    for i in range(10):
        # density_shuffle works on any-shape arrays (uses seed parameter)
        field_shuffled = density_shuffle_realization(field, seed=777 + i)
        betti = compute_betti_numbers_2d(field_shuffled, threshold_percentile=50.0)
        betti_shuffled.append(betti["beta_1"])

    # At least one shuffle should yield a different beta_1 (nonzero variance)
    has_variance = any(b != beta_1_orig for b in betti_shuffled)
    assert has_variance, (
        f"No variance detected in density_shuffle: orig={beta_1_orig}, "
        f"shuffled={set(betti_shuffled)}"
    )


# Generated-by: Haiku 4.5 | Verified-by: manual hand-checked test execution |
# Reviewed-by: pending T0


# --- WP-E5 audit A-8: the E2.16 guard must fail closed on degenerate input ---

def test_resolvable_2d_zero_extent_fails_closed():
    """A zero-extent axis must return UNRESOLVABLE, never RESOLVABLE.

    Regression for WP-E5 audit finding A-8: extent 0 gave voxel 0, scale/0 = inf,
    and inf >= min_voxels reported RESOLVABLE — the guard's most permissive
    verdict on its most degenerate input.
    """
    from pipeline.transverse import resolvable_2d
    r = resolvable_2d(1.0, (0.0, 50.0), nbins=32)
    assert r["verdict"] == "UNRESOLVABLE", r
    assert r["resolvable_per_axis"] == (False, False)

    r2 = resolvable_2d(1.0, (0.0, 0.0), nbins=32)
    assert r2["verdict"] == "UNRESOLVABLE", r2


def test_resolvable_2d_rejects_bad_nbins():
    from pipeline.transverse import resolvable_2d
    import pytest
    with pytest.raises(ValueError):
        resolvable_2d(1.0, (50.0, 50.0), nbins=0)


# --- WP-E5 audit A-9: mock generation must not pile mass on the box boundary ---

def test_generate_mock_slice_does_not_pile_up_on_edges():
    """Clipping stray Gaussian draws would build an artificial ridge along the frame.

    These mocks serve as the null baseline, so a boundary ridge biases beta_0/beta_1
    in the null itself. Resampling keeps points in-box without stacking them on it.
    """
    import numpy as np
    from pipeline.transverse import generate_mock_slice

    ra_range, dec_range = (0.0, 10.0), (0.0, 10.0)
    # Clusters with wide scatter relative to the box maximise edge pressure.
    ra, dec = generate_mock_slice(4000, ra_range, dec_range, seed=7,
                                  n_clusters=4, clustered_fraction=0.9)

    assert ra.min() >= ra_range[0] and ra.max() <= ra_range[1]
    assert dec.min() >= dec_range[0] and dec.max() <= dec_range[1]

    # No mass concentration exactly ON the boundary values.
    on_edge = ((ra == ra_range[0]) | (ra == ra_range[1]) |
               (dec == dec_range[0]) | (dec == dec_range[1])).sum()
    assert on_edge == 0, f"{on_edge} points sit exactly on the box boundary"


def test_generate_mock_slice_is_deterministic_per_seed():
    import numpy as np
    from pipeline.transverse import generate_mock_slice
    a = generate_mock_slice(300, (0.0, 10.0), (0.0, 10.0), seed=11)
    b = generate_mock_slice(300, (0.0, 10.0), (0.0, 10.0), seed=11)
    assert np.array_equal(a[0], b[0]) and np.array_equal(a[1], b[1])
