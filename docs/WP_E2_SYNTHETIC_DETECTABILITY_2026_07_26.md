# WP-E2: Synthetic Controlled-Injection Detectability Sweep

**ALL RESULTS ARE SYNTHETIC CONTROLLED-INJECTION — NOT A MEASUREMENT OF ANY SURVEY, NOT A TEST OF ANY HYPOTHESIS.**

Engineering-only exploration on mock catalogs. Ground truth is known because we inject the deformation ourselves.

## Pre-Registered Decision Rule

Statistic: β₁ and β₂ only (β₀ reported but not used; WP-R7). Tail: two-sided, abs(z) >= 3.0. Threshold: absolute density as multiples of undeformed mean. Null hypothesis: no deformation (null bank from undeformed field).

## Scale Honesty

**Box extent:** 734.8 × 613.2 × 442.9 Mpc (x, y, z)

**Voxel scale (Mpc per axis):** 45.927 (x), 38.328 (y), 27.683 (z)

**Swept R_voxels range:** 0.5 to 4.0 voxels

**Corresponding physical scale range:** 13.842 to 183.706 Mpc

**Overlap with survey-resolvable window [0.22–0.27 Mpc]:** NO

The default synthetic box cannot probe the resolvable window. Reaching it requires a box smaller by a factor of ~680.4x.

## Cross-Scheme Agreement

Per (R_voxels, amplitude, threshold, statistic), count how many of 3 schemes detected the deformation. Disagreement cells are those where ≥1 scheme detected and ≥1 did not.

| R_voxels | Amplitude | Threshold | Stat | Schemes Detected (0-3) |
|----------|-----------|-----------|------|------------------------|
|      0.5 |       0.0 |       0.5× | beta_1 |                      3 |
|      0.5 |       0.0 |       0.5× | beta_2 |                      1 |
|      0.5 |       0.0 |       1.0× | beta_1 |                      3 |
|      0.5 |       0.0 |       1.0× | beta_2 |                      1 |
|      0.5 |       0.0 |       1.5× | beta_1 |                      3 |
|      0.5 |       0.0 |       1.5× | beta_2 |                      0 |
|      0.5 |       0.1 |       0.5× | beta_1 |                      3 |
|      0.5 |       0.1 |       0.5× | beta_2 |                      2 |
|      0.5 |       0.1 |       1.0× | beta_1 |                      2 |
|      0.5 |       0.1 |       1.0× | beta_2 |                      2 |
|      0.5 |       0.1 |       1.5× | beta_1 |                      3 |
|      0.5 |       0.1 |       1.5× | beta_2 |                      0 |
|      0.5 |       0.3 |       0.5× | beta_1 |                      3 |
|      0.5 |       0.3 |       0.5× | beta_2 |                      2 |
|      0.5 |       0.3 |       1.0× | beta_1 |                      2 |
|      0.5 |       0.3 |       1.0× | beta_2 |                      2 |
|      0.5 |       0.3 |       1.5× | beta_1 |                      3 |
|      0.5 |       0.3 |       1.5× | beta_2 |                      0 |
|      0.5 |       0.5 |       0.5× | beta_1 |                      2 |
|      0.5 |       0.5 |       0.5× | beta_2 |                      3 |
|      0.5 |       0.5 |       1.0× | beta_1 |                      2 |
|      0.5 |       0.5 |       1.0× | beta_2 |                      2 |
|      0.5 |       0.5 |       1.5× | beta_1 |                      3 |
|      0.5 |       0.5 |       1.5× | beta_2 |                      0 |
|      0.5 |       1.0 |       0.5× | beta_1 |                      3 |
|      0.5 |       1.0 |       0.5× | beta_2 |                      3 |
|      0.5 |       1.0 |       1.0× | beta_1 |                      2 |
|      0.5 |       1.0 |       1.0× | beta_2 |                      2 |
|      0.5 |       1.0 |       1.5× | beta_1 |                      3 |
|      0.5 |       1.0 |       1.5× | beta_2 |                      0 |
|      1.0 |       0.0 |       0.5× | beta_1 |                      3 |
|      1.0 |       0.0 |       0.5× | beta_2 |                      1 |
|      1.0 |       0.0 |       1.0× | beta_1 |                      3 |
|      1.0 |       0.0 |       1.0× | beta_2 |                      1 |
|      1.0 |       0.0 |       1.5× | beta_1 |                      3 |
|      1.0 |       0.0 |       1.5× | beta_2 |                      0 |
|      1.0 |       0.1 |       0.5× | beta_1 |                      2 |
|      1.0 |       0.1 |       0.5× | beta_2 |                      2 |
|      1.0 |       0.1 |       1.0× | beta_1 |                      3 |
|      1.0 |       0.1 |       1.0× | beta_2 |                      2 |
|      1.0 |       0.1 |       1.5× | beta_1 |                      3 |
|      1.0 |       0.1 |       1.5× | beta_2 |                      0 |
|      1.0 |       0.3 |       0.5× | beta_1 |                      3 |
|      1.0 |       0.3 |       0.5× | beta_2 |                      2 |
|      1.0 |       0.3 |       1.0× | beta_1 |                      3 |
|      1.0 |       0.3 |       1.0× | beta_2 |                      2 |
|      1.0 |       0.3 |       1.5× | beta_1 |                      3 |
|      1.0 |       0.3 |       1.5× | beta_2 |                      0 |
|      1.0 |       0.5 |       0.5× | beta_1 |                      3 |
|      1.0 |       0.5 |       0.5× | beta_2 |                      3 |
|      1.0 |       0.5 |       1.0× | beta_1 |                      1 |
|      1.0 |       0.5 |       1.0× | beta_2 |                      2 |
|      1.0 |       0.5 |       1.5× | beta_1 |                      3 |
|      1.0 |       0.5 |       1.5× | beta_2 |                      0 |
|      1.0 |       1.0 |       0.5× | beta_1 |                      3 |
|      1.0 |       1.0 |       0.5× | beta_2 |                      3 |
|      1.0 |       1.0 |       1.0× | beta_1 |                      2 |
|      1.0 |       1.0 |       1.0× | beta_2 |                      2 |
|      1.0 |       1.0 |       1.5× | beta_1 |                      2 |
|      1.0 |       1.0 |       1.5× | beta_2 |                      0 |
|      2.0 |       0.0 |       0.5× | beta_1 |                      3 |
|      2.0 |       0.0 |       0.5× | beta_2 |                      1 |
|      2.0 |       0.0 |       1.0× | beta_1 |                      3 |
|      2.0 |       0.0 |       1.0× | beta_2 |                      1 |
|      2.0 |       0.0 |       1.5× | beta_1 |                      3 |
|      2.0 |       0.0 |       1.5× | beta_2 |                      0 |
|      2.0 |       0.1 |       0.5× | beta_1 |                      3 |
|      2.0 |       0.1 |       0.5× | beta_2 |                      2 |
|      2.0 |       0.1 |       1.0× | beta_1 |                      1 |
|      2.0 |       0.1 |       1.0× | beta_2 |                      2 |
|      2.0 |       0.1 |       1.5× | beta_1 |                      3 |
|      2.0 |       0.1 |       1.5× | beta_2 |                      0 |
|      2.0 |       0.3 |       0.5× | beta_1 |                      3 |
|      2.0 |       0.3 |       0.5× | beta_2 |                      2 |
|      2.0 |       0.3 |       1.0× | beta_1 |                      1 |
|      2.0 |       0.3 |       1.0× | beta_2 |                      2 |
|      2.0 |       0.3 |       1.5× | beta_1 |                      3 |
|      2.0 |       0.3 |       1.5× | beta_2 |                      0 |
|      2.0 |       0.5 |       0.5× | beta_1 |                      3 |
|      2.0 |       0.5 |       0.5× | beta_2 |                      3 |
|      2.0 |       0.5 |       1.0× | beta_1 |                      1 |
|      2.0 |       0.5 |       1.0× | beta_2 |                      2 |
|      2.0 |       0.5 |       1.5× | beta_1 |                      2 |
|      2.0 |       0.5 |       1.5× | beta_2 |                      0 |
|      2.0 |       1.0 |       0.5× | beta_1 |                      3 |
|      2.0 |       1.0 |       0.5× | beta_2 |                      2 |
|      2.0 |       1.0 |       1.0× | beta_1 |                      3 |
|      2.0 |       1.0 |       1.0× | beta_2 |                      2 |
|      2.0 |       1.0 |       1.5× | beta_1 |                      2 |
|      2.0 |       1.0 |       1.5× | beta_2 |                      0 |
|      4.0 |       0.0 |       0.5× | beta_1 |                      3 |
|      4.0 |       0.0 |       0.5× | beta_2 |                      1 |
|      4.0 |       0.0 |       1.0× | beta_1 |                      3 |
|      4.0 |       0.0 |       1.0× | beta_2 |                      1 |
|      4.0 |       0.0 |       1.5× | beta_1 |                      3 |
|      4.0 |       0.0 |       1.5× | beta_2 |                      0 |
|      4.0 |       0.1 |       0.5× | beta_1 |                      3 |
|      4.0 |       0.1 |       0.5× | beta_2 |                      1 |
|      4.0 |       0.1 |       1.0× | beta_1 |                      2 |
|      4.0 |       0.1 |       1.0× | beta_2 |                      2 |
|      4.0 |       0.1 |       1.5× | beta_1 |                      3 |
|      4.0 |       0.1 |       1.5× | beta_2 |                      0 |
|      4.0 |       0.3 |       0.5× | beta_1 |                      3 |
|      4.0 |       0.3 |       0.5× | beta_2 |                      1 |
|      4.0 |       0.3 |       1.0× | beta_1 |                      3 |
|      4.0 |       0.3 |       1.0× | beta_2 |                      2 |
|      4.0 |       0.3 |       1.5× | beta_1 |                      3 |
|      4.0 |       0.3 |       1.5× | beta_2 |                      0 |
|      4.0 |       0.5 |       0.5× | beta_1 |                      3 |
|      4.0 |       0.5 |       0.5× | beta_2 |                      2 |
|      4.0 |       0.5 |       1.0× | beta_1 |                      3 |
|      4.0 |       0.5 |       1.0× | beta_2 |                      2 |
|      4.0 |       0.5 |       1.5× | beta_1 |                      3 |
|      4.0 |       0.5 |       1.5× | beta_2 |                      0 |
|      4.0 |       1.0 |       0.5× | beta_1 |                      3 |
|      4.0 |       1.0 |       0.5× | beta_2 |                      2 |
|      4.0 |       1.0 |       1.0× | beta_1 |                      3 |
|      4.0 |       1.0 |       1.0× | beta_2 |                      2 |
|      4.0 |       1.0 |       1.5× | beta_1 |                      2 |
|      4.0 |       1.0 |       1.5× | beta_2 |                      0 |

**Total cells:** 120. **Disagreement cells (≥1 detected, ≥1 not):** 51. (Agreement = 69/120)

## Amplitude Sensitivity Floor

Per R_voxels and statistic, the smallest amplitude at which all three schemes agree on detection (at any threshold). If no tested amplitude shows all-three agreement, that R is listed as 'none'.

> ⚠ **Read this table together with the amplitude-0.0 section below.** A floor of `0.0`
> does **not** mean "detectable at arbitrarily small deformation" — it means the statistic
> was already outside the randomization null band with **no deformation applied at all**,
> i.e. the raw z is measuring the mock's clustering rather than the deformation. Only the
> `β₂` rows (floor ≈ 0.5, not detected at A=0) are deformation-attributable floors. The
> `β₁` rows are baseline-dominated and must not be quoted as sensitivity floors.

| R_voxels | Beta Statistic | Floor Amplitude |
|----------|----------------|-----------------|
|      0.5 | beta_1         | 0.0             |
|      0.5 | beta_2         | 0.5             |
|      1.0 | beta_1         | 0.0             |
|      1.0 | beta_2         | 0.5             |
|      2.0 | beta_1         | 0.0             |
|      2.0 | beta_2         | 0.5             |
|      4.0 | beta_1         | 0.0             |
|      4.0 | beta_2         | none            |

## Amplitude 0.0 — baseline offset (headline finding; the original "guard" framing was wrong)

**Detections at amplitude = 0.0: 44/72 cells (61.1%).**

At amplitude = 0.0 the deformed field is *exactly* the undeformed field — verified
bit-exactly (`pipeline/tests/test_deformation.py`, identity test). The sweep
specification originally called this a "tautological-zero guard" and expected ~0
detections. **That expectation was incorrect, and the 61% is not a defect.**

The two null hypotheses were conflated:

| Null construction used | What it actually asks | Behaviour at A=0 |
|---|---|---|
| Coordinate-level randomization (CSR, z-shuffle) | *"does this field have clustering structure?"* | **Detection expected** — the mock is clustered by construction, and randomization destroys clustering |
| *"is this field undeformed?"* | what the guard wording assumed | would require a null built by re-deforming the same point set, which is not what any of these three schemes do |

**Consequence, and the reason this is the headline result:** a z-score measured against a
randomization null is **not a measure of deformation detectability**. It is dominated by a
deformation-independent offset — the field is clustered. The deformation-attributable
quantity is the *increment over the A = 0 baseline*, `Δz(A) = z(A) − z(A=0)`, not the raw
`z(A)`.

This has a direct bearing on the real-data sweep it was designed to inform:
`scripts/wp_e_gpu_sandbox.py` line 59 reads
`A_GRID = [0.1, 0.3, 0.5, 0.7, 0.9]` — **no zero-amplitude baseline**. WP-E therefore never
measured its own offset, so its reported σ values (including the headline max |σ| = 6.33 for
`euclid_z_edf_north`) cannot be attributed to the deformation without one. This is a
**methodological qualification, not an error or a retraction**: WP-E's σ is a valid
"structured-vs-randomized, after deformation" statistic; it is simply not the
deformation-attributable one. WP-E3
(`docs/WP_E3_REALDATA_THIRD_SCHEME_2026_07_26.md`) adds the A = 0 baseline and reports
`Δσ` on the real field.

Read together with the floor table above: **β₂ is the statistic carrying
deformation-attributable signal here** (not detected at A=0, real floor at A≈0.5), while
**β₁'s raw z is dominated by the clustering baseline** (detected at A=0 across all R).

---
Generated by: Haiku 4.5 | Sweep config: n_objects=4000, nbins=16, n_null_trials=40