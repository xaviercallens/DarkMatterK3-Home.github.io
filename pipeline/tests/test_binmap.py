#!/usr/bin/env python3
"""
Unit tests for WP-E6-BINMAP (pipeline/binmap.py).

Merge-blocking test suite. Tests verify:
  1. Band membership (9 bins, 0.1 dex bands, all nonempty)
  2. Nyquist constraint (every bin member k ≤ 0.0527412 s/km)
  3. Z-grid constraint (z=4.2 only; z=4.6, 5.0 unavailable)
  4. Covariance function blocking (intentionally raises NotImplementedError)
  5. Independent re-verification of membership (log₁₀k arithmetic)
"""

import os
import sys
import json
import pytest
import numpy as np
import pandas as pd

# Import the binmap module
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(repo_root, 'pipeline'))
import binmap


# Test data path
DESI_CSV_PATH = os.path.join(repo_root, 'data', 'literature', 'desi_dr1_lya_p1d_2026_07_27.csv')


class TestDESIDataAvailable:
    """Verify that the test data file exists."""

    def test_desi_csv_exists(self):
        """DESI P1D CSV must exist at expected path."""
        assert os.path.isfile(DESI_CSV_PATH), \
            f"DESI CSV not found at {DESI_CSV_PATH}"

    def test_desi_csv_structure(self):
        """DESI CSV must have correct columns and dimensions."""
        df = pd.read_csv(DESI_CSV_PATH)
        assert len(df) == 1020, f"Expected 1020 rows, got {len(df)}"
        expected_cols = ['z', 'k_s_per_km', 'p1d_kms', 'e_stat_kms', 'e_syst_kms', 'e_total_kms', 'pfid_kms']
        for col in expected_cols:
            assert col in df.columns, f"Missing column: {col}"

    def test_desi_csv_z_grid(self):
        """DESI CSV must have 12 z-bins from 2.2 to 4.4."""
        df = pd.read_csv(DESI_CSV_PATH)
        z_unique = sorted(df['z'].unique())
        expected_z = [2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4]
        np.testing.assert_allclose(z_unique, expected_z, rtol=1e-10)

    def test_desi_csv_k_grid(self):
        """DESI CSV must have 85 unique k-bins."""
        df = pd.read_csv(DESI_CSV_PATH)
        k_unique = df['k_s_per_km'].unique()
        assert len(k_unique) == 85, f"Expected 85 k-bins, got {len(k_unique)}"
        k_max = k_unique.max()
        assert k_max <= 0.0527412, f"Max k = {k_max} exceeds Nyquist 0.0527412"


class TestRestrictionMapBasics:
    """Test restriction_map() function basic behavior."""

    def test_restriction_map_default_z(self):
        """Should use z=4.2 by default (only overlap between emulator and DESI)."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        assert map_out['z_selected'] == 4.2

    def test_restriction_map_wrong_z_raises(self):
        """Should raise ValueError for z not in DESI CSV."""
        with pytest.raises(ValueError, match="not found in DESI CSV"):
            binmap.restriction_map(DESI_CSV_PATH, z_target=5.0)

        with pytest.raises(ValueError, match="not found in DESI CSV"):
            binmap.restriction_map(DESI_CSV_PATH, z_target=4.6)

    def test_restriction_map_z_4_2_available(self):
        """z=4.2 should be the only emulator z-value in DESI CSV."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        assert len(map_out['bands']) == 9
        assert map_out['z_selected'] == 4.2

    def test_restriction_map_9_bins(self):
        """Should return exactly 9 bins."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        assert len(map_out['bands']) == 9
        for i, band in enumerate(map_out['bands']):
            assert band['bin_index'] == i

    def test_restriction_map_default_k_targets(self):
        """Should use the 9 natively-resolved emulator K_BINS by default."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, emulator_k_targets=None, z_target=4.2)
        emulator_k = map_out['metadata']['emulator_k_bins']
        emulator_log10k = map_out['metadata']['emulator_log10k_bins']
        expected_log10k = [-2.2, -2.1, -2.0, -1.9, -1.8, -1.7, -1.6, -1.5, -1.4]
        np.testing.assert_allclose(emulator_log10k, expected_log10k, rtol=1e-10)

    def test_metadata_present(self):
        """Should include metadata dict with provenance."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        meta = map_out['metadata']
        assert 'source_csv' in meta
        assert 'emulator_k_bins' in meta
        assert 'k_nyquist_s_per_km' in meta
        assert meta['k_nyquist_s_per_km'] == 0.0527412


class TestBandMembership:
    """Test band membership correctness."""

    def test_all_bands_nonempty(self):
        """All 9 bands must be nonempty (at z=4.2)."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        for band in map_out['bands']:
            assert band['member_count'] > 0, \
                f"Bin {band['bin_index']} is empty (no DESI rows in 0.1 dex band)"

    def test_band_min_max_consistent(self):
        """For each band, band_min_k < k_target < band_max_k."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        for band in map_out['bands']:
            k_target = band['k_target']
            k_min = band['band_min_k']
            k_max = band['band_max_k']
            assert k_min < k_target < k_max, \
                f"Bin {band['bin_index']}: band boundaries inconsistent with target"

    def test_band_members_in_range(self):
        """All members of each band must satisfy k_min ≤ k ≤ k_max (log-space)."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        for band in map_out['bands']:
            band_min_log = band['band_min_log10k']
            band_max_log = band['band_max_log10k']
            member_log10k = np.array(band['member_log10k_values'])
            assert np.all(member_log10k >= band_min_log - 1e-10), \
                f"Bin {band['bin_index']}: some members below band_min"
            assert np.all(member_log10k <= band_max_log + 1e-10), \
                f"Bin {band['bin_index']}: some members above band_max"

    def test_nearest_neighbor_in_band(self):
        """Nearest neighbor should be within the band (or closest outside)."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        df = pd.read_csv(DESI_CSV_PATH)
        df_z = df[df['z'] == 4.2]
        for band in map_out['bands']:
            nn_idx = band['nearest_neighbor_csv_idx']
            k_nn = df.loc[nn_idx, 'k_s_per_km']
            k_target = band['k_target']
            # NN should be close to target (within a DESI k-bin spacing)
            assert abs(k_nn - k_target) < 0.01, \
                f"Bin {band['bin_index']}: NN too far from target"


class TestNyquistConstraint:
    """Test Nyquist limit constraint (k ≤ 0.0527412 s/km)."""

    def test_all_members_within_nyquist(self):
        """All members of all 9 bins must satisfy k ≤ 0.0527412 s/km."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        k_nyquist = 0.0527412
        for band in map_out['bands']:
            member_k = np.array(band['member_k_values'])
            assert np.all(member_k <= k_nyquist + 1e-10), \
                f"Bin {band['bin_index']}: some members exceed Nyquist ({k_nyquist})"
            assert band['all_within_nyquist'], \
                f"Bin {band['bin_index']}: flag all_within_nyquist should be True"

    def test_emulator_k_targets_within_nyquist(self):
        """All 9 emulator K_BINS targets must be ≤ Nyquist."""
        emulator_log10k = [-2.2, -2.1, -2.0, -1.9, -1.8, -1.7, -1.6, -1.5, -1.4]
        emulator_k = 10.0 ** np.array(emulator_log10k)
        k_nyquist = 0.0527412
        assert np.all(emulator_k <= k_nyquist), \
            "Some emulator K_BINS exceed Nyquist limit"


class TestIndependentVerification:
    """Test verify_bins() independent verification (re-derives membership)."""

    def test_verify_bins_passes(self):
        """verify_bins() should pass all checks."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        vresult = binmap.verify_bins(map_out)
        assert vresult['passes'], \
            f"verify_bins() failed: {vresult}"

    def test_verify_bins_nonempty(self):
        """verify_bins() should confirm all bins nonempty."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        vresult = binmap.verify_bins(map_out)
        assert vresult['all_bins_nonempty'], \
            "verify_bins() found empty bins"

    def test_verify_bins_nyquist(self):
        """verify_bins() should confirm Nyquist constraint."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        vresult = binmap.verify_bins(map_out)
        assert vresult['all_within_nyquist'], \
            "verify_bins() found Nyquist violations"

    def test_verify_bins_independent_membership(self):
        """verify_bins() should recompute membership independently and match."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        vresult = binmap.verify_bins(map_out)
        assert vresult['membership_matches_stored'], \
            "verify_bins() independent re-verification disagrees with stored membership"


class TestCovarianceBlocking:
    """Test that covariance_block() is intentionally blocked."""

    def test_covariance_raises_not_implemented(self):
        """covariance_block() should always raise NotImplementedError."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        with pytest.raises(NotImplementedError, match="blocked"):
            binmap.covariance_block(map_out)

    def test_covariance_error_mentions_zenodo(self):
        """NotImplementedError should mention Zenodo DOI."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        try:
            binmap.covariance_block(map_out)
        except NotImplementedError as e:
            assert '10.5281/zenodo.16943723' in str(e)
            assert 'COVARIANCE' in str(e)


class TestEscalationFlags:
    """Test escalation flags and documentation."""

    def test_z_overlap_escalation_present(self):
        """Should document z-grid mismatch escalation."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        assert 'z_overlap_status' in map_out
        assert 'Z-grid mismatch' in map_out['z_overlap_status']
        assert 'z=4.2' in map_out['z_overlap_status']

    def test_metadata_bin_def_documented(self):
        """Should document 0.1 dex band definition."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        meta = map_out['metadata']
        assert 'bin_membership_def' in meta
        assert '0.1 dex' in meta['bin_membership_def']


class TestOutputFormat:
    """Test output format and JSON serialization."""

    def test_output_structure(self):
        """Should have expected top-level keys."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        assert 'bands' in map_out
        assert 'z_selected' in map_out
        assert 'z_overlap_status' in map_out
        assert 'metadata' in map_out

    def test_band_structure(self):
        """Each band should have expected keys."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        expected_keys = [
            'bin_index', 'log10k_target', 'k_target',
            'band_min_log10k', 'band_max_log10k',
            'band_min_k', 'band_max_k',
            'members', 'member_k_values', 'member_log10k_values',
            'nearest_neighbor_csv_idx', 'all_within_nyquist',
            'member_count', 'k_nyquist_limit',
        ]
        for band in map_out['bands']:
            for key in expected_keys:
                assert key in band, f"Band missing key: {key}"

    def test_json_serializable(self):
        """Output should be JSON-serializable."""
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        try:
            json_str = json.dumps(map_out)
            json.loads(json_str)
        except (TypeError, ValueError) as e:
            pytest.fail(f"Output not JSON-serializable: {e}")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
