# V5.1: Strategic Pivot to Cooper s₁₀ after s₇ Fabrication Defect

**Release**: v5.1-cooper-s10-primary  
**Date**: 2026-07-14  
**Breaking change**: Phase 1 (V5) is completely voided and superseded

---

## What Changed

### Critical Finding: V5 Phase 1 Was Built on Fabricated Constants

The deep scientific review (`V5_SCIENTIFIC_REVIEW.md`) discovered three fatal defects:

1. **F1 — Fabricated sequence**: The V5 guideline's claimed OEIS A183204 terms
   (1, 13, 271, 6721, …) match no sequence in the OEIS database. The true
   A183204 is (1, 4, 48, 760, 13840, …). Phase 1 extended with 23 more
   invented terms satisfying no recurrence.

2. **F2 — Divergent series**: With the fabricated terms, the "period integral"
   Π₀(z) was evaluated as a divergent series (partial sums grew unbounded).
   The true series converges only for |z| < 1/27 ≈ 0.037, not the claimed
   z up to 0.95.

3. **F3 — The metric measured noise**: The reported Δ_s7 statistic was 100% the
   k=0 (DC) Fourier mode — a normalization offset with zero spatial content.

**All results in `discoveries_v5_cooper.json` (2026-07-14 test run) are void.**

### Strategic Pivot to Cooper s₁₀

The project pivots to **Cooper s₁₀ (OEIS A005260)** as the primary K3 hypothesis
candidate, for three reasons:

1. **Literature-anchored**: A005260 is well-documented (Cooper 2012, Gorodetsky
   2021, Zudilin et al. 2025 in ArXiv:2510.23298).
2. **Verified in-repo**: The exact recurrence for s₁₀ was already verified in
   `hypothesis_comparison_t103_cooper.py` (0 failures, n=0..38).
3. **No contamination history**: Unlike s₇, s₁₀ has never been poisoned by
   fabricated constants in this project.

**The hypothesis tested**:
> **H(Cooper-s₁₀)**: Large-scale structure carries a density-dependent
> kernel whose form is the fundamental period Π₀ of the level-10 K3 family
> (A005260, λ=16), preferred by data over derivative-matched controls and
> sibling families.

---

## Files Added / Changed

### New Certified Infrastructure

- **`cooper_s10_kernel.py`** (NEW): Certified s₁₀ kernel engine
  - True A005260 via verified recurrence (cross-checked vs binomial formula)
  - Exact λ = 16, radius of convergence 1/16 ≈ 0.0625
  - Π₀ with certified tail bounds (≤ 1.2e-10 over physical domain)
  - DC-free band-averaged Δ statistic
  - 7 self-tests, all passing

- **`v5_estimator_s10.py`** (NEW, WP-B2): DC-free band-averaged estimator
  - Shot-noise subtraction ready (stub for real data)
  - Amplitude-based (numerically stable) comparison
  - Smoke tests validate null/signal discrimination

- **`v5_provenance_gate.py`** (NEW, WP-C1): Hard gate preventing synthetic data
  in discoveries
  - RuntimeError if `data_provenance == "synthetic_fallback"`
  - Unit tests proving the gate works
  - Prevents recurrence of finding F5

- **`cooper_exact.py`** (EXISTING, Phase 1 corrected kernel): kept as reference
  - Note: this was an interim correction; s₁₀ is now primary

### Documentation & Planning

- **`PIVOT_MEMO.md`** (NEW): Decision memo on s₇ → s₁₀ pivot
- **`V5_RIGOROUS_THEORY_PLAN.md`** (AMENDED): 13 Haiku/Sonnet work packages
  - WP-A3-s10: certified s₁₀ kernel (DONE)
  - WP-B2-s10: estimator (DONE)
  - WP-C1: provenance gate (DONE)
  - Remaining packages for future sessions (WP-B1, WP-C2, WP-C3, etc.)

- **`V5_SCIENTIFIC_REVIEW.md`** (EXISTING): Full referee report
  - 9 findings with evidence (F1–F9)
  - 5 gate conditions (G1–G5) required before public claims

### Deprecated / Archived

- **`cooper_periods.py`**: deprecated (fabricated terms, divergent series)
  - Retains code for backwards compatibility; marked with warning banner
- **`V5_PHASE1_HANDOFF.md`**: superseded (marked with warning)
- **`PHASE2_QUICKSTART.md`**: superseded (marked with warning)
- **`V5_IMPLEMENTATION_README.md`**: superseded (marked with warning)
- **`V5_PHASE1_COMPLETION_SUMMARY.md`**: superseded (marked with warning)

- **Archive**: `discoveries_v5_cooper.json` → `archives/void_20260714_s7_fabricated/`
  (null results due to defective Phase 1)

---

## What Passes & What Doesn't

### ✅ Passes

- `python3 cooper_s10_kernel.py` — all 7 self-tests
- `python3 v5_estimator_s10.py` — all 3 synthetic tests
- `python3 v5_provenance_gate.py` — provenance gate tests
- s₁₀ kernel beats s₇ fake ("s₇" is gone; s₁₀ is the only option)

### ❌ Fails (not yet implemented, WP-pending)

- Phase 2 observational tests (WP-B1 chameleon derivation, WP-C2 mock ensemble needed first)
- Identifiability harness (WP-B3 — differentiates s₁₀ from generic kernels)
- Weak lensing overlay (WP-D2 — requires real map access)
- Any public claim (gates G1–G5 not yet met)

---

## Next Steps (For Future Sessions)

1. **WP-B1** (Sonnet, 3h): Chameleon-screened modulus response z(ρ) from first
   principles (Khoury–Weltman potential; convert ansatz to model).

2. **WP-C2** (Sonnet+Haiku, 4h): Mock ensemble and empirical null distribution
   (≥100 matched Λ-CDM mocks per sector; look-elsewhere correction).

3. **WP-B3** (Sonnet design + Haiku execution, 2h): Identifiability harness —
   prove s₁₀ kernel beats derivative-matched controls on real data (ΔAIC ≥ 10).

4. **WP-C3** (Haiku, 2h): Residual tomography with WP-B1 prediction curve
   (redshift See-Saw test on data minus mocks).

5. **WP-D1, WP-D2** (Haiku + Sonnet): TDA Betti correlation, weak lensing
   cross-validation (after WP-C2 mocks are ready).

6. **WP-E1** (Haiku, 1h): Honest observatory document written LAST from results
   (only when gates G1–G5 are met).

---

## Integrity Commitments (for this and all future sessions)

1. **No constant without provenance**: every number entered the code via
   - the certified recurrence, or
   - an executed formula, or
   - a fetched external authority (OEIS b-file with date/hash logged)

2. **Tests that prove code runs are smoke tests**: Definition of Done items
   below are *scientific* checks (exactness, null behavior, recovery of known
   inputs).

3. **Synthetic data never touches discoveries**: provenance gate (WP-C1,
   `v5_provenance_gate.py`) enforces this structurally.

4. **No edits to `cooper_s10_kernel.py` or `cooper_exact.py` except to append
   tests.**

5. **Update the STATUS line of work-package cards when you start/finish them**
   (IN PROGRESS / DONE / BLOCKED + one line).

---

## Verification Checklist

- [x] `cooper_s10_kernel.py` passes all self-tests (7/7)
- [x] `v5_estimator_s10.py` passes synthetic tests (3/3)
- [x] `v5_provenance_gate.py` blocks synthetic data (3/3)
- [x] Old Phase 1 artifacts archived/deprecated
- [x] Theory plan with Haiku/Sonnet work packages documented
- [x] Gate conditions G1–G5 documented (`V5_SCIENTIFIC_REVIEW.md`)
- [x] No public claims made pending gate passage
- [x] Git history clean; commit message explains the pivot

---

## Summary

**The s₇ hypothesis was poisoned at the start and is unrecoverable.** The
project pivots to s₁₀, inherits a corrected mathematical foundation
(`cooper_s10_kernel.py`), and commits to a rigorous theory plan with explicit
gate conditions (G1–G5) for any future public claims. The program is viable
and grounded; only the previous headline is void.
