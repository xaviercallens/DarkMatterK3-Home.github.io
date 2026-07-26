#!/usr/bin/env python3
"""Synthetic null-variance scan: testing null infrastructure on mock data.

Mirrors WP-R7 (docs/WP_R7_BETA_VARIANCE_SCAN.md) but operates entirely on
synthetic mock catalogs (pipeline/synthetic_catalog.py) rather than real data.
This is a **sanity check** that the null-randomization infrastructure works
sensibly before any real-data use, and a **template** for what a real report
would look like if the gate (G1) ever reopens.

ENGINEERING ONLY. No real data. All outputs labeled SYNTHETIC. No TEST/FIT
labels. Tests the machinery, not any hypothesis or prediction.

Reproduces the WP-R7 analysis structure:
- For each seed (independent mock catalog): bin into 3D field at multiple nbins
- Compute observed Betti numbers (β₀, β₁, β₂)
- For each null scheme (z-shuffle, angular-csr, density-shuffle):
  - Generate N null realizations
  - Compute Betti for each
  - Record: mean, std, and percentile of the observed value in the null dist
- Return and render nested results dict
"""
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

import numpy as np
from typing import Optional

from pipeline.synthetic_catalog import generate_mock_catalog
from pipeline.cosmology import radec_z_to_cartesian_mpc
from pipeline.realfield3d import (
    density_field_cartesian_mpc,
    z_shuffle_realization,
    angular_csr_realization,
    density_shuffle_realization,
)
from pipeline.observables_real import compute_betti_numbers


def run_synthetic_null_scan(
    n_objects: int = 2000,
    n_clusters: int = 5,
    seeds: Optional[list[int]] = None,
    nbins_list: Optional[list[int]] = None,
    n_null_trials: int = 30,
    threshold_percentile: float = 50.0,
) -> dict:
    """Run a full synthetic null-variance scan across multiple seeds/resolutions.

    For each seed: generate a mock catalog, bin at each nbins, compute observed
    topology and null distributions across three schemes (z-shuffle, angular-csr,
    density-shuffle). Percentiles are computed carefully: if null_std==0,
    percentile is None (never coerced to 0 or 100).

    Parameters
    ----------
    n_objects : int
        Number of objects per mock catalog. Default 2000.
    n_clusters : int
        Number of cluster cores per mock catalog. Default 5.
    seeds : list[int], optional
        Seeds for generating independent mock catalogs. Default [1, 2, 3].
    nbins_list : list[int], optional
        Resolution(s) to scan. Default [4, 8, 16] (matching WP-R7's emphasis
        on nbins=8 but spanning a range).
    n_null_trials : int
        Number of null realizations per scheme per (seed, nbins) combo.
        Default 30.
    threshold_percentile : float
        Density threshold for Betti computation. Default 50.0 (median).

    Returns
    -------
    dict
        Nested structure: {seed: {nbins: {statistic: {scheme: {
        "observed": int, "null_mean": float, "null_std": float,
        "percentile": float | None}}}}}.
        - "observed": the β value for the real field.
        - "null_mean", "null_std": mean and std of the null distribution.
        - "percentile": percentile rank of observed in null dist, or None if
          null_std == 0 (exact tie with all nulls).
    """
    if seeds is None:
        seeds = [1, 2, 3]
    if nbins_list is None:
        nbins_list = [4, 8, 16]

    results = {}

    for seed in seeds:
        seed_results = {}

        # Generate one mock catalog per seed
        catalog = generate_mock_catalog(
            n_objects=n_objects,
            n_clusters=n_clusters,
            seed=seed,
            ra_range=(150.0, 160.0),
            dec_range=(0.0, 10.0),
            z_range=(0.5, 0.7),
        )
        ra = catalog["ra"]
        dec = catalog["dec"]
        z = catalog["z"]

        # Convert to Cartesian
        x, y, z_cart = radec_z_to_cartesian_mpc(ra, dec, z)

        for nbins in nbins_list:
            nbins_results = {}

            # Compute field and ranges once per (seed, nbins)
            field = density_field_cartesian_mpc(x, y, z_cart, nbins=nbins)
            ranges = ((x.min(), x.max()), (y.min(), y.max()), (z_cart.min(), z_cart.max()))

            # Compute observed Betti numbers
            observed_topo = compute_betti_numbers(field, threshold_percentile=threshold_percentile)

            for stat in ("beta_0", "beta_1", "beta_2"):
                stat_results = {}
                obs_value = observed_topo[stat]

                for scheme in ("csr", "z_shuffle", "density_shuffle"):
                    if scheme == "density_shuffle":
                        # Density shuffle works directly on the binned field
                        null_values = []
                        for trial in range(n_null_trials):
                            trial_seed = seed * 1000 + trial
                            shuffled_field = density_shuffle_realization(field, seed=trial_seed)
                            null_topo = compute_betti_numbers(
                                shuffled_field, threshold_percentile=threshold_percentile
                            )
                            null_values.append(null_topo[stat])

                    else:
                        # CSR and z-shuffle work on the catalog, then rebin
                        null_values = []
                        rng = np.random.default_rng(seed)

                        for trial in range(n_null_trials):
                            if scheme == "csr":
                                ra_s, dec_s, z_s = angular_csr_realization(ra, dec, z, rng)
                            elif scheme == "z_shuffle":
                                ra_s, dec_s, z_s = z_shuffle_realization(ra, dec, z, rng)

                            x_s, y_s, z_cart_s = radec_z_to_cartesian_mpc(ra_s, dec_s, z_s)
                            field_s = density_field_cartesian_mpc(
                                x_s, y_s, z_cart_s, nbins=nbins, ranges=ranges
                            )
                            null_topo = compute_betti_numbers(
                                field_s, threshold_percentile=threshold_percentile
                            )
                            null_values.append(null_topo[stat])

                    null_values = np.array(null_values, dtype=np.float64)
                    null_mean = float(np.mean(null_values))
                    null_std = float(np.std(null_values))

                    # Percentile: rank of observed in null distribution
                    # If null_std == 0, percentile is None (no variance to rank against)
                    if null_std == 0:
                        percentile = None
                    else:
                        # Percentile using empirical CDF: fraction of nulls <= observed
                        percentile = float(np.mean(null_values <= obs_value) * 100.0)

                    stat_results[scheme] = {
                        "observed": int(obs_value),
                        "null_mean": null_mean,
                        "null_std": null_std,
                        "percentile": percentile,
                    }

                nbins_results[stat] = stat_results

            seed_results[nbins] = nbins_results

        results[seed] = seed_results

    return results


def render_report(results: dict) -> str:
    """Render the scan results as a markdown table.

    Mirrors WP-R7's report style but operates on synthetic data.
    """
    lines = []

    lines.append("# Synthetic Null-Variance Scan (SYNTHETIC Mock Data)")
    lines.append("")
    lines.append("**ALL VALUES IN THIS REPORT ARE SYNTHETIC MOCK DATA — NOT A CLAIM ABOUT ANY REAL SURVEY.**")
    lines.append("")
    lines.append("Engineering-only synthetic sanity check of the null-randomization infrastructure.")
    lines.append("")

    # For each seed
    for seed in sorted(results.keys()):
        seed_data = results[seed]
        lines.append(f"## Seed {seed}")
        lines.append("")

        # For each nbins
        for nbins in sorted(seed_data.keys()):
            nbins_data = seed_data[nbins]

            lines.append(f"### nbins={nbins}")
            lines.append("")

            # Build a table per statistic
            for stat in ("beta_0", "beta_1", "beta_2"):
                lines.append(f"#### {stat}")
                lines.append("")
                lines.append("| Scheme | Observed | Null Mean | Null Std | Percentile |")
                lines.append("|--------|----------|-----------|----------|------------|")

                schemes_data = nbins_data[stat]
                for scheme in ("csr", "z_shuffle", "density_shuffle"):
                    sch_results = schemes_data[scheme]
                    obs = sch_results["observed"]
                    n_mean = sch_results["null_mean"]
                    n_std = sch_results["null_std"]
                    perc = sch_results["percentile"]

                    perc_str = f"{perc:.1f}%" if perc is not None else "N/A (no variance)"

                    lines.append(
                        f"| {scheme:20s} | {obs:8d} | {n_mean:9.2f} | {n_std:8.2f} | {perc_str:10s} |"
                    )

                lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    print("Running synthetic null-variance scan...")
    results = run_synthetic_null_scan()

    report = render_report(results)
    print(report)

    # Write to docs/
    output_path = Path(__file__).parent.parent / "docs" / "SYNTHETIC_NULL_SCAN_REPORT.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(report)
    print(f"\nReport saved to {output_path}")


# Generated-by: Haiku 4.5 | Verified-by: pipeline/tests/test_synthetic_null_report.py
# (determinism, nonzero variance, None-percentile handling, labeling) |
# Reviewed-by: pending T0
