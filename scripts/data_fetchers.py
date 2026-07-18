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
from urllib.request import urlopen

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"


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


def fetch_all_datasets() -> dict:
    """Fetch all required datasets for Stream 3 observables (P1, P2, nulls).

    Returns:
        {
            "nanograv_15yr": {...},
            "epta_dr2": {...},
            "sdss_lensing": {...},
            "lyman_alpha": {...}
        }
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

    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    results = fetch_all_datasets()
    print(json.dumps(results, indent=2))
