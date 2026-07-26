# WP-E5 Phase 0 — 2D transverse pre-flight on real photo-z data: NO-GO at both dz

**Label:** `SANDBOX-EXPERIMENTAL` (real-data-touching, exploratory; not `TEST`, not `FIT`)
**Date:** 2026-07-26
**Executed by:** Stream 3, `scripts/wpe_preflight_baseline.py`
**Artifact:** `data/derived/wp_e5_preflight_2026_07_26.json` (persisted before this prose)
**Data:** `euclid_z_edf_north`, SHA256 `8b5b287f3f031656…`, nbins = 32, observable β₁ (2D),
40 geometry- and count-matched mocks per slice, gate |σ| ≤ 5.
**Downstream:** Phase 2/3 does **not** proceed. The sweep script is independently quarantined
for unrelated defects (`docs/WP_E5_AUDIT_2026_07_26.md`).

---

## 1. Verdict

| dz | Verdict | Driver |
|---|---|---|
| 0.01 (T0 directive value) | **NO-GO** | σ undefined at every slice and threshold — zero variance in the mock bank |
| 0.20 (documented deviation, σ_z-matched) | **NO-GO** | one slice at σ = 7.31, above the |σ| ≤ 5 baseline gate |

The gate requires every slice × threshold cell to clear; it fails closed. Both dz values fail,
for different reasons, and neither reason is fixable by re-binning.

## 2. Measured numbers

**dz = 0.01** — top-3 slices by occupancy hold 25, 24, 24 objects. Real β₁ = 0 at every slice
and threshold; every mock bank has zero variance, so σ is undefined (9 of 9 cells). This
confirms deviation #1 in `docs/WP_E5_T0_RULING_IMPLEMENTATION_2026_07_26.md` §3 as measurement
rather than estimate: a Δz = 0.01 slice of this field is topologically empty, and it is also
12× finer than the photo-z error kernel (σ_z = 0.119 at the field's median z = 1.39).

**dz = 0.20** — top-3 slices hold 188, 182, 163 objects:

| slice z_lo | n | real β₁ | mock mean | mock std | σ | gate |
|---|---|---|---|---|---|---|
| 0.84 | 188 | 2 | 0.075 | 0.263 | **+7.31** | NO-GO |
| 0.64 | 182 | 1 | 0.200 | 0.458 | +1.75 | GO |
| 1.04 | 163 | 0 | 0.125 | 0.399 | −0.31 | GO |

## 3. Two degeneracies found in the measurement itself

Both were found by reading the persisted JSON, and both matter more than the verdict.

### 3.1 The three-point threshold ladder yields one distinct mask, not three

σ is **bit-identical across 0.5×, 1.0× and 1.5× the field mean** in every one of the nine
dz = 0.20 cells. That is not a coincidence and not a bug in the script — it is arithmetic:

With 188 objects on a 32 × 32 = 1024-bin grid, the mean occupancy is 0.1836 objects per cell.
After normalising the field to mean 1.0, a cell holding *k* objects takes the value
*k* / 0.1836:

| objects in cell | field value |
|---|---|
| 0 | 0.000 |
| 1 | **5.447** |
| 2 | 10.894 |

All three thresholds (0.5, 1.0, 1.5) fall inside the gap (0, 5.447). Every one of them
therefore selects the identical mask — "cell is non-empty". **The threshold ladder carries no
information at this occupancy**; it reports one measurement three times. Any future protocol
quoting agreement across thresholds as robustness evidence on a field this sparse would be
quoting the same number three times.

### 3.2 σ = 7.31 is a near-zero-variance artifact, not a detection

The failing cell reads σ = (2 − 0.075) / 0.263. The mock bank has β₁ = 0 in 37 of 40
realizations, giving a standard deviation of 0.26 — so a real field with β₁ = 2 is
mechanically ≫ 5σ from it. Across all six defined cells, real β₁ ∈ {0, 1, 2} and mock means
lie between 0.075 and 0.2.

**The statistic has no dynamic range at achievable occupancy.** This is the same degeneracy
the 3D β₂ pre-flight recorded
(`data/derived/wp_e_preflight_mock_data_sigma_2026_07_26.json`: β₂ identically zero in real
data *and* mocks at 2 of 3 thresholds, σ undefined). Moving from 3D β₂ to 2D β₁ changed the
observable and the geometry; it did not change the outcome. The 2D framing was given its own
Phase 0 verdict and inherited nothing — and it failed independently.

## 4. What this means for Stream 2

1. **The 2D transverse route does not rescue the measurement.** It was the cheapest remaining
   informative alternative (`briefs/STREAM2_DIRECTIONS_RESOLVABILITY_2026_07_26.md` §5, item 3)
   and it returns NO-GO on real data. Stream 3 has now exhausted the paths that reach a
   ~1 Mpc transverse voxel while keeping non-trivial occupancy.
2. **The binding constraint is object count, not binning.** Refining the grid raises
   resolution and destroys occupancy; coarsening it preserves occupancy and destroys
   resolution. At 2000 objects per field there is no setting where β₁ has both.
3. **No bounding box on (r_s, α) will be delivered.** Per E2.17 and the Phase M directive §1,
   this NO-GO is itself the deliverable: a mechanism whose signature is untestable with
   current data is a complete M1/M2 answer, provided the number is stated. The number is §2
   and §3 above.
4. **Nothing here falsifies or supports any mechanism.** G1-L is closed; no `TEST`/`FIT` label
   is emitted. The deformation classes in the WP-E series are generic stand-ins, not derived
   from the K3 mathematics (WP-E §8).

## 5. What would change the answer

Only more objects. A field with ~10⁴–10⁵ spectroscopic redshifts over a comparable footprint
would give both ~1 Mpc transverse voxels and occupancy sufficient for β₁ to leave {0, 1, 2}.
That is a data-acquisition question, not an analysis question, and nothing in this repo's
current holdings (`data/MANIFEST.md`: 2000 photo-z per Euclid field; 50 spectroscopic in the
largest SDSS field) approaches it.

---

`Generated-by: Claude Opus 5 (Stream 3) | Verified-by: executed against real data this
session, verdict and all numbers read back from data/derived/wp_e5_preflight_2026_07_26.json
(not from stdout); §3.1 quantization derived arithmetically from n=188 on 32x32 and confirmed
against the identical sigma across all three thresholds in the persisted JSON; gate logic read
at scripts/wpe_preflight_baseline.py:266 (fails closed) | Reviewed-by: T0 N — pending Xavier`
