#!/usr/bin/env python3
"""Engineering-only synthetic point catalog generator (RA, Dec, z).

This module generates mock catalogs of (RA, Dec, z) objects for testing the
null-randomization infrastructure (pipeline/realfield3d.py) on controlled,
fully-synthetic data — no real cosmological simulation or observational claims.

The generator produces a two-population model: cluster cores (objects with
small-scatter spatial clustering around cluster centers) plus uniform background.
This is sufficient to inject detectable structure for the topology pipeline to
work on, without claims about realistic large-scale structure.

**ENGINEERING ONLY.** This is test/infrastructure code. No predictions, no real
data, no cosmological claims. Labeled SYNTHETIC in all outputs.
"""
import numpy as np
from typing import Optional


def generate_mock_catalog(
    n_objects: int,
    n_clusters: int,
    seed: int,
    ra_range: tuple = (150.0, 160.0),
    dec_range: tuple = (0.0, 10.0),
    z_range: tuple = (0.5, 0.7),
) -> dict:
    """Generate a synthetic mock catalog (RA, Dec, z) with injected clustering.

    Two-population model: ~70% of objects cluster around `n_clusters` random
    cluster centers with Gaussian scatter; ~30% uniformly distributed background.
    All coordinates clipped/wrapped to stay within the stated ranges.

    Parameters
    ----------
    n_objects : int
        Total number of objects in the catalog.
    n_clusters : int
        Number of random cluster centers to place.
    seed : int
        Random seed for reproducibility. Identical seed → identical catalog.
    ra_range : tuple of float
        (RA_min, RA_max) in degrees. Default (150°, 160°) covers 10° in RA.
    dec_range : tuple of float
        (Dec_min, Dec_max) in degrees. Default (0°, 10°) covers 10° in Dec.
    z_range : tuple of float
        (z_min, z_max) redshift range. Default (0.5, 0.7).

    Returns
    -------
    dict
        {"ra": np.ndarray, "dec": np.ndarray, "z": np.ndarray}
        Each array has length `n_objects`, dtype float64.

    Notes
    -----
    **ENGINEERING ONLY SYNTHETIC DATA.** No cosmological claims. This is
    infrastructure testing for the null-randomization pipeline. The model
    parameters (70/30 split, Gaussian scatter width, cluster placement) are
    arbitrary engineering choices and will be reset if this code is ever used
    outside its test scope.

    Determinism: identical (n_objects, n_clusters, seed, ranges) → bit-identical
    output via np.random.default_rng (never bare np.random). This is essential
    for reproducible null hypothesis tests.
    """
    rng = np.random.default_rng(seed)

    ra_min, ra_max = ra_range
    dec_min, dec_max = dec_range
    z_min, z_max = z_range

    # Draw cluster centers uniformly within the box
    cluster_centers_ra = rng.uniform(ra_min, ra_max, size=n_clusters)
    cluster_centers_dec = rng.uniform(dec_min, dec_max, size=n_clusters)
    cluster_centers_z = rng.uniform(z_min, z_max, size=n_clusters)

    # Allocate objects: ~70% clustered, ~30% background
    n_clustered = int(0.7 * n_objects)
    n_background = n_objects - n_clustered

    ra = np.zeros(n_objects, dtype=np.float64)
    dec = np.zeros(n_objects, dtype=np.float64)
    z = np.zeros(n_objects, dtype=np.float64)

    # Clustered objects: assign each to a random cluster, add Gaussian scatter
    cluster_indices = rng.integers(0, n_clusters, size=n_clustered)
    ra_scatter_scale = (ra_max - ra_min) * 0.02  # 2% of the RA range
    dec_scatter_scale = (dec_max - dec_min) * 0.02  # 2% of the Dec range
    z_scatter_scale = (z_max - z_min) * 0.02  # 2% of the z range

    for i in range(n_clustered):
        cluster_idx = cluster_indices[i]
        ra[i] = cluster_centers_ra[cluster_idx] + rng.normal(0, ra_scatter_scale)
        dec[i] = cluster_centers_dec[cluster_idx] + rng.normal(0, dec_scatter_scale)
        z[i] = cluster_centers_z[cluster_idx] + rng.normal(0, z_scatter_scale)

    # Background objects: uniform throughout the box
    ra[n_clustered:] = rng.uniform(ra_min, ra_max, size=n_background)
    dec[n_clustered:] = rng.uniform(dec_min, dec_max, size=n_background)
    z[n_clustered:] = rng.uniform(z_min, z_max, size=n_background)

    # Clip to ensure all coordinates stay within bounds
    ra = np.clip(ra, ra_min, ra_max)
    dec = np.clip(dec, dec_min, dec_max)
    z = np.clip(z, z_min, z_max)

    return {
        "ra": ra,
        "dec": dec,
        "z": z,
    }


# Generated-by: Haiku 4.5 | Verified-by: pipeline/tests/test_synthetic_null_report.py
# (determinism, catalog structure) | Reviewed-by: pending T0
