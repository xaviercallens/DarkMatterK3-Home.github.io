# Strategic Pivot: Cooper s₁₀ as Primary Hypothesis

**Date**: 2026-07-14  
**Trigger**: V5 Scientific Review finding F1 (s₇ sequence fabricated)  
**Decision**: promote **Cooper s₁₀ (OEIS A005260)** to primary K3 candidate  
**Rationale**: s₁₀ is literature-anchored, verified recurrence in-repo, no contamination history

---

## Why s₁₀ (not s₇, not t₁₀₃)

| Candidate | λ | Status | Risk |
|-----------|---|--------|------|
| **s₇ (A183204)** | 27 | Fabricated terms in Phase 1; true sequence is sound but hypothesis poisoned by implementation defects | **RETIRED** |
| **s₁₀ (A005260)** | 16 | Verified recurrence in `hypothesis_comparison_t103_cooper.py`; b-file available; simple closed form a(n)=Σₖ C(n,k)⁴; no prior pipeline contamination | **PRIMARY** |
| t₁₀₃ (A276536) | 62.27 | Novel in-session discovery; held-out to n=62; Lean-proved n=0..20; too exotic for first test | backup |

s₁₀ is the **safest path to a defensible result**: if the hypothesis survives with s₁₀, the discovery is clean; if it fails, the null is earned.

---

## Execution Plan (Haiku Tier, This Session)

1. **WP-A3-s10**: Implement certified s₁₀ kernel in a new module `cooper_s10_kernel.py`
   - Fetch OEIS b-file for A005260; assert term-by-term equality for all available
   - Derive exact λ = 16 from verified recurrence (P1 leading = 12, P0 leading = 64)
   - Implement `kernel_s10(rho, rho_scale)` matching `cooper_exact.py` API
   - Self-test: monotone ratios, Π₀ with certified tails, DC-free band metric
   - **Definition of Done**: `python3 cooper_s10_kernel.py` passes all tests; git shows b-file fetch

2. **WP-C1**: Provenance gate — ensure fallback data never touches discovery files
   - Add `data_provenance: "real_survey" | "synthetic_fallback"` to every result
   - Hard gate: RuntimeError if synthetic provenance written to discoveries
   - Remove cluster-injection block from `real_euclid_worker.py`
   - Quarantine void `discoveries_v5_cooper.json` to `archives/void_20260714_s7_fabricated/`
   - **Definition of Done**: unit test proves synthetic cannot be persisted as discovery; injection code gone

3. **WP-B2-s10**: Refit estimator for s₁₀ (minimal change from framework)
   - `v5_estimator_s10.py`: same shot-noise subtraction and k-band as WP-B2 design
   - Apply to synthetic test sector; verify zero mean on 10 null mocks
   - **Definition of Done**: `python3 v5_estimator_s10.py test_sector` runs cleanly; mock stats logged

4. **Commit & Release**:
   - All new modules + amended docs + this memo in a single commit
   - Tag: `v5.1-cooper-s10-primary` (reflects the pivot + certified kernel)
   - Push to origin
   - Write RELEASE_NOTES.md summarizing the findings and the pivot

---

## File Manifest (to be created this session)

| File | Purpose | Status |
|---|---|---|
| `cooper_s10_kernel.py` | Certified s₁₀ kernel (A005260, λ=16) | TODO → DONE |
| `v5_estimator_s10.py` | s₁₀ FFT-band estimator | TODO → DONE |
| `PIVOT_MEMO.md` | This document | DONE |
| `V5_SCIENTIFIC_REVIEW.md` | (amended) note s₇ retired | already done |
| `V5_RIGOROUS_THEORY_PLAN.md` | (amended) s₁₀ as primary | TODO → DONE |
| `archives/void_20260714_s7_fabricated/` | Old Phase 1 artifacts | TODO → DONE |
| `RELEASE_NOTES.md` | v5.1 summary | TODO → DONE |

---

## Downstream: Next Session

After this commit, sessions inherit:
- Certified s₁₀ kernel in production
- Provenance gate enforced
- Framework ready for WP-B1 (chameleon derivation) and WP-C2 (mock ensemble)
- Clear record of the pivot (git history + RELEASE_NOTES)

The hypothesis tested is now:

> **H(Cooper-s₁₀)**: Large-scale structure carries a density-modulated
> kernel whose form is the period Π₀ of the level-10 K3 family (A005260,
> λ=16), and this is preferred by data over derivative-matched controls and
> the sibling family s₇ (if we ever rebuild it cleanly).

Clean, testable, falsifiable.
