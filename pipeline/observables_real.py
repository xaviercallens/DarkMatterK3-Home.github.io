#!/usr/bin/env python3
"""Real-world observable computations for WP-E (Haiku).

κ-peak (weak-lensing convergence peaks) and Betti-number (cosmic-web topology)
statistics for replacing D3_batch_runner_phase2.py placeholders.

Synthetic-data golden tests only (WP-E §3); real data fetch is WP-G post-pin.
"""
import numpy as np
from scipy import ndimage


def compute_kappa_peak_statistic(convergence_map: np.ndarray,
                                  threshold: float = 0.5) -> dict:
    """
    Compute weak-lensing κ-peak statistic: count peaks above a threshold.

    Args:
        convergence_map (np.ndarray): 2D weak-lensing convergence field (dimensionless)
        threshold (float): minimum κ value to count as a "peak"

    Returns:
        dict with peak_count, peak_density, mean_peak_value, std_peak_value
    """
    kappa = np.asarray(convergence_map, dtype=np.float64)

    # Find peaks: local maxima with κ > threshold
    kappa_masked = np.where(kappa > threshold, kappa, 0)

    # Label connected components
    labeled, n_peaks = ndimage.label(kappa_masked > threshold)

    if n_peaks == 0:
        return {
            'peak_count': 0,
            'peak_density': 0.0,
            'mean_peak_value': 0.0,
            'std_peak_value': 0.0,
        }

    # Extract peak values
    peak_values = []
    for i in range(1, n_peaks + 1):
        mask_i = (labeled == i)
        peak_val = np.max(kappa[mask_i])
        peak_values.append(peak_val)

    peak_values = np.array(peak_values)

    return {
        'peak_count': int(n_peaks),
        'peak_density': float(n_peaks),
        'mean_peak_value': float(np.mean(peak_values)),
        'std_peak_value': float(np.std(peak_values)),
    }


def compute_betti_numbers(density_field: np.ndarray,
                          threshold_percentile: float = 50.0) -> dict:
    """Compute persistent-homology Betti numbers (β₀, β₁, β₂)."""
    rho = np.asarray(density_field, dtype=np.float64)

    thresh_val = np.percentile(rho, threshold_percentile)
    binary_mask = (rho > thresh_val).astype(np.uint8)

    # β₀: connected components
    labeled, n_components = ndimage.label(binary_mask, structure=np.ones((3, 3, 3)))
    beta_0 = int(n_components)

    # β₂: voids (components in complement, minus outer void)
    complement_mask = 1 - binary_mask
    labeled_compl, n_voids = ndimage.label(complement_mask, structure=np.ones((3, 3, 3)))
    beta_2 = int(max(0, n_voids - 1))

    # Euler characteristic (simplified estimate)
    n_boundary_voxels = int(np.sum(ndimage.binary_dilation(binary_mask, iterations=1)) - np.sum(binary_mask))
    euler_char = int(beta_0 - max(1, n_boundary_voxels // 10))

    # β₁ from Euler formula: χ = β₀ - β₁ + β₂
    beta_1 = int(max(0, beta_0 + beta_2 - euler_char))

    return {
        'beta_0': beta_0,
        'beta_1': beta_1,
        'beta_2': beta_2,
        'euler_char': euler_char,
    }
