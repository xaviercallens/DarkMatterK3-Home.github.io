#!/usr/bin/env python3
"""
Unit tests for WP-E6-SWEEP design §4 (pipeline/keff.py), pinned in
briefs/WP_E6_SWEEP_KEFF_RULING_PINNED_2026_09_17.md (pin 57a6065).

Merge-blocking. Every positive check is paired with a negative control that must fail
(a test that cannot fail is not a test). No emulator or raw data needed: fake emulators and
tmp copies of tracked artifacts stand in where required.
"""
import json
import os
import sys

import numpy as np
import pytest

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(repo_root, "pipeline"))
import keff  # noqa: E402

NODES_K = 10.0 ** keff.NATIVE_LOG10K


class TestPredictAtKeff:
    """K1: log-log linear interpolation at k_eff with a capped edge extrapolation."""

    def test_power_law_is_exact_including_band0_extrapolation(self):
        p = 3.7 * NODES_K ** -1.3                     # straight line in log-log
        k_eff = keff.load_k_eff()
        np.testing.assert_allclose(keff.predict_at_keff(p, k_eff), 3.7 * k_eff ** -1.3, rtol=1e-12)

    def test_negative_control_curved_spectrum_is_not_exact(self):
        # ln P quadratic in ln k: linear interpolation must NOT reproduce it off-node
        lnk = np.log(NODES_K)
        p = np.exp(2.0 - 0.8 * lnk - 0.6 * lnk ** 2)
        k_eff = keff.load_k_eff()
        truth = np.exp(2.0 - 0.8 * np.log(k_eff) - 0.6 * np.log(k_eff) ** 2)
        err = np.abs(keff.predict_at_keff(p, k_eff) / truth - 1)
        assert err.max() > 1e-6

    def test_nodes_are_reproduced_exactly(self):
        rng = np.random.default_rng(3)
        p = rng.uniform(1, 100, keff.NATIVE_LOG10K.size)
        np.testing.assert_allclose(keff.predict_at_keff(p, NODES_K[:9]), p[:9], rtol=1e-12)

    def test_pinned_segments_per_band(self):
        # pinned table K1: band -> lower node of the segment used
        pinned_lower = [-2.2, -2.1, -2.0, -2.0, -1.8, -1.7, -1.6, -1.5, -1.5]
        x = np.log10(keff.load_k_eff())
        i = np.clip(np.searchsorted(keff.NATIVE_LOG10K, x, side="right") - 1, 0, 14)
        assert keff.NATIVE_LOG10K[i].tolist() == pinned_lower

    def test_band0_extrapolation_is_the_pinned_0p003_dex(self):
        x0 = np.log10(keff.load_k_eff()[0])
        assert abs((-2.2 - x0) - 0.0030) < 5e-5

    @pytest.mark.parametrize("log10k", [-2.2 - 0.02, -0.7 + 0.011])   # beyond the low and high edges
    def test_cap_is_a_hard_stop(self, log10k):
        k = keff.load_k_eff().copy()
        k[0] = 10.0 ** log10k
        with pytest.raises(keff.KeffCapError):
            keff.predict_at_keff(np.ones(16), k)

    def test_just_inside_cap_is_allowed(self):
        k = keff.load_k_eff().copy()
        k[0] = 10.0 ** (-2.2 - 0.009)
        assert np.all(np.isfinite(keff.predict_at_keff(np.ones(16), k)))

    @pytest.mark.parametrize("bad", [np.ones(15), np.r_[np.ones(15), 0.0], np.r_[np.ones(15), np.nan]])
    def test_malformed_native_input_rejected(self, bad):
        with pytest.raises(ValueError):
            keff.predict_at_keff(bad, keff.load_k_eff())

    def test_no_variant_paths_exposed(self):
        # K4: no k_target or no-systematic evaluation path in the module
        names = [n.lower() for n in dir(keff)]
        assert not any("target" in n or "no_sys" in n or "without" in n for n in names)


@pytest.fixture(scope="module")
def cov9():
    return np.load(keff.AGG_NPY)


class TestAugmentedCovariance:
    """K2: C₉,sys = C₉ + diag((β_b σ_b)²) with pinned β."""

    def test_diagonal_term_matches_pinned_table(self, cov9):
        aug = keff.augmented_covariance(cov9)
        np.testing.assert_allclose(np.diag(aug) - np.diag(cov9), keff.PINNED_TERM, rtol=0, atol=5e-9)

    def test_term_reproduces_from_artifacts_to_1e_6(self, cov9):
        aug = keff.augmented_covariance(cov9)
        beta = np.asarray(json.load(open(keff.PRECHECK_JSON))["bound_sigma_max_per_band"])
        exact = (beta * np.sqrt(np.diag(cov9))) ** 2
        np.testing.assert_allclose(np.diag(aug) - np.diag(cov9), exact, rtol=1e-6)

    def test_off_diagonals_unchanged_and_pd(self, cov9):
        aug = keff.augmented_covariance(cov9)
        off = ~np.eye(9, dtype=bool)
        assert np.array_equal(aug[off], cov9[off])
        np.linalg.cholesky(aug)

    def test_band5_inflation_is_pinned_4p75_percent(self, cov9):
        aug = keff.augmented_covariance(cov9)
        infl = np.sqrt(np.diag(aug) / np.diag(cov9))
        assert abs(infl[5] - 1.04749) < 1e-5 and infl.max() == infl[5]

    def test_negative_control_tampered_beta_rejected(self, cov9, tmp_path):
        d = json.load(open(keff.PRECHECK_JSON))
        d["bound_sigma_max_per_band"][5] += 1e-3
        bad = tmp_path / "precheck.json"
        bad.write_text(json.dumps(d))
        with pytest.raises(keff.PinMismatchError):
            keff.augmented_covariance(cov9, precheck_json=bad)

    def test_negative_control_different_cov9_rejected(self, cov9):
        with pytest.raises(keff.PinMismatchError):
            keff.augmented_covariance(cov9 * 1.01)

    def test_asymmetric_input_rejected(self, cov9):
        bad = cov9.copy()
        bad[0, 1] += 0.1
        with pytest.raises(keff.PinMismatchError):
            keff.augmented_covariance(bad)


def _fake_emulator(scale=1.0):
    ref = json.load(open(keff.GRID_CONTROLS_JSON))
    p_ref = np.asarray(ref["checks"][0]["pk_reference"], dtype=float)
    return (lambda pack, *args: p_ref * scale), None


class TestSweepGate:
    """K3: mechanical gate; passes only if every item holds."""

    def test_passes_with_artifacts_and_matching_emulator(self, tmp_path):
        out = tmp_path / "gate.json"
        rec = keff.sweep_gate(emulator=_fake_emulator(), out_path=out)
        assert rec["passes"], rec
        assert json.loads(out.read_text())["passes"] is True

    def test_does_not_pass_without_emulator(self):
        rec = keff.sweep_gate()
        assert rec["passes"] is False
        assert rec["items"]["3_emulator_regression"]["status"].startswith("NOT_RUN")
        assert all(v["pass"] for k, v in rec["items"].items() if not k.startswith("3_"))

    def test_negative_control_emulator_drift_fails(self):
        rec = keff.sweep_gate(emulator=_fake_emulator(1.00001))
        assert rec["items"]["3_emulator_regression"]["pass"] is False and rec["passes"] is False

    def test_negative_control_precheck_bytes_changed_fails_sha(self, tmp_path):
        bad = tmp_path / "precheck.json"
        bad.write_bytes(open(keff.PRECHECK_JSON, "rb").read() + b"\n")
        rec = keff.sweep_gate(precheck_json=bad, emulator=_fake_emulator())
        assert rec["items"]["1_precheck_sha256"]["pass"] is False and rec["passes"] is False

    def test_negative_control_failed_precheck_flag_fails(self, tmp_path):
        d = json.load(open(keff.PRECHECK_JSON))
        d["control_1_pass"] = False
        bad = tmp_path / "precheck.json"
        bad.write_text(json.dumps(d))
        rec = keff.sweep_gate(precheck_json=bad, expected_sha256=keff._sha256(bad), emulator=_fake_emulator())
        assert rec["items"]["2_precheck_flags"]["pass"] is False and rec["passes"] is False

    def test_negative_control_wrong_cov9_fails(self, tmp_path):
        bad = tmp_path / "cov.npy"
        np.save(bad, np.load(keff.AGG_NPY) * 1.02)
        rec = keff.sweep_gate(agg_npy=bad, emulator=_fake_emulator())
        assert rec["items"]["4_augmented_covariance"]["pass"] is False and rec["passes"] is False

    def test_negative_control_keff_beyond_cap_fails(self, tmp_path):
        d = json.load(open(keff.AGG_JSON))
        d["k_eff_s_per_km"][0] = 10.0 ** (-2.2 - 0.02)
        bad = tmp_path / "agg.json"
        bad.write_text(json.dumps(d))
        rec = keff.sweep_gate(agg_json=bad, emulator=_fake_emulator())
        assert rec["items"]["4_augmented_covariance"]["pass"] is False and rec["passes"] is False
