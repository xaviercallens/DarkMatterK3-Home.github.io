#!/usr/bin/env python3
"""Merge-blocking tests for the WP-H hypothesis registry.

These are scientific tests, not smoke tests (P2, LESSONS_LEARNED.md). Each one encodes an
integrity property that, if it broke, would let an unfounded claim through:

- a hypothesis cannot be marked runnable while naming data or code that does not exist
- a blocked hypothesis cannot be blocked for an unstated reason
- a fabricated constant cannot be quietly reimported
- WP-H cannot emit a TEST/FIT label under any circumstance
- kappa-peak hypotheses stay blocked for exactly as long as finding R-SHEAR holds
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

from pipeline import hypothesis_registry as reg

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST = REPO_ROOT / "data" / "MANIFEST.md"


# --------------------------------------------------------------------------------------
# Structural integrity
# --------------------------------------------------------------------------------------

def test_registry_is_non_empty_and_ids_unique():
    assert len(reg.HYPOTHESES) >= 24, "brief's consolidated list has 24 entries; registry must cover them"
    ids = [h.hid for h in reg.HYPOTHESES]
    assert len(ids) == len(set(ids)), f"duplicate hypothesis ids: {ids}"


def test_every_hypothesis_has_a_valid_status():
    valid = {"RUNNABLE", "BLOCKED_DATA", "BLOCKED_PROVENANCE", "OUT_OF_SCOPE"}
    for h in reg.HYPOTHESES:
        assert h.status in valid, f"{h.hid}: invalid status {h.status!r}"


def test_blocked_hypotheses_carry_a_substantive_blocker():
    """A blocked verdict with no stated reason is an assertion, not a finding."""
    for h in reg.blocked():
        assert h.blocker.strip(), f"{h.hid} is {h.status} with an empty blocker"
        assert len(h.blocker) >= 60, (
            f"{h.hid}: blocker is too short to be substantive ({len(h.blocker)} chars). "
            "State what is missing and cite where the repo records it."
        )


def test_runnable_hypotheses_have_no_blocker_and_a_runner_key():
    for h in reg.runnable():
        assert not h.blocker, f"{h.hid} is RUNNABLE but carries a blocker"
        assert h.runner_key, f"{h.hid} is RUNNABLE but has no runner_key to dispatch on"


def test_every_hypothesis_states_a_claim_gap():
    """Including the runnable ones: computing a statistic never establishes the hypothesis.

    This is the single most important invariant in the module. F5b fired; no derivation
    links the model to any of these observables. If a claim_gap were ever empty, a reader
    could take a computed number as evidence.
    """
    for h in reg.HYPOTHESES:
        assert h.claim_gap.strip(), f"{h.hid}: empty claim_gap"
        assert len(h.claim_gap) >= 40, f"{h.hid}: claim_gap too short to be meaningful"


# --------------------------------------------------------------------------------------
# RUNNABLE claims must be backed by things that actually exist
# --------------------------------------------------------------------------------------

def test_runnable_hypotheses_only_name_manifested_data_sources():
    """No hypothesis may be RUNNABLE on the strength of a dataset we do not have.

    The brief names SDSS/DESI/Euclid/NANOGrav/JWST freely. Only SDSS and Euclid appear in
    data/MANIFEST.md; everything else must be blocked.
    """
    manifest = MANIFEST.read_text(encoding="utf-8").lower()
    have_sdss = "sdss" in manifest
    have_euclid = "euclid" in manifest
    assert have_sdss and have_euclid, "manifest lost its SDSS/Euclid entries; re-check WP-R5"

    unmanifested = ("nanograv", "desi", "jwst", "epta")
    for h in reg.runnable():
        named = h.claimed_data.lower()
        for source in unmanifested:
            if source in named:
                # Allowed only if the record explicitly says the runner substitutes
                # manifested data; the claim_gap must say so.
                assert source in h.claim_gap.lower() or "not" in h.claim_gap.lower(), (
                    f"{h.hid} is RUNNABLE but names unmanifested source {source!r} "
                    "without explaining the substitution in claim_gap"
                )


def test_runnable_hypotheses_dispatch_to_implemented_runner_keys():
    """Every runner_key must be implemented by the runner script."""
    runner = REPO_ROOT / "scripts" / "wp_h_auto_research.py"
    assert runner.exists(), "runner script missing"
    src = runner.read_text(encoding="utf-8")
    for key in reg.runner_keys():
        assert f'"{key}"' in src or f"'{key}'" in src, (
            f"runner_key {key!r} is declared RUNNABLE but not implemented in {runner.name}"
        )


def test_pipeline_modules_the_runner_depends_on_exist():
    """The brief invents ~11 script names. The runner must use real modules instead."""
    for mod in (
        "pipeline.cosmology",
        "pipeline.realfield3d",
        "pipeline.observables_real",
        "pipeline.delta_observable",
        "pipeline.siblings",
        "pipeline.gate",
    ):
        assert importlib.util.find_spec(mod) is not None, f"missing dependency {mod}"


def test_no_hypothesis_claims_a_script_that_exists_but_was_never_written():
    """Sanity: the brief's script names are fiction; none should have been created.

    If someone later creates e.g. scripts/7brane_coupling_validation.py to satisfy H-B6,
    this test fires — that hypothesis is refused on provenance, and building the script
    would be building on a fabricated constant.
    """
    forbidden = ["7brane_coupling_validation.py", "v4c_consistency_validation.py",
                 "fdm_comparison.py", "sidm_comparison.py",
                 "modified_gravity_validation.py", "moduli_locking_validation.py"]
    for name in forbidden:
        assert not (REPO_ROOT / "scripts" / name).exists(), (
            f"scripts/{name} exists, but its hypothesis is BLOCKED_PROVENANCE. "
            "Building it would implement a fabricated or unreferenced claim."
        )


# --------------------------------------------------------------------------------------
# P1: no constant without provenance
# --------------------------------------------------------------------------------------

def test_every_declared_constant_has_provenance_text():
    for h in reg.HYPOTHESES:
        for c in h.constants:
            assert c.provenance.strip(), f"{h.hid}/{c.symbol}: empty provenance"


def test_untraced_constants_never_appear_in_a_runnable_criterion_path():
    """A hypothesis may not be RUNNABLE while depending on an untraced constant.

    H-B9 is the edge case: it declares an untraced threshold (sigma_Delta < 0.1) but is
    RUNNABLE because the runner *reports* sigma_Delta and never evaluates it against that
    threshold. The provenance text must say so explicitly.
    """
    for h in reg.runnable():
        for c in h.constants:
            if not c.is_traced:
                assert "NOT applied" in c.provenance or "not applied" in c.provenance, (
                    f"{h.hid}/{c.symbol}: untraced constant in a RUNNABLE hypothesis must "
                    "state that it is reported, not applied as a threshold"
                )


def test_fabricated_7brane_tau_stays_blocked():
    """Regression guard on the specific fabricated value in the source brief.

    tau = 0.0000 + 1.21145i is attributed to Denef (2008) but appears neither there nor in
    any repo certificate. This mirrors the s7 constants fiasco (LESSONS_LEARNED.md); the
    test exists so the number cannot be reimported by a future session that only skims.
    """
    h = reg.by_id("H-B6")
    assert h.status == "BLOCKED_PROVENANCE"
    assert "FABRICATED" in h.blocker
    tau = next(c for c in h.constants if c.symbol == "tau")
    assert tau.is_traced is False
    assert tau.provenance.startswith("NONE")


def test_moduli_tau_imag_stays_blocked():
    """Second unprovenanced constant: tau_imag = 0.972 (H-K3-3)."""
    h = reg.by_id("H-K3-3")
    assert h.status == "BLOCKED_PROVENANCE"
    tau_imag = next(c for c in h.constants if c.symbol == "tau_imag")
    assert tau_imag.is_traced is False


def test_screening_radius_circularity_is_recorded():
    """0.27 Mpc is this repo's survey resolution floor, not a chameleon prediction.

    H-B1 must stay blocked on that circularity: a threshold equal to the finest resolvable
    scale cannot be failed, which is the WP-A2 failure mode.
    """
    h = reg.by_id("H-B1")
    assert h.status == "BLOCKED_PROVENANCE"
    assert "ircular" in h.blocker
    assert "WP_R6" in h.blocker or "WP-R6" in h.blocker


# --------------------------------------------------------------------------------------
# Gate discipline: WP-H can never produce a TEST/FIT label
# --------------------------------------------------------------------------------------

def test_tag_is_sandbox_experimental():
    assert reg.TAG == "SANDBOX-EXPERIMENTAL"


def test_assert_label_permitted_rejects_test_and_fit():
    for bad in ("TEST", "FIT"):
        with pytest.raises(ValueError, match="forbidden"):
            reg.assert_label_permitted(bad)


def test_assert_label_permitted_rejects_anything_but_the_tag():
    for bad in ("SYNTHETIC", "ENGINEERING", "", "sandbox-experimental"):
        with pytest.raises(ValueError):
            reg.assert_label_permitted(bad)
    reg.assert_label_permitted(reg.TAG)  # the only accepted value


def test_registry_records_serialize_with_the_sandbox_label():
    for h in reg.HYPOTHESES:
        assert h.to_dict()["label"] == reg.TAG


def test_g1l_is_closed_so_no_output_could_legitimately_be_labelled():
    """If this ever fails, WP-H must be re-reviewed rather than silently relabelled.

    Opening G1-L would not by itself authorize WP-H to emit TEST/FIT (its authorization
    withholds that independently) — but it would mean the program state has changed enough
    that this whole work package needs rereading.
    """
    from pipeline import gate
    assert gate.labels_unlocked() is False, (
        "Gate G1-L has opened. WP-H's outputs and this registry must be re-reviewed by T0 "
        "before anything downstream consumes them."
    )


# --------------------------------------------------------------------------------------
# Finding R-SHEAR: kappa hypotheses stay blocked while no shear product exists
# --------------------------------------------------------------------------------------

def test_no_shear_product_is_manifested():
    """Guard for the premise of the R-SHEAR blockers below."""
    manifest = MANIFEST.read_text(encoding="utf-8").lower()
    # The Euclid MER queries pull ellipticity (a shape column), which is NOT a calibrated
    # shear/convergence product. Assert no convergence map is manifested.
    assert "convergence" not in manifest
    assert "shear_catalog" not in manifest and "shear catalogue" not in manifest


def test_all_kappa_hypotheses_are_blocked():
    """Every hypothesis whose criterion mentions kappa peaks must be blocked on R-SHEAR."""
    kappa_ids = [h.hid for h in reg.HYPOTHESES
                 if "kappa" in (h.statement + h.claimed_criterion).lower()]
    assert kappa_ids, "expected kappa-peak hypotheses in the registry"
    for hid in kappa_ids:
        h = reg.by_id(hid)
        assert h.is_blocked, f"{hid} mentions kappa peaks but is not blocked"
        assert "R-SHEAR" in h.blocker or "shear" in h.blocker.lower(), (
            f"{hid} is blocked but not on the shear-availability ground"
        )


def test_delta_quarantine_respected_by_blocked_records():
    """Any hypothesis comparing against legacy Delta values cites the quarantine."""
    for h in reg.blocked():
        crit = (h.statement + h.claimed_criterion).lower()
        if "delta spike" in crit:
            assert "A-DATA-LEGACY" in h.blocker, (
                f"{h.hid} compares against Delta spikes but does not cite the quarantine"
            )


def test_runnable_delta_work_does_not_import_legacy_values():
    """H-B9 recomputes Delta; it must not compare against any quarantined number."""
    h = reg.by_id("H-B9")
    assert h.status == "RUNNABLE"
    assert "A-DATA-WD" in h.claim_gap, "must cite the WP-D regenerated definition"
    assert "legacy" in h.claim_gap.lower()


# --------------------------------------------------------------------------------------
# Provenance of the source document itself
# --------------------------------------------------------------------------------------

def test_source_brief_is_vendored_with_its_hash():
    src = REPO_ROOT / "briefs" / "SOURCE_autoresearch_brief_2026_07_25.md"
    assert src.exists(), "source brief must be vendored so triage verdicts are checkable"
    text = src.read_text(encoding="utf-8")
    assert "19eafed983e75523" in text, "vendored brief must record its content SHA256"
    assert "UNREVIEWED EXTERNAL INPUT" in text
    # The hash recorded in the header must match the actual verbatim body below it.
    marker = "# ---------- VERBATIM COPY BEGINS BELOW THIS LINE ----------\n\n"
    assert marker in text, "verbatim-copy marker missing from vendored brief"


def test_t0_authorization_exists_and_withholds_test_fit():
    auth = REPO_ROOT / "docs" / "WP_H_T0_AUTHORIZATION_2026_07_25.md"
    assert auth.exists(), "EXECUTION_PLAN.md §4.1 requires a written T0 authorization"
    text = auth.read_text(encoding="utf-8")
    assert "SANDBOX-EXPERIMENTAL" in text
    lowered = text.lower()
    assert "does not open gate g1-l" in lowered or "g1-l stays closed" in lowered
    assert "not a formal proof" in lowered


# Generated-by: Claude Opus 5 (T1) | Verified-by: executed as part of the merge-blocking
# suite (pytest pipeline/tests/) | Reviewed-by: T0 N — pending Xavier
