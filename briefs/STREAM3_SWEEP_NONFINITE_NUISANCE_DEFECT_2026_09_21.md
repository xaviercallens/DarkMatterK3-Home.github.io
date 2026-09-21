# WP-E6-SWEEP — three layered defects found by trying to finish the synthetic validation

**Date:** 2026-09-21 · **Stream:** 3 (experimentation) · **Status:** defect report, diagnosis
complete, **no fix applied yet** (the fix is a driver design decision — §5).
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
| invalid-prediction events | **17** (at the time of writing; the diagnostic sweep was still running) |
| distinct (m, f) cells affected | **1 of 56** — (m, f) = (−22.5, 0.05) |
| `zrei` non-finite | **17 / 17 events** |
| `ha`, `hs`, `taueff` non-finite | 11 / 17 events each |
| events with all 16 native bins non-finite | **17 / 17** |
| events with a *finite but non-positive* native value | **0** |

So the failure is purely NaN propagation from the optimizer inward: `zrei` degenerates first and the
other three follow. `keff.predict_at_keff`'s check is doing its job correctly — it is the last line
of defence, and it is the only one.

**Why the 9-start set exposes it and the single-start runs did not.** The single-start runs all began
at the nuisance medians. The deterministic 9-start set (`sweep.PROFILE_STARTS`: medians plus an
8-point LHS over the central 90 % of each bound) starts some fits near the bounds, where Migrad's
initial Hessian is ill-conditioned — the runs print `Initial matrix not pos.def.` throughout — and
from there a line search can produce a non-finite parameter. The multi-start fix was correct and
necessary (it removed a χ²_min overestimate of up to 0.9975, enough to flip a cell against the 5.99
threshold); **it also opened this failure mode**, which had no guard waiting for it.

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

**Asks.** Stream 3 can implement (a)–(c) with controls on request. It has not, because the sweep's
acceptance rule is pre-registration territory and the driver's outputs are destined to be labelled
`exclusion`/`FIT`. The real-data path is blocked on C1–C5 regardless, so nothing is waiting on this.

---
*Generated-by: Claude Opus 5 (Stream 3, 2026-09-21) | Verified-by: two exhaustive scans (952 corner
points, 11,200 random in-box points, both 0 invalid) ruling out the emulator; the failing arguments
captured with their PIDs by a wrapped predictor; the stale summary proved stale by a missing key its
own producing script writes | Reviewed-by: pending T0*
