#!/usr/bin/env python3
"""
WP-E6-BINMAP — 9-bin Restriction Map & DESI DR1 P1D Data Contact

ENGINEERING / DESIGN, DRAFT label (per CLAUDE.md rule 3 — not TEST, not FIT).

Authority: T0 RATIFICATION 2026-07-31 (DL-1..DL-5). Real-data contact authorized
under escalation PIN (real-data k-bin and covariance source gaps identified separately).

Scope (IMMUTABLE): Build the exact 9-bin restriction map from emulator K_BINS
(log₁₀k = −2.2…−1.4) into the DESI DR1 P1D CSV's native 85 k-bin grid. Use 0.1-dex
bands centered on each target; verify bin membership against k ≤ 0.0527412 s/km
Nyquist constraint.

Status: BLOCKED on real-data covariance. This module maps bins and flags where
to extract covariance (DESI Collaboration 2024 Zenodo FITS, HDU COVARIANCE);
retrieval is a datalake acquisition decision (T0-gated, not deployed here).

Key findings:
1. Z-GRID MISMATCH: Emulator Z_FLOAT = {4.2, 4.6, 5.0}; DESI CSV z ∈ {2.2, ..., 4.4}.
   Only z = 4.2 overlaps. A 9×9 real-data covariance sub-block is necessarily
   a single-z slice at z = 4.2 only. (See escalation flags in code.)

2. COVARIANCE NOT IN THIS BUCKET: GCS stream3_desi_dr1/ holds BAO (DM/DH/DV)
   measurements only. DESI P1D k-bin covariance lives in Zenodo publication data
   (DOI 10.5281/zenodo.16943723, `desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits`,
   HDU COVARIANCE). Data/MANIFEST.md §101-123 documents provenance; `e_total_kms`
   column in the CSV is the diagonal. Full covariance is not stored in this repo
   (GitHub 100MB limit). Fetching it is a T0-gated datalake acquisition.

3. BIN MEMBERSHIP: Each of 9 emulator bins is defined as log₁₀k ∈ [target − 0.05, target + 0.05]
   (0.1 dex band, matching wp_e6_covariance.py line 438). Band membership is
   one-to-many; each bin collects all DESI rows within its k-range. Independent
   re-verification: log₁₀k arithmetic on DESI k values, not reusing this module.
   Never interpolate across bins.

Outputs:
  - restriction_map(k_desi_csv, emulator_k_targets, z_target=4.2)
    → dict with band membership, verification status, escalation flags
  - covariance_block(map_output)
    → raises NotImplementedError with pointer to Zenodo FITS and remediation.
"""

import os
import sys
import json
import numpy as np
import pandas as pd

__all__ = ['restriction_map', 'covariance_block', 'verify_bins']


def restriction_map(desi_csv_path, emulator_k_targets=None, z_target=4.2):
    """
    Build bin membership map from emulator K_BINS to DESI DR1 P1D CSV rows.

    Parameters
    ----------
    desi_csv_path : str
        Path to DESI DR1 P1D CSV (columns: z, k_s_per_km, p1d_kms, errors, pfid_kms).
    emulator_k_targets : array-like, optional
        Emulator K_BINS targets (s/km). If None, use the 9 natively-resolved bins.
    z_target : float, optional
        Redshift slice to extract (default 4.2, only overlap between emulator and DESI).

    Returns
    -------
    dict
        'bands': list of 9 dicts, each with:
            'bin_index': int (0-8)
            'log10k_target': float (target log10 k)
            'k_target': float (target k in s/km)
            'band_min': float (lower k edge, exclusive; used for log-space band def)
            'band_max': float (upper k edge, exclusive)
            'members': list of int (DESI CSV row indices in this band)
            'member_k_values': list of float (actual k values of members, s/km)
            'member_indices': list of int (DESI bin indices for each member)
            'nearest_neighbor_idx': int (index of DESI row closest to k_target)
            'all_within_nyquist': bool (every member k ≤ 0.0527412?)
        'z_selected': float (redshift of the slice)
        'z_overlap_status': str (escalation note on z mismatch)
        'metadata': dict with CSV provenance, date, counts
    """

    if not os.path.isfile(desi_csv_path):
        raise FileNotFoundError(f"DESI CSV not found: {desi_csv_path}")

    # Load DESI P1D data
    df = pd.read_csv(desi_csv_path)

    # Define 9 natively-resolved emulator K_BINS if not provided
    if emulator_k_targets is None:
        emulator_log10k = np.array([-2.2, -2.1, -2.0, -1.9, -1.8, -1.7, -1.6, -1.5, -1.4])
        emulator_k_targets = 10.0 ** emulator_log10k
    else:
        emulator_k_targets = np.asarray(emulator_k_targets)
        emulator_log10k = np.log10(emulator_k_targets)

    # Filter to the target redshift
    df_z = df[df['z'] == z_target].copy()
    if len(df_z) == 0:
        available_z = sorted(df['z'].unique())
        raise ValueError(
            f"z={z_target} not found in DESI CSV. "
            f"Available z values: {available_z}. "
            f"Emulator Z_FLOAT = {{4.2, 4.6, 5.0}}; only z=4.2 overlaps DESI CSV range."
        )

    # Extract k-values and compute log10k
    k_desi = df_z['k_s_per_km'].values
    log10k_desi = np.log10(k_desi)
    desi_row_indices = df_z.index.values  # Original row indices in full CSV

    # Nyquist limit (from wp_e6_covariance.py L25)
    k_nyquist = 0.0527412  # s/km

    # Build membership for each emulator bin
    # Band: log10k ∈ [target − 0.05, target + 0.05] (0.1 dex wide)
    bands = []

    for bin_idx, (k_target, log10k_target) in enumerate(zip(emulator_k_targets, emulator_log10k)):
        band_min_log = log10k_target - 0.05
        band_max_log = log10k_target + 0.05
        band_min_k = 10.0 ** band_min_log
        band_max_k = 10.0 ** band_max_log

        # Find members: log10k ∈ [band_min_log, band_max_log]
        mask = (log10k_desi >= band_min_log) & (log10k_desi <= band_max_log)
        member_log10k = log10k_desi[mask]
        member_k = k_desi[mask]
        member_desi_indices = desi_row_indices[mask]

        # Nearest neighbor
        if len(member_k) > 0:
            nn_local_idx = np.argmin(np.abs(member_k - k_target))
            nn_desi_idx = member_desi_indices[nn_local_idx]
        else:
            nn_desi_idx = np.argmin(np.abs(k_desi - k_target))

        # Verify Nyquist
        all_within_nyquist = np.all(member_k <= k_nyquist) if len(member_k) > 0 else True

        bands.append({
            'bin_index': bin_idx,
            'log10k_target': float(log10k_target),
            'k_target': float(k_target),
            'band_min_log10k': float(band_min_log),
            'band_max_log10k': float(band_max_log),
            'band_min_k': float(band_min_k),
            'band_max_k': float(band_max_k),
            'members': member_desi_indices.tolist(),
            'member_k_values': member_k.tolist(),
            'member_log10k_values': member_log10k.tolist(),
            'nearest_neighbor_csv_idx': int(nn_desi_idx),
            'all_within_nyquist': bool(all_within_nyquist),
            'member_count': len(member_k),
            'k_nyquist_limit': float(k_nyquist),
        })

    # Escalation notes
    z_overlap_note = (
        "Z-grid mismatch escalation (T0-acknowledged 2026-07-31): "
        "Emulator Z_FLOAT = {4.2, 4.6, 5.0}; DESI CSV z ∈ {2.2, ..., 4.4, step 0.2}. "
        f"Only z={z_target} overlaps. This restriction to a single-z slice means "
        "any real-data covariance sub-block is necessarily (9×9) for z=4.2 only. "
        "A z-dependent covariance (P1D redshift evolution) cannot be tested until "
        "emulator is extended to z ∈ {2.2, ..., 4.2, ...} or real data restricted to z={4.2}. "
        "(Documented escalation, not error.)"
    )

    return {
        'bands': bands,
        'z_selected': float(z_target),
        'z_overlap_status': z_overlap_note,
        'metadata': {
            'source_csv': str(desi_csv_path),
            'emulator_k_bins': emulator_k_targets.tolist(),
            'emulator_log10k_bins': emulator_log10k.tolist(),
            'n_emulator_bins': len(emulator_k_targets),
            'desi_csv_rows_total': len(df),
            'desi_csv_rows_at_z': len(df_z),
            'k_nyquist_s_per_km': k_nyquist,
            'bin_membership_def': '0.1 dex bands centered on each target',
        },
    }


def verify_bins(map_output):
    """
    Independent verification that bin membership is correct.
    Re-computes membership from log₁₀k arithmetic (not reusing restriction_map).

    Parameters
    ----------
    map_output : dict
        Output from restriction_map().

    Returns
    -------
    dict
        Verification results: 'all_bins_nonempty', 'all_within_nyquist',
        'membership_matches', 'k_nyquist_max', 'escalation_flags'.
    """

    z = map_output['z_selected']
    desi_csv = map_output['metadata']['source_csv']
    df = pd.read_csv(desi_csv)
    df_z = df[df['z'] == z].copy()

    k_desi = df_z['k_s_per_km'].values
    log10k_desi = np.log10(k_desi)
    desi_indices = df_z.index.values

    k_nyquist = map_output['metadata']['k_nyquist_s_per_km']
    emulator_k = map_output['metadata']['emulator_k_bins']
    emulator_log10k = np.log10(emulator_k)

    # Verify each band independently
    all_nonempty = True
    all_within_nyquist = True
    membership_matches = True
    max_k = 0.0

    for band in map_output['bands']:
        bin_idx = band['bin_index']
        log10k_target = band['log10k_target']
        band_min_log = log10k_target - 0.05
        band_max_log = log10k_target + 0.05

        # Re-compute membership independently
        mask = (log10k_desi >= band_min_log) & (log10k_desi <= band_max_log)
        independent_members = desi_indices[mask].tolist()
        stored_members = band['members']

        if independent_members != stored_members:
            membership_matches = False

        if len(independent_members) == 0:
            all_nonempty = False

        member_k = k_desi[mask]
        if len(member_k) > 0:
            if np.any(member_k > k_nyquist):
                all_within_nyquist = False
            max_k = max(max_k, member_k.max())

    return {
        'all_bins_nonempty': all_nonempty,
        'all_within_nyquist': all_within_nyquist,
        'membership_matches_stored': membership_matches,
        'k_nyquist_max_s_per_km': float(max_k),
        'k_nyquist_limit': k_nyquist,
        'passes': all_nonempty and all_within_nyquist and membership_matches,
    }


def covariance_block(map_output, covariance_fits_path=None):
    """
    Extract the real DESI DR1 P1D covariance sub-block for the 9 bins.

    THIS FUNCTION IS INTENTIONALLY BLOCKED.

    The full P1D covariance matrix resides in the DESI Collaboration's Zenodo
    publication (DOI 10.5281/zenodo.16943723):
      file: desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits
      HDU: COVARIANCE (1020 × 1020 matrix, covering all 12 z × 85 k bins)

    To extract the sub-block for the 9 resolved bins at z=4.2:
    1. Download FITS file from Zenodo.
    2. Open HDU COVARIANCE → full 1020×1020 matrix.
    3. Extract rows/cols corresponding to the 9 emulator bins at z=4.2
       (using the 'members' field from map_output['bands']).
    4. Return 9×9 symmetric sub-block + eigenvalue spectrum verification.

    Fetching this covariance is a datalake acquisition decision (T0-gated under
    escalation PIN). This function raises NotImplementedError with remediation steps.

    Parameters
    ----------
    map_output : dict
        Output from restriction_map().
    covariance_fits_path : str, optional
        Path to locally downloaded FITS file (if already fetched outside this module).

    Returns
    -------
    None (always raises)

    Raises
    ------
    NotImplementedError
        With remediation instructions.
    """

    raise NotImplementedError(
        "Real DESI DR1 P1D covariance extraction is blocked pending T0 datalake decision.\n\n"
        "Remediation (T0 approval required):\n"
        "  1. Authority: DESI Collaboration 2024, Zenodo DOI 10.5281/zenodo.16943723\n"
        "  2. File: desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits\n"
        "  3. HDU: COVARIANCE (1020 × 1020 matrix)\n"
        "  4. Rows/cols to extract:\n"
        f"       z = {map_output['z_selected']}\n"
        f"       Band membership (DESI CSV row indices) from map_output['bands']\n"
        "  5. Symmetry check & eigenvalue spectrum required in output.\n"
        "  6. Escalation PIN notes (real-data-contact gaps):\n"
        "       - No published k-bin ↔ emulator-bin correspondence (independent\n"
        "         re-verification of bin membership required, DONE).\n"
        "       - No documented covariance sub-block extraction protocol\n"
        "         (this module provides the bin map; sub-block extraction deferred).\n\n"
        "Decision precedent: WP-E6-P2A (wp_e6_covariance.py) delivered 9×9 synthetic\n"
        "covariance and refused to fabricate the other 7 bins; same structure here.\n"
    )


if __name__ == '__main__':
    # Quick test
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    desi_csv = os.path.join(repo_root, 'data', 'literature', 'desi_dr1_lya_p1d_2026_07_27.csv')

    print("WP-E6-BINMAP: 9-bin Restriction Map for DESI DR1 P1D")
    print("=" * 70)

    map_out = restriction_map(desi_csv, z_target=4.2)

    print(f"Redshift: z = {map_out['z_selected']}")
    print(f"Total bins: {len(map_out['bands'])}")
    print()

    for band in map_out['bands']:
        print(
            f"Bin {band['bin_index']}: "
            f"log10k = {band['log10k_target']:.2f} "
            f"(band [{band['band_min_log10k']:.3f}, {band['band_max_log10k']:.3f}]) "
            f"→ {band['member_count']} DESI rows, "
            f"Nyquist OK: {band['all_within_nyquist']}"
        )

    print()
    print("Verification:")
    vresult = verify_bins(map_out)
    print(f"  All bins nonempty: {vresult['all_bins_nonempty']}")
    print(f"  All within Nyquist: {vresult['all_within_nyquist']}")
    print(f"  Membership matches: {vresult['membership_matches_stored']}")
    print(f"  Max k in data: {vresult['k_nyquist_max_s_per_km']:.10f} s/km")
    print(f"  Nyquist limit: {vresult['k_nyquist_limit']:.10f} s/km")
    print(f"  Overall PASS: {vresult['passes']}")

    print()
    print("Escalation flags:")
    print(map_out['z_overlap_status'])
