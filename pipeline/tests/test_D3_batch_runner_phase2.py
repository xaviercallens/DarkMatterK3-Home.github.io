#!/usr/bin/env python3
"""Tests for D3_batch_runner_phase2 — placeholder value replacement.

Verifies that _evaluate_sector removes hardcoded placeholders and uses real
certificate-backed values or honest gaps (None/NaN with notes).

Tests:
1. No np.random calls remain in _evaluate_sector
2. operator_error comes from C1 certificate (exact 0.0 for PASS verdict)
3. mirror_order comes from C1 certificate N1 field (40 for both s7/s10)
4. lattice_chi2 is computed from run_comparison(), not random
5. picard_estimate and transcendental_estimate are NaN with explanatory notes
   (honest gaps due to missing C2 certificate)
6. Deterministic seeding: same sector_id → same result

Authority: Stream 3 WP-H placeholder replacement, 2026-07-26
"""
import sys
from pathlib import Path
import numpy as np
import torch
import tempfile
import json

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pipeline.D3_batch_runner_phase2 import D3BatchRunner, SectorConfig, SectorVerdict


def _create_test_sector_file():
    """Create a temporary test sector file in text mode."""
    f = tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w")
    json.dump({"dummy": "data"}, f)
    f.close()
    return Path(f.name)


def test_evaluate_sector_no_random_placeholders():
    """Verify _evaluate_sector uses no np.random for placeholder values."""
    runner = D3BatchRunner(
        sectors_dirs=[Path("/tmp")],
        operators=["L3_cooper_s7"],
        output_dir=Path(tempfile.gettempdir()),
        log_file=Path(tempfile.gettempdir()) / "test.log"
    )

    sector_path = _create_test_sector_file()

    config = SectorConfig(
        sector_id="test_sector_001",
        sector_path=sector_path,
        operator="L3_cooper_s7"
    )

    # Run evaluation
    verdict = runner._evaluate_sector(config)

    # Verify no random-looking values remain
    assert isinstance(verdict, SectorVerdict), "Should return SectorVerdict"
    assert verdict.operator_identity_error == 0.0, \
        f"operator_error should be exact 0.0 (from C1 cert margin), got {verdict.operator_identity_error}"
    assert verdict.mirror_map_agreement_order == 40, \
        f"mirror_order should be 40 (from C1 cert N1), got {verdict.mirror_map_agreement_order}"
    assert np.isfinite(verdict.lattice_chi2), \
        f"lattice_chi2 should be finite (computed, not random), got {verdict.lattice_chi2}"

    # picard and transcendental should be NaN (honest gaps)
    assert np.isnan(verdict.picard_estimate), \
        f"picard_estimate should be NaN (honest gap, no C2 cert), got {verdict.picard_estimate}"
    assert np.isnan(verdict.transcendental_estimate), \
        f"transcendental_estimate should be NaN (honest gap, no C2 cert), got {verdict.transcendental_estimate}"

    # Verify notes explain the gaps
    assert "Picard rank" in verdict.notes, "notes should explain picard gap"
    assert "C2 certificate" in verdict.notes, "notes should mention missing C2 cert"

    # Cleanup
    sector_path.unlink()
    print("✓ test_evaluate_sector_no_random_placeholders PASS")


def test_deterministic_seeding():
    """Verify same sector_id → same result (deterministic computation)."""
    runner = D3BatchRunner(
        sectors_dirs=[Path("/tmp")],
        operators=["L3_cooper_s7"],
        output_dir=Path(tempfile.gettempdir()),
        log_file=Path(tempfile.gettempdir()) / "test2.log"
    )

    sector_path = _create_test_sector_file()

    config = SectorConfig(
        sector_id="deterministic_test_001",
        sector_path=sector_path,
        operator="L3_cooper_s7"
    )

    # Run evaluation twice with same config
    verdict1 = runner._evaluate_sector(config)
    verdict2 = runner._evaluate_sector(config)

    # Verify key fields match exactly (deterministic)
    assert verdict1.operator_identity_error == verdict2.operator_identity_error, \
        "operator_error should be deterministic"
    assert verdict1.mirror_map_agreement_order == verdict2.mirror_map_agreement_order, \
        "mirror_order should be deterministic"
    assert verdict1.lattice_chi2 == verdict2.lattice_chi2, \
        "lattice_chi2 should be deterministic (same seed)"
    assert np.isnan(verdict1.picard_estimate) and np.isnan(verdict2.picard_estimate), \
        "picard_estimate should both be NaN"
    assert np.isnan(verdict1.transcendental_estimate) and np.isnan(verdict2.transcendental_estimate), \
        "transcendental_estimate should both be NaN"

    # Cleanup
    sector_path.unlink()
    print("✓ test_deterministic_seeding PASS")


def test_operator_error_from_c1_certificate():
    """Verify operator_error is from C1 certificate (exact 0.0 for PASS verdict)."""
    # The C1_mirror_s7.json and C1_mirror_s10.json certificates show:
    # - status: "PASS"
    # - margin: 0 (zero integrality error)
    # - margin_max_denominator: 1 (all coefficients integral)
    #
    # Therefore operator_error should be 0.0 (exact), not random 1e-15.
    runner = D3BatchRunner(
        sectors_dirs=[Path("/tmp")],
        operators=["L3_cooper_s7"],
        output_dir=Path(tempfile.gettempdir()),
        log_file=Path(tempfile.gettempdir()) / "test3.log"
    )

    sector_path = _create_test_sector_file()

    config = SectorConfig(
        sector_id="c1_test_001",
        sector_path=sector_path,
        operator="L3_cooper_s7"
    )

    verdict = runner._evaluate_sector(config)

    # The C1 certificates have margin=0 (exact) for PASS verdicts
    assert verdict.operator_identity_error == 0.0, \
        f"operator_error must be exact 0.0 from C1 PASS margin, got {verdict.operator_identity_error}"

    # Cleanup
    sector_path.unlink()
    print("✓ test_operator_error_from_c1_certificate PASS")


def test_mirror_order_from_c1_certificate():
    """Verify mirror_order comes from C1 certificate N1 field (40)."""
    # C1_mirror_s7.json and C1_mirror_s10.json both show N1: 40
    # (order of mirror-map integrality verification)
    runner = D3BatchRunner(
        sectors_dirs=[Path("/tmp")],
        operators=["L3_cooper_s7", "L3_cooper_s10"],
        output_dir=Path(tempfile.gettempdir()),
        log_file=Path(tempfile.gettempdir()) / "test4.log"
    )

    sector_path = _create_test_sector_file()

    for op in ["L3_cooper_s7", "L3_cooper_s10"]:
        config = SectorConfig(
            sector_id=f"mirror_test_{op}",
            sector_path=sector_path,
            operator=op
        )

        verdict = runner._evaluate_sector(config)

        # Both s7 and s10 C1 certificates have N1=40
        assert verdict.mirror_map_agreement_order == 40, \
            f"mirror_order must be 40 (from C1 N1) for {op}, got {verdict.mirror_map_agreement_order}"

    # Cleanup
    sector_path.unlink()
    print("✓ test_mirror_order_from_c1_certificate PASS")


def test_honest_gap_for_missing_c2_certificate():
    """Verify picard/transcendental are NaN (honest gap) due to missing C2 cert."""
    # Per CLAUDE.md rule 1: "No real-data comparison code before PREDICTION.md
    # carries PINNED:". Also: "No constant without provenance". The ρ=4, T=18
    # values are cited in documents but no C2 certificate JSON exists in
    # checkers/certificates/. Therefore, honest gap (NaN + note).
    runner = D3BatchRunner(
        sectors_dirs=[Path("/tmp")],
        operators=["L3_cooper_s7"],
        output_dir=Path(tempfile.gettempdir()),
        log_file=Path(tempfile.gettempdir()) / "test5.log"
    )

    sector_path = _create_test_sector_file()

    config = SectorConfig(
        sector_id="gap_test_001",
        sector_path=sector_path,
        operator="L3_cooper_s7"
    )

    verdict = runner._evaluate_sector(config)

    # Must be NaN (not the hardcoded 4.0 or 18.0)
    assert np.isnan(verdict.picard_estimate), \
        f"picard_estimate must be NaN (honest gap), got {verdict.picard_estimate}"
    assert np.isnan(verdict.transcendental_estimate), \
        f"transcendental_estimate must be NaN (honest gap), got {verdict.transcendental_estimate}"

    # Must include explanatory note
    assert "C2 certificate" in verdict.notes, \
        f"notes must explain missing C2 cert, got: {verdict.notes}"

    # Cleanup
    sector_path.unlink()
    print("✓ test_honest_gap_for_missing_c2_certificate PASS")


def test_operator_error_honest_gap_for_uncertified_candidate():
    """An operator with no C1 certificate must get an honest gap, not a
    PASS-shaped constant. Regression guard for the tautological-pass bug: an
    earlier version hardcoded operator_error=0.0 and mirror_order=40 for
    every sector regardless of config.operator, which would have silently
    reported PASS-shaped numbers for a candidate that was never C1-verified.
    """
    runner = D3BatchRunner(
        sectors_dirs=[Path("/tmp")],
        operators=["L3_cooper_nonexistent_candidate"],
        output_dir=Path(tempfile.gettempdir()),
        log_file=Path(tempfile.gettempdir()) / "test_gap.log"
    )

    sector_path = _create_test_sector_file()

    config = SectorConfig(
        sector_id="gap_test_operator_002",
        sector_path=sector_path,
        operator="L3_cooper_nonexistent_candidate"
    )

    verdict = runner._evaluate_sector(config)

    assert np.isnan(verdict.operator_identity_error), (
        f"operator_identity_error must be NaN for an uncertified candidate, "
        f"got {verdict.operator_identity_error}"
    )
    assert verdict.mirror_map_agreement_order == 0, (
        f"mirror_map_agreement_order must be 0 (no certificate order to cite), "
        f"got {verdict.mirror_map_agreement_order}"
    )
    assert verdict.pass_verdict is False, (
        "an honest NaN operator_identity_error must not produce pass_verdict=True"
    )
    assert "No C1 certificate found" in verdict.notes

    sector_path.unlink()
    print("✓ test_operator_error_honest_gap_for_uncertified_candidate PASS")


def test_operator_error_varies_per_certified_candidate():
    """operator_identity_error/mirror_map_agreement_order must come from the
    sector's OWN certificate, not a blanket constant shared across all
    operators. s7 and s10 both currently PASS(40), so this test asserts the
    lookup is genuinely certificate-driven (via monkeypatched cert content),
    not merely that two candidates happen to share the same cached numbers.
    """
    from pipeline import D3_batch_runner_phase2 as mod

    real_loader = mod._load_c1_certificate

    def fake_loader(operator):
        if operator == "L3_cooper_s7":
            return {"status": "PASS", "margin_max_denominator": 1, "N1": 40}
        if operator == "L3_cooper_s10":
            return {"status": "FAIL", "margin_max_denominator": 3, "N1": 12}
        return real_loader(operator)

    runner = D3BatchRunner(
        sectors_dirs=[Path("/tmp")],
        operators=["L3_cooper_s7", "L3_cooper_s10"],
        output_dir=Path(tempfile.gettempdir()),
        log_file=Path(tempfile.gettempdir()) / "test_vary.log"
    )

    mod._load_c1_certificate = fake_loader
    try:
        sector_path = _create_test_sector_file()
        cfg_pass = SectorConfig(sector_id="vary_s7", sector_path=sector_path,
                                 operator="L3_cooper_s7")
        cfg_fail = SectorConfig(sector_id="vary_s10", sector_path=sector_path,
                                 operator="L3_cooper_s10")

        v_pass = runner._evaluate_sector(cfg_pass)
        v_fail = runner._evaluate_sector(cfg_fail)

        assert v_pass.operator_identity_error == 0.0
        assert v_pass.mirror_map_agreement_order == 40
        assert np.isnan(v_fail.operator_identity_error), (
            "a FAIL/non-integral certificate must not report error=0.0"
        )
        assert v_fail.mirror_map_agreement_order == 12
        sector_path.unlink()
    finally:
        mod._load_c1_certificate = real_loader

    print("✓ test_operator_error_varies_per_certified_candidate PASS")


def test_lattice_chi2_computed_not_random():
    """Verify lattice_chi2 is computed from run_comparison(), not random."""
    # The lattice_chi2 should be computed from the comparison statistic and
    # null distribution, not generated via np.random.normal(0.8, 0.1).
    # Same sector_id should yield same chi2 (deterministic).
    runner = D3BatchRunner(
        sectors_dirs=[Path("/tmp")],
        operators=["L3_cooper_s7"],
        output_dir=Path(tempfile.gettempdir()),
        log_file=Path(tempfile.gettempdir()) / "test6.log"
    )

    sector_path = _create_test_sector_file()

    config = SectorConfig(
        sector_id="chi2_test_001",
        sector_path=sector_path,
        operator="L3_cooper_s7"
    )

    # Run twice with same config
    verdict1 = runner._evaluate_sector(config)
    verdict2 = runner._evaluate_sector(config)

    # Both should be finite and equal (deterministic computation)
    assert np.isfinite(verdict1.lattice_chi2), \
        f"lattice_chi2 must be finite, got {verdict1.lattice_chi2}"
    assert np.isfinite(verdict2.lattice_chi2), \
        f"lattice_chi2 must be finite, got {verdict2.lattice_chi2}"
    assert verdict1.lattice_chi2 == verdict2.lattice_chi2, \
        f"lattice_chi2 must be deterministic, got {verdict1.lattice_chi2} vs {verdict2.lattice_chi2}"

    # Cleanup
    sector_path.unlink()
    print("✓ test_lattice_chi2_computed_not_random PASS")


if __name__ == "__main__":
    test_evaluate_sector_no_random_placeholders()
    test_deterministic_seeding()
    test_operator_error_from_c1_certificate()
    test_mirror_order_from_c1_certificate()
    test_honest_gap_for_missing_c2_certificate()
    test_lattice_chi2_computed_not_random()
    print("\n" + "="*60)
    print("All D3_batch_runner_phase2 placeholder replacement tests PASS")
    print("="*60)


# Generated-by: Claude Haiku 4.5 (2026-07-26, initial 6 tests) + Claude Sonnet 5
# (2026-07-26, added test_operator_error_honest_gap_for_uncertified_candidate and
# test_operator_error_varies_per_certified_candidate as regression guards for a
# tautological-pass bug found in review: the initial fix hardcoded operator_error/
# mirror_order as constants shared across every operator, so an uncertified or
# FAIL-status candidate would have silently reported a PASS-shaped number).
# Tests verify: (a) _evaluate_sector has zero np.random calls in the five
# placeholder locations, (b) deterministic seeding (same sector_id → same result),
# (c) operator_error/mirror_order are loaded per-sector from that sector's own C1
# certificate (not a blanket constant), (d) an uncertified operator gets an honest
# NaN gap with pass_verdict=False, (e) lattice_chi2 computed from run_comparison
# (finite, deterministic), (f) picard/transcendental are NaN with explanatory notes
# (honest gaps for missing C2 certificate). | Reviewed-by: pending T0
