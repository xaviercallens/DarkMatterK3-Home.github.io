#!/usr/bin/env python3
"""
WP-E6-SWEEP — emulator evaluation at k_eff + interpolation systematic (design §4)

ENGINEERING / DESIGN label (CLAUDE.md rule 3). This module performs no model–data comparison.
Every comparison that consumes its output is exclusion/FIT, never TEST.

Authority: T0 ruling A2 2026-09-17 (Option B), pinned in
`briefs/WP_E6_SWEEP_KEFF_RULING_PINNED_2026_09_17.md` (pin commit 57a6065, which predates this file).

  K1  predict_at_keff()       log-log linear interpolation of the 16 native emulator bins at each
                              band's k_eff; band 0 extrapolates 0.003 dex; > 0.01 dex beyond a grid
                              edge is a hard stop (KeffCapError), never a clamp.
  K2  augmented_covariance()  C₉,sys = C₉ + diag((β_b σ_b)²) with the pinned β; the term is fixed and
                              data-independent, and is checked against the pinned table.
  K3  sweep_gate()            mechanical pre-sweep gate over the pinned pre-check JSON, the C₉/k_eff
                              artifact and (optionally) the live emulator wrapper.
  (K4 "no variants": this module exposes no k_target or no-systematic path.)
"""
import hashlib
import json
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent

NATIVE_LOG10K = np.round(np.arange(-2.2, -0.65, 0.1), 1)      # 16 emulator bins, s/km
N_BANDS = 9
EXTRAPOLATION_CAP_DEX = 0.01

AGG_JSON = REPO_ROOT / "data/derived/wp_e6_sweep_cov_agg9_z4p2_2026_09_16.json"
AGG_NPY = REPO_ROOT / "data/derived/wp_e6_sweep_cov_agg9_z4p2_2026_09_16.npy"
PRECHECK_JSON = REPO_ROOT / "data/derived/wp_e6_sweep_keff_emulator_precheck_2026_09_17.json"
PRECHECK_SHA256 = "508717c8fa87e07e77a871b7d184e6525975cfea6357922ba9f02adf2bbace2c"
GRID_CONTROLS_JSON = REPO_ROOT / "data/derived/wp_e6_grid_controls_report_2026_07_28.json"

# Pinned K2 table (WP_E6_SWEEP_KEFF_RULING_PINNED_2026_09_17.md). Copied, not recomputed at import:
# augmented_covariance() re-derives these from the artifacts and hard-stops on disagreement.
PINNED_BETA = np.array([0.161049, 0.208265, 0.062253, 0.029042, 0.162314,
                        0.311839, 0.055129, 0.003139, 0.029494])
PINNED_TERM = np.array([0.56416863, 0.62891846, 0.04306201, 0.00525071, 0.11954302,
                        0.39281729, 0.01353629, 0.00005315, 0.00612911])
PIN_TOL_REL = 1e-6


class KeffCapError(ValueError):
    """Evaluation requested beyond the pinned 0.01-dex extrapolation cap (K1 hard stop)."""


class PinMismatchError(RuntimeError):
    """An artifact or derived value disagrees with the pinned ruling (K2/K3 hard stop)."""


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_k_eff(agg_json=AGG_JSON):
    return np.asarray(json.load(open(agg_json))["k_eff_s_per_km"], dtype=float)


def predict_at_keff(p_native, k_eff):
    """K1: log-log linear interpolation of the emulator's native P1D at each band's k_eff.

    p_native: 16 positive values on NATIVE_LOG10K (emulator output order).
    k_eff:    N_BANDS effective wavenumbers (s/km).
    """
    p_native = np.asarray(p_native, dtype=float)
    k_eff = np.asarray(k_eff, dtype=float)
    if p_native.shape != NATIVE_LOG10K.shape:
        raise ValueError(f"expected {NATIVE_LOG10K.size} native bins, got {p_native.shape}")
    if not np.all(np.isfinite(p_native)) or np.any(p_native <= 0):
        raise ValueError("native P1D must be finite and positive for log-log interpolation")
    x = np.log10(k_eff)
    lo_edge, hi_edge = NATIVE_LOG10K[0], NATIVE_LOG10K[-1]
    beyond = np.maximum(lo_edge - x, x - hi_edge)
    if np.any(beyond > EXTRAPOLATION_CAP_DEX):
        b = int(np.argmax(beyond))
        raise KeffCapError(f"band {b}: log10 k_eff = {x[b]:.4f} is {beyond[b]:.4f} dex beyond the "
                           f"native grid (cap {EXTRAPOLATION_CAP_DEX} dex)")
    lnp = np.log(p_native)
    # segment index i such that the segment is (NATIVE_LOG10K[i], NATIVE_LOG10K[i+1]); edges extrapolate
    i = np.clip(np.searchsorted(NATIVE_LOG10K, x, side="right") - 1, 0, NATIVE_LOG10K.size - 2)
    x0, x1 = NATIVE_LOG10K[i], NATIVE_LOG10K[i + 1]
    t = (x - x0) / (x1 - x0)
    return np.exp(lnp[i] + t * (lnp[i + 1] - lnp[i]))


def systematic_term(cov9, beta):
    sigma = np.sqrt(np.diag(np.asarray(cov9, dtype=float)))
    return (np.asarray(beta, dtype=float) * sigma) ** 2


def pinned_beta(precheck_json=PRECHECK_JSON):
    """Full-precision β from the pinned pre-check JSON, checked against the pinned table's 6-decimal rounding."""
    beta = np.asarray(json.load(open(precheck_json))["bound_sigma_max_per_band"], dtype=float)
    if beta.shape != (N_BANDS,) or not np.all(np.abs(beta - PINNED_BETA) <= 5e-7 + 1e-12):
        raise PinMismatchError(f"pre-check β {beta} disagrees with pinned β table {PINNED_BETA}")
    return beta


def augmented_covariance(cov9, precheck_json=PRECHECK_JSON):
    """K2: C₉,sys = C₉ + diag((β_b σ_b)²), β from the pinned pre-check; hard-stops on any pin mismatch."""
    cov9 = np.asarray(cov9, dtype=float)
    if cov9.shape != (N_BANDS, N_BANDS) or not np.allclose(cov9, cov9.T, rtol=0, atol=1e-12 * np.abs(cov9).max()):
        raise PinMismatchError("C₉ must be a symmetric 9×9 matrix")
    term = systematic_term(cov9, pinned_beta(precheck_json))
    # the pinned K2 table prints s_b² to 8 decimals
    if not np.all(np.abs(term - PINNED_TERM) <= 5e-9 + 1e-12):
        raise PinMismatchError(f"derived term {term} disagrees with pinned K2 table {PINNED_TERM}")
    out = cov9 + np.diag(term)
    np.linalg.cholesky(out)   # raises LinAlgError: hard stop, no pseudo-inverse
    return out


def sweep_gate(precheck_json=PRECHECK_JSON, agg_npy=AGG_NPY, agg_json=AGG_JSON,
               expected_sha256=PRECHECK_SHA256, emulator=None, out_path=None):
    """K3: mechanical pre-sweep gate. Returns a record; `passes` is True only if every item holds.

    emulator: optional (predict_pk, pack) pair. If given, item 3 checks it reproduces the
    2026-07-28 grid-control CDM reference (max rel. diff ≤ 1e-6); if None, item 3 is recorded
    as NOT_RUN and the gate does not pass (the sweep cannot run without the emulator anyway).
    The record is written to out_path (if given) before it is returned.
    """
    rec = {"label": "ENGINEERING/DESIGN — WP-E6-SWEEP K3 gate; not TEST, not FIT",
           "pin": "briefs/WP_E6_SWEEP_KEFF_RULING_PINNED_2026_09_17.md", "items": {}}
    items = rec["items"]
    try:
        sha = _sha256(precheck_json)
        items["1_precheck_sha256"] = {"pass": sha == expected_sha256, "sha256": sha}
    except OSError as exc:
        items["1_precheck_sha256"] = {"pass": False, "error": str(exc)}
    try:
        pc = json.load(open(precheck_json))
        flags = {k: bool(pc.get(k)) for k in ("control_1_pass", "control_2_cap_fires", "band0_within_cap")}
        flags["wrapper_regression"] = bool(pc.get("wrapper_regression", {}).get("pass"))
        items["2_precheck_flags"] = {"pass": all(flags.values()), **flags}
    except (OSError, ValueError) as exc:
        items["2_precheck_flags"] = {"pass": False, "error": str(exc)}
    if emulator is None:
        items["3_emulator_regression"] = {"pass": False, "status": "NOT_RUN (no emulator supplied)"}
    else:
        predict_pk, pack = emulator
        ref = json.load(open(GRID_CONTROLS_JSON))
        med = ref["igm_nuisance_point"]
        p_ref = np.asarray(ref["checks"][0]["pk_reference"], dtype=float)
        p_now = predict_pk(pack, -22.9, 0.0, med["zrei"], med["ha"], med["hs"], med["taueff"], "4.2")
        rel = float(np.max(np.abs(np.asarray(p_now) / p_ref - 1)))
        items["3_emulator_regression"] = {"pass": rel <= 1e-6, "max_rel_diff": rel}
    try:
        cov9 = np.load(agg_npy)
        aug = augmented_covariance(cov9, precheck_json)
        diff = np.diag(aug) - np.diag(cov9)
        exact = systematic_term(cov9, pinned_beta(precheck_json))    # K2: ≤ 1e-6 relative to artifacts
        rel = float(np.max(np.abs(diff / exact - 1)))
        k_eff = load_k_eff(agg_json)
        predict_at_keff(np.ones(NATIVE_LOG10K.size), k_eff)      # cap check on the pinned k_eff
        items["4_augmented_covariance"] = {"pass": rel <= PIN_TOL_REL, "max_rel_diff_vs_artifact_term": rel,
                                           "max_abs_diff_vs_pinned_table": float(np.max(np.abs(diff - PINNED_TERM))),
                                           "cholesky": True, "k_eff_within_cap": True}
    except (PinMismatchError, KeffCapError, np.linalg.LinAlgError, OSError, ValueError) as exc:
        items["4_augmented_covariance"] = {"pass": False, "error": f"{type(exc).__name__}: {exc}"}
    rec["passes"] = all(v["pass"] for v in items.values())
    if out_path is not None:
        Path(out_path).write_text(json.dumps(rec, indent=1))
    return rec
