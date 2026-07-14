# V5 Deep Scientific Review: The Cooper s₇ Hypothesis

**Date**: 2026-07-14
**Reviewer stance**: adversarial referee, string-theory / mathematical-physics standard
**Scope**: the Cooper s₇ (OEIS A183204) K3-vacuum hypothesis, the V5 Phase 1
implementation (`cooper_periods.py`, `v5_cooper_worker.py`), the V5 guideline
document, and the inherited Phase 4 / V4C claims.
**Method**: every finding below was verified by executed code or an external
authority (OEIS) in this session; transcripts are reproducible from the repo.

---

## Executive Verdict

The project contains **one genuinely sound mathematical pillar** (the
exact-rational recurrence verification of Cooper's sporadic sequences and the
order-2-elliptic / order-3-K3 classification logic), surrounded by a numerical
and inferential structure that does not survive review. The V5 Phase 1
implementation was built on a **fabricated sequence**, evaluates a
**divergent series**, and reports a statistic that is **provably a
normalization artifact**. The physical hypothesis itself is an undeclared
ansatz chain, and the headline statistical claims inherited from Phase 4 are
not defensible in any peer context.

None of this is fatal to the *program*. It is fatal to the current *claims*.
The corrected kernel (`cooper_exact.py`, shipped with this review) restores a
sound mathematical foundation; `V5_RIGOROUS_THEORY_PLAN.md` defines the path
from ansatz to falsifiable model.

**All results in `discoveries_v5_cooper.json` (2026-07-14) are void** and must
not be cited.

---

## Part I — What Stands (credit where due)

**S1. A183204 is real mathematics with the right pedigree.**
Cooper's s₇ (A183204) is a genuine sporadic Apéry-like sequence
(Cooper, *Ramanujan J.* 29 (2012) 163–183; Gorodetsky arXiv:2102.11839;
Cooper–Guillera–Straub–Zudilin arXiv:1604.01106). Its generating function
satisfies an order-3 Picard–Fuchs-type ODE, which is exactly the signature of
a K3-surface (rank-19 family) period, in contrast to order-2 operators
(elliptic curves). The project's Part VIII classification — rejecting the
legacy S₁₂ candidate as elliptic-type and promoting order-3 candidates — is
methodologically legitimate.

**S2. The exact-rational recurrence verification is correct and was the key
to this review.** `hypothesis_comparison_t103_cooper.py` fitted, in exact
arithmetic, the recurrence

    (n+2)³ a(n+2) = (26n³+117n²+177n+90) a(n+1) + (27n³+81n²+78n+24) a(n)

verified for n = 0..38 with zero failures. Its characteristic equation
λ² = 26λ + 27 = (λ−27)(λ+1) gives the **exact** growth rate λ = 27, hence
radius of convergence **1/27** for Π₀(z). This single exact fact exposed
findings F1 and F2 below. Re-verified this session (0 failures; ratios
increase monotonically to 26.797 at n = 199).

**S3. The engineering substrate is real.** GPU pipeline, sector paging,
streaming results, dashboards — competent infrastructure, reusable as-is.

---

## Part II — Findings (severity-ranked, all evidence executed this session)

### F1 — CRITICAL: The V5 sequence is fabricated (two layers deep)

- The V5 guideline document asserts A183204 = 1, 13, 271, 6721, 184561,
  5373583, 163473991. **OEIS query (this session): that sequence matches
  nothing in the database.** The true A183204 is
  **1, 4, 48, 760, 13840, 273504, 5703096, 123519792, …**
  (confirmed against the OEIS b-file, terms 0..702 available).
- `cooper_periods.py::EXACT_TERMS` copied the guideline's seven wrong terms and
  then **continued with 23 further terms that satisfy no consistent
  recurrence** (ratio drift → ~32.8, incompatible with any 3-term Apéry-like
  recurrence; the true λ is 27). These were hallucinated during the previous
  implementation session and labeled "exact integer values; no floating point
  approximation."
- Consequence: every number produced by Phase 1 derives from constants with
  no mathematical referent.

**Lesson institutionalized in the plan**: no numerical constant enters the
pipeline without a machine-checked derivation (recurrence/formula) or an
external authority fetch (OEIS b-file) at build time. See WP-A guardrails.

### F2 — CRITICAL: The "period integral" is a divergent series

`cooper_periods.py` normalizes coefficients by μⁿ with μ = 25.869408 and
evaluates at z up to 0.95. But μ is a finite-n underestimate of the true
growth rate λ = 27 (and of the fabricated terms' ~32.8 drift), so the
normalized coefficients **grow**: c(10)=1.23, c(20)=12.9, c(29)=109.3.
Partial sums at z = 0.9 were measured this session: N=10 → 3.94, N=15 → 6.74,
N=20 → 12.10, N=25 → 22.53, N=30 → 42.69 — **unbounded**. The reported
"Π₀(0.9) = 6.74" is the N=15 partial sum of a divergent series, i.e., an
artifact of where the truncation happened to stop.

Correct statement: Π₀(z) = Σ a(n) zⁿ converges iff |z| < 1/27 ≈ 0.037. In the
proper variable w = 27z ∈ [0, 0.9], the certified values are gentle:
Π₀ ∈ [1.0, 1.277] with tail bounds ≤ 1.3 × 10⁻¹⁰ (`cooper_exact.py`, test 5).
Physically this matters: the K3 warping is a **percent-level modulation**,
not the ~7× amplification Phase 1 reported — every downstream threshold was
calibrated to an artifact.

### F3 — CRITICAL: Δ_s7 measured nothing spatial

Executed check on the Phase 1 metric: the argmax of |FFT(G_Cooper) −
FFT(G_raw)| sits at **voxel (0,0,0) — the DC mode — at 0.0625, with the
next-largest mode 14× smaller (0.0045)**. The k=0 coefficient is the grid
sum, so the reported "Δ_s7" is exactly the difference of the two grids' means
under the chosen normalization: a **single scalar with zero spatial,
clustering, or topological content**. All three "discoveries" in
`discoveries_v5_cooper.json` are this normalization offset.

Remedy (implemented): `cooper_exact.py::delta_s7_band` works on zero-mean
density contrasts (DC removed by construction) and compares shell-averaged
Fourier amplitudes over a calibrated k-band.

### F4 — HIGH: The Phase 2 test suite is circular as designed

The pipeline applies a pointwise, monotone, convex kernel to density. *Any*
such kernel amplifies overdense regions relative to voids; therefore "high Δ
at massive filament intersections" and "Δ traces the cosmic-web spine" are
**guaranteed by construction**, for the Cooper kernel, for log(1+ρ), for ρ^α —
for anything of that shape. The guideline's Success Metrics for the Filament
Test would be "passed" by a pipeline with no K3 content whatsoever.

The only way the Cooper hypothesis acquires empirical content is
**identifiability**: the data must *prefer* the Π₀ kernel over
derivative-matched control kernels under a proper model-selection criterion.
Self-test 7 of `cooper_exact.py` already shows naive kernel comparison is
confounded by amplitude (log-control Δ = 0.54 vs Cooper 0.079) — controls
must be matched in the first two derivatives at the mean density (WP-B3).

### F5 — HIGH: Discoveries were generated from synthetic data with injected clusters

`real_euclid_worker.py`'s fallback **seeds artificial clusters** into sectors
satisfying `(int(ra_min) % 20 == 0) and (int(dec_min) % 20 == 0)` — the
comment says "pour avoir de superbes découvertes" (to get superb
discoveries). The V5 test run used the synthetic path for all three sectors,
and its outputs were written to a file named `discoveries_*.json` without a
provenance field. A discovery pipeline that can manufacture its own anomalies
and record them indistinguishably from data has **zero evidentiary value**.
Remedy: hard provenance gate (WP-C1) — fallback data may never write to any
discovery store.

### F6 — HIGH: The physics chain is an undeclared ansatz stack

Stated as a string theorist would: for the hypothesis to be a *model* rather
than a metaphor, each arrow below must be either derived or declared an
ansatz with parameters to be constrained:

1. **Compactification claim**: a K3 (×T²?) factor with complex-structure
   modulus z whose Picard–Fuchs periods are Cooper-s₇. *Status: choice of
   family — legitimate as a postulate; the mirror-map/Frobenius structure
   (Π₁ = Π₀ log z + …, q = exp(Π₁/Π₀)) is computable and should be (WP-A2),
   because physical couplings live in q, not raw z.*
2. **Modulus–matter coupling**: local baryonic density sources a shift of z.
   *Status: pure ansatz. The saturating map z(ρ) = z_max ρₙ/(1+ρₙ) was chosen
   for boundedness, not physics. A chameleon-type derivation exists in the
   literature (Khoury–Weltman 2004; Brax et al.) for scalar moduli with
   V_eff(σ;ρ) = V(σ) + ρ e^{βσ/M_Pl}; minimizing it yields σ_min(ρ) and hence
   a **derived** z(ρ) with slope and saturation scale fixed by (V, β) — this
   is WP-B1 and it converts two free functions into two parameters.*
3. **Observable**: Π₀(z(ρ)) modulates effective clustering.
   *Status: needs a propagator-level statement (which term in the effective
   action is Π₀ multiplying?). Until then the kernel is phenomenology and
   must beat controls (F4).*
4. **Cosmic See-Saw** (μ_Δ rises with redshift): as designed, the test
   confounds survey selection — number density, magnitude limits, and shot
   noise all drift with z, and any density-dependent statistic will trend in
   z from selection alone. The V4C log shows a smooth *monotone decline* of
   Δ across sequentially processed sectors — the signature of a systematic,
   not of physics. *Remedy: per-bin matched mocks; test the data-minus-mock
   residual slope only (WP-C3).*
5. Cited authority "Tsai et al., PRD 2026" for extra-dimensional resonance:
   treat as unverified until a DOI is produced; do not cite in outreach.

### F7 — MEDIUM: Inherited claim hygiene (Phase 4)

"126.7% confidence" is not a statistic. "10.2σ (P < 10⁻²⁸⁰)" for a 35-sector
survey with no mock-calibrated covariance and no look-elsewhere correction is
not defensible; numbers of this order signal a broken null model, and their
presence in documents intended for peers is the single fastest way to be
dismissed. HMAC "cryptographic verification" of discovery files
authenticates *file integrity*, not *scientific validity* — the two are
conflated repeatedly in Phase 4 documents. Recommended: reframe all Phase 4
significance language as "uncalibrated internal metrics" pending WP-C2.

### F8 — MEDIUM: The outreach message would misrepresent the state of evidence

The guideline's prewritten forum post asserts results ("naturally suppresses
low-mass noise", "strictly increases with redshift") that (a) were never
measured, and (b) per F3/F4 *could not have been* measured by the shipped
code. Posting it would burn credibility with exactly the community whose
scrutiny the project needs. No outreach until the gate conditions below are
met.

### F9 — LOW: Documentation asserted success prematurely

`V5_PHASE1_HANDOFF.md` / `V5_PHASE1_COMPLETION_SUMMARY.md` declare "COMPLETE
AND TESTED ✓" for components now shown void. Tests that only confirm code
*runs* are smoke tests; they were presented as scientific validation.
Correction notices required (applied as part of this review).

---

## Part III — The Hypothesis, Restated Rigorously

The defensible core, stripped to a falsifiable statement:

> **H(Cooper-s₇)**: Large-scale structure statistics carry a
> density-dependent modulation whose functional form is the fundamental
> period Π₀ of the level-7 K3 family (A183204) composed with a
> chameleon-screened modulus response z(ρ; M, β), and this specific form is
> preferred by data over derivative-matched generic kernels *and* over the
> sibling K3 families (s₁₀ = A005260, t₁₀₃ = A276536).

This is testable, and — crucially — **losable**: the sibling-family
comparison (same mathematics, different level) is the cleanest internal
control available, because any generic density effect will fit all three
families equally well.

**Gate conditions for any public claim** (all must hold):

| Gate | Condition |
|---|---|
| G1 | All numerics on certified kernel (`cooper_exact.py`); zero fabricated constants |
| G2 | Real survey data only; provenance field on every record; fallback path physically unable to write discoveries |
| G3 | Δ statistic beats derivative-matched controls AND sibling K3 families at ΔAIC ≥ 10 on data, calibrated on ≥100 matched mocks |
| G4 | Tomography measured on data-minus-mock residuals, selection-matched per bin |
| G5 | Significance from empirical mock null with look-elsewhere correction; thresholds frozen (pre-registered in git) before unblinding |

---

## Part IV — Corrected Kernel: What Shipped With This Review

`cooper_exact.py` (all self-tests passing this session):

- True A183204 via the certified recurrence, cross-checked term-by-term
  against both the OEIS b-file and the independent Zudilin binomial sum.
- Exact λ = 27, radius 1/27; physical variable w = 27z ∈ [0, 0.9].
- Π₀ evaluation with **certified geometric tail bounds** (≤ 1.3 × 10⁻¹⁰ over
  the physical domain), valid because a(n+1)/a(n) ↑ 27 monotonically
  (verified to n = 199).
- Verified K3 asymptotics: a(n) ≈ C·27ⁿ·n^(−3/2) (b(n)·n^1.5 stable to 0.3%
  between n = 100 and n = 300).
- `delta_s7_band`: DC-free, shell-averaged spectral statistic; discriminates
  structured from flat fields; control-kernel API for the identifiability
  program.
- `cooper_periods.py` carries a deprecation banner voiding its outputs.

**Verdict**: foundation restored; hypothesis unproven; program viable.
Proceed via `V5_RIGOROUS_THEORY_PLAN.md`.
