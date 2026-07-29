# WP-E6-P2C — Masking Fix: Result (DRAFT)

**Status: DRAFT. Producer != verifier** (EXECUTION_PLAN_2026_07_29 Sec.0 rule 1) — not
promoted to LIVE. Coordinator/T0 verification pass required before WP-E6-SWEEP consumes
this (P2A's covariance was itself built *unmasked*, pending this fix — see
`WP_E6_P2A_COVARIANCE_RESULT_2026_07_29.md` deviation 2 — and will likely need
regeneration once this lands).

**Date:** 2026-07-29.
**Module:** `pipeline/compare_p1d.py`. **Tests:** `pipeline/tests/test_compare_p1d.py`
(8/8 pass). **Label: ENGINEERING / CONTROL** (CLAUDE.md rule 3 — not TEST, not FIT).
Entirely synthetic; touches no pinned prediction, no real DESI data (CLAUDE.md rule 1).

---

## Mandatory first step: paper verification (done)

`ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md` Sec 3.2 flags its masking-bias recipe as
reconstructed from a WebSearch summary, not a verbatim paper read. Fetched and read the
actual PDF (arXiv:2306.06311 / MNRAS 526, 5118 — Ravoux et al. 2023; WebFetch on the
arXiv abstract page alone returns only metadata, so the PDF had to be downloaded
directly). Citations used, verbatim section/equation numbers:

- Sec 3.1 eq. (1): flux-contrast definition δ_F(λ) = F(λ)/F̄(λ) − 1.
- Sec 5.3 "Spectrum pixel masking" (p.14): the paper's own pipeline sets δ_F = 0 at
  masked pixels (the zero-fill-in-contrast convention) and corrects the resulting
  k-dependent bias empirically, rather than avoiding the convention.
- Sec 5.3, eq. (22)/(23): correction coefficients defined as **A(k,z) = P_1D,CONT /
  P_1D,MASKEDm** — i.e. unmasked over masked.
- Sec 5.3.1: atmospheric-line correction A_line(k,z) modeled by a 2nd-order polynomial
  in k. Sec 5.3.2: DLA correction is instead k-independent (single scalar, ~0.5%
  amplitude).

This pipeline's `MASK_FRAC` random masking is broadband, not concentrated in
narrow-line- or DLA-like regions — closer to the atmospheric-line case per
ANALYSIS_PROTOCOL Sec 3.3's own reasoning — so `calibrate_window_correction` defaults to
the Sec 5.3.1 polynomial recipe, not the Sec 5.3.2 constant.

## ⚠️ Delta from the live ANALYSIS_PROTOCOL_DRAFT — flagged for T0, not silently resolved

`ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md` L290 states "the ratio p_masked / p_clean IS the
correction function". The paper-verified recipe (eq. 22/23 above) is the **opposite**
ratio: A = P_unmasked / P_masked, applied by **multiplying** the masked (measured) power
by A(k) to recover the unmasked estimate. Using the DRAFT's stated ratio directly would
apply the correction backwards (squaring the bias instead of removing it).

This module implements the paper-verified direction. `test_calibrate_window_correction_
recovers_known_bias` pins the direction with an injected, known bias function and
explicitly asserts the inverted ratio does *not* recover it (so a future regression to
the DRAFT's stated direction would fail loudly, not silently). **The DRAFT document
itself still has the wrong direction written down and needs a correction note or T0
ruling — this brief does not edit ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md.**

## Two bugs fixed

1. **Edge-discontinuity artifact**: masked pixels were zero-filled in the flux array
   before the FFT — a sharp jump from the true flux value to exactly 0 at every masked
   pixel leaks power across all k via the implicit rectangular window on each gap.
2. **Biased mean (previously unflagged)**: the per-spectrum mean subtracted before the
   FFT was computed over *all* pixels including the zero-filled ones, biasing the
   subtracted mean low and compounding bug 1. Fixed via `_masked_mean` (mean over
   unmasked pixels only), then `δ_F = 0` imposed exactly at masked pixels — matching the
   paper's own convention (Sec 5.3), not avoiding it.

## Before/after — measured on synthetic mock ensemble

`test_ensemble_before_after_reduces_bias` (N=500 synthetic colored-noise realizations,
seed=100, 3% random masking, 350/150 train/test split, aggregate power-weighted relative
bias on held-out test spectra vs the true unmasked P1D, restricted to k-bins where clean
power > 1% of peak):

| Estimator | Aggregate relative bias (held-out) |
|---|---|
| Legacy (zero-fill, biased mean) | **1.8021** (180%) |
| Fixed (bugs 1+2 corrected), uncorrected | **0.0535** (5.4%) |
| Fixed + mock-calibrated window correction | **0.0305** (3.1%) |

Numbers are from a live `pytest -s` run of the committed test, not hand-computed or
estimated. This is a synthetic-noise stand-in, not desisim mocks — WP-E6-P2A's real
desisim ensemble (`data/derived/wp_e6_covariance_2026_07_29.json`) had not landed when
this test was written; `calibrate_window_correction` is designed to consume that
ensemble directly once reused (same `return_per_spectrum=True` shape contract).

## Tests (8/8 pass, `pytest pipeline/tests/test_compare_p1d.py`)

Includes: isolated Bug-2 unit test; deterministic flat-spectrum exact-arithmetic proof
that both bugs are live in the legacy path and absent in the fix; no-mask
backward-compatibility check; zero-mask-frac negative control; `return_per_spectrum`
shape contract (needed by P2A); window-correction direction pin (above); shape-mismatch
rejection; full ensemble before/after (above).

## Deliverables

- `pipeline/compare_p1d.py` — `flux_power_1d()`, `_masked_mean()`,
  `calibrate_window_correction()`.
- `pipeline/tests/test_compare_p1d.py` — 8 regression tests.
- This brief.

## Escalation for T0 / coordinator

1. **Direction delta vs ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md L290** (above) — the DRAFT
   document itself needs a correction note; this module does not edit it.
2. **Reuse P2A's real desisim ensemble** for calibration once P2A's covariance is
   regenerated with masking applied (P2A explicitly built unmasked, pending this fix).
3. No gap interpolation was added (T0 ruling 2026-07-28, honored as instructed).

---
Generated-by: T1 agent (WP-E6-P2C) | Verified-by: pytest pipeline/tests/test_compare_p1d.py (8/8 pass, this session) | Reviewed-by: pending T0.
