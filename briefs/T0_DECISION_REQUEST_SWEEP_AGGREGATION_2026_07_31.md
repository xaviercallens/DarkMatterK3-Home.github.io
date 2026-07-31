# T0 Decision Request — SWEEP's 66→9 Band-Aggregation Rule

**Date:** 2026-07-31
**From:** Fable 5 (T1 coordinator)
**To:** T0 (Xavier Callens)
**Status:** DECISION REQUESTED — one item, blocks WP-E6-SWEEP
**Scope note:** This is filed as a decision request, not ruled under the 2026-07-31
delegation ("no Deep Think needed"). That delegation covers execution-level interpretation
of already-ratified decisions; this is new preregistration content — per the WP-E6-PIN
hard rule ("every analysis choice must trace to an ALREADY-LIVE or ALREADY-PINNED
document... do not introduce any new free analysis choice"), it must be resolved by T0
before the confirmatory test runs, exactly like PIN's original open items 1–3.

---

## What's blocking

WP-E6-BINMAP-C (S3 `f2704a3`, coordinator-verified) extracted the real DESI DR1 P1D
covariance's z=4.2 member-level 66×66 sub-block — 9 emulator bins, each covering between 3
and 11 native DESI k-bins (counts: 3,4,4,6,8,9,11,11,10). It correctly delivered the
member-level block and stopped, rather than invent a 66→9 aggregation rule: neither the
pinned amendment nor `pipeline/binmap.py` fixes one, and the off-diagonal member
correlations are non-negligible (so the choice materially changes the resulting 9-bin
covariance, not just a rounding detail).

**WP-E6-P2B's dof design (S3, coordinator-verified) is unaffected and needs no re-decision**
— it is stated correctly: 5 dof for per-cell goodness-of-fit, 2 dof (Wilks' theorem) for
Δχ² exclusion contours. Noted here only for completeness; not part of this request.

## The three candidate aggregation rules

1. **Inverse-variance weighted mean (diagonal-only).** Standard band-power practice: weight
   each native k-bin by 1/σ²_diag, ignore off-diagonal member correlations when forming the
   mean, then separately propagate the *full* member covariance (not just the diagonal)
   into the resulting 9×9 block via the weight vector: `C_9 = W C_66 Wᵀ`. This is the
   textbook default for combining correlated band-powers (Percival et al. 2001, MNRAS 327,
   1297, §3; standard in DESI/eBOSS P1D pipelines) and is the simplest to audit.
2. **Unweighted mean.** Equal weight per native bin regardless of σ. Simpler, but throws
   away information the survey's own noise model provides — no found precedent for this
   choice in the DESI P1D literature; would need independent justification.
3. **GLS-optimal weighted mean.** Weights chosen to minimize the variance of the 9-bin
   estimate given the *full* (not diagonal-only) 66×66 covariance — the fully
   correlation-aware version of (1). Statistically optimal, but the weight vector itself
   then depends on the covariance being estimated, and documenting/auditing it is more
   involved for a first pinned implementation.

## Recommendation

**Option 1 (inverse-variance weighted mean, diagonal weights + full covariance
propagation).** It matches standard practice in the literature the DESI DR1 P1D product
itself comes from, is simple enough to audit end-to-end (the weight vector is just
`1/σ²_diag` per native bin, normalized), and — critically — still propagates the *entire*
66×66 covariance (including off-diagonals) through to the resulting 9×9 block, so no
correlation information is discarded even though the weights themselves only use the
diagonal. Option 3's added optimality is marginal here (bin counts are small, 3–11 members)
and not worth the audit complexity for a preregistered pin. Option 2 has no defensible
rationale once diagonal weights are available.

## What T0 approval unlocks

On ruling: the aggregation formula gets written into a pinned SWEEP design doc alongside
the already-settled 5-dof/2-dof statistic split, `pipeline/binmap.py`'s
`covariance_block()` gets the aggregation step appended (currently returns only the
member-level block by design), and **WP-E6-SWEEP becomes unblocked** — the last remaining
gate item once TW2-A's independent CY4/M₁₉ track (unrelated to this empirical-test track)
resolves separately.

---

*Verification note: BINMAP-C's per-bin member counts and the "off-diagonal non-negligible"
claim were read directly from `briefs/WP_E6_BINMAP_C_RESULT_2026_07_31.md` and
`data/derived/wp_e6_binmap_c_cov_member66_z4p2_2026_07_31.json`, not restated from the
agent's prose summary alone.*
