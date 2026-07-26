#!/usr/bin/env python3
"""WP-E2: Mass-preserving void-to-filament deformation operator.

This module implements a single deformation function for use in controlled-injection
detectability sweeps on synthetic density fields. The deformation is mass-preserving
by construction: it redistributes density from local minima toward local maxima at
a characteristic scale, without creating or destroying mass.

Used by: scripts/run_synthetic_detectability_sweep.py (WP-E2)
"""
import numpy as np
from scipy import ndimage


def void_to_filament_deformation(field: np.ndarray, R_voxels: float, amplitude: float) -> np.ndarray:
    """Mass-preserving density redistribution from voids to filaments.

    Pushes density from local minima toward local maxima at characteristic scale
    `R_voxels`, with controllable amplitude. Implementation:

    1. Smooth the field at scale R_voxels using a Gaussian filter.
    2. Compute local contrast as field minus its smoothed version (positive where
       field exceeds its local average).
    3. Deform by adding amplitude times the contrast to the original field.
    4. Clip to non-negative values (density cannot be negative).
    5. Renormalize to preserve the total mass exactly (guard against zero sum).

    This ensures:
    - amplitude=0.0 returns the input field exactly (identity operation).
    - Total mass is preserved to float64 tolerance for all (R, amplitude).
    - Deterministic: no RNG anywhere in this function.
    - float64 throughout (critical to avoid float32 artifacts per WP-E findings).

    Parameters
    ----------
    field : np.ndarray
        3D or lower-dimensional density field (must be non-negative). Converted
        to float64. Any NaN or inf values will propagate into the output.
    R_voxels : float
        Gaussian filter sigma in voxel units. Controls the characteristic scale
        of the deformation. Must be non-negative.
    amplitude : float
        Strength of the deformation, dimensionless. amplitude=0 → identity.
        Positive amplitude pushes density from minima to maxima; negative
        amplitude does the reverse (both are valid transformations).

    Returns
    -------
    np.ndarray
        Deformed field with the same shape and dtype (float64) as the input.
        Total mass preserved exactly (up to float64 rounding).

    Notes
    -----
    The deformation is symmetric: it treats the smooth field as a local baseline,
    then boosts (or suppresses) values based on their deviation from that baseline.
    This naturally concentrates mass in overdense regions and depletes voids,
    making it suitable for testing whether the null schemes can detect such a
    known-present, controlled deformation.
    """
    field = np.asarray(field, dtype=np.float64)
    original_mass = float(np.sum(field))

    # Step 1: Smooth the field at scale R_voxels
    smooth = ndimage.gaussian_filter(field, sigma=R_voxels, mode="nearest")

    # Step 2: Compute local contrast (positive where field > local average)
    contrast = field - smooth

    # Step 3: Deform by adding amplitude * contrast
    deformed = field + amplitude * contrast

    # Step 4: Clip to non-negative
    deformed = np.clip(deformed, 0.0, None)

    # Step 5: Renormalize to preserve total mass exactly
    deformed_mass = float(np.sum(deformed))
    if deformed_mass > 0.0:
        # Guard against zero mass: if amplitude and contrast combine to zero out
        # the field entirely, preserve that result (don't divide by zero).
        deformed = deformed * (original_mass / deformed_mass)
    else:
        # If deformation resulted in zero mass, return a uniform field at the
        # original mean density. This is the only sensible fallback and is
        # extremely rare (would require amplitude and contrast to exactly cancel
        # everywhere after clipping).
        if original_mass > 0.0:
            cell_count = float(field.size)
            deformed = np.full_like(field, original_mass / cell_count)
        # else: original field was zero; deformed remains zero.

    return deformed


# Generated-by: Haiku 4.5 | Verified-by: pipeline/tests/test_deformation.py
# (identity, mass preservation, determinism, monotonicity, float64, smoke test, labeling) |
# Reviewed-by: pending T0
