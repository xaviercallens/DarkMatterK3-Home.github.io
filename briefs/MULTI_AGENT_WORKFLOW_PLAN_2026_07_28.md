# Multi-Agent Workflow Plan — Stream 2 (G1 Route A) & Stream 3 (WP-E6 Phase 2 / WP-E7)

**Status: DESIGN ONLY — NOT IMPLEMENTED.** Per T0 directive 2026-07-28
(`T0_DECISIONS_2026_07_28_PENDING_ITEMS.md`, final authorization): this document defines
the workflow, tier assignments, definitions of done, and validation gates. No agent is
launched, no code is written, and no task list is created by this document. Implementation
begins only when T0 (or the coordinator under the standing autonomy mandate, if T0 defers)
green-lights a specific work package below.

---

## 1. Model-tier ladder (who does what)

| Tier | Model | Role | May | May NOT |
|---|---|---|---|---|
| **T-grind** | Haiku 4.5 | Mechanical execution | Run existing scripts/checkers, timing benchmarks, golden/control tests, report numbers verbatim, file mechanical logs | Write new mathematics, interpret results, edit prose carrying tier labels, decide PASS/FAIL beyond a pre-stated mechanical criterion |
| **T-work** | Sonnet 5 | Derivation & implementation | New derivations/code inside a scoped WP, self-checks, draft briefs (DRAFT-labeled) | Promote its own output, close a gate, amend a pin/grid, touch another WP's files |
| **T-verify** | Fable 5 / Opus | Verification gates & coordination | Independent re-derivation, adversarial review, DRAFT→coordinator-verified promotion recommendation, T0 briefs | Self-promote past T0-reserved gates (G1→G2 opening, pin amendments, paper submission) |
| **T0** | Xavier | Authority | Everything | — |

**Standing rules (all tiers):**
1. **Three-strikes escalation** (from the S1 tactic-ladder precedent): a lower tier that
   fails the same subtask 3 times escalates up one tier with a written stuck-report; it does
   not grind past 3.
2. **Verification is never done by the producing tier.** Whoever wrote it, a different
   agent (≥ same tier, fresh context, no reading the original implementation first for
   from-scratch re-derivations) validates it.
3. **Epistemic guardrails skill loads before any prose** in either repo; tier checker must
   be clean before commit (S3: `scripts/check_tier_language.py`).
4. **Every agent output is DRAFT until the validation column below says otherwise.**
5. Environment invariants: venv `~/venv` only; **no mpi4py ever**; `phase1_work/` stays
   gitignored — new original code lands in tracked `pipeline/`; S2 sessions check
   `git status -sb` first (other tools work concurrent branches in that checkout).

---

## 2. Stream 2 — WP S2-G Phase G1 (Route A, opened `256017d`)

Reference plan: `briefs/WP_S2G_X4_EXHIBITION_PLAN_2026_07_27.md` (S2, canonical).
All work exact-symbolic (sympy integer/rational); ML quarantined per T0 directive.

### WP G1-a — CY condition over the B₂ ladder
- **Tier:** T-work (Sonnet) derivation; T-grind (Haiku) reruns the resulting checker over
  the full ladder (P², P¹×P¹, F_n for the n-range the derivation certifies).
- **Task:** for each base, construct the pullback family and derive the CY (c₁ = 0 / twist)
  condition exactly; emit a per-base certificate JSON + checker script under `checkers/`.
- **DoD:** checker runs green for ≥1 base; every certificate field traces to a derivation
  step in the accompanying brief; ≥2 negative controls (a base/twist that must FAIL, and a
  deliberately corrupted input) fail as predicted; no floats in lattice/divisor arithmetic.
- **Validation:** T-verify re-derives the CY condition for ONE base from scratch (fresh
  session, no reading the implementation) and matches the certificate bit-for-bit —
  the U1/G0 precedent standard. Mismatch ⇒ both derivations quarantined, escalate T0.

### WP G1-b — Crepant resolution analysis (the plan's main risk)
- **Tier:** T-work attempts; **T-verify mandatory** before any status is recorded (this is
  the phase the plan itself flags as most likely to fail honestly).
- **Task:** classify the singularities of each pulled-back family; determine crepant
  resolvability exactly; if obstructed, record the obstruction as a first-class result.
- **DoD:** per-base disposition {resolvable + exhibited resolution data | obstructed +
  exact obstruction | undetermined + precise blocker}, each with a certificate or a
  written blocker note. "Undetermined" is an allowed, honest terminal state.
- **Validation:** T-verify checks the singularity classification independently for every
  base ruled "resolvable"; spot-checks one "obstructed". A FAIL here fires the plan's
  stop-condition → T0 (Route B decision), not a workaround.

### WP G1-c — F-theory posability certificate
- **Tier:** T-work; entry **blocked until G1-a and G1-b both validated** for at least one base.
- **Task:** for surviving bases, certify the relative elliptic structure (the G0 caveat #2:
  monodromy-invariant isotropic NS class — reuse `check_U1_lattice.py` stage2/3 monodromy
  generators, previously unused for this).
- **DoD:** posability certificate (not a tadpole *solution* — G2 scope) for ≥1 base, with
  the fiberwise-vs-relative distinction stated in the certificate itself.
- **Validation:** T-verify audits that no Tier-C leakage occurred (no observables, no
  free-exponent bridges — Deep Think ruling stands); coordinator brief → T0 for the G1→G2
  gate, which **only T0 opens**.

## 3. Stream 3 — WP-E6 Phase 2 (protocol LIVE `7d0b2ce`) & WP-E7

Reference: `ANALYSIS_PROTOCOL` (ratified) + `T0_DECISIONS_2026_07_28_STREAM3.md`.
All outputs CONTROL/synthetic-labeled; real-data comparison stays behind the PREDICTION v2
pin (CLAUDE.md rule 1) — nothing below changes that.

### WP P2-t — desisim timing benchmark (N=50)
- **Tier:** T-grind (Haiku) — purely mechanical.
- **Task:** run desisim mock generation N=50 at the protocol's spec; record wall-clock,
  peak RSS, per-mock marginal cost into a timing JSON in `data/derived/`.
- **DoD:** timing report with machine specs + exact command line; extrapolated N=200 cost.
- **Validation:** T-verify sanity-checks the extrapolation (linear-scaling assumption
  stated, not assumed silently) and rules GO/NO-GO on N=200 against the session budget;
  NO-GO ⇒ T0 chooses reduced-N (with recomputed Hartlap factor) — agent may not.

### WP P2-A — covariance builder (16×16 Hartlap)
- **Tier:** T-work implements; T-grind runs the ensemble once P2-t rules GO.
- **DoD:** covariance module + tests: symmetric PD matrix, Hartlap factor applied and
  logged, N recorded in-file; a fixed-seed regression test; mocks confirmed independent
  draws (protocol Part A finding) cited in the module docstring.
- **Validation:** T-verify checks PD-ness, the Hartlap arithmetic against the formula, and
  that the 16 k-bins match `emu_predict.py`'s `K_BINS` exactly (the protocol's own
  corrected count — do not re-introduce 10).

### WP P2-C — masking fix (Bug 1 + Bug 2, Ravoux-style correction)
- **Tier:** T-work; **the Ravoux et al. 2023 recipe must be verified against the actual
  paper (arXiv:2306.06311) before coding** — the protocol flags that its summary came from
  a search result, not a verbatim read. That read is a T-work prerequisite subtask.
- **DoD:** `compare_p1d.py` fixed (zero-fill edge artifact + biased mean); multiplicative
  window correction implemented mock-calibrated, **no interpolation across gaps** (T0
  directive); before/after demonstrated on synthetic spectra with known truth.
- **Validation:** T-grind reruns the Phase-1 masking experiment — the +7% naive-masking
  artifact must be gone/attributable; T-verify reviews the diff against the paper's
  equations and confirms taueff bounds are documented as **prior-box** everywhere they
  appear (T0 resolution, non-negotiable wording).

### WP P2-B — nuisance profiling
- **Tier:** T-work; entry blocked until P2-A validated (needs the covariance).
- **DoD:** profiling module extending `integration_iminuit.py` to the Part A covariance
  (single z=4.2 term, 12 dof/cell per protocol); convergence + boundary-hit diagnostics
  logged per cell; taueff documented as prior-box in every artifact.
- **Validation:** T-verify runs a fixed-cell spot check reproducing the profiled minimum
  independently; grid-controls suite reruns green (the f=0 / null-row invariants must
  survive profiling untouched).

### WP E7-o — occupancy ratification on LRGpCMASS
- **Tier:** T-grind (counts, footprints, z-histograms vs published values) + T-verify writes
  the occupancy brief.
- **DoD:** occupancy report on the fetched primary sample; row counts MATCH the published
  377,458; eBOSS-only files present as labeled secondary.
- **Validation:** numbers cross-checked against Ross et al. 2020 and the MANIFEST integrity
  block; brief → T0.

## 4. Coordination protocol

- **One WP = one agent = one scoped prompt** naming: inputs (exact files), the DoD above,
  the tier rules, and the stop conditions. No agent receives two WPs.
- **Dependencies:** G1-c ⇐ (G1-a ∧ G1-b); P2-A ⇐ P2-t GO; P2-B ⇐ P2-A. G1-a ∥ G1-b may
  run in parallel; S2 and S3 tracks are fully parallel (different repos, no shared files).
- **Commits:** per-WP milestone commits by the coordinator (not by sub-agents), conventional
  messages, canonical-repo rule (S2 results canonical in S2, mirrored briefs elsewhere).
- **Reporting:** each WP ends with a DRAFT brief + certificate; coordinator batches
  T0-only items (gate openings, pin changes, NO-GO choices) into a single decision request.
- **Kill criteria:** any tier-language CI failure, any control-test regression, or any
  attempt to touch `data/raw/`, the pinned grid, or PREDICTION.md ⇒ hard stop + report.

---
Generated-by: Fable 5 (coordinator) | Verified-by: WP definitions checked against
WP_S2G_X4_EXHIBITION_PLAN_2026_07_27.md, ANALYSIS_PROTOCOL draft + T0 decision records,
G0 result brief caveats, grid-controls report this session | Reviewed-by: T0 N (submitted for review; design only, nothing executes until approved)
