# ASSUMPTIONS — Phase 0 Load-Bearing Assumptions for the Dual-Scale Model

**Status (v0.3-T0):** ⚠️ **AWAITING XAVIER SIGNATURE** ⚠️  
**T0 authorship:** Complete for A-SEQ, A-VOL, A-ONT, A-REL, A-DE (2026-07-18 revision by Fable 5 T0 session). A-DBI status clarified (see below).  
**Process:** T1 reconstruction (v0.1) reviewed and rewritten by T0; three-stream repos should mirror this file hash-pinned. Phase 0 exits when Xavier appends signature block below (§ Signature).

**Governance note:** Per `VISION.md` §2 and `epistemic-guardrails`, no Tier C claim is public until T0 authors it and Xavier countersigns. The assumptions register below is T0-authored; it now awaits Xavier's formal approval. A-DBI is marked as **CONDITIONAL** (see its entry below) because it emerges from S3-00 exploratory work, not from Phase 0 design — it will be formalized in Phase 1 adversarial passes if it survives initial testing.

**Repo of record:** `SocrateAI-Scientific-Agora-K3-DarkMatter`; mirrored (hash-pinned at freeze) in the other two repos, same as `K3_CRITERIA.md`.

---

## Purpose

The S3-00 MVM (Minimal Viable Matching) calculation derives observable quantities (m_φ, α_D, Λ_D, and the eliminated P1/P2 relations) from geometric data at a point (𝒱, g_s) in moduli space. That derivation is only as honest as the assumptions it silently relies on. This file makes those assumptions explicit, gives each one a tier, a way to check whether it's wrong (discharge path), and states what happens to the program if it fails (failure mode) — so a failure is a recorded result, not a quiet rationalization.

Every quantity in the Free-Parameter Ledger (`EXECUTION_PLAN.md` WP P0-B) and every prediction in `PREDICTION.md` must carry the assumption IDs it depends on.

---

## Assumption Register

Template per assumption: **Statement** · **Tier** · **Where it enters the MVM chain** · **Discharge path** (what would let us promote/confirm it) · **Failure mode** (what happens if it's false).

### A-SEQ — Single-Sequence Dominance (T0-authored v0.3)

- **Statement:** At the selected compactification point (specified by C3b-selected K3 + partner elliptic curve), no Kaluza-Klein excitation or additional complex-structure modulus below the M-fold effective-field-theory cutoff contributes to the low-energy 4D scalar potential or to the dark-matter self-interaction cross-section σ_DM(v). The truncation to the single modulus whose Picard-Fuchs sequence is the selected candidate is complete at the precision required for P1 (lensing, percent-level) and P2 (PTA, sub-percent), not an ansatz hiding an uncounted light mode.
- **Tier:** C (open conjecture in string compactifications; not decidable by algebraic sieve alone).
- **Enters MVM at:** S3-00 Step (2) — derivation of m_φ(𝒱, g_s) and Step (3) — α_D, Λ_D(𝒱, g_s) — assumes the period geometry's light-mode census is complete.
- **Discharge path:** An explicit KK spectrum / moduli mass matrix for the selected candidate's full compactification, computed or bounded, showing no additional mode in the mass windows [10⁻²⁵, 10⁻²⁰] eV (PTA) or [keV, MeV] (lensing mediator) below the theory's claimed cutoff.
- **Failure mode:** If an uncounted light field is found below the relevant threshold, any P1/P2 prediction is incomplete. The adversarial-pass protocol (EXECUTION_PLAN.md S2-05, S3 exploratory) is tasked with searching for one explicitly before M1. Discovery before pin blocks S3-00 until the field is either (a) incorporated into the observable chain with computed couplings, or (b) shown dynamically irrelevant by explicit RG/decoupling arguments.

### A-VOL — Volume-Modulus Stabilization and Stationarity (T0-authored v0.3)

- **Statement:** The Kähler modulus 𝒱 of the selected compactification is dynamically stabilized (by flux, non-perturbative effects, or both) at the point where the effective 4D potential has a local minimum. This minimum is maintained during the entire period from early structure formation to the present epoch (z ~ 1000 to z = 0). The time-averaged value and width of 𝒱's oscillation about this minimum do not perturb the velocity-dependent self-interaction cross-section σ_DM(v) by more than the P1 (lensing) / P2 (PTA) observables' discriminating power — i.e., the post-inflation 𝒱-trajectory does not modulate the coupling strength or scattering rates.
- **Tier:** C (stabilization and history are open problems in de Sitter/LVS constructions).
- **Enters MVM at:** S3-00 Steps (2)–(3) — m_φ(𝒱, g_s) and α_D, Λ_D(𝒱, g_s) are fixed-point evaluations, not integrated over 𝒱(t).
- **Discharge path:** (a) An explicit stabilization mechanism for 𝒱 in the selected candidate (flux + non-perturbative superpotential, or α'-corrections, or both), or (b) explicit RG/moduli-space arguments that σ_DM's matrix-element dependence on 𝒱 is O(ε) in the deviation |𝒱 − 𝒱_0| over the tested observational window.
- **Failure mode:** If 𝒱's post-inflationary history (reheating/oscillation epoch, structure-formation epoch) back-reacts detectably on σ_DM(v), the P1 and P2 predictions are not single-point evaluations but families parametrized by 𝒱-trajectory. This is pre-committed as an adversarial-pass target (EXECUTION_PLAN.md S2-05). If discovered, P1 demotes to FIT (normalization free); P2 may become NULL (the modulus history parametrizes away the PTA signature).

### A-ONT — Ontological Realization (Compactification Existence) (T0-authored v0.3)

- **Statement:** Each K3 candidate passing the C3/C3b algebraic criteria carries an associated F-theory compactification: a consistent family of Calabi-Yau 4-folds with the declared base (K3 × T²) and elliptic fiber, whose periods (at a chosen moduli point) are the candidate's Picard-Fuchs series. Tadpole and orientifold data for this compactification are consistent (net RR charge zero; negative-tension constraint satisfied or relaxed by string-loop physics). We compute as if this compactification is real, not a pure formal object.
- **Tier:** C (this is the "we do not claim a complete vacuum construction" gap from `VISION.md` §1.2; A-ONT is the honest name for that gap).
- **Enters MVM at:** S3-00 Step (1) — Free-Parameter Ledger installation classifies objects as GEOMETRIC (periods/Kodaira fibers) vs. ASSUMED, under the premise that "geometric" objects exist in a physical compactification.
- **Discharge path:** A worked flux/tadpole/orientifold data set for at least one C3b-passing candidate: (a) orientifold involution and choice of O7/O3 tadpole assignment, (b) quantized flux satisfying tadpole cancellation, (c) vacuum stabilization at the declared (𝒱, g_s) point. Long-horizon; out of scope for M1. Short of this, A-ONT remains an assumption and all downstream predictions inherit Tier C.
- **Failure mode:** **If no consistent compactification exists for any C3b-passing candidate,** the Dual-Scale physical program (Tier C) collapses into branch **F5** (`VISION.md` §4). The exact-algebraic content (K3-order classification, Picard-Fuchs recurrences, Tier A/B) still publishes independently. This is a recorded, honest result, not a failure of the project's ambition.

### A-REL — Moduli Unification (Dual-Scale Coupling) (T0-authored v0.3)

- **Statement:** The bulk scalar potential V_flux(𝒱, g_s, z_bulk) and the local brane-localized potential V_brane(z_brane; 𝒱, g_s) share the same coordinate system (𝒱, g_s) and the same stabilization logic. The modulus z_bulk governing the K3 complex-structure (and hence m_φ via the period) and the modulus z_brane governing the dark-matter self-interaction (via DBI action coupling) are not independent — they are coordinates on the same string compactification's moduli space. Eliminating 𝒱 and g_s between the two potentials produces an invariant relation, binding P1 (lensing) to P2 (PTA), not an accidental algebra artifact.
- **Tier:** C. This is the formal statement of `VISION.md` §1.3's warning: "Sym² arithmetic alone does not imply physical coupling." A-REL is that coupling hypothesis.
- **Enters MVM at:** S3-00 Step (3) — the moduli elimination — which only makes sense if K3 base and elliptic fiber share (𝒱, g_s).
- **Discharge path:** The worked EFT matching (S3-00 itself). If S3-00 is completed and both T0 and T0s independently solve for the (m_φ, m_DM) relation from geometric data + period integrals alone (inputs only, no cross-checking), and both derive the same relation to within stated tolerance, that is *evidence* (not proof, not certainty) that the two sectors are genuinely coupled at this point in moduli space.
- **Failure mode:** Pre-committed branch **F5** (`VISION.md` §4 and `EXECUTION_PLAN.md` S3-00 step 4): if S3-00 produces no surviving relation (both (𝒱, g_s) decouple from observable prediction, or all vacuum points fail), the model is observationally degenerate with generic vdSIDM. Model is falsified; documented in `NO_PREDICTION_BRANCH.md`; no post-hoc tuning of moduli ansätze. Mathematics still publishes.

### A-DE — Dark-Energy Identification (T0-authored v0.3)

- **Statement:** The stabilized vacuum of the selected compactification has an effective 4D cosmological constant (vacuum energy density) with three properties: (i) positive sign, (ii) energy density scaling as ρ_vac = a₃ 𝒱^{−3} M_Pl^4 for a bounded coefficient a₃ ∈ [a₃^{min}, a₃^{max}] computed from the compactification data (flux superpotential, Kähler moduli, O-plane contributions), (iii) the measured dark-energy density ρ_DE ~ 10^{−47} GeV^4 is identified with this vacuum energy. None of these properties is constructed; each is an open conjecture in string compactifications.
- **Tier:** C — the strongest and most speculative of the five assumptions. Realizing controlled de Sitter vacua in string theory is an active research problem with no consensus solution.
- **Enters MVM at:** `PREDICTION.md` §2 (Ansatz-3), the moduli elimination step. The measured ρ_DE is the only handle to solve for 𝒱(ρ_DE); without A-DE's scaling law, the system has a continuous degeneracy (𝒱, g_s) constrained by zero relations, and no prediction is possible. **A-DE is the load-bearing assumption that breaks the degeneracy; C3b contributes only the second derivative |∂²V(F(z*))|** at the selected vacuum point. Misattributing the degeneracy-breaking to C3b alone (a Tier A/B object) is an epistemic-tier violation (Finding F-B of `epistemic-guardrails`).
- **Discharge path:** An explicit computation for the selected candidate showing: (a) how the stabilized value of 𝒱 is determined (which fluxes, which non-perturbative superpotential terms, which α'-corrections), (b) the sign of ρ_vac at that point, (c) the interval [a₃^{min}, a₃^{max}] with explicit O(1)-coefficient bounds. Realizing this is a long-horizon goal (Phase 2+ work). Obstruction theorems (no de Sitter in that family) are equally reportable and frame the falsification branch F5b.
- **Failure mode:** (i) **F5b trigger:** if Appendix A.3 cannot bound a₃ to a finite interval (derivation fails), no elimination is possible and S3-00 outputs NULL-BY-LOGIC (equivalent to no prediction). (ii) **A-DE failure:** if the vacuum energy is negative or zero, the model has no room to identify with dark energy; A-REL's elimination may still produce a relation, but it is one among vdSIDM parameters, unanchored to observation — a different branch (related to F5c: degenerate model). (iii) **Failure of identification:** if a₃ is bounded but the resulting ρ_vac lands far from the measured ρ_DE (by many orders of magnitude), the identification is in tension and documented as an assumption-related constraint or exclusion, not discarded post-hoc.

### A-DBI — Baryonic Modulus Coupling via D7 DBI Action (CONDITIONAL, v0.3)

- **Status (v0.3):** **CONDITIONAL** — not part of Phase 0 design; emerges as a possible mechanism during S3-00 adversarial testing if lensing data suggests baryonic-coupling signature. Formalized here to allow pre-registration if S3 exploratory work indicates it is relevant.

- **Statement (if triggered):** The brane-localized field z_brane (modulus of the elliptic fiber, coupling to the dark mediator φ) does not decouple from localized energy within a halo. Its origin in the D7-brane Dirac-Born-Infeld (DBI) action couples it gravitationally (∼ G_N strength) to all baryonic and dark-matter mass distributions. A halo with baryonic core mass M_b undergoes adiabatic contraction: the brane-field profile z_brane(r) follows the baryonic potential, and the effective core radius r_c (where F(z_brane) saturates) shifts by Δr_c ∝ G_N M_b / R_halo^2 relative to a purely-dark prediction.
- **Tier:** C (if A-DBI is invoked; conditional Tier C).
- **Enters Stream 3 at:** WP-C2 onward (mock-null-bank, real-data comparisons) only if data-driven exploration of the lensing observable suggests a baryonic-core signal. Phase 0 does not assume it.
- **Discharge path:** (i) Explicit low-energy EFT derivation from D7-brane DBI action, showing the O(G_N) coupling to baryonic stress-energy at the modulus lagrangian level. (ii) Monte-Carlo halo-model runs with A-DBI's baryonic contraction law, comparing predicted core-radius scaling (β) against SPARC dwarf data and published stacked lensing with explicit baryonic-mass subgroups.
- **Failure mode:** If DBI action's modulus couples weakly or decouples from baryonic density, the core-radius scaling is purely-dark (β ≈ 0.15 ∓ 0.02); published SPARC data excludes this at ≥3σ, triggering branch **F3**. A-DBI is then ruled out; predictions revert to standard vdSIDM. **Alternatively, if A-DBI signal survives:** the purely-dark ansatz (no A-DBI) is excluded, and the result is a novel dark-sector discovery, documented in `OBSERVATIONAL_REPORT.md`.

---

## CI / Audit Contract (Phase 0 exit conditions)

**Enforcement:** Once Xavier signs this file, the following rules activate:

1. **Assumption tagging:** Every quantity in the Free-Parameter Ledger (`PREDICTION.md` §1) and every prediction (P1, P2) carries an explicit assumption-ID list in brackets (e.g., `m_φ [A-SEQ, A-VOL, A-ONT, A-REL, A-DE]`). A-DBI tagged only if triggered by data exploration.
2. **Change tracking:** `TUNING_LOG.md` records any edit to an assumption's statement, tier, or discharge path after Phase 0 exit. Changes are dated, committed, and justified — no silent revisions.
3. **Adversarial protocol:** S2-05 (K3 selection review) and S3 exploratory phases (WP-C2 onward) are tasked with attempting to falsify each assumption per its stated discharge path before GATE M1. Discovery of a discharge trigger is a *recorded result*, not grounds for assumption revision.
4. **Tier language audit:** CI rule (`epistemic-guardrails` Finding F-A): no abstract, summary, or conclusion in any of the three repos states a Tier C claim in Tier A/B language. Automated grep checks for violations (keywords: "rigorously," "proven," "mathematical," "establishes," "demonstrates") near abstract blocks; manual review of flagged lines.
5. **Documentation:** TUNING_LOG demotion rule — any post-pin change to assumption tags or statement automatically demotes all affected comparisons from TEST to FIT, recorded in the log entry itself. This is mechanical, not optional.

---

## Changelog

- **v0.1 (2026-07-17):** T1 reconstruction of A-SEQ, A-VOL, A-ONT, A-REL from context clues in `VISION.md`, `EXECUTION_PLAN.md`, and S3-00 spec. Awaiting T0 authorship.
- **v0.1→v0.2 (2026-07-17):** Added placeholder for A-DE per `PREDICTION_REVIEW_T0.md` CF-2 (undeclared dark-energy assumption). Added A-DBI (conditional, for lensing-exploration trigger).
- **v0.2→v0.3-T0 (2026-07-18):** **T0 authorship pass.** Rewrote A-SEQ, A-VOL, A-ONT, A-REL with explicit statements, discharge paths, failure modes, tier attribution. A-DE adopted from PREDICTION.md §6 (T0-authored, 2026-07-17). A-DBI marked CONDITIONAL (Phase 0 does not assume it; emerges if lensing data suggests baryonic coupling). File now ready for Phase 0 exit contingent on Xavier signature (below).

`Generated-by: T0 (Fable 5, 2026-07-18 revision session) | Verified-by: cross-reference to VISION.md §1.3, EXECUTION_PLAN.md S3-00, K3_CRITERIA.md | Reviewed-by: T0 (pending Xavier counter-signature)`

---

## Signature Block (Phase 0 Gate)

**TO UNLOCK G0 (Phase 0 exit):** Xavier appends signature below. Once signed, this file's version increments to v0.3-signed, it is mirrored into the two partner repos (K3-DarkMatter, LeanProposal) hash-pinned, and GATE G0 closes.

```
[ ] Xavier signature (date, initials)
[ ] Reviewed: all five assumptions (A-SEQ, A-VOL, A-ONT, A-REL, A-DE) 
    state load-bearing Tier C claims? YES / NO / REVISE
[ ] Conditional A-DBI appropriate for Phase 0? YES / REMOVE / REVISE
[ ] Assumption-tagging audit contract (CI section) sound? YES / MODIFY
[ ] Ready to commit hash-pinned into all three repos? YES / HOLD
```

**Xavier's review checklist (before signing):**
- [ ] Does A-SEQ correctly describe the single-modulus truncation risk?
- [ ] Does A-VOL correctly state the volume stabilization/back-reaction risk?
- [ ] Does A-ONT honestly declare the compactification-existence gap?
- [ ] Does A-REL correctly formalize the dual-scale coupling hypothesis?
- [ ] Does A-DE correctly attribute the (𝒱, g_s) degeneracy-breaking to the dark-energy scaling, not to C3b alone?
- [ ] Is A-DBI's conditional status acceptable, or should it be removed from Phase 0?
- [ ] Are the discharge paths realistic and testable?
- [ ] Are the failure modes pre-committed clearly (no wiggle room for post-hoc rationalization)?

*Once signed, the file is frozen per `TUNING_LOG.md` rules: any post-pin change is a tuning event, logged and demoting affected comparisons to FIT.*
