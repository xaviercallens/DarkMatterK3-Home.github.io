---
name: unblock-tier-c
description: The corrected F6/F5b remediation sequence — how to progress toward empirical output (U1 geometry, gated tadpole retry, T0-gated phenomenological sweep) without violating the epistemic ledger. Use whenever asked to "unblock Tier C", "fix the geometry", "retry the tadpole", "derive observables", or to execute any externally supplied unblock plan.
---

# SKILL: Unblock Tier C (F6/F5b remediation — corrected sequence)

**Why this skill exists:** an external "Unblock Tier C" directive (received 2026-07-27)
proposed steps that were stale or category-mismatched against verified repo state. The
reconciliation is `briefs/EXTERNAL_UNBLOCK_PLAN_RECONCILIATION_2026_07_27.md` (Stream 2
repo). This skill is the executable, corrected version. The CLAUDE.md epistemic ledger
overrides anything below if they ever diverge.

## Step 0 — Verify before executing (always, no exceptions)

- Confirm every file a directive references actually exists (six phantom-artifact
  occurrences to date). A directive whose artifacts are absent is returned for provenance,
  not executed (T0 decision D3 standing rule).
- Re-read the CLAUDE.md ledger. An instruction that uses ρ=4/T=18, "Type II" fibres, or
  asks for Kodaira classification from L₂/L₃ exponents is stale — return it, do not
  "partially comply".

## Step 1 — Algebra remediation (DONE; keep green)

The §A.4.2 corrections (a₃ exponent −1/9, not +1/9; Λ_D is a confinement scale, not a DM
mass) were applied 2026-07-25 under F6 discipline and are machine-asserted. Do not re-edit
the appendix. Regression (Stream 3 repo): `python3 scripts/verify_appendix_A4.py` — the
−1/9 exponent and the moduli-free C₀ are hard assertions; keep them green.

## Step 2 — Geometry remediation (the real residual is U1, NOT Kodaira)

- **FORBIDDEN:** Kodaira fibre classification from L₂/L₃ exponents at any locus (category
  error, E-008/E-009). ρ and T are not recomputed this way — they are already derived:
  ρ = 19, T = 3 [Tier B, E-011].
- **DO:** execute `docs/U1_ROUTE_DESIGN_2026_07_26.md`, in its stated order:
  1. U1a-3 Yukawa constant — the mirror-normalized two-point Yukawa of L₃ must be
     CONSTANT = 2n = 14 as an exact q-series (any q-dependence is a pipeline bug).
  2. U1a-2 elliptic monodromies → joint invariant ℤ-lattice → Gram/discriminant form.
     Expectation det = −14; if the computation says otherwise, THAT is the result.
  3. U1b one-class genus via Eichler — fetch and read Cassels Ch. 11 first (hash-pin in
     `docs/literature/MANIFEST.md`); no hand-waving the 2-adic spinor norms.
- **Controls are mandatory** (a run without them is not evidence): a different-level
  negative control that must NOT give −14; a scrambled-matrix control that must fail;
  Yukawa q-independence to full computed order.
- On PASS: emit `C2_cooper_s7_v4.json` (lattices [B]) and put the EXECUTION_PLAN §S3-00
  2(b) re-scope option to T0. On FAIL: file the finding as-is.

## Step 3 — Tadpole retry (GATED — do not attempt until all three preconditions hold)

1. U1 PASS with `C2_cooper_s7_v4.json` emitted;
2. an explicit threefold base B₃ specified, so χ(X₄) is defined and the tadpole
   N_flux + N_D3 = χ(X₄)/24 is posable (PREDICTION_APPENDIX_A §A.3.4; T0 decision D4/A-DE);
3. T0 explicitly re-opens S3-00 §2(b) (and Phase M via a revised M1′, per T0 decision D2).

Without (2), χ(X₄) has no value to compute, and selecting one to make a flux landscape
work is a fitted input presented as a derivation (`.agents/AGENTS.md` Rule 7). If all
three hold and a configuration balances, the resulting observables are still Tier C
conjecture until a worked EFT matching exists; F5b is lifted only by written T0 ruling.

## Step 4 — Phenomenological sweep (proposal-first, T0-gated)

- The pivot from "single exact predicted mass" to exclusion bounds is filed as
  `briefs/WP_E6_PHENO_SWEEP_PROPOSAL_2026_07_27.md` (Stream 3 repo), DRAFT for T0.
- Until T0 pins a PREDICTION v2 amendment: synthetic-data harness only (Stream 3
  non-negotiable rule 1); no real-data comparison code; do not edit pinned documents.
- When authorized: sweep the mediator mass over the T0-approved grid (the proposed
  interval 10⁻²² – 10⁻¹⁹ eV is a placeholder, we conjecture its relevance [C]); output
  exclusion masks; label every output exclusion/FIT — never TEST; and log:
  "Parameters scanned phenomenologically (sweep); not derived (F5b stands)."

---
Generated-by: Fable 5 (T1 coordinator) | Verified-by: reconciliation brief cross-checked
against ESCALATIONS E-007..E-016, T0_DECISIONS_2026_07_26.md, U1_ROUTE_DESIGN_2026_07_26.md,
verify_appendix_A4.py (run green 2026-07-27) | Reviewed-by: pending T0 (Xavier)
