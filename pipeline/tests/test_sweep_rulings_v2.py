#!/usr/bin/env python3
"""
Controls for the design-v2 sweep rulings (briefs/T0_RULING_SWEEP_C1_C5_EB_2026_10_10.md): C4(b) aggregation,
the v2 K2 table, the C1/C2 corrections module and the extra-nuisance profiler path.
Every positive check has a negative control that must fail. No real data vector is fitted anywhere here.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import sys

import numpy as np
import pytest

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(repo_root, "pipeline"))
import chi2_profile  # noqa: E402
import keff  # noqa: E402
import sweep_corrections as sc  # noqa: E402

_spec = importlib.util.spec_from_file_location("agg_c4", os.path.join(repo_root, "scripts", "wp_e6_sweep_aggregate_9x9_c4.py"))
agg_c4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(agg_c4)

HAVE_PICKLE = sc.CORRECTOR_WITH_PATCHY.exists()
HAVE_V2 = keff.V2.agg_json.exists() and keff.V2.precheck_json.exists()


def _map(ks):
    return {"bands": [{"bin_index": 8, "members": list(range(len(ks))), "member_k_values": list(ks),
                       "member_log10k_values": list(np.log10(ks)), "member_count": len(ks), "all_within_nyquist": False}]}


class TestC4Cut:
    def test_cut_value_is_computed_from_provider_constants(self):
        kmax, r_z = agg_c4.k_cut()
        assert abs(kmax - 0.5 * np.pi / r_z) < 1e-15
        assert 0.0413 < kmax < 0.0415

    def test_cut_drops_exactly_members_above(self):
        kmax, _ = agg_c4.k_cut()
        m, dropped = agg_c4.apply_cut(_map([0.03, kmax, kmax * 1.0001, 0.05]), kmax)
        assert m["bands"][0]["member_count"] == 2          # k == kmax kept (cut is k < k_max, boundary not hit by data)
        assert len(dropped) == 2

    def test_negative_control_wrong_cut_changes_count(self):
        # a cut of 2*pi/R_z (a wrong factor) would keep everything: the control must see a different count
        kmax, _ = agg_c4.k_cut()
        _, dropped = agg_c4.apply_cut(_map([0.03, 0.045, 0.05]), 2 * kmax)
        assert len(dropped) == 0 != 2

    @pytest.mark.skipif(not agg_c4.OUT_JSON.exists(), reason="C4 artifact not generated")
    def test_artifact_band8_has_seven_members_and_others_unchanged(self):
        a = json.load(open(agg_c4.OUT_JSON))
        assert a["members_after"] == [3, 4, 4, 6, 8, 9, 11, 11, 7]
        assert a["members_before"][:8] == a["members_after"][:8]
        assert all(d["bin_index"] == 8 for d in a["dropped"]) and len(a["dropped"]) == 3
        assert a["checks"]["positive_definite_cholesky"] and a["checks"]["symmetric"]
        assert all(abs(s - 1) < 1e-12 for s in a["row_sums"])


@pytest.mark.skipif(not HAVE_V2, reason="v2 artifacts absent")
class TestKeffV2:
    def test_precheck_hash_pinned(self):
        assert hashlib.sha256(open(keff.V2.precheck_json, "rb").read()).hexdigest() == keff.V2.precheck_sha256

    def test_v2_table_rederives_from_artifacts(self):
        cov9 = np.load(keff.V2.agg_npy)
        aug = keff.augmented_covariance(cov9, keff.V2.precheck_json, keff.V2)
        assert np.all(np.abs((np.diag(aug) - np.diag(cov9)) - keff.V2.pinned_term) < 5e-9 + 1e-12)

    def test_negative_control_v2_cov_against_v1_table_fails(self):
        cov9 = np.load(keff.V2.agg_npy)
        with pytest.raises(keff.PinMismatchError):
            keff.augmented_covariance(cov9, keff.V2.precheck_json, keff.V1)

    def test_negative_control_tampered_beta_fails(self, tmp_path):
        d = json.load(open(keff.V2.precheck_json))
        d["bound_sigma_max_per_band"][8] *= 1.01
        p = tmp_path / "pc.json"
        p.write_text(json.dumps(d))
        with pytest.raises(keff.PinMismatchError):
            keff.pinned_beta(p, keff.V2.pinned_beta)

    def test_bands_0_to_7_beta_equal_v1(self):
        assert np.allclose(keff.V2.pinned_beta[:8], keff.V1.pinned_beta[:8], atol=1e-6)

    def test_only_band8_term_changes_materially(self):
        # diag_actual of bands 0-7 are untouched by the cut; band 8 is the only one that may differ
        v1 = json.load(open(keff.V1.agg_json))["diag_actual"]
        v2 = json.load(open(keff.V2.agg_json))["diag_actual"]
        assert np.allclose(v1[:8], v2[:8], rtol=1e-12)
        assert abs(v1[8] - v2[8]) > 0


@pytest.mark.skipif(not HAVE_PICKLE, reason="upstream corrector pickle absent (gitignored emulator tree)")
class TestCorrections:
    def test_s1_is_bit_identical_to_upstream_total(self):
        c = sc.load_corrector()
        assert np.array_equal(sc.multiplier(c, 1.0), sc.upstream_total(c))

    def test_negative_control_s0_differs_from_upstream(self):
        c = sc.load_corrector()
        assert not np.allclose(sc.multiplier(c, 0.0), sc.upstream_total(c), rtol=0, atol=1e-6)

    def test_multiplier_is_linear_in_s_before_fixed_factors(self):
        c = sc.load_corrector()
        a, b, m = sc.multiplier(c, 0.0), sc.multiplier(c, 2.0), sc.multiplier(c, 1.0)
        assert np.allclose(m, 0.5 * (a + b), rtol=1e-12)

    def test_hash_gate_refuses_wrong_pin(self):
        with pytest.raises(sc.CorrectorPinError):
            sc.load_corrector(sha256="0" * 64)

    def test_restricted_unpickler_refuses_arbitrary_global(self, tmp_path):
        import pickle

        class Evil:
            def __reduce__(self):
                return (os.system, ("true",))

        p = tmp_path / "evil.pkl"
        raw = pickle.dumps(Evil())
        p.write_bytes(raw)
        with pytest.raises(sc.CorrectorPinError):
            sc.load_corrector(path=p, sha256=hashlib.sha256(raw).hexdigest())


class TestEligibilityEB:
    class R:
        def __init__(self, fvals, per):
            self.start_fvals, self.start_nonfinite = tuple(fvals), tuple(per)
            self.nonfinite_evaluations = sum(per)

    def test_EB_restores_cell_when_pathological_start_lost(self):
        import sweep
        r = self.R([3.0, 5.0], [0, 17])         # clean start 1 has the lowest chi2; guarded start 2 lost
        assert sweep.cell_eligible(r, "E-B") and not sweep.cell_eligible(r, "E-A")

    def test_negative_control_EB_withholds_when_pathological_start_won(self):
        import sweep
        r = self.R([5.0, 3.0], [0, 17])         # the guarded start 2 has the lowest chi2: retained minimum is degenerate
        assert not sweep.cell_eligible(r, "E-B")

    def test_unknown_rule_raises_and_default_is_conservative(self):
        import sweep
        assert sweep.ELIGIBILITY_RULE == "E-A" and sweep.DOF_CELL == 5 and sweep.DOF_CELL_V2 == 4
        with pytest.raises(ValueError):
            sweep.cell_eligible(self.R([1.0], [0]), "E-Z")


class TestExtraNuisanceProfiler:
    """A synthetic 9-vector model with a known 5th parameter: the profiler must recover it; the four-nuisance
    path must be untouched when no extras are given."""

    @staticmethod
    def _pred(m, f, zrei, ha, hs, taueff, s=1.0):
        base = np.linspace(1.0, 2.0, 9)
        return base * (1 + 0.05 * (zrei - 10.5) / 5 + 0.02 * (ha - 2) + 0.01 * hs + 0.03 * (taueff - 1)) * (1 + 0.1 * s * np.arange(9) / 8)

    def test_recovers_injected_amplitude(self):
        truth = 2.5
        data = self._pred(0, 0, 10.5, 2.0, 0.0, 1.0, s=truth)
        prof = chi2_profile.Chi2Profiler(data, np.eye(9) * 1e4, self._pred, extra_nuisances={"s_siiii": (0.0, 4.0, 1.0)})
        r = prof.profile_likelihood(0.0, 0.0, starts=[{"zrei": 10.5, "ha": 2.0, "hs": 0.0, "taueff": 1.0, "s_siiii": 0.5}])
        assert r.chi2_min < 1e-3
        assert "s_siiii" in r.nuisance_params

    def test_negative_control_pinned_s_cannot_fit_s_data(self):
        data = self._pred(0, 0, 10.5, 2.0, 0.0, 1.0, s=3.5)
        prof = chi2_profile.Chi2Profiler(data, np.eye(9) * 1e4, lambda *a: self._pred(*a, s=0.0))
        r = prof.profile_likelihood(0.0, 0.0, starts=[{"zrei": 10.5, "ha": 2.0, "hs": 0.0, "taueff": 1.0}])
        assert r.chi2_min > 1.0   # the four IGM nuisances cannot absorb a k-dependent amplitude change

    def test_box_edge_is_reported(self):
        data = self._pred(0, 0, 10.5, 2.0, 0.0, 1.0, s=9.0)      # outside the [0, 4] box
        prof = chi2_profile.Chi2Profiler(data, np.eye(9) * 1e4, self._pred, extra_nuisances={"s_siiii": (0.0, 4.0, 1.0)})
        r = prof.profile_likelihood(0.0, 0.0, starts=[{"zrei": 10.5, "ha": 2.0, "hs": 0.0, "taueff": 1.0, "s_siiii": 1.0}])
        assert r.at_boundary
