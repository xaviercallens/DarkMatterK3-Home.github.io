#!/usr/bin/env python3
"""WP-E6b -- Lyman-alpha P1D adequacy pre-flight (ENGINEERING, no real-data
comparison). T0 decision D-e, briefs/T0_DECISIONS_2026_07_27.md.

Tag: `ENGINEERING` (WP-E7 labeling lineage). NOT `TEST`, NOT `FIT`, NOT
`SANDBOX-EXPERIMENTAL`. The statistic uses ONLY the published DESI DR1 P1D
measurement UNCERTAINTIES (data/literature/desi_dr1_lya_p1d_2026_07_27.csv)
-- the published central values are never used as a fit target; this
mechanically decides, over a grid of ultralight mass m and mixed fraction
f, whether the published measurement precision could in principle
distinguish (m, f) from f=0 under an explicitly OPTIMISTIC linear-theory
ratio forward model (pipeline/wp_e6b_lya.py) -- a pre-flight, not a result.

Grid: m in logspace(1e-22, 1e-19 eV, 13 points) x f in {0.05, 0.10, ...,
1.00} (20 points) = 260 cells (same grid as WP-E6's DES-Y6 pre-flight).

Statistic: Delta-chi2(m, f) = sum over the DESI DR1 paper's own valid (k, z)
bins of [(R(k,z;m,f) - 1) / sigma_rel(k,z)]^2, where sigma_rel is the
PUBLISHED fractional P1D measurement uncertainty. Because R is linear in f
(pipeline/wp_e6b_lya.py module docstring section 2), Delta-chi2(m,f) =
f^2 * Delta-chi2_shape(m) exactly -- computed once per mass.
"""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.wp_e6b_lya import (  # noqa: E402
    DEFAULT_DESI_DR1_P1D_CSV,
    K_MIN_VALID_SKM,
    desi_dr1_k_max_valid_skm,
    desi_dr1_validity_mask,
    k_velocity_to_comoving_mpc,
    load_desi_dr1_p1d_table,
    rho_shape_factor_cached,
    sigma_rel_from_table,
)
from scripts.wp_e6_adequacy_preflight import (  # noqa: E402
    PUBLISHED_MIXED_FDM_ANCHORS,
    pure_fdm_exclusion_status,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUT_JSON = REPO_ROOT / "data" / "derived" / "wp_e6b_lya_adequacy_preflight_2026_07_27.json"

M_EV_GRID = np.logspace(-22, -19, 13)
F_GRID = np.round(np.arange(0.05, 1.0 + 1e-9, 0.05), 2)
SIGNIFICANCE_THRESHOLDS = {"2sigma": 2.0, "3sigma": 3.0}

# Mixed-fraction anchor tolerance for matching a grid mass to a published
# Liu, Gong & Zhou 2026 anchor (1e-22, 1e-21 eV) -- the grid is constructed
# by np.logspace so these land within float noise of the anchors, not
# bit-exact; 0.5% relative tolerance comfortably separates "is this anchor"
# from "is the adjacent grid point" (grid spacing is a factor of 10^0.25
# =~78% apart).
MIXED_ANCHOR_REL_TOL = 0.005


def mixed_fdm_bound_at_mass(m_ev: float) -> dict | None:
    """Published mixed-fraction bound (Liu, Gong & Zhou 2026) if m_ev
    matches one of their anchor masses (1e-22: f<0.12; 1e-21: f<0.65) within
    MIXED_ANCHOR_REL_TOL; else None (no published mixed constraint reaches
    this mass -- 'unconstrained higher', docs/DATA_LANDSCAPE_RESEARCH_
    2026_07_27.md Sec.4)."""
    for anchor in PUBLISHED_MIXED_FDM_ANCHORS:
        if anchor["m_ev"] <= 0:
            continue
        rel_diff = abs(m_ev - anchor["m_ev"]) / anchor["m_ev"]
        if rel_diff < MIXED_ANCHOR_REL_TOL:
            return anchor
    return None


def genuinely_open_cell(m_ev: float, f: float, pure_excluded: bool) -> dict:
    """Is (m, f) genuinely open per the PUBLISHED landscape (independent of
    this pre-flight's own reachability)? Two disjoint published-constraint
    axes apply depending on f:

      - f == 1.0 (pure FDM): governed by the pure-FDM lower-bound status
        (pure_fdm_exclusion_status, corrected direction -- see
        docs/WP_E6_SYNTHETIC_ADEQUACY_PREFLIGHT_2026_07_27.md's correction
        note). In THIS grid (1e-22-1e-19 eV) every mass is pure-FDM
        excluded (May, Dalal & Kravtsov 2025's 8e-18 eV UFD bound covers the
        whole grid), so f=1.0 is never open here.
      - f < 1.0: governed by the published MIXED-fraction bound (Liu, Gong
        & Zhou 2026) if this mass is one of their anchors (1e-22: f<0.12;
        1e-21: f<0.65); otherwise no published mixed constraint applies and
        the cell is open by default ('unconstrained higher').
    """
    if f >= 1.0:
        return {"open": not pure_excluded, "governing_constraint": "pure_fdm_bound"}
    anchor = mixed_fdm_bound_at_mass(m_ev)
    if anchor is not None:
        return {
            "open": f < anchor["f_fdm_bound"],
            "governing_constraint": f"mixed_fdm_bound ({anchor['citation']}, "
                                     f"f<{anchor['f_fdm_bound']} at m={anchor['m_ev']:.0e} eV)",
        }
    return {"open": True, "governing_constraint": "none published (unconstrained)"}


def optimism_calibration_vs_published_anchors(columns: dict) -> list[dict]:
    """How far this OPTIMISTIC linear-theory proxy sits from the published,
    emulator-based analysis that produced the mixed-fraction bounds.

    For each Liu, Gong & Zhou 2026 anchor mass that is also a grid mass,
    evaluate THIS pre-flight's own sigma_equiv exactly AT the published 95%
    upper bound on f. A forward model of comparable fidelity to the one
    behind that bound would land near this pre-flight's own decision
    threshold (sigma_equiv = 2); the ratio

        overstatement = sigma_equiv(f = f_bound) / 2

    is therefore a mechanical, in-artifact measure of how much the
    linear-theory ratio proxy OVERSTATES reachability. It is a diagnostic of
    THIS proxy only -- it makes no claim about the published analysis, and
    the identification of a 95% CL bound with this pre-flight's 2-sigma_equiv
    threshold is a deliberately generous convention (a one-sided 95% limit is
    nearer 1.64 sigma, which would make the ratio LARGER, not smaller).
    """
    calibration = []
    for anchor in PUBLISHED_MIXED_FDM_ANCHORS:
        for col in columns.values():
            rel_diff = abs(col["m_ev"] - anchor["m_ev"]) / anchor["m_ev"]
            if rel_diff >= MIXED_ANCHOR_REL_TOL:
                continue
            f_bound = anchor["f_fdm_bound"]
            sigma_at_bound = f_bound * col["sigma_shape"]
            calibration.append({
                "m_ev": col["m_ev"],
                "published_f_fdm_bound": f_bound,
                "citation": anchor["citation"],
                "proxy_sigma_equiv_at_published_bound": sigma_at_bound,
                "overstatement_factor_vs_2sigma": sigma_at_bound / 2.0,
            })
    return calibration


def run_grid(csv_path: Path | str | None = None,
             table: dict | None = None,
             m_ev_grid: np.ndarray | None = None,
             f_grid: np.ndarray | None = None) -> dict:
    """Run the (m, f) adequacy grid.

    `table` (a dict as returned by load_desi_dr1_p1d_table) and the two grid
    overrides exist so pipeline/tests/test_wp_e6b_lya.py can drive this
    function END-TO-END under injected conditions (zero suppression,
    inflated/scrambled/degenerate published errors, all-invalid k range) at
    a tractable cost. Defaults reproduce the filed artifact exactly.
    """
    if table is None:
        table = load_desi_dr1_p1d_table(csv_path)
    m_ev_grid = M_EV_GRID if m_ev_grid is None else np.asarray(m_ev_grid, dtype=np.float64)
    f_grid = F_GRID if f_grid is None else np.asarray(f_grid, dtype=np.float64)
    valid_mask = desi_dr1_validity_mask(table["z"], table["k_s_per_km"])
    z_valid = table["z"][valid_mask]
    k_skm_valid = table["k_s_per_km"][valid_mask]
    k_mpc_valid = k_velocity_to_comoving_mpc(k_skm_valid, z_valid)
    sigma_rel_valid = sigma_rel_from_table(table)[valid_mask]

    n_total_bins = len(table["z"])
    n_valid_bins = int(valid_mask.sum())

    columns = {}
    decisive_cells = []  # reachable (>=2sigma) AND genuinely open
    for m_ev in m_ev_grid:
        m22 = m_ev / 1e-22
        # rho(k,z;m) at every valid bin, then Delta-chi2_shape(m) once.
        rho = np.array([
            rho_shape_factor_cached(k_mpc, m22) for k_mpc in k_mpc_valid
        ])
        chi2_shape = float(np.sum((rho / sigma_rel_valid) ** 2))
        sigma_shape = float(np.sqrt(chi2_shape))

        pure_status = pure_fdm_exclusion_status(m_ev)
        cells = []
        smallest_f_2sigma = None
        smallest_f_3sigma = None
        for f in f_grid:
            sigma_equiv = float(f) * sigma_shape
            delta_chi2 = sigma_equiv**2
            reaches_2sigma = sigma_equiv >= SIGNIFICANCE_THRESHOLDS["2sigma"]
            reaches_3sigma = sigma_equiv >= SIGNIFICANCE_THRESHOLDS["3sigma"]
            if reaches_2sigma and smallest_f_2sigma is None:
                smallest_f_2sigma = float(f)
            if reaches_3sigma and smallest_f_3sigma is None:
                smallest_f_3sigma = float(f)

            openness = genuinely_open_cell(float(m_ev), float(f), pure_status["excluded"])
            is_decisive = reaches_2sigma and openness["open"]
            if is_decisive:
                decisive_cells.append({
                    "m_ev": float(m_ev), "f": float(f),
                    "sigma_equiv": sigma_equiv,
                    "governing_constraint": openness["governing_constraint"],
                })

            cells.append({
                "f": float(f),
                "delta_chi2": delta_chi2,
                "sigma_equiv": sigma_equiv,
                "reaches_2sigma": reaches_2sigma,
                "reaches_3sigma": reaches_3sigma,
                "genuinely_open": openness["open"],
                "governing_constraint": openness["governing_constraint"],
            })

        columns[f"{m_ev:.4e}"] = {
            "m_ev": float(m_ev),
            "m22": float(m22),
            "chi2_shape": chi2_shape,
            "sigma_shape": sigma_shape,
            "pure_fdm_exclusion": pure_status,
            "smallest_f_reaching_2sigma": smallest_f_2sigma,
            "smallest_f_reaching_3sigma": smallest_f_3sigma,
            "cells": cells,
        }

    return {
        "label": "ENGINEERING (linear-theory Lya P1D ratio pre-flight, published "
                  "error bars, no real-data COMPARISON -- optimistic proxy, see "
                  "module docstring caveats)",
        "generated": datetime.now(timezone.utc).isoformat(),
        "grid": {
            "m_ev": m_ev_grid.tolist(),
            "f": f_grid.tolist(),
            "n_cells": int(m_ev_grid.size * f_grid.size),
        },
        "data_source": {
            "csv": str(Path(csv_path) if csv_path is not None else DEFAULT_DESI_DR1_P1D_CSV),
            "citation": "DESI DR1 Lyman-alpha 1D flux power spectrum, baseline QMLE, "
                        "arXiv:2505.07974, via Zenodo DOI 10.5281/zenodo.16943723 "
                        "(data/MANIFEST.md provenance entry)",
            "n_total_bins": n_total_bins,
            "n_valid_bins": n_valid_bins,
            "validity_range": f"k_par > {K_MIN_VALID_SKM} s/km and "
                               f"k_par < 0.5*pi/R_z(z) (paper's own recommended cuts)",
        },
        "published_mixed_fdm_anchors": PUBLISHED_MIXED_FDM_ANCHORS,
        "columns": columns,
        "optimism_calibration_vs_published_anchors":
            optimism_calibration_vs_published_anchors(columns),
        "decisive_cells_reachable_and_open": decisive_cells,
        "n_decisive_cells": len(decisive_cells),
    }


def summarize(results: dict) -> list[str]:
    lines = []
    for key, col in results["columns"].items():
        pure = "EXCLUDED" if col["pure_fdm_exclusion"]["excluded"] else "OPEN"
        s2 = col["smallest_f_reaching_2sigma"]
        s3 = col["smallest_f_reaching_3sigma"]
        lines.append(
            f"m={col['m_ev']:.3e} eV | sigma_shape(f=1)={col['sigma_shape']:.4f} | "
            f"pure-FDM: {pure:8s} | smallest f -> 2sigma: {s2!s:>5} | "
            f"3sigma: {s3!s:>5}"
        )
    lines.append(f"Decisive (reachable AND genuinely open) cells: {results['n_decisive_cells']}")
    for cal in results.get("optimism_calibration_vs_published_anchors", []):
        lines.append(
            f"OPTIMISM CALIBRATION m={cal['m_ev']:.3e} eV: published bound "
            f"f<{cal['published_f_fdm_bound']} -> this proxy assigns "
            f"sigma_equiv={cal['proxy_sigma_equiv_at_published_bound']:.1f} there, "
            f"{cal['overstatement_factor_vs_2sigma']:.1f}x this pre-flight's own "
            f"2-sigma threshold"
        )
    return lines


def main() -> int:
    logger.info(
        "WP-E6b Lya P1D adequacy pre-flight: ENGINEERING, published-error-bar "
        "linear-theory ratio arithmetic only. NOT a TEST, NOT a FIT. Grid: "
        "%d masses x %d fractions = %d cells.",
        M_EV_GRID.size, F_GRID.size, M_EV_GRID.size * F_GRID.size,
    )

    results = run_grid()

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as fh:
        json.dump(results, fh, indent=2)
    logger.info("Wrote %s", OUT_JSON)

    for line in summarize(results):
        logger.info(line)

    return 0


if __name__ == "__main__":
    sys.exit(main())
