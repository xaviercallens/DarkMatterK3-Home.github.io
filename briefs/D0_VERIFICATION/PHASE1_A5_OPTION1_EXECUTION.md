# Phase 1 — Agent 5: Option 1 Execution (DESI z=4.2 Verification + Emulator Landscape)

**Date:** 2026-07-27
**Scope:** `briefs/D0_VERIFICATION/PHASE1_DECISION_2026_07_27.md` items 1 and 2.
**Working dir:** `phase1_work/agent5_option1_execution/`
**Web/TAP calls used:** 4 (1 total-count sanity, 1 z>3.5 count, 1 z∈[4.0,4.4] count,
1 bulk pull of z∈[3.5,4.6] rows for histogram) — well under the 10-call budget.
**Provenance:** Generated-by: Sonnet (Agent 5) | Verified-by: not yet reviewed |
Reviewed-by: T0 N

---

## Task A — DESI DR1 z=4.2 usability (real data)

### What was wrong with the cached file

`data/raw/desi_dr1_noirlab/qso_zpix_photometry_2026_07_27.csv` (WP-E7, 895,372 rows,
all z<2.1) was capped by a hardcoded `zmin=0.8, zmax=2.1` cut, confirmed directly in
`data/raw/desi_dr1_noirlab/fetch_manifest_draft.json` (`"QSO": {"zmin": 0.8, "zmax": 2.1"}`)
and `fetch_log.txt`. That is the standard DESI BAO/LSS QSO-tracer redshift range —
WP-E7's own stated purpose (BAO-tracer photometry cross-match testing), not a
statement about DESI's redshift reach. The absence of z>2.1 rows in that file is a
query-scope artifact, not evidence about DESI's data.

### Fresh query (this pass)

Ran directly against `desi_dr1.zpix` (NOIRLab TAP, pyvo 1.9.1, anonymous sync),
`survey='main' AND zwarn=0 AND spectype='QSO'`, no upper z cut:

| Quantity | Count |
|---|---|
| Total QSO-spectype rows (main, zwarn=0) | 1,600,854 |
| z > 3.5 | 21,439 |
| z ∈ [4.0, 4.4] | 3,912 |
| z ∈ [4.1, 4.3] (±0.1 of the emulator's 4.2 anchor) | 1,867 |

Histogram, z∈[3.5,4.6], 0.1-wide bins (n = 19,917 rows pulled):

| z bin | n | z bin | n |
|---|---|---|---|
| 3.5–3.6 | 4071 | 4.1–4.2 | 1066 |
| 3.6–3.7 | 3448 | 4.2–4.3 | 801 |
| 3.7–3.8 | 3054 | 4.3–4.4 | 540 |
| 3.8–3.9 | 2682 | 4.4–4.5 | 398 |
| 3.9–4.0 | 2073 | 4.5–4.6 | 279 |
| 4.0–4.1 | 1505 | 4.6–4.7 | 0 |

Raw pulled rows: `phase1_work/agent5_option1_execution/desi_dr1_qso_z_3.5_4.6_fresh_query.csv`.
Full query log/summary: `phase1_work/agent5_option1_execution/task_a_desi_highz_qso_results.json`.

### Verdict

DESI DR1 has a real, non-trivial QSO population near z=4.2 — thousands of objects, not
zero and not a handful. The count falls off smoothly and steeply with z (roughly
halving every Δz≈0.4-0.5 in this range), which is the expected shape of the QSO N(z)
luminosity-function decline at high z, not evidence of an artificial cutoff.

**Caveat, stated plainly:** this count is *spectroscopically confirmed QSOs by redshift*,
not *forest sightlines usable for a Lyman-α P1D measurement*. A P1D-ready sample needs
further per-spectrum cuts (continuum S/N in the forest region, BAL/DLA flags, forest
wavelength coverage at the target k range) that were not applied here — that is a
Phase-2-scale task, not part of this verification. So: the z≈4.2 slice is **usable in
the sense of "DESI has real, sizeable statistics there"** (thousands of QSOs, not an
empty bin) — it is **not yet verified as P1D-measurement-ready** at that specific
z-slice (that requires the forest-quality cuts noted above, out of scope here).

---

## Task B — Emulator forward-model landscape at z=4.2

**This step computes the emulator's own P1D(k) predictions across the frozen 20-cell
(m, f) grid — it is model exploration, not a project result** (per
`PHASE1_DECISION_2026_07_27.md` item 3 and Stream 3 CLAUDE.md rule 1).

### Grid units — a citation could not be verified, flagged rather than silently fixed

`phase1_work/agent2_sweep/fallback_sweep.py` and
`briefs/D0_VERIFICATION/PHASE1_A2_SWEEP_SCAFFOLD.md` label the grid's `m` axis
"axion mass, meV" and attribute it to "K3_CRITERIA.md v0.1 frozen spec." Grepping
`K3_CRITERIA.md` directly (for `mass`, `axion`, `FDM`, `meV`) returns **no matches** —
that file contains K3-geometry selection criteria (mirror maps, Kodaira fibers,
Sym² structure), not a dark-matter mass grid. The citation could not be verified in
this pass. Taken literally as milli-eV, the grid values `[0, 0.1, 0.5, 1, 5]` map to
`log10(m_FDM/eV) ≈ [-∞, -4, -3.3, -3, -2.3]` — about 19 orders of magnitude outside
the emulator's trained domain (`log10(m/eV) ∈ [-22.99, -19.0]`) and outside the
physical mass range associated with "fuzzy" dark matter in the cited literature.

The only interpretation landing inside the emulator's trained domain is the standard
FDM-literature convention **m22 = m_FDM / (1e-22 eV)**. This script adopts that
reinterpretation explicitly (documented in
`phase1_work/agent5_option1_execution/task_b_emulator_landscape.py` module docstring)
rather than assuming it silently. **This is a flagged assumption, not a verified
fact — T0 should confirm or correct the grid's intended units before this landscape
is used for anything beyond interpretability exploration.**

### Grid coverage: 17/20 cells computed, 3 flagged undefined

- **5 cells** at f=0 (any m22): all four identical CDM-only P1D(k) curves confirmed
  numerically equal (`predict_pk`'s CDM branch does not take m or f as inputs at all
  when f≤F_EPS — verified from the emulator's own code, not assumed).
- **12 cells**: m22∈{0.1,0.5,1,5} × f∈{0.1,0.5,1.0} — computed via
  `predict_pk(log10(m22)-22, f, zrei=10.5, ha=2.0, hs=0.0, taueff=1.0, z_str="4.2")`.
- **3 cells flagged UNDEFINED, not computed**: m22=0 with f∈{0.1,0.5,1.0}. log10(0) has
  no value; m22=0 is not a point in the emulator's Latin-Hypercube training design.
  These were **not** silently mapped to CDM or to a domain edge.
- m22=0.1 → log10(m/eV) = −23.0, just outside the trained lower bound (−22.987) by
  0.013 dex — computed and reported, flagged `in_trained_domain=False` (a mild
  extrapolation, not a hard out-of-domain call).

Full results (all 17 P1D(k) arrays, k-bins, fractional differences):
`phase1_work/agent5_option1_execution/task_b_emulator_landscape_results.json`.

### Fractional suppression relative to CDM, ranked (mixed cells only)

| m22 | f | log10(m/eV) | in domain | max supp. | at k [s/km] | supp @ k_min | supp @ k_max |
|---|---|---|---|---|---|---|---|
| 0.1 | 1.0 | −23.0 | No (extrap.) | 86.7% | 0.0251 | −24.9%* | 59.4% |
| 0.5 | 1.0 | −22.30 | Yes | 74.1% | 0.0501 | −6.3%* | 35.1% |
| 0.1 | 0.5 | −23.0 | No (extrap.) | 69.1% | 0.0398 | −10.2%* | 47.5% |
| 1 | 1.0 | −22.00 | Yes | 63.1% | 0.0501 | −0.8%* | 25.9% |
| 0.5 | 0.5 | −22.30 | Yes | 55.4% | 0.0501 | −1.9%* | 29.0% |
| 1 | 0.5 | −22.00 | Yes | 42.8% | 0.0501 | +0.7% | 20.4% |
| 0.1 | 0.1 | −23.0 | No (extrap.) | 21.3% | 0.0501 | −0.8%* | 15.9% |
| 5 | 1.0 | −21.30 | Yes | 19.8% | 0.0631 | +5.0% | +2.9% |
| 0.5 | 0.1 | −22.30 | Yes | 13.5% | 0.0501 | +0.5% | +8.7% |
| 1 | 0.1 | −22.00 | Yes | 8.6% | 0.0501 | +0.9% | +5.5% |
| 5 | 0.5 | −21.30 | Yes | 5.7% | 0.0501 | +3.1% | −0.6%* |
| 5 | 0.1 | −21.30 | Yes | 0.8% | 0.0063 | +0.8% | −0.2%* |

\* negative "supp" = P1D(k) *enhanced* relative to CDM at that endpoint, not suppressed
(the sign flips within a cell's own k-range for several rows).

### Interpretation (model behavior only — see boundary statement below)

- **Suppression scales with both lower mass and higher f**, as expected qualitatively
  for a fuzzy-dark-matter-type mechanism (we state this as a description of the
  emulator's trained behavior on this grid, not a physics derivation — the emulator is
  an external, cited surrogate for hydrodynamic simulations, not a result of this
  project's own modeling).
- The single largest fractional deviation on the computed grid is **m22=0.1, f=1.0:
  86.7% suppression at k≈0.025 s/km**, but the same cell shows a sign flip to ~25%
  *enhancement* at the smallest k bin — the largest-amplitude cell is not monotonic
  across the k range.
- Across all 12 mixed cells, **maximum suppression consistently peaks at intermediate
  k (≈0.025–0.06 s/km)**, not at the smallest or largest k probed (k spans
  0.0063–0.1995 s/km) — the suppression is not simply "more at small scales," it has
  a k-dependent shape with a peak, mirrored across nearly all 12 cells regardless of
  (m,f) values.
- At f=0.1 (the smallest admixture on the grid), fractional deviations from CDM stay
  under ~21% for all masses tested; deviations only exceed 50% once f≥0.5.
- **As a forward-model statement about the emulator's own trained behavior** (not a
  statement about whether DESI data could detect or exclude any of this — that
  requires the comparison step this pass explicitly did not perform): the spread
  across the (m,f) grid is large in relative terms (order unity at several cells),
  meaning the emulator's surrogate model treats this parameter range as producing
  substantially different P1D(k) shapes, not a near-degenerate family. Whether that
  spread survives real observational uncertainties and systematics is a separate,
  ungated question left for Phase 2/3.

---

## Explicit confirmation: no data-comparison statistic was computed

- `task_b_emulator_landscape.py` never imports, opens, or references
  `lya-mfdm/data/lya_data.pkl` (the emulator's bundled Boera et al. 2019 observational
  data) or any DESI file.
- No `chi2`, `Cov_inv`, `loglike`, or goodness-of-fit quantity appears anywhere in
  `task_b_emulator_landscape.py` — grepped directly to confirm, not just asserted.
- `task_a_desi_highz_qso_query.py` only counts/pulls redshift values from DESI's
  catalog; it does not touch the emulator, does not compute P1D from DESI data, and
  performs no comparison between the two tasks' outputs.
- Both scripts wrote outputs only to `phase1_work/agent5_option1_execution/` (this
  agent's own working dir) — `data/raw/`, `PREDICTION.md`, and all other repo files
  were not touched, consistent with the task's explicit restrictions.

This is model exploration for interpretability (Task B) and a real-data adequacy
check on QSO counts only (Task A) — neither constitutes, nor should be read as, a
project result or a step toward one under the current (unpinned) `PREDICTION.md`.

---

## What Phase 2/3 would need to do next (once PREDICTION v2 is pinned)

1. **Resolve the grid-units flag above with T0** before any downstream use — confirm
   whether the frozen (m,f) grid's `m` axis is m22, literal meV, or something else;
   this changes which physical mass range every cell in this landscape actually
   represents.
2. **Build a P1D-ready DESI Lyα forest sample near z≈4.2** — apply continuum S/N,
   BAL/DLA, and forest-coverage cuts to the QSO catalog counted in Task A; this pass
   only confirmed the raw QSO population, not a science-ready forest sample.
3. **Design the statistic** (Q3 from `WP_E6_V2_PROPOSAL_LYA_P1D_2026_07_27.md`,
   currently the live open question per MEMORY.md) — decide what comparison quantity
   (binned P1D chi2, power-spectrum ratio, other) will be used once comparison is
   permitted.
4. **Pin PREDICTION v2** specifying the exact (m,f) cells, z-slice, statistic, and
   pass/fail criteria in advance, per the pre-registration gate (rule 1).
5. **Only then** write real-data comparison code — at which point this landscape's
   17 P1D(k) arrays become candidate model predictions to compare against the
   P1D-ready DESI sample from step 2, and the DESI counts from Task A inform whether
   the statistical power at z≈4.2 is adequate for whatever test v2 specifies.

---

**Files produced (all under `phase1_work/agent5_option1_execution/`, none committed):**
- `task_a_desi_highz_qso_query.py`, `task_a_desi_highz_qso_results.json`,
  `desi_dr1_qso_z_3.5_4.6_fresh_query.csv`
- `task_b_emulator_landscape.py`, `task_b_emulator_landscape_results.json`

Generated-by: Sonnet (Agent 5) | Verified-by: not yet reviewed | Reviewed-by: T0 N
