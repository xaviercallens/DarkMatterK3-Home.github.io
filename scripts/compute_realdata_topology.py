#!/usr/bin/env python3
"""Real-data topology analysis: compute Betti numbers on real SDSS fields.

Loads validated SDSS datasets, builds 3D density fields, computes topology
statistics, and compares to pre-built null bank. All labeled ENGINEERING
(no TEST/FIT; gate G1-L closed).

Results saved to external disk with full provenance tracking.
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

from pipeline.realfield import density_field_from_catalog
from pipeline.observables_real import compute_betti_numbers

# Real SDSS datasets to analyze
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

# Configuration (same as null bank: nbins=24, threshold=50th percentile)
NBINS = 24
THRESHOLD_PERCENTILE = 50.0

# Output directory on external disk
OUTPUT_DIR = Path("/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/topology_results")


def compute_percentile_rank(value, null_distribution):
    """Compute percentile rank of a value within a null distribution."""
    null_array = np.array(null_distribution)
    rank = np.mean(null_array <= value) * 100
    return float(rank)


def run_topology_analysis():
    """Compute topology on real SDSS data and compare to null bank."""
    print("Real-Data Topology Analysis")
    print("=" * 80)
    print(f"Configuration: nbins={NBINS}, threshold={THRESHOLD_PERCENTILE}%")
    print(f"Scope: ENGINEERING only (no TEST/FIT; gate G1-L closed)\n")

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load null bank
    print("Loading pre-built null bank...")
    nullbank_path = Path("data/nullbanks/real/nullbank_2026_07_25.json")
    with open(nullbank_path) as f:
        null_bank = json.load(f)
    print(f"  ✓ Loaded {len(null_bank)} datasets from null bank\n")

    # Analyze each real dataset
    results = {}

    for dataset_info in SDSS_DATASETS:
        name = dataset_info["name"]
        path = dataset_info["path"]

        print(f"Analyzing {name}...")
        df = pd.read_csv(path)
        n_obj = len(df)
        print(f"  Loaded {n_obj} objects")

        # Build 3D field (fake z = object index)
        ra = df["ra"].values
        dec = df["dec"].values
        z_fake = np.linspace(0.0, 1.0, n_obj)

        print(f"  Building density field (nbins={NBINS})...", end="", flush=True)
        field = density_field_from_catalog(ra, dec, z=z_fake, nbins=NBINS)
        print(" ✓")

        # Compute topology
        print(f"  Computing Betti numbers...", end="", flush=True)
        topo = compute_betti_numbers(field, threshold_percentile=THRESHOLD_PERCENTILE)
        print(" ✓")

        # Compare to null bank
        if name in null_bank:
            null_shuffle = np.array([r["beta_0"] for r in null_bank[name]["shuffle"]])
            null_rotate = np.array([r["beta_0"] for r in null_bank[name]["rotate"]])

            # Combined null distribution
            null_combined = np.concatenate([null_shuffle, null_rotate])

            # Compute percentile ranks
            b0_percentile = compute_percentile_rank(topo["beta_0"], null_combined)
            b1_percentile = compute_percentile_rank(topo["beta_1"], null_combined)
            b2_percentile = compute_percentile_rank(topo["beta_2"], null_combined)

            print(f"  Null bank comparison:")
            print(f"    β₀={topo['beta_0']} (null mean={null_combined.mean():.1f}±{null_combined.std():.1f}, "
                  f"percentile={b0_percentile:.1f}%)")
            print(f"    β₁={topo['beta_1']} (percentile={b1_percentile:.1f}%)")
            print(f"    β₂={topo['beta_2']} (percentile={b2_percentile:.1f}%)")

            results[name] = {
                "n_objects": n_obj,
                "topology": topo,
                "null_stats": {
                    "null_mean_b0": float(null_combined.mean()),
                    "null_std_b0": float(null_combined.std()),
                },
                "percentile_ranks": {
                    "beta_0": b0_percentile,
                    "beta_1": b1_percentile,
                    "beta_2": b2_percentile,
                },
                "label": "ENGINEERING",  # Not TEST/FIT (gate G1-L closed)
            }
        else:
            print(f"  ⚠ No null bank for {name}")
            results[name] = {
                "n_objects": n_obj,
                "topology": topo,
                "label": "ENGINEERING",
                "note": "No null bank for comparison",
            }

        print()

    # Save results
    output_file = OUTPUT_DIR / "topology_results_2026_07_25.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    # Compute checksum
    with open(output_file, 'rb') as f:
        file_sha = hashlib.sha256(f.read()).hexdigest()

    print("=" * 80)
    print(f"Results saved to: {output_file}")
    print(f"SHA256: {file_sha}\n")

    # Write report
    report_file = OUTPUT_DIR / "TOPOLOGY_RESULTS_REPORT_2026_07_25.txt"
    with open(report_file, 'w') as f:
        f.write("Real-Data Topology Analysis Report\n")
        f.write("=" * 80 + "\n")
        f.write(f"Date: {datetime.now().isoformat()}\n")
        f.write(f"Label: ENGINEERING (no TEST/FIT; gate G1-L closed)\n")
        f.write(f"Configuration: nbins={NBINS}, threshold={THRESHOLD_PERCENTILE}%\n")
        f.write(f"Output SHA256: {file_sha}\n\n")

        for name, result in results.items():
            f.write(f"\n{name}:\n")
            f.write(f"  Objects: {result['n_objects']}\n")
            f.write(f"  β₀ = {result['topology']['beta_0']}\n")
            f.write(f"  β₁ = {result['topology']['beta_1']}\n")
            f.write(f"  β₂ = {result['topology']['beta_2']}\n")
            f.write(f"  χ  = {result['topology']['euler_char']}\n")

            if "percentile_ranks" in result:
                f.write(f"  Percentile ranks (vs. null bank):\n")
                f.write(f"    β₀: {result['percentile_ranks']['beta_0']:.1f}%\n")
                f.write(f"    β₁: {result['percentile_ranks']['beta_1']:.1f}%\n")
                f.write(f"    β₂: {result['percentile_ranks']['beta_2']:.1f}%\n")

    print(f"Report: {report_file}\n")

    # Print summary
    print("Summary:")
    for name, result in results.items():
        print(f"  {name}: β₀={result['topology']['beta_0']}, "
              f"β₁={result['topology']['beta_1']}, "
              f"β₂={result['topology']['beta_2']}")

    print(f"\n✅ All results labeled ENGINEERING (not TEST/FIT)")
    print(f"✅ Full provenance: {output_file}")

    return 0


if __name__ == "__main__":
    sys.exit(run_topology_analysis())
