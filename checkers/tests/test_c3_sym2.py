"""Golden tests for the C3 symmetric-square checker (K3_CRITERIA.md C3).

Merge-blocking: known-good pairs must PASS(N), known-bad must FAIL, the check
must be deterministic, and margins exact. All exact rational arithmetic.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from checkers.check_C3_sym2 import (  # noqa: E402
    ORDER2_ZAGIER, ORDER3_AZ_COOPER, BIJECTION,
    verify_c3_sym2, zagier_order2, az_cooper_order3,
)


# --- sequence generators reproduce their literature closed forms ----------
def test_apery_b_closed_form():
    """Order-2 D = Apéry b_n = Σ C(n,k)^2 C(n+k,k)."""
    import math
    b = zagier_order2(*ORDER2_ZAGIER["D"], N=8)
    closed = [sum(math.comb(n, k) ** 2 * math.comb(n + k, k) for k in range(n + 1))
              for n in range(9)]
    assert b == closed
    assert b[:5] == [1, 3, 19, 147, 1251]


def test_s10_is_A005260():
    """Cooper s10 = Σ C(n,k)^4 (A005260)."""
    import math
    s10 = az_cooper_order3(*ORDER3_AZ_COOPER["s10"], N=8)
    closed = [sum(math.comb(n, k) ** 4 for k in range(n + 1)) for n in range(9)]
    assert s10 == closed
    assert s10[:5] == [1, 2, 18, 164, 1810]


def test_domb_positive_and_A002895():
    """Order-3 alpha = Domb numbers, all positive."""
    domb = az_cooper_order3(*ORDER3_AZ_COOPER["alpha"], N=10)
    assert domb[:6] == [1, 4, 28, 256, 2716, 31504]
    assert all(t > 0 for t in domb)


# --- the Sym² identity: matching pairs pass, mismatches fail ---------------
@pytest.mark.parametrize("o2,o3", list(BIJECTION.items()))
def test_bijection_pairs_pass(o2, o3):
    res = verify_c3_sym2(ORDER2_ZAGIER[o2], ORDER3_AZ_COOPER[o3], N=30)
    assert res["status"] == "PASS", res["verdict"]
    assert res["verdict"] == "PASS(30)"
    assert res["margin"] == 0


@pytest.mark.parametrize("o2,o3", [
    ("C", "eta"), ("D", "alpha"), ("A", "eta"), ("C", "gamma"),
])
def test_mismatched_pairs_fail(o2, o3):
    res = verify_c3_sym2(ORDER2_ZAGIER[o2], ORDER3_AZ_COOPER[o3], N=30)
    assert res["status"] == "FAIL"
    assert res["first_mismatch_order"] is not None


def test_cooper_s10_has_no_zagier_sym2_partner():
    """Honest negative result: Cooper s10 (d≠0, extended family) is NOT the
    symmetric square of any Zagier order-2 via the AZ bijection identity.
    C3 for s10 is therefore UNVERIFIED by this route — a finding, not a pass."""
    for o2 in ORDER2_ZAGIER:
        res = verify_c3_sym2(ORDER2_ZAGIER[o2], ORDER3_AZ_COOPER["s10"], N=24)
        assert res["status"] == "FAIL"


# --- determinism + stability ----------------------------------------------
def test_determinism_bit_identical():
    r1 = verify_c3_sym2(ORDER2_ZAGIER["C"], ORDER3_AZ_COOPER["alpha"], N=30)
    r2 = verify_c3_sym2(ORDER2_ZAGIER["C"], ORDER3_AZ_COOPER["alpha"], N=30)
    assert r1 == r2
    assert r1["determinism_hash"] == r2["determinism_hash"]


def test_high_order_stable_margin():
    """PASS margin stays exactly 0 at high N (no rational drift)."""
    r = verify_c3_sym2(ORDER2_ZAGIER["C"], ORDER3_AZ_COOPER["alpha"], N=80)
    assert r["status"] == "PASS"
    assert r["margin"] == 0
    assert r["verdict"] == "PASS(80)"
