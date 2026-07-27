# WP-E7 — DESI DR1 Resolvability Pre-Flight (Geometry Arithmetic Only)

**Date:** 2026-07-27

**Executor:** Sonnet (Stream 3 agent), T0-approved per `briefs/T0_DECISIONS_2026_07_27.md`
decision D-a.

**Tag:** `ENGINEERING` — pure geometry/counting arithmetic on published survey numbers, in
the WP-E4 lineage (`docs/WP_E4_RESOLVABILITY_FLOOR_2026_07_26.md`).

⚠️ **NOT `TEST`, NOT `FIT`, NOT `SANDBOX-EXPERIMENTAL`.** This makes no physics claim,
runs no comparison against real data, and falsifies nothing. It decides, mechanically,
whether a deformation-scale analysis on DESI DR1 tracer samples could even be resolvable
at some r_s, before any comparison design exists — a pre-flight, not a result.

Script: `scripts/wp_e7_desi_preflight.py`. Artifact:
`data/derived/wp_e7_desi_preflight_2026_07_27.json`. Regression tests:
`pipeline/tests/test_wp_e7_desi_preflight.py` (23 tests, all passing; full suite
373 = 350 prior + 23 new, green).

---

## 1. Inputs and method

**Dataset numbers** (docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md §3, citing
arXiv:2404.03000 — DESI DR1 BAO/LSS catalog samples, ~7,500 deg² footprint):

| Tracer | N (BAO/LSS sample) | z range |
|---|---|---|
| BGS | 300,017 | 0.1 < z < 0.4 |
| LRG | 2,138,600 | 0.4 < z < 1.1 |
| ELG | 2,432,022 | 0.8 < z < 1.6 |
| QSO | 856,652 | 0.8 < z < 2.1 |

**Cosmology:** flat ΛCDM, H₀ = 67.4 km/s/Mpc, Ωm = 0.315 (Planck 2018 TT,TE,EE+lowE+lensing
headline values) — a standard fiducial choice, not fit to anything in this program.
Comoving distances computed via `astropy.cosmology.FlatLambdaCDM` (installed and used in
this run); a manual Simpson-rule integral of c/H(z) is implemented as a fallback and
cross-checked against astropy to < 1e-4 relative error at every tracer boundary redshift
(`pipeline/tests/test_wp_e7_desi_preflight.py::TestComovingDistanceRoundTrip`).

**Survey-mean number density.** For each tracer, `n = N / V_survey`, where `V_survey` is
the comoving volume of a single cone of solid angle Ω(7,500 deg²) between `D_C(zmin)` and
`D_C(zmax)` (exact flat-space cone-shell formula `V = (Ω/3)(D_far³ − D_near³)`, valid
because flat-ΛCDM comoving space is Euclidean). **This is a survey mean, not a local
density** — footprint geometry is idealized as one cone of the stated area; angular
masking, depth variation, and large-scale structure are not modeled.

| Tracer | D_C(zmin) Mpc | D_C(zmax) Mpc | V_survey Mpc³ | n (survey-mean, Mpc⁻³) |
|---|---|---|---|---|
| BGS | 434.1 | 1604.6 | 3.084×10⁹ | 9.73×10⁻⁵ |
| LRG | 1604.6 | 3642.6 | 3.366×10¹⁰ | 6.35×10⁻⁵ |
| ELG | 2873.5 | 4665.1 | 5.925×10¹⁰ | 4.10×10⁻⁵ |
| QSO | 2873.5 | 5455.5 | 1.056×10¹¹ | 8.11×10⁻⁶ |

**Candidate analysis boxes:** square transverse footprints of side ∈ {100, 200, 300, 400,
500} Mpc, crossed with a Δz = 0.1 radial slice placed at three positions in each tracer's
range (`zmin`, `zmid`, `zmax − 0.1`) — radial comoving depth of a Δz = 0.1 slice shrinks
with z (c/H(z) falls as z rises), so slice placement matters:

| Tracer | depth at zmin (Mpc) | depth at zmid (Mpc) | depth at zmax−0.1 (Mpc) |
|---|---|---|---|
| BGS | 412.2 | 379.1 | 368.1 |
| LRG | 346.8 | 280.1 | 241.3 |
| ELG | 271.8 | 215.2 | 183.0 |
| QSO | 271.8 | 187.9 | 143.4 |

**r_s grid:** {2, 5, 10, 15, 20, 25} Mpc, as specified.

**Geometry criterion (fixed, not reimplemented):** `pipeline.resolvability.required_nbins`
gives the per-axis nbins needed for r_s to span ≥ 1 voxel; the uniform nbins a real
pipeline would actually bin at is `max()` over the three per-axis values (matching how
WP-E4's own sweep applied one nbins value across a highly anisotropic box);
`pipeline.resolvability.resolvability()` is then called with that uniform nbins to get the
spatial verdict (RESOLVABLE / PARTIALLY_RESOLVABLE / UNRESOLVABLE), exactly as WP-E4
defines it.

**Occupancy criterion — PROPOSAL, NOT FIXED BY WP-E4 OR `resolvability.py`, NEEDS T0
RATIFICATION:** `pipeline/resolvability.py` fixes only the spatial (≥1 voxel) criterion.
WP-E4 §4 argues informally that sparsity makes topology trivial "independent of voxel
size" when occupancy is far below ~1 object/voxel, and `resolvability.py`'s own
`null_degeneracy()` treats "less than 1 count" as degenerate elsewhere in this codebase.
Following that precedent, this pre-flight proposes:

> **Primary threshold: mean occupancy ≥ 1.0 object/voxel → RESOLVABLE.**
> Occupancy in [threshold/10, threshold) → PARTIALLY_RESOLVABLE.
> Occupancy < threshold/10, or a spatial-criterion failure (hard stop regardless of
> occupancy) → UNRESOLVABLE.

Every verdict below is also computed under a **10× stricter threshold (10.0
objects/voxel)**, per the brief's explicit instruction, so the conclusion's sensitivity to
this unratified number is visible (§3).

---

## 2. Verdict table (representative box: 300 Mpc transverse, Δz=0.1 slice at z_mid)

Occupancy = expected objects per voxel of edge ≈ r_s, at survey-mean density.

**Under the primary threshold (≥1.0 obj/voxel):**

| r_s (Mpc) | BGS | LRG | ELG | QSO |
|---|---|---|---|---|
| 2  | UNRESOLVABLE (occ=0.000) | UNRESOLVABLE (occ=0.000) | UNRESOLVABLE (occ=0.000) | UNRESOLVABLE (occ=0.000) |
| 5  | UNRESOLVABLE (occ=0.008) | UNRESOLVABLE (occ=0.007) | UNRESOLVABLE (occ=0.004) | UNRESOLVABLE (occ=0.001) |
| 10 | UNRESOLVABLE (occ=0.060) | UNRESOLVABLE (occ=0.059) | UNRESOLVABLE (occ=0.029) | UNRESOLVABLE (occ=0.005) |
| 15 | PARTIALLY_RESOLVABLE (occ=0.189) | PARTIALLY_RESOLVABLE (occ=0.200) | UNRESOLVABLE (occ=0.099) | UNRESOLVABLE (occ=0.017) |
| 20 | PARTIALLY_RESOLVABLE (occ=0.484) | PARTIALLY_RESOLVABLE (occ=0.475) | PARTIALLY_RESOLVABLE (occ=0.236) | UNRESOLVABLE (occ=0.041) |
| 25 | PARTIALLY_RESOLVABLE (occ=0.810) | PARTIALLY_RESOLVABLE (occ=0.927) | PARTIALLY_RESOLVABLE (occ=0.460) | UNRESOLVABLE (occ=0.079) |

**Under the 10× stricter threshold (≥10.0 obj/voxel) — same box/placement:**

| r_s (Mpc) | BGS | LRG | ELG | QSO |
|---|---|---|---|---|
| 2–25 | UNRESOLVABLE (all) | UNRESOLVABLE (all) | UNRESOLVABLE (all) | UNRESOLVABLE (all) |

No cell in the tested grid reaches even PARTIALLY_RESOLVABLE under the 10× threshold — the
occupancy criterion is the binding constraint throughout this grid, not the spatial one:
every (tracer, box, r_s) combination tested has the geometry (spatial) criterion satisfied
(≥1 voxel spanned), because the candidate boxes (100–500 Mpc) are always large compared to
r_s (≤25 Mpc); it is occupancy that fails.

**Box-size sensitivity.** Occupancy at fixed r_s is NOT independent of box size: because a
single uniform nbins is applied across the (transverse, transverse, radial) extent,
ceil-rounding in `required_nbins` over/under-resolves axes differently depending on the
ratio of box side to radial depth, and small boxes (100 Mpc) are penalized relative to
larger ones. Full grid (5 box sizes × 3 slice placements × 6 r_s × 4 tracers = 360 cells)
in `data/derived/wp_e7_desi_preflight_2026_07_27.json`.

Requiring the verdict to hold at **every** tested box size and slice placement
(conservative) vs. at **any** one of them (best case, largest boxes dominate):

| Tracer | Primary — conservative | Primary — best case | 10×-stricter — conservative | 10×-stricter — best case |
|---|---|---|---|---|
| BGS | not reached in grid | **25 Mpc** (500 Mpc box, z_min slice) | not reached | not reached |
| LRG | not reached in grid | not reached in grid (max occupancy 0.93 at r_s=25) | not reached | not reached |
| ELG | not reached in grid | not reached in grid (max occupancy 0.59 at r_s=25) | not reached | not reached |
| QSO | not reached in grid | not reached in grid (max occupancy 0.15 at r_s=25) | not reached | not reached |

---

## 3. The decisive sentence

**Smallest resolvable r_s per tracer, under the stated (proposed, unratified) occupancy
criterion:** within the tested grid (r_s ≤ 25 Mpc, boxes 100–500 Mpc transverse), **only
BGS reaches a full RESOLVABLE verdict, and only in the best case (largest boxes, r_s = 25
Mpc)** — no tracer reaches RESOLVABLE at every box size tested, LRG comes closest without
crossing (occupancy 0.93 at r_s = 25 Mpc, box-dependent), and ELG/QSO stay further below
threshold throughout. **Under a 10× stricter occupancy threshold, no tracer reaches even
PARTIALLY_RESOLVABLE anywhere in the tested grid** — the conclusion is highly sensitive to
the unratified occupancy number, which is exactly why it is flagged as a proposal rather
than asserted as fact.

This is directionally consistent with — but more conservative and precise than — the
landscape survey's back-of-envelope claim
(`docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md` §3: "BGS number density ~10⁻³–10⁻⁴ Mpc⁻³ ⇒
order-unity occupancy at 10–20 Mpc voxels"): this pre-flight's computed BGS density
(9.73×10⁻⁵ Mpc⁻³) sits at the low end of that range, and order-unity occupancy is reached
here at r_s ≈ 20–25 Mpc rather than 10–20 Mpc. **The 10⁴-objects/slice floor discussed
elsewhere (WP-E5/WP-E6 landscape survey) and the per-voxel occupancy floor here are
different criteria** — DESI DR1 clears the former by 1–2 orders of magnitude for every
tracer, but that says nothing about per-voxel occupancy at Mpc-scale voxels, which is the
binding constraint measured here.

---

## 4. Caveats (explicit)

1. **Footprint geometry is idealized as a single cone** of the stated survey area; no
   angular mask, depth variation, or veto-region structure is modeled. Real DESI DR1
   subfields will have local density that differs from the survey mean computed here —
   possibly substantially, in either direction.
2. **Densities are survey-mean, not local.** A specific 100–500 Mpc subfield could sit in
   an overdense or underdense region; this pre-flight cannot and does not claim otherwise.
3. **The occupancy threshold (1.0 obj/voxel primary, 10.0 obj/voxel strict) is a proposal
   of this script, not a value fixed by WP-E4 or `pipeline/resolvability.py`.** It needs
   explicit T0 ratification before any downstream work package treats it as settled.
4. **Box size is not a free, harmless choice** (§2) — reported figures separate the
   conservative (robust to box-size choice) and best-case (largest-box) answers rather than
   collapsing to one number.
5. **This is arithmetic on published survey-level counts, not a measurement on an actual
   fetched DESI catalog.** The parallel data-acquisition task (WP-E7 companion, this
   session) attempted to fetch the actual DESI DR1 LSS catalogs for a follow-on empirical
   check; see the fetch report for what succeeded and what the DESI portal refused.
6. **No physics claim is made.** This says nothing about whether a deformation-scale
   analysis at any resolvable r_s would show anything; it only says whether the arithmetic
   permits the analysis to be attempted at all.

---

## 5. Reproducibility

```
python3 scripts/wp_e7_desi_preflight.py
pytest pipeline/tests/test_wp_e7_desi_preflight.py -q
```

---

Generated-by: Sonnet (Stream 3 agent) | Verified-by:
pipeline/tests/test_wp_e7_desi_preflight.py (23 tests: comoving-distance round-trip
astropy-vs-manual, WP-E4 euclid_z_edf_north known-answer reproduction, verdict-combining
logic) | Reviewed-by: pending T0 (Xavier)
