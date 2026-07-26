# WP-E2 — Triage of the re-pasted "Empirical Bounding for Stream 2" protocol, and what is executed instead

**Date:** 2026-07-26
**From:** Stream 3, executing under the mechanical triage protocol (`pipeline/triage.py`,
WP-T1) that `briefs/STREAM3_AUDIT_DIRECTIVES_2026_07_26.md` D1.3 requires for every
inbound brief.
**To:** Stream 1, Stream 2, and T0 (Xavier).
**Branch:** `wp-e2-synthetic-detectability` (experimental, per instruction).
**Verdict:** **PARTIAL — DISCARD §2.2/§3/§4/§5 as written; EXECUTE a re-scoped
synthetic-only core (WP-E2).** Rationale below, every claim checked against the repo.

---

## 1. Decisive finding: this protocol has already been executed

The pasted protocol is a **re-paste of the WP-E directive of 2026-07-25**, which was
already triaged, authorized, executed, and closed. Receipts:

- `docs/WP_E_T0_AUTHORIZATION_2026_07_25.md` §1 records the original paste verbatim
  ("STREAM 3 DIRECTIVE: WP-E Series — Autonomous GPU Auto-Research Loop") and states it
  "was flagged before execution for three issues: it targets the retracted WP-R3 null
  bank, it computes significance thresholds against real SDSS/Euclid data, and it labels
  the result `ENGINEERING/SYNTHETIC-BOUNDING`". **The re-paste re-proposes the same
  `[SYNTHETIC-BOUNDING]` label that T0 already replaced** with `SANDBOX-EXPERIMENTAL`
  (`EXECUTION_PLAN.md` §4.1).
- `docs/WP_E_EMPIRICAL_BOUNDS.md` — the exact deliverable path the protocol says Stream 3
  "will generate" — **already exists, is complete, and is T0-signed.** It contains the
  bounding box (§4), two disclosed implementation bugs (§2), a retraction of a float32
  artifact (§5), a T1 CPU spot-check (§6), and resolution-floor compliance (§7).
- Its **primary candidate window is already published to Stream 2**: `euclid_z_edf_north`,
  both deformation classes, distinguishable from the corrected null at
  **R ∈ [0.3, 4.0] Mpc**, max |σ| = 6.33 at (R=0.3, A=0.3, thr=1.5×mean, β₁).

Executing the protocol as written would **overwrite a completed, T0-authorized artifact**
with a re-run that re-introduces a label T0 already rejected. That alone is a stop.

## 2. Other defects found in triage (all mechanically verified)

| # | Claim in the protocol | Repo state | Severity |
|---|---|---|---|
| D-1 | `python3 scripts/auto_research_pipeline.py --observable betti_1_2 …` | **File does not exist.** The real WP-E entry points are `scripts/wp_e_gpu_sandbox.py` and `scripts/wp_e_t1_spotcheck.py` | Command would fail; same non-existent-script pattern as the D-3 brief |
| D-2 | β₀ excluded "due to proven null-degeneracy on sparse fields (Finding `R-NULLDEGENERATE`)" | **Mis-attributed.** `docs/FINDING_R_NULLDEGENERATE_2026_07_25.md` is about WP-R3's *null schemes* being point-pattern-preserving no-ops — it is not a β₀ finding. The β₀ power result is **WP-R7**: β₁/β₂ carry nonzero null variance at 30/30 scanned (threshold, scheme) combinations vs β₀'s 14/30 | Provenance defect — right conclusion, wrong citation |
| D-3 | `[SYNTHETIC-BOUNDING]` classification | Not in the authorized taxonomy. Five labels exist; the one T0 chose for exactly this kind of work is `SANDBOX-EXPERIMENTAL` (`EXECUTION_PLAN.md` §4.1) | Would silently create a sixth label |
| D-4 | `rm -rf data/derived/synthetic_sweeps/*` | Target does not exist; `data/derived/` holds `wp_e_sandbox_pointer_2026_07_25.json`, a WP-E artifact | Destructive command adjacent to a live artifact; not run |
| D-5 | "The autonomous coding agent is authorized to begin this study immediately" | Self-authorizing. WP-E's real-data significance computation required and received **explicit T0 authorization** (`docs/WP_E_T0_AUTHORIZATION_2026_07_25.md`) | Same self-authorization pattern as the D-3 brief |
| D-6 | Zone 2 = "Falsified … vacuum state falsified" via 5σ vs real SDSS/Euclid | The transformation `T(r_s, α)` is, by the protocol's own §2.3, a **"generalized spatial transformation"** introduced "without relying on unproven theoretical parameters" — i.e. not derived from the K3 mathematics | See §3 — this is the load-bearing defect |

## 3. The load-bearing defect: the bounding box cannot bind Stream 2 as claimed

The protocol instructs (§4): *"Stream 2's theoretical parameters … **must mathematically
land inside Zone 1**"*, and if they land in Zone 2, *"Stream 2 must report the vacuum
state as falsified."*

That inference does not hold, for two independent reasons:

**3.1 The zones bound an invented warp, not the model.** `T(r_s, α)` is admittedly generic.
A region where *a generic void→filament warp* becomes distinguishable from noise is not a
region where *the K3-derived mechanism* becomes distinguishable, and a region where the
generic warp conflicts with SDSS/Euclid does not falsify a vacuum that never predicted
that warp. Deriving a constraint on a model from a transformation chosen independently of
it is the same failure mode that ended WP-A2 (`WP_A2_CIRCULARITY_AUDIT.md`) — and WP-E's
own §8 already says this in plain terms: its σ cells are *"a statement about where a
generic smoothing/evacuation deformation becomes distinguishable from noise on this field
at this resolution — not a detection of anything, and not tied to any specific mechanism."*

**3.2 The Mpc-scale chameleon premise is already closed by a two-model adjudication.**
The protocol sweeps a chameleon screening radius over **r_s ∈ [0.27, 10.0] Mpc**.
`NO_PREDICTION_BRANCH.md` §8.5 records the adjudicated finding (gap G-1 →
**CLOSED-NEGATIVE**): *"under the cited chameleon mechanism and B3's own m_φ ~ m_KK
anchoring, the mediator's range never exceeds ~30 μm at any density, so **no Mpc-scale
observable can test the B1/B3 window in principle**."* That is ~11 orders of magnitude
below the sweep's floor. Sweeping Mpc-scale chameleon screening radii and reporting Zones
as "testable/falsified" would re-open Off-Ramp 3 **by assumption**, which requires a
written T0 ruling (CLAUDE.md rule 5), not a pasted protocol.

**None of this makes the underlying question worthless** — it makes the *real-data
falsification framing* unavailable. What survives is a genuine, unanswered, and currently
blocking question, addressed in §4.

## 4. What is executed instead — WP-E2, and why it is the actual unblock

WP-E delivered its bounding box using the two corrected null schemes available on
2026-07-25 (z-shuffle, angular-CSR). A **third** valid scheme, density-shuffle, landed
today (`pipeline/realfield3d.py::density_shuffle_realization`, WP-T2). Immediately after,
WP-T6's synthetic scan produced finding **F-SYN-1**
(`briefs/STREAM3_AUDIT_DIRECTIVES_2026_07_26.md` §3): *the same observed β₁ sat at the
100th percentile against CSR and z-shuffle nulls and the 0th percentile against
density-shuffle nulls, in all three seeds.*

That raises a specific, falsifiable question about the artifact Stream 2 is being told to
build on: **is WP-E's R ∈ [0.3, 4.0] Mpc window a robust feature, or an artifact of which
null schemes happened to exist when it was computed?**

WP-E2 answers it in the one setting where the answer is unambiguous — **controlled
injection on synthetic mocks, where ground truth is known because we inject the
deformation ourselves**:

- Apply a parameterized void→filament deformation `T(R, A)` to synthetic mock fields
  (`pipeline/synthetic_catalog.py`, WP-T6) at known (scale, amplitude).
- Score detectability of the *known-present* deformation against **all three** null
  schemes independently, on β₁ and β₂.
- Report, per (R, A) cell, whether the three schemes **agree** that the deformation is
  detectable — and the **amplitude floor** below which none of them detect it.

This yields two things Stream 2 does not currently have:

1. **A cross-scheme robustness rule** — quantifying how often single-scheme significance
   disagrees with the other schemes under *known* injection. This is what determines
   whether WP-E's σ numbers may be read at face value.
2. **An amplitude sensitivity floor** — the complement to WP-R6's *scale* floor
   (0.22–0.27 Mpc). The protocol's own §1 names this need ("if they derive a massive
   coupling constant…"); WP-R6/R7 bound *where* we can look, never *how strong* a
   signature must be to be seen.

**Compliance:** synthetic data only (no real-data fetch, no G1 exposure, no T0
authorization required); `SYNTHETIC` label only — no new label, no `TEST`/`FIT`; scheme
and tail pre-registered before running (D2.1); absolute density thresholds, never
percentile ladders (D2.2, WP-R7 §4); null-bank size and percentile convention stated
(D2.3); β₀ reported for completeness but not used for any verdict, cited to **WP-R7**, not
R-NULLDEGENERATE (fixes D-2); `docs/WP_E_EMPIRICAL_BOUNDS.md` **not touched**.

## 5. Directives — Stream 2 (Phase M / M1 memo)

| # | Directive | Basis |
|---|---|---|
| **E2.1** | Do **not** adopt the re-pasted protocol's §4 instruction ("parameters must land inside Zone 1", "Zone 2 ⇒ vacuum falsified"). WP-E's window is a generic-deformation detectability statement, per its own §8 — it can render a mechanism *untestable-by-construction*, it cannot *falsify* one. | §3.1 |
| **E2.2** | Any M1 mechanism whose scale-setting routes through an **Mpc-scale chameleon** is dead on arrival and must say so in its own §1 — the ~30 μm ceiling is adjudicated, two-model, CLOSED-NEGATIVE. This is the directive's existing "[A-DD] dead on arrival" rule applied to the chameleon range specifically. | §3.2 |
| **E2.3** | Treat WP-E's R ∈ [0.3, 4.0] Mpc window as **provisional pending WP-E2's cross-scheme result**. If WP-E2 shows the three schemes disagree under known injection, M1 must require agreement across all three before citing any window. | §4 |
| **E2.4** | When M1 states its predicted signature, state it as **(scale, amplitude)** — amplitude in units of the field mean, so it can be checked against WP-E2's floor, not scale alone. | §4 |

## 6. Directives — Stream 1 (Geometric Theory / Lean)

| # | Directive | Basis |
|---|---|---|
| **E2.5** | `briefs/STREAM3_AUDIT_DIRECTIVES_2026_07_26.md` D1.1 (resolve `K3_CRITERIA.md` C2's `TBD-AT-FREEZE`) is unchanged and remains the single blocker on any computed ρ=4/T=18 or fibre-content certificate. Nothing in this protocol substitutes for it. | prior brief |
| **E2.6** | Do not cite the re-pasted protocol's "K3 order-3 Picard-Fuchs recurrence and Chameleon mechanism" linkage as established; no artifact in either repo connects the order-3 recurrence to a chameleon screening radius. The geometric relation is not a physical coupling (VISION §1.3). | §3.1 |
| **E2.7** | Route future briefs through `pipeline/triage.py` before circulating. This is the fifth pasted brief in four days whose factual predicates did not survive checking; the protocol now exists precisely so this check is cheap. | D1.3 |

## 7. Escalation to T0 (Xavier) — one decision requested

If you want the **real-data** third-scheme check (density-shuffle applied to the actual
`edf_north` field, directly re-testing WP-E's published window rather than a synthetic
analogue), that touches real data and therefore needs the same explicit authorization
WP-E received. **Stream 3 will not self-authorize it.** WP-E2 as scoped here is the
synthetic-only version and needs no ruling.

---

`Generated-by: Claude Opus 5 (Stream 3), triage per pipeline/triage.py discipline |
Verified-by: every row of §2 checked by direct file/grep/ls against the working tree this
session (missing script, existing deliverable, label taxonomy, finding attribution, rm
target, authorization record); §3.2 quoted verbatim from NO_PREDICTION_BRANCH.md §8.5 |
Reviewed-by: T0 N — pending Xavier`
