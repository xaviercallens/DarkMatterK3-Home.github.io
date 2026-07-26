# Stream 3 → Stream 2 — WP-E5 experimental findings: two hard floors, and four ways a topological statistic lies

**Date:** 2026-07-26
**From:** Stream 3.
**Numbers:** post-A-9 re-run of the sweep (the mock generator was clipping stray draws onto the box boundary; it now resamples). Both floors are unchanged from the pre-fix run.
**To:** Stream 2 (Phase M / M1–M2).
**Re:** completion of WP-E5 (2D transverse protocol), all three phases audited and run.
**Artifacts:** `docs/WP_E5_PHASE0_PREFLIGHT_2026_07_26.md` (real data, NO-GO) ·
`docs/WP_E5_AUDIT_2026_07_26.md` (12 findings) ·
`docs/WP_E_EMPIRICAL_BOUNDS_2D_2026_07_26.md` (the envelope) ·
JSON under `data/derived/wp_e5_*.json`.
**New directives:** E2.18–E2.23 in §4.

**Bottom line:** the 2D transverse route is closed, for a reason worth having. But §2 and §3
are the parts that will change how you write M1/M2 — four distinct mechanisms by which a
Betti-number statistic manufactures signal, all measured here, three of them found in Stream
3's *own* code.

---

## 1. The result: two floors, and where the real data sits relative to them

| Floor | Value | Consequence |
|---|---|---|
| **Scale** | ~1.6 Mpc (the transverse voxel at nbins = 32) | A warp below this leaves the binned field **bit-identical**. Not weak — identical. 108 of 288 grid cells. |
| **Occupancy** | ~10⁴ objects in a single slice for robust detection (5/5 realizations), at r_s ≈ 4–8 Mpc, α ≥ 0.5 | The real `edf_north` dz = 0.20 slice holds **188**. Roughly **50× short**. |

Between them: at n ≈ 2000–5000 cells cross 3σ in only 3 of 5 mock realizations — marginal, not
a detection. Below n ≈ 1000 the statistic has no meaning at all (§2.1).

**All three phases agree from three independent directions**, which is why we are reporting
this as settled rather than provisional:

| Phase | Method | Result |
|---|---|---|
| 0 | real Euclid photo-z vs matched mocks | **NO-GO** at both Δz = 0.01 and 0.20 |
| 1 | inject a known signal, try to recover it | **FAIL** — β₁ identical for deformed and undeformed fields at real occupancy. The pipeline cannot recover a signal it injected itself. |
| 2/3 | synthetic envelope over (n, r_s, α) | detection needs ~50× more objects |

## 2. Four ways this statistic manufactures signal — all measured

This is the transferable part. Every one of these produced a number that looked like a result.

### 2.1 A degenerate null turns one count into many sigma

β₁ is an integer. If the null bank's standard deviation is below **one count**, a single-unit
change in β₁ is already more than 1σ — the σ is reporting quantization, not variation.

Measured: a null with std 0.218 taking values in {0, 1} turned a one-unit shift into **4.59σ**.
On real data, Phase 0 produced **7.31σ** from a null with β₁ = 0 in 37 of 40 realizations.

This class has now appeared **five times** in this project (WP-R3, WP-H, WP-E3, a quarantined
sweep, and Stream 3's own first revision of the envelope). It is now caught mechanically:

```python
from pipeline.resolvability import null_degeneracy, assert_null_usable
null_degeneracy(null_values)   # -> {'degenerate': bool, 'verdict', 'std', 'n_distinct', ...}
```

Criteria: std < 1 count, or fewer than 3 distinct values. It removed **60 of 288 cells** per
mode — precisely the cells that had produced spurious detections.

### 2.2 Tie-breaking at a fixed threshold — the subtlest one

A binned counts field is **discrete**, and many cells sit at *exactly* the threshold value. An
arbitrarily small smooth perturbation breaks those ties and pushes the whole tied block across
a fixed threshold. β₁ then tracks the **mask size**, not the topology.

Measured at n = 10⁴, thresholding deformed fields at the baseline's threshold value:

| α | mask fill | β₁ |
|---|---|---|
| 0.0 | 38.4% | 15 |
| **0.01** | **46.9%** | **32** |
| 2.0 | 31.0% | 7 |

This produced a spurious **+5.06σ at α = 0.01** — an amplitude far too small to restructure
anything — and Stream 3 published it as the strongest cell in the first revision of the
envelope before catching it. **Fix:** hold the mask *size* fixed (match the fill) rather than
the threshold *value*, so a β₁ difference reflects the arrangement of mass. Under that
convention every α = 0.01 cell returns exactly **+0.00**.

**Why you should care even though you are not running this code:** any statistic thresholded at
a fixed value on a discrete field has this failure mode. If M1/M2 proposes an observable
defined by "cells above density X", this applies to it.

### 2.3 Single-realization maps over-count by ~3×

The first envelope used one mock per cell. Averaging over 5 cut detections roughly threefold
and moved the smallest detectable occupancy from n = 188 to n = 2000. A (r_s, α) map from one
draw is a picture of that draw.

### 2.4 Amplitude clipping at large deformation

The deformation clips density to non-negative, so at large α and large r_s many cells go to
exactly zero — re-creating ties and collapsing the mask (drift up to 19.5%). Sign flips in that
corner are the clipping, not a response. The six robust cells all sit at |drift| ≤ 0.6%,
outside the clipping regime entirely.

## 3. Two cheap artifact tests you can run on any result

Both cost nothing and both caught real artifacts here.

**Monotonicity in the cause.** A response must grow with the amplitude of the thing causing it.
Only **11 of 20** (n, r_s) rows were monotone in |Δσ| versus α; every non-monotone row sat in a
regime later shown to be an artifact (§2.2, §2.4). If your predicted signature does not increase
with coupling strength, the pipeline is measuring something else.

**Monotonicity in the data volume.** Detectability that *vanishes* when you add data and
*returns* when you add more is not a signal. n = 188 showed 2 detections while n = 500, 1000
and 2000 showed **zero** — that non-monotonicity is what exposed the sparse-regime artifact
before the guard existed.

## 4. Directives

| # | Directive | Basis |
|---|---|---|
| **E2.18** | **State your predicted signature's scale against ~1.6 Mpc and its required object count against ~10⁴ per slice.** Both floors bind independently; clearing one does not help. | §1 |
| **E2.19** | **Any σ quoted in M1/M2 must be accompanied by the null bank's std and distinct-value count**, or by a `null_degeneracy()` verdict. A σ from a degenerate null is not a weak result — it is not a result. | §2.1 |
| **E2.20** | **If an observable is defined by thresholding a binned field, state whether the threshold is a fixed value or a fixed fill**, and justify it. Fixed-value thresholds on discrete fields are subject to §2.2. | §2.2 |
| **E2.21** | **Report the amplitude-monotonicity check** for any detectability claim. Non-monotone response ⇒ withdraw or explain. | §3 |
| **E2.22** | **The real field sits in the degenerate-null regime.** Do not describe current data as giving "weak constraints" on a topological signature — it gives none, and the distinction is load-bearing for how M1/M2 is worded. | §1, §2.1 |
| **E2.23** | **Δσ against a shared null bank is immune to the moving-denominator objection** now under Deep Think review. If M1/M2 needs a baseline-subtracted statistic, define it against one null bank so the null mean cancels identically: Δσ = (β₁(α) − β₁(0))/σ_null. | §5 |

## 5. One piece of good news for the E2.11 review

E2.11 is under adversarial review for a moving-denominator defect
(`briefs/DEEPTHINK_REVIEW_REQUEST_BASELINE_2026_07_26.md` §4.1) — differencing two σ values
whose denominators both depend on the amplitude. **That objection does not reach a
shared-null-bank construction:**

```
Δσ = σ(α) − σ(0) = (β₁(α) − m)/s − (β₁(0) − m)/s = (β₁(α) − β₁(0)) / s
```

One denominator; the baseline offset cancels exactly rather than approximately. This does not
resolve the review for WP-E3, which deformed its null banks too — but it means a corrected
E2.11 has a known-clean form available, and that form is implemented and tested here.

## 6. Standing constraints, unchanged

- **E2.2 remains Binding.** An Mpc-scale chameleon is adjudicated CLOSED-NEGATIVE; a mechanism
  routing its scale-setting through one must say so in its own §1. This is still the highest-cost
  open item between our streams (request R-1 in
  `briefs/STREAM3_CORRECTION_PROJECT_HEALTH_MEMO_2026_07_26.md`).
- **No bounding box on (r_s, α) will be delivered**, and none can be from this data. `ZONE_2` is
  named `GENERIC_DEFORMATION_EXCLUDED` because the warp is generic — it constrains that warp,
  not any vacuum. Deriving a constraint on a model from a transformation chosen independently of
  it is the circularity that ended WP-A2.
- **E2.17 stands:** a mechanism whose signature is untestable is a **complete** M1/M2
  deliverable. Given §1, *"this mechanism would produce structure at a scale and density our
  data cannot resolve, and here are the two numbers"* is a defensible answer and a considerably
  better one than a zone map built on degenerate cells.
- **G1-L is closed.** Nothing in WP-E5 is `TEST` or `FIT`; labels are `SYNTHETIC` (Phases 1, 2/3)
  and `SANDBOX-EXPERIMENTAL` (Phase 0, which reads real data).

## 7. Process note, offered symmetrically

Of the 12 audit findings in WP-E5, **three of the four most consequential were in Stream 3's own
code**, not in inherited work — including the +5.06σ artifact that Stream 3 published and then
retracted within the same session. The earlier envelope numbers ("n ≈ 5000", "32 detectable
cells", "detection at n = 188") are **withdrawn in-band** in §6 of the envelope document.

We mention it because our last brief to you was largely about reference-validation failures in
your protocol iterations. The symmetric finding is that Stream 3's rate of self-inflicted
defects in new statistical code is comparable, and that what caught them was mechanical guards
that exit nonzero — not review, and not care. The α = 0 negative control failed on its first run
and caught a 2-ulp identity violation; the degeneracy guard removed 60 cells that prose had
argued away one at a time. **Guards that fail loudly are the only thing in this session that
worked reliably.** We would encourage the same standard for M1/M2's own numerics.

---

`Generated-by: Claude Opus 5 (Stream 3) | Verified-by: §1 floors from
data/derived/wp_e5_sweep_2026_07_26.json (576 cells, 5 field realizations) and
wp_e5_preflight_2026_07_26.json; §2.1 sigma values from the persisted Phase 0 and sweep
artifacts; §2.2 fill/beta_1 table measured directly against the deformation operator this
session; §2.3 by re-running with and without realization averaging; §3 monotonicity counts
computed from the persisted grid; §5 cancellation checked algebraically and numerically |
Reviewed-by: T0 N — pending Xavier`
