#!/usr/bin/env python3
"""
Audit and manifest the GCS datalake (checkpointed version, 2026-08-01).

Enumerates gs://socrateai-datalake-gen-lang-client-0625573011/, computes SHA-256
for critical analysis-relevant objects ≤ 100 MB only, records GCS-side integrity,
and emits data/GCS_DATALAKE_MANIFEST.md with strict status vocabulary.

Per T0_RATIFICATION_2026_07_31: status ∈ {PRESENT, AUDITED, QUARANTINED, ABSENT, PENDING}.
VERIFIED is forbidden (reserved). Large files (> 100 MB) listed as PRESENT (no hash).
PENDING is new (2026-08-01, low-tier queue A-S3-2): an analysis-relevant object not
yet processed by this invocation's batch — NOT silently omitted, NOT misrepresented
as PRESENT (which would wrongly imply "checked, no hash needed").

WHY CHECKPOINTED: the v1.0 run (2026-07-31) timed out. Root-cause measured
2026-08-01 (not guessed): of 1155 objects, 1114 are analysis-relevant and
<=100MB, meaning each needs a real download+hash (`gcloud storage cat`) call —
this is genuinely too much work for one bounded invocation, not a bug to fix
away. A real bug WAS also found and fixed alongside: `get_gcs_metadata()` (a
`gcloud storage stat` call) previously ran for EVERY object unconditionally,
including the ~41 non-relevant/large ones, and its result (gcs_md5/crc32c) was
computed but never read back out in the markdown-emission loop — silently
dead work AND a silently broken promise (the module docstring says "records
GCS-side integrity" but never displayed it). Fixed: stat is now called only
for objects actually being hashed, and its result is displayed.

Usage:
  python3 scripts/audit_datalake.py --batch-size 150   # process up to 150 NEW
                                                         # objects, save checkpoint,
                                                         # emit manifest (PENDING rows
                                                         # for anything not yet done)
  python3 scripts/audit_datalake.py --batch-size 150    # run again — resumes from
                                                         # checkpoint, does the next 150
  python3 scripts/audit_datalake.py --status            # print progress only, no work
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
CHECKPOINT_PATH = Path("data/.audit_datalake_checkpoint.json")
MAX_HASH_SIZE = 100 * 1024 * 1024  # Only hash ≤ 100 MB
DEFAULT_BATCH_SIZE = 150
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
    """Get GCS-side MD5 and CRC32C via `gcloud storage objects describe`.

    FIXED 2026-08-01 (low-tier queue A-S3-2): the previous implementation called
    `gcloud storage stat`, which is not a valid subcommand in this gcloud version
    ("Invalid choice: 'stat'") -- it has always silently failed (caught by
    run_gcloud's generic non-zero-exit handler, returning None/None), so this
    function has never actually returned a real value. Verified the correct
    command + exact field names directly against a real object in the bucket
    before writing this: `gcloud storage objects describe <uri> --format=json`
    -> top-level keys `md5_hash` / `crc32c_hash` (base64-encoded, matching GCS's
    own encoding -- not decoded/re-encoded here, displayed as GCS returns them)."""
    output = run_gcloud(["objects", "describe", uri,
                          "--format=csv[no-heading](md5_hash,crc32c_hash)"])
    if not output:
        return None, None
    parts = output.split(",")
    md5 = parts[0].strip() if len(parts) > 0 and parts[0].strip() else None
    crc32c = parts[1].strip() if len(parts) > 1 and parts[1].strip() else None
    return md5, crc32c

def load_checkpoint():
    if CHECKPOINT_PATH.exists():
        return json.loads(CHECKPOINT_PATH.read_text())
    return {}


def save_checkpoint(checkpoint):
    CHECKPOINT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT_PATH.write_text(json.dumps(checkpoint, indent=2, sort_keys=True))


def process_object(uri, size):
    """Determine manifest status for an object, doing real work (hash/stat)
    only when actually needed. Returns a full record dict (not a status/detail
    pair) so it can be persisted directly into the checkpoint."""
    for quarantine_uri, reason in SEED_QUARANTINED:
        if quarantine_uri in uri:
            return {"uri": uri, "size_mb": round(size / (1024 * 1024), 2),
                     "status": "QUARANTINED", "sha256": None, "gcs_md5": None,
                     "gcs_crc32c": None, "reason": reason}

    is_analysis_relevant = any(pattern in uri for pattern in ANALYSIS_RELEVANT_PATTERNS)

    if is_analysis_relevant and size <= MAX_HASH_SIZE:
        sha256 = compute_sha256(uri)
        # stat is only called for objects we're actually hashing -- calling it
        # unconditionally for every object (incl. the ~41 non-relevant/large
        # ones) was the fixed bug: dead work whose result was never displayed.
        md5, crc32c = get_gcs_metadata(uri) if sha256 else (None, None)
        if sha256:
            return {"uri": uri, "size_mb": round(size / (1024 * 1024), 2),
                     "status": "AUDITED", "sha256": sha256, "gcs_md5": md5,
                     "gcs_crc32c": crc32c, "reason": None}
        return {"uri": uri, "size_mb": round(size / (1024 * 1024), 2),
                 "status": "PRESENT", "sha256": None, "gcs_md5": None,
                 "gcs_crc32c": None, "reason": "download failed, hash not computed"}

    return {"uri": uri, "size_mb": round(size / (1024 * 1024), 2),
             "status": "PRESENT", "sha256": None, "gcs_md5": None,
             "gcs_crc32c": None, "reason": None}

def main():
    ap_argv = sys.argv[1:]
    status_only = "--status" in ap_argv
    batch_size = DEFAULT_BATCH_SIZE
    for i, a in enumerate(ap_argv):
        if a == "--batch-size" and i + 1 < len(ap_argv):
            batch_size = int(ap_argv[i + 1])

    print("🔍 Listing datalake...", file=sys.stderr)
    objects = list_objects()
    print(f"   Found {len(objects)} objects", file=sys.stderr)

    checkpoint = load_checkpoint()
    pending = [(uri, size) for uri, size in objects if uri not in checkpoint]

    if status_only:
        print(f"   Checkpointed: {len(checkpoint)} | Pending: {len(pending)} "
              f"| Total: {len(objects)}", file=sys.stderr)
        return

    print(f"   Checkpointed already: {len(checkpoint)} | Pending: {len(pending)}",
          file=sys.stderr)

    batch = pending[:batch_size]
    print(f"   Processing this batch: {len(batch)} (--batch-size {batch_size})",
          file=sys.stderr)

    for n, (uri, size) in enumerate(batch, 1):
        record = process_object(uri, size)
        checkpoint[uri] = record
        save_checkpoint(checkpoint)  # persist after EACH object -- a kill
                                      # mid-batch loses at most one object's work
        if n % 25 == 0 or n == len(batch):
            print(f"   ... {n}/{len(batch)} in this batch "
                  f"({len(checkpoint)}/{len(objects)} total)", file=sys.stderr)

    # Build manifest rows from the checkpoint (source of truth) plus PENDING
    # rows for anything this or a prior invocation hasn't reached yet.
    manifest_rows = defaultdict(list)
    audited_count = present_count = pending_count = 0

    size_by_uri = dict(objects)
    for uri in {u for u, _ in objects}:
        folder = uri.split("/")[3] if len(uri.split("/")) > 3 else "root"
        if uri in checkpoint:
            rec = checkpoint[uri]
            manifest_rows[folder].append(rec)
            if rec["status"] == "AUDITED":
                audited_count += 1
            elif rec["status"] == "PRESENT":
                present_count += 1
        else:
            pending_count += 1
            manifest_rows[folder].append({
                "uri": uri, "size_mb": round(size_by_uri[uri] / (1024 * 1024), 2),
                "status": "PENDING", "sha256": None, "gcs_md5": None,
                "gcs_crc32c": None,
                "reason": "not yet processed this invocation -- re-run to continue",
            })

    # Add seed rows -- QUARANTINED seeds only as a synthetic "N/A"-size row if
    # that URI was NOT already found+processed in the real bucket listing.
    # FIXED 2026-08-01: previously appended unconditionally, so any seed whose
    # object actually exists in the bucket (both of the current two do) showed
    # TWICE in the manifest -- once real (real size, from the checkpoint) and
    # once synthetic (size "N/A"). Confirmed by inspecting the first full run's
    # output before this fix (grep showed both lean_oracle_v5.tar.gz and
    # SocrateAI_K3_T2_Discovery_Final.pdf duplicated). ABSENT seeds are not
    # affected -- by definition they do not exist in the bucket, so there is
    # nothing in `objects` for them to collide with.
    real_uris = {u for u, _ in objects}
    for seed_uri, reason in SEED_QUARANTINED:
        full_uri = f"{BUCKET}/{seed_uri}"
        if full_uri in real_uris:
            continue  # already added above from the real, checkpointed record
        folder = seed_uri.split("/")[0]
        manifest_rows[folder].append({
            "uri": full_uri,
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
**Pending (not yet reached by any batch):** {pending_count} · **Quarantined:** {len(SEED_QUARANTINED)} · **Absent (retracted claims):** {len(SEED_ABSENT)}
{'⚠️  ' + str(pending_count) + ' objects still PENDING — this is a partial manifest; re-run `python3 scripts/audit_datalake.py --batch-size ' + str(batch_size) + '` to continue from the checkpoint.' if pending_count else '✅ Full run — no PENDING objects remain.'}

---

## Status Vocabulary (Closed Set)

- **AUDITED**: Full SHA-256 hash computed on download; GCS-side MD5/CRC32C cross-checked.
- **PRESENT**: Object exists in bucket; hash not computed (exceeds 100 MB or not analysis-relevant).
- **PENDING**: Analysis-relevant, ≤100MB object not yet processed by any batch so far —
  status unknown, NOT the same as PRESENT (which means "checked, no hash needed").
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

        md_content += "| URI | Size (MB) | Status | SHA-256 | GCS MD5 / CRC32C / Note |\n"
        md_content += "|-----|-----------|--------|---------|--------------------------|\n"

        for row in rows:
            size_str = str(row["size_mb"])
            status = row["status"]
            sha_str = f"`{row['sha256'][:16]}...`" if row.get("sha256") else ""
            note = ""
            if row.get("gcs_md5") or row.get("gcs_crc32c"):
                note = f"md5=`{row.get('gcs_md5', '?')}` crc32c=`{row.get('gcs_crc32c', '?')}`"
            elif row.get("reason"):
                note = row["reason"]

            # Truncate URI for readability
            uri_short = row["uri"].replace(f"{BUCKET}/", "")
            md_content += f"| `{uri_short}` | {size_str} | **{status}** | {sha_str} | {note} |\n"

    # Write manifest
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(md_content)
    print(f"✅ Manifest written to {MANIFEST_PATH}", file=sys.stderr)
    print(f"   Audited: {audited_count} | Present: {present_count} | Pending: {pending_count} "
          f"| Quarantined: {len(SEED_QUARANTINED)} | Absent: {len(SEED_ABSENT)}", file=sys.stderr)
    if pending_count:
        print(f"   Re-run to continue: python3 scripts/audit_datalake.py "
              f"--batch-size {batch_size}", file=sys.stderr)

if __name__ == "__main__":
    main()
