# WP-R5 — Real 3D Comoving Density Field + Corrected Null Bank

**Date:** 2026-07-25  
**Executor:** Claude Sonnet 5 (higher-tier review, as required by the master plan: "a Sonnet/Opus session must review before anything downstream uses it")  
**Status:** ✅ **COMPLETE** — genuine 3D field built, cosmology cited and tested, null schemes validated as functionally correct; one honest power limitation documented (not hidden)

> ⚠️ **Every number in this document is ENGINEERING-only.** No TEST/FIT label (gate G1-L closed, F5b active). No comparison to any prediction. No interpretation of any topology value as evidence for or against any hypothesis — that interpretation is T0-only and gated, and explicitly out of scope for this WP (`HAIKU_PLAN_REALDATA_VERIFICATION_2026_07_25.md`, WP-R5 "STOP AND FLAG" clause).

---

## 0. This WP superseded a defective predecessor

While building this WP, a genuine methodological defect was found in WP-R3's null bank (commit 4c99217): both its randomization schemes were no-ops (see `docs/FINDING_R_NULLDEGENERATE_2026_07_25.md` for full root-cause analysis). That finding is filed separately and the retraction is recorded in `docs/EXECUTION_SUMMARY_2026_07_25.md`. This document describes the **replacement** null infrastructure, built and verified correctly from scratch.

---

## 1. Data Fetched (New, Separately Manifested)

Per WP-R5 instructions, a new query set was fetched — not aliased to the WP-R1 morphology-only files:

| Dataset | Query | Rows | SHA256 (16-char) |
|---|---|---|---|
| `sdss_z_cosmos` | SDSS `spectro=True`, same field as WP-R1 | 8 | `45fa2b9cf9a2643d` |
| `sdss_z_stripe82_center` | SDSS `spectro=True` | 27 | `39024d048ca9513a` |
| `sdss_z_coma_cluster` | SDSS `spectro=True` | 50 | `7b7c753e9a116831` |
| `sdss_z_docs_example` | SDSS `spectro=True` | 7 | `454e839dd3c3cf0b` |
| `euclid_z_edf_north` | MER ⋈ `phz_photo_z` on `object_id` | 2000 | `8b5b287f3f031656` |
| `euclid_z_edf_fornax` | MER ⋈ `phz_photo_z` on `object_id` | 2000 | `4095efd8603519f4` |
| `euclid_z_edf_south` | MER ⋈ `phz_photo_z` on `object_id` | 2000 | `7fe629517de7a620` |

Full-fidelity provenance appended to `data/MANIFEST.md` (§"Full-fidelity provenance — scripts/fetch_survey_redshifts.py"). All 7/7 fetches succeeded; gate G1 (real-data access) checked and open; no fallback logic triggered.

**Sanity check:** SDSS Coma cluster spectroscopic redshifts measured z = 0.023 ± 0.006 (mean ± std over 50 objects) — matches the cluster's well-known literature redshift (~0.0231). Real spectroscopy, not placeholder data.

---

## 2. Cosmology (Free Input, Cited)

**`pipeline/cosmology.py`** uses `astropy.cosmology.Planck18`:
> Planck Collaboration 2018/2020, A&A, 641, A6 (Paper VI), Table 2 (TT,TE,EE+lowE+lensing+BAO). H0 = 67.66 km/s/Mpc, Ωm = 0.30966, flat ΛCDM.

This is a **free input, not a prediction** — every comoving distance, and therefore every field and topology number below, changes if this choice changes. Stated explicitly in the module docstring; not retyped from memory anywhere downstream.

**Validation (`pipeline/tests/test_cosmology.py`, 16/16 pass):**
- Comoving-distance conversion checked against an **independently coded** numerical integration (scipy.quad over the flat-ΛCDM Friedmann equation, including matter + radiation + dark energy terms) — agrees with astropy to <0.5% out to z=2. The residual is attributed to astropy's massive-neutrino equation-of-state treatment, documented in the test rather than silently tightened or ignored.
- Low-z Hubble-law approximation cross-check.
- Coma cluster's real measured z=0.023 lands at D_C ≈ 99 Mpc — consistent with the cluster's known ~100 Mpc distance (order-of-magnitude sanity, not a precision claim).
- Cartesian/tangent-plane conversions unit-tested for centre-mapping, small-angle correctness, and distance preservation.

---

## 3. Binning Frame — Why Global Cartesian Was Wrong, and the Fix

**Initial attempt** used global Cartesian (x, y, z) embedding (`radec_z_to_cartesian_mpc`). Diagnosis on the real Euclid North field:

| Axis | Span |
|---|---|
| x | 147 Mpc |
| y | 3,380 Mpc |
| z | 7,462 Mpc |

A 0.2°-radius cone spanning redshift 0.04–5.86 embeds as a **thin diagonal sliver inside a mostly-empty axis-aligned bounding box** — only 40/512 bins (8%) were occupied at nbins=8. This is a real geometric property of narrow, deep pencil-beam surveys, not a data-quality problem.

**Fix:** `radec_z_to_tangent_plane_mpc` (new function, `pipeline/cosmology.py`) projects onto a small-angle tangent plane centred on the field's own (RA, Dec) centroid — transverse Mpc offsets plus radial comoving distance — the standard frame for narrow-field LSS analysis. Result:

| Field | Bin occupancy (global Cartesian) | Bin occupancy (tangent-plane) |
|---|---|---|
| euclid_z_edf_north | 8% | **41.2%** |
| euclid_z_edf_fornax | ~8% (not separately re-measured) | **44.5%** |
| euclid_z_edf_south | ~8% (not separately re-measured) | **37.3%** |

Both frames are physically valid conversions of the same real data — the tangent-plane frame is simply the correct engineering choice for this survey geometry. All downstream WP-R5 numbers use the tangent-plane frame.

---

## 4. Redshift-Drop Discipline (Never Impute)

Per WP-R5's hard rule, invalid redshifts (Euclid photo-z NaN for objects the pipeline couldn't fit) are dropped and counted, never imputed:

| Field | n_input | n_dropped (NaN) | n_dropped (negative) | n_valid |
|---|---|---|---|---|
| euclid_z_edf_north | 2000 | 17 | 0 | 1983 |
| euclid_z_edf_fornax | 2000 | 7 | 0 | 1993 |
| euclid_z_edf_south | 2000 | 4 | 0 | 1996 |
| sdss_z_coma_cluster | 50 | 0 | 0 | 50 |

`drop_invalid_redshifts()` (`pipeline/cosmology.py`) enforces this mechanically; `radec_z_to_tangent_plane_mpc`/`radec_z_to_cartesian_mpc` both **raise** if called with unfiltered NaN/negative z, rather than silently producing NaN coordinates.

---

## 5. Null Bank — Two Valid Schemes (Replacing WP-R3's Defective Ones)

`pipeline/realfield3d.py`:

1. **z-shuffle:** fix each object's (RA, Dec); independently permute redshift assignment across objects. Breaks radial-angular correlation.
2. **Angular CSR:** fix each object's redshift; redraw (RA, Dec) uniformly at random within the observed angular footprint (uniform in RA, uniform in sin(Dec) — the correct measure for angular uniformity).

**Both schemes are directly verified to produce genuinely different point patterns per call** (`pipeline/tests/test_realfield3d.py`, 8/8 pass) — the exact check that would have caught WP-R3's bug. 200 realizations per scheme per field, independent RNG seeds (101, 102), no seed reuse.

---

## 6. Results

| Field | N (valid) | Bin occ. | Real β₀,β₁,β₂ | Null z-shuffle (mean±σ) | Null CSR (mean±σ) | Real percentile (z-sh / CSR) |
|---|---|---|---|---|---|---|
| euclid_z_edf_north | 1983 | 41.2% | 1, 0, 2 | 1.00 ± 0.00 | 1.00 ± 0.00 | 100% / 100% |
| euclid_z_edf_fornax | 1993 | 44.5% | 1, 0, 0 | 1.00 ± 0.00 | 1.00 ± 0.00 | 100% / 100% |
| euclid_z_edf_south | 1996 | 37.3% | 1, 0, 0 | 1.05 ± 0.22 | 1.00 ± 0.00 | 95% / 100% |
| sdss_z_coma_cluster | 50 | 6.2% | 5, 0, 0 | 5.96 ± 1.40 | 5.22 ± 1.81 | 39.5% / 58.0% |

Full data: `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/wp_r5_3d_field/wp_r5_results_2026_07_25.json` (SHA256: `2a69505ebe510c8249abac145c20f7c6c762d959bf02df706a8b6832bb5bd65c`)

---

## 7. Honest Finding: β₀ Has Little Discriminating Power for the Euclid Fields at These Settings

Three of the four fields show **zero variance in β₀ across 200 null realizations at nbins=8, threshold=50th percentile**, despite the null schemes being independently proven to randomize correctly (§5). This is diagnosed, not swept aside:

A follow-up power scan on `euclid_z_edf_north` (50 realizations per threshold, z-shuffle only) shows:

| Threshold | β₀ values seen | Variance |
|---|---|---|
| 50% | {1} | 0.000 |
| 60% | {1} | 0.000 |
| 70% | {1} | 0.000 |
| 80% | {1, 2} | 0.038 |
| 90% | {1} | 0.000 |

**Diagnosis:** at ~40% bin occupancy, the top-50%-density region of the field generically **percolates into a single connected component** — a well-known property of coarse-grained density fields near the median threshold (analogous to percolation thresholds studied in cosmic-web genus statistics). This is a property of the (statistic, threshold, resolution) combination interacting with these specific fields' occupancy, not a defect in the randomization (which is independently verified functional).

The sparser SDSS Coma field (50 objects, 6.2% occupancy) shows real, substantial null variance (σ≈1.4–1.8) — sparse fields don't hit the percolation regime at this threshold.

**This is reported as a genuine engineering/statistical-power finding**, not forced into a "pass." Any future WP wanting a discriminating topology statistic on Euclid-density fields at this cone size should either use a higher/narrower threshold window (~80% showed some sensitivity), increase `nbins`, or use β₁/β₂ rather than β₀ (β₂ was already nonzero for one field — 2 cavities in edf_north's real data — worth a dedicated variance study, not run here to keep this WP's scope bounded).

---

## 8. Euler Identity

Held exactly in every real-field and every null-realization computation across all 4 fields × (1 real + 400 null) evaluations — inherited directly from the exact voxel-complex formula in `pipeline/observables_real.py`, unchanged by this WP. No violations.

---

## 9. What This Does NOT Do

- Does not test any hypothesis, Stream 1's or otherwise.
- Does not pin or draft any prediction.
- Does not interpret any β₀/β₁/β₂ value, percentile rank, or occupancy fraction as evidence for or against structure, clustering, or any physical model.
- Does not claim the percolation finding (§7) is itself evidence of anything cosmological — it is a statement about the (statistic, resolution, threshold) triple's sensitivity, established via a synthetic-parameter scan, not a data-driven physics conclusion.

---

## 10. Validation Summary

| Check | Result |
|---|---|
| Cosmology cited, not from memory | ✅ Planck18, source in docstring |
| Comoving distance vs. independent integration | ✅ <0.5% agreement (16/16 tests pass) |
| Photo-z NaN handling | ✅ dropped + counted (17/7/4), never imputed |
| Comoving conversion unit tests | ✅ 16/16 pass |
| Null schemes proven non-degenerate | ✅ 8/8 pass (`test_realfield3d.py`) |
| Euler identity | ✅ holds in all 401 field evaluations per dataset |
| Bin-occupancy diagnostic reported | ✅ 6–45% depending on field |
| Statistical-power limitation | ✅ diagnosed and reported, not hidden |
| No TEST/FIT label anywhere | ✅ all ENGINEERING |
| Tier language | ✅ no Tier C claims |

---

## 11. Files

| File | Purpose |
|---|---|
| `pipeline/cosmology.py` | Planck18-cited comoving distance, Cartesian + tangent-plane conversion, redshift-drop discipline |
| `pipeline/tests/test_cosmology.py` | 16 tests incl. independent-integration cross-check |
| `pipeline/realfield3d.py` | Cartesian 3D binning + two valid null schemes |
| `pipeline/tests/test_realfield3d.py` | 8 tests incl. nonzero-variance QC (the check WP-R3 lacked) |
| `scripts/fetch_survey_redshifts.py` | New, separately-manifested SDSS spectro-z + Euclid photo-z fetcher |
| `scripts/run_wp_r5_3d_field.py` | End-to-end real-field + null-bank runner |
| `docs/FINDING_R_NULLDEGENERATE_2026_07_25.md` | Root-cause writeup of the WP-R3 defect this WP replaces |
| External disk: `wp_r5_3d_field/wp_r5_results_2026_07_25.json` | Full results, checksummed |

---

## Provenance

`Generated-by: Claude Sonnet 5 (higher-tier review per master plan requirement) | Verified-by: 24 pytest tests (16 cosmology + 8 realfield3d), all passing | Reviewed-by: T0 Y (Fable 5, 2026-07-25, docs/T0_SIGNOFF_WP_R5_R6_R7_2026_07_25.md)`
