"""WP-0 regression guards for refs/ recurrence data.

Locks in: (a) the documented v1.4 defect stays documented (order-3 non-integral
at k=1); (b) the v2 corrected order-3 recurrence is integral through n=12 with
the stated terms and is the Sym² partner of Apéry b_n; (c) the order-2 entry is
Apéry b_n and matches its binomial closed form. Exact arithmetic only.
"""
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

import sympy as sp  # noqa: F401  (recurrence strings reference sp.Rational)

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from checkers.check_C3_sym2 import (  # noqa: E402
    ORDER2_ZAGIER, ORDER3_AZ_COOPER, verify_c3_sym2,
)


def _run_recurrence(entry, N):
    """Faithfully evaluate a JSON recurrence entry (n from 1)."""
    s = [F(x) for x in entry["initial_terms"]]
    expr = entry["recurrence_python"]
    for n in range(1, N):
        val = eval(expr, {"sp": sp, "n": n, "s": s})  # noqa: S307 (trusted repo data)
        s.append(val)
    return s


def test_v14_order3_defect_present():
    """The v1.4 order-3 entry is non-integral at k=1 — guard the documented bug."""
    v14 = json.loads((REPO / "refs/sporadic_recurrences.json").read_text())
    entry = v14["sequences"]["az_eq14_level11"]
    s = [F(x) for x in entry["initial_terms"]]
    expr = entry["recurrence_python"]
    # k=0 gives 25 (integral); k=1 gives 1015/4 (non-integral)
    for k in range(0, 2):
        s.append(eval(expr, {"sp": sp, "k": k, "s": s}))  # noqa: S307
    assert s[-1].denominator != 1, "expected documented non-integrality at k=1"


def test_v2_order3_corrected_integral_and_terms():
    v2 = json.loads((REPO / "refs/sporadic_recurrences_v2.json").read_text())
    eta = v2["sequences"]["az_eta_level11"]
    s = _run_recurrence(eta, 13)[:13]
    assert all(x.denominator == 1 for x in s), "corrected eta must be integral through n=12"
    assert [int(x) for x in s] == [
        1, 5, 35, 275, 2275, 19255, 163925, 1385725,
        11483875, 91781375, 688658785, 4581861025, 22550427925,
    ]
    assert eta["term_confirmation"] == "PENDING"  # honesty flag preserved


def test_v2_order2_is_apery_b():
    v2 = json.loads((REPO / "refs/sporadic_recurrences_v2.json").read_text())
    b = _run_recurrence(v2["sequences"]["az_apery_b_level11"], 9)
    closed = [sum(math.comb(n, k) ** 2 * math.comb(n + k, k) for k in range(n + 1))
              for n in range(9)]
    assert [int(x) for x in b][:9] == closed


def test_v2_pair_is_sym2_partner():
    """The corrected (order-2, order-3) pair satisfies the C3 Sym² identity —
    the property C3/C3b actually consume."""
    res = verify_c3_sym2(ORDER2_ZAGIER["D"], ORDER3_AZ_COOPER["eta"], N=40)
    assert res["verdict"] == "PASS(40)"
