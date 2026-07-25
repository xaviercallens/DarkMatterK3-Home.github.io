# WP S3-00b — Flux/Tadpole Construction Brief

**To:** Deep Think (T0s — adversarial concurrence, Two-Model Rule) and Fable 5 (T0 — primary derivation)
**From:** Stream 3 (Empirical Validation)
**Date:** 2026-07-25
**Subject:** Construct (or rule out) the explicit flux/tadpole data needed to compute a₁, a₂, a₃ for the cooper_s7 + A279619 candidate — the blocker recorded as F5b in `NO_PREDICTION_BRANCH.md`
**Authority:** Xavier Callens (T0 Owner), direct instruction 2026-07-25
**Governance:** `.agents/AGENTS.md` (8 workspace rules) applies in full, especially Rules 3, 4, 7 below — read before starting

---

## 0. Read this first

`NO_PREDICTION_BRANCH.md` (this repo, commit `23b947e`) records that WP S3-00 (the MVM
derivation of m_φ, α_D, Λ_D) hit **F5b**: the certified K3/Sym² mathematics is real, but
the three physical coefficients needed to turn that geometry into numbers all require an
**explicit F-theory flux/tadpole compactification that has never been constructed** for
this candidate.

This is not an engineering gap. It is not something a pipeline script can produce. It is
genuine string-model-building work, explicitly flagged by this project's own
`PREDICTION_APPENDIX_A.md` as *"the most speculative part... an active research problem
in string theory."* This brief exists because that work needs to actually happen — by
Deep Think and Fable 5, not by fabricating plausible-sounding numbers under pipeline
pressure, which is exactly what a prior session in this repo declined to do (see commit
`23b947e`'s message for why).

**Do not skip to producing numbers.** Read §1–§3 fully first.

---

## 1. Fixed inputs — certified, not up for negotiation

These come from Stream 2's certificates (`data/certificates/C1_cooper_s7_partner.json`,
`C1loci_cooper_s7_partner.json`, `C2_cooper_s7_partner.json`,
`C3b_symsqrt_cooper_s7.json`, mirrored into this repo's `checkers/certificates/` — verify
against source before use, do not re-derive from memory per Rule 5 of `AGENTS.md`):

| Quantity | Value | Source |
|---|---|---|
| Bulk operator L₃ | cooper_s7 (OEIS A183204), order-3 recurrence, Cooper 2012 | `refs/recurrences_v1.json` |
| Elliptic partner L₂ | A279619, order-2, **integral** | `C3b_symsqrt_cooper_s7.json` |
| Operator identity | L₃ = Sym²(L₂), all-n, kernel-verified in Lean 4 (no `sorry`/axiom) | `Structures/CooperSym2Proof.lean` (Stream 1) |
| Mirror map | z(L₂) = z(L₃) to q¹⁴ | `C3b_symsqrt_cooper_s7.json` |
| Picard rank ρ | 4 | `C2_cooper_s7_partner.json` (Shioda–Tate, exact) |
| Transcendental rank T | 18 (= 22 − ρ) | same |
| Mordell–Weil rank | 0 | same |
| Kodaira fibres | 2× Type II (cuspal) | `C1loci_cooper_s7_partner.json` |
| Singular loci (corrected, F6) | z ∈ {−1, 1/27} | `C1loci_cooper_s7_partner.json` (supersedes the retracted earlier loci — check the F6 note before using any older cert) |
| Frobenius exponents | [0, 1/2] at each singular point | same |

**Sibling candidate for comparison/fallback:** cooper_s10 (OEIS A005260), same ρ=4/T=18,
same Kodaira structure, but its L₂ partner is **non-integral** (rational coefficients) —
weaker as a starting point for brane wrapping (see §4 fallback option).

Treat every number above as ground truth; if either of you finds a discrepancy against
the actual certificate file, that is itself a finding — report it, don't silently
resolve it.

---

## 2. What's actually being asked for — per coefficient

All three are defined in `PREDICTION_APPENDIX_A.md` (this repo) — read it in full before
starting; this section is a summary, not a replacement.

### 2.1 — a₁ (confinement scale Λ_D, `Appendix A.1`)

$$\ln(M_{Pl}/Λ_D) = a_1 \cdot 𝒱^{2/3}/g_s$$

**Needed:** an explicit divisor D (holomorphic 4-cycle in the compactification) that a
D7-brane wraps, realizing a dark-sector gauge group of some rank N, so that the gauge
kinetic function Re(f) ~ 𝒱^{2/3}/g_s can be written down concretely and a₁(N, b₀) fixed
(not just bounded by dimensional analysis — the current placeholder 0.5–2.0 range is not
a derivation).

**Literature anchor already identified:** Witten hep-th/0001083; LVS volume-scaling
(Conlon et al., Weigand et al.). Find and cite the specific result you use.

### 2.2 — a₂ (mediator mass m_φ, `Appendix A.2`)

$$m_φ = a_2 \cdot (g_s/𝒱) \cdot M_{Pl} \cdot |∂_z^2 V_{flux}(F(z^*))|^{1/2}$$

**Needed:** the flux superpotential $W(z)$ itself, built from actual flux quanta (not
just the certified moduli map $F(z_e)$, which only gives you *where* to evaluate — not
*what to differentiate*). Once $W(z)$ exists from real flux data, $V_{flux} =
e^{K}(|D_zW|^2 - 3|W|^2)$ and its second derivative at the certified vacuum point z* is
mechanical symbolic computation — this part becomes genuinely Tier A/B once the flux
input exists.

**Literature anchor:** Denef–Douglas hep-th/0404116; Weigand hep-th/1502.04199.

### 2.3 — a₃ / A-DE (dark energy identification, `Appendix A.3`) — the hard one

$$ρ_{DE} = a_3 \cdot 𝒱^{-3} \cdot M_{Pl}^4, \quad \text{identified with } ρ_{DE,obs} \sim 10^{-47}\,\text{GeV}^4$$

**Needed, explicitly, per `Appendix A.3.3`:**
1. Explicit flux quanta (F₃, H₃ or their F-theory G₄ analogue) for a specific
   compactification containing this K3
2. **Verified D3-brane tadpole cancellation** for that flux choice — this is a checkable
   arithmetic condition (Sethi–Vafa–Witten-type: N_flux + N_D3 = χ(X)/24 for the relevant
   fourfold X), not a matter of taste. State the fourfold, compute χ(X), show the flux
   contributes an integer N_flux ≤ χ/24
3. Sign check: ρ_vac > 0 (**this is not automatic** — most flux vacua in this class give
   AdS, not dS; getting a positive, small vacuum energy is precisely the open problem KKLT
   and LVS exist to address)
4. Magnitude check: does ρ_vac land anywhere near ρ_DE,obs, or does it require additional
   fine-tuning/uplift (KKLT anti-D3, LVS-style) that itself needs justification?

**Literature anchor:** KKLT hep-th/0301240; LVS 0907.2969; swampland program (Vafa,
Obied et al.) for the honest-bound fallback (§4 below).

---

## 3. Task split — Two-Model Rule (`EXECUTION_PLAN.md` S3-00, already the project's own requirement)

**Fable 5 (T0 — primary derivation):**
Attempt the construction in §2 in order (a₂ is the most tractable — it only needs flux
data once, reused for a₁'s brane and a₃'s tadpole check; a₃ is genuinely the hardest and
may not close — see §4). Produce, for anything you can actually construct: the explicit
flux/brane data, the resulting numeric value or bound with uncertainty, and the
literature citation the construction rests on. **Do not produce a number without the
construction behind it** — per Rule 7 (`AGENTS.md`), a coefficient chosen to land a
plausible-looking m_φ is a circular derivation, not a result, and must be labeled as such
if that's what happened.

**Deep Think (T0s — blind adversarial re-derivation):**
Do not read Fable 5's construction first. Independently attempt the same three
constructions from §1's fixed inputs and §2's requirements. Then compare. Per the
`DEEPTHINK_C3B_ADVERSARIAL_BRIEF.md` precedent in this project, your job is **not to
confirm — it is to find the failure mode**:
- Is the flux choice actually tadpole-cancelled, or does the arithmetic not close?
- Is the D7-brane wrapping choice geometrically consistent with the certified Kodaira
  fibre structure (2× Type II, ρ=4), or does it implicitly contradict it?
- Is the sign of ρ_vac genuinely positive from the construction, or asserted?
- Does the "identification" of ρ_vac with ρ_DE,obs require silent extra tuning
  (Rule 7 violation) — if so, say so explicitly rather than absorbing it into a₃'s
  interval.

**Agreement criterion (per `EXECUTION_PLAN.md` M1 gate):** both derivations must agree
within stated tolerance on any coefficient either of you actually closes. Disagreement →
`DERIVATION_DISPUTES.md` (this repo), not silent reconciliation.

---

## 4. Honest off-ramps — use these before fabricating anything

This brief is explicitly not a demand for a positive result. Per `VISION.md §4` and
`PREDICTION_APPENDIX_A.md §A.3.2`/`§A.3.3`, any of the following are acceptable, real
outcomes:

1. **Full construction succeeds** → update `PREDICTION_APPENDIX_A.md` with real values +
   citations, then `PREDICTION.md §6` (v1.1) with m_φ, α_D, Λ_D + uncertainties. S3-00
   resumes, D-3 empirical rerun becomes meaningful.
2. **a₁, a₂ close but a₃ doesn't** → per `Appendix A.3.2`'s third option, bound a₃ via
   swampland-literature constraints instead of explicit tadpole construction. Weaker
   evidence, wider interval, but real — cite the specific swampland bound used, don't
   invent one.
3. **Nothing closes after genuine effort** → F5b stands as recorded. Update
   `NO_PREDICTION_BRANCH.md` with what was specifically attempted and why it didn't
   close (this is itself useful — it tells future work exactly where the wall is).
4. **cooper_s10 (non-integral partner) turns out more tractable** than s7 for some part
   of the construction → flag it; the Route B decision in `K3_SELECTION_REPORT.md` chose
   s7 for integrality, not for flux-tractability, so this isn't settled if it matters here.

Whichever outcome, **write it up honestly** — `.agents/AGENTS.md` Rule 4 (adversarial
skepticism, no self-congratulatory framing) and Rule 6 (caveats must propagate to every
document making the corresponding claim) apply to the writeup, not just the derivation.

---

## 5. Deliverable format

- `PREDICTION_APPENDIX_A.md` updated in place, each ansatz section filled in with: the
  actual construction, the resulting value/interval, literature citation, and an explicit
  Tier label (per `epistemic-guardrails`)
- Symbolic verification (Sympy or equivalent) of the `Appendix A.4` elimination algebra,
  checked in as a script with its output log — not asserted by hand
- If §4 outcome 1: a `PREDICTION.md` v1.1 commit appending §6 (derived quantities),
  timestamped, with the same mechanical `PINNED:` discipline this repo's
  `pipeline/gate.py` already enforces
- If §4 outcome 2 or 3: an update to `NO_PREDICTION_BRANCH.md` or a new
  `SWAMPLAND_BOUND_A3.md`, whichever applies
- A `DERIVATION_DISPUTES.md` entry for anything Fable 5 and Deep Think don't agree on

---

`Generated-by: Claude (session 2026-07-25) at T0 direction | Prepared for: Deep Think (T0s), Fable 5 (T0) | Reviewed-by: pending Xavier`
