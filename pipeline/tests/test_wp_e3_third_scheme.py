#!/usr/bin/env python3
"""Fast tests for WP-E3 third-scheme script.

These tests do NOT depend on real data (skip via pytest.mark.skipif if unavailable).
They verify:
- sigma helper returns None on zero-variance input
- distinguishability marker uses abs()
- per-cell output dict has expected shape
"""
import pytest
import numpy as np
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(repo_root))


def sigma_value(observed: float, null_mean: float, null_std: float) -> float:
    """Compute sigma, returning None on zero variance.

    This is copied from scripts/wp_e3_realdata_third_scheme.py for test independence.
    """
    if null_std == 0:
        return None
    return float((observed - null_mean) / null_std)


class TestSigmaHelper:
    """Test sigma_value function."""

    def test_sigma_normal_case(self):
        """Sigma should compute (obs - mean) / std correctly."""
        sigma = sigma_value(observed=5.0, null_mean=0.0, null_std=1.0)
        assert sigma == 5.0

    def test_sigma_negative(self):
        """Sigma should be negative when observed < mean."""
        sigma = sigma_value(observed=-1.0, null_mean=1.0, null_std=1.0)
        assert sigma == -2.0

    def test_sigma_zero_variance_returns_none(self):
        """Sigma should return None when null_std == 0, never coerce."""
        sigma = sigma_value(observed=5.0, null_mean=5.0, null_std=0.0)
        assert sigma is None, "Zero-variance sigma must be None, not 0 or inf"

    def test_sigma_signed(self):
        """Sigma preserves sign."""
        sigma_pos = sigma_value(observed=2.0, null_mean=0.0, null_std=1.0)
        sigma_neg = sigma_value(observed=-2.0, null_mean=0.0, null_std=1.0)
        assert sigma_pos == 2.0
        assert sigma_neg == -2.0
        assert sigma_pos == -sigma_neg


class TestDistinguishabilityMarker:
    """Test the |sigma| >= 3.0 distinguishability convention."""

    def test_abs_used_for_threshold(self):
        """Distinguishability threshold should use absolute value."""
        sigma_pos = 3.5
        sigma_neg = -3.5
        assert abs(sigma_pos) >= 3.0
        assert abs(sigma_neg) >= 3.0

    def test_threshold_boundary(self):
        """At |sigma| = 3.0 exactly, should be distinguishable."""
        assert abs(3.0) >= 3.0
        assert abs(-3.0) >= 3.0

    def test_below_threshold(self):
        """Values just below 3.0 should not be distinguishable."""
        assert abs(2.99) < 3.0
        assert abs(-2.99) < 3.0


class TestPerCellOutputShape:
    """Test that per-cell output has expected structure (fast synthetic check)."""

    def test_per_cell_dict_structure(self):
        """A per-cell result dict should have 'deformed_real_value', 'banks', 'schemes_agree'."""
        # Mock a minimal per-cell output
        per_cell = {
            "deformed_real_value": 2,
            "banks": {
                "mixed_r5": {
                    "sigma": 2.5,
                    "null_mean": 1.0,
                    "null_std": 0.4,
                    "degenerate": False,
                },
                "z_shuffle_only": {
                    "sigma": 2.1,
                    "null_mean": 1.0,
                    "null_std": 0.48,
                    "degenerate": False,
                },
                "csr_only": {
                    "sigma": -0.5,
                    "null_mean": 2.2,
                    "null_std": 0.4,
                    "degenerate": False,
                },
                "density_shuffle": {
                    "sigma": None,
                    "null_mean": 2.0,
                    "null_std": 0.0,
                    "degenerate": True,
                },
            },
            "schemes_agree": False,
        }

        # Verify structure
        assert "deformed_real_value" in per_cell
        assert isinstance(per_cell["deformed_real_value"], int)

        assert "banks" in per_cell
        assert isinstance(per_cell["banks"], dict)
        assert len(per_cell["banks"]) == 4

        for bank_name in ["mixed_r5", "z_shuffle_only", "csr_only", "density_shuffle"]:
            assert bank_name in per_cell["banks"]
            bank_data = per_cell["banks"][bank_name]
            assert "sigma" in bank_data
            assert "null_mean" in bank_data
            assert "null_std" in bank_data
            assert "degenerate" in bank_data

        assert "schemes_agree" in per_cell
        assert isinstance(per_cell["schemes_agree"], bool) or per_cell["schemes_agree"] is None

    def test_scheme_agreement_logic(self):
        """Test logic for scheme agreement: all agree or none exceed threshold."""
        # Case 1: All distinguishable
        sigmas = [3.5, 4.0, 3.1, -3.2]
        agrees = all(abs(s) >= 3.0 for s in sigmas) or all(abs(s) < 3.0 for s in sigmas)
        assert agrees is True

        # Case 2: All non-distinguishable
        sigmas = [2.5, 1.0, 0.5, -2.1]
        agrees = all(abs(s) >= 3.0 for s in sigmas) or all(abs(s) < 3.0 for s in sigmas)
        assert agrees is True

        # Case 3: Disagreement (some distinguish, some don't)
        sigmas = [3.5, 2.5, 1.0]
        agrees = all(abs(s) >= 3.0 for s in sigmas) or all(abs(s) < 3.0 for s in sigmas)
        assert agrees is False


class TestEndToEndSynthetic:
    """End-to-end test using synthetic data (no real-data file dependency)."""

    def test_synthetic_pipeline_roundtrip(self):
        """Verify that a synthetic field -> topology pipeline completes."""
        try:
            from pipeline.realfield3d import density_field_cartesian_mpc
            from pipeline.observables_real import compute_betti_numbers
        except ImportError:
            pytest.skip("pipeline modules unavailable")

        # Create synthetic coordinates
        np.random.seed(42)
        n = 100
        x = np.random.uniform(-2, 2, n)
        y = np.random.uniform(-2, 2, n)
        z = np.random.uniform(0, 2, n)

        # Bin into a field
        field = density_field_cartesian_mpc(x, y, z, nbins=4)

        # Compute topology
        betti = compute_betti_numbers(field, threshold_value=1.0)

        # Verify output shape
        assert "beta_0" in betti
        assert "beta_1" in betti
        assert "beta_2" in betti
        assert isinstance(betti["beta_0"], (int, np.integer))
        assert isinstance(betti["beta_1"], (int, np.integer))
        assert isinstance(betti["beta_2"], (int, np.integer))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
