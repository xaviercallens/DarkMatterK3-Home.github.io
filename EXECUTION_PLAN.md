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

## 2.1 Phase 0 — Foundational Assumptions & Epistemic Framework (NEW)

*Prerequisite work for S2-01 and S3-00 freezes. Must complete before G0 gate.*

| WP | Task | Instructions | Model | Definition of Done | Validation |
|---|---|---|---|---|---|
| P0-A | Formalize `ASSUMPTIONS.md` | Transcribe Phase 0 ASSUMPTIONS (v0.2) into repo artifact with frontmatter: A-SEQ, A-VOL, A-ONT, A-REL. Each assumption carries tier, discharge path, failure mode. Every assumption ID is grep-able; CI enforces consistency with K3_CRITERIA and PREDICTION.md tags. | T1 under T0 brief | `ASSUMPTIONS.md` exists; all four assumptions (A-SEQ, A-VOL, A-ONT, A-REL) carry explicit tier and per-assumption checker contract. VISION.md §2 validates all Tier C tiering. | grep audit in CI; T0 review against Phase 0 doc |
| P0-B | Design Free-Parameter Ledger schema | Establish the 7-row table (GEOMETRIC / CONTINUOUS-FREE / DISCRETE / ASSUMED classification) as a Jinja template for `PREDICTION.md`. Each row carries: quantity name, class, status in MVM, dependencies (which assumptions). Extend K3_CRITERIA.md §C4 to reference the ledger schema. | T1 drafts; T0 reviews | Template file `templates/free_parameter_ledger.jinja`; PREDICTION.md ready to receive filled-in instance | Schema + one golden example |
| P0-C | Update epistemic-guardrails skill | Add new standing rule (Finding F-A): abstracts and summaries are reviewed against the tier ledger line-by-line; a claim may not appear in an abstract at a stronger tier than in its section. CI rule: grep for words like "Rigidly locks", "Rigidity Theorem", "zero continuous" in abstract blocks; flag any claim without an explicit tier marker. | T1 under T0 direction | Skill file updated; CI rule added and tested on a control example | Rule + CI test pass |
| P0-D | Create `TUNING_LOG.md` skeleton | Establish the log file for tracking assumption-list changes after phase pin (VISION §5 "tuning event"). Structure: date, commit, quantity, old assumption list, new assumption list, justification. CI checks that every new commit touching PREDICTION.md assumptions is logged here. | T2 | Empty but initialized file; CI rule that every PREDiCTION.md assumption-tag change requires a TUNING_LOG entry | File exists + CI test |

**Phase 0 exit:** ASSUMPTIONS.md complete + signed, Free-Parameter Ledger schema live, epistemic-guardrails F-A rule in all three repos, TUNING_LOG.md initialized.

---

## 3. Stream 2 — K3 Selection (AutoEvolve) — Detailed Work Packages

**Master verifiers: frozen `K3_CRITERIA.md` + symbolic computation (Sage/Pari/sympy) + golden tests.**

| WP | Task | Instructions | Model | Definition of Done | Validation |
|---|---|---|---|---|---|
| S2-01 | Freeze `K3_CRITERIA.md` v1.0 | Enumerate exact, checkable criteria: C1 mirror-map integrality (N terms), C2 Kodaira fiber content, **C3 Sym² relation (from S1-04), C3b Shioda-Inose moduli map F (new**, per T0 Architecture Review), C4 Picard-rank bounds, C5 Swampland checks *with the precise inequality stated*. Each criterion: definition (with assumption tags if Tier C), checking procedure, pass/fail threshold, and failure consequence. **Integrate ASSUMPTIONS.md references: C2 depends on A-ONT; C3b depends on A-SEQ, A-VOL.** | **T0 + T0s jointly** | Document frozen, versioned v1.0, hash-pinned in all three repos; every C criterion carries explicit assumption list and discharge path | Two-model rule (§1.2.3) + Xavier sign-off; P0-A complete |
| S2-01b | Define `check_C3b_moduli_map.py` | Per-candidate symbolic check: given the order-3 and order-2 PF operators (hauptmoduls from literature), construct the Shioda-Inose correspondence and compute F as an explicit algebraic/q-series relation. Verification: expand both sides to order N symbolically and confirm equality. Output: the map F (as polynomial/q-expansion), margin of agreement, certificate JSON. | T1 under T0 spec | Checker `checkers/check_C3b_moduli_map.py` passes golden tests (known-good pair with explicit F; known-bad pair with no F) | pytest CI + manual verification on control |
| S2-02 | Symbolic checkers | One script per criterion (`check_C1.py` … `check_C5.py`, plus `check_C3b_moduli_map.py` from S2-01b) computing each from first principles with Sage/sympy — **not** from LLM recall | T1 writes; T2 writes tests | Each checker reproduces a known-good and known-bad control case (golden tests); deterministic, seeded; includes assumption dependency check (each result carries its assumption list). | pytest golden suite in CI; assumption-list audit |
| S2-03 | AutoEvolve harness | AutoEvolve searches/scores candidates strictly by calling S2-02 checkers; scoring weights are read from frozen criteria file; all runs logged with config hash; **C3b pass is a hard gate** (candidate fails C3b ⇒ F1 removal, no score computed) | T1 | Harness produces a reproducible ranking from a fixed seed; re-run reproduces bit-identical scores; C3b failures trigger F1 log | Reproducibility CI job; C3b gate test |
| S2-04 | Run + `K3_SELECTION_REPORT.md` | Execute ranking on s7/s10/S22/t103; report per-candidate criterion table (pass/fail/C3b-grade), scores, and F1-branch removals. **Tag each observable quantity with its assumption list** (e.g., `m_φ [A-SEQ, A-VOL, A-ONT]`). | T2 runs; T1 drafts report from machine-generated tables only | Report tables are auto-generated from checker output (no hand-entered numbers); every failure triggers F1 log entry; all tagged with assumption lists | Table-generation script diff = 0; T0 review of prose + assumption tags |
| S2-05 | Adversarial review | Deep Think attempts to break the ranking: (1) propose a criterion the winner should fail; (2) specifically attempt to break A-SEQ (find the light field we forgot) and verify assumption-driven gate logic. | T0s | Written adversarial memo; each objection either refuted with a checker or adopted as a criteria amendment (versioned). Separate section: A-SEQ adversarial pass. | T0 adjudicates; amendments logged |

**Stream 2 exit criterion (feeds G1/M1):** ranked report with fully machine-generated evidence tables + assumption tags; C3b checker validated; adversarial memo resolved; identified **top C3b-passing candidate pair** for MVM matching (§3.00 input).

---

## 4. Stream 3 — Experimentation (MVM + Observables) — Detailed Work Packages

**Master verifiers: pre-registered `PREDICTION.md` + public datasets + golden pipelines. Critical: MVM calculation gates all downstream work (GATE M1).**

| WP | Task | Instructions | Model | Definition of Done | Validation |
|---|---|---|---|---|---|
| S3-00 | **`PREDICTION.md` — MVM Matching** | **Gate: the single hardest task in the program.** (1) Install Free-Parameter Ledger template (P0-B): 7-row table classifying all EFT degrees of freedom under A-SEQ/A-VOL/A-ONT/A-REL assumptions. (2) For the top C3b-passing candidate pair from S2-04, derive in order: (a) m_φ(𝒱, g_s) from period geometry at the C3b-selected vacuum point; (b) α_D, Λ_D(𝒱, g_s) from Kodaira fiber data (C2 output) and gauge kinetics RG running; (c) eliminate (𝒱, g_s) between observables to produce a **relation, not a number**. (3) Pinned observable (choose first available): **P1 (PTA):** if m_φ ∈ 10⁻²³–10⁻²² eV, ultralight modulus induces nHz-band pulsar-timing residuals with frequency f = m_φ/π and amplitude set by local DM density (computable from public PTA data, kernel-blind). **P2 (lensing):** σ(v)/m velocity-shape and r_c(M_halo) scaling; shape pinned (TEST), normalization (FIT), labeled in advance. (4) Kill condition (pre-committed): if no observable-relation survives (𝒱, g_s) elimination, model is generic vdSIDM → F5 triggers. **All predictions tagged with assumption list: [A-SEQ, A-VOL, A-ONT, A-REL].** | **T0 derives (§1.2.1 role A3), T0s blind re-derives from S2 certificates + literature inputs only** | Both derivations (T0, T0s) agree within stated tolerance on m_φ, α_D, Λ_D, final observable(s); numbers + uncertainties + assumption tags committed hash-pinned **before any data contact**; kill condition evaluated and result recorded | Two-model rule (§1.2.3); blind re-derivation diff report; assumptions audit; commit timestamp check |
| S3-01 | Data acquisition | Scripted, checksummed download of NANOGrav 15-yr free-spectrum posteriors, EPTA DR2, published lensing stacked-profile tables, Lyman-α constraint tables; document versions | T2 | `data/MANIFEST.md` with URLs, versions, SHA256; fetch script idempotent | Checksum CI |
| S3-02 | V5 pipeline core | Pipeline reads frozen `PREDICTION.md` parameters and Free-Parameter Ledger (no free knobs; (𝒱, g_s) values if not eliminated); computes model observable; compares to data; outputs pass/fail + likelihood/exclusion level; labels every comparison `TEST` or `FIT` per VISION §5 and per the ledger strategy | T1 architecture per T0 spec; T2 implements modules | Full run on synthetic data recovers injected signal (closure test); on null synthetic data reports null (no false positive at stated α) | Closure + null golden tests in CI; assumption-tag pass-through |
| S3-03 | PTA comparison (P1 observable) | If P1 selected: compare predicted nHz spectrum (f, amplitude) against public NANOGrav/EPTA posteriors. Report as exclusion σ or Bayes factor. Explicitly: comparison against published products, no collaboration claim. Mark as TEST (kernel-blind by design). | T2 runs; T1 drafts | Result reproduces from clean checkout in one command; assumption tags preserved | Reproducibility CI; T0 reviews interpretation |
| S3-04 | Lensing comparison (P2 observable) | If P2 selected: halo-profile prediction (r_c vs M_halo shape) vs published stacked profiles (dwarf regime). Split label: r_c shape = TEST, normalization = FIT. Same pattern as S3-03. | T2 runs; T1 drafts | Same | Same |
| S3-05 | `OBSERVATIONAL_REPORT.md` | Machine-generated results tables (from S3-02/03/04) + T0-written interpretation; every observable result carries TEST/FIT label + assumption list; F3/F4/F5 branches triggered mechanically from thresholds + kill-condition check, not judgment. Report published **even (especially) if all results are exclusions.** | T1 assembles tables; **T0 writes interpretation section only** | Report published; kill-condition evaluation recorded; no hand-entered numbers in evidence sections | T0s adversarial pass (assumption-breaking focus); Xavier sign-off |

**Stream 3 exit criterion (feeds G1/M1 → G2/M2):** `PREDICTION.md` complete with Free-Parameter Ledger + MVM steps 1–4; both T0 and T0s agree; observable(s) chosen and pre-registered; all assumptions tagged; kill condition evaluated; commit timestamp audit clean.

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

## 7. Phase Gates (updated for MVM + assumptions architecture)

| Gate | Contents | Blocking checks |
|---|---|---|
| **G0** (wk 2) | VISION v1.2 (with §0 amendments), Phase 0 complete (P0-A/B/C/D), `K3_CRITERIA.md` v1.0 frozen with C3b, S1-01 CI green | A1–A3 applied; ASSUMPTIONS.md complete; P0 artifacts live; criteria two-model-signed; C3b checker golden tests pass |
| **G1 = M1** (mo 2.5) | **GATE M1 (new).** C3b checker passes on all candidates, identifies top pair; S2-04 SelectionReport complete; S3-00 `PREDICTION.md` complete (Free-Parameter Ledger + MVM steps 1–4 + observable selection + kill-condition evaluation); both T0 and T0s derivations agree; assumption tags audit clean; commit timestamp check (prediction ≤ data touch); `DERIVATION_DISPUTES.md` empty or all resolved | Two-model agreement on MVM; C3b identification valid; S2 adversarial memo resolved; S3 assumption-breaking adversarial pass resolved; timestamp audit |
| **G2 = M2** (mo 8) | Stream 1 kernel-green core + Stream 2 report; arXiv math preprint draft | Open-goal list honest; adversarial memo resolved; assumption hygiene audit (no axiom encodes non-reproducible constant); C3b certificates archived |
| **G3 = M3** (mo 14) | `OBSERVATIONAL_REPORT.md` with results tables (P1/P2 comparisons) | Pre-registration audit + timestamp audit; branch triggers (F1–F5) mechanical from thresholds; TUNING_LOG.md updated if assumptions changed; TEST/FIT labels honest |
| **G4** (mo 18) | Manuscript(s), venue by result strength | T0 claim-vs-evidence review; assumption-list consistency check (every claim tagged); Xavier sign-off |

---

## 8. Changelog

- **v1.0 (2026-07-17):** Initial execution plan. Adds model-tier routing (T0 Fable 5 / T0s Deep Think / T1 Sonnet–Gemini Pro / T2 Haiku–Flash), verifier-first delegation rule, two-model blind re-derivation rule for physics, per-WP DoD and validation gates, and amendments A1–A3 correcting VISION v1.1 epistemic regressions.
- **v1.1 (2026-07-17):** **Major revision integrating Phase 0 ASSUMPTIONS (v0.2) and T0 Architecture Review.** New: (1) Phase 0 work packages (P0-A/B/C/D) establishing ASSUMPTIONS.md, Free-Parameter Ledger schema, abstract-tier rule, TUNING_LOG.md; (2) C3b criterion (Shioda-Inose moduli map as checkable claim) added to S2-01 + dedicated checker S2-01b; (3) S3-00 completely rewritten as MVM matching calculation with steps 1–4 (m_φ, α_D, Λ_D, observable elimination) under assumptions [A-SEQ, A-VOL, A-ONT, A-REL]; (4) T0/T0s blind re-derivation gate for MVM (two-model rule); (5) P1 (PTA ultralight) and P2 (lensing shape) observables as checkable outputs; (6) kill condition pre-committed (no invariant → F5); (7) GATE M1 (new) inserted between G0 and G2 as the MVM completion gate; (8) assumption tags on all predictions + TUNING_LOG tracking; (9) adversarial passes extended to explicitly attempt breaking A-SEQ and A-REL. Critical path now: C3b checker → top pair identification → MVM derivation → blind re-derivation agreement → M1 pin.

---

## Related Documents

- **VISION.md** — Master vision (epistemic framework, falsification branches, phase roadmap)
- **K3_CRITERIA.md** — Frozen criteria for K3 ranking (feeds S2-01)
- **PREDICTION.md** — Falsifiable predictions (gates S3-00, feeds Phase gates)
- **BRIEFS/** — Per-WP execution instructions (generated by T0 per §5.1)
- **ADVERSARIAL/** — Deep Think adversarial memos (per §5.2)
- **TIER_LEDGER.md** — Epistemic rulings (per §5.1)
