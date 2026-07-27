# PREDICTION.md Appendix A — Derivation of the Three Ansätze

**Status:** v0.2 — WP S3-00b construction attempted 2026-07-25 and **BLOCKED (F5b)** for all
three ansätze; see A.1.4, A.2.5, A.3.4 for the per-coefficient obstruction and
`NO_PREDICTION_BRANCH.md` for the recorded outcome. The A.4 elimination algebra **was**
verified symbolically (`scripts/verify_appendix_A4.py`, executed, assertions green) and that
verification corrected two errors in A.4.2 as previously written — see the F6 disclosure
there. No numerical value for a₁, a₂, or a₃ is derived anywhere in this document.  
**Purpose:** Make explicit, before any numerical work, the three scaling laws (ANSATZ-1, ANSATZ-2, ANSATZ-3 = A-DE) that are the load-bearing structure of the MVM (Minimal Viable Matching) calculation. Each ansatz is stated as a **proportionality with bounded O(1) coefficients**, not as an assertion of exact functional form.  
**Tier:** C throughout. These are conjectures, not theorems. Each discharge path is listed.

---

## Preamble: What This Appendix Does and Does Not Claim

This appendix **derives, not asserts**, three power-law scalings that relate the low-energy EFT parameters (m_φ, α_D, Λ_D, 𝒱, g_s, N) to geometric data from the K3 compactification. Derivation here means:
- Starting from stated first principles (D7-brane gauge kinetics, flux-potential energy, Kodaira fiber structure)
- Identifying the dominant term in each observable
- Bounding the prefactor (the O(1) coefficient) by dimensional analysis and literature values
- Stating the proportionality and its valid regime

**Crucially, this appendix does NOT:**
- Solve for 𝒱 or g_s independently (they are determined by stabilization, which is a separate Tier C step — A-VOL)
- Claim rigidity of β (the lensing exponent) — rigidity is tested by the robustness protocol of PREDICTION.md §3
- Produce numbers — numbers are computed only at S3-00 pin time, using this appendix as the formula template
- Justify why these scalings are correct — that is a literature question, addressed via citations to string compactifications papers (KKLT, LVS, de Sitter constructions)

---

## A.1 — ANSATZ-1: Confinement Scale vs. Moduli

**Statement:** The dark-sector gauge-symmetry confinement scale Λ_D (the running coupling's Landau pole) scales as

$$\ln\left(\frac{M_{Pl}}{Λ_D}\right) = a_1 \cdot \frac{\mathcal{V}^{2/3}}{g_s} \quad ,\quad a_1 = a_1(N, b_0) \in [a_1^{min}, a_1^{max}]$$

where 𝒱 is the four-cycle volume (in units of $M_s = M_{Pl}/\sqrt{g_s}$), g_s is the string coupling, N is the dark-gauge rank, and b_0 is the one-loop beta-function coefficient.

### A.1.1 — Derivation Path (to be expanded at pin time)

**Primary literature anchor:** Witten hep-th/0001083 (gauge coupling from Kähler form); LVS volume-scaling phenomenology (Conlon et al., Weigand et al.).

1. **Gauge kinetic function on a D7-brane divisor:** The D7-brane wrapping a holomorphic divisor D in the K3 base induces a gauge kinetic function proportional to 1/g_s with a volume dependence from the Kähler metric.

2. **Weak coupling from volume:** In the large-volume regime, the running-coupling threshold follows from the gauge kinetic function Re(f) ∼ 𝒱^{2/3}/g_s at the K3-moduli point.

3. **Taking logs:** The Landau pole yields a_1 ∼ 1/(π b_0), bounded by 0.5 < a_1 < 2 for typical SU(N) with b_0(N) ≈ 11N/3.

4. **N-dependence:** The coefficient a_1(N) must account for how the beta function scales. SU(N): b_0 = 11N/3 − 2n_f/3.

### A.1.2 — Interval Specification (to be calculated)

Define [a_1^{min}, a_1^{max}] conservatively for all ranks 3 ≤ N ≤ 10.

**Placeholder range:** a_1 ∈ [0.05, 2.0] — to be refined at pin time with explicit literature citation.

### A.1.3 — Discharge Path (A-VOL, A-REL)

Credibility depends on: A-VOL (𝒱 stabilization), A-REL (K3 + D7 in same compactification).

### A.1.4 — WP S3-00b construction outcome (2026-07-25)

**Status:** BLOCKED (F5b). Tier C, parametrically bounded only — not derived.

**Attempted.** Wrap D7-branes on an explicit divisor D to engineer a dark-sector gauge group
of definite rank N, so Re(f) ~ 𝒱^{2/3}/g_s could be written concretely and a₁(N, b₀) fixed
rather than merely bounded.

**Obstruction — the Type II veto.** The certified Kodaira fibre content of the cooper_s7
partner is 2× Type II, cuspal (`C1loci_cooper_s7_partner.json`). Under the standard
Kodaira–Tate dictionary a Type II fibre carries no gauge algebra; perturbative ADE
enhancement begins at Type III (su(2)) and Type IV (su(3)). The certified fibres therefore do
not supply the weakly coupled SU(N) sector this ansatz needs — in a 4d N=2 setting such cusps
are instead associated with strongly coupled non-Lagrangian (Argyres–Douglas-type) sectors.
Engineering SU(N) would require an independent divisor in the full Calabi–Yau fourfold X₄, but
the certificates fix only the local K3 fibre (ρ=4, T=18); neither X₄ nor its threefold base B₃
is specified anywhere in this program, so Vol(D) cannot be evaluated.

> **Basis correction (2026-07-27).** The certificate basis cited above — "2× Type II"
> fibres and (ρ=4, T=18) — was retracted by Stream 2 escalation E-007 on 2026-07-26: the
> labels came from a faulty exponent→Kodaira lookup, and E-008/E-009 subsequently found
> that no Kodaira reading is available from this family's operators at any locus (the
> finite singular points are order-2 elliptic points of X₀(7)+, not Kodaira degenerations;
> current derived lattice data: ρ = 19, T = 3, Tier B, E-011). The obstruction therefore
> stands in strengthened form: there is still no derivable weakly coupled SU(N) sector —
> now because no gauge-algebra reading exists at these loci at all — and X₄/B₃ remain
> unspecified. BLOCKED (F5b) status unchanged.

**Consequence.** a₁ remains bounded by dimensional analysis via generic LVS volume scaling
(Witten hep-th/0001083). The A.1.2 interval stands as a placeholder, not a result.
[A-VOL, A-REL, A-ONT]

---

## A.2 — ANSATZ-2: Mediator Mass vs. Flux Curvature

**Statement:** The ultralight scalar mediator φ has a mass

$$m_φ = a_2 \cdot \frac{g_s}{𝒱} \cdot M_{Pl} \cdot |\partial_z^2 V_{flux}(F(z^*))| ^{1/2}$$

where F is the **C3b Shioda-Inose map** (certified geometric), z* is the flux-potential minimum, and a_2 ∈ [a_2^{min}, a_2^{max}] accounts for DBI action and geometric couplings.

### A.2.1 — Derivation Path

**Primary literature anchor:** Denef–Douglas hep-th/0404116 (moduli masses from flux potentials); Weigand hep-th/1502.04199 (D7-brane moduli in F-theory).

The D7-brane modulus z_brane couples to the flux superpotential via the DBI action. At the flux-stabilized vacuum, the mass-squared follows from the second derivative of the effective potential.

### A.2.2 — Certificate Dependence (C3b)

The second derivative |∂_z^2 V_{flux}(F(z*))|^{1/2} is **computed exactly from the C3b certificate**:
- The map F(z_e) is the output of the S2-01b checker (Tier A/B)
- Flux potential V_flux is constructed from K3 periods (Picard-Fuchs + mirror-symmetry)
- Taking derivatives is automatic symbolic computation

**This is the only part of the MVM leveraging a Tier A/B (certified geometric) input.** The prefactor a_2 is Tier C.

### A.2.3 — Interval Specification

**Conservative range:** a_2 ∈ [0.1, 10.0] (weakly-warped to strongly-warped)  
**Refined range (if stronger evidence):** [0.5, 3.0] (mild warping, single D7)

Choice at pin time; robustness protocol (PREDICTION.md §3-P1) computes over Cartesian product of all aᵢ intervals.

### A.2.4 — Discharge Path

If flux potential is non-perturbative (gaugino condensation), the form of V_flux changes and a_2 may not be derivable. Flagged as A-VOL / A-ONT contingency.

### A.2.5 — WP S3-00b construction outcome (2026-07-25)

**Status:** BLOCKED (F5b). The |∂²V| factor is algebraically defined but not evaluable.

**Attempted.** Construct the Gukov–Vafa–Witten flux superpotential W(z) = ∫ G₄ ∧ Ω₄ and
evaluate ∂²_z V_flux at the certified singular loci z ∈ {−1, 1/27}
(`C1loci_cooper_s7_partner.json`, the F6-corrected loci).

**Obstruction — the flat-direction wall.** The cooper_s7 operator is order 3, so it governs a
rank-3 sub-variation of Hodge structure. The C2 certificate gives transcendental rank T = 18
(`C2_cooper_s7_partner.json`). Introducing G₄ flux only along the rank-3 subspace the
Picard–Fuchs operator actually controls leaves 18 − 3 = 15 moduli unstabilized. Those flat
directions would correspond to massless scalars, which existing fifth-force bounds do not
permit as a dark sector. Building a fully stabilizing flux vector would need the full
18-dimensional intersection data, which the certificates do not contain.

> **Basis correction (2026-07-27).** "T = 18" above is retracted (Stream 2 E-007); the
> derived value is T = 3, Tier B (E-011), and the 2026-07-27 U1 execution derived
> T ≅ U⊕⟨14⟩ [B] with an explicit splitting. The "18 − 3 = 15 unstabilized moduli"
> count therefore does not survive: the PF operator's rank-3 sub-VHS is the whole of
> T ⊗ ℂ. The obstruction's operative content is narrower but stands: no G₄ flux
> superpotential is constructible without the fourfold X₄ (the same missing object as
> §A.1.4/§A.3.4), so |∂²V| remains unevaluable and BLOCKED (F5b) is unchanged. See
> Stream 2 `briefs/STREAM2_M1PRIME_MECHANISM_MEMO_2026_07_27.md` route R2.

**Consequence.** |∂²V_flux(F(z*))|^{1/2} is carried symbolically (as `C_flux` in
`scripts/verify_appendix_A4.py`) and assigned no value. A point-mass m_φ obtained from a
rank-3 flux choice alone would not be physically meaningful absent a stabilizing flux vector
(Denef–Douglas hep-th/0404116). Note the certified geometric input here (the mirror map F,
Tier A/B) is real; what is missing is the flux potential to differentiate. [A-VOL, A-ONT]

---

## A.3 — ANSATZ-3 (= A-DE): Dark-Energy Scaling and Identification

**Statement:** The stabilized vacuum energy density is

$$ρ_{DE} = a_3 \cdot \mathcal{V}^{-3} \cdot M_{Pl}^4 \quad ,\quad a_3 \in [a_3^{min}, a_3^{max}]$$

and is **identified with the measured dark-energy density today** (ρ_DE,obs ~ 10^{−47} GeV^4). This breaks the (𝒱, g_s) degeneracy using ρ_DE,obs as a measured quantity.

### A.3.1 — Derivation Path

**Warning:** This is the most speculative part. De Sitter vacua are an active research problem in string theory.

**Primary literature anchors:** KKLT (Kachru et al. hep-th/0301240), LVS (Balasubramanian et al. 0907.2969), swampland program (Vafa et al., Obied et al.).

In type-IIB F-theory compactifications:
$$V_{flux} = \frac{W_0^2}{2 \mathcal{V}^2} + a_3 \mathcal{V}^{-3} + \text{(other terms)}$$

The leading scaling is 𝒱^{-2}, but non-perturbative corrections and flux backreaction modify this to 𝒱^{-3} in the LVS regime.

### A.3.2 — Interval Specification

**Critical decision for Phase 1:** Either compute a_3 via explicit flux/tadpole construction (hard), bound a_3 via swampland constraints (medium), or defer to post-pin adversarial pass (weak constraint but honest).

**Placeholder range:** a_3 ∈ [10^{−10}, 10^{−6}] — conservative, to be tightened at pin time if explicit vacuum construction is available.

### A.3.3 — Discharge Path (A-DE)

Requires:
- Explicit flux/tadpole data for the chosen candidate
- Sign verification: ρ_vac > 0
- Identification test: ρ_vac ≈ ρ_DE,obs

If unavailable before M1 → **F5b** (no prediction), documented honestly in `NO_PREDICTION_BRANCH.md`.

### A.3.4 — WP S3-00b construction outcome (2026-07-25) — **this is the trigger that fired**

**Status:** BLOCKED (F5b). Swampland-boundable in principle; no explicit construction.

**Attempted.** Satisfy the D3 tadpole condition N_flux + N_D3 = χ(X₄)/24, then sign-check
ρ_vac > 0 and magnitude-check against ρ_DE,obs.

**Obstruction — the topology void.** χ(X₄) is a global invariant of the Calabi–Yau fourfold and
depends on the choice of threefold base B₃. This program specifies a K3 with certified lattice
data (ρ=4, T=18) and no global fourfold, so χ(X₄) is undefined and the tadpole condition is not
merely unsatisfied — it is not posable. Selecting a χ(X₄) to admit a flux landscape large enough
to tune W₀ for a KKLT-style de Sitter uplift would be a fitted input presented as a derivation,
which `.agents/AGENTS.md` Rule 7 forbids.

> **Basis correction (2026-07-27).** "(ρ=4, T=18)" above is retracted (Stream 2 E-007);
> the derived values are ρ = 19, T = 3, Tier B (E-011). The obstruction is unaffected:
> χ(X₄) depends on the unspecified threefold base B₃, not on the K3 lattice ranks, so the
> tadpole condition remains not posable. Standing policy: until a B₃ is specified and the
> tadpole is posable, no model under this program makes any dark-energy / vacuum-energy
> claim (T0 decision D4, 2026-07-26; assumption A-DE).

**Consequence.** a₃ is not derived, so the A.3.3 discharge path fails and **F5b fires** exactly
as pre-committed. Per A.3.2's third option a₃ could instead be bounded phenomenologically via
the de Sitter swampland conjecture (Obied et al. 1806.08362); that bound was **not** computed in
this work package and remains open. The A.3.2 placeholder interval is not a result.
[A-DE, A-VOL, A-ONT]

---

## A.4 — Elimination Algebra (Pure Algebra; to be verified at pin time)

Given ANSATZ-1, ANSATZ-2, ANSATZ-3, eliminate (𝒱, g_s) to produce the invariant relation.

### A.4.1 — Setup

**Three equations:**

1. From ANSATZ-1: $\ln(M_{Pl}/Λ_D) = a_1 \cdot 𝒱^{2/3}/g_s$

2. From ANSATZ-2: $m_φ = a_2 \cdot (g_s/𝒱) \cdot M_{Pl} \cdot |∂²V|^{1/2}$

3. From ANSATZ-3: $ρ_{DE} = a_3 \cdot 𝒱^{-3} \cdot M_{Pl}^4$

**Solve for 𝒱 from (3):**
$$𝒱 = (a_3 M_{Pl}^4 / ρ_{DE})^{1/3}$$

**Substitute into (1) and (2), then multiply/eliminate to cancel g_s and 𝒱.**

### A.4.2 — Invariant Relation (Pre-Registration Form)

**Verified form (2026-07-25).** Machine-verified by `scripts/verify_appendix_A4.py` (executed;
assertions green; output log in the WP S3-00b commit). The elimination yields:

$$m_φ \cdot \ln(M_{Pl}/Λ_D) = C_0(a_1, a_2, a_3) \cdot M_{Pl} \cdot (ρ_{DE}/M_{Pl}^4)^{1/9} \cdot |∂²V(F(z^*))|^{1/2}$$

where:
- **C_0 = a_1 a_2 a_3^{−1/9}** — verified free of residual dependence on 𝒱, g_s, M_Pl, ρ_DE, Λ_D
- ρ_DE/M_{Pl}^4 is dimensionless, from measured dark energy
- |∂²V(F(z*))|^{1/2} from the C3b certificate (Tier A/B) — certified, but see A.2.5: the flux
  potential needed to evaluate it was not constructible
- Λ_D is the confinement scale of A.1, **not** a dark-matter mass

Under [A-ONT, A-VOL, A-REL, A-DE] this **would be** the relation constraining the P1 and P2
observables jointly, *if* the worked EFT matching existed — it does not (F5b, see A.1.4/A.2.5/
A.3.4). Per VISION §1.3 the certified Sym² geometry does not by itself supply that matching.

> #### F6 disclosure — two errors in this section as previously written
>
> The symbolic verification corrected the prior text of A.4.2, which had stood since
> 2026-07-18 and was never machine-checked:
>
> 1. **Sign of the a₃ exponent.** Prior text: `C_0 = a_1 a_2 a_3^{1/9}`. Derivation gives
>    `a_3^{−1/9}`. This is **not** cosmetic: over A.3.2's placeholder interval
>    a₃ ∈ [10⁻¹⁰, 10⁻⁶] the two forms differ by a factor of a₃^{−2/9} ≈ 21× to 167×
>    (≈60× at mid-range a₃ = 10⁻⁸), i.e. roughly 1.3–2.2 decades in m_φ. The observable
>    decision rule of `PREDICTION.md` §3 branches on whether m_φ falls in the
>    **one-decade** window [10⁻²³, 10⁻²²] eV, so an error of this size could have flipped
>    the pre-registered branch between P1 (PTA) and P2 (lensing). Recorded here rather
>    than silently fixed, per F6 discipline.
> 2. **Left-hand-side quantity.** Prior text wrote `ln(M_{Pl}/m_{DM})` and glossed m_DM as
>    "a benchmark dark-matter mass". The elimination of A.1 produces `ln(M_{Pl}/Λ_D)`. Λ_D
>    and m_DM are distinct quantities; substituting one for the other would be an additional
>    physical assumption (Λ_D ≈ m_DM) requiring its own tier label and assumption tag, not a
>    notational convenience. The verified form above uses Λ_D.
>
> A third, cosmetic inconsistency is also corrected: the prior closing line labelled
> "P1 (lensing)" and "P2 (PTA)", which inverts `PREDICTION.md` §3 (P1 = PTA, P2 = lensing).
>
> Neither error affected any published result, because no numbers were ever computed from
> this relation — F5b blocked that path before any value existed. Both are disclosed under
> the F6 rule because A.4.2 was previously presented as a settled algebraic result.

### A.4.3 — Robustness Protocol

Compute m_{DM} from measured lensing data; eliminate to solve for m_φ; compute β across Cartesian product [a_1^{min}, a_1^{max}] × [a_2^{min}, a_2^{max}] × [a_3^{min}, a_3^{max}] × {all R1 roots}. Report [β_min, β_max] as TEST prediction.

---

## Summary: Status and Next Steps

This appendix is a **template**. At S3-00 pin time, each section will be completed with:

1. Specific numerical values and intervals for a_1, a_2, a_3
2. Literature citations justifying each bound
3. Symbolic algebra verification (Sympy) of the elimination step
4. Sensitivity analysis showing β and P2 dependence on aᵢ intervals
5. Assumption tags ([A-SEQ, A-VOL, A-ONT, A-REL, A-DE]) on each step

**Status checklist — actual state after WP S3-00b (2026-07-25):**
- [ ] All three ansätze have derivations — **BLOCKED (F5b)**: A.1.4 (Type II veto), A.2.5 (15 flat directions), A.3.4 (χ(X₄) undefined)
- [ ] Intervals [a_i^{min}, a_i^{max}] specified for all three — placeholders only; not results
- [x] **Elimination algebra verified symbolically** — `scripts/verify_appendix_A4.py`, executed, assertions green; corrected two errors in A.4.2 (F6 disclosure there)
- [ ] C3b certificate loaded; |∂²V(F(z*))| computed — certificate loaded and the mirror map F is certified, but |∂²V| is not evaluable (A.2.5)
- [ ] Robustness-protocol β interval computed — depends on a_i values that do not exist
- [ ] P2 observable (if triggered) computed — no m_φ, so no branch has been selected
- [x] All assumption IDs tagged on every quantity
- [x] Adversarial passes completed — Deep Think (T0s) blind re-derivation; unified concurrence on Off-Ramp 3, no dispute (`DERIVATION_DISPUTES.md`)
- [ ] Xavier sign-off on the derivation chain — nothing to sign; there is no derivation chain to approve

**Net:** one line of this appendix is now machine-verified (A.4 algebra) and the other three are
recorded as blocked. That is the honest state; it is not a partial success toward a number.

---

**Generated by:** Fable 5 (T0) — WP S3-00b construction attempt, 2026-07-25 (outline: Fable 5, 2026-07-18)  
**Verified by:** `scripts/verify_appendix_A4.py` executed (A.4 algebra only); Deep Think (T0s) adversarial concurrence on A.1.4/A.2.5/A.3.4 obstructions and on the A.4.2 C_0 correction  
**Reviewed by:** T0 N — pending Xavier review of the F5b outcome and the F6 disclosure in A.4.2
