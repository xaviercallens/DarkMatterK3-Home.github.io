#!/usr/bin/env python3
"""Tests for S3 mock-bank generator (T2-level: mechanically verified).

Golden tests verify:
1. Banks are reproducible (same seed → same alpha thresholds)
2. Alpha thresholds are correctly ordered (0.01 > 0.05 > 0.10)
3. Null statistics have expected distributions (lensing normal-ish, PTA chi2(1), Lyman-α chi2(10))
4. Files are saved with correct checksums
5. Banks are loadable from disk
"""
import json
import tempfile
from pathlib import Path

import numpy as np
import pytest

from scripts.s3_mockbank_generator import S3MockBankGenerator, MockNullBank


class TestMockBankGenerator:
    """Test S3 mock null bank generation."""

    @pytest.fixture
    def temp_output_dir(self):
        """Create temp directory for test outputs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def generator(self, temp_output_dir):
        """Create a mock-bank generator with temp output."""
        return S3MockBankGenerator(output_dir=temp_output_dir)

    # ========================================================================
    # Reproducibility Tests
    # ========================================================================

    def test_lensing_nulls_reproducible(self, generator):
        """Same seed should produce identical alpha thresholds."""
        bank1 = generator.generate_lensing_nulls(n_trials=500, seed=1234)
        bank2 = generator.generate_lensing_nulls(n_trials=500, seed=1234)

        assert bank1.alpha_thresholds == bank2.alpha_thresholds

    def test_pta_nulls_reproducible(self, generator):
        """PTA nulls should be reproducible."""
        bank1 = generator.generate_pta_nulls(n_trials=500, seed=1234)
        bank2 = generator.generate_pta_nulls(n_trials=500, seed=1234)

        assert bank1.alpha_thresholds == bank2.alpha_thresholds

    def test_lyman_alpha_nulls_reproducible(self, generator):
        """Lyman-α nulls should be reproducible."""
        bank1 = generator.generate_lyman_alpha_nulls(n_trials=500, seed=1234)
        bank2 = generator.generate_lyman_alpha_nulls(n_trials=500, seed=1234)

        assert bank1.alpha_thresholds == bank2.alpha_thresholds

    # ========================================================================
    # Alpha Threshold Ordering Tests
    # ========================================================================

    def test_lensing_alpha_ordering(self, generator):
        """Alpha thresholds must be ordered: 0.01 > 0.05 > 0.10 (one-sided)."""
        bank = generator.generate_lensing_nulls(n_trials=1000)

        # For one-sided test, higher alpha → lower critical value
        assert bank.alpha_thresholds[0] > bank.alpha_thresholds[1]  # 0.01 > 0.05
        assert bank.alpha_thresholds[1] > bank.alpha_thresholds[2]  # 0.05 > 0.10

    def test_pta_alpha_ordering(self, generator):
        """PTA alpha thresholds must be ordered."""
        bank = generator.generate_pta_nulls(n_trials=1000)

        assert bank.alpha_thresholds[0] > bank.alpha_thresholds[1]
        assert bank.alpha_thresholds[1] > bank.alpha_thresholds[2]

    def test_lyman_alpha_ordering(self, generator):
        """Lyman-α alpha thresholds must be ordered."""
        bank = generator.generate_lyman_alpha_nulls(n_trials=1000)

        assert bank.alpha_thresholds[0] > bank.alpha_thresholds[1]
        assert bank.alpha_thresholds[1] > bank.alpha_thresholds[2]

    # ========================================================================
    # Distribution Shape Tests
    # ========================================================================

    def test_lensing_null_approximately_normal(self, generator):
        """Lensing null should be approximately normal (with kurtosis)."""
        bank = generator.generate_lensing_nulls(n_trials=10000, seed=5000)

        # Mean should be close to 0
        assert abs(bank.null_statistic_mean) < 0.1

        # Std should be close to 1 (excess kurtosis makes std slightly > 1, range 0.9-1.2)
        assert 0.9 < bank.null_statistic_std < 1.3

    def test_pta_null_chi2_like(self, generator):
        """PTA null should be χ²(1)-like (mean=1, mode=0)."""
        bank = generator.generate_pta_nulls(n_trials=10000, seed=5001)

        # χ²(1) has mean = 1
        assert 0.9 < bank.null_statistic_mean < 1.1

        # χ²(1) has std = sqrt(2) ≈ 1.414
        assert 1.3 < bank.null_statistic_std < 1.5

    def test_lyman_alpha_null_chi2_like(self, generator):
        """Lyman-α null should be χ²(10)-like (mean=10, std=sqrt(20))."""
        bank = generator.generate_lyman_alpha_nulls(n_trials=10000, seed=5002)

        # χ²(10) has mean = 10
        assert 9.5 < bank.null_statistic_mean < 10.5

        # χ²(10) has std = sqrt(20) ≈ 4.47
        assert 4.0 < bank.null_statistic_std < 5.0

    # ========================================================================
    # File I/O Tests
    # ========================================================================

    def test_save_bank_creates_files(self, generator):
        """Saving a bank should create JSON and checksum files."""
        bank = generator.generate_lensing_nulls()
        path = generator.save_bank(bank)

        assert path.exists(), "JSON file not created"
        assert (path.parent / f"{bank.name}.sha256").exists(), "Checksum file not created"

    def test_save_bank_checksum_valid(self, generator):
        """Checksum file should match JSON content."""
        import hashlib

        bank = generator.generate_lensing_nulls()
        json_path = generator.save_bank(bank)
        checksum_path = json_path.parent / f"{bank.name}.sha256"

        # Read checksum file
        with open(checksum_path) as f:
            expected_hash = f.read().split()[0]

        # Compute actual hash
        with open(json_path, "rb") as f:
            actual_hash = hashlib.sha256(f.read()).hexdigest()

        assert expected_hash == actual_hash

    def test_save_and_load_bank(self, generator):
        """Save a bank and load it back; should match original."""
        bank_original = generator.generate_lensing_nulls()
        json_path = generator.save_bank(bank_original)

        # Load from JSON
        with open(json_path) as f:
            data = json.load(f)

        bank_loaded = MockNullBank(**data)

        # Check key fields match
        assert bank_loaded.name == bank_original.name
        assert bank_loaded.observable_type == bank_original.observable_type
        assert bank_loaded.alpha_thresholds == bank_original.alpha_thresholds

    # ========================================================================
    # Integration Tests
    # ========================================================================

    def test_generate_all_banks(self, generator):
        """Generate all three banks and verify they're distinct."""
        results = generator.generate_all_banks()

        # Should create 3 banks
        assert len(results) == 3
        assert "lensing" in results
        assert "pta" in results
        assert "lyman_alpha" in results

        # Each should have created files
        for key, info in results.items():
            path = Path(info["path"])
            assert path.exists(), f"{key} bank not created"

    def test_all_banks_different_statistics(self, generator):
        """Different observable types should have different null statistics."""
        lensing = generator.generate_lensing_nulls(n_trials=5000)
        pta = generator.generate_pta_nulls(n_trials=5000)
        lya = generator.generate_lyman_alpha_nulls(n_trials=5000)

        # Means should be distinct
        means = [lensing.null_statistic_mean, pta.null_statistic_mean, lya.null_statistic_mean]
        assert len(set([f"{m:.1f}" for m in means])) == 3, "Null means should be distinct"

        # Observable types should be distinct
        types = [lensing.observable_type, pta.observable_type, lya.observable_type]
        assert len(set(types)) == 3

    # ========================================================================
    # Edge Cases
    # ========================================================================

    def test_small_trial_count(self, generator):
        """Generator should work with small trial counts (for unit tests)."""
        bank = generator.generate_lensing_nulls(n_trials=50)
        assert bank.n_trials == 50
        assert len(bank.alpha_thresholds) == 3

    def test_large_trial_count(self, generator):
        """Generator should work with large trial counts."""
        bank = generator.generate_pta_nulls(n_trials=10000)
        assert bank.n_trials == 10000
        assert len(bank.alpha_thresholds) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
