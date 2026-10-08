"""Merge-blocking tests for E1b (checkers/check_aubry_andre_localization_scaling.py). Fast ring sizes only;
the full N = 89..987 run is the checker itself. Several tests encode the diagnosis of the first run."""
import json
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from checkers import check_aubry_andre_localization_scaling as e1b  # noqa: E402
from checkers import check_aubry_andre_selfduality as e1  # noqa: E402

N, P = 89, 55


def test_duality_of_mean_ipr_holds_on_a_nondegenerate_cell():
    gap, mingap = e1b.duality_gap(N, P, 1.5)
    assert mingap > e1b.TOL and gap < e1b.TOL


def test_N1_random_potential_breaks_the_mean_ipr_duality():
    gap, _ = e1b.duality_gap(N, P, 1.0, onsite=e1.random_matched(N, 1.0, 7))
    assert gap > 1e3 * e1b.TOL


def test_N2_random_potential_fails_extended_scaling():
    rnd = lambda Nn, pp, lam: e1.random_matched(Nn, lam, 20261008 + Nn)
    nx, _ = e1b.scaling_regime(1.0, rnd)
    assert nx[-1] / nx[0] > e1b.EXT_FACTOR


def test_diagnosis_theta0_localized_regime_has_exact_mirror_degeneracy():
    """The first-run failure: at theta = 0 the potential is symmetric under n -> -n, so localized states come in exactly
    degenerate mirror pairs and the eigenbasis is arbitrary. A generic phase removes every degeneracy."""
    w0 = np.linalg.eigvalsh(e1.hamiltonian(N, P, 1.0, e1.cosine(N, P, 3.0)))
    assert float(np.min(np.diff(w0))) < e1b.TOL
    pot = 3.0 * np.cos(2 * np.pi * P * np.arange(N) / N + e1b.THETA)
    w1 = np.linalg.eigvalsh(e1.hamiltonian(N, P, 1.0, pot))
    assert float(np.min(np.diff(w1))) > e1b.TOL


def test_phase_iprs_refuses_a_degenerate_spectrum():
    with pytest.raises(RuntimeError):
        e1b.phase_iprs(N, P, 3.0, 0.0)          # theta = 0 is degenerate: the guard must fire, not average


def test_crossing_is_exactly_at_2J():
    ix, ik, _ = e1b.cos_iprs(N, P, 2.0)
    assert abs(ix - ik) < e1b.TOL
    ix, ik, _ = e1b.cos_iprs(N, P, 1.5)
    assert ix < ik
    ix, ik, _ = e1b.cos_iprs(N, P, 2.5)
    assert ix > ik


def test_claim_revisions_are_in_band_and_the_criterion_was_not_retuned():
    assert len(e1b.CLAIM_REVISIONS) == 2 and e1b.LOC_CONST == 0.10 and e1b.NEAR_CRITICAL == 0.15
    assert "REPORTED, NOT CLAIMED" in e1b.CLAIM_REVISIONS[1]["change"]


def test_emitted_certificate_records_the_near_critical_failure_not_hidden():
    c = json.loads((Path(e1b.CERT_PATH)).read_text())["result"]
    near = [r for r in c["scaling"] if r.get("near_critical_reported_not_claimed")]
    assert any((not r["pass"]) for r in near), "the near-critical non-convergence must stay visible in the certificate"
    assert c["verdict"].startswith("PASS(N)")
