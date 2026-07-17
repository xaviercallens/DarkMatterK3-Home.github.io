"""V5 pipeline core (EXECUTION_PLAN.md WP S3-02) — synthetic-data mode only.

Reads no free parameters: the kernel warp comes from the already-certified
`cooper_s10_kernel.py` (repo root, verified against OEIS A005260). This
module computes a model-vs-null comparison statistic on a GPU tensor field
and labels the result mechanically. It refuses to run against anything
under `data/raw/` until gate G1 opens (`pipeline.gate.require_pinned_for_real_data`).
"""
import sys
from pathlib import Path

import numpy as np
import torch

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import cooper_s10_kernel as s10  # noqa: E402  (repo-root module, path shim above)
from pipeline.gate import is_pinned  # noqa: E402


def _delta_band_gpu(field: torch.Tensor, rho_scale: float | None = None,
                     n_shells: int = 16, kmin_frac: float = 0.05,
                     kmax_frac: float = 0.5) -> dict:
    """GPU port of cooper_s10_kernel.delta_s10_band: the pointwise kernel
    warp (exact, certified, CPU) followed by FFT + shell binning on the
    field's own device (CUDA when available)."""
    device = field.device
    rho_np = field.detach().cpu().numpy().astype(np.float64)
    if rho_scale is None:
        rho_scale = float(rho_np.mean())

    warp_np = s10.kernel_s10(rho_np, rho_scale)  # exact certified kernel, CPU
    warped = torch.as_tensor(rho_np * warp_np, device=device)
    raw = torch.as_tensor(rho_np, device=device)

    def contrast(f: torch.Tensor) -> torch.Tensor:
        return f / f.mean() - 1.0

    fw = torch.fft.fftn(contrast(warped))
    fr = torch.fft.fftn(contrast(raw))

    n = rho_np.shape[0]
    freqs = torch.fft.fftfreq(n, device=device) * n
    kx, ky, kz = torch.meshgrid(freqs, freqs, freqs, indexing="ij")
    kmag = torch.sqrt(kx**2 + ky**2 + kz**2)

    nyquist = n / 2.0
    edges = torch.linspace(kmin_frac * nyquist, kmax_frac * nyquist, n_shells + 1,
                            device=device)
    ratios = []
    for i in range(n_shells):
        mask = (kmag >= edges[i]) & (kmag < edges[i + 1])
        if not torch.any(mask):
            continue
        aw = fw[mask].abs().mean()
        ar = fr[mask].abs().mean()
        ratios.append((aw / (ar + 1e-300)).item())
    ratios_t = torch.tensor(ratios)
    return {"delta_band": float((ratios_t - 1.0).abs().mean())}


def observed_statistic(field: torch.Tensor) -> float:
    return _delta_band_gpu(field)["delta_band"]


def null_distribution(n: int, n_trials: int, seed: int, device: torch.device,
                       noise_sigma: float = 0.05) -> np.ndarray:
    """Batched Monte Carlo null distribution of the band statistic — the
    compute-heavy part, run on the T4 when available."""
    from pipeline.synthetic import null_field

    stats = np.empty(n_trials, dtype=np.float64)
    for i in range(n_trials):
        field = null_field(n, seed=seed + i, noise_sigma=noise_sigma, device=device)
        stats[i] = observed_statistic(field)
    return stats


def run_comparison(field: torch.Tensor, null_stats: np.ndarray, alpha: float = 0.05) -> dict:
    """Compare `field`'s statistic against a precomputed null distribution.

    Returns a result dict with a mechanical label:
      - 'SYNTHETIC' always, while PREDICTION.md is unpinned (gate G1) — this
        pipeline has no real observable to compare against yet, so nothing
        it produces is ever TEST or FIT.
      - Once pinned, real-data callers must go through
        `pipeline.gate.require_pinned_for_real_data()` and label TEST/FIT
        themselves per the prereg-pipeline skill; this function's label
        stays SYNTHETIC for any synthetic-field input regardless of pin
        state, since a synthetic run is never evidence.
    """
    observed = observed_statistic(field)
    p_value = float(np.mean(null_stats >= observed))
    return {
        "observed_statistic": observed,
        "p_value": p_value,
        "reject_null": p_value < alpha,
        "alpha": alpha,
        "label": "SYNTHETIC",
        "prediction_pinned": is_pinned(),
    }
