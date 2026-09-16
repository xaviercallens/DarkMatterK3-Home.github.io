#!/usr/bin/env python3
"""WP-E6-SWEEP — independent re-run of the 9×9 aggregation + audit of the §4 k_eff estimate.

ENGINEERING / DESIGN, DRAFT label (CLAUDE.md rule 3). No emulator is run and no model
comparison is made: the k_eff offsets are estimated from the DESI data table alone.

Independence (producer ≠ verifier, EXECUTION_PLAN_2026_07_29 §0 rule 1): written in a
different session (Claude Opus 5) from the producer (Claude Fable 5.1). It does NOT import
pipeline/; the band grouping is re-derived from the pinned design text (0.1-dex bands
centred on log10 k = -2.2 … -1.4, half-open [c-0.05, c+0.05)), the member covariance is
re-extracted from the hash-gated FITS, and the rule is the pinned design §1.2 formula.
Same repo, same machine, same T1 role — not an external audit.

    python scripts/fetch_data.py
    python scripts/wp_e6_sweep_rerun_and_keff_audit_2026_09_16.py

Writes data/derived/wp_e6_sweep_rerun_keff_audit_2026_09_16.json (persisted before any print).
"""
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from astropy.io import fits

REPO_ROOT = Path(__file__).resolve().parent.parent
FITS_PATH = (REPO_ROOT / "data" / "raw" / "desi_dr1_lya_p1d_zenodo"
             / "desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits")
FITS_SHA256 = "bbb98dc3d1865a50bb878e949a644604ce729da419db8e7db5adbb532a894857"
DESI_CSV = REPO_ROOT / "data" / "literature" / "desi_dr1_lya_p1d_2026_07_27.csv"
ART_NPY = REPO_ROOT / "data" / "derived" / "wp_e6_sweep_cov_agg9_z4p2_2026_09_16.npy"
ART_JSON = REPO_ROOT / "data" / "derived" / "wp_e6_sweep_cov_agg9_z4p2_2026_09_16.json"
OUT_JSON = REPO_ROOT / "data" / "derived" / "wp_e6_sweep_rerun_keff_audit_2026_09_16.json"
Z = 4.2
CENTRES = np.round(np.arange(-2.2, -1.35, 0.1), 1)
# Slopes as printed in the uncommitted draft of briefs/T0_DECISION_REQUEST_SWEEP_KEFF_2026_09_16.md
DRAFT_SLOPES = [-0.91, -0.20, -1.46, -0.14, 0.43, -2.89, -1.08, -1.60, -3.04]


def main() -> int:
    if not FITS_PATH.exists():
        print(f"FITS not found: {FITS_PATH}\nRun: python scripts/fetch_data.py")
        return 1
    sha = hashlib.sha256(FITS_PATH.read_bytes()).hexdigest()
    if sha != FITS_SHA256:
        print(f"SHA-256 mismatch: {sha}")
        return 1

    with fits.open(FITS_PATH) as h:
        tab = h["P1D_BLIND"].data
        cov_full = np.asarray(h["COVARIANCE"].data, dtype=float)
        fits_idx = np.where(np.isclose(tab["Z"], Z))[0]
        k_fits = np.asarray(tab["K"][fits_idx], dtype=float)

    rows = [r for r in csv.DictReader(open(DESI_CSV)) if abs(float(r["z"]) - Z) < 1e-6]
    k = np.array([float(r["k_s_per_km"]) for r in rows])
    p = np.array([float(r["p1d_kms"]) for r in rows])
    e_tot = np.array([float(r["e_total_kms"]) for r in rows])
    pfid = np.array([float(r["pfid_kms"]) for r in rows])
    if len(k) != len(k_fits) or not np.allclose(k, k_fits):
        print("CSV/FITS k-grid mismatch at z=4.2")
        return 1

    lk = np.log10(k)
    groups = [np.where((lk >= c - 0.05) & (lk < c + 0.05))[0] for c in CENTRES]
    sel = np.concatenate(groups)
    cov_m = cov_full[np.ix_(fits_idx[sel], fits_idx[sel])]

    W = np.zeros((len(groups), len(sel)))
    off = 0
    for b, g in enumerate(groups):
        inv = 1.0 / np.diag(cov_m)[off:off + len(g)]
        W[b, off:off + len(g)] = inv / inv.sum()
        off += len(g)
    c9 = W @ cov_m @ W.T
    p9 = W @ p[sel]
    k_eff = W @ k[sel]
    k_t = 10.0 ** CENTRES
    sig9 = np.sqrt(np.diag(c9))
    np.linalg.cholesky(c9)  # hard stop if not PD

    art = np.load(ART_NPY)
    art_json = json.load(open(ART_JSON))
    rerun = {
        "group_sizes": [len(g) for g in groups],
        "diag_vs_e_total_sq_max_rel": float(np.max(abs(np.diag(cov_m) / e_tot[sel] ** 2 - 1))),
        "C9_max_rel_diff_vs_artifact": float(np.max(abs(c9 / art - 1))),
        "P9_max_rel_diff_vs_artifact": float(np.max(abs(p9 / np.array(art_json["data_agg_p1d_kms"]) - 1))),
        "keff_ratio_max_abs_diff_vs_artifact": float(np.max(abs(k_eff / k_t - np.array(art_json["k_eff_over_k_target"])))),
        "sigma9": sig9.tolist(),
        "condition_number": float(np.linalg.cond(c9)),
    }

    # --- §4 offset estimates from the data table (no emulator) ---
    ln_k, ln_p = np.log(k), np.log(p)
    ln_r = np.log(k_eff / k_t)

    def summarise(slopes=None, dp=None):
        if dp is None:
            dp = np.asarray(slopes) * ln_r * p9
        return {
            "slopes": None if slopes is None else [float(s) for s in slopes],
            "pct": (np.abs(dp) / p9 * 100).tolist(),
            "shift_over_sigma": (np.abs(dp) / sig9).tolist(),
            "max_shift_over_sigma": float(np.max(np.abs(dp) / sig9)),
            "argmax_band": int(np.argmax(np.abs(dp) / sig9)),
            "chi2_offset": float(dp @ np.linalg.solve(c9, dp)),
        }

    def band_ols(y):
        out, o = [], 0
        for g in groups:
            m = sel[o:o + len(g)]
            out.append(np.polyfit(ln_k[m], y[m], 1)[0])
            o += len(g)
        return out

    grad = np.gradient(ln_p, ln_k)
    p_eff = np.exp(np.interp(np.log(k_eff), ln_k, ln_p))
    p_tgt = np.exp(np.interp(np.log(k_t), ln_k, ln_p))
    estimates = {
        "smooth: OLS of ln P on ln k within band (PLYA)": summarise(band_ols(ln_p)),
        "smooth: OLS within band on DESI fiducial PFID": summarise(band_ols(np.log(pfid))),
        "smooth: gradient across the 9 band centres (P9)": summarise(np.gradient(np.log(p9), np.log(k_t))),
        "point-to-point: log-log interpolation of table, P(k_eff)-P(k_target)": summarise(dp=p_eff - p_tgt),
        "point-to-point: central-difference gradient, interpolated to k_target": summarise(np.interp(np.log(k_t), ln_k, grad)),
        "draft brief slope column (as printed, recomputed here)": summarise(DRAFT_SLOPES),
    }

    payload = {
        "label": "DRAFT (ENGINEERING/DESIGN — not TEST, not FIT); no emulator run, no model comparison",
        "wp": "WP-E6-SWEEP (independent re-run of aggregation + design §4 offset audit)",
        "generated": datetime.now(timezone.utc).isoformat(),
        "generated_by": "Claude Opus 5 (session distinct from producer Claude Fable 5.1); no pipeline/ import",
        "fits_sha256": sha,
        "rerun": rerun,
        "k_eff_over_k_target": (k_eff / k_t).tolist(),
        "p9_kms": p9.tolist(),
        "offset_estimates": estimates,
    }
    with open(OUT_JSON, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {OUT_JSON}")
    for key, val in rerun.items():
        print(f"  {key}: {val}")
    for name, e in estimates.items():
        print(f"  {name}: max shift/σ={e['max_shift_over_sigma']:.2f} (band {e['argmax_band']}), "
              f"chi2={e['chi2_offset']:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
