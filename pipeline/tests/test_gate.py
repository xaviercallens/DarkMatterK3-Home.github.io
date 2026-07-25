"""Gate G1 control-example tests (golden-good pinned / golden-bad unpinned)."""
import hashlib

import pytest

import pipeline.gate as gate


def _write_prediction(path, body: str, pin: bool):
    if pin:
        sha = hashlib.sha256(body.encode()).hexdigest()
        text = f"PINNED: {sha}\n{body}"
    else:
        text = body
    path.write_text(text)


def test_unpinned_prediction_blocks_real_data(tmp_path, monkeypatch):
    p = tmp_path / "PREDICTION.md"
    _write_prediction(p, "Status: draft\n", pin=False)
    monkeypatch.setattr(gate, "PREDICTION_PATH", p)

    assert gate.is_pinned() is False
    with pytest.raises(gate.GateError):
        gate.require_pinned_for_real_data()


def test_pinned_prediction_with_valid_hash_opens_gate(tmp_path, monkeypatch):
    p = tmp_path / "PREDICTION.md"
    _write_prediction(p, "Status: frozen\nm_phi: 1e-23 eV\n", pin=True)
    monkeypatch.setattr(gate, "PREDICTION_PATH", p)

    assert gate.is_pinned() is True
    assert gate.verify_pin_hash() is True
    gate.require_pinned_for_real_data()  # must not raise


def test_pinned_header_with_tampered_body_fails_hash_check(tmp_path, monkeypatch):
    p = tmp_path / "PREDICTION.md"
    _write_prediction(p, "Status: frozen\nm_phi: 1e-23 eV\n", pin=True)
    monkeypatch.setattr(gate, "PREDICTION_PATH", p)

    # Tamper with the body after pinning without updating the hash.
    tampered = p.read_text().replace("1e-23 eV", "1e-20 eV")
    p.write_text(tampered)

    assert gate.is_pinned() is True  # header still present
    assert gate.verify_pin_hash() is False  # but content no longer matches


def test_missing_prediction_file_is_unpinned(tmp_path, monkeypatch):
    monkeypatch.setattr(gate, "PREDICTION_PATH", tmp_path / "does_not_exist.md")
    assert gate.is_pinned() is False


# ===========================================================================
# Gate G1-L — TEST/FIT labelling requires §6 derived quantities
#
# Added 2026-07-25 under T0 ruling after WP S3-00b. The defect these guard
# against: labelling was keyed on the pin alone, so opening G1 caused
# placeholder computations to be stamped FIT/TEST even though PREDICTION.md
# §6 (m_phi, alpha_D, Lambda_D) was empty by design. See
# briefs/GATE_G1L_RULING_2026_07_25.md.
# ===========================================================================

RESERVED_S6 = "## 6. Derived quantities — RESERVED (v1.1)\n\nEmpty by design.\n"
FILLED_S6 = "## 6. Derived quantities\n\nLambda_D in [6.6e-3, 2.24e1] eV [A-DD]\n"
PROSE_ONLY_S6 = "## 6. Derived quantities\n\nThis section describes derived results.\n"
DUMMY_S6 = "## 6. Derived quantities\n\nm_phi = 3.1e-23 eV +/- 0.4e-23 [A-VOL]\n"


def _write_with_sections(path, section6: str, pin: bool, derive: bool):
    """Build a PREDICTION.md with rules + a §6, optionally pinned and/or derived.

    Mirrors the real file's layout: marker lines on top, §6 lower down.
    """
    body = "## 5. Kill condition\n\npre-committed\n\n" + section6
    header = ""
    if pin:
        header += f"PINNED: {hashlib.sha256(body.encode()).hexdigest()}\n"
    if derive:
        header += f"DERIVED: {hashlib.sha256(section6.encode()).hexdigest()}\n"
    path.write_text(header + body)


def test_pin_without_derived_quantities_blocks_labelling(tmp_path, monkeypatch):
    """The exact WP S3-00b state: rules pinned, §6 reserved. Labels stay locked."""
    p = tmp_path / "PREDICTION.md"
    _write_with_sections(p, RESERVED_S6, pin=True, derive=False)
    monkeypatch.setattr(gate, "PREDICTION_PATH", p)

    assert gate.is_pinned() is True
    assert gate.verify_pin_hash() is True
    gate.require_pinned_for_real_data()          # G1 open: data access allowed
    assert gate.has_derived_quantities() is False
    assert gate.labels_unlocked() is False       # G1-L closed: no labelling
    with pytest.raises(gate.GateError):
        gate.require_derived_for_labels()


def test_pin_plus_derived_quantities_unlocks_labelling(tmp_path, monkeypatch):
    p = tmp_path / "PREDICTION.md"
    _write_with_sections(p, FILLED_S6, pin=True, derive=True)
    monkeypatch.setattr(gate, "PREDICTION_PATH", p)

    assert gate.verify_pin_hash() is True
    assert gate.verify_derived_hash() is True
    assert gate.has_derived_quantities() is True
    assert gate.labels_unlocked() is True
    gate.require_derived_for_labels()  # must not raise


def test_derived_marker_over_reserved_section_is_refused(tmp_path, monkeypatch):
    """A correctly-computed DERIVED hash over a still-RESERVED §6 must not pass.

    Guards the footgun of pinning an empty section: the hash verifies, so only
    the placeholder-wording check catches it.
    """
    p = tmp_path / "PREDICTION.md"
    _write_with_sections(p, RESERVED_S6, pin=True, derive=True)
    monkeypatch.setattr(gate, "PREDICTION_PATH", p)

    assert gate.verify_derived_hash() is True     # hash is genuinely correct
    assert gate.has_derived_quantities() is False  # but §6 is still a placeholder
    assert gate.labels_unlocked() is False


def test_tampered_section6_fails_derived_hash(tmp_path, monkeypatch):
    p = tmp_path / "PREDICTION.md"
    _write_with_sections(p, FILLED_S6, pin=True, derive=True)
    monkeypatch.setattr(gate, "PREDICTION_PATH", p)

    # Edit a derived value after pinning it -- the classic post-hoc tune.
    p.write_text(p.read_text().replace("6.6e-3", "9.9e-3"))

    assert gate.derived_pin() is not None       # header still there
    assert gate.verify_derived_hash() is False  # content no longer matches
    assert gate.labels_unlocked() is False


def test_derived_without_pin_does_not_unlock(tmp_path, monkeypatch):
    """§6 values with no pin on the rules is not a pre-registration."""
    p = tmp_path / "PREDICTION.md"
    _write_with_sections(p, FILLED_S6, pin=False, derive=True)
    monkeypatch.setattr(gate, "PREDICTION_PATH", p)

    assert gate.has_derived_quantities() is True
    assert gate.is_pinned() is False
    assert gate.labels_unlocked() is False
    with pytest.raises(gate.GateError):
        gate.require_derived_for_labels()


def test_adding_derived_marker_preserves_existing_pin_hash(tmp_path, monkeypatch):
    """Backward compatibility: a DERIVED: line must not invalidate a PINNED: hash.

    The two markers are set in different commits, so stripping logic has to
    ignore both when recomputing the body hash.
    """
    p = tmp_path / "PREDICTION.md"
    _write_with_sections(p, FILLED_S6, pin=True, derive=False)
    monkeypatch.setattr(gate, "PREDICTION_PATH", p)
    assert gate.verify_pin_hash() is True

    # Now add the DERIVED: header exactly as a later commit would.
    text = p.read_text()
    section6_hash = hashlib.sha256(FILLED_S6.encode()).hexdigest()
    p.write_text(f"DERIVED: {section6_hash}\n" + text)

    assert gate.verify_pin_hash() is True, "adding DERIVED: broke the pin hash"
    assert gate.labels_unlocked() is True


def test_schema_validator_accepts_valid_bounded_quantity(tmp_path, monkeypatch):
    """Schema-conformant line in §6 passes validation."""
    p = tmp_path / "PREDICTION.md"
    _write_with_sections(p, FILLED_S6, pin=True, derive=True)
    monkeypatch.setattr(gate, "PREDICTION_PATH", p)

    assert gate.section6_has_bounded_quantities() is True
    assert gate.has_derived_quantities() is True


def test_schema_validator_refuses_prose_only(tmp_path, monkeypatch):
    """§6 with no schema-conformant line fails validation."""
    p = tmp_path / "PREDICTION.md"
    _write_with_sections(p, PROSE_ONLY_S6, pin=True, derive=True)
    monkeypatch.setattr(gate, "PREDICTION_PATH", p)

    assert gate.section6_has_bounded_quantities() is False
    assert gate.has_derived_quantities() is False  # fails schema check


def test_schema_validator_refuses_dummy_string(tmp_path, monkeypatch):
    """A dummy string designed to fool the old wording check still fails schema."""
    p = tmp_path / "PREDICTION.md"
    # DUMMY_S6 looks plausible (has "eV", "[A-VOL]") but doesn't match the regex
    _write_with_sections(p, DUMMY_S6, pin=True, derive=True)
    monkeypatch.setattr(gate, "PREDICTION_PATH", p)

    assert gate.section6_has_bounded_quantities() is False
    assert gate.has_derived_quantities() is False  # fails schema check


def test_this_repo_is_pinned_but_labels_locked():
    """Live state of this repo, no monkeypatch: G1 open, G1-L closed.

    This is the F5b end-state and is expected to hold indefinitely on the
    cooper_s7 branch. If it ever flips, either §6 was populated (a real S3-00
    result -- update this test) or the gate regressed.
    """
    assert gate.is_pinned() is True
    assert gate.verify_pin_hash() is True
    assert gate.labels_unlocked() is False
