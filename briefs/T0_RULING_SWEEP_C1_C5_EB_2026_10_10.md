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

## Coverage run: INCOMPLETE (5 of 12 planned draws; stopped by the system for low memory, 2026-10-10)

`scripts/wp_e6_sweep_v2_coverage_2026_10_10.py`, record `data/derived/wp_e6_sweep_v2_coverage_2026_10_10.json` (no summary block:
the run never finished). Draw count, seeds and grid were fixed before the run. Five draws are not a coverage result.

| Measure (5 draws) | Count |
|---|---|
| Truth cell inside the 2-dof 95% region | 5 |
| Truth cell's fit a valid minimum | 4 |
| Truth cell's fit at a bound | 3 |
| Fitted s (true 1.0) | 3.21, 0.00, 1.73, 0.00, 1.53 |

Reading: the truth is not excluded in any draw, but the Si III amplitude is weakly constrained and often sits on a box edge.
Rerun needs a quiet machine: 12 draws at roughly 15 minutes each. Not rerun, by instruction.

## To make it live (T0)

Name this file in `REAL_DATA_RULING_PIN`; then wire `run_sweep` to V2 and run the validation in item 2 before any real vector
is fitted. Changing any choice after real data are seen is a `TUNING_LOG.md` event.
