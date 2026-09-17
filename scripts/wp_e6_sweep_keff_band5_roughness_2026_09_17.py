#!/usr/bin/env python3
"""WP-E6-SWEEP — is the band-5 curvature real emulator structure or output roughness? (DRAFT, ENGINEERING)

Diagnostic after the PROPOSED R-KEFF-2 failed in band 5. No data vector; no comparison.
At the fiducial point (f = 0, training medians, z = 4.2) and at f = 0.99 / m = −22.9:
 (1) stability: second difference of ln P at nodes 4, 5, 6 under small input perturbations
     (taueff ± 1e-3, zrei ± 1e-3 — above float32 resolution after MinMax scaling);
 (2) ensemble spread: the same second difference computed from each of the 5 CV folds separately
     (CDM branch; plus residual branch when f > 0). Fold disagreement comparable to the mean
     signals emulator noise; tight agreement signals structure the ensemble has actually learned.
 (3) the same second difference in the upstream training P1D at z = 4.2 (all_pk_num2_cdm.pkl,
     simulation output, not DESI data), so we can see whether the zig-zag exists in the simulations.
Writes data/derived/wp_e6_sweep_keff_band5_roughness_2026_09_17.json before print.
"""
import json, pickle, sys, warnings
from datetime import datetime, timezone
from pathlib import Path
import numpy as np, torch
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "phase1_work" / "agent1_emulator"))
import emu_predict as E  # noqa: E402
OUT = ROOT / "data/derived/wp_e6_sweep_keff_band5_roughness_2026_09_17.json"
NODES_IDX = [4, 5, 6]


def sd(lnP, c):
    return float(lnP[c - 1] - 2 * lnP[c] + lnP[c + 1])


def fold_logp(pack, m, f, zrei, ha, hs, taueff):
    x_cdm = pack["scaler_cdm"].transform(np.array([[4.2, zrei, ha, hs, taueff]]))
    x_res = pack["scaler_res"].transform(np.array([[4.2, m, f, zrei, ha, hs, taueff]]))
    out = []
    with torch.no_grad():
        for cm, rm in zip(pack["cdm"], pack["res"]):
            c = cm(torch.tensor(x_cdm, dtype=torch.float32))[0].numpy()
            r = rm(torch.tensor(x_res, dtype=torch.float32))[0].numpy()
            out.append((c if f <= E.F_EPS else c + f * r) * np.log(10))   # ln P
    return np.array(out)


def main():
    ref = json.load(open(ROOT / "data/derived/wp_e6_grid_controls_report_2026_07_28.json"))["igm_nuisance_point"]
    base = [ref["zrei"], ref["ha"], ref["hs"], ref["taueff"]]
    pack = E.load()
    rec = {"label": "DRAFT (ENGINEERING/DESIGN) — band-5 roughness diagnostic; no data vector",
           "generated_utc": datetime.now(timezone.utc).isoformat(), "points": {}}
    for name, (m, f) in {"fiducial_f0": (-22.9, 0.0), "strong_m-22.9_f0.99": (-22.9, 0.99)}.items():
        lnP = np.log(E.predict_pk(pack, m, f, *base, "4.2"))
        pert = {}
        for label, idx, eps in (("taueff+1e-3", 3, 1e-3), ("taueff-1e-3", 3, -1e-3), ("zrei+1e-3", 0, 1e-3), ("zrei-1e-3", 0, -1e-3)):
            v = list(base); v[idx] += eps
            lp = np.log(E.predict_pk(pack, m, f, *v, "4.2"))
            pert[label] = {str(c): sd(lp, c) for c in NODES_IDX}
        folds = fold_logp(pack, m, f, *base)
        fold_sd = {str(c): [sd(folds[i], c) for i in range(len(folds))] for c in NODES_IDX}
        rec["points"][name] = {
            "ensemble_second_diff": {str(c): sd(lnP, c) for c in NODES_IDX},
            "perturbed_second_diff": pert,
            "per_fold_second_diff": fold_sd,
            "per_fold_mean_std": {c: [float(np.mean(v)), float(np.std(v, ddof=1))] for c, v in fold_sd.items()},
        }
    # simulation training spectra at z = 4.2 (CDM), 16 k-bins
    sims = pickle.load(open(ROOT / "phase1_work/agent1_emulator/lya-mfdm/data/all_pk_num2_cdm.pkl", "rb"))
    names = sims.dtype.names
    kcols = [f"{x:.1f}" for x in np.round(np.arange(-2.2, -0.65, 0.1), 1)]   # P1D columns named by log10 k
    rec["sim_fields"] = list(names) if names else None
    pk_field = kcols if names and all(c in names for c in kcols) else []
    if pk_field:
        P = np.array([[float(r[c]) for c in kcols] for r in sims])
        P = P[np.all(P > 0, axis=1)]
        lnS = np.log(P)
        sim_sd = {str(c): (lnS[:, c - 1] - 2 * lnS[:, c] + lnS[:, c + 1]) for c in NODES_IDX}
        rec["sim_second_diff_stats"] = {c: {"median": float(np.median(v)), "p16": float(np.percentile(v, 16)), "p84": float(np.percentile(v, 84)),
                                            "frac_same_sign_as_emulator_fiducial": float(np.mean(np.sign(v) == np.sign(rec["points"]["fiducial_f0"]["ensemble_second_diff"][c])))}
                                        for c, v in sim_sd.items()}
        rec["sim_spectra_used"] = int(P.shape[0]); rec["sim_pk_field"] = "columns -2.2 .. -0.7"
    OUT.write_text(json.dumps(rec, indent=1))
    for name, r in rec["points"].items():
        print(f"== {name}")
        print("   ensemble 2nd diff (nodes 4,5,6):", {c: round(v, 4) for c, v in r["ensemble_second_diff"].items()})
        for lab, v in r["perturbed_second_diff"].items():
            print(f"   {lab:12}:", {c: round(x, 4) for c, x in v.items()})
        print("   per-fold mean ± std:", {c: (round(a, 4), round(b, 4)) for c, (a, b) in r["per_fold_mean_std"].items()})
    if "sim_second_diff_stats" in rec:
        print(f"training sims (z=4.2 CDM, n={rec['sim_spectra_used']}, field {rec['sim_pk_field']}):")
        for c, st in rec["sim_second_diff_stats"].items():
            print(f"   node {c}: median {st['median']:.4f} [p16 {st['p16']:.4f}, p84 {st['p84']:.4f}]  same sign as emulator: {st['frac_same_sign_as_emulator_fiducial']:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
