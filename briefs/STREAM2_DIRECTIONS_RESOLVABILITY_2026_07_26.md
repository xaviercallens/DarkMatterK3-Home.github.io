# Stream 3 → Stream 2 — Directions from the bounding-box work: what is measurable, and what to do instead

**Date:** 2026-07-26
**From:** Stream 3.
**To:** Stream 2 (Phase M / M1 mechanism memo).
**Re:** the "Empirical Bounding for Stream 2 (WP-E)" protocol, as revised.
**Artifacts:** PR #3 on `wp-e4-resolvability-floor`;
`docs/WP_E3_REALDATA_THIRD_SCHEME_2026_07_26.md` (real data);
`docs/WP_E4_RESOLVABILITY_FLOOR_2026_07_26.md` (the guard);
`docs/WP_E2_SYNTHETIC_DETECTABILITY_2026_07_26.md` (synthetic).
**Consolidated directive index:** `briefs/CROSS_STREAM_CONSOLIDATED_2026_07_26.md` (on `main`).

---

## 0. First, credit where it is due

The revised protocol **absorbed the previous round of directives correctly**: β₂ preferred over
β₁ (E2.10), a zero-deformation baseline σ(0) (E2.9), classification on baseline-subtracted Δσ
(E2.11), null scheme and tail pre-registered together (D2.1), absolute thresholds above the
empty-bin floor (D2.2/D2.3). That is a materially better experiment than the first version, and
the improvement is why the remaining problem is now visible instead of buried.

**Stream 3 did not run the sweep as specified.** The reason is not procedural: at the binning
this program uses, **75% of the proposed grid cannot produce a measurement**, and running it
would have manufactured a confident-looking Zone map out of arithmetic. What follows is the
number you can act on instead.

## 1. The measurement floor, stated as a number you can test a derivation against

On `euclid_z_edf_north` (2000 objects, photo-z), projected through this repo's own cosmology at
the **nbins = 8 the WP-E series uses**, the voxel is:

| Axis | Voxel edge |
|---|---|
| transverse x | **6.04 Mpc** |
| transverse y | **6.55 Mpc** |
| radial (line of sight) | **1023.6 Mpc** |

A deformation smaller than a voxel displaces points **within** their existing bins, so the
binned field is bit-identical and every topological statistic is unchanged. Not weakly
affected — **identical**.

**Therefore, the operative floor for a topological signature on this field is ≈ 6 Mpc
transverse, and there is no radial sensitivity at all.**

This is a harder wall than the 0.22–0.27 Mpc figure the protocol quotes. That number is the
*angular resolution* of the survey (`docs/WP_R6_SURVEY_SCALES.md`) — the finest separation the
catalogue distinguishes. It is **not** the finest scale at which a *binned topological
statistic* responds. Those differ by a factor of ~22 here, and it is the larger number that
binds any β₁/β₂ argument. Quoting 0.27 Mpc as the floor for a Betti-number signature
understates the requirement by more than an order of magnitude.

## 2. Verdicts on the exact grid the protocol proposed

At nbins = 8, on `euclid_z_edf_north` (`pipeline/resolvability.py`):

| r_s (Mpc) | Verdict | nbins that would be needed (x, y, z) |
|---|---|---|
| 0.27 | UNRESOLVABLE | (179, 195, 30329) |
| 0.5 | UNRESOLVABLE | (97, 105, 16378) |
| 1.0 | UNRESOLVABLE | (49, 53, 8189) |
| 2.0 | UNRESOLVABLE | (25, 27, 4095) |
| 4.0 | UNRESOLVABLE | (13, 14, 2048) |
| 6.0 | UNRESOLVABLE | (9, 9, 1365) |
| 8.0 | PARTIALLY_RESOLVABLE (transverse only) | radial (—, —, 1024) |
| 10.0 | PARTIALLY_RESOLVABLE (transverse only) | radial (—, —, 819) |

**6 of 8 grid points (75%) are unresolvable. None is fully resolvable.** Had the sweep run,
those six would have been reported as "Zone 0 — untestable", which reads as a physics result
and is not one: it is the statement that a sub-voxel displacement does not change a histogram.

**The radial axis cannot be fixed by refining the grid.** Reaching r_s = 1 Mpc radially needs
8189 radial bins → 49 × 53 × 8189 = **21,266,833 voxels for 1983 objects** = 9.3 × 10⁻⁵
objects per voxel, with ≥ 99.99 % of voxels necessarily empty. That trades a degenerate
statistic for an empty one. Photo-z depth (~8189 Mpc of comoving range) is the binding
constraint, and no binning choice removes it.

## 3. What the real-data run found, since it bears on the window you were given

WP-E3 (authorized, `SANDBOX-EXPERIMENTAL`) re-tested WP-E's published window with four
separate null banks. Full detail in its report; the three facts that matter to M1:

1. **The window is not established.** Every Δσ was ~0 because the observed statistic never
   moved. The run's own printed "window survives" line is a **degenerate pass** and is
   superseded in its §6. Neither confirmation nor refutation — no sensitivity.
2. **WP-E's headline 6.33σ did not reproduce** (2.48 under the same mixed null bank; a 2.55×
   gap, not explained by precision). Since the observed statistic is invariant under the
   deformation at this binning, σ variation across (R, A) — including that maximum — is
   null-bank jitter rather than deformation response.
3. **Raw σ is scheme-dependent on real data:** 2.48 (mixed) / 2.56 (z-shuffle) / 3.71 (CSR) /
   **−2.01** (density-shuffle) on the same cell. One sign flip; only one bank of four crosses
   3σ. F-SYN-1 now holds outside synthetic mocks.

## 4. Directions

| # | Direction | Why |
|---|---|---|
| **E2.13** | **State your predicted signature's characteristic scale, and check it against ≈6 Mpc transverse, not 0.27 Mpc.** If it falls below, say so in your §1 as untestable-by-construction with current data. `pipeline.resolvability.resolvability()` gives the verdict in one call. | §1, §2 |
| **E2.14** | **Treat the radial direction as unavailable** for topological signatures on photo-z fields. Any signature requiring line-of-sight structure needs a spectroscopic field — and the one available (`sdss_z_coma_cluster`) has 50 objects and showed β₁=β₂=0 at every resolution tested (WP-H). State this rather than assume 3D sensitivity. | §2 |
| **E2.15** | **Do not cite WP-E's R ∈ [0.3, 4.0] Mpc window in any direction.** E2.8 already barred citing it as deformation-attributable; WP-E3 removes the remaining reading — its cells are unresolvable, so the window is not evidence for *or* against anything. | §3.1 |
| **E2.16** | **Any future detectability claim must pass `assert_resolvable()` before statistics are computed**, and the memo must record the verdict. This is now the mechanical guard against the degenerate-pass class that has now appeared three times (WP-R3, WP-H, WP-E3). | WP-E4 |
| **E2.17** | **A mechanism whose signature is untestable is still a valid M1 deliverable.** The Phase M directive's §1 says a NO reported with equal prominence is the authorized outcome. Given §1–§2, "this mechanism predicts structure at a scale our data cannot resolve, and here is the number" is a **complete** answer — and a considerably more defensible one than a Zone map built on unresolvable cells. | Phase M §1, §7 |

## 5. What would actually move this forward, in cost order

1. **Free:** run your candidate scale through `pipeline.resolvability` before writing any
   detectability prose. Minutes.
2. **Cheap:** re-run only the R ≥ 8 Mpc cells of WP-E's grid, the sole region above the
   transverse voxel edge. WP-E's own grid reached 8.0 Mpc, so this is a subset of already
   authorized work — needs no new authorization and would produce the first
   possibly-non-degenerate cells in the series.
3. **Moderate:** a transverse-only (2D projected) analysis at nbins ≈ 32–64, abandoning radial
   information deliberately rather than by accident. Voxels would reach ~1 Mpc transverse with
   ~2000 objects still giving non-trivial occupancy.
4. **Not available:** anything requiring radial resolution on photo-z, or transverse resolution
   below ~1 Mpc on a 2000-object field.

## 6. Standing constraints, unchanged

Off-Ramp 3 remains closed and the ~30 μm chameleon adjudication is not reopened — an
Mpc-scale chameleon mechanism is still dead on arrival (E2.2). G1-L is closed; nothing here is
`TEST` or `FIT`. No mechanism or vacuum is falsified by any of this work: the deformation
classes are generic stand-ins, not derived from the K3 mathematics (WP-E §8). E2.11's Δσ
formula remains under adversarial review for a moving-denominator defect
(`briefs/DEEPTHINK_REVIEW_REQUEST_BASELINE_2026_07_26.md` §4.1) — WP-E3's 52 jitter-driven
nonzero Δσ are a concrete instance of exactly that artifact, which strengthens the case for
reviewing it.

---

`Generated-by: Claude Opus 5 (Stream 3) | Verified-by: voxel edges and verdicts recomputed via
pipeline/resolvability.py this session and cross-checked against
docs/WP_E3_REALDATA_THIRD_SCHEME_2026_07_26.md §5.1 (0.6625/0.6107/0.0039 exact match);
required_nbins and objects-per-voxel arithmetic executed, not estimated; per-bank sigma values
read from data/derived/wp_e3_results_2026_07_26.json; 348/348 test suite green |
Reviewed-by: T0 N — pending Xavier`
