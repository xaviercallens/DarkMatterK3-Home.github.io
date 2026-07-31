#!/usr/bin/env python3
"""S3-01 — Data Acquisition: Fetch & checksum public datasets.

Datasets:
1. NANOGrav 15-yr free-spectrum posteriors (PTA)
2. EPTA DR2 posteriors (PTA)
3. SDSS/DES/Euclid published weak-lensing stacked profiles (lensing)
4. Lyman-α power-spectrum constraints (small-scale structure)

Each fetcher:
- Is idempotent (skips re-download if file exists + checksum matches)
- Computes and verifies SHA256 checksums
- Records dataset entry in data/MANIFEST.md
- Returns dict with {url, version, sha256, path}

No gate check here (fetch_data.py checks gate before calling).
"""
import hashlib
import json
import logging
from pathlib import Path
from typing import Optional
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"


def check_url_reachable(url: str, timeout: float = 15.0) -> dict:
    """HEAD/small-ranged-request pre-check before committing to a multi-GB
    download (WP-E7 Task B discipline, T0-approved 2026-07-27, per
    briefs/T0_DECISIONS_2026_07_27.md D-a). Never retries with spoofed
    headers; a refusal here is recorded as-is, not scraped around.

    Returns {"reachable": bool, "content_length": int | None, "error": str | None}.
    """
    req = Request(url, method="HEAD")
    try:
        with urlopen(req, timeout=timeout) as resp:
            length = resp.headers.get("Content-Length")
            return {
                "reachable": True,
                "content_length": int(length) if length else None,
                "error": None,
            }
    except Exception as e:
        return {"reachable": False, "content_length": None, "error": str(e)}


def compute_sha256(file_path: Path) -> str:
    """Compute SHA256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def fetch_file(url: str, dest_path, expected_sha256: Optional[str] = None) -> dict:
    """
    Fetch a file from URL; verify checksum if provided; skip if already present.

    Args:
        url: Remote URL
        dest_path: Where to save the file (within data/ dir); str or Path
        expected_sha256: If provided, verify the downloaded file matches this hash

    Returns:
        {
            "url": url,
            "version": extracted from URL or metadata,
            "sha256": computed hash of downloaded file,
            "path": relative path within data/,
            "retrieved": ISO timestamp,
            "status": "new" | "cached" (was already present)
        }
    """
    dest_path = Path(dest_path)
    dest_path = DATA_DIR / dest_path if not dest_path.is_absolute() else dest_path
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # Check if file already exists
    if dest_path.exists():
        computed_sha = compute_sha256(dest_path)
        if expected_sha256 is None or computed_sha == expected_sha256:
            logger.info(f"Dataset already cached: {dest_path.relative_to(REPO_ROOT)}")
            from datetime import datetime
            return {
                "url": url,
                "version": "cached",
                "sha256": computed_sha,
                "path": str(dest_path.relative_to(DATA_DIR)),
                "retrieved": datetime.now().isoformat(),
                "status": "cached",
            }
        else:
            logger.warning(
                f"Cached file {dest_path} has checksum mismatch. Re-downloading."
            )
            dest_path.unlink()

    # Download
    logger.info(f"Downloading {url}...")
    try:
        with urlopen(url, timeout=30) as response:
            data = response.read()
        with open(dest_path, "wb") as f:
            f.write(data)
    except Exception as e:
        logger.error(f"Failed to download {url}: {e}")
        raise

    # Verify checksum
    computed_sha = compute_sha256(dest_path)
    if expected_sha256 and computed_sha != expected_sha256:
        logger.error(
            f"Checksum mismatch for {url}: got {computed_sha}, "
            f"expected {expected_sha256}"
        )
        dest_path.unlink()
        raise ValueError("Checksum verification failed")

    from datetime import datetime
    return {
        "url": url,
        "version": "retrieved",
        "sha256": computed_sha,
        "path": str(dest_path.relative_to(DATA_DIR)),
        "retrieved": datetime.now().isoformat(),
        "status": "new",
    }


# ============================================================================
# Dataset-specific fetchers (URLs and expected checksums from published sources)
# ============================================================================

NANOGRAV_15YR_FREE_SPECTRUM_URL = (
    "https://data.nanograv.org/static/data/dr15/free_spectrum/"
    "free_spectrum_fullband_mg30ts.json"
)
NANOGRAV_15YR_SHA256 = (
    "placeholder_sha256_nanograv_15yr"  # Will be computed on first download
)

EPTA_DR2_URL = (
    "https://zenodo.org/record/6504504/files/"
    "EPTA_DR2_spectrum.txt"  # Placeholder; actual URL from EPTA release notes
)
EPTA_DR2_SHA256 = "placeholder_sha256_epta_dr2"

SDSS_LENSING_URL = (
    "https://svn.sdss.org/public/dr12/eboss/lss/DR12_Lensing_Catalog.fits"
    # Placeholder; actual SDSS data server URL
)
SDSS_LENSING_SHA256 = "placeholder_sha256_sdss_lensing"

# Lyman-alpha constraints (XQ-100 or similar public dataset)
LYMAN_ALPHA_CONSTRAINTS_URL = (
    "https://archive.stsci.edu/missions/hlsp/xq100/dr1/"
    "lya_transmission.fits"  # Placeholder
)
LYMAN_ALPHA_SHA256 = "placeholder_sha256_lya"


def fetch_nanograv_15yr() -> dict:
    """Fetch NANOGrav 15-yr free-spectrum posteriors (PTA observable P2)."""
    return fetch_file(
        NANOGRAV_15YR_FREE_SPECTRUM_URL,
        "pta/nanograv_15yr_free_spectrum.json",
        expected_sha256=NANOGRAV_15YR_SHA256,
    )


def fetch_epta_dr2() -> dict:
    """Fetch EPTA DR2 free-spectrum posteriors (PTA observable P2, alternative)."""
    return fetch_file(
        EPTA_DR2_URL,
        "pta/epta_dr2_spectrum.txt",
        expected_sha256=EPTA_DR2_SHA256,
    )


def fetch_sdss_lensing() -> dict:
    """Fetch SDSS published weak-lensing stacked profiles (lensing observable P1)."""
    return fetch_file(
        SDSS_LENSING_URL,
        "lensing/sdss_dr12_lensing_catalog.fits",
        expected_sha256=SDSS_LENSING_SHA256,
    )


def fetch_lyman_alpha() -> dict:
    """Fetch Lyman-α power-spectrum constraints (small-scale structure check)."""
    return fetch_file(
        LYMAN_ALPHA_CONSTRAINTS_URL,
        "lya/xq100_lya_transmission.fits",
        expected_sha256=LYMAN_ALPHA_SHA256,
    )


# ============================================================================
# WP-E7 Task B (T0-approved 2026-07-27, briefs/T0_DECISIONS_2026_07_27.md D-a):
# scoped acquisition of DESI DR1 (+ SDSS/eBOSS DR16 secondary) LSS/clustering
# catalogs. Priority order per the brief:
#   (i)   SDSS/eBOSS DR16 LSS combined LRG clustering catalog + random (public,
#         no auth, data.sdss.org)
#   (ii)  DESI DR1 LRG clustering (LSS) catalog, public DESI portal
#   (iii) DESI DR1 BGS clustering catalog, if within the 20 GB cap
# Only LSS/clustering catalogs — no spectra, no imaging. Files land in
# data/raw/ (immutable thereafter, hook-enforced: .claude/hooks/prereg_guard.sh).
# ============================================================================

# --- (i) SDSS/eBOSS DR16 LSS LRG clustering catalogs + randoms --------------
# Two distinct, correctly-published DR16 catalogs at the same base URL (see
# briefs/WP_E7_EBOSS_LRG_SAMPLE_IDENTITY_INVESTIGATION_2026_07_28.md; the
# original comment here described the combined sample while the dict pointed
# at the eBOSS-only filenames — that mismatch was the root cause of the
# 174,816-vs-377,458 row-count "mystery"):
#
#   PRIMARY (T0 decision D3, briefs/T0_DECISIONS_2026_07_28_PENDING_ITEMS.md):
#   eBOSS_LRGpCMASS_* — SDSS-recommended combined BOSS+eBOSS LRG sample,
#   377,458 objects, 0.6<z<1.0, 9,493 deg^2 (Ross et al. 2020,
#   arXiv:2007.09000). SDSS DR16 LSS docs recommend it in place of the z>0.6
#   BOSS bin for clustering work — WP-E7's stated purpose.
#
#   SECONDARY/CROSS-CHECK: eBOSS_LRG_* — eBOSS-only sample, 174,816 objects,
#   4,242 deg^2. Already fetched 2026-07-27; kept for eBOSS-specific
#   systematics isolation. File sizes HEAD-verified 2026-07-27:
#   data-NGC   7,747,200 bytes   data-SGC   4,852,800 bytes
#   random-NGC 349,493,760 bytes random-SGC 221,028,480 bytes  (~0.58 GB total)
EBOSS_LSS_BASE_URL = "https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16"

EBOSS_LRGPCMASS_FILES = {
    "eboss_lrgpcmass_clustering_data_ngc": "eBOSS_LRGpCMASS_clustering_data-NGC-vDR16.fits",
    "eboss_lrgpcmass_clustering_data_sgc": "eBOSS_LRGpCMASS_clustering_data-SGC-vDR16.fits",
    "eboss_lrgpcmass_clustering_random_ngc": "eBOSS_LRGpCMASS_clustering_random-NGC-vDR16.fits",
    "eboss_lrgpcmass_clustering_random_sgc": "eBOSS_LRGpCMASS_clustering_random-SGC-vDR16.fits",
}

EBOSS_LRG_FILES = {
    "eboss_lrg_clustering_data_ngc": "eBOSS_LRG_clustering_data-NGC-vDR16.fits",
    "eboss_lrg_clustering_data_sgc": "eBOSS_LRG_clustering_data-SGC-vDR16.fits",
    "eboss_lrg_clustering_random_ngc": "eBOSS_LRG_clustering_random-NGC-vDR16.fits",
    "eboss_lrg_clustering_random_sgc": "eBOSS_LRG_clustering_random-SGC-vDR16.fits",
}


def fetch_eboss_lrgpcmass_clustering() -> dict:
    """SDSS DR16 combined BOSS+eBOSS LRGpCMASS clustering catalog (data +
    random, NGC+SGC). PRIMARY WP-E7 LRG sample per T0 decision D3 2026-07-28.

    Returns a dict keyed by the four EBOSS_LRGPCMASS_FILES entries, each a
    fetch_file() result (or an error dict). No fallback: a failed fetch is
    recorded as-is.
    """
    out = {}
    for key, filename in EBOSS_LRGPCMASS_FILES.items():
        url = f"{EBOSS_LSS_BASE_URL}/{filename}"
        try:
            out[key] = fetch_file(url, f"raw/sdss_eboss_dr16_lss/{filename}")
        except Exception as e:
            logger.error(f"eBOSS LRGpCMASS fetch failed for {key}: {e}")
            out[key] = {"status": "error", "error": str(e), "url": url}
    return out


def fetch_eboss_lrg_clustering() -> dict:
    """SDSS/eBOSS DR16 eBOSS-only LRG clustering catalog (data + random,
    NGC+SGC). SECONDARY/cross-check sample per T0 decision D3 2026-07-28.

    Returns a dict keyed by the four EBOSS_LRG_FILES entries, each a fetch_file()
    result (or an error dict). No fallback: a failed fetch is recorded as-is.
    """
    out = {}
    for key, filename in EBOSS_LRG_FILES.items():
        url = f"{EBOSS_LSS_BASE_URL}/{filename}"
        try:
            out[key] = fetch_file(url, f"raw/sdss_eboss_dr16_lss/{filename}")
        except Exception as e:
            logger.error(f"eBOSS LRG fetch failed for {key}: {e}")
            out[key] = {"status": "error", "error": str(e), "url": url}
    return out


# --- (ii)/(iii) DESI DR1 LRG / BGS clustering (LSS) catalogs ----------------
# arXiv:2404.03000 (BAO/LSS catalog samples); public portal per
# docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md. Internal production name "iron",
# LSScats version v1.5 (best-documented path as of 2026-07-27; not independently
# verified against a live directory listing because the portal is unreachable
# from this environment -- see check below). Filenames follow the documented
# DESI LSS convention: "{TRACER}_{NGC,SGC}_clustering.dat.fits" for data,
# "{TRACER}_{NGC,SGC}_clustering.ran.fits" for randoms.
DESI_DR1_LSS_BASE_URL = (
    "https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/v1.5/clustering"
)

DESI_DR1_LRG_DATA_URL = f"{DESI_DR1_LSS_BASE_URL}/LRG_NGC_clustering.dat.fits"
DESI_DR1_BGS_DATA_URL = f"{DESI_DR1_LSS_BASE_URL}/BGS_BRIGHT_NGC_clustering.dat.fits"

DESI_MANUAL_DOWNLOAD_NOTE = (
    "Manual download: browse "
    "https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/v1.5/clustering/ "
    "(DESI DR1, 'iron' spectroscopic production, LSScats v1.5) from a network that can "
    "reach data.desi.lbl.gov / NERSC (128.55.206.0/24), download the "
    "{TRACER}_{NGC,SGC}_clustering.dat.fits data files and matching "
    "{TRACER}_{NGC,SGC}_clustering.ran.fits random files, compute SHA256, and append a "
    "row to data/MANIFEST.md following the same convention as the eBOSS LRG entries. "
    "Alternative access path (reachable from this environment, not independently used "
    "for this fetch): NOIRLab Astro Data Lab TAP, https://datalab.noirlab.edu/tap, "
    "table desi_dr1 -- whether it re-exposes the LSS clustering/random weight columns "
    "needed for this analysis is unverified."
)


def _fetch_desi_dr1_catalog(url: str, dest_relpath: str, label: str) -> dict:
    """Shared DESI DR1 fetch path: HEAD-check first (never a blind multi-GB
    GET), record an exact failure + manual-download instruction on refusal,
    and do not retry with spoofed headers or scrape around the refusal."""
    check = check_url_reachable(url)
    if not check["reachable"]:
        logger.error(f"{label}: portal unreachable ({check['error']}). Recording refusal.")
        return {
            "status": "error",
            "url": url,
            "error": f"unreachable: {check['error']}",
            "manual_download": DESI_MANUAL_DOWNLOAD_NOTE,
        }
    try:
        return fetch_file(url, dest_relpath)
    except Exception as e:
        logger.error(f"{label}: fetch failed after reachability check: {e}")
        return {"status": "error", "url": url, "error": str(e),
                 "manual_download": DESI_MANUAL_DOWNLOAD_NOTE}


def fetch_desi_dr1_lrg_clustering() -> dict:
    """DESI DR1 LRG clustering (LSS) catalog. HEAD-checked before any GET."""
    return _fetch_desi_dr1_catalog(
        DESI_DR1_LRG_DATA_URL,
        "raw/desi_dr1_lss/LRG_NGC_clustering.dat.fits",
        "DESI DR1 LRG",
    )


def fetch_desi_dr1_bgs_clustering() -> dict:
    """DESI DR1 BGS clustering (LSS) catalog. HEAD-checked before any GET."""
    return _fetch_desi_dr1_catalog(
        DESI_DR1_BGS_DATA_URL,
        "raw/desi_dr1_lss/BGS_BRIGHT_NGC_clustering.dat.fits",
        "DESI DR1 BGS",
    )


# ============================================================================
# WP-E6-BINMAP-C (T1 delegated ruling R2, briefs/T1_DELEGATED_RULINGS_2026_07_31.md,
# executing T0-ratified D1 `dbf1337`): DESI DR1 Lya P1D data release from the
# paper's own Zenodo record (arXiv:2505.07974 Data Availability). The artifact
# is already hash-pinned in data/MANIFEST.md (literature section, 2026-07-27
# entry): file data_points.tar -> the contcorr_v3 FITS whose COVARIANCE HDU is
# the real published covariance. HARD GATE: the extracted FITS SHA-256 must
# equal the MANIFEST-pinned value below BEFORE anything reads the FITS;
# a mismatch raises and nothing downstream may proceed.
# ============================================================================

DESI_DR1_LYA_P1D_ZENODO_TAR_URL = (
    "https://zenodo.org/records/16943723/files/data_points.tar"
)
# Zenodo-published md5 for the parent tar (also recorded in data/MANIFEST.md).
DESI_DR1_LYA_P1D_TAR_MD5 = "33d7fc21bfd3d745ed71a0bbe80ca433"
DESI_DR1_LYA_P1D_FITS_NAME = (
    "desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits"
)
# MANIFEST-pinned SHA-256 of the FITS (data/MANIFEST.md "Source file SHA256",
# 2026-07-27 literature entry). This is the hard gate value.
DESI_DR1_LYA_P1D_FITS_SHA256 = (
    "bbb98dc3d1865a50bb878e949a644604ce729da419db8e7db5adbb532a894857"
)
DESI_DR1_LYA_P1D_RAW_SUBDIR = "raw/desi_dr1_lya_p1d_zenodo"


def _compute_md5(file_path: Path) -> str:
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(1 << 20), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()


def fetch_desi_dr1_lya_p1d_covariance() -> dict:
    """DESI DR1 Lya P1D data release (Zenodo DOI 10.5281/zenodo.16943723):
    fetch data_points.tar, verify its Zenodo-published md5, extract ONLY the
    baseline contcorr_v3 FITS, and hard-gate its SHA-256 against the
    MANIFEST-pinned value. Idempotent: if the FITS is already present with
    the pinned SHA-256, nothing is re-downloaded.

    Returns a fetch_file()-shaped dict describing the FITS (path relative to
    data/, full SHA-256). Raises ValueError on any checksum failure — a hash
    mismatch is a hard stop, never worked around.
    """
    from datetime import datetime

    dest_dir = DATA_DIR / DESI_DR1_LYA_P1D_RAW_SUBDIR
    dest_dir.mkdir(parents=True, exist_ok=True)
    fits_path = dest_dir / DESI_DR1_LYA_P1D_FITS_NAME
    tar_path = dest_dir / "data_points.tar"

    # Idempotency: FITS already present and hash-verified -> cached.
    if fits_path.exists():
        computed = compute_sha256(fits_path)
        if computed == DESI_DR1_LYA_P1D_FITS_SHA256:
            logger.info(f"DESI DR1 Lya P1D FITS already cached + SHA-256 verified: {fits_path}")
            return {
                "url": DESI_DR1_LYA_P1D_ZENODO_TAR_URL,
                "version": "cached",
                "sha256": computed,
                "path": str(fits_path.relative_to(DATA_DIR)),
                "retrieved": datetime.now().isoformat(),
                "status": "cached",
            }
        raise ValueError(
            "HARD-GATE FAILURE (WP-E6-BINMAP-C): cached FITS SHA-256 mismatch: "
            f"got {computed}, MANIFEST pin {DESI_DR1_LYA_P1D_FITS_SHA256}. "
            "Stopping — do not read this file; escalate."
        )

    # Fetch the parent tar (md5-verified against Zenodo's published checksum).
    if not tar_path.exists() or _compute_md5(tar_path) != DESI_DR1_LYA_P1D_TAR_MD5:
        result = fetch_file(DESI_DR1_LYA_P1D_ZENODO_TAR_URL, tar_path)
        logger.info(f"Fetched {tar_path} ({result['status']}), verifying md5...")
    tar_md5 = _compute_md5(tar_path)
    if tar_md5 != DESI_DR1_LYA_P1D_TAR_MD5:
        raise ValueError(
            "HARD-GATE FAILURE (WP-E6-BINMAP-C): data_points.tar md5 mismatch: "
            f"got {tar_md5}, Zenodo published {DESI_DR1_LYA_P1D_TAR_MD5}. "
            "Stopping — escalate."
        )

    # Extract ONLY the baseline FITS member (no blanket extraction).
    import tarfile
    with tarfile.open(tar_path, "r") as tar:
        members = [m for m in tar.getmembers()
                   if m.isfile() and Path(m.name).name == DESI_DR1_LYA_P1D_FITS_NAME]
        if len(members) != 1:
            raise ValueError(
                f"Expected exactly 1 tar member named {DESI_DR1_LYA_P1D_FITS_NAME}, "
                f"found {len(members)}."
            )
        src = tar.extractfile(members[0])
        with open(fits_path, "wb") as out:
            while True:
                chunk = src.read(1 << 20)
                if not chunk:
                    break
                out.write(chunk)

    # HARD GATE: SHA-256 of the extracted FITS vs the MANIFEST pin, BEFORE
    # any consumer reads it.
    computed = compute_sha256(fits_path)
    if computed != DESI_DR1_LYA_P1D_FITS_SHA256:
        raise ValueError(
            "HARD-GATE FAILURE (WP-E6-BINMAP-C): extracted FITS SHA-256 mismatch: "
            f"got {computed}, MANIFEST pin {DESI_DR1_LYA_P1D_FITS_SHA256}. "
            "Stopping — do not read this file; escalate."
        )
    logger.info(f"SHA-256 hard gate PASSED for {fits_path.name}: {computed}")

    return {
        "url": DESI_DR1_LYA_P1D_ZENODO_TAR_URL,
        "version": "retrieved",
        "sha256": computed,
        "path": str(fits_path.relative_to(DATA_DIR)),
        "retrieved": datetime.now().isoformat(),
        "status": "new",
    }


def fetch_all_datasets() -> dict:
    """Fetch all required datasets for Stream 3 observables (P1, P2, nulls),
    plus the WP-E7 Task B scoped acquisition (eBOSS LRG clustering + DESI DR1
    LRG/BGS clustering attempts).

    Returns a flat dict of dataset_name -> fetch_file()-shaped result (or an
    error dict). The four eboss_lrg_* keys are unpacked from
    fetch_eboss_lrg_clustering()'s nested dict so every entry here is a single
    dataset, matching data/MANIFEST.md's one-row-per-dataset convention.
    """
    results = {}
    fetchers = {
        "nanograv_15yr": fetch_nanograv_15yr,
        "epta_dr2": fetch_epta_dr2,
        "sdss_lensing": fetch_sdss_lensing,
        "lyman_alpha": fetch_lyman_alpha,
    }

    for name, fetcher in fetchers.items():
        try:
            results[name] = fetcher()
        except Exception as e:
            logger.error(f"Failed to fetch {name}: {e}")
            results[name] = {"status": "error", "error": str(e)}

    try:
        results.update(fetch_eboss_lrgpcmass_clustering())
    except Exception as e:
        logger.error(f"eBOSS LRGpCMASS clustering fetch group failed: {e}")
        for key in EBOSS_LRGPCMASS_FILES:
            results.setdefault(key, {"status": "error", "error": str(e)})

    try:
        results.update(fetch_eboss_lrg_clustering())
    except Exception as e:
        logger.error(f"eBOSS LRG clustering fetch group failed: {e}")
        for key in EBOSS_LRG_FILES:
            results.setdefault(key, {"status": "error", "error": str(e)})

    for name, fetcher in {
        "desi_dr1_lrg_clustering": fetch_desi_dr1_lrg_clustering,
        "desi_dr1_bgs_clustering": fetch_desi_dr1_bgs_clustering,
        "desi_dr1_lya_p1d_covariance_fits": fetch_desi_dr1_lya_p1d_covariance,
    }.items():
        try:
            results[name] = fetcher()
        except Exception as e:
            logger.error(f"Failed to fetch {name}: {e}")
            results[name] = {"status": "error", "error": str(e)}

    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    results = fetch_all_datasets()
    print(json.dumps(results, indent=2))
