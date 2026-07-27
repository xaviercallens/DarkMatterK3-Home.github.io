# Correction: Fabricated Grid Provenance Claim

**Date:** 2026-07-27, evening
**Severity:** Process failure, not a physics error — no false physics claim was ever computed
against real DESI data, but a false data-provenance claim was asserted repeatedly and treated as
ground truth for several hours of planning and agent work.

## What happened

In the very first literature-review document produced this session
(`literature_review/03_parameter_sweeps_literature/index.md:230`), the assistant wrote:

> **Proposed (from K3_CRITERIA.md v0.1):**
> m (meV): {0, 0.1, 0.5, 1, 5}
> f (frac): {0.0, 0.1, 0.5, 1.0}

**`K3_CRITERIA.md` was never actually read at that point.** These specific numeric values and
the "meV" unit were invented and mislabeled as sourced from a real, frozen project artifact.

That false claim was then repeated as established fact across:
- `briefs/D0_VERIFICATION/D0_AGENT_PLAN_2026_07_27.md` ("does not touch ... `K3_CRITERIA.md`
  (frozen)")
- `briefs/D0_VERIFICATION/PHASE1_AGENT_PLAN_2026_07_27.md` ("this is the frozen K3_CRITERIA.md
  v0.1 grid — do not alter it")
- `briefs/D0_VERIFICATION/PHASE1_DECISION_2026_07_27.md`
- Two agents' real computational work (Agent 2's sweep scaffold, Agent 5's forward-model
  landscape at z=4.2) ran against these fabricated values without the claim ever being checked.

## What's actually true (verified 2026-07-27 evening, by directly reading the file)

`K3_CRITERIA.md` exists, in the **Stream 3** repo (`SocrateAI-Scientific-Agora-Home`), not
Stream 2 as earlier memory/context implied. Its actual content: geometric selection criteria
for K3 vacuum candidates (C1 mirror-map integrality, C2 Kodaira fiber content, C3 symmetric-square
structure, C3b Shioda-Inose moduli map, C4 lattice/Picard consistency, C5 swampland bounds). It
contains **zero** content about dark-matter mass, FDM fraction, or any physics parameter grid.
It is explicitly still `SKELETON v0.1 — NOT YET FROZEN`.

There is currently **no project-approved (m,f) grid** for the WP-E6 Lyman-alpha MFDM sweep,
in units or values. This needs a real T0 decision, not an assumption.

## What survives this correction

- The engineering/integration work is still valid and useful: Agent 1's emulator wrapper
  (iminuit + Cobaya, cross-validated), Agent 2's sweep scaffold mechanics (20-cell grid
  execution, verified to actually run), and Agent 5's model-landscape computation method are all
  real, working pipeline components. They were exercised against placeholder numbers, which is a
  legitimate way to validate a pipeline — the failure was in claiming those numbers were
  something they weren't, not in using placeholder numbers per se.
- Agent 5's DESI z∈[4.0,4.4] population count (3,912 QSOs, 1,867 in [4.1,4.3]) is real data,
  independently queried fresh, unaffected by this correction.
- The epistemic boundary around real-data comparison (gated behind a future PREDICTION v2 pin)
  was correctly maintained throughout, independent of this grid issue.

## What does NOT survive

- Any claim that `K3_CRITERIA.md` defines, constrains, or freezes an (m,f) grid — false, strike
  it wherever seen.
- The specific values {0, 0.1, 0.5, 1, 5} meV / {0, 0.1, 0.5, 1.0} — not wrong per se, just
  unsourced. Treat as illustrative placeholders only until a real grid is defined.
- The "meV" unit label specifically — separately flagged by Agent 5 as physically implausible
  for this emulator's domain (which trains on log10(m_FDM/eV) ∈ [-23,-19], i.e. m22 units, not
  meV = 1e-3 eV) even before the K3_CRITERIA.md sourcing issue was found.

## Required before Phase 2 (Stats Design) proceeds

A real (m,f) grid — values AND units — needs to be defined and approved by T0, from actual
physics motivation (e.g. matching the emulator's own trained domain, matching what DESI can
plausibly constrain, or matching a specific FDM literature convention), not inherited from an
unverified assistant claim. This file exists so that claim never gets treated as ground truth
again.

**RESOLVED 2026-07-27 evening:** Xavier delegated grid-definition authority same session
("I give you authority to propose (m,f) grid value and unit"). The real grid is now defined in
`T0_MF_GRID_DEFINITION_2026_07_27.md` — log₁₀(m_FDM/eV) native units (no conversions anywhere),
8 × 7 = 56 cells, every value anchored to a re-verified primary source (param.pkl trained
support, mcmc.py F_EPS branch, arXiv:2606.06969 published bounds), with built-in null/CDM
control cells. Countermand window open per the [T0-DELEGATED] convention.
