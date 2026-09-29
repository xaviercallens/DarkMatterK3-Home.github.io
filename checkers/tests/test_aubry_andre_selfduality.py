"""Merge-blocking tests for E1 (checkers/check_aubry_andre_selfduality.py).

Positive: the duality holds at tol on every case. Negative: each control must fail on its own,
and the checker must refuse when a control does not fail. No K3 content.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from checkers import check_aubry_andre_selfduality as e1  # noqa: E402


def test_dual_unitary_is_unitary():
    for N, p in e1.CASES:
        U = e1.dual_unitary(N, p)
        assert np.max(np.abs(U.conj().T @ U - np.eye(N))) < e1.TOL


def test_refuses_non_coprime():
    with pytest.raises(e1.Refuse):
        e1.dual_unitary(12, 4)


def test_intertwiner_identity_holds():
    for N, p in e1.CASES:
        for lam in e1.LAMS:
            assert e1.intertwiner_gap(N, p, e1.J, lam) < e1.TOL


def test_spectral_and_scaled_forms_hold():
    for N, p in e1.CASES:
        for lam in e1.LAMS:
            assert e1.spectral_duality_gap(N, p, e1.J, e1.cosine(N, p, lam), lam) < e1.TOL
            assert e1.scaled_duality_gap(N, p, e1.J, lam) < e1.TOL


def test_selfdual_point_ipr_identity():
    for N, p in e1.CASES:
        gap, min_gap = e1.selfdual_ipr_gap(N, p, e1.J, e1.cosine(N, p, 2 * e1.J))
        assert min_gap > e1.TOL, "degenerate spectrum: identity ill-posed, checker must refuse"
        assert gap < e1.TOL


def test_random_potential_breaks_both_identities():
    for N, p in e1.CASES:
        v = e1.random_matched(N, 2 * e1.J, seed=1)
        assert e1.spectral_duality_gap(N, p, e1.J, v, 2 * e1.J) > 1e3 * e1.TOL
        gap, _ = e1.selfdual_ipr_gap(N, p, e1.J, v)
        assert gap > 1e3 * e1.TOL


def test_off_selfdual_point_ipr_identity_fails():
    """lam != 2J: IPR_x != IPR_k in general -- the identity is a property of the point, not a tautology."""
    N, p = e1.CASES[1]
    gap, _ = e1.selfdual_ipr_gap(N, p, e1.J, e1.cosine(N, p, 3.0))
    assert gap > 1e3 * e1.TOL


def test_run_passes_and_controls_fail():
    report, rc = e1.run()
    assert rc == 0
    assert all(nc["all_controls_fail_as_required"] for nc in report["negative_controls"])
    assert all(c["pass"] for c in report["cases"])
