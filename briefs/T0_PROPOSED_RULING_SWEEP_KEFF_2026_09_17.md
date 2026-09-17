# PROPOSED T0 Ruling — emulator evaluation point for the 9 aggregated bands (design §4)

> **⚠ STATUS UPDATE 2026-09-17 (later): the acceptance check R-KEFF-2 as written below FAILS on the
> real emulator, in band 5.** The threshold was committed (`f17f3b7`) before any emulator run; it has
> not been relaxed. R-KEFF-1's direction holds: evaluating at `k_target` is 3–8× worse in every band.
> **Read § "Emulator pre-check result and options for T0" at the end before the ruling text.** The text
> below is kept as committed, so the audit trail shows what was tested.

**Date:** 2026-09-17 · **Status: PROPOSED — NOT IN FORCE.** Drafted by Claude (Fable 5.1), T1,
at T0's request ("propose on my behalf"). It becomes a ruling only when T0 (Xavier Callens)
approves it in session; until then the SWEEP gate stays closed and nothing below is implemented.
**Basis:** `briefs/T0_DECISION_REQUEST_SWEEP_KEFF_2026_09_16.md`, including its audit correction
(smooth estimators: shift ≤ 0.41σ per band, χ² ≈ 0.3–0.55; the draft's "~1σ in band 5" did not
reproduce).

---

## Proposed ruling text

**R-KEFF-1. The emulator is evaluated at `k_eff,b`, not `k_target,b` (Option 1).**
For each band b, `P_pred,b` = log-log linear interpolation (ln P_emu against ln k) on the
native emulator segment containing `k_eff,b`. `k_eff,b` is the value in the tracked artifact
`data/derived/wp_e6_sweep_cov_agg9_z4p2_2026_09_16.json`; it is fixed and data-side only.
Native grid: `emu_predict.K_BINS`, 16 bins, log₁₀k = −2.2 … −0.7 in 0.1-dex steps; the 9
targets are the **lowest** nine.

| band | log₁₀k_eff − log₁₀k_target | segment used |
|---|---|---|
| 0 | −0.0030 | **extrapolation below −2.2**, using the (−2.2, −2.1) segment |
| 1 | +0.0047 | (−2.1, −2.0) |
| 2 | +0.0014 | (−2.0, −1.9) |
| 3 | −0.0012 | (−2.0, −1.9) |
| 4 | +0.0063 | (−1.8, −1.7) |
| 5 | +0.0083 | (−1.7, −1.6) |
| 6 | +0.0036 | (−1.6, −1.5) |
| 7 | +0.0002 | (−1.5, −1.4) |
| 8 | −0.0025 | (−1.5, −1.4) |

**Band 0 is the one extrapolation**: 0.003 dex below the lowest native bin (3 % of one bin
spacing). It is allowed only up to a fixed cap of **0.01 dex beyond a grid edge**; any
evaluation past the cap is a hard stop, not a silent clamp.

**R-KEFF-2. Acceptance check before the sweep runs, threshold fixed now.**
On the emulator's own output, with no data involved, bound each band's interpolation error by
the local curvature of ln P in ln k:

    f''_b ≈ |ln P(t−0.1) − 2 ln P(t) + ln P(t+0.1)| / h²,   h = 0.1·ln10,  t = log₁₀k_target,b
    bands 1–8 (interpolation):  err_b ≤ ½ f''_b · δ_b (h − δ_b) · P(k_eff,b)
    band 0 (extrapolation):     err_0 ≤ ½ f''_0 · δ_0 (h + δ_0) · P(k_eff,0)

Here δ_b is the ln-k distance from k_eff,b to the nearest node of its segment. Band 0's curvature
uses the (−2.2, −2.1, −2.0) nodes, because no node exists below −2.2. Evaluate at the fiducial
point and at the corners of the (m, f) grid.
**Pass:** err_b ≤ **0.1 σ_b** for every band at every checked point (σ_b from the pinned `C₉`
diagonal). The JSON is persisted before print.
**Negative controls (both must behave as stated, otherwise the check counts as FAILED):**
1. *Check can fail:* on the emulator curve at the fiducial point, multiply P at each band's
   curvature node by 1.10 and evaluate at worst-case placement (δ = h/2 for bands 1–8; 0.05 dex
   beyond the edge for band 0). The bound must exceed 0.1σ_b in **all 9 bands**.
   (On the `pfid_kms` stand-in: 9/9 fail with the 10 % bump, 3/9 without it.)
2. *Cap can fire:* a synthetic k_eff 0.02 dex below −2.2 must trigger the R-KEFF-1 hard stop.

Bands whose k_eff sits almost on a node (2, 3, 7, 8: |offset| ≤ 0.0025 dex) are *correctly*
insensitive to curvature at their real placement. This is why control 1 uses worst-case
placement rather than the real k_eff.

*Why this form (tested 2026-09-17 on DESI's smooth fiducial `pfid_kms` at z = 4.2 as a stand-in
curve, not the emulator):*

| band | true error at real k_eff (σ) | leave-one-out 0.2-dex check (σ) | curvature bound (σ) |
|---|---|---|---|
| 0 | 0.004 | 0.383 | 0.005 |
| 1 | 0.010 | 0.208 | 0.009 |
| 2 | 0.004 | 0.253 | 0.003 |
| 3 | 0.004 | 0.348 | 0.004 |
| 4 | 0.025 | 0.420 | 0.025 |
| 5 | 0.034 | 0.424 | 0.032 |
| 6 | 0.012 | 0.338 | 0.012 |
| 7 | 0.000 | 0.205 | 0.000 |
| 8 | 0.001 | 0.071 | 0.002 |

An earlier draft of this proposal used a leave-one-out check over a 0.2-dex span. **It would
fail 8 of 9 bands at 0.1σ while the true error is ≤ 0.034σ**, so under R-KEFF-3 it would stop
the sweep for a reason unrelated to the real interpolation error. The curvature bound tracks the true
error in every band. This test is on a stand-in curve; the pre-registered check runs on the
emulator itself.

**R-KEFF-3. Failure is a hard stop.** If R-KEFF-2 fails anywhere, the sweep does not run and
the item returns to T0. No silent fallback to `k_target`, no covariance inflation (Option 2),
no threshold change after seeing the numbers.

**R-KEFF-4. One rule, no variants.** The sweep is run with R-KEFF-1 only. No parallel
`k_target` run is produced or compared (it would be a forking path). Options 2 and 3 are
rejected: Option 2's covariance term depends on which slope estimator is chosen (χ² 0.34 → 3.26);
Option 3 leaves a known, removable mismatch in place.

**R-KEFF-5. Audit trail.** On approval: (a) this text is pinned as a follow-on note by
commit-as-pin — the pinned design file is not edited; (b) a `TUNING_LOG.md` row records the
interpolation scheme as a post-pin analysis choice; (c) every consuming output stays
`exclusion`/`FIT`, never `TEST`; (d) the pin commit predates any sweep-driver code.

## Why this option (engineering reasons only)
It removes the k mismatch rather than estimating it. Its only new ingredients are one interpolation
rule and one capped 0.003-dex edge extrapolation. Their error is bounded on the emulator alone,
before any data contact. ~~On a smooth stand-in curve the true error is ≤ 0.034σ and the bound
≤ 0.032σ in every band.~~ **Superseded 2026-09-17:** on the real emulator the bound reaches 0.148σ
(fiducial) and 0.31σ (grid and nuisance box) in band 5; see the end of this document. The stand-in had
no curvature at band 5; the emulator and its training simulations do. And the choice does not depend on
the disputed size of the shift: whether the bias is 0.4σ or 1σ, the rule is the same.

## Not covered by this proposal
Whether the 2026-09-16 Opus-5 re-run satisfies producer ≠ verifier — a separate T0 item.

---

## Emulator pre-check result and options for T0 (2026-09-17)

### What was run
The emulator is restored (lya-mfdm `9182aa4`, gitignored; the rebuilt wrapper reproduces the
2026-07-28 grid-control outputs **exactly**, max diff 0). The committed R-KEFF-2 check was run at all
56 grid cells × 17 nuisance points (training medians + all 16 corners of the scaler training box) =
952 points. No data vector was used and no comparison made. Scripts and JSON, commit `b8cf11e`:
`wp_e6_sweep_keff_emulator_precheck_2026_09_17`, `…_failure_anatomy_…`, `…_quadratic_probe_…`,
plus `…_band5_roughness_…`.

### Result (curvature bound, units of σ_b)

| band | fiducial | median-nuisance cells failing | all 952: max | p95 | Option 3 (`k_target`) mismatch: max | p95 |
|---|---|---|---|---|---|---|
| 0 | 0.013 | 0/56 | 0.161 | 0.034 | 0.477 | 0.133 |
| 1 | 0.020 | 0/56 | 0.208 | 0.054 | 1.112 | 0.322 |
| 2 | 0.005 | 0/56 | 0.062 | 0.019 | 0.372 | 0.131 |
| 3 | 0.003 | 0/56 | 0.029 | 0.011 | 0.215 | 0.117 |
| 4 | 0.005 | 0/56 | 0.162 | 0.041 | 0.834 | 0.656 |
| **5** | **0.148** | **55/56** | **0.312** | **0.241** | **1.456** | **1.185** |
| 6 | 0.030 | 0/56 | 0.055 | 0.031 | 0.479 | 0.401 |
| 7 | 0.002 | 0/56 | 0.003 | 0.003 | 0.023 | 0.020 |
| 8 | 0.005 | 0/56 | 0.029 | 0.019 | 0.167 | 0.156 |

- **R-KEFF-2: FAIL.** Band 5 fails at the fiducial point and at 279 of 952 points. Bands 0, 1 and 4
  fail only at 13 extreme nuisance-box corners, and at 0 median-nuisance cells.
- **Controls:** control 1 as specified (fiducial): the bumped curve fails in all 9 bands, so the control **PASSES**. Control 2 fires. Band 0's
  0.003-dex extrapolation is within the cap. (Control 1 run at all 952 points is out of spec: the bump
  loses power where emulator P is small relative to data σ, i.e. at strong suppression. A "sign-fixed"
  variant did worse, 7/9 at the fiducial point, and was not adopted.)
- **Option 3 is worse than Option 1 in every band**, by 3–8×. On the emulator the `k_target` mismatch in
  band 5 is 1.19σ at p95. So the original draft's "~1σ in band 5" was right in size for the emulator.
  The 2026-09-16 audit correction's smooth-stand-in estimate (≤ 0.41σ) understated it.
- **A 3-point quadratic rule does not fix it:** 77/952 points still exceed 0.1σ, bands 4–5 up to 0.18σ.

### Why band 5 fails: real structure, not emulator noise
The second difference of ln P at node 5 (log₁₀k = −1.7) at the fiducial point is −0.191. It is:
- **stable** under input perturbations of ±1e-3 in taueff and zrei (changes ≤ 2e-4);
- **consistent across the 5 CV folds**: −0.191 ± 0.007 (std);
- **present in the training simulations**: median −0.165 (16–84 %: −0.23 … −0.10) over 3,100 z = 4.2
  CDM spectra, with the same sign as the emulator in 100 % of them.

The sampled P1D bends sharply between nodes −1.8 and −1.6 on the 0.1-dex grid, so the curve between
nodes is not determined to 0.1σ by any low-order rule. Smoothing the emulator would remove structure the
simulations contain.

### Options (each departs from the committed design after seeing it fail; that departure is what T0 rules on)

- **A — Keep linear at `k_eff`; carry the residual as a disclosed limitation only.** The sweep runs;
  every output states a pre-registered band-5 interpolation residual ≤ 0.31σ (≤ 0.21σ elsewhere at extreme
  corners). The residual is not propagated into the statistic.
- **B — Keep linear at `k_eff`; propagate the residual into the covariance.** Add a fixed, data-independent
  diagonal term (max bound_b · σ_b)² from the committed pre-check JSON. This inflates σ_b by 1.000–1.048×
  (band 5: 4.75 %, band 1: 2.15 %, others ≤ 1.3 %). It is fixed before any sweep run and uses no data. Unlike
  the rejected Option 2, it comes from one fixed estimator on the emulator, not from noisy data slopes.
- **C — Raise the threshold to 0.35σ**, which passes all 952 points. This **moves a pre-registered
  threshold after seeing it fail**, the pattern this repo's discipline exists to catch. The only defence
  is that 0.1σ was set before any emulator curve existed.
- **D — Stop; re-design** (e.g. drop or re-aggregate band 5). Changes the pinned aggregation (T0 ruling
  A1) or discards information. It is a new design item.

**T1 recommendation: B.** It keeps R-KEFF-1, which the numbers support in every band. It propagates the
known residual into the statistic rather than only disclosing it (A). It sets no new threshold (C). Its size
is fixed now, from a committed emulator-only artifact, before any comparison. Its effect is bounded and
small (≤ 4.75 % on one σ). If B is ruled, R-KEFF-2's pass/fail gate becomes: the pre-check JSON exists at a
recorded commit, the wrapper regression passes, controls 1–2 pass, and the diagonal term is taken from it
unchanged. The decision is T0's.

---
*Generated-by: Claude (Fable 5.1) | Verified-by: numbers quoted from the committed decision
request and `wp_e6_sweep_rerun_keff_audit_2026_09_16.json`; emulator K_BINS grid read from `pipeline/wp_e6_covariance.py` docstring; R-KEFF-2 bound and negative control 1 tested on `pfid_kms` stand-in; no emulator run ; emulator pre-check commit `b8cf11e` + roughness diagnostic | Reviewed-by:
T0 — PENDING APPROVAL (not a ruling until signed)*
