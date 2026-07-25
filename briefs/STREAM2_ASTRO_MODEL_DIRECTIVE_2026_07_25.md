# Stream 2 Directive — Astrophysical Model Construction (Phase M)

**Date:** 2026-07-25
**From:** Fable 5 (T0), **[T0-DELEGATED]** under Xavier's instruction of 2026-07-25
("provide directions for stream 2 to build the astrophysic model"). Xavier countermand
window open, as always.
**To:** Stream 2 (K3 Theory & Candidate Selection)
**Prerequisite reading:** `NO_PREDICTION_BRANCH.md` §8.5 (the terminus this must not
re-walk), `docs/T0_SIGNOFF_WP_R5_R6_R7_2026_07_25.md`, `docs/WP_R6_SURVEY_SCALES.md`,
`docs/WP_R7_BETA_VARIANCE_SCAN.md`, `ASSUMPTIONS.md` v2.0-SIGNED, `LESSONS_LEARNED.md`.

---

## 1. Objective — stated at its honest tier

Stream 2 is directed to **attempt** the construction of an astrophysical model
**[Tier C — this is conjecture work by definition]**: a worked EFT/mechanism chain that
*would*, if it exists, connect the certified K3 mathematics (Tier A/B: Sym² identity,
ρ=4/T=18 Shioda–Tate, 2× Type II Kodaira fibres) to an observable that Stream 3's data
can actually resolve.

Two framings of this objective, and only the second is authorized:

- ❌ "Find a way to test the theory" — that is how programs quietly become unfalsifiable.
- ✅ "Determine whether a testable model exists, and report either outcome with equal
  prominence" — a NO here is a deliverable, exactly as F5b and Off-Ramp 3 were.

## 2. What is closed and stays closed

The **[A-DD]-anchored branch is terminated** (Off-Ramp 3, `NO_PREDICTION_BRANCH.md`
§8.5): under the Dark Dimension identification, the mediator range never exceeds ~30 μm
at any density; no Mpc-scale observable can test it, and the lab-scale re-scope failed
its circularity/reach audit (`WP_A2_CIRCULARITY_AUDIT.md`). This directive does **not**
reopen it. Any model that routes its scale-setting through [A-DD] is dead on arrival —
do not spend hours discovering this again.

Likewise off-limits: the quarantined `[A-DATA-LEGACY]` Δ observables (`ASSUMPTIONS.md`),
and any post-hoc inheritance of the v1.0 pin — a new model gets a **new pre-registration
(PREDICTION v2.0) or nothing**.

## 3. The three walls, named up front

F5b failed at three specific, independent obstructions (`NO_PREDICTION_BRANCH.md` §8).
A new model memo must state, per coefficient, which wall it hits and how it proposes to
get past it — *before* any derivation work begins. Silence on any wall = automatic
return of the memo.

| Wall | What blocked it last time | What a new attempt must supply |
|---|---|---|
| **Type II veto (a₁ / Λ_D)** | Certified fibres are 2× Type II — no gauge algebra under Kodaira–Tate; no weakly coupled dark SU(N) available from the fibres | A different gauge-sector origin, stated explicitly as conjecture, with its own falsifiable consequence — or a candidate whose certified fibre content is Type III or beyond |
| **Flat-direction wall (a₂ / m_φ)** | Order-3 PF operator controls a rank-3 sub-VHS; T=18 leaves 15 moduli unstabilized → massless scalars excluded by fifth-force bounds | A stabilization story for the full transcendental lattice, or an argument (checkable, Tier B at best) that the uncontrolled moduli decouple from the observable |
| **Topology void (a₃ / vacuum energy)** | χ(X₄) depends on an unspecified base B₃; tadpole condition not even posable | Either specify B₃ (real model-building), or drop the vacuum-energy identification entirely and let the model make no dark-energy claim |

A model that gets past **two** walls and honestly reports the third as open is a
partial result worth having. A model that "gets past" all three by assumption-stacking
is a fit dressed as a derivation (`.agents/AGENTS.md` Rule 7) and will not clear T0.

## 4. Design envelope — measured, not assumed (WP-R6/R7 outputs)

Any proposed observable must land inside what the data on hand can resolve. These
numbers are measured from the real catalogs (sources cited; do not re-derive from
memory):

- **Transverse scales:** finest resolved ≈ 0.22–0.27 Mpc at median z ≈ 1.4–1.5 in the
  Euclid photo-z cones (`docs/WP_R6_SURVEY_SCALES.md`, Redshift-Dependent Facts table).
- **Volumes:** ~9.5–9.7 × 10⁶ Mpc³ per Euclid cone; only 8.46 Mpc³ in the local
  spectroscopic Coma field (same table).
- **Statistic:** target **β₁ and/or β₂, not β₀**, at nbins=8 — β₁/β₂ carry nonzero null
  variance in 30/30 scanned (threshold, scheme) combinations on the Euclid fields
  vs. β₀'s 14/30 (`docs/WP_R7_BETA_VARIANCE_SCAN.md` §3/§5). A β₀-type signature is
  admissible only with threshold ≥ 80% or a finer grid, justified in the memo.
- **Threshold specification:** state thresholds in absolute density or explicitly above
  the field's empty-bin fraction — percentile ladders below that floor are degenerate
  on sparse fields (WP-R7 §4: Coma is 93.8% empty; percentiles 50–90 all collapse to
  threshold 0).
- **No shear:** public Euclid has no lensing shear catalogue (finding R-SHEAR); any
  κ-peak-based proposal is synthetic-only until that changes.

A model whose predicted signature falls outside this envelope is
**untestable-by-construction with current data** and must say so in its own §1 — that
statement is what separates an honest speculative model from a repeat of Gap G-1.

## 5. Mandatory process gates (unchanged, restated)

1. **P4 siblings:** every candidate-dependent quantity is computed across all sibling
   families via `pipeline/siblings.py` (WP-R4) — parameters certificate-traced, never
   typed. If every sibling fits equally well, the result is null; that check cannot be
   skipped, the harness raises if you try.
2. **Two-model rule:** any physical derivation destined for PREDICTION v2.0 is produced
   by one of {Fable 5, Deep Think} and blind re-derived by the other; disagreement →
   `DERIVATION_DISPUTES.md`, deliverable blocked.
3. **Pre-registration:** PREDICTION v2.0 hash-pinned *before* any contact with the data
   it names; §6 derived quantities hash-pinned before any TEST/FIT label (gate G1-L,
   mechanical, `pipeline/gate.py`).
4. **Kill condition, pre-committed now:** if after the two-model pass no relation
   survives (𝒱, g_s)-elimination — or no mechanism clears §3 without importing an
   unconstructed scenario — Stream 2 files the negative under this directive and stops.
   That outcome is reportable, publishable, and not a failure of process.
5. **Tier language:** every mechanism sentence carries its conjecture marker;
   `check_tier_language.py` clean on every commit; forbidden verbs
   (predicts/establishes/shows/implies/locks/governs/determines/demonstrates/proves)
   never applied to unconstructed physics.

## 6. Deliverables and stop-points, in order

| # | Deliverable | Owner | Stop-point |
|---|---|---|---|
| M1 | **Mechanism memo** (≤2 pages): which wall-route per §3, which envelope cell per §4, sibling list, kill condition restated | Stream 2 (T1 drafting allowed) | → T0 review before any derivation |
| M2 | **Derivation attempt** under the two-model rule; all constants certificate- or literature-traced | T0 + T0s only | → adjudication in `DERIVATION_DISPUTES.md` |
| M3 | **PREDICTION v2.0 draft** with Free-Parameter Ledger and assumption tags | T0 | → Xavier pin decision |
| M4 | Only after pin: Stream 3 parameterizes the existing scaffold (`pipeline/stream3_comparison.py`, config-only change) and the WP-R5 null infrastructure ingests the observable | Stream 3 | G1-L opens mechanically iff §6 hash-pinned |

**No step may be started before the previous stop-point clears.** M1 is the only step
authorized by this directive today.

## 7. Effort guidance

M1 is a thinking-and-writing task, not a computing task: 4–8 focused hours, T1-draftable
with T0 review. If M1 cannot name a route past §3's walls in that time, the honest
output is a short memo saying so — which would be the third clean negative of this
program, and worth exactly as much as the first two.

---

`Generated-by: Fable 5 (T0, [T0-DELEGATED] under Xavier instruction 2026-07-25) | Verified-by: envelope numbers traced to docs/WP_R6_SURVEY_SCALES.md + docs/WP_R7_BETA_VARIANCE_SCAN.md (T0-recomputed same day, docs/T0_SIGNOFF_WP_R5_R6_R7_2026_07_25.md §1); wall statements traced to NO_PREDICTION_BRANCH.md §8 | Reviewed-by: T0 Y — Xavier countermand window open`
