# WP-E6-SWEEP — theory-correction and eligibility rulings C1–C5, E-B (design v2) — STAGED, NOT PINNED

**Date:** 2026-10-10 · **Label:** ENGINEERING / DESIGN (not TEST, not FIT) · **Status:** STAGED. This file is not named by
`REAL_DATA_RULING_PIN`, so `sweep.load_real_observation()` still refuses. Merging this PR does not pin it.

## Authority, verbatim

T0 (Xavier), 2026-10-10, relayed through the Stream 2 session: *"implement on my behalf"*, against the list
*"The Home real-data rulings (C1–C5, E-A/B/C)"*. The options below are the ones Stream 3 recommended in
`T0_DECISION_REQUEST_SWEEP_THEORY_CORRECTIONS_2026_09_17.md` and `T0_DECISION_REQUEST_SWEEP_ELIGIBILITY_2026_09_21.md`.
This is a delegated decision, not a T0 sentence. It is reversible by one T0 sentence, and it is not in force until T0 sets
`REAL_DATA_RULING_PIN` to this file (that edit is the pin; it is deliberately left undone).

## The rulings as implemented

| Item | Chosen | What the code does |
|---|---|---|
| C1 Si III–Lyα | c, profiled amplitude | upstream's oscillation shape g(k), amplitude `s` a 5th nuisance, prior box [0, 4], init 1 (`pipeline/sweep_corrections.py`) |
| C2 patchy reionization | b | upstream's fixed `with_patchy` factor at z = 4.2, from the sha256-pinned upstream pickle |
| C3 resolution template | a | none (provider default) |
| C4 band 8 beyond the provider k cut | b | drop 3 members with k > 0.5π/R_z = 0.041403 s/km, re-aggregate band 8 from 7 (`scripts/wp_e6_sweep_aggregate_9x9_c4.py`) |
| C5 χ²_ν | a | cell dof = 9 − 5 = 4 (`sweep.DOF_CELL_V2`); the DESI k-cut term is not on disk, so it is not added |
| E-B eligibility | E-B | cell eligible iff the retained minimum came from a start with zero guarded evaluations (`sweep.cell_eligible`) |
| E-C | follow-up | not done; optimizer pathology is not diagnosed |

## What was re-derived (computed, not typed)

* Aggregation with the cut: members per band 3,4,4,6,8,9,11,11,7 (v1: …,11,10). Bands 0–7 are unchanged; the matrix is
  symmetric, Cholesky-positive-definite, condition number 23.61.
* K2 re-run unchanged on the new artifacts (same script body, same 0.1 σ threshold, 952 points). The wrapper regression
  against the 2026-07-28 controls is exact. Both pre-check controls pass. As in v1 the flag `pass_R_KEFF_2` is false, which
  is why K2 adds the bound as a variance term. New table in `pipeline/keff.py` (`V2`), pre-check sha256
  `0fb1e998e48703bd3160c64bf88770b4c871fcc133df007a583974f251c35a9f`; it re-derives at use, and a mismatch hard-stops.
* Bands 0–7 of the K2 β table equal v1 to 1e-6; band 8 is the only band whose aggregation changed.

## What is NOT done, and what it blocks

1. **No real-data run was made and no pin was set.** `run_sweep(..., design="v2")` is wired: Si III predictor, 4 dof, E-B,
   V2 artifacts, a synthetic-mode refusal of either real vector, and the real-mode refusal while the pin is unset.
2. **Injection–recovery was done on a fake smooth emulator with a known truth, not on the real emulator.** The truth cell
   fits a noiseless vector to chi2 < 1e-3. The Si III amplitude injected at 2.5 came back as 2.41, so it is partly degenerate
   with the IGM nuisances at this covariance; the test pins that observed bound (0.25), not exactness. A real-emulator
   synthetic validation is still to do before any real vector is fitted.
   Also fixed in this change: the per-cell `contour_eligible` field now follows the active rule (it used the guard count).
3. **Si II, Mg II and C IV are not modelled.** C5 states 4 dof on that basis; it is a known limitation, not a fix.
4. The Si III box [0, 4] is a prior box, not a trained support. A best fit at an edge is reported as such.
5. Anything fitted under this design remains exclusion/FIT, never TEST (ledger item 5), until a PREDICTION v2 amendment pins it.

## Real-emulator synthetic validation (2026-10-10; `data/derived/wp_e6_sweep_v2_synthetic_validation_2026_10_10.json`)

3×3 grid containing the truth cell (m = −22.0, f = 0.2), IGM medians, v2 predictor, V2 covariance. No real vector.

| Case | Truth-cell χ² | Fitted s (true) | Grid minimum | Fit valid |
|---|---|---|---|---|
| s = 1, noiseless | 0 | 1.000 (1.0) | the truth cell | yes |
| s = 2.5, noiseless | 1e-6 | 2.500 (2.5) | the truth cell | yes |
| s = 1, one noise draw (seed 20261010) | 8.77 | 2.32 (1.0) | (−22.5, 0.2), χ² 5.28 | no, at a bound |

What this does and does not say:
* Noiseless injection is recovered exactly on the real emulator, for both amplitudes. This tests the code path, not the statistics.
* The noisy case is **one draw, not a coverage study**. The truth cell sits Δχ² = 3.5 above the grid minimum, inside the 2-dof 95%
  threshold of 5.99, so the truth is not excluded. The truth cell's own fit did not return a valid minimum and sat at a bound,
  and its fitted s is 2.3 against a true 1.0. The amplitude is weakly constrained by one draw at this covariance.
* The whole region near the truth is flat: neighbouring cells differ by less than a few in χ². A sweep on real data should not
  be expected to localise (m, f) here.
* Not done: a multi-draw coverage study, or a run over the full 56-cell grid. Both are needed before any real vector is fitted.

## Coverage run: 12 fixed-seed noise draws, synthetic only (2026-10-10; resumed once after a low-memory stop)

`scripts/wp_e6_sweep_v2_coverage_2026_10_10.py`, record `data/derived/wp_e6_sweep_v2_coverage_2026_10_10.json`. Draw count, seeds and
the 3×3 grid were fixed before the run. Draws 0–4 ran first, then the run was stopped by the system for low memory and resumed
with the same seeds for draws 5–11 (BLAS threads capped at 2).

| Measure (12 draws) | Count |
|---|---|
| Truth cell inside the 2-dof 95% region | 12 |
| Truth cell eligible under E-B | 12 |
| Truth cell's fit a **valid** minimum | **5** |
| Truth cell's fit at a bound | 6 |
| Mean truth-cell χ² (expectation 4 for 4 dof) | 4.21 |
| Fitted s, true 1.0 | median 1.38, range 0.00 to 3.66 |

What this says and what it does not:
* **The inside-95% count is weak evidence.** The grid is flat (the truth's Δχ² is at most 1.4 in every draw), so a region that
  large contains the truth almost regardless of the fit. It is not a power statement.
* **The optimizer is the problem, not the physics.** Seven of 12 truth-cell fits did not return a valid minimum, and the
  run logged repeated "initial matrix not pos.def." messages. **E-B did not catch them:** eligibility keys on non-finite
  guard evaluations, not on `valid_minimum`, so an invalid minimum is currently contour-eligible. This is a defect of the
  eligibility rule as written, not of the data.
* The χ² level is plausible (mean 4.2 for 4 degrees of freedom), and s is poorly constrained (box-edge fits in half the draws).
* **Consequence for T0:** do not pin on this evidence. Before any real vector, the rule needs a decision on invalid minima
  (an E-C follow-up or an added validity condition), and the fifth nuisance may need a tighter box or a prior. Both change the
  ruling and are T0's.

## T0's choice on invalid minima: rule E-B+V (2026-10-10)

T0 (Xavier), replying to the open question on invalid minima, in these words: **"Rule E-B+V"**. This is a T0 sentence, not a
delegated decision, and it supersedes the delegated E-B for design v2. A cell is contour-eligible iff the start that produced
the retained minimum had zero guarded evaluations **and** the retained fit is a valid Minuit minimum (`sweep.cell_eligible`,
rule `"E-B+V"`; `run_sweep(design="v2")` now uses it, v1 is unchanged).

What it does not settle, still open:
* On the 12 synthetic draws, 7 of 12 truth-cell fits were invalid, so this rule withholds those cells and a v2 sweep on
  similar data would withhold most of them. The rule makes the defect visible; it does not fix the optimizer (E-C).
* The Si III amplitude box [0, 4] and whether it needs a prior are undecided.
* The pin (`REAL_DATA_RULING_PIN`) is still unset, and a pin on this evidence would be T0's call.

## Delegated decisions taken on T0's behalf, 2026-10-10 ("continue and take decision on my behalf")

Each is reversible by one T0 sentence.

1. **Si III box stays [0, 4], no prior added.** Reason: the only evidence for changing it is the synthetic validation, and
   tightening a box after seeing where fits land is tuning on the validation. Fits at the lower edge are not a defect (s ≥ 0 is
   physical) and are reported as at-boundary. A prior is a modelling choice with no data behind it today.
2. **The pin is NOT set.** Reason: 7 of 12 synthetic truth-cell fits were invalid, so a real sweep under E-B+V would withhold
   most cells. Pinning would pre-register a design whose validation has not passed. The pin stays T0's one-line edit.
3. **E-C (fix the optimizer) is opened as follow-up work, not done here.** The messages ("initial matrix not pos.def.") point at
   flat directions interacting with the box; that is a diagnosis to make, with its own validation, not a change to slip into a
   ruling. Suggested first step: re-run the 7 invalid draws with a bounded fallback for a start that returns invalid, and count.
4. **PR #19 is merged.** It adds evidence, a selectable rule and T0's E-B+V choice; it sets no pin and runs no real data.

## E-C diagnosis (2026-10-10, synthetic only, pipeline unchanged)

`scripts/wp_e6_sweep_v2_optimizer_diagnosis_2026_10_10.py`, record `data/derived/wp_e6_sweep_v2_optimizer_diagnosis_2026_10_10.json`.
The truth cell of the seven invalid coverage draws (3, 5, 6, 7, 8, 9, 10) was re-profiled with the same 9 starts under three
variants. Best-start validity: BASE (Migrad, re-run once) 5 of 7, STRATEGY 2 0 of 7, SIMPLEX then Migrad 4 of 7.

| Draw | BASE χ² (valid) | STRAT2 χ² (valid) | SIMPLEX χ² (valid) |
|---|---|---|---|
| 3 | 7.235 (yes) | 6.203 (no) | 6.409 (no) |
| 5 | 4.604 (yes) | 4.625 (no) | 4.618 (yes) |
| 6 | 5.433 (no) | 5.436 (no) | 5.624 (yes) |
| 7 | 4.749 (yes) | 4.761 (no) | 4.757 (no) |
| 8 | 0.892 (no) | 0.783 (no) | 0.970 (yes) |
| 9 | 12.406 (yes) | 12.531 (no) | 12.201 (no) |
| 10 | 4.283 (yes) | 4.272 (no) | 4.325 (yes) |

What this says:
* **The validity flag is not a stable property of the fit.** BASE here returned a valid best start in 5 of the 7 draws that the
  pipeline recorded as invalid. The two code paths differ only by numerically equivalent arithmetic (matrix inverse route,
  array ordering). A flag that flips under that is not a safe eligibility test, which weakens E-B+V as the sole gate.
* **The minima are not reliably found.** Across variants the best χ² differs by up to about 1.0 (draw 3: 7.24 against 6.20),
  and no variant is lowest in every draw. The multi-start optimizer leaves χ² on the table in some draws.
* Strategy 2 never returned a valid best start here, so it is not a fix.
* No variant is adopted. This is a diagnosis; any change to the optimizer or to the eligibility rule is a ruling.

Suggested next step for T0 or Stream 3: judge eligibility on a **reproducibility** condition (best χ² agreeing across two
optimizer variants within a tolerance) instead of the Minuit validity flag, and pre-register the tolerance before any real vector.

## T0's replacement of the validity flag: rule E-B+R (2026-10-11)

T0 (Xavier), after the diagnosis above, in these words: **"replace the validity flag"**. This supersedes E-B+V for design v2.

**Rule E-B+R.** A cell is contour-eligible iff (E-B) the start that produced the retained minimum had zero guarded evaluations
**and** (R) the two optimizer passes over the same starts, Migrad and simplex-then-Migrad, agree on the best χ² to within
`REPRO_TOL`. The retained minimum is the lower of the two passes. A missing or NaN gap is ineligible. The Minuit validity flag is
still recorded per cell and no longer gates anything. v1 and rule E-B+V remain selectable and unchanged.

**Tolerance, taken on T0's behalf and pre-registered here:** `REPRO_TOL = 1.0` in χ². Δχ² = 1 is the one-parameter 1σ step; two
passes that disagree by more have not found the same minimum at the resolution the 95% contour (5.99, 2 dof) is read at. It was
set looking at the synthetic diagnosis (largest pass difference 0.83), so it is not blind to that data; it was fixed before any
real vector, and changing it after real data are seen is a `TUNING_LOG.md` event. Reversible by one T0 sentence.

**Effect on the 12 synthetic draws** (truth cell only, `scripts/wp_e6_sweep_v2_rule_ebr_check_2026_10_11.py`):

| Rule | Truth cells eligible (of 12) |
|---|---|
| E-B | 12 |
| E-B+V (Minuit validity flag) | 5 |
| E-B+R (tolerance 1.0) | 11 |

* Pass-to-pass gap: median 0.012, maximum 1.28. One draw (3) is withheld for a gap of 1.28; its two passes reached χ² of about
  5.9 and 7.2.
* Seven fits that the validity flag rejected have gaps of 0.6 or less and are kept: the flag was rejecting reproducible fits.
* Two optimizer passes are not a proof of a global minimum. Both could miss the same basin. The rule measures agreement.
* Not done: a re-run of the full 56-cell grid under this rule, a multi-draw cell-level coverage study on the noisy draws beyond
  the truth cell, and any real vector. The pin is unset and the evidence for it is still the synthetic record only.

## Full 56-cell synthetic sweep under E-B+R (2026-10-11)

`scripts/wp_e6_sweep_v2_fullgrid_2026_10_11.py`, record `data/derived/wp_e6_sweep_v2_fullgrid_2026_10_11.json` (synthetic label).
One fixed-seed noisy draw (seed 20261011) around the truth (m = −22.0, f = 0.2, s = 1) on the real emulator, the full pinned
8 × 7 grid, design v2. No real vector.

| Measure | Result |
|---|---|
| Cells run / ineligible under E-B+R | 56 / 0 |
| Contour status | COMPLETE |
| Grid minimum | m = −22.0, f = 0.35, χ² 1.48 |
| Truth cell | χ² 1.61, eligible |
| Pass-to-pass gap | median 0.015, maximum 0.14, cells above 1.0: 0 |
| Minuit validity flag invalid | 29 of 56 |
| Fits at a box edge | 14 of 56 |

What this says and what it does not:
* **The reproducibility gap is small everywhere on this draw** (maximum 0.14 against the 1.0 tolerance), while the Minuit flag
  would have withheld 29 of 56 cells. That is consistent with the flag-instability finding and is why E-B+V was a poor gate.
* The grid minimum is at the truth's mass and one grid step away in f; the truth sits 0.13 above it in χ². The surface is
  flat, so this is not localisation evidence.
* **One draw.** Gaps this small on one draw do not bound the gap on others: on the truth-cell check one of 12 draws had a gap
  of 1.28. A multi-draw full-grid study is not done (about an hour per draw).
* Both passes agreeing says the optimizer is stable here, not that the minimum is global.
* 14 fits at a box edge are reported, not excluded; a contour that depends on an edge fit should be read with that in view.
* The pin is still unset. This is the evidence the brief listed as missing, and it is a single synthetic draw.

## To make it live (T0)

Name this file in `REAL_DATA_RULING_PIN`; then wire `run_sweep` to V2 and run the validation in item 2 before any real vector
is fitted. Changing any choice after real data are seen is a `TUNING_LOG.md` event.
