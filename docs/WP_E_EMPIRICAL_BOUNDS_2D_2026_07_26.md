# WP-E5 Phase 2/3 — 2D transverse detectability envelope (SYNTHETIC)

**Label:** `SYNTHETIC`. Every density field here is a mock. The only external quantity is the
transverse extent of `euclid_z_edf_north`, taken from a committed measurement
(`docs/WP_E4_RESOLVABILITY_FLOOR_2026_07_26.md`), so no real-data access occurs and no
`TEST`/`FIT` label is emitted.
**Date:** 2026-07-26 (revised same day after self-review — see §6)
**Script:** `scripts/wpe_transverse_sweep.py`
**Artifact:** `data/derived/wp_e5_sweep_2026_07_26.json` — 576 cells (2 threshold modes ×
6 occupancies × 8 r_s × 6 α), 5 field realizations each, persisted before any summary printed.
**Companion to, and not a replacement for,** `docs/WP_E_EMPIRICAL_BOUNDS.md` (the 3D study,
T0-signed, untouched).

---

## 0. What this is, and what it is not

This is **not** a bounding box on any mechanism. `void_to_filament_deformation` is a generic
warp chosen independently of the K3 mathematics (WP-E §8), so a cell where it becomes
detectable constrains **that warp** and nothing else. `ZONE_2` is named
`GENERIC_DEFORMATION_EXCLUDED` for exactly that reason.

What it *is*: a measurement of **how much data this statistic would need before it responds at
all** — the question left live by Phase 0's NO-GO on real data and Phase 1's closure failure,
where deformed and undeformed fields gave identical β₁ so the pipeline could not recover a
signal it had injected itself.

## 1. Headline

| Regime | Finding |
|---|---|
| r_s < ~1.6 Mpc | **Never measurable.** Sub-voxel at nbins = 32; 108 cells per mode, all r_s ∈ {0.27, 0.5, 1.0}. |
| n < ~1000 | **Null is degenerate** — σ is not Gaussian-interpretable at all. Includes the real field's 188. |
| n ≈ 2000–5000 | Marginal only: cells cross 3σ in 3 of 5 realizations. |
| **n ≈ 10000, r_s ≈ 6–8 Mpc, α ≥ 0.5** | **Robust detection** — 5/5 realizations, monotone in amplitude, low mask drift. |

The real `edf_north` dz = 0.20 slice holds **188 objects**. Robust detection needs on the order
of **10⁴ in a single slice** — a shortfall of roughly **50×** — and even then only for warps at
6–8 Mpc, well above the ~1.6 Mpc voxel.

## 2. Zone counts

| Zone | `percentile` | `matched_fill` |
|---|---|---|
| `ZONE_0_UNRESOLVABLE` | 108 | 108 |
| `ZONE_0_DEGENERATE_NULL` | 60 | 60 |
| `ZONE_0_UNTESTABLE` | 108 | 109 |
| `ZONE_1_DETECTABLE` | 11 | 9 |
| `ZONE_2_GENERIC_DEFORMATION_EXCLUDED` | 1 | 2 |
| smallest occupancy with any detection | n = 2000 | n = 2000 |
| smallest r_s with any detection | 2.0 Mpc | 4.0 Mpc |

Two independent thresholding conventions agreeing on the occupancy floor is the main
robustness check available here, and it holds.

## 3. Robust cells (`matched_fill`, the clean comparison)

Only cells crossing 3σ in **5 of 5** realizations:

| n | r_s (Mpc) | α | Δσ | mask drift |
|---|---|---|---|---|
| 10000 | 6.0 | 1.0 | +4.74 ± 0.80 | 0.9% |
| 10000 | 6.0 | 2.0 | +5.11 ± 0.56 | 0.9% |
| 10000 | 8.0 | 0.5 | +3.49 ± 0.37 | 6.9% |
| 10000 | 8.0 | 1.0 | +5.19 ± 0.57 | 6.9% |

Everything else that crossed did so in 2–4 realizations of 5. **11 of 20 (n, r_s) rows are
monotone in \|Δσ\| versus amplitude** — a response that does not grow with the amplitude of the
thing causing it is not a response, and the non-monotone rows are all in the high-clipping
regime of §5.

## 4. Two guards were added, and both fired

### 4.1 `ZONE_0_DEGENERATE_NULL` — the statistical sibling of the resolvability guard

`pipeline.resolvability.null_degeneracy()` refuses a null bank that cannot support a Gaussian
σ, on two mechanical criteria: standard deviation below **one count** (β₁ is an integer, so a
sub-unit std makes a single-unit change exceed 1σ), or fewer than **3 distinct values** (no
shape for a tail probability to be read from).

It removes **60 cells per mode**, comprising every cell at n = 188 (null std 0.18, 1.8 distinct
values) and n = 500 (std 0.83). Those are precisely the cells that produced the spurious
detections in the previous revision of this document. The guard is now mechanical rather than
argued in prose, which is the difference that matters: this artifact class has appeared **five
times** in the project (WP-R3, WP-H, WP-E3, the quarantined sweep, and the first revision here).

### 4.2 The α = 0 negative control

**PASS**, 0 violations across all 576 cells and all 5 realizations. It **failed on the previous
run** and caught a real defect — the mass-preservation renormalization in
`void_to_filament_deformation` broke its own documented bit-exact identity by 2 ulp
(1.42 × 10⁻¹⁴). β₁ was unaffected, but a control that cannot assert exactness is not a control.
Fixed at source with regression tests.

## 5. A confound found in this document's own method, and fixed

The first revision thresholded deformed fields at the **baseline's threshold value**. That is
wrong, and measurably so. The binned counts field is discrete, with many cells tied at exactly
the percentile; an arbitrarily small smooth perturbation breaks those ties and pushes the whole
tied block across a fixed threshold. Measured at n = 10000:

| α | mask fill at fixed threshold | β₁ |
|---|---|---|
| 0.0 | 39.6% | 17 |
| **0.01** | **47.8%** | **30** |
| 2.0 | 31.5% | 13 |

So β₁ was tracking **mask size**, not topology. This produced a spurious **+5.06σ at α = 0.01**
— an amplitude far too small to restructure anything — which the previous revision reported as
its strongest cell.

`matched_fill` holds the mask **size** at the baseline's achieved fill, so a β₁ difference
reflects the *arrangement* of mass. Under it, **every α = 0.01 cell returns exactly +0.00** and
the artifact disappears completely.

**Residual effect, stated because it bounds the result:** at large amplitude and large r_s the
deformation clips many cells to exactly zero, re-creating ties and making the target fill
unreachable — mask drift reaches 19.5% at n = 5000, r_s = 10, α = 2.0. The sign flips in that
corner are that clipping, not a topological response. The four robust cells in §3 all sit at
≤ 6.9% drift.

## 6. Retraction of this document's previous numbers

The revision of earlier today reported **"detection needs n ≈ 5000; 32 detectable cells; the
smallest detectable occupancy is n = 188."** **That is withdrawn.** It came from a single mock
realization per cell, a fixed threshold, and no degeneracy guard. Corrected:

| Claim | Previous | Now |
|---|---|---|
| detectable cells | 32 | 12 (`percentile`) / 11 (`matched_fill`) |
| smallest detectable occupancy | n = 188 | n = 2000 (marginal); n ≈ 10000 for 5/5 robustness |
| strongest cell | n = 10000, r_s = 2.0, **α = 0.01**, +5.06σ | artifact of §5; now +0.00 |

Averaging over 5 realizations alone cut detections from 32 to 12 — the single-draw map was
roughly a threefold over-count. Nothing downstream cited the withdrawn numbers; they were
published within this session and are corrected in place, in-band, per D-2.

## 7. Why Δσ here is immune to the objection under review

E2.11's formula is under adversarial review for a moving-denominator defect
(`briefs/DEEPTHINK_REVIEW_REQUEST_BASELINE_2026_07_26.md` §4.1): differencing two σ values
whose denominators both depend on the amplitude is an artifact generator.

**That objection does not reach this implementation.** Both terms are taken against the *same*
null bank, built once from the undeformed field, so the null mean cancels identically:

```
Δσ = σ(α) − σ(0) = (β₁(α) − m)/s − (β₁(0) − m)/s = (β₁(α) − β₁(0)) / s
```

One denominator, and the baseline offset cancels exactly rather than approximately. This does
not resolve the review question for WP-E3's construction, which deformed its null banks too —
it only records that this sweep is not exposed to it.

## 8. For Stream 2

1. **Two floors, both hard:** ~1.6 Mpc in scale and ~10⁴ objects per slice in occupancy. The
   available field misses the second by ~50×.
2. **The real field sits in the degenerate-null regime**, where σ is not interpretable at all —
   not merely "weak evidence", but a regime where the statistic has no meaning.
3. **Under E2.17 this is a complete answer.** A mechanism whose signature falls below either
   floor is untestable by construction with current data, and saying so with the numbers
   attached is a valid M1/M2 deliverable.
4. **Nothing here excludes any mechanism.** G1-L is closed; the warp is generic.

## 9. Reproduction

```bash
PYTHONPATH=. python3 scripts/wpe_transverse_sweep.py   # ~6 min; exits 1 if the control fails
python3 -m pytest pipeline/tests/ checkers/tests/ -q
```

---

`Generated-by: Claude Opus 5 (Stream 3) | Verified-by: executed this session; every number read
back from data/derived/wp_e5_sweep_2026_07_26.json rather than stdout; §5 fill/beta_1 table
measured directly against the deformation operator; §4.1 guard exercised by
pipeline/tests/test_resolvability.py against the actual artifact banks; §7 cancellation checked
algebraically and numerically; zone counts verified to sum to 288 per mode |
Reviewed-by: T0 N — pending Xavier`
