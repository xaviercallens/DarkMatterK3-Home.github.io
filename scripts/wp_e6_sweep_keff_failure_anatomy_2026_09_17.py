#!/usr/bin/env python3
"""WP-E6-SWEEP — anatomy of the PROPOSED R-KEFF-2 failure on the real emulator (DRAFT, ENGINEERING).

Descriptive only, run after seeing the precheck FAIL. It changes no threshold and proposes no
relaxation. For every (nuisance point, m, f) in the precheck set it records, in units of σ_b:
  lin_bound  — R-KEFF-2 curvature bound for log-log linear interpolation at k_eff (as proposed)
  opt3_shift — |P_loglog(k_eff) − P(k_target)|: the mismatch Option 3 (k_target) would leave in place
  quad_minus_lin — |3-point log-log quadratic − linear| at k_eff (size of the correction a
                   higher-order rule would make; a proxy for linear-rule error)
No data vector is used. Writes data/derived/wp_e6_sweep_keff_failure_anatomy_2026_09_17.json before print.
"""
import itertools, json, sys, warnings
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "phase1_work" / "agent1_emulator")); sys.path.insert(0, str(ROOT / "scripts"))
import emu_predict as E  # noqa: E402
from wp_e6_sweep_keff_emulator_precheck_2026_09_17 import band_bounds, M_GRID, F_GRID, NODES  # noqa: E402
AGG = ROOT / "data/derived/wp_e6_sweep_cov_agg9_z4p2_2026_09_16.json"
REF = ROOT / "data/derived/wp_e6_grid_controls_report_2026_07_28.json"
OUT = ROOT / "data/derived/wp_e6_sweep_keff_failure_anatomy_2026_09_17.json"


def quad_at(lnP, x, b):
    c = 1 if b == 0 else b
    xs = NODES[c - 1:c + 2]; ys = lnP[c - 1:c + 2]
    return np.polyval(np.polyfit(xs, ys, 2), x)


def lin_at(lnP, x, b):
    if b == 0:
        return lnP[0] + (lnP[1] - lnP[0]) * (x - NODES[0]) / 0.1
    return np.interp(x, NODES, lnP)


def main():
    agg = json.load(open(AGG)); ref = json.load(open(REF)); med = ref["igm_nuisance_point"]
    lk = np.log10(np.array(agg["k_eff_s_per_km"])); sig = np.sqrt(np.array(agg["diag_actual"]))
    pack = E.load(); s = pack["scaler_res"]; lo, hi = s.data_min_[3:7], s.data_max_[3:7]
    nuis = [("median", [med["zrei"], med["ha"], med["hs"], med["taueff"]])]
    nuis += [("corner" + "".join(map(str, bits)), [hi[i] if bt else lo[i] for i, bt in enumerate(bits)])
             for bits in itertools.product((0, 1), repeat=4)]
    rows = []
    for (nn, nv), m, f in itertools.product(nuis, M_GRID, F_GRID):
        lnP = np.log(E.predict_pk(pack, m, f, *nv, "4.2"))
        lin_b = band_bounds(lnP, lk, sig)
        opt3 = np.array([abs(np.exp(lin_at(lnP, lk[b], b)) - np.exp(lnP[b])) / sig[b] for b in range(9)])
        qml = np.array([abs(np.exp(quad_at(lnP, lk[b], b)) - np.exp(lin_at(lnP, lk[b], b))) / sig[b] for b in range(9)])
        rows.append({"nuisance": nn, "m": m, "f": f, "lin_bound": lin_b.tolist(), "opt3_shift": opt3.tolist(),
                     "quad_minus_lin": qml.tolist(), "fails": bool(np.any(lin_b > 0.1))})
    L = np.array([r["lin_bound"] for r in rows]); O = np.array([r["opt3_shift"] for r in rows]); Q = np.array([r["quad_minus_lin"] for r in rows])
    failing = [r for r in rows if r["fails"]]
    by_f = {str(f): sum(1 for r in failing if r["f"] == f) for f in F_GRID}
    by_n = {"median": sum(1 for r in failing if r["nuisance"] == "median"),
            "corners": sum(1 for r in failing if r["nuisance"] != "median")}
    med_rows = [r for r in rows if r["nuisance"] == "median"]
    summ = {
        "label": "DRAFT (ENGINEERING/DESIGN) — descriptive failure anatomy; no threshold changed; no data vector",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "points": len(rows), "points_failing_0p1sigma": len(failing),
        "failing_by_f": by_f, "failing_by_nuisance": by_n,
        "median_nuisance_points_failing": sum(r["fails"] for r in med_rows), "median_nuisance_points": len(med_rows),
        "max_sigma_per_band": {"lin_bound": L.max(0).tolist(), "opt3_shift": O.max(0).tolist(), "quad_minus_lin": Q.max(0).tolist()},
        "p95_sigma_per_band": {"lin_bound": np.percentile(L, 95, 0).tolist(), "opt3_shift": np.percentile(O, 95, 0).tolist()},
        "max_ratio_opt3_over_lin_bound_at_lin_worst": [float(O[np.argmax(L[:, b]), b] / max(L[:, b].max(), 1e-12)) for b in range(9)],
        "rows": rows,
    }
    OUT.write_text(json.dumps(summ, indent=1, default=str))
    print(f"points {len(rows)}, failing {len(failing)}; by f {by_f}; by nuisance {by_n}; "
          f"median-nuisance failing {summ['median_nuisance_points_failing']}/{len(med_rows)}")
    print("band | lin bound max  p95 | Option-3 shift max  p95 | quad−lin max | opt3/lin at lin-worst")
    for b in range(9):
        print(f"  {b}  | {L[:, b].max():7.3f} {np.percentile(L[:, b], 95):6.3f} | {O[:, b].max():7.3f} {np.percentile(O[:, b], 95):6.3f} | "
              f"{Q[:, b].max():7.3f} | {summ['max_ratio_opt3_over_lin_bound_at_lin_worst'][b]:6.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
