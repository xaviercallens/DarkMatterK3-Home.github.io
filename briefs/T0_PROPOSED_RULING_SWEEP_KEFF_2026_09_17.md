# PROPOSED T0 Ruling — emulator evaluation point for the 9 aggregated bands (design §4)

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
**Negative control:** the same procedure with interpolation linear in k (not ln k) must give a
larger bound or a larger error. If it does not, the check is not discriminating and counts as a failure.

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
before any data contact. On a smooth stand-in curve that bound is ≤ 0.034σ in every band. And the choice does
not depend on the disputed size of the shift: whether the bias is 0.4σ or 1σ, the rule is the same.

## Not covered by this proposal
Whether the 2026-09-16 Opus-5 re-run satisfies producer ≠ verifier — a separate T0 item.

---
*Generated-by: Claude (Fable 5.1) | Verified-by: numbers quoted from the committed decision
request and `wp_e6_sweep_rerun_keff_audit_2026_09_16.json`; emulator K_BINS grid read from `pipeline/wp_e6_covariance.py` docstring; R-KEFF-2 design tested on `pfid_kms` stand-in (table above); no emulator run | Reviewed-by:
T0 — PENDING APPROVAL (not a ruling until signed)*
