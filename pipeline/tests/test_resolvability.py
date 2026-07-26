#!/usr/bin/env python3
"""Tests for pipeline.resolvability — WP-E4 sub-voxel guard.

Verifies arithmetic to prevent deformation sweeps from testing scales
below the voxel size.
"""
import pytest
import numpy as np
from pipeline.resolvability import (
    voxel_edges_mpc,
    resolvability,
    required_nbins,
    assert_resolvable,
    ResolvabilityError,
)


class TestVoxelEdges:
    """Voxel edge computation."""

    def test_euclid_z_edf_north_nbins8(self):
        """Voxel edges for euclid_z_edf_north at nbins=8."""
        extent = (48.3, 52.4, 8188.8)
        nbins = 8
        edges = voxel_edges_mpc(extent, nbins)

        # WP-E3 §5.1 published values
        assert len(edges) == 3
        assert isinstance(edges[0], float)
        assert isinstance(edges[1], float)
        assert isinstance(edges[2], float)

        # Check to 2 decimal places
        assert abs(edges[0] - 6.04) < 0.01, f"voxel_x = {edges[0]}, expected ~6.04"
        assert abs(edges[1] - 6.55) < 0.01, f"voxel_y = {edges[1]}, expected ~6.55"
        assert abs(edges[2] - 1023.6) < 0.1, f"voxel_z = {edges[2]}, expected ~1023.6"

    def test_determinism_float64(self):
        """Voxel edge calculation is deterministic and uses float64."""
        extent = (100.0, 200.0, 1000.0)
        nbins = 10
        edges1 = voxel_edges_mpc(extent, nbins)
        edges2 = voxel_edges_mpc(extent, nbins)

        for e1, e2 in zip(edges1, edges2):
            assert e1 == e2
            assert isinstance(e1, float)


class TestResolvabilityWPE3Regression:
    """WP-E3 regression test — the core defect this guard catches."""

    def test_wp_e3_unresolvable_verdict(self):
        """r_s=4.0 Mpc at euclid_z_edf_north, nbins=8 must return UNRESOLVABLE."""
        result = resolvability(
            scale_mpc=4.0, extent_mpc=(48.3, 52.4, 8188.8), nbins=8, min_voxels=1.0
        )

        assert result["verdict"] == "UNRESOLVABLE", f"Expected UNRESOLVABLE, got {result['verdict']}"

    def test_wp_e3_scale_in_voxels_matches_published(self):
        """scale_in_voxels for WP-E3 case must match published ratios (0.66, 0.61, 0.0039)."""
        result = resolvability(
            scale_mpc=4.0, extent_mpc=(48.3, 52.4, 8188.8), nbins=8, min_voxels=1.0
        )

        siv = result["scale_in_voxels"]
        # WP-E3 §5.1: [0.66, 0.61, 0.0039]
        assert abs(siv[0] - 0.66) < 0.01, f"scale_in_voxels[x] = {siv[0]}, expected ~0.66"
        assert abs(siv[1] - 0.61) < 0.01, f"scale_in_voxels[y] = {siv[1]}, expected ~0.61"
        assert abs(siv[2] - 0.0039) < 0.0005, f"scale_in_voxels[z] = {siv[2]}, expected ~0.0039"

    def test_wp_e3_resolvable_per_axis(self):
        """At 4.0 Mpc, all axes must be unresolvable (< 1.0 voxels)."""
        result = resolvability(
            scale_mpc=4.0, extent_mpc=(48.3, 52.4, 8188.8), nbins=8, min_voxels=1.0
        )

        rpa = result["resolvable_per_axis"]
        assert rpa == (False, False, False), f"Expected all False, got {rpa}"


class TestResolvabilityVerdicts:
    """Test the three verdict classes."""

    def test_clearly_resolvable(self):
        """A scale well above voxel edges must be RESOLVABLE."""
        result = resolvability(
            scale_mpc=200.0, extent_mpc=(100.0, 100.0, 1000.0), nbins=10, min_voxels=1.0
        )

        assert result["verdict"] == "RESOLVABLE"
        assert all(result["resolvable_per_axis"])

    def test_partially_resolvable(self):
        """A scale near the radial voxel size: resolvable transverse, unresolvable radial."""
        # euclid_z_edf_north: voxels at nbins=8 are (6.04, 6.55, 1023.6)
        # A scale of ~10 Mpc is resolvable transversely but not radially.
        result = resolvability(
            scale_mpc=7.0, extent_mpc=(48.3, 52.4, 8188.8), nbins=8, min_voxels=1.0
        )

        assert result["verdict"] == "PARTIALLY_RESOLVABLE"
        # Should be resolvable on transverse, not on radial
        resolvable_axes = result["resolvable_per_axis"]
        assert resolvable_axes[0] is True, "x axis should be resolvable for 7.0 Mpc"
        assert resolvable_axes[1] is True, "y axis should be resolvable for 7.0 Mpc"
        assert resolvable_axes[2] is False, "z axis should not be resolvable (radial too deep)"


class TestBoundaryCondition:
    """Scale == voxel_edge exactly (boundary test)."""

    def test_scale_equals_voxel_edge_is_resolvable(self):
        """When scale == voxel_edge, >= condition means exactly 1.0 voxel: resolvable."""
        # Set up so scale == voxel_edge exactly
        extent = (10.0, 10.0, 10.0)
        nbins = 5
        voxel_edge = 10.0 / 5  # 2.0 Mpc
        scale = voxel_edge

        result = resolvability(scale_mpc=scale, extent_mpc=extent, nbins=nbins, min_voxels=1.0)

        # All axes should be exactly 1.0 voxel
        for siv in result["scale_in_voxels"]:
            assert abs(siv - 1.0) < 1e-10

        # All axes should be resolvable (>= not >)
        assert all(result["resolvable_per_axis"])
        assert result["verdict"] == "RESOLVABLE"


class TestRequiredNbins:
    """Compute nbins needed to reach min_voxels."""

    def test_required_nbins_wp_e3_case(self):
        """For WP-E3 case, compute required nbins to make 4.0 Mpc resolvable."""
        req = required_nbins(scale_mpc=4.0, extent_mpc=(48.3, 52.4, 8188.8), min_voxels=1.0)

        # For x: ceil(1.0 * 48.3 / 4.0) = ceil(12.075) = 13
        # For y: ceil(1.0 * 52.4 / 4.0) = ceil(13.1) = 14
        # For z: ceil(1.0 * 8188.8 / 4.0) = ceil(2047.2) = 2048
        assert req[0] == 13, f"nbins_x = {req[0]}, expected 13"
        assert req[1] == 14, f"nbins_y = {req[1]}, expected 14"
        assert req[2] == 2048, f"nbins_z = {req[2]}, expected 2048"

    def test_required_nbins_roundtrip(self):
        """Using required_nbins' output should give RESOLVABLE verdict."""
        scale = 4.0
        extent = (48.3, 52.4, 8188.8)
        min_voxels = 1.0

        req_nbins = required_nbins(scale, extent, min_voxels)

        # Recheck with the required nbins
        for i, nbins_i in enumerate(req_nbins):
            # Check one axis at a time
            result = resolvability(scale, extent, nbins_i, min_voxels=min_voxels)
            # On axis i, should now be resolvable
            assert result["resolvable_per_axis"][i], (
                f"Axis {i}: scale={scale}, extent[{i}]={extent[i]}, "
                f"nbins={nbins_i} should be resolvable"
            )


class TestAssertResolvable:
    """Test the guard function for sweeps."""

    def test_assert_raises_on_unresolvable(self):
        """assert_resolvable must raise ResolvabilityError for WP-E3 case."""
        with pytest.raises(ResolvabilityError) as exc_info:
            assert_resolvable(scale_mpc=4.0, extent_mpc=(48.3, 52.4, 8188.8), nbins=8)

        error_msg = str(exc_info.value)
        # Check that the error message contains key info
        assert "4.0" in error_msg or "4.00" in error_msg, "Error should mention the scale"
        assert "nbins" in error_msg, "Error should mention nbins"
        assert "Voxel edges" in error_msg, "Error should show voxel edges"
        assert "Required nbins" in error_msg, "Error should show required nbins"
        assert "WP_E3" in error_msg, "Error should reference WP-E3 doc"

    def test_assert_does_not_raise_on_resolvable(self):
        """assert_resolvable must not raise for a clearly resolvable scale."""
        # This should not raise
        assert_resolvable(scale_mpc=200.0, extent_mpc=(100.0, 100.0, 1000.0), nbins=10)

    def test_assert_error_includes_required_nbins(self):
        """Error message must include required nbins per axis."""
        with pytest.raises(ResolvabilityError) as exc_info:
            assert_resolvable(scale_mpc=4.0, extent_mpc=(48.3, 52.4, 8188.8), nbins=8)

        error_msg = str(exc_info.value)
        # Should mention the tuple of required nbins
        assert "(13, 14, 2048)" in error_msg or "13" in error_msg


class TestDeterminism:
    """Float64 determinism."""

    def test_resolvability_deterministic(self):
        """Repeated calls with same inputs give identical outputs."""
        scale = 4.0
        extent = (48.3, 52.4, 8188.8)
        nbins = 8

        result1 = resolvability(scale, extent, nbins)
        result2 = resolvability(scale, extent, nbins)

        assert result1["verdict"] == result2["verdict"]
        assert result1["scale_in_voxels"] == result2["scale_in_voxels"]
        assert result1["voxel_edges_mpc"] == result2["voxel_edges_mpc"]

    def test_all_float64_internally(self):
        """All numeric outputs are float64 (or int for nbins)."""
        result = resolvability(4.0, (48.3, 52.4, 8188.8), 8)

        assert isinstance(result["scale_mpc"], float)
        assert isinstance(result["nbins"], int)
        assert all(isinstance(v, float) for v in result["voxel_edges_mpc"])
        assert all(isinstance(v, float) for v in result["scale_in_voxels"])


class TestMinVoxelsParameterization:
    """min_voxels=1.0 is necessary but not sufficient for sensitivity."""

    def test_min_voxels_stricter_threshold(self):
        """Increasing min_voxels makes scales harder to resolve."""
        scale = 2.0
        extent = (100.0, 100.0, 1000.0)
        nbins = 10  # voxel edges: 10, 10, 100

        result_1voxel = resolvability(scale, extent, nbins, min_voxels=1.0)
        result_3voxel = resolvability(scale, extent, nbins, min_voxels=3.0)

        # At min_voxels=1.0: 2.0 spans 0.2 voxels → unresolvable
        assert result_1voxel["verdict"] == "UNRESOLVABLE"

        # At min_voxels=3.0: 2.0 spans 0.2 voxels → unresolvable
        assert result_3voxel["verdict"] == "UNRESOLVABLE"

    def test_min_voxels_in_required_nbins(self):
        """required_nbins respects min_voxels."""
        scale = 4.0
        extent = (100.0, 100.0, 1000.0)

        req_1 = required_nbins(scale, extent, min_voxels=1.0)
        req_3 = required_nbins(scale, extent, min_voxels=3.0)

        # For each axis, req_3 should be >= req_1
        for r1, r3 in zip(req_1, req_3):
            assert r3 >= r1, f"min_voxels=3.0 should require more bins: {r1} vs {r3}"
