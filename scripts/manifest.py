#!/usr/bin/env python3
"""MANIFEST.md updater — Record dataset provenance with checksums.

Each fetch updates data/MANIFEST.md with a new row. Never hand-edits entries;
corrections are new rows (record the change history, not overwrite).

Tracks: URL, version, SHA256, retrieval timestamp, use case.
"""
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_FILE = REPO_ROOT / "data" / "MANIFEST.md"

DATASET_USE_CASES = {
    "nanograv_15yr": "S3-03 (PTA observable P2)",
    "epta_dr2": "S3-03 (PTA observable P2, alternative)",
    "sdss_lensing": "S3-04 (lensing observable P1)",
    "lyman_alpha": "S3 null check (small-scale structure)",
    "sdss_cosmos": "engineering prep (G1-scope; no G1-L target pinned)",
    "sdss_stripe82_center": "engineering prep (G1-scope; no G1-L target pinned)",
    "sdss_coma_cluster": "engineering prep (G1-scope; no G1-L target pinned)",
    "sdss_docs_example": "engineering prep (G1-scope; no G1-L target pinned)",
    "euclid_edf_north": "engineering prep (G1-scope; no G1-L target pinned)",
    "euclid_edf_fornax": "engineering prep (G1-scope; no G1-L target pinned)",
    "euclid_edf_south": "engineering prep (G1-scope; no G1-L target pinned)",
}


def update_manifest(fetch_results: dict) -> None:
    """
    Update data/MANIFEST.md with fetched dataset entries.

    Args:
        fetch_results: Dict from data_fetchers.fetch_all_datasets()
                      e.g., {"nanograv_15yr": {...}, "epta_dr2": {...}, ...}
    """
    if not MANIFEST_FILE.exists():
        raise FileNotFoundError(f"MANIFEST.md not found at {MANIFEST_FILE}")

    # Read current manifest
    with open(MANIFEST_FILE, "r") as f:
        lines = f.readlines()

    # Find the data table (starts after header, between | markers)
    table_start = None
    table_end = None
    for i, line in enumerate(lines):
        if "| Dataset |" in line:
            table_start = i
        if table_start is not None and "| _(none yet)_" in line:
            table_end = i

    if table_start is None:
        raise ValueError("Could not find MANIFEST table header")

    # Build new rows
    new_rows = []
    for dataset_name, result in fetch_results.items():
        if result.get("status") == "error":
            new_rows.append(
                f"| {dataset_name} | ERROR | {result.get('error', 'unknown')} | | | |\n"
            )
            continue

        url = result.get("url", "")
        version = result.get("version", "")
        sha256 = result.get("sha256", "")[:16]  # Truncate for readability
        retrieved = result.get("retrieved", datetime.now().isoformat())
        use_case = DATASET_USE_CASES.get(dataset_name, "unknown")

        new_rows.append(
            f"| {dataset_name} | {url} | {version} | {sha256}... | {retrieved} | {use_case} |\n"
        )

    # Rebuild manifest: header + table rows + new rows
    if table_end is not None:
        # Replace the "_(none yet)_" row with new rows
        new_lines = lines[: table_end] + new_rows + lines[table_end + 1 :]
    else:
        # Append new rows at end of table
        new_lines = lines + new_rows

    # Update the "Status" note at top to reflect that data has been fetched.
    # The original "Empty" notice wraps across 3 markdown source lines (soft-wrap,
    # one logical sentence) — replace all 3 or a dangling fragment survives (found
    # 2026-07-25: "has not opened..." left orphaned after only line 1 was swapped).
    start = None
    for i, line in enumerate(new_lines):
        if "**Status:** Empty." in line:
            start = i
            break
    if start is not None:
        end = start + 1
        while end < len(new_lines) and new_lines[end].strip() and not new_lines[end].startswith("|"):
            end += 1
        new_lines[start:end] = [
            f"**Status:** Updated {datetime.now().isoformat()}. "
            f"{len(fetch_results)} dataset(s) fetched.\n"
        ]

    # Write updated manifest
    with open(MANIFEST_FILE, "w") as f:
        f.writelines(new_lines)

    print(f"Updated {MANIFEST_FILE}")


if __name__ == "__main__":
    # Test: dummy fetch results
    test_results = {
        "nanograv_15yr": {
            "url": "https://example.com/nanograv.json",
            "version": "15-yr DR",
            "sha256": "abc123" * 10,  # 60 chars
            "retrieved": datetime.now().isoformat(),
        }
    }
    update_manifest(test_results)
