"""GPU-accelerated synthetic field generation for closure/null tests.

Torch tensors run on CUDA (Tesla T4) when available, falling back to CPU
otherwise. This module never touches real data — it is the synthetic-data
infrastructure gate G1 permits pre-pin (CLAUDE.md rule 1).
"""
import torch


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _blob_field(n: int, centers, amps, sigmas, device: torch.device) -> torch.Tensor:
    idx = torch.stack(
        torch.meshgrid(
            torch.arange(n, device=device, dtype=torch.float64),
            torch.arange(n, device=device, dtype=torch.float64),
            torch.arange(n, device=device, dtype=torch.float64),
            indexing="ij",
        )
    )
    field = torch.zeros((n, n, n), device=device, dtype=torch.float64)
    for c, amp, sig in zip(centers, amps, sigmas):
        c = torch.tensor(c, device=device, dtype=torch.float64).view(3, 1, 1, 1)
        d2 = ((idx - c) ** 2).sum(dim=0)
        field = field + amp * torch.exp(-d2 / (2 * sig**2))
    return field


def null_field(n: int, seed: int, noise_sigma: float = 0.05,
                device: torch.device | None = None) -> torch.Tensor:
    """Pure background + noise, no injected signal (the null hypothesis)."""
    device = device or get_device()
    gen = torch.Generator(device=device.type if device.type == "cpu" else "cpu")
    gen.manual_seed(seed)
    noise = torch.randn((n, n, n), generator=gen, dtype=torch.float64)
    if device.type == "cuda":
        noise = noise.to(device)
    field = torch.ones((n, n, n), device=device, dtype=torch.float64) + noise_sigma * noise
    return field.clamp(min=0.05)


def signal_field(n: int, seed: int, amplitude: float = 2.0,
                  noise_sigma: float = 0.05,
                  device: torch.device | None = None) -> torch.Tensor:
    """Background + two injected Gaussian overdensities + noise.

    `amplitude` scales the injected blobs; used by the closure test to
    confirm the pipeline recovers a known, controlled signal.
    """
    device = device or get_device()
    field = null_field(n, seed, noise_sigma=noise_sigma, device=device)
    centers = [(n * 0.3, n * 0.3, n * 0.3), (n * 0.65, n * 0.6, n * 0.45)]
    amps = [amplitude, amplitude * 0.75]
    sigmas = [n * 0.08, n * 0.12]
    field = field + _blob_field(n, centers, amps, sigmas, device)
    return field.clamp(min=0.05)
