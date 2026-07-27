# Data Landscape Distillation — inputs to WP-E6 (and a WP-E5 reopening question)

**Date:** 2026-07-27 · **Status:** informational + T0 decision list. Makes no physics
claim; all dataset numbers are sourced in `docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md`
(full survey, per-number URLs, unverified items explicitly marked).
**Origin:** T0 (Xavier) requested a survey of open data ("DESI and others") to support
more empirical elements; executed by a delegated research agent 2026-07-27; distilled and
cross-checked against repo pre-registration artifacts by the coordinator session.

---

## 1. Answers to WP-E6 proposal open questions (partial)

- **Q1 (the new data):** the strongest currently-public candidates are —
  need (a) transverse/spectroscopic: **DESI DR1** (LRG 2,138,600 spec-z at 0.4<z<1.1;
  ELG 2,432,022 at 0.8<z<1.6; ~3×10⁵ objects per Δz=0.1 slice; access via NOIRLab Astro
  Data Lab TAP / SPARCL, no NERSC account) with SDSS/eBOSS DR16 LSS as the frictionless
  secondary; need (b) lensing/structure: **DES Y6 Metadetection** (151,922,791 galaxies,
  4,422 deg², n_eff = 8.22 arcmin⁻²), **DESI DR1 Lyman-α P1D** (>300,000 forests, 1.7×
  eBOSS), **KiDS-Legacy DR5**. DESI DR2 spectra are NOT yet public (summary products
  only); Euclid DR1 and Rubin data are not usable yet (scheduled / rights-restricted).
- **Q2 (dataset choice):** recommend DES Y6 as primary weak-lensing product, pending one
  verification (whether the Metadetection FITS files are posted at
  des.ncsa.illinois.edu/releases — flagged unverified in the survey §5).

## 2. Decisive fact for WP-E6 scoping — the grid is already covered for pure FDM

Published bounds cover the ENTIRE proposed 10⁻²²–10⁻¹⁹ eV interval for a mediator that is
all of the dark matter: Lyman-α excludes m < 2×10⁻²⁰ eV (Rogers & Peiris 2021, PRL
126.071302) and ultra-faint-dwarf kinematics exclude up to m < 8×10⁻¹⁸ eV (May, Dalal &
Kravtsov 2025, arXiv:2509.02781), each with stated model dependences. Consequences for
the (still DRAFT, unpinned) WP-E6 proposal:

1. A sweep presented as novel pure-FDM exclusion would be re-derivation of known results;
   the pre-registration must not frame it that way.
2. The legitimately open territory is: (i) **mixed fractions** — f_FDM < 1 is genuinely
   weakly constrained above ~10⁻²¹ eV (f < 0.65 at 10⁻²¹ eV; effectively unconstrained
   higher, arXiv:2606.06969); (ii) **reproduction/robustness** runs, labeled as such.
3. Which framing (if any) to adopt is a T0 scoping decision that must precede the
   PREDICTION v2 amendment. The proposal's §1 grid line is amended accordingly (addendum).

## 3. WP-E5 floor re-examined against the new data — a reopening question for T0

The survey initially flagged a tension: no wide survey approaches 1.6 Mpc mean
inter-object spacing (DESI LRG ~25 Mpc). Cross-checking the repo's own artifact
(`docs/WP_E4_RESOLVABILITY_FLOOR_2026_07_26.md`) resolves the definition: the floor is a
**joint resolvability constraint** — the deformation scale r_s must span ≥ 1 voxel per
axis at achievable nbins, AND per-voxel occupancy must be non-trivial — enforced
mechanically by `assert_resolvable`, not a mean-spacing requirement. Therefore:

- The **object floor (~10⁴/slice) is cleared ~30×** by DESI DR1 (the 50-object ceiling
  that closed WP-E5 is obsolete as a statement about available data).
- The **occupancy constraint still rules out Mpc-scale r_s** on any wide survey (mean
  spacing 8–25 Mpc ⇒ (1.6 Mpc)³ voxels are almost all empty).
- **r_s ≳ 10–25 Mpc becomes plausibly resolvable for the first time** (BGS number
  density ~10⁻³–10⁻⁴ Mpc⁻³ ⇒ order-unity occupancy at 10–20 Mpc voxels, with field
  extents no longer the binding constraint). Whether the pre-registered deformation
  framework is meaningful at those scales is a physics-scoping question, not a data
  question, and is NOT asserted here.
- WP-E5's closure verdict stands as recorded (it was about the fields then available at
  the scales then proposed). Any reopening is a NEW work package with its own pre-flight:
  run `assert_resolvable` on actual DESI field geometry across an r_s grid BEFORE any
  comparison design — same discipline as WP-E6 precondition 2.

## 4. T0 decisions requested (supersedes Q1/Q2 of the WP-E6 proposal; Q3/Q4 still open)

- **D-a.** Approve DESI DR1 (+ eBOSS secondary) as the target for a resolvability
  pre-flight at r_s ∈ ~{5, 10, 15, 20, 25} Mpc — synthetic/geometry arithmetic only, no
  comparison code (rule 1 compliant). Cheap, mechanical, and decides whether a WP-E5
  successor is posable at all.
- **D-b.** Choose the WP-E6 framing: mixed-fraction (f_FDM < 1), robustness/reproduction,
  or defer WP-E6 until after the D-a pre-flight. (The pure-FDM novel-exclusion framing is
  off the table per §2.)
- **D-c.** Confirm DES Y6 vs KiDS-Legacy as the lensing product (pending the file-posting
  check), if WP-E6 proceeds.

---
Generated-by: Fable 5 (T1 coordinator), distilling delegated-agent survey | Verified-by:
survey numbers carry per-item source URLs and unverified-flags in
docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md; floor definition cross-checked against
docs/WP_E4_RESOLVABILITY_FLOOR_2026_07_26.md | Reviewed-by: pending T0 (Xavier)
