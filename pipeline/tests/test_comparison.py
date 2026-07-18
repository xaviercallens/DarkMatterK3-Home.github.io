#!/usr/bin/env python3
"""Tests for S3-02 comparison framework (TEST/FIT machinery, mock-bank integration).

Golden tests verify:
1. Mock banks load correctly
2. Observables compute critical values from alpha levels
3. Comparisons correctly reject/accept null
4. TEST/FIT labels are mechanical (depend on observable type, not result)
5. Assumption tags are correct per observable
6. Pre-G1 (synthetic) label enforcement works
"""
import json
import tempfile
from pathlib import Path

import numpy as np
import pytest

from pipeline.comparison import (
    ComparisonPipeline,
    LensingComparison,
    LymanAlphaComparison,
    MockNullBank,
    NullBankManager,
    PTAComparison,
)


class TestNullBankManager:
    """Test loading and managing mock null banks."""

    @pytest.fixture
    def temp_nullbank_dir(self):
        """Create temp directory with a mock null bank."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Create a simple mock null bank
            bank_data = {
                "name": "test_mock_bank",
                "description": "Test bank",
                "observable_type": "lensing",
                "null_statistic_mean": 0.5,
                "null_statistic_std": 1.0,
                "n_trials": 1000,
                "seed": 999,
                "alpha_thresholds": [2.5, 1.6, 1.3],  # 99th, 95th, 90th
                "provenance": "test",
                "calibration_notes": "Test bank",
            }
            bank_path = tmpdir / "test_mock_bank.json"
            with open(bank_path, "w") as f:
                json.dump(bank_data, f)

            yield tmpdir

    def test_load_bank_from_disk(self, temp_nullbank_dir):
        """Load a mock null bank from disk."""
        manager = NullBankManager(temp_nullbank_dir)
        bank = manager.load_bank("test_mock_bank")

        assert bank.name == "test_mock_bank"
        assert bank.observable_type == "lensing"
        assert bank.alpha_thresholds == [2.5, 1.6, 1.3]

    def test_load_bank_caching(self, temp_nullbank_dir):
        """Second load should return cached instance."""
        manager = NullBankManager(temp_nullbank_dir)
        bank1 = manager.load_bank("test_mock_bank")
        bank2 = manager.load_bank("test_mock_bank")

        assert bank1 is bank2  # Same object

    def test_load_nonexistent_bank_raises(self, temp_nullbank_dir):
        """Loading a nonexistent bank should raise."""
        manager = NullBankManager(temp_nullbank_dir)
        with pytest.raises(FileNotFoundError):
            manager.load_bank("nonexistent_bank")

    def test_alpha_threshold_lookup(self, temp_nullbank_dir):
        """Get critical values for specific alpha levels."""
        manager = NullBankManager(temp_nullbank_dir)

        # alpha=0.01 → 99th percentile (index 0)
        assert manager.get_alpha_threshold("test_mock_bank", 0.01) == 2.5

        # alpha=0.05 → 95th percentile (index 1)
        assert manager.get_alpha_threshold("test_mock_bank", 0.05) == 1.6

        # alpha=0.10 → 90th percentile (index 2)
        assert manager.get_alpha_threshold("test_mock_bank", 0.10) == 1.3

    def test_alpha_threshold_invalid_alpha_raises(self, temp_nullbank_dir):
        """Invalid alpha level should raise."""
        manager = NullBankManager(temp_nullbank_dir)
        with pytest.raises(ValueError):
            manager.get_alpha_threshold("test_mock_bank", 0.03)


class TestLensingComparison:
    """Test lensing observable comparison."""

    @pytest.fixture
    def temp_nullbank_dir(self):
        """Create temp directory with lensing mock bank."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            bank_data = {
                "name": "mock_lensing_sdss",
                "description": "Mock lensing bank",
                "observable_type": "lensing",
                "null_statistic_mean": 0.0,
                "null_statistic_std": 1.0,
                "n_trials": 1000,
                "seed": 7000,
                "alpha_thresholds": [2.33, 1.64, 1.28],  # 99th, 95th, 90th
                "provenance": "test",
                "calibration_notes": "Test",
            }
            bank_path = tmpdir / "mock_lensing_sdss.json"
            with open(bank_path, "w") as f:
                json.dump(bank_data, f)

            yield tmpdir

    def test_lensing_reject_null(self, temp_nullbank_dir):
        """Observed statistic > critical value → reject null."""
        manager = NullBankManager(temp_nullbank_dir)
        comparison = LensingComparison(manager)

        # Observed = 2.5 > critical (1.64 at alpha=0.05) → reject
        result = comparison.compare(2.5, alpha=0.05, synthetic=True)

        assert result.reject_null is True
        assert result.observed_statistic == 2.5
        assert result.critical_value == 1.64

    def test_lensing_accept_null(self, temp_nullbank_dir):
        """Observed statistic < critical value → accept null."""
        manager = NullBankManager(temp_nullbank_dir)
        comparison = LensingComparison(manager)

        # Observed = 0.5 < critical (1.64 at alpha=0.05) → accept
        result = comparison.compare(0.5, alpha=0.05, synthetic=True)

        assert result.reject_null is False
        assert result.observed_statistic == 0.5

    def test_lensing_label_synthetic_pre_g1(self, temp_nullbank_dir):
        """Pre-G1 (unpinned), synthetic=True → SYNTHETIC label."""
        manager = NullBankManager(temp_nullbank_dir)
        comparison = LensingComparison(manager)

        result = comparison.compare(2.5, alpha=0.05, synthetic=True)

        assert result.label == "SYNTHETIC"

    def test_lensing_assumption_tags(self, temp_nullbank_dir):
        """Lensing should carry [A-SEQ, A-VOL, A-ONT] tags."""
        manager = NullBankManager(temp_nullbank_dir)
        comparison = LensingComparison(manager)

        result = comparison.compare(1.0, alpha=0.05, synthetic=True)

        assert set(result.assumption_tags) == {"A-SEQ", "A-VOL", "A-ONT"}


class TestPTAComparison:
    """Test PTA observable comparison."""

    @pytest.fixture
    def temp_nullbank_dir(self):
        """Create temp directory with PTA mock bank."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            bank_data = {
                "name": "mock_pta_nanograv",
                "description": "Mock PTA bank",
                "observable_type": "pta",
                "null_statistic_mean": 1.0,
                "null_statistic_std": 1.414,  # sqrt(2) for chi2(1)
                "n_trials": 1000,
                "seed": 7001,
                "alpha_thresholds": [6.64, 3.84, 2.71],  # χ²(1) quantiles
                "provenance": "test",
                "calibration_notes": "Test",
            }
            bank_path = tmpdir / "mock_pta_nanograv.json"
            with open(bank_path, "w") as f:
                json.dump(bank_data, f)

            yield tmpdir

    def test_pta_chi2_like_distribution(self, temp_nullbank_dir):
        """PTA bank should have χ²(1)-like properties."""
        manager = NullBankManager(temp_nullbank_dir)
        bank = manager.load_bank("mock_pta_nanograv")

        # χ²(1): mean ≈ 1, std ≈ 1.414
        assert 0.9 < bank.null_statistic_mean < 1.1
        assert 1.3 < bank.null_statistic_std < 1.5

    def test_pta_assumption_tags(self, temp_nullbank_dir):
        """PTA should carry [A-SEQ, A-VOL] tags."""
        manager = NullBankManager(temp_nullbank_dir)
        comparison = PTAComparison(manager)

        result = comparison.compare(1.0, alpha=0.05, synthetic=True)

        assert set(result.assumption_tags) == {"A-SEQ", "A-VOL"}


class TestLymanAlphaComparison:
    """Test Lyman-α observable comparison (null check)."""

    @pytest.fixture
    def temp_nullbank_dir(self):
        """Create temp directory with Lyman-α mock bank."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            bank_data = {
                "name": "mock_lyman_alpha_xq100",
                "description": "Mock Lyman-α bank",
                "observable_type": "lyman_alpha",
                "null_statistic_mean": 10.0,
                "null_statistic_std": 4.47,  # sqrt(20) for chi2(10)
                "n_trials": 1000,
                "seed": 7002,
                "alpha_thresholds": [23.21, 18.31, 15.99],  # χ²(10) quantiles
                "provenance": "test",
                "calibration_notes": "Test",
            }
            bank_path = tmpdir / "mock_lyman_alpha_xq100.json"
            with open(bank_path, "w") as f:
                json.dump(bank_data, f)

            yield tmpdir

    def test_lyman_alpha_chi2_like_distribution(self, temp_nullbank_dir):
        """Lyman-α bank should have χ²(10)-like properties."""
        manager = NullBankManager(temp_nullbank_dir)
        bank = manager.load_bank("mock_lyman_alpha_xq100")

        # χ²(10): mean ≈ 10, std ≈ 4.47
        assert 9.5 < bank.null_statistic_mean < 10.5
        assert 4.0 < bank.null_statistic_std < 5.0

    def test_lyman_alpha_assumption_tags(self, temp_nullbank_dir):
        """Lyman-α should carry [A-SEQ] tag (null check)."""
        manager = NullBankManager(temp_nullbank_dir)
        comparison = LymanAlphaComparison(manager)

        result = comparison.compare(10.0, alpha=0.05, synthetic=True)

        assert result.assumption_tags == ["A-SEQ"]


class TestComparisonPipeline:
    """Test orchestration of all three observables."""

    @pytest.fixture
    def temp_nullbank_dir(self):
        """Create temp directory with all three mock banks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            banks = [
                {
                    "name": "mock_lensing_sdss",
                    "observable_type": "lensing",
                    "null_statistic_mean": 0.0,
                    "null_statistic_std": 1.0,
                    "n_trials": 1000,
                    "seed": 7000,
                    "alpha_thresholds": [2.33, 1.64, 1.28],
                },
                {
                    "name": "mock_pta_nanograv",
                    "observable_type": "pta",
                    "null_statistic_mean": 1.0,
                    "null_statistic_std": 1.414,
                    "n_trials": 1000,
                    "seed": 7001,
                    "alpha_thresholds": [6.64, 3.84, 2.71],
                },
                {
                    "name": "mock_lyman_alpha_xq100",
                    "observable_type": "lyman_alpha",
                    "null_statistic_mean": 10.0,
                    "null_statistic_std": 4.47,
                    "n_trials": 1000,
                    "seed": 7002,
                    "alpha_thresholds": [23.21, 18.31, 15.99],
                },
            ]

            for bank_data in banks:
                bank_data["description"] = f"Mock {bank_data['observable_type']} bank"
                bank_data["provenance"] = "test"
                bank_data["calibration_notes"] = "Test"

                bank_path = tmpdir / f"{bank_data['name']}.json"
                with open(bank_path, "w") as f:
                    json.dump(bank_data, f)

            yield tmpdir

    def test_compare_all_observables(self, temp_nullbank_dir):
        """Run all three observable comparisons."""
        pipeline = ComparisonPipeline(temp_nullbank_dir)

        results = pipeline.compare_all(
            lensing_stat=2.5,
            pta_stat=5.0,
            lya_stat=15.0,
            alpha=0.05,
            synthetic=True,
        )

        assert len(results) == 3
        assert "lensing" in results
        assert "pta" in results
        assert "lyman_alpha" in results

    def test_all_results_synthetic_pre_g1(self, temp_nullbank_dir):
        """All results pre-G1 should be SYNTHETIC."""
        pipeline = ComparisonPipeline(temp_nullbank_dir)

        results = pipeline.compare_all(
            lensing_stat=2.5,
            pta_stat=5.0,
            lya_stat=15.0,
            alpha=0.05,
            synthetic=True,
        )

        for result in results.values():
            assert result.label == "SYNTHETIC"

    def test_partial_comparison(self, temp_nullbank_dir):
        """Compare only some observables."""
        pipeline = ComparisonPipeline(temp_nullbank_dir)

        results = pipeline.compare_all(
            lensing_stat=2.5,
            pta_stat=None,
            lya_stat=15.0,
            alpha=0.05,
            synthetic=True,
        )

        assert len(results) == 2
        assert "lensing" in results
        assert "lyman_alpha" in results
        assert "pta" not in results

    def test_save_results_to_json(self, temp_nullbank_dir):
        """Save comparison results to JSON."""
        pipeline = ComparisonPipeline(temp_nullbank_dir)

        results = pipeline.compare_all(
            lensing_stat=2.5,
            pta_stat=5.0,
            alpha=0.05,
            synthetic=True,
        )

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_path = Path(f.name)

        pipeline.save_results(results, output_path)

        # Verify JSON was created and is valid
        assert output_path.exists()

        with open(output_path) as f:
            saved = json.load(f)

        assert "lensing" in saved
        assert "pta" in saved
        assert saved["lensing"]["label"] == "SYNTHETIC"
        assert saved["lensing"]["reject_null"] is True  # 2.5 > 1.64


class TestAssupmtionTagging:
    """Verify assumption tags are correct per observable."""

    @pytest.fixture
    def temp_nullbank_dir(self):
        """Create temp directory with mock banks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            banks = [
                {
                    "name": "mock_lensing_sdss",
                    "observable_type": "lensing",
                    "alpha_thresholds": [2.33, 1.64, 1.28],
                },
                {
                    "name": "mock_pta_nanograv",
                    "observable_type": "pta",
                    "alpha_thresholds": [6.64, 3.84, 2.71],
                },
                {
                    "name": "mock_lyman_alpha_xq100",
                    "observable_type": "lyman_alpha",
                    "alpha_thresholds": [23.21, 18.31, 15.99],
                },
            ]

            for bank_data in banks:
                bank_data.update({
                    "description": f"Mock {bank_data['observable_type']} bank",
                    "null_statistic_mean": 0.0,
                    "null_statistic_std": 1.0,
                    "n_trials": 1000,
                    "seed": 7000 + len(banks),
                    "provenance": "test",
                    "calibration_notes": "Test",
                })

                bank_path = tmpdir / f"{bank_data['name']}.json"
                with open(bank_path, "w") as f:
                    json.dump(bank_data, f)

            yield tmpdir

    def test_lensing_tags(self, temp_nullbank_dir):
        """Lensing: [A-SEQ, A-VOL, A-ONT]."""
        manager = NullBankManager(temp_nullbank_dir)
        comparison = LensingComparison(manager)
        assert set(comparison.assumption_tags()) == {"A-SEQ", "A-VOL", "A-ONT"}

    def test_pta_tags(self, temp_nullbank_dir):
        """PTA: [A-SEQ, A-VOL]."""
        manager = NullBankManager(temp_nullbank_dir)
        comparison = PTAComparison(manager)
        assert set(comparison.assumption_tags()) == {"A-SEQ", "A-VOL"}

    def test_lyman_alpha_tags(self, temp_nullbank_dir):
        """Lyman-α: [A-SEQ]."""
        manager = NullBankManager(temp_nullbank_dir)
        comparison = LymanAlphaComparison(manager)
        assert comparison.assumption_tags() == ["A-SEQ"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
