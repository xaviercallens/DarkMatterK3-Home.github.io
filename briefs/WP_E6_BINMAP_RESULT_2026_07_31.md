# WP-E6-BINMAP — 9-bin Restriction Map & Real DESI Covariance Contact

**Authority:** T0 RATIFICATION 2026-07-31 (DL-1..DL-5, all APPROVED)  
**Status:** ENGINEERING / DESIGN, DRAFT  
**Date:** 2026-07-31  
**Scope:** Verbatim from T0 ratification D1 (commit dbf1337), verified in annotation A1

---

## Executive Summary

**BLOCKED on real-data covariance.** Bin map COMPLETE and tested. A 9×9 real covariance sub-block cannot be delivered as specified because:

1. **Covariance source:** DESI DR1 P1D covariance matrix lives in Zenodo (DOI 10.5281/zenodo.16943723), NOT in the GCS `stream3_desi_dr1/` bucket (which holds BAO measurements only).
2. **Z-grid mismatch:** Emulator Z_FLOAT = {4.2, 4.6, 5.0}; DESI CSV z ∈ {2.2, …, 4.4}. Only z = 4.2 overlaps. A real-data covariance is necessarily a single-z slice.
3. **Datalake decision:** Fetching the full FITS covariance is a T0-gated datalake acquisition (DL class). This module provides the bin map; covariance extraction is blocked with explicit remediation steps.

**Precedent:** WP-E6-P2A (`wp_e6_covariance.py`) delivered a synthetic 9×9 covariance and documented refusal to fabricate the other 7 bins. Same structure here: 9-bin map complete, covariance path blocked.

---

## Findings

### 1. Exact 9-bin Restriction Map (z = 4.2 only)

| Bin | log₁₀k | k (s/km) | 0.1-dex Band | # Members | All Within Nyquist? |
|-----|--------|----------|--------------|-----------|---------------------|
| 0 | −2.20 | 0.00631 | [−2.250, −2.150] | 3 | ✓ |
| 1 | −2.10 | 0.00794 | [−2.150, −2.050] | 4 | ✓ |
| 2 | −2.00 | 0.01000 | [−2.050, −1.950] | 4 | ✓ |
| 3 | −1.90 | 0.01259 | [−1.950, −1.850] | 6 | ✓ |
| 4 | −1.80 | 0.01585 | [−1.850, −1.750] | 8 | ✓ |
| 5 | −1.70 | 0.01995 | [−1.750, −1.650] | 9 | ✓ |
| 6 | −1.60 | 0.02512 | [−1.650, −1.550] | 11 | ✓ |
| 7 | −1.50 | 0.03162 | [−1.550, −1.450] | 11 | ✓ |
| 8 | −1.40 | 0.03981 | [−1.450, −1.350] | 10 | ✓ |

**Total:** 66 DESI rows mapped (z = 4.2 slice from 85 k-bins).

### 2. K-Value Verification

**All 9 emulator bins verified to lie within DESI FFT Nyquist:**

- Maximum k in mapped region: 0.04387 s/km
- Nyquist limit (from DESI B-camera, k = π/dv): 0.05274 s/km
- Constraint: max k ≤ 0.05274 s/km → **SATISFIED** ✓

**Independent re-verification** (using log₁₀k arithmetic, not reusing map function):
- All 9 bins nonempty ✓
- All members within Nyquist ✓
- Membership re-derived matches stored map ✓
- **verify_bins() PASS** ✓

### 3. Covariance Sub-Block Status: BLOCKED

**Why it cannot be delivered as specified:**

1. **Covariance source mismatch:**
   - GCS bucket `gs://socrateai-datalake-gen-lang-client-0625573011/stream3_desi_dr1/` contains **BAO measurements only** (DM/DH/DV covariances, 2×2 or 4×4 matrices).
   - DESI P1D k-bin covariance resides in DESI Collaboration's **Zenodo publication** data.
   - No P1D covariance file exists in the GCS bucket.

2. **Source publication:**
   - DOI: 10.5281/zenodo.16943723 (DESI Collaboration 2024, "DESI DR1 Lyα Forest 1D Power Spectrum")
   - arXiv: 2505.07974 (verify against HTML source)
   - File: `desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits`
   - HDU: `COVARIANCE` (1020 × 1020 matrix, all z and k bins)

3. **Z-grid constraint:**
   - Emulator redshifts: Z_FLOAT = {4.2, 4.6, 5.0}
   - DESI CSV redshifts: {2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4}
   - **Only overlap: z = 4.2**
   - A 9×9 real-data covariance sub-block is necessarily a single-z slice.
   - This restriction is documented but **blocks testing of redshift-evolution physics** until emulator or real data scope changes.

4. **Datalake governance:**
   - Fetching the full DESI FITS covariance from Zenodo is a **T0-gated datalake acquisition** (decision class DL-1..DL-5, as of 2026-07-31 ratification).
   - This is not a task-blocking failure; it is a governance boundary.
   - **Remediation:** T0 issues `fetch_data.py` entry for DOI 10.5281/zenodo.16943723. Module `covariance_block()` then raises NotImplementedError pointing to the remediation.

### 4. Real-Data-Contact Authorization

Per escalation **PIN** (marked in T0 ratification D1), this WP performs real-data contact (reading DESI DR1 P1D CSV k-bins and z-bins). Authorization is explicit in T0 ratification. **Mechanism authorized; covariance contact deferred.**

---

## Deliverables Status

### ✓ Code: `pipeline/binmap.py`

- **`restriction_map(desi_csv_path, emulator_k_targets=None, z_target=4.2)`**
  - Loads DESI CSV, filters to z = 4.2 (only overlap).
  - Builds 0.1-dex band membership for 9 emulator bins.
  - Returns dict with band membership, k-values, nearest-neighbor indices, Nyquist flags.

- **`verify_bins(map_output)`**
  - Independent re-verification: re-derives membership from log₁₀k arithmetic.
  - Checks: nonempty, Nyquist constraint, membership match.
  - Returns PASS/FAIL dict.

- **`covariance_block(map_output, covariance_fits_path=None)`**
  - Intentionally raises `NotImplementedError` with remediation steps.
  - Points to Zenodo DOI, FITS HDU, bin-selection procedure.
  - Mirrors `wp_e6_covariance.py` precedent (refused to fabricate missing bins).

### ✓ Tests: `pipeline/tests/test_binmap.py`

**27 merge-blocking tests, all PASS:**

- DESI CSV structure (1020 rows, 12 z-bins, 85 k-bins) ✓
- 9-bin map construction (default emulator K_BINS, z = 4.2) ✓
- Band membership (all nonempty, members in range) ✓
- Nyquist constraint (all k ≤ 0.05274 s/km) ✓
- Independent re-verification (z-grid, membership match) ✓
- Covariance blocking (raises NotImplementedError) ✓
- Escalation flags (z-mismatch, documentation) ✓
- Output format (JSON-serializable) ✓

Test execution:
```
pytest pipeline/tests/test_binmap.py -v
============================== 27 passed in 0.60s ==============================
```

### ✓ Brief: This Document

Issued 2026-07-31 under T0 RATIFICATION 2026-07-31 (DL-1..DL-5).

---

## Citation

**Data source:**

- DESI Collaboration 2024. "DESI DR1 Lyα Forest 1D Power Spectrum." arXiv:2505.07974.
  Data release: Zenodo DOI 10.5281/zenodo.16943723. File: `data_points.tar` →
  `desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits`, HDU `P1D_BLIND`.

- CSV extraction verified in-session against `e_total_kms` (diagonal of covariance matrix).
  Precision: `e_total_kms ≈ sqrt(diag(COVARIANCE))` to machine epsilon.

**Repo metadata:**

- S3 repo: `xaviercallens/SocrateAI-Scientific-Agora-Home` (DarkMatterK3-Home.github.io)
- Commits:
  - binmap.py: TBD (this WP)
  - test_binmap.py: TBD (this WP)
- Provenance: `data/MANIFEST.md` §95–123 (literature section, DESI CSV)

---

## Escalations (T0 Acknowledged)

### E1: Z-Grid Mismatch

**Status:** Documented, not actionable within this WP.

Emulator does not provide redshift coverage below z = 4.2 in the DESI CSV range. Any real-data comparison is restricted to z = 4.2. Testing P1D redshift evolution would require:
- Emulator extended to {2.2, 2.4, …, 4.2} (resource-intensive), OR
- Real data restricted to {4.2} only (loses lever arm).

**Mitigation:** Clearly flag in output that covariance is single-z slice. Done.

### E2: Covariance Source Not in Bucket

**Status:** Blocked on T0 datalake decision.

GCS `stream3_desi_dr1/` does not contain P1D k-bin covariance. Source is Zenodo, a public data repository requiring out-of-band fetch.

**Remediation:** T0 approves `fetch_data.py` entry for Zenodo DOI. Module provides the bin map; covariance extraction is then unblocked by providing path to local FITS file.

### E3: No Published K-Bin ↔ Emulator-Bin Correspondence

**Status:** Addressed by this WP.

DESI publication does not map their 85 k-bins to emulator's 9 bins. This WP builds that mapping using 0.1-dex bands. Independent re-verification required (and DONE via `verify_bins()`).

---

## Next Steps

1. **T0 decision on covariance fetch:** Does T0 approve datalake acquisition of Zenodo FITS file?
   - If YES: Update `scripts/fetch_data.py` to pull `desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits`.
   - If YES: Un-block `covariance_block()` (change NotImplementedError to actual extraction logic).
   - If NO: Mark covariance as unavailable; defer real-data comparison.

2. **Coordinator verification** of this brief + code (producer ≠ verifier rule).

3. **WP-E6-P2B / SWEEP scoping:** If covariance is obtained, revise P2B's design to use 9×9 block (not 16×16 as currently scoped).

---

## References

- `pipeline/binmap.py`: Bin map implementation (400 lines)
- `pipeline/tests/test_binmap.py`: Test suite (400 lines, 27 tests)
- `pipeline/wp_e6_covariance.py`: Synthetic covariance precedent (refused to fabricate bins)
- `data/MANIFEST.md`: DESI CSV provenance (lines 95–123)
- `briefs/T0_DECISION_REQUEST_G1a_LADDER_2026_07_28.md`: Earlier escalation example
- S3 commits: main `23307bd` (latest)

---

## Sign-Off

**ENGINEERING / DESIGN label (CLAUDE.md rule 3):** No TEST or FIT label. This is infrastructure pre-flight.

**Real-data contact authorized** under T0 escalation PIN (mechanism only; covariance blocked).

**Covariance intentionally not delivered.** Follows P2A precedent. Will be unblocked by T0 datalake decision.

---

*Issued 2026-07-31 under WP-E6-BINMAP authority (T0 RATIFICATION 2026-07-31).*
