# Phase 1 Decision — Reverted to Option 1 (z≈4.2 slice)

**Date:** 2026-07-27 (supersedes the earlier "commission emulator extension" choice from the
same day)

## What changed

Xavier's original AskUserQuestion answer was "Commission emulator extension." Agent 4's
scoping (see `PHASE1_A4_EMULATOR_EXTENSION_SCOPING.md`) found this needs ~10,000-200,000+
core-hours of HPC compute this VM cannot provide (no MPI, no GPU, 8 cores). Given that, Xavier
reverted the decision: **defer the extension to a future phase** (recorded in
`briefs/FUTURE_PHASE_EMULATOR_EXTENSION_2026_07_27.md`), and **proceed now with Option 1** —
restrict to the emulator's usable z≈4.2 slice, for quick, realistic, achievable-today progress.

## Active path from here

1. Verify DESI DR1's own z-binning lands close enough to z=4.2 to be usable (flagged as
   unverified by Agent 1's original integration report)
2. Use Agent 1's validated iminuit/Cobaya wrappers (both cross-validated,
   chi2=77.41 vs loglike=-38.71) + Agent 2's sweep scaffold (20-cell grid, verified) to produce
   an interpretable model landscape across a PLACEHOLDER (m,f) grid (not T0-approved, see correction note) at z=4.2
3. **Epistemic boundary, explicit:** per Stream 3 CLAUDE.md rule 1 — "No real-data comparison
   code before PREDICTION.md carries PINNED: (gate G1). Synthetic-data infra only" — this step
   computes the emulator's own forward-model P1D(k) predictions across the grid, NOT a
   comparison against any observational dataset (DESI or otherwise). Real-data comparison stays
   gated behind the Phase 3 PREDICTION v2 pin, as originally planned. This is model exploration,
   not a project result.

## Not superseded

- D0's other findings (tooling repos, package installs, Agent 2/3 results) stand as-is.
- The original 90-day roadmap's Phase 2/3/4 structure (stats design → pre-reg → real data)
  still governs when actual DESI comparison happens.
