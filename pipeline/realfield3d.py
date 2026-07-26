#!/usr/bin/env python3
"""WP-R5: Genuine 3D comoving density field + valid randomization nulls.

Two things this module provides that pipeline/realfield.py (WP-R2) does not:

1. `density_field_cartesian_mpc`: bins a real 3D density field on a regular
   Cartesian *comoving-Mpc* grid (not degenerate ra/dec/z-index bins) — the
   "genuinely missing piece" WP-R5 targets.

2. Two methodologically VALID null schemes, replacing the degenerate WP-R3
   schemes (see docs/FINDING_R_NULLDEGENERATE_2026_07_25.md — WP-R3's
   "shuffle" permuted RA/Dec together, a no-op; its "rotate" applied a rigid
   rotation, an isometry that preserves all internal structure). Both bugs
   share one root cause: neither scheme changed the relative point pattern.
   These two schemes do:
     - z-shuffle: fix (RA, Dec), permute redshift assignment across objects
       independently. Breaks radial-angular correlation.
     - angular CSR: fix redshift per object, redraw (RA, Dec) uniformly at
       random within the catalog's observed angular bounding box. Breaks
       angular clustering at fixed radial slicing.
"""
import numpy as np
from typing import Optional, Tuple

from pipeline.cosmology import radec_z_to_cartesian_mpc


def density_field_cartesian_mpc(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    nbins: int = 16,
    ranges: Optional[Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]] = None,
) -> np.ndarray:
    """Plain 3D histogram density field in comoving Cartesian Mpc.

    No smoothing, no kernels. Normalized to mean 1.0. `ranges`, if given, fixes
    the bin extents (needed so a real field and its null realizations share an
    identical grid — otherwise each realization's auto-ranged extent would
    silently change the effective bin volume).
    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    z = np.asarray(z, dtype=np.float64)

    if len(x) == 0:
        return np.ones((nbins, nbins, nbins), dtype=np.float64)

    if ranges is None:
        ranges = ((x.min(), x.max()), (y.min(), y.max()), (z.min(), z.max()))

    field, _ = np.histogramdd(
        np.column_stack([x, y, z]), bins=[nbins, nbins, nbins], range=list(ranges)
    )

    mean_count = field.mean()
    if mean_count > 0:
        field = field / mean_count
    else:
        field = np.ones_like(field)

    return field


def z_shuffle_realization(
    ra: np.ndarray, dec: np.ndarray, z: np.ndarray, rng: np.random.Generator
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Fix (RA, Dec); independently permute z across objects.

    Breaks any real radial-angular correlation. Genuinely different point set
    per call (unlike WP-R3's degenerate co-permutation).
    """
    z_perm = rng.permutation(z)
    return ra.copy(), dec.copy(), z_perm


def angular_csr_realization(
    ra: np.ndarray, dec: np.ndarray, z: np.ndarray, rng: np.random.Generator
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Fix z per object; redraw (RA, Dec) uniformly within the observed
    angular bounding box (complete spatial randomness at fixed radial
    slicing).

    Dec is drawn uniform in sin(dec) between the data's sin(dec) extremes,
    which is the correct measure for uniform angular density (not uniform in
    dec itself, which would over-sample the poles).
    """
    n = len(ra)
    ra_min, ra_max = ra.min(), ra.max()
    sin_dec_min, sin_dec_max = np.sin(np.radians(dec)).min(), np.sin(np.radians(dec)).max()

    ra_random = rng.uniform(ra_min, ra_max, size=n)
    sin_dec_random = rng.uniform(sin_dec_min, sin_dec_max, size=n)
    dec_random = np.degrees(np.arcsin(sin_dec_random))

    return ra_random, dec_random, z.copy()


def density_shuffle_realization(field: np.ndarray, seed: int) -> np.ndarray:
    """Permute cell values across a binned density field (voxel shuffle).

    Takes an already-binned density field (2D or 3D), flattens it, randomly
    permutes the cell values (preserving the exact multiset), and reshapes
    back to the original shape. This randomization scheme tests whether a
    topology statistic (e.g., Betti numbers) depends on the spatial
    arrangement of values vs. only on the value distribution.

    The scheme is valid because it breaks spatial correlations while exactly
    preserving the marginal distribution (histogram of cell values), so any
    topological change across realizations reflects the role of arrangement.

    Args:
        field: Binned density field, 2D or 3D numpy array (output of
               density_field_cartesian_mpc or similar).
        seed: Random seed for reproducibility.

    Returns:
        Shuffled field with identical shape and multiset of values.
    """
    field = np.asarray(field, dtype=np.float64)
    original_shape = field.shape
    flat = field.flatten()
    rng = np.random.default_rng(seed)
    flat_shuffled = rng.permutation(flat)
    return flat_shuffled.reshape(original_shape)


# Generated-by: Claude Sonnet 5 (z-shuffle, angular-csr) + Haiku 4.5 (density-shuffle) |
# Verified-by: pipeline/tests/test_realfield3d.py (nonzero-variance check + Euler identity)
# + pipeline/tests/test_density_shuffle_golden.py (conservation + determinism + integration) |
# Reviewed-by: T0 Y for z-shuffle/angular-csr only (Fable 5, 2026-07-25,
# docs/T0_SIGNOFF_WP_R5_R6_R7_2026_07_25.md) — density_shuffle_realization (2026-07-26)
# is NOT covered by that sign-off; pending T0 review
