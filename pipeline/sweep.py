#!/usr/bin/env python3
"""
WP-E6-SWEEP — (m, f) profile-likelihood sweep driver.

Authority chain (all pinned): PREDICTION v2 amendment (§4 statistic, §5 labels, §8 resolution),
`WP_E6_SWEEP_DESIGN_PINNED_2026_09_16.md` (C₉/P₉ aggregation; χ²_min 5 dof, Δχ² 2 dof, 5.9915),
`WP_E6_SWEEP_KEFF_RULING_PINNED_2026_09_17.md` (K1 k_eff interpolation, K2 C₉,sys, K3 gate).

REAL-DATA MODE IS MECHANICALLY BLOCKED. `briefs/T0_DECISION_REQUEST_SWEEP_THEORY_CORRECTIONS_2026_09_17.md`
(C1–C5: Si III/Si II/Mg II/C IV modelling, patchy reionization, resolution template, DESI k cut in
band 8, χ²_ν treatment) is unruled. `load_real_observation()` raises until REAL_DATA_RULING_PIN names
an existing pinned ruling file. Synthetic mode (emulator-generated observations) is engineering
validation only and is never labeled exclusion or FIT.

Labels: real-mode outputs are `exclusion` (the Δχ² contour) and `FIT` (per-cell χ²_min, best-fit
nuisances). TEST is foreclosed (amendment §5). Synthetic outputs carry SYNTHETIC_LABEL.
taueff bounds (0.3, 1.8) are a PRIOR-BOX, not a trained-support extremum (T0 2026-07-28 item 2):
a best fit pinned there is reported as a prior-box edge.
"""
import json
import multiprocessing as mp
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy import linalg, stats

import chi2_profile
import keff

REPO_ROOT = Path(__file__).resolve().parent.parent

# Pinned grid: briefs/T0_MF_GRID_DEFINITION_2026_07_27.md §3 (countermand window closed 2026-07-28).
M_GRID = np.array([-22.9, -22.5, -22.0, -21.5, -21.0, -20.5, -20.0, -19.1])
F_GRID = np.array([0.0, 0.05, 0.1, 0.2, 0.35, 0.6, 0.99])
DOF_CELL = 5                                  # 9 bins − 4 profiled nuisances (design §2)
DCHI2_95_2DOF = float(stats.chi2.ppf(0.95, 2))  # 5.9915 (design §2; computed, not recalled)

# Set to the path of a PINNED ruling on C1–C5 to unblock real data. Changing this line is itself a
# pinned-design event (commit-as-pin, TUNING_LOG row); it is never set by a driver run.
REAL_DATA_RULING_PIN = None

def _profile_starts(n_lhs=8, seed=20260917):
    """Deterministic multi-start set: training medians + an n_lhs-point Latin hypercube (fixed seed) over the
    central 90 % of each nuisance bound. Fixed in code so every run is reproducible bit-for-bit."""
    names = ["zrei", "ha", "hs", "taueff"]
    rng = np.random.default_rng(seed)
    lhs = np.array([(rng.permutation(n_lhs) + rng.uniform(size=n_lhs)) / n_lhs for _ in names]).T
    pts = [dict(chi2_profile.NUISANCE_INIT)]
    for row in lhs:
        pts.append({n: chi2_profile.NUISANCE_BOUNDS[n][0] + (chi2_profile.NUISANCE_BOUNDS[n][1] - chi2_profile.NUISANCE_BOUNDS[n][0])
                    * (0.05 + 0.9 * u) for n, u in zip(names, row)})
    return pts


PROFILE_STARTS = _profile_starts()
RESIDUAL_SPLIT = 5          # optimizer residual = χ² best of first 5 starts − best of all 9

SYNTHETIC_LABEL = "SYNTHETIC-VALIDATION — emulator-generated observation; not exclusion, not FIT, not TEST"
REAL_LABELS = {"contour": "exclusion", "cell_statistics": "FIT"}
TAUEFF_NOTE = "taueff bounds (0.3, 1.8) are a PRIOR-BOX, not a trained-support extremum (T0 ruling 2026-07-28 item 2)"
PENDING_CORRECTIONS = "NONE_PENDING_T0_C1_C5"


class RealDataBlockedError(PermissionError):
    """Real-data sweep requested before the theory-corrections ruling is pinned."""


def load_real_observation():
    """P₉ from the tracked aggregation artifact — refused until C1–C5 are pinned."""
    if REAL_DATA_RULING_PIN is None or not (REPO_ROOT / REAL_DATA_RULING_PIN).is_file():
        raise RealDataBlockedError(
            "real-data sweep blocked: theory-corrections ruling (C1–C5) not pinned; see "
            "briefs/T0_DECISION_REQUEST_SWEEP_THEORY_CORRECTIONS_2026_09_17.md")
    return np.asarray(json.load(open(keff.AGG_JSON))["data_agg_p1d_kms"], dtype=float)


def make_predictor(predict_native, k_eff, theory_multiplier, mode):
    """(m, f, zrei, ha, hs, taueff) → 9-band prediction: native emulator × multiplier, then K1 at k_eff.

    predict_native(m, f, zrei, ha, hs, taueff) → 16 native values.
    theory_multiplier: required. A 16-vector, or PENDING_CORRECTIONS, which is allowed only in synthetic
    mode (the synthetic truth is built with the same predictor, so no correction is being assumed about data).
    """
    if isinstance(theory_multiplier, str):
        if theory_multiplier != PENDING_CORRECTIONS or mode != "synthetic":
            raise RealDataBlockedError("theory corrections must be an explicit pinned 16-vector outside synthetic mode")
        mult = np.ones(keff.NATIVE_LOG10K.size)
    else:
        mult = np.asarray(theory_multiplier, dtype=float)
        if mult.shape != keff.NATIVE_LOG10K.shape or not np.all(np.isfinite(mult)) or np.any(mult <= 0):
            raise ValueError("theory_multiplier must be 16 finite positive values")
    k_eff = np.asarray(k_eff, dtype=float)

    def predict(m, f, zrei, ha, hs, taueff):
        return keff.predict_at_keff(np.asarray(predict_native(m, f, zrei, ha, hs, taueff)) * mult, k_eff)
    return predict


_WORKER = {}


def _profile_cell(ij):
    i, j = ij
    prof, m_grid, f_grid = _WORKER["prof"], _WORKER["m_grid"], _WORKER["f_grid"]
    r = prof.profile_likelihood(float(m_grid[i]), float(f_grid[j]), starts=PROFILE_STARTS)
    return i, j, r


def run_sweep(p_obs, cov9_sys, predict, mode, out_path, m_grid=M_GRID, f_grid=F_GRID, meta=None, workers=1):
    """Profile every (m, f) cell (deterministic multi-start); persist the JSON record before returning it.

    mode: "synthetic" or "real". Real mode requires load_real_observation() to have succeeded, and is
    re-checked here so a caller cannot pass real P₉ under a synthetic label.
    workers > 1 profiles cells in forked processes (the predictor is inherited, not pickled).
    """
    if mode not in ("synthetic", "real"):
        raise ValueError("mode must be 'synthetic' or 'real'")
    if mode == "real":
        load_real_observation()            # raises while blocked
    real_p9 = np.asarray(json.load(open(keff.AGG_JSON))["data_agg_p1d_kms"], dtype=float)
    if mode == "synthetic" and np.allclose(np.asarray(p_obs, dtype=float), real_p9, rtol=1e-9, atol=0):
        raise RealDataBlockedError("synthetic mode was given the real observed vector")

    cov9_sys = np.asarray(cov9_sys, dtype=float)
    cov_inv = linalg.cho_solve(linalg.cho_factor(cov9_sys), np.eye(9))
    cov_inv = 0.5 * (cov_inv + cov_inv.T)
    prof = chi2_profile.Chi2Profiler(np.asarray(p_obs, dtype=float), cov_inv, predict, hartlap_n=None)

    _WORKER.update(prof=prof, m_grid=np.asarray(m_grid), f_grid=np.asarray(f_grid))
    todo = [(i, j) for i in range(len(m_grid)) for j in range(len(f_grid))]
    if workers > 1:
        with mp.get_context("fork").Pool(workers) as pool:
            results = pool.map(_profile_cell, todo, chunksize=1)
    else:
        results = [_profile_cell(ij) for ij in todo]

    names = ["zrei", "ha", "hs", "taueff"]
    chi2 = np.zeros((len(m_grid), len(f_grid)))
    cells = []
    for i, j, r in sorted(results, key=lambda x: (x[0], x[1])):
        chi2[i, j] = r.chi2_min
        tau = r.nuisance_params["taueff"]
        fv = np.asarray(r.start_fvals)
        cells.append({
            "m": float(m_grid[i]), "f": float(f_grid[j]), "chi2_min": float(r.chi2_min),
            "gof_p_value_5dof": float(stats.chi2.sf(r.chi2_min, DOF_CELL)),
            "best_fit": {n: float(r.nuisance_params[n]) for n in names},
            "valid_minimum": bool(r.valid_minimum), "at_boundary": bool(r.at_boundary),
            "taueff_at_prior_box_edge": bool(min(abs(tau - 0.3), abs(tau - 1.8)) < 1e-4),
            "start_chi2": fv.tolist(),
            "optimizer_residual": float(fv[:RESIDUAL_SPLIT].min() - fv.min()),
            "n_calls": int(r.n_calls), "messages": list(r.messages),
        })
    dchi2 = chi2 - chi2.min()
    imin = np.unravel_index(np.argmin(chi2), chi2.shape)
    resid = np.array([c["optimizer_residual"] for c in cells])
    rec = {
        "label": SYNTHETIC_LABEL if mode == "synthetic" else REAL_LABELS,
        "mode": mode,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "pins": ["briefs/PREDICTION_V2_AMENDMENT_DRAFT_2026_07_29.md", "briefs/WP_E6_SWEEP_DESIGN_PINNED_2026_09_16.md",
                 "briefs/WP_E6_SWEEP_KEFF_RULING_PINNED_2026_09_17.md"],
        "statistic": {"cell": f"chi2_min, {DOF_CELL} dof", "contour": f"delta chi2, 2 dof, threshold {DCHI2_95_2DOF:.4f} (95%)"},
        "optimizer": {"method": "iminuit Migrad, deterministic multi-start (medians + 8-pt LHS, seed 20260917), re-run once if invalid",
                      "n_starts": len(PROFILE_STARTS), "residual_definition": f"best of first {RESIDUAL_SPLIT} starts − best of all",
                      "max_residual": float(resid.max()), "cells_with_residual_gt_0p1": int((resid > 0.1).sum())},
        "taueff_note": TAUEFF_NOTE,
        "m_grid": list(map(float, m_grid)), "f_grid": list(map(float, f_grid)),
        "chi2_min_grid": chi2.tolist(), "delta_chi2_grid": dchi2.tolist(),
        "outside_95_region": (dchi2 > DCHI2_95_2DOF).tolist(),
        "grid_minimum": {"m": float(m_grid[imin[0]]), "f": float(f_grid[imin[1]]), "chi2_min": float(chi2[imin])},
        "all_minima_valid": bool(all(c["valid_minimum"] for c in cells)),
        "cells": cells,
        "meta": meta or {},
    }
    Path(out_path).write_text(json.dumps(rec, indent=1))
    return rec
