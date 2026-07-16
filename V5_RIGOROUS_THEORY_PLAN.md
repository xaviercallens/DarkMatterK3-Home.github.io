# V5 Rigorous Theory Plan: From Ansatz to Falsifiable Model

**Date**: 2026-07-14 (unified vision added 2026-07-16)
**Prerequisite reading**: `V5_SCIENTIFIC_REVIEW.md` (findings F1–F9) — nothing
below makes sense without it. `PIVOT_MEMO.md` records the 2026-07-14 pivot:
**s₁₀ is now the primary family; s₇ is retired pending clean rebuild.**
**Foundation**: `cooper_s10_kernel.py` (primary, A005260, λ=16) and
`cooper_exact.py` (s₇ reference, A183204, λ=27). These are the ONLY permitted
sources of Cooper-family numerics.

---

## 0-bis. Unified Vision — Dual-Scale Topological Universe Model

**Full program statement**: `UNIFIED_VISION.md` (hypotheses H-DT1/H-DT2/H-DT3
in pre-registered form, cross-stream contracts, near-term milestones). This
section is the plan-local summary; the work packages for the dual-theory
classification tests are **Track F** below.

The V5 program is one stream of a three-stream architecture. The unifying
theoretical frame is an **F-theory compactification with K3 × T² base and
elliptic fiber**: order-3 Picard–Fuchs candidates are interpreted as K3-base
periods; order-2 candidates as elliptic-fiber (curve) periods.

### Three Parallel Streams

| Stream | Repository | Focus | Goal |
|---|---|---|---|
| 1. Theory | `SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal` | F-theory formalization in Lean 4 | Mathematically certify the Dual-Scale Model |
| 2. K3 Selection | `SocrateAI-Scientific-Agora-K3-DarkMatter` | AutoEvolve for K3 sequence selection | Confirm Cooper s₇/s₁₀ as true K3 surfaces |
| 3. Experimentation | `DarkMatterK3-Home.github.io` | GPU-based validation (SDSS, Euclid, PTA) | Empirically validate the model |

This repository is the engine room of Streams 2 and 3: the certified kernels,
estimators, mocks, and gates below are what "validation" means concretely.

### Key Hypotheses (each labeled per practice P1/P2 — status, not slogan)

1. **K3-base identification** — Cooper s₇ (A183204) and s₁₀ (A005260) satisfy
   order-3 Picard–Fuchs-type ODEs → periods of K3 surfaces, candidates for
   the F-theory base.
   *Status: the order-3 classification is verified in-repo (exact recurrence,
   0 failures; review S1–S2). The identification of these periods with the
   physical compactification is the declared ansatz that Tracks A/B convert
   into a testable model. s₁₀ is primary; s₇ retired per `PIVOT_MEMO.md`.*
2. **Elliptic-fiber identification** — S₁₂/S₂₁ satisfy order-2 Picard–Fuchs
   ODEs → elliptic-curve periods, candidates for the F-theory fiber.
   *Status: order-2 classification verified (review S1: S₁₂ rejected as a K3
   candidate for exactly this reason). Reinterpreting order-2 candidates as
   the fiber rather than discards is a Stream-1 (Lean) formalization task; no
   empirical claim attaches to it yet.*
3. **7-brane / discriminant-locus interpretation** — spatial spikes in Δ_obs
   correspond to 7-brane intersections (discriminant locus of the elliptic
   fibration).
   *Status: interpretive ansatz, currently unsupported. The motivating record
   K3-DISC-0003 was produced by the legacy Phase 4 max-asymmetry metric,
   which review F7 classifies as an uncalibrated internal metric; it is
   motivation only. Any brane-locus claim requires a Δ measured by the WP-B2
   estimator, calibrated on WP-C2 mocks, and passing gates G1–G5.*

### Stream ↔ Work-Package Mapping

- Stream 1 (Lean 4 theory): consumes the exact recurrences and mirror-map
  results of WP-A2/WP-A3 as formalization targets; the integrality check of
  WP-A2 is the natural first Lean theorem.
- Stream 2 (K3 selection / AutoEvolve): the order-3 vs order-2 classifier is
  the selection criterion; sibling families (WP-A3, practice P4) are its
  control set.
- Stream 3 (GPU experimentation): everything in Tracks B/C/D; no result
  leaves this stream without gates G1–G5.

---

## 0. Epistemic Frame

The hypothesis under construction (s₁₀-primary form, per `PIVOT_MEMO.md`):

> **H(Cooper-s₁₀)**: Large-scale structure statistics carry a
> density-dependent modulation whose functional form is the fundamental
> period Π₀ of the level-10 K3 family (OEIS A005260, λ=16) composed with a
> chameleon-screened modulus response z(ρ; M, β) — and this specific form is
> preferred by data over (a) derivative-matched generic kernels and (b) the
> sibling K3 families s₇ (A183204, if rebuilt cleanly) and t₁₀₃ (A276536).

The sibling-family test is the heart of the program: **if the data cannot
tell level 10 from level 7 (or from t₁₀₃), there is no Cooper-s₁₀
hypothesis** — only a generic nonlinearity, and the honest conclusion is
null. Both outcomes are publishable within the project's own documentation;
only one of them is a discovery.

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
STATUS: PARTIAL 2026-07-14 — s₁₀ done as `cooper_s10_kernel.py` (WP-A3-s10,
b-file verified, λ=16 derived, self-tests pass); t₁₀₃ kernel still TODO.

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
STATUS: PARTIAL 2026-07-14 — interim `v5_estimator_s10.py` shipped
(WP-B2-s10: shot-noise handling, null-mock check on 10 mocks); full design
with mask handling, mock covariance, and 50-mock validation still TODO.

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
STATUS: DONE 2026-07-14 — `v5_provenance_gate.py`; void artifacts quarantined
under `archives/void_20260714_s7_fabricated/`.

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

## Track F — Dual-Scale Unification (added 2026-07-16, see `UNIFIED_VISION.md`)

### WP-F1 — Picard-Fuchs order classification  [HAIKU]
**Objective**: turn hypotheses H-DT1/H-DT2 (order-3 ⇒ K3 base, order-2 ⇒
elliptic fiber) into a mechanical, reproducible classification — the
selection criterion for Stream 2.
**Steps**:
1. New module `pf_order_classifier.py`: for each candidate family
   {s₇, s₁₀, t₁₀₃, S₁₂, S₂₁}, derive the operator order from the *verified
   in-repo recurrence* (`cooper_exact.py`, `cooper_s10_kernel.py`,
   `logs/hypothesis_comparison_t103_cooper.json`, and the legacy S₁₂/S₂₁
   definitions). Print the recurrence, its order, and the characteristic
   roots — derive, don't assume (P1).
2. Integrality check per class: K3 candidates get the WP-A2 mirror-map
   criterion; elliptic candidates get the weight-2 (elliptic/modular)
   integrality analog. S₁₂'s historical GATE-C failure must be *reproduced*
   by the classifier as "not K3", then re-tested as "elliptic: yes/no".
3. Output `logs/pf_classification.json`: family → {order, class, integrality
   pass/fail, evidence pointers}. This file is the Stream-2 → Stream-3
   kernel allowlist input (cross-stream contract 2 in `UNIFIED_VISION.md`).
**Definition of Done**: classifier reproduces the known answers (s₁₀
order-3/K3-integral; S₁₂ not-K3) as a known-answer test (P2); every entry
carries a provenance pointer; self-test passes.
**Fails honestly if**: any Cooper family is not order-3, or S₁₂/S₂₁ fail
elliptic integrality — record the failure in the JSON; that family exits its
candidate list (H-DT1/H-DT2 failure conditions).
STATUS: TODO.

### WP-F2 — AutoEvolve selection harness (Stream 2 contract)  [SONNET]
**Objective**: spec + reference implementation for the
`SocrateAI-Scientific-Agora-K3-DarkMatter` repo: an AutoEvolve loop that
proposes candidate sequences and classifies them with WP-F1's classifier.
**Contract**:
- Search space: integer sequences with verified holonomic recurrences
  (OEIS-anchored or generated); fitness = passes classification (order +
  integrality + λ growth derivable), never "fits the data" — data fitting
  stays in Stream 3 behind pre-registration (P3).
- Sibling families are the control set (P4): the harness must rediscover
  s₁₀ and t₁₀₃ from scratch as a known-answer test before proposing novel
  candidates.
- Deliverable here: `STREAM2_AUTOEVOLVE_SPEC.md` + the classifier module;
  the evolutionary loop itself lives in the Stream-2 repo.
**Definition of Done**: spec committed; known-answer rediscovery demonstrated;
interface (classification JSON schema) frozen and referenced by both repos.
STATUS: TODO (depends on WP-F1).

### WP-F3 — Lean 4 formalization contract (Stream 1 interface)  [SONNET]
**Objective**: define what the `…-LeanProposal` repo formalizes first and
what artifacts flow back.
**Contract** — first three formalization targets, in order:
1. Recurrence → operator-order statement for s₁₀ (A005260): the certified
   recurrence implies an order-3 Picard-Fuchs-type ODE.
2. The GATE-C integrality criterion as a formal definition (so "is a K3
   period candidate" has a machine-checked meaning — the arbiter for
   Stream-2 classification disputes, contract 1 in `UNIFIED_VISION.md`).
3. The LVS perturbative bound: for the observationally bounded regime
   (S ≤ 1.177), geometric symmetry breaking stays perturbative.
Artifacts flow back as a pinned commit hash + statement list in
`lean/STREAM1_STATUS.md` here; no numeric constant may be transcribed from
Lean files into pipeline code without its own provenance (P1).
**Definition of Done**: contract doc committed in both repos; target 1 either
proved or reduced to explicitly named axioms/sorries with an honest count.
STATUS: TODO.

### WP-F4 — Discriminant-locus (Δ spike) census  [HAIKU, gated]
**Objective**: test H-DT3 — Δ_obs spikes as 7-brane intersections — as a
measurement, not an overlay.
**Steps** (only after WP-C2 null bank and WP-B3 harness exist; runs on
provenance-gated real-survey sectors only):
1. Census: top-decile Δ_band sectors per kernel (Cooper-s₁₀ AND every
   control) with empirical-null p-values and look-elsewhere correction.
2. Kernel-specificity requirement: a sector is a discriminant-locus
   *candidate* only if the Cooper kernel's spike is not reproduced by the
   matched controls (ΔAIC ≥ 10 per WP-B3 convention).
3. K3-DISC-0003 (RA 205°, Dec 35°): re-measure the sector under the gated
   pipeline. Until then it is motivation only (review F7) and must not be
   cited as evidence anywhere.
**Definition of Done**: census JSON + figure with per-kernel spike maps and
null statistics; explicit pass/fail against the H-DT3 failure condition.
STATUS: TODO (blocked on C2, B3).

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
| F1 | PF-order classification | Haiku | A1, A3 | F2, Stream-2 allowlist |
| F2 | AutoEvolve harness spec | Sonnet | F1 | Stream-2 repo work |
| F3 | Lean 4 contract (Stream 1) | Sonnet | — | Stream-1 repo work |
| F4 | Discriminant-locus census | Haiku | C2, B3 | H-DT3 verdict |

**Original first three sessions** (WP-C1, WP-A3, WP-B1): C1 done, A3 done for
s₁₀ (t₁₀₃ pending), B1 still open.
**Next sessions to schedule (2026-07-16)**: WP-B1 (Sonnet, ~3h),
WP-F1 (Haiku, ~2h), WP-F3 (Sonnet, ~2h) — independent of each other;
B1 unblocks Track C, F1 unblocks Stream 2, F3 starts Stream 1.
