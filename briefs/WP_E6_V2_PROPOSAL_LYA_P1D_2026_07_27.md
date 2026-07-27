# WP-E6 v2 Proposal — Mixed-Fraction f_FDM vs. the DESI DR1 Lyman-α P1D

**Status: DRAFT — PROPOSAL ONLY. This proposal awaits T0 sign-off; no phase executes
before that.**

**Date:** 2026-07-27
**Authority to draft:** T0 decision **D-f** (`briefs/T0_DECISIONS_2026_07_27.md`), option
(A) of `docs/WP_E6B_LYA_ADEQUACY_PREFLIGHT_2026_07_27.md` §7. D-f authorizes *drafting this
document*. It authorizes nothing in it.
**Lineage:** v1 = `briefs/WP_E6_PHENO_SWEEP_PROPOSAL_2026_07_27.md` (structure and
stop-condition discipline inherited from it; v1's own stop condition is what caught the
DES-Y6 negative honestly, and every stop condition below is written to be at least as
strict). Statistic re-scope = T0 **D-e**. Framing = T0 **D-b** (mixed fraction).

**No code, no data acquisition, and no comparison is proposed for execution here.** Each
phase below is gated; each gate requires a named artifact from the phase before it; each
phase carries a stop condition that fires on its own evidence without a further decision.

---

## 1. Objective

### 1.1 What a real comparison would deliver

A calibrated mixed-fraction analysis of the DESI DR1 Lyman-α 1D flux power spectrum would
deliver **an upper bound on f_FDM — the fraction of the dark matter carried by an ultralight
scalar of mass m — as a function of m, over a mass region where the published literature
currently records no such bound.** The output is an exclusion contour in the (m, f) plane:
"f_FDM > f*(m) is excluded at N σ by DESI DR1 P1D, under modeling assumptions M." Nothing
else. In particular it would not measure f_FDM, and a null result would constrain the
parameter space rather than falsify anything.

### 1.2 Which (m, f) region

The target region is the part of the WP-E6/E6b grid — m ∈ [10⁻²², 10⁻¹⁹] eV,
f ∈ [0.05, 1.00] — that survives **both** filters after Phase 0:

- **decisive** under a *calibrated* forward model (not the pre-flight proxy — see §3), and
- **open** against the published mixed-fraction landscape as re-surveyed in Phase 0.

The pre-flight's 221-cell count is the *upper* bound on that region under an optimistic
proxy and an unverified openness overlay. The honest expectation is that the real region is
substantially smaller, possibly empty; Phase 0 and Phase 2's re-derivation are the two
places that gets decided, and either may end the WP.

Note the f = 1 column is already excluded across the whole grid by published pure-FDM mass
limits (tightest: May, Dalal & Kravtsov 2025, m > 8×10⁻¹⁸ eV). The open territory is
entirely f < 1. That is why D-b's mixed-fraction framing is the only framing available.

### 1.3 Relation to F5b and PREDICTION.md — tier-correct statement

Under F5b **no exact top-down observable (m_φ, α_D, Λ_D) is derivable on current state**;
`PREDICTION.md` v1.1-PINNED §6 records F5b as reversible, and no pinned prediction selects a
mass. Therefore:

- This program can **constrain** or **exclude** regions of an assumed (m, f) parameter
  space. It cannot confirm, support, favour, or corroborate the dual-scale hypothesis, and
  no output of it may be worded that way.
- Every output is labeled **exclusion/FIT**, never `TEST`, until and unless a `PREDICTION`
  v2 amendment is pinned that pre-registers this statistic (CLAUDE.md rules 1, 3, 5).
- A fully excluded grid would constrain the phenomenological parameter space. It would not
  bear on the Tier A result (`L₃ = Sym²(L₂)`, kernel-proven) or the Tier B ρ = 19 / T = 3
  derivation, neither of which supplies a coupling or a mass.
- The mediator-mass interval is an **input choice**, tier [C] as a physical relevance claim,
  inherited from v1 §1 and unchanged. It is not derived from the K3 mathematics.
- Rule 5 applies in full: no pipeline may depend on a single predicted scalar mass, because
  none exists.

---

## 2. What this proposal is NOT

1. **Not an authorization.** D-f authorized this draft. Execution needs its own T0 sign-off,
   and Phase 3+ additionally needs a pinned `PREDICTION` v2.
2. **Not a reopening of WP-E5.** The 2D transverse route stays closed on its data floors
   (~1.6 Mpc, ~10⁴ objects/slice). A different observable is not an appeal.
3. **Not a hydrodynamic simulation program.** This repo has no hydro capability, no
   simulation compute, and no calibration data. §4 Phase 1 makes "build our own emulator" an
   explicit **stop**, not a fallback.
4. **Not a derivation.** Every run would log: *"Parameters scanned phenomenologically
   (sweep); not derived (F5b stands)."*
5. **Not an edit of any pinned document.** `PREDICTION.md` v1.1-PINNED is untouched. Entry is
   via `PREDICTION_v2_DRAFT.md` under the pin protocol, or not at all.
6. **Not a dark-energy program.** T0 decision D4 / A-DE stands.
7. **Not a re-derivation dressed as novelty.** Where a published bound already covers a cell,
   the honest label is reproduction/robustness, and the headline claim is confined to the
   region Phase 0 finds genuinely unconstrained.

---

## 3. Honest-optimism ledger (carried forward, binding)

The WP-E6b pre-flight's forward model is a **linear-theory P1D ratio**. Confronted with the
only two masses where an emulator-grade published mixed-fraction bound exists, it is
optimistic by the following factors relative to its own 2σ decision threshold:

| m (eV) | published 95% bound (Liu, Gong & Zhou 2026) | pre-flight σ_equiv at that f | overstatement vs. 2σ |
|---|---|---|---|
| 1.000×10⁻²² | f_FDM < 0.12 | 36.9 | **18.5×** |
| 1.000×10⁻²¹ | f_FDM < 0.65 | 98.6 | **49.3×** |

Computed in `data/derived/wp_e6b_lya_adequacy_preflight_2026_07_27.json`
(`optimism_calibration_vs_published_anchors`), pinned by
`test_optimism_calibration_is_present_and_exceeds_unity`. The overstatement is itself
mass-dependent and grows by ~2.7× across one decade in m, so it may **not** be applied as a
uniform correction factor to the rest of the grid.

**Binding consequences for v2:**

1. **No v2 sensitivity number may be inherited from the pre-flight.** Every σ, every contour,
   every reachability count in v2 must be **re-derived** with the calibrated forward model,
   the full covariance, and nuisance marginalization in place. The pre-flight's 221 is an
   adequacy statement — "the statistic is not intrinsically precision-starved" — and is
   retired the moment Phase 2 produces its own number.
2. **The v2 report must republish this table** alongside its own recomputed sensitivity, so a
   reader can see how much of the pre-flight's headroom survived.
3. **If the calibrated re-derivation lands within the 18.5×–49.3× band of the pre-flight's
   own threshold**, the honest reading is that the pre-flight's headroom was entirely
   modeling optimism, and Phase 2's stop condition fires.

---

## 4. Phased plan

Notation: **G_n** = the gate that must be passed to *enter* phase n. Every stop condition is
mechanical — it fires on the phase's own filed artifact, without a further decision — and
firing means **file the negative and stop the WP**, in the WP-E6/DES-Y6 manner.

### Phase 0 — Literature re-survey to close the 207-cell honesty flag

**Do first. Cheapest phase; the one most likely to end the WP.**

**G_0:** T0 sign-off on this proposal.

**Why:** WP-E6b §2 records that **207 of the 221 decisive cells are open only because
`docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md` §4 lists no mixed-fraction bound at their
masses** (`governing_constraint: "none published (unconstrained)"`). That is a statement
about *this repo's survey of the literature*, not about the literature. Only 14 cells are
open against an actual published mixed-fraction constraint. If the survey is incomplete, the
target region shrinks — possibly to nothing — and every downstream phase is wasted effort.

**Work:** a targeted literature check on published mixed-fraction (f_FDM < 1) constraints
above 10⁻²¹ eV, from Lyman-α forest, CMB, galaxy clustering, UFD kinematics, and strong
lensing, including constraints stated for generic ultralight-axion fractions rather than
"FDM" by name. Extend `docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md` §4 in place with a dated
addendum. No downloads, no code.

**Deliverable:** a revised openness overlay and a recomputed decisive-and-open cell count,
plus an explicit statement of what was searched and what "no bound found" is worth after
searching it.

**STOP CONDITION P0:** if, after the re-survey, **fewer than 10 cells** remain both decisive
(under the pre-flight proxy, which is the generous filter) *and* open against the published
landscape — or if the surviving cells lie entirely at f ≥ 0.5, where mixed-fraction limits
are least interesting — file the re-survey as the terminal artifact of the WP-E6 line and
**STOP**. Do not proceed to Phase 1.

**Secondary trigger:** if the re-survey finds a published analysis that has *already* done
substantially what this WP proposes on DESI DR1 P1D, STOP and file it as such.

---

### Phase 1 — Modeling adequacy: source (do not build) a calibrated forward model

**G_1:** Phase 0 filed and P0 not fired.

This phase addresses WP-E6b §5 items 1, 2, 3 and 6 — the items that carry the 18.5×–49.3×
optimism. Its governing rule: **obtain a forward model, do not manufacture one.**

**Work — evaluate, in order, the public options catalogued in §5 of this proposal:**

1. Can a **public mixed-FDM (CDM + ultralight) flux-power emulator or a published,
   citable suppression fit with quantified accuracy** be obtained that covers the Phase-0
   surviving region in (m, f) and the DESI z = 2.2–4.4, k ≤ 5.3×10⁻² s/km range?
2. If not directly: can a **two-arm construction** be justified and validated — a public
   ΛCDM P1D emulator for the baseline arm, plus a *published* nonlinear/flux-level
   mixed-DM suppression prescription for the ratio arm — with a stated and citable accuracy
   over the target region?
3. In either case, the hand-rolled linear interpolation `S(k;m,f) = 1 − f·(1 − T_F(k;m)²)`
   from `pipeline/wp_e6_sweep.py` is **retired**, replaced by a solved two-component linear
   calculation from a public Boltzmann code (§5.3), which is a necessary but *not sufficient*
   upgrade — it fixes §5 item 3, not items 1, 2 or 6.

**Deliverable:** a modeling-adequacy report naming the chosen forward model, its training or
calibration domain, its stated accuracy, where the target region sits relative to that
domain, and an explicit list of what remains uncalibrated.

**STOP CONDITION P1 (the hard one):** if no public mixed-FDM P1D forward model with a
**quantified accuracy over the target region** can be obtained, **STOP and file.**

Specifically and without exception:

- **Do not hand-roll a hydrodynamic emulator.** Every published bound in this mass range
  rests on a hydro-simulation suite spanning cosmology × IGM thermal history. Reproducing
  one is a multi-year, multi-million-CPU-hour program. This repo has no such capability, and
  an uncalibrated substitute reproduces exactly the failure mode the pre-flight's own
  optimism calibration exposed.
- **Do not extrapolate a public emulator outside its stated calibration domain** and call
  the result calibrated. If the target region lies outside the domain, that is a P1 stop,
  not a caveat.
- **Do not treat "we could not find one" as "one does not exist"** without the Phase 1 report
  recording what was searched — the same discipline Phase 0 applies to the bounds survey.
- If an adequate model exists but is **not public** (author-held), that is a **T0 question**
  under CLAUDE.md rule 4 (*public data products only; never phrase results as
  collaboration/submission/endorsement*), not an agent decision. Requesting it is not
  authorized by this proposal; the honest default while awaiting a T0 ruling is P1 STOP.

---

### Phase 2 — Statistical design and calibrated sensitivity re-derivation

**G_2:** Phase 1 filed, P1 not fired, and a named forward model with a stated accuracy in
hand.

This phase addresses WP-E6b §5 items 2, 4 and 5, and produces the number that replaces the
pre-flight's 221.

**Work:**

1. **Likelihood.** A Gaussian likelihood in the P1D bins, with the mixed-FDM forward model
   from Phase 1 as the mean. Statistic and threshold fixed *here*, before any real-data
   number is computed, and carried verbatim into the Phase 3 pin.
2. **Full covariance.** Replace the diagonal `e_total = √diag(COV)` used in the pre-flight
   with the **published covariance matrix**, which ships in the same Zenodo product this repo
   already holds (DOI 10.5281/zenodo.16943723; `data/MANIFEST.md` records that `e_total_kms`
   was verified in-session to equal `√diag(COVARIANCE)` to floating-point noise, so the full
   matrix is present and its diagonal is already cross-checked). Ignoring the off-diagonal
   structure inflates significance; this is a sensitivity **loss**, expected and accepted.
3. **Validity cuts** per the paper's own §4.1 (arXiv:2505.07974): `k > 10⁻³ s km⁻¹`
   (continuum-error contamination) and `k < 0.5π/R_z` with
   `R_z ≡ cΔλ_DESI/(1+z)λ_Lyα`, `Δλ_DESI = 0.8 Å`. Bins outside the range are dropped
   entirely, not down-weighted — already implemented in `pipeline/wp_e6b_lya.py` and
   test-guarded (`test_both_validity_cut_arms_actually_exclude_bins`; 755 of 1020 bins
   survive). Cuts are declared before the pin and not revisited after.
4. **IGM nuisance parameters and marginalization strategy.** Free and marginalized, not
   cancelled by a ratio: mean transmitted flux F̄(z); the temperature–density relation
   (T₀, γ); the pressure/filtering scale k_F; thermal Doppler broadening. Plus the
   contaminant terms the DESI analysis itself carries: metals (SB1 and companions), DLAs,
   continuum/resolution systematics — as nuisance parameters, **not** as an assumption that
   the SB1-subtracted central product is clean. Priors taken from the published analyses and
   cited, never invented. The ratio construction cancels these only at first order and only
   if they are FDM-independent, which they are not: the IGM thermal history responds to the
   modified collapse history. Marginalization-induced degeneracy with the suppression shape
   is expected to be the **dominant** sensitivity loss.
5. **Closure test on mocks before anything else** — the WP-E5 lesson, mechanized. Inject a
   known (m, f) into synthetic P1D realizations built from the published covariance; recover
   it with the full pipeline including marginalization. Plus a null test at f = 0 with a
   calibrated false-positive rate, and a null-degeneracy guard
   (`pipeline.resolvability.assert_null_usable`) run before any statistic.
6. **Calibrated sensitivity re-derivation.** Recompute the reachable region under items 1–4.
   This number, not 221, is what v2 reports.

**Deliverable:** a design document plus a filed synthetic-only sensitivity artifact and its
test suite. **Synthetic data only throughout — CLAUDE.md rule 1 forbids real-data comparison
code before the pin.**

**STOP CONDITIONS P2 (any one fires):**

- **P2-a (the DES-Y6 analogue):** if the calibrated re-derivation leaves **no cell** that is
  both ≥ 2σ-reachable *and* open post-Phase-0, file the negative and **STOP**. This is the
  direct counterpart of WP-E6's stop condition, and it is the outcome the §3 ledger says to
  expect.
- **P2-b:** if the closure test cannot recover its own injected signal at the target (m, f),
  **STOP**. WP-E5 Phase 1 failed exactly here and stopping was correct.
- **P2-c:** if the null test's false-positive rate exceeds its declared α, or the null is
  degenerate under `assert_null_usable`, **STOP**.
- **P2-d:** if the surviving reachable region requires nuisance priors tighter than those
  used in the published analyses, **STOP** — sensitivity bought with a prior is a FIT, not a
  bound.

---

### Phase 3 — Pre-registration pin

**G_3:** Phase 2 filed, no P2 condition fired, a non-empty reachable-and-open region
established on synthetic data.

**Work:** draft the `PREDICTION` v2 amendment in `PREDICTION_v2_DRAFT.md`, fixing before any
real-data statistic is computed: the (m, f) grid; the forward model and its version/commit;
the likelihood and test statistic; the covariance treatment; the validity cuts; the nuisance
parameters, their priors and the marginalization scheme; the significance threshold; the
dataset version and DOI; and the exclusion/FIT labeling rule. Submit to T0 for pinning under
the pin protocol (`scripts/pin_prediction.py`; the `prereg-pipeline` skill governs).

**Deliverable:** a pinned `PREDICTION` v2 amendment, or nothing.

**STOP CONDITION P3:** **no pin, no execution.** Gate G1 discipline is absolute — real-data
comparison code does not exist before the pin. There is no partial or provisional version of
this gate, and no agent may pin on T0's behalf.

---

### Phase 4 — Pre-registered comparison (real data)

**G_4:** a pinned `PREDICTION` v2 amendment carrying the Phase 3 text.

**Work:** run exactly the pinned analysis on the DESI DR1 P1D product already held in
`data/literature/` (SHA256 in `data/MANIFEST.md`), once. Produce the exclusion contour.
Report it as an exclusion bound with its modeling assumptions stated inline, alongside the §3
optimism ledger and the Phase 2 calibrated sensitivity.

**Deliverable:** an exclusion contour in (m, f), labeled **exclusion/FIT**, plus an
`OBSERVATIONAL_REPORT.md` table update. Interpretation prose is **T0-only** (CLAUDE.md
rule 6): draft the tables and a stub, then flag.

**STOP CONDITIONS P4:**

- **P4-a:** any deviation from the pinned text — grid, statistic, cuts, priors, threshold —
  **stops the run**. The remedy is a re-pin, never an edit. Post-hoc changes go to
  `TUNING_LOG.md` and force the FIT label (`scripts/check_tuning_log.py`).
- **P4-b:** the analysis is run **once**. A second run on the same data after seeing the
  first is a FIT and must be labeled one.
- **P4-c:** no result of this phase may be worded as confirming, supporting, or favouring the
  dual-scale hypothesis, and none may be presented as reopening F5b or Tier C. F5b is
  reversible only by its own stated trigger, which this WP does not touch.

---

## 5. Concrete public modeling options (surveyed 2026-07-27 via WebSearch/WebFetch)

**Provenance note:** the resources below were located by web search and, where indicated,
by fetching the project page or arXiv abstract **during this drafting session**. Existence
and public availability are asserted at the level of "a public repository/page under that
name was returned and read"; **suitability for this WP is not asserted** and is exactly what
Phase 1 must establish. Nothing here has been downloaded, installed, or run.

### 5.1 ΛCDM Lyman-α P1D emulators — public, but ΛCDM-shaped

- **LaCE** (`github.com/igmhub/LaCE`) — a public emulator for the 1D Lyman-α flux power
  spectrum, the one underlying the DESI P1D analysis chain. Its input basis is
  **compressed**: `Delta2_p`, `n_p` (linear amplitude and slope near a pivot) plus four IGM
  parameters `mF`, `sigT_Mpc`, `gamma`, `kF_Mpc` (project page fetched this session).
  **Critical limitation for this WP:** a two-number compression of the linear power around a
  pivot cannot represent an FDM free-streaming cutoff, which is a *shape* feature at a
  specific scale. LaCE is therefore usable — at most — as the ΛCDM **baseline arm** of a
  two-arm construction (Phase 1 route 2), never as the suppression arm.
- **cup1d** (`github.com/igmhub/cup1d`) — the public cosmological-analysis and MCMC layer
  built on LaCE. Same compressed-basis limitation; relevant as a reference implementation of
  the IGM nuisance treatment and the likelihood, not as a mixed-FDM model.
- **lym1d** (`github.com/schoeneberg/lym1d`) — a public, framework-independent Lyman-α
  likelihood (MontePython and Cobaya wrappers), with a Gaussian-process emulator over the
  Lyssa simulation suite and eBOSS DR14 P1D support. Again a ΛCDM(+ν)-shaped parameter basis.
  Relevant as the **fallback error-bar/likelihood route** already named in T0 D-e.
- **ForestFlow** (`github.com/igmhub/ForestFlow`) — public neural emulator for the *3D* flux
  power spectrum. Listed for completeness; the observable here is P1D.

### 5.2 Mixed-FDM flux-power models — the gap

- **Liu, Gong & Zhou 2026** (arXiv:2606.06969) is the paper that supplies this repo's two
  mixed-fraction anchors (f < 0.12 at 10⁻²² eV, f < 0.65 at 10⁻²¹ eV, 95%) and the
  emulator-grade standard the §3 ledger is measured against: hydrodynamic simulations with
  modified initial conditions plus a **two-stage neural emulator** (stage 1 = CDM P1D,
  stage 2 = the mixed-FDM effect relative to that baseline). **Its abstract page carries no
  code or data availability statement, and no public repository for that emulator was found
  this session.** Treat as not publicly available pending Phase 1's own search.
- **arXiv:2604.06038** (mixed fuzzy + cold DM Lyman-α signatures, hybrid Schrödinger–Poisson
  + N-body) reports a ~10% intermediate-scale effect but at a **single parameter point**
  (m₂₂ = 0.01, f_A = 0.1) in an idealized FGPA framework, with no availability statement
  found. Not a grid-spanning model.
- **Consequence, stated plainly:** on this session's survey, **no public flux-power emulator
  spanning mixed (m, f) exists.** That is the single most likely reason Phase 1 stops, and
  P1 is written so that stopping is the default rather than the exception.

### 5.3 Linear two-component transfer functions — public, and sufficient only for §5 item 3

- **axionCAMB** (`github.com/dgrin1/axionCAMB`) — the standard public CAMB modification for
  ultralight axion / mixed-DM linear observables.
- **AxiECAMB** (`github.com/Ra-yne/AxiECAMB`) — a more recent public CAMB-based code
  ("effective method") covering ultralight axions from the FDM regime (~10⁻¹⁸ eV) down to
  the frozen-dark-energy regime, reported as faster and as fixing inaccuracies in axionCAMB.
- **Use:** either retires the hand-rolled linear-interpolation `S(k;m,f)` in favour of a
  solved two-component linear calculation. **This fixes WP-E6b §5 item 3 only.** It supplies
  no flux power, no IGM physics, and no nonlinear correction, so on its own it does not move
  the 18.5×–49.3× optimism.

### 5.4 Nonlinear mixed-DM matter power — public, wrong observable, wrong mass range

- **axionHMcode** (`github.com/SophieMLV/axionHMcode`) — a public halo-model calculator for
  the **non-linear matter** power spectrum in mixed ULA cosmologies, HMCode-2020-inspired.
  Calibration ranges as reported: the basic prescription against ULA simulations for
  10⁻³³ ≤ m/eV ≤ 10⁻²¹ with axion fraction < 0.5; the "DOME" prescription for f ≤ 0.3 near
  m ≈ 10⁻²⁴·⁵ eV.
- **Two disqualifying mismatches for a P1D analysis, both of which Phase 1 must weigh
  explicitly:** (i) matter power is not flux power — the flux-power mapping is precisely
  the hydro/IGM step this WP cannot supply; (ii) the calibrated mass range **ends at
  10⁻²¹ eV**, i.e. at the *bottom* two decades of the WP grid, while the region Phase 0 is
  meant to open lies *above* 10⁻²¹ eV. Using it there is extrapolation outside the stated
  domain, which P1 forbids.

### 5.5 The data product itself — held, verified, and adequate

`data/literature/desi_dr1_lya_p1d_2026_07_27.csv` (arXiv:2505.07974 via Zenodo DOI
10.5281/zenodo.16943723, SHA256 in `data/MANIFEST.md`): 1020 rows = 12 z-bins × 85 k-bins,
QMLE baseline, SB1-subtracted, continuum-corrected, with `e_stat`, `e_syst`, `e_total`, and
the fiducial `pfid`. The **full covariance matrix ships in the same product** and is what
Phase 2 item 2 consumes. No further data acquisition is proposed by this document.

---

## 6. Resource and feasibility notes

**Runs on this VM, cheaply:**

- Phase 0 (literature re-survey) — web access only.
- Phase 2's likelihood, covariance handling, validity cuts, mock generation, closure/null
  tests, and the sensitivity re-derivation. Scale reference: the WP-E6b pre-flight's full
  260-cell grid runs in **~4 minutes** (`scripts/wp_e6b_lya_adequacy_preflight.py`), and the
  DESI P1D product plus its covariance is MB-scale, already on disk.
- Linear Boltzmann runs (§5.3) — axionCAMB/AxiECAMB are CPU-modest and buildable locally.
- Evaluating a *pre-trained* public emulator (§5.1) — inference is inexpensive; the cost is
  in the training suite, which is why sourcing rather than building is the rule.

**Needs external compute — therefore out of scope, therefore a stop condition:**

- Any hydrodynamic simulation suite spanning cosmology × IGM thermal history: millions of
  CPU-hours, specialist codes, and calibration data this program does not have. This is the
  substance of stop condition **P1**.
- Training a mixed-FDM P1D emulator from scratch: the same, plus a neural-emulator training
  program. Also **P1**.

**Data-access notes carried forward:**

- The DESI portal (`data.desi.lbl.gov`) was **unreachable from this VM** in prior sessions;
  the P1D product was obtained via Zenodo instead, and that route is already exercised and
  hashed. No new DESI acquisition is needed for Phases 0–4 as scoped.
- `data/raw/` is a symlink to the 500 GB data disk and is gitignored — never `git add` raw
  datasets (CLAUDE.md rule 2). Nothing in this proposal adds to `data/raw/`.
- Public data products only (rule 4). An author-held emulator is not a public product; see
  the P1 note.

**Effort shape, for T0's cost calculus:** Phase 0 is hours. Phase 1 is days of search and
reading, and its most likely outcome is a stop. Phase 2 is the substantial engineering phase
and only begins if Phase 1 returns a real model. This ordering is deliberate: the cheap
phases are the ones most likely to end the WP.

---

## 7. Open questions for T0

- **Q1 — author-held models.** If Phase 1 finds that the only adequate forward model is
  author-held rather than public, is a request to the authors in scope, given CLAUDE.md
  rule 4's public-products-only discipline and its prohibition on phrasing anything as
  collaboration or endorsement? Default absent a ruling: **P1 STOP**.
- **Q2 — the significance threshold.** The pre-flight used σ_equiv ≥ 2 with a deliberately
  rough one-d.o.f. convention. Phase 2 should fix a defensible threshold (and a multi-d.o.f.
  treatment) before the pin. T0 to confirm 2σ, or set another.
- **Q3 — reproduction tier.** Should v2 carry an explicit reproduction arm against the
  Liu/Gong/Zhou anchors (a check that the calibrated pipeline recovers their published
  bounds at their two masses) as a Phase 2 acceptance criterion? It is the strongest
  available external validation, and it costs a run.
- **Q4 — v1's Q4, still open.** Should the mass interval be bounded by Appendix A.4.3's
  robustness protocol (β interval over the aᵢ box) rather than by the FDM-motivated
  placeholder? Unanswered since the v1 draft; it belongs to the Phase 3 pin.
- **Q5 — stopping posture.** If Phase 2 returns a non-empty but narrow region — say a handful
  of cells at f ≳ 0.4 above 10⁻²¹ eV — is that worth Phases 3–4, or is the honest call to
  file it as a sensitivity statement and stop? A pre-agreed answer prevents the decision
  being made after seeing the number.

---

## 8. Decision requested

T0 to: **(a)** approve, amend, or reject this proposal as the scope of WP-E6 v2; **(b)**
answer Q1–Q5; **(c)** if approved, authorize **Phase 0 only** — the literature re-survey —
with entry to each later phase requiring the prior phase's filed artifact and no stop
condition having fired.

Approval of this document is **not** approval to execute Phase 1 or beyond; each gate is a
separate step, and Phase 3's pin is T0's alone.

---

**This proposal awaits T0 sign-off; no phase executes before that.**

Generated-by: Claude Opus 5 (Stream 3 agent, WP-E6 v2 proposal drafting under T0 D-f) |
Verified-by: pending T0 — this is a proposal, not a result; its factual dependencies are
`docs/WP_E6B_LYA_ADEQUACY_PREFLIGHT_2026_07_27.md` (§2, §3, §5, §7),
`docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md` §4, `data/MANIFEST.md`, CLAUDE.md rules 1–6 and
the post-F5b/F6 ledger, and a WebSearch/WebFetch survey of public emulator and Boltzmann-code
resources conducted 2026-07-27 (§5, with availability caveats stated inline) |
Reviewed-by: pending T0 (Xavier)
