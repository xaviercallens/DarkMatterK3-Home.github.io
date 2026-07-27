# (m, f) Grid Definition for WP-E6 v2 — [T0-DELEGATED]

**Date:** 2026-07-27, evening
**Authority:** Xavier Callens (T0), verbal delegation this session: "I give you authority to
propose (m,f) grid value and unit to define so Phase 2 could proceed for real." Marked
**[T0-DELEGATED]** per the PREDICTION.md v1.0-PINNED precedent (2026-07-24). Countermand window
open: any countermand is recorded here with date, and the grid reverts to UNDEFINED.
**Supersedes:** the fabricated placeholder grid {0, 0.1, 0.5, 1, 5 "meV"} × {0, 0.1, 0.5, 1.0}
— see `CORRECTION_FABRICATED_GRID_PROVENANCE_2026_07_27.md`. That grid is void for all
physics purposes; its only residual role is that it exercised the pipeline mechanics.

---

## 1. Unit — decided first, because the last failure was a unit failure

**The mass coordinate is `log10(m_FDM / eV)`, dimensionless.**

Rationale:
- It is the emulator's **native input coordinate** (`param.pkl` field `m`; `predict_pk`'s `m`
  argument). Using it end-to-end means **zero unit conversions anywhere in the pipeline** — the
  class of error that produced the "meV" fabrication (19 orders of magnitude off) becomes
  structurally impossible rather than merely guarded against.
- It is also the source paper's own reporting convention (arXiv:2606.06969 quotes all bounds as
  log₁₀(m_FDM/eV) = −23, −22, −21).
- For literature comparison, the m22 convention (m22 = m / 10⁻²² eV) is provided as a derived
  column in the table below, never as a pipeline input.

## 2. Anchor facts (every number below traces to one of these; all re-verified today)

| # | Fact | Source (primary, checked directly) |
|---|------|-------------------------------------|
| A1 | Trained support: log₁₀(m/eV) ∈ [−22.987, −19.006] | `data/param.pkl`, min/max computed 2026-07-27 evening (210-pt LHS) |
| A2 | Trained support: f ∈ [0.00235, 0.99829]; f = 0 exact via CDM branch (`f ≤ F_EPS = 1e-8` → stage-1 only) | `param.pkl` + `mcmc.py` L49, L155, read directly |
| A3 | Published 95% CL bounds: f < 0.07 @ log₁₀m = −23; f < 0.12 @ −22; f < 0.65 @ −21; **no effective bound for log₁₀m ≳ −20** | arXiv:2606.06969 abstract, fetched via arXiv API 2026-07-27 |
| A4 | Usable redshift: z = 4.2 slice only (Option 1 decision); DESI DR1 has 3,912 QSOs in z ∈ [4.0, 4.4] | `PHASE1_DECISION_2026_07_27.md`; Agent 5 fresh NOIRLab TAP query |
| A5 | The exact endpoints −23.0 / −19.0 and f = 1.0 lie (barely) **outside** A1/A2's sampled range | direct consequence of A1/A2 — grid must not sit on nominal endpoints |

## 3. The grid

**Mass axis — 8 values of log₁₀(m_FDM/eV):**

| log₁₀(m/eV) | m22 equivalent | Role |
|---|---|---|
| −22.9 | 0.126 | Near lower trained edge (inside A1); tightest published bound regime (A3) — maximum discrimination |
| −22.5 | 0.316 | Half-decade ladder through the sensitive region |
| −22.0 | 1.0 | Canonical FDM benchmark; published bound f < 0.12 (A3) |
| −21.5 | 3.16 | Ladder |
| −21.0 | 10 | Published bound f < 0.65 (A3) — the exclusion boundary's steep section |
| −20.5 | 31.6 | Ladder |
| −20.0 | 100 | Paper's own sensitivity edge (A3): bounds die here |
| −19.1 | 794 | **Null control** near upper trained edge (inside A1): published result says no constraint here, so the pipeline must recover ~no suppression signal — a cell that "detects" FDM here indicates a pipeline defect, not physics |

**Fraction axis — 7 values of f_FDM:**

| f | Role |
|---|---|
| 0 | **CDM control column** (exact via A2's F_EPS branch). Structural free check: at f = 0 the prediction is m-independent by construction, so all 8 cells in this column must return byte-identical P1D(k) — any spread is a pipeline bug detector at zero extra cost |
| 0.05 | Below the tightest published bound (0.07 @ −23) — probes inside currently-allowed space |
| 0.10 | Brackets the −22 bound (0.12) from below |
| 0.20 | Between the low-m and mid-m bound regimes |
| 0.35 | Mid-range |
| 0.60 | Just below the −21 bound (0.65) — the steep section of the published exclusion boundary |
| 0.99 | Pure-FDM limit, inside trained support (A2: max 0.99829) — deliberately NOT 1.0 per A5 |

**Grid: 8 × 7 = 56 cells.** Emulator cost is milliseconds per cell (MLP forward pass) — the
factor-2.8 growth over the void 20-cell placeholder costs nothing and buys resolution exactly
where the published exclusion boundary lives (f ∈ [0.05, 0.12] at low m; f ≈ 0.6 at −21).

**Redshift:** z_str = "4.2" only (A4). IGM nuisance parameters (zrei, ha, hs, taueff) are NOT
part of this grid — they are marginalized/profiled per the Phase 2 stats design, which is the
next deliverable and is now unblocked.

## 4. Design principles (why these numbers and not others)

1. **Stay strictly inside trained support** (A1/A2/A5). No cell requires the network to
   extrapolate beyond its LHS sample — the z-axis lesson (3-point extrapolation is not
   physics) applied preemptively to the (m,f) axes.
2. **Sample where the answer changes.** Cell density concentrates around the published 95%
   boundary (A3), because exclusion contours are resolved by cells that straddle them, not by
   uniform coverage of allowed interior.
3. **Built-in controls, zero marginal cost.** The f = 0 column (m-independence check) and the
   −19.1 row (published-null recovery check) turn 15 of the 56 cells into standing pipeline
   diagnostics. This grid ships with its own falsification hooks, per Stream 3 house style.
4. **No cell is load-bearing for a physics claim yet.** This grid defines where the forward
   model is evaluated. Comparison against any observational dataset remains gated behind the
   Phase 3 PREDICTION v2 pin (CLAUDE.md rule 1) — unchanged by this document.

## 5. Status and countermand

- Effective immediately as the **working grid** for Phase 2 (Stats Design) under delegated
  authority. The git commit introducing this file is its hash-anchor, per the PREDICTION.md
  pin convention.
- Xavier may countermand or amend any value; the countermand gets recorded in this section
  with date, and downstream Phase 2 work re-runs from the amended grid (cheap by design).
- At the eventual PREDICTION v2 pin (Phase 3), this grid — as then amended — freezes for real,
  under the full pin protocol.

*Countermand log: (empty)*
