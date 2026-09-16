# T0 Decision Request — Emulator evaluation point for the 9 aggregated bands (design §4)

**Date:** 2026-09-16 · **From:** Claude (Fable 5.1), T1 · **To:** T0 (Xavier Callens)
**Status:** DECISION REQUESTED — one item, the last design gate on WP-E6-SWEEP
**Scope note:** new preregistration content (WP-E6-PIN hard rule); not delegable. Filed the
same way as the 07-31 aggregation request. Nothing below is implemented.

---

**⚠ AUDIT CORRECTION (2026-09-16, later same day, Claude Opus 5 — read before the table):**
the per-band slope table and the "χ² = 3.16" figure below did **not** reproduce under an
independent recomputation; the ~1σ band-5 conclusion is estimator-dependent and does not
survive a smooth estimator. See **§ Audit correction** at the end. Draft text is left as
filed so the audit trail shows what was corrected.

## What's open

The pinned design (`WP_E6_SWEEP_DESIGN_PINNED_2026_09_16.md` §4) makes the data side a
weighted mean over each band's members, with effective wavenumber `k_eff,b`. The emulator
returns P1D only at its 16 native bins, so today the only available comparison is
`P_pred(k_target,b)` vs `P₉,b`, where `k_target` is the band's nominal centre. The ratio
`k_eff / k_target` is 0.993 … 1.019 per band (verification brief §2).

## How big is it — model-free estimate from the data table itself

No emulator was run (that is sweep code, gated). Instead the DESI 85-bin table at z = 4.2
supplies its own local slope `d ln P / d ln k`, so `|ΔP/P| ≈ |slope| · |ln(k_eff/k_target)|`:

| band | k_eff/k_t | slope (data) | ΔP/P from shift | σ/P₉ | shift / σ |
|---|---|---|---|---|---|
| 0 | 0.993 | −0.91 | 0.6 % | 5.4 % | 0.12 |
| 1 | 1.011 | −0.20 | 0.2 % | 4.7 % | 0.05 |
| 2 | 1.003 | −1.46 | 0.5 % | 4.9 % | 0.10 |
| 3 | 0.997 | −0.14 | 0.04 % | 4.7 % | 0.01 |
| 4 | 1.015 | +0.43 | 0.6 % | 4.5 % | 0.14 |
| **5** | **1.019** | **−2.89** | **5.5 %** | 5.1 % | **1.07** |
| 6 | 1.008 | −1.08 | 0.9 % | 6.6 % | 0.14 |
| 7 | 1.000 | −1.60 | 0.1 % | 9.6 % | 0.01 |
| 8 | 0.994 | −3.04 | 1.8 % | 14.7 % | 0.12 |

Treating the whole offset vector as a bias with `C₉`: **χ² = 3.16** (the 2-dof 95 % contour
is Δχ² = 5.99). A second, log-log interpolation of the table gives the same picture
(per-band 0.2–5.2 %, band 5 largest).

**Caveat, stated plainly:** these slopes come from a noisy table (±5 % per point), so the
per-band numbers are rough — band 5's −2.9 in particular may be partly noise. The
emulator's smooth P(k) would give the clean value. What the estimate does establish is
that "ignore it" is **not** safely below the error bars for every band; it has to be
ruled, not assumed away.

## The three candidate rules

1. **Evaluate the emulator at `k_eff`** by log-log linear interpolation between its 16
   native bins (9 of which are the targets; the other 7 bracket them). The model then
   answers the same question the data aggregate asks. Interpolation error is checkable on
   the emulator's own smooth curve and is documented, not hidden. One new analysis choice
   (the interpolation scheme), recorded in `TUNING_LOG.md`, outputs stay exclusion/FIT.
2. **Keep `k_target`, carry the offset as a systematic**: add `(ΔP)ᵀ`-type term or inflate
   `C₉` by the offset vector's outer product. Keeps the emulator untouched but bakes a
   data-derived bias term into the covariance — harder to audit, and the term's size
   depends on the noisy slopes above.
3. **Keep `k_target`, do nothing.** Only defensible if the emulator-side estimate of the
   shift is ≪ σ in every band; the data-side estimate says it is ~1σ in band 5, so this
   would need an explicit T0 override of a ≥1σ known bias.

## Recommendation

**Option 1.** It is the only rule that removes the mismatch rather than modelling it, it
uses the emulator exactly as built (no extrapolation — every `k_eff` lies inside the
native range), and the correction is one documented interpolation whose accuracy can be
tested on the emulator's own output before the sweep runs. Option 2 puts a noisy
data-derived term into the covariance; Option 3 knowingly accepts a bias comparable to
the error bar in one band.

## What ruling unlocks

On ruling: §4 of the pinned design is resolved by a dated resolution block in a follow-on
pinned note (the pinned file is not edited), `TUNING_LOG.md` gets the row, and WP-E6-SWEEP's
design gate is fully open — the remaining gate items are the independent (producer ≠
verifier) re-run of the aggregation step (§ below) and the sweep driver itself.

## Independent re-run status

**Done 2026-09-16, `scripts/wp_e6_sweep_rerun_and_keff_audit_2026_09_16.py` →
`data/derived/wp_e6_sweep_rerun_keff_audit_2026_09_16.json`** (JSON persisted before print).

Scope of independence, stated precisely: different session and model (Claude Opus 5) from
the producer (Claude Fable 5.1); new code that does **not** import `pipeline/`; band grouping
re-derived from the pinned design text (half-open 0.1-dex bands), member covariance
re-extracted from the FITS (SHA-256 `bbb98dc3…4857` re-checked), rule taken from design
§1.2. **Same repo, same machine, same T1 role — not an external audit.** Whether this
satisfies `EXECUTION_PLAN_2026_07_29` §0 rule 1 for promotion beyond DRAFT is T0's call.

| check | result |
|---|---|
| group sizes | 3, 4, 4, 6, 8, 9, 11, 11, 10 (matches pin) |
| member diag vs CSV `e_total_kms`² | max rel 2.7e-9 (as BINMAP-C) |
| `C₉` vs tracked `.npy` | max rel diff **2.2e-16** |
| `P₉` vs tracked JSON | exact |
| `k_eff/k_target` vs tracked JSON | exact |
| Cholesky of `C₉`; condition number | passes; 27.08 |

---

## Audit correction (2026-09-16, Claude Opus 5)

**What failed to reproduce.** No estimator tried reproduces the slope column above
(tried: central-difference gradient over the 85-bin table interpolated to `k_target`;
gradient at nearest bin; OLS of ln P on ln k within each band, on `p1d_kms` and on
`pfid_kms`; gradient across band centres; secant `k_target→k_eff` on the interpolated table).
The slope column **as printed** gives χ² = **2.46**, not 3.16. The 3.16 is close to the
log-log **interpolation** route's χ² (3.26 here), which suggests it came from that vector
rather than from the table above it. The interpolation route's per-band range (0.2–5.2 %,
band 5 largest) **does** reproduce.

**What the numbers say, all from the persisted JSON (shift/σ per band 0…8):**

| estimator | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | max | χ² |
|---|---|---|---|---|---|---|---|---|---|---|---|
| smooth — OLS within band, `p1d_kms` | .08 | .03 | .13 | .01 | .30 | .36 | .12 | .01 | .07 | 0.36 | 0.47 |
| smooth — OLS within band, DESI `pfid_kms` | .05 | .11 | .04 | .04 | .29 | .41 | .16 | .01 | .07 | 0.41 | 0.55 |
| smooth — gradient across band centres | .04 | .12 | .06 | .04 | .21 | .32 | .13 | .01 | .05 | 0.32 | 0.34 |
| point-to-point — log-log interpolation | .08 | .47 | .22 | .07 | .64 | 1.08 | .31 | .02 | .11 | 1.08 | 3.26 |
| point-to-point — central difference | .06 | .05 | .06 | .07 | .90 | .11 | .31 | .01 | .07 | 0.90 | 1.47 |
| draft slope column (as printed) | .12 | .05 | .10 | .01 | .14 | 1.07 | .14 | .01 | .12 | 1.07 | 2.46 |

**Reading (engineering, not physics).** The ~1σ figures come only from estimators that
follow the table point to point, so they pick up the ±5 % per-point scatter. The
emulator's P(k) is smooth, so the smooth rows are the closer proxy for the shift the sweep
would actually see: **≤ 0.41σ in every band, χ² ≈ 0.3–0.55 (vs 5.99 for the 2-dof 95 %
contour)**, band 5 still the largest. Which band is worst and whether it reaches 1σ depends on
the estimator, so the draft's "~1σ known bias in band 5" should not be relied on.

**Effect on the options (for T0; the decision is not delegated).**
- Option 3 is **less** clearly ruled out than the draft says: the smooth estimate is a
  ≤ 0.4σ per-band shift, not ≥ 1σ. It still is not zero, and the clean number needs the
  emulator's own curve.
- Option 1's case does not depend on the 1σ claim: it removes the mismatch instead of
  bounding it, and its interpolation error can be checked on the emulator's output before
  the sweep. The recommendation stands, on that basis only.
- Option 2 is weaker than drafted: the size of its covariance term depends on which
  estimator is chosen (χ² 0.34 → 3.26 across the rows above).

No `TUNING_LOG.md` row is added: that records a choice after T0 rules, not a proposal.

---

*Generated-by: Claude (Fable 5.1) | Verified-by: all numbers computed this session from
`data/literature/desi_dr1_lya_p1d_2026_07_27.csv` and the tracked 9×9 artifact; no emulator
run | Audit: Claude Opus 5 — slope table not reproduced; corrected in-band, JSON `wp_e6_sweep_rerun_keff_audit_2026_09_16.json` | Reviewed-by: T0 — pending*
