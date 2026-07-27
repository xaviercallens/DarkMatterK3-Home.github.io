# WP-E7 — NOIRLab TAP Acquisition Recipe (verified 2026-07-27)

## What WP-E7 needs (from docs/WP_E7_DESI_RESOLVABILITY_PREFLIGHT_2026_07_27.md + data/MANIFEST.md)
- DESI DR1 BAO/LSS tracer catalogs: BGS (N=300,017, 0.1<z<0.4), LRG (2,138,600, 0.4<z<1.1),
  ELG (2,432,022, 0.8<z<1.6), QSO (856,652, 0.8<z<2.1), ~7,500 deg² footprint.
  `data.desi.lbl.gov` LSScats v1.5 `clustering.dat/.ran.fits` files are UNREACHABLE from
  this VM (No route to host, confirmed in MANIFEST.md lines 71-91).
- eBOSS DR16 LRG clustering NGC+SGC data+random FITS: ALREADY FETCHED successfully via
  `data.sdss.org` (reachable) — 174,816 rows combined vs. published 377,458 (MISMATCH,
  logged in MANIFEST.md — likely NGC+SGC "clustering" subset ≠ full combined BOSS+eBOSS
  sample; not investigated further here, out of scope).
- Occupancy-threshold and eBOSS-LRG-sample-identity T0 decisions are PENDING — not made
  here; both branches noted below where relevant.

## Verified via NOIRLab TAP (https://datalab.noirlab.edu/tap, pyvo 1.9.1, anonymous sync)

**No dedicated `desi_dr1` LSS/BAO clustering-catalog table exists in this TAP schema**
(no FKP/completeness/systematic weight columns, no randoms table). Full `desi_dr1.*`
table list obtained from `TAP_SCHEMA.tables` (query below); relevant tables:

| Table | Rows | Contents |
|---|---|---|
| `desi_dr1.zpix` | 23,060,727 | Redrock redshift catalog (z, zerr, zwarn, spectype, chi2, deltachi2, targeting bitmasks `bgs_target`/`desi_target`/`mws_target`, survey, program, zcat_primary, healpix/htm9). **No ra/dec column.** |
| `desi_dr1.target` | 133,235,021 | Targeting bitmasks + tileid, hpxpixel, obsconditions, priority — join key `targetid`. **No ra/dec.** |
| `desi_dr1.photometry` | 76,001,45x | RA/Dec + Legacy Survey DR9 photometry, join key `targetid`. |
| `desi_dr1.ztile` | — | Per-tile redshift catalog (alternative grouping to zpix). |

**Verdict: RA/Dec + z + tracer selection is obtainable only by joining `zpix` (z, target
bits, survey/program) to `photometry` (ra, dec) on `targetid`** — this is a real-object
catalog (individual redrock redshifts + Legacy Survey imaging), NOT the official DESI
LSS/BAO clustering catalog (no FKP weight, no `WEIGHT_SYS`, no matched random catalog).
For WP-E7's stated purpose — checking real-field resolvability/occupancy geometry, not
running an actual clustering statistic — this join is **sufficient and usable**; it is
**not** a substitute for the official clustering catalogs if a later WP wants BAO-grade
systematics weighting.

Sanity queries run (cheap, <35s each, anonymous sync, no download >10MB):
```sql
SELECT COUNT(*) as n FROM desi_dr1.zpix                                    -- 23,060,727
SELECT COUNT(*) as n FROM desi_dr1.target WHERE survey='main'              -- 133,235,021
SELECT COUNT(*) as n FROM desi_dr1.zpix WHERE survey='main' AND spectype='GALAXY'  -- 14,981,891
```
(`zcat_primary` is BOOLEAN and this TAP backend rejects `=TRUE`/`=1` literals in ADQL —
use `zcat_primary` bare as a boolean predicate, e.g. `AND zcat_primary` not `=TRUE`, in
the real pull script; not resolved further here, budget-limited.)
`TOP 5` on the join key columns confirmed queryable (returned rows, not tested at scale).

## Ready-to-run recipe (both T0-decision branches unaffected — this pulls raw z/ra/dec,
tracer-class selection depends only on target-bit convention, not on the pending
occupancy-threshold or eBOSS-sample-identity decisions)

```python
import pyvo
svc = pyvo.dal.TAPService("https://datalab.noirlab.edu/tap")

# Step 1: pull real z + targeting bits for main-survey galaxies/QSOs (adjust spectype/z
# cuts per tracer; BGS/LRG/ELG separated by desi_target/bgs_target bitmask, not spectype
# alone — bit values must be taken from the desitarget package's bitmask YAML, not
# guessed; NOT resolved in this pass, flag for the fetch script).
q = """
SELECT z.targetid, z.z, z.zwarn, z.spectype, z.survey, z.program,
       z.bgs_target, z.desi_target, p.ra, p.dec
FROM desi_dr1.zpix AS z
JOIN desi_dr1.photometry AS p ON z.targetid = p.targetid
WHERE z.survey='main' AND z.zwarn=0 AND z.spectype='GALAXY'
"""
res = svc.search(q)  # ~15M rows if unfiltered further -- MUST add z-range + bitmask
                      # cuts before running for real; this is the join pattern only.
```

Practical acquisition path for WP-E7 given this:
1. Use the join above with the tracer's exact `(zmin, zmax)` cut from the preflight JSON
   (`data/derived/wp_e7_desi_preflight_2026_07_27.json`) and the correct `desi_target`/
   `bgs_target` bitmask for BGS_BRIGHT/LRG/ELG/QSO (must be pulled from the `desitarget`
   package's public bit definitions — a 5-minute lookup, not done here).
2. Run server-side `COUNT(*)` first per tracer/z-cut to cross-check against the published
   N (BGS 300,017 etc.) before pulling rows — cheap, catches selection-cut errors early.
3. Pull `targetid, ra, dec, z` only (small columns) in batches (TAP has row/size limits on
   anonymous sync; use `TAP async` or paginate by healpix/RA range for the full LRG/ELG
   samples, which are ~2M+ rows each — full row-and-column pulls would be 10s of MB to
   ~100MB+ per tracer, i.e. this step must NOT be run to completion in a
   read-only/no-large-download recon pass; the real fetch is a separate, larger task).
4. This gives real (ra, dec, z) triples for actual field-geometry resolvability checks —
   answering "what does the real DESI field's occupancy look like" rather than the
   survey-mean arithmetic the current preflight uses — without needing
   `data.desi.lbl.gov` at all.

## What remains blocked / manual regardless of NOIRLab
- **Official LSS/BAO clustering catalogs with FKP/systematic weights and matched random
  catalogs** are NOT exposed by NOIRLab TAP's `desi_dr1` schema — these exist only as the
  `*_clustering.dat/.ran.fits` files on `data.desi.lbl.gov`, which remains unreachable
  (connection-level, verified today). SPARCL (spectra service, also NOIRLab-hosted) was
  not queried this pass — irrelevant to WP-E7 (spectra, not catalogs).
- **eBOSS DR16 LRG row-count mismatch** (174,816 fetched vs. 377,458 published) is
  unresolved — likely a real vs. combined-BOSS+eBOSS sample-identity question, i.e.
  exactly the pending "eBOSS LRG sample-identity" T0 decision; not investigated further
  here per instructions.
- **desi_target/bgs_target exact bitmask values** for BGS_BRIGHT/LRG/ELG/QSO were not
  looked up this pass (budget-limited) — needed before the join above can reproduce the
  published per-tracer N.
- **Occupancy-threshold T0 decision**: irrelevant to acquisition itself; only affects how
  a real-field pull like the one above would later be interpreted, not whether it can be
  fetched.

## Data volume estimate
- `zpix`×`photometry` join, columns above, all tracers combined (main survey, zwarn=0,
  GALAXY+QSO spectype): ~15-20M rows × ~10 columns of numeric/short-string data ≈
  low hundreds of MB if pulled in full uncompressed CSV/VOTable. Per-tracer pulls
  (BGS/LRG/ELG/QSO individually, matching published N) would each be 10s of MB. This
  recon pass pulled 0 bytes of bulk data (COUNT/TOP-5 only, well under the 10MB cap).

---
Recon pass by read-only agent, 2026-07-27. No repo files written or modified.
