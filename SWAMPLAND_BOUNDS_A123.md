# SWAMPLAND_BOUNDS_A123.md — WP-A: Off-Ramp 2 Executed (Partial Closure)

**Work package:** WP-A (`briefs/HAIKU_PLAN_STREAM3_PIVOT_2026_07_25.md` §3)
**Agents:** Fable 5 (T0, primary derivation). Deep Think (T0s) blind re-derivation: **PENDING**
(`briefs/WP_A_BLIND_REDERIVATION_BRIEF_2026_07_25.md`) — nothing in this document has
two-model concurrence yet.
**Machine verification:** `scripts/verify_swampland_bounds.py` — executed 2026-07-25,
assertions green.
**Date:** 2026-07-25
**Honest outcome up front:** **partial closure.** One conditional bound derived (B1), one
consistency result derived plus one declared assumption (B2), one result recast with an
explicit refusal (B3). One new obstruction discovered (gap G-1) that blocks pinning the
κ-peak observable against the derived window as currently scoped. F5b is *superseded in
part*, not erased: exact point-mass extraction remains dead, exactly as recorded.

---

## 1. Scope and method

The T0 ruling of 2026-07-25 authorized replacing the failed exact-coefficient extraction
(Off-Ramp 3 / F5b, `NO_PREDICTION_BRANCH.md` §8) with literature-grounded *bounds*
(Off-Ramp 2, `PREDICTION_APPENDIX_A.md` §A.3.2 third option). This document performs that
derivation. Rules applied: every number traces to a citation verified by fetch on
2026-07-25 (§8) or to a symbolic computation executed in
`scripts/verify_swampland_bounds.py`; every physical identification carries a tier label
and assumption tags; anything not derivable is refused, not approximated.

## 2. B1 — Λ_D window via the Dark Dimension scenario — Tier C, conditional

**Identification (conjecture).** We conjecture that the dark scale Λ_D of Appendix A.1 is
realized not as an SU(N) confinement scale — the certified 2× Type II fibres carry no
perturbative gauge algebra, Stream-2-confirmed — but as the Kaluza–Klein scale m_KK of a
single mesoscopic extra dimension, per the Dark Dimension scenario. This identification is
an assumption, tagged **[A-DD]**, and it is *not constructed for this K3*: nothing in the
certified cooper_s7 geometry exhibits a mesoscopic circle. If [A-DD] fails, B1 carries no
content.

**Literature chain (verified §8).** The AdS Distance Conjecture applied to the measured
cosmological constant, with the exponent fixed to 1/4 by experimental and theoretical
constraints, would give one light KK tower: m_KK = λ⁻¹Λ^{1/4} with 10⁻⁴ ≲ λ ≲ 10⁻¹
[2205.12293]; astrophysical follow-up narrows the effective size to l ≈ 1–30 μm
[2309.09330].

**Computed window** (`verify_swampland_bounds.py` [B1-num], Λ^{1/4} = 2.240 meV computed
from Planck-2018 + CODATA inputs, not memory):

| Route | Window for m_KK |
|---|---|
| λ-form [2205.12293] | [0.0224, 22.4] eV |
| size-form [2309.09330] | [0.00658, 0.197] eV |
| **conservative union (adopted)** | **[6.6 × 10⁻³, 22.4] eV** (3.5 decades) |

The two cited routes overlap (asserted in the script); the union is adopted because
pre-registration should take the *widest* defensible window, never the narrowest.

**Candidate §6 line (schema form):**
`Lambda_D in [6.6e-3, 2.24e1] eV [A-DD, A-ONT]` — conjectural identification; the window
is the scenario's, not this K3's.

## 3. B2 — the a₃ ansatz: one derived consistency result, one declared assumption

**What IS derived (machine-verified).** The Appendix A.3 ansatz ρ_DE = a₃ 𝒱⁻³ M_Pl⁴,
written in canonically normalized volume-modulus variables (K = −3 ln(T+T̄),
𝒱 = (Re T)^{3/2}), is the exponential V ∝ exp(−λ_vol φ/M_Pl) with

**λ_vol = 3√(3/2) ≈ 3.674** — derived symbolically and asserted in
`verify_swampland_bounds.py` [B2-core].

This exceeds every candidate swampland lower bound: the dS-conjecture constant c ~ O(1)
[1806.08362, which states only that c is positive; O(1) is the common reading], and the
TCC bound in both readings found in [1909.11063] (interior 2/√6 ≈ 0.816; asymptotic
2/√2 ≈ 1.414 — the exact coefficient is flagged for the blind pass, and the conclusion is
insensitive to the choice). **Result: the 𝒱⁻³ ansatz is swampland-consistent.** This is a
consistency check on the ansatz's *form* — it is not evidence for the ansatz, and it
bounds nothing about a₃'s magnitude.

**What is NOT derived — and is declared instead.** No swampland statement reached in this
work package yields a magnitude for a₃. The ruling's interval 𝒪(10⁻³…1) is therefore
adopted **as a naturalness assumption, not a derivation**, tagged **[A-NAT]**: the
dimensionless coefficient of a leading-order term is assumed to lie within three decades
of unity. This is a conventional but unproven prior; if a₃ lay outside it, the test built
on it would be testing the prior, not the geometry. Anyone quoting B2 must carry [A-NAT]
with it (atomic caveat).

**R2(b) resolved.** The bounded symbol is **a₃ (dimensionless)**. ρ_DE is a *measured
input* (Λ^{1/4} = 2.240 meV equivalent, computed in the script from cited constants) and
is bounded by observation, not by topology. The ruling's phrase "ρ_DE bounded
𝒪(10⁻³…1)" does not survive as written.

**Candidate §6 line (schema form):**
`a_3 in [1.0e-3, 1.0e0] dimensionless [A-NAT, A-DE]` — declared naturalness prior, not a
derived bound; the derived content is the λ_vol consistency result above.

## 4. B3 — chameleon profile regularity: recast, one refusal, one open gap

**What survives as mathematics (Tier A, as PDE theory).** If the mediator couples to
matter density, its static profile obeys a semilinear elliptic equation
∇²φ = ∂_φ V_eff(φ; ρ) with ρ ∈ L^∞ [chameleon mechanism: astro-ph/0309411,
astro-ph/0309300]. For such equations, De Giorgi–Nash–Moser theory (De Giorgi 1957, Nash
1958, Moser 1960; Gilbarg–Trudinger ch. 8) guarantees locally Hölder-continuous
solutions: field profiles across density transitions are C^α — no cusps, no jumps. That
regularity class is a theorem *about the PDE*; applying it to a dark-sector mediator is
Tier C and inherits [A-DD, A-REL].

**Refusal — the ruling's α ∈ (0, 0.5] cannot enter §6 as-worded.** Two independent
reasons. (i) DGNM guarantees *existence* of some α > 0 depending on ellipticity and data;
it does not produce the numeric window (0, 0.5] for this system — no derivation of that
window exists here or in the cited literature, and writing it would be a number from
memory. (ii) Dimensionally, a Hölder exponent is a pure regularity index and **cannot
bound the mass m_φ** (R2(a)); the m_φ slot cannot be filled by α under any wording. If T0
wants an α window pinned, it must first be derived from a specified V_eff and density
model — that work does not exist.

**Conditional m_φ statement.** If the mediator is the radion/volume modulus of the [A-DD]
scenario, we conjecture m_φ ~ m_KK, inheriting B1's union window
[6.6 × 10⁻³, 22.4] eV [A-DD, A-REL] — a bare-mass statement, subject to gap G-1 below.

**⚠ Gap G-1 — discovered in this work package; blocks the κ-peak pin as scoped.** An
*unscreened* scalar in B1's window has force range ħc/m ∈ [8.8 nm, 30 μm] (computed in
the script) — micron-scale, i.e. **no effect whatsoever on weak-lensing κ peaks at
Mpc scales**. The pivot's observable is coherent only if chameleon density-dependence
makes the *cosmic-density* effective mass m_eff(ρ_cosmic) many decades smaller than the
bare window — the mechanism points the right way (m_eff falls with density
[astro-ph/0309411]), but **the quantitative bridge for this system is underived**: no
V_eff has been specified, so m_eff(ρ_cosmic) is currently unbounded in both directions.
Until G-1 is closed (derive m_eff(ρ) from a specified potential) or the observable is
re-scoped to scales where an eV-window scalar acts (e.g. short-range/laboratory bounds as
the TEST, with cosmology dropped), **PREDICTION v2.0 must not pin κ peaks against B1's
window** — doing so would pre-register a test the theory's own numbers say is null by
construction, which would manufacture a guaranteed-pass FIT. This is the single most
important sentence in this document for WP-F.

## 5. New assumption tags (for ASSUMPTIONS.md ledger, T0 to apply)

| Tag | Content | Used by |
|---|---|---|
| **[A-DD]** | The dark sector realizes the Dark Dimension scenario (one mesoscopic dimension; m_KK = λ⁻¹Λ^{1/4}); *not constructed for the cooper_s7 K3* | B1, B3 |
| **[A-NAT]** | Dimensionless leading coefficients lie in [10⁻³, 1] (naturalness prior, declared not derived) | B2 |

Carried over: [A-ONT], [A-REL], [A-DE] as defined in `ASSUMPTIONS.md`.

## 6. R2 resolutions (from `briefs/HAIKU_PLAN_STREAM3_PIVOT_2026_07_25.md` §1)

| Item | Resolution |
|---|---|
| R2(a) Hölder α as m_φ bound | **Refused** — dimensionally impossible; α recast as (underived) profile-regularity content; m_φ handled via conditional m_KK identification instead (§4) |
| R2(b) ρ_DE vs a₃ ambiguity | **Resolved** — bounded symbol is dimensionless a₃ under [A-NAT]; ρ_DE is measured input (§3) |
| R2(c) Λ_D ~ m_KK uncited | **Resolved conditionally** — full citation chain verified; identification explicitly tagged [A-DD], not constructed for this K3 (§2) |

## 7. What may and may not enter PREDICTION v2.0 §6

**May enter** (schema-conformant, each with its tags):
- `Lambda_D in [6.6e-3, 2.24e1] eV [A-DD, A-ONT]` (B1)
- `a_3 in [1.0e-3, 1.0e0] dimensionless [A-NAT, A-DE]` (B2 — declared prior)
- `m_phi in [6.6e-3, 2.24e1] eV [A-DD, A-REL]` (B3 bare mass — **only if** the v2.0
  observable set is re-scoped per gap G-1; forbidden alongside a κ-peak TEST as scoped)

**May NOT enter:** any α ∈ (0, 0.5] line (§4 refusal); any κ-peak-vs-m_φ TEST while G-1
is open; any a₃ line presented as *derived*.

**Consequence for the batch pipeline:** even after a legitimate v2.0 pin, the observables
WP-E implements (κ peaks, Betti numbers) test the *profile/topology* predictions, not the
B1/B3 mass window, unless G-1 closes. WP-F must draft §2–§5 accordingly.

## 8. Citation table (all verified by fetch, 2026-07-25)

| Ref | Verified content used |
|---|---|
| arXiv:2205.12293, Montero–Vafa–Valenzuela, JHEP 02 (2023) 022 | l ~ Λ^{-1/4} ~ 10⁻⁶ m; m_KK = λ⁻¹Λ^{1/4}, λ ∈ [10⁻⁴, 10⁻¹]; species scale 10⁹–10¹⁰ GeV |
| arXiv:2309.09330 | effective size 1–30 μm |
| arXiv:1806.08362, Obied–Ooguri–Spodyneiko–Vafa | \|∇V\| ≥ c·V, c a positive constant (abstract does not fix c; O(1) is the common reading) |
| arXiv:1909.11063, Bedroya–Vafa | TCC slope bound; **coefficient ambiguity flagged** (fetch reports interior 2/√((d−1)(d−2)) and asymptotic 2/√(d−2); conclusion insensitive — blind pass to pin down) |
| astro-ph/0309411 + astro-ph/0309300, Khoury–Weltman | chameleon: m_eff density-dependent; range mm (terrestrial) to 10–10⁴ AU (solar) |
| arXiv:1807.06209, Planck 2018 | H₀ = 67.4 km/s/Mpc, Ω_Λ = 0.685 (inputs to Λ^{1/4} = 2.240 meV, computed) |
| De Giorgi 1957 / Nash 1958 / Moser 1960; Gilbarg–Trudinger ch. 8 | Hölder regularity of solutions to divergence-form elliptic PDE with L^∞ data (textbook) |

Memory-error corrections made *by* the verification process, disclosed per F6 spirit:
the third author of 2205.12293 is Valenzuela (primary derivation initially recalled
Villadoro); the TCC coefficient carried an interior/asymptotic split not present in the
primary derivation's recollection.

## 9. Status vs F5b

F5b's core finding stands: **no exact coefficient is extractable** from the certified
geometry. What Off-Ramp 2 adds is strictly weaker content — one scenario-conditional
window ([A-DD]), one consistency result (λ_vol), one declared prior ([A-NAT]) — plus a
new obstruction (G-1) that constrains how even this weaker content may be used. Whether
that is enough to pin a falsifiable v2.0 is a WP-F/T0 decision, made with G-1 in view.

---

`Generated-by: Fable 5 (T0) WP-A, 2026-07-25 | Verified-by: scripts/verify_swampland_bounds.py executed (assertions green); all citations fetch-verified same day; Deep Think (T0s) blind re-derivation PENDING — no two-model concurrence yet | Reviewed-by: T0 N (pending Xavier + blind pass)`
