#!/usr/bin/env python3
"""c3_normalization_applicability_2026_09_21.py — is criterion C3's checker APPLICABLE
to the K3_CRITERIA register primaries (Cooper s7, s10)?

WHY THIS IS NOT A C3 RUN. `checkers/check_C3_sym2.py` tests Gorodetsky's identity
    Sum_n s_n w^{n+1} == (-x) F(x)^2,   w = -x/(1 - A x + B x^2)
through the bijection (a, b, c) = (A, A - 2*lambda, A^2 - 4*B). That bijection emits
order-3 operators with **d = 0** only. Cooper s7 has d = 3 and s10 has d = 4, so feeding
them to that checker is a test that CANNOT PASS. Recording its output as a C3 `FAIL` would
label a normalization mismatch as a geometric falsification. This script therefore reports
**applicability**, never a C3 verdict, and writes to `data/derived/` — never to
`checkers/certificates/`, whose contents are (K3_CRITERIA.md §3.5) the only admissible
evidence for a C3 claim.

Exact rational arithmetic only (`Fraction`); deterministic; no network; no model recall.

NEGATIVE CONTROLS (this check can fail):
  NC-1  the six d=0 sporadic families must come out APPLICABLE and must reproduce the
        order-2 parameters coded in `check_C3_sym2.ORDER2_ZAGIER`. A disagreement means
        this script's inverse bijection is wrong, not that the family is.
  NC-2  a deliberate mutation (d: 0 -> 1) of each known-good family must flip it to
        INAPPLICABLE. Without this, "s7/s10 are inapplicable" could not be distinguished
        from "this script calls everything inapplicable".

Generated-by: Claude Opus 5 (Stream 3) | Verified-by: NC-1 against the committed
ORDER2_ZAGIER table + NC-2 mutation control, both enforced in-process (exit 1 on failure)
| Reviewed-by: pending T0
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from fractions import Fraction as Frac
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from checkers.check_C3_sym2 import (  # noqa: E402
    BIJECTION, ORDER2_ZAGIER, ORDER3_AZ_COOPER, zagier_order2,
)

N_INTEGRALITY = 40          # matches the N used by the committed C3/C1 certificates
OUT = REPO / "data/derived/c3_normalization_applicability_2026_09_21.json"


def invert_bijection(a: int, b: int, c: int, d: int) -> dict:
    """Gorodetsky p.3 bijection, inverted: (a,b,c) = (A, A-2*lam, A^2-4*B), d must be 0."""
    A = Frac(a)
    lam = Frac(a - b, 2)
    B = Frac(a * a - c, 4)
    return {"A": A, "lam": lam, "B": B, "d_is_zero": d == 0}


def applicability(name: str, abcd: tuple[int, int, int, int]) -> dict:
    a, b, c, d = abcd
    inv = invert_bijection(a, b, c, d)
    lam, B, A = inv["lam"], inv["B"], inv["A"]
    reasons: list[str] = []

    if not inv["d_is_zero"]:
        reasons.append(f"d = {d} != 0; the Sym^2 bijection emits only d = 0 operators")
    if lam.denominator != 1:
        reasons.append(f"lambda = {lam} is not an integer, so no integral order-2 partner exists")
    if B.denominator != 1:
        reasons.append(f"B = {B} is not an integer")

    # Does the implied order-2 partner even generate an integer sequence?
    order2_integral, order2_detail, order2_first = None, None, None
    if lam.denominator == 1 and B.denominator == 1:
        try:
            seq = zagier_order2(int(A), int(B), int(lam), N_INTEGRALITY)
            order2_integral, order2_first = True, seq[:8]
        except ArithmeticError as exc:
            order2_integral = False
            order2_detail = str(exc)
            reasons.append(f"implied order-2 partner (A,B,lambda)=({A},{B},{lam}) is "
                           f"non-integral: {exc}")

    applicable = not reasons
    return {
        "name": name,
        "order3_abcd": list(abcd),
        "implied_order2_ABlambda": [str(A), str(B), str(lam)],
        "implied_order2_is_a_coded_zagier_case": (int(A), int(B), int(lam)) in set(
            ORDER2_ZAGIER.values()) if (lam.denominator == 1 and B.denominator == 1) else False,
        "order2_sequence_integral_to_N": order2_integral,
        "order2_first_terms": order2_first,
        "order2_non_integrality_detail": order2_detail,
        "verdict": "APPLICABLE" if applicable else "INAPPLICABLE_NORMALIZATION",
        "reasons": reasons,
    }


def main() -> int:
    rows = {n: applicability(n, p) for n, p in ORDER3_AZ_COOPER.items()}

    # ---- NC-1: the six d=0 sporadic families must be APPLICABLE and reproduce ORDER2_ZAGIER
    nc1 = {}
    for o2, o3 in BIJECTION.items():
        r = rows[o3]
        coded = ORDER2_ZAGIER[o2]
        derived = tuple(int(Frac(x)) for x in r["implied_order2_ABlambda"])
        nc1[f"{o2}<->{o3}"] = {
            "verdict": r["verdict"],
            "coded_ABlambda": list(coded),
            "derived_ABlambda": list(derived),
            "agrees": derived == coded and r["verdict"] == "APPLICABLE",
        }
    nc1_pass = all(v["agrees"] for v in nc1.values())

    # ---- NC-2: mutating d 0 -> 1 on each known-good family must flip it to INAPPLICABLE
    nc2 = {}
    for o3 in BIJECTION.values():
        a, b, c, _ = ORDER3_AZ_COOPER[o3]
        mutated = applicability(f"{o3}_mutated_d1", (a, b, c, 1))
        nc2[o3] = {"verdict": mutated["verdict"],
                   "flips": mutated["verdict"] == "INAPPLICABLE_NORMALIZATION"}
    nc2_pass = all(v["flips"] for v in nc2.values())

    payload = {
        "artifact": "c3_normalization_applicability",
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "label": "MATH-APPLICABILITY — not a C3 verdict, not exclusion, not FIT, not TEST",
        "question": "Is checkers/check_C3_sym2.py applicable to the K3_CRITERIA register "
                    "primaries (Cooper s7, s10)?",
        "normalization": "Gorodetsky arXiv:2102.11839v2 p.3: (a,b,c)=(A, A-2*lambda, A^2-4*B), d=0",
        "source": "refs/papers/ (checksum-verified); operator table checkers/check_C3_sym2.py",
        "N_integrality": N_INTEGRALITY,
        "candidates": rows,
        "negative_control_NC1_known_good_reproduced": {"pass": nc1_pass, "detail": nc1},
        "negative_control_NC2_mutation_flips": {"pass": nc2_pass, "detail": nc2},
        "register_primaries": {
            n: {"verdict": rows[n]["verdict"], "reasons": rows[n]["reasons"]}
            for n in ("s7", "s10") if n in rows
        },
        "consequence": (
            "No C3 certificate can be produced for s7 or s10 with the committed checker. "
            "The absence of checkers/certificates/C3_sym2_*_s7.json and *_s10.json is a "
            "normalization gap, NOT a recorded geometric failure. Producing a C3 verdict for "
            "either candidate requires an order-3 Sym^2 identity valid for d != 0, with a "
            "citation, added to the checker under K3_CRITERIA.md section 6 amendment."),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))          # persist BEFORE printing

    for n, r in rows.items():
        print(f"  {n:8s} abcd={tuple(r['order3_abcd'])!s:20s} -> {r['verdict']}")
        for why in r["reasons"]:
            print(f"           - {why}")
    print(f"  NC-1 known-good reproduced : {'PASS' if nc1_pass else 'FAIL'}")
    print(f"  NC-2 mutation flips        : {'PASS' if nc2_pass else 'FAIL'}")
    print(f"  artifact: {OUT.relative_to(REPO)}")
    return 0 if (nc1_pass and nc2_pass) else 1


if __name__ == "__main__":
    raise SystemExit(main())
