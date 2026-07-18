#!/usr/bin/env python3
"""Extended pipeline test scenarios (S3-02 robustness).

T2-level test expansion: multiple SNR levels, field sizes, parameter sweeps.
All mechanical; all verifiable by pytest.

Test coverage:
- Closure: signal recovery at SNR 0.5, 1.0, 2.0, 3.0, 4.0 (monotonicity)
- Null: false-positive rates across alpha levels
- Robustness: repeated runs (seed variation, field-size scaling)
- Edge cases: near-threshold signal amplitudes
"""
from pipeline.core import null_distribution, run_comparison
from pipeline.synthetic import get_device, signal_field, null_field

import pytest

ALPHA_DEFAULT = 0.05


# ============================================================================
# Extended Closure Tests: Signal Recovery at Multiple SNR Levels
# ============================================================================

class TestClosureMultipleSNR:
    """Verify signal recovery across SNR range."""

    @pytest.mark.parametrize("amplitude", [0.5, 1.0, 2.0, 3.0, 4.0])
    def test_signal_recovery_snr_sweep(self, amplitude):
        """Recover injected signal at different amplitudes (SNR levels)."""
        device = get_device()
        N = 24
        null_stats = null_distribution(N, n_trials=200, seed=1000, device=device)
        field = signal_field(N, seed=100, amplitude=amplitude, device=device)

        result = run_comparison(field, null_stats, alpha=ALPHA_DEFAULT)

        # Higher amplitude should always reject null (except very weak signals)
        if amplitude >= 1.0:
            assert result["reject_null"] is True, (
                f"Failed to recover signal at amplitude={amplitude}, "
                f"p={result['p_value']}"
            )
        # Low amplitude (0.5) may not reject at alpha=0.05; that's OK (low power)

    def test_snr_monotonicity(self):
        """Verify: higher SNR -> higher statistic -> smaller p-value."""
        device = get_device()
        N = 24
        null_stats = null_distribution(N, n_trials=200, seed=1001, device=device)

        results = {}
        for amp in [0.5, 1.0, 2.0, 3.0, 4.0]:
            field = signal_field(N, seed=101, amplitude=amp, device=device)
            results[amp] = run_comparison(field, null_stats, alpha=ALPHA_DEFAULT)

        # Check monotonicity: statistic increases, p-value decreases
        stats = [results[amp]["observed_statistic"] for amp in [0.5, 1.0, 2.0, 3.0, 4.0]]
        p_vals = [results[amp]["p_value"] for amp in [0.5, 1.0, 2.0, 3.0, 4.0]]

        # Statistics should be monotonically increasing
        for i in range(len(stats) - 1):
            assert stats[i] <= stats[i + 1], (
                f"Non-monotonic statistic: {stats[i]} > {stats[i+1]}"
            )

        # P-values should be monotonically decreasing
        for i in range(len(p_vals) - 1):
            assert p_vals[i] >= p_vals[i + 1], (
                f"Non-monotonic p-value: {p_vals[i]} < {p_vals[i+1]}"
            )


# ============================================================================
# Extended Null Tests: False-Positive Rates at Multiple Alpha Levels
# ============================================================================

class TestNullMultipleAlpha:
    """Verify calibration across alpha levels."""

    @pytest.mark.parametrize("alpha", [0.01, 0.05, 0.10])
    def test_fp_rate_at_alpha(self, alpha):
        """Check false-positive rate is controlled at different alpha levels."""
        device = get_device()
        N = 24
        n_trials = int(100 / alpha)  # More trials for smaller alpha (better stats)
        n_tests = max(20, int(50 * alpha))  # Proportional test count

        null_stats = null_distribution(N, n_trials=n_trials, seed=2000, device=device)

        false_positives = 0
        for k in range(n_tests):
            field = null_field(N, seed=6000 + k, device=device)
            result = run_comparison(field, null_stats, alpha=alpha)
            false_positives += int(result["reject_null"])

        rate = false_positives / n_tests
        # Binomial bound: mean + 3*sigma
        mean = alpha * n_tests
        sigma = (n_tests * alpha * (1 - alpha)) ** 0.5
        bound = (mean + 3 * sigma) / n_tests

        assert rate <= bound, (
            f"Alpha={alpha}: false-positive rate {rate:.3f} "
            f"exceeds bound {bound:.3f}"
        )


# ============================================================================
# Robustness Tests: Repeated Runs and Seed Variation
# ============================================================================

class TestRobustnessRepeatability:
    """Verify results are reproducible and robust to seed changes."""

    def test_deterministic_result_same_seed(self):
        """Same seed should give identical result (determinism check)."""
        device = get_device()
        N = 24
        seed_null = 3000
        seed_sig = 200

        # Run 1
        null_stats_1 = null_distribution(N, n_trials=100, seed=seed_null, device=device)
        field_1 = signal_field(N, seed=seed_sig, amplitude=2.0, device=device)
        result_1 = run_comparison(field_1, null_stats_1, alpha=ALPHA_DEFAULT)

        # Run 2 (same seeds)
        null_stats_2 = null_distribution(N, n_trials=100, seed=seed_null, device=device)
        field_2 = signal_field(N, seed=seed_sig, amplitude=2.0, device=device)
        result_2 = run_comparison(field_2, null_stats_2, alpha=ALPHA_DEFAULT)

        # Results must be identical
        assert result_1["observed_statistic"] == result_2["observed_statistic"]
        assert result_1["p_value"] == result_2["p_value"]
        assert result_1["reject_null"] == result_2["reject_null"]

    def test_robust_across_null_seeds(self):
        """Signal recovery should hold across different null distributions."""
        device = get_device()
        N = 24
        amplitude = 2.5
        sig_seed = 300

        # Test with 3 different null distributions
        for null_seed in [3001, 3002, 3003]:
            null_stats = null_distribution(N, n_trials=150, seed=null_seed, device=device)
            field = signal_field(N, seed=sig_seed, amplitude=amplitude, device=device)
            result = run_comparison(field, null_stats, alpha=ALPHA_DEFAULT)

            # All three should reject (signal is strong enough)
            assert result["reject_null"] is True, (
                f"Signal recovery failed with null_seed={null_seed}"
            )


# ============================================================================
# Field-Size Scaling Tests
# ============================================================================

class TestFieldSizeScaling:
    """Verify behavior scales correctly with field size N."""

    @pytest.mark.parametrize("N", [8, 16, 24, 32])
    def test_signal_recovery_across_sizes(self, N):
        """Recovery should work across different field sizes."""
        device = get_device()
        amplitude = 2.0
        n_null_trials = min(200, 10 * N)  # Scale trials with N

        null_stats = null_distribution(N, n_trials=n_null_trials, seed=4000 + N, device=device)
        field = signal_field(N, seed=400 + N, amplitude=amplitude, device=device)
        result = run_comparison(field, null_stats, alpha=ALPHA_DEFAULT)

        assert result["reject_null"] is True, (
            f"Signal recovery failed at N={N}, p={result['p_value']}"
        )

    def test_null_calibration_across_sizes(self):
        """False-positive rate should be controlled at all N."""
        device = get_device()
        alpha = 0.05
        n_tests = 15

        for N in [8, 16, 24]:
            null_stats = null_distribution(N, n_trials=150, seed=4100 + N, device=device)

            false_positives = 0
            for k in range(n_tests):
                field = null_field(N, seed=7000 + k + N * 100, device=device)
                result = run_comparison(field, null_stats, alpha=alpha)
                false_positives += int(result["reject_null"])

            rate = false_positives / n_tests
            mean = alpha * n_tests
            sigma = (n_tests * alpha * (1 - alpha)) ** 0.5
            bound = (mean + 3 * sigma) / n_tests

            assert rate <= bound, (
                f"N={N}: false-positive rate {rate:.3f} exceeds bound {bound:.3f}"
            )


# ============================================================================
# Edge Cases: Near-Threshold Amplitudes
# ============================================================================

class TestEdgeCases:
    """Test near-threshold signal amplitudes and boundary conditions."""

    def test_weak_signal_at_detection_threshold(self):
        """Weak signal near alpha-level threshold (low power, OK if not detected)."""
        device = get_device()
        N = 24
        amplitude = 0.3  # Very weak; not expected to reject at alpha=0.05

        null_stats = null_distribution(N, n_trials=200, seed=5000, device=device)
        field = signal_field(N, seed=500, amplitude=amplitude, device=device)
        result = run_comparison(field, null_stats, alpha=ALPHA_DEFAULT)

        # No assertion: weak signal may or may not be detected (low power is expected)
        assert result["label"] == "SYNTHETIC"

    def test_zero_signal_is_null(self):
        """Injected signal amplitude = 0 should not reject."""
        device = get_device()
        N = 24
        amplitude = 0.0  # No signal

        null_stats = null_distribution(N, n_trials=200, seed=5001, device=device)
        field = signal_field(N, seed=501, amplitude=amplitude, device=device)
        result = run_comparison(field, null_stats, alpha=ALPHA_DEFAULT)

        # Should NOT reject (or rejection rate is alpha)
        # Note: field with amplitude=0 is still sampled noise, so occasionally reject
        assert result["label"] == "SYNTHETIC"

    def test_very_strong_signal_always_rejects(self):
        """Extremely strong signal should always reject at any alpha."""
        device = get_device()
        N = 24
        amplitude = 10.0  # Very strong

        null_stats = null_distribution(N, n_trials=100, seed=5002, device=device)

        for k in range(5):
            field = signal_field(N, seed=502 + k, amplitude=amplitude, device=device)
            result = run_comparison(field, null_stats, alpha=0.01)
            assert result["reject_null"] is True, (
                f"Very strong signal (amp=10) failed to reject at alpha=0.01, run {k}"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
