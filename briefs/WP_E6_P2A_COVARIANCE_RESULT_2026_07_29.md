# WP-E6-P2A — Hartlap Covariance Build: Result (DRAFT)

**Status: DRAFT. Producer != verifier** (EXECUTION_PLAN_2026_07_29 Sec.0 rule 1) — not
promoted to LIVE. Coordinator/T0 verification pass required before WP-E6-P2B or
WP-E6-SWEEP may consume this.

**Date:** 2026-07-29.
**Script:** `pipeline/wp_e6_covariance.py`.
**Output:** `data/derived/wp_e6_covariance_2026_07_29.json`.
**Label: ENGINEERING / DESIGN** (CLAUDE.md rule 3 — not TEST, not FIT). Entirely
`desisim`-synthetic infrastructure; no real DESI data touched (CLAUDE.md rule 1).

---

## Headline finding — dimension conflict, blocks P2B/SWEEP as currently scoped

`emu_predict.py`'s `K_BINS` grid has 16 entries (log₁₀k = −2.2 … −0.7, s/km — confirmed
directly from the code, not from any brief). This pipeline's actual measurable range is
narrower than that: the DESI B-camera output grid `sim_spectra()` resamples onto has a
native pixel scale of ≈1.0 Å (measured, not assumed — `np.diff(b_wave_f).mean()` on the
FITS output), giving a velocity pixel width `dv_kms ≈ 60.8 km/s` and an FFT Nyquist
frequency `k_Nyquist = π/dv_kms ≈ 0.0516 s/km`.

Using 0.05-dex-half-width bands centered on each `K_BINS` value (the natural band width
given the grid's uniform 0.1 dex spacing), **only 9 of 16 target bins (log₁₀k = −2.2 …
−1.4) lie fully within the resolved native range.** The remaining 7 (log₁₀k = −1.3 …
−0.7) are partially or fully beyond Nyquist. Per EXECUTION_PLAN_2026_07_29.md §0 rule 7
("never fabricate a fallback result"), **no extrapolation was performed** for those 7
bins — they are not computed, not estimated, not filled with a placeholder.

This is a property of the synthetic pipeline's instrumental resolution, not of `N`, seed
choice, or windowing: running more realizations does not change it. It was not
anticipated by the task brief or by `ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md` (which
assumed a literal 16×16 build). **This blocks a literal 16×16 covariance and, downstream,
WP-E6-P2B's 12-dof chi² design and WP-E6-SWEEP as currently scoped — needs T0/coordinator
disposition** (e.g., re-derive `K_BINS` bounds against this pipeline's actual resolution,
or find a finer-sampled camera output path, or restrict the sweep to the 9 measurable
bins with a documented dof change).

Delivered instead: a **9×9 measurable sub-block**, all 4 required validation checks run
on that matrix, plus the full index map (`measurable_target_indices_0based` /
`unmeasurable_target_indices_0based` in the JSON) so a consumer can see exactly what is
and is not covered.

---

## Two other documented, intentional deviations (not silent)

1. **Estimator normalization.** `compare_p1d.py::flux_power_1d()` FFTs the
   mean-*subtracted* absolute flux (units flux²·km/s), not the standard flux-contrast
   field. This script instead uses `δ_F = flux/mean_spec − 1` (units s/km, dimensionally
   matching the emulator's own P1D quantity) — see `flux_power_1d_delta()` in the script.
2. **No masking applied.** ANALYSIS_PROTOCOL §1.3 states Part A should consume Part C's
   (WP-E6-P2C) corrected masking estimator. P2C has not landed as of this run. Baking in
   the *current*, known-buggy zero-fill estimator (Bug 1: edge discontinuity; Bug 2:
   biased mean-over-zero-filled-pixels) would permanently encode a known defect into a
   covariance artifact, so this build uses the **unmasked** `sim_spectra` output. This
   covariance will likely need regeneration once P2C's fix lands.
3. **Band-averaging, not point interpolation.** Native FFT `Δk` (≈7.76×10⁻⁵ s/km) is far
   finer than the target grid spacing — a k-bin near 0.05 s/km spans ~150 native modes.
   Point-interpolating onto `K_BINS` would give single-mode χ²(2 dof)-level scatter per
   bin instead of a proper band-averaged estimate, badly inflating the diagonal. This
   script averages all native modes within each 0.05-dex band (mode counts per bin
   recorded in `band_mode_counts_16`).

---

## Generation

- N = 200 realizations, full pipeline (`MockMaker.get_lya_skewers` → `resample_flux` →
  `desisim.scripts.quickspectra.sim_spectra`) for every one — **not** the
  `MockMaker`-only shortcut that was previously caught missing 99% of the wall-clock.
- Batched as 4 × 50 (not 200 individual calls). Two timing points measured in-session
  (Ns=4 → 10.54 s; Ns=50 → 11.91 s for the `sim_spectra` step alone) imply ≈10.4 s fixed
  overhead per `sim_spectra()` call plus ≈0.03 s/skewer marginal — 200 single-realization
  calls would have cost ≈35 min (≈43× the benchmark), tripping the >10× STOP trigger.
  4×50 matches the exact configuration the 48 s benchmark measured.
- **Seeds:** 4 distinct batch seeds (20260729, 20260730, 20260731, 20260732), one per
  batch of 50. Every one of the 200 realizations has a recorded, distinct
  `{realization_id, batch_seed, row_in_batch}` entry (`seed_records_per_realization` in
  the JSON) — verified: 200/200 entries are pairwise distinct. The native wave grid was
  asserted byte-identical across all 4 batches before pooling (assertion passed; MockMaker's
  grid depends on `N2`/`dv_kms`, not on the seed).
- `DESIMODEL` = `<repo>/phase1_work/agent3_synthetic/desimodel_data_test` — resolved
  correctly, no download attempted (data was already on disk, per task brief).

---

## Required validation checks

1. **Symmetry (exact):** `True` (`np.array_equal(C, C.T)`).
2. **Positive-definiteness:** minimum eigenvalue of the stored 9×9 covariance =
   **1.689080×10⁻²** (positive → PD confirmed).
3. **Stability (N=100 random subsample vs full N=200):** maximum relative diagonal drift
   across the 9 delivered bins = **18.41%**, at delivered-bin index 3 (target `K_BINS`
   index 3, log₁₀k = −1.9). **Below the 20% flag threshold, but only by 1.6 points** —
   close enough to flag as marginal, not comfortably stable. Given N=200 is itself an
   engineering choice (ANALYSIS_PROTOCOL §1.5), this is worth a second look before
   treating the covariance as final.
4. **Wall-clock:** 29.67 s total for N=200 full pipeline, vs the 48 s benchmark
   (`WP_P2t_DESISIM_TIMING_2026_07_28.md`) → **ratio 0.62×** (faster than benchmark, well
   under the 10× STOP trigger). No performance blocker encountered.

---

## Hartlap factor

- **Task-specified** (printed verbatim per task instruction): `(N−p−2)/(N−1)`, N=200,
  p=16 → **182/199 = 0.914573**. **NOT applied to the stored inverse** — the delivered
  matrix is 9×9, not 16×16 (see headline finding).
- **Actually applied** to the stored inverse: `(N−p−2)/(N−1)`, N=200, p=9 (true delivered
  dimension) → **189/199 = 0.949749**.
- Both factors and both formulas are recorded explicitly in the output JSON
  (`hartlap_factor_p16_task_specified`, `hartlap_factor_p_delivered_applied`), along with
  which one is actually baked into `covariance_inverse_hartlap_corrected_delivered`.

---

## Deliverables

- `pipeline/wp_e6_covariance.py` — generation + covariance script.
- `data/derived/wp_e6_covariance_2026_07_29.json` — 9×9 covariance, naive and
  Hartlap-corrected inverse, mean vector `p̄`, full 16-bin index map, all 200 seed
  records, per-batch timing, validation results.
- This brief.

## Escalation for T0 / coordinator

1. **Dimension conflict (headline finding above)** — the 16-bin design in
   ANALYSIS_PROTOCOL / EXECUTION_PLAN cannot be built from this pipeline as specified;
   needs a ruling before P2B/SWEEP proceed.
2. **Stability check at 18.4%**, close to the 20% flag — recommend a second opinion on
   whether N=200 is adequate for the 9 delivered bins, or whether a larger N should be
   considered once the dimension question is resolved (cost is cheap: 30s per 200 at
   this batching, so N=400 would be ~60s, comfortably inside budget).
3. **Masking dependency on WP-E6-P2C** (noted in ANALYSIS_PROTOCOL §1.3) — this
   covariance does not yet incorporate the masking fix; flagged for regeneration once
   P2C lands, not resolved here.

---
Generated-by: T1 agent (WP-E6-P2A) | Verified-by: pending (producer != verifier, not yet re-run by coordinator) | Reviewed-by: pending T0.
