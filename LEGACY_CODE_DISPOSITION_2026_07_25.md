# LEGACY_CODE_DISPOSITION_2026_07_25.md — Deprecation Status and Leverage Assessment

**Date:** 2026-07-25
**Author:** Fable 5 (T0-delegated)
**Purpose:** Formal disposition of pre-epistemic-guardrails Stream 3 scripts — what is
deprecated and why, and what is genuinely leverageable given what Stream 1 and Stream 2
have actually certified. Companion to `DUAL_SCALE_EXPERIMENTATION_BRIEF_2026_07_25.md`
(which found three of these live in an earlier pass) and
`scripts/fetch_survey_astroquery.py` (the real replacement fetcher, this session).

---

## 1. Deprecated — do not run, do not cite output

All six files below now carry an in-file `DEPRECATED / EXPERIMENTAL` banner. **None are
deleted** — they stay as historical record of the pre-guardrails era and as negative
examples for the pattern each one demonstrates. None may be imported by new pipeline code.

| File | Defect | Pattern (LESSONS_LEARNED.md) |
|---|---|---|
| `real_euclid_worker.py` | Fallback path injects a fabricated cluster into `discoveries.json` under a `ra_min/dec_min` modulo-20 condition, indistinguishable from a real detection | L5 (synthetic-seeded discoveries) |
| `ned_cross_validator.py` | Defines `NED_API_BASE`, never calls it; hardcodes "VALIDATED AND CONFIRMED" regardless of input | Not on file before this pass — new instance of the L5 family |
| `process_nanograv.py` | Silently substitutes `np.random` for RNAMP/RNIDX when a `.par` field is absent, no output flag | Partial-fabrication variant of L5 — more dangerous than a pure stub because the real parts make it easy to trust |
| `euclid_validation_run.py` | Pure `np.random` mock catalog + a load-test polynomial mislabeled a cosmological "validation" | Adjacent to F9 (`V5_SCIENTIFIC_REVIEW.md`, premature "complete/tested" framing) |
| `weak_lensing_overlay.py` | `delta_spikes = kappa_peaks * 22.0 + noise` — correlation > 0.8 guaranteed by construction on every call | F4 (circular test, `V5_SCIENTIFIC_REVIEW.md`) |
| `NANOGrav_prediction.py` | Hardcoded, uncited `base_strain`/`pta_limit`; inputs are the **fabricated** cooper_s7/s10 μ constants from the 2026-07-14 review (L1) | L1 directly — reuses the exact debunked numbers |

## 2. What Stream 1 and Stream 2 have actually certified (as of 2026-07-25)

This is the leverage question: given real certified content exists elsewhere in the
project, what should any *future* real implementation build on, instead of starting from
these six files' internals?

- **Stream 2 (K3-DarkMatter):** ρ=4, T=18 (Shioda–Tate, exact), 2× Type II Kodaira
  classification, L₃ = Sym²(L₂) operator identity (Lean 4, kernel-verified,
  `C3b_symsqrt_cooper_s7.json`). This is the one piece of genuinely machine-certified
  geometry in the whole project. Any future observable code should read these
  certificates directly (as `pipeline/observables_real.py` and the checker suite already
  do) — never re-derive or re-type the lattice numbers.
- **Stream 1 (Dual-Scale/LeanProposal, see the companion brief):** the same s7/s10
  operator pair, reframed via F-theory + chameleon mediator. `Agora/Axioms/
  PipelineBound.lean` demonstrates the correct pattern for handling an unfilled empirical
  input (disclosed-vacuous quarantine, not silent fabrication) — worth following as a
  template if any future script needs to represent "value not yet measured" honestly,
  which is exactly where `process_nanograv.py` and `ned_cross_validator.py` failed.
  `Agora/Phenomenology/ChameleonRescue.lean`'s `alpha_effective` density-boost mechanism
  is real, checked arithmetic on assumed inputs — reusable as a *formula*, not as a
  physical claim, until the assumed inputs are derived (open question in the brief).
- **This repo's own certified machinery:** `pipeline/gate.py` (G1/G1-L), the closure/null
  harness, `scripts/pin_prediction.py`, `pipeline/observables_real.py` (exact κ-peak/Betti,
  golden-tested). None of the six deprecated files did anything these don't already do
  correctly.

**Conclusion: nothing in the six deprecated files' internals is worth porting forward.**
Their only reusable part was the *idea* of "query real SDSS/Euclid data via astroquery"
(`real_euclid_worker.py`'s attempted `astroquery.sdss.SDSS.query_sql` call was the right
library, wrong execution) — which this session's `scripts/fetch_survey_astroquery.py`
implements for real, gated, checksummed, and without any fallback fabrication path.

## 3. What replaces them

`scripts/fetch_survey_astroquery.py` (this session) — real `astroquery.sdss.SDSS` and
`astroquery.esa.euclid.Euclid` queries, gate-checked (`pipeline.gate
.require_pinned_for_real_data`), no synthetic fallback of any kind: a query either
returns real rows or the fetch records an error, full stop. See
`DUAL_SCALE_EXPERIMENTATION_BRIEF_2026_07_25.md` §5 for the quarantine rationale and
this document for the full six-file list.

---

`Generated-by: Fable 5 (T0-delegated) | Verified-by: direct read of all six flagged files (line-level, not summarized from memory) | Reviewed-by: T0 Y (delegated); Xavier countermand window open`
