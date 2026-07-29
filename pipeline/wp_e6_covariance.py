#!/usr/bin/env python3
"""
WP-E6-P2A -- Hartlap-corrected mock covariance build for the DESI-like Lyman-alpha
P1D comparison (ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md Part A).

label: ENGINEERING / DESIGN (CLAUDE.md rule 3 -- not TEST, not FIT). This script
touches no real DESI data and no pinned PREDICTION.md artifact; it is entirely
`desisim`-synthetic infrastructure (CLAUDE.md rule 1, synthetic-data infra only).

Status: DRAFT. Producer != verifier (EXECUTION_PLAN_2026_07_29 Sec.0 rule 1) -- this
output has NOT been promoted to LIVE and must not be treated as final until a
separate verification pass accepts it.

---------------------------------------------------------------------------
HEADLINE FINDING -- dimension conflict, escalate before P2B/SWEEP consume this
---------------------------------------------------------------------------
`emu_predict.py`'s K_BINS grid (16 values, log10 k = -2.2 .. -0.7 in steps of 0.1,
units s/km) was assumed to be directly buildable as a 16x16 sample covariance from
this desisim pipeline. It is NOT, for a real, discovered-during-execution reason
(not a coding mistake carried in from the task brief):

  The DESI B-camera output grid that `sim_spectra()` resamples onto has a native
  pixel scale of ~1.0 Angstrom (measured empirically below, not assumed), giving a
  velocity pixel width dv_kms ~ 60.8 km/s and hence an FFT Nyquist frequency
  k_Nyquist = pi / dv_kms ~ 0.0516 s/km. Six of the sixteen K_BINS values are above
  this (log10 k = -1.3 through -0.7; the -1.3 bin sits at 0.97x Nyquist, i.e. its
  target 0.05-dex band only partially overlaps resolved native modes). This is a
  genuine instrumental-resolution ceiling of the synthetic B-camera output, not an
  artifact of N, seed choice, or windowing -- more realizations does not fix it.

  Per EXECUTION_PLAN_2026_07_29.md Sec.0 rule 7 ("never fabricate a fallback
  result") this script does NOT extrapolate power into the unresolved bins. It
  delivers a **9x9 measurable sub-block** (log10 k = -2.2 .. -1.4, all fully within
  the resolved band) plus an explicit index map showing which of the 16 target bins
  are and are not covered. The task-specified p=16 Hartlap factor (182/199) is
  still printed verbatim per the task instruction, but the factor actually baked
  into the stored inverse uses p=9 (the true delivered dimension): see
  `hartlap_factor_p16_task_specified` vs `hartlap_factor_p9_applied` in the output
  JSON and the printed summary below.

  This blocks P2A's promotion to LIVE and blocks WP-E6-P2B / WP-E6-SWEEP from
  using a 16-bin chi^2 as currently scoped -- flagged for T0/coordinator, not
  resolved here.
---------------------------------------------------------------------------

Also deviates from `phase1_work/agent3_synthetic/compare_p1d.py`'s estimator on
purpose (documented, not silent):
  - `compare_p1d.py::flux_power_1d()` FFTs the mean-SUBTRACTED absolute flux
    (units: flux^2 * km/s), not the flux-CONTRAST field delta_F = flux/mean - 1
    (units: km/s, matching a standard P1D and the emulator's own quantity). This
    script uses delta_F so the covariance is dimensionally comparable to
    `emu_predict.py`'s K_BINS-indexed P1D output. See `flux_power_1d_delta()`.
  - No MASK_FRAC pixel masking is applied here. ANALYSIS_PROTOCOL Part A/C are
    coupled (Sec 1.3: "A consumes C's corrected estimator") but WP-E6-P2C (the
    masking bug fix) has not landed yet as of this run. Baking the CURRENT
    known-buggy zero-fill estimator (Bug 1: edge discontinuity; Bug 2: biased
    mean-over-zero-filled-pixels) into a covariance artifact would encode a known
    defect permanently. This covariance is therefore built on the UNMASKED
    sim_spectra output. It will likely need regeneration once P2C's corrected
    estimator lands -- flagged, not resolved, here.

Batching / seeds:
  Two independent timing points measured in this session (Ns=4: 10.54s;
  Ns=50: 11.91s for the sim_spectra step) give an intercept of ~10.4s fixed cost
  per `sim_spectra()` call plus ~0.03s/skewer marginal -- i.e. per-call overhead
  dominates at small Ns. 200 single-realization calls would cost roughly
  200 * 10.4s =~ 35 min (~43x the 48s N=200 benchmark), tripping the >10x STOP
  trigger. The N=50-per-call structure is exactly what the WP_P2t timing brief
  benchmarked (48s for N=200 via linear scaling of one N=50 batch), so this script
  uses 4 batches of 50, each with its own recorded, distinct seed -- this keeps
  wall-clock close to the benchmarked structure while still giving genuinely
  distinct per-batch seeds (not one shared seed for all 200). Every one of the 200
  realizations gets a recorded {realization_id, batch_seed, row_in_batch} entry
  (distinct per realization by construction: same seed + different row index is a
  different, reproducible draw from that batch's RNG stream).

Environment: venv /home/callensxavier_gmail_com/venv (py3.10.12). Requires
DESIMODEL env var set before import (see main()). NO mpi4py.
"""
import json
import os
import sys
import time
import tempfile
import shutil
from datetime import datetime, timezone

import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "phase1_work", "agent1_emulator"))

DESIMODEL_PATH = os.path.join(
    REPO_ROOT, "phase1_work", "agent3_synthetic", "desimodel_data_test"
)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
N_TOTAL = 200
BATCH_SIZE = 50
N_BATCHES = N_TOTAL // BATCH_SIZE
assert N_BATCHES * BATCH_SIZE == N_TOTAL
BATCH_SEEDS = [20260729, 20260730, 20260731, 20260732]
assert len(BATCH_SEEDS) == N_BATCHES

CONTINUUM_LEVEL = 6.0  # 1e-17 erg/s/cm2/A, matches run_mock_and_compare.py / compare_p1d.py
DWAVE = 0.2             # matches quickquasars internal default (pre-camera-resample grid)
QSO_REDSHIFT = 3.0
BENCHMARK_N200_SECONDS = 48.0  # WP_P2t_DESISIM_TIMING_2026_07_28.md, full-pipeline GO number
STOP_RATIO = 10.0

OUT_JSON = os.path.join(REPO_ROOT, "data", "derived", "wp_e6_covariance_2026_07_29.json")


def flux_power_1d_delta(flux, dv_kms):
    """Per-spectrum P1D via the flux-CONTRAST field delta_F = flux/mean_spec - 1,
    NOT the mean-subtracted absolute flux compare_p1d.py uses (see module
    docstring). Returns (k [s/km], power [n_spec, n_k])."""
    nspec, npix = flux.shape
    mean_spec = flux.mean(axis=1, keepdims=True)
    delta = flux / mean_spec - 1.0
    fft = np.fft.rfft(delta, axis=1)
    power = (np.abs(fft) ** 2) * dv_kms / npix
    k = np.fft.rfftfreq(npix, d=dv_kms) * 2 * np.pi
    return k, power


def band_average(k_native, power_native, k_bins, half_dex=0.05):
    """Average native FFT modes into log-spaced bands centered on k_bins (each
    band = [center - half_dex, center + half_dex] dex). Returns (banded_power
    [n_spec, n_bins], mode_counts [n_bins], fully_resolved [n_bins] bool array --
    True only if the ENTIRE band (both edges) lies within the native k range
    (excluding the k=0 mode)."""
    n_spec = power_native.shape[0]
    n_bins = len(k_bins)
    banded = np.full((n_spec, n_bins), np.nan)
    counts = np.zeros(n_bins, dtype=int)
    fully_resolved = np.zeros(n_bins, dtype=bool)
    k_min_native = k_native[1]   # skip DC mode
    k_max_native = k_native[-1]
    log_k_native = np.log10(k_native[1:])  # exclude DC
    power_ac = power_native[:, 1:]
    for i, kc in enumerate(k_bins):
        lo = np.log10(kc) - half_dex
        hi = np.log10(kc) + half_dex
        edge_lo = 10 ** lo
        edge_hi = 10 ** hi
        fully_resolved[i] = (edge_lo >= k_min_native) and (edge_hi <= k_max_native)
        sel = (log_k_native >= lo) & (log_k_native < hi)
        counts[i] = int(sel.sum())
        if counts[i] > 0:
            banded[:, i] = power_ac[:, sel].mean(axis=1)
    return banded, counts, fully_resolved


def run_batch(batch_seed, batch_size, tmpdir):
    """Runs the FULL pipeline (MockMaker -> resample -> sim_spectra) for one
    batch, returns (wave_native, k_native, power_native[batch_size, nk],
    timing_dict)."""
    from desisim.lya_mock_p1d import MockMaker
    from desisim.scripts.quickspectra import sim_spectra
    from desispec.interpolation import resample_flux
    import astropy.io.fits as pyfits

    t_batch_start = time.time()

    mm = MockMaker(N2=12, dv_kms=20.0, seed=batch_seed, white_noise=False)
    t0 = time.time()
    wave_native, trans_native = mm.get_lya_skewers(Ns=batch_size)
    t_mockmaker = time.time() - t0

    wave = np.arange(wave_native.min(), wave_native.max(), DWAVE)
    t0 = time.time()
    trans = np.array([resample_flux(wave, wave_native, trans_native[i]) for i in range(batch_size)])
    t_resample = time.time() - t0

    continuum = CONTINUUM_LEVEL * (wave / wave.mean()) ** (-0.5)
    clean_flux = continuum[None, :] * trans

    sourcetype = np.array(["qso"] * batch_size)
    redshift = np.full(batch_size, QSO_REDSHIFT)
    out_file = os.path.join(tmpdir, f"spectra-batch-{batch_seed}.fits")
    t0 = time.time()
    sim_spectra(
        wave, clean_flux, program="DARK",
        spectra_filename=out_file,
        sourcetype=sourcetype, redshift=redshift, seed=batch_seed,
        use_poisson=True, save_resolution=False,
    )
    t_sim_spectra = time.time() - t0

    hdus = pyfits.open(out_file)
    b_wave = hdus["B_WAVELENGTH"].data
    b_flux = hdus["B_FLUX"].data
    hdus.close()

    sel = (b_wave >= wave_native.min() + 5) & (b_wave <= wave_native.max() - 5)
    b_wave_f = b_wave[sel]
    b_flux_f = b_flux[:, sel]

    c_kms = 299792.458
    dv_kms = c_kms * np.diff(b_wave_f).mean() / b_wave_f.mean()

    k_native, power_native = flux_power_1d_delta(b_flux_f, dv_kms)

    t_batch_total = time.time() - t_batch_start
    timing = {
        "mockmaker_seconds": t_mockmaker,
        "resample_seconds": t_resample,
        "sim_spectra_seconds": t_sim_spectra,
        "batch_total_seconds": t_batch_total,
        "dv_kms": float(dv_kms),
        "n_forest_pixels": int(sel.sum()),
    }
    return wave_native, k_native, power_native, timing


def main():
    if os.environ.get("DESIMODEL") != DESIMODEL_PATH:
        os.environ["DESIMODEL"] = DESIMODEL_PATH
    print(f"DESIMODEL = {os.environ['DESIMODEL']}")
    if not os.path.isdir(os.path.join(DESIMODEL_PATH, "data", "focalplane")):
        print("BLOCKER: expected desimodel focalplane data not found at "
              f"{DESIMODEL_PATH}/data/focalplane -- STOPPING per task instructions "
              "(do not attempt to download / work around).", file=sys.stderr)
        sys.exit(2)

    try:
        import desisim  # noqa: F401
        import desispec  # noqa: F401
        import desimodel.io as dio
        dio.load_focalplane()
    except Exception as e:
        print(f"BLOCKER: desisim/desispec/desimodel import or focalplane load failed: {e}",
              file=sys.stderr)
        sys.exit(2)

    from emu_predict import K_BINS  # noqa: E402  (16 target bins, s/km)
    k_bins = np.asarray(K_BINS)
    assert k_bins.size == 16, f"expected 16 K_BINS, got {k_bins.size}"

    tmpdir = tempfile.mkdtemp(prefix="wp_e6_cov_", dir="/tmp")
    t_start = time.time()

    all_power_native = []  # list of [batch_size, nk] arrays
    wave_native_ref = None
    per_batch_timing = []
    seed_records = []

    try:
        for b_idx, seed in enumerate(BATCH_SEEDS):
            print(f"\n=== Batch {b_idx+1}/{N_BATCHES}, seed={seed}, Ns={BATCH_SIZE} ===")
            wave_native, k_native, power_native, timing = run_batch(seed, BATCH_SIZE, tmpdir)
            print(f"  mockmaker={timing['mockmaker_seconds']:.3f}s "
                  f"resample={timing['resample_seconds']:.3f}s "
                  f"sim_spectra={timing['sim_spectra_seconds']:.3f}s "
                  f"batch_total={timing['batch_total_seconds']:.3f}s "
                  f"dv_kms={timing['dv_kms']:.3f}")
            if wave_native_ref is None:
                wave_native_ref = wave_native
                k_native_ref = k_native
            else:
                assert np.array_equal(wave_native, wave_native_ref), (
                    "native wave grid differs across batches -- cannot pool "
                    "(dv_kms / k-grid would differ per batch)"
                )
                assert np.array_equal(k_native, k_native_ref), (
                    "native k grid differs across batches"
                )
            all_power_native.append(power_native)
            per_batch_timing.append(timing)
            for row in range(BATCH_SIZE):
                seed_records.append({
                    "realization_id": b_idx * BATCH_SIZE + row,
                    "batch_seed": seed,
                    "row_in_batch": row,
                })
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    wall_clock_total = time.time() - t_start
    print(f"\nTotal wall-clock for N={N_TOTAL} full pipeline: {wall_clock_total:.3f} s")
    ratio = wall_clock_total / BENCHMARK_N200_SECONDS
    print(f"Ratio vs {BENCHMARK_N200_SECONDS}s benchmark (WP_P2t_DESISIM_TIMING_2026_07_28.md): "
          f"{ratio:.3f}x")
    if ratio > STOP_RATIO:
        print(f"BLOCKER: wall-clock {ratio:.1f}x over the {BENCHMARK_N200_SECONDS}s benchmark "
              f"(>{STOP_RATIO}x STOP trigger). Halting before further analysis, per task "
              "instructions (do not silently work around a performance problem).",
              file=sys.stderr)
        sys.exit(3)

    power_native_all = np.concatenate(all_power_native, axis=0)  # [200, nk]
    assert power_native_all.shape[0] == N_TOTAL

    # --- band-average onto the 16 K_BINS targets, flag which are fully resolved ---
    banded_all, mode_counts, fully_resolved = band_average(k_native_ref, power_native_all, k_bins)
    measurable_idx = np.where(fully_resolved)[0]
    unmeasurable_idx = np.where(~fully_resolved)[0]
    p_delivered = len(measurable_idx)
    print(f"\nk-bin resolution check: {p_delivered}/16 K_BINS fully within native FFT "
          f"resolution (Nyquist k={k_native_ref[-1]:.5f} s/km).")
    print(f"  Measurable target indices (0-based): {measurable_idx.tolist()}")
    print(f"  Unmeasurable (beyond Nyquist / partial band) target indices: {unmeasurable_idx.tolist()}")

    P = banded_all[:, measurable_idx]  # [200, p_delivered]  -- the delivered sub-block
    p_bar = P.mean(axis=0)

    # --- full N=200 sample covariance (p_delivered x p_delivered) ---
    C_full = np.cov(P, rowvar=False, ddof=1)
    if p_delivered == 1:
        C_full = np.array([[C_full]])

    # --- validation 1: exact symmetry check ---
    symmetric_exact = bool(np.array_equal(C_full, C_full.T))

    # --- validation 2: positive-definiteness, min eigenvalue ---
    eigvals = np.linalg.eigvalsh(C_full)
    min_eigenvalue = float(eigvals.min())
    positive_definite = bool(min_eigenvalue > 0)

    # --- Hartlap factors ---
    N = N_TOTAL
    p_task = 16
    hartlap_p16_task_specified = (N - p_task - 2) / (N - 1)  # 182/199, printed per task instruction
    p_applied = p_delivered
    hartlap_p_applied = (N - p_applied - 2) / (N - 1)

    print(f"\nHartlap factor, TASK-SPECIFIED formula (N-p-2)/(N-1), N={N}, p={p_task}: "
          f"{hartlap_p16_task_specified:.6f}  (= 182/199 = {182/199:.6f}) "
          f"-- NOT applied to the stored inverse (dimension mismatch, see header).")
    print(f"Hartlap factor ACTUALLY APPLIED, N={N}, p={p_applied} (delivered sub-block dim): "
          f"{hartlap_p_applied:.6f}  (= {N-p_applied-2}/{N-1})")

    C_inv_naive = np.linalg.inv(C_full)
    C_inv_hartlap = hartlap_p_applied * C_inv_naive

    # --- validation 3: stability check, random N=100 subsample vs full N=200 ---
    rng = np.random.RandomState(2026_07_29)
    sub_idx = rng.choice(N_TOTAL, size=100, replace=False)
    P_sub = P[sub_idx]
    C_sub = np.cov(P_sub, rowvar=False, ddof=1)
    if p_delivered == 1:
        C_sub = np.array([[C_sub]])
    diag_full = np.diag(C_full)
    diag_sub = np.diag(C_sub)
    rel_drift = np.abs(diag_sub - diag_full) / np.abs(diag_full)
    max_rel_drift = float(rel_drift.max())
    max_rel_drift_idx = int(rel_drift.argmax())
    stability_flag = max_rel_drift > 0.20
    print(f"\nStability check (N=100 random subsample vs full N=200), max relative diagonal "
          f"drift: {100*max_rel_drift:.2f}% at delivered-bin index {max_rel_drift_idx} "
          f"(target K_BINS index {int(measurable_idx[max_rel_drift_idx])})."
          f"{'  FLAG: exceeds 20%!' if stability_flag else ''}")

    print(f"\nMatrix symmetry (exact): {symmetric_exact}")
    print(f"Min eigenvalue: {min_eigenvalue:.6e}  positive_definite={positive_definite}")

    # --- assemble output ---
    result = {
        "provenance": {
            "generated_by": "pipeline/wp_e6_covariance.py (T1 agent, WP-E6-P2A)",
            "verified_by": "pending (producer != verifier, not yet re-run by coordinator)",
            "reviewed_by_t0": "pending",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "status": "DRAFT -- not promoted to LIVE, producer != verifier",
            "wp": "WP-E6-P2A",
            "execution_plan": "briefs/EXECUTION_PLAN_2026_07_29_TWISTED_AND_WPE6.md",
            "analysis_protocol": "briefs/ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md Part A",
            "timing_reference": "briefs/WP_P2t_DESISIM_TIMING_2026_07_28.md (48s benchmark, N=200)",
            "desimodel_path": os.environ["DESIMODEL"],
        },
        "headline_finding": (
            "Dimension conflict: only 9 of 16 K_BINS targets (log10 k = -2.2..-1.4) are "
            "fully within this pipeline's native FFT resolution (Nyquist k=%.5f s/km, "
            "set by the DESI B-camera's ~1.0 Angstrom native pixel scale). The other 7 "
            "(log10 k = -1.3..-0.7) were NOT computed -- no extrapolation was performed "
            "(EXECUTION_PLAN Sec.0 rule 7, never fabricate a fallback result). This "
            "blocks a literal 16x16 covariance and needs T0/coordinator disposition "
            "before WP-E6-P2B / WP-E6-SWEEP proceed." % k_native_ref[-1]
        ),
        "k_bins_target_s_per_km_16": k_bins.tolist(),
        "measurable_target_indices_0based": measurable_idx.tolist(),
        "unmeasurable_target_indices_0based": unmeasurable_idx.tolist(),
        "k_bins_delivered_s_per_km": k_bins[measurable_idx].tolist(),
        "native_fft_nyquist_s_per_km": float(k_native_ref[-1]),
        "band_mode_counts_16": mode_counts.tolist(),
        "n_realizations": N_TOTAL,
        "n_batches": N_BATCHES,
        "batch_size": BATCH_SIZE,
        "batch_seeds": BATCH_SEEDS,
        "seed_records_per_realization": seed_records,
        "p_bar_delivered": p_bar.tolist(),
        "covariance_delivered": C_full.tolist(),
        "hartlap_factor_p16_task_specified": hartlap_p16_task_specified,
        "hartlap_factor_p16_formula": "(N-p-2)/(N-1), N=200, p=16 -> 182/199",
        "hartlap_factor_p16_applied_to_stored_inverse": False,
        "hartlap_factor_p_delivered_applied": hartlap_p_applied,
        "p_delivered": p_applied,
        "hartlap_formula_applied": f"(N-p-2)/(N-1), N={N}, p={p_applied} -> "
                                    f"{N-p_applied-2}/{N-1}",
        "covariance_inverse_naive_delivered": C_inv_naive.tolist(),
        "covariance_inverse_hartlap_corrected_delivered": C_inv_hartlap.tolist(),
        "validation": {
            "symmetry_exact": symmetric_exact,
            "min_eigenvalue": min_eigenvalue,
            "positive_definite": positive_definite,
            "stability_check_n100_subsample": {
                "subsample_size": 100,
                "subsample_rng_seed": 2026_07_29,
                "max_relative_diagonal_drift": max_rel_drift,
                "max_relative_diagonal_drift_percent": 100 * max_rel_drift,
                "max_drift_at_delivered_bin_index": max_rel_drift_idx,
                "max_drift_at_target_k_bin_index": int(measurable_idx[max_rel_drift_idx]),
                "exceeds_20_percent_flag": stability_flag,
            },
            "wall_clock_seconds": wall_clock_total,
            "benchmark_seconds": BENCHMARK_N200_SECONDS,
            "wall_clock_ratio_vs_benchmark": ratio,
        },
        "per_batch_timing": per_batch_timing,
        "estimator_notes": {
            "flux_power_1d_delta": (
                "Uses flux-contrast delta_F = flux/mean_spec - 1 (units s/km, matches "
                "the emulator's P1D quantity), NOT compare_p1d.py's mean-subtracted "
                "absolute flux (units flux^2*km/s). Intentional deviation, documented "
                "in module docstring."
            ),
            "masking": (
                "No MASK_FRAC pixel masking applied. ANALYSIS_PROTOCOL Sec 1.3 notes "
                "Part A should consume Part C's (WP-E6-P2C) corrected masking estimator "
                "once it lands; P2C has not landed as of this run, so this covariance is "
                "built on unmasked sim_spectra output and may need regeneration."
            ),
            "band_averaging": (
                "Native FFT modes are averaged into 0.05-dex-half-width log bands "
                "centered on each K_BINS value (uniform 0.1 dex spacing), not point "
                "interpolation -- point interpolation would give single-mode "
                "chi^2(2 dof)-level scatter per bin instead of a band-averaged estimate."
            ),
        },
    }

    with open(OUT_JSON, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nWrote {OUT_JSON}")


if __name__ == "__main__":
    main()
