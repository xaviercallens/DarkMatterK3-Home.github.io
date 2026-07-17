# ASSUMPTIONS — Phase 0 Load-Bearing Assumptions for the Dual-Scale Model

**Status:** ⚠️ **DRAFT v0.1 — UNVERIFIED — NOT YET T0-AUTHORED OR SIGNED OFF** ⚠️

**Provenance note:** The names A-SEQ, A-VOL, A-ONT, A-REL originate in `DUAL_SCALE_THREE_STREAM_PLAN.md` §5/§10 and `EXECUTION_PLAN.md` WP P0-A ("Phase 0 ASSUMPTIONS v0.2"), which reference this file but predate it. No source draft for their content exists in either repository at time of writing. The statements below are a **best-inference reconstruction from context clues already present in `VISION.md` §1.2–1.3 and the S3-00 MVM spec** — they are explicitly *not* an authoritative Tier C ruling. Per this project's own `epistemic-guardrails` rule, no Tier C claim may be asserted without T0 authorship. **Xavier: every entry below needs your review, correction, or replacement before Phase 0 can exit.**

**Repo of record:** `SocrateAI-Scientific-Agora-K3-DarkMatter`; mirrored (hash-pinned at freeze) in the other two repos, same as `K3_CRITERIA.md`.

---

## Purpose

The S3-00 MVM (Minimal Viable Matching) calculation derives observable quantities (m_φ, α_D, Λ_D, and the eliminated P1/P2 relations) from geometric data at a point (𝒱, g_s) in moduli space. That derivation is only as honest as the assumptions it silently relies on. This file makes those assumptions explicit, gives each one a tier, a way to check whether it's wrong (discharge path), and states what happens to the program if it fails (failure mode) — so a failure is a recorded result, not a quiet rationalization.

Every quantity in the Free-Parameter Ledger (`EXECUTION_PLAN.md` WP P0-B) and every prediction in `PREDICTION.md` must carry the assumption IDs it depends on.

---

## Assumption Register

Template per assumption: **Statement** · **Tier** · **Where it enters the MVM chain** · **Discharge path** (what would let us promote/confirm it) · **Failure mode** (what happens if it's false).

### A-SEQ — Single-Sequence Dominance

- **Statement (DRAFT):** No light degree of freedom other than the modulus associated with the selected candidate's own Picard-Fuchs sequence contributes to the low-energy 4D EFT at the scales relevant to m_φ and the P1/P2 observables. I.e., the truncation to one modulus (the C3/C3b-selected candidate's) is complete, not an approximation hiding an uncounted light field.
- **Tier:** C (physical conjecture; not checkable by the exact-algebraic sieve alone).
- **Enters MVM at:** Step (2), derivation of m_φ(𝒱, g_s) from period data — assumes the period geometry fully determines the light spectrum.
- **Discharge path:** Would require an explicit KK/moduli spectrum computation for the selected candidate's full compactification (not just the K3 factor) showing no additional mode below the relevant mass scale. Not attempted before M1; recorded as an open assumption.
- **Failure mode:** **A-SEQ failure ⇒ an uncounted light field exists.** Any P1/P2 prediction derived without it is incomplete; the adversarial pass (S2-05 / DUAL_SCALE_THREE_STREAM_PLAN.md §10 R6) is explicitly tasked with trying to find one. If found before M1, S3-00 is blocked until the field is either incorporated or shown irrelevant.

### A-VOL — Volume-Modulus Stability Over Cosmological History

- **Statement (DRAFT):** The volume modulus 𝒱 sits at (or close enough to) the stabilization point used to evaluate m_φ, α_D, Λ_D across the cosmological history relevant to today's observables (structure formation through present-day halos). Its production/relaxation history does not back-react on the velocity-dependence of the dark-matter self-interaction cross-section σ(v) used in the P2 (lensing) observable.
- **Tier:** C.
- **Enters MVM at:** Steps (2)–(3) — m_φ(𝒱, g_s) and α_D, Λ_D(𝒱, g_s) are evaluated at a fixed point, not integrated over a modulus trajectory.
- **Discharge path:** Requires either (a) an explicit stabilization mechanism for 𝒱 (flux/non-perturbative — not yet exhibited, per VISION §1.2 "no explicit flux stabilization"), or (b) an argument that σ(v)'s velocity-dependence is insensitive to plausible 𝒱-histories within the tested range.
- **Failure mode:** If 𝒱's history back-reacts materially on σ(v), the P2 lensing prediction is not a fixed prediction but a family; DUAL_SCALE_THREE_STREAM_PLAN.md §10 R6 flags this explicitly as an adversarial-pass target ("find a production history that back-reacts on σ(v)"). Failure demotes P2 from TEST to a conditional/FIT-labeled statement, or removes it as a candidate observable.

### A-ONT — Ontological Identification of the Selected Candidate with a Physical Compactification

- **Statement (DRAFT):** The K3 candidate selected by the exact-algebraic sieve (Tier A/B, `K3_CRITERIA.md`) is treated as if it corresponds to an actual, consistent string compactification geometry (flux/orientifold/tadpole data exhibited or exhibitable), not merely as an abstract sequence/operator satisfying checkable arithmetic properties.
- **Tier:** C (this is precisely the gap the README already flags: "we do not claim a complete vacuum construction").
- **Enters MVM at:** Step (1), Free-Parameter Ledger installation — the ledger classifies quantities as GEOMETRIC/CONTINUOUS-FREE/DISCRETE/ASSUMED under the premise that "geometric" quantities are physically real, not merely formally computable.
- **Discharge path:** A worked flux/orientifold construction for at least one C3b-passing candidate (long-horizon; explicitly out of scope for M1 per VISION §1.2 "unconstructed"). Short of that, A-ONT stays an assumption and every downstream number inherits its Tier C ceiling.
- **Failure mode:** If no consistent full compactification exists for any surviving candidate, the entire physical program (Tier C) collapses to F5 (`VISION.md` §4) — the mathematics (Tier A/B) still stands and publishes independently.

### A-REL — Global–Local Sector Relation (the Dual-Scale Coupling Itself)

- **Statement (DRAFT):** The global K3 (bulk vacuum) sector and the local elliptic-curve (brane-localized dark-matter EFT) sector share the same underlying moduli (𝒱, g_s), such that eliminating (𝒱, g_s) between the independently-derived m_φ(𝒱,g_s) and α_D, Λ_D(𝒱,g_s) relations produces a genuine, physically-meaningful parameter-free relation between P1 and P2 — not an artifact of forcing two unrelated sectors onto a shared coordinate.
- **Tier:** C. This is the formal restatement of VISION.md §1.3's central ruling: "It does not, by itself, imply any physical coupling... between a bulk vacuum and a brane EFT."
- **Enters MVM at:** Step (3), the elimination step — this is the step that only makes sense if A-REL holds.
- **Discharge path:** The worked EFT matching itself (VISION §1.3's Phase 1 blocker) *is* the discharge path — if S3-00 completes and both T0 and T0s independently re-derive the same eliminated relation from geometric data alone (not from each other), that is evidence (not proof) for A-REL at the specific candidate point tested.
- **Failure mode:** **This is the kill condition already pre-committed in `EXECUTION_PLAN.md` WP S3-00 step (4):** if no relation survives the (𝒱, g_s) elimination, the model is generic vdSIDM and triggers **F5** — a reportable, non-post-hoc result, not a silent abandonment.

### A-DE — Dark-Energy Identification (REQUIRED, NOT YET AUTHORED)

- **Status:** ⚠️ **Flagged, not drafted.** Per `PREDICTION_REVIEW_T0.md` CF-2: a
  reviewed prediction-draft's elimination of the volume modulus 𝒱 silently relied
  on (i) ρ_vac ∝ 𝒱⁻³, (ii) that vacuum energy being positive, and (iii) its
  identification with the *measured* dark energy density — i.e. the string-theory
  de Sitter/uplift problem, smuggled in as an unnumbered proportionality and
  credited to the (unrelated) C3b geometric criterion instead. This is a
  first-order Tier C physical assumption and it is the actual load-bearing step
  in that elimination, not C3b.
- **What this entry is not:** this is a placeholder, not the assumption. Drafting
  A-DE's statement/tier/discharge-path/failure-mode (matching the template used
  by A-SEQ/A-VOL/A-ONT/A-REL above) is T0/T0s content, same as the other four —
  a T1 session should not author Tier C physical assumptions any more than it
  should author the elimination itself. See `PREDICTION_REVIEW_T0.md` §4 pin
  checklist item "ASSUMPTIONS v0.3 with A-DE."
- **Blocks:** any future PREDICTION.md draft that eliminates (𝒱, g_s) via a
  measured-ρ_DE identification must carry this assumption once authored; until
  then such an elimination is undischarged per the same review.

---

## CI / Audit Contract (once Phase 0 exits)

1. Every quantity in the Free-Parameter Ledger and every prediction in `PREDICTION.md` carries an explicit assumption-ID list (e.g., `m_φ [A-SEQ, A-VOL, A-ONT, A-REL]`).
2. `TUNING_LOG.md` records any change to an assumption's statement or an assumption-list tag after Phase 0 exit.
3. The S2-05 / S3-00-adjacent adversarial passes must explicitly attempt to break each assumption (see per-assumption "discharge path" above) before GATE M1.
4. No abstract or summary in any of the three repos may state a Tier C conclusion (this file) in Tier A/B language (`epistemic-guardrails` Finding F-A).

---

## Changelog

- **v0.1 (2026-07-17):** Initial draft. Best-inference reconstruction of A-SEQ, A-VOL, A-ONT, A-REL from context in `VISION.md` §1.2–1.3, `DUAL_SCALE_THREE_STREAM_PLAN.md` §5/§10, and `EXECUTION_PLAN.md` WP P0-A/S3-00. **Awaiting T0/Xavier review before Phase 0 can be marked complete.**
- **v0.1, +A-DE flag (2026-07-17):** Added a placeholder (not a drafted assumption) for **A-DE** per `PREDICTION_REVIEW_T0.md` CF-2 — a reviewed prediction draft's dark-energy identification step was undeclared and misattributed to C3b. Still v0.1: the flag records that A-DE is required before any such elimination can be pinned; it does not author A-DE's content (T0/T0s work).

---

`Generated-by: Claude Sonnet 5 (Claude Code session, inference from repo context) | Verified-by: none — no checker exists for physical-assumption content | Reviewed-by: T0 N`
