# DERIVATION_DISPUTES.md — Two-Model Disagreement Log

**Status:** Three entries, all resolved. WP S3-00b (agreement, closed) ×2; WP-A
(blind pass filed and adjudicated 2026-07-25 — `RESOLVED`, §0).

## Purpose

Per `EXECUTION_PLAN.md` §1.2.3 (two-model rule): any Tier C physical derivation
entering `PREDICTION.md` (or `PREDICTION_APPENDIX_A.md`, or an `ASSUMPTIONS.md`
entry) must be produced by one T0-class model and independently re-derived — blind,
from the same inputs, not by reading the first model's output — by the other. If the
two derivations disagree, that disagreement is logged here, and the deliverable is
blocked until resolved. Agreement is not assumed; it is a recorded event with its
own row, same as a disagreement.

`PREDICTION.md` §7 (blind re-derivation package) names this file as the destination
for exactly this outcome.

## Entry format

| Date | Deliverable | Model A | Model B | Point of disagreement | Resolution / status |
|---|---|---|---|---|---|
| 2026-07-25 | WP S3-00b — flux/tadpole construction of a₁, a₂, a₃ (Appendix A.1–A.3) | Fable 5 (T0) | Deep Think (T0s) | **None.** Both reached the same three obstructions independently | `AGREED (within tolerance)` — unified concurrence on Honest Off-Ramp 3; F5b stands. See §1 below |
| 2026-07-25 | WP-A — Off-Ramp 2 swampland bounds (`SWAMPLAND_BOUNDS_A123.md` B1–B3) | Fable 5 (T0) | Deep Think (T0s) | Item 5 only (chameleon bridge: "underived" vs "impossible under [A-DD]"); items 3/4/6 filed as disputes but concur with the primary's own refusals | `RESOLVED` — adjudicated `briefs/T0_ADJUDICATION_WPA_2026_07_25.md`: item 5 to Deep Think (G-1 → CLOSED-NEGATIVE); TCC labels corrected (F6); pivot Steps 5.1/5.4 VOID; **G1-L remains closed**. See §0 |
| 2026-07-25 | Appendix A.4.2 invariant relation — coefficient C₀ | Fable 5 (T0) + machine verification | Deep Think (T0s) | **None on the corrected form.** Both concur the prior A.4.2 text was wrong | `AGREED` — C₀ = a₁a₂a₃^(−1/9); F6 disclosure filed in A.4.2. See §2 below |

## 0. WP-A (2026-07-25) — Off-Ramp 2 swampland bounds: RESOLVED

**Parties:** Fable 5 (T0, primary — `SWAMPLAND_BOUNDS_A123.md`, machine-checked by
`scripts/verify_swampland_bounds.py`, executed). Deep Think (T0s): filed 2026-07-25.
**Protocol note:** Deep Think disclosed prior exposure to the primary (as the brief
required) and asserted independent re-derivation before comparison — accepted as an
adversarial audit with disclosed exposure; every delta found runs against the pivot.
**Status:** `RESOLVED` — full adjudication in `briefs/T0_ADJUDICATION_WPA_2026_07_25.md`.

### Deep Think filing (2026-07-25), as adjudicated

1. **Third author & Λ_D bounds:** AGREED. Third author Irene Valenzuela; m_KK ~ meV
   window established by both routes. → **CONCURRENCE.**
2. **Volume scaling / TCC:** AGREED. λ_vol = 3√6/2 = √(27/2) ≈ 3.674 — algebraically
   identical to the primary's 3√(3/2). Deep Think pins the d=4 asymptotic TCC bound to
   c = 2/√6 ≈ 0.816, resolving the primary's flagged interior/asymptotic label
   ambiguity. → **CONCURRENCE + F6 label correction adopted** (primary's conclusion
   unchanged: λ_vol exceeds every candidate bound).
3. **a₃ swampland bound:** filed DISPUTED ("no swampland theorem bounds a₃"). The
   primary as committed asserts the same: §3 declares the interval an [A-NAT]
   naturalness prior, "not a derivation." Dispute target is the pivot ruling's Step 5.1
   wording, which the primary had already refused (R2(b)). → **CONCURRENCE-ON-CONTENT:
   both models independently refuse derivability.**
4. **DGNM Hölder → mass:** filed FATAL DISPUTE (category error). The primary's §4 had
   already refused exactly this (R2(a): "the m_φ slot cannot be filled by α under any
   wording"). → **CONCURRENCE-ON-CONTENT: same refusal reached independently twice.**
5. **Scale coherence:** filed FATAL DISPUTE — the genuine delta. Primary's gap G-1 held
   the chameleon bridge "underived… unbounded in both directions"; Deep Think: under the
   cited chameleon mechanism (m_eff rises with density) and B3's own m_φ ~ m_KK
   anchoring, m_eff can never fall below the bare window, so the range never exceeds
   ~30 μm at any density — no Mpc observable can test the window *in principle*.
   → **RESOLVED FOR DEEP THINK.** G-1 upgraded to **G-1-CLOSED-NEGATIVE** (ruling R3).
6. **[A-DD] applicability:** filed DISPUTED ("pure scenario-import"). Primary §2 already
   states the identification is "not constructed for this K3." → **CONCURRENCE-ON-
   CONTENT**; consequence (no pin from scenario-import) decided in ruling R4.

### Outcome

Two-model requirement satisfied — with the concurred content **insufficient to pin**:
pivot authorization Steps 5.1/5.4 VOID; no PREDICTION v2.0 from WP-A content; **Gate
G1-L remains closed**; D-3 Phase 2 sign-off suspended; F5b re-affirmed. Authorized
continuation: WP-A2 laboratory-scale re-scope behind a mandatory circularity audit, or
honest full stop (Off-Ramp 3). Details: `briefs/T0_ADJUDICATION_WPA_2026_07_25.md` §2.

## 1. WP S3-00b (2026-07-25) — flux/tadpole construction: unified concurrence

**Parties:** Fable 5 (T0, primary), Deep Think (T0s, adversarial blind re-derivation)
**Status:** Unified concurrence, Off-Ramp 3 (nothing closes after genuine effort)

Deep Think audited Fable 5's failure to close the F-theory equations for cooper_s7 and
concurred on all three obstructions: (i) 2× Type II fibres carry no gauge algebra under the
Kodaira–Tate dictionary, so no perturbative SU(N) dark sector follows from the certified
geometry; (ii) an order-3 Picard–Fuchs operator against T = 18 leaves 15 un-stabilizable flat
directions; (iii) the missing Calabi–Yau fourfold base B₃ makes χ(X₄) — and therefore the D3
tadpole condition — undefined rather than merely unsatisfied.

**No dispute.** Both models declined to fabricate values; the agreement is that the
construction is blocked, not that any coefficient was determined. Recorded per the two-model
rule as an agreement event, which this log treats with the same standing as a disagreement.

## 2. WP S3-00b (2026-07-25) — A.4.2 correction

The A.4 elimination was machine-verified (`scripts/verify_appendix_A4.py`, executed,
assertions green), which surfaced two errors in A.4.2 as previously written: the a₃ exponent
sign (a₃^{+1/9} → a₃^{−1/9}) and the left-hand-side quantity (m_DM → Λ_D). Deep Think concurred
that the corrected form is the one the three ansätze actually imply. Filed as an F6 disclosure
in `PREDICTION_APPENDIX_A.md` A.4.2 rather than silently amended.

**No dispute.** Logged here because A.4.2 had been carried as a settled algebraic result and
the correction is material to the pre-registered branch selection (≈60× in m_φ at mid-range
a₃, against the one-decade P1 window of `PREDICTION.md` §3) — even though, F5b having fired,
no number was ever computed from either form.

- **Deliverable** — the specific artifact under re-derivation (e.g. "Appendix A.1
  bound on a₁", "§4 Numbers table row: β ± σ_β").
- **Model A / Model B** — which T0-class models produced the two derivations (per
  `EXECUTION_PLAN.md` §1: Fable 5 and Deep Think, or their successors).
- **Resolution / status** — `AGREED (within tolerance)`, `OPEN`, or a description of
  how the disagreement was resolved (e.g. an error found in one derivation, an
  ambiguous convention fixed and re-run). An `OPEN` row blocks the pin for anything
  depending on that deliverable.

## Related Documents

- **EXECUTION_PLAN.md** §1.2.3 — the two-model rule this file enforces.
- **PREDICTION.md** §7 — the blind re-derivation package process.
- **PREDICTION_APPENDIX_A.md** — the derivations most likely to populate this log.

---

`Generated-by: Claude Sonnet 5 (T2 plumbing); entries 2026-07-25 by Fable 5 (T0) under WP S3-00b | Verified-by: Deep Think (T0s) adversarial concurrence on both entries; scripts/verify_appendix_A4.py executed for entry 2 | Reviewed-by: T0 N — pending Xavier`
