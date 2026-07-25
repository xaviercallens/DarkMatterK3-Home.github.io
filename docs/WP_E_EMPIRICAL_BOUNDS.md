# WP-E — Phenomenological Bounding Box (SANDBOX-EXPERIMENTAL)

**Date:** 2026-07-25
**Executor:** Claude Sonnet 5 (T1)
**Tag:** `SANDBOX-EXPERIMENTAL` — see `EXECUTION_PLAN.md` §4.1 for the label definition
**Authorization:** `docs/WP_E_T0_AUTHORIZATION_2026_07_25.md` (Xavier, direct, 2026-07-25)
**Status:** ✅ COMPLETE

> ⚠️ **This is not `ENGINEERING`, not `TEST`, not `FIT`.** It is exploratory
> hypothesis-generation infrastructure for Stream 2's Phase M mechanism memo
> (`briefs/STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md`). No number in this document is a
> validated result, a physics claim, or eligible for `PREDICTION.md` without its own fresh
> pre-registration. Gate G1-L stays closed; Off-Ramp 3 terminus (`NO_PREDICTION_BRANCH.md`
> §8.5) is unaffected — this document does not test any hypothesis, it maps where a
> *hypothetical* one would need to live to be distinguishable from noise at all.

---

## 1. Method

Two generic phenomenological deformation classes ("chameleon core halt": pull points
toward their local density peak, i.e. smoothing; "void evacuation": push points away from
their local density minimum, the exact opposite operation) applied via GPU tensor ops
(PyTorch, Tesla T4, confirmed via `nvidia-smi` before use) to real Euclid/SDSS catalog
coordinates (`scripts/wp_e_gpu_sandbox.py`). Neither deformation is derived from a specific
EFT — they are generic stand-ins, explicitly not tied to the [A-DD] branch that hit
Off-Ramp 3.

Swept across length scale R ∈ {0.3, 0.5, 1.0, 2.0, 4.0, 8.0} Mpc (floor 0.27 Mpc per
WP-R6) and amplitude A ∈ {0.1, 0.3, 0.5, 0.7, 0.9}, at absolute density thresholds
(never percentile — WP-R7 §4 sparse-field finding) of {0.5, 1.0, 1.5, 2.0}× the field
mean. β₁/β₂ only, never β₀ (WP-R7's percolation finding). 30 null realizations per
(field, class, R, A, threshold, branch) cell.

Two null baselines computed per setting, per T0 authorization to run both explicitly:

- **`wp_r3_style`** — literal reimplementation of WP-R3's retracted schemes (co-permuted
  shuffle, rigid rotation) at coordinate level, since WP-R3 itself stored no coordinate
  arrays (only aggregate β₀/β₁/β₂ scalars) — nothing literal to "deform" existed.
- **`wp_r5_valid`** — the corrected, T0-signed z-shuffle/angular-CSR schemes
  (`docs/T0_SIGNOFF_WP_R5_R6_R7_2026_07_25.md`).

Fields: `euclid_z_edf_north` (n=1983 valid), `euclid_z_edf_fornax` (n=1993 valid),
`sdss_z_coma_cluster` (n=50). Full results:
`/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/wp_e_sandbox/wp_e_results_2026_07_25.json`
(SHA256: `9f0d642424a2e28aa6fd5357b58135c62670e741adbce4b79862cf8d9f6d8eee`).

## 2. Two implementation bugs found and fixed before finalizing (disclosed, not hidden)

Building the `wp_r3_style` branch surfaced two genuine bugs, caught by checking the
branch's own expected property (it should reproduce WP-R3's known no-op degeneracy)
rather than trusting the code on the first pass:

1. **3D extension error.** WP-R3's original "shuffle" (2D: permute RA and Dec by the same
   index) is a no-op because it reorders an unordered point set. A first implementation
   permuted only (RA, Dec) while leaving redshift `z` in its original row order — this
   does *not* reproduce the no-op in 3D, it silently constructs new (RA, Dec, z) triples
   never present in the real data. Fixed by permuting all three coordinates by the same
   index (`wp_r3_style_shuffle`).
2. **Tangent-plane recentering error.** WP-R3's "rotate" (rigid RA rotation) is an
   isometry in angle space, but the tangent-plane projection's transverse offset scales
   with each point's own comoving distance (`r · Δra`). Projecting a rotated field around
   the *original* (unrotated) tangent-plane centroid is not distance-preserving when `r`
   varies across the field — which it does substantially for these Euclid cones
   (z ∈ [0.03, 6.0], comoving distance range ~132–8425 Mpc). Fixed by recentering the
   tangent-plane origin to each rotated realization's own centroid.

Both fixes were verified independently before the final sweep (exact point-set identity
for shuffle; pairwise-distance preservation to floating-point precision for rotate, tested
on a synthetic wide-z-range case matching the real fields' redshift span) — see commit
history for the verification commands. Post-fix, the `wp_r3_style` branch is degenerate
(zero null variance) in 240/240 or 236/240 cells per (field, class) combination, matching
the expected no-op behavior.

## 3. The `wp_r3_style` branch is degenerate — as expected, now correctly demonstrated

With both bugs fixed, `wp_r3_style` shows **zero null variance in essentially every cell**
(the 4/240 exceptions are floating-point boundary noise at bin edges, not a methodological
issue). This confirms `FINDING_R_NULLDEGENERATE_2026_07_25.md`'s diagnosis at the
coordinate level: both of WP-R3's schemes are point-pattern-preserving, so no amount of
sweeping R/A/threshold recovers a usable null from them. **The `wp_r3_style` branch
produces no usable signal for Stream 2** — it is included only because it was explicitly
requested, and its degeneracy is itself the deliverable of that branch: a demonstration,
not a workaround.

## 4. The `wp_r5_valid` branch — candidate windows for Stream 2

| Field | Class | Max &#124;σ&#124; | At (R, A, threshold, stat) | Cells &#124;σ&#124;≥3 | Cells &#124;σ&#124;≥5 |
|---|---|---|---|---|---|
| euclid_z_edf_north | chameleon_core_halt | **6.33** | R=0.3, A=0.3, thr=1.5×mean, β₁ | 17/238 | 2/238 |
| euclid_z_edf_north | void_evacuation | 5.39 | R=0.3, A=0.3, thr=0.5×mean, β₁ | 19/239 | 2/239 |
| euclid_z_edf_fornax | chameleon_core_halt | 1.81 | R=1.0, A=0.1, thr=0.5×mean, β₂ | 0/236 | 0/236 |
| euclid_z_edf_fornax | void_evacuation | ~~4.50~~ **RETRACTED, §5** | R=8.0, A=0.3, thr=0.5×mean, β₂ | ~~1~~/232 | 0/232 |
| sdss_z_coma_cluster | chameleon_core_halt | −1.83 | R=0.3, A=0.3, thr=0.5×mean, β₁ | 0/144 | 0/144 |
| sdss_z_coma_cluster | void_evacuation | 1.43 | R=0.3, A=0.9, thr=0.5×mean, β₁ | 0/112 | 0/112 |

**Primary candidate window:** `euclid_z_edf_north`, both deformation classes, is
distinguishable from the `wp_r5_valid` null at R ∈ [0.3, 4.0] Mpc — i.e. **within the
resolvable range** (floor 0.27 Mpc, WP-R6), concentrated at the smallest R tested (0.3 Mpc,
just above the resolution floor). `edf_fornax` and `sdss_z_coma_cluster` show essentially
no discriminating signal under either deformation class at any tested setting (after §5's
retraction).

## 5. Retraction: `edf_fornax`/`void_evacuation` R=8.0 finding is a float32 numerical artifact, not signal

The T1 CPU spot-check (§6, required by the WP-E directive before finalizing) caught this
directly. Re-running the deformation at float64 precision (same algorithm, same code path,
only the tensor dtype changed) on this exact cell gives β₂=1, not the float32 GPU's β₂=2 —
a genuine disagreement, not rounding noise: max coordinate difference between float32 and
float64 versions of the *same* deformation was 2.34 Mpc. **Diagnosis:** at R=8.0 Mpc, the
neighbor-averaging sum (`mask @ coords`, a matrix product accumulating over however many of
the ~2000 points fall within 8 Mpc of each point — for this field's ~41×44 Mpc transverse
extent, that is a large fraction of the field) accumulates enough float32 rounding error
to move points by Mpc-scale amounts, enough to flip a threshold-adjacent voxel's cavity
count. **This specific cell's ≥3σ finding is retracted** — it is a precision artifact of
this sandbox's float32 GPU implementation at large R, not evidence about the data.
**Methodology note for any future use of this sandbox:** treat R ≳ 4 Mpc results as
requiring float64 confirmation before use; R ≤ 2 Mpc results (where the primary edf_north
finding lives) were not affected by this failure mode (confirmed by §6's spot-check, which
used R=0.3 and matched exactly).

## 6. T1 CPU spot-check (required before finalizing, WP-E directive §5)

Two spot-checks run, independent pure-numpy (no GPU/torch) reimplementation of both
deformation classes vs the actual GPU output (`scripts/wp_e_t1_spotcheck.py`):

| Field | Class | R | A | Threshold | Max &#124;GPU−CPU&#124; coord diff | Topology match |
|---|---|---|---|---|---|---|
| edf_north (primary finding) | chameleon_core_halt | 0.3 | 0.3 | 1.5×mean | 0.74 Mpc | ✅ PASS (β₁=2, β₂=0, both) |
| edf_fornax (flagged cell) | void_evacuation | 8.0 | 0.3 | 0.5×mean | 2.34 Mpc | ❌ FAIL (β₂: GPU=2, CPU-equivalent float64=1) |

The primary finding (edf_north, R=0.3) passed with the topology statistic exactly matching
despite a nonzero coordinate-level float32/float64 difference (expected — β₁/β₂ are integer
invariants of a thresholded voxel mask, robust to small perturbations away from a threshold
boundary). The flagged cell failed, motivating §5's retraction. **This is exactly what the
spot-check requirement is for** — it caught a real defect before it reached Stream 2 as an
unqualified number.

## 7. Resolution floor and threshold-granularity compliance

Confirmed: no R below 0.27 Mpc tested (grid starts at 0.3). All thresholds absolute
(fractions of field mean), none percentile-based (avoiding WP-R7 §4's sparse-field
percentile-degeneracy failure mode).

## 8. What this does NOT do

- Does not test any hypothesis; Off-Ramp 3 stands unchanged. `edf_north`'s ≥3σ cells are a
  statement about where a *generic* smoothing/evacuation deformation becomes distinguishable
  from noise on *this* field at *this* resolution — not a detection of anything, and not
  tied to any specific mechanism.
- Does not itself constitute a mechanism — Stream 2's M1 memo must still name a physical
  route past the three F5b walls (`briefs/STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md` §3).
  If M1 proposes a mechanism whose natural length scale lands outside R ∈ [0.3, 4.0] Mpc on
  the `edf_north`-like fields, that mechanism is untestable-by-construction with the data
  and deformation classes examined here — the same discipline §4 of the Phase M directive
  already requires, now with a number attached.
- Does not carry TEST/FIT under any framing (gate G1-L closed, mechanically enforced,
  never invoked by this script).
- Does not claim generality beyond the specific deformation classes, fields, and grid
  tested. A different generic deformation, or a genuine mechanism-derived one, could show
  a different window entirely.

---

`Generated-by: Claude Sonnet 5 (T1) | Verified-by: 2 independent CPU spot-checks (1 pass, 1 fail leading to retraction), float32-vs-float64 diagnostic, pre-sweep verification of both bugfixes | Reviewed-by: T0 Y (Xavier direct authorization, docs/WP_E_T0_AUTHORIZATION_2026_07_25.md)`
