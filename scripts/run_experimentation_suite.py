#!/usr/bin/env python3
"""Demo: Run the parametric exploration and dual-scale analysis suite.

Usage:
    python scripts/run_experimentation_suite.py [--output-dir LOGS]

This script demonstrates the improved experimentation layer:
  1. Power curve estimation (rejection rate vs signal amplitude)
  2. False-positive rate calibration
  3. Effect size computation (Cohen's d, SNR)
  4. Dual-scale signal decomposition
  5. Scale-mixing analysis

All results are logged to logs/experiments.json and summarized in OBSERVATIONAL_REPORT.md.
"""
import json
import sys
import argparse
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

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
from pipeline.experiment_log import ExperimentLogger, ObservationalReportWriter
from pipeline.synthetic import signal_field, get_device


def main():
    parser = argparse.ArgumentParser(
        description="Run parametric exploration and dual-scale analysis"
    )
    parser.add_argument(
        "--output-dir",
        default="logs",
        help="Output directory for experiment logs",
    )
    parser.add_argument(
        "--field-size",
        type=int,
        default=24,
        help="Field size (n for nxnxn cube)",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick run with fewer trials (for testing)",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    device = get_device()
    logger = ExperimentLogger(output_dir / "experiments.json")

    print("=" * 70)
    print("PARAMETRIC EXPLORATION & DUAL-SCALE ANALYSIS")
    print("=" * 70)
    print()

    # Power curve estimation
    print("1. Power Curve Estimation")
    print("-" * 70)
    config = ExperimentConfig(
        field_size=args.field_size,
        n_null_trials=50 if args.quick else 300,
    )
    amplitudes = np.array([0.5, 1.0, 1.5, 2.0, 3.0, 4.0])
    trials_per_amp = 5 if args.quick else 20

    power = estimate_power_curve(
        config, amplitudes, trials_per_amplitude=trials_per_amp, device=device
    )
    print(f"Tested {len(amplitudes)} amplitudes with {trials_per_amp} trials each")
    print("\nAmplitude | Rejection Rate | CI Lower | CI Upper")
    print("-" * 50)
    for amp, rate, ci_l, ci_u in zip(
        power.amplitudes, power.rejection_rates, power.ci_lower, power.ci_upper
    ):
        print(f"  {amp:5.1f}   |     {rate:5.2%}     | {ci_l:6.2%}  | {ci_u:6.2%}")

    logger.log_experiment(
        "power_curve",
        {
            "field_size": config.field_size,
            "n_null_trials": config.n_null_trials,
            "trials_per_amplitude": trials_per_amp,
        },
        {
            "amplitudes": power.amplitudes.tolist(),
            "rejection_rates": power.rejection_rates.tolist(),
            "ci_lower": power.ci_lower.tolist(),
            "ci_upper": power.ci_upper.tolist(),
        },
        label="SYNTHETIC",
    )
    print()

    # False-positive rate calibration
    print("2. False-Positive Rate Calibration")
    print("-" * 70)
    alphas = np.array([0.01, 0.05, 0.10])
    trials_per_alpha = 10 if args.quick else 30

    calib = estimate_false_positive_rate(
        config, alphas, trials_per_alpha=trials_per_alpha, device=device
    )
    print(f"Tested {len(alphas)} alpha levels with {trials_per_alpha} trials each")
    print("\n Alpha  | FP Rate | CI Lower | CI Upper")
    print("-" * 40)
    for alpha, rate, ci_l, ci_u in zip(
        calib.alphas, calib.fp_rates, calib.ci_lower, calib.ci_upper
    ):
        print(f" {alpha:5.2f} | {rate:6.2%}  | {ci_l:6.2%}  | {ci_u:6.2%}")

    logger.log_experiment(
        "calibration",
        {"field_size": config.field_size, "trials_per_alpha": trials_per_alpha},
        {
            "alphas": calib.alphas.tolist(),
            "fp_rates": calib.fp_rates.tolist(),
            "ci_lower": calib.ci_lower.tolist(),
            "ci_upper": calib.ci_upper.tolist(),
        },
        label="SYNTHETIC",
    )
    print()

    # Effect sizes
    print("3. Effect Size Metrics")
    print("-" * 70)
    effects = compute_effect_sizes(config, device=device)
    print(f"Config: amplitude={config.amplitude}, noise_sigma={config.noise_sigma}")
    print(f"\nCohen's d (standardized difference): {effects['cohens_d']:.3f}")
    print(f"SNR (signal/noise ratio):            {effects['snr']:.3f}")
    print(f"Null distribution mean:              {effects['null_mean']:.4f}")
    print(f"Null distribution std:               {effects['null_std']:.4f}")
    print(f"Signal mean:                         {effects['signal_mean']:.4f}")
    print(f"Signal std:                          {effects['signal_std']:.4f}")

    logger.log_experiment(
        "effect_sizes", {"field_size": config.field_size}, effects, label="SYNTHETIC"
    )
    print()

    # Dual-scale analysis
    print("4. Dual-Scale Signal Decomposition")
    print("-" * 70)
    field = signal_field(
        config.field_size,
        seed=42,
        amplitude=config.amplitude,
        noise_sigma=config.noise_sigma,
        device=device,
    )

    decomp = decompose_scales(field)
    coarse_metrics = compute_scale_metrics(decomp.coarse, scale="coarse")
    fine_metrics = compute_scale_metrics(decomp.fine, scale="fine")

    print(f"Field size: {config.field_size}³")
    print(f"Frequency cutoff: {decomp.cutoff_freq:.1f}")
    print()
    print("COARSE (low-freq) component:")
    print(f"  Energy ratio:        {coarse_metrics.energy_ratio:.4f}")
    print(f"  Contrast recovery:   {coarse_metrics.contrast_recovery:.4f}")
    print(f"  SNR:                 {coarse_metrics.snr_per_scale:.3f}")
    print(f"  Peak frequency:      {coarse_metrics.peak_frequency:.2f}")
    print()
    print("FINE (high-freq) component:")
    print(f"  Energy ratio:        {fine_metrics.energy_ratio:.4f}")
    print(f"  Contrast recovery:   {fine_metrics.contrast_recovery:.4f}")
    print(f"  SNR:                 {fine_metrics.snr_per_scale:.3f}")
    print(f"  Peak frequency:      {fine_metrics.peak_frequency:.2f}")

    # Scale mixing analysis
    mixing = analyze_scale_mixing(field, decomp)
    print()
    print("SCALE MIXING ANALYSIS:")
    print(f"  Orthogonality violation: {mixing['orthogonality_violation']:.6f}")
    print(f"  Energy conservation:     {mixing['energy_conservation_error']:.6f}")
    print(f"  Cross-correlation:       {mixing['cross_correlation']:.4f}")

    logger.log_experiment(
        "dual_scale",
        {
            "field_size": config.field_size,
            "cutoff_freq": decomp.cutoff_freq,
            "amplitude": config.amplitude,
        },
        {
            "coarse_metrics": {
                "energy_ratio": coarse_metrics.energy_ratio,
                "contrast_recovery": coarse_metrics.contrast_recovery,
                "snr": coarse_metrics.snr_per_scale,
                "peak_frequency": coarse_metrics.peak_frequency,
            },
            "fine_metrics": {
                "energy_ratio": fine_metrics.energy_ratio,
                "contrast_recovery": fine_metrics.contrast_recovery,
                "snr": fine_metrics.snr_per_scale,
                "peak_frequency": fine_metrics.peak_frequency,
            },
            "scale_mixing": mixing,
        },
        label="SYNTHETIC",
    )
    print()

    # Summary
    print("=" * 70)
    print("EXPERIMENT LOG SUMMARY")
    print("=" * 70)
    summary = logger.get_summary()
    print(f"Total experiments logged: {summary['count']}")
    print(f"Log file: {logger.log_path}")
    print()

    # Auto-update OBSERVATIONAL_REPORT
    reporter = ObservationalReportWriter(repo_root=Path(__file__).parent.parent)
    reporter.write_report_stub()
    print(f"Auto-generated report stub: {reporter.report_path}")
    print()
    print("✓ Experimentation suite complete!")


if __name__ == "__main__":
    main()
