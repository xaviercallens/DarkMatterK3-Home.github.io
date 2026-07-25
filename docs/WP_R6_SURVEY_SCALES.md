# WP-R6 — Survey Scale Characterization (Bottom-Up Facts for Streams 1 & 2)

**Date:** 2026-07-25  
**Executor:** Claude Sonnet 5  
**Status:** ✅ **COMPLETE**

> ⚠️ **ENGINEERING-only.** Pure descriptive statistics of real catalogs already on hand. No model, no hypothesis, no TEST/FIT label (gate G1-L closed). These numbers characterize *what the data can resolve*, not any physical claim about dark matter, K3 geometry, or the dual-scale conjecture.

---

## Purpose

Streams 1 (chameleon screening formalization, WP-B1) and 2 (K3 candidate selection) both eventually need to know what observational regimes are empirically accessible with data already fetched. This WP answers with measured numbers from the real catalogs, not assumed or literature-recalled ones — continuing the WP-R series' bottom-up, simplest-first approach (WP-R0 math → R1 integrity → R2 machinery → R3/R4/R5 field & null infrastructure → **R6 scale facts**).

---

## Method

For each of 8 real datasets (4 photometric-only, 1 spectroscopic, 3 photo-z), measured directly from the catalog:
- **Footprint area** (from the known query box/cone size, `data/MANIFEST.md`)
- **Surface density** (objects per sq. degree)
- **Median nearest-neighbor angular separation** (brute-force, small-angle approximation)
- For fields with redshift: **comoving distance range** (Planck18, `pipeline/cosmology.py`), **comoving volume** of the cone, **number density**, and the **transverse physical scale** corresponding to the angular resolution at the median redshift

No fitting, no model. All formulas are direct geometric/statistical calculations on real coordinates.

---

## Results

### Angular / Surface Density Facts

| Field | Survey | N | Area (sq deg) | Surface density (/sq deg) | Median NN sep. |
|---|---|---|---|---|---|
| sdss_cosmos | SDSS | 1,068 | 0.0278 | 38,448 | 0.31″ |
| sdss_stripe82_center | SDSS | 14,007 | 0.0278 | 504,252 | 0.14″ |
| sdss_coma_cluster | SDSS | 822 | 0.0278 | 29,592 | 5.56″ |
| euclid_edf_north | Euclid | 2,000 | 0.1600 | 12,500 | 7.82″ |

### Redshift-Dependent Facts

| Field | z range | z median | D_C range (Mpc) | Comoving volume (Mpc³) | Number density (Mpc⁻³) | Transverse scale @ median z (Mpc) |
|---|---|---|---|---|---|---|
| sdss_z_coma_cluster | [0.001, 0.033] | 0.023 | [3.5, 144.2] | 8.46 | 5.91 | ~0 (see caveat) |
| euclid_z_edf_north | [0.040, 5.860] | 1.390 | [175.6, 8364.4] | 9.51×10⁶ | 2.09×10⁻⁴ | 0.266 |
| euclid_z_edf_fornax | [0.030, 6.000] | 1.530 | [132.0, 8425.1] | 9.72×10⁶ | 2.05×10⁻⁴ | 0.261 |
| euclid_z_edf_south | [0.110, 5.990] | 1.500 | [474.6, 8420.8] | 9.70×10⁶ | 2.06×10⁻⁴ | 0.217 |

**Sanity check:** Coma cluster's spectroscopic z range [0.001, 0.033] straddles the cluster's literature redshift (~0.0231) — consistent with real cluster members plus foreground/background contamination in the 10-arcmin beam, as expected.

---

## Data-Quality Finding: SDSS Spectroscopic Repeat Observations

**36 of 50 rows** in `sdss_z_coma_cluster` share identical (RA, Dec) with at least one other row — they are the **same physical object observed on different SDSS plates/MJDs** (standard SDSS repeat/calibration spectroscopy), not 36 independent close pairs. Example:

| RA | Dec | z | plate | mjd |
|---|---|---|---|---|
| 194.894151 | 27.914554 | 0.001970 | 2240 | 53823 |
| 194.894151 | 27.914554 | 0.000781 | 6483 | 56341 |

**Consequence:** the "median nearest-neighbor separation ≈ 0″" reported above for this field is an artifact of these exact-duplicate positions, not a genuine angular-resolution measurement. **Any future WP treating this catalog's row count as an independent-object count must deduplicate on (RA, Dec) or `specobjid` first.** This is exactly the kind of real-data quirk WP-R2's "machinery survives real conditions" mandate anticipates — flagged here rather than silently absorbed into a downstream statistic.

---

## Facts Available to Stream 1 (WP-B1, Chameleon Screening)

WP-B1 formalizes environment-dependent screening with a force-range r_S(ρ). These measured numbers bound what observational regimes are *currently accessible* with data in hand, independent of any specific mass/coupling hypothesis:

- **Finest resolved transverse physical scale in the Euclid photo-z cones:** ≈0.22–0.27 Mpc at median redshift (z~1.4–1.5), set by angular sampling density (~10–13″ median nearest-neighbor separation) combined with cosmological distance.
- **Comoving volume probed per Euclid cone:** ~9.5–9.7 × 10⁶ Mpc³ (0.2°-radius, z∈[0.03–0.11, 6.0]).
- **Local low-z volume (Coma, spectroscopic):** only 8.5 Mpc³ — tiny compared to the deep photo-z cones, but with genuine 3D positions (real spec-z) rather than photometric estimates.

These are the concrete scales any future chameleon force-range prediction would need to either exceed (to be invisible to current data, consistent with a screened/short-range scenario) or fall within (to be testable with catalogs already fetched) — a fact about instrument/survey capability, not a physics claim.

---

## Facts Available to Stream 2 (K3 Candidate Selection)

- **Sibling-family control harness (WP-R4)** is independent of real-data scale facts — it operates on certificate-backed mathematical parameters (order-(a,b,c,d) tuples), not survey data. No new dependency introduced here.
- The **real-data null-bank infrastructure (WP-R5)**, once a derived observable exists (post-G1-L), can directly ingest whichever candidate's prediction Stream 2 selects — the pipeline (cosmology → tangent-plane field → null comparison) is candidate-agnostic by construction.

---

## Validation

- ✅ All 8 fields processed without error
- ✅ Comoving-distance/volume calculations reuse the same cited Planck18 cosmology and tested functions from WP-R5 (no new unvalidated formulas)
- ✅ Data-quality anomaly (repeat spectroscopy) found and flagged rather than silently producing a misleading "0 arcsec resolution" number
- ✅ No TEST/FIT label; no hypothesis evaluated

---

## Files

| File | Purpose |
|---|---|
| `scripts/characterize_survey_scales.py` | Runner: measures footprint, density, resolution, volume facts |
| External disk: `survey_characterization/survey_scales_2026_07_25.json` | Full results (SHA256: `70630739a3ae77ea343fb529857faac645ec9612469454ff1042a608735f68d1`) |

---

## Provenance

`Generated-by: Claude Sonnet 5 | Verified-by: manual duplicate-row trace + reuse of WP-R5-tested cosmology functions | Reviewed-by: [pending T0]`
