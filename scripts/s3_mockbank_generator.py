#!/usr/bin/env python3
"""S3 Mock-Bank Generator — Synthetic null distributions for S3-02 testing.

Purpose: Generate reference null distributions (mock-sky, mock-timing, mock-lensing)
that S3-02 pipeline can use to calibrate test/FIT decision boundaries before
real-data comparisons.

This is T2 work: mechanically specified null-generation with golden tests.
Not meant for real predictions (real nulls come from data); meant for
robustness testing, calibration validation, and CI integration checks.

Generates three distinct null banks:
1. Mock-sky nulls (lensing observable null distribution, SDSS-like)
2. Mock-timing nulls (PTA observable null distribution, NANOGrav-like)
3. Mock-spectrum nulls (small-scale structure constraints, Lyman-α-like)
"""
import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data" / "nullbanks"


@dataclass
class MockNullBank:
    """A single mock null distribution for calibration."""

    name: str
    description: str
    observable_type: str  # "lensing" | "pta" | "lyman_alpha"
    null_statistic_mean: float
    null_statistic_std: float
    n_trials: int
    seed: int
    alpha_thresholds: List[float]  # Critical values for [0.01, 0.05, 0.10]
    provenance: str  # "synthetic_mock_v1"
    calibration_notes: str


class S3MockBankGenerator:
    """Generate and store mock null distributions for S3-02 testing."""

    def __init__(self, output_dir: Path = DATA_DIR):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_lensing_nulls(self, n_trials: int = 1000, seed: int = 7000) -> MockNullBank:
        """Generate mock null distribution for lensing observable (weak-lensing stacked profiles).

        Context: P1 (lensing) tests whether observed core-radius scaling β differs
        from ΛCDM prediction. Mock null assumes pure-CDM halo profiles with SDSS-like
        observational scatter.

        Args:
            n_trials: Number of mock null realizations
            seed: RNG seed for reproducibility

        Returns:
            MockNullBank with alpha thresholds calibrated at [0.01, 0.05, 0.10]
        """
        rng = np.random.RandomState(seed)

        # Mock lensing statistic: test-statistic for core-radius scaling deviation.
        # Under null (ΛCDM), this is approximately N(0, 1) with mild fat tails.
        # Add 15% excess kurtosis to simulate observational systematics.
        base_normal = rng.standard_normal(n_trials)
        kurtosis_term = 0.15 * rng.standard_normal(n_trials) ** 3
        null_stats = base_normal + kurtosis_term

        mean = np.mean(null_stats)
        std = np.std(null_stats)

        # Critical values at alpha thresholds (one-sided test)
        alpha_thresholds = [
            float(np.percentile(null_stats, 99)),    # alpha=0.01
            float(np.percentile(null_stats, 95)),    # alpha=0.05
            float(np.percentile(null_stats, 90)),    # alpha=0.10
        ]

        return MockNullBank(
            name="mock_lensing_sdss",
            description="Mock weak-lensing null: SDSS-like core-radius scaling statistic under ΛCDM",
            observable_type="lensing",
            null_statistic_mean=float(mean),
            null_statistic_std=float(std),
            n_trials=n_trials,
            seed=seed,
            alpha_thresholds=alpha_thresholds,
            provenance="synthetic_mock_v1",
            calibration_notes="Mock null assumes pure-CDM profiles (NFW) with 15% excess kurtosis from observational systematics",
        )

    def generate_pta_nulls(self, n_trials: int = 1000, seed: int = 7001) -> MockNullBank:
        """Generate mock null distribution for PTA observable (pulsar-timing residuals).

        Context: P2 (PTA) tests whether observed timing residuals show a spectral
        signature consistent with ultralight dark matter. Mock null assumes GW-background-only
        (no ultralight scalar signal).

        Args:
            n_trials: Number of mock null realizations (fewer because expensive)
            seed: RNG seed

        Returns:
            MockNullBank with alpha thresholds
        """
        rng = np.random.RandomState(seed)

        # Mock PTA statistic: log-likelihood ratio (2 * Δ log L) for ultralight scalar signal.
        # Under null (no scalar), this is approximately χ²(1) (one extra parameter in signal model).
        # Approximate χ²(1) as |Z|² where Z ~ N(0, 1).
        z_scores = rng.standard_normal(n_trials)
        null_stats = z_scores ** 2

        mean = np.mean(null_stats)
        std = np.std(null_stats)

        alpha_thresholds = [
            float(np.percentile(null_stats, 99)),
            float(np.percentile(null_stats, 95)),
            float(np.percentile(null_stats, 90)),
        ]

        return MockNullBank(
            name="mock_pta_nanograv",
            description="Mock PTA null: GW-background-only (no ultralight scalar) under NANOGrav-like conditions",
            observable_type="pta",
            null_statistic_mean=float(mean),
            null_statistic_std=float(std),
            n_trials=n_trials,
            seed=seed,
            alpha_thresholds=alpha_thresholds,
            provenance="synthetic_mock_v1",
            calibration_notes="Mock null is χ²(1) (LRT for scalar amplitude = 0) under GW-background-only hypothesis",
        )

    def generate_lyman_alpha_nulls(self, n_trials: int = 1000, seed: int = 7002) -> MockNullBank:
        """Generate mock null distribution for Lyman-α observable (small-scale power constraint).

        Context: Lyman-α acts as a null check: ultra-light dark matter should NOT
        significantly modify small-scale power where standard constraints apply.
        Mock null assumes standard ΛCDM power spectrum.

        Args:
            n_trials: Number of mock null realizations
            seed: RNG seed

        Returns:
            MockNullBank with alpha thresholds
        """
        rng = np.random.RandomState(seed)

        # Mock Lyman-α statistic: chi-square goodness-of-fit for power spectrum.
        # Degrees of freedom ~ 10 (number of k-bins in forest).
        # Under null (ΛCDM), approximately χ²(10).
        null_stats = rng.chisquare(df=10, size=n_trials)

        mean = np.mean(null_stats)
        std = np.std(null_stats)

        alpha_thresholds = [
            float(np.percentile(null_stats, 99)),
            float(np.percentile(null_stats, 95)),
            float(np.percentile(null_stats, 90)),
        ]

        return MockNullBank(
            name="mock_lyman_alpha_xq100",
            description="Mock Lyman-α null: χ²(10) goodness-of-fit for ΛCDM power spectrum",
            observable_type="lyman_alpha",
            null_statistic_mean=float(mean),
            null_statistic_std=float(std),
            n_trials=n_trials,
            seed=seed,
            alpha_thresholds=alpha_thresholds,
            provenance="synthetic_mock_v1",
            calibration_notes="Mock null is χ²(10) over 10 Lyman-α forest k-bins; assumes ΛCDM power",
        )

    def save_bank(self, bank: MockNullBank) -> Path:
        """Save a mock null bank to JSON with checksum."""
        data = asdict(bank)
        json_path = self.output_dir / f"{bank.name}.json"

        with open(json_path, "w") as f:
            json.dump(data, f, indent=2)

        # Compute SHA256 of the JSON file
        with open(json_path, "rb") as f:
            sha256 = hashlib.sha256(f.read()).hexdigest()

        # Write a checksum file
        checksum_path = self.output_dir / f"{bank.name}.sha256"
        with open(checksum_path, "w") as f:
            f.write(f"{sha256}  {json_path.name}\n")

        return json_path

    def generate_all_banks(self) -> dict:
        """Generate all three mock null banks and save to disk."""
        banks = {
            "lensing": self.generate_lensing_nulls(),
            "pta": self.generate_pta_nulls(),
            "lyman_alpha": self.generate_lyman_alpha_nulls(),
        }

        results = {}
        for key, bank in banks.items():
            path = self.save_bank(bank)
            results[key] = {
                "path": str(path),
                "name": bank.name,
                "observable_type": bank.observable_type,
            }

        return results


def main():
    """Generate all mock null banks."""
    gen = S3MockBankGenerator()
    results = gen.generate_all_banks()

    print("✓ Mock null banks generated:")
    for key, info in results.items():
        print(f"  {key}: {info['path']}")

    # Summary statistics
    print("\nSummary:")
    print(f"  Output directory: {gen.output_dir}")
    print(f"  Banks generated: {len(results)}")


if __name__ == "__main__":
    main()
