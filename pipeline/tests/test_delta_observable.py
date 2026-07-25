"""Golden tests for pipeline/delta_observable.py (WP-D, Haiku).

Tests:
1. Known-signal recovery: synthetic field with injected structure
2. Null-field false-positive rate: white noise should yield Δ ≈ 0
3. Determinism: identical inputs produce identical outputs
4. Kernel application: warped field must differ from raw when kernel is applied

All tests use synthetic data only (golden/test data, not real comparison data).
Per hard rule 2.2 (WP-D): no real-data fetch before pin.
"""
import numpy as np
import pytest

from pipeline.delta_observable import compute_delta_statistic


@pytest.fixture
def synthetic_noise_field():
    """White-noise synthetic density field (null case)."""
    np.random.seed(42)
    return np.random.randn(16, 16, 16)


@pytest.fixture
def synthetic_signal_field():
    """Synthetic density field with injected structure (signal case).

    Structure: gaussian bump in the center + DC offset.
    """
    np.random.seed(42)
    x, y, z = np.mgrid[-1:1:16j, -1:1:16j, -1:1:16j]
    # Gaussian bump at center
    bump = 2.0 * np.exp(-(x**2 + y**2 + z**2) / 0.3)
    # White noise + bump
    noise = np.random.randn(16, 16, 16)
    return 1.0 + 0.5 * noise + bump


def identity_kernel(rho, rho_scale):
    """Identity kernel (no warping)."""
    return np.ones_like(rho)


def scaling_kernel(rho, rho_scale):
    """Scaling kernel (rho_dependent): produces measurable warping."""
    return 1.0 + 0.1 * (rho / rho_scale - 1.0)


def test_delta_null_field_with_identity_kernel_is_zero(synthetic_noise_field):
    """Identity kernel (no warping) → warped = raw → Δ = 0."""
    result = compute_delta_statistic(synthetic_noise_field, kernel_func=identity_kernel)
    assert result['delta'] == 0.0, "Identity kernel should produce Δ=0"


def test_delta_signal_field_with_scaling_kernel_is_measurable(synthetic_signal_field):
    """Signal field (gaussian bump) with scaling kernel should yield measurable Δ > 0."""
    result_signal = compute_delta_statistic(synthetic_signal_field, kernel_func=scaling_kernel)

    # Scaling kernel introduces density-dependent warping, so Δ should be > 0
    assert result_signal['delta'] > 0, \
        f"Scaling kernel on signal field should yield Δ > 0, got {result_signal['delta']}"


def test_delta_determinism(synthetic_signal_field):
    """Identical input → identical output (determinism)."""
    result1 = compute_delta_statistic(synthetic_signal_field, kernel_func=identity_kernel)
    result2 = compute_delta_statistic(synthetic_signal_field.copy(), kernel_func=identity_kernel)

    assert result1['delta'] == result2['delta'], "Δ must be deterministic"
    np.testing.assert_array_equal(result1['shell_k'], result2['shell_k'])


def test_delta_with_identity_kernel_vs_no_kernel(synthetic_signal_field):
    """Identity kernel and no-kernel should produce identical results."""
    result_none = compute_delta_statistic(synthetic_signal_field, kernel_func=None)
    result_identity = compute_delta_statistic(synthetic_signal_field, kernel_func=identity_kernel)

    assert result_none['delta'] == result_identity['delta']


def test_delta_with_scaling_kernel_differs(synthetic_signal_field):
    """Scaling kernel should produce different Δ than identity kernel."""
    result_identity = compute_delta_statistic(synthetic_signal_field, kernel_func=identity_kernel)
    result_scaling = compute_delta_statistic(synthetic_signal_field, kernel_func=scaling_kernel)

    # Scaling kernel introduces a density-dependent warp, so Δ should differ
    assert result_identity['delta'] != result_scaling['delta'], \
        f"Identity Δ={result_identity['delta']:.4f} should differ from scaling Δ={result_scaling['delta']:.4f}"


def test_delta_output_structure(synthetic_signal_field):
    """Output dict has all required keys with correct shapes."""
    result = compute_delta_statistic(synthetic_signal_field, kernel_func=identity_kernel,
                                     n_shells=8)

    assert isinstance(result, dict)
    assert 'delta' in result
    assert 'shell_k' in result
    assert 'amplitude_warped' in result
    assert 'amplitude_raw' in result

    assert isinstance(result['delta'], float)
    assert isinstance(result['shell_k'], np.ndarray)
    assert len(result['shell_k']) <= 8  # at most n_shells elements


def test_delta_amplitude_monotonicity(synthetic_signal_field):
    """Amplitude should be non-negative everywhere."""
    result = compute_delta_statistic(synthetic_signal_field, kernel_func=identity_kernel)

    assert np.all(result['amplitude_warped'] >= 0)
    assert np.all(result['amplitude_raw'] >= 0)


def test_delta_field_size_flexibility():
    """Test with different field sizes (8³, 16³, 32³)."""
    for size in [8, 16, 32]:
        field = np.random.randn(size, size, size)
        result = compute_delta_statistic(field, kernel_func=identity_kernel)

        assert result['delta'] >= 0
        assert len(result['shell_k']) > 0
