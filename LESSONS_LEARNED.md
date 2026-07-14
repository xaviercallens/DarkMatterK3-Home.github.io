# Lessons Learned: V5 Deep Review & Pivot (2026-07-14)

**Date**: 2026-07-14  
**Context**: Scientific review of V5 Phase 1 discovered fabricated constants; strategic pivot to s₁₀

---

## Critical Lessons

### L1 — Never Trust User Guidelines for Mathematical Constants

**What happened**: The V5 guideline document asserted Cooper s₇ sequence as
[1, 13, 271, 6721, 184561, …] without citing OEIS. I implemented this
directly. Verification against OEIS revealed: **the sequence matches nothing
in the database**. True A183204 = [1, 4, 48, 760, …].

**Lesson**: Every numeric constant must be verified against an external
authority *before* entering the code. For OEIS sequences, fetch the b-file
(example: `https://oeis.org/A183204/b183204.txt`) and cross-check at build
time or test time.

**Action for future**: WP-A guardrails in `V5_RIGOROUS_THEORY_PLAN.md` mandate:
- All sequence terms from: recurrence formula (exact integer arithmetic) OR fetched b-file (logged with hash)
- No hardcoding of raw values from unverified sources
- Automated CI gate: compare computed terms vs external authority

### L2 — Convergence Radius Is Not a Dial to Turn

**What happened**: I normalized Cooper s₇ coefficients by μ=25.869, computed
truncated sums at z=0.95, and reported them as convergent. But μ was an
underestimate of the true growth rate λ=27, so the series was actually
*divergent* at z=0.95 (partial sums grew unbounded).

**Lesson**: The radius of convergence for a power series is a mathematical
fact, not a design choice. For Π₀(z) = Σ a(n) z^n with a(n) ~ λⁿ, the radius
is *exactly* 1/λ. Do not guess; compute λ from the recurrence's characteristic
equation.

**Action for future**: WP-A2 (Frobenius basis) includes verification that the
mirror-map q-expansion has *integral* coefficients — this is the same rigidity
check used to falsify s₇ in Phase VIII, applied here as a proof of consistency.

### L3 — A Statistic That Only Measures Normalization Is Not A Discovery

**What happened**: The Δ_s7 metric reported as the max |FFT difference|
turned out to be 100% the k=0 (DC) mode — a global normalization offset with
zero spatial content. Every "discovery" was this artifact.

**Lesson**: Before computing a statistic, verify it has the expected null
behavior. On synthetic uniform-density data (no structure), Δ should be ~0
(or stable at a small level). If Δ is instead dominated by a single mode, the
metric is measuring something other than what was intended.

**Action for future**: The revised estimator (`v5_estimator_s10.py`) works
on zero-mean contrasts (DC removed by construction) and compares shell-averaged
Fourier amplitudes — this is a structural fix. But before deploying any
metric on real data, run it on matched null mocks and verify the null
distribution (WP-C2).

### L4 — Circular Tests Prove Nothing

**What happened**: The "Filament Test" design (Phase 2.1) would have been
circular: any monotone kernel amplifies overdense regions; therefore high Δ
at filament intersections is *guaranteed* by construction, not evidence of
K3 physics.

**Lesson**: Model-selection tests must be *adversarial*. The Cooper hypothesis
only has content if data *prefers* the s₁₀ kernel over:
  (a) derivative-matched generic kernels (same derivatives at mean density), and
  (b) sibling K3 families (s₇ if we rebuild it, t₁₀₃)

Without this discrimination, the result is null (or unfalsifiable).

**Action for future**: WP-B3 (Identifiability Harness) implements the
adversarial test using ΔAIC (or mock-based likelihood) to rank kernels. Only
when s₁₀ beats controls at ΔAIC ≥ 10 can we claim discovery.

### L5 — Synthetic Data + Discovery Files = Disaster

**What happened**: `real_euclid_worker.py` injects artificial clusters into
synthetic fallback data ("pour avoir de superbes découvertes") and the Phase 1
pipeline wrote these to `discoveries_v5_cooper.json` indistinguishably from
real results. The discovery store became part data, part fiction.

**Lesson**: Data provenance must be a hard gate at the point of persistence.
Fallback data must be statistically featureless (flat null) so it can serve
as a null model, not a discovery generator.

**Action for future**: WP-C1 (Provenance Gate, `v5_provenance_gate.py`) blocks
any synthetic-provenance record from entering a discoveries file via RuntimeError.
This is *structural* — not a linter, not a review practice — because the bug
cuts at the heart of evidentiary integrity.

---

## Institutional Practices to Lock In

### P1 — No Constant Without Provenance

Every numeric value entering the codebase must come from one of:
1. An explicit recurrence formula (tested for exactness)
2. A closed-form computation (code + docstring)
3. A fetched external authority (OEIS b-file, survey documentation) with
   - URL logged in code or test
   - Date of fetch recorded
   - Hash or range of terms cross-checked

**Implementation**: WP-A guardrails in the theory plan.

### P2 — Tests Are Hierarchical, Not Flat

- **Smoke test**: "Code runs without crashing" (necessary, insufficient)
- **Scientific test**: "Code produces the *correct* output on known inputs"
  - For sequences: term-by-term match vs independent derivation
  - For metrics: null behavior on flat data, signal recovery on synthetic injections
  - For estimators: bias/variance on matched mocks

**Implementation**: Every WP below Haiku-tier has a Definition of Done with
scientific (not just functional) criteria.

### P3 — Pre-register Before Unblinding

All analysis choices (k-band, mock count, ΔAIC threshold, tomography bins,
look-elsewhere convention) are frozen in git *before* applying them to real
data or computing significances. Deviations are documented in `DEVIATIONS.md`.

**Implementation**: WP-C4 (Pre-registration & Blinding).

### P4 — Sibling Families as the Control

The Cooper hypothesis is testable *only if* data can discriminate between:
  - s₁₀ (level-10 K3)
  - s₇ (level-7 K3) if rebuilt cleanly
  - t₁₀₃ (level-∞/∞ K3?)
  - generic derivative-matched controls

If all fit equally (ΔAIC < 2), the result is null. This is not a weakness; it
is how the hypothesis acquires falsifiability.

**Implementation**: WP-A3 (Sibling Kernels) and WP-B3 (Identifiability).

---

## Skills Developed This Session

1. **Deep scientific review**: identifying fabricated constants via OEIS
   verification, diagnosing divergent series, spotting circular logic
2. **Numerical rigor**: certified tail bounds, growth-rate computation,
   separation of ansatz from derivation
3. **Institutional governance**: gates (G1–G5), provenance barriers,
   work-package routing by epistemic tier
4. **Recovery under defect**: pivoting from s₇ to s₁₀, salvaging the program
   while retiring the false headline

---

## What Worked Well

- The existing recurrence-verification work in
  `hypothesis_comparison_t103_cooper.py` was sound and became the pivot point
- Executed code to verify claims (OEIS fetch, partial-sum test, FFT-mode check)
  rather than reasoning abstractly
- Clear differentiation between the hypothesis (worth developing) and a
  particular mathematical realization (s₇, contaminated)
- Documentation trail: review, plan, gates, lessons — all in the repo

---

## What Failed

- Not verifying user-supplied constants against external authority *during*
  Phase 1 implementation
- Misreading the FFT metric without sanity tests on synthetic data first
- Circular test design in Phase 2 (blocked now via WP-B3)
- Synthetic data contamination (blocked now via WP-C1)

---

## Summary

**Pivot to s₁₀ is the right move**: the hypothesis is sound, only the first
implementation was poisoned. The program survives by:
1. Vetoing the fabricated constants (found via OEIS check)
2. Adopting a certified kernel for s₁₀ (built this session)
3. Committing to adversarial model selection (WP-B3)
4. Installing structural gates (WP-C1, C4, C5)
5. Documenting all ansatze and their parameters (WP-B1)

The next phase is implementation of the rigorous theory plan. All Haiku-tier
packages (mechanical, verifiable) are routed to the fastest channel. Sonnet
packages (requiring derivation and judgment) are detailed and documented for
expert designers.
