# PREDICTION.md — T0 Proposal (v0.9-T0)

**Status: DRAFT — PIN BLOCKED ON:** (i) refs/ transcription merged, (ii) C3b certificate
PASS(N≥50) for the named pair, (iii) Appendix A derivations complete, (iv) ASSUMPTIONS
v0.3 (A-DE), (v) blind re-derivation agreement, (vi) Xavier signature.
**Design principle:** this document is *compilable*. Every number is a slot ⟨…⟩ bound to
a formula, an input provenance (certificate field or measured public value in refs/), and
an error-budget procedure — all fixed NOW, before any number exists, so that computing the
numbers later involves zero discretionary choices. Discretion spent today cannot be
re-spent at pin time.

> **Epistemic notice.** Mathematical inputs (C3/C3b certificates) are Tier A/B. The
> translation to 4D observables is Tier C, conditional on [A-SEQ, A-VOL, A-ONT, A-REL,
> A-DE]. One relation among observables survives parameter elimination; the model retains
> one residual continuous freedom (§2). If the pre-registered tests fail, the physical
> hypothesis is dead per the kill switches of §5.

**Scope:** Applies to Stream 3 observational testing (`SocrateAI-Scientific-Agora-Home`).
**Provenance:** Supersedes the Desk draft v1.0 rejected in `PREDICTION_REVIEW_T0.md`
(2026-07-17) and the earlier three-observable outline (§6 Changelog, below). This is
T0-authored content, submitted in response to that review — see the changelog vs. Desk
draft v1.0 at the end of this document for exactly what changed and why. **None of the
six pin-blocking conditions above are satisfied yet** — no certificate exists (`checkers/`
is not implemented), no `refs/` manifest exists, Appendix A is not written, ASSUMPTIONS.md
does not yet carry a T0-authored, Xavier-signed A-DE, no blind re-derivation has run, and
there is no Xavier signature. **Gate G1/M1 remain closed; nothing below is pinned.**

---

## 0. Provenance block (filled at pin; empty fields block the pin)

| Field | Value |
|---|---|
| Candidate pair (bulk, brane) | ⟨from K3_SELECTION_REPORT⟩ |
| C3b certificate file + determinism hash | ⟨…⟩ |
| C1, C2 certificates + hashes | ⟨…⟩ |
| refs/ manifest hashes (Cooper 2012; AESZ tables; measured-values file) | ⟨…⟩ |
| ASSUMPTIONS version | v0.3 (must include A-DE) |
| Blind re-derivation record | ⟨file + agreement statement⟩ |
| Pin commit | ⟨sha⟩ — verified to precede all data-touching commits |

---

## 1. Free-Parameter Ledger (corrected conclusion)

| Quantity | Class | Status |
|---|---|---|
| z_brane | GEOMETRIC | dynamical mediator field φ |
| z_bulk | GEOMETRIC | eliminated via certified map F (C3b) |
| F, z* (vacuum point) | GEOMETRIC | fixed by C3b certificate: z* = ⟨root selection rule R1, below⟩ |
| G₄ flux quanta | DISCRETE | fixed-and-declared: ⟨list at pin⟩ |
| N of dark SU(N) | DISCRETE | fixed by C2 certificate fiber table |
| 𝒱, g_s | CONTINUOUS-FREE | reduced to ONE residual freedom by [A-DE] (§2) |
| non-sequence Y₄ moduli | ASSUMED | [A-SEQ] |

**Conclusion (honest form):** conditional on the discrete data and [A-SEQ, A-VOL, A-DE],
the two continuous unknowns (𝒱, g_s) are constrained by one measured quantity (ρ_DE),
leaving **one residual continuous freedom** and therefore **one predicted relation** among
(m_φ, m_DM): the observables lie on a computable one-dimensional curve. "Zero free
parameters" is not claimed and must not appear in any summary of this document.

**R1 (root selection rule, fixed now):** z* is the real root of ∂_z V_flux(F(z)) = 0
nearest the MUM point on the physical branch ⟨branch convention fixed in Appendix A.2⟩;
if multiple candidate roots survive, ALL are carried as separate prediction rows — no
post-hoc choice among vacua.

## 2. The Invariant Relation (attribution corrected)

Scaling ansätze — each an obligation on Appendix A, not an assertion:

- **ANSATZ-1 (confinement):** ln(M_Pl/m_DM) = a₁ · 𝒱^{2/3}/g_s, a₁ = a₁(N, b₀) ∈ ⟨bounded
  interval, Appendix A.1⟩ — from the gauge kinetic function on the wrapped divisor +
  one-loop running; the N-dependence must be explicit.
- **ANSATZ-2 (mediator mass):** m_φ = a₂ · (g_s/𝒱) · M_Pl · |∂²_z V_flux(F(z*))|^{1/2},
  a₂ ∈ ⟨bounded interval, A.2⟩ — flux-potential curvature along the sequence modulus,
  computed from the certified periods.
- **ANSATZ-3 = [A-DE] (vacuum energy):** ρ_DE = a₃ · 𝒱^{-3} · M_Pl⁴, a₃ ∈ ⟨bounded
  interval, A.3⟩, **positive sign and identification with observed dark energy ASSUMED —
  this is the load-bearing Tier C assumption of the whole chain** (text in §6). The
  elimination below is credited to A-DE; the C3b map contributes the certified value of
  |∂²V| at F(z*). Any summary attributing the degeneracy-breaking to C3b alone violates
  the guardrails.

**Elimination (algebra verified in PREDICTION_REVIEW_T0):** multiplying ANSATZ-1 × ANSATZ-2
cancels g_s; substituting 𝒱 = (a₃ M_Pl⁴/ρ_DE)^{1/3} yields

  m_φ · ln(M_Pl/m_DM) = C₀ · M_Pl · (ρ_DE/M_Pl⁴)^{1/9} · |∂²_z V_flux(F(z*))|^{1/2},
  C₀ = a₁a₂a₃^{1/9} ∈ ⟨interval computed from A.1–A.3 bounds⟩.

The residual freedom parametrizes position along this curve; the curve itself is the
prediction.

## 3. Pre-Registered Observables

### P1 — Lensing: core-radius scaling exponent (primary)
Chain (each step's convention fixed now): Yukawa mediator ⇒ σ(v)/m_DM with shape set by
(m_φ/m_DM, α_D) along the §2 curve ⟨transfer-cross-section convention: σ_T; velocity
averaging: Maxwellian at the halo's v_char(M_halo)⟩ ⇒ gravothermal core formation ⇒
r_c ∝ M_halo^β over the mass window ⟨M_min, M_max fixed at pin from the dataset's dwarf
selection, declared before unblinding⟩.

- **[TEST] β:** value ⟨computed at pin⟩ ± σ_β, where σ_β is produced ONLY by the
  robustness protocol RP (below). Comparison: published stacked weak-lensing profile
  posteriors (SDSS/DES/Euclid), F3 threshold ≥3σ exclusion.
- **[FIT] normalization:** one declared amplitude parameter absorbing C₀ and halo-model
  O(1)s. Pre-declared; its best-fit value is reported but never converts to a TEST.

**RP (robustness protocol, the honest version of "rigid"):** compute β over the full
Cartesian product of the bounded intervals a₁, a₂, a₃ and the surviving R1 roots. The
pre-registered TEST is the interval [β_min, β_max]. **Auto-demotion rule:** if
(β_max − β_min) exceeds the data's discriminating width against the CDM-expected scaling
⟨width computed from the public posterior BEFORE our interval is unblinded to it⟩, the
channel demotes itself from TEST to FIT automatically, and this demotion is reported as a
partial F5 outcome — rigidity was claimed and not delivered.

### P2 — PTA: ultralight scalar timing signature (secondary, conditional)
Active iff the §2 curve intersects m_φ ∈ ⟨PTA sensitivity band, taken from the published
NANOGrav/EPTA sensitivity curves in refs/⟩.

- **[TEST]:** monochromatic timing-residual line at f = m_φ/π with amplitude
  Ψ_c = ⟨formula: fixed fraction of G·ρ_DM,local/m_φ², convention and derivation in
  Appendix A.4⟩, using the measured local dark-matter density ⟨cited public value + its
  published uncertainty, entered in refs/ with source⟩. No dark-sector free parameter.
  F4 trigger: predicted amplitude above the 95% upper limit at the predicted f.
- If the curve does not intersect the band: P2 reports NULL-BY-PREDICTION (a valid,
  publishable outcome), and F4 cannot trigger.

## 4. Numbers table (all rows ⟨COMPUTED-AT-PIN⟩; the formulas are frozen NOW)

| Symbol | Formula / procedure | Inputs (provenance) |
|---|---|---|
| F | C3b certificate relation | cert field `c3b_relations[k].relation` |
| z* | rule R1 on V_flux ∘ F | A.2 potential + cert |
| |∂²V(F(z*))| | exact/interval arithmetic on certified periods | cert + A.2 |
| (m_φ, m_DM) curve | §2 relation, a-intervals | A.1–A.3 |
| β ± σ_β | RP over a-intervals × R1 roots | §3-P1 chain |
| (f, Ψ_c) | P2 formulas | curve + measured ρ_DM,local (refs/) |

## 5. Kill switches (full breadth restored)

1. **F5a:** F not extractable by the exact solver (C3b FAIL for all pairs).
2. **F5b:** Appendix A cannot bound any aᵢ to a finite interval (a scaling law fails to
   be derivable) — the relation was invariant-in-name-only.
3. **F5c:** RP auto-demotion fires AND P2 is NULL-BY-PREDICTION — no surviving TEST;
   the model is observationally degenerate. NO_PREDICTION_BRANCH.md is written.
4. **F3:** β interval excluded ≥3σ by the pre-declared lensing posteriors.
5. **F4:** P2 amplitude above the 95% limit at predicted f.
6. Any post-pin change to a formula, convention, interval, or root selection is a tuning
   event (TUNING_LOG.md) and demotes every affected comparison to FIT — including changes
   motivated by "obvious errors"; obvious errors are reported as errors (F6 spirit), not
   silently fixed.

## 6. A-DE — draft text for ASSUMPTIONS v0.3

**A-DE (Dark-Energy Identification).** We assume the stabilized vacuum of the selected
compactification has positive energy density scaling as ρ_vac = a₃𝒱^{-3}M_Pl⁴ with a₃
bounded per Appendix A.3, and that this vacuum energy is the observed dark energy.
*(Tier C — the strongest assumption in the chain: obtaining controlled positive-energy
vacua is an open problem in string compactifications, and this program does not solve it;
it declares it. Discharge path: an explicit stabilization computation for the selected
candidate, or an obstruction — either is reportable. Every §2–§4 output carries [A-DE].)*

*(This text is transcribed into `ASSUMPTIONS.md` as the A-DE entry, replacing the
"required, not yet authored" placeholder — see that file's changelog. It is still T0
draft, not Xavier-signed; ASSUMPTIONS.md does not reach v0.3 until it is.)*

## 7. Blind re-derivation package (inputs-only, per EXECUTION_PLAN §1.2.3)

Contents: the certificates, ASSUMPTIONS v0.3, Appendix A statements *without* the
resulting numbers, refs/ measured-values file. The second T0-class model computes the §4
table independently. Agreement tolerance: overlapping intervals for every row.
Disagreement → DERIVATION_DISPUTES.md; no pin.

**Changelog vs. Desk draft v1.0:** consensus header removed (protocol violation);
"zero free parameters" corrected to one-relation/one-freedom; degeneracy-breaking credit
reassigned from C3b to A-DE (new assumption); scaling laws converted to bounded-interval
ansätze with derivation obligations (Appendix A); all numbers converted to bound slots;
RP auto-demotion added (rigidity must be demonstrated or self-demote); F5 restored to
full breadth (a/b/c); P2 NULL-BY-PREDICTION outcome added; R1 root rule fixed in advance.

---

## Changelog (this repo's document history)

- **v1.0-draft (2026-07-17):** Initial draft. Three candidate observables outlined (halo profile, stochastic background, Lyman-α power). Author: Xavier Callens.
- **v1.0-draft, +Phase 0 scaffold (2026-07-17):** Added §6a placeholder cross-referencing the Free-Parameter Ledger schema (WP P0-B). Not a tuning event (pre-pin).
- **v0.9 status correction, T0 review (2026-07-17):** Status corrected to "DRAFT v0.9 — TEMPLATE ACCEPTED, PREDICTION PENDING" per `PREDICTION_REVIEW_T0.md`, which rejected a "FROZEN v1.0" claim (the "Desk draft v1.0") made outside this repo's git history.
- **v0.9-T0 (2026-07-17):** **Full replacement**, T0-authored, submitted in direct response to `PREDICTION_REVIEW_T0.md`. Replaces the three-observable outline with the compilable slot-based structure above (§0–§7): provenance block, corrected Free-Parameter Ledger, attribution-corrected invariant relation (A-DE, not C3b, breaks the degeneracy), P1 (lensing β, with the RP robustness/auto-demotion protocol) and P2 (PTA, with an explicit NULL-BY-PREDICTION outcome) as the two pre-registered observables, restored full-breadth kill switches (F5a/b/c), A-DE draft text for ASSUMPTIONS v0.3, and a blind re-derivation package description. **Still unpinned** — see the six blocking conditions in the status line above. Not a tuning event: nothing was ever pinned, so nothing demotes from TEST to FIT.

## Related Documents

- **VISION.md** §3–§4: Why falsifiable predictions are essential; falsification branches (F1–F6).
- **K3_CRITERIA.md:** Frozen criteria for K3 candidate ranking (Stream 2); C1/C2/C3b certificates this document's Provenance block cites are produced there.
- **ASSUMPTIONS.md:** A-SEQ, A-VOL, A-ONT, A-REL, A-DE — the Tier C assumption register this document's every §2–§4 output is tagged against.
- **PREDICTION_REVIEW_T0.md:** The T0 review that rejected the prior "Desk draft v1.0" and produced the pin checklist this document is structured to satisfy.
- **PREDICTION_APPENDIX_A.md:** Bounded-interval derivations for a₁, a₂, a₃ (referenced throughout §2–§4) — required before pin; not yet authored (T0/T0s work).
- **TUNING_LOG.md:** Post-pin change log (kill switch 6, above).
- **DERIVATION_DISPUTES.md:** Where a blind re-derivation disagreement (§7) is logged.
- **K3_SELECTION_REPORT.md** (to be generated in Phase 2): Source of the Provenance block's candidate pair.
- **NO_PREDICTION_BRANCH.md** (conditional): Generated if kill switch F5c fires.

---

`Generated-by: T0 architecture session | Verified-by: §2 algebra independently re-derived in PREDICTION_REVIEW_T0; all numeric content deliberately absent pending certificates | Reviewed-by: pending blind re-derivation + Xavier sign-off`
