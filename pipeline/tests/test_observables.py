#!/usr/bin/env python3
"""Tests for S3-02 observable computation framework (stubs for T2).

Golden tests verify:
1. Observables compute stub values pre-G1
2. Labels are mechanical (TEST/FIT per type, SYNTHETIC pre-G1)
3. Assumptions are correct
4. Observable registry manages all observables
5. Observable info is accessible
"""
import pytest

from pipeline.observables import (
    LensingObservable,
    LensingObservableConfig,
    LymanAlphaObservable,
    LymanAlphaObservableConfig,
    PTAObservable,
    PTAObservableConfig,
    ObservableRegistry,
)


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

    def test_lensing_label_pre_g1(self):
        """Pre-G1, lensing label should be SYNTHETIC."""
        obs = LensingObservable()
        # Assuming PREDICTION.md is unpinned (pre-G1)
        label = obs.label()
        assert label == "SYNTHETIC"

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

    def test_pta_label_pre_g1(self):
        """Pre-G1, PTA label should be SYNTHETIC (TEST post-G1)."""
        obs = PTAObservable()
        label = obs.label()
        assert label == "SYNTHETIC"

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

    def test_lya_label_pre_g1(self):
        """Pre-G1, Lyman-α label should be SYNTHETIC (TEST post-G1)."""
        obs = LymanAlphaObservable()
        label = obs.label()
        assert label == "SYNTHETIC"

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

    def test_registry_observable_info(self):
        """Get metadata for a single observable."""
        registry = ObservableRegistry()
        info = registry.observable_info("lensing")

        assert "name" in info
        assert "description" in info
        assert "label" in info
        assert "assumptions" in info
        assert "statistic" in info

        assert info["name"] == "lensing_core_radius"
        assert info["label"] == "SYNTHETIC"  # Pre-G1
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

    def test_registry_all_labels_synthetic_pre_g1(self):
        """All observables should label as SYNTHETIC pre-G1."""
        registry = ObservableRegistry()

        for obs_name in registry.list_observables():
            obs = registry.get_observable(obs_name)
            label = obs.label()
            assert label == "SYNTHETIC"  # Pre-G1

    def test_registry_reproducible_statistics(self):
        """Same registry instance should produce same statistics."""
        registry = ObservableRegistry()

        results1 = registry.compute_all()
        results2 = registry.compute_all()

        for obs_name in registry.list_observables():
            assert results1[obs_name] == results2[obs_name]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
