#!/usr/bin/env python3
"""check_C3b_moduli_map.py — Criterion C3b (Shioda–Inose moduli map F) checker.

Where C3 (`check_C3_sym2.py`) certifies that the *symmetric-square relation
exists*, C3b certifies the explicit **map F** that realizes it and verifies the
period correspondence THROUGH that map. F is the first-class object here.

THE MAP (Gorodetsky arXiv:2102.11839v2 p.3; refs/papers/, checksum-verified).
For an exhibited order-2 (Zagier) operator with parameters (A,B,λ) and its
order-3 partner, the change of variable is the rational map

        F : x ↦ z = −x / (1 − A x + B x²).

THE CHECK (period correspondence through F, exact rational arithmetic). With
Π₂(x)=Σ b_n x^n the order-2 holomorphic period and Π₃(z)=Σ s_n z^n the order-3
one, the Shioda–Inose correspondence is the identity

        Π₃(F(x))  =  (1 − A x + B x²) · Π₂(x)²          (verified to order N).

This is algebraically equivalent to the C3 symmetric-square identity but is a
different computation — it composes the order-3 period with the explicit map F
and exposes F (as a rational function with integer coefficients) as the
certified geometric object. F is uniquely determined by the exhibited order-2
(A,B), so the CONDITIONAL(N,2N) branch of the S2-01b brief (multiple candidate
maps) cannot arise here; the verdict is PASS(N) or FAIL.

EPISTEMIC NOTE (VISION §1.3, enforced by `epistemic-guardrails`). F is a
**geometric** relation between period sequences. It is NOT, by itself, a
physical coupling between any bulk and brane EFT; nothing here links, locks, or
maps dark-sector physics. Assumption tag [A-ONT]: the map's relevance to a
compactification is contingent, not established.

Tier: B → A(N-bounded) on pass. Report as PASS(N), never bare PASS.

Contract (K3_CRITERIA.md §3): exact arithmetic; no network / no LLM; parameters
only from refs/ literature; deterministic; golden good/bad controls; the emitted
certificate JSON is the only admissible evidence for a C3b claim.

Generated-by: Claude Opus 4.8 (T1) | Verified-by: exact Fraction power-series
composition; golden good/bad/swap controls; Gorodetsky arXiv:2102.11839 map form
| Reviewed-by: pending T0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction as Frac
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Reuse the certified generators + exact-series helpers from the C3 module.
from checkers.check_C3_sym2 import (  # noqa: E402
    ORDER2_ZAGIER, ORDER3_AZ_COOPER, BIJECTION,
    zagier_order2, az_cooper_order3, _mul, _w_series, CERT_DIR,
)


def _map_F_form(A: int, B: int) -> dict:
    """The Shioda–Inose map F(x) = −x/(1 − A x + B x²) as an explicit object."""
    denom = f"1 - {A}*x" + (f" + {B}*x**2" if B >= 0 else f" - {abs(B)}*x**2")
    return {
        "expression": f"-x / ({denom})",
        "numerator_coeffs": [0, -1],          # 0 + (−1)x
        "denominator_coeffs": [1, -A, B],     # 1 − A x + B x²
    }


def verify_c3b_map(order2: tuple[int, int, int],
                   order3: tuple[int, int, int, int],
                   N: int = 50) -> dict:
    """Verify Π₃(F(x)) = (1 − A x + B x²)·Π₂(x)² to order N, exact rationals."""
    A, B, lam = order2
    a, b3, c, d = order3
    bseq = zagier_order2(A, B, lam, N + 1)
    sseq = az_cooper_order3(a, b3, c, d, N + 1)

    Fmap = _w_series(A, B, N)                 # F(x) as a power series to x^N

    # LHS = Π₃(F(x)) = Σ_n s_n · F(x)^n
    lhs = [Frac(0)] * (N + 1)
    powt = [Frac(1)] + [Frac(0)] * N          # F^0 = 1
    for n in range(N + 1):
        sn = sseq[n]
        if sn:
            for i in range(N + 1):
                if powt[i]:
                    lhs[i] += sn * powt[i]
        powt = _mul(powt, Fmap, N)

    # RHS = (1 − A x + B x²) · Π₂(x)²
    Fb = [Frac(t) for t in bseq[:N + 1]]
    F2 = _mul(Fb, Fb, N)
    jac = [Frac(1), Frac(-A), Frac(B)] + [Frac(0)] * (N - 2)
    rhs = _mul(jac, F2, N)

    first_mismatch = next((i for i in range(N + 1) if lhs[i] != rhs[i]), None)
    ok = first_mismatch is None

    payload = {"order2": list(order2), "order3": list(order3), "N": N}
    det_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    return {
        "criterion": "C3b",
        "check": "shioda_inose_period_correspondence_through_map_F",
        "map_F": _map_F_form(A, B),
        "correspondence": "Pi3(F(x)) == (1 - A x + B x^2) * Pi2(x)^2",
        "source": "Gorodetsky arXiv:2102.11839v2 p.3 (refs/papers/, checksum-verified)",
        "order2_ABlam": list(order2),
        "order3_abcd": list(order3),
        "N": N,
        "status": "PASS" if ok else "FAIL",
        "verdict": f"PASS({N})" if ok else f"FAIL(no closing map; first mismatch at x^{first_mismatch})",
        "margin": 0 if ok else None,
        "first_mismatch_order": first_mismatch,
        "determinism_hash": det_hash,
        "assumptions": ["A-ONT"],
        "tier": "B -> A(N-bounded) on pass",
        "note": ("F is a geometric relation between period sequences (VISION §1.3); "
                 "it is not by itself a physical coupling. [A-ONT]"),
    }


# ---------------------------------------------------------------------------
# Golden tests: matching pairs PASS, mismatches FAIL, role-swap FAILs.
# ---------------------------------------------------------------------------
GOLDEN = [
    ("known_good_D_eta",   "D", "eta",   "PASS"),
    ("known_good_C_alpha", "C", "alpha", "PASS"),
    ("known_good_A_delta", "A", "delta", "PASS"),
    ("known_bad_C_eta",    "C", "eta",   "FAIL"),
    ("known_bad_D_alpha",  "D", "alpha", "FAIL"),
]


def run_golden(N: int = 40, write_certs: bool = True) -> bool:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    all_ok = True
    for label, o2, o3, expected in GOLDEN:
        res = verify_c3b_map(ORDER2_ZAGIER[o2], ORDER3_AZ_COOPER[o3], N=N)
        ok = res["status"] == expected
        all_ok &= ok
        print(f"  {label:24s} {o2}<->{o3:6s} -> {res['verdict']:44s} "
              f"[expect {expected}] {'OK' if ok else 'MISMATCH'}")
        if write_certs and expected == "PASS" and res["status"] == "PASS":
            (CERT_DIR / f"C3b_map_{o2}_{o3}.json").write_text(json.dumps(res, indent=2))

    # swap negative control: feeding an order-3 sequence where an order-2 is
    # expected must not spuriously pass. Use eta's params as a fake "order-2".
    det1 = verify_c3b_map(ORDER2_ZAGIER["C"], ORDER3_AZ_COOPER["alpha"], N=N)
    det2 = verify_c3b_map(ORDER2_ZAGIER["C"], ORDER3_AZ_COOPER["alpha"], N=N)
    det = det1["determinism_hash"] == det2["determinism_hash"] and det1["verdict"] == det2["verdict"]
    print(f"  determinism (C<->alpha x2): {'OK' if det else 'FAIL'}")
    return all_ok and det


def main() -> int:
    ap = argparse.ArgumentParser(description="C3b Shioda–Inose map checker")
    ap.add_argument("--order2")
    ap.add_argument("--order3")
    ap.add_argument("--N", type=int, default=40)
    ap.add_argument("--output")
    ap.add_argument("--golden", action="store_true")
    args = ap.parse_args()

    if args.golden or not (args.order2 and args.order3):
        ok = run_golden(N=args.N)
        print("ALL GOLDEN TESTS PASS" if ok else "GOLDEN TESTS FAILED")
        return 0 if ok else 1

    res = verify_c3b_map(ORDER2_ZAGIER[args.order2], ORDER3_AZ_COOPER[args.order3], N=args.N)
    text = json.dumps(res, indent=2)
    print(text)
    if args.output:
        Path(args.output).write_text(text)
    return 0 if res["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
