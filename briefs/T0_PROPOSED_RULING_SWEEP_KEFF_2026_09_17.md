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
On the emulator's own output, with no data involved:
- **Interior (bands 1–8):** for each native bin log₁₀k = −2.1 … −1.4, predict its value by
  log-log interpolation from its two neighbours (a 0.2-dex span, twice the span the sweep uses,
  so a conservative bound) and compare to the native value.
- **Edge (band 0):** predict the −2.2 bin by log-log **extrapolation** from the (−2.1, −2.0)
  segment, i.e. 0.1 dex out, about 33× the real 0.003-dex distance, and compare to the native value.
Evaluated at the fiducial point and at the corners of the (m, f) grid.
**Pass:** |interpolated − native| ≤ **0.1 σ_b** for every target band at every checked point
(σ_b from the pinned `C₉` diagonal; the edge check uses σ₀). The JSON is persisted before print. A negative control ships with it
(a deliberately wrong rule, linear in k rather than in ln k, must give a larger error).

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
rule and one capped 0.003-dex edge extrapolation. The error of each can be measured on the
emulator alone, before any data contact, with the edge check deliberately ~33× harsher than the real case. And the choice does
not depend on the disputed size of the shift: whether the bias is 0.4σ or 1σ, the rule is the same.

## Not covered by this proposal
Whether the 2026-09-16 Opus-5 re-run satisfies producer ≠ verifier — a separate T0 item.

---
*Generated-by: Claude (Fable 5.1) | Verified-by: numbers quoted from the committed decision
request and `wp_e6_sweep_rerun_keff_audit_2026_09_16.json`; emulator K_BINS grid read from `pipeline/wp_e6_covariance.py` docstring; no emulator run | Reviewed-by:
T0 — PENDING APPROVAL (not a ruling until signed)*
