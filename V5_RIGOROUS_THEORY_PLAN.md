# V5 Rigorous Theory Plan: From Ansatz to Falsifiable Model

**Date**: 2026-07-14
**Prerequisite reading**: `V5_SCIENTIFIC_REVIEW.md` (findings F1–F9) — nothing
below makes sense without it.
**Foundation**: `cooper_exact.py` — the certified kernel. It is the ONLY
permitted source of Cooper-s₇ numerics.

---

## 0. Epistemic Frame

The hypothesis under construction:

> **H(Cooper-s₇)**: Large-scale structure statistics carry a
> density-dependent modulation whose functional form is the fundamental
> period Π₀ of the level-7 K3 family (OEIS A183204) composed with a
> chameleon-screened modulus response z(ρ; M, β) — and this specific form is
> preferred by data over (a) derivative-matched generic kernels and (b) the
> sibling K3 families s₁₀ (A005260) and t₁₀₃ (A276536).

The sibling-family test is the heart of the program: **if the data cannot
tell level 7 from level 10, there is no Cooper-s₇ hypothesis** — only a
generic nonlinearity, and the honest conclusion is null. Both outcomes are
publishable within the project's own documentation; only one of them is a
discovery.

**Gate conditions G1–G5** (defined in the review, Part III) must all hold
before any outreach or public claim. No exceptions.

---

## 1. Session Routing Rules (Haiku vs Sonnet)

**Haiku-tier sessions** get tasks that are: mechanically specified, verifiable
by an included test, and free of design judgment. Every Haiku card below
contains exact formulas, file targets, and a Definition of Done that a script
can check.

**Sonnet-tier sessions** get tasks requiring derivation, estimator design, or
statistical judgment. Sonnet cards specify the *contract* (inputs, outputs,
invariants) and the literature anchors, leaving method choices open.

**Universal guardrails (every session, both tiers)** — these encode the three
failure modes that produced findings F1, F3, F5:

1. **No constant without provenance.** Any numeric constant entering code
   must come from: the certified recurrence, an executed formula, or a
   fetched external authority (OEIS b-file, survey documentation) — with the
   fetch/derivation left in the code or test. If you cannot derive or fetch
   it, STOP and leave a `BLOCKED:` note in the work-package file.
2. **A test that only proves the code runs is a smoke test.** Definition of
   Done items below are *scientific* checks (exactness, null behavior,
   recovery of known inputs). Do not mark a package done on smoke tests.
3. **Synthetic data never touches a discovery file.** Provenance gate WP-C1
   is the first package to run for a reason.
4. Do not edit `cooper_exact.py` except to append tests. Do not resurrect
   `cooper_periods.py`.
5. Update the `STATUS` line of your work-package card in this file when you
   start and when you finish (IN PROGRESS / DONE / BLOCKED + one line).

---

## 2. Dependency Graph

```
WP-A1 (done) ──► WP-A2 ──► WP-B2 ──► WP-C2 ──► WP-C3, WP-C4 ──► unblind
        │                    ▲
        ├──► WP-A3 ──► WP-B3 ┘
        │
WP-C1 (run first, independent)
WP-B1 (independent, feeds z(ρ) parameters into WP-B2)
WP-D1 (after WP-B2)      WP-D2 (after WP-C2)      WP-E1 (last)
```

Recommended order: **C1 → A3 → B1 → A2 → B2 → B3 → C2 → C3/C4 → D1 → D2 → E1**

---

## Track A — Mathematics (make the geometry exact)

### WP-A1 — Certified kernel  ✅ DONE (this session)
`cooper_exact.py`: true A183204 via certified recurrence (cross-checked
against OEIS b-file + Zudilin binomial formula), exact λ = 27, radius 1/27,
Π₀ with certified tail bounds, DC-free band statistic, control-kernel API.
STATUS: DONE 2026-07-14.

### WP-A2 — Frobenius basis and mirror map  [SONNET]
**Objective**: physical couplings in string compactifications live in the
mirror coordinate q, not the algebraic coordinate z. Compute the second
period and the mirror map for the level-7 family.
**Contract**:
- Around z = 0 the order-3 operator has Frobenius solutions
  Π₀ = Σ a(n) zⁿ and Π₁ = Π₀ log z + Σ b(n) zⁿ. Derive the b(n) recurrence by
  differentiating the a(n) recurrence (standard Frobenius bootstrap), exact
  rationals, in a new module `cooper_mirror.py`.
- Mirror map q(z) = exp(Π₁/Π₀). **Integrality check**: the q-expansion
  z(q) = Σ cₙ qⁿ must have integer coefficients — this is the same GATE-C
  integrality criterion the project already used to reject S₁₂, now applied
  as a *consistency proof* of the level-7 family. If cₙ are not integral,
  something is wrong: STOP and report.
- Expose `kernel_cooper_q(rho)` = same pipeline kernel but through q(z(ρ)).
**Definition of Done**: b(n) recurrence verified exactly for n = 0..30;
z(q) integral to 20 coefficients; plot Π₀ vs q-kernel over w ∈ [0, 0.9]
saved to `figures/`; self-test block passes.
**Do NOT**: use floating point in the recurrence derivation; guess b(n).
STATUS: TODO.

### WP-A3 — Sibling-family kernels  [HAIKU]
**Objective**: build the two control K3 families needed for the decisive
model-selection test.
**Steps** (mechanical — all data already in the repo):
1. In a new module `cooper_siblings.py`, implement exact term generators for
   s₁₀ = A005260 (a(n) = Σₖ C(n,k)⁴) and t₁₀₃ = A276536
   (a(n) = Σₖ C(n,k)·C(2k,k)³) — formulas already in
   `hypothesis_comparison_t103_cooper.py`; import or copy them exactly.
2. Fetch OEIS b-files for both (`https://oeis.org/A005260/b005260.txt`,
   `https://oeis.org/A276536/b276536.txt`) and assert term-by-term equality
   for all available terms (cache the b-files under `data/oeis/`).
3. Compute each family's exact growth rate from its verified recurrence in
   `logs/hypothesis_comparison_t103_cooper.json`: for s₁₀, P1 leading coeff
   12 and P0 leading coeff 64 give λ² = 12λ + 64 → λ = 16 (verify the ratio
   a(n+1)/a(n) → 16 numerically to n = 200). Do the same for t₁₀₃ from its
   recurrence entry. **Derive, don't assume** — print the characteristic
   roots.
4. Implement `kernel_s10(rho, rho_scale)` and `kernel_t103(rho, rho_scale)`
   exactly parallel to `cooper_exact.kernel_cooper` (same w = λz variable,
   same W_MAX = 0.9, certified tail bounds using each family's monotone
   ratio property — assert monotonicity numerically like cooper_exact test 3).
**Definition of Done**: b-file equality asserted; λ printed as exact root of
characteristic polynomial and confirmed by ratios; kernels return certified
(value, tail) pairs; `python3 cooper_siblings.py` runs a self-test mirroring
cooper_exact's tests 1–5 and passes.
**Do NOT**: hardcode any term you did not fetch or compute; reuse μ-style
growth "constants" for normalization.
STATUS: TODO.

---

## Track B — Physics (from ansatz to model)

### WP-B1 — Chameleon derivation of z(ρ)  [SONNET]
**Objective**: replace the arbitrary saturating map with a derived response.
**Contract**: write `THEORY_MEMO_CHAMELEON.md` + `chameleon_response.py`.
- Setup: a modulus scalar σ with runaway potential V(σ) = M⁴⁺ⁿ σ⁻ⁿ and matter
  coupling A(σ) = e^{βσ/M_Pl} (Khoury–Weltman 2004 chameleon; Brax et al.
  reviews). Effective potential V_eff(σ; ρ) = V(σ) + ρ A(σ).
- Derive σ_min(ρ) analytically (standard result:
  σ_min ∝ (n M⁴⁺ⁿ M_Pl / βρ)^{1/(n+1)}), then posit the modulus–geometry
  identification w = w_max · f(σ_min/σ_*) with f the simplest monotone map
  consistent with w ∈ [0, w_max) — **state explicitly which step is
  identification (ansatz) vs derivation**, in the memo.
- Deliverable function: `w_of_rho(rho, M, beta, n)` replacing `rho_to_w`;
  predicted redshift scaling of the response (ρ̄(z) ∝ (1+z)³ enters through
  σ_min) written as a closed-form expectation for the tomography test — this
  is the theory's *prediction* for WP-C3, derived BEFORE looking at data.
- Include the screening condition (thin-shell) and state at what halo mass
  screening turns off — this is what makes "suppresses low-mass objects" a
  *derived* claim instead of a slogan (cf. review F4).
**Definition of Done**: memo with every equation numbered and each
ansatz/derivation labeled; module with unit tests (limits: ρ→0, ρ→∞,
monotonicity); tomography prediction curve committed to `figures/` before
WP-C3 runs on data (this is part of the pre-registration).
STATUS: TODO.

### WP-B2 — Estimator design  [SONNET]
**Objective**: a statistically defensible Δ estimator to replace both the
legacy max-asymmetry and the interim `delta_s7_band`.
**Contract** (requirements, method open):
- Operates on density *contrast* δ = ρ/ρ̄ − 1 (DC-free by construction).
- Shot-noise subtraction (1/n̄ Poisson term) and survey-mask handling
  (at minimum: multiply-by-mask forward modeling on mocks; document the
  choice).
- Output: band statistic Δ_band with a per-sector covariance estimated from
  mocks (WP-C2), not from the data itself.
- Must accept `kernel=` so the same estimator serves Cooper/siblings/controls.
- k-band selection frozen on mocks (document why the band; typical choice:
  0.05–0.3 of Nyquist to avoid grid aliasing and the smoothing scale).
**Definition of Done**: `v5_estimator.py` + a validation notebook/script
showing (i) zero mean on 50 Poisson mocks, (ii) known injected signal
recovered within errors, (iii) invariance under galaxy-count downsampling at
fixed structure.
STATUS: TODO.

### WP-B3 — Identifiability harness (the anti-circularity engine)  [SONNET design, HAIKU execution]
**Objective**: make F4 impossible — the Cooper claim only stands if data
prefers Π₀ over matched alternatives.
**Sonnet part**: in `v5_identifiability.py`, implement derivative-matched
controls: given kernel K, construct log/power/logistic controls with
K_c(ρ̄) = K(ρ̄), K_c′(ρ̄) = K′(ρ̄), K_c″(ρ̄) = K″(ρ̄) (2-parameter families
fitted at the mean density) so all candidates agree locally and differ only
in global shape. Model-selection metric: ΔAIC (or log-Bayes via mock-based
likelihood) between kernels fitted to the measured Δ_band(k) spectra.
**Haiku part** (after Sonnet ships the harness): run the 5-way comparison —
{Cooper-s₇, s₁₀, t₁₀₃, matched-log, matched-power} — over all available real
sectors; produce the ranking table with errors from WP-C2 mocks.
**Definition of Done**: on mocks with a Cooper signal injected, the harness
ranks Cooper first with ΔAIC ≥ 10; on null mocks, no kernel wins (ΔAIC < 2
spread). Only then run on data.
STATUS: TODO.

---

## Track C — Statistics & Data Integrity

### WP-C1 — Provenance gate  [HAIKU] — RUN THIS FIRST
**Objective**: make finding F5 structurally impossible.
**Steps**:
1. In `v5_cooper_worker.py` (and any future worker): add
   `data_provenance: "real_survey" | "synthetic_fallback"` to every result
   record, derived from which code path actually served the data (not from a
   CLI flag).
2. Hard gate: any function writing to a `discoveries*.json` file must raise
   `RuntimeError` if `data_provenance != "real_survey"`. No override flag.
3. Delete the seeded-cluster injection block in
   `real_euclid_worker.py::fetch_real_sdss_data` (the
   `% 20 == 0` block that plants clusters "pour avoir de superbes
   découvertes") — synthetic fallback must be statistically featureless
   (uniform + selection-matched redshift draw) so it can serve as a null,
   not as a discovery generator.
4. Quarantine: move `discoveries_v5_cooper.json` (void per review) to
   `archives/void_20260714/` with a README naming the review finding.
**Definition of Done**: unit test proving a synthetic-provenance record
cannot be persisted as a discovery; grep shows no cluster-injection code
remains; void file quarantined.
STATUS: TODO.

### WP-C2 — Mock ensemble & empirical null  [SONNET design, HAIKU execution]
**Objective**: replace analytic-fantasy significances (F7) with an empirical
null distribution.
**Sonnet part**: `v5_mocks.py` — lognormal mock generator matched per sector
to the real n(z), angular footprint, and galaxy count (document the input
power spectrum; a Λ CDM linear P(k) with the survey's effective bias is
sufficient at this stage). Poisson mocks as the degenerate case.
**Haiku part**: run ≥100 mocks per configuration through the WP-B2 estimator;
store the null Δ_band distributions per sector in `logs/null_bank/`;
implement `significance(delta_obs, sector)` as an empirical tail probability
with a global look-elsewhere correction over the number of sectors scanned
(report both per-sector and global p).
**Definition of Done**: null bank exists; a known injected signal at 3σ
recovers p ≈ 0.0013 within Monte-Carlo error; all significance reporting in
the pipeline routed through this function (no more σ arithmetic anywhere
else).
STATUS: TODO.

### WP-C3 — Tomography done right  [HAIKU]
**Objective**: the See-Saw test on residuals, not raw trends (F6.4).
**Steps** (only after WP-B1 prediction curve + WP-C2 null bank exist):
1. Bin real galaxies by redshift: z ∈ [0.05,0.2), [0.2,0.3), [0.3,0.4),
   [0.4,0.6) (SDSS BOSS range; extend only if Euclid depth is actually
   ingested).
2. For each bin: matched mocks (same n(z) within bin, same footprint, same
   count), measure Δ_band on data and on the mock ensemble.
3. Statistic: r(z) = Δ_data(z) − ⟨Δ_mock(z)⟩, with error bars from mock
   scatter. Fit slope of r(z) vs z with errors.
4. Compare the fitted slope against the WP-B1 predicted curve (committed to
   git before this step — check the git history date and note it in output).
**Definition of Done**: figure + JSON with slope, error, p-value against
zero AND against the chameleon prediction; explicit statement of which
selection effects the mock matching does/does not absorb.
**Do NOT**: fit raw μ_Δ(z); tune bins after seeing results.
STATUS: TODO.

### WP-C4 — Pre-registration & blinding  [SONNET]
**Objective**: freeze all analysis choices before unblinding data
significance (gate G5).
**Contract**: `PREREGISTRATION.md` committed to git containing: the frozen
k-band, kernel list, matched-control construction, ΔAIC threshold (10),
mock count, tomography bins, look-elsewhere convention, and the exact
success/failure criteria for H(Cooper-s₇) — including the sentence "if the
sibling families fit equally well (ΔAIC < 2), the result is null." Data
Δ values may be *computed* before this commit but not *compared to the null*
until after.
**Definition of Done**: file committed; git hash recorded inside WP-C3 and
WP-B3 outputs; any later deviation documented in a `DEVIATIONS.md`.
STATUS: TODO.

---

## Track D — External Validation

### WP-D1 — Real persistent homology  [HAIKU]
**Objective**: replace TDA references with computed Betti statistics.
**Steps**:
1. `pip install ripser persim` (fallback: `giotto-tda`). If install fails,
   STATUS: BLOCKED with the pip error — do not hand-roll persistence.
2. `v5_tda.py`: per sector, subsample ≤ 2000 galaxies (document the
   subsampling; persistence is O(n³)-ish), compute H₀/H₁/H₂ persistence
   diagrams on comoving coordinates, summary = total H₁ persistence and
   count of H₁ features with persistence > 2× the mean nearest-neighbor
   distance.
3. Correlate sector-level β₁ summaries with sector Δ_band — **for the Cooper
   kernel AND for every control kernel** (the correlation is only evidence
   if it is kernel-specific; expect it not to be — report either way).
**Definition of Done**: diagrams cached per sector; scatter figure
β₁ vs Δ_band per kernel; Spearman r with mock-based p for each.
STATUS: TODO.

### WP-D2 — Lensing cross-correlation  [SONNET]
**Objective**: the "invisible mass" test, done as a measurement rather than
an overlay-by-eye.
**Contract**: use the public Planck 2018 lensing convergence map (available
without collaboration access; DES Y3 κ maps if accessible). Implement in
`v5_lensing_xcorr.py`: project the top-decile Δ_band sectors onto the sky,
measure the stacked κ signal at their positions vs (i) random positions in
the same footprint and (ii) 90°-rotated positions (null test). Errors by
bootstrap over sectors.
**Definition of Done**: stacked profile with null tests; the writeup must
state the resolution mismatch honestly (Planck κ beam vs sector size) and
what amplitude would be expected from ordinary galaxy-mass correlation —
Cooper-specificity again requires the control kernels.
STATUS: TODO.

### WP-E1 — Honest observatory document  [HAIKU]
**Objective**: `V5_COOPER_OBSERVATORY.md`, written LAST, from results only.
**Steps**: template = review Part III hypothesis + gate table; fill each gate
with measured numbers and its pass/fail; include the void-results notice for
the 2026-07-14 artifacts; NO claim that does not cite a JSON/figure in the
repo. The guideline's prewritten outreach message must NOT be used; if gates
pass, draft a new one stating measured quantities with errors; if gates
fail, the document reports a null result with the same care.
STATUS: TODO (blocked on all other tracks).

---

## 3. Summary Table

| WP | Title | Tier | Depends on | Blocking for |
|----|-------|------|-----------|--------------|
| A1 | Certified kernel | done | — | everything |
| A2 | Mirror map / Frobenius | Sonnet | A1 | B2 (q-kernel option) |
| A3 | Sibling kernels s₁₀, t₁₀₃ | Haiku | A1 | B3 |
| B1 | Chameleon z(ρ) derivation | Sonnet | — | C3 prediction |
| B2 | Estimator design | Sonnet | A1 | B3, C2 |
| B3 | Identifiability harness | Sonnet+Haiku | A3, B2 | gates G3 |
| C1 | Provenance gate | Haiku | — | ALL data runs |
| C2 | Mock ensemble & null bank | Sonnet+Haiku | B2 | C3, C4, D2 |
| C3 | Residual tomography | Haiku | B1, C2 | gate G4 |
| C4 | Pre-registration | Sonnet | B2, B3 designs | gate G5 |
| D1 | Persistent homology | Haiku | B2 | observatory doc |
| D2 | Lensing cross-correlation | Sonnet | C2 | observatory doc |
| E1 | Observatory document | Haiku | all | outreach |

**First three sessions to schedule**: WP-C1 (Haiku, ~1h), WP-A3 (Haiku, ~2h),
WP-B1 (Sonnet, ~3h). They are independent and unblock everything else.
