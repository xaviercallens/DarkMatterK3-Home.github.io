# WP-E6-SWEEP — Emulator evaluation point (design §4) — PINNED

**PINNED: 2026-09-17, by T0 ruling A2 (`briefs/T0_RULINGS_2026_09_17.md`; T0 text: "go for B").**
The git commit introducing this file IS the hash-pin (commit-as-pin, same precedent as
`WP_E6_SWEEP_DESIGN_PINNED_2026_09_16.md`). This commit predates any code implementing it and any
sweep-driver code. `WP_E6_SWEEP_DESIGN_PINNED_2026_09_16.md` is **not edited**; this note is the
dated resolution of its §4.

**Label of every output this governs: `exclusion` / `FIT`, never `TEST`.** This document and the
augmented covariance it specifies are ENGINEERING / DESIGN (CLAUDE.md rule 3).
**Record of the decision:** `briefs/T0_PROPOSED_RULING_SWEEP_KEFF_2026_09_17.md` (options A–D, evidence),
`briefs/T0_DECISION_REQUEST_SWEEP_KEFF_2026_09_16.md` (request + two dated corrections).
**Disclosed departure:** the proposal's original 0.1σ pass/fail gate (commit `f17f3b7`) failed on the real
emulator in band 5 (commit `b8cf11e`). T0 chose Option B, which replaces that gate with propagating the
measured bound. This is a post-result design change, ruled by T0 and logged in `TUNING_LOG.md`. No threshold
was moved.

---

## K1. Evaluation point — log-log linear interpolation at `k_eff,b`
For band b, `ln P_pred,b` = linear interpolation in `ln k` of the emulator's `ln P` on the native segment
containing `k_eff,b`:
- Native grid: 16 bins, log₁₀k = −2.2 … −0.7 (0.1-dex), lya-mfdm `emu_N100`; the 9 targets are the lowest nine.
- `k_eff,b` is taken unchanged from `data/derived/wp_e6_sweep_cov_agg9_z4p2_2026_09_16.json`
  (`k_eff_s_per_km`). Segments per band: 0 (−2.2,−2.1) extrapolated · 1 (−2.1,−2.0) · 2 (−2.0,−1.9) ·
  3 (−2.0,−1.9) · 4 (−1.8,−1.7) · 5 (−1.7,−1.6) · 6 (−1.6,−1.5) · 7 (−1.5,−1.4) · 8 (−1.5,−1.4).
- **Band 0 extrapolates 0.0030 dex below −2.2.** Any evaluation more than **0.01 dex** beyond a grid edge
  is a hard stop (exception), never a clamp.

## K2. Interpolation systematic — fixed diagonal term added to C₉ (Option B)
    C₉,sys = C₉ + diag(s_b²),   s_b = β_b · σ_b,   σ_b = sqrt((C₉)_bb)
β_b is the **maximum R-KEFF-2 curvature bound** over the 952 pre-check points (56 grid cells × 17 nuisance
points), in units of σ_b, from `data/derived/wp_e6_sweep_keff_emulator_precheck_2026_09_17.json`
(commit `b8cf11e`, SHA-256 `508717c8fa87e07e77a871b7d184e6525975cfea6357922ba9f02adf2bbace2c`,
field `bound_sigma_max_per_band`). **Pinned values:**

| band | β_b (σ units) | σ_b (km/s) | s_b² ((km/s)²) | σ inflation √(1+β²) |
|---|---|---|---|---|
| 0 | 0.161049 | 4.663873 | 0.56416863 | 1.01289 |
| 1 | 0.208265 | 3.807858 | 0.62891846 | 1.02146 |
| 2 | 0.062253 | 3.333382 | 0.04306201 | 1.00194 |
| 3 | 0.029042 | 2.495108 | 0.00525071 | 1.00042 |
| 4 | 0.162314 | 2.130127 | 0.11954302 | 1.01309 |
| 5 | 0.311839 | 2.009854 | 0.39281729 | 1.04749 |
| 6 | 0.055129 | 2.110408 | 0.01353629 | 1.00152 |
| 7 | 0.003139 | 2.322444 | 0.00005315 | 1.00000 |
| 8 | 0.029494 | 2.654403 | 0.00612911 | 1.00043 |

- The term is **data-independent** (emulator curvature only; σ_b only sets the scale) and **fixed**. It is not
  recomputed per cell or per nuisance value and not refit after any sweep output.
- Off-diagonals of C₉ are unchanged. C₉,sys⁻¹ via Cholesky; no Hartlap (design §1.3 unchanged).
- The implementation must reproduce s_b² from the JSON and C₉ artifact to ≤ 1e-6 relative and hard-stop otherwise.

## K3. Gate before the sweep runs (replaces the 0.1σ pass/fail gate)
All must hold, checked mechanically, with the result persisted before print:
1. The pre-check JSON exists with the SHA-256 above.
2. Its `wrapper_regression.pass`, `control_1_pass`, `control_2_cap_fires` and `band0_within_cap` are all true.
3. The emulator wrapper in use reproduces the 2026-07-28 grid-control outputs (max rel. diff ≤ 1e-6).
4. C₉,sys is symmetric and Cholesky-factorable, and its diagonal minus C₉'s equals the K2 table to ≤ 1e-6 relative.
Any failure is a hard stop that returns the item to T0.

## K4. One rule, no variants
The sweep uses K1 + K2 only. No parallel `k_target` run, no run without the K2 term, no alternative
interpolation order is produced or compared. Options A, C and D are not adopted; Option 3 (`k_target`) is
rejected, being 3–8× worse than K1 in every band (proposal, table).

## K5. Scope
Resolves design §4 only. Statistic, dof, labels and the aggregation rule are as pinned on 2026-09-16.
Emulator source: lya-mfdm `9182aa4` (upstream, no LICENSE; kept gitignored; never committed).

---
*Generated-by: Claude (Opus 5), recording T0 ruling A2 | Verified-by: β_b, σ_b, s_b² recomputed from the two
committed artifacts in this session | Reviewed-by: T0 Y (ruling "go for B", in session 2026-09-17)*
