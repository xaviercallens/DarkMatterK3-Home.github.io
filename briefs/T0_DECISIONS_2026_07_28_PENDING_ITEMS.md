# T0 Decision Record: Pending Items Ratification (2026-07-28, second record of the day)

**Authority:** T0 (Xavier Callens) | **Ratifies:** `T0_PENDING_DECISIONS_PROPOSALS_2026_07_28.md`
**Coordinator review:** every factual claim in the T0 rationale below was checked against its
source artifact before commit; two annotations recorded inline (marked ⚠), neither affecting
any decision.

---

## D1. Grid countermand window — CLOSED

The 56-cell grid (anchor `27cff4a`) stands as pinned. T0 rationale, verified against
`data/derived/wp_e6_grid_controls_report_2026_07_28.json`:

1. **Null control (m = −19.1):** max deviation 1.72%, under the 10% defect threshold —
   the pipeline recovers the expected regime where heavy FDM is indistinguishable from CDM
   at these scales (within the emulator's own resolution; CONTROL-labeled, not a physics
   result).
2. **Positive control:** 35× suppression-ratio contrast confirms m is genuinely plumbed
   through — check 1's null recovery is not vacuous.
3. **Internal consistency:** byte-identical P1D for the f = 0 column confirms the CDM-only
   branch (`f <= F_EPS` in `emu_predict.py`) is exactly m-independent — verified naming:
   `F_EPS = 1e-8`, `emu_predict.py:28`.
4. All cells sit strictly inside the trained LHS support; an open window added ambiguity
   with no benefit.

**Action taken:** countermand log entry appended to `briefs/T0_MF_GRID_DEFINITION_2026_07_27.md`
§5, marked WINDOW CLOSED. Next freeze point remains the PREDICTION v2 pin (unchanged).

## D2. Paper PLAN.md §5 — ALL FIVE APPROVED (Stream 1)

- **D2.1 Scope:** Option A (one unified paper; lattice/monodromy as labeled conditional
  sections). Option B retained only as structural fallback if referees force a split.
- **D2.2 Venue:** *Experimental Mathematics*.
- **D2.3 Authorship:** sole author Xavier Callens, "Independent Researcher". T0-mandated
  acknowledgment wording (verbatim, non-negotiable):
  > "Computations, architectural drafting, and formal verification tooling were accelerated
  > via AI models (Anthropic Claude/Google Gemini). However, no mathematical claim relies on
  > generative text. All claims are explicitly backed by either Lean 4 kernel verification,
  > exact symbolic Python execution, or hash-pinned literature, with all artifacts publicly
  > available for reproduction."
- **D2.4 ρ = 19 / T = 3:** stays a conditional proposition with explicit hypotheses (A–vS
  operator identification + very-general-member caveat).
  ⚠ *Coordinator tier annotation:* T0's rationale phrase "mathematically proven" is recorded
  here with its tier reading made explicit: the rank result is **Tier B (derived)** — two
  independent exact-symbolic routes (Zarhin E-011; Nikulin complement, S2 G0 certificate,
  LIVE) resting on cited literature — not kernel-checked Tier A. The paper text already
  presents it at exactly this tier; no wording change needed anywhere.
- **D2.5 Internal manuscript:** cited explicitly as a hash-pinned unpublished technical
  report.

**Action taken:** `paper/PLAN.md` §5 updated in Stream 1 with these rulings (see S1 commit
referenced in the cross-links section below).

## D3. WP-E7 LRG catalog — OPTION A (combined LRGpCMASS primary)

eBOSS-only files (174,816 rows, 4,242 deg²) reclassified as secondary/cross-check;
combined LRGpCMASS (377,458 rows, 9,493 deg², SDSS-recommended for z > 0.6 clustering)
fetched as primary. Occupancy ratification proceeds on the combined sample.

⚠ *Coordinator correction to one rationale sentence (decision unaffected):* the combined
sample has ~2.2× the rows (377,458 vs 174,816) and ~2.2× the footprint (9,493 vs
4,242 deg²), but the **surface densities are comparable** (≈39.8 vs ≈41.2 objects/deg²) —
it is not "double the density." The statistical gain is from doubled solid angle/volume
(sample variance) and doubled total counts, at essentially unchanged per-area density; the
per-mode shot-noise level is set by number density and is roughly unchanged. The decision
stands on the correct grounds: more volume, more total objects, and SDSS's explicit
recommendation for this redshift bin.

**Actions taken:** `EBOSS_LRGPCMASS_FILES` + `fetch_eboss_lrgpcmass_clustering()` added to
`scripts/data_fetchers.py` (primary); eBOSS-only block relabeled secondary with the
root-cause note; `PUBLISHED_ROW_COUNTS` in `scripts/fetch_data.py` corrected — LRGpCMASS
compares against 377,458, eBOSS-only against 174,816 (was the mislabeled comparator that
caused the "mismatch"). Fetch executed via `scripts/fetch_data.py` (MANIFEST.md updated by
the script; result recorded in the session brief).

## D4. GitHub tokens

T0 will revoke the classic PATs in-browser and provision a fine-grained repo-scoped PAT.
No agent action.

## Final authorization (standing)

Coordinator authorized to execute: S3 grid-closure logging + WP-E7 fetch (done above);
S1 PLAN.md update (done); continued S2 G1 Route A and S3 desisim/masking executions on
exact mathematical paths. Multi-agent workflow plan for S2/S3 requested as a **design
document only — no implementation** — delivered as
`briefs/MULTI_AGENT_WORKFLOW_PLAN_2026_07_28.md`.

---
Generated-by: Fable 5 (coordinator) | Verified-by: rationale claims checked against
wp_e6_grid_controls_report_2026_07_28.json, emu_predict.py, WP-E7 investigation brief
§2c/§4, paper/PLAN.md this session | Reviewed-by: T0 Y (this document records T0's own ruling)
