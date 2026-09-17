#!/usr/bin/env python3
"""WP-E6-SWEEP — probe of a 3-point log-log quadratic rule (DRAFT, ENGINEERING; option for T0, not adopted).

After the PROPOSED linear rule failed R-KEFF-2 on the real emulator, this measures, per band and in σ_b:
  quad_next_term — |4-point cubic − 3-point quadratic| at k_eff: the next-order correction, i.e. the
                   error proxy for the quadratic rule (same logic by which quad−lin tracked the linear bound)
  quad_minus_lin — size of what quadratic changes relative to linear (context)
  median_fail_bands — which bands fail the linear 0.1σ check at median nuisances
It also tries a "sign-fixed" variant of negative control 1 (bump in the direction that increases
|second difference|). RESULT: NOT ADOPTED. At the fiducial point the committed control passes 9/9 and this
variant only 7/9. The apparent control failure came from running it at all 952 points, outside its spec. The threshold stays 0.1σ. No data vector is used.
Writes data/derived/wp_e6_sweep_keff_quadratic_probe_2026_09_17.json before print.
"""
import itertools, json, sys, warnings
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "phase1_work" / "agent1_emulator")); sys.path.insert(0, str(ROOT / "scripts"))
import emu_predict as E  # noqa: E402
from wp_e6_sweep_keff_emulator_precheck_2026_09_17 import band_bounds, M_GRID, F_GRID, NODES, THRESH  # noqa: E402
OUT = ROOT / "data/derived/wp_e6_sweep_keff_quadratic_probe_2026_09_17.json"


def poly_at(lnP, x, idx, deg):
    return np.polyval(np.polyfit(NODES[idx], lnP[idx], deg), x)


def main():
    agg = json.load(open(ROOT / "data/derived/wp_e6_sweep_cov_agg9_z4p2_2026_09_16.json"))
    ref = json.load(open(ROOT / "data/derived/wp_e6_grid_controls_report_2026_07_28.json")); med = ref["igm_nuisance_point"]
    lk = np.log10(np.array(agg["k_eff_s_per_km"])); sig = np.sqrt(np.array(agg["diag_actual"]))
    pack = E.load(); s = pack["scaler_res"]; lo, hi = s.data_min_[3:7], s.data_max_[3:7]
    nuis = [("median", [med["zrei"], med["ha"], med["hs"], med["taueff"]])]
    nuis += [("corner" + "".join(map(str, b)), [hi[i] if t else lo[i] for i, t in enumerate(b)]) for b in itertools.product((0, 1), repeat=4)]
    NT, QL, med_fail, ctrl_min, sd_med = [], [], np.zeros(9, int), 9, []
    for (nn, nv), m, f in itertools.product(nuis, M_GRID, F_GRID):
        lnP = np.log(E.predict_pk(pack, m, f, *nv, "4.2"))
        nt, ql = [], []
        for b in range(9):
            c = 1 if b == 0 else b
            q3 = [c - 1, c, c + 1]
            # 4th node on the side of k_eff (band 0: extend upward; no node below −2.2)
            q4 = sorted(q3 + ([c + 2] if (b == 0 or lk[b] >= NODES[c]) else [c - 2]))
            quad = np.exp(poly_at(lnP, lk[b], q3, 2)); cub = np.exp(poly_at(lnP, lk[b], q4, 3))
            lin = np.exp(lnP[0] + (lnP[1] - lnP[0]) * (lk[b] - NODES[0]) / 0.1) if b == 0 else np.exp(np.interp(lk[b], NODES, lnP))
            nt.append(abs(cub - quad) / sig[b]); ql.append(abs(quad - lin) / sig[b])
        NT.append(nt); QL.append(ql)
        if nn == "median":
            med_fail += (band_bounds(lnP, lk, sig) > THRESH).astype(int)
            sd_med.append([float(lnP[c - 1] - 2 * lnP[c] + lnP[c + 1]) for c in range(1, 15)])
        fails = 0
        for b in range(9):
            c = 1 if b == 0 else b
            sd = lnP[c - 1] - 2 * lnP[c] + lnP[c + 1]
            lb = lnP.copy(); lb[c] += -np.log(1.10) if sd <= 0 else np.log(1.10)   # grow |second difference|
            fails += band_bounds(lb, lk, sig, worst=True)[b] > THRESH
        ctrl_min = min(ctrl_min, fails)
    NT, QL = np.array(NT), np.array(QL)
    out = {"label": "DRAFT (ENGINEERING/DESIGN) — quadratic-rule probe; option for T0, not adopted; no data vector",
           "generated_utc": datetime.now(timezone.utc).isoformat(), "points": len(NT),
           "quad_next_term_sigma_max_per_band": NT.max(0).tolist(),
           "quad_next_term_sigma_p95_per_band": np.percentile(NT, 95, 0).tolist(),
           "quad_rule_points_over_0p1sigma": int(np.sum(np.any(NT > THRESH, axis=1))),
           "quad_minus_lin_sigma_max_per_band": QL.max(0).tolist(),
           "linear_rule_median_nuisance_fail_count_per_band": med_fail.tolist(),
           "median_nuisance_second_difference_lnP_nodes_1_to_14_mean": np.mean(sd_med, 0).tolist(),
           "control_1_signfixed_min_bands_failing": int(ctrl_min), "control_1_signfixed_pass": bool(ctrl_min == 9)}
    OUT.write_text(json.dumps(out, indent=1))
    print("linear rule, median-nuisance cells failing per band:", med_fail.tolist())
    print("mean 2nd difference of ln P at nodes −2.1..−0.8 (median nuisances):", np.round(out["median_nuisance_second_difference_lnP_nodes_1_to_14_mean"], 3).tolist())
    print("quadratic rule next-term max σ per band:", np.round(NT.max(0), 4).tolist())
    print("quadratic rule next-term p95 σ per band:", np.round(np.percentile(NT, 95, 0), 4).tolist())
    print(f"quadratic rule: points with any band > 0.1σ: {out['quad_rule_points_over_0p1sigma']}/{len(NT)}")
    print(f"control 1 (sign fixed): min bands failing {ctrl_min}/9 -> pass {out['control_1_signfixed_pass']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
