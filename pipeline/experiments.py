"""Parametric exploration layer for dual-scale signal recovery analysis.

Systematically explores the (amplitude, noise, field_size) parameter space,
computing power curves, calibration, and effect sizes. All experiments labeled
TEST (synthetic pre-pin) or FIT (post-pin real data per PREDICTION.md gate).
"""
import numpy as np
import torch
from typing import NamedTuple
from dataclasses import dataclass, asdict

from pipeline.core import null_distribution, run_comparison
from pipeline.synthetic import signal_field, null_field, get_device


@dataclass
class ExperimentConfig:
    """Configuration for a parametric experiment."""
    field_size: int = 24
    amplitude: float = 2.0
    noise_sigma: float = 0.05
    alpha: float = 0.05
    n_null_trials: int = 300
    seed_base: int = 1000


@dataclass
class ExperimentResult:
    """Result of a single experiment trial."""
    config: dict  # serializable ExperimentConfig
    observed_statistic: float
    p_value: float
    reject_null: bool
    label: str  # "SYNTHETIC", "TEST", or "FIT"
    trial_seed: int


class PowerCurve(NamedTuple):
    """Power curve: (amplitudes, rejection_rates, 95%_CI_lower, 95%_CI_upper)"""
    amplitudes: np.ndarray
    rejection_rates: np.ndarray
    ci_lower: np.ndarray
    ci_upper: np.ndarray


class CalibrationCurve(NamedTuple):
    """False-positive rate curve: (alphas, observed_fp_rates, 95%_CI)"""
    alphas: np.ndarray
    fp_rates: np.ndarray
    ci_lower: np.ndarray
    ci_upper: np.ndarray


def estimate_power_curve(
    config: ExperimentConfig,
    amplitudes: np.ndarray,
    trials_per_amplitude: int = 20,
    device: torch.device | None = None,
) -> PowerCurve:
    """Estimate power curve: rejection rate as a function of signal amplitude.

    Parameters
    ----------
    config : ExperimentConfig
        Base configuration (noise, field size, etc.)
    amplitudes : np.ndarray
        Amplitudes to test (e.g., [0.5, 1.0, 2.0, 3.0, 4.0])
    trials_per_amplitude : int
        Trials per amplitude for stable estimates
    device : torch.device, optional
        Compute device; defaults to CUDA if available

    Returns
    -------
    PowerCurve
        Rejection rates and 95% binomial confidence intervals
    """
    device = device or get_device()
    null_stats = null_distribution(
        config.field_size, config.n_null_trials, config.seed_base, device
    )

    rejection_rates = []
    ci_lower = []
    ci_upper = []

    for amp in amplitudes:
        rejects = 0
        for trial in range(trials_per_amplitude):
            field = signal_field(
                config.field_size,
                seed=config.seed_base + 1000 + trial,
                amplitude=amp,
                noise_sigma=config.noise_sigma,
                device=device,
            )
            result = run_comparison(field, null_stats, alpha=config.alpha)
            rejects += int(result["reject_null"])

        rate = rejects / trials_per_amplitude
        rejection_rates.append(rate)

        # 95% binomial CI via normal approximation
        se = np.sqrt(rate * (1 - rate) / trials_per_amplitude)
        ci_lower.append(np.clip(rate - 1.96 * se, 0, 1))
        ci_upper.append(np.clip(rate + 1.96 * se, 0, 1))

    return PowerCurve(
        amplitudes=amplitudes,
        rejection_rates=np.array(rejection_rates),
        ci_lower=np.array(ci_lower),
        ci_upper=np.array(ci_upper),
    )


def estimate_false_positive_rate(
    config: ExperimentConfig,
    alphas: np.ndarray = np.array([0.01, 0.05, 0.10, 0.20]),
    trials_per_alpha: int = 50,
    device: torch.device | None = None,
) -> CalibrationCurve:
    """Estimate false-positive rate curve (calibration).

    Parameters
    ----------
    config : ExperimentConfig
        Base configuration (noise, field size, etc.)
    alphas : np.ndarray
        Nominal alpha levels to test
    trials_per_alpha : int
        Trials per alpha for stable estimates
    device : torch.device, optional
        Compute device

    Returns
    -------
    CalibrationCurve
        Empirical false-positive rates with 95% binomial CI
    """
    device = device or get_device()
    null_stats = null_distribution(
        config.field_size, config.n_null_trials, config.seed_base, device
    )

    fp_rates = []
    ci_lower = []
    ci_upper = []

    for alpha in alphas:
        fp_count = 0
        for trial in range(trials_per_alpha):
            field = null_field(
                config.field_size,
                seed=config.seed_base + 5000 + trial,
                noise_sigma=config.noise_sigma,
                device=device,
            )
            result = run_comparison(field, null_stats, alpha=alpha)
            fp_count += int(result["reject_null"])

        rate = fp_count / trials_per_alpha
        fp_rates.append(rate)

        # 95% binomial CI
        se = np.sqrt(rate * (1 - rate) / trials_per_alpha)
        ci_lower.append(np.clip(rate - 1.96 * se, 0, 1))
        ci_upper.append(np.clip(rate + 1.96 * se, 0, 1))

    return CalibrationCurve(
        alphas=alphas,
        fp_rates=np.array(fp_rates),
        ci_lower=np.array(ci_lower),
        ci_upper=np.array(ci_upper),
    )


def compute_effect_sizes(
    config: ExperimentConfig,
    device: torch.device | None = None,
) -> dict:
    """Compute effect size metrics (Cohen's d, signal-to-noise ratio).

    Returns
    -------
    dict
        - "cohens_d": standardized difference between signal and null
        - "snr": signal-to-noise ratio in the FFT domain
        - "null_mean": mean of null distribution
        - "null_std": std of null distribution
    """
    device = device or get_device()

    # Null stats
    null_stats = null_distribution(
        config.field_size, config.n_null_trials, config.seed_base, device
    )
    null_mean = float(np.mean(null_stats))
    null_std = float(np.std(null_stats))

    # Signal stats
    signal_stats = []
    for trial in range(20):
        field = signal_field(
            config.field_size,
            seed=config.seed_base + 100 + trial,
            amplitude=config.amplitude,
            noise_sigma=config.noise_sigma,
            device=device,
        )
        from pipeline.core import observed_statistic
        signal_stats.append(observed_statistic(field))

    signal_mean = float(np.mean(signal_stats))
    signal_std = float(np.std(signal_stats))

    # Cohen's d (pooled std)
    pooled_std = np.sqrt((null_std**2 + signal_std**2) / 2)
    cohens_d = (signal_mean - null_mean) / (pooled_std + 1e-10)

    # SNR approximation (ratio of signal to noise variance)
    snr = signal_std / (null_std + 1e-10)

    return {
        "cohens_d": float(cohens_d),
        "snr": float(snr),
        "null_mean": null_mean,
        "null_std": null_std,
        "signal_mean": signal_mean,
        "signal_std": signal_std,
    }
