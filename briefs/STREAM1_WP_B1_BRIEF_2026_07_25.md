# Stream 1 Brief — WP-B1 Chameleon Mechanism (Lean 4)

**Date:** 2026-07-25  
**Authority:** Fable 5 (T0-delegated)  
**Executor:** Claude Haiku 4.5 (T2 mechanics); blockers escalate to Sonnet (T1)  
**Governing docs:** `VISION.md` §1.2–§1.3, `EXECUTION_PLAN.md` §3, `epistemic-guardrails` skill

---

## Context

The Dual-Scale pivot (2026-07-25) reframes the dark-sector physics to include chameleon screening as a bridge between global K3 vacuum and local elliptic halo EFT. This WP formalizes the chameleon mechanism in Lean 4 as **Tier A mathematics**: the screening potential and environment-dependent effective mass.

**Blocker resolved:** The scale-coherence gap (G-1, §3 below) is closed by instantiating chameleon field dynamics. This is infrastructure — not a physics proof, but a structural fact about screening EFTs.

---

## Work Package Scope

### What This WP Delivers

1. **Formalize the chameleon scalar field Φ** as a dependent type indexed by environment density ρ  
   - Signature: `def chameleon_field (ρ : ℝ≥0) : Scalar ℝ`
   - Properties: effective mass m_eff(ρ), coupling α_ch, screening radius r_S(ρ, m_eff)
   
2. **Prove screening condition:** m_eff(ρ) ≥ m_bare (always) and derive force range r_S as a function of ρ  
   - **Lemma:** In dense environments (ρ >> ρ_env), r_S ≲ meter scale; no Mpc-range force
   - Cite [astro-ph/0309411] (Jordan–Brans–Dicke screening review) + [1109.2709] (Khoury–Weltman cosmological chameleon)
   
3. **Bridge to B3 local EFT:** show how chameleon field couples to elliptic-curve brane stack  
   - No explicit coupling constant yet (that is S3-00 scope)
   - Just the structure: `def brane_coupling_site := chameleon_field.bulk_boundary_interaction`

4. **False-positive check:** demonstrate that naive screening *without* chameleon (pure K3 mediation) *cannot* produce Mpc-range force under any parameter choice  
   - This is the negative result that justifies introducing the mechanism

### What This WP Does NOT Do

- **No physics parameter derivation.** m_φ, α_D remain uncomputed (F5b stays in effect).
- **No observable prediction.** No κ-peaks, no PTA, no Lyman-α (G1-L closed).
- **No K3 geometry changes.** Stream 1 is unmodified; s7/s10 criteria stay frozen.

---

## Definition of Done

✅ **Lean 4 compiles** (zero `sorry`, zero new `axiom` unless listed in `Axioms/B1_Screening.lean`)  
✅ **Four lemmas proven:**  
  - `screening_always_triggers : ∀ ρ, m_eff ρ ≥ m_bare`
  - `force_range_bounded : ∀ ρ, r_S ρ ≤ C * (m_eff ρ)^(-1)` where C is a computable constant
  - `dense_env_short_range : ∀ ε > 0, ∃ ρ_crit, ∀ ρ > ρ_crit, r_S ρ < ε`
  - `no_unscreened_lmp : ¬(∃ params, K3_bulk_unscreened_force (r > Mpc))`  

✅ **Coupled to `SYM2_PARTNER` (B3 local EFT)** — interface compiles without error  
✅ **All citations in docstrings** — every lemma name + source in a `-- Source:` comment  
✅ **Provenance footer** in commit message: `Generated-by: Haiku | Verified-by: lake build | Reviewed-by: [pending]`

---

## Files to Create/Modify

| File | Action | Content |
|------|--------|---------|
| `Axioms/B1_Screening.lean` | Create | Chameleon field type, environment coupling, effective-mass axiomatization (if any formal axioms needed — prefer theorems) |
| `B1_Chameleon.lean` | Create | Four lemmas (see DoD); screening potential V_eff(Φ, ρ); screening radius formula |
| `Tests/B1_screening_golden.lean` | Create | Golden-test cases: known good (astro-ph/0309411 Table 1 values), known bad (unscreened-force attempt) |
| `.github/workflows/stream1_b1.yml` | Create | CI: `lake build`, test golden cases, check docstrings for citations |
| `briefs/STREAM1_WP_B1_RESULTS.md` | Create | Results table after completion (lemma verdicts, CI status, source list) |

---

## Validation Gate

**CI job:** `lake build --test` in the `B1_Chameleon` module → all proofs check → gate PASS  
**Manual gate:** Sonnet (T1) reviews the four lemmas against [astro-ph/0309411 §3–§4] and approves structure.  
**Escalation:** If proof of `force_range_bounded` stalls after 3 attempts, escalate to Sonnet for lemma redesign.

---

## Epistemic Tier Markers

- **Chameleon mechanism structure** [A] — established formalism (Jordan–Brans–Dicke screening)
- **Quantitative screening radius formula** [B] — conjectured but standard in cosmology; this WP formalizes the qualitative structure
- **Coupling to K3 dual-scale architecture** [C] — the hypothesis this project is testing; B1 just establishes that IF coupling occurs, screening works

---

## Next Handoffs

- **Stream 1 (S1-04, S1-05):** After B1 proof, incorporate `chameleon_field` as a formal object into the symmetric-square API (S1-04).
- **Stream 2 (S2-01):** No direct dependency; informational (screening justifies looking for candidate K3s with elliptic partners).
- **Stream 3 (if gate reopened):** B1 structures become input to S3-00 MVM derivation.

---

**Assigned to:** Haiku 4.5  
**Est. duration:** 20–40 hrs (proof search; 2–3 escalations expected)  
**Blocker escalation:** Sonnet (T1) on third failed proof attempt per lemma
