#!/usr/bin/env python3
"""c3_sym2_gauge_existence_2026_09_21.py — does an order-2 operator L2 exist AT ALL for the
K3_CRITERIA register primaries, in any gauge? And can C3 discriminate within their family?

This settles branch (iii) of briefs/STREAM3_K3_SELECTION_ROUTE_AUDIT_2026_09_21.md sec.3.
`c3_normalization_applicability_2026_09_21.py` showed only that the COMMITTED checker's
d = 0 bijection cannot run on s7/s10, leaving three branches: (i) an uncoded d != 0
identity, (ii) gauge-equivalence to a d = 0 operator, (iii) no order-2 L2 exists at all.
Branch (iii) would be a C3 FAILURE under C3's own definition ("an explicitly exhibited
order-2 operator L2"), not a normalization gap.

RESULT: branch (iii) is EXCLUDED, and for a stronger reason than one candidate at a time.
The vanishing is an IDENTITY IN THE SYMBOLIC PARAMETERS (a, b, c, d) of the AZ/Cooper
operator shape, so every member of that family is anti-self-adjoint and therefore (for
irreducible L3) a symmetric square. s7 and s10 are members. Two consequences:
  * an order-2 L2 exists for both, exhibited as d^2 + P/4 in the projective normal form;
  * **C3 has no discriminating power inside this family** — every member satisfies it by
    the shape of the recurrence, so C3 cannot rank or separate register candidates drawn
    from it. That is a finding about the criterion, not about any candidate.

WHAT IS DECIDED, AND WHAT IS NOT. The test is **projective (gauge) equivalence** to a
symmetric square, in the same variable z. K3_CRITERIA C3 instead requires equality of
operators in a fixed normalization. The two outcomes are NOT symmetric:
  * nonzero -> NO_SYM2_IN_ANY_GAUGE: decisive; no order-2 L2 exists in any gauge.
  * zero    -> SYM2_EXISTS_UP_TO_GAUGE: branch (iii) excluded and an L2 exhibited. This is
               NOT a C3 pass. The exhibited L2 need not meet C3's normalization, and the
               integrality of its associated sequence is a separate question — the s10
               partner (6,25,2) is already known non-integral at n = 1.
Verdicts are `NO_SYM2_IN_ANY_GAUGE` / `SYM2_EXISTS_UP_TO_GAUGE`, never PASS/FAIL, and the
artifact goes to `data/derived/`, never to `checkers/certificates/`.

SCOPE LIMIT. "Anti-self-adjoint <=> symmetric square" requires L3 irreducible; for a
reducible L3 the reading can degenerate. Irreducibility is NOT checked here and is not
claimed. This is recorded in the artifact as `scope_limits`.

NO-LLM-RECALL (VISION sec.6.1). Nothing is a cited formula. Derived at run time:
  D1. Sym^2 of an order-2 operator: if y'' = -r y then u = y1*y2 satisfies
      u''' + 4 r u' + 2 r' u = 0. Verified by substituting a generic product and reducing
      the y_i''/y_i''' terms; residual must be identically 0.
  D2. The projective normal form: the substitution y = w*u with w'/w = -p2/3 is carried out
      symbolically and P, Q are read off; the classical closed forms are never typed in.
      The u'' coefficient must come out 0, which is checked.
  D3. (consistency check, NOT a derivation — see `derive_adjoint_condition`.) The formal
      adjoint of d^3 + P d + Q is hand-supplied as -d^3 - (P .)' + Q, and L* + L is
      confirmed to collapse to (2Q - P') f, so L* = -L iff 2Q - P' == 0.
Vanishing is tested by `cancel` + zero-polynomial test on the numerator — never by
sampling, never by eyeballing `simplify`.

NEGATIVE CONTROLS (all enforced; exit 1 on any failure):
  NC-0  the theta -> d/dz conversion is validated against the committed sequence generator:
        the reconstructed operator must annihilate each candidate's own power series.
  NC-1  SHAPE controls. Breaking the AZ/Cooper shape symbolically — c(th+1)^3 -> c*th^3, and
        dropping the (2th+1) factor — must make 2Q - P' NONZERO. Without these, the
        family-wide identity could be an artifact of the normal-form code rather than a
        property of the shape.
  NC-2  OFF-FAMILY controls: explicit d/dz-form operators with 2Q - P' provably nonzero
        (hand-computed in the table) must come out NO_SYM2_IN_ANY_GAUGE.
  NC-3  ANCHOR to committed data: every family carrying a committed C3_sym2_*.json whose
        own recorded status is PASS must come out SYM2_EXISTS_UP_TO_GAUGE, and at least
        three such certificates must be found. Anchored this way it can fail — if the
        certificates were absent, unreadable, or not PASS, NC-3 fails rather than passing
        vacuously. (An earlier version asserted only "the six d = 0 families come out
        SYM2_EXISTS", which the symbolic identity makes true for every input in the family:
        a control that cannot fail. Fixed.)

DOCUMENTED EXPECTED NON-MATCH. P/4 does NOT equal the projective normal form R of the
Zagier order-2 partner (checked, reported in `order2_partner_coordinate_note`). That is
expected, not a defect: the Gorodetsky C3 identity carries a change of variable
w = -x/(1 - A x + B x^2), so the Zagier L2 lives in the w coordinate while P/4 lives in z.
Being a symmetric square is invariant under change of variable, so both readings stand.

Generated-by: Claude Opus 5 (Stream 3) | Verified-by: D1/D3 derivations executed, NC-0
series annihilation, NC-1 two shape controls, NC-2 off-family controls, NC-3 vs committed
certificates, all enforced in-process | Reviewed-by: pending T0
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from checkers.check_C3_sym2 import (  # noqa: E402
    BIJECTION, ORDER2_ZAGIER, ORDER3_AZ_COOPER, az_cooper_order3,
)

z = sp.Symbol("z")
OUT = REPO / "data/derived/c3_sym2_gauge_existence_2026_09_21.json"
CERT_DIR = REPO / "checkers/certificates"


def th(e):
    return z * sp.diff(e, z)


def _tp1(e):
    return th(e) + e


def l3_applied(a, b, c, d, y):
    """L = th^3 - z(2th+1)(a th^2 + a th + b) + z^2( c(th+1)^3 + d(th+1) ) applied to y."""
    v = a * th(th(y)) + a * th(y) + b * y
    return th(th(th(y))) - z * (2 * th(v) + v) + z ** 2 * (c * _tp1(_tp1(_tp1(y))) + d * _tp1(y))


def l3_shape_broken_cube(a, b, c, d, y):
    """NC-1 control: c(th+1)^3 -> c*th^3."""
    v = a * th(th(y)) + a * th(y) + b * y
    return th(th(th(y))) - z * (2 * th(v) + v) + z ** 2 * (c * th(th(th(y))) + d * _tp1(y))


def l3_shape_broken_factor(a, b, c, d, y):
    """NC-1 control: drop the (2th+1) factor."""
    v = a * th(th(y)) + a * th(y) + b * y
    return th(th(th(y))) - z * v + z ** 2 * (c * _tp1(_tp1(_tp1(y))) + d * _tp1(y))


def l2_applied(A, B, lam, y):
    """Zagier order-2: th^2 - z(A th^2 + A th + lam) + B z^2 (th+1)^2, applied to y."""
    return th(th(y)) - z * (A * th(th(y)) + A * th(y) + lam * y) + B * z ** 2 * _tp1(_tp1(y))


def dz_coefficients(applied, y, order):
    e = sp.expand(applied)
    out = []
    for k in range(order, 0, -1):
        ck = sp.simplify(e.coeff(sp.Derivative(y, (z, k))))
        out.append(ck)
        e = sp.expand(e - ck * sp.Derivative(y, (z, k)))
    out.append(sp.simplify(e.coeff(y)))
    return out


# ---- D1: derive Sym^2(d^2 + r) = d^3 + 4 r d + 2 r' --------------------------
def derive_sym2_form():
    r = sp.Function("r")(z)
    y1, y2 = sp.Function("y1")(z), sp.Function("y2")(z)
    expr = (sp.diff(y1 * y2, z, 3) + 4 * r * sp.diff(y1 * y2, z)
            + 2 * sp.diff(r, z) * (y1 * y2))
    for f in (y1, y2):
        expr = expr.subs(sp.Derivative(f, (z, 3)),
                         -sp.diff(r, z) * f - r * sp.diff(f, z))
        expr = expr.subs(sp.Derivative(f, (z, 2)), -r * f)
    expr = sp.expand(sp.simplify(expr))
    return expr == 0, f"residual = {expr}"


# ---- D3: derive the adjoint condition, i.e. that the test is 2Q - P' ---------
def derive_adjoint_condition():
    """CONSISTENCY CHECK, not a derivation — the adjoint is supplied, then checked.

    The formal adjoint of d^3 + P d + Q is written down as -d^3 - (P .)' + Q and this
    function confirms that L* + L collapses exactly to (2Q - P') f, so that L* = -L iff
    2Q - P' = 0. The adjoint itself is hand-supplied rather than derived by parts, so this
    is weaker than D1: it verifies the algebra of the step, not the step's premise. Recorded
    honestly rather than described as a derivation (VISION sec.6.1). D1 IS a real derivation.
    """
    P, Q = sp.Function("P")(z), sp.Function("Q")(z)
    f = sp.Function("f")(z)
    L = sp.diff(f, z, 3) + P * sp.diff(f, z) + Q * f
    # formal adjoint applied to f: -f''' - (P f)' + Q f
    Ladj = -sp.diff(f, z, 3) - sp.diff(P * f, z) + Q * f
    resid = sp.expand(sp.simplify(Ladj + L))     # L* + L  == (2Q - P') f  when it collapses
    target = sp.expand((2 * Q - sp.diff(P, z)) * f)
    return sp.simplify(resid - target) == 0, f"L*+L - (2Q-P')f = {sp.simplify(resid - target)}"


def normal_form(A3, A2, A1, A0):
    p2, p1, p0 = [sp.cancel(x / A3) for x in (A2, A1, A0)]
    s = sp.cancel(-p2 / 3)
    s1, s2 = sp.diff(s, z), sp.diff(s, z, 2)
    w1, w2, w3 = s, s1 + s ** 2, s2 + 3 * s * s1 + s ** 3
    c_upp = sp.cancel(3 * s + p2)
    P = sp.cancel(3 * w2 + 2 * p2 * w1 + p1)
    Q = sp.cancel(w3 + p2 * w2 + p1 * w1 + p0)
    return c_upp, P, Q


def normal_form_order2(B2, B1, B0):
    q1, q0 = [sp.cancel(x / B2) for x in (B1, B0)]
    t = sp.cancel(-q1 / 2)
    c_up = sp.cancel(2 * t + q1)
    R = sp.cancel(sp.diff(t, z) + t ** 2 + q1 * t + q0)
    return c_up, R


def rational_is_zero(expr) -> bool:
    num, _ = sp.fraction(sp.cancel(sp.together(sp.expand(expr))))
    num = sp.expand(sp.simplify(num))
    if num == 0:
        return True
    free = num.free_symbols - {z}
    return bool(sp.Poly(num, z, *sorted(free, key=str)).is_zero)


def classify(applied, y, label) -> dict:
    c_upp, P, Q = normal_form(*dz_coefficients(applied, y, 3))
    if not rational_is_zero(c_upp):
        raise ArithmeticError(f"{label}: normal form left a u'' term: {c_upp}")
    defect = sp.cancel(sp.together(2 * Q - sp.diff(P, z)))
    is_sym2 = rational_is_zero(defect)
    return {
        "label": label,
        "verdict": "SYM2_EXISTS_UP_TO_GAUGE" if is_sym2 else "NO_SYM2_IN_ANY_GAUGE",
        "defect_2Q_minus_Pprime": "0" if is_sym2 else sp.sstr(sp.simplify(defect)),
        "P": sp.sstr(P),
        "exhibited_r_for_L2_dd_plus_r": sp.sstr(sp.cancel(P / 4)) if is_sym2 else None,
    }


def annihilates_series(abcd, n_terms=14, check_to=9) -> bool:
    a, b, c, d = abcd
    u = az_cooper_order3(a, b, c, d, n_terms)
    y = sum(sp.Integer(int(t)) * z ** i for i, t in enumerate(u))
    res = sp.expand(l3_applied(a, b, c, d, y))
    return all(sp.simplify(sp.expand(res).coeff(z, k)) == 0 for k in range(check_to))


def main() -> int:
    y = sp.Function("y")(z)
    ok_d1, d1_detail = derive_sym2_form()
    ok_d3, d3_detail = derive_adjoint_condition()

    # ---- headline: the symbolic family identity
    sa, sb, sc, sd = sp.symbols("a b c d")
    fam = classify(l3_applied(sa, sb, sc, sd, y), y, "AZ/Cooper shape, symbolic (a,b,c,d)")
    family_identity = fam["verdict"] == "SYM2_EXISTS_UP_TO_GAUGE"

    # ---- NC-1 shape controls
    nc1 = {}
    for nm, fn in (("c_theta_cubed_instead_of_theta_plus_1_cubed", l3_shape_broken_cube),
                   ("drop_the_2theta_plus_1_factor", l3_shape_broken_factor)):
        r = classify(fn(sa, sb, sc, sd, y), y, nm)
        nc1[nm] = {"verdict": r["verdict"],
                   "breaks": r["verdict"] == "NO_SYM2_IN_ANY_GAUGE"}
    nc1_pass = all(v["breaks"] for v in nc1.values())

    # ---- NC-2 off-family controls, with 2Q-P' computed by hand in the comment
    one = sp.Integer(1)
    off = {                                   # (A3, A2, A1, A0)
        "d3 + z d + 1":      (one, sp.Integer(0), z, one),          # P=z,Q=1 -> 2-1=1
        "d3 + d2 + d + z":   (one, one, one, z),
        "d3 + z d + z^2":    (one, sp.Integer(0), z, z ** 2),       # 2z^2-1 != 0
    }
    nc2 = {}
    for nm, (A3, A2, A1, A0) in off.items():
        c_upp, P, Q = normal_form(A3, A2, A1, A0)
        defect = sp.cancel(sp.together(2 * Q - sp.diff(P, z)))
        v = "SYM2_EXISTS_UP_TO_GAUGE" if rational_is_zero(defect) else "NO_SYM2_IN_ANY_GAUGE"
        nc2[nm] = {"verdict": v, "detects": v == "NO_SYM2_IN_ANY_GAUGE"}
    nc2_pass = all(v["detects"] for v in nc2.values())

    # ---- per-candidate + NC-0 + NC-3
    rows, nc0 = {}, {}
    for name, abcd in ORDER3_AZ_COOPER.items():
        rows[name] = classify(l3_applied(*abcd, y), y, name) | {"order3_abcd": list(abcd)}
        nc0[name] = annihilates_series(abcd)
    nc0_pass = all(nc0.values())

    known_good = sorted(set(BIJECTION.values()))
    nc3 = {}
    for n in known_good:
        cert_path = next(iter(CERT_DIR.glob(f"C3_sym2_*_{n}.json")), None)
        if cert_path is None:
            nc3[n] = {"verdict": rows[n]["verdict"], "committed_certificate": None,
                      "anchored": False}
            continue
        cert = json.loads(cert_path.read_text())
        nc3[n] = {
            "verdict": rows[n]["verdict"],
            "committed_certificate": cert_path.name,
            "certificate_status": cert.get("status"),
            "anchored": True,
            "ok": cert.get("status") == "PASS"
                 and rows[n]["verdict"] == "SYM2_EXISTS_UP_TO_GAUGE",
        }
    anchored = [v for v in nc3.values() if v["anchored"]]
    # Must find at least 3 anchoring certificates AND agree with every one of them.
    nc3_pass = len(anchored) >= 3 and all(v["ok"] for v in anchored)

    # ---- documented expected non-match against the Zagier partner's R
    note = {}
    for o2, o3 in BIJECTION.items():
        c_up, R = normal_form_order2(*dz_coefficients(l2_applied(*ORDER2_ZAGIER[o2], y), y, 2))
        P = sp.sympify(rows[o3]["P"])
        note[f"{o2}<->{o3}"] = {"P_over_4_equals_R": rational_is_zero(sp.cancel(P / 4 - R))}

    payload = {
        "artifact": "c3_sym2_gauge_existence",
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "label": "MATH-EXISTENCE — projective/gauge equivalence only; not a C3 verdict, "
                 "not exclusion, not FIT, not TEST",
        "question": "Does an order-2 L2 with L3 = Sym^2(L2) exist in ANY gauge for the "
                    "K3_CRITERIA register primaries, and can C3 discriminate within their family?",
        "derivations_executed_at_runtime": {
            "D1_sym2_of_order2": "Sym^2(d^2 + r) = d^3 + 4 r d + 2 r'",
            "D1_verified": ok_d1, "D1_detail": d1_detail,
            "D3_test_is_2Q_minus_Pprime": ok_d3, "D3_detail": d3_detail,
        },
        "headline_family_identity": {
            "statement": "For the AZ/Cooper shape th^3 - z(2th+1)(a th^2 + a th + b) "
                         "+ z^2(c(th+1)^3 + d(th+1)), 2Q - P' vanishes IDENTICALLY in the "
                         "symbolic parameters (a, b, c, d).",
            "holds": family_identity,
            "defect": fam["defect_2Q_minus_Pprime"],
            "consequence_1": "An order-2 L2 exists for every member, including s7 and s10; "
                             "branch (iii) of the audit sec.3 is EXCLUDED.",
            "consequence_2": "C3 has NO discriminating power inside this family — every "
                             "member satisfies it by the shape of the recurrence. C3 cannot "
                             "rank or separate register candidates drawn from it.",
            "consequence_2_scope": "Applies to register entries IN THIS FAMILY (s7, s10). "
                                   "K3_CRITERIA.md also registers S22 and t103, whose defining "
                                   "recurrences are TBD-AT-FREEZE and are absent from "
                                   "ORDER3_AZ_COOPER, so whether they belong to this family is "
                                   "UNRESOLVED and is not claimed either way here.",
            "consequence_3": "C1 is left as the only committed checker with per-candidate "
                             "discriminating power on this register (C1 certificates exist at "
                             "PASS(40) for s7, s10, alpha, gamma, delta, eta), since C3 is "
                             "non-discriminating here and C3b is gated on C3.",
        },
        "scope_limits": [
            "Tests projective (gauge) equivalence in the variable z, NOT C3's equality in a "
            "fixed normalization. SYM2_EXISTS_UP_TO_GAUGE is not a C3 pass.",
            "'Anti-self-adjoint <=> symmetric square' requires L3 irreducible. Irreducibility "
            "is NOT checked here and is not claimed.",
            "Integrality of the exhibited L2's sequence is a separate question and is not "
            "addressed; the s10 partner (6,25,2) is known non-integral at n = 1.",
        ],
        "candidates": rows,
        "register_primaries": {n: {"verdict": rows[n]["verdict"],
                                   "exhibited_r": rows[n]["exhibited_r_for_L2_dd_plus_r"]}
                               for n in ("s7", "s10") if n in rows},
        "order2_partner_coordinate_note": {
            "P_over_4_vs_zagier_R": note,
            "explanation": "A non-match is EXPECTED, not a defect: the Gorodetsky C3 identity "
                           "carries the change of variable w = -x/(1 - A x + B x^2), so the "
                           "Zagier L2 lives in the w coordinate while P/4 lives in z. Being a "
                           "symmetric square is invariant under change of variable.",
        },
        "negative_control_NC0_operator_annihilates_own_series": {"pass": nc0_pass, "detail": nc0},
        "negative_control_NC1_shape_breaks_the_identity": {"pass": nc1_pass, "detail": nc1},
        "negative_control_NC2_off_family_detected": {"pass": nc2_pass, "detail": nc2},
        "negative_control_NC3_anchored_to_committed_certificates": {
            "pass": nc3_pass, "anchoring_certificates_found": len(anchored),
            "minimum_required": 3, "detail": nc3},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))          # persist BEFORE printing

    print(f"  D1 Sym^2 form derived        : {'OK' if ok_d1 else 'FAIL'} ({d1_detail})")
    print(f"  D3 test is 2Q - P' derived   : {'OK' if ok_d3 else 'FAIL'}")
    print(f"  FAMILY IDENTITY (symbolic)   : 2Q-P' == 0 for all (a,b,c,d) -> {family_identity}")
    for n, r in rows.items():
        tag = "known-good" if n in known_good else "CANDIDATE "
        print(f"    {tag} {n:8s} {tuple(r['order3_abcd'])!s:20s} -> {r['verdict']}")
    print(f"  NC-0 annihilates own series  : {'PASS' if nc0_pass else 'FAIL'}")
    print(f"  NC-1 shape controls break it : {'PASS' if nc1_pass else 'FAIL'}")
    print(f"  NC-2 off-family detected     : {'PASS' if nc2_pass else 'FAIL'}")
    print(f"  NC-3 anchored to {len(anchored)} certs      : {'PASS' if nc3_pass else 'FAIL'}")
    print(f"  artifact: {OUT.relative_to(REPO)}")
    all_ok = all([ok_d1, ok_d3, family_identity, nc0_pass, nc1_pass, nc2_pass, nc3_pass])
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
