#!/usr/bin/env python3
"""Delta (Δ) observable regeneration (WP-D, Haiku).

DC-free band-averaged asymmetry statistic, regenerated from the legacy definition
in v5_estimator_s10.py and documented in RELEASE_NOTES.md. Golden tests only —
synthetic data, no real-data fetch (that is WP-G post-pin, per hard rule 2.2).

Definition (committed definition, source: v5_estimator_s10.py, RELEASE_NOTES.md):
  Δ = mean(|A_warped / A_raw − 1|) across k-space shells
  where A = |FFT(field − mean)| (DC-free Fourier amplitude)
  and field_warped = field × kernel (here: kernel_s10)

This module computes Δ from a density field without reference to any kernel
(parametrized version for testing against synthetic fields).
"""
import numpy as np


def compute_delta_statistic(density_field: np.ndarray, kernel_func=None,
                            n_shells: int = 16,
                            kmin_frac: float = 0.05,
                            kmax_frac: float = 0.5) -> dict:
    """
    Compute the DC-free band-averaged Δ statistic from a density field.

    Args:
        density_field (np.ndarray): 3D density field (shape must be cubic for FFT)
        kernel_func (callable): optional kernel function f(rho, rho_scale) -> kernel_field
                                if None, uses identity (kernel = 1 everywhere)
        n_shells (int): number of k-space shells to bin
        kmin_frac, kmax_frac (float): k-band edges as fractions of Nyquist frequency

    Returns:
        dict: {
            'delta': float — the Δ statistic (mean fractional amplitude difference)
            'shell_k': np.ndarray — shell center frequencies
            'amplitude_warped': np.ndarray — mean |FFT| per shell (warped field)
            'amplitude_raw': np.ndarray — mean |FFT| per shell (raw field)
        }

    Citation: v5_estimator_s10.py (RELEASE_NOTES.md; legacy definition, recovered 2026-07-25).
    """
    rho = np.asarray(density_field, dtype=np.float64)
    rho_scale = float(np.mean(rho))

    # Apply kernel if provided (identity if None)
    if kernel_func is not None:
        kernel_vals = kernel_func(rho, rho_scale)
        warped = rho * kernel_vals
    else:
        warped = rho.copy()

    def dc_free_amplitude(field):
        """DC-free Fourier amplitude: A(k) = |FFT(field - mean)| / sqrt(volume)."""
        f_zero_mean = field - np.mean(field)
        fft_result = np.fft.fftn(f_zero_mean)
        amplitude = np.abs(fft_result) / np.sqrt(field.size)
        return amplitude

    a_warped = dc_free_amplitude(warped)
    a_raw = dc_free_amplitude(rho)

    # Binning: radial shells in k-space
    n = rho.shape[0]
    freqs = np.fft.fftfreq(n) * n
    kx, ky, kz = np.meshgrid(freqs, freqs, freqs, indexing='ij')
    kmag = np.sqrt(kx**2 + ky**2 + kz**2)

    nyquist = n / 2.0
    edges = np.linspace(kmin_frac * nyquist, kmax_frac * nyquist, n_shells + 1)

    shell_k, aw_shells, ar_shells = [], [], []
    for i in range(n_shells):
        mask = (kmag >= edges[i]) & (kmag < edges[i + 1])
        if not np.any(mask):
            continue
        shell_center = 0.5 * (edges[i] + edges[i + 1])
        shell_k.append(shell_center)
        aw_shells.append(np.mean(a_warped[mask]))
        ar_shells.append(np.mean(a_raw[mask]))

    aw_shells = np.array(aw_shells)
    ar_shells = np.array(ar_shells)

    # Asymmetry statistic (amplitude ratio)
    ratio = aw_shells / np.maximum(ar_shells, 1e-300)
    delta = float(np.mean(np.abs(ratio - 1.0)))

    return {
        'delta': delta,
        'shell_k': np.array(shell_k),
        'amplitude_warped': aw_shells,
        'amplitude_raw': ar_shells,
    }


# Generated-by: Haiku 4.5 WP-D, 2026-07-25 | Verified-by: n/a (implementation only) |
# Reviewed-by: T2 (pending)
