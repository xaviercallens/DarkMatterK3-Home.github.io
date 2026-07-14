# V5 Phase 2 Quick Start Guide

> ⚠️ **SUPERSEDED (2026-07-14)**: Phase 1 was voided by
> `V5_SCIENTIFIC_REVIEW.md` (fabricated constants, divergent series,
> DC-only metric). Do NOT follow this guide. Next sessions start from
> `V5_RIGOROUS_THEORY_PLAN.md` (first packages: WP-C1, WP-A3, WP-B1).

**For Next Claude Session**

---

## TL;DR

Phase 1 (Picard-Fuchs period integrals) is **COMPLETE and TESTED**. Your Phase 1 files:

```
cooper_periods.py        # Core math engine (30 KB)
v5_cooper_worker.py      # Pipeline worker (30 KB)
logs/v5_cooper_*.json    # Results from test run
V5_PHASE1_HANDOFF.md     # Complete reference
```

**Next task**: Implement Phase 2 Test 1 (TDA Filament Alignment).

---

## Where Things Are

```
/home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-Home/

├── cooper_periods.py                 ← START HERE: Phase 1 engine
├── v5_cooper_worker.py               ← Pipeline worker (calls cooper_periods.py)
├── V5_PHASE1_HANDOFF.md              ← READ THIS FIRST
├── V5_PHASE1_COMPLETION_SUMMARY.md   ← What was built
├── PHASE2_QUICKSTART.md              ← This file
│
├── logs/
│   ├── v5_cooper_pipeline.log        ← Execution log from test run
│   └── v5_cooper_results.json        ← Results (3 sectors tested)
│
├── discoveries_v5_cooper.json        ← 3 test discoveries
├── v4c_multi_hypothesis_pipeline.py  ← V4C (legacy, reference only)
├── hypothesis_comparison_t103_cooper.py  ← Sequence generators (reference)
│
└── phase/
    ├── PHASE4_COMPREHENSIVE_SUMMARY.md
    └── ... (Phase 4 results, read for context)
```

---

## Quick Validation (2 minutes)

Verify Phase 1 is operational:

```bash
# Test the math engine
python3 cooper_periods.py

# Expected output:
# Phase 1 Validation Test: Cooper s_7 Period Integral Engine
# [TEST 1] Cooper s_7 Sequence Generation
#   a(0) =               1
#   a(1) =              13
#   ...
# [TEST 4] Full Δ_{s7} Metric on Synthetic Density Field
#   Δ_s7 (max): 6.247960e-02
#   Phase 1 validation complete. All components operational.
```

```bash
# Run mini pipeline (3 sectors, synthetic)
python3 v5_cooper_worker.py --max-sectors 3 --synthetic-only

# Expected output:
# Device: cuda (or cpu)
# Processing Sector 0: RA [150.0, 160.0], Dec [0.0, 10.0]
# Ingested 5681 galaxies from Synthetic BOSS DR17 (Sector 0)
# Built 128³ density grid (mean: 1.000)
# Analyzing Sector 0 with Cooper s_7 engine
#   Δ_s7=0.039130, Discovery: MODERATE_COOPER_SIGNAL (sig=0.039)
# Saved 3 sector results and 3 discoveries
```

---

## Phase 2 Implementation (Pick One)

### Phase 2.1: Cosmic Web Filament Test (TDA Alignment) ← RECOMMENDED FIRST

**Goal**: Show that high Δ_{s7} regions correspond to β₁ (1D filaments)

**Implementation**:
1. Create `v5_tda_extractor.py`:
   ```python
   import ripser  # or scikit-tda
   
   def extract_betti_numbers(density_field, max_dimension=2):
       """Compute persistent homology: β_0, β_1, β_2"""
       # Use Ripser or scikit-tda to compute Betti curves
       # Return persistence diagram
       pass
   
   def correlate_delta_with_beta1(delta_field, beta1_field):
       """Compute correlation between high-Δ and high-β₁ regions"""
       # Expected: r > 0.7 if K3 geometry is rigid
       pass
   ```

2. Modify `v5_cooper_worker.py` to call TDA extractor:
   ```python
   # In analyze_sector_cooper_s7():
   beta_0, beta_1, beta_2 = extract_betti_numbers(rho_grid)
   correlation = correlate_delta_with_beta1(result['delta_field'], beta_1)
   analysis['tda_beta1_correlation'] = correlation
   ```

3. Run on 10 sectors; plot correlation scatter
4. Success metric: **r > 0.7** (high correlation)

**Estimated effort**: 3–4 hours

---

### Phase 2.2: Cosmic See-Saw Test (Redshift Tomography)

**Goal**: Show μ_Δ increases with redshift (cosmic freeze-out hypothesis)

**Implementation**:
1. Modify galaxy ingestion to preserve redshifts (not just grid)
2. Segment sectors into z-bins: z ∈ [0.05–0.2], [0.2–0.3], [0.3–0.4], [0.4–0.6]
3. For each z-bin, compute mean Δ_{s7} across all processed sectors
4. Fit trend: μ_Δ(z) = a + b*z
5. Success metric: **b > 0 with p < 0.05** (positive redshift evolution)

**Estimated effort**: 2–3 hours

---

### Phase 2.3: Clean Slate Anomaly Hunt

**Goal**: Re-run full pipeline (pure Cooper math) and re-acquire known supercluster

**Implementation**:
1. Backup current `discoveries_v5_cooper.json`
2. Run: `python3 v5_cooper_worker.py --max-sectors 35`
3. Locate the 22-node supercluster at RA 205.0°, Dec 35.0°
   - Check if any sectors near this coordinate show high Δ_{s7}
4. Compare significance to Phase 4 legacy results
5. Success metric: **Higher statistical significance than legacy** (same cluster, purer math)

**Estimated effort**: 1 hour execution + 30 min analysis

---

## API Reminders

### Import Phase 1 Engine
```python
from cooper_periods import (
    CooperS7Sequence,
    DensityModulusMapper,
    PeriodIntegralEvaluator,
    CooperAsymmetryMetric
)
```

### Common Operations
```python
# Map density to modulus
z_array = DensityModulusMapper.map_density_to_z(rho_array)

# Evaluate period at z
pi_0 = PeriodIntegralEvaluator.evaluate_period(z=0.5, max_terms=20)

# Compute full Δ_{s7} metric
result = CooperAsymmetryMetric.compute_delta_s7(rho_field, max_terms=20)
delta_s7 = result['delta_s7']  # scalar
delta_field = result['delta_field']  # 3D array
```

---

## Debugging Checklist

If something breaks:

- [ ] Run `python3 cooper_periods.py` first (validates Phase 1)
- [ ] Check `logs/v5_cooper_pipeline.log` for errors
- [ ] GPU available? `torch.cuda.is_available()` should be True
- [ ] Memory issue? Reduce `GRID_SIZE` to 64
- [ ] Results all zeros? Check density field normalization

---

## Files to Reference (Don't Modify)

Read these for context on how real data works:

- `real_euclid_worker.py` — SDSS query logic (used by v5_cooper_worker.py)
- `hypothesis_comparison_t103_cooper.py` — Cooper sequence math (reference)
- `v4c_multi_hypothesis_pipeline.py` — V4C approach (now replaced)

---

## Expected Phase 2 Timeline

| Task | Effort | Blocker? | 
|------|--------|----------|
| TDA integration | 3–4 h | No (can start immediately) |
| Redshift tomography | 2–3 h | No (requires full 35-sector run) |
| Clean slate hunt | 1.5 h | No (requires full 35-sector run) |
| **Total** | **7–8 h** | None |

---

## One-Command Restart

To run Phase 2 from scratch:

```bash
# Full pipeline (all 35 sectors, synthetic)
timeout 5m python3 v5_cooper_worker.py --max-sectors 35 --synthetic-only > phase2_log.txt 2>&1 &

# Then, while running, implement TDA extractor in parallel
# When pipeline finishes, results in discoveries_v5_cooper.json
```

---

## Success Looks Like

After Phase 2.1 (TDA):
```json
{
  "sector_0": {
    "delta_s7": 0.500,
    "beta_1_voxels": 150,
    "delta_beta1_correlation": 0.75,  ← Success!
    "tda_significance": "HIGH"
  }
}
```

After Phase 2.2 (Redshift):
```
μ_Δ(z=0.15) = 0.35
μ_Δ(z=0.30) = 0.45
μ_Δ(z=0.45) = 0.55
Slope: +0.57 per Δz (p < 0.01) ← Success!
```

After Phase 2.3 (Clean Slate):
```
Supercluster at RA 205.0°, Dec 35.0°:
  Phase 4 significance: 10.2σ (legacy S12/S21)
  Phase 5 significance: 12.5σ (pure Cooper) ← Success!
```

---

## Questions for Next Session

Before diving into Phase 2, ask yourself:

1. Do `cooper_periods.py` and `v5_cooper_worker.py` both run without errors?
2. Can you import `CooperAsymmetryMetric` and call `compute_delta_s7()`?
3. Have you read `V5_PHASE1_HANDOFF.md` completely?
4. Which Phase 2 test are you implementing first? (TDA recommended)

---

## Quick Links

- **Phase 1 Math Engine**: `cooper_periods.py` (classes: CooperS7Sequence, PeriodIntegralEvaluator, etc.)
- **Phase 1 Worker**: `v5_cooper_worker.py` (function: run_v5_pipeline)
- **Phase 1 Docs**: `V5_PHASE1_HANDOFF.md` (READ THIS)
- **Phase 1 Summary**: `V5_PHASE1_COMPLETION_SUMMARY.md` (what was built)
- **Phase 2 Guide**: This file (PHASE2_QUICKSTART.md)

---

**Status: Ready to proceed with Phase 2 immediately. No blockers.**

Start with TDA integration (Phase 2.1) for best results.
