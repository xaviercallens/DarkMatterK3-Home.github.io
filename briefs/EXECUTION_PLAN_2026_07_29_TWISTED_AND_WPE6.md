# Execution Plan 2026-07-29 — Twisted-Weierstrass Primary Route + WP-E6 Sweep Unblock

**Authority:** T0 countermand & directives 2026-07-29 (S2 `briefs/T0_COUNTERMAND_R2_2026_07_29.md`
— binding; read it and its §B annotations before executing anything here).
**Audience:** T1 (Sonnet/Gemini Pro) and T2 (Haiku/Gemini Flash) agents executing
autonomously. Each WP below is self-contained: inputs, steps, Definition of Done (DoD),
validation criteria, escalation triggers. The coordinator (Fable 5) verifies every DRAFT
before promotion — **no WP promotes its own output.**

## §0 Global execution rules (binding for every WP)

1. **Producer ≠ verifier.** Deliver DRAFT, never self-promote. Verification is a separate pass.
2. **Commits:** only specifically named new/changed files (`git add <file>...`, never
   `git add -A`). Before any commit in S2: `git status -sb` + `git branch -vv`; work lands on
   `main` only, and only if the checkout is clean of others' work first.
3. **No `isolation:worktree`** for S2 (shared checkout, mechanism unreliable — see 07-28
   session log) or for anything touching S3 `phase1_work/` (gitignored, absent in worktrees).
4. **Math WPs (S2): exact symbolic computation only** (sympy integers/rationals; no floats
   in lattice/divisor arithmetic). Every numeric claim traces to checker output.
5. **Epistemic guardrails skill applies to all prose.** Specifically: NO Kodaira labels from
   Picard–Fuchs exponents ever (S2 ledger rule 3, E-008/E-009); finite-order checks reported
   `PASS(N)`; Tier C sentences carry conjecture markers; provenance footer on every file.
6. **Environment:** venv `/home/callensxavier_gmail_com/venv` (py3.10.12). NO mpi4py ever.
   For any sim_spectra work: `export DESIMODEL=<S3>/phase1_work/agent3_synthetic/desimodel_data_test`.
7. **Escalation = write a brief in `briefs/` + STOP.** Never work around a blocker silently;
   never fabricate a fallback result. Triggers are listed per-WP.
8. **Route A is CLOSED** (S2 ledger entry 6). If any task seems to require strict-pullback or
   G1-b work, that is a misreading — stop and escalate.

## §1 Dependency graph

```
WP-TW0 (T2, S2)  ──┐  independent, parallel
WP-TW1 (T1, S2)  ──┼─ independent, parallel
WP-P1  (T1, S1)  ──┘  independent, parallel

WP-E6-PIN (T1, S3) ──> [T0 pins amendment] ──> WP-E6-SWEEP
WP-E6-P2A (T1, S3) ──┬────────────────────────> WP-E6-P2B (T1, S3) ──> WP-E6-SWEEP
WP-E6-P2C (T2, S3) ──┴────────────────────────────────────────────────> WP-E6-SWEEP
```
PIN, P2A, P2C may start immediately and run in parallel. P2B needs P2A's covariance.
SWEEP needs ALL of: pinned amendment, P2A, P2B, P2C.

---

## WP-TW0 — In-house verification of ℓ = 2 (S2, T2, ~hours)

**Goal:** verify the ratified Tier B-external value ℓ = 2 (Hodge-bundle degree of the
cooper_s7 family) by exact in-house computation; characterize the ∞ point in exponent
language as a by-product.
**Inputs:** L₂/L₃ operator definitions already in S2 (start from `check_U1_lattice.py` and
the checkers' operator sources — read the source, not certificates); Tier-A fact
L₃ = Sym²(L₂); singular loci {−1, 1/27} are order-2 elliptic points (ledger rule 3).
**Steps:**
1. Extract L₂'s Riemann scheme: local exponents at z = −1, 1/27, ∞ (exact sympy `indicial`
   computation from the operator itself, not from any document).
2. Compute deg ℒ_ell for the L₂ elliptic realization by exponent bookkeeping; state the
   formula used and each term's origin.
3. Derive deg ℒ_K3 via the Sym² relation, with an EXPLICIT section addressing whether the
   order-2 orbifold points contribute a fractional/integral correction under ⊗2 (this
   sub-step is the audit's flagged gap — do not wave it through).
4. Record the ∞-point exponents verbatim. **No Kodaira classification** — exponent values
   and monodromy order (finite n / infinite) only. This settles the 07-28-vs-07-29
   Deep Think discrepancy on the ∞ point.
**Deliverables:** `checkers/check_TW0_hodge_degree.py`, certificate
`data/certificates/TW0_hodge_degree_cooper_s7.json`, DRAFT brief
`briefs/TW0_HODGE_DEGREE_RESULT_2026_07_29.md`. ≥2 negative controls (e.g. a deliberately
perturbed operator whose degree computation must land ≠ 2; an operator with a known degree).
**DoD:** checker runs clean from a fresh shell; controls PASS; brief states ℓ with full
derivation chain and the orbifold-correction analysis; committed as DRAFT (named files).
**Validation (coordinator):** re-run checker + controls; hand-check the exponent sums.
**Escalation triggers:** computed ℓ ≠ 2 (STOP — F6 disclosure path, T0 escalation, do NOT
"reconcile"); orbifold correction found nonzero; exponents at {−1, 1/27} inconsistent with
order-2 elliptic points.

## WP-TW1 — Two-E8 degree-feasibility check, twisted route gate (S2, T1)

**Goal:** T0 Action 1 — decide PASS/FAIL: can f ∈ H⁰(−4K_B₃), g ∈ H⁰(−6K_B₃) support TWO
E8 divisors (per-divisor Tate orders v(f) ≥ 4, v(g) = 5, v(Δ) = 10, Δ = 4f³+27g²) on
standard 3D bases? FAIL on all bases = a documented No-Go; PASS names the surviving bases.
**Inputs:** G0 certificate (NS ⊇ E8(-1)⊕E8(-1) — the constraint's origin);
S3 `DEEPTHINK_DEBRIEF_AUDIT_2026_07_29.md` §A5 (adopted check + correction: **deg Δ = 48 on
P³, not 144** — the verbatim debrief's 144 is a recorded error, do not propagate it).
**Steps:**
1. Formalize the necessary condition exactly (this is part of the deliverable, not given):
   for base B₃ with candidate E8 divisors D₁, D₂ of classes [D₁], [D₂], the divisibility
   requirements 4[D₁]+4[D₂] ≤ [−4K], 5[D₁]+5[D₂] ≤ [−6K], 10[D₁]+10[D₂] ≤ [−12K] in the
   effective cone, PLUS the collision analysis of step 3.
2. Base ladder, in order: (a) P³; (b) P¹×P²; (c) P¹-bundles over P² (P(O⊕O(n)) for small n —
   include these: two *disjoint* sections are exactly the geometry F-theory's E8×E8
   heterotic duals use, and they are the physically canonical candidates).
3. **Collision/non-minimality analysis is load-bearing, not optional:** on P³ any two
   surfaces intersect, so D₁∩D₂ ≠ ∅ and vanishing orders ADD on the intersection — check the
   non-minimality/(4,6)-type conditions there; on P¹-bundles check the disjoint-section
   configuration separately. A base "passes" only if some configuration survives both the
   degree bounds and the collision analysis.
4. Controls: ≥1 positive (a configuration classically known to admit E8×E8 — expected: the
   disjoint-section P¹-bundle geometry) and ≥2 negative (e.g. artificially shrunken bounds
   that must FAIL; three E8's where two barely fit).
5. Per-base certificate + one summary verdict table.
**Deliverables:** `checkers/check_TW1_two_e8_feasibility.py`, certificates
`data/certificates/TW1_two_e8_<base>.json`, DRAFT brief
`briefs/TW1_TWO_E8_FEASIBILITY_RESULT_2026_07_29.md`.
**DoD:** boolean verdict per base with the certifying inequality chains printed exactly;
controls PASS; explicit statement that this is a NECESSARY-condition screen (a PASS does not
assert the M-polarized family exists on that base — that is the next, separate WP).
**Validation (coordinator):** re-run controls; hand-recompute the P³ bounds (f: 16, g: 24,
Δ: 48) and one collision computation independently.
**Escalation triggers:** ALL bases FAIL (that's the No-Go — STOP after documenting, T0 will
rule on publication framing); ambiguity in the non-minimality criterion that the literature
in `refs/` doesn't resolve (do not guess a convention — escalate with the two candidate
readings).

## WP-P1 — Stream 1 paper drafting kickoff (S1, T1)

**Goal:** T0 Action 2 — draft for *Experimental Mathematics* per resolved PLAN.md §5.
**Inputs:** S1 `PLAN.md` §5 (ALL five framing decisions — read before writing a word);
existing 33pp/10-section skeleton (`5bd0916` lineage); S2 ledger for every claim's tier.
**Steps:**
1. Draft in this order: (i) L₃ = Sym²(L₂) (Tier A, kernel-proven — may state as fact, noting
   any `native_decide`/axiom dependence per guardrails rule 4); (ii) monodromy/lattice
   sections; (iii) U1 / T ≅ U⊕⟨14⟩ (Tier B, double-verified); (iv) G0 NS-genus certificate
   (Tier B, three independent lineages — cite the S2 certificate + decision log).
2. G1/Calabi-Yau narrative: PLACEHOLDER section with a dated stub only — do not draft until
   WP-TW1 resolves (T0 directive).
3. AI-acknowledgment paragraph: copy VERBATIM from PLAN.md §5.3 — the wording is T0-mandated,
   non-negotiable; do not paraphrase.
4. ρ = 19 / T = 3: conditional Tier-B proposition phrasing everywhere (never "proven").
   Internal manuscript citations hash-pinned.
5. Run the epistemic-guardrails review checklist over every section before committing.
**Deliverables:** section drafts committed to S1 (named files per the paper's existing
structure), DRAFT brief `briefs/P1_DRAFT_STATUS_2026_07_29.md` listing what's drafted, what's
stubbed, and every tier-sensitive sentence flagged for review.
**DoD:** sections (i)–(iv) drafted and building (if LaTeX: compiles; if Markdown: renders);
guardrails checklist run and recorded; G1 section stubbed not drafted.
**Validation (coordinator):** guardrails re-check on the diff; verify AI-ack is byte-identical
to PLAN.md §5.3; spot-check three citations' hash pins.
**Escalation triggers:** any claim whose tier is unclear (add TIER_LEDGER.md
`RULING-REQUESTED` entry + use lower-tier phrasing meanwhile); any pressure to state ρ=19
unconditionally.

## WP-E6-PIN — PREDICTION v2 amendment draft (S3, T1, blocks the sweep)

**Goal:** implement T0 Action 4 *through* S2 ledger rule 5: the sweep enters only via a
pre-registered PREDICTION v2 amendment under the pin protocol.
**Steps:** draft the amendment specifying: the pinned 56-cell grid (8 masses × 7 fractions,
pin `27cff4a` — cite, don't restate numbers); data = DESI DR1 Lyman-α P1D via the LIVE
ANALYSIS_PROTOCOL; statistic = Hartlap-corrected 16×16 covariance chi² with the four
nuisance parameters (taueff bound documented as PRIOR-BOX per T0 ruling 2026-07-28);
output labels = **exclusion/FIT only, never TEST**; and an explicit F5b guard sentence:
results are standalone (m, f) constraints from Lyman-α data — no K3-derived observable is
claimed or implied (Tier C block stands).
**Deliverables:** `briefs/PREDICTION_V2_AMENDMENT_DRAFT_2026_07_29.md` (DRAFT).
**DoD:** every analysis choice in the amendment traces to an already-LIVE/pinned document
(no new free choices smuggled in); F5b guard present.
**Validation:** coordinator cross-checks against ANALYSIS_PROTOCOL + grid pin; **then T0
pins it — the sweep may not start before the pin.**
**Escalation triggers:** any analysis choice NOT already fixed by a LIVE document (list it,
don't pick).

## WP-E6-P2A — Hartlap covariance build (S3, T1)

**Goal:** the 16×16 mock covariance per ANALYSIS_PROTOCOL Part A.
**Inputs:** LIVE `ANALYSIS_PROTOCOL` (S3, `7d0b2ce` lineage); timing GO
(`WP_P2t_DESISIM_TIMING_2026_07_28.md`: N=200 ≈ 48 s core pipeline); `DESIMODEL` env var
(§0.6); venv desisim; 16 k-bins per `emu_predict.py` `K_BINS`.
**Steps:** generate N=200 independent mock realizations (full pipeline INCLUDING
sim_spectra — the 07-28 scope-gap lesson: get_lya_skewers alone is not the pipeline);
compute the 16×16 sample covariance; apply the Hartlap factor with N=200, p=16
((N−p−2)/(N−1) = 182/199); persist inputs/outputs.
**Deliverables:** `pipeline/wp_e6_covariance.py`, `data/derived/wp_e6_covariance_2026_07_29.json`
(covariance + Hartlap-corrected inverse + generation metadata), DRAFT brief
`briefs/WP_E6_P2A_COVARIANCE_RESULT_2026_07_29.md`.
**DoD:** matrix symmetric; positive-definite (report min eigenvalue, exact check on the
stored matrix); Hartlap factor printed with its formula; stability check reported
(covariance from a random N=100 subsample vs full N=200 — report max relative diagonal
drift, flag if > 20%); wall-clock reported vs the 48 s benchmark.
**Validation (coordinator):** re-verify PD + Hartlap arithmetic; check realization
independence (seeds recorded, all distinct).
**Escalation triggers:** non-positive-definite; runtime > 10× benchmark; any desisim import
or DESIMODEL failure (report, don't work around).

## WP-E6-P2C — Masking fix implementation (S3, T2)

**Goal:** fix BOTH `compare_p1d.py` bugs (zero-fill edge discontinuity + per-spectrum mean
over zero-filled pixels) and implement the mock-calibrated multiplicative window correction.
**MANDATORY first step:** fetch/read the actual Ravoux et al. 2023 paper (MNRAS 526, 5118 /
arXiv:2306.06311) and verify the correction recipe against the paper itself — the recipe
currently in ANALYSIS_PROTOCOL came from a WebSearch summary and is explicitly flagged
unverified. Record section/equation numbers used. If the portal/fetch fails: escalate, do
not implement from the summary.
**Steps:** implement Bug-2 fix + window correction (reusing P2A's mock ensemble for
calibration — no extra generation cost); NO gap interpolation (T0 ruling 2026-07-28);
add regression tests; run existing `pytest pipeline/tests/`.
**Deliverables:** patched `pipeline/compare_p1d.py` (or successor), new tests, DRAFT brief
`briefs/WP_E6_P2C_MASKING_FIX_2026_07_29.md` with before/after P1D comparison on one mock.
**DoD:** both bugs demonstrably fixed (test that fails on old code, passes on new); full S3
test suite green; paper-verified recipe with equation citations.
**Validation (coordinator):** re-run tests; check the correction is multiplicative-window
form, not interpolation.
**Escalation triggers:** paper recipe disagrees with the ANALYSIS_PROTOCOL summary (report
the delta — protocol is LIVE, changing it needs T0); any test regression.

## WP-E6-P2B — Nuisance profiling (S3, T1, AFTER P2A)

**Goal:** ANALYSIS_PROTOCOL Part B — extend the working `integration_iminuit.py` chi²
pattern to P2A's Hartlap-corrected covariance, single z=4.2 term (12 dof/cell), profiling
the four nuisance parameters (`taueff` — documented prior-box (0.3, 1.8); `zrei`, `ha`, `hs`
— LHS trained-support bounds).
**Deliverables:** `pipeline/wp_e6_profile.py`, DRAFT brief with a null-cell sanity result
(profiled chi² at the null mass cell must be statistically unremarkable — report it).
**DoD:** profiling converges on all 4 params across a 3-cell test set (null + max-contrast +
one random cell); bounds provenance documented per-parameter in the code.
**Validation (coordinator):** re-run the 3-cell test; check no parameter pins at a bound
without a warning being emitted.
**Escalation triggers:** convergence failures; best-fit persistently at a prior-box edge
(that's a finding, not a nuisance — escalate).

## WP-E6-SWEEP — 56-cell exclusion sweep (S3, T1, LAST — needs pin + P2A + P2B + P2C)

**Goal:** the pre-registered sweep over the pinned grid, per the PINNED amendment.
**Steps:** run profiled chi² per cell; produce the exclusion/FIT table + rendered figure
(load `dataviz` skill before plotting); label every output artifact exclusion/FIT.
**Deliverables:** `data/derived/wp_e6_sweep_results_2026_07_29.json`, figure(s), DRAFT brief
`briefs/WP_E6_SWEEP_RESULT_2026_07_29.md`.
**DoD:** all 56 cells computed with per-cell convergence status; f=0 column behaves as the
null (consistent with the byte-identity control); no sentence anywhere in the outputs links
results to K3/dark-sector predictions (F5b guard); labels correct.
**Validation (coordinator):** re-run 3 spot cells fresh; check label discipline + F5b guard;
verify figure numbers match the JSON.
**Escalation triggers:** amendment not yet pinned (DO NOT START); any cell result that would
tempt "TEST" language.

---
Generated-by: Fable 5 (coordinator), implementing T0 directives 2026-07-29 | Verified-by:
every parameter above traces to a LIVE/pinned document named inline (grid pin `27cff4a`,
ANALYSIS_PROTOCOL, timing brief, G0 certificate, audit 2026-07-29) | Reviewed-by: T0 Y
(executes T0's §3 Actions 1/2/4 under the §B annotations of the countermand record)
