# GCS Datalake Manifest — Lightweight Audit Trail (v0.1)

**Generated:** 2026-07-31T17:30:00Z
**Bucket:** `gs://socrateai-datalake-gen-lang-client-0625573011`
**Status:** PRESENT for all 1155+ enumerated objects; SHA-256 audit on critical small files in progress (see WP-DL-MANIFEST notes below).
**Quarantined:** 2 · **Absent (retracted claims):** 4

---

## Note on Versioning

This is **v0.1 (lightweight)** — a live checklist of what exists in the bucket as of 2026-07-31 enumeration. Full SHA-256 audit of all ≤100 MB analysis-relevant objects is ongoing under WP-DL-MANIFEST (the `audit_datalake.py` script). This manifest will be updated to v1.0 (full hashes) once that WP completes.

---

## Status Vocabulary (Closed Set)

- **PRESENT**: Object verified to exist in bucket via `gcloud storage ls`.
- **AUDITED**: Full SHA-256 hash computed on download (reserved for v1.0).
- **QUARANTINED**: Object flagged for audit/review before use; remains in bucket untouched.
- **ABSENT**: Retracted from 2026-07-31 status table; does not exist in bucket (verified 2026-07-31).

⚠️ **Never emitted: "VERIFIED"** (reserved for human review only).

---

## Actual Folders & Holdings (Verified Exist)

### stream3_desi_dr1/ — DESI 2024 BAO + SDSS DR12/DR16/MGS
- `desi_2024_gaussian_bao_*_{cov,mean}.txt` (14× files, ~14.2 MB total) — **PRESENT**
- `sdss_DR12Consensus_*.dat`, `sdss_DR16_*.dat`, `sdss_MGS_*.txt` (30+ files) — **PRESENT**
- `README.md` — **PRESENT**
- ⚠️ Includes DESI DR2 **forecast** covariances (projections, never fit as data) — **PRESENT**

### nanograv_15yr/ — NANOGrav 15-year free-spectrum distribution
- `15yr_emp_distr.json` (26 MB) — **PRESENT** (free-spectrum empirical distribution, not raw TOAs)
- `input.json`, `output.json` (metadata) — **PRESENT**

### euclid_q1/ — ESA Euclid Q1 FITS catalogs + audit certificate
- 9 FITS files across 3 tiles (tile_102042288, tile_102042289, tile_102157301) (193 MB total) — **PRESENT**
- Per-file SHA-256 audit certificate `AUDIT-EUCLID-Q1-1785441737` — **PRESENT** (verified against NASA-IPAC IRSA)
- `README.md`, `s8_joint_covariance.txt`, `s8_joint_means.txt` — **PRESENT**

### stream3_euclid_q2/ — KiDS-1000 cosmic shear bandpowers
- `kids1000_*_BandPowers.*.data*` (3 files, ~14.5 MB) — **PRESENT**
- `kids1000_bandpowers_EE.json`, covariance/params — **PRESENT**
- `euclid_q2_proxy_bridge.*` (bridging dataset) — **PRESENT**

### stream2_cy4_ml/ — Calabi-Yau 4-fold ML tensors
- Data/Transverse Weierstrass embeddings — **PRESENT**
- Partition datasets (A, B) — **PRESENT**
- Python analysis modules — **PRESENT**

### formal_verification/ — Lean 4 proof oracle
- `lean_oracle_v5.tar.gz` (32.38 MB) — **QUARANTINED** (binary; source audit pending WP-B; see `#print axioms` requirement)

### publications/ — Paper artifacts & figures
- `SocrateAI_K3_T2_Discovery_Final.pdf` (793 KB) — **QUARANTINED** (F5b claim status pending audit WP-A; title claim unsubstantiated)
- `paper_artifacts_v5.tar.gz` — **PRESENT**
- `paper_figures/*.{pdf,png}` (chi2_convergence, parameter_evolution, hodge_diamond, etc.) — **PRESENT**

### stream4_bridge/ — Stream-4 exploratory sandbox
- `convergence_report.json` — **PRESENT**
- `deterministic_k3_candidate_cooper_s10.json` — **PRESENT**
- `spectral_bridge_verification.json` — **PRESENT**
- 🔬 **EXPLORATORY SANDBOX**: no claim from Stream 4 may be cited as evidence in Streams 1–3 (T0 decision DL-3)

### checkpoints/, mcmc_posteriors/, dark_matter/, audit/, mcmc_chains/
- All holdings — **PRESENT** (inventory not enumerated here; see full WP-DL-MANIFEST output for details)

---

## Seed Rows (Immutable by T0 Ratification)

| Path | Status | Reason |
|------|--------|--------|
| `des_y3/` | **ABSENT** | Retracted from 2026-07-31 status table; verified not in bucket |
| `planck_2018/` | **ABSENT** | Retracted from 2026-07-31 table; pending P1 acquisition (T0 DL-2) |
| `ipta_dr2/` | **ABSENT** | Retracted and DEFERRED per T0 decision DL-2 |
| `proofs/GeneratedK3.lean` | **ABSENT** | Retracted from 2026-07-31 table; file does not exist |
| `formal_verification/lean_oracle_v5.tar.gz` | **QUARANTINED** | Binary unverifiable; source audit pending WP-B |
| `publications/SocrateAI_K3_T2_Discovery_Final.pdf` | **QUARANTINED** | F5b claim status pending audit WP-A |

---

## Next: Full SHA-256 Audit (WP-DL-MANIFEST v1.0)

The `audit_datalake.py` script will:
1. Compute SHA-256 for all ≤100 MB analysis-relevant objects
2. Record GCS-side MD5/CRC32C for all objects
3. Emit a detailed v1.0 manifest with per-file hashes and verification status
4. Push to S3 main with a dated commit

**ETA:** WP-DL-MANIFEST completion milestone (T2 Haiku task, parallel with daemon restart and T1 agent launches).

---

*Status: v0.1 live checklist. Coordinator verification of full v1.0 audit pending completion.*
