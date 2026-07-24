#!/usr/bin/env python3
"""check_C1_mirror_integrality.py — Criterion C1 (mirror-map integrality).

Verifies, by EXACT rational arithmetic, that the inverse mirror map of a
candidate order-3 Picard–Fuchs operator has integer q-expansion coefficients up
to order N₁. Finite-order integrality is EVIDENCE, not proof → report PASS(N₁).

NORMALIZATION (fixed here, stated explicitly per K3_CRITERIA.md C1). The
operator (Gorodetsky eq. 1.7, refs/papers/, checksum-verified) is

    L = θ³ − z(2θ+1)(a θ²+a θ+b) + z²( c(θ+1)³ + d(θ+1) ),   θ = z d/dz,

with a maximal-unipotent-monodromy point at z=0 (indicial θ³). Its holomorphic
solution is y₀(z)=Σ aₙ zⁿ (the candidate sequence). The Frobenius log-solution is
y₁ = y₀·log z + Σ aₙ'(0) zⁿ, where aₙ(ρ) solves the ρ-shifted recurrence and
aₙ'(0)=d/dρ aₙ(ρ)|₀. The (inverse) mirror map is

    q = z·exp( (Σ aₙ'(0) zⁿ) / y₀(z) ),        z(q) = q + Σ_{n≥2} mₙ qⁿ.

C1 PASS(N₁) iff mₙ ∈ ℤ for all n ≤ N₁. The margin reported is the largest
denominator among m₂..m_{N₁} (1 on a clean pass).

METHOD. aₙ(0) and aₙ'(0) are carried together as exact dual numbers in ρ (no
symbolic ρ, no floats); the series operations (inverse, exp, reversion) are exact
`Fraction` power-series arithmetic. Deterministic; no network; no model recall.

Tier: B → A(N₁-bounded) on pass. Assumption tag: [] (pure mathematics — C1 makes
no physical claim). Certificate JSON is the only admissible evidence for a C1
claim in any report.

Generated-by: Claude Opus 4.8 (T1) | Verified-by: exact Fraction/dual-number
Frobenius mirror map; golden good (sporadic operators) + bad (perturbed
operators) controls | Reviewed-by: pending T0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction as Frac
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from checkers.check_C3_sym2 import ORDER3_AZ_COOPER, CERT_DIR  # noqa: E402


# ---------------------------------------------------------------------------
# Exact power-series helpers (lists of Fraction; index = power; length N+1)
# ---------------------------------------------------------------------------
def _mul(p, q, N):
    o = [Frac(0)] * (N + 1)
    for i, pi in enumerate(p):
        if pi == 0 or i > N:
            continue
        for j, qj in enumerate(q):
            if i + j > N:
                break
            if qj:
                o[i + j] += pi * qj
    return o


def _inv(p, N):
    """1/p as a series, requires p[0] != 0."""
    o = [Frac(0)] * (N + 1)
    o[0] = 1 / p[0]
    for n in range(1, N + 1):
        s = Frac(0)
        for k in range(1, n + 1):
            if k < len(p) and p[k]:
                s += p[k] * o[n - k]
        o[n] = -s / p[0]
    return o


def _exp(p, N):
    """exp(p) as a series, requires p[0] == 0."""
    o = [Frac(0)] * (N + 1)
    o[0] = Frac(1)
    for n in range(1, N + 1):
        s = Frac(0)
        for k in range(1, n + 1):
            if k < len(p) and p[k]:
                s += k * p[k] * o[n - k]
        o[n] = s / n
    return o


def _revert(q, N):
    """Series reversion: given q(z)=z+…  return z(w)=w+…  with q(z(w))=w."""
    c = [Frac(0)] * (N + 1)
    c[1] = Frac(1)
    for n in range(2, N + 1):
        ztrial = list(c)
        ztrial[n] = Frac(0)
        comp = [Frac(0)] * (N + 1)          # q(ztrial)
        zp = [Frac(0)] * (N + 1)
        zp[0] = Frac(1)
        for k in range(N + 1):
            if k < len(q) and q[k]:
                for i in range(N + 1):
                    if zp[i]:
                        comp[i] += q[k] * zp[i]
            zp = _mul(zp, ztrial, N)
        c[n] = -comp[n]                     # coeff of unknown c[n] in comp[n] is q[1]=1
    return c


# ---------------------------------------------------------------------------
# Dual numbers in the indicial parameter ρ (value, d/dρ at ρ=0), exact
# ---------------------------------------------------------------------------
class _Dual:
    __slots__ = ("v", "d")

    def __init__(self, v, d=Frac(0)):
        self.v = Frac(v)
        self.d = Frac(d)

    def _c(self, o):
        return o if isinstance(o, _Dual) else _Dual(o)

    def __add__(self, o):
        o = self._c(o)
        return _Dual(self.v + o.v, self.d + o.d)
    __radd__ = __add__

    def __sub__(self, o):
        o = self._c(o)
        return _Dual(self.v - o.v, self.d - o.d)

    def __mul__(self, o):
        o = self._c(o)
        return _Dual(self.v * o.v, self.v * o.d + self.d * o.v)
    __rmul__ = __mul__

    def __truediv__(self, o):
        o = self._c(o)
        return _Dual(self.v / o.v, (self.d * o.v - self.v * o.d) / (o.v * o.v))

    def __neg__(self):
        return _Dual(-self.v, -self.d)

    def cube(self):
        return self * self * self


def _frobenius(a, b, c, d, N):
    """Return (y0, h): y0[n]=aₙ(0) (holomorphic sol), h[n]=aₙ'(0) (log-part)."""
    A = [_Dual(1, 0)]                        # a_0(ρ)=1 exactly
    for n in range(1, N + 1):
        t1 = _Dual(n - 1, 1)                 # (n-1)+ρ
        t2 = _Dual(n - 2, 1)                 # (n-2)+ρ
        tn = _Dual(n, 1)                     # n+ρ
        p1 = -(_Dual(2) * t1 + _Dual(1)) * (_Dual(a) * t1 * t1 + _Dual(a) * t1 + _Dual(b))
        num = p1 * A[n - 1]
        if n >= 2:
            p2 = _Dual(c) * (t2 + _Dual(1)).cube() + _Dual(d) * (t2 + _Dual(1))
            num = num + p2 * A[n - 2]
        A.append((-num) / tn.cube())
    y0 = [x.v for x in A]
    h = [x.d for x in A]
    h[0] = Frac(0)
    return y0, h


def mirror_map_zq(order3: tuple[int, int, int, int], N: int):
    """Inverse mirror map z(q) coefficients [0, 1, m₂, …, m_N] (exact Fraction)."""
    a, b, c, d = order3
    y0, h = _frobenius(a, b, c, d, N)
    S = _mul(h, _inv(y0, N), N)             # S = h / y0  (S[0]=0)
    Q = _exp(S, N)                          # exp(S)
    qz = [Frac(0)] * (N + 1)                # q(z) = z·exp(S)
    for n in range(N):
        qz[n + 1] = Q[n]
    return _revert(qz, N)


def verify_c1(order3: tuple[int, int, int, int], N1: int = 50) -> dict:
    zq = mirror_map_zq(order3, N1)
    coeffs = zq[1:N1 + 1]                    # m_1=1, m_2, …
    first_bad = next((n for n in range(2, N1 + 1) if zq[n].denominator != 1), None)
    ok = first_bad is None
    max_denom = max((zq[n].denominator for n in range(2, N1 + 1)), default=1)

    payload = {"order3": list(order3), "N1": N1}
    det_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    return {
        "criterion": "C1",
        "check": "inverse_mirror_map_integrality",
        "normalization": "q = z*exp((sum a_n'(0) z^n)/y0); z(q)=q+sum m_n q^n; integrality is m_n in Z",
        "source": "Gorodetsky arXiv:2102.11839v2 eq.(1.7) operator (refs/papers/, checksum-verified)",
        "order3_abcd": list(order3),
        "holomorphic_first_terms": [int(t) for t in y0_first(order3)],
        "mirror_map_first_coeffs": [str(x) for x in zq[1:9]],
        "N1": N1,
        "status": "PASS" if ok else "FAIL",
        "verdict": f"PASS({N1})" if ok else f"FAIL(first non-integral at q^{first_bad})",
        "margin_max_denominator": int(max_denom),
        "first_non_integral_order": first_bad,
        "determinism_hash": det_hash,
        "assumptions": [],
        "tier": "B -> A(N1-bounded) on pass",
    }


def y0_first(order3, k=8):
    y0, _ = _frobenius(*order3, k)
    return y0[:k]


# ---------------------------------------------------------------------------
# Golden tests. Good: sporadic operators (integral mirror). Bad: perturbed
# operators whose mirror map has a non-integer coefficient at low order.
# ---------------------------------------------------------------------------
GOLDEN_GOOD = ["gamma", "alpha", "delta", "eta", "s7", "s10"]
GOLDEN_BAD = {
    "Domb_perturbed_c63": (10, 4, 63, 0),   # Domb (10,4,64) with c→63
    "Apery_perturbed_c2": (17, 5, 2, 0),    # Apéry a_n (17,5,1) with c→2
}


def run_golden(N1: int = 40, write_certs: bool = True) -> bool:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    all_ok = True
    for name in GOLDEN_GOOD:
        res = verify_c1(ORDER3_AZ_COOPER[name], N1=N1)
        ok = res["status"] == "PASS"
        all_ok &= ok
        print(f"  good {name:8s} {tuple(res['order3_abcd'])} -> {res['verdict']:26s} {'OK' if ok else 'MISMATCH'}")
        if write_certs and ok:
            (CERT_DIR / f"C1_mirror_{name}.json").write_text(json.dumps(res, indent=2))
    for name, params in GOLDEN_BAD.items():
        res = verify_c1(params, N1=N1)
        ok = res["status"] == "FAIL"
        all_ok &= ok
        print(f"  bad  {name:18s} {params} -> {res['verdict']:34s} {'OK' if ok else 'MISMATCH'}")
    r1 = verify_c1(ORDER3_AZ_COOPER["alpha"], N1=N1)
    r2 = verify_c1(ORDER3_AZ_COOPER["alpha"], N1=N1)
    det = r1["determinism_hash"] == r2["determinism_hash"] and r1["verdict"] == r2["verdict"]
    print(f"  determinism (Domb x2): {'OK' if det else 'FAIL'}")
    return all_ok and det


def main() -> int:
    ap = argparse.ArgumentParser(description="C1 mirror-map integrality checker")
    ap.add_argument("--order3", help="AZ/Cooper name (gamma,alpha,delta,eta,s7,s10,…)")
    ap.add_argument("--N1", type=int, default=50)
    ap.add_argument("--output")
    ap.add_argument("--golden", action="store_true")
    args = ap.parse_args()

    if args.golden or not args.order3:
        ok = run_golden(N1=args.N1)
        print("ALL GOLDEN TESTS PASS" if ok else "GOLDEN TESTS FAILED")
        return 0 if ok else 1

    res = verify_c1(ORDER3_AZ_COOPER[args.order3], N1=args.N1)
    text = json.dumps(res, indent=2)
    print(text)
    if args.output:
        Path(args.output).write_text(text)
    return 0 if res["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
