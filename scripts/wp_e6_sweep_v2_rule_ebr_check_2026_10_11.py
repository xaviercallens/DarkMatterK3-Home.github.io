#!/usr/bin/env python3
"""WP-E6-SWEEP design v2 — effect of eligibility rule E-B+R on the 12 synthetic coverage draws (truth cell only).

ENGINEERING / DESIGN (not TEST, not FIT; no real vector). Regenerates the 12 coverage draws (same seeds as
`wp_e6_sweep_v2_coverage_2026_10_10.py`), profiles ONLY the truth cell with the design-v2 profiler (two optimizer passes) and
reports, per draw, the pass-to-pass gap and eligibility under E-B, E-B+V and E-B+R at the pre-registered REPRO_TOL.

    OMP_NUM_THREADS=2 ~/venv/bin/python scripts/wp_e6_sweep_v2_rule_ebr_check_2026_10_11.py
Writes data/derived/wp_e6_sweep_v2_rule_ebr_check_2026_10_11.json after every draw.
"""
import json
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy import linalg

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))
sys.path.insert(0, str(ROOT / "phase1_work" / "agent1_emulator"))
import chi2_profile as cp  # noqa: E402
import emu_predict as E  # noqa: E402
import keff  # noqa: E402
import sweep  # noqa: E402
import sweep_corrections as sc  # noqa: E402

OUT = ROOT / "data/derived/wp_e6_sweep_v2_rule_ebr_check_2026_10_11.json"
COV = ROOT / "data/derived/wp_e6_sweep_v2_coverage_2026_10_10.json"
REF = ROOT / "data/derived/wp_e6_grid_controls_report_2026_07_28.json"


def main():
    cov_rec = json.load(open(COV))
    pack = E.load()
    corr = sc.load_corrector()
    k_eff = np.asarray(json.load(open(keff.V2.agg_json))["k_eff_s_per_km"])
    cov_sys = keff.augmented_covariance(np.load(keff.V2.agg_npy), keff.V2.precheck_json, keff.V2)
    cov_inv = linalg.cho_solve(linalg.cho_factor(cov_sys), np.eye(9))
    cov_inv = 0.5 * (cov_inv + cov_inv.T)
    L = np.linalg.cholesky(cov_sys)
    med = json.load(open(REF))["igm_nuisance_point"]
    nu = [med["zrei"], med["ha"], med["hs"], med["taueff"]]
    pred = sweep.make_predictor_v2(lambda m, f, z, a, h, t: E.predict_pk(pack, m, f, z, a, h, t, "4.2"), k_eff, corr)
    t = cov_rec["truth"]
    clean = pred(t["m"], t["f"], *nu, t["s"])
    starts = sweep._v2_starts(sweep.PROFILE_STARTS)
    extra = {sweep.SIII_NAME: (*sc.SIII_PRIOR_BOX, sc.SIII_INIT)}
    rec = {"label": "SYNTHETIC — emulator-generated; not exclusion, not FIT, not TEST; no real vector",
           "generated_utc": datetime.now(timezone.utc).isoformat(), "repro_tol": sweep.REPRO_TOL,
           "seed0": cov_rec["seed0"], "truth": t, "draws": []}
    for i in range(cov_rec["n_draws"]):
        data = clean + L @ np.random.default_rng(cov_rec["seed0"] + i).standard_normal(9)
        prof = cp.Chi2Profiler(data, cov_inv, pred, hartlap_n=None, extra_nuisances=extra)
        r = prof.profile_likelihood(t["m"], t["f"], starts=starts)
        rec["draws"].append({
            "draw": i, "chi2_min": r.chi2_min, "repro_delta": r.repro_delta, "minuit_valid": r.valid_minimum,
            "s_fit": r.nuisance_params["s_siiii"], "at_boundary": r.at_boundary,
            "elig_E_B": sweep.cell_eligible(r, "E-B"), "elig_E_BV": sweep.cell_eligible(r, "E-B+V"),
            "elig_E_BR": sweep.cell_eligible(r, "E-B+R"),
        })
        OUT.write_text(json.dumps(rec, indent=1))
    ds = rec["draws"]
    rec["summary"] = {"n": len(ds), "elig_E_B": sum(d["elig_E_B"] for d in ds), "elig_E_BV": sum(d["elig_E_BV"] for d in ds),
                      "elig_E_BR": sum(d["elig_E_BR"] for d in ds),
                      "max_repro_delta": float(max(d["repro_delta"] for d in ds)),
                      "median_repro_delta": float(np.median([d["repro_delta"] for d in ds]))}
    OUT.write_text(json.dumps(rec, indent=1))
    print(json.dumps(rec["summary"], indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
