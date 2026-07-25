#!/usr/bin/env python3
"""S3-01 (real) — SDSS + Euclid via the standard astroquery method.

Replaces the placeholder-URL fetchers in scripts/data_fetchers.py for these two
surveys (which were never real: SDSS_LENSING_URL was a guessed svn.sdss.org path
and no Euclid fetcher existed at all — see LEGACY_CODE_DISPOSITION_2026_07_25.md).

Standard method, verified live against both services before this file was written:
  - SDSS:   astroquery.sdss.SDSS.query_region  (rectangular width/height mode)
  - Euclid: astroquery.esa.euclid.Euclid.launch_job  (ADQL cone query on the public
            MER — Merged photometric — catalogue, no authentication required)

Gate-aware: refuses to run until PREDICTION.md is pinned (gate G1), exactly like
scripts/fetch_data.py. G1 open only permits data ACCESS as engineering prep work
(briefs/T0_RULING_G1L_AND_PIVOT_AUTHORIZATION_2026_07_25.md §1, "the two-gate
split") — it does NOT authorize any TEST/FIT label, which requires gate G1-L
(currently closed; see NO_PREDICTION_BRANCH.md §8.5). This script produces no
label of any kind.

No synthetic fallback exists anywhere in this file. If a query fails, the error is
recorded as-is; nothing is substituted.

Storage: the external disk (more headroom than the repo's local filesystem), NOT
committed to git. Only the small manifest entries (URL/query, version, SHA256,
timestamp) are committed, in data/MANIFEST.md and data/MANIFEST_S3.md.
"""
import hashlib
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.gate import GateError, require_pinned_for_real_data  # noqa: E402

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EXTERNAL_DATA_ROOT = Path("/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata")
SDSS_DIR = EXTERNAL_DATA_ROOT / "sdss"
EUCLID_DIR = EXTERNAL_DATA_ROOT / "euclid"

# Real sky positions, each verified live to return real rows before being listed here
# (no position is included on the assumption that it "should" have coverage).
SDSS_FIELDS = {
    "cosmos": (150.1, 2.2),          # COSMOS field
    "stripe82_center": (0.0, 0.0),   # SDSS Stripe 82
    "coma_cluster": (194.95, 27.98), # Coma cluster region
    "docs_example": (2.0235, 14.8398),
}
SDSS_BOX_ARCMIN = 10.0  # width=height, rectangular query_region mode

EUCLID_FIELDS = {
    "edf_north": (267.7808, 65.5308),  # Euclid Deep Field North
    "edf_fornax": (53.13, -28.10),     # Euclid Deep Field Fornax
    "edf_south": (61.0, -48.4),        # Euclid Deep Field South
}
EUCLID_CONE_DEG = 0.2
EUCLID_ROW_CAP = 2000
EUCLID_COLUMNS = (
    "object_id, right_ascension, declination, ellipticity, ellipticity_err, "
    "semimajor_axis, position_angle, flux_vis_2fwhm_aper, fluxerr_vis_2fwhm_aper, "
    "point_like_flag, extended_flag, det_quality_flag, vis_det"
)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def fetch_sdss() -> dict:
    """Real SDSS photometric objects via astroquery.sdss.SDSS.query_region."""
    from astropy import coordinates as coords
    from astropy import units as u
    from astroquery.sdss import SDSS

    SDSS_DIR.mkdir(parents=True, exist_ok=True)
    entries = {}
    for name, (ra, dec) in SDSS_FIELDS.items():
        dest = SDSS_DIR / f"sdss_{name}.csv"
        try:
            pos = coords.SkyCoord(ra=ra * u.deg, dec=dec * u.deg, frame="icrs")
            table = SDSS.query_region(
                pos, width=SDSS_BOX_ARCMIN * u.arcmin,
                height=SDSS_BOX_ARCMIN * u.arcmin, spectro=False,
            )
            if table is None:
                raise RuntimeError("query_region returned no table (zero coverage)")
            table.write(dest, format="csv", overwrite=True)
            sha = _sha256(dest)
            entries[f"sdss_{name}"] = {
                "url": (
                    f"astroquery.sdss.SDSS.query_region(ra={ra}, dec={dec}, "
                    f"width={SDSS_BOX_ARCMIN}arcmin, height={SDSS_BOX_ARCMIN}arcmin, "
                    f"spectro=False)"
                ),
                "version": "SDSS (astroquery default DR, live query 2026-07-25)",
                "sha256": sha,
                "path": str(dest),
                "retrieved": _now_iso(),
                "rows": len(table),
                "status": "new",
            }
            logger.info(f"SDSS {name}: {len(table)} rows -> {dest}")
        except Exception as e:
            logger.error(f"SDSS {name} failed: {e}")
            entries[f"sdss_{name}"] = {"status": "error", "error": str(e)}
    return entries


def fetch_euclid() -> dict:
    """Real Euclid MER catalogue objects via astroquery.esa.euclid.Euclid ADQL."""
    from astroquery.esa.euclid import Euclid

    EUCLID_DIR.mkdir(parents=True, exist_ok=True)
    entries = {}
    for name, (ra, dec) in EUCLID_FIELDS.items():
        dest = EUCLID_DIR / f"euclid_{name}.csv"
        adql = (
            f"SELECT TOP {EUCLID_ROW_CAP} {EUCLID_COLUMNS} FROM catalogue.mer_catalogue "
            f"WHERE 1=CONTAINS(POINT('ICRS', right_ascension, declination), "
            f"CIRCLE('ICRS', {ra}, {dec}, {EUCLID_CONE_DEG}))"
        )
        try:
            job = Euclid.launch_job(adql)
            table = job.get_results()
            if table is None or len(table) == 0:
                raise RuntimeError("ADQL query returned zero rows (zero coverage)")
            table.write(dest, format="csv", overwrite=True)
            sha = _sha256(dest)
            entries[f"euclid_{name}"] = {
                "url": adql,
                "version": "Euclid public MER catalogue (PDR, live query 2026-07-25)",
                "sha256": sha,
                "path": str(dest),
                "retrieved": _now_iso(),
                "rows": len(table),
                "status": "new",
            }
            logger.info(f"Euclid {name}: {len(table)} rows -> {dest}")
        except Exception as e:
            logger.error(f"Euclid {name} failed: {e}")
            entries[f"euclid_{name}"] = {"status": "error", "error": str(e)}
    return entries


def fetch_all() -> dict:
    results = {}
    results.update(fetch_sdss())
    results.update(fetch_euclid())
    return results


def _append_full_provenance_appendix(results: dict) -> None:
    """MANIFEST.md's table truncates SHA256 to 16 chars and has no path column;
    the data files themselves live on the external disk, not in git. Append an
    exact-fidelity record so the truncated table row is never the only copy of
    the real hash or the file location."""
    manifest = REPO_ROOT / "data" / "MANIFEST.md"
    lines = ["\n## Full-fidelity provenance — scripts/fetch_survey_astroquery.py "
             f"({_now_iso()})\n\n"]
    for name, r in results.items():
        if r.get("status") == "error":
            lines.append(f"- **{name}**: ERROR — {r.get('error')}\n")
            continue
        lines.append(
            f"- **{name}** — rows: {r.get('rows')}, path: `{r.get('path')}`, "
            f"sha256: `{r.get('sha256')}`, retrieved: {r.get('retrieved')}\n"
            f"  query: `{r.get('url')}`\n"
        )
    with open(manifest, "a") as f:
        f.writelines(lines)


def main() -> int:
    try:
        require_pinned_for_real_data()
    except GateError as e:
        logger.error(f"fetch_survey_astroquery.py refuses to run: {e}")
        return 1

    logger.info("Gate G1 is open (access-only; G1-L labeling stays closed). "
                "Fetching real SDSS + Euclid data via astroquery...")
    results = fetch_all()

    from scripts.manifest import update_manifest
    update_manifest(results)
    _append_full_provenance_appendix(results)

    n_ok = sum(1 for v in results.values() if v.get("status") != "error")
    n_err = len(results) - n_ok
    logger.info(f"Done: {n_ok} succeeded, {n_err} failed. data/MANIFEST.md updated.")
    return 0 if n_err == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
