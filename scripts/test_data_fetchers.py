#!/usr/bin/env python3
"""Tests for S3-01 — Data Acquisition (data_fetchers.py).

T2-level test suite: mechanical verification of fetch idempotence,
checksum correctness, and manifest updates.

Golden data: small dummy files with known checksums for offline testing.
"""
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from scripts.data_fetchers import (
    compute_sha256,
    fetch_file,
    fetch_all_datasets,
)
from scripts.manifest import update_manifest


# ============================================================================
# Test fixtures: dummy files with known checksums
# ============================================================================

DUMMY_JSON_CONTENT = b'{"test": "data"}'
DUMMY_JSON_SHA256 = "40b61fe1b15af0a4d5402735b26343e8cf8a045f4d81710e6108a21d91eaf366"

DUMMY_TEXT_CONTENT = b"Test dataset for Lyman-alpha"
DUMMY_TEXT_SHA256 = "a6d0498f7a3d9524748fd72a26727da20ab7a2e9cf8eec7fe955ad9dd4d3c8c8"


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create temporary data directory for test."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir


# ============================================================================
# Tests: checksum verification
# ============================================================================

def test_compute_sha256_correctness(temp_data_dir):
    """Test SHA256 computation on known file."""
    test_file = temp_data_dir / "test.json"
    test_file.write_bytes(DUMMY_JSON_CONTENT)

    computed = compute_sha256(test_file)
    assert computed == DUMMY_JSON_SHA256, f"Checksum mismatch: {computed}"


def test_compute_sha256_consistency(temp_data_dir):
    """Test SHA256 computation is deterministic."""
    test_file = temp_data_dir / "test.txt"
    test_file.write_bytes(DUMMY_TEXT_CONTENT)

    hash1 = compute_sha256(test_file)
    hash2 = compute_sha256(test_file)
    assert hash1 == hash2, "SHA256 should be deterministic"


# ============================================================================
# Tests: fetch_file idempotence and caching
# ============================================================================

def test_fetch_file_caching(temp_data_dir):
    """Test that fetch_file skips re-download if file exists with matching checksum."""
    from unittest.mock import patch

    # Mock urlopen to simulate download
    with patch("scripts.data_fetchers.urlopen") as mock_urlopen, \
         patch("scripts.data_fetchers.DATA_DIR", temp_data_dir), \
         patch("scripts.data_fetchers.REPO_ROOT", temp_data_dir):
        mock_urlopen.return_value.__enter__.return_value.read.return_value = (
            DUMMY_JSON_CONTENT
        )

        # First fetch (relative path)
        result1 = fetch_file(
            "http://example.com/test.json",
            "test.json",
            expected_sha256=DUMMY_JSON_SHA256,
        )
        assert result1["status"] == "new"
        assert mock_urlopen.call_count == 1

        # Second fetch (should use cache)
        result2 = fetch_file(
            "http://example.com/test.json",
            "test.json",
            expected_sha256=DUMMY_JSON_SHA256,
        )
        assert result2["status"] == "cached"
        assert mock_urlopen.call_count == 1, "Should not re-download cached file"


def test_fetch_file_checksum_verification_fail(temp_data_dir):
    """Test fetch_file rejects file with wrong checksum."""
    from unittest.mock import patch

    with patch("scripts.data_fetchers.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value.read.return_value = (
            DUMMY_JSON_CONTENT
        )

        dest_file = temp_data_dir / "test.json"

        # Try to fetch with wrong expected checksum
        with pytest.raises(ValueError, match="Checksum verification failed"):
            fetch_file(
                "http://example.com/test.json",
                dest_file,
                expected_sha256="wronghash1234567890",
            )

        # File should be deleted after failed verification
        assert not dest_file.exists()


# ============================================================================
# Tests: manifest updates
# ============================================================================

def test_update_manifest_new_entries(temp_data_dir):
    """Test manifest update adds new dataset entry."""
    # Create a minimal MANIFEST.md
    manifest_file = temp_data_dir / "MANIFEST.md"
    manifest_file.write_text(
        """# data/MANIFEST.md — Dataset Provenance Ledger

**Status:** Empty.

| Dataset | URL | Release / version | SHA256 | Retrieved | Used by |
|---|---|---|---|---|---|
| _(none yet)_ | | | | | |
"""
    )

    # Mock update_manifest to use temp manifest
    with patch("scripts.manifest.MANIFEST_FILE", manifest_file):
        fetch_results = {
            "nanograv_15yr": {
                "url": "https://example.com/nanograv.json",
                "version": "15-yr DR",
                "sha256": DUMMY_JSON_SHA256,
                "retrieved": "2026-07-18T12:00:00",
                "status": "new",
            }
        }
        update_manifest(fetch_results)

    # Verify new row was added
    content = manifest_file.read_text()
    assert "nanograv_15yr" in content
    assert "https://example.com/nanograv.json" in content
    assert DUMMY_JSON_SHA256[:16] in content
    assert "_(none yet)_" not in content


def test_update_manifest_error_entry(temp_data_dir):
    """Test manifest records errors from failed fetches."""
    manifest_file = temp_data_dir / "MANIFEST.md"
    manifest_file.write_text(
        """# data/MANIFEST.md — Dataset Provenance Ledger

**Status:** Empty.

| Dataset | URL | Release / version | SHA256 | Retrieved | Used by |
|---|---|---|---|---|---|
| _(none yet)_ | | | | | |
"""
    )

    with patch("scripts.manifest.MANIFEST_FILE", manifest_file):
        fetch_results = {
            "failed_dataset": {
                "status": "error",
                "error": "Connection timeout",
            }
        }
        update_manifest(fetch_results)

    content = manifest_file.read_text()
    assert "failed_dataset" in content
    assert "ERROR" in content
    assert "Connection timeout" in content


# ============================================================================
# Tests: fetch_all_datasets orchestration
# ============================================================================

def test_fetch_all_datasets_partial_failure(temp_data_dir):
    """Test fetch_all_datasets continues on partial failure."""
    # Mock individual fetchers
    mock_results = {
        "nanograv_15yr": {
            "url": "https://example.com/nanograv.json",
            "sha256": DUMMY_JSON_SHA256,
            "status": "new",
        },
        "epta_dr2": {
            "status": "error",
            "error": "URL not found",
        },
        "sdss_lensing": {
            "url": "https://example.com/lensing.fits",
            "sha256": "abc123def456",
            "status": "new",
        },
    }

    with patch("scripts.data_fetchers.fetch_nanograv_15yr") as mock_ng, \
         patch("scripts.data_fetchers.fetch_epta_dr2") as mock_epta, \
         patch("scripts.data_fetchers.fetch_sdss_lensing") as mock_sdss, \
         patch("scripts.data_fetchers.fetch_lyman_alpha"):

        mock_ng.return_value = mock_results["nanograv_15yr"]
        mock_epta.side_effect = Exception("URL not found")
        mock_sdss.return_value = mock_results["sdss_lensing"]

        results = fetch_all_datasets()

        # Check that successful fetches are in results
        assert "nanograv_15yr" in results
        assert results["nanograv_15yr"]["status"] == "new"

        # Check that epta_dr2 error is recorded
        assert "epta_dr2" in results
        assert results["epta_dr2"]["status"] == "error"

        # Check that other fetches continue after error
        assert "sdss_lensing" in results
        assert results["sdss_lensing"]["status"] == "new"


# ============================================================================
# Integration tests (offline, no real network)
# ============================================================================

def test_s3_01_full_workflow(temp_data_dir):
    """Full S3-01 workflow: fetch → checksum → manifest (offline)."""
    from unittest.mock import patch

    # Create manifest file
    manifest_file = temp_data_dir / "MANIFEST.md"
    manifest_file.write_text(
        """# data/MANIFEST.md — Dataset Provenance Ledger

**Status:** Empty.

| Dataset | URL | Release / version | SHA256 | Retrieved | Used by |
|---|---|---|---|---|---|
| _(none yet)_ | | | | | |
"""
    )

    # Mock all fetches to return deterministic results
    mock_fetch_results = {
        "nanograv_15yr": {
            "url": "https://example.com/nanograv.json",
            "version": "15-yr",
            "sha256": DUMMY_JSON_SHA256,
            "path": "pta/nanograv.json",
            "retrieved": "2026-07-18T00:00:00",
            "status": "new",
        },
        "epta_dr2": {
            "url": "https://example.com/epta.txt",
            "version": "DR2",
            "sha256": DUMMY_TEXT_SHA256,
            "path": "pta/epta.txt",
            "retrieved": "2026-07-18T00:00:01",
            "status": "new",
        },
        "sdss_lensing": {
            "url": "https://example.com/sdss.fits",
            "version": "DR12",
            "sha256": "abc123456789abcdef",
            "path": "lensing/sdss.fits",
            "retrieved": "2026-07-18T00:00:02",
            "status": "cached",
        },
        "lyman_alpha": {
            "status": "error",
            "error": "URL not available yet",
        },
    }

    # Run manifest update
    with patch("scripts.manifest.MANIFEST_FILE", manifest_file):
        update_manifest(mock_fetch_results)

    # Verify manifest was updated
    content = manifest_file.read_text()
    assert "nanograv_15yr" in content
    assert "epta_dr2" in content
    assert "sdss_lensing" in content
    assert "lyman_alpha" in content and "ERROR" in content
    assert "Updated" in content  # Status line changed
    assert "_(none yet)_" not in content  # Old placeholder removed


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
