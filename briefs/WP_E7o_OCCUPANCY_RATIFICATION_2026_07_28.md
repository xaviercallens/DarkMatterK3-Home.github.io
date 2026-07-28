# WP E7-o — Occupancy Ratification on the Primary LRGpCMASS Sample (2026-07-28)

**Status:** COMPLETE. Column-level FITS occupancy check on the T0-selected primary
LRG catalog (`briefs/T0_DECISIONS_2026_07_28_PENDING_ITEMS.md` D3). This is a mechanical
verification pass — no scope decision made here (D3 already made the primary/secondary
call); this brief only checks that the fetched data is what it claims to be.

**Scope:** Read-only. No file under `data/raw/` was modified. No code changed. Nothing
re-fetched.

---

**Scope note on "occupancy":** this brief ratifies the *sample's data content* (row
counts, z-coverage, footprint sanity, column structure) — it does not compute or ratify
the objects/voxel occupancy criterion/threshold proposed in
`docs/WP_E7_DESI_RESOLVABILITY_PREFLIGHT_2026_07_27.md` §1, which that document's own
caveat 3 flags as an unratified proposal still awaiting T0. No occupancy-threshold verdict
is made here.

## 1. Method

Opened all four primary LRGpCMASS FITS files directly with `astropy.io.fits` (venv
`/home/callensxavier_gmail_com/venv`, astropy 6.1.7) and read out, per file: row count,
full column list, the `Z` column's min/max/percentiles/histogram, `RA`/`DEC` extent,
every `WEIGHT_*` column's min/max/mean/NaN-count/non-positive-count, and the `NZ` column.
Files:

- `data/raw/sdss_eboss_dr16_lss/eBOSS_LRGpCMASS_clustering_data-NGC-vDR16.fits`
- `data/raw/sdss_eboss_dr16_lss/eBOSS_LRGpCMASS_clustering_data-SGC-vDR16.fits`
- `data/raw/sdss_eboss_dr16_lss/eBOSS_LRGpCMASS_clustering_random-NGC-vDR16.fits`
- `data/raw/sdss_eboss_dr16_lss/eBOSS_LRGpCMASS_clustering_random-SGC-vDR16.fits`

All numbers below were read directly out of these files by the checking script (kept at
`/tmp/.../wp_e7o_occupancy_check.py` in this session's scratchpad, not committed —
reproducible by rerunning the same `astropy.io.fits` calls against the paths above); none
are estimated or recalled from memory.

## 2. Row counts

| File | Row count |
|---|---|
| LRGpCMASS data NGC | 255,741 |
| LRGpCMASS data SGC | 121,717 |
| **LRGpCMASS data TOTAL** | **377,458** |
| LRGpCMASS random NGC | 13,180,418 |
| LRGpCMASS random SGC | 6,065,434 |
| **LRGpCMASS random TOTAL** | **19,245,852** |

Data total (377,458) matches the published Ross et al. 2020 (arXiv:2007.09000) combined
BOSS+eBOSS LRGpCMASS count exactly, and matches the row-count-only MATCH verdict already
logged in `data/MANIFEST.md` line 184 — this pass re-derives the same total independently
via full FITS table reads rather than the manifest's row-count helper, so it is a genuine
second check, not a re-statement. Random-to-data ratio ≈ 51.0×. A ~50× random oversampling is typical of published SDSS/
eBOSS LSS random catalogs (kept to suppress shot noise in the random field) — this
expectation was not independently checked against a reference this session; it is
context for why the ratio is unsurprising, not a separately verified claim.

## 3. Redshift distribution

All four files carry a `Z` column. Per-file statistics (data files shown in full; random
files match the same shape):

| File | z_min | z_max | z_mean | rows z<0.6 | rows z≥1.0 | rows outside [0.6,1.0) |
|---|---|---|---|---|---|---|
| data NGC | 0.600000 | 0.999987 | 0.694683 | 0 | 0 | 0 |
| data SGC | 0.600001 | 0.999935 | 0.703959 | 0 | 0 | 0 |
| random NGC | 0.600000 | 0.999987 | 0.694075 | 0 | 0 | 0 |
| random SGC | 0.600001 | 0.999935 | 0.702530 | 0 | 0 | 0 |

**Every row in every file falls inside 0.6 ≤ z < 1.0. Zero rows outside the documented
range, in data or random, NGC or SGC.** No NaN values in `Z` in any file (0/255,741,
0/121,717, 0/13,180,418, 0/6,065,434).

Percentiles (data NGC; 0/1/5/25/50/75/95/99/100): 0.60000, 0.60103, 0.60533, 0.62953,
0.66987, 0.73836, 0.86852, 0.94767, 0.99999 (SGC percentiles are similar, skewed slightly
higher — median 0.6807 SGC vs 0.6699 NGC).

z-histogram, 0.05-wide bins, data NGC (counts): [0.55–0.60)=0, [0.60–0.65)=99,607,
[0.65–0.70)=61,699, [0.70–0.75)=37,757, [0.75–0.80)=24,172, [0.80–0.85)=15,614,
[0.85–0.90)=9,297, [0.90–0.95)=5,199, [0.95–1.00)=2,396, [1.00–1.05)=0. The sample is
heavily front-loaded toward low z: (99,607+61,699)/255,741 = 63.1% of NGC data rows sit
in [0.60,0.70) alone, and cumulatively 77.8% sit in [0.60,0.75). This shape is consistent
with the expectation that eBOSS LRG target density and the CMASS z>0.6 supplement both
fall off toward the high-z end of the bin — that expectation was not independently
verified against a target-density reference this session, it is offered as context for
the observed shape, not as a separately confirmed fact.

## 4. Sky footprint

| File | RA min | RA max | Dec min | Dec max |
|---|---|---|---|---|
| data NGC | 109.019° | 263.696° | −3.596° | 68.736° |
| data SGC | 0.0005° | 359.9995° | −10.991° | 36.247° |
| random NGC | 108.915° | 263.929° | −3.639° | 68.749° |
| random SGC | 0.000009° | 359.999998° | −10.9998° | 36.249° |

NGC forms a single contiguous RA range (109°–264°), consistent with the standard SDSS
North Galactic Cap footprint. SGC spans the full 0°–360° RA range because the SGC
footprint straddles RA=0 (standard SDSS South Galactic Cap geometry — this is expected
survey shape, not an anomaly or a data-quality flag). No RA/Dec NaNs in any file
(0 in all four). No area/solid-angle figure is computed here from these RA/Dec bounding
boxes — a bounding-box area would over-estimate the true (irregularly-masked) footprint;
the 9,493 deg² figure already on record (Ross et al. 2020, cited in
`docs/WP_E7_EBOSS_LRG_SAMPLE_IDENTITY_INVESTIGATION_2026_07_28.md` §2b) is the correct
source for footprint area, not something re-derivable from these bounds. No HEALPix/mask
column is present in these files (see column list, §5) to cross-check against directly.

## 5. Columns present and selection-relevant fields

**Schema differs between data and random files, not identical across all four.** Data
files (NGC and SGC) carry 15 columns: `RA`, `DEC`, `Z`, `WEIGHT_FKP_EBOSS`,
`WEIGHT_SYSTOT`, `WEIGHT_CP`, `WEIGHT_NOZ`, `NZ`, `LRG_ID`, `ISCMASS`,
`WEIGHT_ALL_NOFKP`, `IN_EBOSS_FOOT`, `SECTOR`, `WEIGHT_FKP_CMASS`, `WEIGHT_FKP`. Random
files carry the same 14 columns minus `LRG_ID` (no source-object ID for randoms, as
expected), in a different column order after `NZ`: `..., WEIGHT_ALL_NOFKP,
IN_EBOSS_FOOT, ISCMASS, WEIGHT_FKP_CMASS, SECTOR, WEIGHT_FKP`.

**`ISCMASS`** (bool) flags each row's provenance — CMASS-era vs. genuine-eBOSS origin.
Counts: data NGC 148,241 CMASS-origin / 107,500 eBOSS-origin; data SGC 54,401
CMASS-origin / 67,316 eBOSS-origin. **This exactly explains a NaN pattern that would
otherwise look like a data-quality problem:** `WEIGHT_FKP_EBOSS` is NaN in *precisely* the
148,241 (NGC) / 54,401 (SGC) `ISCMASS=True` rows, and `WEIGHT_FKP_CMASS` is NaN in
*precisely* the 107,500 (NGC) / 67,316 (SGC) `ISCMASS=False` rows — a 1:1 correlation,
confirmed by direct cross-tabulation, not inferred. This is the expected structure of a
combined catalog (each row only carries the FKP weight relevant to the survey it came
from; `WEIGHT_FKP` is the single combined weight to actually use) — **not an anomaly.**

**`IN_EBOSS_FOOT`** (bool) present in all files, both True/False values populated — a
genuine footprint-membership flag, not degenerate.

**`WEIGHT_CP`, `WEIGHT_NOZ`, `WEIGHT_SYSTOT`, `WEIGHT_ALL_NOFKP`, `WEIGHT_FKP`** — all
finite-ranged, no NaNs, no non-positive values, in all four files, with means near 1.0
(`WEIGHT_SYSTOT` mean 0.996 NGC / 1.009 SGC; `WEIGHT_CP` mean 1.04 NGC / 1.04 SGC —
consistent with the standard SDSS/eBOSS weighting scheme where systematic/completeness
weights cluster near unity). **`WEIGHT_SYSTOT`'s "no non-positive values" holds strictly
(min > 0 everywhere), but see §6.1 for a small handful of NGC rows where it floors to a
value effectively indistinguishable from zero (~10⁻³¹) — flagged there, not a
contradiction of the statement here.** `WEIGHT_FKP` (the combined FKP weight, no NaNs in
any file) is the field a resolvability/clustering pipeline should use rather than the two
split `WEIGHT_FKP_EBOSS`/`WEIGHT_FKP_CMASS` columns.

**`NZ`** (redshift-dependent number density, used to build FKP weights) — finite, no
NaNs, in all four files; ranges ~1.4×10⁻⁸ to ~3.0×10⁻⁴ (units consistent with a
volume number density, not independently re-derived here).

**`LRG_ID`** (data files only, int64) — not a per-row unique identifier as might be
assumed: `ISCMASS=False` (genuine-eBOSS-origin) rows carry unique real IDs (107,500
unique values for 107,500 NGC rows; 67,316 for 67,316 SGC rows — a clean 1:1), while
every `ISCMASS=True` (CMASS-origin) row shares a single shared placeholder value
`999999` (148,241 NGC rows, 54,401 SGC rows, all identical) — this is why the naive
unique-value count (107,501 / 67,317) looked lower than the row count; fully explained
by `ISCMASS`, not a defect.

**`SECTOR`** (float64) — no NaNs in either data file (NGC or SGC, checked directly). In
the **random** files, `SECTOR` is NaN for a large fraction of rows (5,436,717 / 13,180,418
NGC; 3,232,148 / 6,065,434 SGC) — but this is exact-1:1 structural, not scattered
corruption: every NaN `SECTOR` random row has `ISCMASS=False`, and every `ISCMASS=True`
random row has a populated `SECTOR` (cross-tabulated directly, confirmed exact). Same
explanatory shape as the `WEIGHT_FKP_EBOSS`/`WEIGHT_FKP_CMASS` split in §5 above, just the
opposite origin-flag assignment.

## 6. Anomalies found

1. **`WEIGHT_SYSTOT` near-zero floor, negligible fraction, NGC only.** 1 row / 255,741 in
   data NGC (0.00039%) and 58 rows / 13,180,418 in random NGC (0.00044%) carry
   `WEIGHT_SYSTOT` ≈ 10⁻³¹ (floating-point-scale, effectively zero) rather than a value
   near 1.0; both are still strictly positive, so no non-positive-value violation. **The
   SGC files show zero such rows** (data SGC min 0.863, random SGC min 0.454 — both well
   away from zero). All affected NGC rows have `ISCMASS=False` (genuine-eBOSS origin).
   A near-zero systematic-correction weight at a small number of low-completeness/edge
   sectors is a plausible benign explanation, but that specific mechanism was not
   independently traced to a sector/mask condition this session — offered as a plausible
   read, not a confirmed root cause. **Fraction affected is negligible (≤0.00044% of rows
   in the two NGC files where it occurs at all; zero occurrences in both SGC files)** and
   does not change the fit-for-purpose verdict below; flagged for completeness, not as a
   blocker.
2. **`SECTOR` is NaN for a large fraction of rows in both random files** (5,436,717 /
   13,180,418 NGC = 41.3%; 3,232,148 / 6,065,434 SGC = 53.3%) — reported as a finding, not
   silently normalized away, even though §5 shows it is fully explained by the
   `ISCMASS=False` origin split (exact 1:1 correlation, cross-tabulated directly) and is
   therefore structural rather than a parsing defect.
3. **No HEALPix/mask column present** to directly verify footprint against a published
   mask map (RA/Dec bounding box was reported instead, §4). This is a data-content gap,
   not a data-quality defect — LSS clustering catalogs of this kind commonly ship the
   veto/mask logic as a separate product; it was not investigated further here (out of
   scope for this occupancy check).
4. **No rows fall outside the documented 0.6 ≤ z < 1.0 range**, in any of the four files —
   explicitly checked and confirmed zero out-of-range rows (§3). This is a **pass**, listed
   here because the task specifically asked it be flagged either way.

Columns for which NaN/null counts were actually computed and checked this session: `Z`,
`RA`, `DEC`, `NZ`, `SECTOR`, and all seven `WEIGHT_*` columns (all zero except
`WEIGHT_FKP_EBOSS`/`WEIGHT_FKP_CMASS`, structurally explained in §5, and the
`WEIGHT_SYSTOT` floor in item 1 above). `LRG_ID` is int64 (not nullable in this
representation) and was checked for its unique-value structure instead (§5).
`IN_EBOSS_FOOT` and `ISCMASS` are bool columns confirmed to take both True/False values
(§5) — a bool column cannot itself be null in this FITS representation, so no separate
null count applies to them.

## 7. Secondary (eBOSS-only) files — presence check

Per `data/MANIFEST.md` "Sample-role classification" (T0 decision D3), the eBOSS-only
files are the labeled secondary/cross-check sample. Confirmed present on disk, not
re-fetched, not modified — row counts read (existence + row-count only, no deeper
column check, per task instructions):

| File | Present | Row count |
|---|---|---|
| `eBOSS_LRG_clustering_data-NGC-vDR16.fits` | yes | 107,500 |
| `eBOSS_LRG_clustering_data-SGC-vDR16.fits` | yes | 67,316 |
| **eBOSS-only data TOTAL** | | **174,816** |
| `eBOSS_LRG_clustering_random-NGC-vDR16.fits` | yes | 5,460,719 |
| `eBOSS_LRG_clustering_random-SGC-vDR16.fits` | yes | 3,453,453 |

174,816 matches the published eBOSS-only figure and the existing MANIFEST MATCH verdict
(`data/MANIFEST.md` line 186). Labeling in `data/MANIFEST.md` §"Sample-role
classification" correctly marks these as SECONDARY/cross-check, not primary — confirmed
by direct read of that section (lines 188–195), no discrepancy found.

## 8. Verdict

**Fit-for-purpose: YES, with one minor caveat (not blocking).**

Cross-checked against `docs/WP_E7_DESI_RESOLVABILITY_PREFLIGHT_2026_07_27.md`'s stated
purpose (z>0.6 clustering/resolvability analysis):

- Row totals match published figures exactly, confirmed at the FITS-column level (not
  just row-count), in both data and random catalogs.
- Redshift coverage is airtight: 100% of rows in all four files sit inside the documented
  0.6 ≤ z < 1.0 window; zero contamination from out-of-range redshifts.
- Sky footprint is structurally sane (NGC contiguous; SGC RA-wraps as expected for its
  known geometry); no footprint anomalies found from the RA/Dec extent check performed.
- All weight/selection columns are populated, finite, and structured exactly as a combined
  BOSS+eBOSS LRGpCMASS catalog should be (the `ISCMASS`-correlated NaN split in the two
  component FKP-weight columns is expected structure, not a defect; use `WEIGHT_FKP`
  for downstream work, not the two split columns).
- The one genuine unexplained anomaly (near-zero `WEIGHT_SYSTOT` floor, §6.1) affects
  ≤0.00044% of rows in the two NGC files where it occurs and zero rows in both SGC files;
  it does not compromise the sample for the stated z>0.6 resolvability purpose. The large
  `SECTOR`-NaN counts in the random files (§6.2) looked concerning at first glance but are
  fully and exactly explained by the `ISCMASS` origin split — not a separate defect.

**Caveats:** (1) no in-file mask/HEALPix product was available to independently verify
the footprint against a published veto map beyond RA/Dec bounding-box sanity; (2) the
near-zero-`WEIGHT_SYSTOT` rows (§6.1) were not traced to a specific root cause beyond a
plausible-but-unconfirmed read. Neither caveat blocks the WP-E7 z>0.6 resolvability use
case this catalog was fetched for.

---
Generated-by: Sonnet (Stream 3 agent), read-only occupancy check | Verified-by: every row
count, z statistic, RA/Dec extent, weight-column statistic, and NaN count above was read
directly out of the four primary FITS files via `astropy.io.fits` in this session (venv
`/home/callensxavier_gmail_com/venv`, astropy 6.1.7); the ISCMASS/`WEIGHT_FKP_*` NaN
correlation, the `LRG_ID` placeholder pattern, and the ISCMASS/`SECTOR` NaN correlation in
randoms were all independently cross-tabulated by column, not assumed; secondary-file row
counts and MANIFEST labeling were read directly, not recalled; percentages recomputed and
checked against the raw histogram/count figures before inclusion | Reviewed-by: pending T0
(Xavier)
