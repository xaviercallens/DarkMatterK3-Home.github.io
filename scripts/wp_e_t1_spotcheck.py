#!/usr/bin/env python3
"""WP-E T1 spot-check: re-run the highest-displacement (field, class, R, A) combination
through a pure-numpy (no GPU/torch) reimplementation of the deformation, to confirm the
GPU tensor math did not hallucinate the topology. Required by the WP-E directive Section 5
("Sonnet 5 (T1) must manually re-run the highest-scoring parameter pair through the
standard CPU pipeline").

Compares: (a) deformed coordinates position-by-position (max abs difference), and
(b) resulting beta_1/beta_2 at the same absolute thresholds, GPU vs CPU.
"""
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

import numpy as np
import pandas as pd

from pipeline.cosmology import radec_z_to_tangent_plane_mpc, drop_invalid_redshifts
from pipeline.realfield3d import density_field_cartesian_mpc
from pipeline.observables_real import compute_betti_numbers


def deform_chameleon_core_halt_numpy(coords: np.ndarray, radius_mpc: float, amplitude: float) -> np.ndarray:
    """Pure-numpy reimplementation of scripts/wp_e_gpu_sandbox.py's
    deform_chameleon_core_halt, for CPU cross-validation (no torch, no GPU)."""
    n = coords.shape[0]
    out = coords.copy()
    for i in range(n):
        d = np.linalg.norm(coords - coords[i], axis=1)
        mask = (d < radius_mpc)
        mask[i] = False
        if mask.sum() == 0:
            continue
        centroid = coords[mask].mean(axis=0)
        out[i] = coords[i] + amplitude * (centroid - coords[i])
    return out


def deform_void_evacuation_numpy(coords: np.ndarray, radius_mpc: float, amplitude: float) -> np.ndarray:
    n = coords.shape[0]
    out = coords.copy()
    for i in range(n):
        d = np.linalg.norm(coords - coords[i], axis=1)
        mask = (d < radius_mpc)
        mask[i] = False
        if mask.sum() == 0:
            continue
        centroid = coords[mask].mean(axis=0)
        out[i] = coords[i] + amplitude * (coords[i] - centroid)
    return out


DEFORM_NUMPY = {
    "chameleon_core_halt": deform_chameleon_core_halt_numpy,
    "void_evacuation": deform_void_evacuation_numpy,
}


def run_spotcheck(field_info: dict, cls: str, R: float, A: float, nbins: int, threshold: float):
    import torch
    from scripts.wp_e_gpu_sandbox import DEFORM_FN, DEVICE

    df = pd.read_csv(field_info["path"])
    ra_raw = df[field_info["ra_col"]].values
    dec_raw = df[field_info["dec_col"]].values
    z_raw = df[field_info["z_col"]].values
    ra, dec, z, _ = drop_invalid_redshifts(ra_raw, dec_raw, z_raw)
    ra0, dec0 = float(np.mean(ra)), float(np.mean(dec))
    x, y, zc = radec_z_to_tangent_plane_mpc(ra, dec, z, ra0_deg=ra0, dec0_deg=dec0)
    ranges = ((x.min(), x.max()), (y.min(), y.max()), (zc.min(), zc.max()))
    coords_np = np.column_stack([x, y, zc])

    # GPU path (same function the sweep used)
    coords_t = torch.tensor(coords_np, dtype=torch.float32, device=DEVICE)
    gpu_deformed = DEFORM_FN[cls](coords_t, R, A).cpu().numpy()

    # CPU path (independent reimplementation, no torch)
    cpu_deformed = DEFORM_NUMPY[cls](coords_np.astype(np.float64), R, A)

    max_abs_diff = float(np.max(np.abs(gpu_deformed.astype(np.float64) - cpu_deformed)))

    field_gpu = density_field_cartesian_mpc(gpu_deformed[:, 0], gpu_deformed[:, 1], gpu_deformed[:, 2], nbins=nbins, ranges=ranges)
    topo_gpu = compute_betti_numbers(field_gpu, threshold_value=threshold)

    field_cpu = density_field_cartesian_mpc(cpu_deformed[:, 0], cpu_deformed[:, 1], cpu_deformed[:, 2], nbins=nbins, ranges=ranges)
    topo_cpu = compute_betti_numbers(field_cpu, threshold_value=threshold)

    print(f"Field={field_info['name']} class={cls} R={R} A={A} threshold={threshold}")
    print(f"  Max |GPU - CPU| coordinate difference: {max_abs_diff:.2e} Mpc")
    print(f"  GPU topology: beta_1={topo_gpu['beta_1']}, beta_2={topo_gpu['beta_2']}")
    print(f"  CPU topology: beta_1={topo_cpu['beta_1']}, beta_2={topo_cpu['beta_2']}")
    match = (topo_gpu['beta_1'] == topo_cpu['beta_1']) and (topo_gpu['beta_2'] == topo_cpu['beta_2'])
    print(f"  Topology match: {'PASS' if match else 'FAIL'}")
    return max_abs_diff, match


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--field", required=True)
    p.add_argument("--path", required=True)
    p.add_argument("--ra_col", required=True)
    p.add_argument("--dec_col", required=True)
    p.add_argument("--z_col", required=True)
    p.add_argument("--cls", required=True)
    p.add_argument("--R", type=float, required=True)
    p.add_argument("--A", type=float, required=True)
    p.add_argument("--nbins", type=int, default=8)
    p.add_argument("--threshold", type=float, required=True)
    args = p.parse_args()
    field_info = {"name": args.field, "path": args.path, "ra_col": args.ra_col,
                  "dec_col": args.dec_col, "z_col": args.z_col}
    run_spotcheck(field_info, args.cls, args.R, args.A, args.nbins, args.threshold)


# Generated-by: Claude Sonnet 5 (T1) | Verified-by: independent numpy reimplementation
# vs torch GPU output, coordinate-level and topology-level comparison | Reviewed-by: T0 Y
# (Xavier direct authorization, docs/WP_E_T0_AUTHORIZATION_2026_07_25.md)
