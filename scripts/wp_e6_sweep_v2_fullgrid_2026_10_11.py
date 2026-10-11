#!/usr/bin/env python3
"""WP-E6-SWEEP design v2 — full 56-cell synthetic sweep under rule E-B+R on the REAL emulator. No real vector.

ENGINEERING / DESIGN (not TEST, not FIT). One fixed-seed noisy draw (seed 20261011, the first coverage seed) around the
known truth (m = -22.0, f = 0.2, IGM medians, s = 1). The full pinned 8 x 7 grid, design v2 (C4 aggregation, V2 K2 table,
Si III fifth nuisance, 4 dof, E-B+R at REPRO_TOL). Reports eligibility, contour status and where the grid minimum falls.

    OMP_NUM_THREADS=2 ~/venv/bin/python scripts/wp_e6_sweep_v2_fullgrid_2026_10_11.py
Writes data/derived/wp_e6_sweep_v2_fullgrid_2026_10_11.json (the full sweep record; synthetic label) and prints a summary.
"""
import json
import sys
import warnings
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))
sys.path.insert(0, str(ROOT / "phase1_work" / "agent1_emulator"))
import emu_predict as E  # noqa: E402
import keff  # noqa: E402
import sweep  # noqa: E402
import sweep_corrections as sc  # noqa: E402

OUT = ROOT / "data/derived/wp_e6_sweep_v2_fullgrid_2026_10_11.json"
REF = ROOT / "data/derived/wp_e6_grid_controls_report_2026_07_28.json"
TRUTH = dict(m=-22.0, f=0.2, s=1.0)
SEED = 20261011


def main():
    pack = E.load()
    corr = sc.load_corrector()
    k_eff = np.asarray(json.load(open(keff.V2.agg_json))["k_eff_s_per_km"])
    cov_sys = keff.augmented_covariance(np.load(keff.V2.agg_npy), keff.V2.precheck_json, keff.V2)
    med = json.load(open(REF))["igm_nuisance_point"]
    nu = [med["zrei"], med["ha"], med["hs"], med["taueff"]]
    pred = sweep.make_predictor_v2(lambda m, f, z, a, h, t: E.predict_pk(pack, m, f, z, a, h, t, "4.2"), k_eff, corr)
    data = pred(TRUTH["m"], TRUTH["f"], *nu, TRUTH["s"]) + np.linalg.cholesky(cov_sys) @ np.random.default_rng(SEED).standard_normal(9)
    rec = sweep.run_sweep(data, cov_sys, pred, "synthetic", OUT, design="v2",
                          meta={"truth": TRUTH, "seed": SEED, "truth_nuisance": nu, "script": Path(__file__).name})
    cells = [c for c in rec["cells"] if not c["failed"]]
    gaps = np.array([c["repro_delta"] for c in cells if c.get("repro_delta") is not None])
    summ = {
        "cells": len(rec["cells"]), "ineligible": len(rec["ineligible_cells"]), "contour_status": rec["contour_status"][:60],
        "grid_minimum": rec["grid_minimum"], "repro_gap_median": float(np.median(gaps)), "repro_gap_max": float(gaps.max()),
        "n_gap_gt_tol": int((gaps > sweep.REPRO_TOL).sum()),
        "minuit_invalid": int(sum(not c["valid_minimum"] for c in cells)),
        "at_boundary": int(sum(c["at_boundary"] for c in cells)),
        "truth_cell_chi2": next(c["chi2_min"] for c in cells if c["m"] == TRUTH["m"] and c["f"] == TRUTH["f"]),
        "truth_cell_eligible": next(c["contour_eligible"] for c in cells if c["m"] == TRUTH["m"] and c["f"] == TRUTH["f"]),
    }
    print(json.dumps(summ, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
