# WP-E6b — Lyman-α P1D Adequacy Pre-Flight (Mixed-Fraction FDM vs. DESI DR1's Published P1D Precision)

**Date:** 2026-07-27

**Executor:** Stream 3 agent, under `briefs/T0_DECISIONS_2026_07_27.md` **D-e**
(commit `c4171f0`), which re-scoped the WP-E6 statistic from DES-Y6 broadband
convergence to the DESI DR1 Lyman-α 1D flux power spectrum after the DES-Y6
adequacy negative was filed, and required this pre-flight to precede any
WP-E6 v2 proposal drafting.

**Tag: `ENGINEERING`** — a linear-theory forward model confronted with the
*published measurement uncertainties* of a released data product, in the
WP-E7 labeling lineage (`docs/WP_E7_DESI_RESOLVABILITY_PREFLIGHT_2026_07_27.md`).
Direct precedent: `docs/WP_E6_SYNTHETIC_ADEQUACY_PREFLIGHT_2026_07_27.md` —
same discipline, different observable.

⚠️ **NOT `TEST`, NOT `FIT`, NOT `SANDBOX-EXPERIMENTAL`.** The published
central P1D values are never used as a fit target; only the published
per-bin error bars enter the statistic. This document tests no pre-registered
prediction, makes no physics claim, falsifies nothing, and is **not a
forecast**. It answers one mechanical question: *under an explicitly
optimistic linear-theory forward model, is the Lyman-α P1D statistic in
principle capable of separating a mixed ultralight component from f = 0 at
DESI DR1's own published precision?* Its fidelity requires ratification (or
replacement) at `PREDICTION_v2` pin time; nothing here may be cited as an
exclusion, a bound, or a sensitivity projection.

Module: `pipeline/wp_e6b_lya.py`. Script:
`scripts/wp_e6b_lya_adequacy_preflight.py`. Artifact:
`data/derived/wp_e6b_lya_adequacy_preflight_2026_07_27.json`. Data:
`data/literature/desi_dr1_lya_p1d_2026_07_27.csv` (provenance +
SHA256 in `data/MANIFEST.md`). Tests: `pipeline/tests/test_wp_e6b_lya.py`
(**34 tests**; suite for this WP and its two dependencies —
`test_wp_e6b_lya.py` + `test_wp_e6_sweep.py` + `test_cosmology.py` — is
**70/70 passing**).

---

## 0. Headline

> **Under an explicitly optimistic linear-theory P1D-ratio forward model,
> confronted with DESI DR1's own published per-bin uncertainties across the
> 755 (k, z) bins inside the paper's recommended validity range, 221 of the
> 260 (m, f) grid cells — m ∈ [10⁻²², 10⁻¹⁹] eV, f ∈ [0.05, 1.00] — reach
> σ_equiv ≥ 2 against f = 0 *and* remain open under the published
> mixed-fraction landscape. This is an ADEQUACY answer only — "the statistic
> is not intrinsically precision-starved on this grid" — and the same proxy,
> evaluated at the two masses where Liu, Gong & Zhou 2026 publish a 95%
> mixed-fraction bound, assigns σ_equiv ≈ 37 and ≈ 99 where an
> emulator-grade analysis places its limit: it is optimistic there by
> **18.5×** and **49.3×** relative to this pre-flight's own 2σ threshold.
> The 221 figure is therefore a statement about the observable's headroom,
> NOT a count of cells a real DESI Lyman-α analysis would reach.**

Contrast with the WP-E6 DES-Y6 filing, which returned an honest negative
(best cell σ_equiv ≈ 0.49; ≈ 1.48 even at full sky). The two pre-flights
disagree by ~2.5 orders of magnitude in σ_equiv at the same best-case cell,
and §5 argues that gap is real in direction but heavily inflated in size.

---

## 1. What was computed

### 1.1 The observable: a P1D ratio

`R(k_∥, z; m, f) = P1D_mixed / P1D_ΛCDM`, in **linear theory**, via the
standard real-space (Kaiser-free) 1D projection of an isotropic 3D power
spectrum:

```
P1D(k_∥) = (1/2π) ∫_{k_∥}^{∞} P3D(k) k dk
```

Taking the **ratio** cancels the unknown flux bias and, at first order, much
of the IGM modeling — the load-bearing engineering choice this WP is built
around, and simultaneously the reason its answer is optimistic (§5).

The 3D inputs are reused from `pipeline/wp_e6_sweep.py` without
reimplementation: Eisenstein & Hu 1998 no-wiggle ΛCDM shape (σ8-normalized,
Planck18); Hu, Barkana & Gruzinov 2000 pure-FDM transfer `T_F(k)`; and that
module's **linear-interpolation mixed-fraction ENGINEERING APPROXIMATION**
`S(k; m, f) = 1 − f·(1 − T_F(k;m)²)`, whose full caveat (it is *not* a
solved two-component perturbation calculation) carries over unchanged and is
restated in §5.

### 1.2 Linear-in-f closed form

Because `S` is linear in f and the projection integral is linear in P3D, the
ratio has an exact closed form:

```
R(k_∥; m, f) = 1 − f·ρ(k_∥; m),   ρ = I_supp / I_ΛCDM ≥ 0
```

so `Δχ²(m, f) = f²·Δχ²_shape(m)` exactly, computed once per mass. Two
required sanity properties (R → 1 as f → 0; R non-increasing in f) fall out
of this structure rather than being imposed. The closed form is **verified
against direct numerical integration**, not assumed
(`TestClosedFormMatchesDirectIntegration`, 36 (k, m, f) combinations, rel.
err < 10⁻⁶).

### 1.3 Unit conversion and validity cuts

DESI's P1D table is in velocity units; `k_comoving = k_velocity · H(z)/(1+z)`
(`pipeline.cosmology.hubble_kms_mpc`, Planck18, added this WP with three
independent tests including a manual-Friedmann cross-check out to z = 4.4).
Because the conversion factor moves with z, the same tabulated k_∥ [s/km]
samples a *different* point of the (comoving-fixed) suppression curve in
each of DESI's 12 redshift bins.

Validity cuts are the **paper's own recommendation** (arXiv:2505.07974
**§4.1**, "recommended k cuts" — section number re-verified against the
arXiv HTML during this audit, correcting an earlier "§4.3" in
`data/MANIFEST.md` and the module docstring). The paper's words:
`k > 10⁻³ s km⁻¹ due to continuum error contamination`, and
`k < 0.5π/R_z, where R_z ≡ cΔλ_DESI/(1+z)λ_Lyα and Δλ_DESI = 0.8 Å, based
on a conservative estimate of the size of the spectrograph resolution
correction`. Bins outside the range are **dropped entirely** — not
down-weighted, not imputed. **755 of the 1020 tabulated bins survive**; both
arms of the cut are checked to actually remove bins, so the "restricted to
the paper's validity range" claim is not vacuous
(`test_both_validity_cut_arms_actually_exclude_bins`).

### 1.4 The statistic

```
Δχ²(m, f) = Σ_{valid (k,z)} [ (R(k,z;m,f) − 1) / σ_rel(k,z) ]²,
σ_rel = e_total / P1D  (published fractional uncertainty)
```

reported as `σ_equiv = √Δχ²`. Same deliberately-rough combined-significance
convention as WP-E6 (exact for one d.o.f.; no inversion of the multi-d.o.f.
χ² tail) — adequate for *ordering* cells, not for a publication-grade
significance.

**Grid:** m ∈ logspace(10⁻²², 10⁻¹⁹ eV, 13) × f ∈ {0.05, …, 1.00} (20) =
260 cells — deliberately identical to WP-E6's, so the two pre-flights are
comparable cell-for-cell.

---

## 2. The (m, f) adequacy table

`σ_shape(m)` is the value at f = 1; every cell is `σ_equiv = f · σ_shape(m)`.
"Published pure-FDM (f=1) status" uses the **corrected** exclusion direction
(published FDM mass limits are *lower* limits — see the correction note in
`docs/WP_E6_SYNTHETIC_ADEQUACY_PREFLIGHT_2026_07_27.md`, a direction bug
found and fixed during this audit).

| m (eV) | σ_shape (at f=1) | smallest f reaching 2σ | published pure-FDM (f=1) status |
|---|---|---|---|
| 1.000×10⁻²² | 307.65 | 0.05 | EXCLUDED |
| 1.778×10⁻²² | 259.30 | 0.05 | EXCLUDED |
| 3.162×10⁻²² | 217.65 | 0.05 | EXCLUDED |
| 5.623×10⁻²² | 182.02 | 0.05 | EXCLUDED |
| 1.000×10⁻²¹ | 151.69 | 0.05 | EXCLUDED |
| 1.778×10⁻²¹ | 126.02 | 0.05 | EXCLUDED |
| 3.162×10⁻²¹ | 104.38 | 0.05 | EXCLUDED |
| 5.623×10⁻²¹ | 86.22 | 0.05 | EXCLUDED |
| 1.000×10⁻²⁰ | 71.04 | 0.05 | EXCLUDED |
| 1.778×10⁻²⁰ | 58.39 | 0.05 | EXCLUDED |
| 3.162×10⁻²⁰ | 47.89 | 0.05 | EXCLUDED |
| 5.623×10⁻²⁰ | 39.19 | 0.10 | EXCLUDED |
| 1.000×10⁻¹⁹ | 32.01 | 0.10 | EXCLUDED |

Every mass in this grid is pure-FDM excluded at f = 1 (the tightest bound
covering the whole grid is May, Dalal & Kravtsov 2025's 8×10⁻¹⁸ eV UFD
threshold, three decades above the grid's own ceiling), so the f = 1.00
column is never "open" and the open region is entirely f < 1.

Counts (all from the artifact, `TestFiledArtifact`):

| quantity | count (of 260) |
|---|---|
| cells reaching σ_equiv ≥ 2 | 258 |
| cells genuinely open per the published landscape | 223 |
| **decisive = both** | **221** |

The two open-but-unreachable cells are (5.623×10⁻²⁰ eV, f = 0.05) and
(10⁻¹⁹ eV, f = 0.05). Smallest σ_equiv among decisive cells: **2.39**;
largest: **246.3**.

**Where the openness comes from — read this before quoting 221.** Of the 221
decisive cells, **207 are open only because no published mixed-fraction
bound in this repo's landscape survey reaches their mass**
(`governing_constraint: "none published (unconstrained)"`). Just 14 are open
against an actual published mixed-fraction constraint: 12 below Liu, Gong &
Zhou 2026's f < 0.65 at m = 10⁻²¹ eV, and 2 below their f < 0.12 at
m = 10⁻²² eV. "Unconstrained" here means *absent from
`docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md` §4*, which is a statement about
this repo's survey of the literature — not evidence that no published
mixed-fraction constraint exists at those masses.

---

## 3. The optimism calibration (why 221 is not a sensitivity claim)

The proxy can be checked against the published landscape at the two masses
where a mixed-fraction bound exists. A forward model of comparable fidelity
to the one behind those bounds would put the published limit near this
pre-flight's own decision threshold (σ_equiv = 2). It does not:

| m (eV) | published 95% bound | this proxy's σ_equiv at that f | overstatement vs. 2σ |
|---|---|---|---|
| 1.000×10⁻²² | f_FDM < 0.12 (Liu, Gong & Zhou 2026) | 36.9 | **18.5×** |
| 1.000×10⁻²¹ | f_FDM < 0.65 (Liu, Gong & Zhou 2026) | 98.6 | **49.3×** |

This is computed in the artifact
(`optimism_calibration_vs_published_anchors`), not asserted in prose, and is
pinned by `test_optimism_calibration_is_present_and_exceeds_unity`. It is a
diagnostic **of this proxy** — it makes no claim about the published
analysis, and the identification of a one-sided 95% CL with 2σ_equiv is
deliberately generous (a 95% one-sided limit is nearer 1.64σ, which would
make the ratio larger).

**Reading:** the linear-theory ratio proxy overstates reachability by
roughly one to two orders of magnitude at the only two points where an
independent, emulator-grade answer is available. Applying that same factor
to the rest of the grid is not licensed — the overstatement is itself
mass-dependent, and grows by a factor of ~2.7 across just one decade in m —
but it is enough to say the 221 count carries no sensitivity content.

---

## 4. What this pre-flight is, in one line each

- **It is:** an adequacy check — the DESI DR1 P1D published precision is
  fine enough, and the FDM suppression signature large enough in the
  surviving (k, z) bins, that the statistic is not dead on arrival for this
  grid, unlike the DES-Y6 broadband convergence route.
- **It is not:** a comparison (no published central value is used as a
  target), a forecast (no realistic modeling or nuisance marginalization), a
  bound, an exclusion, or a claim that 221 cells are reachable in practice.

---

## 5. What would be required before ANY real comparison

Each item below degrades sensitivity relative to a bias-free linear-theory
ratio; none is attempted here; all of the published bounds this document
cites required the first two.

1. **Hydrodynamic-simulation-calibrated modeling.** Lyman-α P1D is not a
   linear observable. Every published FDM/mixed bound in this mass range
   (Rogers & Peiris 2021; Liu, Gong & Zhou 2026) is built on a
   hydro-simulation **emulator** spanning cosmology × IGM thermal history.
   A linear-theory ratio has no such calibration, and the nonlinear
   regeneration of small-scale power under gravitational collapse — which
   Hu, Barkana & Gruzinov 2000 flag themselves — cuts directly against the
   suppression this statistic is built on.
2. **Marginalization over IGM nuisance parameters.** Mean flux, the
   temperature–density relation (T₀, γ), the pressure/filtering scale, and
   thermal Doppler broadening are all fit or marginalized in the real
   analyses. The ratio construction cancels them only at first order and
   only if they are FDM-independent, which they are not (the IGM thermal
   history responds to the modified collapse history). Marginalization also
   induces degeneracies with the suppression shape itself — the dominant
   sensitivity loss.
3. **The mixed-fraction transfer function.** `S(k;m,f)` is a linear
   interpolation between the f=0 and f=1 endpoints, not a solved
   two-component (CDM + ultralight) perturbation calculation. This is the
   single largest physics simplification and the first thing to replace.
4. **The full covariance, not its diagonal.** Only `e_total = √diag(COV)` is
   used. The published covariance has off-diagonal structure (correlated
   systematics, continuum, resolution) that a diagonal Δχ² ignores, and
   ignoring it inflates significance.
5. **Metal, DLA, and continuum systematics as free parameters**, rather than
   accepting the paper's SB1-subtracted, continuum-corrected central
   product as a clean measurement.
6. **z-dependent suppression.** Redshift enters only through the k-unit
   conversion; the FDM Jeans scale's own redshift evolution is not modeled
   (inherited unchanged from `wp_e6_sweep.py`).
7. **A pre-registered `PREDICTION` v2 amendment before any real-data touch**
   (CLAUDE.md rule 1 and rule 5). No pipeline may depend on a single
   predicted scalar mass — none exists under F5b — and every output would be
   labeled exclusion/FIT, never `TEST`, until pinned.

---

## 6. Contrast with the WP-E6 DES-Y6 negative

| | WP-E6 (DES-Y6 convergence) | WP-E6b (DESI DR1 Lyman-α P1D) |
|---|---|---|
| observable | broadband κ band powers, 6 ℓ-bands | P1D(k_∥) ratio, 755 (k, z) bins |
| error source | Knox Gaussian, shape-noise dominated, from published survey params | published per-bin P1D uncertainties |
| best cell | σ ≈ 0.486 (m = 10⁻²², f = 1) | σ ≈ 307.7 (same cell) |
| full-sky variant | σ ≈ 1.484 — still under 2σ | n/a |
| decisive cells | **0 of 260** | 221 of 260 (optimistic proxy) |
| verdict filed | honest negative; WP stopped per its own stop condition | adequacy not refuted; see §7 |

Both pre-flights are optimistic relative to a real analysis, so the DES-Y6
negative is the more robust of the two results: a route that cannot reach 2σ
*even under a favorable toy model* is genuinely closed, whereas a route that
reaches 2σ under a favorable toy model has only failed to be closed. The
direction of the gap is consistent with why the strongest published bounds
in this mass range come from Lyman-α forest power rather than broad
cosmic-shear band powers — but §3 records that the *magnitude* of this
pre-flight's σ values cannot be taken at face value.

---

## 7. The explicit T0 ask (Xavier)

WP-E6b returns **adequacy not refuted** — the opposite outcome to WP-E6's
filed negative, and therefore a decision point rather than an automatic
stop. Two options:

- **(A) PROCEED** — authorize drafting a **WP-E6 v2 proposal** built on the
  DESI DR1 Lyman-α P1D statistic. Scope of that draft would be the §5 list
  (emulator-grade or emulator-anchored modeling, IGM nuisance
  marginalization, full covariance, a real mixed-fraction transfer
  function), plus the `PREDICTION` v2 pre-registration text, with no
  real-data comparison executed before the pin. Cost is substantial: items
  §5.1–§5.3 are not small refinements of what exists here, and an honest
  version of this WP would likely need to consume a published emulator
  rather than build one.
- **(B) STOP** — file WP-E6b as the terminal artifact of the WP-E6 line, on
  the ground that §3's 18.5×–49.3× overstatement means this pre-flight has
  not exhibited headroom that survives realistic modeling, and that the
  program's Lyman-α capability would in any case be bounded by the
  published bounds it would be re-deriving.

**A third question is embedded in either choice** and should be answered
first: §2 records that 207 of the 221 decisive cells are open only because
`docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md` §4 lists no mixed-fraction
bound at their masses. Whether that reflects the literature or only this
repo's survey of it is unverified. A targeted literature check on published
mixed-fraction (f_FDM) constraints above 10⁻²¹ eV would change the openness
overlay materially, and is cheap relative to either option above.

No option is exercised here. This WP stops at the filing.

---

## 8. Audit record (this session)

`pipeline/wp_e6b_lya.py` and its tests were audited end-to-end before this
report was written. Findings:

1. **The filed headline had no checker.** `run_grid` — the function that
   produces `n_decisive_cells` — was not invoked by any test. Fixed:
   `run_grid` now accepts an injected table and grid overrides, and
   `TestEndToEndGridControls` drives it under six injected conditions.
2. **One negative control could not fail.** The original
   "scrambled sigma under a null signal" test computed `sum((zeros/σ)²)`
   inside the test itself, with no module code between the injected null and
   the asserted zero. It was **deleted** and replaced by controls that
   inject the same failure modes through `run_grid`.
3. **Controls added** (each one fails under deliberate mutation of
   `run_grid` — an `is_decisive = openness["open"]` mutation and a
   "published errors ignored" mutation were each caught by exactly the
   intended tests): zero-suppression injection → 0 decisive cells;
   errors inflated ×10⁶ → 0 decisive cells; errors shrunk ×10⁻⁶ → decisive
   count rises to exactly the open-cell count (pinning the two criteria as
   independent); scrambled error-to-bin correspondence → statistic must
   change; all bins outside the validity range → fails closed at zero;
   inert-cut guard on the real table.
4. **Filed-artifact tests added:** headline internal consistency (221 of
   260, 755 of 1020 bins), the linear-in-f closed form as stored, and a
   full-resolution recomputation of the m = 10⁻²² eV column from the code.
5. **Published-bound directions verified.** Pure-FDM limits are *lower*
   limits on mass (excluded region = below threshold); mixed-fraction
   anchors are *upper* limits on f (open region = below the bound). The
   pure-FDM direction was inverted in `scripts/wp_e6_adequacy_preflight.py`
   and in two of its tests — found and fixed in this session's work, with a
   correction note appended to the WP-E6 report.
6. **Validity cuts verified against the source.** The paper's recommended
   cuts were re-fetched and quoted verbatim (§1.3); the section number was
   **§4.1**, not the "§4.3" previously recorded — corrected in
   `data/MANIFEST.md` and the module docstring.
7. **Optimism calibration added** (§3), so the report's central caveat is a
   computed artifact field rather than a prose assertion.

---

## 9. Reproducibility

```
python3 scripts/wp_e6b_lya_adequacy_preflight.py       # ~4 min
python3 -m pytest pipeline/tests/test_wp_e6b_lya.py \
                 pipeline/tests/test_wp_e6_sweep.py \
                 pipeline/tests/test_cosmology.py -q   # 70 passed
```

---

Generated-by: Claude Opus 5 (Stream 3 agent, WP-E6b) | Verified-by:
`pipeline/tests/test_wp_e6b_lya.py` (34 tests: known-answer P1D projection
against an analytic power-law result, the linear-in-f closed form
cross-checked against direct numerical integration, R→1 as f→0, monotonicity
in f, unit-conversion round-trip, six end-to-end negative controls on
`run_grid` each of which fails under deliberate mutation, filed-artifact
consistency and one full-resolution recomputation, and published-bound
direction/lookup checks) + arXiv source re-fetch for the validity cuts and
the published-bound directions | Reviewed-by: pending T0 (Xavier)
