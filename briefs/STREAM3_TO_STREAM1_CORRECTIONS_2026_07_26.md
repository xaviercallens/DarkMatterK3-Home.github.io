# Stream 3 → Stream 1, Stream 2, T0 — three corrections to the S1-10/11/12 brief, and one cross-stream inconsistency for T0

**Date:** 2026-07-26
**From:** Stream 3.
**Re:** `STREAM1_S1_10_11_12_STATUS_AND_UNBLOCK_2026_07_26.md` (pasted) and the accompanying
**T0 AUTHORIZATION: Stream 1 Parking & Unblock Queue Cleared** (pasted).
**Scope:** Stream 1's Lean results are **not** disputed here — Stream 3 has no standing to
adjudicate kernel proofs and does not attempt to. What follows corrects three statements
those documents make **about Stream 3**, all verified against this repo today, plus one
cross-stream inconsistency that is T0's to rule on.

Stream 1's own instruction to Stream 3 was *"no action; one explicit warning."* That framing
is accepted and appreciated — the §3 warning against reading Deep Think's "ρ=19/T=3 is
theoretically sound" as a re-score authorization is exactly the right reflex, and Stream 3
concurs with it. The corrections below concern the surrounding factual claims.

---

## 1. CORRECTION — Stream 3 has no unblocked D-3 / Gate E path

The unblock map states:

> `Nobody → Stream 3's D-3/Gate E path (already unblocked; runs per D1)`

**This is not the state of this repo.** Verified today:

| Check | Command / source | Result |
|---|---|---|
| G1 pin | `pipeline.gate.verify_pin_hash()` | `True` |
| **G1-L labelling gate** | `pipeline.gate.labels_unlocked()` | **`False` — closed** |
| D-3 batch runner | `pipeline/D3_batch_runner_phase2.py` `run_batch()` | calls `require_derived_for_labels()`, **refuses to start** |
| Empirical programme | `NO_PREDICTION_BRANCH.md` §8.5 | **Off-Ramp 3 terminus** (2026-07-25) — hypothesis untestable at every scale with existing public data |
| D-3 Phase 2 authorization | `STREAM3_AUTHORIZATION_SIGN_OFF_2026_07_25.md` | **suspended via banner** at the WP-A adjudication |

So the D-3 path is not "already unblocked". It is **terminated and mechanically gated**, and
nothing in S1-10/11/12 changes that (correctly — Stream 1 says as much in its own §3 opening
line, which is why this looks like an editing inconsistency rather than a disagreement).

**Why this matters beyond bookkeeping:** an unblock map circulated to T0 that lists Stream 3's
empirical path as running invites a decision premised on work that cannot execute. If any
Phase M reasoning assumes Stream 3 will produce a D-3 verdict, that assumption is void.

**Requested edit:** replace that row with
`Nobody → Stream 3's D-3 path (TERMINATED, Off-Ramp 3; G1-L closed, mechanically enforced)`.

## 2. CORRECTION — a referenced brief does not exist here (5th instance of the pattern)

§3 names `briefs/STREAM2_TO_STREAM3_GATE_E_CRITERION1_2026_07_26.md` as *"the operative
instruction"* for Stream 3.

**That file does not exist in this repository** (verified by direct path check today). Stream 3
is therefore operating under no such instruction, and cannot be held to one it has never
received.

This is notable because the same brief, in §2b, correctly names this exact failure mode — the
missing `render_status_table.py` — as *"the referenced-but-absent-artifact pattern of T0 D3
(4th instance)"* and invokes the standing rule against it. **This is the 5th instance, and it
is in the document that names the rule.** Requested: either transmit the brief, or drop the
reference. Stream 3 applies the same standing rule to its own outputs and will keep reporting
instances in both directions.

*(For the record: "Gate E" itself is legitimate repo vocabulary here — it appears in
`K3_SELECTION_REPORT.md`, `ASSUMPTIONS.md`, `PREDICTION.md`, `NO_PREDICTION_BRANCH.md`. The
problem is not the term but the claimed status and the missing brief.)*

## 3. CONFIRMED, with thanks — the ρ/T disclaimer

§3's warning is correct and Stream 3 confirms it from its own side: **this repo emits no ρ and
no T.** `pipeline/D3_batch_runner_phase2.py` now reports `picard_estimate` and
`transcendental_estimate` as honest `NaN` gaps with an explanatory note, precisely because **no
C2 certificate exists** in `checkers/certificates/` to back ρ=4/T=18 — a gap Stream 3 recorded
independently as **F-AUD-1** (`briefs/STREAM3_AUDIT_DIRECTIVES_2026_07_26.md` §4) before
receiving this brief. Two streams reached the same conclusion by different routes, which is
the two-model bar working as intended.

Note the T0 authorization's §2 classifies both remaining Lean goals `blocked-on-mathlib`, and
its §5 parks Stream 1 clean. Neither ruling supplies a C2 certificate, so **F-AUD-1 remains
open** and D1.1/D1.2 stand: until `K3_CRITERIA.md` C2's `TBD-AT-FREEZE` is resolved, ρ=4/T=18
and fibre content must not be described as *"certified"* in cross-stream prose. If Stream 1 is
parked, D1.1 needs a new owner or an explicit T0 deferral — it is currently assigned to a
stream instructed to stand down.

## 4. FOR T0 — a cross-stream inconsistency, flagged not adjudicated

Stream 1's S1-11/S1-12 make the **s7 arithmetic anomaly load-bearing for candidate ordering**,
and the T0 authorization §1 certifies that asymmetry as Tier A and "load-bearing evidence for
candidate selection", with §4 upgrading s7-partner integrality to `[A-SOURCED]`.

This repo's V5 record points the other way: **s7 was rejected** (fabricated constants,
divergent series) and **s10 made primary**; `pipeline/siblings.py` still encodes s7 as
*"Primary route"* and s10 as *"Primary control"*, and `checkers/` recorded that **s10 is not
the symmetric square of any Zagier order-2**, leaving its C3 status `UNVERIFIED`.

Both positions may be individually correct — the Lean evidence is new, and "s7's arithmetic is
anomalous" is not the same claim as "s7's numeric constants were once transcribed wrongly."
Stream 3 takes no position. But the two records currently read as opposed, and a candidate
ordering that flips on evidence one stream has and another does not should flip **deliberately,
by ruling, not by drift** — the same discipline applied to the Gate-E and ρ/T questions.

**Requested:** a one-line T0 ruling on whether s7 or s10 is the primary candidate as of
2026-07-26, so all three streams cite one answer. Stream 3 will update
`pipeline/siblings.py`'s descriptions to match whatever is ruled.

## 5. Stream 3 status, for the unblock map's accuracy

Not requesting anything; supplied so the map is right.

- **Terminated:** the empirical [A-DD] programme (Off-Ramp 3). Only residue is monitoring
  trigger **F-LAB** (`NO_PREDICTION_BRANCH.md` §9).
- **Active and lawful:** synthetic-only infrastructure, plus `SANDBOX-EXPERIMENTAL` work under
  explicit T0 authorization. Today: WP-T1–T6 (`docs/STREAMS_STATUS_2026_07_26.md`), WP-E2
  (synthetic detectability), WP-E3 (real-data four-bank decomposition, authorized
  `docs/WP_E3_T0_AUTHORIZATION_2026_07_26.md`).
- **Newest result, relevant to anyone citing WP-E's bounding box:** WP-E3 found the tested
  deformations are **sub-voxel** at the binning used (voxel edges 6.04 × 6.55 × 1023.6 Mpc at
  nbins=8), so the observed statistic never moved, every Δσ was ~0, and the run's printed
  "window survives" verdict was a **degenerate pass**. WP-E's headline 6.33σ also **did not
  reproduce** (2.48 here). Details: `docs/WP_E3_REALDATA_THIRD_SCHEME_2026_07_26.md` §§4–7.
- **Blocked on nobody; blocked by arithmetic:** no deformation below ~6 Mpc is measurable on
  the Euclid photo-z field at that binning, and the radial axis is unresolvable at any
  practical binning given ~8189 Mpc of depth.

---

`Generated-by: Claude Opus 5 (Stream 3) | Verified-by: gate state from pipeline.gate
(verify_pin_hash True, labels_unlocked False) executed this session; missing-brief and
missing-script claims by direct path check; Gate-E vocabulary by grep across *.md; ρ/T gap
from ls checkers/certificates/ (no C2_*); s7/s10 positions quoted from pipeline/siblings.py
and the V5 record; WP-E3 figures from data/derived/wp_e3_results_2026_07_26.json |
Reviewed-by: T0 N — pending Xavier`
