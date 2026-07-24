"""Golden tests for the C1 mirror-map integrality checker (K3_CRITERIA.md C1).

Merge-blocking: sporadic operators have integral inverse mirror maps → PASS(N₁);
perturbed operators go non-integral at low order → FAIL; determinism and margin
are exact. All exact rational / dual-number arithmetic.
"""
import sys
from fractions import Fraction as F
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from checkers.check_C3_sym2 import ORDER3_AZ_COOPER  # noqa: E402
from checkers.check_C1_mirror_integrality import (  # noqa: E402
    verify_c1, mirror_map_zq, GOLDEN_GOOD, GOLDEN_BAD,
)


@pytest.mark.parametrize("name", GOLDEN_GOOD)
def test_sporadic_operators_mirror_integral(name):
    res = verify_c1(ORDER3_AZ_COOPER[name], N1=40)
    assert res["status"] == "PASS", res["verdict"]
    assert res["verdict"] == "PASS(40)"
    assert res["margin_max_denominator"] == 1


@pytest.mark.parametrize("name,params", list(GOLDEN_BAD.items()))
def test_perturbed_operators_non_integral(name, params):
    res = verify_c1(params, N1=40)
    assert res["status"] == "FAIL"
    assert res["first_non_integral_order"] is not None


def test_cooper_s7_s10_pass_c1_even_though_they_fail_c3():
    """Honest nuance: s7/s10 PASS C1 (genuine MUM period operators) though they
    FAIL C3/C3b (not symmetric squares of a Zagier order-2)."""
    for name in ("s7", "s10"):
        assert verify_c1(ORDER3_AZ_COOPER[name], N1=30)["status"] == "PASS"


def test_mirror_map_starts_with_q():
    """z(q) = q + O(q²): leading coefficient is exactly 1."""
    zq = mirror_map_zq(ORDER3_AZ_COOPER["alpha"], 20)
    assert zq[0] == 0
    assert zq[1] == F(1)


def test_domb_mirror_known_coeffs():
    """Regression pin on exact low-order mirror coefficients for Domb (10,4,64)."""
    zq = mirror_map_zq(ORDER3_AZ_COOPER["alpha"], 8)
    assert [int(x) for x in zq[1:9]] == [1, -6, 21, -68, 198, -510, 1248, -2904]


def test_determinism_bit_identical():
    r1 = verify_c1(ORDER3_AZ_COOPER["delta"], N1=30)
    r2 = verify_c1(ORDER3_AZ_COOPER["delta"], N1=30)
    assert r1 == r2
    assert r1["determinism_hash"] == r2["determinism_hash"]


def test_high_order_stable():
    res = verify_c1(ORDER3_AZ_COOPER["alpha"], N1=80)
    assert res["status"] == "PASS"
    assert res["margin_max_denominator"] == 1
    assert res["verdict"] == "PASS(80)"
