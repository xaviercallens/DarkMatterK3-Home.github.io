#!/usr/bin/env python3
"""External brief triage protocol — mechanical validation against repo state.

This module provides a formal, reusable protocol for vetting external briefs,
directives, and pull-request claims before they are acted upon. The repo has
been hit 3 times by fabricated briefs containing:
- Fabricated commit hashes
- Fabricated file paths
- Fabricated constants (cited to non-existent papers or misquoted values)
- Circular thresholds (bounds numerically equal to measured resolution, cited elsewhere)

Each time, fabrication was caught ad hoc by manual `git log`, `ls`, and `grep` calls.
This module automates the process via mechanical checks against the live repo state.

Usage:
    source_text = "<pasted brief text>"
    claims = [
        {"type": "commit", "value": "30fcd15"},
        {"type": "file", "value": "checkers/certificates/C3b_x.json"},
        {"type": "constant", "value": "1.21145"},
    ]
    report = build_triage_report("external_directive_2026_07_25", source_text, claims)

    if report.action == "DISCARD":
        print(f"Fabrication detected: {report.discrepancies}")
    elif report.action == "EXECUTE":
        print("All claims verified; safe to execute")
"""

import hashlib
import json
import subprocess
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal


def _get_repo_root() -> Path:
    """Get the repository root directory.

    Uses the same convention as pipeline/siblings.py:
    parent of the directory containing this file.

    Returns
    -------
    Path
        Absolute path to repo root.
    """
    return Path(__file__).resolve().parent.parent


def check_commit_exists(commit_sha: str) -> bool:
    """Check if a commit exists in the repo's history.

    Uses `git cat-file -e <sha>` which returns 0 if the object exists,
    nonzero otherwise.

    Parameters
    ----------
    commit_sha : str
        Commit SHA (any length >= 7).

    Returns
    -------
    bool
        True if commit exists, False otherwise.
    """
    if not commit_sha:
        return False

    repo_root = _get_repo_root()
    try:
        subprocess.run(
            ["git", "cat-file", "-e", commit_sha],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except (subprocess.CalledProcessError, TypeError):
        return False


def check_file_exists(path: str) -> bool:
    """Check if a file or directory exists relative to repo root.

    Parameters
    ----------
    path : str
        Path relative to repo root (e.g. "CLAUDE.md", "checkers/certificates/C1.json").

    Returns
    -------
    bool
        True if file/directory exists, False otherwise.
    """
    repo_root = _get_repo_root()
    full_path = repo_root / path
    return full_path.exists()


def check_constant_in_repo(value_str: str, search_root: str = ".") -> list:
    """Grep the repo for a literal string (constant, identifier, etc.).

    Parameters
    ----------
    value_str : str
        String to search for (e.g. "1.21145", "SYM2_UNVERIFIED").
    search_root : str
        Directory to search from, relative to repo root. Default ".".

    Returns
    -------
    list[str]
        List of file paths (relative to repo root) where value_str is found.
        Empty list if not found anywhere (red flag for a "cited" constant).
    """
    if not value_str:
        return []

    repo_root = _get_repo_root()
    search_path = repo_root / search_root

    if not search_path.exists():
        return []

    try:
        result = subprocess.run(
            ["grep", "-r", value_str, str(search_path)],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and result.stdout:
            # Parse output: each line is "path:content"
            lines = result.stdout.strip().split("\n")
            files = set()
            for line in lines:
                if ":" in line:
                    file_path = line.split(":")[0]
                    # Make relative to repo root
                    try:
                        rel_path = Path(file_path).relative_to(repo_root)
                        files.add(str(rel_path))
                    except ValueError:
                        # Already relative or outside repo, use as-is
                        files.add(file_path)
            return sorted(list(files))
        else:
            return []
    except Exception:
        # If grep fails, return empty (safe default for triage)
        return []


@dataclass
class TriageReport:
    """Report on external brief validation.

    Fields
    ------
    source_name : str
        Name/label of the source (e.g. "external_directive_2026_07_25").
    fetched_at : str
        ISO 8601 timestamp of when the report was generated.
    source_sha256 : str
        SHA256 hash of the source text.
    repo_head_sha : str
        Short SHA of the current git HEAD.
    repo_branch : str
        Current git branch name.
    claims : list[dict]
        List of claims checked; each dict has fields:
        {"claim": str, "check_type": str, "verified": bool, "detail": str}
    discrepancies : list[str]
        List of discrepancy descriptions (one per unverified claim).
    action : Literal["EXECUTE", "DISCARD", "CONDITIONAL"]
        Recommended action: "EXECUTE" (all claims verified), "DISCARD" (any
        discrepancy), or "CONDITIONAL" (set manually by the caller).
    """

    source_name: str
    fetched_at: str
    source_sha256: str
    repo_head_sha: str
    repo_branch: str
    claims: list = field(default_factory=list)
    discrepancies: list = field(default_factory=list)
    action: Literal["EXECUTE", "DISCARD", "CONDITIONAL"] = "EXECUTE"

    def to_dict(self) -> dict:
        """Convert report to a JSON-serializable dictionary."""
        return asdict(self)

    def to_json_str(self) -> str:
        """Serialize report to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


def vendor_source(text: str, source_name: str) -> dict:
    """Compute provenance metadata for an external source.

    Parameters
    ----------
    text : str
        The source text (brief, directive, etc.).
    source_name : str
        Label for the source (e.g. "external_brief_2026_07_25").

    Returns
    -------
    dict
        Dictionary with fields:
        - source_name: str (passed in)
        - source_sha256: str (SHA256 of text)
        - fetched_at: str (ISO 8601 timestamp, UTC)
        - repo_head_sha: str (short SHA of HEAD, 7 chars)
        - repo_branch: str (current branch name)
    """
    repo_root = _get_repo_root()

    # Compute source SHA256
    source_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()

    # Get repo HEAD short SHA
    try:
        head_sha_result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        head_sha = head_sha_result.stdout.strip()
    except subprocess.CalledProcessError:
        head_sha = "UNKNOWN"

    # Get repo branch
    try:
        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        branch = branch_result.stdout.strip()
    except subprocess.CalledProcessError:
        branch = "UNKNOWN"

    # Get ISO 8601 timestamp (UTC)
    fetched_at = datetime.now(timezone.utc).isoformat()

    return {
        "source_name": source_name,
        "source_sha256": source_sha,
        "fetched_at": fetched_at,
        "repo_head_sha": head_sha,
        "repo_branch": branch,
    }


def build_triage_report(
    source_name: str, source_text: str, claims: list
) -> TriageReport:
    """Build a triage report from external brief claims.

    Orchestrates:
    1. Vendors the source (computes SHA256, HEAD SHA, branch, timestamp)
    2. For each claim, runs the appropriate check (commit, file, constant)
    3. Collects discrepancies (any claim with verified=False)
    4. Sets action: "EXECUTE" if all verified, "DISCARD" if any discrepancy

    Parameters
    ----------
    source_name : str
        Name/label of the source.
    source_text : str
        The source text (brief, directive, etc.).
    claims : list[dict]
        List of claims to check. Each dict must have:
        - "type": one of "commit", "file", "constant"
        - "value": the value to check (commit SHA, file path, or string to grep)

        Optional field:
        - "claim": human-readable description (used for reporting)

    Returns
    -------
    TriageReport
        Complete report with all checks performed, action recommendation.
    """
    # Vendor the source
    vendor_info = vendor_source(source_text, source_name)

    # Check each claim
    checked_claims = []
    discrepancies = []

    for claim_dict in claims:
        claim_type = claim_dict.get("type")
        value = claim_dict.get("value")
        claim_text = claim_dict.get("claim", f"{claim_type}:{value}")

        verified = False
        detail = ""

        if claim_type == "commit":
            verified = check_commit_exists(value)
            if not verified:
                detail = f"Commit {value} does not exist in repo history"
                discrepancies.append(detail)
            else:
                detail = f"Commit {value} verified in repo history"

        elif claim_type == "file":
            verified = check_file_exists(value)
            if not verified:
                detail = f"File {value} does not exist in repo"
                discrepancies.append(detail)
            else:
                detail = f"File {value} exists in repo"

        elif claim_type == "constant":
            found_in_files = check_constant_in_repo(value)
            verified = len(found_in_files) > 0
            if not verified:
                detail = f"Constant '{value}' not found anywhere in repo"
                discrepancies.append(detail)
            else:
                detail = f"Constant '{value}' found in {len(found_in_files)} file(s)"

        else:
            detail = f"Unknown claim type: {claim_type}"
            discrepancies.append(detail)

        checked_claims.append(
            {
                "claim": claim_text,
                "check_type": claim_type,
                "verified": verified,
                "detail": detail,
            }
        )

    # Determine action
    action = "EXECUTE" if len(discrepancies) == 0 else "DISCARD"

    return TriageReport(
        source_name=vendor_info["source_name"],
        fetched_at=vendor_info["fetched_at"],
        source_sha256=vendor_info["source_sha256"],
        repo_head_sha=vendor_info["repo_head_sha"],
        repo_branch=vendor_info["repo_branch"],
        claims=checked_claims,
        discrepancies=discrepancies,
        action=action,
    )


# Generated-by: Haiku 4.5 | Verified-by: tests/test_triage.py | Reviewed-by: [pending T0]
