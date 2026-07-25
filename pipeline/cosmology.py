#!/usr/bin/env python3
"""WP-R5: (RA, Dec, z) -> comoving Cartesian coordinates.

Cosmology: astropy.cosmology.Planck18 — Planck Collaboration 2018/2020, A&A,
641, A6 (Paper VI), Table 2 (TT,TE,EE+lowE+lensing+BAO column). Concretely:
H0 = 67.66 km/s/Mpc, Om0 = 0.30966, flat ΛCDM. Source cited in astropy's own
docstring for `astropy.cosmology.Planck18`; not retyped from memory here.

**This cosmology is a FREE INPUT to this pipeline, not a prediction.** Every
comoving distance, and therefore every density field and topology number
built from it, changes if this choice changes. No claim in this repo treats
these coordinates as validating or testing any cosmological model — they are
plumbing to turn angles + redshift into a Cartesian grid.

Coordinate convention: standard comoving Cartesian with x toward (RA=0,Dec=0),
y toward (RA=90 deg,Dec=0), z toward the north celestial pole (Dec=90 deg),
scaled by the astropy comoving distance D_C(z) in Mpc.
"""
import numpy as np
from astropy.cosmology import Planck18
from astropy import units as u


def comoving_distance_mpc(z: np.ndarray) -> np.ndarray:
    """Comoving distance in Mpc for redshift(s) z, using Planck18.

    Thin wrapper for traceability: every caller in this module goes through
    here so the cosmology choice is in exactly one place.
    """
    z = np.asarray(z, dtype=np.float64)
    return Planck18.comoving_distance(z).to(u.Mpc).value


def radec_z_to_cartesian_mpc(
    ra_deg: np.ndarray,
    dec_deg: np.ndarray,
    z: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Convert (RA, Dec, z) to comoving Cartesian (x, y, z_cart) in Mpc.

    Parameters
    ----------
    ra_deg, dec_deg : array-like
        Right ascension, declination in degrees.
    z : array-like
        Redshift (spectroscopic or photometric point estimate).

    Returns
    -------
    x, y, z_cart : ndarray
        Comoving Cartesian coordinates in Mpc.

    Notes
    -----
    Objects with non-finite or negative z are NOT silently dropped here —
    callers must filter before calling (see `drop_invalid_redshifts`), so
    that every drop is counted and reported, never imputed.
    """
    ra = np.asarray(ra_deg, dtype=np.float64)
    dec = np.asarray(dec_deg, dtype=np.float64)
    z = np.asarray(z, dtype=np.float64)

    if np.any(~np.isfinite(z)) or np.any(z < 0):
        raise ValueError(
            "radec_z_to_cartesian_mpc received non-finite or negative z; "
            "filter with drop_invalid_redshifts() first so drops are counted."
        )

    d_c = comoving_distance_mpc(z)

    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)

    x = d_c * np.cos(dec_rad) * np.cos(ra_rad)
    y = d_c * np.cos(dec_rad) * np.sin(ra_rad)
    z_cart = d_c * np.sin(dec_rad)

    return x, y, z_cart


def radec_z_to_tangent_plane_mpc(
    ra_deg: np.ndarray,
    dec_deg: np.ndarray,
    z: np.ndarray,
    ra0_deg: float | None = None,
    dec0_deg: float | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Convert (RA, Dec, z) to (transverse_x, transverse_y, radial_r) in Mpc
    using a small-angle tangent-plane projection around a field centre.

    Why this exists (not just global Cartesian): a narrow pencil-beam survey
    cone (few-arcmin to ~0.2 deg radius, but Gpc-scale radial depth) embeds
    into GLOBAL axis-aligned Cartesian coordinates as a thin diagonal sliver
    inside a bounding box whose volume is dominated by empty corners — most
    bins in any reasonable grid are empty regardless of true structure. The
    tangent-plane + radial-distance frame instead aligns the grid with the
    survey's actual footprint, so bins are populated efficiently. This is a
    standard technique in large-scale-structure pipelines for deep, narrow
    fields (e.g. BAO/void analyses of pencil-beam surveys).

    Parameters
    ----------
    ra_deg, dec_deg, z : array-like
        Sky position and redshift.
    ra0_deg, dec0_deg : float, optional
        Tangent-plane centre. Defaults to the (RA, Dec) centroid of the input.

    Returns
    -------
    transverse_x, transverse_y, radial_r : ndarray
        transverse_x = r * (ra - ra0) * cos(dec0)   [Mpc, small-angle]
        transverse_y = r * (dec - dec0)             [Mpc, small-angle]
        radial_r = comoving_distance(z)              [Mpc]
        (ra, dec differences in radians before scaling by r)

    Notes
    -----
    Small-angle approximation is excellent for cone half-angles well under a
    few degrees (error ~ theta^2/6, i.e. <0.1% at 0.2 deg); not intended for
    wide-field (tens of degrees) surveys.
    """
    ra = np.asarray(ra_deg, dtype=np.float64)
    dec = np.asarray(dec_deg, dtype=np.float64)
    z = np.asarray(z, dtype=np.float64)

    if np.any(~np.isfinite(z)) or np.any(z < 0):
        raise ValueError(
            "radec_z_to_tangent_plane_mpc received non-finite or negative z; "
            "filter with drop_invalid_redshifts() first so drops are counted."
        )

    if ra0_deg is None:
        ra0_deg = float(np.mean(ra))
    if dec0_deg is None:
        dec0_deg = float(np.mean(dec))

    dec0_rad = np.radians(dec0_deg)
    d_ra_rad = np.radians(ra - ra0_deg)
    d_dec_rad = np.radians(dec - dec0_deg)

    r = comoving_distance_mpc(z)

    transverse_x = r * d_ra_rad * np.cos(dec0_rad)
    transverse_y = r * d_dec_rad

    return transverse_x, transverse_y, r


def drop_invalid_redshifts(
    ra_deg: np.ndarray,
    dec_deg: np.ndarray,
    z: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict]:
    """Filter out non-finite / negative redshifts; NEVER impute.

    Photo-z columns from survey joins (e.g. Euclid phz_median) can carry NaN
    for objects the pipeline could not fit. WP-R5's rule: such objects are
    dropped and the count reported, never filled with a guessed value.

    Returns
    -------
    ra_valid, dec_valid, z_valid : ndarray
        Filtered arrays.
    report : dict
        {"n_input": int, "n_valid": int, "n_dropped": int,
         "n_dropped_nan": int, "n_dropped_negative": int}
    """
    ra = np.asarray(ra_deg, dtype=np.float64)
    dec = np.asarray(dec_deg, dtype=np.float64)
    z = np.asarray(z, dtype=np.float64)

    n_input = len(z)
    is_nan = ~np.isfinite(z)
    is_negative = np.isfinite(z) & (z < 0)
    is_valid = np.isfinite(z) & (z >= 0)

    report = {
        "n_input": int(n_input),
        "n_valid": int(is_valid.sum()),
        "n_dropped": int(n_input - is_valid.sum()),
        "n_dropped_nan": int(is_nan.sum()),
        "n_dropped_negative": int(is_negative.sum()),
    }

    return ra[is_valid], dec[is_valid], z[is_valid], report


# Generated-by: Claude Sonnet 5 | Verified-by: pipeline/tests/test_cosmology.py
# (two independent comoving-distance references) | Reviewed-by: T0 Y (Fable 5,
# 2026-07-25, docs/T0_SIGNOFF_WP_R5_R6_R7_2026_07_25.md)
