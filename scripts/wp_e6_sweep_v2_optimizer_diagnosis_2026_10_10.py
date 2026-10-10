#!/usr/bin/env python3
"""WP-E6-SWEEP design v2 — diagnosis of the invalid minima found by the 12-draw synthetic coverage run (E-C follow-up).

DIAGNOSTIC ONLY (not TEST, not FIT; no real vector). The pipeline is NOT changed. For the coverage draws whose truth-cell fit
was invalid, regenerate the same noisy vector (same seeds) and profile ONLY the truth cell under three optimizer variants,
recording per start: valid flag, chi2, whether the best start is valid, and whether the fit sits at a box edge.
Variants: BASE (Migrad, re-run once if invalid: what the pipeline does), STRAT2 (Migrad strategy 2), SIMPLEX (simplex then Migrad).

    OMP_NUM_THREADS=2 ~/venv/bin/python scripts/wp_e6_sweep_v2_optimizer_diagnosis_2026_10_10.py
Writes data/derived/wp_e6_sweep_v2_optimizer_diagnosis_2026_10_10.json after every draw.
"""
import json
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from iminuit import Minuit

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))
sys.path.insert(0, str(ROOT / "phase1_work" / "agent1_emulator"))
import chi2_profile as cp  # noqa: E402
import emu_predict as E  # noqa: E402
import keff  # noqa: E402
import sweep  # noqa: E402
import sweep_corrections as sc  # noqa: E402

OUT = ROOT / "data/derived/wp_e6_sweep_v2_optimizer_diagnosis_2026_10_10.json"
COV = ROOT / "data/derived/wp_e6_sweep_v2_coverage_2026_10_10.json"
REF = ROOT / "data/derived/wp_e6_grid_controls_report_2026_07_28.json"
NAMES = ["zrei", "ha", "hs", "taueff", "s_siiii"]
BOUNDS = dict(cp.NUISANCE_BOUNDS, s_siiii=tuple(sc.SIII_PRIOR_BOX))


def run_variant(chi2fn, starts, variant):
    out = []
    for st in starts:
        mi = Minuit(chi2fn, np.array([st[n] for n in NAMES]), name=NAMES)
        for n in NAMES:
            mi.limits[n] = BOUNDS[n]
        mi.errordef = Minuit.LEAST_SQUARES
        if variant == "STRAT2":
            mi.strategy = 2
        if variant == "SIMPLEX":
            mi.simplex()
        mi.migrad()
        if variant == "BASE" and not mi.valid:
            mi.migrad()
        edge = [n for n in NAMES if min(abs(mi.values[n] - BOUNDS[n][0]), abs(mi.values[n] - BOUNDS[n][1])) < 1e-4]
        out.append({"valid": bool(mi.valid), "chi2": float(mi.fval), "edge": edge,
                    "accurate": bool(mi.accurate), "s": float(mi.values["s_siiii"])})
    best = min(range(len(out)), key=lambda i: out[i]["chi2"])
    return {"per_start": out, "best_index": best, "best_valid": out[best]["valid"], "best_chi2": out[best]["chi2"],
            "n_valid_starts": sum(o["valid"] for o in out)}


def main():
    cov_rec = json.load(open(COV))
    bad = [d["draw"] for d in cov_rec["draws"] if not d["truth_valid_minimum"]]
    pack = E.load()
    corr = sc.load_corrector()
    agg = json.load(open(keff.V2.agg_json))
    k_eff = np.asarray(agg["k_eff_s_per_km"])
    cov_sys = keff.augmented_covariance(np.load(keff.V2.agg_npy), keff.V2.precheck_json, keff.V2)
    cov_inv = np.linalg.inv(cov_sys)
    cov_inv = 0.5 * (cov_inv + cov_inv.T)
    L = np.linalg.cholesky(cov_sys)
    med = json.load(open(REF))["igm_nuisance_point"]
    nu = [med["zrei"], med["ha"], med["hs"], med["taueff"]]
    pred = sweep.make_predictor_v2(lambda m, f, z, a, h, t: E.predict_pk(pack, m, f, z, a, h, t, "4.2"), k_eff, corr)
    t = cov_rec["truth"]
    clean = pred(t["m"], t["f"], *nu, t["s"])
    starts = sweep._v2_starts(sweep.PROFILE_STARTS)
    rec = {"label": "DIAGNOSTIC — synthetic only; no real vector; pipeline unchanged",
           "generated_utc": datetime.now(timezone.utc).isoformat(), "invalid_draws": bad, "draws": {}}
    for i in bad:
        data = clean + L @ np.random.default_rng(cov_rec["seed0"] + i).standard_normal(9)

        def chi2fn(x, data=data):
            if not np.all(np.isfinite(x)):
                return cp.NONFINITE_PENALTY
            r = pred(t["m"], t["f"], *[float(v) for v in x]) - data
            return float(r @ cov_inv @ r)

        rec["draws"][str(i)] = {v: run_variant(chi2fn, starts, v) for v in ("BASE", "STRAT2", "SIMPLEX")}
        OUT.write_text(json.dumps(rec, indent=1))
    agg_out = {v: {"best_valid": sum(rec["draws"][str(i)][v]["best_valid"] for i in bad),
                   "n_draws": len(bad),
                   "median_valid_starts": float(np.median([rec["draws"][str(i)][v]["n_valid_starts"] for i in bad]))}
               for v in ("BASE", "STRAT2", "SIMPLEX")}
    rec["summary"] = agg_out
    OUT.write_text(json.dumps(rec, indent=1))
    print(json.dumps(agg_out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
