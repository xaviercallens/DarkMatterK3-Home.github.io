# WP-R7 — β₁/β₂ Discriminating-Power Scan (Follow-on to WP-R5 §7)

**Date:** 2026-07-25
**Executor:** Claude Sonnet 5
**Status:** ✅ **COMPLETE**

> ⚠️ **ENGINEERING-only.** This characterizes the STATISTIC (does β₁/β₂ carry nonzero null
> variance at settings where β₀ is percolation-saturated?), not the data. No TEST/FIT label
> (gate G1-L closed; Off-Ramp 3 terminus stands, `NO_PREDICTION_BRANCH.md` §8.5). No
> comparison to any prediction; no claim about dark matter, K3 geometry, or any hypothesis.

---

## 1. Why this WP exists

`docs/WP_R5_3D_FIELD.md` §7 found that β₀ has near-zero discriminating power for 3 of 4 real
fields at (nbins=8, threshold=50th percentile): the top-density region generically percolates
into a single connected component, so both null schemes correctly produce zero β₀ variance —
a genuine statistical-power limit, not a broken null (both schemes independently verified
functional, `pipeline/tests/test_realfield3d.py`). That report explicitly flagged β₁/β₂ as
worth a dedicated variance study and left it out of scope to keep WP-R5 bounded (one real
field, `euclid_z_edf_north`, already showed β₂=2 — two real cavities — in the actual data).
This WP runs that study.

## 2. Method

Reused WP-R5's exact pipeline (`pipeline/cosmology.py` tangent-plane conversion,
`pipeline/realfield3d.py` z-shuffle + angular CSR null schemes, `pipeline/observables_real.py`
Betti computation) via `scripts/wp_r7_beta_variance_scan.py`. For all 4 WP-R5 fields, scanned
`threshold_percentile` ∈ {50, 60, 70, 80, 90}% at fixed `nbins=8` (matches WP-R5, for direct
comparability), 50 null realizations per scheme per threshold (matches WP-R5's own §7 power
scan). Recorded β₀/β₁/β₂ mean, std, variance, and the real value's percentile rank, under both
null schemes, at every (field, threshold) combination.

## 3. Result: β₁/β₂ do carry substantially more discriminating power than β₀

Across the three Euclid fields (dense photo-z cones, ~1980–2000 objects), **β₁ and β₂ show
nonzero null variance at every single (threshold, scheme) combination scanned** — 30/30 for
those three fields. β₀ is nonzero at only 14/30 of the same combinations, concentrated at the
higher thresholds (70–90%), consistent with WP-R5 §7's percolation diagnosis: the top-density
region stays a single blob until the threshold gets aggressive enough to fragment it, but β₁
(tunnels/loops) and β₂ (cavities) are sensitive to the field's internal structure across a much
wider threshold range.

**Recommendation for any future WP choosing a topology statistic on these Euclid-cone fields at
nbins=8:** β₁ or β₂, not β₀, unless the threshold is pushed to ≥80%. This directly answers the
question WP-R5 §7 raised and left open.

## 4. Second, distinct finding: Coma's threshold scan is degenerate for a different reason

`sdss_z_coma_cluster` (the sparse field, 50 objects, 6.2% bin occupancy per
`docs/WP_R6_SURVEY_SCALES.md`) shows **numerically identical** variance at all 5 thresholds
scanned (β₀ var=2.346/2.852, β₁ var=1.014/3.744, β₂ var=0.000/0.020 for z-shuffle/CSR
respectively — unchanged from 50% through 90%). This is not a bug in the scan and not the same
phenomenon as the Euclid percolation finding: with >93% of bins empty, `np.percentile` at 50
through 90% all land on the same value (0) — the mask `field > threshold` is identical
regardless of which percentile in that range is chosen, because the percentile ladder is finer
than the field's actual value granularity at this occupancy. **For sparse fields, a blind
percentile ladder in the 50–90% range is not actually scanning distinct thresholds** — the
effective threshold only starts moving once the percentile exceeds the empty-bin fraction
(here, >93.8%). This is a genuine methodological finding about percentile-based thresholding on
sparse cubical fields, reported honestly rather than smoothed over.

## 5. Data

| Field | Nonzero-variance combos (β₁ or β₂) | Nonzero-variance combos (β₀) |
|---|---|---|
| euclid_z_edf_north | 10/10 | 4/10 |
| euclid_z_edf_fornax | 10/10 | 3/10 |
| euclid_z_edf_south | 10/10 | 7/10 |
| sdss_z_coma_cluster | 10/10 (identical across thresholds, §4) | 10/10 (identical across thresholds, §4) |

Full data: `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/wp_r7_beta_variance/wp_r7_results_2026_07_25.json`
(SHA256: `b700f1f31c40cbb32f3f325f6b28178bf8185057d1ec21dcb97a41e4618bb226`)

## 6. What this does NOT do

- Does not test any hypothesis, Stream 1's or otherwise (Off-Ramp 3 terminus stands regardless
  — this WP does not touch or reopen it).
- Does not compare real data to a null with the intent of finding an anomaly; it characterizes
  which statistic/threshold combinations are even *capable* of showing variance.
- Does not claim β₁/β₂'s greater sensitivity here generalizes beyond this specific (nbins=8,
  these 4 fields, these two null schemes) setup.

## 7. Validation

- Reused WP-R5's already-tested cosmology/realfield3d functions (24 tests, `pipeline/tests/`);
  no new pipeline code, only a new scan script.
- `check_tier_language.py`: 0 violations.
- No TEST/FIT label produced.

## 8. Files

| File | Purpose |
|---|---|
| `scripts/wp_r7_beta_variance_scan.py` | Scan runner |
| External disk: `wp_r7_beta_variance/wp_r7_results_2026_07_25.json` | Full results, checksummed |

---

## Provenance

`Generated-by: Claude Sonnet 5 | Verified-by: reuses pipeline/tests/test_cosmology.py + test_realfield3d.py (24 tests, unchanged), scan output reproduced above | Reviewed-by: [pending T0]`
