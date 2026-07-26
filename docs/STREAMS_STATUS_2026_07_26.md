# Three-Stream Status (2026-07-26) — Stream 3 addendum

**Scope of this doc:** Stream 3 only. Streams 1/2 status unchanged since
`docs/STREAMS_STATUS_2026_07_25.md` — see that document for their sections and for the
full Off-Ramp 3 terminus narrative this addendum builds on. Nothing below reopens G1,
touches real data, or revisits the terminus; it is entirely the "remaining lawful work"
scoped in `docs/STREAMS_STATUS_2026_07_25.md` §"What is currently live in Stream 3".

## Stream 3: synthetic-only pipeline infrastructure (WP-T series)

Following the Off-Ramp 3 terminus (2026-07-25), a work-package plan
(`briefs/STREAM3_SYNTHETIC_RERUN_FRAMEWORK_2026_07_26.md`) applied Stream 2's process
rigor (`STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md`, `STREAM2_WP_H_EXPERIENCE_BRIEF_2026_07_25.md`)
to prevent recurrence of the D-3/WP-H fabrication pattern in future external-brief handling,
and to close two structural gaps left dormant by the terminus. Executed 2026-07-26.

| WP | Deliverable | Status |
|---|---|---|
| T1 | `pipeline/triage.py` — mechanical brief-verification protocol (git/file/grep checks, SHA256 vendoring) | ✅ Complete, 28 tests |
| T2 | `density_shuffle_realization()` in `pipeline/realfield3d.py` — third null scheme, alongside existing CSR/z-shuffle | ✅ Complete, 6 tests |
| T3 | Replaced `np.random` placeholders in `D3_batch_runner_phase2._evaluate_sector` with real per-sector C1-certificate lookups | ✅ Complete, 8 tests (incl. 2 regression guards, see below) |
| T4 | `PREDICTION_v2_DRAFT.md` — structural schema stub for a future v2.0 pin, no real values | ✅ Complete, 6 tests |
| T5 | `NO_PREDICTION_BRANCH.md` §9 + `pipeline.gate.check_flab_trigger()` — F-LAB monitoring trigger doc + advisory pre-check | ✅ Complete, 9 tests |
| T6 | Synthetic mock-catalog generator (`pipeline/synthetic_catalog.py`) + integrated 3-scheme null-percentile report (`pipeline/synthetic_null_report.py`), mirroring `docs/WP_R7_BETA_VARIANCE_SCAN.md`'s methodology entirely on synthetic data | ✅ Complete, 10 tests |

Committed: `b8e2597` (T1–T5). G1/G1-L gates untouched throughout — verified by grep on every
WP touching `pipeline/gate.py` or `pipeline/D3_batch_runner_phase2.py`.

### T6 detail

`generate_mock_catalog()` produces a synthetic (RA, Dec, z) point cloud (two-population
model: ~70% clustered around random centers with Gaussian scatter, ~30% uniform
background) — deterministic per seed, no bare `np.random`. `run_synthetic_null_scan()`
bins it at nbins=[4,8,16], computes observed β₀/β₁/β₂, and runs all three null schemes
(CSR, z-shuffle, density-shuffle) against it, reporting null mean/std/percentile per
(seed, nbins, statistic, scheme) — with `percentile=None` (never coerced to 0/100) when a
null bank has zero variance. Output: `docs/SYNTHETIC_NULL_SCAN_REPORT.md`, labeled
**SYNTHETIC** throughout, never TEST/FIT.

Reviewed directly (not just via the agent's self-report, given the T2/T3 defects found
in prior packages): the observed field and null-rebinning both reuse the same bounding
box, computed once per (seed, nbins) from the real catalog and passed to every null
realization — the correct control for a fair comparison. The None-percentile test uses
`pytest.skip()` rather than a silent pass if no degenerate case arises in a given run,
and in the run reviewed it genuinely hit and correctly handled a zero-variance case
(confirmed PASSED, not skipped). No defects found in this package.

### Defects caught in review (both fixed before commit)

1. **False provenance footer (T2).** The initial footer on `pipeline/realfield3d.py`
   claimed `Reviewed-by: T0 Y` for the new `density_shuffle_realization()` by citing a
   sign-off (`docs/T0_SIGNOFF_WP_R5_R6_R7_2026_07_25.md`) that only reviewed the
   pre-existing z-shuffle/CSR code it sits beside. Corrected to distinguish reviewed vs.
   unreviewed portions of the same file.

2. **Tautological-pass bug (T3).** The first pass at replacing `np.random` placeholders
   for `operator_error`/`mirror_order` substituted **hardcoded constants** (`0.0` / `40`)
   applied to every sector regardless of `config.operator`, rather than a genuine
   per-sector certificate lookup. Since `0.0 < 1e-14` and `40 ≥ 32` unconditionally, this
   made 2 of the 3 `pass_verdict` conditions vacuously true for *any* candidate —
   including one with no certificate or a failing one. Same failure class as the retracted
   WP-R3 null bank (`docs/FINDING_R_NULLDEGENERATE_2026_07_25.md`) and WP-H's self-caught
   Δ bug (`docs/WP_H_AUTO_RESEARCH_TRIAGE.md`). Fixed via `_load_c1_certificate()` /
   `_candidate_from_operator()` — genuine per-sector lookup with an honest NaN gap when no
   certificate exists or `status != PASS` / `margin_max_denominator != 1`. Two regression
   tests guard both the gap path and the certified path
   (`pipeline/tests/test_D3_batch_runner_phase2.py`). Currently dormant in practice
   (`require_derived_for_labels()` still blocks `run_batch()` entirely — G1-L is closed)
   but would have been a live defect the moment that gate opens.

**Lesson for future placeholder-replacement work:** verify a replacement is a genuine
per-input computation, not a different flavor of constant. A hardcoded "real-looking"
number is harder to notice than the random placeholder it replaces, because it doesn't
look suspicious on a single read.

### Full suite

300/300 tests passing after T1–T5 (up from 243 baseline pre-2026-07-26).

---

`Generated-by: Claude Sonnet 5, orchestrating 5 Haiku 4.5 agents (T1/T2/T4/T5) + direct
fix (T3 correction) | Verified-by: full pytest suite (300/300), git grep on gate-call
sites | Reviewed-by: pending T0`
