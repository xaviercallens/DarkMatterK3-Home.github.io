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
    """covariance_block() without an explicit path stays blocked: real-data
    contact must be a deliberate act (WP-E6-BINMAP-C keeps this invariant)."""

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


# --------------------------------------------------------------------------
# WP-E6-BINMAP-C (2026-07-31, T1 ruling R2 executing T0 D1): real covariance
# extraction tests. The raw FITS lives in data/raw/ (gitignored), so the
# FITS-dependent tests skip on a clean checkout; the derived-artifact tests
# below run everywhere (npy/json + CSV are all tracked).
# --------------------------------------------------------------------------

COVARIANCE_FITS_PATH = os.path.join(
    repo_root, 'data', 'raw', 'desi_dr1_lya_p1d_zenodo',
    'desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits')

needs_fits = pytest.mark.skipif(
    not os.path.isfile(COVARIANCE_FITS_PATH),
    reason="raw Zenodo FITS not fetched (run scripts/fetch_data.py)")


class TestCovarianceHashGate:
    """The SHA-256 hard gate must refuse to read any non-pinned file."""

    def test_wrong_hash_hard_stops(self, tmp_path):
        """A file with a non-pinned SHA-256 raises RuntimeError, unread."""
        fake = tmp_path / 'tampered.fits'
        fake.write_bytes(b'not the pinned DESI FITS')
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        with pytest.raises(RuntimeError, match='HARD-GATE FAILURE'):
            binmap.covariance_block(map_out, covariance_fits_path=str(fake))

    def test_pin_matches_manifest_value(self):
        """The module pin must be the data/MANIFEST.md value, verbatim."""
        assert binmap.COVARIANCE_FITS_SHA256_PIN == (
            'bbb98dc3d1865a50bb878e949a644604ce729da419db8e7db5adbb532a894857')


@pytest.fixture(scope='module')
def result():
    """Shared real-extraction result (module-scoped: one FITS read)."""
    map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
    return binmap.covariance_block(
        map_out, covariance_fits_path=COVARIANCE_FITS_PATH)


@needs_fits
class TestCovarianceBlockReal:
    """Real member-level sub-block extraction from the hash-gated FITS."""

    def test_shape_66x66(self, result):
        assert result['cov_member'].shape == (66, 66)
        assert len(result['member_csv_indices']) == 66

    def test_grouping_member_counts(self, result):
        counts = [len(g['member_csv_indices']) for g in result['grouping']]
        assert counts == [3, 4, 4, 6, 8, 9, 11, 11, 10]
        # positions partition 0..65 in order
        flat = [p for g in result['grouping'] for p in g['member_positions']]
        assert flat == list(range(66))

    def test_mandatory_checks_all_pass(self, result):
        checks = result['checks']
        assert checks['diag_matches_csv_e_total_sq_rtol1e6']
        assert checks['symmetric']
        assert checks['positive_definite_cholesky']
        assert checks['max_rel_diag_discrepancy'] <= 1e-6

    def test_diag_matches_csv_independently(self, result):
        """Independent re-derivation of check 1, not reusing the module's."""
        df = pd.read_csv(DESI_CSV_PATH)
        e_sq = df.loc[result['member_csv_indices'], 'e_total_kms'].values ** 2
        np.testing.assert_allclose(np.diag(result['cov_member']), e_sq, rtol=1e-6)

    def test_symmetry_and_cholesky_independently(self, result):
        sub = result['cov_member']
        assert np.allclose(sub, sub.T)
        np.linalg.cholesky(sub)  # raises LinAlgError if not positive-definite

    def test_aggregated_block_is_pinned_option1(self, result):
        """Since the 2026-09-16 pin the 9x9 IS produced, by the pinned rule
        only (it was correctly None before that pin)."""
        assert result['aggregated_9x9'].shape == (9, 9)
        assert 'WP_E6_SWEEP_DESIGN_PINNED_2026_09_16' in result['aggregation_note']
        assert result['aggregation']['checks']['positive_definite_cholesky']

    def test_provenance_sha_is_pin(self, result):
        assert result['provenance']['fits_sha256'] == \
            binmap.COVARIANCE_FITS_SHA256_PIN
        assert result['provenance']['hdu'] == 'COVARIANCE'
        assert result['provenance']['z_selected'] == 4.2


class TestDerivedCovarianceArtifacts:
    """The committed data/derived/ artifacts must stay self-consistent with
    the committed CSV (runs on a clean checkout, no raw FITS needed)."""

    NPY = os.path.join(repo_root, 'data', 'derived',
                       'wp_e6_binmap_c_cov_member66_z4p2_2026_07_31.npy')
    JSON = os.path.join(repo_root, 'data', 'derived',
                        'wp_e6_binmap_c_cov_z4p2_2026_07_31.json')

    def test_artifacts_exist(self):
        assert os.path.isfile(self.NPY)
        assert os.path.isfile(self.JSON)

    def test_npy_consistent_with_csv_and_map(self):
        sub = np.load(self.NPY)
        assert sub.shape == (66, 66)
        with open(self.JSON) as f:
            meta = json.load(f)
        # member indices in the JSON must equal a fresh restriction_map's
        map_out = binmap.restriction_map(DESI_CSV_PATH, z_target=4.2)
        fresh = [i for b in map_out['bands'] for i in b['members']]
        assert meta['member_csv_indices'] == fresh
        # diagonal must equal the CSV's e_total_kms**2 (rtol 1e-6)
        df = pd.read_csv(DESI_CSV_PATH)
        e_sq = df.loc[fresh, 'e_total_kms'].values ** 2
        np.testing.assert_allclose(np.diag(sub), e_sq, rtol=1e-6)
        # symmetric + positive-definite
        assert np.allclose(sub, sub.T)
        np.linalg.cholesky(sub)

    def test_json_label_and_checks(self):
        with open(self.JSON) as f:
            meta = json.load(f)
        assert meta['label'].startswith('DRAFT')
        assert all([
            meta['checks']['diag_matches_csv_e_total_sq_rtol1e6'],
            meta['checks']['symmetric'],
            meta['checks']['positive_definite_cholesky'],
        ])
        assert meta['aggregated_9x9'] is None
        assert meta['provenance']['fits_sha256'] == \
            binmap.COVARIANCE_FITS_SHA256_PIN


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


# --------------------------------------------------------------------------
# WP-E6-SWEEP aggregation step (pinned 2026-09-16, T0 ruling A1 Option 1):
# briefs/WP_E6_SWEEP_DESIGN_PINNED_2026_09_16.md Sec.1.2. Synthetic-matrix
# tests run everywhere; the tracked 66x66 artifact test runs on a clean
# checkout; the FITS-dependent test skips without the raw file.
# --------------------------------------------------------------------------

def _independent_option1(cov, groups):
    """Plain-loop re-derivation of Sec.1.2, sharing no code with binmap."""
    nb = len(groups)
    C9 = [[0.0] * nb for _ in range(nb)]
    W = [[0.0] * cov.shape[0] for _ in range(nb)]
    for b, ps in enumerate(groups):
        norm = sum(1.0 / cov[j, j] for j in ps)
        for i in ps:
            W[b][i] = (1.0 / cov[i, i]) / norm
    for a in range(nb):
        for b in range(nb):
            acc = 0.0
            for i in groups[a]:
                for j in groups[b]:
                    acc += W[a][i] * cov[i, j] * W[b][j]
            C9[a][b] = acc
    return np.array(W), np.array(C9)


def _synthetic_cov(n, rng, corr=0.3):
    sig = rng.uniform(1.0, 5.0, n)
    R = np.full((n, n), corr) + (1 - corr) * np.eye(n)
    return np.outer(sig, sig) * R


def _groups_from_sizes(sizes):
    groups, pos = [], 0
    for s in sizes:
        groups.append(list(range(pos, pos + s)))
        pos += s
    return groups


def _grouping(groups):
    return [{'bin_index': b, 'log10k_target': -2.2 + 0.1 * b, 'member_positions': ps}
            for b, ps in enumerate(groups)]


class TestBandAggregation:
    SIZES = [3, 4, 4, 6, 8, 9, 11, 11, 10]  # the real z=4.2 band sizes

    def test_weights_rows_sum_to_one_and_disjoint_support(self):
        rng = np.random.default_rng(0)
        cov = _synthetic_cov(66, rng)
        out = binmap.aggregate_bands(cov, _grouping(_groups_from_sizes(self.SIZES)))
        W = out['weights']
        assert W.shape == (9, 66)
        np.testing.assert_allclose(W.sum(axis=1), 1.0, atol=1e-12)
        assert np.count_nonzero(W) == 66  # each member in exactly one band

    def test_uncorrelated_reduces_to_inverse_variance(self):
        """Design Sec.1.2 property 2: diagonal C_66 -> C_9 diagonal, 1/sum(1/sigma^2)."""
        rng = np.random.default_rng(1)
        sig2 = rng.uniform(1.0, 25.0, 66)
        groups = _groups_from_sizes(self.SIZES)
        out = binmap.aggregate_bands(np.diag(sig2), _grouping(groups))
        expected = np.array([1.0 / np.sum(1.0 / sig2[ps]) for ps in groups])
        np.testing.assert_allclose(np.diag(out['cov_agg']), expected, rtol=1e-12)
        off = out['cov_agg'][~np.eye(9, dtype=bool)]
        assert np.all(np.abs(off) < 1e-15)
        np.testing.assert_allclose(out['diag_if_uncorrelated'], expected, rtol=1e-12)

    def test_single_member_band_is_identity(self):
        """Design Sec.1.2 property 3."""
        rng = np.random.default_rng(2)
        cov = _synthetic_cov(5, rng)
        groups = [[0], [1, 2], [3, 4]]
        data = rng.normal(size=5)
        out = binmap.aggregate_bands(cov, _grouping(groups), data_member=data)
        assert out['cov_agg'][0, 0] == pytest.approx(cov[0, 0], rel=1e-14)
        assert out['data_agg'][0] == pytest.approx(data[0], rel=1e-14)

    def test_positive_correlation_inflates_diagonal(self):
        """Design Sec.1.2 property 2, second sentence: with positively
        correlated members, (C_9)_bb exceeds the uncorrelated value."""
        rng = np.random.default_rng(3)
        cov = _synthetic_cov(66, rng, corr=0.3)
        out = binmap.aggregate_bands(cov, _grouping(_groups_from_sizes(self.SIZES)))
        assert np.all(np.diag(out['cov_agg']) > out['diag_if_uncorrelated'])

    def test_member_permutation_invariance(self):
        """Design Sec.1.2 property 4."""
        rng = np.random.default_rng(4)
        cov = _synthetic_cov(12, rng)
        data = rng.normal(size=12)
        g1 = [[0, 1, 2, 3], [4, 5, 6, 7, 8], [9, 10, 11]]
        g2 = [[3, 1, 0, 2], [8, 4, 7, 5, 6], [11, 9, 10]]
        a = binmap.aggregate_bands(cov, _grouping(g1), data_member=data)
        b = binmap.aggregate_bands(cov, _grouping(g2), data_member=data)
        np.testing.assert_allclose(a['cov_agg'], b['cov_agg'], rtol=1e-13)
        np.testing.assert_allclose(a['data_agg'], b['data_agg'], rtol=1e-13)

    def test_matches_independent_loop_derivation(self):
        rng = np.random.default_rng(5)
        cov = _synthetic_cov(66, rng, corr=0.2)
        groups = _groups_from_sizes(self.SIZES)
        out = binmap.aggregate_bands(cov, _grouping(groups))
        W_ref, C9_ref = _independent_option1(cov, groups)
        np.testing.assert_allclose(out['weights'], W_ref, rtol=1e-13)
        np.testing.assert_allclose(out['cov_agg'], C9_ref, rtol=1e-12)

    def test_symmetric_positive_definite_output(self):
        rng = np.random.default_rng(6)
        cov = _synthetic_cov(66, rng, corr=0.5)
        out = binmap.aggregate_bands(cov, _grouping(_groups_from_sizes(self.SIZES)))
        assert out['checks'] == {'symmetric': True, 'positive_definite_cholesky': True,
                                 'weight_rows_sum_to_one': True}
        np.linalg.cholesky(out['cov_agg'])

    def test_k_eff_is_weighted_mean_of_member_k(self):
        rng = np.random.default_rng(7)
        cov = _synthetic_cov(7, rng)
        k = np.sort(rng.uniform(0.005, 0.04, 7))
        groups = [[0, 1, 2], [3, 4, 5, 6]]
        out = binmap.aggregate_bands(cov, _grouping(groups), k_member=k)
        for b, ps in enumerate(groups):
            assert out['k_eff'][b] == pytest.approx(np.dot(out['weights'][b, ps], k[ps]))
        assert out['k_eff_over_k_target'].shape == (2,)

    @pytest.mark.parametrize('groups', [
        [[0, 1], [1, 2]],       # overlap
        [[0, 1], [3]],          # gap
        [[0, 1, 2], []],        # empty band
    ])
    def test_malformed_grouping_rejected(self, groups):
        cov = np.eye(4)
        with pytest.raises(ValueError):
            binmap.aggregate_bands(cov, _grouping(groups))

    def test_non_symmetric_input_rejected(self):
        cov = np.eye(3); cov[0, 1] = 0.5
        with pytest.raises(ValueError, match='symmetric'):
            binmap.aggregate_bands(cov, _grouping([[0, 1, 2]]))

    def test_tracked_member_artifact_aggregates_cleanly(self):
        """Runs on a clean checkout: the committed 66x66 BINMAP-C artifact
        through the pinned rule, cross-checked by the independent loop."""
        sub = np.load(TestDerivedCovarianceArtifacts.NPY)
        with open(TestDerivedCovarianceArtifacts.JSON) as f:
            grouping = json.load(f)['grouping']
        out = binmap.aggregate_bands(sub, grouping)
        groups = [g['member_positions'] for g in grouping]
        _, C9_ref = _independent_option1(sub, groups)
        np.testing.assert_allclose(out['cov_agg'], C9_ref, rtol=1e-12)
        assert out['checks']['positive_definite_cholesky']
        assert [b['n_members'] for b in out['bands']] == self.SIZES


class TestSweepAggregatedArtifacts:
    """The committed 2026-09-16 9x9 artifacts must equal what the pinned rule
    gives from the committed 66x66 artifact + CSV (clean checkout, no FITS)."""

    NPY = os.path.join(repo_root, 'data', 'derived',
                       'wp_e6_sweep_cov_agg9_z4p2_2026_09_16.npy')
    JSON = os.path.join(repo_root, 'data', 'derived',
                        'wp_e6_sweep_cov_agg9_z4p2_2026_09_16.json')

    def test_artifacts_exist(self):
        assert os.path.isfile(self.NPY)
        assert os.path.isfile(self.JSON)

    def test_npy_reproduces_from_member_artifact(self):
        sub = np.load(TestDerivedCovarianceArtifacts.NPY)
        with open(TestDerivedCovarianceArtifacts.JSON) as f:
            grouping = json.load(f)['grouping']
        out = binmap.aggregate_bands(sub, grouping)
        np.testing.assert_allclose(np.load(self.NPY), out['cov_agg'], rtol=1e-12)

    def test_json_consistent_with_csv(self):
        with open(self.JSON) as f:
            meta = json.load(f)
        assert meta['label'].startswith('DRAFT')
        assert 'TEST' not in meta['label'].split(';')[-1]
        assert meta['matrix_shape'] == [9, 9]
        assert all(meta['checks'].values())
        np.testing.assert_allclose(meta['row_sums'], 1.0, atol=1e-12)
        # P_9 and k_eff must be W applied to the CSV columns at the member rows
        df = pd.read_csv(DESI_CSV_PATH)
        idx = meta['member_csv_indices']
        W = np.array(meta['weights_9x66'])
        np.testing.assert_allclose(meta['data_agg_p1d_kms'],
                                   W @ df.loc[idx, 'p1d_kms'].values, rtol=1e-12)
        np.testing.assert_allclose(meta['k_eff_s_per_km'],
                                   W @ df.loc[idx, 'k_s_per_km'].values, rtol=1e-12)
        assert meta['provenance']['fits_sha256'] == binmap.COVARIANCE_FITS_SHA256_PIN


@needs_fits
class TestSweepAggregationFromFits:
    def test_fits_path_matches_tracked_artifact(self, result):
        np.testing.assert_allclose(
            result['aggregated_9x9'],
            np.load(TestSweepAggregatedArtifacts.NPY), rtol=1e-12)
