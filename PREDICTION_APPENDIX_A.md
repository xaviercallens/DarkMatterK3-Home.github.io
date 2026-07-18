# PREDICTION.md Appendix A — Derivation of the Three Ansätze

**Status:** v0.1-outline (structure template) completed 2026-07-18; numerical values and full derivations TBD at S3-00 implementation.  
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

The result has the structure:

$$m_φ \cdot \ln(M_{Pl}/m_{DM}) = C_0(a_1, a_2, a_3) \cdot M_{Pl} \cdot (ρ_{DE}/M_{Pl}^4)^{1/9} \cdot |∂²V(F(z^*))|^{1/2}$$

where:
- C_0 = a_1 a_2 a_3^{1/9} (product of O(1) coefficients; itself O(1))
- ρ_DE/M_{Pl}^4 is dimensionless, from measured dark energy
- |∂²V(F(z*))|^{1/2} from C3b certificate (Tier A/B)
- m_{DM} is a benchmark dark-matter mass

**This is the predicted relation** binding P1 (lensing) to P2 (PTA) via a single constraint.

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

**Status checklist at pin time:**
- [ ] All three ansätze have derivations
- [ ] Intervals [a_i^{min}, a_i^{max}] specified for all three
- [ ] Elimination algebra verified symbolically
- [ ] C3b certificate loaded; |∂²V(F(z*))| computed
- [ ] Robustness-protocol β interval computed
- [ ] P2 observable (if triggered) computed
- [ ] All assumption IDs tagged on every quantity
- [ ] Adversarial passes completed
- [ ] Xavier sign-off on the derivation chain

---

**Generated by:** T0 outline (Fable 5, 2026-07-18)  
**To be completed by:** T0 and T0s (blind re-derivation) at S3-00  
**Reviewed by:** Pending Xavier signature on ASSUMPTIONS.md and C3b certificate
