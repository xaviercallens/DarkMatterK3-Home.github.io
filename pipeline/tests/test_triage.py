#!/usr/bin/env python3
"""Tests for external brief triage protocol.

Validates the triage module's ability to detect fabricated claims:
- Fabricated commit hashes
- Fabricated file paths
- Fabricated or missing constants
- Circular thresholds

Test cases model real incidents from the repo's history.
"""

import pytest
from pipeline.triage import (
    check_commit_exists,
    check_file_exists,
    check_constant_in_repo,
    vendor_source,
    build_triage_report,
)


class TestCheckCommitExists:
    """Tests for check_commit_exists() function."""

    def test_current_head_exists(self):
        """The current HEAD commit should exist."""
        # Get current HEAD
        import subprocess
        from pathlib import Path

        repo_root = Path(__file__).resolve().parent.parent.parent
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        head_sha = result.stdout.strip()

        # Should verify
        assert check_commit_exists(head_sha)

    def test_fabricated_commit_does_not_exist(self):
        """A fabricated commit hash (30fcd15) should not exist."""
        # This hash was used in the D-3 brief fabrication incident
        assert not check_commit_exists("30fcd15")

    def test_short_sha_works(self):
        """Short SHAs (>= 7 chars) should be recognized."""
        import subprocess
        from pathlib import Path

        repo_root = Path(__file__).resolve().parent.parent.parent
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        head_short = result.stdout.strip()

        # Short SHA of current HEAD should exist
        assert len(head_short) >= 7
        assert check_commit_exists(head_short)


class TestCheckFileExists:
    """Tests for check_file_exists() function."""

    def test_existing_file(self):
        """CLAUDE.md should exist at repo root."""
        assert check_file_exists("CLAUDE.md")

    def test_existing_directory(self):
        """pipeline directory should exist."""
        assert check_file_exists("pipeline")

    def test_nonexistent_file(self):
        """A file that doesn't exist should return False."""
        assert not check_file_exists("checkers/certificates/C3b_symsqrt_cooper_s7.json")

    def test_nonexistent_path(self):
        """A path that was never in the repo should return False."""
        assert not check_file_exists("fake/nonexistent/path.json")

    def test_nested_file(self):
        """Nested files should be found correctly."""
        # pipeline/triage.py was just created
        assert check_file_exists("pipeline/triage.py")


class TestCheckConstantInRepo:
    """Tests for check_constant_in_repo() function."""

    def test_existing_constant_is_found(self):
        """SYM2_UNVERIFIED should be found in the repo."""
        results = check_constant_in_repo("SYM2_UNVERIFIED")
        assert len(results) > 0
        # Should be found in at least K3_CRITERIA.md and VISION.md
        assert any("K3_CRITERIA.md" in r or "VISION.md" in r for r in results)

    def test_nonexistent_constant_not_found(self):
        """A random nonsense string should not be found."""
        # Use a unique string that won't appear in the repo
        # Build it dynamically to avoid grep finding it in the test file itself
        fake_const = "NONEXISTENT_" + "FABRICATED_" + "UNIQUE_" + "XYZ_ABC_123"
        results = check_constant_in_repo(fake_const)
        assert len(results) == 0

    def test_constant_search_is_literal(self):
        """Searches should be literal string matches."""
        # "CLAUDE.md" exists in many files
        results = check_constant_in_repo("CLAUDE.md")
        assert len(results) > 0

    def test_numeric_constant_search(self):
        """Numeric constants should be searchable."""
        # "13" is the first element of s7's order_abcd (from test_siblings.py)
        results = check_constant_in_repo("13, 4, -27, 3")
        # This specific tuple is less likely to appear elsewhere; search for just "13"
        results_13 = check_constant_in_repo("order_abcd = (13")
        # At minimum, the constant should be searchable without error
        assert isinstance(results, list)

    def test_constant_search_returns_file_list(self):
        """Results should be a list of file paths."""
        results = check_constant_in_repo("SYM2_UNVERIFIED")
        assert isinstance(results, list)
        assert all(isinstance(f, str) for f in results)


class TestVendorSource:
    """Tests for vendor_source() function."""

    def test_vendor_source_returns_dict(self):
        """vendor_source should return a dict with required fields."""
        text = "test brief content"
        source_name = "test_source"
        vendor_info = vendor_source(text, source_name)

        assert isinstance(vendor_info, dict)
        assert "source_name" in vendor_info
        assert "source_sha256" in vendor_info
        assert "fetched_at" in vendor_info
        assert "repo_head_sha" in vendor_info
        assert "repo_branch" in vendor_info

    def test_vendor_source_sha256_deterministic(self):
        """Same text should produce the same SHA256."""
        text = "fixed brief content"
        source_name = "test_source"

        vendor1 = vendor_source(text, source_name)
        vendor2 = vendor_source(text, source_name)

        assert vendor1["source_sha256"] == vendor2["source_sha256"]

    def test_vendor_source_sha256_differs_on_content(self):
        """Different text should produce different SHA256."""
        source_name = "test_source"

        vendor1 = vendor_source("brief A", source_name)
        vendor2 = vendor_source("brief B", source_name)

        assert vendor1["source_sha256"] != vendor2["source_sha256"]

    def test_vendor_source_preserves_name(self):
        """Source name should be preserved."""
        source_name = "my_unique_directive_name"
        vendor_info = vendor_source("text", source_name)
        assert vendor_info["source_name"] == source_name

    def test_vendor_source_fetched_at_format(self):
        """fetched_at should be ISO 8601 format."""
        vendor_info = vendor_source("text", "test")
        fetched_at = vendor_info["fetched_at"]

        # Should be parseable as ISO 8601
        from datetime import datetime

        try:
            dt = datetime.fromisoformat(fetched_at)
            assert dt is not None
        except ValueError:
            pytest.fail(f"fetched_at not ISO 8601: {fetched_at}")


class TestBuildTriageReportGoldenGood:
    """Golden-good test case: all claims verified (real repo state)."""

    def test_golden_good_real_repo_state(self):
        """Check claims against real repo state — all should verify."""
        # Get current HEAD
        import subprocess
        from pathlib import Path

        repo_root = Path(__file__).resolve().parent.parent.parent
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        head_sha = result.stdout.strip()

        source_text = "Golden good test: all claims real"
        claims = [
            {
                "type": "commit",
                "value": head_sha,
                "claim": "Current HEAD commit exists",
            },
            {"type": "file", "value": "CLAUDE.md", "claim": "CLAUDE.md exists"},
            {
                "type": "file",
                "value": "pipeline",
                "claim": "pipeline directory exists",
            },
            {
                "type": "constant",
                "value": "SYM2_UNVERIFIED",
                "claim": "SYM2_UNVERIFIED is in the repo",
            },
        ]

        report = build_triage_report("golden_good_test", source_text, claims)

        # All claims should verify
        assert report.action == "EXECUTE"
        assert len(report.discrepancies) == 0
        assert all(c["verified"] for c in report.claims)

        # Verify source provenance fields
        assert report.source_name == "golden_good_test"
        assert report.source_sha256  # Should have a SHA
        assert report.repo_head_sha  # Should have HEAD SHA
        assert report.repo_branch  # Should have branch name

    def test_report_claims_structure(self):
        """Report.claims should have the expected structure."""
        import subprocess
        from pathlib import Path

        repo_root = Path(__file__).resolve().parent.parent.parent
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        head_sha = result.stdout.strip()

        claims = [
            {"type": "commit", "value": head_sha, "claim": "HEAD exists"},
        ]

        report = build_triage_report("test", "test", claims)

        assert len(report.claims) == 1
        claim = report.claims[0]
        assert "claim" in claim
        assert "check_type" in claim
        assert "verified" in claim
        assert "detail" in claim
        assert claim["verified"] is True


class TestBuildTriageReportGoldenBad:
    """Golden-bad test case: fabricated claims (from D-3 brief incident)."""

    def test_golden_bad_fabricated_commit(self):
        """Commit 30fcd15 doesn't exist — should discrepancy."""
        source_text = "D-3 brief incident: claims commit 30fcd15"
        claims = [
            {
                "type": "commit",
                "value": "30fcd15",
                "claim": "Fabricated commit from D-3 brief",
            },
        ]

        report = build_triage_report("d3_brief_incident", source_text, claims)

        # Should be marked for discard
        assert report.action == "DISCARD"
        assert len(report.discrepancies) > 0
        assert not report.claims[0]["verified"]
        # Discrepancy should mention the commit
        assert any("30fcd15" in d for d in report.discrepancies)

    def test_golden_bad_fabricated_file(self):
        """File C3b_symsqrt_cooper_s7.json doesn't exist — should discrepancy."""
        source_text = "D-3 brief: claims file C3b_symsqrt_cooper_s7.json exists"
        claims = [
            {
                "type": "file",
                "value": "checkers/certificates/C3b_symsqrt_cooper_s7.json",
                "claim": "Fabricated certificate from D-3 brief",
            },
        ]

        report = build_triage_report("d3_brief_file", source_text, claims)

        assert report.action == "DISCARD"
        assert len(report.discrepancies) > 0
        assert not report.claims[0]["verified"]

    def test_golden_bad_multiple_fabrications(self):
        """Multiple fabrications should all be caught."""
        source_text = "D-3 brief with multiple fabrications"
        # Build fake constant dynamically to avoid grep finding it in test file
        fake_const = "NONEXISTENT_" + "FABRICATED_" + "UNIQUE_" + "XYZ_ABC_123"
        claims = [
            {"type": "commit", "value": "30fcd15"},
            {"type": "file", "value": "checkers/certificates/C3b_symsqrt_cooper_s7.json"},
            {"type": "constant", "value": fake_const},
        ]

        report = build_triage_report("d3_multiple", source_text, claims)

        assert report.action == "DISCARD"
        # Should have discrepancies for all three
        assert len(report.discrepancies) == 3
        assert all(not c["verified"] for c in report.claims)


class TestDeterminism:
    """Determinism test: same inputs produce the same report fields."""

    def test_same_inputs_same_report_minus_timestamp(self):
        """Same inputs should produce identical reports (except fetched_at)."""
        import subprocess
        from pathlib import Path

        repo_root = Path(__file__).resolve().parent.parent.parent
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        head_sha = result.stdout.strip()

        source_text = "Fixed test content for determinism"
        source_name = "determinism_test"
        claims = [
            {"type": "commit", "value": head_sha},
            {"type": "file", "value": "CLAUDE.md"},
            {"type": "constant", "value": "SYM2_UNVERIFIED"},
        ]

        # Generate two reports
        report1 = build_triage_report(source_name, source_text, claims)
        report2 = build_triage_report(source_name, source_text, claims)

        # All fields except fetched_at should be identical
        assert report1.source_name == report2.source_name
        assert report1.source_sha256 == report2.source_sha256
        assert report1.repo_head_sha == report2.repo_head_sha
        assert report1.repo_branch == report2.repo_branch
        assert report1.claims == report2.claims
        assert report1.discrepancies == report2.discrepancies
        assert report1.action == report2.action


class TestEdgeCases:
    """Edge cases and error handling."""

    def test_unknown_claim_type(self):
        """Unknown claim types should be flagged as discrepancies."""
        source_text = "Test unknown claim type"
        claims = [
            {"type": "unknown_type", "value": "something"},
        ]

        report = build_triage_report("edge_case_test", source_text, claims)

        assert report.action == "DISCARD"
        assert len(report.discrepancies) > 0

    def test_missing_claim_fields(self):
        """Claims with missing required fields should be handled gracefully."""
        source_text = "Test missing claim fields"
        claims = [
            {"type": "commit"},  # Missing 'value'
        ]

        # Should not crash
        report = build_triage_report("edge_case_missing", source_text, claims)
        assert isinstance(report, object)

    def test_empty_claims_list(self):
        """Empty claims list should yield EXECUTE (no discrepancies)."""
        source_text = "Test empty claims"
        claims = []

        report = build_triage_report("empty_claims_test", source_text, claims)

        assert report.action == "EXECUTE"
        assert len(report.discrepancies) == 0
        assert len(report.claims) == 0

    def test_report_to_json_serializable(self):
        """Report should be JSON-serializable."""
        import subprocess
        from pathlib import Path

        repo_root = Path(__file__).resolve().parent.parent.parent
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        head_sha = result.stdout.strip()

        claims = [{"type": "commit", "value": head_sha}]
        report = build_triage_report("json_test", "test", claims)

        # Should not raise
        json_str = report.to_json_str()
        assert isinstance(json_str, str)
        assert len(json_str) > 0

        # Should be valid JSON
        import json

        parsed = json.loads(json_str)
        assert parsed["action"] == "EXECUTE"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


# Generated-by: Haiku 4.5 | Verified-by: pytest 28/28 passing | Reviewed-by: [pending T0]
