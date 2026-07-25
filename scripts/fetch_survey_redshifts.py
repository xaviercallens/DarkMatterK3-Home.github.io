#!/usr/bin/env python3
"""WP-R5 fetcher — real 3D positions (SDSS spectro-z + Euclid photo-z).

Extends scripts/fetch_survey_astroquery.py with the two queries WP-R5 needs to
build genuine 3D density fields:

  - SDSS:   astroquery.sdss.SDSS.query_region(..., spectro=True) — same fields
            and box size as the WP-R1 morphology fetch, but restricted to rows
            with a spectroscopic redshift (`z` column populated by SDSS itself).
  - Euclid: catalogue.mer_catalogue JOIN catalogue.phz_photo_z ON object_id —
            same cone fields as the morphology fetch, adding `phz_median` and
            `phz_mode_1` (photo-z point estimates; the PDF is not fetched here).

Gate-aware and no-fallback, identical discipline to fetch_survey_astroquery.py:
refuses pre-G1, records errors as-is, writes only to the external disk, and
appends a full-fidelity provenance block to data/MANIFEST.md. This is a
SEPARATE, separately-manifested query set per WP-R5 instructions — it does not
overwrite or alias the WP-R1 morphology-only files.
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
SDSS_Z_DIR = EXTERNAL_DATA_ROOT / "sdss_z"
EUCLID_Z_DIR = EXTERNAL_DATA_ROOT / "euclid_z"

# Same fields as fetch_survey_astroquery.py, same box/cone sizes — the point is
# a redshift-bearing companion to the WP-R1 files, not a new footprint.
SDSS_FIELDS = {
    "cosmos": (150.1, 2.2),
    "stripe82_center": (0.0, 0.0),
    "coma_cluster": (194.95, 27.98),
    "docs_example": (2.0235, 14.8398),
}
SDSS_BOX_ARCMIN = 10.0

EUCLID_FIELDS = {
    "edf_north": (267.7808, 65.5308),
    "edf_fornax": (53.13, -28.10),
    "edf_south": (61.0, -48.4),
}
EUCLID_CONE_DEG = 0.2
EUCLID_ROW_CAP = 2000


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def fetch_sdss_spectro() -> dict:
    """SDSS spectroscopic-redshift objects (same fields/box as WP-R1, spectro=True)."""
    from astropy import coordinates as coords
    from astropy import units as u
    from astroquery.sdss import SDSS

    SDSS_Z_DIR.mkdir(parents=True, exist_ok=True)
    entries = {}
    for name, (ra, dec) in SDSS_FIELDS.items():
        dest = SDSS_Z_DIR / f"sdss_z_{name}.csv"
        try:
            pos = coords.SkyCoord(ra=ra * u.deg, dec=dec * u.deg, frame="icrs")
            table = SDSS.query_region(
                pos, width=SDSS_BOX_ARCMIN * u.arcmin,
                height=SDSS_BOX_ARCMIN * u.arcmin, spectro=True,
            )
            if table is None:
                raise RuntimeError("query_region returned no table (zero spectro coverage)")
            table.write(dest, format="csv", overwrite=True)
            sha = _sha256(dest)
            entries[f"sdss_z_{name}"] = {
                "url": (
                    f"astroquery.sdss.SDSS.query_region(ra={ra}, dec={dec}, "
                    f"width={SDSS_BOX_ARCMIN}arcmin, height={SDSS_BOX_ARCMIN}arcmin, "
                    f"spectro=True)"
                ),
                "version": "SDSS spectroscopic (astroquery default DR, live query 2026-07-25)",
                "sha256": sha,
                "path": str(dest),
                "retrieved": _now_iso(),
                "rows": len(table),
                "status": "new",
            }
            logger.info(f"SDSS-z {name}: {len(table)} rows -> {dest}")
        except Exception as e:
            logger.error(f"SDSS-z {name} failed: {e}")
            entries[f"sdss_z_{name}"] = {"status": "error", "error": str(e)}
    return entries


def fetch_euclid_photoz() -> dict:
    """Euclid MER JOIN phz_photo_z on object_id (same cones as WP-R1)."""
    from astroquery.esa.euclid import Euclid

    EUCLID_Z_DIR.mkdir(parents=True, exist_ok=True)
    entries = {}
    for name, (ra, dec) in EUCLID_FIELDS.items():
        dest = EUCLID_Z_DIR / f"euclid_z_{name}.csv"
        adql = (
            f"SELECT TOP {EUCLID_ROW_CAP} m.object_id, m.right_ascension, "
            f"m.declination, p.phz_median, p.phz_mode_1 "
            f"FROM catalogue.mer_catalogue AS m "
            f"JOIN catalogue.phz_photo_z AS p ON m.object_id = p.object_id "
            f"WHERE 1=CONTAINS(POINT('ICRS', m.right_ascension, m.declination), "
            f"CIRCLE('ICRS', {ra}, {dec}, {EUCLID_CONE_DEG}))"
        )
        try:
            job = Euclid.launch_job(adql)
            table = job.get_results()
            if table is None or len(table) == 0:
                raise RuntimeError("ADQL join returned zero rows (zero coverage)")
            table.write(dest, format="csv", overwrite=True)
            sha = _sha256(dest)
            entries[f"euclid_z_{name}"] = {
                "url": adql,
                "version": "Euclid public MER JOIN phz_photo_z (PDR, live query 2026-07-25)",
                "sha256": sha,
                "path": str(dest),
                "retrieved": _now_iso(),
                "rows": len(table),
                "status": "new",
            }
            logger.info(f"Euclid-z {name}: {len(table)} rows -> {dest}")
        except Exception as e:
            logger.error(f"Euclid-z {name} failed: {e}")
            entries[f"euclid_z_{name}"] = {"status": "error", "error": str(e)}
    return entries


def fetch_all() -> dict:
    results = {}
    results.update(fetch_sdss_spectro())
    results.update(fetch_euclid_photoz())
    return results


def _append_full_provenance_appendix(results: dict) -> None:
    manifest = REPO_ROOT / "data" / "MANIFEST.md"
    lines = ["\n## Full-fidelity provenance — scripts/fetch_survey_redshifts.py "
             f"(WP-R5, {_now_iso()})\n\n"]
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
        logger.error(f"fetch_survey_redshifts.py refuses to run: {e}")
        return 1

    logger.info("Gate G1 is open (access-only; G1-L labeling stays closed). "
                "Fetching SDSS spectro-z + Euclid photo-z via astroquery...")
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
