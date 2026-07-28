# WP-E7 — eBOSS DR16 LRG Sample-Identity Investigation (2026-07-28)

**Status:** RESOLVED. Not a data-integrity mystery — a filename/labeling error in the
fetch script. Both 174,816 and 377,458 are correct, documented counts for two different,
separately-named catalogs published by the same SDSS/eBOSS DR16 LSS release. The fetch
grabbed the smaller (eBOSS-only) catalog while the code's own comment, and the row-count
sanity check in `scripts/fetch_data.py`, describe the larger (combined BOSS+eBOSS)
catalog. No data was corrupted, mis-downloaded, or lost.

**Scope:** documentation/investigation only, per instructions. No code changed, no new
fetch run, nothing committed to git.

---

## 1. What was already on record (starting point)

- `data/MANIFEST.md` line 93: fetched `eboss_lrg_clustering_data_ngc` +
  `eboss_lrg_clustering_data_sgc` row-count total = **174,816** (exact — computed from
  the actual FITS row count via `_fits_row_count()` in `scripts/fetch_data.py`, not
  estimated). Compared against a hardcoded "published" figure of **377,458**
  (`docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md` §3, citing arXiv:2007.09000). Verdict
  logged: MISMATCH.
- `briefs/WP_E7_NOIRLAB_TAP_RECIPE_2026_07_27.md` (lines ~7-11, ~94-98): logged the
  mismatch, hypothesized "likely NGC+SGC 'clustering' subset ≠ full combined BOSS+eBOSS
  sample," explicitly left uninvestigated, flagged as a pending T0 decision
  ("eBOSS-LRG-sample-identity").
- `scripts/data_fetchers.py` lines 216-229: the code comment states the *intent* —
  "Ross et al. 2020 (arXiv:2007.09000); combined BOSS+eBOSS LRG, 377,458 objects,
  0.6<z<1.0, 9,493 deg²" — but the `EBOSS_LRG_FILES` dict immediately below it hardcodes
  four filenames all prefixed `eBOSS_LRG_clustering_*` (not `eBOSS_LRGpCMASS_*`).
- `scripts/fetch_data.py` line 45: `PUBLISHED_ROW_COUNTS` hardcodes `377_458` as the
  expected total for the NGC+SGC pair, labeled in a comment as "Combined NGC+SGC eBOSS
  LRG clustering sample (Ross et al. 2020)" — conflating "NGC+SGC combined" with
  "BOSS+eBOSS combined," which is the actual source of the false-alarm mismatch.

So going in: the fetch script's own comments already *said* it wanted the combined
BOSS+eBOSS sample and even cited the right paper and the right count (377,458) — but the
filenames it actually requested from `data.sdss.org` were for a different, smaller
sample. This is the shape of a copy/paste or naming error, not a corrupted download.

## 2. Primary-source verification

### 2a. Ross et al. 2020 (arXiv:2007.09000) — the cited paper itself

Fetched the abstract directly (https://arxiv.org/abs/2007.09000). Title: *"The Completed
SDSS-IV extended Baryon Oscillation Spectroscopic Survey: Large-scale Structure Catalogs
for Cosmological Analysis"* (Ross et al., 55 co-authors). The abstract states, verbatim
in substance:

> ...**174,816 eBOSS LRG redshifts over 4,242 deg²** in the redshift interval
> 0.6 < z < 1.0, [combined] with SDSS-III BOSS LRGs in the same redshift range to
> produce a **combined sample of 377,458 galaxy redshifts distributed over 9,493 deg²**.

This is decisive: **174,816 is not an error or a subset artifact — it is the exact,
named eBOSS-only LRG count from the paper's own abstract.** 377,458 is the same paper's
number for a *different, larger, explicitly "combined" sample* that adds BOSS-era CMASS
LRGs in the same redshift range over a larger footprint (9,493 deg² vs. eBOSS's own
4,242 deg²). The fetched data (174,816, exact FITS row count) matches the eBOSS-only
figure to the digit.

### 2b. SDSS DR16 LSS documentation page (sdss4.org/dr16/spectro/lss/)

Fetched directly. The page confirms the catalog naming convention
(`eBOSS_{samp}_clustering_*`) and explicitly documents a second, distinct sample:

> **LRGpCMASS** is an additional available `samp`... combining BOSS CMASS at redshifts
> greater than 0.6 with the eBOSS LRGs... **"We recommend that this new eBOSS+BOSS
> catalog be used in place of the z>0.6 bin from BOSS."**

So SDSS's own documentation (a) confirms LRGpCMASS is the combined-sample name and (b)
actively recommends it over either component alone for z>0.6 large-scale-structure work.

### 2c. Directory listing at the actual fetch URL

Fetched `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/` directly. Both file
families exist side by side on the server, confirming this is a same-release,
same-directory naming distinction — not a different data release or an access-restricted
product:

- `eBOSS_LRG_clustering_data-{NGC,SGC}-vDR16.fits` / `_random-{NGC,SGC}-vDR16.fits` —
  **the files actually fetched** (eBOSS-only LRG, 174,816 total).
- `eBOSS_LRGpCMASS_clustering_data-{NGC,SGC}-vDR16.fits` / `_random-{NGC,SGC}-vDR16.fits`
  (+ `_data_rec-*` / `_random_rec-*` reconstructed-density variants) — **not fetched**;
  this is the SDSS-recommended combined BOSS+eBOSS sample, 377,458 total.
- `eBOSS_LRG_full_ALLdata-vDR16.fits` — a third product (pre-veto/full target list, not
  the clustering-ready catalog); not investigated further, out of scope for this task.

## 3. Root cause

Not a real mismatch. Two conflated things:

1. **The fetch itself is correct and internally consistent** for what it is named:
   `eBOSS_LRG_clustering_data/random-{NGC,SGC}-vDR16.fits` is the genuine, complete,
   correctly-checksummed eBOSS DR16 LRG-only clustering catalog (174,816 objects,
   0.6<z<1.0, 4,242 deg², per Ross et al. 2020's own abstract). Nothing is missing or
   truncated.
2. **The sanity check compared it against the wrong reference number.** The 377,458
   figure in `docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md` §3 and hardcoded into
   `scripts/fetch_data.py::PUBLISHED_ROW_COUNTS` is the count for a *differently-named,
   not-yet-fetched* catalog (`eBOSS_LRGpCMASS_clustering_*`, combined BOSS+eBOSS). The
   code comment in `scripts/data_fetchers.py` (lines 216-218) already states the intent
   to fetch "combined BOSS+eBOSS LRG, 377,458 objects" — but the `EBOSS_LRG_FILES`
   dict two lines later requests the `eBOSS_LRG_clustering_*` (eBOSS-only) filenames
   instead of `eBOSS_LRGpCMASS_clustering_*`. The MISMATCH verdict is thus the sanity
   check correctly catching a real discrepancy — just not the one it was interpreted as
   ("did the fetch fail/truncate?" — no) — the actual discrepancy is "the fetch script
   asked for the wrong one of two legitimately different, correctly documented eBOSS
   DR16 LRG catalogs."

## 4. Recommendation for the T0 "eBOSS LRG sample identity" decision

The ambiguity is now fully resolved from public documentation — this is a **choice**, not
an open mystery. Two clean options, both well-defined:

**Option A — fetch the SDSS-recommended combined sample (LRGpCMASS).** If WP-E7's
purpose is z>0.6 large-scale-structure/BAO/RSD-style clustering analysis (which is how
`docs/WP_E7_DESI_RESOLVABILITY_PREFLIGHT_2026_07_27.md` frames it — resolvability of a
deformation-scale analysis on tracer clustering catalogs), SDSS's own documentation says
to use LRGpCMASS "in place of the z>0.6 bin from BOSS." This is the larger, higher-density
sample (377,458 over 9,493 deg², vs. 174,816 over 4,242 deg²) and is the one the fetch
script's comment already intended. Concretely: fetch
`eBOSS_LRGpCMASS_clustering_data-{NGC,SGC}-vDR16.fits` and the matching
`_random-{NGC,SGC}-vDR16.fits` (four more files, confirmed present at the same base URL,
`EBOSS_LSS_BASE_URL` in `scripts/data_fetchers.py`); treat the already-fetched
`eBOSS_LRG_*` (eBOSS-only) files as either superseded or kept as a documented secondary/
cross-check sample, not the primary one.

**Option B — keep the eBOSS-only sample deliberately.** If a future WP specifically wants
the *new sky and new statistics eBOSS itself contributes*, independent of the BOSS-era
CMASS supplement (e.g. to isolate eBOSS-specific systematics, or because the smaller
4,242 deg² footprint is intentional), the currently held 174,816-row files are already
correct, complete, and exactly what their filenames say. In this branch the only
remaining action is hygiene: fix the mislabeled comparator in
`scripts/fetch_data.py::PUBLISHED_ROW_COUNTS` (line 45) from 377,458 to 174,816, and
correct the misleading intent comment in `scripts/data_fetchers.py` (lines 216-218) so it
no longer describes the combined sample while pointing at the eBOSS-only filenames.

**This brief does not pick between A and B** — that's a WP-E7 purpose/scope call for T0,
not a factual one. What this brief resolves is that the choice is between two specific,
correctly-published, differently-named, non-overlapping-in-definition catalogs from the
same DR16 release — not a data-quality problem requiring re-fetching or forensic
recovery.

## 5. Sources

- Ross et al. 2020, "The Completed SDSS-IV extended Baryon Oscillation Spectroscopic
  Survey: Large-scale Structure Catalogs for Cosmological Analysis," arXiv:2007.09000
  (abstract fetched directly 2026-07-28).
- SDSS DR16 spectroscopic LSS documentation, https://www.sdss4.org/dr16/spectro/lss/
  (fetched directly 2026-07-28; LRGpCMASS description and recommendation).
- Directory listing, https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/ (fetched
  directly 2026-07-28; confirms both `eBOSS_LRG_clustering_*` and
  `eBOSS_LRGpCMASS_clustering_*` file families exist).
- In-repo: `data/MANIFEST.md` (lines 67-70, 80-93), `scripts/fetch_data.py` (lines 38-46,
  77-110), `scripts/data_fetchers.py` (lines 204-236),
  `briefs/WP_E7_NOIRLAB_TAP_RECIPE_2026_07_27.md`,
  `docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md` §3.

---
Investigation by read-only research pass, 2026-07-28. No repo files fetched/modified other
than this brief. Not committed to git per instructions — flagged for coordinator review.

Generated-by: Sonnet (general-purpose agent), read-only investigation | Verified-by:
every count above traces to a directly fetched primary source (arXiv abstract, SDSS DR16
docs page, SDSS SAS directory listing) or an in-repo file, cited inline; no numbers from
memory | Reviewed-by: pending T0 (Xavier)
