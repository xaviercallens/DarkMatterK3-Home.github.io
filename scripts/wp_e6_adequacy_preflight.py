#!/usr/bin/env python3
"""WP-E6 — synthetic adequacy pre-flight (ENGINEERING, no real data).

Tag: `ENGINEERING` — synthetic-data arithmetic (Fisher/Delta-chi^2
distinguishability on a toy forward model), in the WP-E7 labeling lineage
(docs/WP_E7_DESI_RESOLVABILITY_PREFLIGHT_2026_07_27.md). NOT `TEST`, NOT
`FIT`, NOT `SANDBOX-EXPERIMENTAL`: no real data is read anywhere in this
script (CLAUDE.md rule 1 -- no real-data comparison code before PREDICTION
v2 is pinned). This decides, mechanically, over a grid of ultralight mass m
and mixed fraction f, whether a DES-Y6-like survey could in principle tell a
given (m, f) apart from f=0 (no ultralight component) under the toy forward
model in pipeline/wp_e6_sweep.py -- a pre-flight, not a result.

T0 authorization: briefs/T0_DECISIONS_2026_07_27.md D-b (mixed-fraction
framing, T1-delegated ruling) and D-c (DES Y6). Framing per
briefs/WP_E6_PHENO_SWEEP_PROPOSAL_2026_07_27.md + its Addendum: pure-FDM
(f=1) exclusion is already public across the grid (Lya-forest, UFD
kinematics); the open question is where MIXED fractions f < 1 remain
unconstrained, which is why every grid cell also carries the published
pure-FDM exclusion status alongside the synthetic distinguishability.

Grid: m in logspace(1e-22, 1e-19 eV, 13 points) x f in {0.05, 0.10, ...,
1.00} (20 points) = 260 cells.

Statistic: a diagonal Fisher/Delta-chi^2 distance between the (m, f) model
band powers and the f=0 baseline, under the Knox-formula Gaussian covariance
computed at the BASELINE (f=0) spectrum (not at each cell -- the covariance
of a survey does not depend on which hypothesis is true, only on what it
actually measures, which is dominated by shape noise here; see caveats in
the accompanying report). Reported as an "equivalent sigma" =
sqrt(Delta-chi^2): EXACT for one degree of freedom, and used here as a
DELIBERATELY ROUGH combined-significance proxy across the several ell bands
(no attempt is made to invert the multi-dof chi^2 distribution to an exact
tail probability) -- adequate for ordering cells, not for a publication-grade
significance.
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

from pipeline.wp_e6_sweep import (  # noqa: E402
    DES_Y6_AREA_DEG2,
    DES_Y6_N_EFF_ARCMIN2,
    DES_Y6_SIGMA_E,
    des_y6_synthetic_convergence_bandpowers,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUT_JSON = REPO_ROOT / "data" / "derived" / "wp_e6_adequacy_preflight_2026_07_27.json"

# ---------------------------------------------------------------------------
# Grid (task spec: m in logspace(-22,-19 eV, >=13 pts) x f in {0.05..1.0})
# ---------------------------------------------------------------------------
M_EV_GRID = np.logspace(-22, -19, 13)
F_GRID = np.round(np.arange(0.05, 1.0 + 1e-9, 0.05), 2)
ELL_BANDS = np.array([100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0])

SIGNIFICANCE_THRESHOLDS = {"2sigma": 2.0, "3sigma": 3.0}

# ---------------------------------------------------------------------------
# Published pure-FDM (f=1) exclusion bounds, docs/DATA_LANDSCAPE_RESEARCH_
# 2026_07_27.md Sec.4. A grid mass m is "pure-FDM excluded" if it exceeds
# the LOWEST (most inclusive) threshold below that applies to it. Sources
# and their stated mass thresholds, ascending:
# ---------------------------------------------------------------------------
PURE_FDM_EXCLUSION_BOUNDS = [
    {
        "m_ev_threshold": 1.9e-21,
        "citation": "Liu, Gong & Zhou 2026 (arXiv:2606.06969)",
        "method": "Lyman-alpha P1D z=4.2-5.0, pure FDM, 95% CL",
    },
    {
        "m_ev_threshold": 2e-20,
        "citation": "Rogers & Peiris 2021 (PRL 126, 071302)",
        "method": "Lyman-alpha forest (high-res + emulator), 95% CL",
    },
    {
        "m_ev_threshold": 3e-19,
        "citation": "Dalal & Kravtsov 2022 (arXiv:2203.05750)",
        "method": "UFD sizes + stellar kinematics (Segue 1/2), 99% CL",
    },
    {
        "m_ev_threshold": 8e-18,
        "citation": "May, Dalal & Kravtsov 2025 (arXiv:2509.02781)",
        "method": "UFD kinematics (Ursa Major III/UNIONS I), 95% CL",
    },
]

# Published MIXED-fraction bounds at specific anchor masses (same source,
# Liu, Gong & Zhou 2026) -- NOT interpolated onto the grid; reported
# alongside the nearest grid mass for context only (task instruction is to
# mark PURE-FDM status per m column; this is additional context, kept out
# of the mechanical per-cell computation).
PUBLISHED_MIXED_FDM_ANCHORS = [
    {"m_ev": 1e-23, "f_fdm_bound": 0.07, "citation": "Liu, Gong & Zhou 2026 (arXiv:2606.06969)"},
    {"m_ev": 1e-22, "f_fdm_bound": 0.12, "citation": "Liu, Gong & Zhou 2026 (arXiv:2606.06969)"},
    {"m_ev": 1e-21, "f_fdm_bound": 0.65, "citation": "Liu, Gong & Zhou 2026 (arXiv:2606.06969)"},
]


def pure_fdm_exclusion_status(m_ev: float) -> dict:
    """Published pure-FDM (f=1) exclusion status at mass m_ev, per the
    docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md Sec.4 bound list. Excluded
    if m_ev exceeds the LOWEST applicable threshold (the most constraining
    published bound, since a higher-mass-only bound cannot be evaded by a
    tighter one that already excludes a lower mass)."""
    applicable = [b for b in PURE_FDM_EXCLUSION_BOUNDS if m_ev > b["m_ev_threshold"]]
    if not applicable:
        return {
            "excluded": False,
            "note": "not excluded by any published pure-FDM bound in the "
                    "landscape survey -- genuinely open even at f=1",
            "excluded_by": [],
        }
    return {
        "excluded": True,
        "note": f"excluded by {len(applicable)} published pure-FDM bound(s)",
        "excluded_by": [
            {"citation": b["citation"], "method": b["method"],
             "m_ev_threshold": b["m_ev_threshold"]}
            for b in applicable
        ],
    }


def delta_chi2_vs_baseline(c_ell_model: np.ndarray, c_ell_baseline: np.ndarray,
                            cov_diag_baseline: np.ndarray) -> float:
    """Diagonal Delta-chi^2 between a model band-power vector and the f=0
    baseline, under the baseline's own Knox-formula covariance (see module
    docstring for why the covariance is evaluated at the baseline, not at
    each cell)."""
    diff = np.asarray(c_ell_model) - np.asarray(c_ell_baseline)
    return float(np.sum(diff**2 / np.asarray(cov_diag_baseline)))


def area_scaling_sensitivity_check(m22_best_case: float = 1.0, f: float = 1.0) -> dict:
    """How far the best-case in-grid cell (lightest mass, f=1) is from 2sigma
    if the survey area were scaled up, holding n_eff and sigma_e fixed
    (Knox-formula covariance scales as 1/area, so Delta-chi2 scales
    approximately as area at fixed signal). This is a mechanical re-run of
    the forward model at larger DES_Y6_AREA_DEG2 values -- not a claim about
    any real survey -- included so the report's "even full-sky would not
    reach 2sigma" sentence traces to a computed number in this artifact
    rather than to an unverified scaling argument.
    """
    import pipeline.wp_e6_sweep as sweep_module

    original_area = sweep_module.DES_Y6_AREA_DEG2
    full_sky_deg2 = 4.0 * np.pi * (180.0 / np.pi) ** 2  # exact, 4pi sr in deg^2

    areas_deg2 = [original_area, 20_000.0, full_sky_deg2, 100_000.0]
    rows = []
    try:
        for area in areas_deg2:
            sweep_module.DES_Y6_AREA_DEG2 = area
            baseline = sweep_module.des_y6_synthetic_convergence_bandpowers(
                m22=None, f=0.0, ell_bands=ELL_BANDS
            )
            model = sweep_module.des_y6_synthetic_convergence_bandpowers(
                m22=m22_best_case, f=f, ell_bands=ELL_BANDS
            )
            dchi2 = delta_chi2_vs_baseline(
                np.asarray(model["c_ell"]), np.asarray(baseline["c_ell"]),
                np.asarray(baseline["cov_diag"]),
            )
            rows.append({
                "area_deg2": area,
                "is_des_y6_actual_area": area == original_area,
                "is_full_sky": area == full_sky_deg2,
                "sigma_equiv": float(np.sqrt(dchi2)),
            })
    finally:
        sweep_module.DES_Y6_AREA_DEG2 = original_area

    return {
        "note": (
            "Best-case in-grid cell (m=1e-22 eV, f=1.0) sigma_equiv as a "
            "function of survey area, holding n_eff and sigma_e fixed at "
            "the DES Y6 values -- illustrates how much of the non-detection "
            "is attributable to area alone vs. the intrinsic smallness of "
            "the FDM-induced signal at these (m, ell) combinations."
        ),
        "m22": m22_best_case,
        "f": f,
        "rows": rows,
    }


def run_grid() -> dict:
    baseline = des_y6_synthetic_convergence_bandpowers(m22=None, f=0.0, ell_bands=ELL_BANDS)
    c_ell_baseline = np.asarray(baseline["c_ell"])
    cov_diag_baseline = np.asarray(baseline["cov_diag"])

    columns = {}
    for m_ev in M_EV_GRID:
        m22 = m_ev / 1e-22
        pure_status = pure_fdm_exclusion_status(m_ev)
        cells = []
        smallest_f_2sigma = None
        smallest_f_3sigma = None
        prev_delta_chi2 = -1.0
        monotone_violation = False
        for f in F_GRID:
            result = des_y6_synthetic_convergence_bandpowers(m22=m22, f=float(f), ell_bands=ELL_BANDS)
            c_ell_model = np.asarray(result["c_ell"])
            delta_chi2 = delta_chi2_vs_baseline(c_ell_model, c_ell_baseline, cov_diag_baseline)
            sigma_equiv = float(np.sqrt(max(delta_chi2, 0.0)))
            if delta_chi2 < prev_delta_chi2 - 1e-9:
                monotone_violation = True
            prev_delta_chi2 = delta_chi2

            reaches_2sigma = sigma_equiv >= SIGNIFICANCE_THRESHOLDS["2sigma"]
            reaches_3sigma = sigma_equiv >= SIGNIFICANCE_THRESHOLDS["3sigma"]
            if reaches_2sigma and smallest_f_2sigma is None:
                smallest_f_2sigma = float(f)
            if reaches_3sigma and smallest_f_3sigma is None:
                smallest_f_3sigma = float(f)

            cells.append({
                "f": float(f),
                "delta_chi2": delta_chi2,
                "sigma_equiv": sigma_equiv,
                "reaches_2sigma": reaches_2sigma,
                "reaches_3sigma": reaches_3sigma,
            })

        columns[f"{m_ev:.4e}"] = {
            "m_ev": float(m_ev),
            "m22": float(m22),
            "pure_fdm_exclusion": pure_status,
            "smallest_f_reaching_2sigma": smallest_f_2sigma,
            "smallest_f_reaching_3sigma": smallest_f_3sigma,
            "monotone_in_f": not monotone_violation,
            "cells": cells,
        }

    return {
        "label": "ENGINEERING (synthetic Fisher/Delta-chi2 pre-flight, no real data)",
        "generated": datetime.now(timezone.utc).isoformat(),
        "grid": {
            "m_ev": M_EV_GRID.tolist(),
            "f": F_GRID.tolist(),
            "ell_bands": ELL_BANDS.tolist(),
            "n_cells": int(M_EV_GRID.size * F_GRID.size),
        },
        "survey_parameters_des_y6": {
            "n_eff_arcmin2": DES_Y6_N_EFF_ARCMIN2,
            "sigma_e": DES_Y6_SIGMA_E,
            "area_deg2": DES_Y6_AREA_DEG2,
            "citation": "arXiv:2501.05665 (DES Y6 Metadetection), via "
                        "docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md",
        },
        "baseline_f0": {
            "c_ell": c_ell_baseline.tolist(),
            "cov_diag": cov_diag_baseline.tolist(),
        },
        "published_pure_fdm_bounds": PURE_FDM_EXCLUSION_BOUNDS,
        "published_mixed_fdm_anchors_context_only": PUBLISHED_MIXED_FDM_ANCHORS,
        "columns": columns,
        "area_scaling_sensitivity_check": area_scaling_sensitivity_check(),
    }


def summarize(results: dict) -> list[str]:
    lines = []
    for key, col in results["columns"].items():
        pure = "EXCLUDED" if col["pure_fdm_exclusion"]["excluded"] else "OPEN"
        s2 = col["smallest_f_reaching_2sigma"]
        s3 = col["smallest_f_reaching_3sigma"]
        lines.append(
            f"m={col['m_ev']:.3e} eV | pure-FDM: {pure:8s} | "
            f"smallest f -> 2sigma: {s2!s:>5} | 3sigma: {s3!s:>5} | "
            f"monotone-in-f: {col['monotone_in_f']}"
        )
    return lines


def main() -> int:
    logger.info(
        "WP-E6 adequacy pre-flight: ENGINEERING, synthetic Fisher/Delta-chi2 "
        "arithmetic only. NOT a TEST, NOT a FIT. Grid: %d masses x %d "
        "fractions = %d cells.", M_EV_GRID.size, F_GRID.size,
        M_EV_GRID.size * F_GRID.size,
    )

    results = run_grid()

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as fh:
        json.dump(results, fh, indent=2)
    logger.info("Wrote %s", OUT_JSON)

    for line in summarize(results):
        logger.info(line)

    any_violation = any(not c["monotone_in_f"] for c in results["columns"].values())
    if any_violation:
        logger.error(
            "MONOTONICITY VIOLATION: at least one m column has non-monotone "
            "Delta-chi2(f) -- see JSON for details. This should not happen "
            "under the linear-interpolation suppression model; investigate "
            "before trusting the adequacy table."
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
