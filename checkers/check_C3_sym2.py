#!/usr/bin/env python3
"""check_C3_sym2.py — Criterion C3 (Symmetric-Square structure) checker.

Verifies, by EXACT rational arithmetic, that a candidate order-3 Apéry-like
sequence is the symmetric square of an exhibited order-2 (Zagier) sequence —
the honest, checkable content of the K3_CRITERIA.md C3 claim "L₃ = Sym²(L₂)".

THE CHECK (Gorodetsky, arXiv:2102.11839v2, p.3 — a checksum-verified source in
refs/papers/). For an order-2 sequence u_n with generating function
F(x)=Σ u_n x^n satisfying a Zagier recurrence with parameters (A,B,λ), and the
order-3 sequence u'_n corresponding to it, the symmetric-square relation is the
generating-function identity

        Σ_{n≥0} u'_n · w^{n+1}  =  (−x) · F(x)²,      w = −x / (1 − A x + B x²).

The change of variable w(x) is exactly the C3b Shioda–Inose / mirror map, so
this identity is the same-object statement of "order-3 operator = Sym²(order-2
operator)" AFTER that map. A same-variable operator equality L₃(z)=Sym²(L₂)(z)
does NOT hold for these pairs (verified: it fails even for known Sym² pairs) —
the map is not optional, which is why C3 and C3b are entangled here.

Method: build both sequences from their certified recurrences (exact Fraction,
integrality asserted at every step — no floats, no OEIS lookup, no model
recall), then compare the two sides of the identity coefficient-by-coefficient
as exact rational power series to order N. Margin is exact 0 on PASS.

Tier: B → A(N-bounded) on pass. Report as PASS(N), never bare PASS
(finite-order evidence, not a proof for all n).

Checker contract (K3_CRITERIA.md §3): exact arithmetic; no network / no LLM;
deterministic and seeded (there is no randomness here); ships golden-good and
golden-bad controls; the emitted certificate JSON is the only admissible
evidence source for any C3 claim in a report.

Generated-by: Claude Opus 4.8 (T1) | Verified-by: exact Fraction power-series
arithmetic, golden good/bad controls, cross-checked vs Gorodetsky arXiv:2102.11839
tables (in refs/) | Reviewed-by: pending T0
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Frac
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CERT_DIR = REPO_ROOT / "checkers" / "certificates"

# ---------------------------------------------------------------------------
# Candidate register — parameters ONLY from refs/ literature (Gorodetsky
# arXiv:2102.11839v2 tables, p.2–3). No sequence values are hard-coded; they
# are generated from these recurrence parameters below and integrality-checked.
# ---------------------------------------------------------------------------

# Order-2 Zagier family, recurrence (Gorodetsky eq. 1.5):
#   (n+1)^2 u_{n+1} = (A n^2 + A n + λ) u_n − B n^2 u_{n-1},  u_0=1, u_1=λ.
ORDER2_ZAGIER = {
    # name: (A, B, lambda)
    "A": (7, -8, 2),    # Franel numbers,  Σ C(n,k)^3
    "B": (9, 27, 3),
    "C": (10, 9, 3),    # Σ C(n,k)^2 C(2k,k)
    "D": (11, -1, 3),   # Apéry b_n,  Σ C(n,k)^2 C(n+k,k)
    "E": (12, 32, 4),
    "F": (17, 72, 6),
}

# Order-3 Almkvist–Zudilin / Cooper family, recurrence (Gorodetsky eq. 1.7):
#   (n+1)^3 u_{n+1} = (2n+1)(a n^2 + a n + b) u_n − (c n^3 + d n) u_{n-1},
#   u_0=1, u_1=b.   (Almkvist–Zudilin: d=0;  Cooper's extension: d≠0.)
ORDER3_AZ_COOPER = {
    # name: (a, b, c, d)
    "delta": (7, 3, 81, 0),     # Almkvist–Zudilin numbers
    "zeta":  (9, 3, -27, 0),
    "alpha": (10, 4, 64, 0),    # Domb numbers (A002895)
    "eta":   (11, 5, 125, 0),
    "epsilon": (12, 4, 16, 0),
    "gamma": (17, 5, 1, 0),     # Apéry a_n
    "s7":  (13, 4, -27, 3),     # Cooper s7
    "s10": (6, 2, -64, 4),      # Cooper s10 = Yang–Zudilin, Σ C(n,k)^4 (A005260)
    "s18": (14, 6, 192, -12),   # Cooper s18
}

# The Sym² bijection (Gorodetsky p.3): order-2 (A,B,λ) ↔ order-3
# (a,b,c)=(A, A−2λ, A²−4B). Matching pairs satisfy the identity; others do not.
BIJECTION = {"A": "delta", "B": "zeta", "C": "alpha",
             "D": "eta", "E": "epsilon", "F": "gamma"}


# ---------------------------------------------------------------------------
# Exact sequence generators (Fraction; integrality asserted every step)
# ---------------------------------------------------------------------------
def zagier_order2(A: int, B: int, lam: int, N: int) -> list[int]:
    u = [Frac(1), Frac(lam)]
    for n in range(1, N):
        val = ((A * n * n + A * n + lam) * u[n] - B * n * n * u[n - 1]) / Frac((n + 1) ** 2)
        if val.denominator != 1:
            raise ArithmeticError(f"order-2 (A={A},B={B},λ={lam}) non-integral at n={n}: {val}")
        u.append(val)
    return [int(t) for t in u[:N + 1]]


def az_cooper_order3(a: int, b: int, c: int, d: int, N: int) -> list[int]:
    u = [Frac(1), Frac(b)]
    for n in range(1, N):
        val = ((2 * n + 1) * (a * n * n + a * n + b) * u[n]
               - (c * n ** 3 + d * n) * u[n - 1]) / Frac((n + 1) ** 3)
        if val.denominator != 1:
            raise ArithmeticError(f"order-3 (a={a},b={b},c={c},d={d}) non-integral at n={n}: {val}")
        u.append(val)
    return [int(t) for t in u[:N + 1]]


# ---------------------------------------------------------------------------
# Exact power-series helpers (lists of Fraction, truncated at order M => x^M)
# ---------------------------------------------------------------------------
def _mul(p: list[Frac], q: list[Frac], M: int) -> list[Frac]:
    out = [Frac(0)] * (M + 1)
    for i, pi in enumerate(p):
        if pi == 0 or i > M:
            continue
        for j, qj in enumerate(q):
            if i + j > M:
                break
            if qj:
                out[i + j] += pi * qj
    return out


def _w_series(A: int, B: int, M: int) -> list[Frac]:
    """w = −x/(1 − A x + B x²) as a power series to order x^M.
    1/(1−Ax+Bx²): c_0=1, c_n = A c_{n-1} − B c_{n-2}."""
    c = [Frac(0)] * (M + 1)
    c[0] = Frac(1)
    for n in range(1, M + 1):
        c[n] = A * c[n - 1] - (B * c[n - 2] if n >= 2 else 0)
    w = [Frac(0)] * (M + 1)
    for n in range(M):
        w[n + 1] = -c[n]        # multiply by −x  (shift up by 1)
    return w


def verify_c3_sym2(order2: tuple[int, int, int],
                   order3: tuple[int, int, int, int],
                   N: int = 50) -> dict:
    """Verify the symmetric-square generating-function identity to order N.

    order2 = (A, B, λ);  order3 = (a, b, c, d).  Exact rational arithmetic.
    Returns a certificate dict; status is 'PASS' iff the identity holds
    coefficient-wise to order x^N with exact-zero margin."""
    A, B, lam = order2
    a, b3, c, d = order3
    M = N
    bseq = zagier_order2(A, B, lam, N + 1)
    sseq = az_cooper_order3(a, b3, c, d, N + 1)

    # RHS = (−x) · F(x)²   where F = Σ bseq[n] x^n
    Fb = [Frac(t) for t in bseq[:M + 1]]
    F2 = _mul(Fb, Fb, M)
    rhs = [Frac(0)] * (M + 1)
    for n in range(M):
        rhs[n + 1] = -F2[n]

    # LHS = Σ_n sseq[n] · w^{n+1}
    w = _w_series(A, B, M)
    lhs = [Frac(0)] * (M + 1)
    term = list(w)                     # w^1
    for n in range(M + 1):
        sn = sseq[n]
        if sn:
            for i in range(M + 1):
                if term[i]:
                    lhs[i] += sn * term[i]
        term = _mul(term, w, M)        # w^{n+2}

    first_mismatch = next((i for i in range(M + 1) if lhs[i] != rhs[i]), None)
    ok = first_mismatch is None

    payload = {"order2_ABlam": list(order2), "order3_abcd": list(order3), "N": N}
    det_hash = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()).hexdigest()

    return {
        "criterion": "C3",
        "check": "symmetric_square_generating_function_identity",
        "identity": "sum_n s_n w^{n+1} == (-x) F(x)^2, w=-x/(1-A x+B x^2)",
        "source": "Gorodetsky arXiv:2102.11839v2 p.3 (refs/papers/, checksum-verified)",
        "order2_ABlam": list(order2),
        "order3_abcd": list(order3),
        "order2_first_terms": bseq[:8],
        "order3_first_terms": sseq[:8],
        "N": N,
        "status": "PASS" if ok else "FAIL",
        "verdict": f"PASS({N})" if ok else f"FAIL(first mismatch at x^{first_mismatch})",
        "margin": 0 if ok else None,
        "first_mismatch_order": first_mismatch,
        "determinism_hash": det_hash,
        "assumptions": [],   # C3 is a mathematical operator identity (Tier B→A(N)); no physics assumption
        "tier": "B -> A(N-bounded) on pass",
    }


# ---------------------------------------------------------------------------
# Golden-test harness
# ---------------------------------------------------------------------------
GOLDEN = [
    # (label, order2_name, order3_name, expected_status)
    ("known_good_C_alpha_Domb", "C", "alpha", "PASS"),
    ("known_good_A_delta",      "A", "delta", "PASS"),
    ("known_good_D_eta",        "D", "eta",   "PASS"),
    ("known_bad_C_eta",         "C", "eta",   "FAIL"),   # wrong partner
    ("known_bad_D_alpha",       "D", "alpha", "FAIL"),
]


def run_golden(N: int = 40, write_certs: bool = True) -> bool:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    all_ok = True
    for label, o2, o3, expected in GOLDEN:
        res = verify_c3_sym2(ORDER2_ZAGIER[o2], ORDER3_AZ_COOPER[o3], N=N)
        ok = res["status"] == expected
        all_ok &= ok
        print(f"  {label:26s} {o2}<->{o3:6s} -> {res['verdict']:32s} "
              f"[expect {expected}] {'OK' if ok else 'MISMATCH'}")
        if write_certs and expected == "PASS" and res["status"] == "PASS":
            out = CERT_DIR / f"C3_sym2_{o2}_{o3}.json"
            out.write_text(json.dumps(res, indent=2))
    # determinism: same input twice -> identical hash + verdict
    r1 = verify_c3_sym2(ORDER2_ZAGIER["C"], ORDER3_AZ_COOPER["alpha"], N=N)
    r2 = verify_c3_sym2(ORDER2_ZAGIER["C"], ORDER3_AZ_COOPER["alpha"], N=N)
    det = r1["determinism_hash"] == r2["determinism_hash"] and r1["verdict"] == r2["verdict"]
    print(f"  determinism (C<->alpha x2): {'OK' if det else 'FAIL'}")
    return all_ok and det


def main() -> int:
    ap = argparse.ArgumentParser(description="C3 symmetric-square checker")
    ap.add_argument("--order2", help="Zagier name (A..F)")
    ap.add_argument("--order3", help="AZ/Cooper name (delta,alpha,eta,gamma,s7,s10,...)")
    ap.add_argument("--N", type=int, default=40)
    ap.add_argument("--output")
    ap.add_argument("--golden", action="store_true", help="run golden-test harness")
    args = ap.parse_args()

    if args.golden or not (args.order2 and args.order3):
        ok = run_golden(N=args.N)
        print("ALL GOLDEN TESTS PASS" if ok else "GOLDEN TESTS FAILED")
        return 0 if ok else 1

    res = verify_c3_sym2(ORDER2_ZAGIER[args.order2],
                         ORDER3_AZ_COOPER[args.order3], N=args.N)
    text = json.dumps(res, indent=2)
    print(text)
    if args.output:
        Path(args.output).write_text(text)
    return 0 if res["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
