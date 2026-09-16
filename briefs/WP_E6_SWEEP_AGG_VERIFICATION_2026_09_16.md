# WP-E6-SWEEP aggregation step — Verification pass (DRAFT)

**Date:** 2026-09-16. **Label: ENGINEERING / DESIGN, DRAFT** (CLAUDE.md rule 3). No model
comparison was run; nothing here is a result about (m, f).
**Producer = verifier in this pass** (same session, Claude Fable 5.1). The
`EXECUTION_PLAN_2026_07_29` §0 rule 1 (producer ≠ verifier) is therefore **not** satisfied
by this document: a coordinator/T0 re-run is still owed before the artifact is promoted
beyond DRAFT. What this pass does provide is three mechanically independent computations
of the same block and the full merge-blocking suite.

**Pin ordering (the prereg invariant), verified from `git log`:**
`79c9444` (2026-09-16 20:29 UTC, pinned design) → `a3ffcfd` (20:37 UTC, code + 9×9
artifact) → this brief. No 9×9 block existed in the repo before the pin.

---

## 1. What was checked

| # | Check | Method | Result |
|---|---|---|---|
| 1 | `aggregate_bands()` equals the pinned formula | plain-Python nested loops, no numpy matmul, sharing no code with the module (`_independent_option1` in the tests) | max rel. diff **< 1e-12** on synthetic and on the tracked 66×66 artifact |
| 2 | Artifact equals a third route | `numpy.einsum` with weights built from the **CSV's** `e_total_kms`² (not from `C₆₆`'s diagonal) | max rel. diff **1.2e-9** (limited by the 2.7e-9 CSV↔FITS diagonal agreement already recorded in BINMAP-C) |
| 3 | Artifact reproduces from the FITS | `covariance_block()` on the hash-gated FITS (SHA-256 `bbb98dc3…4857` re-verified) vs the tracked `.npy` | rel. diff < 1e-12 (`TestSweepAggregationFromFits`) |
| 4 | Artifact reproduces on a clean checkout | tracked 66×66 `.npy` + CSV → 9×9, no FITS | passes (`TestSweepAggregatedArtifacts`) |
| 5 | Design §1.2 properties 1–4 | dedicated tests (symmetry/Cholesky, diagonal-input reduction, single-member identity, permutation invariance) | all pass |
| 6 | No regression | `pytest pipeline/tests/` | **509 passed**, 0 failed (was 492 on 2026-08-01; +17 new) |
| 7 | Prose | `scripts/check_tier_language.py` | 0 violations |

---

## 2. Numbers T0 asked the ruling to protect (all computed this session, none recalled)

Per-band σ of the aggregated observed vector, three ways. "Full" is the pinned rule;
"diag-only" is what one gets by discarding the member off-diagonals (the shortcut the ruling
forbids); "unweighted" is the rejected Option 2.

| band | log₁₀k | n | P₉ (km/s) | σ full | σ diag-only | full/diag-only | σ unweighted | σ/P₉ |
|---|---|---|---|---|---|---|---|---|
| 0 | −2.2 | 3 | 86.73 | 4.664 | 5.124 | 0.910 | 4.668 | 5.4 % |
| 1 | −2.1 | 4 | 81.35 | 3.808 | 4.103 | 0.928 | 3.814 | 4.7 % |
| 2 | −2.0 | 4 | 68.47 | 3.333 | 3.694 | 0.902 | 3.341 | 4.9 % |
| 3 | −1.9 | 6 | 53.22 | 2.495 | 2.722 | 0.917 | 2.499 | 4.7 % |
| 4 | −1.8 | 8 | 47.89 | 2.130 | 2.090 | 1.019 | 2.131 | 4.5 % |
| 5 | −1.7 | 9 | 39.30 | 2.010 | 1.733 | 1.160 | 2.009 | 5.1 % |
| 6 | −1.6 | 11 | 32.20 | 2.110 | 1.418 | 1.488 | 2.108 | 6.6 % |
| 7 | −1.5 | 11 | 24.21 | 2.322 | 1.180 | 1.968 | 2.321 | 9.6 % |
| 8 | −1.4 | 10 | 18.04 | 2.654 | 1.133 | 2.343 | 2.657 | 14.7 % |

Three plain observations (data facts, not interpretation):

1. **Discarding the off-diagonals would shrink the high-k error bars by up to 2.34×**
   (band 8) — the effect the ruling was written to prevent. It is not uniform: in bands 0–3
   the full-covariance σ is *smaller* than diagonal-only (ratios 0.90–0.93), i.e. the
   survey's member covariance has net *negative* within-band correlation at the lowest k.
   **Dated correction note (2026-09-16) to the pinned design §1.2, property 2, second
   sentence** ("With the real off-diagonals, (C₉)_bb is larger than this (positively
   correlated members)"): true for bands 4–8, false for bands 0–3. The pinned file is not
   edited (commit-as-pin); this note is the correction of record. The rule itself, the
   formula, and the artifact are unaffected — the sentence was a wrong expectation about
   the data, not part of the rule.
2. **Option 1 vs Option 2 differ by ≤ 0.2 % in σ** here, because member σ's within a band
   are similar. The consequential choice was full-vs-diagonal propagation, not the weighting.
3. **`C₉` is strongly correlated**: off-diagonal correlations 0.022 … 0.859 (median 0.156).
   Condition number 27.1 (member block: 35.6). The 9-bin χ² must use the full `C₉⁻¹`; a
   diagonal χ² would be wrong by construction.

**Emulator evaluation point (design §4, open for T0):** `k_eff / k_target` per band =
0.993, 1.011, 1.003, 0.997, 1.015, 1.019, 1.008, 1.000, 0.994 — offsets of at most 1.9 %
in k. Whether that is negligible against the emulator's k-resolution is T0's call; the
number is now on the table.

**Statistic constants (design §2), computed with `scipy.stats.chi2.ppf`:** χ²₂ 95 %
quantile = **5.9915** (P2B's "6.0" is this value rounded); χ²₂ 68.3 % = 2.298; χ²₅ 95 % =
11.07 (per-cell goodness-of-fit reference).

---

## 3. What remains before WP-E6-SWEEP can run

1. **T0 ruling on design §4** (k_target vs k_eff). Gate closed on this one item.
2. **Independent verification** of this pass by a different session/operator (producer ≠
   verifier). Everything needed is one command: `python scripts/wp_e6_sweep_aggregate_9x9.py`
   after `scripts/fetch_data.py`, then `pytest pipeline/tests/test_binmap.py`.
3. The sweep driver itself (consuming `C₉`, `P₉`, `Chi2Profiler(hartlap_n=None)`) is not
   written; every output it produces is labeled exclusion/FIT (TUNING_LOG row 2026-09-16).

---

*Generated-by: Claude (Fable 5.1) — producer AND verifier, disclosed above | Verified-by:
three independent computations (nested loops; einsum from CSV `e_total_kms`; FITS re-extraction)
agree to ≤1.2e-9; `pytest pipeline/tests/` 509 passed; `check_tier_language.py` 0 violations |
Reviewed-by: T0 N (pending); coordinator re-run pending*
