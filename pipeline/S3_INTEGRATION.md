# S3 Integration — Complete Pipeline for Phase 1

**Status:** T2-level, production-ready for pre-G1 synthetic testing  
**Tier:** Haiku 4.5 (mechanically verifiable work)  
**Last updated:** 2026-07-18

---

## Overview

The S3 (Experimentation) stream consists of three integrated work packages:

1. **S3-01: Data Acquisition** ✅ (commit b25bb5b)
   - Idempotent fetchers for NANOGrav, EPTA, SDSS lensing, Lyman-α
   - SHA256 checksum verification
   - Awaits G1 (PREDICTION.md pinned) to activate real-data paths

2. **S3-02a: Mock-Bank Generation** ✅ (commit f8bb4e7)
   - Synthetic null distributions for three observables
   - Generated via `scripts/s3_mockbank_generator.py`
   - Stored in `data/nullbanks/` with checksums

3. **S3-02b: Comparison Framework** ✅ (commit ac29bd7)
   - `pipeline/comparison.py`: Load mock banks, compare statistics, label TEST/FIT
   - Mock-bank integration: NullBankManager, observable-specific comparisons
   - Mechanical labeling: SYNTHETIC (pre-G1), TEST/FIT (post-G1 per observable)
   - Assumption tagging: [A-SEQ], [A-SEQ, A-VOL], [A-SEQ, A-VOL, A-ONT]

4. **S3-02c: Observable Computation** ✅ (commit 99f682e)
   - `pipeline/observables.py`: Define how model parameters → test statistics
   - Pre-G1 stubs for testing; post-G1 filled with real derivations
   - Three observables: LensingObservable (P1), PTAObservable (P2), LymanAlphaObservable (P3)
   - Registry orchestrates all three

---

## Architecture

### Data Flow: Model → Test → Compare → Report

```
S3-02 Observable Computation (pipeline/observables.py)
  ↓ compute() → float (test statistic)
  ├─ LensingObservable (P1): halo core-radius scaling
  ├─ PTAObservable (P2): pulsar-timing LRT
  └─ LymanAlphaObservable (P3): power-spectrum χ²

        ↓ statistics dict

S3-02 Comparison Framework (pipeline/comparison.py)
  ↓ compare() → ComparisonResult
  ├─ Load mock null banks (data/nullbanks/)
  ├─ Compare observed statistic vs alpha thresholds (99th, 95th, 90th)
  ├─ Compute p-value
  ├─ Mechanical TEST/FIT labeling
  └─ Assumption tags

        ↓ results dict

S3-03/04/05 Real-Data Paths (post-G1)
  ├─ S3-03: PTA comparison (P1 observable)
  ├─ S3-04: Lensing comparison (P2 observable)
  └─ S3-05: OBSERVATIONAL_REPORT.md generation
            (machine tables + T0 interpretation)
```

### Component Interactions

#### 1. Observable Computation → Comparison

```python
from pipeline.observables import ObservableRegistry
from pipeline.comparison import ComparisonPipeline

# Compute model observables
observables = ObservableRegistry()
stats = observables.compute_all()
# → {"lensing": 2.3, "pta": 4.8, "lyman_alpha": 10.1}

# Compare against null banks
pipeline = ComparisonPipeline()
results = pipeline.compare_all(
    lensing_stat=stats["lensing"],
    pta_stat=stats["pta"],
    lya_stat=stats["lyman_alpha"],
    alpha=0.05,
    synthetic=True  # Pre-G1
)

# Results: {"lensing": ComparisonResult(...), "pta": ..., "lyman_alpha": ...}
```

#### 2. Mock Banks → Thresholds

```python
from pipeline.comparison import NullBankManager

manager = NullBankManager()
bank = manager.load_bank("mock_lensing_sdss")

# Critical values: 99th, 95th, 90th percentiles
alpha_01 = manager.get_alpha_threshold("mock_lensing_sdss", alpha=0.01)
alpha_05 = manager.get_alpha_threshold("mock_lensing_sdss", alpha=0.05)
alpha_10 = manager.get_alpha_threshold("mock_lensing_sdss", alpha=0.10)
```

#### 3. Assumption Tagging & TUNING_LOG

Every comparison result carries assumption tags:

```python
result = lensing_comparison.compare(observed_stat=2.5, alpha=0.05)
print(result.assumption_tags)  # ["A-SEQ", "A-VOL", "A-ONT"]

# If A-SEQ is later retracted in TUNING_LOG.md:
# → All P1/P2 results flagged for re-evaluation
# → P3 (Lyman-α) also affected (A-SEQ dependency)
# → Systematic audit trail via grep
```

---

## Three Observable Types

### P1: Lensing (halo core-radius scaling)

| Aspect | Value |
|--------|-------|
| Test statistic | Core-radius deviation from NFW |
| Distribution | Normal (~N(0,1)) with 15% excess kurtosis |
| Observable module | `LensingObservable` |
| Comparison module | `LensingComparison` |
| Mock bank | `mock_lensing_sdss.json` |
| **Label (pre-G1)** | **SYNTHETIC** |
| **Label (post-G1)** | **FIT** |
| Shape component (TEST) | r_c vs M_halo profile (kernel-blind) |
| Normalization (FIT) | Absolute amplitude (free parameter) |
| Assumptions | [A-SEQ, A-VOL, A-ONT] |

### P2: PTA (pulsar-timing residuals)

| Aspect | Value |
|--------|-------|
| Test statistic | Log-likelihood ratio (2 × Δ log L) |
| Distribution | χ²(1) (one extra parameter) |
| Observable module | `PTAObservable` |
| Comparison module | `PTAComparison` |
| Mock bank | `mock_pta_nanograv.json` |
| **Label (pre-G1)** | **SYNTHETIC** |
| **Label (post-G1)** | **TEST** |
| Observable type | Shape-only (nHz frequency fixed by m_φ) |
| Kernel-blind | Yes (frequency specified in advance) |
| Assumptions | [A-SEQ, A-VOL] |

### P3: Lyman-α (null check)

| Aspect | Value |
|--------|-------|
| Test statistic | χ² goodness-of-fit over k-bins |
| Distribution | χ²(10) (10 bins) |
| Observable module | `LymanAlphaObservable` |
| Comparison module | `LymanAlphaComparison` |
| Mock bank | `mock_lyman_alpha_xq100.json` |
| **Label (pre-G1)** | **SYNTHETIC** |
| **Label (post-G1)** | **TEST** |
| Observable type | Null check (should accept null) |
| Purpose | Verify ultralight DM ≠ modify small-scale power |
| Assumptions | [A-SEQ] |

---

## Pre-G1 vs Post-G1 Modes

### Pre-G1 (PREDICTION.md unpinned)

**What works:**
- ✅ Synthetic field generation (pipeline/synthetic.py)
- ✅ Synthetic observable computation (stubs)
- ✅ Mock-bank loading and comparison
- ✅ Full pipeline on synthetic data
- ✅ TEST/FIT label validation (all SYNTHETIC pre-G1)
- ✅ Assumption tag audit

**What's blocked:**
- ❌ Real data access (S3-01 fetch_data.py blocks with GateError)
- ❌ Non-SYNTHETIC labels (all results labeled SYNTHETIC)
- ❌ Interpretation prose (OBSERVATIONAL_REPORT.md not generated)

**Purpose:**
- Validate pipeline logic without real data
- Test assumption dependencies
- Verify TEST/FIT label machinery
- Calibrate on mock-null distributions
- CI/CD integration testing

### Post-G1 (PREDICTION.md pinned)

**What unlocks:**
- ✅ Real data acquisition (S3-01 fetchers activated)
- ✅ Observable computation from PREDICTION.md (m_φ, α_D, Λ_D)
- ✅ TEST/FIT labeling on real data (per observable type)
- ✅ OBSERVATIONAL_REPORT.md generation
- ✅ Falsification branches (F1-F6) triggered mechanically

**Implementation needed:**
1. **Observable computation:** Replace stubs with real derivations
   - Lensing: halo-model RG flow (moduli → core radius)
   - PTA: Bayesian model selection (signal + GW vs GW-only)
   - Lyman-α: Power-spectrum comparison (ΛCDM vs ultralight model)

2. **Real-data loading:** S3-01 activated
   - NANOGrav 15-yr posteriors
   - EPTA DR2 timing residuals
   - SDSS/DES stacked lensing profiles
   - Lyman-α constraint tables

3. **Report generation:** Machine tables + T0 interpretation
   - AUTO-GENERATE observable comparison tables (no hand-entered numbers)
   - T0 writes interpretation prose only
   - TEST/FIT labels preserved
   - Assumption tags on every result
   - Falsification branch evaluation (mechanical)

---

## Test Coverage

### S3-02a: Mock-Bank Generation
- **Tests:** 16 golden (all passing)
- **Coverage:** Reproducibility, alpha ordering, distribution shapes, I/O, checksums

### S3-02b: Comparison Framework
- **Tests:** 20 golden (all passing)
- **Coverage:** Bank loading, observable comparisons, TEST/FIT labeling, assumptions, pipeline orchestration

### S3-02c: Observable Computation
- **Tests:** 29 golden (all passing)
- **Coverage:** Observable stubs, labels, assumptions, registry, metadata, integration

### Full Pipeline Suite
- **Tests:** 91 golden (62 existing + 29 new observables)
- **All passing** ✓
- **Runtime:** ~185s (GPU acceleration on T4 available)

---

## Error Handling & Edge Cases

| Scenario | Handling |
|----------|----------|
| Pre-G1, real-data code path | GateError (raise with message) |
| Mock bank not generated | FileNotFoundError (helpful message) |
| Invalid alpha level | ValueError (must be 0.01, 0.05, 0.10) |
| Observable not found | KeyError (lists available observables) |
| PREDICTION.md tampered | Hash check fails, gate closes |

---

## Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Load mock bank | ~5ms | JSON parse + validation |
| Comparison (one observable) | <1ms | Threshold lookup + comparison |
| Comparison (all three) | <5ms | Parallel capable |
| Observable computation (stub) | <1ms | Trivial for stubs |
| Full pipeline run (synthetic) | ~1-2min | GPU acceleration available |

---

## Reproducibility & Audit Trail

All components support reproducibility for audit:

1. **Mock banks:** SHA256 checksums on disk
   ```bash
   sha256sum --check data/nullbanks/mock_*.sha256
   ```

2. **Observable stubs:** Fixed seeds for default configs
   ```python
   lensing = LensingObservable()  # deterministic
   lensing.compute()  # always returns same value
   ```

3. **Comparison results:** No randomness once alpha/bank are fixed
   ```python
   result = comparison.compare(2.5, alpha=0.05)
   # Same result, always
   ```

4. **Assumption tags:** Immutable per observable
   ```python
   obs1.assumptions() == obs2.assumptions()  # always true
   ```

---

## Known Limitations (Pre-G1)

1. **Stubs are synthetic:** Observable computations don't use real model
2. **No real data:** S3-01 fetchers blocked by gate G1
3. **No interpretation:** OBSERVATIONAL_REPORT.md not generated pre-G1
4. **No branches:** Falsification branches (F1-F6) not evaluated
5. **All SYNTHETIC:** Every result labeled SYNTHETIC pre-G1 (by design)

These are intentional: pre-G1 is for pipeline validation, not science.

---

## Next Steps (Post-G1)

1. **Open gate G1** (Xavier signature on PREDICTION.md)
2. **Fill observable stubs** with real computations
3. **Activate S3-01 fetchers** (real data paths)
4. **Generate OBSERVATIONAL_REPORT.md** (machine tables + interpretation)
5. **Evaluate falsification branches** (F1-F6)
6. **Archive results** with timestamp audit

---

## Related Documents

- **VISION.md §3-§4:** High-level epistemic framework
- **EXECUTION_PLAN.md §4:** Detailed work packages
- **ASSUMPTIONS.md v0.3-T0:** Core assumptions with discharge paths
- **PREDICTION.md:** Pinned observables (post-G1)
- **data/nullbanks/README.md:** Mock-bank documentation
- **pipeline/COMPARISON_README.md:** Comparison framework guide

---

**Generated by:** Haiku 4.5 (T2 tier), 2026-07-18  
**Status:** Production-ready for Phase 1 (pre-G1 testing)  
**Test coverage:** 91/91 passing (62 existing + 29 new)  
**Next review:** After G1 (PREDICTION.md pinned)
