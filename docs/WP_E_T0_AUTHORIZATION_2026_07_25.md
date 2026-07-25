# WP-E Series — T0 Authorization Record

**Date:** 2026-07-25
**Authority:** Xavier Callens (T0 Owner), confirmed directly in session, same delegation
pattern as `ASSUMPTIONS.md` v2.0 ("take decision... on my behalf").

---

## 1. What was authorized

The WP-E directive (pasted 2026-07-25, "STREAM 3 DIRECTIVE: WP-E Series — Autonomous GPU
Auto-Research Loop") was flagged before execution for three issues: it targets the
retracted WP-R3 null bank, it computes significance thresholds against real SDSS/Euclid
data, and it labels the result `ENGINEERING/SYNTHETIC-BOUNDING` rather than `TEST`/`FIT`.
Xavier confirmed directly, with the issues stated, that:

1. The real-data significance computation may proceed, labeled **`SANDBOX-EXPERIMENTAL`**
   (a distinct, more explicit tag than the directive's own proposal — see §2), not
   `TEST`/`FIT`, and not `ENGINEERING` either (that label is reserved for the WP-R series'
   validated infrastructure; this is exploratory).
2. The WP-R3 (retracted) null schemes are to be used **exactly as the directive specifies**,
   knowingly, as one of several branches in the sweep.
3. Immediate follow-up instruction (same turn): *"implement and consider as a sandbox and
   experimental to test different hypothesis to provide inputs for stream 2, tag it
   accordingly into the repo and in the methodology."* This reframes the entire WP-E series'
   purpose explicitly: **hypothesis generation for Stream 2's Phase M mechanism memo, not a
   validated result, not itself a candidate for PREDICTION v2.0.**

## 2. What this authorization does NOT do

- It does not reopen Off-Ramp 3 (`NO_PREDICTION_BRANCH.md` §8.5). WP-E's outputs are inputs
  *to* Stream 2's model-construction process (`briefs/STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md`),
  not a test of any pinned prediction — there is no pinned v2.0 prediction yet to test.
- It does not authorize a `TEST` or `FIT` label under any framing. Gate G1-L stays closed,
  mechanically, regardless of this document.
- It does not retroactively validate WP-R3's null schemes. They remain retracted
  (`FINDING_R_NULLDEGENERATE_2026_07_25.md`) for the WP-R series' own purposes. WP-E's use
  of them is a **known, deliberate stress-test of a broken baseline** (see
  `docs/WP_E_EMPIRICAL_BOUNDS.md` §3 for what this produces), not a re-endorsement.

## 3. Why a separate document

CLAUDE.md states falsification-trigger overrides require a written T0 ruling, and this
repo's convention throughout has been that such rulings are committed, not verbal-only. This
document is that record — it exists so a future reader (including Xavier, later) can see
exactly what was authorized, by whom, and under what explicit constraints, rather than
inferring intent from commit messages.

---

`Generated-by: Claude Sonnet 5 (T1, recording a direct T0 instruction) | Verified-by: instruction quoted verbatim from session transcript | Reviewed-by: T0 Y (Xavier, direct, 2026-07-25)`
