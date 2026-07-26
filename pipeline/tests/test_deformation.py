#!/usr/bin/env python3
"""Tests for pipeline/deformation.py (WP-E2).

Comprehensive test suite for void_to_filament_deformation, ensuring:
- Identity at amplitude=0.0
- Mass preservation
- Determinism
- Monotonicity sanity (deformation actually does something)
- float64 dtype enforcement
- Quick smoke test on the full sweep
- Correct labeling in report output
"""
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(repo_root))

import numpy as np
import pytest

from pipeline.deformation import void_to_filament_deformation
from scripts.run_synthetic_detectability_sweep import (
    run_detectability_sweep,
    render_detectability_report,
)


class TestDeformationIdentity:
    """Test that amplitude=0.0 is exact identity."""

    def test_amplitude_zero_identity(self):
        """amplitude=0.0 must return field exactly."""
        field = np.array([[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]], dtype=np.float64)
        result = void_to_filament_deformation(field, R_voxels=1.0, amplitude=0.0)

        # Bit-identical check
        assert np.array_equal(result, field), "amplitude=0 should be exact identity"
        assert result.dtype == np.float64, "Output should be float64"

    def test_amplitude_zero_various_r(self):
        """amplitude=0.0 identity must hold for all R_voxels."""
        field = np.random.RandomState(42).uniform(0, 10, size=(8, 8, 8)).astype(np.float64)

        for R_voxels in [0.1, 0.5, 2.0, 5.0]:
            result = void_to_filament_deformation(field, R_voxels=R_voxels, amplitude=0.0)
            assert np.array_equal(result, field), f"Identity failed at R_voxels={R_voxels}"


class TestMassPreservation:
    """Test that total mass is preserved."""

    def test_mass_preservation_various_params(self):
        """Mass must be preserved to float64 tolerance across (R, amplitude) combos."""
        field = np.random.RandomState(123).uniform(0, 5, size=(10, 10, 10)).astype(np.float64)
        original_mass = float(np.sum(field))

        test_params = [
            (0.5, 0.1),
            (1.0, 0.3),
            (2.0, 0.5),
            (1.0, 1.0),
            (0.5, -0.5),  # Negative amplitude is also valid
        ]

        for R_voxels, amplitude in test_params:
            result = void_to_filament_deformation(field, R_voxels=R_voxels, amplitude=amplitude)
            result_mass = float(np.sum(result))

            # Check mass preservation with tight relative tolerance
            np.testing.assert_allclose(
                result_mass, original_mass, rtol=1e-10,
                err_msg=f"Mass not preserved at R={R_voxels}, amp={amplitude}"
            )

    def test_mass_preservation_zero_field(self):
        """Mass preservation on zero field should yield zero."""
        field = np.zeros((5, 5, 5), dtype=np.float64)
        result = void_to_filament_deformation(field, R_voxels=1.0, amplitude=0.5)
        assert float(np.sum(result)) == 0.0, "Zero field should stay zero"


class TestDeterminism:
    """Test that the operation is deterministic."""

    def test_determinism_same_inputs(self):
        """Same inputs must yield bit-identical outputs."""
        field = np.random.RandomState(999).uniform(0, 10, size=(12, 12, 12)).astype(np.float64)
        R_voxels = 1.5
        amplitude = 0.4

        result1 = void_to_filament_deformation(field, R_voxels=R_voxels, amplitude=amplitude)
        result2 = void_to_filament_deformation(field, R_voxels=R_voxels, amplitude=amplitude)

        assert np.array_equal(result1, result2), "Determinism violated: different results for same inputs"


class TestMonotonicitySanity:
    """Test that deformation actually modifies the field (sanity check)."""

    def test_monotonicity_larger_amplitude_larger_contrast(self):
        """Larger amplitude should yield larger max-minus-min contrast (in most cases)."""
        # Create a structured field with injected peaks and valleys
        field = np.zeros((16, 16, 16), dtype=np.float64)
        # Inject a peak at the center
        field[7:9, 7:9, 7:9] = 10.0
        # Inject a valley elsewhere
        field[2:4, 2:4, 2:4] = 0.1

        R_voxels = 1.0
        result_small_amp = void_to_filament_deformation(field, R_voxels=R_voxels, amplitude=0.1)
        result_large_amp = void_to_filament_deformation(field, R_voxels=R_voxels, amplitude=0.5)

        contrast_small = float(np.max(result_small_amp) - np.min(result_small_amp))
        contrast_large = float(np.max(result_large_amp) - np.min(result_large_amp))

        assert contrast_large > contrast_small, (
            f"Larger amplitude should yield larger contrast. "
            f"Got contrast_small={contrast_small:.4f}, contrast_large={contrast_large:.4f}"
        )


class TestFloat64Enforcement:
    """Test that float64 is enforced throughout."""

    def test_output_dtype_is_float64(self):
        """Output must always be float64, regardless of input dtype."""
        # Test with float32 input
        field32 = np.array([[[1.0, 2.0], [3.0, 4.0]]], dtype=np.float32)
        result = void_to_filament_deformation(field32, R_voxels=1.0, amplitude=0.5)
        assert result.dtype == np.float64, "Output must be float64 even if input is float32"

        # Test with int input
        field_int = np.array([[[1, 2], [3, 4]]], dtype=np.int32)
        result = void_to_filament_deformation(field_int, R_voxels=1.0, amplitude=0.5)
        assert result.dtype == np.float64, "Output must be float64 even if input is int"


class TestSweepSmoke:
    """Smoke test on a small, fast sweep configuration."""

    def test_sweep_smoke_test(self):
        """Quick smoke test of the full sweep pipeline with small parameters."""
        # Very small config to keep runtime ~10-30 seconds
        results = run_detectability_sweep(
            n_objects=800,
            n_clusters=4,
            seed=1,
            nbins=8,
            R_voxels_list=[1.0],
            amplitude_list=[0.0, 0.5],
            n_null_trials=8,
            thresholds_x_mean=(1.0,),
        )

        # Check structure
        assert "meta" in results, "Results must have 'meta' key"
        assert 1.0 in results, "Results must have R_voxels key"

        # Check meta
        meta = results["meta"]
        assert meta["nbins"] == 8
        assert meta["n_null_trials"] == 8
        assert len(meta["voxel_scale_mpc_per_axis"]) == 3
        assert len(meta["box_extent_mpc"]) == 3

        # Check nested structure for R_voxels=1.0
        r_dict = results[1.0]
        assert 0.0 in r_dict, "amplitude=0.0 must be present"
        assert 0.5 in r_dict, "amplitude=0.5 must be present"

        amp_0_dict = r_dict[0.0]
        assert 1.0 in amp_0_dict, "threshold_x_mean=1.0 must be present"

        thr_dict = amp_0_dict[1.0]
        for stat in ("beta_1", "beta_2"):
            assert stat in thr_dict, f"{stat} must be present"
            stat_dict = thr_dict[stat]
            for scheme in ("csr", "z_shuffle", "density_shuffle"):
                assert scheme in stat_dict, f"scheme {scheme} must be present"
                scheme_result = stat_dict[scheme]

                # Check required keys
                assert "deformed" in scheme_result
                assert "null_mean" in scheme_result
                assert "null_std" in scheme_result
                assert "z" in scheme_result
                assert "detected" in scheme_result

                # Check types and ranges
                assert isinstance(scheme_result["deformed"], (int, np.integer))
                assert isinstance(scheme_result["null_mean"], (float, np.floating))
                assert isinstance(scheme_result["null_std"], (float, np.floating))
                assert scheme_result["z"] is None or isinstance(scheme_result["z"], (float, np.floating))
                assert isinstance(scheme_result["detected"], (bool, np.bool_))

                # Check z-score logic: if null_std > 0, z must be finite
                if scheme_result["null_std"] > 0.0:
                    assert scheme_result["z"] is not None, "z must not be None when null_std > 0"
                    assert np.isfinite(scheme_result["z"]), "z must be finite when null_std > 0"
                    # Verify detection logic
                    expected_detected = abs(scheme_result["z"]) >= 3.0
                    assert scheme_result["detected"] == expected_detected, "detected flag must match z-score"
                else:
                    # When null_std == 0, z must be None and detected must be False
                    assert scheme_result["z"] is None, "z must be None when null_std == 0"
                    assert not scheme_result["detected"], "detected must be False when z is None"


class TestReportLabeling:
    """Test that the report contains correct labels."""

    def test_report_contains_synthetic_label(self):
        """Report must contain 'SYNTHETIC' label."""
        results = run_detectability_sweep(
            n_objects=400,
            n_clusters=3,
            seed=1,
            nbins=4,
            R_voxels_list=[1.0],
            amplitude_list=[0.0],
            n_null_trials=4,
            thresholds_x_mean=(1.0,),
        )
        report = render_detectability_report(results)
        assert "SYNTHETIC" in report, "Report must contain 'SYNTHETIC' label"

    def test_report_no_test_fit_labels(self):
        """Report must NOT contain 'TEST' or 'FIT' as label tokens."""
        results = run_detectability_sweep(
            n_objects=400,
            n_clusters=3,
            seed=1,
            nbins=4,
            R_voxels_list=[1.0],
            amplitude_list=[0.0],
            n_null_trials=4,
            thresholds_x_mean=(1.0,),
        )
        report = render_detectability_report(results)

        # Check that TEST and FIT do not appear as standalone label tokens
        # (they might appear in words like "TESTING", but not "[TEST]" or "TEST:" as labels)
        lines = report.split("\n")
        for line in lines:
            # Skip if it's a code fence or explanation context
            if "```" in line or "example" in line.lower():
                continue
            # Look for [TEST] or [FIT] patterns or label-like occurrences
            if "[TEST]" in line or "[FIT]" in line:
                raise AssertionError(f"Report contains forbidden label in line: {line}")

        assert "TEST:" not in report or "[TEST]" not in report
        assert "FIT:" not in report or "[FIT]" not in report


class TestAmplitudeZeroGuard:
    """Test the tautological-zero amplitude=0.0 guard in context."""

    def test_amplitude_zero_shows_minimal_detection(self):
        """At amplitude=0.0 (identity), detections should be ~0 (within z < 3.0 range)."""
        results = run_detectability_sweep(
            n_objects=800,
            n_clusters=4,
            seed=1,
            nbins=8,
            R_voxels_list=[1.0],
            amplitude_list=[0.0],
            n_null_trials=16,
            thresholds_x_mean=(1.0,),
        )

        r_dict = results[1.0]
        amp_0_dict = r_dict[0.0]

        detected_count = 0
        total_count = 0

        for threshold_x_mean in amp_0_dict.keys():
            thr_dict = amp_0_dict[threshold_x_mean]
            for stat in ("beta_1", "beta_2"):
                if stat in thr_dict:
                    stat_dict = thr_dict[stat]
                    for scheme_result in stat_dict.values():
                        total_count += 1
                        if scheme_result["detected"]:
                            detected_count += 1

        # At amplitude=0.0, we expect essentially no detections
        # (allow for some fluke detections due to randomness and small sample size)
        detection_rate = detected_count / total_count if total_count > 0 else 0.0
        assert detection_rate < 0.25, (
            f"At amplitude=0.0, detected {detected_count}/{total_count} "
            f"({100*detection_rate:.1f}%) — expected <25%. Guard failed."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


# Generated-by: Haiku 4.5 | Verified-by: test execution against pipeline/deformation.py
# and scripts/run_synthetic_detectability_sweep.py | Reviewed-by: pending T0
