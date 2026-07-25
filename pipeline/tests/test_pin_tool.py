"""Tests for scripts/pin_prediction.py (WP-B: pin tool).

Golden tests:
1. Round-trip: generate -> verify -> hash matches
2. Idempotence: running twice with same file produces identical hashes
3. --force behavior: overwrite existing valid header
4. Marker ordering: DERIVED added after PINNED keeps PINNED valid
"""
import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

# Relative to this test file
PIN_TOOL = Path(__file__).parent.parent.parent / "scripts" / "pin_prediction.py"


def run_pin_tool(tmp_file: Path, *args) -> tuple[int, str, str]:
    """Run pin_prediction.py and return (exit_code, stdout, stderr)."""
    cmd = [sys.executable, str(PIN_TOOL), "--file", str(tmp_file), *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


@pytest.fixture
def unpinned_file(tmp_path):
    """An unpinned PREDICTION.md-like file."""
    f = tmp_path / "PREDICTION.md"
    f.write_text("## 1. Overview\nTest document\n\n## 6. Derived quantities\nReserved.\n")
    return f


def test_round_trip_pin(unpinned_file):
    """Generate pin -> verify hash matches."""
    # Generate
    code, out, err = run_pin_tool(unpinned_file, "--pin")
    assert code == 0, err
    assert "Added PINNED:" in out

    # Extract generated hash
    for line in out.split("\n"):
        if "Added PINNED:" in line:
            generated_hash = line.split()[-1]
            break
    else:
        pytest.fail("No PINNED hash in output")

    # Verify the file now has the header
    text = unpinned_file.read_text()
    assert text.startswith(f"PINNED: {generated_hash}")

    # Recompute hash from the file (strip header, as gate.py does)
    from pipeline.gate import _strip_header_lines
    body = _strip_header_lines(text)
    recomputed = hashlib.sha256(body.encode("utf-8")).hexdigest()
    assert recomputed == generated_hash


def test_idempotence_pin(unpinned_file):
    """Running --pin twice produces identical hashes."""
    # First run
    code1, out1, _ = run_pin_tool(unpinned_file, "--pin")
    assert code1 == 0
    hash1 = None
    for line in out1.split("\n"):
        if "Added PINNED:" in line:
            hash1 = line.split()[-1]
            break

    # Overwrite with --force (since the file now has a valid pin)
    code2, out2, _ = run_pin_tool(unpinned_file, "--pin", "--force")
    assert code2 == 0
    hash2 = None
    for line in out2.split("\n"):
        if "Added PINNED:" in line:
            hash2 = line.split()[-1]
            break

    assert hash1 == hash2, "Idempotent runs should produce same hash"


def test_force_behavior(unpinned_file):
    """Without --force, refuse to overwrite valid header; with --force, allow."""
    # First pin
    code1, _, _ = run_pin_tool(unpinned_file, "--pin")
    assert code1 == 0

    # Second attempt without --force should fail
    code2, out2, err2 = run_pin_tool(unpinned_file, "--pin")
    assert code2 != 0, "Should refuse to overwrite without --force"
    assert "already has a valid PINNED:" in err2

    # With --force, should succeed
    code3, out3, _ = run_pin_tool(unpinned_file, "--pin", "--force")
    assert code3 == 0, "Should succeed with --force"
    assert "Added PINNED:" in out3


def test_check_mode(unpinned_file):
    """--check (default) reports hashes without writing."""
    # Add a pin first
    run_pin_tool(unpinned_file, "--pin")

    # Now --check should report existing and computed hashes
    code, out, _ = run_pin_tool(unpinned_file, "--check")
    assert code == 0
    assert "PINNED (existing):" in out
    assert "PINNED (computed):" in out
    assert "PINNED matches:" in out


def test_marker_ordering_preserved(unpinned_file):
    """DERIVED added after PINNED keeps PINNED header intact."""
    # Add PINNED
    code1, out1, _ = run_pin_tool(unpinned_file, "--pin")
    assert code1 == 0
    pin_hash = None
    for line in out1.split("\n"):
        if "Added PINNED:" in line:
            pin_hash = line.split()[-1]
            break

    # Add DERIVED
    code2, out2, _ = run_pin_tool(unpinned_file, "--derive", "--force")
    assert code2 == 0
    assert "Added DERIVED:" in out2

    # Verify PINNED header is still first and unchanged
    text = unpinned_file.read_text()
    lines = text.split("\n")
    assert lines[0].startswith(f"PINNED: {pin_hash}"), f"PINNED header corrupted: {lines[0]}"
    assert lines[1].startswith("DERIVED:"), "DERIVED should come after PINNED"

    # Verify hash still matches (backward compat)
    from pipeline.gate import _strip_header_lines, verify_pin_hash
    body = _strip_header_lines(text)
    recomputed = hashlib.sha256(body.encode("utf-8")).hexdigest()
    assert recomputed == pin_hash, "PINNED hash should still verify after DERIVED added"


def test_both_mode(unpinned_file):
    """--both generates PINNED and DERIVED in one run."""
    code, out, _ = run_pin_tool(unpinned_file, "--both")
    assert code == 0
    assert "Added PINNED:" in out
    assert "Added DERIVED:" in out

    text = unpinned_file.read_text()
    assert text.startswith("PINNED:")
    assert "DERIVED:" in text


def test_check_default_if_no_mode(unpinned_file):
    """With no mode flag, --check is default."""
    # Add a pin so --check has something to report
    run_pin_tool(unpinned_file, "--pin")

    # Run with no mode flag
    code, out, _ = run_pin_tool(unpinned_file)
    assert code == 0
    assert "PINNED (existing):" in out  # This is --check output


def test_file_not_found():
    """Graceful error if file doesn't exist."""
    code, _, err = run_pin_tool(Path("/nonexistent/PREDICTION.md"), "--check")
    assert code != 0
    assert "not found" in err.lower()
