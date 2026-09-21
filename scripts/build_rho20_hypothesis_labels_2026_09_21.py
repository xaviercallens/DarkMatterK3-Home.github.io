#!/usr/bin/env python3
"""Persist the ρ = 20 hypothesis-label vocabulary (T0 ruling R1, 2026-09-21).

    python3 scripts/build_rho20_hypothesis_labels_2026_09_21.py

Reads the SHA256-pinned Stream 2 mirror, writes
`data/derived/rho20_hypothesis_labels_2026_09_21.json`. Deterministic; no network; no real data.
The output is VOCABULARY for hypotheses — see `pipeline/cm_labels.py` for what it is not.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))
import cm_labels as L  # noqa: E402

OUT = ROOT / "data/derived/rho20_hypothesis_labels_2026_09_21.json"


def main() -> int:
    labels = L.load_labels()
    bad = [l.key for l in labels if not L.admits_discriminant(l.D, l.n)]
    if bad:
        print("REFUSING: labels fail the independent discriminant predicate:", bad[:5])
        return 1
    rec = L.vocabulary_record(labels)
    manifest = json.loads((L.MIRROR_DIR / "MIRROR_MANIFEST.json").read_text())
    rec["inputs"] = {"mirror_source_commit": manifest["source_commit"],
                     "sha256": {k: v["sha256"] for k, v in manifest["files"].items()}}
    OUT.write_text(json.dumps(rec, indent=1, sort_keys=True))        # persist BEFORE printing
    for cand, p in rec["per_candidate"].items():
        print(f"  {cand}: n={p['n']} labels={p['labels']} distinct_D={p['distinct_D']} "
              f"advisory={p['advisory']} unusable={p['unusable']}")
    print(f"  artifact: {OUT.relative_to(ROOT)}  [{rec['label']}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
