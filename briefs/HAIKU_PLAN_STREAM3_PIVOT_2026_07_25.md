# Stream 3 Pivot — Haiku-Tier Execution Plan (WP S3-P series)

**Authority:** T0 ruling of 2026-07-25 (`briefs/T0_RULING_G1L_AND_PIVOT_AUTHORIZATION_2026_07_25.md`),
executed under Fable 5 delegation.
**Executor:** Haiku 4.5 sessions (T2 mechanical work), except where a WP is explicitly
marked T0-tier.
**Date:** 2026-07-25
**Governing docs:** `CLAUDE.md` (6 rules), `.agents/AGENTS.md` (8 rules, Stream 2 repo),
`prereg-pipeline` + `epistemic-guardrails` skills, `pipeline/gate.py` (G1/G1-L).

---

## 0. What this plan is

The T0 ruling authorizes pivoting Stream 3 from exact point-mass targets to bounded
dynamic field profiles (chameleon spatial gradients vs weak-lensing κ peaks, plus a
cosmic-web topology criterion), and lifts the `[A-DATA-LEGACY]` quarantine on the Δ
observable. This plan turns that authorization into executable work packages with
validation criteria and definitions of done, sequenced so that **every number that ends up
in `PREDICTION.md` v2.0 §6 exists in a committed, cited, dimensionally-checked derivation
document before it is pinned** — the standard the gates now mechanically enforce.

## 1. Reconciliations — read before starting any WP

Four factual gaps between the ruling's text and the repo record. None voids the
authorization; each maps to a WP that closes it honestly.

**R1 — Off-Ramp 2 is authorized, not yet executed.** The ruling's §4 treats the
swampland-bound derivation as done. The committed record says otherwise: WP S3-00b closed
on **Off-Ramp 3** (`DERIVATION_DISPUTES.md` 2026-07-25 entry: "unified concurrence on
Honest Off-Ramp 3; F5b stands"), and `PREDICTION_APPENDIX_A.md` A.3.4 states the swampland
bound "was **not** computed in this work package and remains open." A precise repo search
(2026-07-25) finds zero occurrences of "Dark Dimension", "Casimir", "De Giorgi", "Nash",
or "Hölder" in either repo. → **WP-A performs the derivation for real.** Until WP-A's
artifact is committed, no §6 content exists to pin. (Per `epistemic-guardrails` rule 5 and
`AGENTS.md` Rule 7, citing the ruling itself as the provenance of a number is circular.)

**R2 — Three §6 entries have definitional defects that block pinning as-worded.**
  (a) *"m_φ bounded by Hölder regularity (α ∈ (0, 0.5])"* — a Hölder exponent is a
  dimensionless regularity index of an elliptic-PDE solution; m_φ carries eV. α can bound
  the chameleon **profile shape** (a legitimate, testable prediction) but cannot bound a
  mass. WP-A must recast this as a shape/gradient bound or derive an actual mass window.
  (b) *"ρ_DE bounded topologically 𝒪(10⁻³…1)"* — ρ_DE is a measured quantity
  (~10⁻⁴⁷ GeV⁴); presumably the coefficient a₃ is meant. Ambiguous as written; WP-A must
  state which symbol, with units.
  (c) *"Λ_D ~ m_KK (Dark Dimension)"* — real literature exists (Montero–Obied–Vafa line),
  but a citation to a scenario is not a derivation for **this** K3. WP-A must derive the
  connection or bound it with the assumption tag that carries the gap.

**R3 — The Δ quarantine lift is recorded but not yet operative.** T0 authority to lift is
respected. But the quarantine's stated reason was *irreproducibility* ("not reproducible
from checkers in this repo today… until regenerated with manifest-pinned data",
`ASSUMPTIONS.md` §2 ledger), and `AGENTS.md` Rules 1/5 forbid using unreproduced numbers
regardless of quarantine status. → **WP-D regenerates Δ from manifest-pinned data**; the
lift becomes operative the moment reproduction succeeds, and the ledger entry records both
the T0 lift and the reproduction evidence.

**R4 — Two mechanical corrections to the ruling's Step 5.2/5.4.**
  (a) `pipeline/gate.py` *verifies* headers; it does not generate them. → WP-B builds the
  pin tool. (b) `D3_batch_runner_phase2.py`'s `_evaluate_sector()` still returns
  `np.random.normal()` placeholder statistics; opening G1-L without replacing them would
  label random numbers `TEST`. → WP-E replaces them with real computations **before** any
  gate opens; the runner's pre-flight `require_derived_for_labels()` stays.

## 2. Hard rules for Haiku sessions (non-negotiable)

1. **Never pin.** Do not add/modify `PINNED:` or `DERIVED:` headers. Pinning is WP-G,
   T0-only.
2. **Never fetch comparison data pre-pin.** The audit rule in `PREDICTION.md` requires the
   pin commit to predate any fetch of the observable's comparison dataset. Pre-pin, only
   synthetic/golden data. (Calibration data that is *not* the comparison target may be
   fetched if hash-pinned in the manifest — when unsure, don't.)
3. **No numbers from memory.** Every constant traces to a certificate, a committed
   derivation doc, or a hash-pinned `refs/` entry. If you cannot point to the source, stop
   and flag.
4. **Do not run `D3_batch_runner_phase2.py`.** It refuses via G1-L; do not weaken the gate
   to make it run.
5. **Do not edit `PREDICTION.md` (v1.0-PINNED) in place.** The v2.0 draft is a separate
   file until T0 promotes it (WP-F/G).
6. **Invoke `prereg-pipeline` before touching `data/`, `pipeline/`, or any comparison;
   `epistemic-guardrails` before writing any prose.** Run
   `python3 scripts/check_tier_language.py` before every commit.
7. Every output stays labeled `SYNTHETIC` until G1-L opens — that is enforced in code;
   do not work around it.
8. Every generated file carries the provenance footer
   (`Generated-by | Verified-by | Reviewed-by`).

## 3. Work packages

### WP-A — Execute Off-Ramp 2: the swampland-bound derivation ⛔ NOT HAIKU

**Tier:** T0 (Fable 5 primary, Deep Think blind re-derivation — two-model rule).
**Blocking:** everything in WP-F §6 content and WP-G. Haiku sessions must treat WP-A's
output as an input; if it does not exist, downstream WPs proceed only in the parts that
don't need it.
**Deliverable:** `SWAMPLAND_BOUNDS_A123.md` containing, for each of Λ_D, m_φ-or-profile,
a₃: the derivation chain, the literature citation (verified to exist, with arXiv ID), the
bound with explicit units, a **dimensional-analysis table**, the R2 defect resolutions,
and assumption tags. Plus a `DERIVATION_DISPUTES.md` entry (agreement or dispute).
**Validation:** every bound has ≥1 verifiable citation; every quantity has units; the R2
items (a)–(c) each have an explicit resolution paragraph; Deep Think entry present.
**DoD:** committed; `check_tier_language.py` clean; F5b section of
`NO_PREDICTION_BRANCH.md` updated to record Off-Ramp 2 execution (superseding, not
deleting, the Off-Ramp 3 record — the history stays).

### WP-B — Pin/derive header tool (Haiku)

**Objective:** `scripts/pin_prediction.py` that generates correct `PINNED:` and `DERIVED:`
headers for a given file, using the exact stripping/hashing algorithm in
`pipeline/gate.py` (`_strip_header_lines`, §6 extraction via the same regex).
**Directions:** (1) import the regexes/helpers from `pipeline.gate` — do not duplicate
them; (2) modes: `--pin`, `--derive`, `--both`, `--check` (dry-run prints hashes without
writing); (3) refuse to overwrite an existing valid header unless `--force`; (4) tests in
`pipeline/tests/test_pin_tool.py`: round-trip (generate → `verify_pin_hash()` and
`verify_derived_hash()` both True), idempotence, `--force` behavior, and the
marker-ordering case (DERIVED added after PINNED must keep both valid).
**Validation:** `pytest pipeline/tests/test_pin_tool.py -q` green; running `--check`
against the current `PREDICTION.md` reproduces its existing pin hash exactly.
**DoD:** tests green in the full suite (`pytest pipeline/tests/ -q`, exit 0); tool never
invoked with write-mode on `PREDICTION.md` by Haiku (rule 2.1).
**Skills:** none beyond baseline; run `/code-review` on the diff.

### WP-C — §6 schema validator in gate.py (Haiku) — Deep Think's recommendation

**Objective:** replace the placeholder string-match in `has_derived_quantities()` with a
schema check that **fails closed**: §6 must contain at least one parseable bounded
quantity to count as populated.
**Directions:** (1) define the schema as a regex family over lines of the form
`<symbol> ∈ [<lo>, <hi>] <unit-or-dimensionless-tag> [<assumption-tags>]` (accept `∈`,
`in`, `≤ … ≤`; accept scientific notation; require an explicit unit token or the literal
`dimensionless`); (2) keep the placeholder-wording check as an additional veto (belt and
suspenders — both must pass); (3) extend `pipeline/tests/test_gate.py`: a §6 with a valid
bound line passes; a §6 with prose but no parseable bound fails; a dummy string designed
to fool the old check (e.g. real-looking text, no interval) fails; existing G1-L tests
stay green unmodified except the FILLED_S6 fixture, which must gain a schema-conformant
line; (4) document the schema in the `gate.py` module docstring.
**Validation:** `pytest pipeline/tests/test_gate.py -q` green; live-repo test
`test_this_repo_is_pinned_but_labels_locked` still passes (this repo's §6 must still
fail the schema — it is reserved).
**DoD:** full suite green; schema documented; no change to G1 behavior.
**Skills:** `/code-review`; `epistemic-guardrails` for the docstring.

### WP-D — Δ observable regeneration scaffold (Haiku)

**Objective:** make the quarantine lift operative by regenerating the Δ statistic from
manifest-pinned inputs, per the quarantine's own discharge terms.
**Directions:** (1) invoke `prereg-pipeline` first; (2) locate the legacy Δ definition
(prior-phase dashboards; if the definition itself is unrecoverable, that is a reportable
finding — stop and flag, do not reverse-engineer from the quarantined numbers); (3)
implement `pipeline/delta_observable.py` computing Δ from a density field, with the
definition cited; (4) golden tests on synthetic fields (`pipeline/tests/test_delta.py`):
known-signal recovery + null-field false-positive rate at stated α; (5) **no real-data
fetch** (rule 2.2) — the real-sector regeneration run is WP-G, post-pin; (6) draft the
`ASSUMPTIONS.md` §2 ledger entry text (T0 lift + pending reproduction evidence) into the
WP report for T0 to apply — Haiku does not edit the SIGNED file.
**Validation:** golden tests green; Δ definition carries a source citation, not a memory.
**DoD:** module + tests committed; ledger-entry draft delivered; explicit statement in the
WP report of whether the legacy definition was recoverable.
**Skills:** `prereg-pipeline` (mandatory), `/code-review`.

### WP-E — Real observable computations (Haiku)

**Objective:** replace every placeholder statistic so that when G1-L opens, what gets
labeled is a real computation.
**Directions:** (1) invoke `prereg-pipeline`; (2) implement in `pipeline/observables.py`:
a weak-lensing **κ-peak statistic** (peak counts above threshold in a convergence map;
cite the standard estimator) and a **cosmic-web Betti-number computation** (β₀, β₁, β₂ via
persistent homology on a point cloud / density field — use an existing library if present
in the venv, else implement cubical-complex counting; cite the method); (3) each gets the
same golden-test pair as WP-D (signal recovery + null calibration) in
`pipeline/tests/test_observables_real.py`; (4) replace `_evaluate_sector()`'s
`np.random.normal()` blocks in `D3_batch_runner_phase2.py` with calls into these
computations; the G1-L pre-flight stays untouched; (5) the topology criterion
`β₁ > β₀ + β₂` is implemented as a *computable predicate* but NOT asserted as a prediction
anywhere in prose — whether it becomes a pinned prediction is WP-A/WP-F's decision.
**Validation:** `grep -n "np.random" pipeline/D3_batch_runner_phase2.py` returns nothing
in `_evaluate_sector`; golden tests green; full suite green; runner still refuses to start
(G1-L closed) — verify by running it and confirming the `GateError`.
**DoD:** all of the above + `/code-review` findings addressed.
**Skills:** `prereg-pipeline`, `/code-review`; `dataviz` if diagnostic plots are produced.

### WP-F — PREDICTION.md v2.0 DRAFT (Haiku drafts; T0 owns content)

**Objective:** `PREDICTION_v2_DRAFT.md` — slot-based, explicitly headed
`DRAFT — NOT PINNED — supersedes nothing until T0 promotion`.
**Directions:** (1) invoke `epistemic-guardrails`; (2) §2–§5 rewritten for the pivoted
observables per the T0 ruling: chameleon profile shape/gradient vs stacked weak-lensing
κ peaks (branch P1′), cosmic-web topology predicate (companion), Δ statistic per WP-D
definition; every TEST/FIT split declared in advance; kill conditions carried over (F5
family unweakened — `VISION.md` §4 permits strengthening only); (3) §6 contains **slots
bound to `SWAMPLAND_BOUNDS_A123.md` sections** — if WP-A is not yet committed, the slots
say `⟨awaiting WP-A §x⟩` and the draft states it cannot be pinned; if WP-A is committed,
transcribe the bounds verbatim with their units and tags, in WP-C schema-conformant
format; (4) changelog section explaining supersession of v1.0 and citing the T0 ruling.
**Validation:** `check_tier_language.py` clean; every §6 number traces to WP-A by section
reference; no forbidden Tier-C verbs without conjecture markers.
**DoD:** draft committed; explicitly unpinned; blind re-derivation package note included
(per `EXECUTION_PLAN.md` §1.2.3 the v2.0 pin also needs a T0s blind pass).
**Skills:** `epistemic-guardrails` (mandatory), `prereg-pipeline`.

### WP-G — Pin, gates, data, run ⛔ NOT HAIKU

**Tier:** T0 (Xavier or explicit delegation), after WP-A…WP-F complete.
**Sequence (order is load-bearing):** (1) T0s blind re-derivation of v2.0 §6 from WP-A
inputs; disputes to `DERIVATION_DISPUTES.md`; (2) promote draft → `PREDICTION.md` v2.0;
(3) `scripts/pin_prediction.py --both` (WP-B tool); commit — **this commit timestamp must
predate every comparison-data fetch**; (4) verify: `is_pinned()`, `verify_pin_hash()`,
`verify_derived_hash()`, `labels_unlocked()` all True; full suite green (the live-repo
gate test will need its expectation flipped in the same commit — that is the one
legitimate moment to do it); (5) fetch SDSS/Euclid comparison data via
`scripts/fetch_data.py` path, hash-pinned into the manifest; (6) run
`D3_batch_runner_phase2.py` (GPU T4, outputs on
`/mnt/disks/disk-socrateai-local-1`); (7) report per `prereg-pipeline`, every output
tagged, physics-washing audit before release.

## 4. Sequencing

```
WP-A (T0) ─────────────┐
WP-B (Haiku) ──┐       ├──> WP-F (draft) ──> WP-G (T0: pin → fetch → run)
WP-C (Haiku) ──┼───────┘
WP-D (Haiku) ──┤   (B, C, D, E are parallel-safe; none depends on WP-A)
WP-E (Haiku) ──┘
```

Haiku sessions can start WP-B/C/D/E immediately and in any order. WP-F can be started
with slot placeholders before WP-A lands, but cannot close until it does.

## 5. Definition of done — whole phase

- [ ] WP-A artifact committed with citations, units, R2 resolutions, two-model entry
- [ ] Pin tool exists, round-trips against the live pin (WP-B)
- [ ] §6 schema validator live, fails closed, Deep Think's dummy-string attack blocked (WP-C)
- [ ] Δ regenerable from a cited definition with golden tests; ledger draft ready (WP-D)
- [ ] Zero `np.random` in sector evaluation; real κ-peak + Betti computations golden-tested (WP-E)
- [ ] v2.0 draft complete, tier-clean, every number sourced (WP-F)
- [ ] Pin predates data contact (git-auditable); gates all True; suite green (WP-G)
- [ ] Nothing in the phase weakened `VISION.md` §2/§4 or the F-series triggers

---

`Generated-by: Fable 5 (T0-delegated) session 2026-07-25 | Verified-by: repo-record cross-check (DERIVATION_DISPUTES.md, NO_PREDICTION_BRANCH.md §8, ASSUMPTIONS.md §2 ledger, precise grep for claimed artifacts); gate state re-verified (pinned=True, labels_unlocked=False) | Reviewed-by: T0 Y (ruling received; reconciliations R1–R4 flagged for T0 awareness)`
