# T0 Sign-Off — WP-R5, WP-R6, WP-R7 (WP-R Series Closure)

**Date:** 2026-07-25
**Authority:** Fable 5 (T0), acting under Xavier's explicit instruction of 2026-07-25
("review the experimentation and signoff WP-R5/6/7"). Marked **[T0-DELEGATED]** per the
precedent of `ASSUMPTIONS.md` v2.0; Xavier's countermand window applies as always.
**Inputs reviewed:** `docs/WP_R5_3D_FIELD.md`, `docs/WP_R6_SURVEY_SCALES.md`,
`docs/WP_R7_BETA_VARIANCE_SCAN.md`, `docs/FINDING_R_NULLDEGENERATE_2026_07_25.md`,
`docs/WP_R5_R6_SONNET_REVIEW_SIGNOFF_2026_07_25.md` (T1 verification pass),
source of `pipeline/cosmology.py`, `pipeline/realfield3d.py`,
`scripts/wp_r7_beta_variance_scan.py`.

---

## 1. What T0 verified beyond the T1 pass

The T1 review (same date) already re-ran the full suite (172/172), re-ran the tier
checker (0 violations), and read the null-scheme code directly. T0's job is not to
repeat that; it is to check at least one load-bearing claim per WP **against raw data**,
independent of every report:

| Claim | Source | T0 recomputation | Verdict |
|---|---|---|---|
| 36/50 Coma spectro rows share (RA, Dec) — repeat observations, not independent objects | WP-R6 §Data-Quality | `pandas.duplicated(subset=['ra','dec'], keep=False)` on the raw CSV → **36/50 exactly** | ✅ Reproduced |
| Coma field is >93% empty bins; percentile thresholds 50–90% are degenerate (all land on 0) | WP-R7 §4 | Field rebuilt from raw CSV through the committed pipeline → empty fraction **93.8%**; `np.percentile` at 50/60/70/80/90 all = 0.0; first nonzero at 95% (=10.24) | ✅ Reproduced |
| β₁/β₂ nonzero-variance count 30/30 vs β₀ 14/30 on Euclid fields | WP-R7 §3/§5 | Recounted from the checksummed results JSON earlier this session (same session log) | ✅ Reproduced |

All three reproduce exactly. The earlier hand-count error in WP-R7's draft table
(edf_south 8/10 → 7/10) was caught and corrected *by* recomputation before commit —
that correction discipline is what the sign-off is meant to confirm exists.

## 2. Defect found at T0 review, fixed as condition of sign-off

`scripts/wp_r7_beta_variance_scan.py` was committed **without the mandatory provenance
footer** (master plan §0.3 rule 8). Every other WP-R artifact carries it. Footer added
in the sign-off commit. Minor, but rule 8 has no minor-exemption clause, and the point
of a T0 pass is that this class of omission gets caught by review, not by accident.

## 3. Rulings

1. **WP-R5 — APPROVED.** The retraction of WP-R3's null bank is handled correctly:
   root-cause doc, retraction banner in the superseded summary, replacement schemes with
   the exact QC check (nonzero ensemble variance) whose absence caused the original
   defect. The §7 percolation finding is reported as a power limitation of the
   (statistic, threshold, resolution) triple — the honest framing. Cosmology is cited,
   centralized, and cross-checked against an independent integration.
2. **WP-R6 — APPROVED.** Descriptive facts only; the duplicate-row data-quality flag is
   real (reproduced §1) and correctly prevents a bogus "0 arcsec resolution" number from
   propagating.
3. **WP-R7 — APPROVED** (with the §2 fix). Its two findings are of different kinds and
   the report correctly refuses to conflate them: the Euclid β₀ saturation is
   percolation physics of dense coarse fields; the Coma threshold degeneracy is a
   percentile-arithmetic artifact of sparse fields. Both matter for any future
   statistic choice.
4. **F6 applicability ruling (WP-R3 retraction):** F6 requires a README disclosure when
   a previously claimed **Tier A/B** result is corrected. WP-R3's retracted claim was
   labeled ENGINEERING, never Tier A/B, and never left the repo's internal docs. Ruling:
   the retraction banner + `FINDING_R_NULLDEGENERATE` doc satisfy disclosure; no README
   entry required. Recorded here so the question is settled, not skipped.
5. **Scope confirmation:** nothing in WP-R5/R6/R7 touches gate G1-L, produces a TEST/FIT
   label, or bears on the Off-Ramp 3 terminus (`NO_PREDICTION_BRANCH.md` §8.5), which
   stands unchanged.

**The WP-R series (R0–R7) is closed.** `[pending T0]` footers in the three WP docs, the
two pipeline modules, and the T1 review doc are updated to `T0 Y` in the sign-off
commit, referencing this document.

## 4. What the series leaves behind (for downstream consumers)

- A **validated real-data null infrastructure** (tangent-plane frame, two proven
  non-degenerate schemes, nonzero-variance QC in CI) that is hypothesis-agnostic.
- A **measured accessibility envelope** (WP-R6): what transverse scales, volumes, and
  number densities the data on hand can actually resolve.
- A **statistic power map** (WP-R7): which topology statistics can discriminate at all,
  at which settings, on which field types.

These three artifacts are exactly the inputs a future model-construction effort needs
*before* drafting any prediction — see the Stream 2 directive issued alongside this
sign-off (`briefs/STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md`).

---

`Generated-by: Fable 5 (T0, [T0-DELEGATED] under Xavier instruction 2026-07-25) | Verified-by: two independent raw-data recomputations (§1 table), executed this session; T1 pass docs/WP_R5_R6_SONNET_REVIEW_SIGNOFF_2026_07_25.md | Reviewed-by: T0 Y — Xavier countermand window open`
