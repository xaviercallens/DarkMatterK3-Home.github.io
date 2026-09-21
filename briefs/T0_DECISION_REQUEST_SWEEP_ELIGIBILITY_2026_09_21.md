# T0 decision request — which cells may contribute to a WP-E6-SWEEP contour?

**Date:** 2026-09-21 · **From:** Stream 3 · **To:** T0 (Xavier)
**Record:** `briefs/STREAM3_SWEEP_NONFINITE_NUISANCE_DEFECT_2026_09_21.md` §5–§7.
**Status:** decision request. Synthetic evidence only; real-data mode is still mechanically blocked on
C1–C5 (`REAL_DATA_RULING_PIN = None`), so nothing waits on this — but it must be ruled **before** the
pin, because it is part of what a sweep's output means.

## The situation in four lines

Minuit sometimes evaluates the objective at non-finite nuisances. Since 2026-09-21 that is guarded,
counted per start, and the sweep survives (T0 ruling R2). The implementation took the **most
conservative** eligibility — a guarded cell gets no verdict and the sweep's contour is WITHHELD — so
that it would decide nothing. Measured over the eight synthetic scenarios, that rule withholds
**7 of 8 sweeps** (26 of 448 cells, 5.8 %), and in one sweep removes the **entire f = 0 column**.

## The options

**E-A — keep the conservative rule.** Any guarded cell voids the contour. Honest and simple; on this
evidence the sweep would almost never report. Choosing it is in effect choosing to fix the optimizer
first (E-C).

**E-B — eligible iff the retained minimum came from a clean start.** Measured, not adopted: in
**25 of 26** ineligible cells the retained minimum came from a start with zero guarded evaluations —
the pathological start simply lost — and in no sweep does the reference minimum move. E-B would
restore those 25 and withhold exactly **one** cell, the original defect cell, whose retained χ²_min
did come from the degenerate start. It needs one line of code and a pinned sentence.

**E-C — fix the optimizer instead of adjudicating its output.** Make the pathology not happen:
a bounded or gradient-free fallback for a start that goes non-finite, or re-running that start from
a perturbed point. Cleanest in principle; it is new design, needs its own validation, and the
internal Minuit step responsible is **not yet isolated** (the counts are quantized — 17, 23, 29, 35 —
which points at a fixed-length routine, but that is an observation, not a diagnosis).

## What Stream 3 recommends, and its limits

**E-B, pinned before the real-data pin, with E-C as follow-up work.** E-B is the rule the evidence
supports: it discards a number only when that number came from a degenerate fit. Two limits, stated
because they are the weak points: the evidence is **synthetic and eight scenarios**; and "the clean
start won" shows the retained χ² is a real local minimum, **not** that it is the global one — though
the separate start-count check (zero verdict flips between 5, 7, 8 and 9 starts, all eight sweeps)
speaks to that.

Whatever is chosen, it is a **pre-registration** sentence: it belongs in the pinned sweep design, and
changing it after seeing real data would be a `TUNING_LOG.md` event.

---
*Generated-by: Claude Fable 5.1 (Stream 3, 2026-09-21) | Verified-by: `guard_incidence.json` and
`start_count_sensitivity.json`, both computed from the eight persisted sweep records |
Reviewed-by: pending T0*
