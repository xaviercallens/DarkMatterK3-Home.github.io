# T0 Decision Request — theory-side corrections before the real-data sweep (Si III, patchy reionization, resolution)

**Date:** 2026-09-17 · **From:** Claude (Opus 5), T1 · **To:** T0 (Xavier Callens)
**Status:** DECISION REQUESTED — **blocks the real-data WP-E6-SWEEP run.** New preregistration content
(WP-E6-PIN hard rule); not delegable. Nothing below is implemented on real data.

---

## What's open
The pinned chain (amendment §4/§8, design 2026-09-16, k_eff ruling 2026-09-17) compares the **raw emulator**
prediction, interpolated to k_eff, with the DESI DR1 baseline P1D at z = 4.2. No pinned or LIVE document
says whether any multiplicative correction is applied to the theory first. Two facts make this a real
choice, not a formality:

1. **The emulator's own authors apply corrections before every data comparison.** `lya-mfdm/mcmc.py`
   `log_probability()` multiplies `predict_pk()` by `LyaCorrector.get_total_correction(z)`, the product of
   a pixel-window multiplier, a Si III–Lyα oscillation `1 + a_auto·exp(k/k_auto) + a_cross·exp(k/k_cross)·cos(2271 k)`,
   and (in the `with_patchy` variant) a patchy-reionization factor. Their data are **Boera et al. 2019**,
   not DESI (`lya-mfdm/README.md`), so these amplitudes were set for a different dataset.
2. **The DESI DR1 P1D leaves Si III in the data.** Verified in the paper's text (arXiv:2505.07974, HTML,
   fetched 2026-09-17):
   - §4.2: *"Subtracting P_SB1 removes power contributions from most metals (λ ≳ 1300 Å). However, some
     residual metal contamination remains, such as Si iii 1207 Å, which introduces oscillatory features."*
   - §4.5.1: *"…detecting them in individual redshift bins of P1D remains difficult. Nevertheless,
     marginalizing over these features when performing parameter inference would lead to more robust constraints."*
   - §4.4.4 (resolution): *"If a template-based marginalization is desired…, the theory power spectrum can be
     multiplied by e^{2 b_res k² R_z²} with b_res as a free parameter with a Gaussian prior of σ = 1.5%."*
   - DLAs: *"We assign the redshift-dependent bias found in the companion paper as a correlated error mode"*
     (in the error budget, not left to the user).
   - The paper's *"We do not recommend using these redshift bins"* (z = 4.2, 4.4) refers to the **high-SNR
     variation** only, not the baseline measurement this sweep uses.

## How big — upstream correction factors, at the fiducial point, after K1 interpolation, in σ of C₉,sys

| correction (upstream `lya_corrector_*.pkl`, z = 4.2) | band 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | max |
|---|---|---|---|---|---|---|---|---|---|---|
| pixel window | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
| Si III oscillation | 0.004 | **0.428** | −0.216 | −0.286 | 0.117 | 0.233 | 0.261 | 0.017 | 0.041 | **0.43** |
| patchy reionization | **0.511** | 0.443 | 0.396 | 0.362 | 0.309 | 0.233 | 0.153 | 0.042 | −0.064 | **0.51** |
| upstream total, `with_patchy` | 0.515 | **0.880** | 0.176 | 0.071 | 0.428 | 0.469 | 0.417 | 0.060 | −0.022 | **0.88** |

Pixel window: negligible. Si III and patchy: each up to about half a σ per band, correlated across bands.
Ignoring or including them could move an exclusion contour.

## Decisions requested (three separate items)

**C1 — Si III.** Options:
- (a) **No Si III term.** Knowingly leaves a documented data feature unmodeled.
- (b) **Upstream's fixed Si III factor.** No new free parameter, but its amplitudes were set on Boera et al.
  2019 high-resolution data, not DESI.
- (c) **Free Si III amplitude, profiled as a 5th nuisance**, following DESI's own recommendation. This changes
  the pinned statistic: 5 nuisances → **4 dof** per cell (Δχ² contours stay 2 dof), and `Chi2Profiler`
  (fixed to 4 nuisances) needs extending. A prior range for the amplitude must be pinned too.

**C2 — Patchy reionization** (a theory-side correction to the simulations, independent of which dataset is used):
- (a) not applied; (b) upstream's fixed `with_patchy` factor.
  Upstream ships both variants; its README's headline posterior file is `corner_cut_with_patchy_fixed_f_95.pdf`.

**C3 — Resolution template:** (a) none; (b) DESI's e^{2 b_res k² R_z²} with b_res profiled under a 1.5 %
Gaussian prior. (b) also adds a nuisance, with the same dof consequence as C1(c).

## T1 recommendation (engineering reasons; the decision is T0's)
- **C1: (c).** The data provider states the feature remains and recommends marginalizing it. The only fixed
  amplitude on hand was set on a different dataset, so (b) would import a calibration choice this repo cannot
  justify, and (a) ignores a documented ~0.4σ-scale effect.
- **C2: (b).** It corrects the simulations, not the data. The emulator authors apply it in their headline result.
- **C3: (a) for now, provided its size is measured before pinning.** The template's effect at our k ≤ 0.045 s/km
  has not been computed here; if it is ≥ 0.1σ in any band, revisit as (b).

Whatever is ruled goes into a pinned note (commit-as-pin), a `TUNING_LOG.md` row, and, for any added nuisance,
a pinned bound or prior before any real-data run. Every output stays `exclusion`/`FIT`.

## What proceeds meanwhile (no real data)
The sweep driver is written with the correction model as a **required** input and a **hard refusal to load
the real observed vector** until a pinned C1–C3 ruling exists. It is validated by injection and recovery on
emulator-generated synthetic data only.

---
*Generated-by: Claude (Opus 5) | Verified-by: correction factors read from `lya-mfdm` 9182aa4 pickles and
`mcmc.py`; σ-sizes computed with `pipeline/keff.py` K1 + C₉,sys; DESI quotes checked against the arXiv HTML text |
Reviewed-by: T0 — pending*
