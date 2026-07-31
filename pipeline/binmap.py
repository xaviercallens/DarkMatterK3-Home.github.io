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

Status (updated 2026-07-31, WP-E6-BINMAP-C): covariance extraction UNBLOCKED by
T1 delegated ruling R2 (`briefs/T1_DELEGATED_RULINGS_2026_07_31.md`, executing
T0-ratified D1 `dbf1337`). `covariance_block()` now extracts the real member-level
sub-block from the MANIFEST-pinned Zenodo FITS (fetched via `scripts/fetch_data.py`),
behind a mandatory SHA-256 hard gate. Calling it WITHOUT an explicit FITS path
still raises NotImplementedError — real-data contact stays a deliberate,
explicit-path act, never an implicit default.

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


# MANIFEST-pinned SHA-256 of the Zenodo FITS (data/MANIFEST.md, literature
# section 2026-07-27 entry; same value as scripts/data_fetchers.py's pin).
# HARD GATE: covariance_block() refuses to read any FITS whose SHA-256
# differs from this value.
COVARIANCE_FITS_SHA256_PIN = (
    "bbb98dc3d1865a50bb878e949a644604ce729da419db8e7db5adbb532a894857"
)
COVARIANCE_FITS_NAME = (
    "desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits"
)


def _sha256_of_file(path, chunk=1 << 20):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def covariance_block(map_output, covariance_fits_path=None):
    """
    Extract the real DESI DR1 P1D covariance sub-block for the 9-bin member rows.

    UNBLOCKED 2026-07-31 (WP-E6-BINMAP-C): T1 delegated ruling R2
    (`briefs/T1_DELEGATED_RULINGS_2026_07_31.md`), executing T0-ratified D1
    (`dbf1337`). Source artifact: DESI Collaboration Zenodo release
    (DOI 10.5281/zenodo.16943723), file
    desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits,
    HDU COVARIANCE (1020 × 1020; ordering = 12 z-bins × 85 k-bins, identical
    to the row order of data/literature/desi_dr1_lya_p1d_2026_07_27.csv).
    Fetch it via `scripts/fetch_data.py` (lands in
    data/raw/desi_dr1_lya_p1d_zenodo/, gitignored).

    HARD GATE: the file's SHA-256 must equal COVARIANCE_FITS_SHA256_PIN
    (the data/MANIFEST.md pin) BEFORE the FITS is opened. Mismatch raises
    RuntimeError and nothing is read.

    Deliverable is the MEMBER-LEVEL sub-block (66×66 at z=4.2 for the default
    map) plus the 9-bin index grouping. NO 9×9 band-aggregated block is
    produced: neither the pinned PREDICTION v2 amendment
    (`briefs/PREDICTION_V2_AMENDMENT_DRAFT_2026_07_29.md`, §8 resolution
    item 2) nor this module defines a band-aggregation (band-averaging)
    rule — the pin names the scheme as something WP-E6-BINMAP builds *and
    verifies before the sweep consumes it*, and no LIVE/pinned document fixes
    the rule. Inventing one here would be a free analysis choice; it is left
    to a ruled design, not fabricated (WP-E6-P2A precedent).

    Mandatory built-in cross-checks (all must pass or this function raises):
      1. diag(sub-block) == e_total_kms**2 from the CSV, row-for-row
         (rtol 1e-6) — the CSV and the FITS reached the repo by different
         paths, so agreement is a genuine integrity check, not circular.
      2. Symmetry (np.allclose with its transpose).
      3. Positive-definiteness (np.linalg.cholesky succeeds).

    Parameters
    ----------
    map_output : dict
        Output from restriction_map().
    covariance_fits_path : str, optional
        Explicit path to the hash-verified local FITS. REQUIRED for
        extraction: passing None raises NotImplementedError (real-data
        contact must be an explicit act, never a silent default).

    Returns
    -------
    dict with keys:
        'cov_member' : np.ndarray, (66, 66) member-level sub-block (s/km units
                       of P1D, squared)
        'member_csv_indices' : list of int, CSV row indices (sorted, unique)
        'grouping' : list of 9 dicts — bin_index, log10k_target,
                     member_csv_indices, member_positions (positions into
                     cov_member's axes)
        'checks' : dict — diag_matches_csv, max_rel_diag_discrepancy,
                   symmetric, positive_definite, all mandatory checks True
        'eigenvalues' : list of float (ascending)
        'condition_number' : float
        'aggregated_9x9' : None (see docstring — no aggregation rule defined)
        'aggregation_note' : str
        'provenance' : dict — fits path, sha256 (verified == pin), HDU name,
                       z_selected

    Raises
    ------
    NotImplementedError
        If covariance_fits_path is None (extraction requires the explicit,
        hash-gated path; previously this entire function was blocked pending
        the T0 datalake decision — that gate is now cleared by ruling R2).
    RuntimeError
        If the SHA-256 hard gate fails (file is NOT read), or any mandatory
        cross-check fails.
    """
    if covariance_fits_path is None:
        raise NotImplementedError(
            "Real DESI DR1 P1D covariance extraction requires an explicit local\n"
            "FITS path — it was formerly blocked pending the T0 datalake decision;\n"
            "that decision is now made (T1 ruling R2 2026-07-31, executing T0 D1),\n"
            "but real-data contact stays an explicit act:\n"
            "  1. Fetch: python scripts/fetch_data.py — pulls Zenodo DOI\n"
            "     10.5281/zenodo.16943723 (data_points.tar) and extracts\n"
            f"     {COVARIANCE_FITS_NAME}\n"
            "     into data/raw/desi_dr1_lya_p1d_zenodo/ behind the SHA-256 gate.\n"
            "  2. Call covariance_block(map_output, covariance_fits_path=<that path>).\n"
            "  3. HDU: COVARIANCE (1020 × 1020 matrix).\n"
            f"     z = {map_output['z_selected']}; rows/cols = the 'members' CSV row\n"
            "     indices from map_output['bands'].\n"
        )

    # ---- HARD GATE: SHA-256 vs the MANIFEST pin, BEFORE any read ----------
    computed_sha = _sha256_of_file(covariance_fits_path)
    if computed_sha != COVARIANCE_FITS_SHA256_PIN:
        raise RuntimeError(
            "HARD-GATE FAILURE (WP-E6-BINMAP-C): FITS SHA-256 mismatch — file NOT read.\n"
            f"  path:     {covariance_fits_path}\n"
            f"  computed: {computed_sha}\n"
            f"  pinned:   {COVARIANCE_FITS_SHA256_PIN} (data/MANIFEST.md)\n"
            "Stop and escalate; do not proceed past a hash mismatch."
        )

    from astropy.io import fits as _fits

    with _fits.open(covariance_fits_path) as hdul:
        cov_full = np.asarray(hdul['COVARIANCE'].data, dtype=np.float64)
    if cov_full.shape != (1020, 1020):
        raise RuntimeError(
            f"COVARIANCE HDU has shape {cov_full.shape}, expected (1020, 1020)."
        )

    # ---- Member indices from the verified bin map --------------------------
    member_indices = [i for band in map_output['bands'] for i in band['members']]
    if len(member_indices) != len(set(member_indices)):
        raise RuntimeError("Band membership contains duplicate CSV row indices.")
    if member_indices != sorted(member_indices):
        raise RuntimeError("Concatenated band members are not in ascending CSV order.")

    grouping = []
    pos = 0
    for band in map_output['bands']:
        n = len(band['members'])
        grouping.append({
            'bin_index': band['bin_index'],
            'log10k_target': band['log10k_target'],
            'member_csv_indices': list(band['members']),
            'member_positions': list(range(pos, pos + n)),
        })
        pos += n

    sub = cov_full[np.ix_(member_indices, member_indices)]

    # ---- Mandatory cross-check 1: diag == e_total_kms**2 (rtol 1e-6) -------
    df = pd.read_csv(map_output['metadata']['source_csv'])
    e_total_sq = df.loc[member_indices, 'e_total_kms'].values ** 2
    diag = np.diag(sub)
    rel = np.abs(diag - e_total_sq) / e_total_sq
    diag_ok = bool(np.all(rel <= 1e-6))

    # ---- Mandatory cross-check 2: symmetry ----------------------------------
    symmetric = bool(np.allclose(sub, sub.T, rtol=1e-12, atol=0.0))

    # ---- Mandatory cross-check 3: positive-definiteness (Cholesky) ----------
    try:
        np.linalg.cholesky(sub)
        pos_def = True
    except np.linalg.LinAlgError:
        pos_def = False

    if not (diag_ok and symmetric and pos_def):
        raise RuntimeError(
            "Mandatory cross-check FAILURE (WP-E6-BINMAP-C):\n"
            f"  diag == e_total_kms**2 (rtol 1e-6): {diag_ok} "
            f"(max rel discrepancy {float(np.max(rel)):.3e})\n"
            f"  symmetric: {symmetric}\n"
            f"  positive-definite (Cholesky): {pos_def}\n"
            "Do not use this sub-block; escalate."
        )

    eigenvalues = np.linalg.eigvalsh(sub)

    return {
        'cov_member': sub,
        'member_csv_indices': list(member_indices),
        'grouping': grouping,
        'checks': {
            'diag_matches_csv_e_total_sq_rtol1e6': diag_ok,
            'max_rel_diag_discrepancy': float(np.max(rel)),
            'symmetric': symmetric,
            'positive_definite_cholesky': pos_def,
        },
        'eigenvalues': eigenvalues.tolist(),
        'condition_number': float(eigenvalues.max() / eigenvalues.min()),
        'aggregated_9x9': None,
        'aggregation_note': (
            "No 9x9 band-aggregated block is produced: neither the pinned "
            "PREDICTION v2 amendment (§8 resolution item 2) nor pipeline/binmap.py "
            "defines a band-aggregation rule. Deliverable is the member-level "
            "sub-block plus the 9-bin index grouping; the aggregation scheme "
            "requires its own ruled design before the sweep consumes it."
        ),
        'provenance': {
            'fits_path': str(covariance_fits_path),
            'fits_sha256': computed_sha,
            'sha256_pin_source': 'data/MANIFEST.md (literature entry, 2026-07-27)',
            'hdu': 'COVARIANCE',
            'z_selected': map_output['z_selected'],
            'n_members': len(member_indices),
        },
    }


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
