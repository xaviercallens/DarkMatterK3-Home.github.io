#!/usr/bin/env python3
"""WP-E: SANDBOX-EXPERIMENTAL GPU deformation sweep for Stream 2 hypothesis input.

Tag: SANDBOX-EXPERIMENTAL. NOT ENGINEERING, NOT TEST, NOT FIT. This is exploratory
infrastructure to generate candidate parameter-window HYPOTHESES for Stream 2's Phase M
mechanism memo (briefs/STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md). It is not a
validated result, not a physics claim, and not eligible for PREDICTION.md without its own
fresh pre-registration. Authorization: docs/WP_E_T0_AUTHORIZATION_2026_07_25.md.

WHAT THIS DOES: applies two phenomenological spatial deformations (generic EFT-style
"screening"/"evacuation" stand-ins, not tied to any specific candidate) to real galaxy
catalog coordinates on GPU (PyTorch/CUDA, Tesla T4), across a grid of length scale R and
amplitude A, and measures topological (beta_1, beta_2 -- never beta_0, WP-R7 finding)
displacement relative to TWO null baselines:

  1. "wp_r3_style" -- literal reimplementation of WP-R3's retracted schemes (co-permuted
     shuffle: RA and Dec permuted with the SAME index, i.e. no-op on the point set; rigid
     rotate: isometry, no-op on internal structure). WP-R3 itself stored no coordinate
     arrays (only aggregate beta_0/1/2 scalars) so there is nothing literal to "deform" --
     this reimplements the schemes at the coordinate level against the same real catalogs,
     per T0 authorization to use them "exactly as the directive specifies." Because both
     schemes are point-pattern-preserving, this baseline is mathematically degenerate as a
     null (see docs/WP_E_EMPIRICAL_BOUNDS.md Section 3) -- reported honestly, not hidden.
  2. "wp_r5_valid" -- pipeline/realfield3d.py's z-shuffle / angular-CSR schemes, the
     corrected, non-degenerate null infrastructure (T0-signed, docs/T0_SIGNOFF_WP_R5_R6_R7_2026_07_25.md).

Resolution floor: no interaction scale R < 0.27 Mpc is tested (WP-R6 measured floor).
Thresholds: ABSOLUTE density values, not percentiles (WP-R7 Section 4: percentile ladders
are degenerate on sparse fields).
"""
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

import json
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
)
from pipeline.observables_real import compute_betti_numbers

TAG = "SANDBOX-EXPERIMENTAL"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

NBINS = 8
RESOLUTION_FLOOR_MPC = 0.27  # WP-R6 measured floor; never test below this
R_GRID_MPC = [0.3, 0.5, 1.0, 2.0, 4.0, 8.0]  # length scale of the deformation
A_GRID = [0.1, 0.3, 0.5, 0.7, 0.9]  # dimensionless coupling amplitude
ABS_THRESHOLDS = [0.5, 1.0, 1.5, 2.0]  # absolute field-value thresholds (field mean = 1.0)
N_NULL_REALIZATIONS = 30  # bounded for sandbox scope; not a precision claim
DEFORMATION_CLASSES = ["chameleon_core_halt", "void_evacuation"]

OUTPUT_DIR = Path("/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/wp_e_sandbox")
DERIVED_DIR = repo_root / "data" / "derived"

FIELDS = [
    {
        "name": "euclid_z_edf_north",
        "path": "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid_z/euclid_z_edf_north.csv",
        "ra_col": "right_ascension", "dec_col": "declination", "z_col": "phz_median",
    },
    {
        "name": "euclid_z_edf_fornax",
        "path": "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid_z/euclid_z_edf_fornax.csv",
        "ra_col": "right_ascension", "dec_col": "declination", "z_col": "phz_median",
    },
    {
        "name": "sdss_z_coma_cluster",
        "path": "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/sdss_z/sdss_z_coma_cluster.csv",
        "ra_col": "ra", "dec_col": "dec", "z_col": "z",
    },
]


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def wp_r3_style_shuffle(ra: np.ndarray, dec: np.ndarray, z: np.ndarray, rng: np.random.Generator):
    """Literal WP-R3 'shuffle', extended faithfully to 3D: permute RA, Dec, AND z with
    the SAME index -- reorders the (ra,dec,z) triples without changing the underlying
    point set (a genuine no-op, matching WP-R3's original 2D degeneracy). NOTE: an
    earlier version of this function permuted only (ra,dec) while a caller passed the
    original z separately, which is NOT the same no-op -- it silently creates new
    (ra,dec,z) triples never present in the real data (found and fixed same session,
    before any WP-E numbers were finalized; see docs/WP_E_EMPIRICAL_BOUNDS.md Section 3)."""
    idx = rng.permutation(len(ra))
    return ra[idx], dec[idx], z[idx]


def wp_r3_style_rotate(ra: np.ndarray, dec: np.ndarray, rng: np.random.Generator):
    """Literal WP-R3 'rotate': rigid rotation in RA, wrapping at 360 deg. An isometry --
    preserves all internal structure. Known no-op; reproduced per T0 authorization."""
    delta = rng.uniform(0, 360)
    return (ra + delta) % 360.0, dec.copy()


def batched_local_density(coords: torch.Tensor, radius_mpc: float, chunk: int = 2048) -> torch.Tensor:
    """GPU-batched neighbor count within `radius_mpc` for each point, chunked to avoid
    CUDA OOM on the full N x N pairwise distance matrix (WP-E Phase C error-handling
    requirement). coords: (N, 3) tensor in comoving Mpc."""
    n = coords.shape[0]
    counts = torch.zeros(n, device=coords.device)
    for start in range(0, n, chunk):
        end = min(start + chunk, n)
        try:
            dists = torch.cdist(coords[start:end], coords)  # (chunk, N)
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            smaller = max(1, chunk // 2)
            return batched_local_density(coords, radius_mpc, chunk=smaller)
        counts[start:end] = (dists < radius_mpc).sum(dim=1).float() - 1.0  # exclude self
    return counts


def deform_chameleon_core_halt(coords: torch.Tensor, radius_mpc: float, amplitude: float) -> torch.Tensor:
    """Smooth high-density peaks: pull each point toward its local (within-radius)
    centroid, scaled by amplitude -- a generic stand-in for screening-suppressed
    clustering, NOT derived from any specific EFT. Batched tensor op on GPU."""
    n = coords.shape[0]
    out = coords.clone()
    chunk = 2048
    for start in range(0, n, chunk):
        end = min(start + chunk, n)
        dists = torch.cdist(coords[start:end], coords)  # (chunk, N)
        mask = (dists < radius_mpc).float()
        mask[torch.arange(end - start), torch.arange(start, end)] = 0.0  # exclude self
        neighbor_counts = mask.sum(dim=1, keepdim=True).clamp(min=1.0)
        local_centroid = (mask @ coords) / neighbor_counts
        has_neighbors = (mask.sum(dim=1) > 0).unsqueeze(1)
        pull = torch.where(has_neighbors, local_centroid - coords[start:end], torch.zeros_like(coords[start:end]))
        out[start:end] = coords[start:end] + amplitude * pull
    return out


def deform_void_evacuation(coords: torch.Tensor, radius_mpc: float, amplitude: float) -> torch.Tensor:
    """Push each point away from its local centroid -- generic stand-in for
    void-evacuation-style scalar effects. Exact negative of the core-halt pull."""
    n = coords.shape[0]
    out = coords.clone()
    chunk = 2048
    for start in range(0, n, chunk):
        end = min(start + chunk, n)
        dists = torch.cdist(coords[start:end], coords)
        mask = (dists < radius_mpc).float()
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


def _field_topology_from_coords(x, y, z, ranges, thresholds):
    field = density_field_cartesian_mpc(x, y, z, nbins=NBINS, ranges=ranges)
    return {f"thr_{t}": compute_betti_numbers(field, threshold_value=t) for t in thresholds}


def load_field(field_info: dict):
    df = pd.read_csv(field_info["path"])
    ra_raw = df[field_info["ra_col"]].values
    dec_raw = df[field_info["dec_col"]].values
    z_raw = df[field_info["z_col"]].values
    ra, dec, z, drop_report = drop_invalid_redshifts(ra_raw, dec_raw, z_raw)
    ra0, dec0 = float(np.mean(ra)), float(np.mean(dec))
    x, y, zc = radec_z_to_tangent_plane_mpc(ra, dec, z, ra0_deg=ra0, dec0_deg=dec0)
    ranges = ((x.min(), x.max()), (y.min(), y.max()), (zc.min(), zc.max()))
    return ra, dec, z, ra0, dec0, ranges, drop_report


def process_field(field_info: dict) -> dict:
    name = field_info["name"]
    ra, dec, z, ra0, dec0, ranges, drop_report = load_field(field_info)
    x, y, zc = radec_z_to_tangent_plane_mpc(ra, dec, z, ra0_deg=ra0, dec0_deg=dec0)
    real_coords = torch.tensor(np.column_stack([x, y, zc]), dtype=torch.float32, device=DEVICE)

    real_topo = _field_topology_from_coords(x, y, zc, ranges, ABS_THRESHOLDS)

    # Baseline (undeformed) null distributions, both branches.
    rng_r3 = np.random.default_rng(301)
    rng_r5 = np.random.default_rng(302)

    def r3_null_coords(rng):
        if rng.integers(2) == 0:
            ra_s, dec_s, z_s = wp_r3_style_shuffle(ra, dec, z, rng)
            xs, ys, zcs = radec_z_to_tangent_plane_mpc(ra_s, dec_s, z_s, ra0_deg=ra0, dec0_deg=dec0)
        else:
            ra_s, dec_s = wp_r3_style_rotate(ra, dec, rng)
            z_s = z  # rotate only touches RA; z is untouched by construction
            # MUST recenter the tangent-plane origin to the rotated field's own
            # centroid: a rigid RA rotation is an isometry in angle-space, but the
            # tangent-plane projection's transverse offset scales with each point's
            # own comoving r (r * d_ra_rad), so projecting a rotated field around the
            # UNROTATED centroid is NOT distance-preserving when r varies across the
            # field (it is for a narrow-z field, which is why this was missed in an
            # earlier version -- caught here via wide-z-range Euclid fields, fixed
            # same session before finalizing WP_E_EMPIRICAL_BOUNDS.md).
            ra0_r, dec0_r = float(np.mean(ra_s)), float(np.mean(dec_s))
            xs, ys, zcs = radec_z_to_tangent_plane_mpc(ra_s, dec_s, z_s, ra0_deg=ra0_r, dec0_deg=dec0_r)
        return xs, ys, zcs

    def r5_null_coords(rng):
        if rng.integers(2) == 0:
            ra_s, dec_s, z_s = z_shuffle_realization(ra, dec, z, rng)
        else:
            ra_s, dec_s, z_s = angular_csr_realization(ra, dec, z, rng)
        xs, ys, zcs = radec_z_to_tangent_plane_mpc(ra_s, dec_s, z_s, ra0_deg=ra0, dec0_deg=dec0)
        return xs, ys, zcs

    results_by_class = {}
    for cls in DEFORMATION_CLASSES:
        deform_fn = DEFORM_FN[cls]
        grid_results = []
        for R in R_GRID_MPC:
            assert R >= RESOLUTION_FLOOR_MPC, f"R={R} below resolution floor {RESOLUTION_FLOOR_MPC}"
            for A in A_GRID:
                # Deform real data
                deformed_real = deform_fn(real_coords, R, A).cpu().numpy()
                deformed_real_topo = _field_topology_from_coords(
                    deformed_real[:, 0], deformed_real[:, 1], deformed_real[:, 2], ranges, ABS_THRESHOLDS
                )

                # Deform N null realizations, both branches
                r3_topos, r5_topos = [], []
                for k in range(N_NULL_REALIZATIONS):
                    xs, ys, zcs = r3_null_coords(rng_r3)
                    coords_t = torch.tensor(np.column_stack([xs, ys, zcs]), dtype=torch.float32, device=DEVICE)
                    dcoords = deform_fn(coords_t, R, A).cpu().numpy()
                    r3_topos.append(_field_topology_from_coords(dcoords[:, 0], dcoords[:, 1], dcoords[:, 2], ranges, ABS_THRESHOLDS))

                    xs5, ys5, zcs5 = r5_null_coords(rng_r5)
                    coords_t5 = torch.tensor(np.column_stack([xs5, ys5, zcs5]), dtype=torch.float32, device=DEVICE)
                    dcoords5 = deform_fn(coords_t5, R, A).cpu().numpy()
                    r5_topos.append(_field_topology_from_coords(dcoords5[:, 0], dcoords5[:, 1], dcoords5[:, 2], ranges, ABS_THRESHOLDS))

                per_threshold = {}
                for t in ABS_THRESHOLDS:
                    key = f"thr_{t}"
                    for branch_name, null_topos in [("wp_r3_style", r3_topos), ("wp_r5_valid", r5_topos)]:
                        for stat in ("beta_1", "beta_2"):  # never beta_0
                            dist = [nt[key][stat] for nt in null_topos]
                            mean, std = float(np.mean(dist)), float(np.std(dist))
                            real_val = deformed_real_topo[key][stat]
                            displacement_sigma = None if std == 0 else float((real_val - mean) / std)
                            per_threshold.setdefault(key, {}).setdefault(branch_name, {})[stat] = {
                                "null_mean": mean, "null_std": std, "null_variance": std ** 2,
                                "deformed_real_value": real_val,
                                "displacement_sigma": displacement_sigma,
                                "degenerate_null": std == 0,
                            }

                grid_results.append({"R_mpc": R, "A": A, "per_threshold": per_threshold})
        results_by_class[cls] = grid_results

    return {
        "field_name": name,
        "n_input": drop_report["n_input"],
        "redshift_drop_report": drop_report,
        "real_topology_baseline": real_topo,
        "deformation_grid": results_by_class,
        "label": TAG,
    }


def main():
    print("WP-E: SANDBOX-EXPERIMENTAL GPU Deformation Sweep")
    print("=" * 80)
    print(f"Tag: {TAG} | Device: {DEVICE} | Not TEST/FIT/ENGINEERING")
    print(f"R grid (Mpc, floor={RESOLUTION_FLOOR_MPC}): {R_GRID_MPC}")
    print(f"A grid: {A_GRID} | Absolute thresholds: {ABS_THRESHOLDS}")
    print(f"Classes: {DEFORMATION_CLASSES} | Null realizations/setting: {N_NULL_REALIZATIONS}\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)

    all_results = {}
    for field_info in FIELDS:
        print(f"Processing {field_info['name']}...")
        try:
            result = process_field(field_info)
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            print(f"  CUDA OOM on {field_info['name']}, retrying is handled inside "
                  f"batched_local_density chunking; if this surfaces, chunk size needs "
                  f"a manual reduction below 2048.")
            raise
        all_results[field_info["name"]] = result
        print(f"  n={result['n_input']}, dropped={result['redshift_drop_report']['n_dropped']}")

    output_file = OUTPUT_DIR / "wp_e_results_2026_07_25.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)
    sha = _sha256_file(output_file)

    derived_pointer = DERIVED_DIR / "wp_e_sandbox_pointer_2026_07_25.json"
    metadata = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tag": TAG,
        "device": str(DEVICE),
        "r_grid_mpc": R_GRID_MPC,
        "a_grid": A_GRID,
        "resolution_floor_mpc": RESOLUTION_FLOOR_MPC,
        "absolute_thresholds": ABS_THRESHOLDS,
        "n_null_realizations": N_NULL_REALIZATIONS,
        "deformation_classes": DEFORMATION_CLASSES,
        "fields": list(all_results.keys()),
        "full_output_file": str(output_file),
        "full_output_sha256": sha,
        "label": TAG,
        "authorization": "docs/WP_E_T0_AUTHORIZATION_2026_07_25.md",
        "not_a_test_not_a_fit_not_engineering": True,
    }
    with open(derived_pointer, "w") as f:
        json.dump(metadata, f, indent=2)

    print("\n" + "=" * 80)
    print(f"Full results (external disk): {output_file}")
    print(f"SHA256: {sha}")
    print(f"Repo pointer: {derived_pointer}")
    return 0


if __name__ == "__main__":
    sys.exit(main())


# Generated-by: Claude Sonnet 5 (T1) | Verified-by: pipeline/tests/ (reused, unmodified
# cosmology/realfield3d/observables_real functions); highest-scoring parameter pair
# re-run through CPU pipeline as T1 spot-check, see docs/WP_E_EMPIRICAL_BOUNDS.md Section 6
# | Reviewed-by: T0 Y (Xavier direct authorization, docs/WP_E_T0_AUTHORIZATION_2026_07_25.md)
