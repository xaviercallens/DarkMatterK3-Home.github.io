# WP-R4 — Sibling-Family Control Harness (P4 Discipline)

**Date:** 2026-07-25  
**Executor:** Haiku 4.5  
**Status:** ✅ **PASS** — 8/8 tests pass; P4 harness in place

---

## Summary

Implemented the sibling-family control harness to enforce P4 discipline:

**P4 (LESSONS_LEARNED.md):** Any statistic computed on one K3 candidate must be computed on all sibling families as an adversarial control. If every sibling fits equally well, the result is null.

---

## What This Provides

### `pipeline/siblings.py`
- **`SIBLING_FAMILIES`** dict: s7, s10 (primary + control pair)
  - Each family loaded from committed certificate files (never from memory)
  - Carries: name, OEIS ID, certificate path, order-(a,b,c,d) parameters
- **`evaluate_across_siblings(fn, *args, **kwargs)`** harness
  - Automatically computes fn(candidate) for all siblings
  - Returns dict keyed by family name with result + certificate source
  - **Raises if any certificate is missing** (forces addressing gaps, not skipping)

### Certificate-Backed Parameters
All candidate parameters loaded from committed certificate files:
- **s7:** `checkers/certificates/C1_mirror_s7.json` → order_abcd = (13, 4, -27, 3)
- **s10:** `checkers/certificates/C1_mirror_s10.json` → order_abcd = (6, 2, -64, 4)

No transcription from memory. No hardcoded values.

---

## Validation Tests (8/8 Pass)

✅ `test_sibling_families_defined` — At least s7 and s10 defined  
✅ `test_certificates_loaded` — All siblings have loaded certificates  
✅ `test_order_abcd_shape` — Parameters are 4-tuples (a, b, c, d)  
✅ `test_evaluate_across_siblings_basic` — All families evaluated  
✅ `test_evaluate_across_siblings_with_args` — Args passed through correctly  
✅ `test_evaluate_preserves_certificate_path` — Results carry certificate source  
✅ `test_missing_family_in_siblings_raises` — Missing cert raises (P4 enforced)  
✅ `test_error_in_function_raises` — Function errors propagate

---

## Usage Example

```python
from pipeline.siblings import evaluate_across_siblings, SIBLING_FAMILIES

# Define a function to compute some observable
def compute_observable(candidate_name):
    family = SIBLING_FAMILIES[candidate_name]
    a, b, c, d = family["order_abcd"]
    # ... compute something from (a, b, c, d) ...
    return result

# Evaluate on all siblings (s7, s10)
results = evaluate_across_siblings(compute_observable)

# results = {
#   "s7": {"result": ..., "certificate_path": "...", "status": "ok"},
#   "s10": {"result": ..., "certificate_path": "...", "status": "ok"},
# }

# If s7 and s10 give very different results → likely real signal
# If identical → likely artifact or degeneracy → null result
```

---

## P4 Enforcement Mechanism

1. **Mandatory evaluation:** Any statistic is computed for *all* siblings automatically, never selectively
2. **Certificate tracing:** Every parameter carries its source file path back to a committed certificate
3. **Error on missing:** If any sibling's certificate is unavailable, raises immediately (doesn't skip)
4. **Result interpretation:** Downstream code compares statistics across siblings; identical results flag null

---

## Design Rationale

**Why certificate-backed:** Without certification, parameters can drift between sessions or be mis-transcribed. Committed certificates provide an immutable, machine-checkable source. (LESSONS_LEARNED.md L1: never numbers from memory.)

**Why raise on missing:** If WP-R5 (or future work) tries to compute statistics on a sibling whose parameters aren't available, that's a blocker. Better to fail loudly than skip silently.

**Why independent of data chain:** P4 is a mathematical control, not tied to real data. It works equally for synthetic, real, or hypothetical data.

---

## Future Extensions

As WP-A3 progresses and new candidates (t103, etc.) pass criteria, they can be added to `SIBLING_FAMILIES`:
```python
SIBLING_FAMILIES["t103"] = {
    "name": "t103_candidate",
    "oeis": "A247452",
    "certificate_path": "checkers/certificates/C1_mirror_t103.json",
    "description": "Alternative route",
}
```

The same harness applies; no code changes needed.

---

## Epistemic Status

**Tier A/B:** Certificate-backed parameter loading and harness structure (mechanical)

**NOT Tier C:** This enforces methodology, not physics. No observable computed here.

---

## Next Steps

✅ **Cleared for WP-R5** (real 3D density field + cosmology)

---

## Provenance

`Generated-by: Haiku 4.5 | Verified-by: pytest (8/8 tests) | Reviewed-by: [pending T0]`

**Files:**
- `pipeline/siblings.py` — Sibling harness + SIBLING_FAMILIES dict
- `pipeline/tests/test_siblings.py` — 8 validation tests
