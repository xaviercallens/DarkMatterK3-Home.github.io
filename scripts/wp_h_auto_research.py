#!/usr/bin/env python3
"""WP-H: auto-research runner for the triaged hypothesis registry.

Executes the RUNNABLE subset of `pipeline/hypothesis_registry.py` against the real
SDSS/Euclid catalogues already recorded in `data/MANIFEST.md`. Every emitted record is
labelled `SANDBOX-EXPERIMENTAL`.

WHAT THIS IS NOT
----------------
Not a test of any hypothesis. Not a formal proof. Gate G1-L is closed; F5b fired; no
derivation links Cooper s7 to any statistic computed here. Each result carries the
`claim_gap` text from the registry stating what it does not establish, so the caveat travels
with the number instead of living only in a report someone might not read.

Authorization: docs/WP_H_T0_AUTHORIZATION_2026_07_25.md (Xavier, direct, 2026-07-25).

GPU
---
Runs on the T4 of Xavier's GCP instance. The GPU computes 3D histograms for batches of null
realizations; all topology (scipy connected components, Euler characteristic) stays on CPU
in the existing verified `pipeline/observables_real.py`. The GPU path is checked against the
numpy path for exact agreement on every field before use — it changes throughput, not a
single reported number, and the run aborts if that ever stops being true.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

import numpy as np
import pandas as pd

from pipeline import gate
from pipeline import hypothesis_registry as reg
from pipeline.cosmology import drop_invalid_redshifts, radec_z_to_tangent_plane_mpc
from pipeline.delta_observable import compute_delta_statistic
from pipeline.observables_real import compute_betti_numbers
from pipeline.realfield3d import (
    angular_csr_realization,
    density_field_cartesian_mpc,
    z_shuffle_realization,
)

# --------------------------------------------------------------------------------------
# Settings. Every one of these is inherited from a prior, T0-signed WP rather than chosen
# here, so the run is comparable to WP-R5/R7 and no new free knob is introduced.
# --------------------------------------------------------------------------------------

NBINS = 8                       # WP-R5/WP-R7 value, for direct comparability
N_NULL = 50                     # WP-R5 §7 / WP-R7 precedent
SCALE_NBINS = [4, 6, 8, 12, 16]  # WP-H scale scan (H-B10); coarser->finer at fixed footprint

# Absolute density thresholds (x mean density), never percentile: WP-R7 §4 found percentile
# thresholds degenerate on sparse fields. The field is normalised to mean 1.0, so these are
# the threshold_value directly.
ABS_THRESHOLDS = [0.5, 1.0, 1.5, 2.0]

OUTPUT_DIR = Path(
    "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/wp_h_auto_research"
)

DATA_ROOT = Path("/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata")

FIELDS = [
    {
        "name": "euclid_z_edf_north",
        "path": DATA_ROOT / "euclid_z/euclid_z_edf_north.csv",
        "ra_col": "right_ascension", "dec_col": "declination", "z_col": "phz_median",
        "survey": "Euclid MER x phz_photo_z (photometric redshift)",
        "manifest_sha256": "8b5b287f3f03165660e6232b904ee264e705788ffd60e67f54169ea2dddac2be",
    },
    {
        "name": "euclid_z_edf_fornax",
        "path": DATA_ROOT / "euclid_z/euclid_z_edf_fornax.csv",
        "ra_col": "right_ascension", "dec_col": "declination", "z_col": "phz_median",
        "survey": "Euclid MER x phz_photo_z (photometric redshift)",
        "manifest_sha256": "4095efd8603519f422bbbdef277228b9a7741345eb4b60ca14d33d085acbc484",
    },
    {
        "name": "euclid_z_edf_south",
        "path": DATA_ROOT / "euclid_z/euclid_z_edf_south.csv",
        "ra_col": "right_ascension", "dec_col": "declination", "z_col": "phz_median",
        "survey": "Euclid MER x phz_photo_z (photometric redshift)",
        "manifest_sha256": "7fe629517de7a620426a60364c47b2f96306b592b6e03752866f417aca6d0b4b",
    },
    {
        "name": "sdss_z_coma_cluster",
        "path": DATA_ROOT / "sdss_z/sdss_z_coma_cluster.csv",
        "ra_col": "ra", "dec_col": "dec", "z_col": "z",
        "survey": "SDSS spectroscopic (spectro=True, real spec-z)",
        "manifest_sha256": "7b7c753e9a116831b8fe820054d85ad57a3c43d1a4ef7d8716a38a22fa3074ea",
    },
]


# --------------------------------------------------------------------------------------
# GPU density field (throughput only — verified identical to the numpy path)
# --------------------------------------------------------------------------------------

def _get_device():
    try:
        import torch
    except ImportError:
        return None, None
    if not torch.cuda.is_available():
        return None, torch
    return torch.device("cuda"), torch


def gpu_density_field(x, y, z, nbins, ranges, torch, device):
    """3D histogram on the GPU, normalised to mean 1.0.

    Mirrors pipeline.realfield3d.density_field_cartesian_mpc exactly, including its
    right-edge inclusion (np.histogramdd puts points equal to the upper edge in the last
    bin) — that edge case is the one place a naive floor() would diverge, so it is handled
    explicitly and covered by the agreement check.
    """
    coords = torch.stack([
        torch.as_tensor(np.asarray(a, dtype=np.float64), device=device) for a in (x, y, z)
    ])  # (3, N)

    idx = torch.empty_like(coords, dtype=torch.long)
    for axis in range(3):
        lo, hi = ranges[axis]
        width = (hi - lo) / nbins
        if width <= 0:
            idx[axis] = 0
            continue
        raw = torch.floor((coords[axis] - lo) / width).to(torch.long)
        raw = torch.clamp(raw, 0, nbins - 1)          # right-edge inclusion + guard
        inside = (coords[axis] >= lo) & (coords[axis] <= hi)
        raw = torch.where(inside, raw, torch.full_like(raw, -1))
        idx[axis] = raw

    valid = (idx >= 0).all(dim=0)
    flat = (idx[0] * nbins * nbins + idx[1] * nbins + idx[2])[valid]
    counts = torch.bincount(flat, minlength=nbins ** 3).to(torch.float64)
    field = counts.reshape(nbins, nbins, nbins)

    mean = field.mean()
    field = field / mean if mean > 0 else torch.ones_like(field)
    return field.cpu().numpy()


# --------------------------------------------------------------------------------------
# Field loading
# --------------------------------------------------------------------------------------

def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def load_field(info: dict) -> dict:
    """Load one manifested catalogue and verify its hash against data/MANIFEST.md."""
    path = Path(info["path"])
    if not path.exists():
        raise FileNotFoundError(
            f"{path} missing. WP-H reads only catalogues already fetched by the WP-R5 "
            "fetchers; it does not fetch. Re-run scripts/fetch_survey_redshifts.py."
        )
    actual = _sha256_file(path)
    if actual != info["manifest_sha256"]:
        raise RuntimeError(
            f"{info['name']}: SHA256 {actual} does not match the value recorded in "
            f"data/MANIFEST.md ({info['manifest_sha256']}). Refusing to compute on data "
            "whose provenance cannot be confirmed."
        )

    df = pd.read_csv(path)
    ra, dec, z, drops = drop_invalid_redshifts(
        df[info["ra_col"]].values, df[info["dec_col"]].values, df[info["z_col"]].values
    )
    ra0, dec0 = float(np.mean(ra)), float(np.mean(dec))
    x, y, zc = radec_z_to_tangent_plane_mpc(ra, dec, z, ra0_deg=ra0, dec0_deg=dec0)
    ranges = ((float(x.min()), float(x.max())),
              (float(y.min()), float(y.max())),
              (float(zc.min()), float(zc.max())))
    return {
        "name": info["name"], "survey": info["survey"], "sha256": actual,
        "n_input": int(len(df)), "n_valid": int(len(ra)), "drop_report": drops,
        "ra": ra, "dec": dec, "z": z, "ra0": ra0, "dec0": dec0, "ranges": ranges,
    }


def field_from_coords(f: dict, ra, dec, z, nbins, torch=None, device=None) -> np.ndarray:
    x, y, zc = radec_z_to_tangent_plane_mpc(ra, dec, z, ra0_deg=f["ra0"], dec0_deg=f["dec0"])
    if device is not None:
        return gpu_density_field(x, y, zc, nbins, f["ranges"], torch, device)
    return density_field_cartesian_mpc(x, y, zc, nbins=nbins, ranges=f["ranges"])


def verify_gpu_matches_cpu(f: dict, torch, device) -> dict:
    """Abort the GPU path unless it reproduces the numpy field bit-for-bit."""
    cpu = field_from_coords(f, f["ra"], f["dec"], f["z"], NBINS)
    gpu = field_from_coords(f, f["ra"], f["dec"], f["z"], NBINS, torch, device)
    exact = bool(np.array_equal(cpu, gpu))
    max_abs = float(np.max(np.abs(cpu - gpu)))
    if not exact:
        raise RuntimeError(
            f"{f['name']}: GPU density field differs from numpy (max |diff| {max_abs:.3e}). "
            "WP-H requires the GPU to change throughput only. Refusing to proceed."
        )
    return {"exact_match": exact, "max_abs_diff": max_abs}


# --------------------------------------------------------------------------------------
# Null bank
# --------------------------------------------------------------------------------------

def null_bank(f: dict, nbins: float, threshold_value: float, torch=None, device=None) -> dict:
    """Betti statistics over both T0-signed null schemes at one (nbins, threshold)."""
    out = {}
    for scheme, fn, seed in (("z_shuffle", z_shuffle_realization, 801),
                             ("angular_csr", angular_csr_realization, 802)):
        rng = np.random.default_rng(seed)
        betti = {"beta_0": [], "beta_1": [], "beta_2": []}
        for _ in range(N_NULL):
            ra_s, dec_s, z_s = fn(f["ra"], f["dec"], f["z"], rng)
            fld = field_from_coords(f, ra_s, dec_s, z_s, nbins, torch, device)
            t = compute_betti_numbers(fld, threshold_value=threshold_value)
            for k in betti:
                betti[k].append(t[k])
        out[scheme] = {
            k: {"mean": float(np.mean(v)), "std": float(np.std(v)),
                "min": int(np.min(v)), "max": int(np.max(v)),
                "nonzero_variance": bool(np.std(v) > 0)}
            for k, v in betti.items()
        }
        out[scheme]["_raw"] = {k: [int(i) for i in v] for k, v in betti.items()}
    return out


def percentile_rank(real: int, nulls: list[int]) -> float | None:
    """Fraction of null realizations strictly below the real value.

    Returns None when the null distribution is degenerate (zero variance) — a percentile
    against a constant is meaningless, and WP-R5 §7 found exactly that for beta_0 at several
    settings. Reporting None is the honest output; reporting 100.0 would not be.
    """
    arr = np.asarray(nulls)
    if arr.std() == 0:
        return None
    return float(100.0 * np.mean(arr < real))


# --------------------------------------------------------------------------------------
# Hypothesis executors. One per runner_key in the registry.
# --------------------------------------------------------------------------------------

def run_betti_dominance(fields, torch, device) -> dict:
    """H-A1: is beta_1 > beta_0 + beta_2 in the real fields?"""
    results = []
    for f in fields:
        per_threshold = []
        for thr in ABS_THRESHOLDS:
            fld = field_from_coords(f, f["ra"], f["dec"], f["z"], NBINS, torch, device)
            t = compute_betti_numbers(fld, threshold_value=thr)
            per_threshold.append({
                "threshold_x_mean": thr,
                "beta_0": t["beta_0"], "beta_1": t["beta_1"], "beta_2": t["beta_2"],
                "euler_char": t.get("euler_characteristic"),
                "beta_1_gt_beta_0_plus_beta_2": bool(
                    t["beta_1"] > t["beta_0"] + t["beta_2"]),
            })
        results.append({"field": f["name"], "n_valid": f["n_valid"],
                        "per_threshold": per_threshold})
    return {"fields": results}


def run_beta2_density_split(fields, torch, device) -> dict:
    """H-B2: beta_2 contrast between low- and high-density thresholds, with nulls."""
    results = []
    for f in fields:
        fld = field_from_coords(f, f["ra"], f["dec"], f["z"], NBINS, torch, device)
        low = compute_betti_numbers(fld, threshold_value=0.5)
        high = compute_betti_numbers(fld, threshold_value=2.0)
        nb_low = null_bank(f, NBINS, 0.5, torch, device)
        nb_high = null_bank(f, NBINS, 2.0, torch, device)
        results.append({
            "field": f["name"],
            "low_threshold_x_mean": 0.5, "high_threshold_x_mean": 2.0,
            "beta_2_low": low["beta_2"], "beta_2_high": high["beta_2"],
            "beta_2_contrast": int(low["beta_2"] - high["beta_2"]),
            "beta_2_percentile_low": {
                s: percentile_rank(low["beta_2"], nb_low[s]["_raw"]["beta_2"])
                for s in ("z_shuffle", "angular_csr")},
            "beta_2_percentile_high": {
                s: percentile_rank(high["beta_2"], nb_high[s]["_raw"]["beta_2"])
                for s in ("z_shuffle", "angular_csr")},
        })
    return {"fields": results,
            "note": "Descriptive density-split contrast only. There is no Cooper-s7 beta_2 "
                    "prediction and no LambdaCDM N-body mock in this repo, so this is not "
                    "the comparison H-B2 states."}


def _chameleon_like_kernel(rho, rho_scale):
    """Generic density-dependent warp: suppressed where dense, active where sparse.

    k(rho) = 1 / (1 + rho/rho_scale). This is a *generic stand-in* for a screening-shaped
    response, NOT derived from any EFT — the same posture as WP-E's deformation classes
    (docs/WP_E_EMPIRICAL_BOUNDS.md §1). It exists so the Delta statistic is non-degenerate;
    it encodes no model and no constant requiring provenance.
    """
    return 1.0 / (1.0 + np.asarray(rho, dtype=np.float64) / max(rho_scale, 1e-300))


def run_delta_stability(fields, torch, device) -> dict:
    """H-B9: field-to-field scatter of the regenerated Delta statistic.

    Uses the WP-D regenerated definition ([A-DATA-WD]); imports no [A-DATA-LEGACY] value
    and evaluates against no threshold.

    DEGENERACY GUARD: compute_delta_statistic with kernel_func=None sets warped == raw, so
    Delta is identically 0 by construction (pipeline/tests/test_delta_observable.py::
    test_delta_null_field_with_identity_kernel_is_zero asserts exactly this). An initial
    WP-H run did precisely that and produced sigma_Delta = 0.000000 across all four fields
    — a tautology, not a stability result, and the same no-op failure mode that got WP-R3's
    null bank retracted (docs/FINDING_R_NULLDEGENERATE_2026_07_25.md). Both branches are
    now computed and the identity branch is asserted to be zero, so the degeneracy is
    documented rather than mistaken for a finding.
    """
    per_field = []
    for f in fields:
        fld = field_from_coords(f, f["ra"], f["dec"], f["z"], NBINS, torch, device)
        d_identity = compute_delta_statistic(fld, kernel_func=None)
        d_warp = compute_delta_statistic(fld, kernel_func=_chameleon_like_kernel)
        per_field.append({
            "field": f["name"],
            "delta_identity_kernel": float(d_identity["delta"]),
            "delta_generic_warp": float(d_warp["delta"]),
        })

    identity = [p["delta_identity_kernel"] for p in per_field]
    warped = [p["delta_generic_warp"] for p in per_field]

    if any(v != 0.0 for v in identity):
        raise RuntimeError(
            "Identity-kernel Delta is non-zero; the estimator's definition has changed and "
            "this executor's degeneracy guard is stale. Stop and re-derive."
        )
    if float(np.std(warped)) == 0.0 and len(set(warped)) == 1:
        raise RuntimeError(
            "Generic-warp Delta is constant across four different real fields. That is the "
            "no-op signature (cf. WP-R3 retraction). Refusing to report it as stability."
        )

    return {
        "per_field": per_field,
        "identity_kernel_is_degenerate_by_construction": True,
        "sigma_delta_across_fields": float(np.std(warped)),
        "mean_delta_across_fields": float(np.mean(warped)),
        "threshold_applied": None,
        "note": "sigma_Delta is REPORTED, not evaluated against the brief's unprovenanced "
                "0.1 threshold. The identity-kernel column is 0 by construction and is kept "
                "only as the degeneracy guard. The warp kernel is a generic screening-shaped "
                "stand-in (not an EFT, not s7/s10), so this measures estimator/field scatter, "
                "not any model.",
    }


def run_scale_scan(fields, torch, device) -> dict:
    """H-B10: how beta_1/beta_2 vary with grid resolution."""
    results = []
    for f in fields:
        per_scale = []
        for nb in SCALE_NBINS:
            fld = field_from_coords(f, f["ra"], f["dec"], f["z"], nb, torch, device)
            t = compute_betti_numbers(fld, threshold_value=1.0)
            xr, yr, zr = f["ranges"]
            per_scale.append({
                "nbins": nb,
                "transverse_bin_mpc_x": float((xr[1] - xr[0]) / nb),
                "transverse_bin_mpc_y": float((yr[1] - yr[0]) / nb),
                "radial_bin_mpc": float((zr[1] - zr[0]) / nb),
                "beta_0": t["beta_0"], "beta_1": t["beta_1"], "beta_2": t["beta_2"],
            })
        results.append({"field": f["name"], "per_scale": per_scale})
    return {"fields": results,
            "note": "Bin sizes are reported so the scan can be read against the WP-R6 "
                    "resolution floor (0.22-0.27 Mpc transverse). Scale dependence of Betti "
                    "numbers is generic to point processes and excludes nothing."}


def run_null_percentiles(fields, torch, device) -> dict:
    """H-C4/H-C5: real Betti numbers against the T0-signed null bank."""
    results = []
    for f in fields:
        per_threshold = []
        for thr in ABS_THRESHOLDS:
            fld = field_from_coords(f, f["ra"], f["dec"], f["z"], NBINS, torch, device)
            real = compute_betti_numbers(fld, threshold_value=thr)
            nb = null_bank(f, NBINS, thr, torch, device)
            per_threshold.append({
                "threshold_x_mean": thr,
                "real": {k: real[k] for k in ("beta_0", "beta_1", "beta_2")},
                "null_summary": {s: {k: nb[s][k] for k in ("beta_0", "beta_1", "beta_2")}
                                 for s in ("z_shuffle", "angular_csr")},
                "percentile_rank": {
                    s: {k: percentile_rank(real[k], nb[s]["_raw"][k])
                        for k in ("beta_0", "beta_1", "beta_2")}
                    for s in ("z_shuffle", "angular_csr")},
            })
        results.append({"field": f["name"], "per_threshold": per_threshold})
    return {
        "fields": results,
        "note": "The control is a structure-destroying randomization (z-shuffle / angular "
                "CSR), NOT a LambdaCDM N-body mock — the repo has none. A percentile against "
                "CSR is a weaker statement than one against LambdaCDM and must be read as "
                "such. 'null' percentile of None means the null distribution had zero "
                "variance at that setting (WP-R5 section 7 percolation regime).",
    }


EXECUTORS = {
    "betti_dominance": run_betti_dominance,
    "beta2_density_split": run_beta2_density_split,
    "delta_stability": run_delta_stability,
    "scale_scan": run_scale_scan,
    "null_percentiles": run_null_percentiles,
}


# --------------------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------------------

def print_triage() -> None:
    counts = reg.status_counts()
    print(f"WP-H triage of {len(reg.HYPOTHESES)} hypotheses "
          f"(source: briefs/SOURCE_autoresearch_brief_2026_07_25.md)\n")
    for status in ("RUNNABLE", "BLOCKED_DATA", "BLOCKED_PROVENANCE", "OUT_OF_SCOPE"):
        n = counts.get(status, 0)
        print(f"  {status:<20} {n}")
    print()
    for h in reg.HYPOTHESES:
        mark = "RUN " if h.status == "RUNNABLE" else "STOP"
        detail = h.runner_key if h.status == "RUNNABLE" else h.status
        print(f"  [{mark}] {h.hid:<8} {detail:<22} {h.statement[:64]}")


def preflight() -> dict:
    """Gate checks. G1 must be open (real-data access); G1-L must be closed (labelling)."""
    gate.require_pinned_for_real_data()
    if gate.labels_unlocked():
        raise RuntimeError(
            "Gate G1-L is OPEN. WP-H was authorized on the premise that it is closed and "
            "that all output is SANDBOX-EXPERIMENTAL. Stop and get a fresh T0 review."
        )
    reg.assert_label_permitted(reg.TAG)
    return {
        "g1_is_pinned": gate.is_pinned(),
        "g1_pin_hash_valid": gate.verify_pin_hash(),
        "g1l_labels_unlocked": gate.labels_unlocked(),
        "label": reg.TAG,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="WP-H auto-research runner (SANDBOX-EXPERIMENTAL)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the triage table and exit without touching data")
    ap.add_argument("--cpu", action="store_true", help="disable the GPU path")
    args = ap.parse_args()

    print_triage()
    if args.dry_run:
        print("\n--dry-run: no data touched.")
        return 0

    print("\n--- pre-flight ---")
    gates = preflight()
    print(f"  G1 pinned={gates['g1_is_pinned']} hash_valid={gates['g1_pin_hash_valid']} "
          f"| G1-L labels_unlocked={gates['g1l_labels_unlocked']} (must be False)")

    device, torch = (None, None) if args.cpu else _get_device()
    gpu_info = {"used": device is not None}
    if device is not None:
        gpu_info["device_name"] = torch.cuda.get_device_name(0)
        gpu_info["torch_version"] = torch.__version__
        print(f"  GPU: {gpu_info['device_name']} (torch {torch.__version__})")
    else:
        print("  GPU: not used (CPU path)")

    print("\n--- loading manifested catalogues ---")
    fields = []
    for info in FIELDS:
        f = load_field(info)
        print(f"  {f['name']:<22} n_valid={f['n_valid']:<6} sha256 verified")
        fields.append(f)

    if device is not None:
        checks = {f["name"]: verify_gpu_matches_cpu(f, torch, device) for f in fields}
        gpu_info["cpu_agreement"] = checks
        print(f"  GPU/CPU density fields: exact match on all {len(checks)} fields")

    print("\n--- executing RUNNABLE hypotheses ---")
    executed, started = {}, datetime.now(timezone.utc)
    for key in reg.runner_keys():
        hids = [h.hid for h in reg.runnable() if h.runner_key == key]
        print(f"  {key} ({', '.join(hids)}) ...", flush=True)
        executed[key] = {
            "hypotheses": hids,
            "label": reg.TAG,
            "claim_gaps": {h.hid: reg.by_id(h.hid).claim_gap for h in reg.runnable()
                           if h.runner_key == key},
            "result": EXECUTORS[key](fields, torch, device),
        }

    payload = {
        "work_package": "WP-H",
        "label": reg.TAG,
        "not_a_test": "No hypothesis is confirmed or refuted by this run. Gate G1-L closed; "
                      "F5b fired; no derivation links the model to any statistic here.",
        "authorization": "docs/WP_H_T0_AUTHORIZATION_2026_07_25.md",
        "source_brief": "briefs/SOURCE_autoresearch_brief_2026_07_25.md "
                        "(sha256 19eafed983e75523e5a5e5e30432cd694a1cc8008a23c05602cda578fb406063)",
        "generated_utc": started.isoformat(),
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "gates": gates,
        "gpu": gpu_info,
        "settings": {"nbins": NBINS, "n_null_realizations": N_NULL,
                     "absolute_thresholds_x_mean": ABS_THRESHOLDS,
                     "scale_scan_nbins": SCALE_NBINS,
                     "null_schemes": ["z_shuffle", "angular_csr"],
                     "null_schemes_provenance": "WP-R5 corrected schemes, T0-signed "
                                                "(docs/T0_SIGNOFF_WP_R5_R6_R7_2026_07_25.md). "
                                                "WP-R3's retracted schemes are NOT used."},
        "fields": [{"name": f["name"], "survey": f["survey"], "sha256": f["sha256"],
                    "n_input": f["n_input"], "n_valid": f["n_valid"]} for f in fields],
        "triage": {"counts": reg.status_counts(),
                   "records": [h.to_dict() for h in reg.HYPOTHESES]},
        "executed": executed,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / f"wp_h_results_{started:%Y_%m_%d}.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    digest = _sha256_file(out)

    print(f"\nresults: {out}")
    print(f"sha256:  {digest}")
    print(f"label:   {reg.TAG} — never TEST, never FIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# Generated-by: Claude Opus 5 (T1) under T0 authorization of 2026-07-25 |
# Verified-by: GPU/CPU exact-agreement check per field at runtime; gate pre-flight asserts
# G1 open and G1-L closed; pipeline/tests/test_hypothesis_registry.py covers dispatch |
# Reviewed-by: T0 N — pending Xavier
