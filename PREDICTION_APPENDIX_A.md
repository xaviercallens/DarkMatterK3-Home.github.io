# PREDICTION_APPENDIX_A.md — Scaling-Law Derivations (NOT YET AUTHORED)

**Status:** ⚠️ **Placeholder only.** `PREDICTION.md` v0.9-T0 §2 requires this appendix
to bound a₁, a₂, a₃ (and the P2 amplitude convention, A.4) to finite intervals with
explicit N-dependence, before any of §2–§4's slots can be filled. This is a required
pin-blocking deliverable (`PREDICTION_REVIEW_T0.md` §4 checklist item "Derivation
appendix for scaling laws (1)–(3)").

**Why this file has no content yet:** deriving these bounds is a physical EFT
derivation — gauge kinetic function arguments, flux-potential curvature, LVS-style
volume scaling — squarely Tier C physics. Per `EXECUTION_PLAN.md` §1.2 (verifier-first
principle, no physics derivation below T0/T0s) and the same discipline already applied
to `ASSUMPTIONS.md`'s A-DE entry, this is T0/T0s-authored content, not something a T1
or T2 session should draft or approximate. Kill condition **F5b** (`PREDICTION.md` §5)
is the honest alternative to guessing: if an aᵢ cannot be bounded to a finite interval,
that is a reportable result, not a reason to relax the requirement.

## Required sections (per `PREDICTION.md` §2–§3 cross-references)

- **A.1 — ANSATZ-1 bound.** a₁ = a₁(N, b₀) ∈ ⟨bounded interval⟩: gauge kinetic
  function on the wrapped divisor + one-loop running, explicit N-dependence.
- **A.2 — ANSATZ-2 bound + R1 branch convention.** a₂ ∈ ⟨bounded interval⟩: flux-
  potential curvature along the sequence modulus from certified periods; and the
  physical-branch convention R1 (`PREDICTION.md` §1) needs fixing here.
- **A.3 — ANSATZ-3 = A-DE bound.** a₃ ∈ ⟨bounded interval⟩, feeding `ASSUMPTIONS.md`
  A-DE directly — this is the same bound A-DE's failure mode (Appendix A.3 failing)
  refers to.
- **A.4 — P2 amplitude convention.** Ψ_c formula derivation: fixed fraction of
  G·ρ_DM,local/m_φ², convention fixed before any comparison to PTA data.

## Definition of done

- Each of A.1–A.4 states its assumptions in, bounds its O(1) constants explicitly
  (with the argument for why they cannot move outside the stated interval), and shows
  its N-dependence (A.1) or periodicity/branch choice (A.2) work.
- Two-model rule (`EXECUTION_PLAN.md` §1.2.3): produced by one T0-class model,
  independently re-derived by the other; disagreement → `DERIVATION_DISPUTES.md`.
- Feeds `PREDICTION.md` §0 Provenance block and §4 Numbers table directly — no
  appendix section may be filled after its corresponding `PREDICTION.md` slot is
  computed (that would be exactly the "discretion re-spent at pin time" this
  document's design principle exists to prevent).

## Related Documents

- **PREDICTION.md** — the document whose §2–§4 slots this appendix discharges.
- **ASSUMPTIONS.md** — A-DE's failure mode is this appendix's A.3 section failing.
- **PREDICTION_REVIEW_T0.md** — §4 pin checklist, the source of this requirement.

---

`Generated-by: (none — placeholder) | Verified-by: none, no content to verify | Reviewed-by: T0 N`
