#!/usr/bin/env python3
"""Tests for S3-02 observable computation framework (stubs for T2).

Golden tests verify:
1. Observables compute stub values while labelling is locked
2. Labels are mechanical (TEST/FIT per type, SYNTHETIC until gate G1-L opens)
3. Assumptions are correct
4. Observable registry manages all observables
5. Observable info is accessible

Gate-state discipline (added 2026-07-25): label tests pin the gate state
explicitly via the `labels_locked` / `labels_open` fixtures instead of relying on
whatever state the repo's own PREDICTION.md happens to be in. The earlier
`*_pre_g1` tests asserted SYNTHETIC while silently assuming the repo was
unpinned; when gate G1 was genuinely opened they failed for the wrong reason,
which hid the real defect (labels were keyed on the pin alone, so placeholder
computations were being stamped FIT/TEST with no §6 prediction behind them).
A label test must therefore state which gate state it is testing.
"""
import pytest

import pipeline.observables as observables_mod
from pipeline.observables import (
    LensingObservable,
    LensingObservableConfig,
    LymanAlphaObservable,
    LymanAlphaObservableConfig,
    PTAObservable,
    PTAObservableConfig,
    ObservableRegistry,
)


@pytest.fixture
def labels_locked(monkeypatch):
    """Gate G1-L closed: no §6 derived quantities, so labels must be SYNTHETIC.

    This is the repo's actual state on the cooper_s7 branch, and permanently so:
    F5b fired (NO_PREDICTION_BRANCH.md §8).
    """
    monkeypatch.setattr(observables_mod, "labels_unlocked", lambda: False)


@pytest.fixture
def labels_open(monkeypatch):
    """Gate G1-L open: pin valid AND §6 carries hash-pinned derived quantities."""
    monkeypatch.setattr(observables_mod, "labels_unlocked", lambda: True)


class TestLensingObservable:
    """Test P1 lensing observable."""

    def test_lensing_compute_stub(self):
        """Lensing observable should compute stub value pre-G1."""
        config = LensingObservableConfig(stub_core_radius_scaling=1.5)
        obs = LensingObservable(config)

        result = obs.compute()
        assert result == 1.5

    def test_lensing_name(self):
        """Lensing observable name."""
        obs = LensingObservable()
        assert obs.name() == "lensing_core_radius"

    def test_lensing_label_locked_is_synthetic(self, labels_locked):
        """With G1-L closed (no §6 prediction), lensing must label SYNTHETIC."""
        assert LensingObservable().label() == "SYNTHETIC"

    def test_lensing_label_open_is_fit(self, labels_open):
        """With G1-L open, lensing labels FIT (normalization fitting allowed)."""
        assert LensingObservable().label() == "FIT"

    def test_lensing_label_synthetic_in_this_repo_today(self):
        """No monkeypatch: the repo's real state must not license a FIT label.

        Guards the WP S3-00b defect directly — a valid pin alone must never be
        enough to label an output, because PREDICTION.md §6 is empty.
        """
        assert LensingObservable().label() == "SYNTHETIC"

    def test_lensing_assumptions(self):
        """Lensing should carry [A-SEQ, A-VOL, A-ONT]."""
        obs = LensingObservable()
        assert set(obs.assumptions()) == {"A-SEQ", "A-VOL", "A-ONT"}

    def test_lensing_description(self):
        """Lensing should have a description."""
        obs = LensingObservable()
        desc = obs.description()
        assert "lensing" in desc.lower()
        assert "shape" in desc.lower()


class TestPTAObservable:
    """Test P2 PTA observable."""

    def test_pta_compute_stub(self):
        """PTA observable should compute stub value pre-G1."""
        config = PTAObservableConfig(stub_pta_lrt=5.2)
        obs = PTAObservable(config)

        result = obs.compute()
        assert result == 5.2

    def test_pta_name(self):
        """PTA observable name."""
        obs = PTAObservable()
        assert obs.name() == "pta_lrt"

    def test_pta_label_locked_is_synthetic(self, labels_locked):
        """With G1-L closed, PTA must label SYNTHETIC — no m_φ to test against."""
        assert PTAObservable().label() == "SYNTHETIC"

    def test_pta_label_open_is_test(self, labels_open):
        """With G1-L open, PTA labels TEST (shape-only, no fitting)."""
        assert PTAObservable().label() == "TEST"

    def test_pta_assumptions(self):
        """PTA should carry [A-SEQ, A-VOL]."""
        obs = PTAObservable()
        assert set(obs.assumptions()) == {"A-SEQ", "A-VOL"}

    def test_pta_description(self):
        """PTA should have a description."""
        obs = PTAObservable()
        desc = obs.description()
        assert "pulsar" in desc.lower() or "p2" in desc.lower()
        assert "timing" in desc.lower()


class TestLymanAlphaObservable:
    """Test P3 Lyman-α observable."""

    def test_lya_compute_stub(self):
        """Lyman-α observable should compute stub value pre-G1."""
        config = LymanAlphaObservableConfig(stub_lya_chi2=9.8)
        obs = LymanAlphaObservable(config)

        result = obs.compute()
        assert result == 9.8

    def test_lya_name(self):
        """Lyman-α observable name."""
        obs = LymanAlphaObservable()
        assert obs.name() == "lyman_alpha_chi2"

    def test_lya_label_locked_is_synthetic(self, labels_locked):
        """With G1-L closed, Lyman-α must label SYNTHETIC."""
        assert LymanAlphaObservable().label() == "SYNTHETIC"

    def test_lya_label_open_is_test(self, labels_open):
        """With G1-L open, Lyman-α labels TEST (null check)."""
        assert LymanAlphaObservable().label() == "TEST"

    def test_lya_assumptions(self):
        """Lyman-α should carry [A-SEQ] only."""
        obs = LymanAlphaObservable()
        assert obs.assumptions() == ["A-SEQ"]

    def test_lya_description(self):
        """Lyman-α should have a description."""
        obs = LymanAlphaObservable()
        desc = obs.description()
        assert "lyman" in desc.lower()
        assert "null" in desc.lower()


class TestObservableRegistry:
    """Test the observable registry."""

    def test_registry_has_three_observables(self):
        """Registry should have lensing, pta, lyman_alpha."""
        registry = ObservableRegistry()
        observables = registry.list_observables()

        assert len(observables) == 3
        assert "lensing" in observables
        assert "pta" in observables
        assert "lyman_alpha" in observables

    def test_registry_compute_all(self):
        """Compute all observables at once."""
        registry = ObservableRegistry()
        results = registry.compute_all()

        assert len(results) == 3
        assert "lensing" in results
        assert "pta" in results
        assert "lyman_alpha" in results

        # Stubs should be positive numbers
        assert isinstance(results["lensing"], (int, float))
        assert isinstance(results["pta"], (int, float))
        assert isinstance(results["lyman_alpha"], (int, float))

    def test_registry_get_observable(self):
        """Get a specific observable by name."""
        registry = ObservableRegistry()
        lensing = registry.get_observable("lensing")

        assert lensing.name() == "lensing_core_radius"

    def test_registry_get_nonexistent_observable_raises(self):
        """Requesting nonexistent observable should raise."""
        registry = ObservableRegistry()

        with pytest.raises(KeyError):
            registry.get_observable("nonexistent")

    def test_registry_observable_info(self, labels_locked):
        """Get metadata for a single observable (G1-L closed)."""
        registry = ObservableRegistry()
        info = registry.observable_info("lensing")

        assert "name" in info
        assert "description" in info
        assert "label" in info
        assert "assumptions" in info
        assert "statistic" in info

        assert info["name"] == "lensing_core_radius"
        assert info["label"] == "SYNTHETIC"  # G1-L closed: no §6 prediction
        assert set(info["assumptions"]) == {"A-SEQ", "A-VOL", "A-ONT"}

    def test_registry_all_info(self):
        """Get metadata for all observables."""
        registry = ObservableRegistry()
        info = registry.all_info()

        assert len(info) == 3
        assert "lensing" in info
        assert "pta" in info
        assert "lyman_alpha" in info

        # Each should have full metadata
        for obs_name, obs_info in info.items():
            assert "name" in obs_info
            assert "label" in obs_info
            assert "assumptions" in obs_info


class TestObservableMetadata:
    """Test observable metadata consistency."""

    def test_lensing_default_config(self):
        """Lensing with default config."""
        obs = LensingObservable()  # Uses default config
        assert obs.compute() > 0  # Default stub is positive

    def test_pta_default_config(self):
        """PTA with default config."""
        obs = PTAObservable()  # Uses default config
        assert obs.compute() > 0  # Default stub is positive

    def test_lya_default_config(self):
        """Lyman-α with default config."""
        obs = LymanAlphaObservable()  # Uses default config
        assert abs(obs.compute() - 10.0) < 0.1  # Default is ~10 (χ²(10) mean)

    def test_observable_assumptions_immutable(self):
        """Observable assumptions should be consistent."""
        obs1 = LensingObservable()
        obs2 = LensingObservable()

        assert obs1.assumptions() == obs2.assumptions()

    def test_observable_label_consistent(self):
        """Observable labels should be consistent across instances."""
        obs1 = PTAObservable()
        obs2 = PTAObservable()

        assert obs1.label() == obs2.label()


class TestObservableRegistry_Integration:
    """Integration tests for observable registry."""

    def test_registry_all_assumptions_distinct(self):
        """Each observable should have distinct assumption set."""
        registry = ObservableRegistry()

        lensing = registry.get_observable("lensing")
        pta = registry.get_observable("pta")
        lya = registry.get_observable("lyman_alpha")

        lensing_assumptions = set(lensing.assumptions())
        pta_assumptions = set(pta.assumptions())
        lya_assumptions = set(lya.assumptions())

        # Lensing has the most assumptions
        assert len(lensing_assumptions) == 3
        # PTA has fewer
        assert len(pta_assumptions) == 2
        # Lyman-α has just one
        assert len(lya_assumptions) == 1

        # Lensing ⊃ PTA ⊃ Lyman-α (subset relationship)
        assert pta_assumptions.issubset(lensing_assumptions)
        assert lya_assumptions.issubset(pta_assumptions)

    def test_registry_all_labels_synthetic_when_locked(self, labels_locked):
        """All observables label SYNTHETIC while G1-L is closed."""
        registry = ObservableRegistry()

        for obs_name in registry.list_observables():
            assert registry.get_observable(obs_name).label() == "SYNTHETIC"

    def test_registry_no_observable_labels_test_or_fit_in_this_repo(self):
        """No monkeypatch: nothing in this repo may currently claim TEST/FIT.

        The merge-blocking guard against the WP S3-00b defect. If this fails,
        something is labelling outputs as tested against a prediction that
        PREDICTION.md §6 does not contain.
        """
        registry = ObservableRegistry()

        for obs_name in registry.list_observables():
            assert registry.get_observable(obs_name).label() == "SYNTHETIC", (
                f"{obs_name} claims a TEST/FIT label, but PREDICTION.md §6 has "
                "no derived quantities (F5b — see NO_PREDICTION_BRANCH.md §8)"
            )

    def test_registry_reproducible_statistics(self):
        """Same registry instance should produce same statistics."""
        registry = ObservableRegistry()

        results1 = registry.compute_all()
        results2 = registry.compute_all()

        for obs_name in registry.list_observables():
            assert results1[obs_name] == results2[obs_name]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
