# S2-01b Golden Test Data — Shioda-Inose Moduli Map Checker

**Purpose:** Reference fixtures for the C3b (Shioda-Inose moduli map) symbolic checker implementation (S2-01b, WP, EXECUTION_PLAN.md).

**Audience:** T1 (Claude Sonnet) implementing `checkers/check_c3b_moduli_map.py`.

---

## Overview

Five golden test cases provided as fixtures in `golden_test_fixtures.json`:

| Test Case | Pair | Status | Purpose |
|---|---|---|---|
| **known_good_s7_S12** | s₇ (order-3) + S₁₂ (order-2) | PASS | Known-good K3-base / fiber pair |
| **known_good_s10_S21** | s₁₀ (order-3) + S₂₁ (order-2) | PASS | Primary candidate pair (Dual-Scale model) |
| **known_bad_s10_generic_order2** | s₁₀ + fabricated order-2 | FAIL | Control: reject non-geometric pairs |
| **known_bad_swap_order2_order3** | s₁₀ and S₂₁ swapped | FAIL | Control: order matters; swapping breaks relation |
| **stress_test_high_order_s7** | s₇ + S₁₂, verified to N=200 | PASS | Stress: margin stable to high order |

---

## How to Use (for T1)

### 1. Load Fixtures in Tests

```python
import json
from pathlib import Path

golden_data_file = Path(__file__).parent / "golden_test_fixtures.json"
with open(golden_data_file) as f:
    golden = json.load(f)

for test_case in golden["test_cases"]:
    name = test_case["name"]
    expected_status = test_case["status"]
    order_2 = test_case["order_2_recurrence"]
    order_3 = test_case["order_3_recurrence"]
    
    # Call your checker
    result = verify_c3b(order_2["first_terms"], order_3["first_terms"], N=50)
    
    assert result["status"] == expected_status, f"{name} failed"
```

### 2. Verify Determinism

```python
# Run the same test case twice
result1 = verify_c3b(order_2["first_terms"], order_3["first_terms"], N=50)
result2 = verify_c3b(order_2["first_terms"], order_3["first_terms"], N=50)

# Both must produce identical JSON (including determinism_hash)
assert result1 == result2, "Determinism check failed"
```

### 3. Interpret Results

- **PASS cases:** expect `status="PASS"`, `margin < 1e-15` (machine precision)
- **FAIL cases:** expect `status="FAIL"` or `status="CONDITIONAL"` (if marginal)
- **Stress case (N=200):** margin should NOT grow compared to N=50 (shows no numerical drift)

---

## Expected Checker Output Format

Each test case should produce a JSON dict:

```json
{
  "status": "PASS|FAIL|CONDITIONAL",
  "order": 50,
  "margin": 1.2e-16,
  "F_series": "q + 2q^2 + ...",
  "determinism_hash": "sha256(input_recurrence + checker_code)",
  "assumptions": ["A-ONT"],
  "notes": "..."
}
```

---

## Rationale

### known_good_s7_S12
- Source: Phase 4/V4 candidate list
- Status: If C3b PASSES, s₇ is a valid K3-base; if FAILS, F1 branch (s₇ removed)
- Literature: Cooper, *Ramanujan J.* 2012; mirror-symmetry Shioda-Inose construction

### known_good_s10_S21
- Source: V5 primary candidate (s₁₀ certified via `cooper_s10_kernel.py`)
- Status: **Critical for M1 gate.** If C3b PASSES on s₁₀, MVM matching can proceed
- Literature: OEIS A005260 with verified λ=16

### known_bad_s10_generic_order2
- Purpose: Ensure checker rejects **unrelated** pairs
- Design: Generic geometric series (λ=5) has no Shioda-Inose relation to s₁₀
- Expected behavior: FAIL at order N=50; margin persists (no convergence)

### known_bad_swap_order2_order3
- Purpose: Verify order-awareness
- Design: Swap which recurrence plays which role
- Expected behavior: FAIL; symmetric swap breaks the asymmetric F relation

### stress_test_high_order_s7
- Purpose: Verify **numerical stability** at high order
- Verification: Same s₇/S₁₂ pair as known_good_s7_S12, but order N=200 instead of 50
- Expected behavior: PASS, margin stable (e.g., 1.3e-15 at N=50 and N=200; no growth)
- Addresses: Avoids symptomatic marginal agreement that breaks at high order

---

## Fixture Metadata Structure

Each `test_case` in `golden_test_fixtures.json` contains:

| Field | Type | Purpose |
|---|---|---|
| `name` | str | Unique identifier (kebab-case) |
| `description` | str | What this case tests |
| `status` | str | Expected C3b checker output status |
| `order_2_recurrence` | dict | Order-2 operator (elliptic curve) |
| `order_3_recurrence` | dict | Order-3 operator (K3 surface) |
| `shioda_inose_map` | dict | Expected moduli map F properties |
| `rationale` | str | Why this test matters |

Each recurrence dict contains:

| Field | Type | Purpose |
|---|---|---|
| `name` | str | Operator identifier |
| `description` | str | Source + context |
| `order` | int | Picard-Fuchs order |
| `lambda` | float | Growth rate (verified or expected) |
| `first_terms` | list[int] | Initial sequence terms (exact integers) |
| `recurrence_polynomial` | str | (optional) Explicit recurrence relation |

---

## Integration with CI

These fixtures will be loaded by:
1. **`pipeline/checkers/test_c3b.py`** (T1-written pytest suite)
2. **S2-04 ranking run** (uses C3b checker output to rank candidates)

Expected integration pattern:

```bash
# T1 implements checkers/check_c3b_moduli_map.py using these fixtures
pytest pipeline/checkers/test_c3b.py  # Must pass all golden tests

# Then S2-02 implements generic checkers C1–C5
# Then S2-04 runs ranking on all candidates
# Output: K3_SELECTION_REPORT.md with per-candidate C3b grades
```

---

## Notes for T1

1. **No network calls needed.** All test data is local JSON; checkers must work offline.
2. **Determinism is critical.** Re-running the same test must produce identical output (same hash).
3. **Precision matters.** Margin < 1e-15 is "excellent"; > 1e-8 is "suspect"; CONDITIONAL if no convergence.
4. **Order-awareness:** verify that swapping order-2/order-3 *breaks* the result (known_bad_swap case).
5. **Stress test:** ensure no numerical drift; margin should not degrade from N=50 to N=200.

---

**Generated by:** T2 (Haiku), 2026-07-18  
**For:** S2-01b C3b checker implementation (T1)  
**Status:** Ready for T1 to use in `pytest pipeline/checkers/test_c3b.py`
