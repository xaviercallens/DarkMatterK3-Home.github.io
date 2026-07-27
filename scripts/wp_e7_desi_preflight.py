#!/usr/bin/env python3
"""WP-E7 — DESI DR1 resolvability pre-flight (geometry arithmetic ONLY).

Tag: `ENGINEERING`, in the WP-E4 lineage. NOT a `TEST`. NOT a `FIT`. NOT
`SANDBOX-EXPERIMENTAL`. This script makes no physics claim and runs no
comparison against real data; it decides, mechanically, whether a
deformation-scale analysis on DESI DR1 tracer samples could even be
resolvable at some r_s, before any comparison design exists.

T0 authorization: briefs/T0_DECISIONS_2026_07_27.md, decision D-a
("the resolvability pre-flight (WP-E7) is geometry arithmetic and precedes
any comparison design"). Dataset numbers are cited from
docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md §3 (arXiv:2404.03000).

What this computes, per tracer sample:
  1. A survey-mean comoving number density n = N_tracer / V_survey(zmin,zmax),
     using a standard flat-LCDM comoving-distance integral over the DESI DR1
     footprint area (stated Planck-like parameters below). This is a SURVEY
     MEAN, not a local density — footprint geometry is idealized as a single
     cone of the stated area; real fields have angular selection/masking this
     script does not model.
  2. For candidate analysis boxes (square transverse footprint x Delta z=0.1
     radial slice) and an r_s grid, the per-axis nbins required for r_s to
     span >= 1 voxel (pipeline.resolvability.required_nbins — NOT
     reimplemented), the uniform nbins a real pipeline would actually bin at
     (max over axes, matching how WP-E4's own sweep used one nbins value
     across a highly anisotropic box), the resulting mean voxel occupancy,
     and a three-tier verdict combining pipeline.resolvability's spatial
     criterion with a proposed occupancy criterion (see OCCUPANCY_THRESHOLD_*
     below — PROPOSAL, needs T0 ratification, not fixed by WP-E4 or
     resolvability.py).

Cosmology: flat LCDM, H0 = 67.4 km/s/Mpc, Omega_m = 0.315 (Planck 2018
TT,TE,EE+lowE+lensing base-LCDM headline values) -- a standard fiducial
choice, not fit to anything in this program. Uses astropy.cosmology if
installed (verified present in this environment); falls back to a manual
Simpson-rule integral of c / H(z) otherwise. Both paths are exercised and
cross-checked in pipeline/tests/test_wp_e7_desi_preflight.py.
"""
from __future__ import annotations

import json
import logging
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.resolvability import (  # noqa: E402
    required_nbins,
    resolvability,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUT_JSON = REPO_ROOT / "data" / "derived" / "wp_e7_desi_preflight_2026_07_27.json"

# ---------------------------------------------------------------------------
# Cosmology (stated parameters; flat LCDM)
# ---------------------------------------------------------------------------
H0_KM_S_MPC = 67.4
OMEGA_M = 0.315
OMEGA_DE = 1.0 - OMEGA_M
C_KM_S = 299792.458  # exact (SI definition)


def comoving_distance_astropy(z: float) -> float | None:
    """Comoving distance in Mpc via astropy.cosmology.FlatLambdaCDM, or None
    if astropy is not importable."""
    try:
        from astropy.cosmology import FlatLambdaCDM
        import astropy.units as u
    except ImportError:
        return None
    cosmo = FlatLambdaCDM(H0=H0_KM_S_MPC, Om0=OMEGA_M)
    return float(cosmo.comoving_distance(z).to(u.Mpc).value)


def comoving_distance_manual(z: float, n_steps: int = 4000) -> float:
    """Comoving distance in Mpc via direct Simpson-rule integration of
    c / H(z') dz' from 0 to z, for a flat LCDM cosmology. Used when astropy
    is unavailable, and cross-checked against astropy in the test suite."""
    if z <= 0.0:
        return 0.0
    if n_steps % 2 == 1:
        n_steps += 1  # Simpson's rule needs an even number of intervals
    zs = np.linspace(0.0, z, n_steps + 1)
    e_of_z = np.sqrt(OMEGA_M * (1.0 + zs) ** 3 + OMEGA_DE)
    integrand = 1.0 / e_of_z
    # Composite Simpson's rule
    h = z / n_steps
    s = integrand[0] + integrand[-1]
    s += 4.0 * np.sum(integrand[1:-1:2])
    s += 2.0 * np.sum(integrand[2:-2:2])
    integral = (h / 3.0) * s
    hubble_distance_mpc = C_KM_S / H0_KM_S_MPC
    return float(hubble_distance_mpc * integral)


def comoving_distance(z: float) -> tuple[float, str]:
    """Comoving distance in Mpc, preferring astropy, with the method used
    recorded so the output is self-documenting."""
    d = comoving_distance_astropy(z)
    if d is not None:
        return d, "astropy.cosmology.FlatLambdaCDM"
    return comoving_distance_manual(z), "manual Simpson-rule integral of c/H(z)"


def deg2_to_steradians(area_deg2: float) -> float:
    return area_deg2 * (math.pi / 180.0) ** 2


def cone_shell_volume_mpc3(omega_sr: float, d_near: float, d_far: float) -> float:
    """Comoving volume (Mpc^3) of a cone of solid angle omega_sr between
    comoving distances d_near and d_far, for a spatially FLAT metric (exact
    Euclidean cone-shell formula; valid because flat-LCDM comoving space is
    Euclidean)."""
    return (omega_sr / 3.0) * (d_far**3 - d_near**3)


# ---------------------------------------------------------------------------
# DESI DR1 tracer samples (docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md §3,
# citing arXiv:2404.03000). Counts and redshift ranges are the BAO/LSS
# catalog samples, not the full DR1 target list.
# ---------------------------------------------------------------------------
DESI_DR1_FOOTPRINT_DEG2 = 7500.0  # stated approx. area, arXiv:2404.03000 / 2503.14745

TRACERS = {
    "BGS": {"N": 300_017, "zmin": 0.1, "zmax": 0.4},
    "LRG": {"N": 2_138_600, "zmin": 0.4, "zmax": 1.1},
    "ELG": {"N": 2_432_022, "zmin": 0.8, "zmax": 1.6},
    "QSO": {"N": 856_652, "zmin": 0.8, "zmax": 2.1},
}

BOX_TRANSVERSE_MPC = [100.0, 200.0, 300.0, 400.0, 500.0]
RS_GRID_MPC = [2.0, 5.0, 10.0, 15.0, 20.0, 25.0]

# --- Occupancy criterion --------------------------------------------------
# pipeline/resolvability.py fixes the SPATIAL criterion (r_s must span >= 1
# voxel per axis) but does not fix an occupancy criterion. WP-E4 §4 argues
# informally that sparsity makes topology "trivial ... independent of voxel
# size" when there is far less than ~1 object per voxel; pipeline.resolvability
# also treats "less than 1 count" as a degenerate regime elsewhere
# (null_degeneracy's min_std_counts=1.0). Following that precedent:
#
#   >>> PROPOSAL — NEEDS T0 RATIFICATION <<<
#   OCCUPANCY_THRESHOLD_PRIMARY = 1.0 objects/voxel (mean).
#
# Verdicts are also computed under a 10x stricter threshold so the
# conclusion's sensitivity to this unratified number is visible, per the
# WP-E7 brief's explicit instruction.
OCCUPANCY_THRESHOLD_PRIMARY = 1.0
OCCUPANCY_THRESHOLD_STRICT = 10.0 * OCCUPANCY_THRESHOLD_PRIMARY


def classify_verdict(geometry_verdict: str, occupancy: float, threshold: float) -> str:
    """Combine the spatial (pipeline.resolvability) verdict with the
    (proposed) occupancy criterion into one three-tier verdict.

    A sub-voxel deformation is a hard stop regardless of occupancy (WP-E4
    doctrine): if the spatial verdict is not RESOLVABLE, the combined verdict
    is UNRESOLVABLE. Otherwise the occupancy criterion decides:
      occupancy >= threshold         -> RESOLVABLE
      threshold/10 <= occ < threshold -> PARTIALLY_RESOLVABLE
      occupancy < threshold/10        -> UNRESOLVABLE
    """
    if geometry_verdict != "RESOLVABLE":
        return "UNRESOLVABLE"
    if occupancy >= threshold:
        return "RESOLVABLE"
    if occupancy >= threshold / 10.0:
        return "PARTIALLY_RESOLVABLE"
    return "UNRESOLVABLE"


def analyze_tracer(name: str, spec: dict) -> dict:
    zmin, zmax, n_total = spec["zmin"], spec["zmax"], spec["N"]
    zmid = 0.5 * (zmin + zmax)

    d_min, method = comoving_distance(zmin)
    d_max, _ = comoving_distance(zmax)
    d_mid, _ = comoving_distance(zmid)

    omega_sr = deg2_to_steradians(DESI_DR1_FOOTPRINT_DEG2)
    v_survey_mpc3 = cone_shell_volume_mpc3(omega_sr, d_min, d_max)
    n_density_mpc3 = n_total / v_survey_mpc3  # survey-mean, NOT local

    def slice_depth_mpc(z0: float) -> float:
        """Radial comoving depth (Mpc) of a Delta z = 0.1 slice starting at z0."""
        d0, _ = comoving_distance(z0)
        d1, _ = comoving_distance(z0 + 0.1)
        return d1 - d0

    # Representative slice placements: shallow (zmin), mid, deep (zmax - 0.1,
    # so the slice stays inside the tracer's published range).
    z_deep_start = max(zmin, zmax - 0.1)
    slice_depths = {
        "zmin": slice_depth_mpc(zmin),
        "zmid": slice_depth_mpc(zmid),
        "zmax": slice_depth_mpc(z_deep_start),
    }

    grid = []
    for placement, radial_depth_mpc in slice_depths.items():
        for box_side in BOX_TRANSVERSE_MPC:
            extent = (box_side, box_side, radial_depth_mpc)
            v_box_mpc3 = box_side * box_side * radial_depth_mpc
            n_expected_in_box = n_density_mpc3 * v_box_mpc3
            for r_s in RS_GRID_MPC:
                req_nbins = required_nbins(r_s, extent, min_voxels=1.0)
                nbins_uniform = int(max(req_nbins))
                geom = resolvability(r_s, extent, nbins_uniform, min_voxels=1.0)
                n_voxels_total = nbins_uniform**3
                mean_occupancy = n_expected_in_box / n_voxels_total

                verdict_primary = classify_verdict(
                    geom["verdict"], mean_occupancy, OCCUPANCY_THRESHOLD_PRIMARY
                )
                verdict_strict = classify_verdict(
                    geom["verdict"], mean_occupancy, OCCUPANCY_THRESHOLD_STRICT
                )

                grid.append({
                    "slice_placement": placement,
                    "radial_depth_mpc": radial_depth_mpc,
                    "box_transverse_mpc": box_side,
                    "r_s_mpc": r_s,
                    "required_nbins_xyz": list(req_nbins),
                    "nbins_uniform": nbins_uniform,
                    "geometry_verdict": geom["verdict"],
                    "n_voxels_total": n_voxels_total,
                    "n_expected_in_box": n_expected_in_box,
                    "mean_occupancy": mean_occupancy,
                    "verdict_primary_threshold": verdict_primary,
                    "verdict_strict_threshold": verdict_strict,
                })

    return {
        "N": n_total,
        "zmin": zmin,
        "zmax": zmax,
        "zmid": zmid,
        "comoving_distance_method": method,
        "d_c_zmin_mpc": d_min,
        "d_c_zmax_mpc": d_max,
        "d_c_zmid_mpc": d_mid,
        "v_survey_mpc3": v_survey_mpc3,
        "n_density_survey_mean_mpc3": n_density_mpc3,
        "slice_depths_mpc": slice_depths,
        "grid": grid,
    }


def smallest_resolvable_rs(tracer_result: dict, verdict_key: str) -> dict:
    """Sensitivity of the "smallest resolvable r_s" answer to box-size choice.

    Box size turns out NOT to be a free, harmless choice: because a single
    uniform nbins is applied across the (transverse, transverse, radial)
    extent, the ratio of box side to r_s changes how much ceil-rounding
    over/under-resolves each axis, and small boxes (100 Mpc side against
    r_s up to 25 Mpc) are penalized relative to large ones (500 Mpc side).
    So this reports THREE numbers instead of collapsing to one:
      - conservative: smallest r_s where EVERY tested box size and slice
        placement gives this verdict (robust to box-size choice)
      - best_case: smallest r_s where AT LEAST ONE tested (box, placement)
        combination gives this verdict (optimistic; largest boxes dominate)
      - best_case_combo: which (box, placement) achieved the best_case value
    """
    by_rs: dict[float, list[tuple]] = {}
    for row in tracer_result["grid"]:
        by_rs.setdefault(row["r_s_mpc"], []).append(
            (row[verdict_key], row["box_transverse_mpc"], row["slice_placement"])
        )

    conservative = None
    for r_s in sorted(by_rs):
        verdicts = {v for v, _, _ in by_rs[r_s]}
        if verdicts == {"RESOLVABLE"}:
            conservative = r_s
            break

    best_case = None
    best_case_combo = None
    for r_s in sorted(by_rs):
        hits = [(box, placement) for v, box, placement in by_rs[r_s] if v == "RESOLVABLE"]
        if hits:
            best_case = r_s
            # Prefer reporting the largest box among the hits at this r_s.
            best_case_combo = max(hits, key=lambda bp: bp[0])
            break

    return {
        "conservative_smallest_resolvable_rs_mpc": conservative,
        "best_case_smallest_resolvable_rs_mpc": best_case,
        "best_case_box_mpc_placement": (
            {"box_transverse_mpc": best_case_combo[0], "slice_placement": best_case_combo[1]}
            if best_case_combo else None
        ),
        "note": (
            f"conservative = smallest r_s in {RS_GRID_MPC} Mpc RESOLVABLE at "
            f"EVERY box size in {BOX_TRANSVERSE_MPC} Mpc and every slice "
            "placement (zmin/zmid/zmax); best_case = smallest r_s RESOLVABLE "
            "at ANY tested (box, placement) combination. None if the grid "
            "never reaches this verdict under either condition."
        ),
    }


def main() -> int:
    logger.info(
        "WP-E7 pre-flight: geometry arithmetic only. NOT a TEST, NOT a FIT, "
        "NOT SANDBOX-EXPERIMENTAL. Cosmology: flat LCDM, H0=%.1f, Om=%.3f.",
        H0_KM_S_MPC, OMEGA_M,
    )

    results = {
        "label": "ENGINEERING (pure geometry arithmetic, no physics claim)",
        "generated": datetime.now(timezone.utc).isoformat(),
        "cosmology": {
            "H0_km_s_mpc": H0_KM_S_MPC,
            "Omega_m": OMEGA_M,
            "Omega_DE": OMEGA_DE,
            "flat": True,
        },
        "desi_dr1_footprint_deg2": DESI_DR1_FOOTPRINT_DEG2,
        "box_transverse_mpc_grid": BOX_TRANSVERSE_MPC,
        "rs_grid_mpc": RS_GRID_MPC,
        "occupancy_threshold_primary": OCCUPANCY_THRESHOLD_PRIMARY,
        "occupancy_threshold_strict": OCCUPANCY_THRESHOLD_STRICT,
        "occupancy_threshold_status": (
            "PROPOSAL — needs T0 ratification. Not fixed by WP-E4 or "
            "pipeline/resolvability.py."
        ),
        "tracers": {},
        "summary": {},
    }

    for name, spec in TRACERS.items():
        logger.info("Analyzing tracer %s ...", name)
        tracer_result = analyze_tracer(name, spec)
        results["tracers"][name] = tracer_result
        results["summary"][name] = {
            "primary_threshold": smallest_resolvable_rs(
                tracer_result, "verdict_primary_threshold"
            ),
            "strict_threshold": smallest_resolvable_rs(
                tracer_result, "verdict_strict_threshold"
            ),
        }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as f:
        json.dump(results, f, indent=2)
    logger.info("Wrote %s", OUT_JSON)

    for name in TRACERS:
        s = results["summary"][name]
        p, st = s["primary_threshold"], s["strict_threshold"]
        logger.info(
            "%s: primary threshold r_s -- conservative=%s Mpc, best_case=%s Mpc | "
            "10x-stricter threshold r_s -- conservative=%s Mpc, best_case=%s Mpc",
            name,
            p["conservative_smallest_resolvable_rs_mpc"],
            p["best_case_smallest_resolvable_rs_mpc"],
            st["conservative_smallest_resolvable_rs_mpc"],
            st["best_case_smallest_resolvable_rs_mpc"],
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
