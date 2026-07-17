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

### A-DE — Dark-Energy Identification

- **Status:** **T0-drafted** (2026-07-17, `PREDICTION.md` §6, "T0 architecture
  session"), submitted in direct response to `PREDICTION_REVIEW_T0.md` CF-2's
  requirement. Unlike A-SEQ/A-VOL/A-ONT/A-REL above (T1 best-inference
  reconstructions, still awaiting T0 authorship), this entry's text is already
  T0-authored — but it is **not yet Xavier-signed**, and ASSUMPTIONS.md does not
  reach v0.3 (the pin-blocking version named in `PREDICTION_REVIEW_T0.md` §4)
  until it is.
- **Statement:** We assume the stabilized vacuum of the selected compactification
  has positive energy density scaling as ρ_vac = a₃𝒱⁻³M_Pl⁴, with a₃ bounded per
  `PREDICTION_APPENDIX_A.md` §A.3 (not yet authored), and that this vacuum energy
  is the observed dark energy.
- **Tier:** C — the strongest assumption in the chain. Obtaining controlled
  positive-energy vacua is an open problem in string compactifications; this
  program does not solve it, it declares it.
- **Enters MVM at:** `PREDICTION.md` §2, the elimination step — ANSATZ-3 = A-DE
  is the load-bearing step that breaks the (𝒱, g_s) degeneracy using the
  *measured* ρ_DE, not the C3b geometric map (which only supplies |∂²V| at the
  C3b-selected vacuum point F(z*)). Any summary crediting C3b alone for the
  degeneracy-breaking violates the `epistemic-guardrails` skill (Finding F-B).
- **Discharge path:** an explicit stabilization computation for the selected
  candidate (positive-energy vacuum realized), or an explicit obstruction —
  either outcome is reportable, neither is assumed in advance.
- **Failure mode:** if a₃ cannot be bounded to a finite interval (Appendix A.3
  fails), this is kill condition **F5b** (`PREDICTION.md` §5); if the sign or
  identification with observed dark energy cannot be justified even given a
  bounded a₃, A-DE itself fails and the entire §2 elimination is undischarged —
  the model reverts to Tier C speculation with no observable-relation prediction
  (adjacent to F5).

### A-DBI — Baryonic Gravitational Coupling via DBI Action

- **Statement:** The local $z_{\text{brane}}$ field, which governs the scalar mediator $\phi$, does not exist in an isolated dark-sector vacuum. Because it arises from the D7-brane Dirac-Born-Infeld (DBI) action in F-theory, the modulus couples gravitationally to all localized energy densities within the halo, including the baryonic core mass ($M_b$). The radial field profile $z_{\text{brane}}(r)$ undergoes adiabatic contraction proportional to the measured baryonic mass fraction $f_b = M_b / M_{\text{halo}}$.
- **Tier:** C (EFT mapping assumption).
- **Enters MVM at:** Stream 3 pipeline translation. The theoretical core radius $r_c$ (where $F(z)$ saturates) is shifted dynamically by the depth of the baryonic gravitational well.
- **Discharge path:** Derivation of the full low-energy EFT from the D7-brane DBI action, confirming the $\mathcal{O}(G_N)$ coupling between the modulus and standard model baryons dominates the scalar potential near the core.
- **Failure mode:** If the DBI action isolates the modulus from baryonic density gradients, then the original purely-dark scaling ($\beta = 0.15$) holds, and the hypothesis remains mathematically falsified by SPARC data.

---

## CI / Audit Contract (once Phase 0 exits)

1. Every quantity in the Free-Parameter Ledger and every prediction in `PREDICTION.md` carries an explicit assumption-ID list (e.g., `m_φ [A-SEQ, A-VOL, A-ONT, A-REL, A-DBI]`).
2. `TUNING_LOG.md` records any change to an assumption's statement or an assumption-list tag after Phase 0 exit.
3. The S2-05 / S3-00-adjacent adversarial passes must explicitly attempt to break each assumption (see per-assumption "discharge path" above) before GATE M1.
4. No abstract or summary in any of the three repos may state a Tier C conclusion (this file) in Tier A/B language (`epistemic-guardrails` Finding F-A).

---

## Changelog

- **v0.1 (2026-07-17):** Initial draft. Best-inference reconstruction of A-SEQ, A-VOL, A-ONT, A-REL from context in `VISION.md` §1.2–1.3, `DUAL_SCALE_THREE_STREAM_PLAN.md` §5/§10, and `EXECUTION_PLAN.md` WP P0-A/S3-00. **Awaiting T0/Xavier review before Phase 0 can be marked complete.**
- **v0.1, +A-DE flag (2026-07-17):** Added a placeholder (not a drafted assumption) for **A-DE** per `PREDICTION_REVIEW_T0.md` CF-2 — a reviewed prediction draft's dark-energy identification step was undeclared and misattributed to C3b. Still v0.1: the flag records that A-DE is required before any such elimination can be pinned; it does not author A-DE's content (T0/T0s work).
- **v0.1, +A-DE T0 draft (2026-07-17):** Replaced the A-DE placeholder with the T0-authored text from `PREDICTION.md` §6 ("T0 architecture session," the v0.9-T0 proposal responding to `PREDICTION_REVIEW_T0.md`). A-DE is now T0-drafted but still unsigned; A-SEQ/A-VOL/A-ONT/A-REL remain T1 reconstructions awaiting T0 authorship. File stays v0.1 overall — v0.3 requires Xavier sign-off on all five entries, per the pin checklist.
- **v0.2 (2026-07-17):** Added A-DBI (Baryonic DBI Translation) to formally log the Option 2 EFT pivot strategy before mathematical testing.

`Generated-by: Claude Sonnet 5 (Claude Code session, inference from repo context) | Verified-by: none — no checker exists for physical-assumption content | Reviewed-by: T0 N`
