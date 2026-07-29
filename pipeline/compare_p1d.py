#!/usr/bin/env python3
"""
WP-E6-P2C — Fixed FFT P1D masking estimator + mock-calibrated window correction.

Relocated/refactored from `phase1_work/agent3_synthetic/compare_p1d.py` (gitignored
scratch script that loads local desisim/quickspectra output files at import time) into
`pipeline/` so the *fix* is part of the tracked audit trail, importable and testable
without desisim/DESIMODEL. The original script is left untouched; this module is the
canonical successor for `flux_power_1d()` and the masking-bias correction referenced by
`briefs/ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md` Part C and
`briefs/EXECUTION_PLAN_2026_07_29_TWISTED_AND_WPE6.md` WP-E6-P2C.

label: CONTROL / ENGINEERING (NOT TEST, NOT FIT — prereg-pipeline skill / CLAUDE.md rule
3). This module operates entirely on synthetic (desisim-mock or, for the lightweight
tests here, hand-rolled Gaussian-process-style) spectra. It touches no pinned prediction
and no real DESI data.

--------------------------------------------------------------------------------
Two bugs fixed (per `phase1_work/agent3_synthetic/compare_p1d.py` L44-L62, reproduced
verbatim in `briefs/ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md` Sec 3.1, and in the legacy
reimplementation `pipeline/tests/test_compare_p1d.py::_legacy_buggy_flux_power_1d` used
to prove these fixes actually change behavior):

  Bug 1 (edge-discontinuity artifact): masked pixels were zero-filled in the FLUX array
  before the FFT. A sharp jump from the true flux value to exactly 0 at every masked
  pixel is not part of the physical signal and leaks power across all k via the implicit
  rectangular window on each gap.

  Bug 2 (biased mean, previously unflagged): the per-spectrum mean subtracted before the
  FFT was computed over ALL pixels INCLUDING the zero-filled ones
  (`flux.mean(axis=1)` on the already-masked array), biasing the subtracted mean low by
  `MASK_FRAC x (true mean flux)` and compounding Bug 1 -- the field that gets FFT'd was
  `(true_flux - biased_mean)` at good pixels and `(0 - biased_mean)` at masked pixels, an
  even sharper discontinuity than zero-fill alone would cause.

Fix applied here, in order (Bug 2 must be fixed first so the window-correction
calibration below measures one clean artifact, not two entangled ones):
  1. Compute the per-spectrum mean over UNMASKED pixels only (`_masked_mean`).
  2. Subtract that corrected mean, then impose delta_F = 0 exactly at masked pixels.
     This is not "avoiding" zero-fill -- it is *exactly* the convention the real DESI
     pipeline uses (see paper citation below): delta_F = 0 at masked pixels is
     equivalent to setting the masked pixel's flux to the (correctly computed) mean
     transmitted flux. The residual bias this convention still introduces is what the
     window correction below corrects for.
  3. Apply a mock-calibrated multiplicative window correction A(k), fit from an ensemble
     of (clean, masked) mock realizations -- reusing WP-E6-P2A's desisim ensemble when
     available (see `calibrate_window_correction`).

--------------------------------------------------------------------------------
Paper verification (mandatory first step of WP-E6-P2C)

`briefs/ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md` Sec 3.2 explicitly flags its masking-bias
recipe as reconstructed from a WebSearch summary, NOT a verbatim paper read, and asks the
implementer to verify against the paper's own methods section before coding the exact
functional form. That verification was done for this module by fetching and reading the
actual paper PDF (arxiv.org/pdf/2306.06311, retrieved 2026-07-29; WebFetch on the arXiv
abstract page alone returns only metadata, consistent with the DRAFT's own note -- the
PDF had to be downloaded and parsed directly).

Ravoux et al. 2023, "The Dark Energy Spectroscopic Instrument: One-dimensional power
spectrum from first Lyman-alpha forest samples with Fast Fourier Transform", MNRAS 526,
5118 (arXiv:2306.06311):

  - Sec 3.1 "Continuum fitting", eq. (1): delta_F(lambda) = F(lambda)/F_bar(lambda) - 1
    (flux contrast definition).
  - Sec 5 "SYNTHETIC DATA CORRECTIONS" -> Sec 5.3 "Spectrum pixel masking" (page 14):
    "...when computing the Fourier transform, we impose a value of delta_F = 0
    (equivalent to mean transmitted flux fraction value for F) and infinite standard
    deviation to the masked spectrum pixels. This masking introduces a k-dependent
    bias, which we need to quantify." -- i.e. the paper's OWN pipeline does the
    zero-in-the-contrast-field convention (Bug 1's mechanism), and corrects the
    resulting bias empirically rather than avoiding the convention.
  - Sec 5.3, unlabeled eq. block immediately preceding eq. (22)/(23): "The coefficients
    used for both masking corrections are defined as the ratio between the UNMASKED and
    the MASKED power spectra":
        eq. (22): A_line(k,z) = P_1D,alpha,CONT(k,z) / P_1D,alpha,LINEm(k,z)
        eq. (23): A_dla(k,z)  = P_1D,alpha,CONT(k,z) / P_1D,alpha,DLAm(k,z)
    (CONT = mock with standard pipeline, no masking applied; LINEm/DLAm = mock with
    atmospheric-line / DLA masking applied, everything else identical.) Sec 5.3.1: "We
    choose to model A_line(k,z) by a second-order polynomial fit and use this correction
    in the final calculation of P_1D,alpha." Sec 5.3.2: DLA correction is instead
    k-independent (a single scalar per z, ~0.5% amplitude) since its impact is smooth in k.

  This pipeline's `MASK_FRAC` random masking is a broadband stand-in (not concentrated
  in narrow atmospheric-line-like regions, not DLA-like either) -- closer in character to
  the atmospheric-line case (broadband, describable across the full k range per
  ANALYSIS_PROTOCOL Sec 3.3's own reasoning), so `calibrate_window_correction` below
  defaults to the paper's Sec 5.3.1 recipe: a 2nd-order polynomial fit in k, not a
  k-independent constant.

  ** DELTA FROM THE LIVE ANALYSIS_PROTOCOL_DRAFT, FLAGGED FOR T0 (do not silently
  resolve): ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md L290 states "the ratio p_masked /
  p_clean IS the correction function". The verified paper recipe (eq. 22/23 above) is the
  OPPOSITE ratio: A(k,z) = P_unmasked / P_masked, applied by MULTIPLYING the masked
  (measured) power by A(k,z) to recover an estimate of the unmasked truth. Using the
  DRAFT's stated ratio directly (p_masked/p_clean) would apply the correction backwards
  (squaring the bias instead of removing it). This module implements the paper-verified
  direction (`calibrate_window_correction` returns A = clean/masked); see
  `briefs/WP_E6_P2C_MASKING_FIX_2026_07_29.md` for the full delta report. **
"""
import numpy as np


def _masked_mean(flux, mask):
    """Per-spectrum mean computed over UNMASKED pixels only (Bug 2 fix).

    `flux`: [nspec, npix]. `mask`: boolean [nspec, npix], True = masked/bad pixel.
    Robust regardless of what value `flux` currently holds at masked positions (zero,
    the original physical value, or anything else) -- masked entries are excluded from
    the sum via `np.where`, not relied upon to already be zero.
    """
    good = ~mask
    counts = good.sum(axis=1, keepdims=True)
    if np.any(counts == 0):
        raise ValueError("At least one spectrum is fully masked; cannot compute a mean.")
    sums = np.where(good, flux, 0.0).sum(axis=1, keepdims=True)
    return sums / counts


def flux_power_1d(flux, dv_kms, mask=None, window_correction=None, return_per_spectrum=False):
    """Per-spectrum |FFT|^2 P1D estimate in velocity space (km/s), mean-subtracted,
    averaged over spectra (unless `return_per_spectrum=True`). Returns (k [s/km], P1D).

    `mask`: optional boolean [nspec, npix], True = masked pixel. When given:
      - the per-spectrum mean subtracted is computed over UNMASKED pixels only (Bug 2 fix,
        `_masked_mean`);
      - masked pixels are then set to delta_F = 0 exactly, matching the real DESI
        pipeline's own convention (Ravoux et al. 2023 Sec 5.3 -- see module docstring).
    `window_correction`: optional per-k multiplicative array A(k), paper eq. (22)/(23)
      form (A = P_unmasked / P_masked from a mock ensemble; see
      `calibrate_window_correction`), applied to the returned (masked) power to correct
      the residual masking-window bias. Must have length `npix // 2 + 1` matching `k`.
    `return_per_spectrum`: if True, return the [nspec, nk] array before averaging over
      spectra (needed by WP-E6-P2A to build the sample covariance from raw realizations,
      per ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md Sec 1.2).
    """
    flux = np.asarray(flux, dtype=float)
    nspec, npix = flux.shape
    if mask is None:
        mean = flux.mean(axis=1, keepdims=True)
        d = flux - mean
    else:
        mask = np.asarray(mask, dtype=bool)
        if mask.shape != flux.shape:
            raise ValueError(f"mask shape {mask.shape} != flux shape {flux.shape}")
        mean = _masked_mean(flux, mask)
        d = flux - mean
        d[mask] = 0.0  # delta_F = 0 at masked pixels (Ravoux et al. 2023 Sec 5.3)

    fft = np.fft.rfft(d, axis=1)
    power = (np.abs(fft) ** 2) * dv_kms / npix
    k = np.fft.rfftfreq(npix, d=dv_kms) * 2 * np.pi

    if window_correction is not None:
        window_correction = np.asarray(window_correction, dtype=float)
        if window_correction.shape != k.shape:
            raise ValueError(
                f"window_correction shape {window_correction.shape} != k shape {k.shape}"
            )
        power = power * window_correction[np.newaxis, :]

    if return_per_spectrum:
        return k, power
    return k, power.mean(axis=0)


def calibrate_window_correction(p_clean_ensemble, p_masked_ensemble, k, poly_degree=2):
    """Mock-calibrated multiplicative window correction, Ravoux et al. 2023 Sec 5.3,
    eq. (22)/(23) form: A(k) = <P_unmasked>_ensemble / <P_masked>_ensemble, fit with a
    low-order polynomial in k (paper's Sec 5.3.1 atmospheric-line recipe -- the closer
    analog to this pipeline's broadband random masking; see module docstring for why the
    Sec 5.3.2 k-independent-constant DLA recipe is not used here).

    `p_clean_ensemble`, `p_masked_ensemble`: [N, nk] arrays -- N independent mock
    realizations' P1D computed WITHOUT and WITH masking respectively, on the SAME
    underlying realizations (paired), via `flux_power_1d(..., return_per_spectrum=True)`
    or an externally supplied ensemble (e.g. WP-E6-P2A's desisim mocks). `p_masked_ensemble`
    must already have Bug 2 fixed (i.e. be the output of THIS module's `flux_power_1d`,
    not the legacy buggy estimator) -- calibrating against a still-buggy masked estimator
    would bake Bug 2's artifact into the "correction" instead of removing it.
    `k`: the shared k-array (s/km), used only for the polynomial fit's x-axis.

    Returns (correction, coeffs, raw_ratio): `correction` is the polynomial-smoothed A(k)
    evaluated at `k` (what to pass as `flux_power_1d`'s `window_correction`); `coeffs` are
    the `np.polyfit` coefficients; `raw_ratio` is the unsmoothed ensemble-mean ratio
    (diagnostic / for the before-after report).
    """
    p_clean_ensemble = np.asarray(p_clean_ensemble, dtype=float)
    p_masked_ensemble = np.asarray(p_masked_ensemble, dtype=float)
    if p_clean_ensemble.shape != p_masked_ensemble.shape:
        raise ValueError(
            f"clean ensemble shape {p_clean_ensemble.shape} != "
            f"masked ensemble shape {p_masked_ensemble.shape}"
        )
    p_clean_mean = p_clean_ensemble.mean(axis=0)
    p_masked_mean = p_masked_ensemble.mean(axis=0)
    if np.any(p_masked_mean <= 0):
        raise ValueError("masked ensemble mean power has a non-positive bin; cannot form ratio")

    raw_ratio = p_clean_mean / p_masked_mean  # A(k) = P_unmasked / P_masked, eq. (22)/(23)
    coeffs = np.polyfit(k, raw_ratio, deg=poly_degree)
    correction = np.polyval(coeffs, k)
    return correction, coeffs, raw_ratio


# Generated-by: Sonnet (Stream 3 agent, WP-E6-P2C) | Verified-by: pipeline/tests/test_compare_p1d.py
# | Reviewed-by: pending T0 (Xavier) -- see flagged DRAFT-vs-paper delta above and in
# briefs/WP_E6_P2C_MASKING_FIX_2026_07_29.md
