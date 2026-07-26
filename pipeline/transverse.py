#!/usr/bin/env python3
"""2D transverse topology analysis for photo-z fields.

WP-E revised protocol (T0 directive 2026-07-26): photo-z fields lack radial
resolution (sigma_z ~ 0.05(1+z) projects to ~100-200 Mpc comoving; a voxel
at nbins=8 is ~1 Gpc — see docs/WP_E3_REALDATA_THIRD_SCHEME_2026_07_26.md §5.1).
Topology is computed on 2D transverse slices at fixed redshift dz intervals,
with explicit control over dz and closed-system coordinates.

This module provides slice selection, projection, extent measurement,
resolvability checks, and mock generation for WP-E Phase 0–3 (preflight,
closure+null, sweep).
"""
import numpy as np
from typing import Tuple, Optional
from pipeline.realfield import density_field_from_catalog
from pipeline.cosmology import radec_z_to_tangent_plane_mpc


def select_slice(z: np.ndarray, z_lo: float, dz: float) -> np.ndarray:
    """Boolean mask for redshift slice [z_lo, z_lo + dz).

    Parameters
    ----------
    z : np.ndarray
        Redshift array.
    z_lo : float
        Lower edge of slice (inclusive).
    dz : float
        Slice thickness (exclusive upper edge).

    Returns
    -------
    mask : np.ndarray
        Boolean array where True indicates (z >= z_lo) & (z < z_lo + dz).
    """
    z = np.asarray(z, dtype=np.float64)
    return (z >= z_lo) & (z < z_lo + dz)


def project_slice_2d(
    ra: np.ndarray,
    dec: np.ndarray,
    mask: np.ndarray,
    nbins: int,
    ranges: Optional[Tuple[Tuple[float, float], Tuple[float, float]]] = None,
) -> np.ndarray:
    """2D binned density field from a masked catalog slice.

    Uses density_field_from_catalog with z=None (2D mode). If ranges is not
    given, computed from the full (ra, dec) arrays before masking — ensures
    all slices of the same catalog share an identical grid.

    Parameters
    ----------
    ra, dec : np.ndarray
        Sky coordinates in degrees.
    mask : np.ndarray
        Boolean array selecting objects in the slice.
    nbins : int
        Number of bins per axis (e.g., 32 → 32×32 field).
    ranges : tuple, optional
        ((ra_min, ra_max), (dec_min, dec_max)) in degrees.
        If None, computed from the full ra/dec extent.

    Returns
    -------
    field : np.ndarray
        2D density field (nbins × nbins), normalized to mean 1.0.
    """
    ra = np.asarray(ra, dtype=np.float64)
    dec = np.asarray(dec, dtype=np.float64)
    mask = np.asarray(mask, dtype=bool)

    # If ranges not given, use full extent of unmasked data
    if ranges is None:
        ra_range = (float(ra.min()), float(ra.max()))
        dec_range = (float(dec.min()), float(dec.max()))
        ranges = (ra_range, dec_range)

    # Extract masked slice
    ra_slice = ra[mask]
    dec_slice = dec[mask]

    # Call density_field_from_catalog with z=None for 2D mode
    field = density_field_from_catalog(
        ra_slice,
        dec_slice,
        z=None,
        nbins=nbins,
        ra_range=ranges[0],
        dec_range=ranges[1],
    )
    return field


def transverse_extent_mpc(
    ra: np.ndarray,
    dec: np.ndarray,
    z: np.ndarray,
    z_mid: float,
) -> Tuple[float, float]:
    """Transverse extent of (RA, Dec, z) catalog in comoving Mpc at fixed z.

    Computes the angular extent of the (RA, Dec) coordinates and converts to
    transverse Mpc at the redshift z_mid using the small-angle tangent-plane
    approximation.

    Returns (extent_ra_mpc, extent_dec_mpc) — physical transverse sizes in Mpc.

    Parameters
    ----------
    ra, dec : np.ndarray
        Sky coordinates in degrees.
    z : np.ndarray
        Redshift array (used to identify the slice centroid).
    z_mid : float
        Central redshift of the slice (the z-value at which extents are measured).

    Returns
    -------
    extent_ra_mpc, extent_dec_mpc : tuple of float
        Field extent in transverse directions (Mpc).
    """
    ra = np.asarray(ra, dtype=np.float64)
    dec = np.asarray(dec, dtype=np.float64)

    ra_extent_deg = float(ra.max() - ra.min())
    dec_extent_deg = float(dec.max() - dec.min())

    # Convert to transverse Mpc at z_mid using tangent-plane geometry.
    # Small angle: x ~ r * theta (in radians), r is comoving distance.
    # Use the cosmology module's tangent-plane function on corner points
    # to measure physical extent.
    from pipeline.cosmology import radec_z_to_tangent_plane_mpc

    # Measure from RA/Dec centroid at four corners of the extent
    ra_min, ra_max = ra.min(), ra.max()
    dec_min, dec_max = dec.min(), dec.max()
    z_arr = np.full(4, z_mid, dtype=np.float64)

    # Four corners
    corners_ra = np.array([ra_min, ra_max, ra_min, ra_max])
    corners_dec = np.array([dec_min, dec_max, dec_min, dec_max])

    tx, ty, _ = radec_z_to_tangent_plane_mpc(corners_ra, corners_dec, z_arr)

    # Extent is the difference between max and min transverse coordinates
    extent_ra_mpc = float(tx.max() - tx.min())
    extent_dec_mpc = float(ty.max() - ty.min())

    return extent_ra_mpc, extent_dec_mpc


def resolvable_2d(
    scale_mpc: float,
    extent_mpc_2d: Tuple[float, float],
    nbins: int,
    min_voxels: float = 1.0,
) -> dict:
    """2D resolvability check: can a deformation scale be measured?

    Arithmetic guard against sub-voxel deformations. For a scale to be
    resolvable, it must span >= min_voxels on both transverse axes.

    Parameters
    ----------
    scale_mpc : float
        Deformation scale in Mpc.
    extent_mpc_2d : tuple of float
        (extent_x, extent_y) of the 2D field in Mpc.
    nbins : int
        Number of bins per axis.
    min_voxels : float, optional
        Minimum voxels the scale must span (default 1.0).

    Returns
    -------
    dict
        Keys:
        - 'scale_mpc': input scale
        - 'nbins': input bins per axis
        - 'voxel_size_mpc': (voxel_x, voxel_y) in Mpc
        - 'scale_in_voxels': (scale_x, scale_y)
        - 'resolvable_per_axis': (bool, bool) for (x, y)
        - 'verdict': "UNRESOLVABLE", "PARTIALLY_RESOLVABLE", or "RESOLVABLE"
        - 'note': plain-language explanation
    """
    scale_mpc = float(scale_mpc)
    extent_mpc_2d = tuple(float(e) for e in extent_mpc_2d)
    nbins = int(nbins)
    min_voxels = float(min_voxels)

    if nbins <= 0:
        raise ValueError(f"resolvable_2d needs nbins >= 1, got {nbins}")

    voxel_x = extent_mpc_2d[0] / nbins
    voxel_y = extent_mpc_2d[1] / nbins

    # Fail CLOSED on a degenerate field. A zero (or negative) extent means the
    # slice has no spatial extent on that axis; dividing by it would give inf,
    # and inf >= min_voxels would report the most permissive verdict for the
    # most degenerate input. This function is the mandatory pre-statistics guard
    # (E2.16), so it must refuse rather than wave through. (WP-E5 audit A-8.)
    if voxel_x <= 0.0 or voxel_y <= 0.0:
        return {
            "scale_mpc": scale_mpc,
            "nbins": nbins,
            "voxel_size_mpc": (voxel_x, voxel_y),
            "scale_in_voxels": (float("nan"), float("nan")),
            "resolvable_per_axis": (False, False),
            "verdict": "UNRESOLVABLE",
            "note": (
                f"Degenerate field: extent {extent_mpc_2d} Mpc gives a non-positive "
                f"voxel edge on at least one axis; no scale is measurable."
            ),
        }

    scale_in_voxels_x = scale_mpc / voxel_x
    scale_in_voxels_y = scale_mpc / voxel_y

    resolvable_x = scale_in_voxels_x >= min_voxels
    resolvable_y = scale_in_voxels_y >= min_voxels

    n_resolvable = int(resolvable_x) + int(resolvable_y)

    if n_resolvable == 0:
        verdict = "UNRESOLVABLE"
        note = f"Scale {scale_mpc:.2f} Mpc < {min_voxels} voxels on both axes; cannot move binned field."
    elif n_resolvable == 2:
        verdict = "RESOLVABLE"
        note = f"Scale {scale_mpc:.2f} Mpc spans >= {min_voxels} voxels on both axes."
    else:
        verdict = "PARTIALLY_RESOLVABLE"
        note = f"Scale {scale_mpc:.2f} Mpc is resolvable on {n_resolvable}/2 axes."

    return {
        "scale_mpc": scale_mpc,
        "nbins": nbins,
        "voxel_size_mpc": (voxel_x, voxel_y),
        "scale_in_voxels": (scale_in_voxels_x, scale_in_voxels_y),
        "resolvable_per_axis": (resolvable_x, resolvable_y),
        "verdict": verdict,
        "note": note,
    }


def generate_mock_slice(
    n_objects: int,
    ra_range: Tuple[float, float],
    dec_range: Tuple[float, float],
    seed: int,
    n_clusters: int = 4,
    clustered_fraction: float = 0.7,
) -> Tuple[np.ndarray, np.ndarray]:
    """Generate a synthetic 2D mock catalog slice with controlled clustering.

    Creates n_objects distributed as a mixture:
    - clustered_fraction of objects: Gaussian scatter around n_clusters random centers
    - (1 - clustered_fraction) of objects: uniform random within the box

    Deterministic per seed (uses np.random.default_rng).

    Parameters
    ----------
    n_objects : int
        Total number of mock objects.
    ra_range : tuple of float
        (ra_min, ra_max) in degrees.
    dec_range : tuple of float
        (dec_min, dec_max) in degrees.
    seed : int
        RNG seed for determinism.
    n_clusters : int, optional
        Number of cluster centers (default 4).
    clustered_fraction : float, optional
        Fraction of objects placed near clusters (default 0.7).

    Returns
    -------
    ra, dec : tuple of np.ndarray
        Mock RA and Dec coordinates, shape (n_objects,), dtype float64.
    """
    rng = np.random.default_rng(seed)

    ra_min, ra_max = float(ra_range[0]), float(ra_range[1])
    dec_min, dec_max = float(dec_range[0]), float(dec_range[1])
    ra_width = ra_max - ra_min
    dec_width = dec_max - dec_min

    # Cluster centers: uniform in the box
    cluster_ra = rng.uniform(ra_min, ra_max, n_clusters)
    cluster_dec = rng.uniform(dec_min, dec_max, n_clusters)

    n_clustered = int(np.round(n_objects * clustered_fraction))
    n_uniform = n_objects - n_clustered

    ra_out = np.zeros(n_objects, dtype=np.float64)
    dec_out = np.zeros(n_objects, dtype=np.float64)

    # Clustered objects: Gaussian scatter (2% of width as sigma) around random centers
    sigma_ra = 0.02 * ra_width
    sigma_dec = 0.02 * dec_width
    for i in range(n_clustered):
        cluster_idx = rng.integers(0, n_clusters)
        ra_out[i] = rng.normal(cluster_ra[cluster_idx], sigma_ra)
        dec_out[i] = rng.normal(cluster_dec[cluster_idx], sigma_dec)

    # Uniform background
    ra_out[n_clustered:] = rng.uniform(ra_min, ra_max, n_uniform)
    dec_out[n_clustered:] = rng.uniform(dec_min, dec_max, n_uniform)

    # Clip to range (Gaussian-scattered points may exceed boundaries)
    ra_out = np.clip(ra_out, ra_min, ra_max)
    dec_out = np.clip(dec_out, dec_min, dec_max)

    return ra_out, dec_out


# Generated-by: Haiku 4.5 | Verified-by: pipeline/tests/test_transverse.py |
# Reviewed-by: pending T0
