"""Tests for parametric exploration and dual-scale analysis (EXECUTION_PLAN.md WP S3-02).

Merge-blocking per CLAUDE.md: all tests must pass and cover both the parametric
sweep infrastructure and the scale decomposition logic.
"""
import numpy as np
import torch
import pytest

from pipeline.experiments import (
    ExperimentConfig,
    estimate_power_curve,
    estimate_false_positive_rate,
    compute_effect_sizes,
)
from pipeline.scales import (
    decompose_scales,
    compute_scale_metrics,
    analyze_scale_mixing,
)
from pipeline.synthetic import get_device, signal_field, null_field


class TestExperimentConfig:
    """Test experiment configuration."""

    def test_config_defaults(self):
        config = ExperimentConfig()
        assert config.field_size == 24
        assert config.amplitude == 2.0
        assert config.noise_sigma == 0.05
        assert config.alpha == 0.05

    def test_config_custom_values(self):
        config = ExperimentConfig(
            field_size=32, amplitude=3.0, noise_sigma=0.1, alpha=0.01
        )
        assert config.field_size == 32
        assert config.amplitude == 3.0
        assert config.noise_sigma == 0.1
        assert config.alpha == 0.01


class TestPowerCurve:
    """Test power curve estimation."""

    def test_power_curve_increases_with_amplitude(self):
        """Higher amplitude signals should have higher rejection rates."""
        config = ExperimentConfig(field_size=16, n_null_trials=50)
        device = get_device()

        amplitudes = np.array([0.5, 1.5, 3.0])
        power = estimate_power_curve(
            config, amplitudes, trials_per_amplitude=10, device=device
        )

        assert len(power.amplitudes) == 3
        assert len(power.rejection_rates) == 3
        # Rejection rate should generally increase (allow some noise)
        assert power.rejection_rates[2] >= power.rejection_rates[0]

    def test_power_curve_ci_coverage(self):
        """Confidence intervals should bound rejection rates."""
        config = ExperimentConfig(field_size=16, n_null_trials=50)
        device = get_device()

        amplitudes = np.array([1.0, 2.0])
        power = estimate_power_curve(
            config, amplitudes, trials_per_amplitude=10, device=device
        )

        for i in range(len(amplitudes)):
            assert power.ci_lower[i] <= power.rejection_rates[i]
            assert power.rejection_rates[i] <= power.ci_upper[i]
            assert 0 <= power.ci_lower[i] <= 1
            assert 0 <= power.ci_upper[i] <= 1


class TestCalibration:
    """Test false-positive rate calibration."""

    def test_fpr_increases_with_alpha(self):
        """Higher alpha should have higher false-positive rates."""
        config = ExperimentConfig(field_size=16, n_null_trials=100)
        device = get_device()

        alphas = np.array([0.01, 0.05, 0.10])
        calib = estimate_false_positive_rate(
            config, alphas, trials_per_alpha=20, device=device
        )

        assert len(calib.alphas) == 3
        assert len(calib.fp_rates) == 3
        # FP rate should increase with nominal alpha
        assert calib.fp_rates[2] >= calib.fp_rates[0]

    def test_fpr_ci_valid(self):
        """Calibration CIs should be valid (lower <= rate <= upper)."""
        config = ExperimentConfig(field_size=16, n_null_trials=100)
        device = get_device()

        alphas = np.array([0.05])
        calib = estimate_false_positive_rate(
            config, alphas, trials_per_alpha=15, device=device
        )

        for i in range(len(alphas)):
            assert calib.ci_lower[i] <= calib.fp_rates[i]
            assert calib.fp_rates[i] <= calib.ci_upper[i]


class TestEffectSizes:
    """Test effect size computation."""

    def test_effect_sizes_positive(self):
        """Effect size metrics should be positive and finite."""
        config = ExperimentConfig(field_size=16, amplitude=2.0)
        device = get_device()

        effects = compute_effect_sizes(config, device=device)

        assert effects["cohens_d"] >= 0
        assert effects["snr"] >= 0
        assert effects["null_std"] > 0
        assert effects["signal_std"] > 0
        assert np.isfinite(effects["cohens_d"])
        assert np.isfinite(effects["snr"])

    def test_effect_sizes_stronger_signal_larger_d(self):
        """Stronger amplitude should yield larger Cohen's d."""
        device = get_device()

        config_weak = ExperimentConfig(field_size=16, amplitude=0.5)
        effects_weak = compute_effect_sizes(config_weak, device=device)

        config_strong = ExperimentConfig(field_size=16, amplitude=3.0)
        effects_strong = compute_effect_sizes(config_strong, device=device)

        assert effects_strong["cohens_d"] >= effects_weak["cohens_d"]


class TestScaleDecomposition:
    """Test dual-scale FFT decomposition."""

    def test_decomposition_reconstructs_field(self):
        """Coarse + fine should approximately equal the full field."""
        device = get_device()
        field = signal_field(16, seed=42, amplitude=2.0, device=device)

        decomp = decompose_scales(field)

        # Reconstruction
        reconstructed = decomp.coarse + decomp.fine
        error = torch.norm(field - reconstructed).item()
        field_norm = torch.norm(field).item()

        # Error should be small (numerical precision)
        relative_error = error / (field_norm + 1e-10)
        assert relative_error < 1e-3

    def test_decomposition_cutoff_parameter(self):
        """Custom cutoff frequency should produce different results."""
        device = get_device()
        field = signal_field(24, seed=42, amplitude=2.0, device=device)

        decomp_coarse = decompose_scales(field, cutoff_freq=6.0)
        decomp_fine = decompose_scales(field, cutoff_freq=3.0)

        # Lower cutoff should put more energy in fine
        coarse_energy_1 = torch.norm(decomp_coarse.coarse).item()
        coarse_energy_2 = torch.norm(decomp_fine.coarse).item()
        assert coarse_energy_2 <= coarse_energy_1

    def test_decomposition_produces_real_fields(self):
        """Coarse and fine should be real-valued (no imaginary parts)."""
        device = get_device()
        field = signal_field(16, seed=42, amplitude=2.0, device=device)

        decomp = decompose_scales(field)

        # Check dtype is floating point (not complex)
        assert decomp.coarse.dtype in [torch.float32, torch.float64]
        assert decomp.fine.dtype in [torch.float32, torch.float64]


class TestScaleMetrics:
    """Test scale-specific signal recovery metrics."""

    def test_scale_metrics_valid_values(self):
        """Scale metrics should be finite and physically meaningful."""
        device = get_device()
        field = signal_field(16, seed=42, amplitude=2.0, device=device)

        metrics = compute_scale_metrics(field, scale="test")

        assert metrics.scale == "test"
        assert metrics.energy_ratio >= 0
        assert metrics.snr_per_scale >= 0
        assert metrics.peak_frequency >= 0
        assert np.isfinite(metrics.energy_ratio)
        assert np.isfinite(metrics.snr_per_scale)
        assert np.isfinite(metrics.peak_frequency)

    def test_signal_field_higher_energy_than_null(self):
        """Signal field should have higher energy ratio than null field."""
        device = get_device()

        signal = signal_field(16, seed=42, amplitude=2.0, device=device)
        null = null_field(16, seed=42, device=device)

        metrics_signal = compute_scale_metrics(signal, scale="signal")
        metrics_null = compute_scale_metrics(null, scale="null")

        assert metrics_signal.energy_ratio > metrics_null.energy_ratio


class TestScaleMixing:
    """Test scale-mixing (orthogonality between coarse and fine)."""

    def test_scale_mixing_orthogonality_low(self):
        """Well-separated scales should have low orthogonality violation."""
        device = get_device()
        field = signal_field(24, seed=42, amplitude=2.0, device=device)

        decomp = decompose_scales(field, cutoff_freq=6.0)
        mixing = analyze_scale_mixing(field, decomp)

        # Orthogonality violation should be small (ideally 0)
        assert mixing["orthogonality_violation"] >= 0
        assert mixing["orthogonality_violation"] < 1.0

    def test_scale_mixing_energy_conservation(self):
        """Decomposition should conserve energy (Parseval's theorem)."""
        device = get_device()
        field = signal_field(16, seed=42, amplitude=2.0, device=device)

        decomp = decompose_scales(field)
        mixing = analyze_scale_mixing(field, decomp)

        # Energy conservation error should be very small
        assert mixing["energy_conservation_error"] < 1e-2

    def test_scale_mixing_cross_correlation(self):
        """Cross-correlation between independent scales should be near 0."""
        device = get_device()
        field = signal_field(16, seed=42, amplitude=2.0, device=device)

        decomp = decompose_scales(field, cutoff_freq=4.0)
        mixing = analyze_scale_mixing(field, decomp)

        # Cross-correlation should be small for orthogonal scales
        # (allow some coupling due to discretization)
        assert abs(mixing["cross_correlation"]) < 0.3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
