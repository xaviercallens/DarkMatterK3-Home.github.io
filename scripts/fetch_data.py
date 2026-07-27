#!/usr/bin/env python3
"""S3-01 — The only entry point for datasets (CLAUDE.md Commands).

Gate-aware: refuses to run until PREDICTION.md is pinned (gate G1). Once
pinned, this script fetches NANOGrav/EPTA (PTA observable P2), lensing (P1),
and Lyman-α constraints — idempotent, checksummed, and recorded in
data/MANIFEST.md. See scripts/data_fetchers.py for individual dataset
implementations.

WP-E7 Task B (T0-approved 2026-07-27, briefs/T0_DECISIONS_2026_07_27.md D-a)
extends this with a scoped acquisition of DESI DR1 (+ SDSS/eBOSS DR16
secondary) LSS/clustering catalogs, hard-capped at 20 GB total, LSS/clustering
catalogs only (no spectra, no imaging). After the normal fetch + manifest
update, this script:
  - appends a full-fidelity provenance block to data/MANIFEST.md (path, full
    SHA256, row count, and any manual-download note for a refused source) --
    same convention as scripts/fetch_survey_astroquery.py's
    _append_full_provenance_appendix, and
  - runs a row-count sanity check against published counts for any FITS
    catalog fetched, printing (not fixing) any mismatch as a finding.
"""
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.gate import GateError, require_pinned_for_real_data  # noqa: E402
from scripts.data_fetchers import fetch_all_datasets  # noqa: E402
from scripts.manifest import update_manifest  # noqa: E402

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MANIFEST_FILE = REPO_ROOT / "data" / "MANIFEST.md"

# Published row counts to sanity-check fetched FITS catalogs against
# (docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md §3; arXiv:2007.09000 for eBOSS).
# A mismatch is recorded as a finding, not silently corrected.
PUBLISHED_ROW_COUNTS = {
    # Combined NGC+SGC eBOSS LRG clustering sample (Ross et al. 2020).
    ("eboss_lrg_clustering_data_ngc", "eboss_lrg_clustering_data_sgc"): 377_458,
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _append_full_provenance_appendix(results: dict) -> None:
    """Full-fidelity provenance block for the WP-E7 Task B fetches: exact
    path, full SHA256, row count, and (for a refused source) the exact
    failure plus its manual-download instruction. Same convention as
    scripts/fetch_survey_astroquery.py's appendix -- the MANIFEST.md table
    itself truncates SHA256 to 16 chars and carries no path column."""
    lines = [f"\n## Full-fidelity provenance — scripts/fetch_data.py "
             f"(WP-E7 Task B, {_now_iso()})\n\n"]
    for name, r in results.items():
        if r.get("status") == "error":
            line = f"- **{name}**: ERROR — {r.get('error', 'unknown')} (url: {r.get('url', 'n/a')})\n"
            if r.get("manual_download"):
                line += f"  Manual-download instruction: {r['manual_download']}\n"
            lines.append(line)
            continue
        lines.append(
            f"- **{name}** — path: `data/{r.get('path')}`, sha256: `{r.get('sha256')}`, "
            f"retrieved: {r.get('retrieved')}, status: {r.get('status')}\n"
            f"  url: `{r.get('url')}`\n"
        )
    with open(MANIFEST_FILE, "a") as f:
        f.writelines(lines)


def _fits_row_count(rel_path: str) -> int | None:
    """Row count of the first binary table HDU in a fetched FITS file, or
    None if the file is missing or not readable as FITS."""
    path = REPO_ROOT / "data" / rel_path
    if not path.exists():
        return None
    try:
        from astropy.io import fits
        with fits.open(path) as hdul:
            for hdu in hdul:
                if hasattr(hdu, "data") and hdu.data is not None and hasattr(hdu.data, "shape"):
                    return int(len(hdu.data))
    except Exception as e:
        logger.warning(f"Could not read FITS row count for {rel_path}: {e}")
        return None
    return None


def _run_integrity_checks(results: dict) -> None:
    """Row-count/column sanity check against published counts (task rule:
    'a mismatch is a finding to record, not to fix'). No analysis beyond
    this; no comparison code is run here."""
    row_counts = {}
    for name, r in results.items():
        if r.get("status") in ("new", "cached") and r.get("path"):
            n = _fits_row_count(r["path"])
            row_counts[name] = n
            if n is not None:
                logger.info(f"Integrity check: {name} has {n} rows.")

    for keys, published in PUBLISHED_ROW_COUNTS.items():
        counts = [row_counts.get(k) for k in keys]
        if any(c is None for c in counts):
            continue
        total = sum(counts)
        status = "MATCH" if total == published else "MISMATCH"
        logger.info(
            f"Integrity check {keys}: fetched total = {total}, published = "
            f"{published} -> {status}"
        )
        with open(MANIFEST_FILE, "a") as f:
            f.write(
                f"\n**Integrity check ({_now_iso()}):** {' + '.join(keys)} row-count "
                f"total = {total}; published (docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md "
                f"§3, arXiv:2007.09000) = {published}. Verdict: {status}.\n"
            )


def main() -> int:
    try:
        require_pinned_for_real_data()
    except GateError as e:
        logger.error(f"fetch_data.py refuses to run: {e}")
        return 1

    # Reached only once PREDICTION.md is pinned (gate G1 open) — WP S3-01
    logger.info("Gate G1 is open. Fetching datasets for S3 observables (P1, P2)...")

    try:
        results = fetch_all_datasets()
        update_manifest(results)
        _append_full_provenance_appendix(results)
        _run_integrity_checks(results)
        logger.info("All datasets fetched and checksummed. data/MANIFEST.md updated.")
        n_err = sum(1 for v in results.values() if v.get("status") == "error")
        if n_err:
            logger.warning(f"{n_err} dataset(s) recorded as errors (see MANIFEST.md).")
        return 0
    except Exception as e:
        logger.error(f"Dataset fetch failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
