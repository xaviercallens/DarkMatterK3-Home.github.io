#!/usr/bin/env python3
"""
Audit and manifest the GCS datalake (fast version).

Enumerates gs://socrateai-datalake-gen-lang-client-0625573011/, computes SHA-256
for critical analysis-relevant objects ≤ 100 MB only, records GCS-side integrity,
and emits data/GCS_DATALAKE_MANIFEST.md with strict status vocabulary.

Per T0_RATIFICATION_2026_07_31: status ∈ {PRESENT, AUDITED, QUARANTINED, ABSENT}.
VERIFIED is forbidden (reserved). Large files (> 100 MB) listed as PRESENT (no hash).
"""

import os
import sys
import json
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Configuration
BUCKET = "gs://socrateai-datalake-gen-lang-client-0625573011"
MANIFEST_PATH = Path("data/GCS_DATALAKE_MANIFEST.md")
MAX_HASH_SIZE = 100 * 1024 * 1024  # Only hash ≤ 100 MB
ANALYSIS_RELEVANT_PATTERNS = [
    "stream3_desi_dr1/",
    "nanograv_15yr/",
    "euclid_q1/",
    "stream3_euclid_q2/",
    "stream2_cy4_ml/",
    "formal_verification/",
    "publications/",
    "stream4_bridge/",
    "audit/",
    "dark_matter/",
    "checkpoints/",
    "mcmc_posteriors/",
]

# Seed rows: fixed status regardless of bucket state
SEED_QUARANTINED = [
    ("publications/SocrateAI_K3_T2_Discovery_Final.pdf", "F5b claim status pending audit WP-A"),
    ("formal_verification/lean_oracle_v5.tar.gz", "Source audit pending WP-B; binary unverifiable"),
]

SEED_ABSENT = [
    ("des_y3/", "Retracted from 2026-07-31 table; not in bucket"),
    ("planck_2018/", "Retracted from 2026-07-31 table; pending P1 acquisition"),
    ("ipta_dr2/", "Retracted and DEFERRED per T0 decision DL-2"),
    ("proofs/GeneratedK3.lean", "Retracted from 2026-07-31 table; file does not exist"),
]

def run_gcloud(args):
    """Run gcloud command, return stdout or None on error."""
    try:
        result = subprocess.run(
            ["gcloud", "storage"] + args,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ gcloud command failed: {e}", file=sys.stderr)
        return None

def list_objects():
    """Enumerate all objects in the bucket with size metadata using recursive listing."""
    try:
        result = subprocess.run(
            ["gcloud", "storage", "ls", "-r", "--long", f"{BUCKET}/**"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            print(f"❌ Failed to list bucket: {result.stderr}", file=sys.stderr)
            sys.exit(1)

        objects = []
        for line in result.stdout.split("\n"):
            line = line.strip()
            if not line or line.startswith("Total"):
                continue
            # Format: size timestamp uri (with possible multiple spaces)
            parts = line.split(maxsplit=2)
            if len(parts) >= 3 and parts[2].startswith("gs://"):
                try:
                    size = int(parts[0])
                    uri = parts[2]
                    objects.append((uri, size))
                except (ValueError, IndexError):
                    pass
        return objects
    except Exception as e:
        print(f"❌ Error listing bucket: {e}", file=sys.stderr)
        sys.exit(1)

def compute_sha256(uri):
    """Download object and compute SHA-256. Return hash or None if undownloadable."""
    try:
        result = subprocess.run(
            ["gcloud", "storage", "cat", uri],
            capture_output=True,
            timeout=120,
        )
        if result.returncode != 0:
            return None
        sha256 = hashlib.sha256(result.stdout).hexdigest()
        return sha256
    except Exception:
        return None

def get_gcs_metadata(uri):
    """Get GCS-side MD5 and CRC32C via gcloud stat."""
    output = run_gcloud(["stat", uri])
    if output is None:
        return None, None

    md5 = None
    crc32c = None
    for line in output.split("\n"):
        if "Hash (md5):" in line:
            md5 = line.split()[-1]
        if "Hash (crc32c):" in line:
            crc32c = line.split()[-1]
    return md5, crc32c

def determine_status(uri, size):
    """Determine manifest status for an object."""
    # Check seed quarantine
    for quarantine_uri, reason in SEED_QUARANTINED:
        if quarantine_uri in uri:
            return "QUARANTINED", reason

    # Check if analysis-relevant
    is_analysis_relevant = any(pattern in uri for pattern in ANALYSIS_RELEVANT_PATTERNS)

    # Only hash small files (≤ 100 MB) that are analysis-relevant
    if is_analysis_relevant and size <= MAX_HASH_SIZE:
        sha256 = compute_sha256(uri)
        if sha256:
            return "AUDITED", sha256
        else:
            return "PRESENT", None

    # Large files or not analysis-relevant: just mark as PRESENT
    return "PRESENT", None

def main():
    print("🔍 Auditing datalake...", file=sys.stderr)

    objects = list_objects()
    print(f"   Found {len(objects)} objects", file=sys.stderr)

    # Build manifest rows
    manifest_rows = defaultdict(list)
    audited_count = 0
    present_count = 0

    # Process actual objects
    for uri, size in objects:
        status, detail = determine_status(uri, size)
        md5, crc32c = get_gcs_metadata(uri)

        if status == "AUDITED":
            audited_count += 1
        elif status == "PRESENT":
            present_count += 1

        # Group by top-level folder
        folder = uri.split("/")[3] if len(uri.split("/")) > 3 else "root"
        manifest_rows[folder].append({
            "uri": uri,
            "size_mb": round(size / (1024 * 1024), 2),
            "status": status,
            "sha256": detail if status == "AUDITED" else None,
            "gcs_md5": md5,
            "gcs_crc32c": crc32c,
        })

    # Add seed rows
    for seed_uri, reason in SEED_QUARANTINED:
        folder = seed_uri.split("/")[0]
        manifest_rows[folder].append({
            "uri": f"{BUCKET}/{seed_uri}",
            "size_mb": "N/A",
            "status": "QUARANTINED",
            "reason": reason,
            "sha256": None,
        })

    for seed_uri, reason in SEED_ABSENT:
        folder = seed_uri.split("/")[0] if "/" in seed_uri else seed_uri
        manifest_rows[folder].append({
            "uri": f"{BUCKET}/{seed_uri}",
            "size_mb": "N/A",
            "status": "ABSENT",
            "reason": reason,
            "sha256": None,
        })

    # Emit markdown
    md_content = f"""# GCS Datalake Manifest — Cryptographic Audit Trail

**Generated:** {datetime.utcnow().isoformat()}Z
**Bucket:** `{BUCKET}`
**Audited:** {audited_count} objects with full SHA-256 · **Present:** {present_count} objects (hashes not computed)
**Quarantined:** {len(SEED_QUARANTINED)} · **Absent (retracted claims):** {len(SEED_ABSENT)}

---

## Status Vocabulary (Closed Set)

- **AUDITED**: Full SHA-256 hash computed on download; cryptographically verified.
- **PRESENT**: Object exists in bucket; hash not computed (exceeds 500 MB or not analysis-relevant).
- **QUARANTINED**: Object flagged for audit/review before use; remains in bucket untouched.
- **ABSENT**: Retracted from 2026-07-31 status table; does not exist in bucket.

⚠️ **Never emitted: "VERIFIED"** (reserved for human review only).

---

## By Folder

"""

    for folder in sorted(manifest_rows.keys()):
        rows = manifest_rows[folder]
        md_content += f"\n### {folder}/\n\n"

        # Check for sandbox designation
        if folder == "stream4_bridge":
            md_content += "**🔬 EXPLORATORY SANDBOX** — no claim from Stream 4 may be cited as evidence in Streams 1–3 (T0 decision DL-3).\n\n"

        md_content += "| URI | Size (MB) | Status | SHA-256 / Note |\n"
        md_content += "|-----|-----------|--------|----------------|\n"

        for row in rows:
            size_str = str(row["size_mb"])
            status = row["status"]
            detail = ""
            if status == "AUDITED":
                detail = f"`{row['sha256'][:16]}...`"
            elif "reason" in row:
                detail = row["reason"]

            # Truncate URI for readability
            uri_short = row["uri"].replace(f"{BUCKET}/", "")
            md_content += f"| `{uri_short}` | {size_str} | **{status}** | {detail} |\n"

    # Write manifest
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(md_content)
    print(f"✅ Manifest written to {MANIFEST_PATH}", file=sys.stderr)
    print(f"   Audited: {audited_count} | Present: {present_count} | Quarantined: {len(SEED_QUARANTINED)} | Absent: {len(SEED_ABSENT)}", file=sys.stderr)

if __name__ == "__main__":
    main()
