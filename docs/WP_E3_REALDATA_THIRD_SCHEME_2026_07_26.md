# WP-E3 — Real-data Third-Scheme Robustness Re-test (SANDBOX-EXPERIMENTAL)

**Date:** 2026-07-26
**Executor:** Claude Haiku 4.5
**Tag:** `SANDBOX-EXPERIMENTAL` — exploratory re-test of WP-E's published window under a fourth null scheme (density-shuffle) and decomposition into per-scheme signal
**Authorization:** `docs/WP_E3_T0_AUTHORIZATION_2026_07_26.md` (Xavier, direct, 2026-07-26)
**Status:** Computing (results below as available)

> ⚠️ **This is not `TEST`, not `FIT`, not `ENGINEERING`.** It is a real-data robustness
> verification of WP-E's published window against a fourth null scheme and quantification
> of baseline offset. No number here is a physics claim, a mechanism test, or eligible for
> falsification framing. It reports only whether the deformation-attributable signal
> (delta_sigma) survives per-scheme decomposition. See authorization §2 for exclusions and §5
> for the pre-committed kill condition (applied to delta_sigma, not raw sigma).

---

## 1. Data provenance

| Item | Value |
|---|---|
| Catalogue | `euclid_z_edf_north` (Euclid public MER ⋈ phz_photo_z, PDR live query 2026-07-25) |
| Path | `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid_z/euclid_z_edf_north.csv` |
| Rows (total) | 2000 |
| Rows (valid after redshift drop) | 1983 |
| SHA256 | `8b5b287f3f03165660e6232b904ee264e705788ffd60e67f54169ea2dddac2be` |
| Verified | ✅ Exact match computed before use |

---

## 2. Method

Two generic phenomenological deformation classes ("chameleon_core_halt": pull points
toward local density peaks; "void_evacuation": push away) applied to real `euclid_z_edf_north`
catalog coordinates via GPU tensor ops (PyTorch, Tesla T4). Float64 precision throughout
(not WP-E's float32), with explicit float32-vs-float64 comparison for the headline cell
to check for precision artifacts (WP-E §5 retraction class).

### 2.1 Grid

**REVISED GRID (per coordinator correction 2026-07-26):** Reduced from WP-E's full sweep to
manageable scope:
- Length scales R ∈ {0.3, 1.0, 4.0} Mpc (all ≥ 0.27 Mpc resolution floor per WP-R6; dropped 2.0 Mpc to accommodate A=0.0)
- Amplitudes A ∈ {0.0, 0.1, 0.3} — **INCLUDES A=0.0 zero-amplitude baseline** (new; not in WP-E)
- Absolute density thresholds (never percentile) {0.5, 1.0, 1.5} × field mean
- Statistics: β₁ and β₂ only (never β₀ for verdicts, per WP-R7 §4 finding: 30/30 cells have nonzero variance vs β₀'s 14/30)
- NBINS = 8 (matching WP-E for apples-to-apples comparison)
- 30 null realizations per (class, R, A, threshold, bank) cell

### 2.2 Four independent null banks

Each bank uses its own seeded RNG and answers a different question:

1. **`mixed_r5`** (RNG seed 302) — faithful reproduction of WP-E's coin-flip mixture: per realization,
   `rng.integers(2)` chooses either z-shuffle or angular-CSR. Coordinate-level null.
   **Purpose:** reproduction control — does our recomputation recover WP-E's published σ values?

2. **`z_shuffle_only`** (RNG seed 303) — always apply z-shuffle (permute redshift assignment, fix RA/Dec).
   Coordinate-level null. **Purpose:** isolate the z-shuffle signal.

3. **`csr_only`** (RNG seed 304) — always apply angular-CSR (redraw RA/Dec uniformly at fixed z).
   Coordinate-level null. **Purpose:** isolate the CSR signal.

4. **`density_shuffle`** (RNG seed 305) — **field-level null.** Apply deformation to real coordinates,
   bin the deformed field, then permute cell values across the binned field (voxel shuffle).
   Preserves the exact marginal distribution of cell values. **Purpose:** ask whether topology
   depends on spatial arrangement vs. only on the value histogram.

**Critical asymmetry:** Banks 1–3 randomize *coordinates then deform then bin*; bank 4 *deforms, bins,
then permutes cell values*. This difference is intentional and must be stated plainly — they answer
different questions and are not expected to agree a priori.

### 2.3 Sigma convention and baseline offset quantification

**Raw σ:** σ_raw = (observed - null_mean) / null_std, signed, reported to 2 decimals. If null_std = 0,
σ is None (never coerced to 0 or ∞).

**Delta sigma (deformation-attributable signal):** Δσ = σ(A) - σ(A=0), where σ(A=0) is the baseline
raw sigma at zero amplitude (no deformation). **Δσ is the quantity that isolates the deformation-induced
signal**, because the raw sigma includes both the field's natural clustering structure AND the deformation.
WP-E did not measure A=0 (its A_GRID started at 0.1), so this offset was not available to it.

**Distinguishability marker:** abs(Δσ) ≥ 3.0 (applied to delta_sigma, not raw sigma).

---

## 3. Baseline offset — why raw sigma overstates deformation detectability

The field is **clustered by construction** (it is a real galaxy survey region). When coordinate-level
nulls (z-shuffle, CSR) randomize coordinates, they destroy that clustering, making the real *undeformed*
field (A=0.0) already distinguishable from the randomized nulls. The raw σ(A) therefore includes two
contributions:
1. The field's intrinsic clustering signal (σ_baseline)
2. The deformation-induced perturbation (Δσ)

At A=0.0, σ_raw = σ_baseline (no deformation, only clustering). At A > 0, σ_raw = σ_baseline + Δσ.

**WP-E's published σ values (including the headline 6.33) are raw sigmas**, not delta sigmas. This is valid
— it is a correct "structured-vs-randomized-after-deformation" statistic — but it does not isolate the
deformation-attributable component. **The kill condition (authorization §5) is applied to delta_sigma** to
answer the actual question: does the deformation, net of baseline clustering, survive per-scheme decomposition?

WP-E's A_GRID (scripts/wp_e_gpu_sandbox.py line 59) is `[0.1, 0.3, 0.5, 0.7, 0.9]` — no zero amplitude
baseline. So WP-E could not compute delta_sigma. This decomposition was not available to it, and is not a
critique of WP-E — it is a methodological qualification that becomes necessary when schemes disagree (finding F-SYN-1 from WP-T6).

---

## 4. Headline reproduction check: raw sigma at A=0.3 under mixed_r5

WP-E §4 reports for `euclid_z_edf_north` / `chameleon_core_halt` a max |σ| of **6.33** (raw)
at (R=0.3, A=0.3, thr=1.5×mean, β₁).

All values below are traceable to `data/derived/wp_e3_results_2026_07_26.json`.

| Metric | Value |
|---|---|
| WP-E headline σ (raw, published) | **6.33** |
| This run, `mixed_r5` σ (raw, float64, A=0.3) | **2.48** |
| This run, `mixed_r5` σ (raw, float64, A=0.0) | **2.48** |
| This run, `mixed_r5` Δσ | **0.00** |
| **Assessment** | **REPRODUCTION NOT ACHIEVED** — discrepancy factor ≈ 2.5× |

**The headline value did not reproduce.** The pre-registered instruction was to report a
discrepancy beyond ~2× prominently rather than tune seeds or parameters to chase 6.33; the
discrepancy is 2.55×, so it is reported here as the primary result of this section. No
parameters were adjusted.

Exact agreement was never expected (WP-E ran float32 with RNG seeds 301/302). A 2.5×
magnitude gap is a different matter and is **not** explained by precision — §8 shows the
float32/float64 difference on this cell is nil. The likely cause is visible in §5: at the
binning WP-E used, the deformation does not move the observed statistic at all, so σ is
governed by null-bank realization jitter, which differs between runs with different seeds.

Per-bank raw σ for the same cell — note the **spread and the sign flip**:

| Bank | raw σ | Δσ | \|σ\| ≥ 3? |
|---|---|---|---|
| `mixed_r5` | 2.48 | 0.00 | no |
| `z_shuffle_only` | 2.56 | 0.00 | no |
| `csr_only` | **3.71** | 0.00 | **yes** |
| `density_shuffle` | **−2.01** | 0.00 | no (opposite sign) |

On **raw** σ the four banks disagree materially: only `csr_only` crosses the |σ| ≥ 3 marker,
and `density_shuffle` returns the **opposite sign**. This is F-SYN-1
(`briefs/STREAM3_AUDIT_DIRECTIVES_2026_07_26.md` §3) reproduced on **real data** rather than
synthetic mocks.

---

## 5. Per-scheme decomposition: delta_sigma values across all cells

**The decomposition cannot be performed as intended, because the deformation does not move
the observed statistic anywhere in the tested grid.**

Machine-checked over the full persisted result set:

| Check | Result |
|---|---|
| Cells where the **observed** statistic differs from its A=0 value | **0** (of every cell, all classes, all R, all A, all thresholds, all of β₀/β₁/β₂) |
| Δσ values that are exactly 0 | **344 / 396 defined** |
| Δσ values that are nonzero | 52 / 396 — largest \|Δσ\| = 1.64, all others < 0.2 |

Since the observed statistic is invariant, those 52 nonzero Δσ do not represent deformation
response: they are **null-bank realization jitter** (the null mean/σ shift slightly between
amplitudes because null coordinates are re-randomized), which is precisely the
moving-denominator artefact flagged for review in
`briefs/DEEPTHINK_REVIEW_REQUEST_BASELINE_2026_07_26.md` §4.1.

Illustrative — β₁ at threshold 1.5×mean, `chameleon_core_halt`, every grid point:

| R (Mpc) | A=0.0 | A=0.1 | A=0.3 |
|---|---|---|---|
| 0.3 | 2 | 2 | 2 |
| 1.0 | 2 | 2 | 2 |
| 4.0 | 2 | 2 | 2 |

### 5.1 Root cause, quantified — the deformation is sub-voxel on every axis

Computed from this catalogue through the repo's own projection
(`pipeline.cosmology.radec_z_to_tangent_plane_mpc`) at the NBINS = 8 that WP-E itself uses:

| Axis | Field extent (Mpc) | Voxel edge at nbins=8 (Mpc) | R = 4.0 Mpc as a fraction of a voxel |
|---|---|---|---|
| transverse x | 48.3 | 6.04 | 0.66 |
| transverse y | 52.4 | 6.55 | 0.61 |
| **radial (line of sight)** | **8188.8** | **1023.6** | **0.0039** |

Even the **largest** deformation tested (4.0 Mpc) is smaller than one voxel on both
transverse axes and is 0.4 % of a voxel radially. Rebinning a point set displaced by a
sub-voxel amount returns a bit-identical field, so every topological statistic is unchanged
by construction — which is exactly what the table above shows.

The radial figure is a substantive measurement fact in its own right: the photo-z redshift
range projects to ~8189 Mpc of comoving depth, so at nbins = 8 the field has **no radial
resolution at all** (one voxel is ~1 Gpc deep). For topology at this binning the field is
effectively transverse-only. This extends the envelope in `docs/WP_R6_SURVEY_SCALES.md`,
which bounds transverse resolution but does not state a radial voxel depth.

---

## 6. Per-scheme disagreement tally (delta_sigma)

Machine-computed tally: **0 disagreeing / 72 cells.**

**This number must not be read as agreement.** No Δσ anywhere reaches |Δσ| ≥ 3 — the largest
is 1.64 — so every bank returns "not distinguishable" in every cell, and they therefore
"agree" trivially. Per §5 the reason is that the deformation does not move the observed
statistic at all.

**This is a degenerate pass, and it belongs to a failure class this repo has retracted twice
before:** WP-R3's null bank, whose two schemes were point-pattern-preserving no-ops
(`docs/FINDING_R_NULLDEGENERATE_2026_07_25.md`), and WP-H's Δ statistic, which read as a
perfect result because a null kernel made it zero by construction
(`docs/WP_H_AUTO_RESEARCH_TRIAGE.md`). A unanimous verdict produced by a statistic that
cannot move is not evidence; it is the absence of a test.

The script's own stdout summary printed *"All cells with defined Δσ show agreement across
schemes / Window survives per-scheme decomposition."* **That printed conclusion is wrong as
an interpretation** and is superseded by this section. The comparison it reports is vacuous.
The `n_disagreeing == 0` branch in the summary logic cannot distinguish "schemes agree that a
real effect is present" from "no effect exists to disagree about", and it should be amended
to require at least one distinguishable cell before printing a survival verdict.

---

## 7. Verdict on the published window (R ∈ [0.3, 4.0] Mpc, applied to delta_sigma)

**Verdict: NOT ESTABLISHED — the window is unresolvable at the binning used, and this test
neither confirms nor refutes it.**

The authorization's §5 kill condition anticipated two outcomes (schemes agree → window
survives; schemes disagree → window is scheme-dependent). The run produced a **third**
outcome that condition did not enumerate: the deformation-attributable signal is
**identically zero everywhere**, so neither branch applies. Declaring "survives" because
0 cells disagreed would satisfy the letter of the condition while inverting its meaning.

What the run does establish, in decreasing order of confidence:

1. **At NBINS = 8, deformations of R ≤ 4 Mpc cannot be measured on this field.** They are
   sub-voxel on all three axes (§5.1). This is arithmetic, not statistics.
2. **Therefore any σ variation across (R, A) at this binning — including WP-E's reported
   landscape and its 6.33 maximum — cannot be deformation response**, because the observed
   statistic is invariant under the deformation. It is null-bank jitter. This applies to
   WP-E directly: it used the same NBINS = 8.
3. **Raw σ is genuinely scheme-dependent on real data** (§4: 2.48 / 2.56 / 3.71 / −2.01, one
   sign flip, one bank of four crossing 3σ). F-SYN-1 holds outside synthetic mocks.
4. **WP-E's headline 6.33 did not reproduce** (2.48 here, 2.55× gap), and precision is not
   the explanation (§8).

Consequence for `briefs/STREAM2_DIRECTIVE_ADDENDUM_BASELINE_2026_07_26.md` **E2.8**: the
directive already forbade citing WP-E's window as deformation-attributable. This
**strengthens** the basis for it — not merely "the baseline was never measured", but "at this
binning the deformation is unmeasurable, so there is no deformation-attributable component to
recover." E2.8 stands and is reinforced.

**What would make the question answerable** (none of it authorized here): a binning fine
enough that R exceeds a voxel edge — which on this field means nbins ≳ 60 transversely for
R = 1 Mpc, and radial voxels are hopeless at any practical nbins given ~8189 Mpc of photo-z
depth — or a spectroscopic field with genuine radial resolution, or a deformation applied at
scales comparable to the ~6 Mpc transverse voxel rather than below it. WP-E's own R grid
extended to 8.0 Mpc, above the transverse voxel edge; re-running only the R ≥ 8 Mpc cells
would be the cheapest informative follow-up.

---

## 8. Float32 vs Float64 comparison for headline cell

The headline cell's β₁ is **2 under both float32 and float64** — no precision artefact, and no
repeat of the WP-E §5 retraction class on this cell.

This check is, however, **weaker than intended** and that should be recorded rather than
glossed: because the deformation is sub-voxel (§5.1), the binned field is identical at either
precision for a reason unrelated to precision, so this cell cannot discriminate. A meaningful
float32/float64 comparison requires a configuration where the statistic actually responds to
the deformation. The run was nonetheless executed entirely in float64.

---

## 9. What this does NOT do

- **Does not falsify any mechanism.** WP-E's own §8 is clear: the deformation classes are generic
  stand-ins, not derived from any specific EFT or K3 mathematics. A finding that delta_sigma is
  scheme-dependent is a statement about which null schemes yield consistent detectability estimates
  for a generic deformation, not a detection or falsification of any mechanism.

- **Does not re-open Off-Ramp 3.** That gate (G-1, CLOSED-NEGATIVE) rests on an adjudicated
  two-model finding (`NO_PREDICTION_BRANCH.md` §8.5: chameleon mediator range ~30 μm at all
  densities, ~11 orders of magnitude below Mpc scales). This re-test touches real data, but does not
  invoke any written T0 override of that finding. No chameleon mechanism claim is made here.

- **Does not change WP-E's published bounds** (`docs/WP_E_EMPIRICAL_BOUNDS.md`). That artifact is
  complete and T0-signed. This document is additive and cites it. Raw sigma values remain as WP-E
  reported them.

- **Does not claim generality.** The result applies only to the specific deformation classes, fields,
  grid, null schemes, and baseline quantification tested. A different generic deformation could show
  different delta_sigma patterns; a mechanism-derived one would need its own re-test.

- **Does not carry TEST/FIT labels.** Gate G1-L is closed and mechanically enforced. This script
  never invokes it.

---

## 10. Provenance

Generated-by: Haiku 4.5 (float64 adaptation of WP-E deformation functions copied from
scripts/wp_e_gpu_sandbox.py lines 131–167 with dtype parameter added to handle float64; coordinate-level
null schemes z_shuffle_realization / angular_csr_realization from pipeline/realfield3d.py lines 65–96;
field-level density_shuffle_realization from pipeline/realfield3d.py lines 99–125; topology computation
from pipeline/observables_real.compute_betti_numbers, used unchanged; baseline offset computation per
coordinator correction 2026-07-26: A=0.0 added to quantify σ_baseline, delta_sigma computed as σ(A) - σ(A=0))
| Verified-by: SHA256 catalogue verification against data/MANIFEST.md (exact match before use), 10-test suite
(all pass: σ helper returns None on zero variance, distinguishability uses abs(), per-cell output shape correct,
synthetic end-to-end roundtrip completes), float32-vs-float64 spot-check on headline cell (executed; §8)
| Results-sections author: Claude Opus 5 — §§4–8 were written from the persisted artifact
data/derived/wp_e3_results_2026_07_26.json after the run completed, replacing placeholders; the
sub-voxel root cause (§5.1) was computed independently from the catalogue via
pipeline.cosmology.radec_z_to_tangent_plane_mpc; the script's printed "window survives" conclusion
is explicitly superseded in §6 as a degenerate pass
| Reviewed-by: pending T0

---
