#!/usr/bin/env python3
"""Golden tests for pipeline/realfield3d.py::density_shuffle_realization.

Implements the three-part validation scheme for the density-shuffle null:
1. Determinism: same field + same seed → identical output.
2. Conservation: multiset of cell values preserved exactly.
3. Integration: synthetic golden field with known structure, verify nonzero
   topological variance across realizations (the check that caught WP-R3's
   broken null bank).
"""
import numpy as np
import pytest
import torch

from pipeline.realfield3d import density_shuffle_realization
from pipeline.observables_real import compute_betti_numbers
from pipeline.synthetic import signal_field


def test_density_shuffle_determinism():
    """Same field + same seed must produce identical output."""
    np.random.seed(42)
    field = np.random.uniform(0.5, 2.5, size=(8, 8, 8))

    result1 = density_shuffle_realization(field, seed=123)
    result2 = density_shuffle_realization(field, seed=123)

    np.testing.assert_array_equal(result1, result2)


def test_density_shuffle_determinism_2d():
    """Determinism also holds for 2D fields."""
    field_2d = np.random.RandomState(7).uniform(0.5, 2.5, size=(16, 16))

    result1 = density_shuffle_realization(field_2d, seed=456)
    result2 = density_shuffle_realization(field_2d, seed=456)

    np.testing.assert_array_equal(result1, result2)


def test_density_shuffle_conservation_3d():
    """Shuffled field has identical multiset of values (same histogram)."""
    np.random.seed(99)
    field = np.random.uniform(0.1, 3.5, size=(10, 10, 10))

    shuffled = density_shuffle_realization(field, seed=777)

    # Shape preserved
    assert shuffled.shape == field.shape

    # Sorted values identical (multiset preservation)
    np.testing.assert_array_almost_equal(
        np.sort(shuffled.flatten()),
        np.sort(field.flatten()),
        decimal=10
    )


def test_density_shuffle_conservation_2d():
    """Conservation holds for 2D fields."""
    field_2d = np.arange(64, dtype=np.float64).reshape(8, 8)

    shuffled = density_shuffle_realization(field_2d, seed=888)

    assert shuffled.shape == field_2d.shape
    np.testing.assert_array_equal(
        np.sort(shuffled.flatten()),
        np.sort(field_2d.flatten())
    )


def test_density_shuffle_conservation_various_seeds():
    """Multiset preservation across multiple seeds (sanity check)."""
    field = np.random.RandomState(1).exponential(scale=1.2, size=(6, 6, 6))

    for seed in [1, 42, 100, 999]:
        shuffled = density_shuffle_realization(field, seed=seed)
        np.testing.assert_array_almost_equal(
            np.sort(shuffled.flatten()),
            np.sort(field.flatten()),
            decimal=10,
            err_msg=f"Conservation failed for seed={seed}"
        )


def test_density_shuffle_golden_integration_nonzero_variance():
    """Integration test: synthetic field with known structure shows nonzero
    topological variance under density shuffling.

    This is the CRITICAL test that catches null-scheme bugs (WP-R3 pattern).
    If all shuffled realizations tie the original's Betti numbers exactly,
    that indicates a broken null scheme (no-op) and must fail loudly.
    """
    # Generate synthetic field with injected structure (two Gaussian blobs)
    # at a modest size to keep test runtime low.
    torch_field = signal_field(n=16, seed=42, amplitude=2.0, noise_sigma=0.05)
    field = torch_field.detach().cpu().numpy().astype(np.float64)

    # Compute Betti numbers of original field
    result_original = compute_betti_numbers(field, threshold_percentile=50.0)
    beta_0_orig = result_original["beta_0"]
    beta_1_orig = result_original["beta_1"]
    beta_2_orig = result_original["beta_2"]

    # Generate 10 density-shuffled realizations
    beta_0_shuffled = []
    beta_1_shuffled = []
    beta_2_shuffled = []

    for i in range(10):
        shuffled = density_shuffle_realization(field, seed=100 + i)
        result = compute_betti_numbers(shuffled, threshold_percentile=50.0)
        beta_0_shuffled.append(result["beta_0"])
        beta_1_shuffled.append(result["beta_1"])
        beta_2_shuffled.append(result["beta_2"])

    # Nonzero-variance check: at least some shuffled realizations must differ
    # from the original in at least one of the three Betti numbers.
    beta_0_differs = any(b != beta_0_orig for b in beta_0_shuffled)
    beta_1_differs = any(b != beta_1_orig for b in beta_1_shuffled)
    beta_2_differs = any(b != beta_2_orig for b in beta_2_shuffled)

    any_differs = beta_0_differs or beta_1_differs or beta_2_differs

    assert any_differs, (
        f"Density-shuffle shows ZERO topological variance across 10 realizations. "
        f"Original: β₀={beta_0_orig}, β₁={beta_1_orig}, β₂={beta_2_orig}. "
        f"All shuffled β₀ values: {beta_0_shuffled}. "
        f"All shuffled β₁ values: {beta_1_shuffled}. "
        f"All shuffled β₂ values: {beta_2_shuffled}. "
        f"This is the exact WP-R3 null-bank bug pattern — the scheme is not "
        f"actually changing the topology. Check: (1) field size too small "
        f"(16³ may have few connected components), (2) thresholding too "
        f"coarse (percentile=50 may not vary much across shuffles)."
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


# Generated-by: Haiku 4.5 | Verified-by: self (6/6 passing, incl. nonzero-variance
# integration check) | Reviewed-by: pending T0
