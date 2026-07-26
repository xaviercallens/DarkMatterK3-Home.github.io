# PREDICTION.md — Pre-Registered Observable & Derivation Protocol (v2.0-UNPINNED DRAFT)

## Document Information
- **Version:** 2.0-UNPINNED
- **Status:** DRAFT — Structural template only; contains zero numeric predictions, zero physics constants, zero candidate-specific claims
- **Placeholder Convention:** All value-bearing fields use reserved markers from `pipeline/gate.py` — `RESERVED`, `Empty by design`, or `TO-BE-DERIVED` — to ensure machine-detectable placeholder status
- **NOTE — Immutability & Pinning:** This draft is NOT pinned and does NOT carry `PINNED:` or `DERIVED:` headers. Only a T0-authorized PREDICTION v2.0 (following successful Stream 2 mechanism memo M1 and derivation M2) may be pinned. Pinning is immutable per CLAUDE.md rule 2 and hook-enforced in `pipeline/gate.py`.

---

## 1. What is being pinned (and what deliberately is not)

**TO-BE-DERIVED:** This section will specify, once M2 (derivation attempt) is complete under the two-model rule and a mechanism memo (M1) has been approved by T0, which quantities are pinned as pre-registration rules versus which are derived.

---

## 2a. Candidate selection — TO-BE-DERIVED

**TO-BE-DERIVED:** The candidate selection process (if any real candidate is entered) will follow the mechanical rule specified in the original v1.0 and as amended by the mechanism memo (M1).

---

## 2. Candidate-selection rule (Route A — retained as override path)

**TO-BE-DERIVED:** A candidate-selection rule governing eligible pairs and tie-breaking criteria. This structure mirrors PREDICTION v1.0 §2 but is awaiting the outcome of Stream 2's M1 mechanism memo and M2 derivation attempt.

---

## 3. Observable decision rule (the pin)

**RESERVED:** The observable decision rule will specify, once M2 is complete, which observable branch (if any) is mechanically triggered by derived quantities and how that observable relates to publicly available comparison data.

**Decision branches anticipated (placeholder structure only):**

| Branch | Trigger Quantity | Observable | Data Product |
|---|---|---|---|
| [SYMBOL] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

*Note: Each entry is a placeholder and will be populated only after two-model M2 derivation and T0 pin.*

---

## 4. TEST/FIT split — declared in advance

**RESERVED:** The TEST/FIT labeling policy will be established by the completed M2 derivation and pinned in this section before any data contact. The split specifies which derived quantities or observable predictions are pre-registered (TEST) versus which are fit post-hoc (FIT).

**Anticipated structure (placeholder):**

| Quantity | Category | Label |
|---|---|---|
| [SYMBOL] | [TYPE] | RESERVED |

*All actual entries TO-BE-DERIVED.*

---

## 5. Kill condition — pre-committed

**TO-BE-DERIVED:** A kill condition specifying the mechanical outcome that would trigger falsification (F-branch in VISION.md §4) or indicate the model is untestable with current data. This structure mirrors v1.0 §5 but is awaiting mechanism memo (M1) clarification of which observable relation is under test.

---

## 6. Derived quantities — Empty by design

**Empty by design at v2.0-UNPINNED.** This section is reserved for the completed, two-model-verified M2 derivation only. All entries below are structural placeholders showing what fields will appear once a T0-authorized mechanism memo (M1) passes review and Deep Think concurs on the M2 derivation.

### Expected Fields per M1/M2 Outputs (Mechanism & Derivation Approved)

The following table outlines expected §6 structure, drawn from the Stream 2 directive (`briefs/STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md`). Each row will be populated only after T0 authorization of M1 and two-model M2 completion.

| Quantity | Symbol (Placeholder) | Unit (Placeholder) | Bounds / Value (Placeholder) | Assumption Tags | Constraint Source |
|---|---|---|---|---|---|
| Mediator mass | `[SYMBOL]` | `[UNIT]` | `[RESERVED]` | [TO-BE-ASSIGNED] | Must land inside envelope per directive §4 (0.22–0.27 Mpc transverse scale) |
| Confinement scale Λ_D | `[SYMBOL]` | `[UNIT]` | `[RESERVED]` | [TO-BE-ASSIGNED] | Must satisfy Type II veto resolution (directive §3 wall 1) |
| Vacuum-energy identification | `[SYMBOL]` | `[UNIT]` | `[RESERVED]` | [TO-BE-ASSIGNED] | Must satisfy tadpole topology (directive §3 wall 3) or be dropped entirely |
| Observable choice (branch) | `[SYMBOL]` | [DIMENSIONLESS] | `[RESERVED]` | [TO-BE-ASSIGNED] | Mechanical trigger from derived quantities; see §3 decision rule |
| Null-test prediction | `[SYMBOL]` | `[UNIT]` | `[RESERVED]` | [TO-BE-ASSIGNED] | Lyman-α small-scale power; model must NOT produce excess (directive §4) |

### Candidate-Dependent Sibling Verification (M1/M2 requirement per directive §5.1)

**Process requirement:** Every quantity above is computed across all sibling families via `pipeline/siblings.py` (WP-R4 infrastructure). If every sibling fits equally well, the result is reported as null — a valid and reportable outcome. This check is mandatory and cannot be skipped.

**Placeholder:** Sibling results TO-BE-ADDED upon M2 completion.

### Observable Envelope Validation (M1/M2 requirement per directive §4)

All predicted observables must land inside the data's resolution envelope, measured from WP-R6/R7:

- **Transverse scales:** finest resolved ≈ 0.22–0.27 Mpc at median z ≈ 1.4–1.5 (Euclid photo-z cones)
- **Volumes:** ~9.5–9.7 × 10⁶ Mpc³ per Euclid cone; 8.46 Mpc³ local spectroscopic Coma field
- **Statistic:** target β₁ and/or β₂ (not β₀) at nbins=8; β₁/β₂ show nonzero null variance in 30/30 (threshold, scheme) combinations
- **Threshold specification:** absolute density or explicitly above field empty-bin fraction; percentile ladders degenerate on sparse fields
- **Shear caveat:** public Euclid has no lensing shear catalogue; κ-peak proposals are SYNTHETIC-only until that changes

**Placeholder:** Observable landing verified TO-BE-CONFIRMED once §3 observable is specified.

---

## Pathway to Real Prediction v2.0 — The M1 → M2 → M3 Chain

This draft exists to validate that the schema for a future PREDICTION v2.0 document is mechanically sound against `pipeline/gate.py`'s parsing logic. **No values, candidate names, or physical claims appear here.** Real population happens only via the gated sequence in `briefs/STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md` §6:

1. **M1 — Mechanism Memo** (Stream 2, T1 drafting allowed, T0 review gate): A ≤2-page memo naming which wall-route (Type II veto, flat-direction wall, or topology void) the proposed mechanism addresses, which envelope cell per §4 the observable lands in, sibling-list, and kill condition. **Stop-point:** T0 review; no derivation work proceeds without M1 approval.

2. **M2 — Derivation Attempt** (T0 + T0s blind re-derivation, two-model rule): Construct a₁, a₂, a₃ (or equivalent mechanism-specific coefficients) from certified geometry + literature / construction data. All constants are certificate- or literature-traced. **Stop-point:** Adjudication in `DERIVATION_DISPUTES.md`; if concurrence fails, M3 does not proceed.

3. **M3 — PREDICTION v2.0 Draft Conversion** (T0): Convert the M1-approved mechanism and M2-agreed derivation into a real PREDICTION v2.0 document, populating this template with actual bounded quantities (`symbol ∈ [lo, hi] unit`), assumption tags, and sibling verification results.

4. **Pinning Decision** (Xavier, T0 Owner): Only after M1/M2/M3 complete does T0 decide whether to pin PREDICTION v2.0. The pin covers §2–§5 (the rules and decision logic) in a first commit; §6 derived quantities are pinned separately in a second commit, with `DERIVED: <sha256>` header, only after both are verified.

5. **Gate G1-L Opens** (Mechanical): Only when both `PINNED:` and `DERIVED:` hashes are present and verified does `pipeline/gate.py`'s `labels_unlocked()` return True. Until then, all outputs are labeled `SYNTHETIC`, never `TEST` or `FIT`.

**Key constraint:** Silence on any of the three walls (directive §3) in M1 = automatic return without review. A negative outcome (no mechanism clears §3 without unconstructed physics) is a valid, reportable deliverable and does not denote failure of process.

---

Generated-by: Structural template (Claude, under T0 delegation 2026-07-26) | Verified-by: test suite `pipeline/tests/test_prediction_v2_draft_schema.py` (asserts zero PIN/DERIVED matches, all RESERVED markers present, all PREDICTION.md sections mirrored) | Reviewed-by: pending T0
