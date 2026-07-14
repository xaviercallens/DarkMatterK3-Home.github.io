#!/usr/bin/env python3
"""
v5_provenance_gate.py
=====================

WP-C1: Provenance gate harness (test suite)

This module ensures that synthetic fallback data can NEVER be written to a
discoveries file. This prevents the finding F5 (synthetic data injection)
from ever recurring.
"""

import json
import tempfile
from pathlib import Path


def test_synthetic_cannot_be_persisted():
    """
    Unit test: attempting to persist a synthetic-provenance record
    as a discovery must raise RuntimeError.
    """
    print("=" * 70)
    print("WP-C1: Provenance Gate Test")
    print("=" * 70)

    # Mock discovery with synthetic provenance
    bad_discovery = {
        "sector_id": 0,
        "type": "MODERATE_SIGNAL",
        "delta_s10": 0.15,
        "data_provenance": "synthetic_fallback",  # THE PROBLEM
        "timestamp": "2026-07-14T00:00:00",
    }

    # Mock good discovery with real provenance
    good_discovery = {
        "sector_id": 1,
        "type": "MODERATE_SIGNAL",
        "delta_s10": 0.18,
        "data_provenance": "real_survey",  # OK
        "timestamp": "2026-07-14T00:00:01",
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        out_file = Path(tmpdir) / "test_discoveries.json"

        # Try to write bad discovery
        print("\n[TEST 1] Attempt to write synthetic-provenance discovery...")
        try:
            persist_discovery(bad_discovery, out_file)
            print("  FAILED: no exception was raised")
            assert False, "synthetic discovery should have been blocked"
        except RuntimeError as e:
            if "synthetic_fallback" in str(e):
                print(f"  PASSED: {e}")
            else:
                raise

        # Write good discovery
        print("\n[TEST 2] Write real-survey-provenance discovery...")
        persist_discovery(good_discovery, out_file)
        with open(out_file) as f:
            data = json.load(f)
        assert data["discoveries"][0]["data_provenance"] == "real_survey"
        print(f"  PASSED: real discovery persisted")

        # Verify file contents
        print("\n[TEST 3] Verify no synthetic records in file...")
        with open(out_file) as f:
            all_discoveries = json.load(f)["discoveries"]
        synth_count = sum(
            1 for d in all_discoveries
            if d.get("data_provenance") == "synthetic_fallback"
        )
        assert synth_count == 0, f"found {synth_count} synthetic records in file"
        print(f"  PASSED: file is clean ({len(all_discoveries)} real discoveries)")

    print("\n" + "=" * 70)
    print("ALL PROVENANCE GATE TESTS PASSED")
    print("=" * 70)


def persist_discovery(discovery, filepath):
    """
    Persist a single discovery record to a discoveries JSON file.

    GATE: raises RuntimeError if data_provenance is synthetic_fallback.
    """
    provenance = discovery.get("data_provenance", "unknown")

    if provenance == "synthetic_fallback":
        raise RuntimeError(
            f"BLOCKED: discovery from synthetic_fallback cannot be persisted. "
            f"Provenance gate active. (sector {discovery.get('sector_id')})"
        )

    if provenance != "real_survey":
        raise RuntimeError(
            f"BLOCKED: unknown provenance '{provenance}'. "
            f"Must be 'real_survey' or 'synthetic_fallback' (gated)."
        )

    # Load existing discoveries
    filepath = Path(filepath)
    if filepath.exists():
        with open(filepath) as f:
            data = json.load(f)
    else:
        data = {"discoveries": []}

    # Append and save
    data["discoveries"].append(discovery)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    test_synthetic_cannot_be_persisted()
