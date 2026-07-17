"""Dual-scale decomposition and cross-scale analysis.

Decomposes 3D fields into coarse (low-freq) and fine (high-freq) components,
computing signal recovery and scale-mixing effects independently.
"""
import numpy as np
import torch
from dataclasses import dataclass
from typing import NamedTuple


class ScaleDecomposition(NamedTuple):
    """Result of wavelet-like scale decomposition."""
    coarse: torch.Tensor  # Low-frequency (coarse-grained) component
    fine: torch.Tensor    # High-frequency (fine-grained) component
    cutoff_freq: float    # Frequency cutoff (in FFT space)


@dataclass
class ScaleMetrics:
    """Metrics for signal recovery at each scale."""
    scale: str  # "coarse", "fine", or "full"
    energy_ratio: float  # (signal energy) / (total energy)
    contrast_recovery: float  # contrast(signal) / contrast(full)
    snr_per_scale: float  # signal-to-noise in this scale
    peak_frequency: float  # dominant frequency


def decompose_scales(
    field: torch.Tensor,
    cutoff_freq: float | None = None,
) -> ScaleDecomposition:
    """Decompose field into coarse and fine scales via FFT.

    Low frequencies (k < cutoff_freq) remain in coarse component;
    high frequencies (k >= cutoff_freq) go into fine component.

    Parameters
    ----------
    field : torch.Tensor
        3D field (n, n, n)
    cutoff_freq : float, optional
        Frequency cutoff in FFT space. Defaults to Nyquist/4.

    Returns
    -------
    ScaleDecomposition
        Coarse and fine components, spatially domain
    """
    device = field.device
    n = field.shape[0]

    if cutoff_freq is None:
        cutoff_freq = n / 4.0

    # FFT
    fft_field = torch.fft.fftn(field)
    fft_shifted = torch.fft.fftshift(fft_field)

    # Frequency grid
    freqs = torch.fft.fftfreq(n, device=device) * n
    kx, ky, kz = torch.meshgrid(freqs, freqs, freqs, indexing="ij")
    kmag = torch.sqrt(kx**2 + ky**2 + kz**2)

    # Coarse: low frequencies
    mask_coarse = kmag < cutoff_freq
    fft_coarse = fft_shifted.clone()
    fft_coarse[~mask_coarse] = 0.0

    # Fine: high frequencies
    mask_fine = kmag >= cutoff_freq
    fft_fine = fft_shifted.clone()
    fft_fine[~mask_fine] = 0.0

    # Inverse FFT back to spatial domain
    fft_coarse = torch.fft.ifftshift(fft_coarse)
    fft_fine = torch.fft.ifftshift(fft_fine)

    coarse = torch.fft.ifftn(fft_coarse).real
    fine = torch.fft.ifftn(fft_fine).real

    return ScaleDecomposition(
        coarse=coarse,
        fine=fine,
        cutoff_freq=cutoff_freq,
    )


def compute_scale_metrics(
    field: torch.Tensor,
    scale: str = "full",
) -> ScaleMetrics:
    """Compute signal recovery metrics for a given scale.

    Parameters
    ----------
    field : torch.Tensor
        3D field (coarse, fine, or full)
    scale : str
        Label for this scale ("coarse", "fine", or "full")

    Returns
    -------
    ScaleMetrics
        Energy ratios, contrast recovery, SNR, peak frequency
    """
    device = field.device
    n = field.shape[0]

    # Energy ratio: variance (energy) in the field
    field_energy = torch.var(field).item()
    bg_energy = float(torch.var(field.mean() * torch.ones_like(field)).item())
    energy_ratio = field_energy / (bg_energy + 1e-10)

    # Contrast: normalized deviation from mean
    contrast = field / (field.mean() + 1e-10) - 1.0
    contrast_recovery = float(torch.std(contrast).item())

    # SNR: ratio of signal std to background noise (approximated)
    signal_std = float(torch.std(field).item())
    noise_std = 0.05  # typical noise sigma; ideally passed in
    snr_per_scale = signal_std / (noise_std + 1e-10)

    # Peak frequency (in FFT domain)
    fft_field = torch.fft.fftn(field)
    freqs = torch.fft.fftfreq(n, device=device) * n
    kx, ky, kz = torch.meshgrid(freqs, freqs, freqs, indexing="ij")
    kmag = torch.sqrt(kx**2 + ky**2 + kz**2)

    power = torch.abs(fft_field) ** 2
    max_power_idx = torch.argmax(power.flatten())
    peak_freq = float(kmag.flatten()[max_power_idx].item())

    return ScaleMetrics(
        scale=scale,
        energy_ratio=energy_ratio,
        contrast_recovery=contrast_recovery,
        snr_per_scale=snr_per_scale,
        peak_frequency=peak_freq,
    )


def analyze_scale_mixing(
    full_field: torch.Tensor,
    decomp: ScaleDecomposition,
) -> dict:
    """Analyze scale-mixing: does fine-scale signal obscure coarse-scale signal?

    Returns
    -------
    dict
        - "coarse_contamination": (energy in fine component of coarse field)
        - "fine_purity": fraction of fine field that is truly high-freq
        - "cross_correlation": correlation between coarse and fine
        - "orthogonality_violation": how much cross-talk between scales
    """
    # Orthogonality check: ideally coarse and fine should be orthogonal
    coarse_dot_fine = torch.sum(decomp.coarse * decomp.fine).item()
    coarse_norm = torch.norm(decomp.coarse).item()
    fine_norm = torch.norm(decomp.fine).item()

    orthogonality = abs(coarse_dot_fine) / (coarse_norm * fine_norm + 1e-10)

    # Energy conservation check
    full_energy = torch.sum(full_field**2).item()
    recon_energy = torch.sum(decomp.coarse**2 + decomp.fine**2).item()
    energy_conservation = abs(full_energy - recon_energy) / (full_energy + 1e-10)

    # Cross-correlation (should be near 0 if scales are independent)
    coarse_centered = decomp.coarse - decomp.coarse.mean()
    fine_centered = decomp.fine - decomp.fine.mean()
    cov = torch.sum(coarse_centered * fine_centered).item()
    coarse_var = torch.var(decomp.coarse).item()
    fine_var = torch.var(decomp.fine).item()
    cross_corr = cov / (np.sqrt(coarse_var * fine_var) + 1e-10)

    return {
        "orthogonality_violation": orthogonality,
        "energy_conservation_error": energy_conservation,
        "cross_correlation": cross_corr,
        "coarse_norm": float(coarse_norm),
        "fine_norm": float(fine_norm),
    }
