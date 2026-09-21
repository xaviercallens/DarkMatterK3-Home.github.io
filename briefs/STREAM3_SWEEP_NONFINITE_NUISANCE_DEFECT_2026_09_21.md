# WP-E6-SWEEP — three layered defects found by trying to finish the synthetic validation

**Date:** 2026-09-21 · **Stream:** 3 (experimentation) · **Status:** defect report, diagnosis
complete. **Fix applied 2026-09-21, same day, under T0 ruling R2 — see §6.** Sections 1–5 are kept as filed.
**Label:** ENGINEERING / SYNTHETIC — no real data touched. `REAL_DATA_RULING_PIN` is still `None`.

## Summary

The synthetic validation of `pipeline/sweep.py` could not be completed, and the reason is a real
defect rather than a configuration problem. Attempting to finish it surfaced **three layered
defects plus one operational hazard**, none previously recorded:

1. **Migrad evaluates the objective at NaN nuisances.** In one grid cell the fit degenerates and
   calls the predictor with `zrei = NaN`.
2. **Nothing guards the objective against non-finite parameters**, so the NaN reaches the emulator,
   which returns 16 NaNs, and `keff.predict_at_keff` correctly refuses them.
3. **One cell's optimizer pathology destroys the entire 56-cell sweep** — `pool.map` propagates the
   exception and every completed cell's work is lost. No per-cell error isolation exists.
4. **Operational:** the run was launched through `| tee run.log`, and a pipeline reports the exit
   status of its *last* command. The crashed run was therefore reported as **exit code 0** — a
   crash presented as a success.

## 1. How it surfaced, and what was already wrong on disk

The directory `data/derived/wp_e6_sweep_synthetic_validation_2026_09_17/` held, untracked, a
`summary.json` reading `pass: true`, one multi-start sweep (`S1_noiseless_fdm`), and a
`superseded_single_start/` folder with all eight single-start sweeps.

**That `summary.json` did not describe the multi-start run.** It summarizes the superseded
single-start sweeps, and this is mechanically provable rather than inferred: the current script
writes an `optimizer_max_residual_per_sweep` key, and that file has only `{label, checks, pass}` —
it predates the multi-start fix. Its mtime (07:01) matches the last single-start file exactly, ten
hours before the one multi-start sweep. A `pass: true` summary of superseded runs, sitting beside
one finished scenario out of eight, is the shape of the WP-E3 defect this repo has recorded once
already ("a printed summary has contradicted persisted data"). It has been **moved into
`superseded_single_start/`** with a dated note, not deleted, so the evidence stays auditable.

So the true state was: the multi-start re-run had been **started and never finished** — one scenario
of eight. Finishing it is what hit the defect.

## 2. Root cause — `zrei = NaN`, established not guessed

Two scans first ruled out the obvious explanation, that the emulator is being asked for predictions
outside its valid region:

- 952 points at the nuisance box's 16 corners plus centre, across all 56 (m, f) cells: **0 invalid**.
- 11,200 uniform random points inside the box, 200 per cell: **0 invalid**.

The emulator does not produce invalid output anywhere in the box. The invalid input is **NaN itself**,
which is why no amount of in-box sampling reproduces it.

`scripts/diag_sweep_nonfinite_nuisance_2026_09_21.py` re-runs the failing sweep with the predictor
wrapped so an invalid prediction is *recorded with its exact arguments* and a sentinel returned,
instead of raising. Result (artifact
`data/derived/wp_e6_sweep_nonfinite_nuisance_diagnosis_2026_09_21/`):

| | |
|---|---|
| invalid-prediction events | **17**, confirmed final by the single-cell reproduction below |
| distinct (m, f) cells affected | **1 of 56** — (m, f) = (−22.5, 0.05) |
| `zrei` non-finite | **17 / 17 events** |
| `ha`, `hs`, `taueff` non-finite | 11 / 17 events each |
| events with all 16 native bins non-finite | **17 / 17** |
| events with a *finite but non-positive* native value | **0** |

So the failure is purely NaN propagation from the optimizer inward: `zrei` degenerates first and the
other three follow. `keff.predict_at_keff`'s check is doing its job correctly — it is the last line
of defence, and it is the only one.

**It is deterministic, and that is now isolated.** Re-running the *real* code path
(`sweep.run_sweep`) on the single affected cell reproduces it exactly, and **the worker count makes
no difference**:

| configuration | events | χ²_min | valid |
|---|---|---|---|
| `run_sweep`, workers = 1, `torch` threads = 1, 1 cell | **17** | 3.65299 | False |
| `run_sweep`, workers = 7, `torch` threads = 1, 1 cell | **17** | 3.65299 | False |

Identical. So this is **not** a fork or concurrency artifact — a hypothesis worth stating because it
was Stream 3's first guess and it is wrong. The defect is deterministic and reproducible in a single
process, which makes it *easier* to fix and harder to dismiss.

**Why the 9-start set exposes it and the single-start runs did not.** The single-start runs all began
at the nuisance medians; the 9-start set (`sweep.PROFILE_STARTS`: medians plus an 8-point LHS over
the central 90 % of each bound) starts some fits near the bounds, where the runs print
`Initial matrix not pos.def.` throughout. The multi-start fix was correct and necessary — it removed
a χ²_min overestimate of up to 0.9975, enough to flip a cell against the 5.99 threshold — and **it
also opened this failure mode**, which had no guard waiting for it. **The step from "ill-conditioned
start" to "a non-finite parameter reaches the objective" is a plausible mechanism, not an isolated
one**; Stream 3 has established *that* Migrad emits NaN parameters deterministically, not yet *by
which internal step*. Stated as a hypothesis rather than a conclusion.

## 3. A second, independent finding in the same run: convergence health was never persisted

The one completed multi-start sweep reports `all_minima_valid: false` — and **the summary artifact
recorded that nowhere.** It appeared only in a run log, and a log is not the artifact.

Quantified from `S1_noiseless_fdm.json` (56 cells):

- **10 cells** have `valid_minimum: false`; **5** of them are away from any bound.
- **7** of those 10 have `optimizer_residual` exactly **0.0**, and an 8th has 1e-4 — the extra starts
  found nothing better, so the minimum *location* is stable and the flag is Minuit's own
  Hesse/EDM verdict on a flat, rugged surface, not a missed minimum.
- `cells_with_residual_gt_0p1`: **0**; max residual **0.073**. The multi-start fix is working.
- `taueff_at_prior_box_edge`: **0 / 56** — and this is a genuine zero, not a dead flag: the cells
  that do hit a bound hit `hs` (18), `ha` (14) or `zrei` (9), never `taueff`. T0's 2026-07-28 item 2
  concern — that `taueff`'s (0.3, 1.8) is a prior box rather than trained support — does not bite in
  synthetic mode, because no best fit rests on that edge.

`scripts/wp_e6_sweep_synthetic_validation_2026_09_17.py` now writes a `convergence_health` block
carrying all of the above per sweep, **reported and not asserted** — the same posture the script
already uses for S2's coverage count. `summary["pass"]` is deliberately left unchanged, and a new
`pass_covers` field states which checks it actually covers, so a reader cannot mistake its scope.
Making convergence a pass/fail gate is a design change and is raised in §5, not taken here.

## 3b. A silent API trap found while diagnosing this — worth its own guard

`Chi2Profiler.__init__(self, p_data, cov_inv, predict_pk, ...)` takes the **inverse** covariance as
its second argument. `run_sweep` passes `cov_inv` correctly. Stream 3's first two diagnostic scripts
passed the **covariance** instead — and nothing complained. The run produced a plausible χ²_min
(127.597 instead of 3.65299) with zero NaN events, from which Stream 3 briefly and wrongly concluded
that the defect was concurrency-dependent. The controlled comparison against the real code path is
what caught it.

The failure is silent by construction: a covariance and its inverse are both symmetric
positive-definite, so the module's existing validity check ("Check that the inverse covariance matrix
is valid") cannot distinguish them. Anything downstream gets a wrong χ² that looks entirely
reasonable.

**Recommendation** (not implemented, same reason as §5): give the constructor a cheap orientation
check — for example, verify that `cov_inv` scaled against the data's own variance has the magnitude
of an inverse rather than a covariance, or accept the covariance and invert internally so the
ambiguity cannot arise. This is the second time in one session that a plausible number came from a
wrong call rather than a wrong pipeline, and both were caught only by comparing against the code
path that actually runs.

## 4. What is *not* affected

- **No real data.** Synthetic mode throughout; `REAL_DATA_RULING_PIN` is `None` and
  `load_real_observation()` still refuses.
- **No result is retracted.** The superseded single-start sweeps were already labelled superseded
  and are not results; the one multi-start sweep is intact and its numbers are unchanged.
- **No pinned artifact touched.** The k_eff ruling, the 9×9 covariance and the K3 gate are untouched;
  the K3 gate passed at the start of every run here.
- **Nothing here is exclusion or FIT.** Every artifact carries the SYNTHETIC label.

## 5. The decision this needs, and why Stream 3 did not just fix it

The crash is trivially removable — guard the objective, return a large penalty for a non-finite
parameter, and Migrad backs off. That is standard practice in likelihood optimization and would let
the validation finish today. **It is not obviously the right thing to do silently**, for two reasons:

1. **A guard converts a loud failure into a quiet one.** A cell whose fit degenerated to NaN is a
   cell whose χ²_min may be untrustworthy. Absorbing the NaN and reporting a number is exactly the
   move this repo has caught five times under a different name. Any guard must **count and persist**
   every non-finite evaluation per cell, and a cell that needed the guard should be flagged in the
   output, not smoothed over.
2. **Per-cell isolation changes what a sweep means.** Today one bad cell voids 56. If instead a bad
   cell is recorded as failed and the sweep continues, the sweep's output becomes partial by design,
   and whether a partial sweep may ever back an exclusion contour is a pre-registration question,
   not an implementation detail.

**Recommended shape** (not implemented): (a) reject non-finite parameters in the objective with a
recorded counter; (b) isolate per cell, so one cell fails rather than the sweep, with the failure in
the artifact; (c) treat any cell that required either mechanism as ineligible to contribute to a
contour until T0 rules otherwise. Each needs a negative control proving the guard fires.

**The number that decides how heavy (c) is has not been measured.** The diagnostic covered
**S2 seed 1 only**, where 1 cell of 56 needed the guard. The other seven scenarios — S2 seeds 2–5,
S3, S4, and S1 (which predates the diagnostic) — have **not** been measured for incidence. This
matters for what T0 is actually ruling on: if one or two cells per sweep need the guard, "ineligible"
is cheap bookkeeping and a contour loses a couple of cells; if it is routinely a dozen, the sweep's
output is **structurally partial** and (c) is a redesign rather than a flag. Measuring it is cheap —
the diagnostic runs unchanged over all eight scenarios — and Stream 3 will do so on request, but the
measurement should precede the ruling rather than follow it.

**Asks.** Stream 3 can implement (a)–(c) with controls on request. It has not, because the sweep's
acceptance rule is pre-registration territory and the driver's outputs are destined to be labelled
`exclusion`/`FIT`. The real-data path is blocked on C1–C5 regardless, so nothing is waiting on this.

## 6. Fix applied, 2026-09-21 — at the most conservative setting

T0 ruled the same day: *"adopt decision 1 and implement what you could at this stage waiting for
others streams"* (`briefs/T0_RULINGS_2026_09_21.md`). Stream 3 reads the second clause as the
request §5 invited, records that reading as an interpretation with a countermand window (R2 item 2),
and has implemented (a)–(c) with (c) at its **most conservative** setting so that the
implementation decides no acceptance rule. Commit `691a4fa`.

- **(a) Counted guard.** The multi-start objective returns a finite penalty (1e30) for a non-finite
  nuisance. Every such evaluation is counted, **per start**, and persisted per cell. Non-finite
  *parameters* only: an emulator returning NaN for finite inputs is a different defect and still
  fails the cell rather than being penalised away.
- **(b) Isolation.** A raising cell is recorded verbatim in the artifact instead of destroying the
  sweep through `pool.map`.
- **(c) Eligibility.** A guarded or failed cell is `contour_eligible: false`: it keeps its χ²_min
  for diagnosis, gets `null` in every grid, receives no inside/outside verdict, and cannot anchor
  Δχ² even when it holds the lowest χ². Any ineligible cell makes the sweep's
  `contour_status` **WITHHELD**; a sweep with no eligible cell refuses to report at all.

**Re-mirrored after Stream 2 re-issued.** T0 confirmed the ρ = 20 adoption in the Stream 2
repository too (their D7′, verbatim: *"oui je confirme la coupure aussi sur ce repo"*), and every
certificate was re-emitted to replace the superseded "cut is NOT adopted" wording. Stream 3 verified
the re-issue independently rather than on report: leaf by leaf with wording and provenance fields set
aside, **0 differing leaves** of 5 459 (`CM_POINTS_RHO20`) and 2 713 (`A2_MEMBERSHIP`) — no computed
value changed — and their control suites re-run on this side, **46/46, 35/35, 33/33**. The mirror is
re-pinned to their `main` (`0e0bfe7`) after checking each file byte-identical to
`main:data/certificates/…`; the 140-label vocabulary is unchanged, as they predicted.

**Confirmed on the real defect cell, real unwrapped predictor.** (m, f) = (−22.5, 0.05) now reports
χ²_min **3.65299** with **guard = 17** — exactly the diagnosis — eligible false, its three
neighbours untouched, contour WITHHELD. Before the fix the identical call raised and produced
nothing.

**What the per-start counter adds to §2.** All 17 evaluations come from **start #9 alone**:
`zrei` 14.30 (bound 14.91), `ha` 0.47 (bound 0.066), `hs` 0.81, `taueff` 0.44 (bound 0.3) — the LHS
point nearest the box's edges. That is consistent with §2's near-bound-start hypothesis and narrows
it to a single start; it still does not isolate Migrad's internal step, and is not claimed to.

> **Correction, 2026-09-21 (same day) — the near-bound-start hypothesis is REFUTED as a general
> explanation; see §7.** "All from start #9" is true of this one cell and is not the pattern. Across
> the eight scenarios the guard fires from **every** start index, **including start #1, the nuisance
> medians**, and most often from start #6. One cell was generalised into a mechanism; the full
> measurement does not support it.

10 new tests (61 pre-existing unchanged), each path with its control, mutation-verified. The
validation script is now null-aware — `not None` is `True`, so an unchecked read would have counted
an ineligible cell as *inside* the region.

**Still T0's:** whether an ineligible cell may ever contribute to a contour, and therefore whether a
WITHHELD sweep is a dead end or a partial result. The incidence measurement across all eight
scenarios — the number that decides how heavy that question is — is what the fix was needed to
produce; see `data/derived/wp_e6_sweep_synthetic_validation_2026_09_17/summary.json` once the run
recorded in `launches.log` completes.

## 7. The incidence, measured — and it is not cheap bookkeeping

With the guard in place the full eight-scenario synthetic validation **completed for the first
time**: one recorded start, one genuine `EXIT=0` under `pipefail`, 1 h 37 min, `pass: true` on S1, S3
and S4, and S2 reporting 4 of 5 injected cells inside the region **with the fifth ineligible** — the
null-handling of §6 mattered in practice, since an unchecked `not None` would have counted it inside.
Artifacts: `summary.json`, `guard_incidence.json`, `start_count_sensitivity.json` in
`data/derived/wp_e6_sweep_synthetic_validation_2026_09_17/`.

| sweep | ineligible / 56 | in the f = 0 column | contour |
|---|---|---|---|
| S1 noiseless FDM | 0 | 0 | COMPLETE |
| S2 seed 1 | 1 | 0 | WITHHELD |
| S2 seed 2 | 2 | 0 | WITHHELD |
| S2 seed 3 | 2 | 0 | WITHHELD |
| S2 seed 4 | **11** | **8 of 8** | WITHHELD |
| S2 seed 5 | 4 | 0 | WITHHELD |
| S3 noiseless CDM | 1 | 0 | WITHHELD |
| S4 strong-FDM control | 5 | 0 | WITHHELD |

**26 of 448 cells (5.8 %), and 7 of 8 sweeps WITHHELD.** That answers §5's open question: under the
most conservative rule the sweep would almost never yield a contour, and in S2 seed 4 the guard takes
out the **entire f = 0 column** — the CDM column every exclusion is measured against. This is a
design question, not a flag.

**The measurement that bears on the ruling.** In **25 of the 26** ineligible cells the *retained*
minimum came from a start that **never fired the guard**; the pathological start simply lost. The
single exception is the original defect cell, (−22.5, 0.05) in S2 seed 1, whose retained χ²_min
3.65299 came from the very start that degenerated. And in no sweep does the reference minimum change
if every cell is kept. So a less conservative rule is available and is *measured here, not adopted*:

> **Rule B** — a cell is eligible iff its retained minimum came from a start with zero guarded
> evaluations. On this evidence it would restore 25 cells and withhold exactly the one whose number
> is genuinely suspect.

**What the pattern is, and is not.** The guard fires from every start index — cells per start:
#1: 1, #2: 2, #3: 2, #4: 3, #5: 2, **#6: 12**, #7: 1, #8: 2, #9: 1 — so it is not a near-bound
phenomenon (start #1 is the medians). The per-cell counts are **quantized**: 17 (13 cells),
23 (11), 29 (1), 35 (1), steps of 6. That regularity suggests a fixed-length internal Minuit routine
running on already-non-finite state rather than a wandering line search. Recorded as an observation;
the internal step is still not isolated.

**A worry raised and then retired by measurement.** The completed sweeps show `optimizer_residual`
(best of first 5 starts − best of all 9) above 0.1 in up to 14 cells per sweep, with maxima of 1.30,
2.42 and 18.9 — far above S1's 0.073, the only number the earlier single-scenario validation saw.
That looked like the single-start defect (0.9975) recurring at larger scale. It is not, at the level
that matters: recomputing every inside/outside verdict with 5, 7 and 8 starts instead of 9 gives
**zero verdict flips in all eight sweeps**, and the grid minimum never moves. The large residuals sit
in cells far from the 5.99 threshold. Stability from 5 to 9 starts is evidence, not proof, that 9
suffice — but it is the relevant evidence, and it is now persisted rather than assumed.

---
*Generated-by: Claude Opus 5 (Stream 3, 2026-09-21) | Verified-by: two exhaustive scans (952 corner
points, 11,200 random in-box points, both 0 invalid) ruling out the emulator; the failing arguments
captured with their PIDs by a wrapped predictor; the stale summary proved stale by a missing key its
own producing script writes | Reviewed-by: pending T0*
