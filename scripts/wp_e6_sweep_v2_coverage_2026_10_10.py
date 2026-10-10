#!/usr/bin/env python3
"""WP-E6-SWEEP design v2 — multi-draw synthetic coverage on the REAL emulator. No real data vector is read or fitted.

ENGINEERING / DESIGN (not TEST, not FIT). N_DRAWS fixed-seed noise draws from the v2 covariance around a known truth
(m = -22.0, f = 0.2, IGM medians, s = 1). Each draw is swept over the same 3x3 grid as the single-draw validation.
Reported per draw: truth-cell dchi2 against the grid minimum, whether the truth cell is inside the 2-dof 95% region
(dchi2 <= 5.99), whether the truth cell's fit is a valid minimum, whether it sits at a bound, and the fitted s.
Nothing here is tuned after the fact: N_DRAWS, the seeds and the grid are fixed below before the run.

    ~/venv/bin/python scripts/wp_e6_sweep_v2_coverage_2026_10_10.py
Writes data/derived/wp_e6_sweep_v2_coverage_2026_10_10.json after EVERY draw (resumable record) and prints at the end.
"""
import json
import sys
import warnings
from datetime import datetime, timezone
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

OUT = ROOT / "data/derived/wp_e6_sweep_v2_coverage_2026_10_10.json"
REF = ROOT / "data/derived/wp_e6_grid_controls_report_2026_07_28.json"
M_GRID = np.array([-22.5, -22.0, -21.0])
F_GRID = np.array([0.1, 0.2, 0.6])
TRUTH = dict(m=-22.0, f=0.2, s=1.0)
N_DRAWS = 12
SEED0 = 20261011
THRESH = 5.9915


def main():
    pack = E.load()
    corr = sc.load_corrector()
    agg = json.load(open(keff.V2.agg_json))
    k_eff = np.asarray(agg["k_eff_s_per_km"])
    cov_sys = keff.augmented_covariance(np.load(keff.V2.agg_npy), keff.V2.precheck_json, keff.V2)
    L = np.linalg.cholesky(cov_sys)
    med = json.load(open(REF))["igm_nuisance_point"]
    nu = [med["zrei"], med["ha"], med["hs"], med["taueff"]]
    pred = sweep.make_predictor_v2(lambda m, f, z, a, h, t: E.predict_pk(pack, m, f, z, a, h, t, "4.2"), k_eff, corr)
    clean = pred(TRUTH["m"], TRUTH["f"], *nu, TRUTH["s"])
    rec = {"label": "SYNTHETIC-VALIDATION — emulator-generated; not exclusion, not FIT, not TEST; no real vector read",
           "generated_utc": datetime.now(timezone.utc).isoformat(), "truth": TRUTH, "n_draws": N_DRAWS, "seed0": SEED0,
           "grid": {"m": M_GRID.tolist(), "f": F_GRID.tolist()}, "threshold_dchi2_2dof_95": THRESH, "draws": []}
    for i in range(N_DRAWS):
        rng = np.random.default_rng(SEED0 + i)
        data = clean + L @ rng.standard_normal(9)
        tmp = ROOT / f"data/derived/_tmp_cov_{i}.json"
        r = sweep.run_sweep(data, cov_sys, pred, "synthetic", tmp, m_grid=M_GRID, f_grid=F_GRID, design="v2")
        tmp.unlink(missing_ok=True)
        cells = {(c["m"], c["f"]): c for c in r["cells"]}
        tc = cells[(TRUTH["m"], TRUTH["f"])]
        elig = {(c["m"], c["f"]): c["contour_eligible"] for c in r["cells"]}
        chis = {k: c["chi2_min"] for k, c in cells.items() if elig[k]}
        cmin = min(chis.values())
        d = tc["chi2_min"] - cmin
        rec["draws"].append({
            "draw": i, "seed": SEED0 + i, "truth_chi2": tc["chi2_min"], "grid_min_chi2": cmin,
            "truth_dchi2": d, "truth_inside_95": bool(d <= THRESH), "truth_eligible": bool(elig[(TRUTH["m"], TRUTH["f"])]),
            "truth_valid_minimum": tc["valid_minimum"], "truth_at_boundary": tc["at_boundary"],
            "truth_s_fit": tc["best_fit"]["s_siiii"], "n_ineligible": len(r["ineligible_cells"]),
            "grid_min_cell": r["grid_minimum"],
        })
        OUT.write_text(json.dumps(rec, indent=1))
    ds = rec["draws"]
    n = len(ds)
    summ = {
        "n": n,
        "truth_inside_95": sum(d["truth_inside_95"] for d in ds),
        "truth_valid_minimum": sum(d["truth_valid_minimum"] for d in ds),
        "truth_at_boundary": sum(d["truth_at_boundary"] for d in ds),
        "truth_eligible": sum(d["truth_eligible"] for d in ds),
        "s_fit_median": float(np.median([d["truth_s_fit"] for d in ds])),
        "s_fit_min": float(min(d["truth_s_fit"] for d in ds)),
        "s_fit_max": float(max(d["truth_s_fit"] for d in ds)),
        "mean_truth_chi2": float(np.mean([d["truth_chi2"] for d in ds])),
    }
    rec["summary"] = summ
    OUT.write_text(json.dumps(rec, indent=1))
    print(json.dumps(summ, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
