#!/usr/bin/env python3
"""
WP-E Phase 0: Preflight baseline (go/no-go) for 2D transverse topology on photo-z fields.

Revised WP-E protocol (T0 directive 2026-07-26): photo-z photo-z data has no radial
resolution; topology computed on 2D transverse slices at fixed redshift intervals dz.

This script:
1. Loads the real Euclid catalogue (SHA256 verification, abort if mismatch).
2. For each dz in (0.01, 0.20) or specified --dz:
   - Selects the top-3 most-populated redshift slices
   - Computes real 2D density field (nbins=32, absolute thresholds {0.5,1.0,1.5}×mean)
   - Generates 40 matched mock slices
   - Computes sigma = (real_beta_1 - mock_mean) / mock_std per slice/threshold
   - Gate verdict: any |sigma| > 5 -> NO-GO; all-None -> NO-GO; else GO
3. Persists JSON to data/derived/wp_e5_preflight_2026_07_26.json
4. Prints compact go/no-go table

MEASURED FACTS (do not re-derive):
- euclid_z_edf_north: 1983 valid objects, z_median=1.39, sigma_z=0.119
- dz=0.01 slices: ~25 objects max (topologically empty)
- dz=0.20 slices: ~196 objects (sigma_z-matched)

DOCUMENTED DEVIATION (per orchestrator):
- T0 directive specifies dz=0.01
- Results must show BOTH dz=0.01 and dz=0.20 side by side
- Note that dz below sigma_z slices finer than error kernel

Label: SANDBOX-EXPERIMENTAL (real-data-touching)
"""

import os
import sys
import json
import argparse
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

# Pipeline imports
from pipeline.transverse import select_slice, project_slice_2d, generate_mock_slice
from pipeline.topology2d import compute_betti_numbers_2d
from pipeline.realfield3d import density_shuffle_realization

# Constants
EUCLID_PATH = "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid_z/euclid_z_edf_north.csv"
EUCLID_SHA256 = "8b5b287f3f03165660e6232b904ee264e705788ffd60e67f54169ea2dddac2be"
OUTPUT_JSON = "data/derived/wp_e5_preflight_2026_07_26.json"
NBINS = 32
THRESHOLD_MULTIPLES = [0.5, 1.0, 1.5]
N_MOCKS = 40
SIGMA_GATE = 5.0


def verify_sha256(path: str, expected_sha256: str) -> None:
    """Abort loudly if file SHA256 does not match."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    computed = sha256.hexdigest()
    if computed != expected_sha256:
        print(f"ABORT: SHA256 mismatch for {path}", file=sys.stderr)
        print(f"  Expected: {expected_sha256}", file=sys.stderr)
        print(f"  Got:      {computed}", file=sys.stderr)
        sys.exit(1)


def load_catalogue() -> tuple:
    """Load and validate Euclid catalogue."""
    print(f"[preflight] Verifying {EUCLID_PATH}...")
    verify_sha256(EUCLID_PATH, EUCLID_SHA256)
    print(f"[preflight] SHA256 verified. Loading...")

    df = pd.read_csv(EUCLID_PATH)
    print(f"[preflight] Loaded {len(df)} rows total.")

    # Extract relevant columns (check MANIFEST.md for exact names)
    ra = df["right_ascension"].values
    dec = df["declination"].values
    z = df["phz_median"].values

    # Drop invalid redshifts
    valid = np.isfinite(z) & (z >= 0)
    ra = ra[valid]
    dec = dec[valid]
    z = z[valid]

    print(f"[preflight] After redshift validation: {len(z)} valid objects")
    print(f"[preflight] z range: [{z.min():.3f}, {z.max():.3f}], median: {np.median(z):.3f}")
    return ra, dec, z


def compute_real_stats(ra, dec, z_slice, thresholds):
    """Compute beta_1 for real field at given thresholds."""
    field = project_slice_2d(ra, dec, z_slice, nbins=NBINS)
    field_mean = float(np.mean(field))

    stats = {}
    for thr_mult in thresholds:
        thresh_val = thr_mult * field_mean
        betti = compute_betti_numbers_2d(field, threshold_value=thresh_val)
        stats[thr_mult] = betti["beta_1"]
    return field_mean, stats


def compute_mock_stats(n_objects, ra_range, dec_range, thresholds, seed_base, n_mocks):
    """Generate mocks and compute beta_1 distribution."""
    mock_stats = {thr: [] for thr in thresholds}

    # Compute field mean from first mock to use as reference
    ra_m, dec_m = generate_mock_slice(n_objects, ra_range, dec_range, seed_base)
    mock_field = project_slice_2d(ra_m, dec_m, np.ones(n_objects, dtype=bool), nbins=NBINS)
    field_mean = float(np.mean(mock_field))

    for i in range(n_mocks):
        ra_m, dec_m = generate_mock_slice(n_objects, ra_range, dec_range, seed_base + i)
        mask_m = np.ones(n_objects, dtype=bool)
        for thr_mult in thresholds:
            thresh_val = thr_mult * field_mean
            # Project the mock
            field_m = project_slice_2d(
                ra_m, dec_m, mask_m, nbins=NBINS,
                ranges=((ra_range[0], ra_range[1]), (dec_range[0], dec_range[1]))
            )
            betti = compute_betti_numbers_2d(field_m, threshold_value=thresh_val)
            mock_stats[thr_mult].append(betti["beta_1"])

    return field_mean, mock_stats


def compute_sigma(real_val, mock_vals):
    """Compute sigma = (real - mean) / std. Return None if std == 0."""
    if len(mock_vals) == 0:
        return None
    mock_mean = float(np.mean(mock_vals))
    mock_std = float(np.std(mock_vals))
    if mock_std == 0:
        return None
    return (real_val - mock_mean) / mock_std


def main():
    parser = argparse.ArgumentParser(description="WP-E Phase 0: Preflight baseline")
    parser.add_argument(
        "--dz",
        type=float,
        default=None,
        help="Single dz to test (default: both 0.01 and 0.20)",
    )
    parser.add_argument(
        "--output",
        default=OUTPUT_JSON,
        help=f"Output JSON path (default: {OUTPUT_JSON})",
    )
    args = parser.parse_args()

    # Load real catalogue
    ra, dec, z = load_catalogue()

    # Determine dz values to test
    dz_values = [args.dz] if args.dz is not None else [0.01, 0.20]

    # Output structure
    results = {
        "label": "SANDBOX-EXPERIMENTAL",
        "description": "WP-E Phase 0 preflight baseline (2D transverse topology, photo-z)",
        "euclid_sha256": EUCLID_SHA256,
        "nbins": NBINS,
        "n_mocks": N_MOCKS,
        "threshold_multiples": THRESHOLD_MULTIPLES,
        "sigma_gate": SIGMA_GATE,
        "observable": "betti_1_2D",
        "note": (
            "dz=0.01 per T0 directive; dz=0.20 (sigma_z-matched) included per DOCUMENTED DEVIATION. "
            "dz < sigma_z slices finer than error kernel."
        ),
        "per_dz": {},
    }

    # For each dz, select top-3 slices and compute verdicts
    for dz in dz_values:
        print(f"\n[preflight] Processing dz={dz}")
        dz_results = {
            "dz": dz,
            "slices": {},
            "verdict": None,
            "go_no_go": None,
        }

        # Find all non-empty slices and rank by occupancy
        z_min = z.min()
        z_max = z.max()
        z_lo_vals = np.arange(z_min, z_max, dz)

        slice_occupancies = []
        for z_lo in z_lo_vals:
            mask = select_slice(z, z_lo, dz)
            n_in_slice = mask.sum()
            if n_in_slice > 0:
                slice_occupancies.append((z_lo, n_in_slice, mask))

        # Sort by occupancy, descending
        slice_occupancies.sort(key=lambda x: x[1], reverse=True)
        top_3 = slice_occupancies[:3]

        print(f"[preflight] Top 3 slices for dz={dz}: {[(z_lo, n) for z_lo, n, _ in top_3]}")

        gate_fails = 0
        gate_all_none = True

        for idx, (z_lo, n_in_slice, mask) in enumerate(top_3):
            print(f"[preflight]   Slice {idx}: z_lo={z_lo:.4f}, n={n_in_slice}")

            # Compute real stats
            field_mean, real_stats = compute_real_stats(ra, dec, mask, THRESHOLD_MULTIPLES)

            # Compute mock stats
            ra_min, ra_max = ra.min(), ra.max()
            dec_min, dec_max = dec.min(), dec.max()
            _, mock_stats = compute_mock_stats(
                n_in_slice,
                (ra_min, ra_max),
                (dec_min, dec_max),
                THRESHOLD_MULTIPLES,
                seed_base=1000 + idx,
                n_mocks=N_MOCKS,
            )

            slice_key = f"z_lo_{z_lo:.4f}"
            dz_results["slices"][slice_key] = {
                "z_lo": float(z_lo),
                "n_objects": int(n_in_slice),
                "field_mean": float(field_mean),
                "verdicts": {},
            }

            for thr in THRESHOLD_MULTIPLES:
                sigma = compute_sigma(real_stats[thr], mock_stats[thr])
                thr_key = f"thr_{thr:.1f}"
                if sigma is None:
                    dz_results["slices"][slice_key]["verdicts"][thr_key] = {
                        "real_beta_1": int(real_stats[thr]),
                        "mock_mean": None,
                        "mock_std": None,
                        "sigma": None,
                        "gate": "NO-GO (zero variance)",
                    }
                    gate_fails += 1
                else:
                    gate_all_none = False
                    gate_verdict = "NO-GO" if abs(sigma) > SIGMA_GATE else "GO"
                    if abs(sigma) > SIGMA_GATE:
                        gate_fails += 1
                    dz_results["slices"][slice_key]["verdicts"][thr_key] = {
                        "real_beta_1": int(real_stats[thr]),
                        "mock_mean": float(np.mean(mock_stats[thr])),
                        "mock_std": float(np.std(mock_stats[thr])),
                        "sigma": float(sigma),
                        "gate": gate_verdict,
                    }

        # Overall verdict per dz
        if gate_all_none or gate_fails > 0:
            dz_results["verdict"] = "NO-GO"
            dz_results["go_no_go"] = False
        else:
            dz_results["verdict"] = "GO"
            dz_results["go_no_go"] = True

        results["per_dz"][f"dz_{dz:.2f}"] = dz_results
        print(f"[preflight] dz={dz}: {dz_results['verdict']}")

    # Persist JSON
    os.makedirs(os.path.dirname(OUTPUT_JSON) or ".", exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[preflight] Results persisted to {OUTPUT_JSON}")

    # Print summary table
    print("\n" + "=" * 70)
    print("PREFLIGHT SUMMARY")
    print("=" * 70)
    for dz_key, dz_res in results["per_dz"].items():
        print(f"\n{dz_key} → {dz_res['verdict']}")
        for slice_key, slice_info in dz_res["slices"].items():
            print(f"  {slice_key}: n={slice_info['n_objects']}")
            for thr_key, v in slice_info["verdicts"].items():
                if v["sigma"] is None:
                    print(f"    {thr_key}: sigma=None (zero variance) → NO-GO")
                else:
                    print(f"    {thr_key}: sigma={v['sigma']:.2f} → {v['gate']}")

    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

# Generated-by: Haiku 4.5 | Verified-by: pipeline tests + integration with real-data path |
# Reviewed-by: pending T0
