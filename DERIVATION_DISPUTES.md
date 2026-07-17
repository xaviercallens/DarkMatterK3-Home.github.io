# DERIVATION_DISPUTES.md — Two-Model Disagreement Log

**Status:** Initialized. Empty — no blind re-derivation has run yet.

## Purpose

Per `EXECUTION_PLAN.md` §1.2.3 (two-model rule): any Tier C physical derivation
entering `PREDICTION.md` (or `PREDICTION_APPENDIX_A.md`, or an `ASSUMPTIONS.md`
entry) must be produced by one T0-class model and independently re-derived — blind,
from the same inputs, not by reading the first model's output — by the other. If the
two derivations disagree, that disagreement is logged here, and the deliverable is
blocked until resolved. Agreement is not assumed; it is a recorded event with its
own row, same as a disagreement.

`PREDICTION.md` §7 (blind re-derivation package) names this file as the destination
for exactly this outcome.

## Entry format

| Date | Deliverable | Model A | Model B | Point of disagreement | Resolution / status |
|---|---|---|---|---|---|
| _(no entries yet)_ | | | | | |

- **Deliverable** — the specific artifact under re-derivation (e.g. "Appendix A.1
  bound on a₁", "§4 Numbers table row: β ± σ_β").
- **Model A / Model B** — which T0-class models produced the two derivations (per
  `EXECUTION_PLAN.md` §1: Fable 5 and Deep Think, or their successors).
- **Resolution / status** — `AGREED (within tolerance)`, `OPEN`, or a description of
  how the disagreement was resolved (e.g. an error found in one derivation, an
  ambiguous convention fixed and re-run). An `OPEN` row blocks the pin for anything
  depending on that deliverable.

## Related Documents

- **EXECUTION_PLAN.md** §1.2.3 — the two-model rule this file enforces.
- **PREDICTION.md** §7 — the blind re-derivation package process.
- **PREDICTION_APPENDIX_A.md** — the derivations most likely to populate this log.

---

`Generated-by: Claude Sonnet 5 (T2 plumbing) | Verified-by: none — log file, no content to verify | Reviewed-by: T0 N`
