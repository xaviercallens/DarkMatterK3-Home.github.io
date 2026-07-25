#!/usr/bin/env python3
"""WP-R2: Real-derived density fields from catalog data.

Constructs a simple binned density field from (RA, Dec) or (RA, Dec, z)
catalog positions. No smoothing, no tuned constants — just histogram-based
binning on a regular grid, normalized to mean 1.

CRITICAL: This is engineering-only. The binning choice is a free parameter,
so any statistic derived from it carries no physical meaning until paired with
a null bank and explicit hypothesis test at gate G1-L.

Pre-G1 use: validate that topology machinery works on real data and survives
survey geometry / mask / non-uniform sampling (WP-R2 smoke test).
"""

import numpy as np
from typing import Tuple, Optional


def density_field_from_catalog(
    ra: np.ndarray,
    dec: np.ndarray,
    z: Optional[np.ndarray] = None,
    nbins: int = 32,
    ra_range: Optional[Tuple[float, float]] = None,
    dec_range: Optional[Tuple[float, float]] = None,
    z_range: Optional[Tuple[float, float]] = None,
) -> np.ndarray:
    """Construct a regular-grid binned density field from catalog coordinates.

    Parameters
    ----------
    ra, dec : array-like
        Right ascension and declination in degrees.
    z : array-like, optional
        Redshift (for 3D field). If None, 2D field is returned.
    nbins : int
        Number of bins per dimension (default 32 → 32×32 or 32×32×32).
    ra_range, dec_range, z_range : tuple, optional
        Bin ranges (min, max). If None, use data extremes.

    Returns
    -------
    field : ndarray
        Density field (2D or 3D) normalized to mean 1.0. Each cell is the count
        of objects in that bin divided by the mean count (so uniform random
        distribution has mean 1 everywhere).

    Notes
    -----
    - No smoothing, no kernels, no tuned weights.
    - Binning choice is a free parameter; results are engineering-only until
      paired with an explicit hypothesis test (WP-G, post-G1-L).
    - The field is normalized to mean 1.0 to make Betti-number changes easy to
      interpret (a threshold percentile has an obvious meaning).
    """
    ra = np.asarray(ra, dtype=np.float64)
    dec = np.asarray(dec, dtype=np.float64)

    if z is None:
        # 2D field
        # Handle empty catalog
        if len(ra) == 0:
            return np.ones((nbins, nbins), dtype=np.float64)

        if ra_range is None:
            ra_range = (ra.min(), ra.max())
        if dec_range is None:
            dec_range = (dec.min(), dec.max())

        # Handle RA wrapping: if range spans >180°, assume it wraps at 360
        if (ra_range[1] - ra_range[0]) > 180:
            # Wrap everything to [0, 360) and re-center if needed
            ra_wrapped = np.where(ra < ra_range[0] + 180, ra, ra - 360)
            ra_range = (ra_wrapped.min(), ra_wrapped.max())
            ra = ra_wrapped

        field, ra_edges, dec_edges = np.histogram2d(
            dec, ra, bins=[nbins, nbins],
            range=[dec_range, ra_range]
        )
        # histogram2d returns (x, y) = (rows, cols), so transpose
        field = field.T

        # Normalize to mean 1
        mean_count = field.mean()
        if mean_count > 0:
            field = field / mean_count
        else:
            field = np.ones_like(field)

        return field

    else:
        # 3D field
        z = np.asarray(z, dtype=np.float64)
        if ra_range is None:
            ra_range = (ra.min(), ra.max())
        if dec_range is None:
            dec_range = (dec.min(), dec.max())
        if z_range is None:
            z_range = (z.min(), z.max())

        # RA wrapping for 3D as well
        if (ra_range[1] - ra_range[0]) > 180:
            ra_wrapped = np.where(ra < ra_range[0] + 180, ra, ra - 360)
            ra_range = (ra_wrapped.min(), ra_wrapped.max())
            ra = ra_wrapped

        field, edges = np.histogramdd(
            np.column_stack([dec, ra, z]),
            bins=[nbins, nbins, nbins],
            range=[dec_range, ra_range, z_range]
        )

        # Normalize to mean 1
        mean_count = field.mean()
        if mean_count > 0:
            field = field / mean_count
        else:
            field = np.ones_like(field)

        return field


# Generated-by: Haiku 4.5 | Verified-by: WP-R2 golden tests | Reviewed-by: [pending]
