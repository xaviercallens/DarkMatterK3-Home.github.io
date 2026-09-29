#!/usr/bin/env python3
"""check_aubry_andre_selfduality.py -- E1, the calibration arm of the laboratory approach
(D12', briefs/STREAM2_TO_STREAM3_NOTICE_PR55_MERGED_2026_09_27.md sec.5 item 1;
briefs/STREAM3_ACTIVATION_2026_09_29.md W4.1).

THE MODEL. Aubry-Andre tight-binding chain on an N-site ring:

    (H psi)_n = J (psi_{n+1} + psi_{n-1}) + lam cos(2 pi p n / N) psi_n,   gcd(p, N) = 1.

THE IDENTITY CHECKED. With U[n,k] = exp(2 pi i p n k / N) / sqrt(N) (unitary because gcd(p,N)=1),

    U^dagger H(J, lam) U = H(lam/2, 2J)                                   (duality, exact)

so the spectrum of H(J, lam) equals that of H(lam/2, 2J); rescaling by 2J/lam gives the form
quoted in the directive, spec H(J, 4J^2/lam) = (2J/lam) spec H(J, lam). At lam = 2J the map is
an automorphism (H is self-dual), so every non-degenerate eigenvector satisfies
IPR_x = IPR_k, where IPR_k is computed in the U-basis.

WHAT IS EXACT AND WHAT IS NOT. The intertwining identity is an algebraic statement; it is
verified here in floating point to a stated tolerance, so every result is PASS(N) at tol,
never bare PASS. Degeneracy would make the per-eigenstate IPR identity ill-posed, so the
checker measures the minimum spectral gap and refuses (fails closed) if it is below tol.

NEGATIVE CONTROLS (standing rule 1: a test that cannot fail is not a test), run BEFORE the
positive checks and required to FAIL:
  N1  a seeded random on-site potential of matched rms strength replaces the cosine: the
      spectral duality must break (max eigenvalue mismatch >> tol) at every lam tested;
  N2  the same random potential at lam = 2J: IPR_x = IPR_k must break;
  N3  p with gcd(p, N) != 1 makes U non-unitary: the checker must refuse to run.

WHAT THIS IS NOT. A model check of an exactly solvable one-dimensional Hamiltonian. It is not
a measurement, it makes no statement about any K3 surface, any Cooper family, any lattice
certificate, any modular curve or any physical system; the directive's guardrail applies:
the K3 side of the laboratory programme is a mathematical shadow, not a target, and no result
here is evidence for anything in K3_CRITERIA.md.

Usage: python3 checkers/check_aubry_andre_selfduality.py [--emit]   (--emit writes the certificate)

Generated-by: Claude (Fable 5.1), Stream 3 activation 2026-09-29 | Verified-by: the negative
controls in this file and checkers/tests/test_aubry_andre_selfduality.py | Reviewed-by: N
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
CERT_PATH = REPO_ROOT / "checkers" / "certificates" / "E1_aubry_andre_selfduality.json"

TOL = 1e-9
CASES = [(13, 8), (89, 55), (233, 144)]  # (N, p): consecutive Fibonacci pairs, gcd = 1
J = 1.0
LAMS = (0.5, 1.0, 3.0)


class Refuse(RuntimeError):
    pass


def hamiltonian(N, p, J, onsite):
    H = np.zeros((N, N))
    for n in range(N):
        H[n, (n + 1) % N] = J
        H[(n + 1) % N, n] = J
        H[n, n] = onsite[n]
    return H


def cosine(N, p, lam):
    return lam * np.cos(2 * np.pi * p * np.arange(N) / N)


def random_matched(N, lam, seed):
    rng = np.random.default_rng(seed)
    v = rng.standard_normal(N)
    v -= v.mean()
    target_rms = float(np.sqrt(np.mean(cosine(N, 1, lam) ** 2)))
    return v * (target_rms / float(np.sqrt(np.mean(v ** 2))))


def dual_unitary(N, p):
    if math.gcd(p, N) != 1:
        raise Refuse(f"gcd({p},{N}) != 1: the dual transform is not unitary; refusing")
    n = np.arange(N)
    return np.exp(2j * np.pi * p * np.outer(n, n) / N) / np.sqrt(N)


def ipr(vecs):
    return np.sum(np.abs(vecs) ** 4, axis=0)


def spectral_duality_gap(N, p, J, onsite, lam):
    """max |spec H(J,onsite) - spec H(lam/2, 2J cos)|; 0 when onsite is the lam-cosine."""
    e1 = np.linalg.eigvalsh(hamiltonian(N, p, J, onsite))
    e2 = np.linalg.eigvalsh(hamiltonian(N, p, lam / 2, cosine(N, p, 2 * J)))
    return float(np.max(np.abs(np.sort(e1) - np.sort(e2))))


def scaled_duality_gap(N, p, J, lam):
    e1 = np.linalg.eigvalsh(hamiltonian(N, p, J, cosine(N, p, lam)))
    e3 = np.linalg.eigvalsh(hamiltonian(N, p, J, cosine(N, p, 4 * J * J / lam)))
    return float(np.max(np.abs(np.sort(e3) - (2 * J / lam) * np.sort(e1))))


def intertwiner_gap(N, p, J, lam):
    U = dual_unitary(N, p)
    H1 = hamiltonian(N, p, J, cosine(N, p, lam))
    H2 = hamiltonian(N, p, lam / 2, cosine(N, p, 2 * J))
    return float(np.max(np.abs(U.conj().T @ H1 @ U - H2)))


def selfdual_ipr_gap(N, p, J, onsite):
    """At the self-dual point: (max |IPR_x - IPR_k| over eigenstates, min spectral gap)."""
    U = dual_unitary(N, p)
    e, v = np.linalg.eigh(hamiltonian(N, p, J, onsite))
    gaps = np.diff(np.sort(e))
    min_gap = float(np.min(gaps))
    vk = U.conj().T @ v
    return float(np.max(np.abs(ipr(v) - ipr(vk)))), min_gap


def run():
    report = {"tol": TOL, "J": J, "lams": list(LAMS), "cases": [], "negative_controls": [], "verdict": None}
    ok = True

    # --- negative controls first --------------------------------------------------------
    for N, p in CASES:
        seed = 20260929 + N
        nc = {"N": N, "p": p, "seed": seed}
        gaps = {str(l): spectral_duality_gap(N, p, J, random_matched(N, l, seed), l) for l in LAMS}
        nc["N1_random_potential_spectral_gap"] = gaps
        nc["N1_breaks"] = all(g > 1e3 * TOL for g in gaps.values())
        ipr_gap, min_gap = selfdual_ipr_gap(N, p, J, random_matched(N, 2 * J, seed))
        nc["N2_random_potential_selfdual_ipr_gap"] = ipr_gap
        nc["N2_breaks"] = ipr_gap > 1e3 * TOL
        try:
            dual_unitary(N, 0)  # gcd(0, N) = N != 1: the constant "transform" is not unitary
            nc["N3_refuses"] = False
        except Refuse:
            nc["N3_refuses"] = True
        nc["all_controls_fail_as_required"] = nc["N1_breaks"] and nc["N2_breaks"] and nc["N3_refuses"]
        ok &= nc["all_controls_fail_as_required"]
        report["negative_controls"].append(nc)

    if not ok:
        report["verdict"] = "REFUSED: a negative control did not fail; the checker is not a test"
        return report, 2

    # --- positive checks ----------------------------------------------------------------
    for N, p in CASES:
        c = {"N": N, "p": p}
        c["A_spectral_duality_gap"] = {str(l): spectral_duality_gap(N, p, J, cosine(N, p, l), l) for l in LAMS}
        c["A_scaled_form_gap"] = {str(l): scaled_duality_gap(N, p, J, l) for l in LAMS}
        c["C_intertwiner_gap"] = {str(l): intertwiner_gap(N, p, J, l) for l in LAMS}
        ipr_gap, min_gap = selfdual_ipr_gap(N, p, J, cosine(N, p, 2 * J))
        c["B_selfdual_min_spectral_gap"] = min_gap
        c["B_selfdual_ipr_gap"] = ipr_gap
        c["B_nondegenerate"] = min_gap > TOL
        c["pass"] = (all(g < TOL for g in c["A_spectral_duality_gap"].values())
                     and all(g < TOL for g in c["A_scaled_form_gap"].values())
                     and all(g < TOL for g in c["C_intertwiner_gap"].values())
                     and c["B_nondegenerate"] and ipr_gap < TOL)
        c["line"] = f"PASS(N={N}) at tol {TOL:g}" if c["pass"] else f"FAIL(N={N})"
        ok &= c["pass"]
        report["cases"].append(c)

    report["verdict"] = "PASS(N) for N in " + ",".join(str(N) for N, _ in CASES) if ok else "FAIL"
    return report, 0 if ok else 1


def certificate(report):
    src = Path(__file__).read_bytes()
    return {
        "checker": "checkers/check_aubry_andre_selfduality.py",
        "checker_sha256": hashlib.sha256(src).hexdigest(),
        "work_package": "E1 calibration arm (D12' laboratory approach, item 1)",
        "tier": "model check (exactly solvable 1D Hamiltonian), verified numerically at the stated tolerance: PASS(N), not a proof and not a measurement",
        "result": report,
        "not_claimed": [
            "any statement about a K3 surface, a Cooper family, a transcendental lattice, a CM point or any certificate in K3_CRITERIA.md: this is the calibration arm of a laboratory programme whose K3 side is a mathematical shadow, not a target (directive sec.5 item 4)",
            "any physical measurement or any physical system: the model is a finite tight-binding ring; nothing here touches data, an experiment, or PREDICTION.md",
            "exactness: every identity is algebraic but is checked in floating point at tol; the per-eigenstate IPR identity is checked only where the spectrum is non-degenerate at tol (the checker refuses otherwise)",
            "the incommensurate (infinite-chain) limit: the ring with rational p/N is exactly self-dual by the twisted DFT; nothing is inferred about N -> infinity",
            "any link between the self-dual point lam = 2J and sigma = i, sigma = (1+i)/2, or the lattice <2>+<2>: such a sentence is Tier C by the directive and does not appear in this certificate",
        ],
        "generated_by": "Claude (Fable 5.1), Stream 3 activation 2026-09-29",
        "verified_by": "negative controls N1-N3 in this file (run first, required to fail); checkers/tests/test_aubry_andre_selfduality.py",
        "reviewed_by": "N",
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    a = ap.parse_args(argv)
    report, rc = run()
    for nc in report["negative_controls"]:
        print(f"  control N={nc['N']}: N1 breaks={nc['N1_breaks']} N2 breaks={nc['N2_breaks']} N3 refuses={nc['N3_refuses']}")
    for c in report["cases"]:
        print(f"  {c['line']}  | max spectral gap {max(c['A_spectral_duality_gap'].values()):.1e}, "
              f"intertwiner {max(c['C_intertwiner_gap'].values()):.1e}, IPR gap {c['B_selfdual_ipr_gap']:.1e}, "
              f"min level gap {c['B_selfdual_min_spectral_gap']:.2e}")
    print(report["verdict"])
    if a.emit and rc == 0:
        CERT_PATH.write_text(json.dumps(certificate(report), indent=2) + "\n")
        print("wrote", CERT_PATH)
    return rc


if __name__ == "__main__":
    sys.exit(main())
