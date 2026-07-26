"""Test suite for PREDICTION_v2_DRAFT.md structural schema validation.

Ensures that the draft remains a valid, non-executable placeholder that:
1. Exists and is parseable
2. Contains ZERO lines matching the PINNED: or DERIVED: header regexes
3. Contains all three _RESERVED_MARKERS strings (proof of placeholder intent)
4. Mirrors all section numbers from the real PREDICTION.md (structural consistency)
"""
import re
from pathlib import Path

import pytest

import pipeline.gate as gate


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PREDICTION_PATH = REPO_ROOT / "PREDICTION.md"
PREDICTION_V2_DRAFT_PATH = REPO_ROOT / "PREDICTION_v2_DRAFT.md"


def test_v2_draft_file_exists():
    """Assert PREDICTION_v2_DRAFT.md exists in the repo root."""
    assert PREDICTION_V2_DRAFT_PATH.exists(), (
        f"PREDICTION_v2_DRAFT.md does not exist at {PREDICTION_V2_DRAFT_PATH}"
    )


def test_v2_draft_contains_no_pinned_header():
    """Assert the draft contains NO line matching the PINNED: <sha256> regex.

    This prevents accidental machine-parsing as a real pin if the file is ever
    mishandled or reused.
    """
    draft_text = PREDICTION_V2_DRAFT_PATH.read_text(encoding="utf-8")
    pin_matches = gate._PIN_RE.findall(draft_text)
    assert len(pin_matches) == 0, (
        f"Draft must not contain PINNED: header lines; found {len(pin_matches)}: "
        f"{pin_matches}"
    )


def test_v2_draft_contains_no_derived_header():
    """Assert the draft contains NO line matching the DERIVED: <sha256> regex.

    This prevents accidental machine-parsing as a real derivation pin if the
    file is ever mishandled.
    """
    draft_text = PREDICTION_V2_DRAFT_PATH.read_text(encoding="utf-8")
    derived_matches = gate._DERIVED_RE.findall(draft_text)
    assert len(derived_matches) == 0, (
        f"Draft must not contain DERIVED: header lines; found {len(derived_matches)}: "
        f"{derived_matches}"
    )


def test_v2_draft_contains_all_reserved_markers():
    """Assert the draft contains all three _RESERVED_MARKERS strings.

    Proof that the file is intentionally a placeholder, not a document with
    missing content by accident.
    """
    draft_text = PREDICTION_V2_DRAFT_PATH.read_text(encoding="utf-8")
    for marker in gate._RESERVED_MARKERS:
        assert marker in draft_text, (
            f"Draft must contain placeholder marker '{marker}'; not found"
        )


def test_v2_draft_mirrors_prediction_v1_section_numbers():
    """Assert every section number in PREDICTION.md also appears in the draft.

    Extract heading patterns like "## 1.", "## 2a.", "## 2.", ..., "## 6." from
    both files and verify the draft contains all of them.
    """
    section_pattern = re.compile(r"^##\s+(\d+[a-z]?)\.", re.MULTILINE)

    prediction_text = PREDICTION_PATH.read_text(encoding="utf-8")
    draft_text = PREDICTION_V2_DRAFT_PATH.read_text(encoding="utf-8")

    prediction_sections = set(section_pattern.findall(prediction_text))
    draft_sections = set(section_pattern.findall(draft_text))

    missing = prediction_sections - draft_sections
    assert len(missing) == 0, (
        f"Draft is missing sections from PREDICTION.md: {sorted(missing)}"
    )

    # Sanity check: both should have the same sections
    assert prediction_sections == draft_sections, (
        f"Section mismatch: PREDICTION v1.0 has {sorted(prediction_sections)}, "
        f"draft has {sorted(draft_sections)}"
    )


def test_v2_draft_is_not_pinned_as_gate_input():
    """Demonstrate that the draft cannot be parsed as a pinned prediction.

    This confirms the file is structurally safe to coexist with PREDICTION.md
    without being accidentally invoked as a replacement.
    """
    # Temporarily point gate.py's PREDICTION_PATH at the draft
    original_path = gate.PREDICTION_PATH
    try:
        gate.PREDICTION_PATH = PREDICTION_V2_DRAFT_PATH
        # Reload the _text() function's cached result (it reads fresh each time)
        assert gate.is_pinned() is False, (
            "Draft should not be parsed as pinned"
        )
        assert gate.has_derived_quantities() is False, (
            "Draft should not be parsed as having derived quantities"
        )
        assert gate.labels_unlocked() is False, (
            "Draft should not unlock TEST/FIT labels"
        )
    finally:
        gate.PREDICTION_PATH = original_path


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
