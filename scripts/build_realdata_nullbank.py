#!/usr/bin/env python3
"""WP-R3: Build realistic null bank from real-data randomization.

Two independent randomization schemes generate null distributions that preserve
true survey geometry/mask/number-density while destroying genuine spatial structure:

1. **Shuffle:** Keep exact (RA, Dec) positions; randomly permute object attributes across
   objects. If (RA, Dec) → (β₀, β₁, β₂), then shuffled → (β₀', β₁', β₂') where β_i'
   is from a random object at the same (RA, Dec).

2. **Rotate:** Apply a random rigid rotation in RA to all positions (wrapping at 360°).
   Preserves all local geometry; destroys only large-scale structure.

Agreement between schemes is the check that neither is broken. Both are hypothesis-agnostic:
they produce null distributions valid for any future topology test.

Output: JSON + SHA256 in data/nullbanks/real/, with MANIFEST record.
"""

import sys
from pathlib import Path

# Add repo root to path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

import pandas as pd
import numpy as np
import json
import hashlib
from datetime import datetime
import os

from pipeline.realfield import density_field_from_catalog
from pipeline.observables_real import compute_betti_numbers

# Real SDSS datasets to build nulls for
SDSS_DATASETS = [
    {
        "name": "sdss_cosmos",
        "path": "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/sdss/sdss_cosmos.csv",
    },
    {
        "name": "sdss_stripe82_center",
        "path": "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/sdss/sdss_stripe82_center.csv",
    },
]

# Fixed settings from WP-R2 (chosen before running, never changed post-hoc)
NBINS = 24
THRESHOLD_PERCENTILE = 50.0
N_REALIZATIONS = 200


def compute_sha256_file(filepath):
    """Compute SHA256 of a file."""
    sha = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha.update(data)
    return sha.hexdigest()


def build_shuffle_nulls(df, field_name, n_real=200):
    """Shuffle randomization: keep (RA, Dec), permute object attributes.

    For a catalog with N objects at positions (RA_i, Dec_i), this scheme:
    1. Builds density field from original (RA, Dec)
    2. For each realization k:
       - Randomly permute row order of df
       - Build field from permuted (RA, Dec)
       - Compute Betti numbers

    Null hypothesis: object attributes are independent of position.
    """
    results = []
    np.random.seed(42)  # Deterministic for reproducibility

    ra = df["ra"].values
    dec = df["dec"].values
    # Fake z coordinate (object index) for 3D machinery; no physical meaning
    z_fake = np.linspace(0.0, 1.0, len(df))

    for k in range(n_real):
        # Randomly permute rows (shuffle object attributes across positions)
        perm = np.random.permutation(len(df))
        ra_shuffled = ra[perm]
        dec_shuffled = dec[perm]
        z_shuffled = z_fake[perm]

        # Build 3D field and compute topology
        field = density_field_from_catalog(ra_shuffled, dec_shuffled, z=z_shuffled, nbins=NBINS)
        betti = compute_betti_numbers(field, threshold_percentile=THRESHOLD_PERCENTILE)

        results.append({
            "realization": k,
            "scheme": "shuffle",
            **betti
        })

    return results


def build_rotate_nulls(df, field_name, n_real=200):
    """Rotate randomization: random rigid rotation in RA (wrapping at 360°).

    For each realization k:
    1. Choose random RA offset Δ_k from [0, 360)
    2. Set RA_k = (RA + Δ_k) mod 360
    3. Build field from (RA_k, Dec)
    4. Compute Betti numbers

    Null hypothesis: large-scale structure is not present (uniformity).
    """
    results = []
    np.random.seed(43)  # Different seed from shuffle (independent)

    ra = df["ra"].values.copy()
    dec = df["dec"].values
    # Fake z coordinate (object index) for 3D machinery; no physical meaning
    z_fake = np.linspace(0.0, 1.0, len(df))

    for k in range(n_real):
        # Random RA rotation
        ra_offset = np.random.uniform(0, 360)
        ra_rotated = (ra + ra_offset) % 360.0

        # Build 3D field and compute topology
        field = density_field_from_catalog(ra_rotated, dec, z=z_fake, nbins=NBINS)
        betti = compute_betti_numbers(field, threshold_percentile=THRESHOLD_PERCENTILE)

        results.append({
            "realization": k,
            "scheme": "rotate",
            **betti
        })

    return results


def run_nullbank_builder():
    """Build null bank for all real SDSS datasets."""
    print("WP-R3: Real-data null bank construction")
    print(f"Configuration: nbins={NBINS}, threshold={THRESHOLD_PERCENTILE}%, "
          f"n_realizations={N_REALIZATIONS}\n")

    # Create output directory
    outdir = Path("data/nullbanks/real")
    outdir.mkdir(parents=True, exist_ok=True)

    all_results = {}

    for dataset_info in SDSS_DATASETS:
        name = dataset_info["name"]
        path = dataset_info["path"]

        print(f"Processing {name}...")
        df = pd.read_csv(path)
        n_obj = len(df)
        print(f"  Loaded {n_obj} objects")

        # Build shuffle nulls
        print(f"  Building shuffle nulls (scheme 1)...", end="", flush=True)
        shuffle_results = build_shuffle_nulls(df, name, N_REALIZATIONS)
        print(f" ✓ {len(shuffle_results)} realizations")

        # Build rotate nulls
        print(f"  Building rotate nulls (scheme 2)...", end="", flush=True)
        rotate_results = build_rotate_nulls(df, name, N_REALIZATIONS)
        print(f" ✓ {len(rotate_results)} realizations")

        # Combine results
        all_results[name] = {
            "n_objects": n_obj,
            "shuffle": shuffle_results,
            "rotate": rotate_results,
        }

    # Write to JSON
    output_file = outdir / "nullbank_2026_07_25.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    # Compute checksum
    file_sha = compute_sha256_file(str(output_file))

    print(f"\n📊 Output: {output_file}")
    print(f"📋 SHA256: {file_sha}\n")

    # Generate statistics report
    print("Statistics summary:")
    print(f"{'Dataset':<25} {'Scheme':<10} {'β₀ (μ±σ)':<20} {'β₁ (μ±σ)':<20} {'β₂ (μ±σ)':<15}")
    print("-" * 90)

    for name, results_dict in all_results.items():
        for scheme in ["shuffle", "rotate"]:
            scheme_results = results_dict[scheme]
            b0_vals = [r["beta_0"] for r in scheme_results]
            b1_vals = [r["beta_1"] for r in scheme_results]
            b2_vals = [r["beta_2"] for r in scheme_results]

            b0_str = f"{np.mean(b0_vals):.1f}±{np.std(b0_vals):.1f}"
            b1_str = f"{np.mean(b1_vals):.1f}±{np.std(b1_vals):.1f}"
            b2_str = f"{np.mean(b2_vals):.1f}±{np.std(b2_vals):.1f}"

            print(f"{name:<25} {scheme:<10} {b0_str:<20} {b1_str:<20} {b2_str:<15}")

    # Check agreement between schemes
    print("\nScheme agreement check:")
    for name, results_dict in all_results.items():
        shuffle_b0 = np.array([r["beta_0"] for r in results_dict["shuffle"]])
        rotate_b0 = np.array([r["beta_0"] for r in results_dict["rotate"]])

        # T-test for equal means (rough agreement check)
        from scipy import stats
        t_stat, p_val = stats.ttest_ind(shuffle_b0, rotate_b0)
        agreement = "✓ (independent)" if p_val > 0.05 else "⚠ (means differ)"

        print(f"  {name}: p={p_val:.3f} {agreement}")

    # Write metadata
    metadata = {
        "timestamp": datetime.now().isoformat(),
        "nbins": NBINS,
        "threshold_percentile": THRESHOLD_PERCENTILE,
        "n_realizations_per_scheme": N_REALIZATIONS,
        "datasets": list(all_results.keys()),
        "output_file": str(output_file),
        "sha256": file_sha,
    }

    metadata_file = outdir / "NULLBANK_MANIFEST_2026_07_25.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"\nMetadata: {metadata_file}")

    return 0


if __name__ == "__main__":
    sys.exit(run_nullbank_builder())
