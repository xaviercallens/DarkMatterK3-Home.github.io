# data/MANIFEST.md — Dataset Provenance Ledger

**Status:** Updated 2026-07-25T11:19:43.695710. 7 dataset(s) fetched (real SDSS +
Euclid queries via `scripts/fetch_survey_astroquery.py`, gate G1 open). This is
engineering data-access prep only — gate G1-L (TEST/FIT labeling authority)
remains closed (`NO_PREDICTION_BRANCH.md` §8.5); nothing here is a comparison
result. Data files live on the external disk (see paths below), not in git.

Updated automatically by `scripts/fetch_data.py`. Never hand-edit an entry
after it's written — a correction is fetching a new version and appending a
new row, not editing the old one.

| Dataset | URL | Release / version | SHA256 | Retrieved | Used by |
|---|---|---|---|---|---|
| sdss_cosmos | astroquery.sdss.SDSS.query_region(ra=150.1, dec=2.2, width=10.0arcmin, height=10.0arcmin, spectro=False) | SDSS (astroquery default DR, live query 2026-07-25) | cf86a84a3d0b16f8... | 2026-07-25T11:19:38.063988+00:00 | engineering prep (G1-scope; no G1-L target pinned) |
| sdss_stripe82_center | astroquery.sdss.SDSS.query_region(ra=0.0, dec=0.0, width=10.0arcmin, height=10.0arcmin, spectro=False) | SDSS (astroquery default DR, live query 2026-07-25) | f1e3a610f47acb89... | 2026-07-25T11:19:38.160618+00:00 | engineering prep (G1-scope; no G1-L target pinned) |
| sdss_coma_cluster | astroquery.sdss.SDSS.query_region(ra=194.95, dec=27.98, width=10.0arcmin, height=10.0arcmin, spectro=False) | SDSS (astroquery default DR, live query 2026-07-25) | 2e31288c5fba0adb... | 2026-07-25T11:19:38.172517+00:00 | engineering prep (G1-scope; no G1-L target pinned) |
| sdss_docs_example | astroquery.sdss.SDSS.query_region(ra=2.0235, dec=14.8398, width=10.0arcmin, height=10.0arcmin, spectro=False) | SDSS (astroquery default DR, live query 2026-07-25) | cc4a0448a68a8503... | 2026-07-25T11:19:38.196468+00:00 | engineering prep (G1-scope; no G1-L target pinned) |
| euclid_edf_north | SELECT TOP 2000 object_id, right_ascension, declination, ellipticity, ellipticity_err, semimajor_axis, position_angle, flux_vis_2fwhm_aper, fluxerr_vis_2fwhm_aper, point_like_flag, extended_flag, det_quality_flag, vis_det FROM catalogue.mer_catalogue WHERE 1=CONTAINS(POINT('ICRS', right_ascension, declination), CIRCLE('ICRS', 267.7808, 65.5308, 0.2)) | Euclid public MER catalogue (PDR, live query 2026-07-25) | 5d152c0df2f75be9... | 2026-07-25T11:19:41.030182+00:00 | engineering prep (G1-scope; no G1-L target pinned) |
| euclid_edf_fornax | SELECT TOP 2000 object_id, right_ascension, declination, ellipticity, ellipticity_err, semimajor_axis, position_angle, flux_vis_2fwhm_aper, fluxerr_vis_2fwhm_aper, point_like_flag, extended_flag, det_quality_flag, vis_det FROM catalogue.mer_catalogue WHERE 1=CONTAINS(POINT('ICRS', right_ascension, declination), CIRCLE('ICRS', 53.13, -28.1, 0.2)) | Euclid public MER catalogue (PDR, live query 2026-07-25) | c3fdfde2f16b4414... | 2026-07-25T11:19:42.493240+00:00 | engineering prep (G1-scope; no G1-L target pinned) |
| euclid_edf_south | SELECT TOP 2000 object_id, right_ascension, declination, ellipticity, ellipticity_err, semimajor_axis, position_angle, flux_vis_2fwhm_aper, fluxerr_vis_2fwhm_aper, point_like_flag, extended_flag, det_quality_flag, vis_det FROM catalogue.mer_catalogue WHERE 1=CONTAINS(POINT('ICRS', right_ascension, declination), CIRCLE('ICRS', 61.0, -48.4, 0.2)) | Euclid public MER catalogue (PDR, live query 2026-07-25) | cfeceb9a76d96c5c... | 2026-07-25T11:19:43.693023+00:00 | engineering prep (G1-scope; no G1-L target pinned) |

## Full-fidelity provenance — scripts/fetch_survey_astroquery.py (2026-07-25T11:19:43.696369+00:00)

- **sdss_cosmos** — rows: 1068, path: `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/sdss/sdss_cosmos.csv`, sha256: `cf86a84a3d0b16f8489d8a2bb27e88656b882e1131c7c4e19a92520140b7c915`, retrieved: 2026-07-25T11:19:38.063988+00:00
  query: `astroquery.sdss.SDSS.query_region(ra=150.1, dec=2.2, width=10.0arcmin, height=10.0arcmin, spectro=False)`
- **sdss_stripe82_center** — rows: 14007, path: `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/sdss/sdss_stripe82_center.csv`, sha256: `f1e3a610f47acb89f0891bfd8de78b8ebbebb8d05dbb267f6465a92160fd05f1`, retrieved: 2026-07-25T11:19:38.160618+00:00
  query: `astroquery.sdss.SDSS.query_region(ra=0.0, dec=0.0, width=10.0arcmin, height=10.0arcmin, spectro=False)`
- **sdss_coma_cluster** — rows: 822, path: `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/sdss/sdss_coma_cluster.csv`, sha256: `2e31288c5fba0adb88e10eadbb1a7272ed2fd53c2ede21f05a1cceb087b38b03`, retrieved: 2026-07-25T11:19:38.172517+00:00
  query: `astroquery.sdss.SDSS.query_region(ra=194.95, dec=27.98, width=10.0arcmin, height=10.0arcmin, spectro=False)`
- **sdss_docs_example** — rows: 3035, path: `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/sdss/sdss_docs_example.csv`, sha256: `cc4a0448a68a850365a19c23b2221dbe00d4d8868ef99f2a677bcae2c3497a90`, retrieved: 2026-07-25T11:19:38.196468+00:00
  query: `astroquery.sdss.SDSS.query_region(ra=2.0235, dec=14.8398, width=10.0arcmin, height=10.0arcmin, spectro=False)`
- **euclid_edf_north** — rows: 2000, path: `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid/euclid_edf_north.csv`, sha256: `5d152c0df2f75be9163064cfa501168121a7da37302a53dbee52c3d82d8e74f5`, retrieved: 2026-07-25T11:19:41.030182+00:00
  query: `SELECT TOP 2000 object_id, right_ascension, declination, ellipticity, ellipticity_err, semimajor_axis, position_angle, flux_vis_2fwhm_aper, fluxerr_vis_2fwhm_aper, point_like_flag, extended_flag, det_quality_flag, vis_det FROM catalogue.mer_catalogue WHERE 1=CONTAINS(POINT('ICRS', right_ascension, declination), CIRCLE('ICRS', 267.7808, 65.5308, 0.2))`
- **euclid_edf_fornax** — rows: 2000, path: `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid/euclid_edf_fornax.csv`, sha256: `c3fdfde2f16b4414f4390ecd84339bcb5f13d24ab2abcfb2bd678c1b6ebe00c6`, retrieved: 2026-07-25T11:19:42.493240+00:00
  query: `SELECT TOP 2000 object_id, right_ascension, declination, ellipticity, ellipticity_err, semimajor_axis, position_angle, flux_vis_2fwhm_aper, fluxerr_vis_2fwhm_aper, point_like_flag, extended_flag, det_quality_flag, vis_det FROM catalogue.mer_catalogue WHERE 1=CONTAINS(POINT('ICRS', right_ascension, declination), CIRCLE('ICRS', 53.13, -28.1, 0.2))`
- **euclid_edf_south** — rows: 2000, path: `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid/euclid_edf_south.csv`, sha256: `cfeceb9a76d96c5c745376bdf79d5bf97ed0479857508e0d4629c8509d9f36fe`, retrieved: 2026-07-25T11:19:43.693023+00:00
  query: `SELECT TOP 2000 object_id, right_ascension, declination, ellipticity, ellipticity_err, semimajor_axis, position_angle, flux_vis_2fwhm_aper, fluxerr_vis_2fwhm_aper, point_like_flag, extended_flag, det_quality_flag, vis_det FROM catalogue.mer_catalogue WHERE 1=CONTAINS(POINT('ICRS', right_ascension, declination), CIRCLE('ICRS', 61.0, -48.4, 0.2))`
