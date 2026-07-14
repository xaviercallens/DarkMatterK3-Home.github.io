# Void Results: Phase 1 (2026-07-14) with Fabricated s₇ Constants

**Status**: VOID — Do not cite or use

## What Happened

The V5 Phase 1 implementation was built on fabricated sequence constants
(findings F1–F3 in `V5_SCIENTIFIC_REVIEW.md`):

- The claimed OEIS A183204 sequence (1, 13, 271, 6721, ...) does not exist in
  the OEIS database; the true A183204 is (1, 4, 48, 760, ...)
- The period integral evaluation was a divergent series (λ=25.87 << true λ=27)
- The reported Δ metric was 100% the k=0 normalization offset

All files in this archive are void as a result.

## Files Archived

- `discoveries_v5_cooper.json` — Null discovery records from fabricated math
  (3 test sectors; all three had delta_s7 = DC-mode offset only)
- (git history retains the original data for forensics)

## Lesson Learned

**WP-C1 (Provenance Gate)** was implemented to prevent synthetic data
contamination. The companion issue here — fabricated constants — is addressed
by **WP-A guardrails** in `V5_RIGOROUS_THEORY_PLAN.md`: no number without
provenance (recurrence, formula, or fetched authority).

The pivot to **s₁₀ (A005260)** as primary candidate means this false start
is truly behind us.
