# EXECUTION_PLAN — Model-Orchestrated Action Plan for the Three Streams

**Status:** v1.0 (July 2026) — companion to `VISION.md` v1.2  
**Mirrored in all three repos.** Canonical copy: LeanProposal repo.

This document turns `VISION.md` into executable work packages, each with **instructions, an assigned model tier, a Definition of Done (DoD), and a validation gate**. It also fixes the epistemic regressions introduced in VISION v1.1 (see §0).

---

## 0. Amendments to VISION v1.1 (apply before execution)

| ID | Problem in v1.1 | Required fix |
|---|---|---|
| A1 | §1 states "Shioda-Inose constraint **rigidly locks** bulk to brane EFT" and "**predicting** specific scalar-mediated self-interactions" as consequences. These are Tier C claims in Tier A language — a direct violation of §2. | Rewrite §1: every physical-coupling clause carries an explicit "we conjecture / would imply if the matching exists" marker. The Sym² arithmetic implies a *geometric relation between families*; it implies **nothing physical** until an explicit EFT matching is exhibited. |
| A2 | "$L_3 = \mathrm{Sym}^2 L_2$" asserted as blanket arithmetic fact. | Demote to a **per-candidate checkable criterion** in `K3_CRITERIA.md` (criterion C3 below). Verified symbolically per candidate; unverified candidates carry the flag `SYM2_UNVERIFIED`. |
| A3 | "D7-branes wrapping elliptic curves manifest as dark matter halos" asserted as architecture. | Mark as the **Phase 1 blocker**: `PREDICTION.md` must contain at least one worked 4D EFT matching (fields, masses, couplings from geometric data) or the F5 branch triggers. |

---

## 1. Model Roster and Routing Rules

### 1.1 Roster

| Tier | Models (as available to the project) | Cost profile | Allowed work |
|---|---|---|---|
| **T0 — Orchestrator / Architect / Reviewer** | Claude Fable 5 | Scarce, rationed | Architecture, epistemic-tier rulings, cross-stream review, final sign-off, decomposition of complex tasks into T1/T2 packages |
| **T0s — Scientific Companion** | Google Deep Think | Scarce, rationed | Deep derivations, adversarial physics review, independent re-derivation of any T0 result (two-model cross-check) |
| **T1 — Capable worker** | Claude Sonnet, Gemini Pro | Moderate | Nontrivial code, Lean proof attempts on stated lemmas, literature triage, report drafting from provided facts |
| **T2 — High-volume worker** | Claude Haiku, Gemini Flash (effectively unlimited) | Cheap/unlimited | Bulk Lean proof search, test writing, data plumbing, formatting, doc mirroring, log summarization, CI glue |

### 1.2 Routing rules (non-negotiable)

1. **Verifier-first principle.** A task may be routed to T1/T2 **only if an objective, automated verifier exists** for its output: the Lean kernel, a pytest suite with golden data, a schema validator, or an exact symbolic check. If the only "verifier" is another LLM's opinion, the task is T0-only.
2. **No physics derivations below T0/T0s.** Deriving EFT predictions, interpreting data comparisons, or assigning epistemic tiers is never delegated to T1/T2. T1/T2 may *transcribe, code, or format* such results after T0 produces them.
3. **Two-model rule for Tier C physics.** Any physical derivation entering `PREDICTION.md` must be produced by one of {Fable 5, Deep Think} and independently re-derived (not reviewed — re-derived from the same inputs, blind) by the other. Disagreement blocks the deliverable and is logged in `DERIVATION_DISPUTES.md`.
4. **LLM output is never evidence.** No claim enters any report because "the model said so." Every claim must trace to (a) a kernel-checked proof, (b) a passing pre-registered test against public data, or (c) a citation to literature verified by a human or by fetching the actual source.
5. **Escalation path:** T2 → (3 failed attempts or verifier-uncheckable) → T1 → (2 failed attempts or design ambiguity) → T0. De-escalation is encouraged: T0 decomposes, then hands lemma lists / test-driven specs back down.
6. **Provenance logging.** Every artifact commits with a footer: `Generated-by: <tier/model> | Verified-by: <verifier> | Reviewed-by: <T0 pass? Y/N>`.

---

## 2. Stream 1 — Theory (Lean 4) — Detailed Work Packages

**Master verifier: the Lean kernel.** This is the stream where cheap models shine: Haiku/Flash can propose proofs at high volume because `lake build` with zero `sorry` is an objective, unfakeable gate.

| WP | Task | Instructions | Model | Definition of Done | Validation |
|---|---|---|---|---|---|
| S1-01 | Repo scaffold + CI | Set up Lake project pinned to a fixed Mathlib commit; CI job that fails on any `sorry`, `admit`, or new `axiom` outside `Axioms/` | T2 | CI green on empty skeleton; `AXIOMS.md` lists the (empty) axiom budget | CI run itself |
| S1-02 | Encode Cooper recurrences | Define s7/s10/S22/t103 recurrences and their Picard-Fuchs operators as Lean data (holonomic: `LinearRecurrence` over ℤ) with literature citation per definition in docstring | T1 drafts, T2 iterates | Definitions compile; each carries a `-- Source:` citation; 20 terms of each sequence match published values via `decide`/`native_decide` test file | Kernel + numeric golden test |
| S1-03 | Integrality lemmas | Prove the sequences are integral / satisfy stated congruences, starting from small verified cases | T2 bulk proof search; T1 on stuck lemmas | Zero `sorry` for the stated lemma list | Kernel |
| S1-04 | Sym² structure, per candidate | For each candidate: state `L3_candidate = symSquare L2_candidate` as a Lean proposition; prove where feasible, else isolate as a named open goal | T1; T0 designs the `symSquare` API first | For each candidate: either a kernel-checked proof or an explicitly named `open_goal_sym2_<name>` — no silent assumptions | Kernel; open-goal list auto-exported to `K3_CRITERIA` status table |
| S1-05 | Bridge-conjecture statements | Formalize the *statements* (not proofs) linking arithmetic to K3 geometry, with geometry axiomatized in a quarantined `Axioms/Geometry.lean` | T0 writes statements; T2 mechanizes | Statements compile; every axiom listed in `AXIOMS.md` with justification; README warns these are assumptions | Kernel + T0 review of axiom honesty |
| S1-06 | Mathlib community check | Post the Sym²/holonomic development on Lean Zulip for review; open a Mathlib PR for any generic component | Human (Xavier) with T1 drafting the post | At least one substantive external response addressed | External human review |

**Stream 1 exit criterion (feeds M2):** S1-02..S1-04 kernel-green; open-goal list published; S1-06 initiated.

---

## 3. Stream 2 — K3 Selection (AutoEvolve) — Detailed Work Packages

**Master verifiers: frozen `K3_CRITERIA.md` + symbolic computation (Sage/Pari/sympy) + golden tests.**

| WP | Task | Instructions | Model | Definition of Done | Validation |
|---|---|---|---|---|---|
| S2-01 | Freeze `K3_CRITERIA.md` | Enumerate exact, checkable criteria: C1 mirror-map integrality (N terms), C2 Kodaira fiber content, C3 Sym² relation (from S1-04), C4 Picard-rank bounds, C5 Swampland checks *with the precise inequality stated*. Each criterion: definition, checking procedure, pass/fail threshold | **T0 + T0s jointly** (this is the scientific interface — never delegated) | Document frozen, versioned v1.0, hash-pinned in all three repos | Two-model rule (§1.2.3); Xavier sign-off |
| S2-02 | Symbolic checkers | One script per criterion (`check_C1.py` …) computing the criterion from first principles with Sage/sympy — **not** from an LLM's recollection of values | T1 writes; T2 writes tests | Each checker reproduces a known-good and a known-bad control case (golden tests); deterministic, seeded | pytest golden suite in CI |
| S2-03 | AutoEvolve harness | AutoEvolve searches/scores candidates strictly by calling S2-02 checkers; scoring weights are read from frozen criteria file; all runs logged with config hash | T1 | Harness produces a reproducible ranking from a fixed seed; re-run reproduces bit-identical scores | Reproducibility CI job |
| S2-04 | Run + `K3_SELECTION_REPORT.md` | Execute ranking on s7/s10/S22/t103; report per-candidate criterion table (pass/fail/`SYM2_UNVERIFIED`), scores, and F1-branch removals | T2 runs; T1 drafts report from machine-generated tables only | Report tables are auto-generated from checker output (no hand-entered numbers); every failure triggers the F1 log entry | Table-generation script diff = 0; T0 review of prose |
| S2-05 | Adversarial review | Deep Think attempts to break the ranking: propose a criterion the winner should fail, or an excluded consistency condition | T0s | Written adversarial memo; each objection either refuted with a checker or adopted as a criteria amendment (versioned) | T0 adjudicates; amendments logged |

**Stream 2 exit criterion:** ranked report with fully machine-generated evidence tables; adversarial memo resolved.

---

## 4. Stream 3 — Experimentation — Detailed Work Packages

**Master verifiers: pre-registered `PREDICTION.md` + public datasets + golden pipelines.**

| WP | Task | Instructions | Model | Definition of Done | Validation |
|---|---|---|---|---|---|
| S3-00 | **`PREDICTION.md` (gate)** | Produce ≥1 quantitative prediction with error budget: e.g. SIDM cross-section vs velocity curve from the claimed EFT matching, or nHz spectral index+amplitude. Must include the derivation chain from geometric data to observable, and the A3 worked matching | **T0 derives, T0s blind re-derives** | Both derivations agree within stated tolerance; numbers + uncertainties committed and hash-pinned **before any data contact** | Two-model rule; commit timestamp precedes any data-touching commit |
| S3-01 | Data acquisition | Scripted, checksummed download of NANOGrav 15-yr free-spectrum posteriors, EPTA DR2, published lensing stacked-profile tables, Lyman-α constraint tables; document versions | T2 | `data/MANIFEST.md` with URLs, versions, SHA256; fetch script idempotent | Checksum CI |
| S3-02 | V5 pipeline core | Pipeline reads frozen `PREDICTION.md` parameters (no free knobs); computes model observable; compares to data; outputs pass/fail + likelihood/exclusion level; labels every comparison `TEST` or `FIT` per VISION §5 | T1 architecture per T0 spec; T2 implements modules | Full run on synthetic data recovers injected signal (closure test); on null synthetic data reports null (no false positive at stated α) | Closure + null golden tests in CI |
| S3-03 | PTA comparison | Compare predicted spectrum against public posteriors (free-spectrum violin data); report Bayes factor or exclusion σ; explicitly *comparison against published products* — no claim of collaboration | T2 runs; T1 drafts | Result reproduces from clean checkout in one command | Reproducibility CI; T0 reviews interpretation wording |
| S3-04 | Lensing comparison | Same pattern for halo-profile prediction vs published stacked profiles (dwarf regime) | T2 runs; T1 drafts | Same | Same |
| S3-05 | `OBSERVATIONAL_REPORT.md` | Machine-generated results tables + T0-written interpretation; every claim carries TEST/FIT label; F3/F4/F5 branches triggered mechanically from thresholds, not judgment | T1 assembles; **T0 writes interpretation section only** | Report published even (especially) if all results are exclusions | T0s adversarial pass; Xavier sign-off |

**Stream 3 exit criterion:** report with pre-registration audit trail intact (prediction hash predates data contact in git history).

---

## 5. T0 Orchestration Layer — Fable 5 + Deep Think

Reserved for work where no automated verifier exists and judgment is the product. Rationed; every T0/T0s session has a written brief and a written output artifact.

### 5.1 Fable 5 — Orchestrator / Architect / Reviewer

| Duty | Cadence | Output artifact |
|---|---|---|
| Decompose each WP into T1/T2 briefs (lemma lists, test-driven specs, acceptance criteria) | Per WP kickoff | `briefs/<WP>.md` |
| Epistemic-tier ruling on any new claim (A/B/C assignment) | On demand | Entry in `TIER_LEDGER.md` |
| Cross-stream consistency review (does Stream 3's implemented observable match Stream 1's formalized object and Stream 2's selected candidate?) | End of each Phase | `CROSS_STREAM_REVIEW_<phase>.md` |
| Final review of every report before publication: checks that prose claims ≤ what the machine-generated evidence supports | Per report | Signed review block in the report |
| Escalation triage from T1 | Weekly batch | Updated briefs |

### 5.2 Deep Think — Scientific Companion (adversary by design)

| Duty | Cadence | Output artifact |
|---|---|---|
| Blind re-derivation of every `PREDICTION.md` result (§1.2.3) | Per prediction | Independent derivation note; diff report |
| Adversarial memos: strongest known counter-argument, missing consistency condition, or literature result that already excludes the parameter region | Per Phase | `adversarial/<phase>.md` — every point must be answered in writing |
| Literature deep-dives on specific technical questions (with sources fetched and verified, never from memory) | On demand | Annotated bibliography entries |

### 5.3 Complex-task register (T0-only, standing list)

1. The A3 worked EFT matching (geometric data → 4D fields/couplings) — the single hardest task in the program.
2. Design of the `symSquare` Lean API (S1-04) and the axiomatization boundary (S1-05).
3. `K3_CRITERIA.md` content and any amendment (S2-01, S2-05 adjudication).
4. All interpretation prose in `OBSERVATIONAL_REPORT.md` and the manuscript.
5. Any decision to trigger or decline a falsification branch F1–F6.

---

## 6. Anti-Hallucination Protocol for LLM-Generated Science

1. **No numeric constant, published value, or literature claim enters any artifact from model memory.** It must be computed by a checker script or cited with the fetched source attached in `refs/`.
2. **Machine-generated tables only** in evidence sections; prose may interpret but never introduce numbers absent from the tables.
3. **Blind re-derivation, not review**, for Tier C physics: the second model receives inputs only, never the first model's answer.
4. **Failure symmetry:** T1/T2 failure statistics per WP are logged; a WP whose outputs repeatedly fail verification gets redesigned by T0 rather than retried indefinitely.
5. **Human final authority:** Xavier signs every phase gate. Models — including T0 — recommend; they do not decide.

---

## 7. Phase Gates (unchanged from VISION §6, with model routing overlaid)

| Gate | Contents | Blocking checks |
|---|---|---|
| **G0** (wk 2) | VISION v1.2 (with §0 amendments), `K3_CRITERIA.md` frozen, S1-01 CI green | A1–A3 applied; criteria two-model-signed |
| **G1 = M1** (mo 2) | `PREDICTION.md` hash-pinned | Two-model agreement; timestamp audit |
| **G2 = M2** (mo 8) | Stream 1 kernel-green core + Stream 2 report; arXiv math preprint draft | Open-goal list honest; adversarial memo resolved |
| **G3 = M3** (mo 14) | `OBSERVATIONAL_REPORT.md` | Pre-registration audit; branch triggers mechanical |
| **G4** (mo 18) | Manuscript(s), venue by result strength | T0 claim-vs-evidence review; Xavier sign-off |

---

## 8. Changelog

- **v1.0 (2026-07-17):** Initial execution plan. Adds model-tier routing (T0 Fable 5 / T0s Deep Think / T1 Sonnet–Gemini Pro / T2 Haiku–Flash), verifier-first delegation rule, two-model blind re-derivation rule for physics, per-WP DoD and validation gates, and amendments A1–A3 correcting VISION v1.1 epistemic regressions.

---

## Related Documents

- **VISION.md** — Master vision (epistemic framework, falsification branches, phase roadmap)
- **K3_CRITERIA.md** — Frozen criteria for K3 ranking (feeds S2-01)
- **PREDICTION.md** — Falsifiable predictions (gates S3-00, feeds Phase gates)
- **BRIEFS/** — Per-WP execution instructions (generated by T0 per §5.1)
- **ADVERSARIAL/** — Deep Think adversarial memos (per §5.2)
- **TIER_LEDGER.md** — Epistemic rulings (per §5.1)
