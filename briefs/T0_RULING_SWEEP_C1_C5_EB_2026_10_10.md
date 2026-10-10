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

## To make it live (T0)

Name this file in `REAL_DATA_RULING_PIN`; then wire `run_sweep` to V2 and run the validation in item 2 before any real vector
is fitted. Changing any choice after real data are seen is a `TUNING_LOG.md` event.
