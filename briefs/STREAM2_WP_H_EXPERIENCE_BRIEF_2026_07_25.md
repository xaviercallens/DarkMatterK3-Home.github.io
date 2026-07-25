# Stream 2 Brief — Experience Return from WP-H (Auto-Research Triage, SANDBOX-EXPERIMENTAL)

**Date:** 2026-07-25
**From:** Claude Sonnet 5 (T1), drafting under standing practice (WP-H itself was drafted
T1, `docs/WP_H_AUTO_RESEARCH_TRIAGE.md`)
**To:** Stream 2 — specifically the M1 mechanism memo under
`briefs/STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md`
**Status:** T0 N — pending Xavier/T0 review before Stream 2 treats §2–§4 below as binding
**Source material:** `docs/WP_H_AUTO_RESEARCH_TRIAGE.md` (full run record),
`pipeline/hypothesis_registry.py` (26 mechanical verdicts)

---

## 1. What this is, and what it is not

WP-H ran a mechanical triage of an external, unreviewed 25-hypothesis brief, then executed
the 6 hypotheses that turned out to be computable against the four real WP-R5 catalogues.
This document extracts the **experience return** — what that run teaches Stream 2 — as a
short, self-contained input. It is not a new WP-H result, not a data delivery, and not a
substitute for reading the full record.

**It does not license anything new.** G1-L is still closed. Nothing here may be cited as
`TEST` or `FIT`, and none of it may be imported into a derivation without re-tracing to its
own source. Points 2–4 below are the parts of the experience return that bind M1; point 5
is process learning with no numeric content.

## 2. Binding finding: the scale wall is tighter than `WP_R6_SURVEY_SCALES.md` stated

`STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md` §4 already bounds transverse resolution at
0.22–0.27 Mpc from the WP-R6 facts table. WP-H's H-B10 run adds a fact WP-R6 did not have
in isolation: **no data configuration reaches that window with a non-degenerate topology
statistic at the same time.**

- Deep Euclid photo-z cones: transverse bins 2.5–12 Mpc across nbins 4–16 (Gpc-deep,
  ~2000 objects) — one to two orders of magnitude coarser than the window.
- The one field with sub-0.27 Mpc transverse bins (`sdss_z_coma_cluster`, 0.016–0.062 Mpc)
  has 50 objects and β₁=β₂=0 at every resolution tested — no topology to measure.

**How to apply:** any M1 mechanism whose predicted signature sits at or near the 0.22–0.27
Mpc floor must say so in its own §1 as untestable-by-construction with current data,
per the directive's §4 closing paragraph. This is not a new wall alongside the three named
in the directive's §3 — it sharpens the existing measurement envelope in §4 and should be
cited there, not treated as a fourth named wall.

## 3. β₂ does not currently separate real fields from randomized nulls

H-B2/H-C4/H-C5 (β₂ density-split contrast against 50 CSR/z-shuffle nulls per field): real
β₂ values landed at the 0th–74th percentile, with two fields producing an undefined
percentile (zero-variance null distribution, correctly reported as `None`, not coerced to
0 or 100). No field showed real β₂ separated from its null band.

**How to apply:** a mechanism memo proposing β₂ as its discriminating statistic needs to
argue for a regime (resolution, redshift range, threshold) where separation from CSR/
z-shuffle nulls actually appears — WP-R7's finding that β₁/β₂ carry nonzero null *variance*
(cited in the directive §4) is a weaker claim than *separation*, and WP-H shows the two
should not be conflated.

## 4. Provenance defects in the source brief — do not reimport

Three defects surfaced during triage; all are now regression-tested
(`pipeline/tests/test_hypothesis_registry.py`) so they cannot silently re-enter, but Stream 2
should not encounter them fresh in some other quotation of the same source brief:

- **Two fabricated constants:** τ = 0.0000 + 1.21145i (H-B6, cited to Denef 2008
  hep-th/0801.1074 — not present) and τ_imag ≈ 0.972 (H-K3-3, cited to Friedman & Morgan
  1994 — not present). Same defect class as the retracted Cooper s7 constants
  ([[cooper-s7-ground-truth]]).
- **A circular threshold:** H-B1's "r_s ≥ 0.27 Mpc," attributed to Brax et al. (2012), is
  numerically this repo's own measured survey resolution floor (`WP_R6_SURVEY_SCALES.md`).
  A bound equal to the finest resolvable scale cannot fail — same failure mode that ended
  WP-A2's circularity audit.
- **A premise contradicting Stream 2's own certificate:** H-A5 asserts Type III fibres for
  Cooper s7; `C1loci_cooper_s7_partner.json` records Type II. This is not a neutral
  discrepancy — Type II vs. Type III is exactly the a₁ "Type II veto" wall in the directive's
  §3. Any future citation of this brief's fibre-type claim should be traced to the
  certificate, not the brief.

## 5. Process learning (no numeric content, applies to M1/M2 method)

- **Tautological-zero check.** WP-H's first Δ run passed a null kernel, making the
  stability statistic zero by mathematical construction rather than by genuine stability —
  it read as a perfect result and was a no-op. Same failure class as the retracted WP-R3
  null bank. Any M2 derivation step that reports a residual, error, or discrepancy at
  exactly zero (or a suspiciously clean pass) should have a standing degeneracy guard before
  the number is trusted.
- **Confirmation-shaped null tests are not controls.** Three of the brief's hypotheses
  (H-C1/H-C2/H-C3) stated their null test as "the alternative model fails," including one
  pair (H-A1 vs. H-C3) that are exact negations of each other with neither independently
  derived — a coin flip framed as two predictions. Genuine adversarial control in this repo
  comes from `pipeline/siblings.py` (P4: s7 and s10 wired, only two families, both
  motivated independently) — not from constructing a comparison whose failure mode was
  chosen after the favoured answer.

## 6. What Stream 2 should not do with this brief

- Do not cite WP-H's runnable-subset numbers (§3 of the full record) as support for or
  against any mechanism — they are resolution/degeneracy statements about the data, not
  measurements of physics, and every one of them is a described point-set property that a
  generic filamentary process would also show.
- Do not treat "6 of 26 runnable" as partial validation of the source brief — the 6 runnable
  hypotheses were never claims Stream 2 endorsed; they were the subset a mechanical triage
  found computable, each with a mandatory `claim_gap` stating what computing it does not
  establish.

---

`Generated-by: Sonnet 5 (T1) | Verified-by: all claims traced to docs/WP_H_AUTO_RESEARCH_TRIAGE.md §§2–4 and pipeline/hypothesis_registry.py, re-read in full before drafting | Reviewed-by: T0 N — pending Xavier`
