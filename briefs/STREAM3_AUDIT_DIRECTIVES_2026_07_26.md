# Stream 3 → Streams 1 & 2 — Audit of the Synthetic-Infrastructure Results + Directives

**Date:** 2026-07-26
**From:** Fable 5 (T0), **[T0-DELEGATED]** under Xavier's instruction of 2026-07-26
("analyze the last results, audit them, interpret them and provide directives and
actions for streams 1 and 2"). Xavier countermand window open, as always.
**To:** Stream 1 (Geometric Theory / Lean) and Stream 2 (K3 Theory & Candidate
Selection, Phase M).
**Location (canonical):** `briefs/STREAM3_AUDIT_DIRECTIVES_2026_07_26.md`, main branch.
**Source material (all committed):** `docs/SYNTHETIC_NULL_SCAN_REPORT.md` (WP-T6 output),
`docs/STREAMS_STATUS_2026_07_26.md` (WP-T1–T6 record incl. two defects caught),
`pipeline/D3_batch_runner_phase2.py` (post-T3 certificate-lookup audit),
`checkers/certificates/` (inventory), release `v0.9.0-stream3-synthetic-infra`.

---

## 1. What was analyzed, and its epistemic ceiling

The WP-T1–T6 series (release v0.9.0) is **synthetic-only pipeline infrastructure**. Its
newest numeric output, `docs/SYNTHETIC_NULL_SCAN_REPORT.md`, is a scan of β₀/β₁/β₂
against three null-randomization schemes on **mock catalogs with injected artificial
clustering**. Nothing below is evidence about the cosmos, any survey, or any hypothesis.
What the scan does carry is **method findings**: how the statistics and null schemes
behave under controlled conditions — and those findings bind how Streams 1/2 may write
future decision rules. Off-Ramp 3 stands; G1/G1-L remain closed; this brief reopens
nothing.

## 2. Audit performed (mechanical, this session)

| Check | Method | Result |
|---|---|---|
| Determinism of the scan | Re-ran seed-1/nbins=8 cell (all 9 statistic×scheme entries) from a fresh process; compared against the committed report | **Exact match, 9/9 cells** |
| Gate integrity | grep on `require_pinned_for_real_data` / `require_derived_for_labels` call sites across the WP-T series diffs | Unmodified; G1-L still blocks `run_batch()` |
| Certificate inventory vs. cross-stream claims | `ls checkers/certificates/` against the premise line of `STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md` §1 | **Gap found — see F-AUD-1** |
| Test suite | Full run on merged main | 310/310 pass |
| Defect review of the executing agents' own output | Direct file reads, not self-reports | 2 defects found and fixed pre-commit (false T0 footer; tautological-pass constants) — recorded in `docs/STREAMS_STATUS_2026_07_26.md` |
| Box geometry sanity | Corner extents via `pipeline.cosmology.radec_z_to_cartesian_mpc` | Mock box ≈ 738×614×448 Mpc → cubic `nbins³` binning gives **anisotropic voxels** (~1.6:1); acceptable for engineering, must be stated if this scan is ever used as a template |

## 3. Interpretation — four method findings (synthetic; method-binding, not physics)

**F-SYN-1 — "Separation from null" is scheme- AND tail-relative.** At nbins=8, the same
observed β₁ sits at the **100th percentile against CSR and z-shuffle nulls and the 0th
percentile against density-shuffle nulls, in all three seeds** (e.g. seed 1: observed 8;
CSR null 0.70±0.74; density-shuffle null 34.97±4.48). Mechanism: density-shuffle
preserves the cell-value histogram but destroys spatial coherence, producing
salt-and-pepper fields rich in spurious small loops; CSR/z-shuffle re-scatter the points,
producing smoother fields poorer in topology than the clustered original. Consequence: a
decision rule that says only "β₁ separates from null" is under-specified to the point of
being unfalsifiable-by-choice — the scheme and the tail (upper/lower) must be
pre-registered together.

**F-SYN-2 — Each statistic has a resolution regime, reproduced under controlled
conditions.** nbins=4 is degenerate (β₀=1, β₁=β₂=0, most null banks zero-variance →
percentile honestly `None`). nbins=16 kills β₂ (observed 0 in all seeds) while CSR nulls
inflate it (mean 8–23): cavity statistics die when voxel scale outruns point density.
This reproduces, on synthetic data, what WP-R7 measured on real fields — the two now
corroborate each other at the infrastructure level.

**F-SYN-3 — Null-bank size bounds the claimable significance.** 30 trials → 3.3%
percentile granularity; "100.0%" means only *observed ≥ all 30 nulls* (one-sided
empirical p ≳ 1/31). Any future decision rule needing p < 0.01 must specify a bank of
≥ 100 trials (or exact-test machinery) in advance.

**F-SYN-4 — The percentile convention matters at the degenerate edge.** The scan uses
*fraction of nulls ≤ observed* (ties count). On near-degenerate banks this reads 93–97%
when the observed value merely ties the bulk (seed-1/nbins=4/β₂/z-shuffle: null
0.03±0.18, observed 0 → 96.7%). The convention is defensible but must be stated wherever
a percentile is quoted; a mid-rank convention is a reasonable pre-registered alternative.

**F-AUD-1 — Cross-stream certificate gap (the audit's one discrepancy).**
`STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md` §1 describes "certified K3 mathematics
(Tier A/B: Sym² identity, ρ=4/T=18 Shioda–Tate, 2× Type II Kodaira fibres)". What is
certificate-backed **in this repo** today: C1 (mirror integrality) for s7 and s10,
`PASS(40)`; C3/C3b **only for the golden AZ control pairs** (A↔δ, C↔α, D↔η), **not for
either Cooper candidate**; **no C2 certificate at all** (the C2 checker is blocked on
`K3_CRITERIA.md`'s `TBD-AT-FREEZE` constraint), so ρ=4/T=18 and the fibre content have
no computed artifact here — which is why `D3_batch_runner_phase2.py` now reports them as
honest NaN gaps rather than constants. The fibre-type certificate cited by WP-H
(`C1loci_cooper_s7_partner.json`) lives in Stream 2's repo; the trace must go there, not
to prose. This is a provenance-wording gap, not an accusation of error — but Rule P1
applies to directives too.

## 4. Directives — Stream 1 (Geometric Theory / Lean)

| # | Directive | Why |
|---|---|---|
| D1.1 | **Resolve `K3_CRITERIA.md` C2's `TBD-AT-FREEZE` constraint** (the exact Kodaira/Euler-characteristic consistency identity, with literature citation). This is the single blocker on `check_C2_kodaira.py`, and therefore on any computed certificate for ρ=4/T=18 and fibre content in Stream 3. | F-AUD-1; `docs/STREAM3_CHECKER_SUITE_PLAN.md` WP-3 has waited on this since 2026-07-24 |
| D1.2 | Until D1.1 lands, **do not describe ρ=4/T=18 or fibre content as "certified" in cross-stream prose**; the honest wording is "certificate-backed: C1 (s7, s10); pending certificate: C2, and C3/C3b for the Cooper candidates". Fibre-type statements trace to Stream 2's `C1loci` certificate file, never to a brief (WP-H found a brief contradicting that certificate). | F-AUD-1; P1 |
| D1.3 | **Route any inbound or outbound brief through the mechanical triage protocol** (`pipeline/triage.py`: commit/file/constant verification, SHA256 vendoring) before acting or asking others to act. Three fabrication-adjacent briefs reached the streams in 72 hours; the protocol is now reference code. | WP-T1; `d3-brief` history |

## 5. Directives — Stream 2 (Phase M, binding on the M1 memo)

These extend — do not replace — `STREAM2_WP_H_EXPERIENCE_BRIEF_2026_07_25.md` §2–§4 and
the directive's own §4 envelope.

| # | Directive | Why |
|---|---|---|
| D2.1 | Any M1 decision rule built on β₁/β₂ must **pre-register the null scheme AND the tail** (e.g. "β₁ above the CSR 95th percentile", not "β₁ separates from null"). The same observed value can sit at opposite extremes under different valid schemes. | F-SYN-1 |
| D2.2 | Any β₂-based signature must **state its resolution regime** (nbins / voxel scale at which cavities survive for the target field's density) in its own §1. | F-SYN-2; consistent with WP-R7 §4 and the WP-H scale wall |
| D2.3 | The memo must **specify the null-bank size matching its claimed significance** and **state its percentile convention** including tie handling and `None`-on-zero-variance. `PREDICTION_v2_DRAFT.md` §6 carries placeholders for exactly these fields. | F-SYN-3, F-SYN-4 |
| D2.4 | **Annotate or correct the "certified" premise line** of the Phase M directive per F-AUD-1: either import the Sym²/fibre certificates into this repo's trace, or adopt the downgraded wording of D1.2. A mechanism memo that inherits the uncorrected line inherits an unverified premise. | F-AUD-1; Rule 7 (`.agents/AGENTS.md`) |

## 6. Actions retained by Stream 3 (follow-ups, non-blocking)

- **A3.1** Efficiency: the scan recomputes identical null realizations once per statistic
  (`compute_betti_numbers` already returns all three β's per call) — 3× waste, zero
  correctness impact since realizations are deliberately shared across statistics.
  Cleanup candidate for the next infra pass.
- **A3.2** Offer a pre-registerable mid-rank percentile option alongside the current
  ≤-convention (F-SYN-4).
- **A3.3** Document voxel anisotropy (§2, last row) in the scan report header when the
  scan is next regenerated.

## 7. What this brief does not do

It does not reopen G1/G1-L, does not modify Off-Ramp 3 or the F-LAB trigger, does not
authorize any real-data comparison, and does not promote any synthetic number to
evidence. A Stream 2 memo may cite §3's findings **as method constraints only**, with
this file as provenance.

---

`Generated-by: Fable 5 (T0, [T0-DELEGATED] under Xavier instruction 2026-07-26) |
Verified-by: determinism spot-check re-executed this session (seed-1/nbins=8, 9/9 exact);
certificate inventory from ls checkers/certificates/; box extents computed via
pipeline.cosmology (this session); full suite 310/310 | Reviewed-by: T0 Y — Xavier
countermand window open`
