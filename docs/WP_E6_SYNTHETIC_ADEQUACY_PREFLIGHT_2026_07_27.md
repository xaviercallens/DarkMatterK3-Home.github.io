# WP-E6 — Synthetic Adequacy Pre-Flight (Mixed-Fraction FDM vs. a DES-Y6-like Survey)

**Date:** 2026-07-27

**Executor:** Sonnet (Stream 3 agent), under
`briefs/T0_DECISIONS_2026_07_27.md` D-b (mixed-fraction framing, T1-delegated
ruling) and D-c (DES Y6 as the lensing product), following the precondition
in `briefs/WP_E6_PHENO_SWEEP_PROPOSAL_2026_07_27.md` §3.2 ("data adequacy
pre-flight ... BEFORE any real-data touch").

**Tag: `ENGINEERING`** — synthetic-data arithmetic (a Fisher/Delta-chi²
distinguishability computed entirely on a toy forward model), in the WP-E7
labeling lineage (`docs/WP_E7_DESI_RESOLVABILITY_PREFLIGHT_2026_07_27.md`).

⚠️ **NOT `TEST`, NOT `FIT`, NOT `SANDBOX-EXPERIMENTAL`.** No real data is
read anywhere in this work package (CLAUDE.md rule 1 — no real-data
comparison code before `PREDICTION.md` carries a v2 pin). This document
makes no physics claim, tests no pre-registered prediction, and falsifies
nothing. It answers one mechanical question: **under a specific, explicitly
approximate forward model, which (mediator mass, ultralight fraction) cells
could in principle be told apart from "no ultralight component" by a survey
with DES Y6's noise properties** — a pre-flight, not a result. Its fidelity
requires ratification (or replacement) at `PREDICTION_v2` pin time; nothing
here should be cited as an exclusion, a forecast, or a derived bound.

Module: `pipeline/wp_e6_sweep.py` (forward model). Script:
`scripts/wp_e6_adequacy_preflight.py`. Artifact:
`data/derived/wp_e6_adequacy_preflight_2026_07_27.json`. Tests:
`pipeline/tests/test_wp_e6_sweep.py` (17 tests, all passing).

---

## 1. What was computed

### 1.1 Matter-power suppression (mixed ultralight fraction)

- **ΛCDM shape:** Eisenstein & Hu 1998 no-wiggle ("zero-baryon") transfer
  function (ApJ 496, 605; arXiv:astro-ph/9709112), their eqs. (26), (28),
  (29), (30), (31) — transcribed and equation-number-verified against the
  arXiv PDF this session, not reproduced from memory. Amplitude fixed by the
  standard σ8-normalization convention (Planck 2018 σ8 = 0.8102, ns = 0.9665,
  Ωb h² = 0.02242, flat ΛCDM H0 = 67.66, Ωm = 0.30966 — the same Planck18
  cosmology `pipeline/cosmology.py` already uses elsewhere in this repo, a
  fiducial choice, not a fit to anything in this program).
- **Pure-FDM (f=1) suppression:** Hu, Barkana & Gruzinov 2000 (PRL 85, 1158;
  arXiv:astro-ph/0003365) eqs. (8)–(9): `T_F(k) = cos(x³)/(1+x⁸)`, `x = 1.61
  m22^(1/18) k/k_Jeq`, `k_Jeq = 9 m22^(1/2) Mpc⁻¹`, `m22 = m / 1e-22 eV`.
  `P_FCDM(k) = T_F(k)² P_CDM(k)`. Verified against the paper's own stated
  "half-power point" `k_1/2 = 4.5 m22^(4/9) Mpc⁻¹`: this pre-flight's
  `T_F(k_1/2)²` evaluates to **0.5432** for every tested m22, consistent
  with (if not exactly) the paper's qualitative "power drops by a factor of
  2" description (`pipeline/tests/test_wp_e6_sweep.py::
  test_hbg_half_power_point_matches_paper`).
- **Mixed fraction f < 1 — *** ENGINEERING APPROXIMATION ***:**
  `S(k; m, f) = 1 - f·(1 - T_F(k; m)²)`, i.e. **linear interpolation of the
  power suppression** between f=0 (S=1, no suppression) and f=1 (S=T_F²).
  This is explicitly **not** a derived mixed-fraction transfer function — a
  genuine two-component (CDM + ultralight) linear calculation requires
  solving coupled perturbation equations (the components' relative growth
  differs below the FDM Jeans scale), which is what **Liu, Gong & Zhou 2026
  (arXiv:2606.06969)** actually do to derive their published f_FDM bounds.
  The linear interpolation reproduces the correct f=0/f=1 endpoints and a
  monotone-in-f ordering — sufficient for an *adequacy* (can-cells-be-told-
  apart) pre-flight — and is flagged in the module docstring as a
  placeholder to be ratified or replaced against Liu, Gong & Zhou's (or an
  equivalent) treatment at `PREDICTION_v2` pin time, never before.

### 1.2 Toy DES-Y6-like synthetic observable

- Projected convergence power spectrum `C_ℓ` in 6 broad ℓ bands (100, 300,
  1000, 3000, 10000, 30000) via the flat-sky Limber approximation, using a
  toy Smail-type source redshift distribution (illustrative shape, **not**
  read from or fit to the actual released DES Y6 n(z)) and the
  Carroll-Press-Turner 1992 growth-factor fitting approximation.
- **Gaussian (Knox 1995) band-diagonal covariance** from the T0-pinned DES
  Y6 survey parameters (D-c): `n_eff = 8.22 arcmin⁻²`, `σ_e = 0.29`, area =
  4,422 deg² (arXiv:2501.05665, via
  `docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md`).
- Fidelity is explicitly **not** the goal (task framing) — this exists to
  order (m, f) cells by distinguishability, not to forecast DES Y6 to
  publication accuracy.

### 1.3 Distinguishability statistic

For each (m, f) cell, a diagonal `Δχ² = Σ_bands (C_ℓ^model − C_ℓ^{f=0})² /
Var(C_ℓ^{f=0})`, reported as an "equivalent σ" = `√Δχ²`. This is **exact**
only for one degree of freedom; combining 6 bands this way is a
deliberately rough proxy (no attempt is made to invert the true multi-dof
χ² tail probability) — adequate for *ordering* cells, not for a
publication-grade significance. The covariance is evaluated once, at the
f=0 baseline (a survey's noise budget does not depend on which hypothesis
is true here, since shape noise dominates the relevant bands — see
caveats).

**Grid:** m ∈ logspace(10⁻²², 10⁻¹⁹ eV, 13 points) × f ∈ {0.05, 0.10, …,
1.00} (20 points) = 260 cells, per the task spec.

---

## 2. The (m, f) adequacy table

**No cell in the tested grid reaches even 2σ.** The table below reports,
per mass column, the maximum equivalent-σ achieved anywhere in that column
(always at f = 1.0, the largest fraction tested — distinguishability is
monotone in f, `pipeline/tests/test_wp_e6_sweep.py::TestMonotonicity`), and
the published pure-FDM (f=1) exclusion status from
`docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md` §4 (excluded if m exceeds the
lowest applicable published threshold — Liu, Gong & Zhou 2026's 1.9×10⁻²¹ eV
Lyman-α bound is the tightest in this range):

| m (eV) | max σ_equiv (at f=1.0) | reaches 2σ anywhere? | published pure-FDM (f=1) status |
|---|---|---|---|
| 1.000×10⁻²² | 0.486 | No | **OPEN** (not excluded even at f=1) |
| 1.778×10⁻²² | 0.324 | No | **OPEN** |
| 3.162×10⁻²² | 0.202 | No | **OPEN** |
| 5.623×10⁻²² | 0.120 | No | **OPEN** |
| 1.000×10⁻²¹ | 0.074 | No | **OPEN** |
| 1.778×10⁻²¹ | 0.046 | No | **OPEN** |
| 3.162×10⁻²¹ | 0.027 | No | EXCLUDED (Liu, Gong & Zhou 2026, m>1.9×10⁻²¹ eV) |
| 5.623×10⁻²¹ | 0.014 | No | EXCLUDED |
| 1.000×10⁻²⁰ | 0.0072 | No | EXCLUDED |
| 1.778×10⁻²⁰ | 0.0035 | No | EXCLUDED |
| 3.162×10⁻²⁰ | 0.0015 | No | EXCLUDED (also: Rogers & Peiris 2021, m>2×10⁻²⁰ eV) |
| 5.623×10⁻²⁰ | 0.0007 | No | EXCLUDED |
| 1.000×10⁻¹⁹ | 0.0002 | No | EXCLUDED |

Sensitivity falls off steeply with mass (σ_equiv ∝ roughly m^{-0.8} across
this grid) because heavier ultralight masses push the FDM suppression scale
to higher k, beyond where this toy survey's broad ℓ-bands carry usable
signal-to-noise against shape noise (§4.2).

Full per-(m, f) cell table (`f`, `Δχ²`, `σ_equiv`, `reaches_2σ`,
`reaches_3σ`) is in `data/derived/wp_e6_adequacy_preflight_2026_07_27.json`.

**Context (not mechanically encoded in the grid above):** the same source,
Liu, Gong & Zhou 2026, already publishes sparse mixed-fraction bounds at
three anchor masses inside/near this grid — f_FDM < 0.07 at m=10⁻²³ eV
(below this grid), f_FDM < 0.12 at m=10⁻²² eV, f_FDM < 0.65 at m=10⁻²¹ eV,
with no effective mixed constraint stated above ~10⁻²¹ eV. These are
genuine, already-published Lyman-α mixed bounds, not reproduced or
challenged here.

---

## 3. The decisive sentence

**Under this toy DES-Y6-like cosmic-shear forward model (single broad
source distribution, 6 ℓ-bands spanning 100–30,000, diagonal Gaussian
shape-noise-dominated covariance), no cell in the pre-registered (m, f)
grid — m ∈ [10⁻²², 10⁻¹⁹] eV, f ∈ [0.05, 1.0] — reaches 2σ
distinguishability from f=0.** The best case in the grid (lightest mass
tested, m=10⁻²² eV, f=1.0, i.e. the *pure*-FDM endpoint, which is already
the least realistic mixed-fraction scenario) reaches only **σ_equiv ≈
0.49**.

**This non-detection is not primarily an area problem.** A mechanical
re-run of the same best-case cell (`data/derived/
wp_e6_adequacy_preflight_2026_07_27.json` →
`area_scaling_sensitivity_check`), holding `n_eff` and `σ_e` fixed at the
DES Y6 values and scaling only the survey area:

| Area (deg²) | σ_equiv (best-case cell) |
|---|---|
| 4,422 (DES Y6 actual) | 0.486 |
| 20,000 | 1.033 |
| 41,253 (**full sky**) | 1.484 |
| 100,000 (unphysical, >full sky) | 2.310 |

Even a **full-sky** version of DES Y6's depth/shape-noise properties would
reach only σ_equiv ≈ 1.48 for the single most favorable cell in the grid —
still short of 2σ. Only an area exceeding the entire sky (not physically
realizable) crosses 2σ under this exact toy model. The bottleneck is the
intrinsic smallness of the FDM-suppression signal in the ℓ-range where this
survey's shape noise is small, not simply insufficient sky coverage — a
finding directionally consistent with why the strongest published FDM
bounds in this mass range come from Lyman-α forest power (Rogers & Peiris
2021; Liu, Gong & Zhou 2026) and small-scale kinematics/lensing-substructure
probes (Dalal & Kravtsov 2022; Powell et al. 2023 VLBI; May, Dalal &
Kravtsov 2025), not broad cosmic-shear band powers.

**Per WP-E6 proposal §3 precondition 2:** "If the answer is 'none of the
grid', that pre-flight result is filed and the WP stops there." This filing
is that result. A weak-lensing cosmic-shear power-spectrum route to
mixed-fraction FDM constraints, at this level of modeling, is **not
adequate** for the proposed grid; if WP-E6 is to proceed empirically, either
a different observable/statistic (e.g. Lyman-α P1D, which is the route the
strongest published bounds already use) or a materially more sensitive
lensing statistic (tomographic bins, non-Gaussian covariance, higher-ℓ
real-space statistics with baryonic marginalization) would need to be
adopted and pre-registered before any real-data touch — none of which is
authorized or attempted here.

---

## 4. Caveats (explicit)

1. **Linear theory only.** No non-linear matter power spectrum (halofit,
   emulators, or FDM-specific non-linear corrections) is modeled anywhere.
   FDM suppression at the relevant scales is known to be partially
   regenerated by non-linear gravitational collapse (Hu, Barkana & Gruzinov
   2000 note this themselves); this toy model cannot capture that.
2. **No baryons beyond the EH98 shape.** No baryonic feedback (AGN,
   feedback-driven power suppression at small scales), which is the
   dominant systematic real DES-like cosmic shear analyses must marginalize
   over at the ℓ ≳ 1000–3000 scales used here.
3. **No photo-z systematics.** The toy n(z) is an illustrative Smail-type
   form, not calibrated to (or drawn from) DES Y6's actual redshift
   distribution or its photo-z uncertainty; no source-redshift scatter,
   bias, or tomographic binning is modeled.
4. **Interpolated mixing (§1.1).** `S(k;m,f)` is a linear interpolation of
   the pure-FDM suppression, not a solved two-component perturbation
   calculation. This is the single largest physics simplification in this
   pre-flight and is the first thing that should be replaced (against Liu,
   Gong & Zhou 2026 or an equivalent treatment) before any real-data
   comparison is designed.
5. **Gaussian, band-diagonal covariance only.** No band-band correlations,
   no non-Gaussian (trispectrum) covariance contribution, and the
   covariance is evaluated at the f=0 baseline for every cell rather than
   at each model point (a standard simplification for small deviations, but
   unverified here for how well it holds at f=1).
6. **z-independent suppression.** `S(k;m,f)` is applied uniformly across
   the redshift kernel; the true FDM Jeans scale (and hence the suppression
   shape) evolves with redshift, which this toy model ignores.
7. **σ_equiv is a rough combined-significance proxy** (§1.3), not an exact
   χ² tail probability for 6 correlated-or-not degrees of freedom.
8. **This is arithmetic on a toy forward model, not a measurement or a
   forecast against an actual DES Y6 data product.** No DES Y6 file was
   read; only its published summary survey parameters (n_eff, σ_e, area)
   were used, exactly as the `prereg-pipeline` skill's synthetic-data
   discipline requires pre-pin.
9. **No physics claim is made.** This says nothing about whether the
   dual-scale program's mathematics has anything to do with fuzzy/mixed
   dark matter; WP-E6 is an explicitly phenomenological, T1-delegated
   framing choice (D-b), not a derivation, and does not touch, test, or
   reopen any Tier A/B result in this repo's epistemic ledger.

**Restated for the record:** this document is **ENGINEERING pre-flight
arithmetic — NOT a `TEST`, NOT a `FIT`.** No real data was touched anywhere
in its production. Its fidelity (§1.1's interpolation above all) requires
explicit ratification or replacement at `PREDICTION_v2` pin time before any
of its numbers may inform a real-data comparison design.

---

## 5. Reproducibility

```
python3 scripts/wp_e6_adequacy_preflight.py
pytest pipeline/tests/test_wp_e6_sweep.py -q
```

---

Generated-by: Sonnet (Stream 3 agent) | Verified-by:
`pipeline/tests/test_wp_e6_sweep.py` (17 tests: known-answer sanity on both
cited transfer functions including the HBG00 half-power-point reproduction,
monotonicity in f for both the suppression factor and the full Δχ²
statistic, a zero-signal negative control, a scrambled-covariance negative
control, and exclusion-status lookup checks) | Reviewed-by: pending T0
(Xavier)
