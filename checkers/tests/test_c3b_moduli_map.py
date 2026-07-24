"""Golden tests for the C3b Shioda–Inose map checker (K3_CRITERIA.md C3b).

Merge-blocking: matching pairs PASS(N) with the explicit map F emitted;
mismatched and role-swapped pairs FAIL; the map F has the correct integer
coefficients; the check is deterministic. Exact rational arithmetic.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from checkers.check_C3_sym2 import ORDER2_ZAGIER, ORDER3_AZ_COOPER, BIJECTION  # noqa: E402
from checkers.check_C3b_moduli_map import verify_c3b_map  # noqa: E402


@pytest.mark.parametrize("o2,o3", list(BIJECTION.items()))
def test_bijection_pairs_pass_with_map(o2, o3):
    res = verify_c3b_map(ORDER2_ZAGIER[o2], ORDER3_AZ_COOPER[o3], N=30)
    assert res["status"] == "PASS", res["verdict"]
    assert res["verdict"] == "PASS(30)"
    assert res["margin"] == 0
    # F(x) = -x/(1 - A x + B x^2): denominator coeffs match the order-2 (A,B)
    A, B, _ = ORDER2_ZAGIER[o2]
    assert res["map_F"]["denominator_coeffs"] == [1, -A, B]
    assert res["map_F"]["numerator_coeffs"] == [0, -1]
    assert res["assumptions"] == ["A-ONT"]


@pytest.mark.parametrize("o2,o3", [("C", "eta"), ("D", "alpha"), ("A", "gamma")])
def test_mismatched_pairs_have_no_closing_map(o2, o3):
    res = verify_c3b_map(ORDER2_ZAGIER[o2], ORDER3_AZ_COOPER[o3], N=30)
    assert res["status"] == "FAIL"
    assert res["first_mismatch_order"] is not None


def test_cooper_s10_no_c3b_map():
    """Consistent with C3: Cooper s10 has no closing Shioda–Inose map to any
    Zagier order-2 (extended family, outside the AZ bijection)."""
    for o2 in ORDER2_ZAGIER:
        res = verify_c3b_map(ORDER2_ZAGIER[o2], ORDER3_AZ_COOPER["s10"], N=24)
        assert res["status"] == "FAIL"


def test_determinism_bit_identical():
    r1 = verify_c3b_map(ORDER2_ZAGIER["D"], ORDER3_AZ_COOPER["eta"], N=30)
    r2 = verify_c3b_map(ORDER2_ZAGIER["D"], ORDER3_AZ_COOPER["eta"], N=30)
    assert r1 == r2
    assert r1["determinism_hash"] == r2["determinism_hash"]


def test_high_order_exact_margin():
    r = verify_c3b_map(ORDER2_ZAGIER["A"], ORDER3_AZ_COOPER["delta"], N=70)
    assert r["status"] == "PASS"
    assert r["margin"] == 0
    assert r["verdict"] == "PASS(70)"


def test_epistemic_note_present():
    """C3b certificate must carry the geometric-not-physical note (VISION §1.3)."""
    r = verify_c3b_map(ORDER2_ZAGIER["C"], ORDER3_AZ_COOPER["alpha"], N=20)
    assert "not by itself a physical coupling" in r["note"]
