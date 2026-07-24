# data/MANIFEST_S3.md — Stream 3 Observable Datasets

**Status:** WP S3-01 in progress (2026-07-24)
**Rule:** Every dataset entry must have: URL (exact, versioned), fetch date, SHA256 (computed, not transcribed), retrieval method.
**Contract:** This is the ONLY admissible source for dataset references in any comparison code or report.

## P1 Observable (Pulsar-Timing Arrays)

### NANOGrav 15-Year Data Release
| Field | Value |
|---|---|
| Observable | P1 (PTA free-spectrum posteriors) |
| Source | Agazie et al. 2023, NANOGrav Collaboration public data release |
| URL | https://data.nanogrv.org/public/nanograv_15yr_dataset.tar.gz (or current release path — to be verified) |
| Version/Release tag | NANOGrav 15-yr DR |
| Retrieved | 2026-07-24 (pending) |
| SHA256 | TBD (compute on fetch via `sha256sum`) |
| Format | FITS or HDF5 (verify on download) |
| Retrieval method | `curl -L <URL> -o data/stream3_datasets/nanograv_15yr.tar.gz && sha256sum ...` |
| Notes | Spectrum or posterior samples? Exact format TBD from docs. |

### EPTA Data Release 2
| Field | Value |
|---|---|
| Observable | P1 (PTA free-spectrum posteriors) |
| Source | Liu et al. 2023, EPTA Collaboration |
| URL | https://gitlab.in2p3.fr/epta/public_releases (or GitHub mirror — exact path to verify) |
| Version/Release tag | EPTA DR2 |
| Retrieved | 2026-07-24 (pending) |
| SHA256 | TBD |
| Format | TBD |
| Retrieval method | TBD (check if git-clone or direct download) |
| Notes | Cross-check overlap with NANOGrav (same pulsars?); if so, merge procedure TBD. |

## P2 Observable (Weak Lensing Halo Profiles)

### SDSS Stacked Weak-Lensing Profiles
| Field | Value |
|---|---|
| Observable | P2 (halo profile r_c vs M_halo) |
| Source | Mandelbaum et al. 2013/2020, SDSS weak-lensing public tables |
| URL | https://svn.sdss.org/public/sdss/data/sdss3/lsst/lensing/ (or direct data.sdss.org link — verify) |
| Version/Release tag | SDSS weak-lensing catalog (version TBD) |
| Retrieved | 2026-07-24 (pending) |
| SHA256 | TBD |
| Format | FITS or ASCII table |
| Retrieval method | TBD |
| Notes | Dwarf vs intermediate vs high-mass bins; check which mass ranges are available. |

### Dark Energy Survey Year 3 Lensing
| Field | Value |
|---|---|
| Observable | P2 (halo profile) |
| Source | Leauthaud et al. 2024, DES public release |
| URL | https://des.ncsa.illinois.edu/ (or Zenodo mirror) |
| Version/Release tag | DES Y3 |
| Retrieved | 2026-07-24 (pending) |
| SHA256 | TBD |
| Format | TBD |
| Retrieval method | TBD |
| Notes | Cross-check with SDSS profiles; merge procedure TBD. |

### Euclid Early Release Observations (if available public)
| Field | Value |
|---|---|
| Observable | P2 (halo profile, future) |
| Source | ESA/Euclid public archive |
| URL | https://www.esa.int/Euclid (to find data portal) |
| Version/Release tag | Euclid ERO (if released by 2026-07-24) |
| Retrieved | TBD (may not be available yet) |
| SHA256 | TBD |
| Format | TBD |
| Retrieval method | TBD |
| Notes | Placeholder; depends on Euclid public-data timeline. Check status before fetching. |

## Lyman-α Null Test Observable

### SDSS DR12 Lyman-α Power Spectrum
| Field | Value |
|---|---|
| Observable | Lyman-α null test (power spectrum, high-z universe) |
| Source | Palanque-Delabrouille et al. 2015, SDSS DR12 public archive |
| URL | https://svn.sdss.org/public/sdss/data/sdss3/boss/lya/ (or direct link — verify) |
| Version/Release tag | SDSS DR12 Lyman-α |
| Retrieved | 2026-07-24 (pending) |
| SHA256 | TBD |
| Format | HDF5 or FITS |
| Retrieval method | TBD |
| Notes | High-z (z=2-4) forest power; exact format/redshift range TBD. |

### DESI Early Data Release
| Field | Value |
|---|---|
| Observable | Lyman-α null test (DESI spectra, future) |
| Source | DESI Collaboration, public EDR |
| URL | https://github.com/desisurvey/desicmx/releases (or data.desi.lbl.gov) |
| Version/Release tag | DESI EDR |
| Retrieved | TBD (pending availability) |
| SHA256 | TBD |
| Format | TBD |
| Retrieval method | TBD |
| Notes | Placeholder; DESI EDR timeline TBD. Check availability. |

---

## Validation / CI Contract
- Every entry **retrieved** by the time this section is removed (WP S3-01 completion).
- **SHA256 is computed, not transcribed** — `sha256sum` output piped directly into this file.
- **No entry without a retrieval date** — timestamps are the audit trail.
- **Fetch script is idempotent** — re-running must match checksums or no-op.
- **CI check:** on every commit touching a dataset path, re-hash against MANIFEST_S3.md entry. FAIL if mismatch.

---

`Generated-by: Stream 3 (Haiku T1, WP S3-01 scaffold) | Verified-by: (pending actual fetches) | Reviewed-by: pending Xavier`
