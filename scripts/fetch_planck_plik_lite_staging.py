#!/usr/bin/env python3
"""
WP-DL-PLANCK — Planck 2018 plik_lite acquisition (DL-2 P1, T0-ratified
2026-07-31, `briefs/T0_RATIFICATION_2026_07_31_DATALAKE.md` + WP scope
`briefs/EXECUTION_PLAN_2026_07_31_DATALAKE_GOVERNANCE.md` Wave 3).

WHAT THIS DOES: fetches the Planck 2018 baseline likelihood release from the
ESA Planck Legacy Archive, extracts ONLY the plik_lite TTTEEE
nuisance-marginalized high-l likelihood (foreground-marginalized TT/TE/EE
bandpowers + covariance), uploads it to GCS **staging** at
gs://.../planck_2018/, and records the source URL + retrieval date.

WHAT THIS DELIBERATELY DOES NOT DO (per the WP scope, annotation A5):
- Does NOT write into data/raw/ or register with fetch_data.py -- this stays
  GCS-staging-only until a Planck channel amendment is pinned (DL-3).
- Does NOT compute or claim any cosmological parameter from this data --
  acquisition only.

Usage:
  python3 scripts/fetch_planck_plik_lite_staging.py

Idempotent: if the destination GCS object already exists with a hash-matching
local re-computation, the download step is skipped.
"""

import hashlib
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path

PLA_URL = (
    "https://pla.esac.esa.int/pla/aio/product-action"
    "?COSMOLOGY.FILE_ID=COM_Likelihood_Data-baseline_R3.00.tar.gz"
)
# Verified 2026-08-01 via the PLA wiki (wiki.cosmos.esa.int, "CMB spectrum &
# Likelihood Code" page) -- not guessed or recalled from memory.
PLIK_LITE_MEMBER_PREFIX = "baseline/plc_3.0/hi_l/plik_lite/"
# CORRECTED 2026-08-01, same session: the PLA wiki text describes the path
# relative to the archive's own top level, but the actual downloaded tarball
# wraps everything in a `baseline/` directory the wiki text didn't mention.
# First run failed loudly (no members found) rather than silently guessing --
# confirmed the real layout by downloading and listing the tarball directly
# (`tar tzf`) before adjusting this constant, not by re-guessing.
BUCKET_STAGING_PREFIX = "gs://socrateai-datalake-gen-lang-client-0625573011/planck_2018/"


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def gcs_object_exists(uri: str) -> bool:
    r = subprocess.run(["gcloud", "storage", "ls", uri],
                        capture_output=True, text=True, timeout=30)
    return r.returncode == 0


def main():
    with tempfile.TemporaryDirectory(prefix="planck_plik_lite_") as tmpdir:
        tmp = Path(tmpdir)
        archive_path = tmp / "COM_Likelihood_Data-baseline_R3.00.tar.gz"

        print(f"Downloading {PLA_URL} ...", file=sys.stderr)
        r = subprocess.run(
            ["curl", "-L", "-f", "--retry", "3", "-o", str(archive_path), PLA_URL],
            timeout=3600,
        )
        if r.returncode != 0 or not archive_path.exists():
            print("FAIL: download failed", file=sys.stderr)
            return 1
        archive_sha256 = sha256_of_file(archive_path)
        archive_size_mb = archive_path.stat().st_size / (1024 * 1024)
        print(f"Downloaded {archive_size_mb:.1f} MB, SHA-256={archive_sha256}",
              file=sys.stderr)

        print(f"Extracting members under {PLIK_LITE_MEMBER_PREFIX} ...", file=sys.stderr)
        extract_dir = tmp / "extracted"
        extract_dir.mkdir()
        n_extracted = 0
        with tarfile.open(archive_path, "r:gz") as tf:
            members = [m for m in tf.getmembers()
                       if m.name.startswith(PLIK_LITE_MEMBER_PREFIX) and m.isfile()]
            if not members:
                print(f"FAIL: no members found under {PLIK_LITE_MEMBER_PREFIX} -- "
                      "archive layout may have changed since this script was "
                      "written (verified 2026-08-01); do not guess, re-check "
                      "the PLA wiki before adjusting the prefix.", file=sys.stderr)
                return 1
            tf.extractall(extract_dir, members=members)
            n_extracted = len(members)
        print(f"Extracted {n_extracted} files", file=sys.stderr)

        plik_lite_root = extract_dir / PLIK_LITE_MEMBER_PREFIX.rstrip("/")
        uploaded = []
        for f in sorted(plik_lite_root.rglob("*")):
            if not f.is_file():
                continue
            rel = f.relative_to(extract_dir)
            dest_uri = BUCKET_STAGING_PREFIX + str(rel)
            local_sha256 = sha256_of_file(f)

            if gcs_object_exists(dest_uri):
                print(f"  already present, skipping upload: {dest_uri}", file=sys.stderr)
                uploaded.append({"uri": dest_uri, "sha256": local_sha256, "status": "cached"})
                continue

            r = subprocess.run(["gcloud", "storage", "cp", str(f), dest_uri],
                                capture_output=True, text=True, timeout=300)
            if r.returncode != 0:
                print(f"FAIL: upload failed for {rel}: {r.stderr}", file=sys.stderr)
                return 1
            print(f"  uploaded: {dest_uri} (sha256={local_sha256[:16]}...)", file=sys.stderr)
            uploaded.append({"uri": dest_uri, "sha256": local_sha256, "status": "uploaded"})

        print(f"\nSUMMARY: {len(uploaded)} plik_lite files staged under "
              f"{BUCKET_STAGING_PREFIX}", file=sys.stderr)
        print(f"Source: {PLA_URL}", file=sys.stderr)
        print(f"Source archive SHA-256: {archive_sha256}", file=sys.stderr)
        print(f"Retrieved: {datetime.now(timezone.utc).isoformat()}", file=sys.stderr)
        print("\nNOT written to data/raw/, NOT registered with fetch_data.py, "
              "per WP-DL-PLANCK scope (staging only until a Planck channel "
              "amendment is pinned, DL-3). Run scripts/audit_datalake.py next "
              "to pick these objects up into GCS_DATALAKE_MANIFEST.md.",
              file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
