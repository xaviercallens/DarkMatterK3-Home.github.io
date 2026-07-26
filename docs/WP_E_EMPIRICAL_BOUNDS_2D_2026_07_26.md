# WP-E5 Phase 2/3 — 2D transverse detectability envelope (SYNTHETIC)

**Label:** `SYNTHETIC`. Every density field here is a mock. The only external quantity is the
transverse extent of `euclid_z_edf_north`, taken from a committed measurement
(`docs/WP_E4_RESOLVABILITY_FLOOR_2026_07_26.md`), so no real-data access occurs and no
`TEST`/`FIT` label is emitted.
**Date:** 2026-07-26
**Script:** `scripts/wpe_transverse_sweep.py` (rewritten per `docs/WP_E5_AUDIT_2026_07_26.md` §3)
**Artifact:** `data/derived/wp_e5_sweep_2026_07_26.json` — 288 cells, persisted before any
summary was printed.
**Companion to, and not a replacement for,** `docs/WP_E_EMPIRICAL_BOUNDS.md` (the 3D study,
T0-signed, untouched).

---

## 0. What this is, and what it is not

This is **not** a bounding box on any mechanism. `void_to_filament_deformation` is a generic
warp, chosen independently of the K3 mathematics (WP-E §8), so a cell where it becomes
detectable constrains **that warp** and nothing else. `ZONE_2` is named
`GENERIC_DEFORMATION_EXCLUDED` for that reason.

What it *is*: a measurement of **how much data this statistic would need before it responds at
all**. That question became the live one after Phase 0 returned NO-GO on real data
(`docs/WP_E5_PHASE0_PREFLIGHT_2026_07_26.md`) and Phase 1 closure **failed** at the real
field's occupancy — the deformed and undeformed fields gave identical β₁, so the pipeline
could not recover a signal it had injected itself.

## 1. Configuration

| Parameter | Value |
|---|---|
| Field extent | 48.32 × 52.40 Mpc (provenance: voxel 6.04 × 6.55 Mpc at nbins = 8, ×8) |
| nbins | 32 → **voxel 1.510 × 1.637 Mpc** |
| Observable | β₁ (2D; there is no β₂ in 2D) |
| Statistic | **Δσ(α) = σ(α) − σ(0)**, baseline-subtracted per E2.11 |
| Null | density-shuffle, 40 realizations per occupancy |
| Swept | n_objects × r_s × α = 6 × 8 × 6 = **288 cells** |

**α = 0 negative control: PASS**, 0 violations across all 288 cells — Δσ is exactly 0 at zero
deformation, and `amplitude=0` is bit-exact identity. This control **failed on first run** and
caught a real defect; see §4.

## 2. Result

| Zone | Cells |
|---|---|
| `ZONE_0_UNRESOLVABLE` | 108 |
| `ZONE_0_UNTESTABLE` | 148 |
| `ZONE_1_DETECTABLE` (3 ≤ \|Δσ\| < 5) | 11 |
| `ZONE_2_GENERIC_DEFORMATION_EXCLUDED` (\|Δσ\| ≥ 5) | 21 |

**Detectable cells by occupancy** (of 48 per occupancy):

| n_objects | null distinct values | detectable | reading |
|---|---|---|---|
| **188** (real dz = 0.20 slice) | **2** | 2 | **artifact — see §3** |
| 500 | 4 | **0** | |
| 1000 | 12 | **0** | |
| 2000 | 21 | **0** | |
| 5000 | 20 | 7 | first genuine detections |
| 10000 | 16 | 23 | |

### 2.1 The two floors

**Scale floor.** All 108 `ZONE_0_UNRESOLVABLE` cells are exactly r_s ∈ {0.27, 0.5, 1.0} Mpc at
every occupancy — every value below the ~1.57 Mpc mean voxel edge. **No deformation below
~1.6 Mpc is measurable at this binning at any occupancy**, because a sub-voxel displacement
leaves the binned field bit-identical. The smallest r_s that ever produces a detection is
**2.0 Mpc**.

**Occupancy floor.** Detection begins at **n ≈ 5000 objects in a single slice**. The real
`edf_north` dz = 0.20 slice holds **188**. That is a shortfall of roughly **27×**, and ~53× to
reach the n = 10000 regime where most of the r_s ≥ 2 Mpc grid responds even at α = 0.01.

## 3. The n = 188 "detections" are discreteness artifacts, and the sweep's own shape shows it

Two cells at n = 188 (r_s = 2.0, α ∈ {1.0, 2.0}) report Δσ = −4.59. They should not be read as
detections:

1. **The null takes 2 distinct values** ([0, 1]) with std 0.218. β₁ moves 1 → 0, a single unit,
   and dividing one unit by a 0.218 std manufactures a large σ. The Gaussian interpretation of
   σ is not valid on a two-valued null.
2. **Detectability is non-monotonic in n across this boundary**, which a real effect cannot be:
   n = 188 gives 2 detections while n = 500, 1000 and 2000 — all with better-conditioned nulls
   (4, 12 and 21 distinct values) — give **zero**. A signal that vanishes when you add data and
   returns when you add more is an artifact of the sparse regime, not a response to the warp.

This is the same failure mode Phase 0 §3.2 recorded on real data (σ = 7.31 from a null with
β₁ = 0 in 37 of 40) and the same one that produced the quarantined sweep's fabricated bounding
box. **Recorded here as excluded, not as a finding.** The genuine frontier starts at n = 5000.

## 4. The negative control earned its place

The α = 0 control **failed on the first run** with 5 violations, all at n = 5000: `amplitude=0`
was not a bit-exact identity. Cause: the mass-preservation renormalization in
`void_to_filament_deformation` multiplies the field by `original_mass / deformed_mass`, which
is 1.0 only up to float64 rounding — measured at **2 ulp (1.42 × 10⁻¹⁴)**.

β₁ was unaffected (33 → 33), so **no result changed**. But a control that cannot assert
exactness is not a control, and the function's own docstring guarantees the identity. Fixed at
source with a short-circuit at `amplitude == 0`, plus two regression tests (bit-exactness
across six occupancies × three scales, and a no-aliasing check). This is the fourth time this
session that a guard written to fail loudly has caught something a summary would have missed.

## 5. For Stream 2

1. **The actionable number is ~5000 objects per slice, at r_s ≥ 2 Mpc.** Below either floor
   this statistic does not respond, at any amplitude down to α = 0.01.
2. **The current data misses the occupancy floor by ~27×.** Combined with Phase 0's NO-GO and
   Phase 1's closure failure, the three phases agree from three directions: real data, real
   occupancy with synthetic fields, and injected-signal recovery.
3. **Under E2.17 this is a complete answer.** A mechanism whose signature sits below ~1.6 Mpc
   transverse, or which would need a field 27× denser than the one held, is untestable by
   construction with current data — and stating that with the number attached is a valid M1/M2
   deliverable, not a failure.
4. **Nothing here excludes any mechanism.** G1-L is closed. The warp is generic. Any Δσ in the
   table above is a statement about `void_to_filament_deformation`, not about a vacuum.

## 6. Reproduction

```bash
PYTHONPATH=. python3 scripts/wpe_transverse_sweep.py     # ~2 min, exits 1 if the control fails
python3 -m pytest pipeline/tests/test_deformation.py -q  # 13 passed
```

---

`Generated-by: Claude Opus 5 (Stream 3) | Verified-by: executed this session, all numbers read
back from data/derived/wp_e5_sweep_2026_07_26.json rather than stdout; zone counts sum to 288
(108+148+11+21); the 108 UNRESOLVABLE cells confirmed to be exactly r_s in {0.27,0.5,1.0} at
all six occupancies; §3 non-monotonicity read from the per-occupancy detectable counts; §4 ulp
figure measured directly against np.spacing before the fix and re-verified as bit-exact after |
Reviewed-by: T0 N — pending Xavier`
