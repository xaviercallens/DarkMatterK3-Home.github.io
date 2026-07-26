# T0-delegated rulings, 2026-07-26

**Authority:** Xavier (T0) delegated decision authority to Stream 3 in-session on 2026-07-26
to unblock the standing items. This document records each decision, the evidence it rests on,
and its scope. Every ruling here is **countermandable by T0 at any time**; none is a precedent
for future delegation.

**Scope limit, declared up front.** Delegated authority is used below only where the repo's own
measured state determines the answer. Where a decision would require evidence nobody currently
holds — a fetched paper, a certificate not yet computed, another stream's unverifiable
mathematics — the ruling is to *record the gap*, not to resolve it by fiat. One item (DR-1) is
declined outright on principle even though authority to decide it was granted; the reasoning is
given there.

---

## DR-1 — `PREDICTION.md` stays untouched. Variant (b). **A re-hash is declined.**

**Decision:** no edit to the pinned body. `verify_pin_hash()` remains `True`, G1 stays open.

**Evidence.** The ρ=4/T=18 claim sits at line 51. An in-band retraction already exists at
line 151, *inside the hashed body* and present at pin time:

> **Blocker before any lattice-dependent step:** correct C1/C2 recompute for the A279619
> partner (F6 — the previous ρ=4/T=18 is retracted).

A reader who reaches line 51 and tries to *use* ρ=4/T=18 for anything lattice-dependent meets
the retraction in the section that governs that use. The epistemic duty Ruling 1 targets is
therefore already discharged.

**Why the re-hash variant (a) is declined rather than merely not chosen.** `verify_pin_hash()`
computes SHA-256 over the entire document body, so *any* edit closes G1 and the pin must be
recomputed. Recomputing it converts a pre-registration into a re-registration. The entire value
of a pinned prediction is that it cannot be edited by whoever currently holds authority — which
means a grant of authority is precisely the circumstance in which it must not be exercised.
Delegated authority is sufficient to run experiments, quarantine code, and rule on scientific
disposition; it is not sufficient to rewrite the artifact those things are audited against.
**If T0 wants variant (a), it needs an explicit, personally-issued "re-hash authorized" — not a
delegation.** The marginal gain (one annotation at line 51 duplicating line 151) does not
approach the structural cost.

## DR-2 — E2.2 stands. The chameleon adjudication is not reopened.

**Decision:** any M1/M2 mechanism whose scale-setting routes through an Mpc-scale chameleon is
dead on arrival and must say so in its own §1. The project-health memo's Step 2 must be
rewritten around a mechanism that does not, or must open by recording that its scale-setting is
closed.

**Evidence.** The ~30 μm ceiling is adjudicated, two-model, CLOSED-NEGATIVE
(`NO_PREDICTION_BRANCH.md` §8.5); E2.2 is marked **Binding** in
`briefs/CROSS_STREAM_CONSOLIDATED_2026_07_26.md`. Nothing produced since — not WP-E5, not the
memo — is evidence bearing on the ceiling. **Reopening an adjudication requires new evidence,
not a new deadline.** The memo's arrival close to a planned M2 write-up is a scheduling fact,
not a physical one.

**What would reopen it:** the F-LAB monitoring trigger (`pipeline.gate.check_flab_trigger()`) on
future public ISL data excluding |α|=1 below 38.6 μm. That path is live and unchanged.

## DR-3 — Roadmap Step 1 (the (r_s, α) bounding box) is withdrawn.

**Decision:** Stream 3 will not deliver a bounding box, and Steps 2 and 3 may not be written as
gated on one. It is replaced by the **measurability envelope** already delivered.

**Evidence — measured, from three independent directions:**

| Phase | Result |
|---|---|
| 0 (real Euclid photo-z) | NO-GO at both Δz |
| 1 (inject a known signal, recover it) | FAIL — β₁ identical deformed vs undeformed |
| 2/3 (synthetic envelope) | two floors: ~1.6 Mpc scale, ~10⁴ objects/slice |

Plus the inferential objection, which stands independently of the arithmetic: `T(r_s, α)` is a
generic warp chosen independently of the K3 mathematics, so a region where it conflicts with
data constrains *that warp*, not any vacuum. That is the circularity that ended WP-A2.

**Replacement deliverable:** `docs/WP_E_EMPIRICAL_BOUNDS_2D_2026_07_26.md` and
`briefs/STREAM3_TO_STREAM2_EXPERIMENTAL_FINDINGS_2026_07_26.md` (E2.18–E2.23). Under E2.17 a
mechanism untestable with current data is a **complete** M1/M2 deliverable.

## DR-4 — s10 remains this repo's primary. s7 may not supply parameters. No position taken on Stream 1's mathematics.

**Decision, stated as three separate things so they are not conflated:**

1. **This repo continues with s10 as primary candidate.** Its kernel is certified and its
   recurrence verified (A005260, λ=16).
2. **s7 may not supply any numeric parameter to any code path here**, under P1 (no constant
   without provenance). `K3_CRITERIA.md:17` carries K-s7 as `TBD-AT-FREEZE` /
   `SYM2_UNVERIFIED` / `C3B_UNVERIFIED`, and this repo's V5 record has its guideline constants
   found fabricated.
3. **Stream 3 takes no position on whether s7 is the correct object for Stream 1's
   mathematics.** Nobody here has shown anything against it.

**Evidence.** `checkers/certificates/` holds C1 for s7 and s10 both, and C3/C3b for **delta,
alpha and eta only** — *neither* s7 nor s10 carries a C3/C3b certificate. So the honest position
is narrower than "s10 is verified": s10 is the primary because its kernel and recurrence are
certified, not because it has passed C3/C3b, which it has not.

**No code change follows.** `pipeline/siblings.py` carries s7 and s10 as a control pair, which
is P4-correct (sibling families as control) and does not constitute use of s7's parameters.
Verified this session.

**Unblocking action for Stream 1:** produce C1/C3/C3b certificates for s7. That is the only
thing that moves it from uncertified to usable here — an assertion that it is load-bearing does
not, and neither does this ruling.

## DR-5 — One ρ/T status line, for all three streams to cite

> **ρ ≤ 19, T ≥ 3 — Tier [B], pending Stienstra–Beukers 1985. No prior is emitted. No code
> path may consume a numeric ρ or T.**

**Evidence.** This matches T0's own Ruling 2/3 as implemented
(`docs/WP_E5_T0_RULING_IMPLEMENTATION_2026_07_26.md` §2) and the repo's behaviour: `grep` across
`pipeline/` and `checkers/` returns no emitted ρ or T value, and `D3_batch_runner_phase2`
reports both as honest `NaN`. It supersedes the memo's "DERIVED [B], independently reproduced"
and is consistent with Stream 1's UNRESOLVED warning — those two were the contradiction.

**Not resolved, and deliberately so:** whether S-B 1985 actually supports ρ ≤ 19. That requires
fetching the paper. Delegated authority cannot substitute for a citation, so the `[B]-pending`
status stays until someone reads it.

## DR-6 — D1.1 (C2 `TBD-AT-FREEZE`) is explicitly **deferred**, not assigned

**Decision:** recorded as deferred with no owner, and removed from the blocking list.

**Evidence.** C2 blocks ρ/T/fibre certificates. Nothing on the current critical path consumes
them: the empirical program is closed at Off-Ramp 3, `run_batch()` is gated, and ρ/T are emitted
as `NaN` by ruling DR-5. Assigning an owner inside a parked stream would be a fiction that reads
as progress. **Revisit when, and only when, a certificate becomes load-bearing for something
live.**

---

## Net effect on the blocking list

| Item | Before | After |
|---|---|---|
| Ruling 1 variant | blocked on T0 | **closed** — (b), re-hash declined (DR-1) |
| E2.2 vs memo Step 2 | blocked on T0 | **closed** — E2.2 stands (DR-2) |
| Roadmap Step 1 | blocked on T0 | **closed** — withdrawn (DR-3) |
| s7 vs s10 | blocked on T0 | **closed here**, action passed to Stream 1 (DR-4) |
| ρ/T status | three versions in circulation | **closed** — one line (DR-5) |
| D1.1 owner | blocked on T0 | **closed** — deferred (DR-6) |

Nothing in this document unlocks G1-L, alters `PREDICTION.md`, reopens Off-Ramp 3, or licenses
a `TEST`/`FIT` label. Those remain where they were, and DR-1 explains why the first of them is
the one that delegation specifically must not touch.

---

`Generated-by: Claude Opus 5 (Stream 3, under T0-delegated authority 2026-07-26) |
Verified-by: DR-1 against PREDICTION.md lines 51 and 149-151 read this session and
pipeline.gate.verify_pin_hash() (True); DR-2 against CROSS_STREAM_CONSOLIDATED_2026_07_26.md
and NO_PREDICTION_BRANCH.md §8.5; DR-3 against the three persisted phase artifacts under
data/derived/; DR-4 against ls checkers/certificates/, K3_CRITERIA.md:17 and
pipeline/siblings.py:80-91; DR-5 against grep over pipeline/ and checkers/ (no rho/T emitted) |
Reviewed-by: T0 — authority delegated, countermand window open on all six`
