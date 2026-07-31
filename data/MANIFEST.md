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
| sdss_z_cosmos | astroquery.sdss.SDSS.query_region(ra=150.1, dec=2.2, width=10.0arcmin, height=10.0arcmin, spectro=True) | SDSS spectroscopic (astroquery default DR, live query 2026-07-25) | 45fa2b9cf9a2643d... | 2026-07-25T12:36:23.901468+00:00 | WP-R5 3D field prep (G1-scope; no G1-L target pinned) |
| sdss_z_stripe82_center | astroquery.sdss.SDSS.query_region(ra=0.0, dec=0.0, width=10.0arcmin, height=10.0arcmin, spectro=True) | SDSS spectroscopic (astroquery default DR, live query 2026-07-25) | 39024d048ca9513a... | 2026-07-25T12:36:23.911040+00:00 | WP-R5 3D field prep (G1-scope; no G1-L target pinned) |
| sdss_z_coma_cluster | astroquery.sdss.SDSS.query_region(ra=194.95, dec=27.98, width=10.0arcmin, height=10.0arcmin, spectro=True) | SDSS spectroscopic (astroquery default DR, live query 2026-07-25) | 7b7c753e9a116831... | 2026-07-25T12:36:23.918799+00:00 | WP-R5 3D field prep (G1-scope; no G1-L target pinned) |
| sdss_z_docs_example | astroquery.sdss.SDSS.query_region(ra=2.0235, dec=14.8398, width=10.0arcmin, height=10.0arcmin, spectro=True) | SDSS spectroscopic (astroquery default DR, live query 2026-07-25) | 454e839dd3c3cf0b... | 2026-07-25T12:36:23.926329+00:00 | WP-R5 3D field prep (G1-scope; no G1-L target pinned) |
| euclid_z_edf_north | SELECT TOP 2000 m.object_id, m.right_ascension, m.declination, p.phz_median, p.phz_mode_1 FROM catalogue.mer_catalogue AS m JOIN catalogue.phz_photo_z AS p ON m.object_id = p.object_id WHERE 1=CONTAINS(POINT('ICRS', m.right_ascension, m.declination), CIRCLE('ICRS', 267.7808, 65.5308, 0.2)) | Euclid public MER JOIN phz_photo_z (PDR, live query 2026-07-25) | 8b5b287f3f031656... | 2026-07-25T12:36:32.151409+00:00 | WP-R5 3D field prep (G1-scope; no G1-L target pinned) |
| euclid_z_edf_fornax | SELECT TOP 2000 m.object_id, m.right_ascension, m.declination, p.phz_median, p.phz_mode_1 FROM catalogue.mer_catalogue AS m JOIN catalogue.phz_photo_z AS p ON m.object_id = p.object_id WHERE 1=CONTAINS(POINT('ICRS', m.right_ascension, m.declination), CIRCLE('ICRS', 53.13, -28.1, 0.2)) | Euclid public MER JOIN phz_photo_z (PDR, live query 2026-07-25) | 4095efd8603519f4... | 2026-07-25T12:36:37.032725+00:00 | WP-R5 3D field prep (G1-scope; no G1-L target pinned) |
| euclid_z_edf_south | SELECT TOP 2000 m.object_id, m.right_ascension, m.declination, p.phz_median, p.phz_mode_1 FROM catalogue.mer_catalogue AS m JOIN catalogue.phz_photo_z AS p ON m.object_id = p.object_id WHERE 1=CONTAINS(POINT('ICRS', m.right_ascension, m.declination), CIRCLE('ICRS', 61.0, -48.4, 0.2)) | Euclid public MER JOIN phz_photo_z (PDR, live query 2026-07-25) | 7fe629517de7a620... | 2026-07-25T12:36:41.472134+00:00 | WP-R5 3D field prep (G1-scope; no G1-L target pinned) |

## Full-fidelity provenance — scripts/fetch_survey_redshifts.py (WP-R5, 2026-07-25T12:36:41.474479+00:00)

- **sdss_z_cosmos** — rows: 8, path: `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/sdss_z/sdss_z_cosmos.csv`, sha256: `45fa2b9cf9a2643dfd51d17b15bc45a5ee06c1453481003a6fdb43be40476731`, retrieved: 2026-07-25T12:36:23.901468+00:00
  query: `astroquery.sdss.SDSS.query_region(ra=150.1, dec=2.2, width=10.0arcmin, height=10.0arcmin, spectro=True)`
- **sdss_z_stripe82_center** — rows: 27, path: `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/sdss_z/sdss_z_stripe82_center.csv`, sha256: `39024d048ca9513af0a04d09598cd8d5a49ff6def422cf45f74ad4a056806e96`, retrieved: 2026-07-25T12:36:23.911040+00:00
  query: `astroquery.sdss.SDSS.query_region(ra=0.0, dec=0.0, width=10.0arcmin, height=10.0arcmin, spectro=True)`
- **sdss_z_coma_cluster** — rows: 50, path: `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/sdss_z/sdss_z_coma_cluster.csv`, sha256: `7b7c753e9a116831b8fe820054d85ad57a3c43d1a4ef7d8716a38a22fa3074ea`, retrieved: 2026-07-25T12:36:23.918799+00:00
  query: `astroquery.sdss.SDSS.query_region(ra=194.95, dec=27.98, width=10.0arcmin, height=10.0arcmin, spectro=True)`
- **sdss_z_docs_example** — rows: 7, path: `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/sdss_z/sdss_z_docs_example.csv`, sha256: `454e839dd3c3cf0b7dba875779e7fb4be379b2f31a0f8d79c2927b22ce8d9bb5`, retrieved: 2026-07-25T12:36:23.926329+00:00
  query: `astroquery.sdss.SDSS.query_region(ra=2.0235, dec=14.8398, width=10.0arcmin, height=10.0arcmin, spectro=True)`
- **euclid_z_edf_north** — rows: 2000, path: `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid_z/euclid_z_edf_north.csv`, sha256: `8b5b287f3f03165660e6232b904ee264e705788ffd60e67f54169ea2dddac2be`, retrieved: 2026-07-25T12:36:32.151409+00:00
  query: `SELECT TOP 2000 m.object_id, m.right_ascension, m.declination, p.phz_median, p.phz_mode_1 FROM catalogue.mer_catalogue AS m JOIN catalogue.phz_photo_z AS p ON m.object_id = p.object_id WHERE 1=CONTAINS(POINT('ICRS', m.right_ascension, m.declination), CIRCLE('ICRS', 267.7808, 65.5308, 0.2))`
- **euclid_z_edf_fornax** — rows: 2000, path: `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid_z/euclid_z_edf_fornax.csv`, sha256: `4095efd8603519f422bbbdef277228b9a7741345eb4b60ca14d33d085acbc484`, retrieved: 2026-07-25T12:36:37.032725+00:00
  query: `SELECT TOP 2000 m.object_id, m.right_ascension, m.declination, p.phz_median, p.phz_mode_1 FROM catalogue.mer_catalogue AS m JOIN catalogue.phz_photo_z AS p ON m.object_id = p.object_id WHERE 1=CONTAINS(POINT('ICRS', m.right_ascension, m.declination), CIRCLE('ICRS', 53.13, -28.1, 0.2))`
- **euclid_z_edf_south** — rows: 2000, path: `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid_z/euclid_z_edf_south.csv`, sha256: `7fe629517de7a620426a60364c47b2f96306b592b6e03752866f417aca6d0b4b`, retrieved: 2026-07-25T12:36:41.472134+00:00
  query: `SELECT TOP 2000 m.object_id, m.right_ascension, m.declination, p.phz_median, p.phz_mode_1 FROM catalogue.mer_catalogue AS m JOIN catalogue.phz_photo_z AS p ON m.object_id = p.object_id WHERE 1=CONTAINS(POINT('ICRS', m.right_ascension, m.declination), CIRCLE('ICRS', 61.0, -48.4, 0.2))`
| nanograv_15yr | ERROR | HTTP Error 404: Not Found | | | |
| epta_dr2 | ERROR | HTTP Error 404: NOT FOUND | | | |
| sdss_lensing | ERROR | HTTP Error 404: Not Found | | | |
| lyman_alpha | ERROR | HTTP Error 404: Not Found | | | |
| eboss_lrg_clustering_data_ngc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_data-NGC-vDR16.fits | retrieved | 5eb836c7e6e69eb2... | 2026-07-27T07:57:31.984722 | WP-E7 Task B (T0-approved 2026-07-27; DESI/eBOSS resolvability follow-on prep) |
| eboss_lrg_clustering_data_sgc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_data-SGC-vDR16.fits | retrieved | aec4b569ad957d82... | 2026-07-27T07:57:32.730485 | WP-E7 Task B (T0-approved 2026-07-27; DESI/eBOSS resolvability follow-on prep) |
| eboss_lrg_clustering_random_ngc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_random-NGC-vDR16.fits | retrieved | 5da0bf41e2679683... | 2026-07-27T07:57:54.447234 | WP-E7 Task B (T0-approved 2026-07-27; DESI/eBOSS resolvability follow-on prep) |
| eboss_lrg_clustering_random_sgc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_random-SGC-vDR16.fits | retrieved | 4aabcaa99cc2855d... | 2026-07-27T07:58:02.269239 | WP-E7 Task B (T0-approved 2026-07-27; DESI/eBOSS resolvability follow-on prep) |
| desi_dr1_lrg_clustering | ERROR | unreachable: <urlopen error [Errno 113] No route to host> | | | |
| desi_dr1_bgs_clustering | ERROR | unreachable: <urlopen error [Errno 113] No route to host> | | | |

## Full-fidelity provenance — scripts/fetch_data.py (WP-E7 Task B, 2026-07-27T07:58:43.727763+00:00)

- **nanograv_15yr**: ERROR — HTTP Error 404: Not Found (url: n/a)
- **epta_dr2**: ERROR — HTTP Error 404: NOT FOUND (url: n/a)
- **sdss_lensing**: ERROR — HTTP Error 404: Not Found (url: n/a)
- **lyman_alpha**: ERROR — HTTP Error 404: Not Found (url: n/a)
- **eboss_lrg_clustering_data_ngc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRG_clustering_data-NGC-vDR16.fits`, sha256: `5eb836c7e6e69eb2cbc3b2dfe2f27826b6e5ac59d1c87e279a81a916f6edc77e`, retrieved: 2026-07-27T07:57:31.984722, status: new
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_data-NGC-vDR16.fits`
- **eboss_lrg_clustering_data_sgc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRG_clustering_data-SGC-vDR16.fits`, sha256: `aec4b569ad957d829aa8337bf2c7d00e25dc777e2e5849552893cbead70071dc`, retrieved: 2026-07-27T07:57:32.730485, status: new
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_data-SGC-vDR16.fits`
- **eboss_lrg_clustering_random_ngc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRG_clustering_random-NGC-vDR16.fits`, sha256: `5da0bf41e267968310ada55ea3bf27c9a3808bba77050e66c54d84dec62b6281`, retrieved: 2026-07-27T07:57:54.447234, status: new
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_random-NGC-vDR16.fits`
- **eboss_lrg_clustering_random_sgc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRG_clustering_random-SGC-vDR16.fits`, sha256: `4aabcaa99cc2855d38eddd5fac903d3281e9436e5ba5b8c230050db3da92d230`, retrieved: 2026-07-27T07:58:02.269239, status: new
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_random-SGC-vDR16.fits`
- **desi_dr1_lrg_clustering**: ERROR — unreachable: <urlopen error [Errno 113] No route to host> (url: https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/v1.5/clustering/LRG_NGC_clustering.dat.fits)
  Manual-download instruction: Manual download: browse https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/v1.5/clustering/ (DESI DR1, 'iron' spectroscopic production, LSScats v1.5) from a network that can reach data.desi.lbl.gov / NERSC (128.55.206.0/24), download the {TRACER}_{NGC,SGC}_clustering.dat.fits data files and matching {TRACER}_{NGC,SGC}_clustering.ran.fits random files, compute SHA256, and append a row to data/MANIFEST.md following the same convention as the eBOSS LRG entries. Alternative access path (reachable from this environment, not independently used for this fetch): NOIRLab Astro Data Lab TAP, https://datalab.noirlab.edu/tap, table desi_dr1 -- whether it re-exposes the LSS clustering/random weight columns needed for this analysis is unverified.
- **desi_dr1_bgs_clustering**: ERROR — unreachable: <urlopen error [Errno 113] No route to host> (url: https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/v1.5/clustering/BGS_BRIGHT_NGC_clustering.dat.fits)
  Manual-download instruction: Manual download: browse https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/v1.5/clustering/ (DESI DR1, 'iron' spectroscopic production, LSScats v1.5) from a network that can reach data.desi.lbl.gov / NERSC (128.55.206.0/24), download the {TRACER}_{NGC,SGC}_clustering.dat.fits data files and matching {TRACER}_{NGC,SGC}_clustering.ran.fits random files, compute SHA256, and append a row to data/MANIFEST.md following the same convention as the eBOSS LRG entries. Alternative access path (reachable from this environment, not independently used for this fetch): NOIRLab Astro Data Lab TAP, https://datalab.noirlab.edu/tap, table desi_dr1 -- whether it re-exposes the LSS clustering/random weight columns needed for this analysis is unverified.

**Integrity check (2026-07-27T07:58:43.928388+00:00):** eboss_lrg_clustering_data_ngc + eboss_lrg_clustering_data_sgc row-count total = 174816; published (docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md §3, arXiv:2007.09000) = 377458. Verdict: MISMATCH.

## Literature derived tables (`data/literature/`, git-COMMITTED — small, published, not raw survey data)

These are small (MB-scale or smaller) machine-readable tables transcribed/extracted
directly from a published paper's own accompanying data release — not a raw survey
catalog, so the `data/raw/` gitignore rule (rule 2, `CLAUDE.md`) does not apply. Fetched
for WP-E6b (`briefs/T0_DECISIONS_2026_07_27.md` D-e).

- **desi_dr1_lya_p1d_2026_07_27.csv** — DESI DR1 Lyman-α 1D flux power spectrum, baseline
  QMLE estimator, metal (SB1) subtracted, continuum-corrected (arXiv:2505.07974, "DESI DR1
  Lyα Forest 1D Power Spectrum"). 1020 rows = 12 redshift bins (z = 2.2–4.4, Δz = 0.2; the
  paper's own z=2.0 and z=4.6 edge bins are already dropped upstream) × 85 k bins (k =
  2.5×10⁻⁴–5.27×10⁻² s/km). Columns: `z, k_s_per_km, p1d_kms, e_stat_kms, e_syst_kms,
  e_total_kms, pfid_kms` — `e_total_kms` is `E_PK` from the source FITS and was verified
  in-session to equal `sqrt(e_stat_kms² + e_syst_kms²)` and `sqrt(diag(COVARIANCE))`
  exactly (max relative discrepancy ~4×10⁻¹⁶, floating-point noise). `pfid_kms` is the
  paper's own fiducial/smooth P1D model (`PFID` column) used to build its covariance
  matrix. The paper calls this a "cosmologically blind" measurement (analysis choices
  fixed before looking at cosmological-parameter implications) — a methodology note, not
  a data-quality caveat.
  - **Source:** paper's own Zenodo data release, DOI 10.5281/zenodo.16943723 (linked from
    the paper's "Data Availability" paragraph, verified against the arXiv source
    `main.tex`), file `data_points.tar` →
    `desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits`, HDU
    `P1D_BLIND` (+ `COVARIANCE`, cross-checked, not stored here — only the diagonal
    is needed and is already carried in `e_total_kms`).
  - **Source file SHA256:** `bbb98dc3d1865a50bb878e949a644604ce729da419db8e7db5adbb532a894857`
    (`desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits`, matches Zenodo's
    published md5 `33d7fc21bfd3d745ed71a0bbe80ca433` for the parent `data_points.tar`).
  - **Derived CSV SHA256:** `ba2cbd746a13931d7a487dbe36002544241afe3233c59e1cd25025d30d4887ed`
  - **Retrieved:** 2026-07-27 (this session), via direct `curl` to `arxiv.org` (e-print
    source, to find the data-availability statement) and `zenodo.org` (data file itself);
    both hosts reachable from this environment (unlike `data.desi.lbl.gov`, which remains
    blocked per the WP-E7 fetch log above).
  - **Used by:** WP-E6b (`pipeline/wp_e6b_lya.py`, `scripts/wp_e6b_lya_adequacy_preflight.py`,
    `docs/WP_E6B_LYA_ADEQUACY_PREFLIGHT_2026_07_27.md`). ENGINEERING pre-flight only — no
    TEST/FIT label; ratio-statistic uses `e_total_kms / p1d_kms` as the published relative
    error, restricted in-code to the paper's stated validity range (**§4.1** of the paper,
    "recommended k cuts" — section number re-verified against the arXiv HTML during the
    WP-E6b audit, correcting an earlier "§4.3" in this entry: k > 10⁻³ s/km; k < 0.5π/R_z
    with R_z = cΔλ/((1+z)λ_Lyα), Δλ = 0.8 Å). 755 of the 1020 tabulated bins survive these
    cuts (pinned mechanically in `pipeline/tests/test_wp_e6b_lya.py`).
  - eBOSS DR14 Chabanier et al. 2019 (arXiv:1812.03554) fallback was **not fetched**: its
    arXiv source package contains only TeX/plots (no machine-readable table; the paper
    states its full P1D table is "available online as fits files in the accompanying
    material attached to the paper" — a journal/JCAP-hosted supplement, not in the arXiv
    package or an obvious Zenodo record), and the DESI DR1 primary fetch above succeeded,
    so the fallback path was not needed this session.
| nanograv_15yr | ERROR | HTTP Error 404: Not Found | | | |
| epta_dr2 | ERROR | HTTP Error 404: NOT FOUND | | | |
| sdss_lensing | ERROR | HTTP Error 404: Not Found | | | |
| lyman_alpha | ERROR | HTTP Error 404: Not Found | | | |
| eboss_lrgpcmass_clustering_data_ngc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRGpCMASS_clustering_data-NGC-vDR16.fits | retrieved | 4059343f572f10d8... | 2026-07-28T16:21:24.901949 | unknown |
| eboss_lrgpcmass_clustering_data_sgc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRGpCMASS_clustering_data-SGC-vDR16.fits | retrieved | ff2398f3d963124b... | 2026-07-28T16:21:32.567684 | unknown |
| eboss_lrgpcmass_clustering_random_ngc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRGpCMASS_clustering_random-NGC-vDR16.fits | retrieved | 3310efb5e279a988... | 2026-07-28T16:25:54.409187 | unknown |
| eboss_lrgpcmass_clustering_random_sgc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRGpCMASS_clustering_random-SGC-vDR16.fits | retrieved | 57977bf3cb320dc6... | 2026-07-28T16:28:18.416468 | unknown |
| eboss_lrg_clustering_data_ngc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_data-NGC-vDR16.fits | cached | 5eb836c7e6e69eb2... | 2026-07-28T16:28:18.697339 | WP-E7 Task B (T0-approved 2026-07-27; DESI/eBOSS resolvability follow-on prep) |
| eboss_lrg_clustering_data_sgc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_data-SGC-vDR16.fits | cached | aec4b569ad957d82... | 2026-07-28T16:28:18.750510 | WP-E7 Task B (T0-approved 2026-07-27; DESI/eBOSS resolvability follow-on prep) |
| eboss_lrg_clustering_random_ngc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_random-NGC-vDR16.fits | cached | 5da0bf41e2679683... | 2026-07-28T16:28:23.157899 | WP-E7 Task B (T0-approved 2026-07-27; DESI/eBOSS resolvability follow-on prep) |
| eboss_lrg_clustering_random_sgc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_random-SGC-vDR16.fits | cached | 4aabcaa99cc2855d... | 2026-07-28T16:28:25.327129 | WP-E7 Task B (T0-approved 2026-07-27; DESI/eBOSS resolvability follow-on prep) |
| desi_dr1_lrg_clustering | ERROR | unreachable: HTTP Error 404: Not Found | | | |
| desi_dr1_bgs_clustering | ERROR | unreachable: HTTP Error 404: Not Found | | | |

## Full-fidelity provenance — scripts/fetch_data.py (WP-E7 Task B, 2026-07-28T16:28:25.402858+00:00)

- **nanograv_15yr**: ERROR — HTTP Error 404: Not Found (url: n/a)
- **epta_dr2**: ERROR — HTTP Error 404: NOT FOUND (url: n/a)
- **sdss_lensing**: ERROR — HTTP Error 404: Not Found (url: n/a)
- **lyman_alpha**: ERROR — HTTP Error 404: Not Found (url: n/a)
- **eboss_lrgpcmass_clustering_data_ngc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRGpCMASS_clustering_data-NGC-vDR16.fits`, sha256: `4059343f572f10d831ac6d524ebc53e0150f9d8772df41e64a664f89ddf990ff`, retrieved: 2026-07-28T16:21:24.901949, status: new
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRGpCMASS_clustering_data-NGC-vDR16.fits`
- **eboss_lrgpcmass_clustering_data_sgc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRGpCMASS_clustering_data-SGC-vDR16.fits`, sha256: `ff2398f3d963124b8685c58249c01af48f42d28c62759d680778f3851891c94e`, retrieved: 2026-07-28T16:21:32.567684, status: new
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRGpCMASS_clustering_data-SGC-vDR16.fits`
- **eboss_lrgpcmass_clustering_random_ngc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRGpCMASS_clustering_random-NGC-vDR16.fits`, sha256: `3310efb5e279a98855dddf95c5724a57422d2a59b5bf097458853f58e5b03525`, retrieved: 2026-07-28T16:25:54.409187, status: new
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRGpCMASS_clustering_random-NGC-vDR16.fits`
- **eboss_lrgpcmass_clustering_random_sgc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRGpCMASS_clustering_random-SGC-vDR16.fits`, sha256: `57977bf3cb320dc6aa7db31ae75e36ce26948c23b45b6df13e8d6c571088fc73`, retrieved: 2026-07-28T16:28:18.416468, status: new
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRGpCMASS_clustering_random-SGC-vDR16.fits`
- **eboss_lrg_clustering_data_ngc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRG_clustering_data-NGC-vDR16.fits`, sha256: `5eb836c7e6e69eb2cbc3b2dfe2f27826b6e5ac59d1c87e279a81a916f6edc77e`, retrieved: 2026-07-28T16:28:18.697339, status: cached
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_data-NGC-vDR16.fits`
- **eboss_lrg_clustering_data_sgc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRG_clustering_data-SGC-vDR16.fits`, sha256: `aec4b569ad957d829aa8337bf2c7d00e25dc777e2e5849552893cbead70071dc`, retrieved: 2026-07-28T16:28:18.750510, status: cached
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_data-SGC-vDR16.fits`
- **eboss_lrg_clustering_random_ngc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRG_clustering_random-NGC-vDR16.fits`, sha256: `5da0bf41e267968310ada55ea3bf27c9a3808bba77050e66c54d84dec62b6281`, retrieved: 2026-07-28T16:28:23.157899, status: cached
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_random-NGC-vDR16.fits`
- **eboss_lrg_clustering_random_sgc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRG_clustering_random-SGC-vDR16.fits`, sha256: `4aabcaa99cc2855d38eddd5fac903d3281e9436e5ba5b8c230050db3da92d230`, retrieved: 2026-07-28T16:28:25.327129, status: cached
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_random-SGC-vDR16.fits`
- **desi_dr1_lrg_clustering**: ERROR — unreachable: HTTP Error 404: Not Found (url: https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/v1.5/clustering/LRG_NGC_clustering.dat.fits)
  Manual-download instruction: Manual download: browse https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/v1.5/clustering/ (DESI DR1, 'iron' spectroscopic production, LSScats v1.5) from a network that can reach data.desi.lbl.gov / NERSC (128.55.206.0/24), download the {TRACER}_{NGC,SGC}_clustering.dat.fits data files and matching {TRACER}_{NGC,SGC}_clustering.ran.fits random files, compute SHA256, and append a row to data/MANIFEST.md following the same convention as the eBOSS LRG entries. Alternative access path (reachable from this environment, not independently used for this fetch): NOIRLab Astro Data Lab TAP, https://datalab.noirlab.edu/tap, table desi_dr1 -- whether it re-exposes the LSS clustering/random weight columns needed for this analysis is unverified.
- **desi_dr1_bgs_clustering**: ERROR — unreachable: HTTP Error 404: Not Found (url: https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/v1.5/clustering/BGS_BRIGHT_NGC_clustering.dat.fits)
  Manual-download instruction: Manual download: browse https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/v1.5/clustering/ (DESI DR1, 'iron' spectroscopic production, LSScats v1.5) from a network that can reach data.desi.lbl.gov / NERSC (128.55.206.0/24), download the {TRACER}_{NGC,SGC}_clustering.dat.fits data files and matching {TRACER}_{NGC,SGC}_clustering.ran.fits random files, compute SHA256, and append a row to data/MANIFEST.md following the same convention as the eBOSS LRG entries. Alternative access path (reachable from this environment, not independently used for this fetch): NOIRLab Astro Data Lab TAP, https://datalab.noirlab.edu/tap, table desi_dr1 -- whether it re-exposes the LSS clustering/random weight columns needed for this analysis is unverified.

**Integrity check (2026-07-28T16:28:29.387373+00:00):** eboss_lrgpcmass_clustering_data_ngc + eboss_lrgpcmass_clustering_data_sgc row-count total = 377458; published (docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md §3, arXiv:2007.09000) = 377458. Verdict: MATCH.

**Integrity check (2026-07-28T16:28:29.387543+00:00):** eboss_lrg_clustering_data_ngc + eboss_lrg_clustering_data_sgc row-count total = 174816; published (docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md §3, arXiv:2007.09000) = 174816. Verdict: MATCH.

## Sample-role classification (T0 decision D3, 2026-07-28)

Per `briefs/T0_DECISIONS_2026_07_28_PENDING_ITEMS.md` (D3):
- **PRIMARY WP-E7 LRG sample:** `eboss_lrgpcmass_*` — SDSS-recommended combined
  BOSS+eBOSS LRGpCMASS (377,458 data rows total, integrity-check MATCH above).
- **SECONDARY/cross-check only:** `eboss_lrg_*` (eBOSS-only, 174,816 data rows total,
  integrity-check MATCH above). Retained for eBOSS-specific systematics isolation;
  not the primary sample for occupancy/resolvability work.

The 2026-07-27 row-count "mismatch" note earlier in this file is superseded: it compared
the eBOSS-only fetch against the combined sample's published count (root cause:
`briefs/WP_E7_EBOSS_LRG_SAMPLE_IDENTITY_INVESTIGATION_2026_07_28.md`). Both catalogs now
carry correct comparators in `scripts/fetch_data.py::PUBLISHED_ROW_COUNTS`.
| nanograv_15yr | ERROR | HTTP Error 404: Not Found | | | |
| epta_dr2 | ERROR | HTTP Error 404: NOT FOUND | | | |
| sdss_lensing | ERROR | HTTP Error 404: Not Found | | | |
| lyman_alpha | ERROR | HTTP Error 404: Not Found | | | |
| eboss_lrgpcmass_clustering_data_ngc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRGpCMASS_clustering_data-NGC-vDR16.fits | cached | 4059343f572f10d8... | 2026-07-31T17:56:26.652895 | unknown |
| eboss_lrgpcmass_clustering_data_sgc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRGpCMASS_clustering_data-SGC-vDR16.fits | cached | ff2398f3d963124b... | 2026-07-31T17:56:26.786973 | unknown |
| eboss_lrgpcmass_clustering_random_ngc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRGpCMASS_clustering_random-NGC-vDR16.fits | cached | 3310efb5e279a988... | 2026-07-31T17:56:37.038093 | unknown |
| eboss_lrgpcmass_clustering_random_sgc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRGpCMASS_clustering_random-SGC-vDR16.fits | cached | 57977bf3cb320dc6... | 2026-07-31T17:56:41.945545 | unknown |
| eboss_lrg_clustering_data_ngc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_data-NGC-vDR16.fits | cached | 5eb836c7e6e69eb2... | 2026-07-31T17:56:42.156797 | WP-E7 Task B (T0-approved 2026-07-27; DESI/eBOSS resolvability follow-on prep) |
| eboss_lrg_clustering_data_sgc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_data-SGC-vDR16.fits | cached | aec4b569ad957d82... | 2026-07-31T17:56:42.176184 | WP-E7 Task B (T0-approved 2026-07-27; DESI/eBOSS resolvability follow-on prep) |
| eboss_lrg_clustering_random_ngc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_random-NGC-vDR16.fits | cached | 5da0bf41e2679683... | 2026-07-31T17:56:46.222283 | WP-E7 Task B (T0-approved 2026-07-27; DESI/eBOSS resolvability follow-on prep) |
| eboss_lrg_clustering_random_sgc | https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_random-SGC-vDR16.fits | cached | 4aabcaa99cc2855d... | 2026-07-31T17:56:48.011750 | WP-E7 Task B (T0-approved 2026-07-27; DESI/eBOSS resolvability follow-on prep) |
| desi_dr1_lrg_clustering | ERROR | unreachable: HTTP Error 404: Not Found | | | |
| desi_dr1_bgs_clustering | ERROR | unreachable: HTTP Error 404: Not Found | | | |
| desi_dr1_lya_p1d_covariance_fits | https://zenodo.org/records/16943723/files/data_points.tar | retrieved | bbb98dc3d1865a50... | 2026-07-31T17:57:23.009479 | WP-E6-BINMAP-C (T1 ruling R2 2026-07-31, executing T0 D1 dbf1337; real COVARIANCE HDU for the 9-bin z=4.2 sub-block) |

## Full-fidelity provenance — scripts/fetch_data.py (WP-E7 Task B, 2026-07-31T17:57:23.010211+00:00)

- **nanograv_15yr**: ERROR — HTTP Error 404: Not Found (url: n/a)
- **epta_dr2**: ERROR — HTTP Error 404: NOT FOUND (url: n/a)
- **sdss_lensing**: ERROR — HTTP Error 404: Not Found (url: n/a)
- **lyman_alpha**: ERROR — HTTP Error 404: Not Found (url: n/a)
- **eboss_lrgpcmass_clustering_data_ngc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRGpCMASS_clustering_data-NGC-vDR16.fits`, sha256: `4059343f572f10d831ac6d524ebc53e0150f9d8772df41e64a664f89ddf990ff`, retrieved: 2026-07-31T17:56:26.652895, status: cached
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRGpCMASS_clustering_data-NGC-vDR16.fits`
- **eboss_lrgpcmass_clustering_data_sgc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRGpCMASS_clustering_data-SGC-vDR16.fits`, sha256: `ff2398f3d963124b8685c58249c01af48f42d28c62759d680778f3851891c94e`, retrieved: 2026-07-31T17:56:26.786973, status: cached
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRGpCMASS_clustering_data-SGC-vDR16.fits`
- **eboss_lrgpcmass_clustering_random_ngc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRGpCMASS_clustering_random-NGC-vDR16.fits`, sha256: `3310efb5e279a98855dddf95c5724a57422d2a59b5bf097458853f58e5b03525`, retrieved: 2026-07-31T17:56:37.038093, status: cached
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRGpCMASS_clustering_random-NGC-vDR16.fits`
- **eboss_lrgpcmass_clustering_random_sgc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRGpCMASS_clustering_random-SGC-vDR16.fits`, sha256: `57977bf3cb320dc6aa7db31ae75e36ce26948c23b45b6df13e8d6c571088fc73`, retrieved: 2026-07-31T17:56:41.945545, status: cached
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRGpCMASS_clustering_random-SGC-vDR16.fits`
- **eboss_lrg_clustering_data_ngc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRG_clustering_data-NGC-vDR16.fits`, sha256: `5eb836c7e6e69eb2cbc3b2dfe2f27826b6e5ac59d1c87e279a81a916f6edc77e`, retrieved: 2026-07-31T17:56:42.156797, status: cached
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_data-NGC-vDR16.fits`
- **eboss_lrg_clustering_data_sgc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRG_clustering_data-SGC-vDR16.fits`, sha256: `aec4b569ad957d829aa8337bf2c7d00e25dc777e2e5849552893cbead70071dc`, retrieved: 2026-07-31T17:56:42.176184, status: cached
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_data-SGC-vDR16.fits`
- **eboss_lrg_clustering_random_ngc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRG_clustering_random-NGC-vDR16.fits`, sha256: `5da0bf41e267968310ada55ea3bf27c9a3808bba77050e66c54d84dec62b6281`, retrieved: 2026-07-31T17:56:46.222283, status: cached
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_random-NGC-vDR16.fits`
- **eboss_lrg_clustering_random_sgc** — path: `data/raw/sdss_eboss_dr16_lss/eBOSS_LRG_clustering_random-SGC-vDR16.fits`, sha256: `4aabcaa99cc2855d38eddd5fac903d3281e9436e5ba5b8c230050db3da92d230`, retrieved: 2026-07-31T17:56:48.011750, status: cached
  url: `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/eBOSS_LRG_clustering_random-SGC-vDR16.fits`
- **desi_dr1_lrg_clustering**: ERROR — unreachable: HTTP Error 404: Not Found (url: https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/v1.5/clustering/LRG_NGC_clustering.dat.fits)
  Manual-download instruction: Manual download: browse https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/v1.5/clustering/ (DESI DR1, 'iron' spectroscopic production, LSScats v1.5) from a network that can reach data.desi.lbl.gov / NERSC (128.55.206.0/24), download the {TRACER}_{NGC,SGC}_clustering.dat.fits data files and matching {TRACER}_{NGC,SGC}_clustering.ran.fits random files, compute SHA256, and append a row to data/MANIFEST.md following the same convention as the eBOSS LRG entries. Alternative access path (reachable from this environment, not independently used for this fetch): NOIRLab Astro Data Lab TAP, https://datalab.noirlab.edu/tap, table desi_dr1 -- whether it re-exposes the LSS clustering/random weight columns needed for this analysis is unverified.
- **desi_dr1_bgs_clustering**: ERROR — unreachable: HTTP Error 404: Not Found (url: https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/v1.5/clustering/BGS_BRIGHT_NGC_clustering.dat.fits)
  Manual-download instruction: Manual download: browse https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/v1.5/clustering/ (DESI DR1, 'iron' spectroscopic production, LSScats v1.5) from a network that can reach data.desi.lbl.gov / NERSC (128.55.206.0/24), download the {TRACER}_{NGC,SGC}_clustering.dat.fits data files and matching {TRACER}_{NGC,SGC}_clustering.ran.fits random files, compute SHA256, and append a row to data/MANIFEST.md following the same convention as the eBOSS LRG entries. Alternative access path (reachable from this environment, not independently used for this fetch): NOIRLab Astro Data Lab TAP, https://datalab.noirlab.edu/tap, table desi_dr1 -- whether it re-exposes the LSS clustering/random weight columns needed for this analysis is unverified.
- **desi_dr1_lya_p1d_covariance_fits** — path: `data/raw/desi_dr1_lya_p1d_zenodo/desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits`, sha256: `bbb98dc3d1865a50bb878e949a644604ce729da419db8e7db5adbb532a894857`, retrieved: 2026-07-31T17:57:23.009479, status: new
  url: `https://zenodo.org/records/16943723/files/data_points.tar`

**Integrity check (2026-07-31T17:57:24.267053+00:00):** eboss_lrgpcmass_clustering_data_ngc + eboss_lrgpcmass_clustering_data_sgc row-count total = 377458; published (docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md §3, arXiv:2007.09000) = 377458. Verdict: MATCH.

**Integrity check (2026-07-31T17:57:24.267165+00:00):** eboss_lrg_clustering_data_ngc + eboss_lrg_clustering_data_sgc row-count total = 174816; published (docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md §3, arXiv:2007.09000) = 174816. Verdict: MATCH.
