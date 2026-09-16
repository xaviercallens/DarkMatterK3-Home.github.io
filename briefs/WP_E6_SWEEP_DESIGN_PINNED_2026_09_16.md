# WP-E6-SWEEP Design — PINNED (band aggregation + statistic declaration)

**PINNED: 2026-09-16, by T0 ruling A1 (`briefs/T0_RULINGS_2026_09_16.md`; ruling text
appended to `briefs/T0_DECISION_REQUEST_SWEEP_AGGREGATION_2026_07_31.md`). The git commit
introducing this file IS the hash-pin (commit-as-pin on a standalone pinned file — the
`PREDICTION_V2_AMENDMENT_DRAFT_2026_07_29.md` §9 option-2 precedent, A6 of
`T0_RATIFICATION_2026_07_29_PM.md`; `PREDICTION.md` v1.0 stays hook-protected and unedited).
This pin commit predates the commit that adds the aggregation step to
`pipeline/binmap.py` and any commit producing a 9×9 aggregated block, per the
`prereg-pipeline` invariant (pin → data-derived artifact → result).**

**Date:** 2026-09-16. **Author:** Claude (Fable 5.1), recording T0 content.
**Label of every output this design governs: `exclusion` / `FIT`** — never `TEST`
(CLAUDE.md ledger item 6; pinned amendment §5, "TEST is foreclosed by the amendment's own
design"). **Label of this document and of the 9×9 covariance artifact it specifies:
ENGINEERING / DESIGN, DRAFT** (CLAUDE.md rule 3 — a covariance is not a comparison output).

**Amends nothing.** This document resolves the two SWEEP-design requirements left open by
already-pinned or already-LIVE records, and introduces no other analysis choice:

| Requirement | Source that left it open | Resolved here |
|---|---|---|
| 66→9 band-aggregation rule | pinned amendment §8 resolution item 2 ("band-averaging scheme ... built by WP-E6-BINMAP and verified before the sweep consumes it"); `WP_E6_BINMAP_C_RESULT_2026_07_31.md`; T0 decision request 2026-07-31 | §1 (T0-ruled Option 1) |
| Statistic the sweep reports | T1 delegated ruling R3 ("the SWEEP design doc must state which statistic it reports before SWEEP runs") | §2 (restates P2B; no new content) |

---

## 1. Band aggregation — T0-ruled Option 1

### 1.1 Inputs (all already pinned or verified; none introduced here)

- **Member-level covariance** `C₆₆`: the real DESI DR1 P1D `COVARIANCE` HDU restricted to
  the 66 CSV rows at z = 4.2 that fall in the 9 emulator bands, as extracted by
  `pipeline/binmap.py::covariance_block()` behind the SHA-256 hard gate
  (`data/MANIFEST.md` pin `bbb98dc3…4857`), with its three mandatory cross-checks
  (diag = `e_total_kms`², symmetry, Cholesky) — WP-E6-BINMAP-C, coordinator-verified.
- **Grouping**: the 9 disjoint, non-empty member sets `M_b` (b = 0…8; sizes
  3, 4, 4, 6, 8, 9, 11, 11, 10) from `restriction_map()` — 0.1-dex bands centred on
  log₁₀k = −2.2 … −1.4, verified in WP-E6-BINMAP.
- **Observed vector at member level** `P₆₆`: the `p1d_kms` column of
  `data/literature/desi_dr1_lya_p1d_2026_07_27.csv` at the same 66 rows (pinned amendment
  §8 resolution item 1: real CSV central values, z = 4.2).

### 1.2 The rule

For each band b and each native DESI k-bin i ∈ M_b, with σᵢ² ≡ (C₆₆)ᵢᵢ:

    w_{b,i} = (1/σᵢ²) / Σ_{j∈M_b} (1/σⱼ²)        (i ∈ M_b),   w_{b,i} = 0 otherwise.

`W` is the 9×66 matrix of these weights. Each row sums to 1 and has support only on its
own band (bands are disjoint, so `W` has full row rank 9).

    P₉  = W P₆₆                 (aggregated observed vector, 9 entries)
    C₉  = W C₆₆ Wᵀ              (aggregated covariance, 9×9 — FULL C₆₆, off-diagonals included)
    k_eff,b = Σ_{i∈M_b} w_{b,i} kᵢ   (diagnostic only; see §4)

The weights use the **diagonal only** (T0-ruled: simplest to audit); the covariance
propagation uses the **entire** member-level block, so no cross-bin or within-bin
correlation is discarded. Consequences the implementation must satisfy (tested in
`pipeline/tests/test_binmap.py::TestBandAggregation`):

1. `C₉` is symmetric and positive-definite whenever `C₆₆` is (congruence by a full-row-rank
   `W`).
2. If `C₆₆` were diagonal, `C₉` would be diagonal with `(C₉)_bb = 1 / Σ_{j∈M_b} 1/σⱼ²` —
   the textbook inverse-variance result. With the real off-diagonals, `(C₉)_bb` is larger
   than this (positively correlated members). Both are reported in the verification brief.
3. A band with a single member reproduces that member's variance and value exactly.
4. The result is invariant under any re-ordering of members within a band.

### 1.3 Inverse and conditioning

The sweep uses `C₉⁻¹` obtained from a Cholesky factorisation of `C₉` (never a pseudo-
inverse; failure of the factorisation is a hard stop, not a fallback). **No Hartlap
correction is applied**: `C₉` derives from the survey's published covariance, not from a
finite mock ensemble, so `Chi2Profiler(..., hartlap_n=None)` (`pipeline/chi2_profile.py`).
The condition number of `C₉` is recorded in the artifact JSON.

### 1.4 Why this is a tuning event and what label follows

The aggregation rule is a post-pin analysis choice not fixed in the pinned amendment (its
§8 resolution item 2 delegated the scheme to BINMAP's build-and-verify, and BINMAP-C
correctly declined to invent it). Per the amendment's own §5 rule, every such choice is
logged in `TUNING_LOG.md` (row added in this pin commit) and every comparison consuming
`C₉`/`P₉` is `exclusion`/`FIT`. This changes nothing in practice — `TEST` was already
foreclosed for this sweep — but the row exists so the audit trail is mechanical, not
narrative.

---

## 2. Statistic declaration (T1 ruling R3 requirement) — restated from P2B, nothing new

Per `WP_E6_P2B_RESULT_2026_07_31.md` §1 (coordinator-verified, R3) and
`ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md` §2.3 (amended 2026-07-29, D2):

- **Per-cell goodness of fit:** `χ²_min(m, f)` = minimum over the 4 profiled nuisances
  (`zrei, ha, hs, taueff`) of `(P_pred − P₉)ᵀ C₉⁻¹ (P_pred − P₉)`, reported with
  **5 dof** (9 bins − 4 nuisances).
- **Exclusion in the (m, f) plane:** `Δχ²(m, f) = χ²_min(m, f) − min_grid χ²_min`, with
  **2 dof** (Wilks). The 95 % C.L. contour is `Δχ² = 5.99` (χ²₂ 0.95-quantile; P2B writes
  6.0; the exact value is computed, not recalled, in the verification brief).
- The sweep reports **both** numbers per cell and labels the exclusion contour, never a
  detection, as the headline: an exclusion or a null gets the same prominence as a
  positive result (`prereg-pipeline`, Reporting).
- F3/F4 triggers remain mechanical (CLAUDE.md rule 5); nothing here reinterprets them.

---

## 3. Implementation contract

- `pipeline/binmap.py::aggregate_bands(cov_member, grouping, data_member=None,
  k_member=None)` — pure function implementing §1.2; returns `W`, `C₉`, and (when given)
  `P₉` and `k_eff`. `covariance_block()` calls it and populates the previously-`None`
  `aggregated_9x9` key; the old `aggregation_note` text is replaced by a pointer to this
  pin.
- `scripts/wp_e6_sweep_aggregate_9x9.py` — one-command regeneration of the tracked
  artifacts `data/derived/wp_e6_sweep_cov_agg9_z4p2_2026_09_16.{npy,json}` from the
  hash-gated FITS (`python scripts/fetch_data.py && python scripts/wp_e6_sweep_aggregate_9x9.py`).
  The 2026-07-31 BINMAP-C artifacts are left untouched (their `aggregated_9x9: null` is a
  true statement about that date).
- Tests are merge-blocking and run on a clean checkout (synthetic matrices + the tracked
  66×66 artifact); FITS-dependent tests skip when the raw file is absent, as BINMAP-C's do.

---

## 4. Open item flagged, NOT resolved here (T0)

**Where the emulator is evaluated for each band.** The data side is now a weighted mean
over each band's members, whose effective wavenumber `k_eff,b` differs from the band's
nominal target `k_target,b = 10^{log₁₀k_b}`. The emulator produces predictions only at its
own 16 native bins (the 9 targets among them), not at arbitrary k, so the only currently
available comparison is `P_pred(k_target,b)` vs `P₉,b`. Whether that offset is negligible
for this sweep, or must be corrected (e.g. by a documented interpolation of the emulator to
`k_eff`, which would itself be a new analysis choice), is **not decided here**. The
verification brief tabulates `k_eff,b / k_target,b` per band so T0 can rule on numbers, not
prose. Until ruled, the SWEEP gate stays closed on this one item.

---

*Generated-by: Claude (Fable 5.1) | Verified-by: every input in §1.1 traces to
`covariance_block()`/`restriction_map()` outputs and the pinned amendment §8 resolution;
formulas in §1.2 are the T0-ruled Option 1 verbatim; §2 restates P2B/R3 without
modification; no numeric value here is new except the χ²₂ quantile, which the verification
brief computes | Reviewed-by: T0 Y for §1 content (ruling A1); §4 open item pending T0*
