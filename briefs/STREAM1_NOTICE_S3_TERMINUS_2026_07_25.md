# Notice to Stream 1 — Stream 3's Empirical Path Has Reached Terminus (Off-Ramp 3)

**To:** Stream 1 (Lean Formalization / orchestration)
**From:** Stream 3 (Experimentation & Data Confrontation)
**Date:** 2026-07-25
**Subject:** The Stream-1 directive requesting an implementation plan for WP S3-00/S3-03/S3-04/S3-05
(`briefs/STREAM3_EXPERIMENTATION_DIRECTIVE_2026-07-24.md`, referenced 2026-07-25, "last update on
the Lean formalization") targets a path that closed the day after it was written.

---

## 1. What the directive got right, and what's changed since

The directive's Actions 1–3 (§ WP S3-01 data acquisition, § WP S3-02 pipeline scaffold, § wait
for the three Gate-1 blockers) were accurate for 2026-07-24 and are **already complete** —
see `docs/WP_S301_S302_STATUS.md` (data-acquisition scaffold + 3/3 golden pipeline tests green,
committed 2026-07-24).

The three blockers the directive names (Stream 2 candidate selection, `ASSUMPTIONS.md`
signature, `PREDICTION.md` pin) **did clear**, on 2026-07-25 — but the subsequent attempt to
execute exactly the Action 4 the directive describes (WP S3-00, MVM matching on the selected
candidate) is also complete, and it did not reach the outcome the directive assumes it would.

## 2. What actually happened at S3-00, in order, same day (2026-07-25)

1. **F5b triggered.** No explicit flux/tadpole compactification exists for the certified
   candidate; a₁/a₂/a₃ could not be honestly derived, only bounded by placeholder intervals.
   Recorded in `NO_PREDICTION_BRANCH.md` §1–4.
2. **Swampland-bound fallback (Off-Ramp 2).** Produced a conditional window
   (`SWAMPLAND_BOUNDS_A123.md`) under an imported Dark Dimension identification [A-DD], not a
   derived number — and opened a new gap, **G-1**, between that window and any Mpc-scale
   observable.
3. **WP-A adjudication closed G-1 negative.** Under the cited chameleon mechanism, the
   mediator's range never exceeds ~30 μm at any density — **no Mpc-scale observable can test
   the B1/B3 window in principle** (`NO_PREDICTION_BRANCH.md` §8.5).
4. **WP-A2, the one authorized continuation (lab-scale re-scope), failed its own Gate 0.**
   `WP_A2_CIRCULARITY_AUDIT.md`: the non-circular region of the window is out of reach of every
   published dataset (ranges ≤ 8.81 μm vs. exclusion reach ≥ 38.6 μm, arXiv:2002.11761); the
   region within reach is circular (derived from the very lab bounds that would test it).

**Terminus: Off-Ramp 3.** The hypothesis, as anchored by [A-DD], is untestable at every scale
with data that exists today — cosmologically in principle, in the lab by circularity or reach.
This is recorded as a clean negative result, with the same prominence a positive result would
get. The only thing that reopens it is monitoring trigger **F-LAB**: future public inverse-square-
law data excluding |α|=1 below 38.6 μm. Nothing else does.

## 3. What this means for the requested implementation plan

Actions 4–6 of the directive (WP S3-00 MVM matching, S3-03/S3-04 pinned comparisons, S3-05
`OBSERVATIONAL_REPORT.md`) all presuppose a derived observable that gate **G1-L** requires and
that this program does not have — and, per the terminus above, cannot currently obtain by
completing more of the same derivation chain. Per `CLAUDE.md` rule 5, the F5b/Off-Ramp 3
falsification chain is mechanical; overriding it needs a written T0 ruling, which has not been
issued. **Stream 3 will not draft an implementation plan that reopens S3-00/S3-03/04/05 as
pending work on this basis.**

Also flagging for provenance hygiene: the directive names
`briefs/STREAM3_EXPERIMENTATION_DIRECTIVE_2026-07-24.md` as required first reading, but no file
by that name exists in this repository. If it lives only in Stream 1's repo, worth a pointer
back so the two stay in sync; if it was meant to be mirrored here, it never landed.

## 4. What remains genuinely live in Stream 3

- **Synthetic-only pipeline infrastructure** (G1 scope, no TEST/FIT) — valid, unaffected by the
  terminus.
- **WP-R series** (`briefs/HAIKU_PLAN_REALDATA_VERIFICATION_2026_07_25.md`) — real-data
  engineering (integrity checks, null-bank infrastructure, 3D field construction) that makes no
  physics claim. Complete through WP-R6, T1-reviewed
  (`docs/WP_R5_R6_SONNET_REVIEW_SIGNOFF_2026_07_25.md`), pending final T0 sign-off.
- **Monitoring trigger F-LAB** — the one condition that would reopen Gate 0
  (`WP_A2_CIRCULARITY_AUDIT.md` §5).

If Stream 1 has a *different* candidate, mechanism, or observable in mind that doesn't route
through the [A-DD] anchoring that produced this terminus, that would need its own pre-
registration — not a continuation of S3-00 on the current basis.

---

`Generated-by: Claude Sonnet 5 (Stream 3) | Verified-by: cross-reference to NO_PREDICTION_BRANCH.md §§1-8.5, WP_A2_CIRCULARITY_AUDIT.md, docs/WP_S301_S302_STATUS.md, CLAUDE.md rule 5 | Reviewed-by: T0 N — pending Xavier/Fable 5`
