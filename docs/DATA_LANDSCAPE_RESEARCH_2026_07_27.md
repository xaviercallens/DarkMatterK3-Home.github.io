# Open Astrophysics Data Landscape — Survey for WP-E5 / WP-E6
**Date:** 2026-07-27. **Scope:** publicly available data products only, as of July 2026. Web survey; nothing downloaded; no physics claims about the K3 program. Numbers carry source URLs; "derived" = simple arithmetic from cited numbers; "unverified" = not confirmed against a primary source in this session.

---

## 1. Executive summary

**Need (a) — transverse/spectroscopic clustering (WP-E5):** the ">= 10^4 spec objects per redshift slice" floor is now cleared by 1–2 orders of magnitude by public data; the previous 50-object ceiling is obsolete.
1. **DESI DR1 LRG** — 2,138,600 spec-z at 0.4<z<1.1 over ~7,500 deg^2 → ~3×10^5 per Δz=0.1 slice (derived), i.e. ~30× the floor. [arXiv:2404.03000]
2. **DESI DR1 ELG** — 2,432,022 spec-z at 0.8<z<1.6 → ~3×10^5 per Δz=0.1 slice (derived). [arXiv:2404.03000]
3. **SDSS/eBOSS DR16 combined LRG** — 377,458 spec-z at 0.6<z<1.0 over 9,493 deg^2 (fully open, no registration; smaller but frictionless). [arXiv:2007.09000]
**Caveat:** the ~1.6 Mpc *effective resolution* floor is NOT met as a mean inter-object spacing by any wide survey — DESI DR1 LRG mean spacing is ~25 Mpc comoving (derived, order-of-magnitude); whether the floor refers to spacing, grid resolution, or scale reach of the estimator must be resolved against the pre-registration text before declaring feasibility.

**Need (b) — weak-lensing / structure exclusion sweep (WP-E6):**
1. **DES Y6 Metadetection shear catalog** — 151,922,791 galaxies, 4,422 deg^2, n_eff = 8.22 arcmin^-2 (final DES release). [arXiv:2501.05665]
2. **DESI DR1 Lyman-alpha P1D** — >300,000 forests, 1.7× eBOSS statistics, the current best public P1D for small-scale suppression tests. [arXiv:2505.07974]
3. **KiDS-Legacy (DR5)** — 1,347 deg^2, 9-band, public ESO release; S8 = 0.815 (+0.016/−0.021). [arXiv:2503.19441]
**Decisive caveat for (b):** published bounds already cover the *entire* 1e-22–1e-19 eV grid for pure FDM — UFD stellar kinematics give m > 8×10^-18 eV (95%) [arXiv:2509.02781] and Lyman-alpha gives m > 2×10^-20 eV [PRL 126.071302] — so a WP-E6 sweep can only be framed as reproduction/robustness or as a *mixed-fraction* (f_FDM < 1) analysis, not as novel exclusion. See §4.

---

## 2. Dataset table

| Dataset / release | Public since | What is public | Counts / area / z | Spec vs photo | Density / resolution proxy | Access & approx. volume | License / terms | Fit |
|---|---|---|---|---|---|---|---|---|
| **DESI DR1** | 2025-03 | Spectra, redshift catalogs, LSS/BAO catalogs, Lya products, VACs | 18.7M unique objects w/ good z (13.1M galaxies, 1.6M QSO, 4M stars); ~7,500 deg^2; z ≈ 0–4 | Spectroscopic | LRG mean spacing ~25 Mpc, BGS ~8–20 Mpc (derived, order-of-mag); per-slice counts ~10^5 | data.desi.lbl.gov (web/NERSC); NOIRLab Astro Data Lab TAP (`desi_dr1`); SPARCL spectra service; volume: unverified (100s of TB scale, unverified) | DESI data license/ack. policy on portal (CC-BY-style, unverified) | **(a) primary; (b) via Lya** |
| **DESI DR2** | partial (2025-03) | BAO/cosmology summary products, chains only; **spectra/redshifts NOT public** | >14M usable objects quoted in papers; ~60% more sky than DR1 | Spectroscopic | — | Full release stated "by early 2027" (unverified) | — | (a) future upgrade |
| **DESI EDR** | 2023-06 | SV spectra + catalogs | ~1.2M unique targets (unverified) | Spectroscopic | small area | data.desi.lbl.gov, Astro Data Lab | as DR1 | neither (superseded) |
| **SDSS-IV eBOSS DR16/DR17 LSS** | 2020–2021 | Full spectra + LSS clustering catalogs + randoms | LRG combined 377,458 (0.6<z<1.0, 9,493 deg^2); ELG 173,736 (0.6<z<1.1, ~1,170 deg^2); QSO 343,708 (0.8<z<2.2, 4,808 deg^2) | Spectroscopic | per-Δz=0.1 slice: LRG ~9×10^4, ELG ~3×10^4, QSO ~2×10^4 (derived) | sdss4.org/dr17/spectro/lss/, data.sdss.org; TB-scale, no registration | SDSS data fully public w/ ack. policy | **(a) secondary** |
| **eBOSS DR14 Lya P1D (Chabanier+19)** | 2019 | P1D tables, 13 z-bins 2.2–4.6, k ≤ 0.02 s/km | 43,751 selected quasars (of 180,413 parent) | Spectroscopic | k up to 0.02 (km/s)^-1 | Tables w/ paper (JCAP 07(2019)017); MB-scale | open w/ citation | **(b)** |
| **DESI DR1 Lya P1D** | 2025 | P1D measurements (FFT + optimal estimators) + forest catalogs in DR1 | >300,000 Lya forests (optimal est.); ~450,000 QSOs at z>2.1 in DR1 | Spectroscopic | 1.7× eBOSS statistics | via DESI DR1 portal + paper products; MB–GB | as DR1 | **(b) primary (Lya)** |
| **DES Y3** | ~2021–2022 | Gold catalog, Metacal shear catalog, 2pt data vectors, chains | ~100M source galaxies, 4,143 deg^2, n_eff ≈ 5.6 arcmin^-2 (unverified), photo-z 0.2–1.3 | Photometric (photo-z) | n_eff ≈ 5.6 arcmin^-2 (unverified) | des.ncsa.illinois.edu/releases; 10s of TB | open w/ ack. | **(b)** |
| **DES Y6** | 2025–2026 (papers + Gold; shear-catalog file status: verify) | Y6 Gold (from DR2), Metadetection shape catalog, cosmology products | 151,922,791 shear galaxies; 4,422 deg^2 | Photometric | n_eff = 8.22 arcmin^-2, σ_e = 0.29 | des.ncsa.illinois.edu/releases | open w/ ack. | **(b) primary** |
| **KiDS-Legacy / KiDS DR5** | 2023–2025 | 9-band imaging + shear + photo-z + calibration products | 1,347 deg^2 (+23 deg^2 calib.); z_B ≤ 2.0 | Photometric | n_eff: unverified (KiDS-1000 was ~6.2 arcmin^-2, unverified) | kids.strw.leidenuniv.nl/DR5 + ESO archive; TB-scale | ESO public survey | **(b)** |
| **HSC-SSP PDR3 (+S19A shape cat.)** | 2021 (PDR3) | Imaging, catalogs; S19A/Y3 shape catalog public within PDR3 | Wide ~670 deg^2 at ~26 mag (5σ, grizy); shape cat. 416 deg^2 | Photometric | n_eff ≈ 15 arcmin^-2 (shape cat.) | hsc-release.mtk.nao.ac.jp (free registration required) | HSC-SSP terms | **(b)** (deep, smaller area) |
| **Euclid Q1** | 2025-03-19 | VIS + NISP imaging, catalogs, NISP slitless spectra & redshifts (H_E ≤ 22.5), ground photometry | 63.1 deg^2 (EDF-N/S/Fornax + LDN1641); ~26–30M detections | Mostly photometric + slitless spec subset | deep-field densities; small area | ESA Euclid Science Archive / ESA Datalabs | CC BY 4.0 (paper); archive terms | (b) marginal now; watch DR1 |
| **Euclid DR1** | scheduled 2026 (not public as of 2026-07, unverified exact date) | Year-1 wide survey | ~1,900 deg^2 expected (unverified) | Photo + slitless spec | — | ESA archive | — | (a)+(b) future |
| **Rubin/LSST DP1** | 2025-06-30 | Commissioning (ComCam) images + catalogs | ~15 deg^2, 7 fields; ~2.3M objects | Photometric | tiny area | data.lsst.cloud — **data-rights holders only, not open** | Rubin data rights policy | neither (access-restricted) |
| **NANOGrav 15-yr** | 2023 | Full timing data (narrowband + wideband), noise models, GWB posteriors | 67–68 MSPs, 16.03 yr baseline | — (PTA) | nHz GW band | Zenodo doi:10.5281/zenodo.7967585; data.nanograv.org; GB-scale | open w/ citation | (b)-adjacent (historical PTA use) |
| **EPTA DR2 / PPTA DR3** | 2023 | Timing data + posteriors | EPTA: 25 MSPs (unverified); PPTA: 32 MSPs, 2004–2022 | — (PTA) | nHz | EPTA archives; CSIRO Data Access Portal | open | (b)-adjacent |
| **IPTA DR3** | not yet public (in preparation as of 2026-07) | — | — | — | — | — | — | future |

---

## 3. Per-dataset notes and sources

### DESI DR1 (primary recommendation for need (a))
- Release March 2025; 18.7M unique targets with high-confidence redshifts: 13.1M galaxies, 1.6M quasars, 4M stars; first 13 months of main survey (May 2021–Jun 2022); ~7,500 deg^2 of the planned 14,200 deg^2. Sources: https://arxiv.org/abs/2503.14745 , https://data.desi.lbl.gov/doc/releases/dr1/
- BAO/LSS catalog samples (exact counts): BGS 300,017 (0.1<z<0.4); LRG 2,138,600 (0.4<z<1.1); ELG 2,432,022 (0.8<z<1.6); QSO 856,652 (0.8<z<2.1); >5.7M total in 0.1<z<2.1; effective volume ~18 Gpc^3. Source: https://arxiv.org/abs/2404.03000
- Per-slice arithmetic (derived): LRG ≈ 2.14M / 7 slices of Δz=0.1 ≈ 3.1×10^5 per slice; even the sparsest tracer (QSO, ~6.6×10^4 per Δz=0.1) clears the 10^4 floor.
- Resolution proxy (derived, order-of-magnitude, Planck-like distances): LRG number density ~6×10^-5 Mpc^-3 → mean comoving spacing ~25 Mpc; BGS denser (~10^-3–10^-4 Mpc^-3 range depending on cut) → ~8–20 Mpc. No wide spectroscopic survey approaches 1.6 Mpc mean spacing (that would require n ≈ 0.24 Mpc^-3).
- Lyman-alpha: DR1 contains ~450,000 z>2.1 quasars; P1D measured from >300,000 forests (largest to date, 1.7× eBOSS). Sources: https://arxiv.org/abs/2505.07974 (optimal estimator), https://arxiv.org/abs/2505.09493 (FFT), https://arxiv.org/abs/2509.13593 (validation).
- Access: https://data.desi.lbl.gov/doc/access/ (portal fetches were blocked from this environment — access details below cross-checked via NOIRLab): NOIRLab Astro Data Lab hosts the `desi_dr1` database with TAP at https://datalab.noirlab.edu/tap, and SPARCL serves DR1 coadded spectra, no NERSC account needed. Sources: https://datalab.noirlab.edu/desi/access.php , https://github.com/astro-datalab/Tutorial-DESI-NOIRLab-2025 . Total DR1 volume: unverified.

### DESI DR2 (status)
- DR2 (3 years of data, to Apr 2024) more than doubles usable objects to >14M and adds ~60% sky vs DR1, but **only cosmology summary products (BAO measurements, chains) are public; spectra and redshift catalogs are not**, with full release stated "by early 2027" (secondary source — unverified). Sources: https://data.desi.lbl.gov/doc/releases/ , https://www.emergentmind.com/topics/dark-energy-spectroscopic-instrument-desi-data-release (unverified aggregator), https://arxiv.org/abs/2503.14742 (DR2 BAO validation).

### SDSS / eBOSS (DR16 LSS catalogs; DR17/DR18 carry them forward)
- Completed-eBOSS LSS catalogs (Ross et al. 2020): combined BOSS+eBOSS LRG 377,458 over 9,493 deg^2 (0.6<z<1.0); eBOSS QSO 343,708 over 4,808 deg^2 (0.8<z<2.2). Sources: https://arxiv.org/abs/2007.09000 , https://www.sdss4.org/dr17/spectro/lss/
- ELG: 173,736 reliable spec-z, 0.6<z<1.1 (NGC 83,769 + SGC 89,967), Raichoor et al. Source: https://www.sdss4.org/dr17/spectro/lss/ (and https://arxiv.org/abs/2007.09009 companion).
- DR18 (2023) is the first SDSS-V release and adds no new LSS catalogs; eBOSS LSS remains the reference. Source: https://www.sdss.org/dr18/data_access/value-added-catalogs/
- Fully open, no registration; assessment: clears the 10^4/slice floor (LRG ~9×10^4 per Δz=0.1, derived) but superseded in raw statistics by DESI DR1.

### eBOSS Lyman-alpha products
- 1D flux power spectrum, SDSS DR14: 43,751 best-quality quasars from 180,413 parent sample; 13 z-bins, z_Lya = 2.2–4.6; k ≤ 0.02 (km/s)^-1 (Chabanier et al. 2019, JCAP 07(2019)017). Source: https://arxiv.org/abs/1812.03554
- 3D Lya power spectrum from eBOSS DR16 also published. Source: https://arxiv.org/abs/2403.08241

### DES (need (b) primary)
- **Y6 (final)**: Metadetection shape catalog: 151,922,791 galaxies over riz, 4,422 deg^2, n_eff = 8.22 arcmin^-2, shape noise 0.29 (MNRAS 543, 4156 (2025), doi:10.1093/mnras/staf1661). Sources: https://arxiv.org/abs/2501.05665 , https://academic.oup.com/mnras/article/543/4/4156/8268899 . Y6 Gold photometric dataset: https://arxiv.org/abs/2501.05739 ; Y6 3x2pt and cosmic-shear cosmology: https://arxiv.org/abs/2601.14559 , https://arxiv.org/abs/2602.10065 . Y6 Gold is public at https://des.ncsa.illinois.edu/releases (per Y6 paper); whether the shear-catalog *files* are already posted there needs a one-click check — unverified.
- **Y3**: shear catalog, 2pt data vectors and chains public at https://des.ncsa.illinois.edu/releases/y3a2 (counts ~100M, n_eff ~5.6 arcmin^-2 — unverified this session).

### KiDS-Legacy / KiDS DR5
- Final release: 1,347 deg^2, 9-band (ugri + ZYJHK_s), +23 deg^2 calibration fields; i-band second pass; +34% area vs DR4; ESO public survey. Sources: https://kids.strw.leidenuniv.nl/DR5/PR/KiDS_DR5.pdf , https://arxiv.org/abs/2503.19441
- Cosmic-shear result S8 = 0.815 (+0.016/−0.021), ~32% tighter than previous KiDS; photo-z to z_B ≤ 2.0. Source: https://arxiv.org/abs/2503.19441 ; redshift calibration: https://arxiv.org/abs/2503.19440
- n_eff for Legacy: unverified this session (KiDS-1000 predecessor ~6.2 arcmin^-2, unverified).

### HSC-SSP PDR3 + S19A shape catalog
- PDR3: wide layer ~670 deg^2 at full depth ~26 mag (5σ, grizy). Source: https://www.researchgate.net/publication/363194579 (PDR3 paper; primary: Aihara et al. 2022, PASJ).
- Y3/S19A shape catalog: 416 deg^2, n_eff ≈ 15 arcmin^-2; public within PDR3. Sources: https://hsc-release.mtk.nao.ac.jp/doc/index.php/s19a-shape-catalog-pdr3/ , https://arxiv.org/abs/2304.00701
- Access requires (free) account at https://hsc-release.mtk.nao.ac.jp — deepest public wide shear data; best for high-z lensing weight, smallest area of the big three.

### Euclid
- **Q1** (2025-03-19): 63.1 deg^2 (EDF-N 20, EDF-S 23, EDF-F 10, LDN1641 ~0.5 deg^2); ~26M detections per press release, ~30M objects per overview paper; VIS I_E + NISP Y_E J_E H_E imaging, ground ugriz, and NISP slitless spectroscopy with redshifts for H_E ≤ 22.5 sources; via ESA archive/Datalabs; paper CC BY 4.0. Sources: https://www.aanda.org/articles/aa/full_html/2026/07/aa54610-25/aa54610-25.html , https://www.euclid-ec.org/public/press-releases/euclid-quick-data-release-1/
- **DR1**: scheduled 2026 per mission timelines (exact date unverified; not public as of 2026-07-27). Sources: https://euclid.caltech.edu/page/data-release-timeline , https://www.euclid-ec.org/public/timeline/
- Assessment: Q1 too small for either floor at survey scale; DR1 is the watch item for both (a) (slitless spec-z) and (b) (space-based shear).

### Rubin/LSST DP1
- Released 2025-06-30 (updated 2026-01-08); ComCam commissioning data: ~15 deg^2, 7 fields, 1,792 exposures, ~2.3M objects, ugrizy. Sources: https://dp1.lsst.io/index.html , https://rubinobservatory.org/for-scientists/data-products/recent-data-releases
- **Access restricted to Rubin data-rights holders** (US/Chile scientists + named in-kind members) via data.lsst.cloud — not an open product for this program unless Xavier qualifies. Source: https://dp1.lsst.io/index.html
- Assessment: neither need today; DR1 (first LSST data release) timing unverified.

### PTAs
- **NANOGrav 15-yr**: 67–68 MSPs, 16.03-yr span (2004–2020); narrowband + wideband TOAs; Zenodo doi:10.5281/zenodo.7967585 (narrowband refresh: https://zenodo.org/records/14773896); portal http://data.nanograv.org. Sources: https://arxiv.org/abs/2306.16217 , https://nanograv.org/news/15yrDataSet
- **EPTA DR2** (public, 2023) and **PPTA DR3** (public at CSIRO Data Access Portal; 32 MSPs, 2004–2022). Sources: https://arxiv.org/abs/2306.16214 , https://www.researchgate.net/publication/371944162
- **IPTA DR3**: still in preparation, no public combined release found as of 2026-07. Source: https://indico.global/event/16100/contributions/140729/attachments/65096/125926/7_POST_Shaifullah.pdf

---

## 4. Already-published fuzzy-DM bounds covering 1e-22–1e-19 eV (a WP-E6 sweep must not present these as novel)

Pure-FDM (f_FDM = 1) lower bounds, strongest last:
- **Iršič et al. 2017** (PRL 119, 031302): first Lya-forest FDM bound, m ≳ 3.8×10^-21 eV (2σ; relaxes to ~10^-21 with conservative IGM priors — exact conservative value unverified). https://www.researchgate.net/publication/315096435 (primary: doi:10.1103/PhysRevLett.119.031302)
- **Armengaud et al. 2017**: independent Lya bound ~2.9×10^-21 eV (unverified this session).
- **Laroche et al. 2022**: quad-lens flux ratios disfavor m < 10^-21.5 eV. Via review: https://arxiv.org/abs/2306.11781
- **Powell et al. 2023**: VLBI strong lensing (MG J0751+2716), m > 4.4×10^-21 eV (95%) — strongest lensing-based FDM bound. Via https://arxiv.org/abs/2306.11781 and https://www.mpa-garching.mpg.de/1076681/hl202306
- **Liu, Gong & Zhou 2026** (arXiv:2606.06969): Lya P1D at z = 4.2–5.0: pure FDM m > 1.9×10^-21 eV (95%); **mixed FDM**: f_FDM < 0.07 at m = 10^-23 eV, < 0.12 at 10^-22 eV, < 0.65 at 10^-21 eV; no effective constraint at higher masses in the mixed case. https://arxiv.org/abs/2606.06969
- **Rogers & Peiris 2021** (PRL 126, 071302): Lya forest (high-res spectra + emulator), m > 2×10^-20 eV (95%) — excludes the lower 1.3 decades of the grid. Cited throughout, e.g. https://arxiv.org/abs/2606.06969
- **Dalal & Kravtsov 2022** (arXiv:2203.05750): UFD sizes + stellar kinematics (Segue 1/2), m > 3×10^-19 eV (99%) — covers the entire grid. https://arxiv.org/abs/2203.05750
- **May, Dalal & Kravtsov 2025** (arXiv:2509.02781): confirms 3×10^-19 as conservative; Ursa Major III/UNIONS I pushes to **m > 8×10^-18 eV (95%)**. https://arxiv.org/abs/2509.02781
- MW satellite abundance (Nadler et al. 2021, m > ~2.9×10^-21 eV — unverified this session).

PTA-band constraints (relevant to the program's NANOGrav lineage; gravitationally-coupled ULDM oscillations sit at m ~ 10^-24–10^-22 eV, i.e. at/below the grid's bottom edge):
- **NANOGrav 15-yr new-physics search** (arXiv:2306.16219): no ULDM signal; updated constraints. https://arxiv.org/abs/2306.16219
- **EPTA DR2 VI** (arXiv:2306.16228): "Challenging the ultralight dark matter paradigm". https://arxiv.org/abs/2306.16228
- **PPTA-DR3 + EPTA-DR2 ULDM/dark-photon constraints** (arXiv:2605.02172). https://arxiv.org/abs/2605.02172

**Net position (fact, not physics claim):** for a mediator assumed to be all of the dark matter, the 1e-22–1e-19 eV window is fully covered by published exclusions (Lya to 2×10^-20; UFDs to 8×10^-18), each with stated model dependences (IGM modeling for Lya; heating/tidal assumptions for UFDs). The open territory a sweep could legitimately target is (i) mixed fractions f_FDM < 1 above ~10^-21 eV, and (ii) mediators that are not the dominant DM component — a framing decision that belongs to the pre-registration, not to this survey.

---

## 5. Open questions
1. **Definition of the 1.6 Mpc floor (WP-E5):** counts clear the 10^4/slice floor everywhere, but mean inter-object spacing in the densest wide spectroscopic samples is ~8–25 Mpc (derived). Is "effective resolution" a per-object spacing requirement (then no public wide survey qualifies) or an estimator/grid property? Must be resolved against PREDICTION.md wording before any feasibility claim.
2. **DES Y6 shear-catalog file availability:** papers are out and Gold is public at des.ncsa.illinois.edu/releases; direct confirmation that the Metadetection FITS files are posted (vs "coming with the y6a2 release page") is pending — one browser check.
3. **DESI DR2 spectra timing:** "early 2027" is from a secondary aggregator (unverified). If WP-E5 can wait, DR2 roughly doubles DR1; if not, DR1 is sufficient by margin.
4. **Euclid DR1 exact date and spec-z counts:** scheduled 2026 but unverified; would add slitless spec-z over ~1,900 deg^2 (unverified) — could matter for (a) at 0.9<z<1.8.
5. **DESI DR1 total data volume and license text:** the DESI portal (data.desi.lbl.gov) refused automated fetches from this environment; volume and exact license wording remain unverified (Astro Data Lab TAP/SPARCL access confirmed via NOIRLab).
6. **Rubin data rights:** DP1/DR1 require data-rights status; worth checking whether any in-kind route applies to Xavier — otherwise exclude Rubin from planning.
7. **KiDS-Legacy n_eff and DES Y3 exact counts:** quoted from memory of predecessor releases, marked unverified; pull from the released catalog papers if these enter WP-E6.
