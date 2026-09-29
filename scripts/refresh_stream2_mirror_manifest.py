#!/usr/bin/env python3
"""refresh_stream2_mirror_manifest.py -- regenerate data/mirrors/stream2/MIRROR_MANIFEST.json
from the mirrored files themselves (sha256 and each certificate's own not_claimed block).

Nothing in the manifest is typed: hashes are computed, not_claimed blocks are copied from the
certificates, and the previous manifest's "refreshed" history is carried forward. The source
commit is the only argument, and it must be the K3-DarkMatter main commit the files were
exported from (verified by the caller with `git show <commit>:<path> | sha256sum`).

Usage: python3 scripts/refresh_stream2_mirror_manifest.py --source-commit <sha> --date YYYY-MM-DD
       python3 scripts/refresh_stream2_mirror_manifest.py --check   # exit 1 if any hash drifted
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MIRROR = REPO / "data" / "mirrors" / "stream2"
MANIFEST = MIRROR / "MIRROR_MANIFEST.json"


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def not_claimed_of(d):
    if isinstance(d.get("not_claimed"), list):
        return d["not_claimed"]
    for k in ("result", "status", "certificate"):
        v = d.get(k)
        if isinstance(v, dict) and isinstance(v.get("not_claimed"), list):
            return v["not_claimed"]
    return None


def files_block():
    out = {}
    for p in sorted(MIRROR.glob("*.json")):
        if p.name == MANIFEST.name:
            continue
        d = json.loads(p.read_text())
        entry = {"sha256": sha256(p)}
        nc = not_claimed_of(d)
        entry["not_claimed"] = nc if nc is not None else "(certificate carries no not_claimed block; read its status field)"
        if isinstance(d.get("status"), str):
            entry["status_as_shipped"] = d["status"][:240]
        out[p.name] = entry
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-commit")
    ap.add_argument("--date")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    old = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    fresh = files_block()
    if a.check:
        drift = [n for n, e in fresh.items() if old.get("files", {}).get(n, {}).get("sha256") != e["sha256"]]
        missing = [n for n in old.get("files", {}) if n not in fresh]
        if drift or missing:
            print("DRIFT:", drift, "MISSING:", missing, file=sys.stderr)
            return 1
        print(f"OK: {len(fresh)} mirrored files match the manifest")
        return 0
    if not (a.source_commit and a.date):
        ap.error("--source-commit and --date are required to rewrite the manifest")
    history = list(old.get("history", []))
    if old:
        history.append({
            "source_commit": old.get("source_commit"),
            "mirrored_on": old.get("mirrored_on"),
            "files_sha256": {n: e.get("sha256") for n, e in old.get("files", {}).items()},
            "refreshed": old.get("refreshed"),
        })
    new = {
        "mirror_of": "SocrateAI-Scientific-Agora-K3-DarkMatter (Stream 2)",
        "source_commit": a.source_commit,
        "mirrored_on": a.date,
        "why": old.get("why", "Stream 2 certificates mirrored so Stream 3 can cite and drift-test them."),
        "honor": ("These are Stream 2 artifacts; Stream 3 neither produced nor re-derived their contents. "
                  "Each certificate's own not_claimed block travels with it and must not be dropped. "
                  "Rows/flags that predate a later Stream 2 ruling (e.g. LATTICE_CERT_DRAFT / advisory=true on "
                  "cooper_s10 rows emitted before D15' of 2026-09-29) are dated, not wrong; do not edit them here."),
        "generated_by": "scripts/refresh_stream2_mirror_manifest.py (hashes computed, not typed)",
        "files": fresh,
        "history": history,
    }
    MANIFEST.write_text(json.dumps(new, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {MANIFEST} ({len(fresh)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
