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
Gaussian prior. (b) also adds a nuisance, with the same dof consequence as C1(c). *(See addendum: DESI §5.4 makes
(a) the provider's default.)*

## T1 recommendation (engineering reasons; the decision is T0's)
- **C1: (c).** The data provider states the feature remains and recommends marginalizing it. The only fixed
  amplitude on hand was set on a different dataset, so (b) would import a calibration choice this repo cannot
  justify, and (a) ignores a documented ~0.4σ-scale effect.
- **C2: (b).** It corrects the simulations, not the data. The emulator authors apply it in their headline result.
- **C3: (a).** *(Revised in the addendum: DESI §5.4 item 3 states the covariance's correlated template already
  handles resolution systematics "without extra parameters".)*

Whatever is ruled goes into a pinned note (commit-as-pin), a `TUNING_LOG.md` row, and, for any added nuisance,
a pinned bound or prior before any real-data run. Every output stays `exclusion`/`FIT`.

## What proceeds meanwhile (no real data)
The sweep driver is written with the correction model as a **required** input and a **hard refusal to load
the real observed vector** until a pinned C1–C3 ruling exists. It is validated by injection and recovery on
emulator-generated synthetic data only.


---

## Addendum (same day): DESI §5.4 "Recommendations for use" — three more items, plus C1 is broader

Verbatim from arXiv:2505.07974 §5.4 (HTML text, checked 2026-09-17):
> 1. Apply the redshift-dependent k scale cut: 10⁻³ s km⁻¹ < k < 0.5π/R_z, where R_z ≡ cΔλ_DESI/(1+z)λ_Lyα and Δλ_DESI = 0.8 Å.
> 2. Do not use redshift bins of 4.2 and 4.4 of the high-SNR sample since the covariance matrix is not reliable due to low statistics in these bins.
> 3. Use the full covariance matrix. The correlated template marginalization handles the systematics we discussed without extra parameters. […] If an alternative marginalization is desired for the resolution systematics, remove its contribution from the covariance matrix and multiply the theory power spectrum by e^{2b_res k² R_z²} and apply a Gaussian prior of σ = 1.5% to b_res.
> 4. Model both Si iii and Si ii oscillations as well as Mg ii and C iv residual doublet contaminations. […]
> 5. If a bad χ²_ν is encountered, which is likely to happen, inflate the diagonals of the covariance matrix until you obtain χ²_ν ∼ 1. Our ad-hoc additive diagonal term in the forest bias measurement is redshift-dependent, which we provide separately, and can be included from the beginning if desired.

Consequences for this sweep:
- **Item 2:** does not apply (baseline sample, not high-SNR). ✔
- **Item 3:** the full covariance is already used. ✔ C3 → (a) is the provider's own default.
- **Item 1 — NEW, C4 (k cut).** At z = 4.2: R_z = 37.94 km/s, so k_max = **0.0414 s/km** (log₁₀ = −1.383).
  The pinned aggregation cut only at Nyquist (0.0527). **Band 8 has 3 of 10 members at k = 0.0419–0.0439 s/km,
  beyond the recommended cut, carrying 29 % of band 8's weight.** Bands 0–7 are unaffected. Options:
  (a) keep, against the provider's recommendation; (b) **drop those 3 members** and re-aggregate band 8 from 7
  members, which changes P₉,₈, C₉'s row/column 8 and k_eff,8, so the K2 β₈ must be re-derived by re-running
  the pre-check (a new pin); (c) drop band 8 (8 bands; 4 dof per cell).
- **Item 4 — C1 is broader than Si III.** The provider asks for Si III **and Si II** oscillations **and Mg II and
  C IV** doublet templates. With 9 bands and 4 IGM nuisances, adding all four amplitudes leaves **1 dof** per cell
  for goodness of fit. The exclusion statistic (Δχ², 2 dof, Wilks) is unaffected by profiled nuisances.
  Options: (c-full) all four profiled; (c-SiIII) Si III only, the "indubitable" 2270 km/s peak (§4.5.1),
  giving 4 dof; (b)/(a) as before.
- **Item 5 — NEW, C5 (χ²_ν).** Options: (a) no inflation — report per-cell χ²_min/5 dof honestly, with a bad
  χ²_ν flagged, not repaired; (b) apply **DESI's own published additive diagonal term** for z = 4.2 as a fixed input
  (it must be located and hash-pinned first; not yet on disk); (c) inflate until χ²_ν ∼ 1 ourselves. **(c) tunes the
  covariance on the data being fit**; it is listed because the provider suggests it, and T1 recommends against it here.

**Revised T1 recommendation (the decision is T0's):**
- **C1 → (c-SiIII)** now, 4 dof; Si II / Mg II / C IV logged as a known limitation rather than profiled with 1 dof left.
- **C2 → (b)** (unchanged).
- **C3 → (a)** (provider default).
- **C4 → (b)** drop the 3 out-of-cut members and re-run the band-8 aggregation and pre-check under a new pin.
  It follows the provider's explicit cut and touches one band.
- **C5 → (b) if DESI's term can be obtained and hash-pinned, otherwise (a).** Never (c).

---
*Generated-by: Claude (Opus 5) | Verified-by: correction factors read from `lya-mfdm` 9182aa4 pickles and
`mcmc.py`; σ-sizes computed with `pipeline/keff.py` K1 + C₉,sys; DESI quotes (incl. §5.4) checked against the arXiv HTML text; band-8 k-cut count from the tracked aggregation JSON |
Reviewed-by: T0 — pending*
