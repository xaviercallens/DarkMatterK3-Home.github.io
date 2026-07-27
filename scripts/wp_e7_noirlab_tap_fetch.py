#!/usr/bin/env python3
"""
wp_e7_noirlab_tap_fetch.py -- background acquisition of real DESI DR1
(ra, dec, z) object catalogs via NOIRLab TAP (zpix JOIN photometry), per the
verified recipe in briefs/WP_E7_NOIRLAB_TAP_RECIPE_2026_07_27.md.

NOT run interactively -- launched as a long background process during a
session pause. Writes CSVs to data/raw/desi_dr1_noirlab/ (gitignored symlink
to the 500GB disk; nothing here is committed to git). Does NOT touch
data/MANIFEST.md or any tracked file -- provenance write-up and row-count
cross-checks against the published N are left for the next interactive
session (this script only fetches and logs).

Tracer bit definitions from desihub/desitarget targetmask.yaml (fetched
2026-07-27, public repo): desi_target LRG=bit0(1), ELG=bit1(2), QSO=bit2(4);
bgs_target BGS_BRIGHT=bit1(2). z-ranges and published N from
data/derived/wp_e7_desi_preflight_2026_07_27.json.

Neither pending T0 decision (occupancy threshold, eBOSS LRG sample identity)
blocks this acquisition -- both only affect downstream interpretation, per
the TAP recipe brief.

Generated-by: Sonnet 5 (T1 coordinator) | Verified-by: count-check per tracer
logged before any row pull | Reviewed-by: pending T0 (Xavier), next session
"""
import csv
import json
import logging
import sys
import time
from pathlib import Path

import pyvo

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "data" / "raw" / "desi_dr1_noirlab"
LOG_PATH = REPO / "data" / "raw" / "desi_dr1_noirlab" / "fetch_log.txt"

TRACERS = {
    "BGS": {"zmin": 0.1, "zmax": 0.4, "published_n": 300017,
            "bit_col": "bgs_target", "bit_val": 2},   # BGS_BRIGHT
    "LRG": {"zmin": 0.4, "zmax": 1.1, "published_n": 2138600,
            "bit_col": "desi_target", "bit_val": 1},  # LRG
    "ELG": {"zmin": 0.8, "zmax": 1.6, "published_n": 2432022,
            "bit_col": "desi_target", "bit_val": 2},  # ELG
    "QSO": {"zmin": 0.8, "zmax": 2.1, "published_n": 856652,
            "bit_col": "desi_target", "bit_val": 4},  # QSO
}

TAP_URL = "https://datalab.noirlab.edu/tap"


def setup_logging():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler(sys.stdout)],
    )


def count_query(svc, tracer, cfg, use_bitmask):
    if use_bitmask:
        bit_test = f"MOD(z.{cfg['bit_col']} / {cfg['bit_val']}, 2) = 1"
    else:
        bit_test = "1=1"
    q = f"""
    SELECT COUNT(*) as n
    FROM desi_dr1.zpix AS z
    WHERE z.survey='main' AND z.zwarn=0 AND z.z >= {cfg['zmin']} AND z.z < {cfg['zmax']}
      AND {bit_test}
    """
    res = svc.search(q)
    return int(res[0]["n"]), q


def pull_tracer(svc, tracer, cfg, use_bitmask):
    if use_bitmask:
        bit_test = f"MOD(z.{cfg['bit_col']} / {cfg['bit_val']}, 2) = 1"
    else:
        bit_test = "1=1"
    q = f"""
    SELECT z.targetid, z.z, z.zwarn, z.spectype, z.survey, z.program,
           z.bgs_target, z.desi_target, p.ra, p.dec
    FROM desi_dr1.zpix AS z
    JOIN desi_dr1.photometry AS p ON z.targetid = p.targetid
    WHERE z.survey='main' AND z.zwarn=0
      AND z.z >= {cfg['zmin']} AND z.z < {cfg['zmax']}
      AND {bit_test}
    """
    logging.info("[%s] submitting async TAP job", tracer)
    job = svc.submit_job(q, language="ADQL")
    job.run()
    job.wait(phases=["COMPLETED", "ERROR", "ABORTED"], timeout=1800)
    job.raise_if_error()
    result = job.fetch_result()
    out_csv = OUT_DIR / f"{tracer.lower()}_zpix_photometry_2026_07_27.csv"
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        cols = result.fieldnames
        w.writerow(cols)
        n = 0
        for row in result:
            w.writerow([row[c] for c in cols])
            n += 1
    job.delete()
    return n, out_csv


def main():
    setup_logging()
    logging.info("=== WP-E7 NOIRLab TAP fetch starting ===")
    svc = pyvo.dal.TAPService(TAP_URL)

    manifest = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "source": "NOIRLab Data Lab TAP, desi_dr1.zpix JOIN desi_dr1.photometry",
                "tracers": {}}

    for tracer, cfg in TRACERS.items():
        logging.info("--- %s (published N=%d) ---", tracer, cfg["published_n"])
        try:
            n_bitmask, q_bm = count_query(svc, tracer, cfg, use_bitmask=True)
            logging.info("[%s] bitmask-filtered count = %d (published %d, ratio %.3f)",
                         tracer, n_bitmask, cfg["published_n"],
                         n_bitmask / cfg["published_n"] if cfg["published_n"] else float("nan"))
            use_bitmask = True
            n_expected = n_bitmask
        except Exception as e:
            logging.warning("[%s] bitmask query failed (%s) -- falling back to "
                             "spectype/z-range only, no tracer-bit filter", tracer, e)
            use_bitmask = False
            try:
                n_fallback, q_fb = count_query(svc, tracer, cfg, use_bitmask=False)
                logging.info("[%s] fallback (no bitmask) count = %d", tracer, n_fallback)
                n_expected = n_fallback
            except Exception as e2:
                logging.error("[%s] fallback count also failed (%s) -- skipping tracer",
                               tracer, e2)
                manifest["tracers"][tracer] = {"status": "FAILED", "error": str(e2)}
                continue

        if n_expected == 0:
            logging.warning("[%s] zero rows match -- skipping pull", tracer)
            manifest["tracers"][tracer] = {"status": "ZERO_ROWS"}
            continue
        if n_expected > 10_000_000:
            logging.warning("[%s] %d rows is very large -- pulling anyway via async, "
                             "may take a while", tracer, n_expected)

        try:
            n_pulled, out_csv = pull_tracer(svc, tracer, cfg, use_bitmask)
            logging.info("[%s] pulled %d rows -> %s", tracer, n_pulled, out_csv)
            manifest["tracers"][tracer] = {
                "status": "OK",
                "use_bitmask": use_bitmask,
                "n_rows": n_pulled,
                "published_n": cfg["published_n"],
                "ratio_to_published": n_pulled / cfg["published_n"] if cfg["published_n"] else None,
                "csv": str(out_csv.relative_to(REPO)),
                "zmin": cfg["zmin"], "zmax": cfg["zmax"],
            }
        except Exception as e:
            logging.error("[%s] pull failed: %s", tracer, e)
            manifest["tracers"][tracer] = {"status": "PULL_FAILED", "error": str(e)}

    manifest_path = OUT_DIR / "fetch_manifest_draft.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    logging.info("=== done. draft manifest: %s ===", manifest_path)
    logging.info("NOTE: this is a DRAFT manifest in data/raw (gitignored). Review row "
                 "counts vs published N, then write a proper data/MANIFEST.md entry by "
                 "hand next session before anything derived from this data is trusted.")


if __name__ == "__main__":
    main()
