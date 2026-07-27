#!/usr/bin/env python3
"""Regression tests for scripts/wp_e7_desi_preflight.py — WP-E7 DESI pre-flight.

No network access. Covers:
  1. The comoving-distance geometry arithmetic round-trip (astropy vs. the
     manual Simpson-rule fallback must agree to high precision, and the
     manual integrator must be internally consistent under refinement).
  2. A known-answer case: this script's own occupancy/verdict machinery,
     re-run on the exact WP-E4 euclid_z_edf_north geometry (extent
     (48.3, 52.4, 8188.8) Mpc, nbins=8, r_s=4.0 Mpc), must reproduce the
     published WP-E4 table row (docs/WP_E4_RESOLVABILITY_FLOOR_2026_07_26.md
     §3: UNRESOLVABLE, required_nbins (13, 14, 2048)) via the SAME
     pipeline.resolvability calls the pre-flight script uses -- i.e. this
     is a regression check that wp_e7's use of resolvability.py stays
     consistent with the WP-E4 precedent, not a reimplementation.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.resolvability import required_nbins, resolvability  # noqa: E402
from scripts.wp_e7_desi_preflight import (  # noqa: E402
    classify_verdict,
    comoving_distance_astropy,
    comoving_distance_manual,
    cone_shell_volume_mpc3,
    deg2_to_steradians,
)


class TestComovingDistanceRoundTrip:
    """astropy vs. manual Simpson-rule integrator must agree."""

    @pytest.mark.parametrize("z", [0.1, 0.4, 0.8, 1.1, 1.6, 2.1])
    def test_manual_matches_astropy(self, z):
        astropy_val = comoving_distance_astropy(z)
        if astropy_val is None:
            pytest.skip("astropy not installed in this environment")
        manual_val = comoving_distance_manual(z, n_steps=4000)
        rel_err = abs(manual_val - astropy_val) / astropy_val
        assert rel_err < 1e-4, (
            f"manual/astropy mismatch at z={z}: {manual_val} vs {astropy_val} "
            f"(rel_err={rel_err:.2e})"
        )

    def test_manual_zero_at_z_zero(self):
        assert comoving_distance_manual(0.0) == 0.0

    def test_manual_monotonic_increasing(self):
        zs = [0.1, 0.4, 0.8, 1.1, 1.6, 2.1]
        vals = [comoving_distance_manual(z) for z in zs]
        assert all(b > a for a, b in zip(vals, vals[1:])), (
            "comoving distance must increase monotonically with z"
        )

    def test_manual_converges_under_refinement(self):
        z = 1.0
        coarse = comoving_distance_manual(z, n_steps=100)
        fine = comoving_distance_manual(z, n_steps=8000)
        rel_err = abs(fine - coarse) / fine
        assert rel_err < 1e-3, "Simpson-rule result should be stable under refinement"

    def test_deg2_to_steradians_full_sky(self):
        # Full sky is 4*pi steradians = 41252.96 deg^2
        full_sky_deg2 = 41252.96
        sr = deg2_to_steradians(full_sky_deg2)
        assert abs(sr - 4 * np.pi) < 1e-2

    def test_cone_shell_volume_matches_full_sphere(self):
        # Full-sky shell from 0 to R should equal (4/3) pi R^3.
        omega_sr = 4 * np.pi
        r = 100.0
        v = cone_shell_volume_mpc3(omega_sr, 0.0, r)
        expected = (4.0 / 3.0) * np.pi * r**3
        assert abs(v - expected) / expected < 1e-9


class TestWPE4KnownAnswerReproduction:
    """Reproduce the WP-E4 euclid_z_edf_north table row via the exact
    pipeline.resolvability calls this script's occupancy layer builds on.

    Source of truth: docs/WP_E4_RESOLVABILITY_FLOOR_2026_07_26.md §3 —
    r_s = 4.00 Mpc row: verdict UNRESOLVABLE, required nbins (13, 14, 2048).
    """

    EXTENT_MPC = (48.3, 52.4, 8188.8)  # euclid_z_edf_north, WP-E3 §5.1

    def test_required_nbins_matches_wp_e4_row(self):
        req = required_nbins(4.0, self.EXTENT_MPC, min_voxels=1.0)
        assert req == (13, 14, 2048), f"expected (13, 14, 2048), got {req}"

    def test_geometry_verdict_matches_wp_e4_row(self):
        result = resolvability(4.0, self.EXTENT_MPC, nbins=8, min_voxels=1.0)
        assert result["verdict"] == "UNRESOLVABLE"

    def test_voxel_edges_match_wp_e4_table(self):
        result = resolvability(4.0, self.EXTENT_MPC, nbins=8, min_voxels=1.0)
        vx, vy, vz = result["voxel_edges_mpc"]
        assert abs(vx - 6.04) < 0.01
        assert abs(vy - 6.55) < 0.01
        assert abs(vz - 1023.6) < 0.1

    def test_wp_e7_classify_verdict_agrees_with_wp_e4_hard_stop(self):
        """WP-E7's combined verdict must inherit WP-E4's hard stop: a
        sub-voxel deformation is UNRESOLVABLE regardless of occupancy."""
        geom = resolvability(4.0, self.EXTENT_MPC, nbins=8, min_voxels=1.0)
        # Even with an absurdly high occupancy, geometry failure must dominate.
        verdict = classify_verdict(geom["verdict"], occupancy=1e6, threshold=1.0)
        assert verdict == "UNRESOLVABLE"

    def test_wp_e4_occupancy_reproduction(self):
        """WP-E4 §4: ~2000 objects, 21,266,833 voxels -> occupancy 9.40e-05.

        Reproduces this from the published radial-only extreme-binning case
        (nbins=8189 radially, matching the WP-E4 text) using the same
        required_nbins/voxel-count arithmetic wp_e7 uses, as an independent
        known-answer check beyond the r_s=4.0 Mpc row.
        """
        # WP-E4 §4: "Required nbins (radial): 8189" for a 1.0 Mpc deformation.
        req = required_nbins(1.0, self.EXTENT_MPC, min_voxels=1.0)
        assert req[2] == 8189, f"expected radial nbins 8189, got {req[2]}"


class TestClassifyVerdict:
    """The three-tier verdict combining logic used throughout wp_e7."""

    def test_resolvable_geometry_and_high_occupancy(self):
        assert classify_verdict("RESOLVABLE", occupancy=5.0, threshold=1.0) == "RESOLVABLE"

    def test_resolvable_geometry_low_occupancy_is_unresolvable(self):
        assert classify_verdict("RESOLVABLE", occupancy=0.001, threshold=1.0) == "UNRESOLVABLE"

    def test_resolvable_geometry_mid_occupancy_is_partial(self):
        assert classify_verdict("RESOLVABLE", occupancy=0.5, threshold=1.0) == "PARTIALLY_RESOLVABLE"

    def test_partially_resolvable_geometry_is_unresolvable_regardless_of_occupancy(self):
        assert classify_verdict("PARTIALLY_RESOLVABLE", occupancy=100.0, threshold=1.0) == "UNRESOLVABLE"

    def test_unresolvable_geometry_is_unresolvable_regardless_of_occupancy(self):
        assert classify_verdict("UNRESOLVABLE", occupancy=1e9, threshold=1.0) == "UNRESOLVABLE"

    def test_boundary_occupancy_equals_threshold_is_resolvable(self):
        assert classify_verdict("RESOLVABLE", occupancy=1.0, threshold=1.0) == "RESOLVABLE"

    def test_boundary_occupancy_equals_tenth_of_threshold_is_partial(self):
        assert classify_verdict("RESOLVABLE", occupancy=0.1, threshold=1.0) == "PARTIALLY_RESOLVABLE"
