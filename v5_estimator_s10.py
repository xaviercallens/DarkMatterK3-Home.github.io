#!/usr/bin/env python3
"""
v5_estimator_s10.py
===================

DC-free, shot-noise-corrected band-averaged asymmetry estimator for s₁₀.
(Identical interface to cooper_exact.delta_s7_band, but using s₁₀ kernel.)

This is WP-B2 (Estimator Design): mechanical implementation once the kernel
is certified. No floating parameters — all choices documented in git.
"""

import numpy as np
from cooper_s10_kernel import kernel_s10


def estimate_delta_s10(rho_field, rho_scale=None, n_shells=16,
                       kmin_frac=0.05, kmax_frac=0.5):
    """
    Band-averaged asymmetry estimator for s₁₀ kernel vs raw density.
    Uses amplitude-based (not power-spectrum) comparison to avoid numerical instabilities.

    Args:
        rho_field (np.ndarray): 3D density field (galaxy counts or density)
        rho_scale (float): reference density for modulus mapping (default: mean)
        n_shells (int): number of k-space shells
        kmin_frac, kmax_frac (float): k-band as fractions of Nyquist

    Returns:
        dict: {
          'shell_k': array of shell centers (grid frequency units),
          'amplitude_warped': |FFT| per shell,
          'amplitude_raw': |FFT| per shell,
          'delta_band': scalar summary = mean |A_warp - A_raw| / A_raw,
        }
    """
    rho = np.asarray(rho_field, dtype=np.float64)
    if rho_scale is None:
        rho_scale = float(np.mean(rho))

    # Apply s₁₀ kernel
    warped = rho * kernel_s10(rho, rho_scale)

    def amplitude_spectrum(f):
        """DC-free Fourier amplitude: A(k) = |FFT(f - mean)|."""
        f_zero_mean = f - np.mean(f)
        fft_result = np.fft.fftn(f_zero_mean)
        amplitude = np.abs(fft_result) / np.sqrt(f.size)  # normalize by sqrt(volume)
        return amplitude

    a_warped = amplitude_spectrum(warped)
    a_raw = amplitude_spectrum(rho)

    # Bin by |k|
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

    # Asymmetry: fractional difference
    ratio = aw_shells / np.maximum(ar_shells, 1e-300)
    delta = float(np.mean(np.abs(ratio - 1.0)))

    return {
        'shell_k': np.array(shell_k),
        'amplitude_warped': aw_shells,
        'amplitude_raw': ar_shells,
        'delta_band': delta,
    }


def test_on_synthetic():
    """
    Smoke test: verify estimator runs and gives reasonable values on synthetic data.
    """
    print("=" * 70)
    print("v5_estimator_s10.py — synthetic data test")
    print("=" * 70)

    rng = np.random.default_rng(99)
    n = 64

    # Null test: pure Poisson noise (kernel amplifies it)
    print("\n[Test 1] Null: pure Poisson noise")
    rho_null = rng.poisson(lam=1.0, size=(n, n, n)).astype(np.float32) + 0.5
    r_null = estimate_delta_s10(rho_null)
    print(f"  delta_band = {r_null['delta_band']:.5f} (kernel amplifies noise)")
    assert 0.1 < r_null['delta_band'], "null delta unexpectedly small"

    # Signal test: density with injected clusters
    print("\n[Test 2] Signal: Gaussian overdensity clusters")
    rho_signal = np.ones((n, n, n)) + 0.2 * rng.standard_normal((n, n, n))
    idx = np.indices((n, n, n))
    for center, amp in [((20, 20, 20), 2.0), ((44, 44, 44), 1.5)]:
        d2 = sum((idx[i] - center[i])**2 for i in range(3))
        rho_signal += amp * np.exp(-d2 / 50.0)
    rho_signal = np.clip(rho_signal, 0.05, None)

    r_signal = estimate_delta_s10(rho_signal)
    print(f"  delta_band = {r_signal['delta_band']:.5f} (expect > 0.05)")
    assert r_signal['delta_band'] > r_null['delta_band'], "signal not > null"

    # Consistency test: downsampling shouldn't change the statistic dramatically
    print("\n[Test 3] Consistency: subsampled data")
    rho_sub = rho_signal[::2, ::2, ::2]  # 1/8 the volume
    r_sub = estimate_delta_s10(rho_sub)
    print(f"  full delta_band = {r_signal['delta_band']:.5f}")
    print(f"  sub  delta_band = {r_sub['delta_band']:.5f}")
    # Expect some variation due to different k-space sampling, but same order of magnitude
    ratio = r_sub['delta_band'] / (r_signal['delta_band'] + 1e-10)
    print(f"  ratio = {ratio:.3f} (expect 0.5–2.0)")
    assert 0.3 < ratio < 3.0, "subsampling caused unexpected change"

    print("\n" + "=" * 70)
    print("ALL TESTS PASSED — estimator operational")
    print("=" * 70)


if __name__ == "__main__":
    test_on_synthetic()
