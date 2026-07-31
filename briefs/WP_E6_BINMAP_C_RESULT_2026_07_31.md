# WP-E6-BINMAP-C — Real DESI DR1 P1D Covariance Extraction (RESULT)

**Label:** DRAFT — ENGINEERING / DESIGN (CLAUDE.md rule 3: not TEST, not FIT; no
model comparison is performed here).
**Authority:** `briefs/T1_DELEGATED_RULINGS_2026_07_31.md` R2 — authorized as
execution of already-ratified T0 D1 (`dbf1337`: "extract the true DESI covariance
before running WP-E6-SWEEP"). No new epistemic authority claimed.
**Date:** 2026-07-31.
**Predecessor:** `briefs/WP_E6_BINMAP_RESULT_2026_07_31.md` (bin map delivered,
covariance blocked pending the datalake decision — that block is what R2 cleared).

---

## 1. Acquisition + SHA-256 hard-gate transcript

Fetched via the repo's only dataset entry point (`scripts/fetch_data.py`,
extended with `fetch_desi_dr1_lya_p1d_covariance()` in
`scripts/data_fetchers.py`), gate G1 open (PREDICTION.md pinned):

- **Source:** Zenodo DOI 10.5281/zenodo.16943723 (the paper's own data release,
  arXiv:2505.07974 Data Availability), file `data_points.tar` (131,624,960 bytes).
- **Parent tar md5:** computed `33d7fc21bfd3d745ed71a0bbe80ca433` — MATCHES both
  Zenodo's published checksum (`zenodo.org/api/records/16943723`, checked live
  this session) and the value recorded in `data/MANIFEST.md` (2026-07-27 entry).
- Extracted ONLY the target member:
  `desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits`
  (25,188,480 bytes) → `data/raw/desi_dr1_lya_p1d_zenodo/` (gitignored, on the
  data disk; NOT added to git).

**HARD GATE (before any FITS read):**

```
MANIFEST pin : bbb98dc3d1865a50bb878e949a644604ce729da419db8e7db5adbb532a894857
fetcher gate : SHA-256 hard gate PASSED for desi_y1_baseline_p1d_..._contcorr_v3.fits:
               bbb98dc3d1865a50bb878e949a644604ce729da419db8e7db5adbb532a894857
independent  : $ sha256sum data/raw/desi_dr1_lya_p1d_zenodo/desi_y1_..._contcorr_v3.fits
               bbb98dc3d1865a50bb878e949a644604ce729da419db8e7db5adbb532a894857
```

Computed value == MANIFEST-pinned value, twice (fetcher's streamed hash + an
independent `sha256sum` invocation). **Gate PASSED; reading authorized.** The
gate is also enforced permanently in code: `pipeline/binmap.py::covariance_block`
re-hashes the file on every call and raises `RuntimeError` (file unread) on any
mismatch; `scripts/data_fetchers.py` refuses to return a non-pinned file.

FITS structure confirmed: HDUs `P1D_BLIND` (1020R), `SYSTEMATICS` (1020R),
`COVARIANCE` (1020×1020 float64), `COVARIANCE_STAT`, `COVARIANCE_SYST`.
Extraction uses `COVARIANCE` (= stat + syst total), consistent with the CSV's
`e_total_kms` diagonal per the MANIFEST's original in-session cross-check.

## 2. What was extracted — member-level 66×66, NOT a 9×9

Row ordering of `COVARIANCE` = 12 z-bins × 85 k-bins, identical to
`data/literature/desi_dr1_lya_p1d_2026_07_27.csv` row order (re-verified: full
1020-diagonal vs CSV `e_total_kms²`, max relative discrepancy 4.4×10⁻⁸, CSV
rounding noise).

The z = 4.2 slice contributes the pinned bin map's **66 member rows** (CSV rows
861–926; per-bin counts 3, 4, 4, 6, 8, 9, 11, 11, 10 — exactly the
`WP_E6_BINMAP_RESULT_2026_07_31.md` table; all 66 unique, ascending). The
delivered object is the **66×66 member-level sub-block** plus the 9-bin index
grouping.

**No 9×9 band-aggregated block is delivered — explicitly.** Neither the pinned
PREDICTION v2 amendment (`briefs/PREDICTION_V2_AMENDMENT_DRAFT_2026_07_29.md`,
§8 resolution item 2: the "band-averaging scheme" is named as something
WP-E6-BINMAP *builds and verifies before the sweep consumes it*, but no rule is
fixed there) nor `pipeline/binmap.py` defines an aggregation rule. Inventing one
(plain average? inverse-variance? including off-diagonal member covariance?)
would be a free analysis choice prohibited by the WP-E6-PIN hard rule. The
member-level block + grouping is sufficient input for whichever aggregation a
ruled SWEEP design later fixes — and the choice materially matters, since the
off-diagonal member correlations are non-negligible. **Flag for the SWEEP design
doc (adds to R3's statistic requirement): it must also state the 66→9 band
aggregation rule before SWEEP runs.**

## 3. Mandatory independent cross-checks — ALL PASS

| Check | Result | Value |
|---|---|---|
| diag(sub-block) == CSV `e_total_kms`², row-for-row, rtol 1e-6 | **PASS** | max rel discrepancy 2.73×10⁻⁹ |
| Symmetry (allclose with transpose, rtol 1e-12, atol 0) | **PASS** | exact |
| Positive-definiteness (`np.linalg.cholesky`) | **PASS** | factorization succeeds |

Check 1 is genuine (non-circular): the CSV was written 2026-07-27 from that
session's own Zenodo download; this FITS was fetched independently today — the
two reached the repo by different paths and agree row-for-row.

## 4. Eigenvalue spectrum / conditioning (66×66 block, (km/s)² P1D units)

- Eigenvalues: min 5.4137, max 192.8809 (all 66 strictly positive).
- First 10 (ascending): 5.414, 5.661, 6.093, 6.266, 6.416, 6.478, 6.606,
  6.910, 7.096, 7.330. Last 5: 72.69, 78.23, 86.01, 96.25, 192.88.
- **Condition number: 35.63** — numerically benign; no regularization needed
  or applied. Full spectrum in the derived JSON.

## 5. Deliverables

- `scripts/data_fetchers.py` — `fetch_desi_dr1_lya_p1d_covariance()` (md5-checked
  tar fetch, single-member extraction, SHA-256 hard gate), wired into
  `fetch_all_datasets()`; `scripts/manifest.py` use-case entry. `data/MANIFEST.md`
  updated by the standard `scripts/fetch_data.py` run (this session's rows:
  `desi_dr1_lya_p1d_covariance_fits`, full SHA-256 in the provenance appendix).
- `pipeline/binmap.py` — `covariance_block()` NotImplementedError replaced with
  the real hash-gated extraction + built-in mandatory cross-checks. Calling it
  **without** an explicit FITS path still raises NotImplementedError (real-data
  contact stays a deliberate act; also keeps the original 27-test contract).
- `pipeline/tests/test_binmap.py` — 39 tests (27 original, unmodified, all still
  passing + 12 new: hash-gate hard stop on a tampered file, pin==MANIFEST value,
  66×66 shape/grouping, independent diag/symmetry/Cholesky re-derivations,
  no-fabricated-9×9, provenance, and clean-checkout consistency of the committed
  derived artifacts against the committed CSV). Full pipeline suite: 492 passed.
- `scripts/wp_e6_binmap_c_extract.py` — one-command reproduction runner.
- `data/derived/wp_e6_binmap_c_cov_member66_z4p2_2026_07_31.npy` (66×66 block)
  and `data/derived/wp_e6_binmap_c_cov_z4p2_2026_07_31.json` (member indices,
  grouping, checks, full eigenvalue spectrum, condition number, provenance) —
  small, tracked in `data/derived/`; raw FITS/tar stay in gitignored `data/raw/`.

## 6. Status vs the SWEEP gate

R2's BINMAP-C deliverable is complete: fetch ✅ hash gate ✅ z=4.2 member
sub-block ✅ all three mandatory cross-checks ✅ `covariance_block()` implemented ✅.
Remaining before WP-E6-SWEEP opens (per T1 rulings Bookkeeping): coordinator
verification of this DRAFT (producer ≠ verifier), plus the SWEEP design doc
stating (a) its statistic (R3) and (b) — added by this brief — the 66→9 band
aggregation rule.

---

*Produced-by: WP-E6-BINMAP-C agent (T1), 2026-07-31. DRAFT pending coordinator
verification. Every number above is machine-generated this session
(`scripts/wp_e6_binmap_c_extract.py` output / `sha256sum` transcript), none
restated from memory.*
