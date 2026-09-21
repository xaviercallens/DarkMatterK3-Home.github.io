#!/usr/bin/env python3
"""
Unit tests for the WP-E6-SWEEP driver (pipeline/sweep.py). Merge-blocking; no emulator needed.

Covers the safety rails (real-data block, label enforcement, required corrections argument) and the
statistic bookkeeping on a toy model whose answer is known. Each rail has a negative control.
"""
import json
import os
import sys

import numpy as np
import pytest

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(repo_root, "pipeline"))
import keff  # noqa: E402
import sweep  # noqa: E402

COV = np.load(keff.AGG_NPY)
REAL_P9 = np.asarray(json.load(open(keff.AGG_JSON))["data_agg_p1d_kms"], dtype=float)


def toy_native(m, f, zrei, ha, hs, taueff):
    # smooth power law in k; amplitude depends on f and m, tilt on taueff; nuisances matter
    k = 10.0 ** keff.NATIVE_LOG10K
    amp = 40.0 * (1.0 - 0.3 * f * (m + 23.0) / 4.0) * (1 + 0.02 * (zrei - 10.5)) * (1 + 0.05 * (ha - 2.0))
    return amp * (k / 0.02) ** (-0.8 * taueff + 0.05 * hs)


class TestRealDataBlock:
    def test_real_observation_refused_while_unpinned(self):
        assert sweep.REAL_DATA_RULING_PIN is None
        with pytest.raises(sweep.RealDataBlockedError):
            sweep.load_real_observation()

    def test_real_mode_sweep_refused(self, tmp_path):
        pred = sweep.make_predictor(toy_native, keff.load_k_eff(), np.ones(16), "real")
        with pytest.raises(sweep.RealDataBlockedError):
            sweep.run_sweep(REAL_P9, COV, pred, "real", tmp_path / "x.json")
        assert not (tmp_path / "x.json").exists()

    def test_real_vector_refused_under_synthetic_label(self, tmp_path):
        pred = sweep.make_predictor(toy_native, keff.load_k_eff(), sweep.PENDING_CORRECTIONS, "synthetic")
        with pytest.raises(sweep.RealDataBlockedError):
            sweep.run_sweep(REAL_P9.copy(), COV, pred, "synthetic", tmp_path / "x.json")

    def test_negative_control_other_vector_is_accepted_in_synthetic_mode(self, tmp_path):
        pred = sweep.make_predictor(toy_native, keff.load_k_eff(), sweep.PENDING_CORRECTIONS, "synthetic")
        obs = pred(-22.0, 0.35, 10.5, 2.0, 0.0, 1.0)
        rec = sweep.run_sweep(obs, COV, pred, "synthetic", tmp_path / "ok.json",
                              m_grid=np.array([-22.0, -19.1]), f_grid=np.array([0.0, 0.35]))
        assert rec["label"] == sweep.SYNTHETIC_LABEL

    def test_pending_corrections_sentinel_refused_outside_synthetic(self):
        with pytest.raises(sweep.RealDataBlockedError):
            sweep.make_predictor(toy_native, keff.load_k_eff(), sweep.PENDING_CORRECTIONS, "real")

    @pytest.mark.parametrize("bad", [np.ones(15), np.r_[np.ones(15), -1.0], "none"])
    def test_malformed_multiplier_refused(self, bad):
        with pytest.raises((ValueError, sweep.RealDataBlockedError)):
            sweep.make_predictor(toy_native, keff.load_k_eff(), bad, "synthetic")


class TestStatisticBookkeeping:
    @pytest.fixture(scope="class")
    def rec(self, tmp_path_factory):
        pred = sweep.make_predictor(toy_native, keff.load_k_eff(), sweep.PENDING_CORRECTIONS, "synthetic")
        obs = pred(-22.0, 0.35, 10.5, 2.0, 0.0, 1.0)
        return sweep.run_sweep(obs, COV, pred, "synthetic", tmp_path_factory.mktemp("s") / "toy.json",
                               m_grid=np.array([-22.9, -22.0, -19.1]), f_grid=np.array([0.0, 0.35, 0.99]))

    def test_threshold_is_computed_chi2_quantile(self):
        assert abs(sweep.DCHI2_95_2DOF - 5.991464547107979) < 1e-12

    def test_noiseless_injection_recovered_at_minimum(self, rec):
        c = np.array(rec["chi2_min_grid"])
        assert np.unravel_index(np.argmin(c), c.shape) == (1, 1) and c[1, 1] < 1e-6

    def test_delta_chi2_and_region_consistent(self, rec):
        d = np.array(rec["delta_chi2_grid"])
        assert d.min() == 0.0
        assert np.array_equal(np.array(rec["outside_95_region"]), d > sweep.DCHI2_95_2DOF)

    def test_negative_control_region_is_not_all_inside(self, rec):
        assert np.array(rec["outside_95_region"]).any()

    def test_record_carries_pins_statistic_and_taueff_note(self, rec):
        assert rec["taueff_note"] == sweep.TAUEFF_NOTE
        assert "5 dof" in rec["statistic"]["cell"] and "2 dof" in rec["statistic"]["contour"]
        assert len(rec["cells"]) == 9 and all("gof_p_value_5dof" in c for c in rec["cells"])

    def test_no_test_label_anywhere(self, rec):
        assert "TEST" not in json.dumps(rec["label"]).replace("not TEST", "")
        assert set(sweep.REAL_LABELS.values()) == {"exclusion", "FIT"}


class TestMultiStart:
    def test_start_set_is_deterministic_and_inside_bounds(self):
        import chi2_profile as C
        again = sweep._profile_starts()
        assert again == sweep.PROFILE_STARTS and len(again) == 9
        for s in again:
            for n, (lo, hi) in C.NUISANCE_BOUNDS.items():
                assert lo <= s[n] <= hi

    def test_multistart_finds_global_minimum_where_single_start_does_not(self):
        # toy χ² with a shallow local basin at the median start and a deeper one elsewhere in zrei
        import chi2_profile as C
        def predict(m, f, zrei, ha, hs, taueff):
            depth = -3.0 * np.exp(-((zrei - 13.5) ** 2) / 0.3) - 0.5 * np.exp(-((zrei - 10.5) ** 2) / 0.5)
            return np.full(9, 10.0 + np.sqrt(max(depth + 3.5, 0.0))) + 0.0 * (ha + hs + taueff)
        cov_inv = np.eye(9)
        prof = C.Chi2Profiler(np.full(9, 10.0), cov_inv, predict)
        single = prof.profile_likelihood(-22.0, 0.1)
        multi = prof.profile_likelihood(-22.0, 0.1, starts=sweep.PROFILE_STARTS)
        assert multi.chi2_min < single.chi2_min - 1.0          # negative control: single start is trapped
        assert len(multi.start_fvals) == 9 and multi.chi2_min == min(multi.start_fvals)

    def test_parallel_and_serial_sweeps_agree(self, tmp_path):
        pred = sweep.make_predictor(toy_native, keff.load_k_eff(), sweep.PENDING_CORRECTIONS, "synthetic")
        obs = pred(-22.0, 0.35, 10.5, 2.0, 0.0, 1.0) * 1.01
        kw = dict(m_grid=np.array([-22.0, -19.1]), f_grid=np.array([0.0, 0.35]))
        a = sweep.run_sweep(obs, COV, pred, "synthetic", tmp_path / "a.json", workers=1, **kw)
        b = sweep.run_sweep(obs, COV, pred, "synthetic", tmp_path / "b.json", workers=2, **kw)
        assert np.array_equal(np.array(a["chi2_min_grid"]), np.array(b["chi2_min_grid"]))
        assert "max_residual" in a["optimizer"]


# ---------------------------------------------------------------------------------------------------
# Non-finite-nuisance guard + per-cell isolation (2026-09-21; T0 ruling R2, most conservative setting).
# Defect: briefs/STREAM3_SWEEP_NONFINITE_NUISANCE_DEFECT_2026_09_21.md
# ---------------------------------------------------------------------------------------------------
import chi2_profile  # noqa: E402

MG, FG = np.array([-22.9, -22.0, -19.1]), np.array([0.0, 0.35, 0.99])


def _pred(native=toy_native):
    return sweep.make_predictor(native, keff.load_k_eff(), sweep.PENDING_CORRECTIONS, "synthetic")


def _strict_json(path):
    def _no_constants(name):
        raise AssertionError(f"non-JSON constant {name} in the persisted artifact")
    return json.loads(open(path).read(), parse_constant=_no_constants)


class TestNonfiniteGuard:
    def _profiler(self):
        pred = _pred()
        ci = np.linalg.inv(COV)
        return chi2_profile.Chi2Profiler(pred(-22.0, 0.35, 10.5, 2.0, 0.0, 1.0), 0.5 * (ci + ci.T), pred)

    def test_nonfinite_parameters_are_counted_per_start_not_silently_absorbed(self):
        starts = [dict(chi2_profile.NUISANCE_INIT), {"zrei": float("nan"), "ha": 2.0, "hs": 0.0, "taueff": 1.0}]
        r = self._profiler().profile_likelihood(-22.0, 0.35, starts=starts)
        assert r.nonfinite_evaluations > 0
        assert r.start_nonfinite[0] == 0 and r.start_nonfinite[1] == r.nonfinite_evaluations
        assert r.chi2_min < 1e-6, "the clean start must win over the penalised one"
        assert any("non-finite nuisances" in m for m in r.messages)

    def test_negative_control_clean_profile_never_fires_the_guard(self):
        r = self._profiler().profile_likelihood(-22.0, 0.35, starts=sweep.PROFILE_STARTS)
        assert r.nonfinite_evaluations == 0 and set(r.start_nonfinite) == {0}
        assert not any("non-finite" in m for m in r.messages)

    def test_penalty_is_finite_so_minuit_can_back_off(self):
        assert np.isfinite(chi2_profile.NONFINITE_PENALTY) and chi2_profile.NONFINITE_PENALTY > 1e20


class TestPerCellIsolation:
    def test_clean_sweep_is_complete_and_every_cell_eligible(self, tmp_path):
        pred = _pred()
        rec = sweep.run_sweep(pred(-22.0, 0.35, 10.5, 2.0, 0.0, 1.0), COV, pred, "synthetic",
                              tmp_path / "clean.json", m_grid=MG, f_grid=FG)
        assert rec["contour_status"] == sweep.CONTOUR_COMPLETE and rec["ineligible_cells"] == []
        assert all(c["contour_eligible"] and not c["failed"] for c in rec["cells"])
        assert all(v is not None for row in rec["outside_95_region"] for v in row)

    def test_failing_cell_is_recorded_and_withholds_the_contour(self, tmp_path):
        """One cell raises. Before 2026-09-21 that destroyed the sweep; now the other cells survive, the
        failure is in the artifact verbatim, and NO contour may be drawn."""
        def native(m, f, *nuis):
            if m == -22.0 and f == 0.99:
                raise FloatingPointError("injected failure in exactly one cell")
            return toy_native(m, f, *nuis)
        pred = _pred(native)
        out = tmp_path / "onefail.json"
        rec = sweep.run_sweep(pred(-22.0, 0.35, 10.5, 2.0, 0.0, 1.0), COV, pred, "synthetic", out,
                              m_grid=MG, f_grid=FG)
        bad = [c for c in rec["cells"] if c["failed"]]
        assert [(c["m"], c["f"]) for c in bad] == [(-22.0, 0.99)]
        assert "injected failure" in bad[0]["error"] and bad[0]["contour_eligible"] is False
        assert rec["contour_status"].startswith("WITHHELD") and "1 cell(s)" in rec["contour_status"]
        assert rec["ineligible_cells"][0]["reason"] == "failed"
        assert rec["outside_95_region"][1][2] is None and rec["chi2_min_grid"][1][2] is None
        assert sum(v is not None for row in rec["chi2_min_grid"] for v in row) == 8
        _strict_json(out)                       # null, never a bare NaN token

    def test_invalid_prediction_from_finite_parameters_is_a_failure_not_a_guarded_evaluation(self, tmp_path):
        """The guard covers the OPTIMIZER's pathology only. An emulator returning NaN for finite inputs is
        a different defect and must not be laundered into a penalty: it fails the cell, loudly."""
        def native(m, f, *nuis):
            v = toy_native(m, f, *nuis)
            return v * np.nan if (m == -19.1 and f == 0.35) else v
        pred = _pred(native)
        rec = sweep.run_sweep(pred(-22.0, 0.35, 10.5, 2.0, 0.0, 1.0), COV, pred, "synthetic",
                              tmp_path / "emu.json", m_grid=MG, f_grid=FG)
        bad = [c for c in rec["cells"] if c["failed"]]
        assert len(bad) == 1 and "finite and positive" in bad[0]["error"]
        assert all(c["nonfinite_evaluations"] == 0 for c in rec["cells"] if not c["failed"])

    def test_guarded_cell_is_ineligible_and_cannot_anchor_delta_chi2(self, tmp_path, monkeypatch):
        """A cell that needed the guard keeps its chi2_min for diagnosis but gets no verdict, and — even
        if it holds the LOWEST chi2 — does not become the reference minimum."""
        real = chi2_profile.Chi2Profiler.profile_likelihood

        def flagged(self, m, f, verbose=False, starts=None):
            r = real(self, m, f, verbose=verbose, starts=starts)
            return r._replace(nonfinite_evaluations=5, start_nonfinite=(0, 5)) if (m, f) == (-22.0, 0.35) else r
        monkeypatch.setattr(chi2_profile.Chi2Profiler, "profile_likelihood", flagged)
        pred = _pred()
        rec = sweep.run_sweep(pred(-22.0, 0.35, 10.5, 2.0, 0.0, 1.0), COV, pred, "synthetic",
                              tmp_path / "guarded.json", m_grid=MG, f_grid=FG)
        cell = next(c for c in rec["cells"] if (c["m"], c["f"]) == (-22.0, 0.35))
        assert cell["chi2_min"] < 1e-6 and cell["contour_eligible"] is False   # it IS the true minimum
        assert (rec["grid_minimum"]["m"], rec["grid_minimum"]["f"]) != (-22.0, 0.35)
        assert rec["outside_95_region"][1][1] is None
        assert rec["ineligible_cells"] == [{"m": -22.0, "f": 0.35, "reason": "nonfinite_nuisance_guard", "detail": 5}]
        assert rec["contour_status"].startswith("WITHHELD")

    def test_sweep_with_no_eligible_cell_refuses_to_report(self, tmp_path, monkeypatch):
        monkeypatch.setattr(sweep, "PROFILE_STARTS",
                            [{"zrei": float("nan"), "ha": 2.0, "hs": 0.0, "taueff": 1.0}])
        pred = _pred()
        out = tmp_path / "none.json"
        with pytest.raises(RuntimeError, match="no contour-eligible cell"):
            sweep.run_sweep(pred(-22.0, 0.35, 10.5, 2.0, 0.0, 1.0), COV, pred, "synthetic", out,
                            m_grid=MG, f_grid=FG)
        assert not out.exists()

    def test_isolation_holds_in_forked_workers_too(self, tmp_path):
        def native(m, f, *nuis):
            if m == -22.9 and f == 0.0:
                raise FloatingPointError("injected failure under fork")
            return toy_native(m, f, *nuis)
        pred = _pred(native)
        rec = sweep.run_sweep(pred(-22.0, 0.35, 10.5, 2.0, 0.0, 1.0), COV, pred, "synthetic",
                              tmp_path / "fork.json", m_grid=MG, f_grid=FG, workers=3)
        assert sum(c["failed"] for c in rec["cells"]) == 1 and rec["contour_status"].startswith("WITHHELD")
