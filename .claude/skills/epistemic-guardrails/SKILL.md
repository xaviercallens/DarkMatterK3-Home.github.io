---
name: epistemic-guardrails
description: Enforce the VISION.md epistemic tier system in ALL written output. Use this skill whenever writing or editing any prose about the project — README files, reports, abstracts, docstrings, commit messages, paper drafts, talk notes, issue comments, or any sentence that describes what the model/mathematics does or shows. Also use when reviewing a PR. Trigger even for one-line descriptions: tier violations happen most in casual summaries.
---

# Epistemic Guardrails

This project's credibility rests on never overstating a claim. VISION.md §2 defines
three tiers; this skill makes the rules operational for every sentence you write.

## The three tiers (short form)

- **Tier A** — established/machine-certified mathematics. May be stated as fact.
- **Tier B** — checkable but unproven (per-candidate Sym², integrality beyond N, Swampland
  checks). Must carry a hedge + its verification route: "conjectured, tracked as criterion C3",
  "verified to order N₁ (evidence, not proof)".
- **Tier C** — physical interpretation (dark sector identification, brane realization,
  bulk/brane coupling). Must carry an explicit conjecture marker in the SAME sentence.

## Hard language rules

1. **Forbidden for Tier C claims** (unless prefixed by "we conjecture", "would", "if the
   matching exists"): *predicts, establishes, shows, implies, locks, governs, determines,
   demonstrates, proves*.
2. **The Sym² relation implies no physics.** Never write that the symmetric-square /
   Shioda-Inose structure "links", "locks", or "couples" the bulk to the brane EFT.
   The binding ruling is VISION §1.3: geometric relation ≠ physical coupling absent a
   worked EFT matching.
3. **`PASS(N)` notation.** Finite-order checks (mirror-map integrality to N terms) are
   always reported as `PASS(N)`, never bare `PASS`.
4. **`native_decide` and axioms.** Any Lean result whose proof uses `native_decide` or an
   axiom from `Axioms/` must say so when cited in prose ("kernel-checked modulo compiler
   trust" / "modulo axioms listed in AXIOMS.md"). It is not plain Tier A.
5. **No numbers from memory.** Every numeric constant or literature value in prose must
   trace to a checker certificate, a Lean `#eval`/test, or a cited file in `refs/`.
   If you cannot point to the source, do not write the number.

## Finding F-A — Abstracts may not outrun their own sections

Abstracts and summaries (README leads, paper abstracts, release-note
headlines, one-line PR descriptions) are reviewed **line-by-line against
the tier ledger of the section they summarize**. A claim may not appear in
an abstract at a stronger tier than the tier it carries in its own section.
Compressing "we conjecture X, and if a worked matching exists, would imply
Y" down to "X implies Y" for brevity is exactly the failure mode this
finding exists to block — casual summaries are where tier violations
concentrate.

CI enforcement (`scripts/check_tier_language.py`, wired into
`.github/workflows/epistemic-guardrails.yml`):
1. Grep every `## Abstract` / `## Summary` / `## Overview` section (and any
   text before the first heading) in all `*.md` files for the phrases
   `"Rigidly locks"`, `"Rigidity Theorem"`, `"zero continuous"` — these are
   flagged unconditionally, no exceptions.
2. Flag any sentence in those sections using a forbidden Tier-C verb
   (*predicts, establishes, shows, implies, locks, governs, determines,
   demonstrates, proves*) with no conjecture marker (*"we conjecture",
   "would", "if the matching exists"*) in the same sentence.
3. A clean run requires zero flags. Run locally with
   `python3 scripts/check_tier_language.py`.

## Finding F-B — Summary/conclusion lines must match the document's own derivation

Per `PREDICTION_REVIEW_T0.md` CF-3: a document's top-line conclusion (an
abstract, a §1 "the result is," a release-notes headline) must be checked
against what its *own* later sections actually derive — not only against
the tier ledger (Finding F-A covers that axis). A conclusion can be
tier-correct (properly hedged, correctly marked Tier C) and still be
**false relative to the document's own math**: e.g. "zero continuous free
parameters" in §1 when §2 derives one relation constraining one residual
continuous freedom. That is not a tier violation, it is an internal
contradiction, and it is the more dangerous failure because it reads as
honest. Before approving any summary line, re-derive (or at minimum
re-read) the section it summarizes and confirm the claimed conclusion is
the one that section actually supports — same document, not memory of a
prior draft.

## Required artifacts

- **Provenance footer** on every generated file:
  `Generated-by: <model/tier> | Verified-by: <verifier> | Reviewed-by: <T0 Y/N>`
- **Tier ruling requests**: if you are unsure of a claim's tier, do NOT guess — add an
  entry to `TIER_LEDGER.md` with status `RULING-REQUESTED` and flag it for the T0
  orchestrator session. Writing the cautious (lower-tier) phrasing in the meantime.
- **F6 discipline**: if you discover an error in a previously claimed Tier A/B result,
  the fix is not enough — add the disclosure note to the repo README in the same PR.

## Review checklist (run on any prose diff)

- [ ] Every Tier C sentence has a conjecture marker in the sentence itself.
- [ ] No forbidden verb applied to an unconstructed physical mechanism.
- [ ] Every number traceable; every `PASS` carries its order.
- [ ] Provenance footer present.
- [ ] Nothing in this diff weakens VISION §2/§4 (those may only be strengthened).
