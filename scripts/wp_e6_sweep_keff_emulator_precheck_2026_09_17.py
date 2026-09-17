#!/usr/bin/env python3
"""WP-E6-SWEEP — pre-approval run of the PROPOSED R-KEFF-2 acceptance check on the real emulator.

ENGINEERING / DESIGN, DRAFT (CLAUDE.md rule 3). No data vector is used: σ_b comes from the pinned
C₉ diagonal and k_eff from the tracked aggregation artifact; P comes only from the emulator.
No model–data comparison is made. The threshold (0.1 σ_b) and both negative controls were
committed in f17f3b7 BEFORE this script existed, so running it cannot tune them.
The proposal is NOT approved; this run informs T0's decision and is not the pinned check.

Needs the gitignored emulator (phase1_work/agent1_emulator/, lya-mfdm 9182aa4 + emu_predict.py).
    ~/venv/bin/python scripts/wp_e6_sweep_keff_emulator_precheck_2026_09_17.py
Writes data/derived/wp_e6_sweep_keff_emulator_precheck_2026_09_17.json (before any print).
"""
import itertools, json, sys, warnings
from datetime import datetime, timezone
from pathlib import Path
import numpy as np

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "phase1_work" / "agent1_emulator"))
import emu_predict as E  # noqa: E402

AGG = ROOT / "data/derived/wp_e6_sweep_cov_agg9_z4p2_2026_09_16.json"
REF = ROOT / "data/derived/wp_e6_grid_controls_report_2026_07_28.json"
OUT = ROOT / "data/derived/wp_e6_sweep_keff_emulator_precheck_2026_09_17.json"
M_GRID = [-22.9, -22.5, -22.0, -21.5, -21.0, -20.5, -20.0, -19.1]   # T0_MF_GRID_DEFINITION §3
F_GRID = [0.0, 0.05, 0.1, 0.2, 0.35, 0.6, 0.99]
THRESH, CAP_DEX, BUMP = 0.1, 0.01, 1.10
H = 0.1 * np.log(10)
NODES = np.round(np.arange(-2.2, -0.65, 0.1), 1)


def band_bounds(lnP, log10_keff, sig, rule="loglog", worst=False):
    """R-KEFF-2 curvature bound per band, in units of σ_b. lnP: ln P at the 16 nodes."""
    out = []
    for b in range(9):
        c = 1 if b == 0 else b                     # curvature centre index (band 0 uses −2.1)
        if rule == "loglog":
            f2 = abs(lnP[c - 1] - 2 * lnP[c] + lnP[c + 1]) / H ** 2
        else:                                      # negative control rule: linear in k, curvature of P in k
            kk = 10.0 ** NODES
            P = np.exp(lnP)
            f2 = abs((P[c + 1] - P[c]) / (kk[c + 1] - kk[c]) - (P[c] - P[c - 1]) / (kk[c] - kk[c - 1])) \
                / (0.5 * (kk[c + 1] - kk[c - 1]))
        x = log10_keff[b]
        if worst:
            x = -2.25 if b == 0 else NODES[b] - 0.05
        if rule == "loglog":
            if b == 0:
                d = abs(x - NODES[0]) * np.log(10); geom = d * (H + d)
            else:
                lo = NODES[b - 1] if x < NODES[b] else NODES[b]
                d = abs(x - lo) * np.log(10); d = min(d, H - d); geom = d * (H - d)
            Pk = np.exp(np.interp(x, NODES, lnP) if b else lnP[0] + (lnP[1] - lnP[0]) * (x - NODES[0]) / 0.1)
            out.append(0.5 * f2 * geom * Pk / sig[b])
        else:
            k = 10.0 ** x
            lo = 10.0 ** (NODES[b - 1] if (b and x < NODES[b]) else NODES[b])
            hi = lo * 10 ** 0.1
            Pk = np.exp(np.interp(x, NODES, lnP))
            out.append(0.5 * f2 * abs(k - lo) * abs(hi - k) / sig[b])
    return np.array(out)


def main():
    agg = json.load(open(AGG)); ref = json.load(open(REF))
    log10_keff = np.log10(np.array(agg["k_eff_s_per_km"]))
    sig = np.sqrt(np.array(agg["diag_actual"]))
    pack = E.load()
    rec = {"label": "DRAFT (ENGINEERING/DESIGN) — pre-approval run of PROPOSED R-KEFF-2; not TEST, not FIT; no data vector used",
           "generated_utc": datetime.now(timezone.utc).isoformat(),
           "threshold_sigma": THRESH, "proposal_commit_fixing_threshold": "f17f3b7",
           "emulator": "lya-mfdm 9182aa4, emu_N100, rebuilt standalone wrapper"}

    # 0. wrapper regression against the 2026-07-28 grid-controls artifact (same z, medians)
    med = ref["igm_nuisance_point"]
    c0 = ref["checks"][0]
    p_ref = np.array(c0["pk_reference"])
    p_now = E.predict_pk(pack, -22.9, 0.0, med["zrei"], med["ha"], med["hs"], med["taueff"], "4.2")
    c2 = ref["checks"][2]
    sup_now = {}
    for row in c2["per_mass"]:
        p = E.predict_pk(pack, row["m"], c2["f_fixed"], med["zrei"], med["ha"], med["hs"], med["taueff"], "4.2")
        sup_now[row["m"]] = float(np.max(np.abs(1 - p / p_now)))
    reg = {"cdm_max_rel_diff_vs_2026_07_28": float(np.max(np.abs(p_now / p_ref - 1))),
           "suppression_max_abs_diff_vs_2026_07_28": float(max(abs(sup_now[r["m"]] - r["max_abs_suppression"]) for r in c2["per_mass"]))}
    reg["pass"] = reg["cdm_max_rel_diff_vs_2026_07_28"] < 1e-5 and reg["suppression_max_abs_diff_vs_2026_07_28"] < 1e-5
    rec["wrapper_regression"] = reg
    if not reg["pass"]:
        OUT.write_text(json.dumps(rec, indent=1)); print("wrapper regression FAILED — stop", reg); return 1

    # nuisance points: training medians + all 16 corners of the scaler_res training box
    s = pack["scaler_res"]; lo, hi = s.data_min_[3:7], s.data_max_[3:7]    # zrei, ha, hs, taueff
    rec["nuisance_training_box"] = {"min": lo.tolist(), "max": hi.tolist(), "order": ["zrei", "ha", "hs", "taueff"]}
    nuis = [("median", [med["zrei"], med["ha"], med["hs"], med["taueff"]])]
    nuis += [("corner" + "".join(map(str, bits)), [hi[i] if bit else lo[i] for i, bit in enumerate(bits)])
             for bits in itertools.product((0, 1), repeat=4)]

    worst = np.zeros(9); worst_at = [None] * 9; n_points = 0; ctrl_bump_min_fails = 9; ctrl_rule_ok = True
    per_band_all = []
    for (nname, nv), m, f in itertools.product(nuis, M_GRID, F_GRID):
        P = E.predict_pk(pack, m, f, *nv, "4.2"); lnP = np.log(P); n_points += 1
        bnd = band_bounds(lnP, log10_keff, sig)
        per_band_all.append(bnd)
        for b in range(9):
            if bnd[b] > worst[b]:
                worst[b] = bnd[b]; worst_at[b] = {"nuisance": nname, "m": m, "f": f}
        # control 1 beyond spec (informational only): same bump at EVERY point. Loses power where the
        # emulator P is small relative to the data σ (strong suppression), so it is not the control.
        fails = 0
        for b in range(9):
            c = 1 if b == 0 else b
            lb = lnP.copy(); lb[c] += np.log(BUMP)
            fails += band_bounds(lb, log10_keff, sig, worst=True)[b] > THRESH
        ctrl_bump_min_fails = min(ctrl_bump_min_fails, fails)
    per_band_all = np.array(per_band_all)

    rec["points_checked"] = n_points
    rec["bound_sigma_max_per_band"] = worst.tolist()
    rec["bound_sigma_max_location"] = worst_at
    rec["bound_sigma_median_per_band"] = np.median(per_band_all, axis=0).tolist()
    rec["pass_R_KEFF_2"] = bool(np.all(worst <= THRESH))
    rec["control_1_beyond_spec_all_points_min_bands_failing"] = int(ctrl_bump_min_fails)
    # control 1 AS SPECIFIED in the proposal (f17f3b7): fiducial point only (f = 0, training medians)
    lnF = np.log(E.predict_pk(pack, M_GRID[0], 0.0, *nuis[0][1], "4.2"))
    fid_fails = []
    for b in range(9):
        c = 1 if b == 0 else b
        lb = lnF.copy(); lb[c] += np.log(BUMP)
        fid_fails.append(int(band_bounds(lb, log10_keff, sig, worst=True)[b] > THRESH))
    rec["control_1_fiducial_fails_per_band"] = fid_fails
    rec["control_1_pass"] = sum(fid_fails) == 9
    rec["fiducial_bound_sigma_per_band"] = band_bounds(lnF, log10_keff, sig).tolist()
    rec["fiducial_pass"] = bool(np.all(np.array(rec["fiducial_bound_sigma_per_band"]) <= THRESH))
    cap_keff = log10_keff.copy(); cap_keff[0] = -2.2 - 0.02
    rec["control_2_cap_fires"] = bool((NODES[0] - cap_keff[0]) > CAP_DEX)
    rec["band0_extrapolation_dex"] = float(NODES[0] - log10_keff[0])
    rec["band0_within_cap"] = bool(rec["band0_extrapolation_dex"] <= CAP_DEX)
    rec["overall"] = bool(rec["pass_R_KEFF_2"] and rec["control_1_pass"] and rec["control_2_cap_fires"] and rec["band0_within_cap"])
    OUT.write_text(json.dumps(rec, indent=1, default=str))

    print(f"wrapper regression: {reg}")
    print(f"points checked: {n_points} (17 nuisance points × 56 grid cells)")
    for b in range(9):
        print(f"  band {b}: max bound {worst[b]:.4f}σ at {worst_at[b]}; median {rec['bound_sigma_median_per_band'][b]:.4f}σ")
    print(f"fiducial bound σ: {np.round(rec['fiducial_bound_sigma_per_band'], 4).tolist()} pass {rec['fiducial_pass']}")
    print(f"R-KEFF-2 pass (all 952 points): {rec['pass_R_KEFF_2']} | control 1 (fiducial, as specified) {sum(fid_fails)}/9 | "
          f"control 2 cap fires: {rec['control_2_cap_fires']} | band-0 {rec['band0_extrapolation_dex']:.4f} dex within cap: {rec['band0_within_cap']}")
    print(f"OVERALL: {rec['overall']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
