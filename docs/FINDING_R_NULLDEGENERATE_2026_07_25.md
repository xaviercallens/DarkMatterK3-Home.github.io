# Finding R-NULLDEGENERATE — WP-R3 Null Bank Was Methodologically Non-Functional

**Date:** 2026-07-25  
**Severity:** Methodological defect (not a data-integrity or corruption issue)  
**Status:** ROOT CAUSE IDENTIFIED, CORRECTED IN WP-R5  
**Discovered during:** WP-R5 execution (real 3D density field work), Sonnet 5 review

---

## What Was Claimed (WP-R3, commit 4c99217)

WP-R3 reported 400 null realizations (2 schemes × 200 each) with "both schemes producing statistically consistent results" and "no contradictions." The report (`docs/WP_R3_REAL_NULLBANK.md`) stated all realizations had zero variance (σ=0.0) and called this a pass.

**That zero variance was the bug, not a clean result — and it was misreported as a pass.**

---

## Root Cause

### Shuffle scheme (`scripts/build_realdata_nullbank.py::build_shuffle_nulls`)

```python
perm = np.random.permutation(len(df))
ra_shuffled = ra[perm]
dec_shuffled = dec[perm]
```

This permutes **RA and Dec with the same index**, so `(ra_shuffled[i], dec_shuffled[i])` is always some original `(ra[j], dec[j])` pair — the shuffled catalog is the *exact same set of points*, just reordered. A histogram (and therefore Betti numbers) is invariant to point order. **This computes the identical topology every single "realization."**

The stated intent ("keep exact (RA, Dec) positions; randomly permute any per-object quantity across objects") requires an independent per-object attribute to shuffle — decoupling something *from* position. With no third attribute available at the time, permuting the position pair against itself is a no-op in disguise.

### Rotate scheme (`build_rotate_nulls`)

```python
ra_offset = np.random.uniform(0, 360)
ra_rotated = (ra + ra_offset) % 360.0
```

A rigid rotation applied identically to every point is an **isometry**: it changes coordinates but preserves all pairwise distances and relative structure. Since `density_field_from_catalog` derives its bin range from the (rotated) data's own min/max, the field's internal shape is reconstructed identically each time. **This also computes the identical topology every "realization," just relabeled.**

### Why this wasn't caught at WP-R3 time

The validation criterion in the master plan was "both schemes produce statistically consistent nulls" — zero-variance-but-consistent technically satisfies a naive reading of that check. The actual required check (do the *null* distributions have any spread at all, and does the *real* data ever fall somewhere other than the extreme percentile) was not run. The subsequent `compute_realdata_topology.py` comparison (commit e52fce7) found real data at the "100th percentile" for every statistic and reported this without flagging that a null with zero variance cannot produce any percentile except 0% or 100% — a degenerate distribution, not a permissive one.

---

## Consequence

- `data/nullbanks/real/nullbank_2026_07_25.json` (WP-R3 output) is **not usable as a null distribution**. It contains 400 copies of two numbers (per dataset), not 400 independent draws from a randomized ensemble.
- `docs/EXECUTION_SUMMARY_2026_07_25.md`'s claim "Real data topology matches null bank exactly... consistent with null hypothesis" is **retracted** — there was no null distribution to be consistent with. The correct statement is: *no valid null was computed.*
- No downstream WP had consumed this null bank for anything beyond the retracted comparison, so no cascading corruption exists.

---

## Fix (Implemented in WP-R5)

WP-R5 builds a new, methodologically valid null bank (`scripts/build_wp_r5_nullbank.py`) using two schemes that actually decouple structure:

1. **z-shuffle:** keep each object's (RA, Dec) fixed; independently permute the *redshift* assignment across objects. This breaks any real radial-angular correlation while preserving the marginal angular pattern and the marginal redshift distribution — a standard technique in large-scale-structure null testing.
2. **Angular CSR (complete spatial randomness):** keep each object's redshift fixed; replace (RA, Dec) with positions drawn uniformly at random within the catalog's observed angular bounding box. This tests the observed angular pattern against uniform randomness at the same radial slicing.

Both schemes produce genuinely different point sets per realization (verified: nonzero variance in β₀/β₁/β₂ across realizations — see `docs/WP_R5_3D_FIELD.md`).

---

## Lesson

Consistent with `LESSONS_LEARNED.md` P2 ("tests are scientific, not smoke") and P3 discipline: a validation check that only confirms internal agreement between two methods, without confirming either method does anything nontrivial, can pass while the underlying computation is vacuous. Any future null-bank or randomization scheme must include an explicit **nonzero-variance check** as part of its own validation, not just cross-scheme agreement.

---

## Provenance

`Generated-by: Claude Sonnet 5 | Verified-by: manual permutation trace + re-derivation | Reviewed-by: [pending T0]`

This finding does not require a T0 falsification-branch ruling (F1–F6): it is an engineering/methodology correction, not a physics result, and gate G1-L was never touched by the retracted comparison (it was already, correctly, labeled ENGINEERING throughout).
