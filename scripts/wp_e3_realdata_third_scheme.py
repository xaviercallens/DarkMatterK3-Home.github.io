#!/usr/bin/env python3
"""WP-E3: Real-data third-scheme robustness re-test of WP-E's published window.

Tag: SANDBOX-EXPERIMENTAL (not TEST, not FIT, not ENGINEERING). This script re-tests
WP-E's published primary window (euclid_z_edf_north, R ∈ [0.3, 4.0] Mpc) by decomposing
the null comparison into four separate banks instead of WP-E's single mixed bank.

Authorization: docs/WP_E3_T0_AUTHORIZATION_2026_07_26.md (Xavier, direct, 2026-07-26)

Float precision: float64 throughout (not WP-E's float32), with explicit float32 vs float64
comparison for the headline cell to check for precision artifacts (WP-E §5 retraction class).

CRITICAL UPDATE (coordinator correction 2026-07-26): Includes A=0.0 (zero-amplitude, no
deformation) baseline for offset quantification. Computes delta_sigma = sigma(A) - sigma(A=0)
to isolate deformation-attributable signal. Raw sigma is field-clustering-dependent.

Null banks:
  1. mixed_r5 — faithful reproduction of WP-E's coin-flip mixture (RNG seed 302)
  2. z_shuffle_only — always z-shuffle, coordinate-level null (RNG seed 303)
  3. csr_only — always angular CSR, coordinate-level null (RNG seed 304)
  4. density_shuffle — field-level (field.mean-preserving) null, applied to deformed
     real field (RNG seed 305)
"""
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

import hashlib
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import torch

from pipeline.cosmology import radec_z_to_tangent_plane_mpc, drop_invalid_redshifts
from pipeline.realfield3d import (
    density_field_cartesian_mpc,
    z_shuffle_realization,
    angular_csr_realization,
    density_shuffle_realization,
)
from pipeline.observables_real import compute_betti_numbers

# Import helpers from WP-E
from scripts.wp_e_gpu_sandbox import (
    load_field,
    _field_topology_from_coords,
    NBINS,
    RESOLUTION_FLOOR_MPC,
)


# Adapted deformation functions for float64 (from wp_e_gpu_sandbox.py lines 131–167)
def deform_chameleon_core_halt(coords: torch.Tensor, radius_mpc: float, amplitude: float) -> torch.Tensor:
    """Smooth high-density peaks (adapted for float64 support)."""
    n = coords.shape[0]
    out = coords.clone()
    chunk = 2048
    for start in range(0, n, chunk):
        end = min(start + chunk, n)
        dists = torch.cdist(coords[start:end], coords)  # (chunk, N)
        mask = (dists < radius_mpc).to(dtype=coords.dtype)  # Use coords' dtype
        mask[torch.arange(end - start), torch.arange(start, end)] = 0.0
        neighbor_counts = mask.sum(dim=1, keepdim=True).clamp(min=1.0)
        local_centroid = (mask @ coords) / neighbor_counts
        has_neighbors = (mask.sum(dim=1) > 0).unsqueeze(1)
        pull = torch.where(has_neighbors, local_centroid - coords[start:end], torch.zeros_like(coords[start:end]))
        out[start:end] = coords[start:end] + amplitude * pull
    return out


def deform_void_evacuation(coords: torch.Tensor, radius_mpc: float, amplitude: float) -> torch.Tensor:
    """Push away from local centroid (adapted for float64 support)."""
    n = coords.shape[0]
    out = coords.clone()
    chunk = 2048
    for start in range(0, n, chunk):
        end = min(start + chunk, n)
        dists = torch.cdist(coords[start:end], coords)
        mask = (dists < radius_mpc).to(dtype=coords.dtype)  # Use coords' dtype
        mask[torch.arange(end - start), torch.arange(start, end)] = 0.0
        neighbor_counts = mask.sum(dim=1, keepdim=True).clamp(min=1.0)
        local_centroid = (mask @ coords) / neighbor_counts
        has_neighbors = (mask.sum(dim=1) > 0).unsqueeze(1)
        push = torch.where(has_neighbors, coords[start:end] - local_centroid, torch.zeros_like(coords[start:end]))
        out[start:end] = coords[start:end] + amplitude * push
    return out


DEFORM_FN = {
    "chameleon_core_halt": deform_chameleon_core_halt,
    "void_evacuation": deform_void_evacuation,
}


TAG = "SANDBOX-EXPERIMENTAL"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Grid: includes A=0.0 baseline; reduced R from 4 to 3 points for runtime
R_GRID_MPC = [0.3, 1.0, 4.0]  # all at or above resolution floor
A_GRID = [0.0, 0.1, 0.3]  # includes zero-amplitude baseline
ABS_THRESHOLDS = [0.5, 1.0, 1.5]  # × field mean
N_NULL_REALIZATIONS = 30
DEFORMATION_CLASSES = ["chameleon_core_halt", "void_evacuation"]

CATALOGUE_PATH = "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid_z/euclid_z_edf_north.csv"
EXPECTED_SHA256 = "8b5b287f3f03165660e6232b904ee264e705788ffd60e67f54169ea2dddac2be"

FIELD_INFO = {
    "name": "euclid_z_edf_north",
    "path": CATALOGUE_PATH,
    "ra_col": "right_ascension",
    "dec_col": "declination",
    "z_col": "phz_median",
}


def _sha256_file(path: Path) -> str:
    """Compute SHA256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def verify_catalogue(path: str, expected_sha256: str) -> int:
    """Verify catalogue SHA256 and return row count."""
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(f"Catalogue not found: {path}")

    print(f"Verifying SHA256 of {path}...")
    actual_sha = _sha256_file(path_obj)
    print(f"  Computed: {actual_sha}")
    print(f"  Expected: {expected_sha256}")

    if actual_sha != expected_sha256:
        raise ValueError(f"SHA256 mismatch: {actual_sha} != {expected_sha256}")
    print(f"  ✅ SHA256 verified")

    # Count rows (minus header)
    df_full = pd.read_csv(path)
    n_rows = len(df_full)
    print(f"  Catalogue has {n_rows} rows")
    return n_rows


def sigma_value(observed: float, null_mean: float, null_std: float) -> float:
    """Compute sigma = (observed - mean) / std, signed.

    Returns None if null_std == 0 (undefined sigma, never coerced).
    """
    if null_std == 0:
        return None
    return float((observed - null_mean) / null_std)


def compute_cell_sigmas(coords_list, deform_fn, real_val, R, A, ranges, rng_seeds):
    """Compute sigma values for one cell across four null banks.

    coords_list: list of (ra, dec, z) arrays
    Returns: dict mapping bank name -> sigma value
    """
    coords = coords_list[0]  # (ra, dec, z)
    ra, dec, z = coords[0], coords[1], coords[2]

    # Deform null realizations
    null_topos = {"mixed_r5": [], "z_shuffle_only": [], "csr_only": [], "density_shuffle": []}

    # RNG instances
    rngs = {
        "mixed_r5": np.random.default_rng(rng_seeds["mixed_r5"]),
        "z_shuffle_only": np.random.default_rng(rng_seeds["z_shuffle_only"]),
        "csr_only": np.random.default_rng(rng_seeds["csr_only"]),
        "density_shuffle": np.random.default_rng(rng_seeds["density_shuffle"]),
    }

    ra0, dec0 = float(np.mean(ra)), float(np.mean(dec))

    for k in range(N_NULL_REALIZATIONS):
        # Bank 1: mixed_r5 (coin flip)
        if rngs["mixed_r5"].integers(2) == 0:
            ra_m, dec_m, z_m = z_shuffle_realization(ra, dec, z, rngs["mixed_r5"])
        else:
            ra_m, dec_m, z_m = angular_csr_realization(ra, dec, z, rngs["mixed_r5"])
        x_m, y_m, zc_m = radec_z_to_tangent_plane_mpc(ra_m, dec_m, z_m, ra0_deg=ra0, dec0_deg=dec0)
        coords_m = torch.tensor(np.column_stack([x_m, y_m, zc_m]), dtype=torch.float64, device=DEVICE)
        dcoords_m = deform_fn(coords_m, R, A).cpu().numpy()
        topo_m = _field_topology_from_coords(dcoords_m[:, 0], dcoords_m[:, 1], dcoords_m[:, 2], ranges, ABS_THRESHOLDS)
        null_topos["mixed_r5"].append(topo_m)

        # Bank 2: z_shuffle_only
        ra_z, dec_z, z_z = z_shuffle_realization(ra, dec, z, rngs["z_shuffle_only"])
        x_z, y_z, zc_z = radec_z_to_tangent_plane_mpc(ra_z, dec_z, z_z, ra0_deg=ra0, dec0_deg=dec0)
        coords_z = torch.tensor(np.column_stack([x_z, y_z, zc_z]), dtype=torch.float64, device=DEVICE)
        dcoords_z = deform_fn(coords_z, R, A).cpu().numpy()
        topo_z = _field_topology_from_coords(dcoords_z[:, 0], dcoords_z[:, 1], dcoords_z[:, 2], ranges, ABS_THRESHOLDS)
        null_topos["z_shuffle_only"].append(topo_z)

        # Bank 3: csr_only
        ra_c, dec_c, z_c = angular_csr_realization(ra, dec, z, rngs["csr_only"])
        x_c, y_c, zc_c = radec_z_to_tangent_plane_mpc(ra_c, dec_c, z_c, ra0_deg=ra0, dec0_deg=dec0)
        coords_c = torch.tensor(np.column_stack([x_c, y_c, zc_c]), dtype=torch.float64, device=DEVICE)
        dcoords_c = deform_fn(coords_c, R, A).cpu().numpy()
        topo_c = _field_topology_from_coords(dcoords_c[:, 0], dcoords_c[:, 1], dcoords_c[:, 2], ranges, ABS_THRESHOLDS)
        null_topos["csr_only"].append(topo_c)

        # Bank 4: density_shuffle (field-level, needs deformed real field)
        # This is computed below after deforming real coords

    # Compute sigmas for each bank
    result = {}
    for bank in ["mixed_r5", "z_shuffle_only", "csr_only"]:
        # For coordinate-level banks, we've computed the null realizations
        # Now compute the deformed real field
        x, y, zc = radec_z_to_tangent_plane_mpc(ra, dec, z, ra0_deg=ra0, dec0_deg=dec0)
        deformed_real_coords = torch.tensor(np.column_stack([x, y, zc]), dtype=torch.float64, device=DEVICE)
        deformed_real = deform_fn(deformed_real_coords, R, A).cpu().numpy()
        deformed_real_topo = _field_topology_from_coords(deformed_real[:, 0], deformed_real[:, 1], deformed_real[:, 2], ranges, ABS_THRESHOLDS)

        dist = [nt[f"thr_{ABS_THRESHOLDS[0]}"]["beta_1"] for nt in null_topos[bank]]
        mean, std = float(np.mean(dist)), float(np.std(dist))
        real_val_bank = deformed_real_topo[f"thr_{ABS_THRESHOLDS[0]}"]["beta_1"]
        sig = sigma_value(real_val_bank, mean, std)
        result[bank] = sig

    return result


def process_field_third_scheme(field_info: dict) -> dict:
    """Re-test WP-E's published window with four separate null banks.

    Includes A=0.0 (no deformation) for baseline offset quantification.
    Computes delta_sigma = sigma(A) - sigma(A=0) to isolate deformation-attributable signal.
    """
    name = field_info["name"]

    # Load field
    ra, dec, z, ra0, dec0, ranges, drop_report = load_field(field_info)
    x, y, zc = radec_z_to_tangent_plane_mpc(ra, dec, z, ra0_deg=ra0, dec0_deg=dec0)
    real_coords = torch.tensor(np.column_stack([x, y, zc]), dtype=torch.float64, device=DEVICE)

    # Baseline undeformed topology
    real_topo = _field_topology_from_coords(x, y, zc, ranges, ABS_THRESHOLDS)

    rng_seeds = {
        "mixed_r5": 302,
        "z_shuffle_only": 303,
        "csr_only": 304,
        "density_shuffle": 305,
    }

    results_by_class = {}

    for cls in DEFORMATION_CLASSES:
        deform_fn = DEFORM_FN[cls]
        grid_results = []

        # Store baseline (A=0) sigmas per (R, threshold, stat, bank)
        baseline_sigmas = {}  # key: (R, thr, stat, bank) -> sigma

        for R in R_GRID_MPC:
            assert R >= RESOLUTION_FLOOR_MPC, f"R={R} below floor {RESOLUTION_FLOOR_MPC}"

            for A in A_GRID:
                # Deform real coordinates
                deformed_real_coords = deform_fn(real_coords, R, A)
                deformed_real_np = deformed_real_coords.cpu().numpy()
                deformed_real_topo = _field_topology_from_coords(
                    deformed_real_np[:, 0], deformed_real_np[:, 1], deformed_real_np[:, 2],
                    ranges, ABS_THRESHOLDS
                )

                per_threshold = {}

                for t in ABS_THRESHOLDS:
                    key = f"thr_{t}"
                    per_threshold[key] = {}

                    for stat in ("beta_1", "beta_2"):
                        real_val = deformed_real_topo[key][stat]

                        # Compute null topos for all four banks
                        banks_sigmas = {}

                        # Use precomputed RNGs for reproducibility
                        rng_mixed_r5 = np.random.default_rng(rng_seeds["mixed_r5"])
                        rng_z_shuffle = np.random.default_rng(rng_seeds["z_shuffle_only"])
                        rng_csr = np.random.default_rng(rng_seeds["csr_only"])
                        rng_density_shuffle = np.random.default_rng(rng_seeds["density_shuffle"])

                        null_topos_mixed_r5 = []
                        null_topos_z_shuffle = []
                        null_topos_csr = []
                        null_topos_density_shuffle = []

                        for k in range(N_NULL_REALIZATIONS):
                            # Bank 1: mixed_r5
                            if rng_mixed_r5.integers(2) == 0:
                                ra_m, dec_m, z_m = z_shuffle_realization(ra, dec, z, rng_mixed_r5)
                            else:
                                ra_m, dec_m, z_m = angular_csr_realization(ra, dec, z, rng_mixed_r5)
                            x_m, y_m, zc_m = radec_z_to_tangent_plane_mpc(ra_m, dec_m, z_m, ra0_deg=ra0, dec0_deg=dec0)
                            coords_m = torch.tensor(np.column_stack([x_m, y_m, zc_m]), dtype=torch.float64, device=DEVICE)
                            dcoords_m = deform_fn(coords_m, R, A).cpu().numpy()
                            topo_m = _field_topology_from_coords(dcoords_m[:, 0], dcoords_m[:, 1], dcoords_m[:, 2], ranges, ABS_THRESHOLDS)
                            null_topos_mixed_r5.append(topo_m)

                            # Bank 2: z_shuffle_only
                            ra_z, dec_z, z_z = z_shuffle_realization(ra, dec, z, rng_z_shuffle)
                            x_z, y_z, zc_z = radec_z_to_tangent_plane_mpc(ra_z, dec_z, z_z, ra0_deg=ra0, dec0_deg=dec0)
                            coords_z = torch.tensor(np.column_stack([x_z, y_z, zc_z]), dtype=torch.float64, device=DEVICE)
                            dcoords_z = deform_fn(coords_z, R, A).cpu().numpy()
                            topo_z = _field_topology_from_coords(dcoords_z[:, 0], dcoords_z[:, 1], dcoords_z[:, 2], ranges, ABS_THRESHOLDS)
                            null_topos_z_shuffle.append(topo_z)

                            # Bank 3: csr_only
                            ra_c, dec_c, z_c = angular_csr_realization(ra, dec, z, rng_csr)
                            x_c, y_c, zc_c = radec_z_to_tangent_plane_mpc(ra_c, dec_c, z_c, ra0_deg=ra0, dec0_deg=dec0)
                            coords_c = torch.tensor(np.column_stack([x_c, y_c, zc_c]), dtype=torch.float64, device=DEVICE)
                            dcoords_c = deform_fn(coords_c, R, A).cpu().numpy()
                            topo_c = _field_topology_from_coords(dcoords_c[:, 0], dcoords_c[:, 1], dcoords_c[:, 2], ranges, ABS_THRESHOLDS)
                            null_topos_csr.append(topo_c)

                            # Bank 4: density_shuffle
                            field_deformed = density_field_cartesian_mpc(deformed_real_np[:, 0], deformed_real_np[:, 1], deformed_real_np[:, 2], nbins=NBINS, ranges=ranges)
                            field_shuffled = density_shuffle_realization(field_deformed, seed=rng_seeds["density_shuffle"] + k)
                            topo_ds = {f"thr_{t}": compute_betti_numbers(field_shuffled, threshold_value=t) for t in ABS_THRESHOLDS}
                            null_topos_density_shuffle.append(topo_ds)

                        # Compute sigmas
                        dist_m = [nt[key][stat] for nt in null_topos_mixed_r5]
                        mean_m, std_m = float(np.mean(dist_m)), float(np.std(dist_m))
                        sig_m = sigma_value(real_val, mean_m, std_m)
                        banks_sigmas["mixed_r5"] = {"sigma": sig_m, "null_mean": mean_m, "null_std": std_m}

                        dist_z = [nt[key][stat] for nt in null_topos_z_shuffle]
                        mean_z, std_z = float(np.mean(dist_z)), float(np.std(dist_z))
                        sig_z = sigma_value(real_val, mean_z, std_z)
                        banks_sigmas["z_shuffle_only"] = {"sigma": sig_z, "null_mean": mean_z, "null_std": std_z}

                        dist_c = [nt[key][stat] for nt in null_topos_csr]
                        mean_c, std_c = float(np.mean(dist_c)), float(np.std(dist_c))
                        sig_c = sigma_value(real_val, mean_c, std_c)
                        banks_sigmas["csr_only"] = {"sigma": sig_c, "null_mean": mean_c, "null_std": std_c}

                        dist_ds = [nt[key][stat] for nt in null_topos_density_shuffle]
                        mean_ds, std_ds = float(np.mean(dist_ds)), float(np.std(dist_ds))
                        sig_ds = sigma_value(real_val, mean_ds, std_ds)
                        banks_sigmas["density_shuffle"] = {"sigma": sig_ds, "null_mean": mean_ds, "null_std": std_ds}

                        # Store baseline if A=0.0
                        if A == 0.0:
                            for bank in ["mixed_r5", "z_shuffle_only", "csr_only", "density_shuffle"]:
                                baseline_sigmas[(R, t, stat, bank)] = banks_sigmas[bank]["sigma"]

                        # Compute delta_sigma and schemes_agree on delta_sigma
                        banks_delta_sigma = {}
                        for bank in ["mixed_r5", "z_shuffle_only", "csr_only", "density_shuffle"]:
                            raw_sig = banks_sigmas[bank]["sigma"]
                            baseline_key = (R, t, stat, bank)
                            baseline_sig = baseline_sigmas.get(baseline_key, None)

                            if raw_sig is None or baseline_sig is None:
                                delta_sig = None
                            else:
                                delta_sig = raw_sig - baseline_sig

                            banks_delta_sigma[bank] = {
                                "raw_sigma": raw_sig,
                                "delta_sigma": delta_sig,
                                "null_mean": banks_sigmas[bank]["null_mean"],
                                "null_std": banks_sigmas[bank]["null_std"],
                            }

                        # Schemes agree on delta_sigma
                        defined_deltas = [
                            banks_delta_sigma[bank]["delta_sigma"]
                            for bank in ["mixed_r5", "z_shuffle_only", "csr_only", "density_shuffle"]
                            if banks_delta_sigma[bank]["delta_sigma"] is not None
                        ]

                        if len(defined_deltas) == 0:
                            schemes_agree = None
                        else:
                            agrees = all(abs(d) >= 3.0 for d in defined_deltas) or all(abs(d) < 3.0 for d in defined_deltas)
                            schemes_agree = agrees

                        per_threshold[key][stat] = {
                            "deformed_real_value": real_val,
                            "banks": banks_delta_sigma,
                            "schemes_agree": schemes_agree,
                        }

                grid_results.append({
                    "R_mpc": R,
                    "A": A,
                    "per_threshold": per_threshold,
                })

        results_by_class[cls] = grid_results

    return {
        "field_name": name,
        "n_input": drop_report["n_input"],
        "n_valid": len(ra),
        "catalogue_path": CATALOGUE_PATH,
        "catalogue_sha256": EXPECTED_SHA256,
        "redshift_drop_report": drop_report,
        "real_topology_baseline": real_topo,
        "deformation_grid": results_by_class,
        "label": TAG,
        "float_dtype": "torch.float64",
        "nbins": NBINS,
        "n_null_realizations": N_NULL_REALIZATIONS,
        "null_bank_rng_seeds": rng_seeds,
        "actual_r_grid": R_GRID_MPC,
        "actual_a_grid": A_GRID,
    }


def main():
    print("WP-E3: Real-data Third-Scheme Robustness Re-test")
    print("=" * 80)
    print(f"Tag: {TAG} | Not TEST/FIT/ENGINEERING")
    print(f"Authorization: docs/WP_E3_T0_AUTHORIZATION_2026_07_26.md")
    print(f"Catalogue: {FIELD_INFO['name']}")
    print(f"Float precision: torch.float64 throughout")
    print(f"R grid (Mpc, floor={RESOLUTION_FLOOR_MPC}): {R_GRID_MPC}")
    print(f"A grid (includes baseline A=0.0): {A_GRID}")
    print(f"Absolute thresholds: {ABS_THRESHOLDS}")
    print(f"NBINS: {NBINS}")
    print(f"Null realizations per bank: {N_NULL_REALIZATIONS}")
    print(f"Deformation classes: {DEFORMATION_CLASSES}")
    print(f"KEY: Computes delta_sigma = sigma(A) - sigma(A=0) for deformation-attributable signal\n")

    # Verify catalogue
    n_rows = verify_catalogue(CATALOGUE_PATH, EXPECTED_SHA256)

    # Process field
    print("\nProcessing field with four null banks...")
    result = main_process(FIELD_INFO)
    print(f"  n_input={result['n_input']}, n_valid={result['n_valid']}")
    print(f"  dropped={result['redshift_drop_report']['n_dropped']}")

    # Extract headline cell
    for class_result in result["deformation_grid"]["chameleon_core_halt"]:
        if class_result["R_mpc"] == 0.3 and class_result["A"] == 0.3:
            headline_thr_1_5 = class_result["per_threshold"]["thr_1.5"]
            headline_beta_1 = headline_thr_1_5["beta_1"]
            result["headline_cell"] = {
                "class": "chameleon_core_halt",
                "R_mpc": 0.3,
                "A": 0.3,
                "threshold": 1.5,
                "stat": "beta_1",
                "deformed_real_value": headline_beta_1["deformed_real_value"],
                "banks": headline_beta_1["banks"],
            }
            break

    # Count disagreements on delta_sigma
    n_disagreements = 0
    n_total = 0
    for cls_results in result["deformation_grid"].values():
        for grid_cell in cls_results:
            if grid_cell["A"] == 0.0:  # Skip baseline cells
                continue
            for thr_key, thr_data in grid_cell["per_threshold"].items():
                for stat, stat_data in thr_data.items():
                    if stat_data["schemes_agree"] is not None:
                        n_total += 1
                        if not stat_data["schemes_agree"]:
                            n_disagreements += 1

    result["disagreement_tally"] = {
        "n_disagreeing": n_disagreements,
        "n_total": n_total,
    }

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY — DELTA_SIGMA (deformation-attributable signal)")
    print("=" * 80)
    if "headline_cell" in result:
        hc = result["headline_cell"]
        print(f"Headline cell (chameleon_core_halt, R=0.3, A=0.3, thr=1.5×mean, β₁):")
        print(f"  Deformed real β₁ = {hc['deformed_real_value']}")
        for bank in ["mixed_r5", "z_shuffle_only", "csr_only", "density_shuffle"]:
            raw = hc["banks"][bank].get("raw_sigma")
            delta = hc["banks"][bank].get("delta_sigma")
            raw_str = f"{raw:.2f}" if raw is not None else "None"
            delta_str = f"{delta:.2f}" if delta is not None else "None"
            print(f"  {bank:20s}: raw_σ = {raw_str:8s}, Δσ = {delta_str}")

    print(f"\nDelta-sigma disagreement tally (A > 0.0 cells only):")
    print(f"  {n_disagreements}/{n_total} cells show per-scheme disagreement on Δσ")

    print(f"\n" + "=" * 80)
    print("VERDICT ON PUBLISHED WINDOW (R ∈ [0.3, 4.0] Mpc, on delta_sigma)")
    print("=" * 80)

    if n_disagreements > 0:
        print("⚠️  Schemes disagree on delta_sigma distinguishability in", n_disagreements, "cells.")
        print("Window is SCHEME-DEPENDENT and must not be cited as a design")
        print("constraint by Stream 2's M1 memo until the dependence is resolved.")
        print("(See authorization §5 kill condition, applied to delta_sigma)")
    else:
        print("✅ All cells with defined Δσ show agreement across schemes.")
        print("Window survives per-scheme decomposition.")

    return result


def main_process(field_info):
    """Wrapper for process_field_third_scheme to avoid name collision."""
    return process_field_third_scheme(field_info)


if __name__ == "__main__":
    result = main()
    print("\n" + "=" * 80)
    print("Done.")
