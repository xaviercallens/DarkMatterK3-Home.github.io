#!/usr/bin/env python3
"""Regression tests for pipeline/compare_p1d.py (WP-E6-P2C masking fix).

No network access; deterministic (fixed seeds throughout). SYNTHETIC DATA ONLY,
ENGINEERING/CONTROL -- see pipeline/compare_p1d.py module docstring. This test suite is
built to prove the two masking bugs described there are actually fixed, not just that the
new code runs:

  1. `_legacy_buggy_flux_power_1d` below is a verbatim reimplementation of the ORIGINAL
     buggy estimator (`phase1_work/agent3_synthetic/compare_p1d.py` L54-L62: zero-fill
     masked pixels, THEN take the mean over all pixels including the zeros). Every test
     that references it demonstrates the legacy code producing a wrong/spurious result
     that `pipeline.compare_p1d.flux_power_1d` does not.
  2. A deterministic flat-spectrum case (test_bug1_and_bug2_flat_spectrum_exact) proves
     both bugs at once with exact arithmetic: a spectrum with genuinely zero fluctuation
     must produce exactly zero power once correctly masked; the legacy estimator does not.
  3. test_calibrate_window_correction_recovers_known_bias proves the correction direction
     (A = clean/masked, Ravoux et al. 2023 eq. 22/23) against a known injected bias
     function -- this is the test that would catch the ANALYSIS_PROTOCOL_DRAFT direction
     error (masked/clean) flagged in the module docstring and the WP-E6-P2C brief.
  4. test_ensemble_before_after_reduces_bias is the full pipeline integration check used
     to generate the before/after numbers reported in
     briefs/WP_E6_P2C_MASKING_FIX_2026_07_29.md.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.compare_p1d import (  # noqa: E402
    _masked_mean,
    calibrate_window_correction,
    flux_power_1d,
)


def _legacy_buggy_flux_power_1d(flux, dv_kms):
    """Verbatim reimplementation of the ORIGINAL buggy estimator, for regression
    comparison only -- never used in production code. Mirrors
    phase1_work/agent3_synthetic/compare_p1d.py L54-L62 exactly: caller has already
    zero-filled masked pixels into `flux`; this function then (buggily) takes the mean
    over ALL pixels, including the zero-filled ones (Bug 2), on top of the zero-fill
    edge discontinuity itself (Bug 1)."""
    nspec, npix = flux.shape
    d = flux - flux.mean(axis=1, keepdims=True)
    fft = np.fft.rfft(d, axis=1)
    power = (np.abs(fft) ** 2) * dv_kms / npix
    k = np.fft.rfftfreq(npix, d=dv_kms) * 2 * np.pi
    return k, power.mean(axis=0)


def _colored_noise_realization(rng, npix=256, corr_len=6.0, amp=0.05, noise_amp=0.02,
                                mean_level=1.0):
    """Synthetic stand-in for a desisim mock realization's flux field: a correlated
    (colored) Gaussian component plus an uncorrelated (white) noise floor around a flat
    continuum -- roughly Lya-forest-contrast-like in that the true P1D has both a
    large-scale-dominated signal and a flat high-k noise floor, which keeps the
    clean/masked power ratio well-conditioned (order-unity, smooth in k) over the fitted
    range instead of decaying through many orders of magnitude, matching the qualitative
    shape of Ravoux et al. 2023 Fig 14/15 (ratios O(0.9-1.05), smooth in k). NOT a
    physical Lya forest model and NOT desisim -- used here only because WP-E6-P2A's real
    desisim ensemble (data/derived/wp_e6_covariance_2026_07_29.json) had not landed yet
    when this test/brief was written; see briefs/WP_E6_P2C_MASKING_FIX_2026_07_29.md for
    the explicit note on reusing the real ensemble once available."""
    white = rng.standard_normal(npix)
    x = np.arange(npix)
    kernel = np.exp(-0.5 * (x - npix // 2) ** 2 / corr_len ** 2)
    kernel /= np.sqrt((kernel ** 2).sum())
    field = np.convolve(white, kernel, mode="same")
    noise = rng.standard_normal(npix)
    return mean_level + amp * field + noise_amp * noise


def _make_ensemble(n, npix=256, mask_frac=0.03, seed=0):
    """N independent (flux, mask) pairs sharing one mask draw per pixel-position
    distribution but independent noise realizations and independent mask draws (mirrors
    the real pipeline: MASK_FRAC applied independently per realization)."""
    rng = np.random.RandomState(seed)
    fluxes = np.stack([_colored_noise_realization(rng, npix=npix) for _ in range(n)])
    mask_rng = np.random.RandomState(seed + 1)
    masks = mask_rng.rand(n, npix) < mask_frac
    return fluxes, masks


# ---------------------------------------------------------------------------
# Bug 2 (biased mean) -- isolated unit test
# ---------------------------------------------------------------------------

def test_bug2_masked_mean_excludes_masked_pixels():
    flux = np.array([[10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 100.0, 100.0]])
    mask = np.array([[False, False, False, False, False, False, True, True]])

    correct_mean = _masked_mean(flux, mask)
    assert np.allclose(correct_mean, 10.0), "mean over unmasked pixels only must be 10.0"

    naive_mean_over_all = flux.mean(axis=1, keepdims=True)
    assert not np.allclose(naive_mean_over_all, 10.0), (
        "sanity check: the naive (buggy) mean-over-all-pixels must differ from the "
        "corrected mean in this constructed case, otherwise the test proves nothing"
    )


# ---------------------------------------------------------------------------
# Bug 1 + Bug 2 combined -- deterministic exact-arithmetic regression test
# ---------------------------------------------------------------------------

def test_bug1_and_bug2_flat_spectrum_exact():
    """A perfectly flat spectrum (zero true fluctuation) with two masked pixels. The
    correct P1D of a flat spectrum is exactly zero at every k. The legacy estimator
    (zero-fill then mean-over-all) must NOT return zero -- proving both bugs are live in
    the old code. The fixed estimator must return exactly zero -- proving both are fixed."""
    dv_kms = 50.0
    flux = np.array([[10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]])
    mask = np.array([[False, False, False, False, False, False, True, True]])

    # Legacy path: caller pre-zero-fills, then legacy estimator runs its buggy mean.
    flux_zerofilled = flux.copy()
    flux_zerofilled[mask] = 0.0
    k_legacy, p_legacy = _legacy_buggy_flux_power_1d(flux_zerofilled, dv_kms)

    # Fixed path: pass the ORIGINAL (not pre-zeroed) flux plus the mask.
    k_fixed, p_fixed = flux_power_1d(flux, dv_kms, mask=mask)

    assert np.allclose(k_legacy, k_fixed)
    assert p_legacy.sum() > 1e-6, (
        "FAILS-ON-OLD-CODE CHECK: legacy estimator must show spurious nonzero power "
        "on a flat (zero-signal) spectrum -- if this assertion fails, the legacy "
        "reimplementation is not faithfully reproducing the original bugs"
    )
    assert np.allclose(p_fixed, 0.0, atol=1e-10), (
        "PASSES-ON-FIX CHECK: fixed estimator must recover exactly zero power on a "
        "flat spectrum once masking is handled correctly"
    )


def test_flux_power_1d_no_mask_matches_naive_unmasked_calc():
    """Backward-compatibility: with mask=None, behavior must be identical to a plain
    (unmasked) mean-subtracted FFT -- the fix must not change unmasked behavior."""
    rng = np.random.RandomState(7)
    flux = 1.0 + 0.1 * rng.standard_normal((5, 64))
    dv_kms = 30.0

    k, p = flux_power_1d(flux, dv_kms, mask=None)

    d = flux - flux.mean(axis=1, keepdims=True)
    fft = np.fft.rfft(d, axis=1)
    expected_power = ((np.abs(fft) ** 2) * dv_kms / 64).mean(axis=0)
    expected_k = np.fft.rfftfreq(64, d=dv_kms) * 2 * np.pi

    assert np.allclose(k, expected_k)
    assert np.allclose(p, expected_power)


def test_flux_power_1d_zero_mask_frac_matches_unmasked():
    """Negative control: mask array of all-False must reduce to the unmasked case."""
    rng = np.random.RandomState(11)
    flux = 1.0 + 0.1 * rng.standard_normal((4, 32))
    mask = np.zeros_like(flux, dtype=bool)
    dv_kms = 40.0

    k_masked, p_masked = flux_power_1d(flux, dv_kms, mask=mask)
    k_unmasked, p_unmasked = flux_power_1d(flux, dv_kms, mask=None)

    assert np.allclose(k_masked, k_unmasked)
    assert np.allclose(p_masked, p_unmasked)


def test_flux_power_1d_return_per_spectrum_shape():
    """Needed by WP-E6-P2A (ANALYSIS_PROTOCOL_DRAFT Sec 1.2): return_per_spectrum=True
    must return the [nspec, nk] array, not collapsed over the realization axis."""
    rng = np.random.RandomState(3)
    flux = 1.0 + 0.1 * rng.standard_normal((9, 40))
    mask = rng.rand(9, 40) < 0.03
    dv_kms = 25.0

    k, p_per_spec = flux_power_1d(flux, dv_kms, mask=mask, return_per_spectrum=True)
    nk = len(k)
    assert p_per_spec.shape == (9, nk)

    # Averaging manually must match the collapsed-return path.
    _, p_mean = flux_power_1d(flux, dv_kms, mask=mask, return_per_spectrum=False)
    assert np.allclose(p_per_spec.mean(axis=0), p_mean)


# ---------------------------------------------------------------------------
# Window correction: direction + recovery of a known bias
# ---------------------------------------------------------------------------

def test_calibrate_window_correction_recovers_known_bias():
    """Inject a KNOWN, k-dependent multiplicative bias (masked = clean / true_A(k)) and
    verify calibrate_window_correction recovers true_A(k) -- this pins the correction
    DIRECTION to the paper-verified A = P_unmasked / P_masked (Ravoux et al. 2023 eq.
    22/23), not the inverse. If the implementation used the ANALYSIS_PROTOCOL_DRAFT's
    stated (and paper-disagreeing) ratio p_masked/p_clean, this test would fail."""
    rng = np.random.RandomState(21)
    nk = 20
    k = np.linspace(0.01, 0.5, nk)
    true_A = 1.0 + 0.6 * k - 0.3 * k ** 2  # arbitrary, non-trivial, non-self-inverse quadratic

    n_real = 50
    p_clean_ensemble = rng.uniform(1.0, 5.0, size=(n_real, nk))  # arbitrary positive "true" P1D
    p_masked_ensemble = p_clean_ensemble / true_A[np.newaxis, :]

    correction, coeffs, raw_ratio = calibrate_window_correction(
        p_clean_ensemble, p_masked_ensemble, k, poly_degree=2
    )

    assert np.allclose(raw_ratio, true_A, rtol=1e-9), (
        "raw ensemble-mean ratio must equal the injected true bias exactly for "
        "noiseless synthetic data with the correct (clean/masked) direction"
    )
    assert np.allclose(correction, true_A, rtol=1e-6), (
        "polynomial-fit correction must recover the known quadratic bias"
    )

    # Explicitly rule out the inverted (wrong) direction as a false pass.
    wrong_direction_ratio = p_masked_ensemble.mean(axis=0) / p_clean_ensemble.mean(axis=0)
    assert not np.allclose(wrong_direction_ratio, true_A, rtol=1e-3), (
        "sanity check: the inverted ratio must NOT equal true_A, otherwise this test "
        "cannot distinguish correct from inverted direction"
    )


def test_calibrate_window_correction_rejects_mismatched_shapes():
    k = np.linspace(0.01, 0.5, 10)
    p_clean = np.ones((5, 10))
    p_masked = np.ones((5, 9))
    with pytest.raises(ValueError):
        calibrate_window_correction(p_clean, p_masked, k)


# ---------------------------------------------------------------------------
# Full ensemble integration: before/after, legacy vs fixed+corrected
# ---------------------------------------------------------------------------

def test_ensemble_before_after_reduces_bias():
    """End-to-end: build a mock ensemble, calibrate the window correction on a TRAIN
    split, and confirm the fixed+corrected estimator's mean bias against the true clean
    P1D on a held-out TEST split is much smaller than the legacy (buggy, uncorrected)
    estimator's bias on the same held-out spectra. Train/test split avoids calibrating
    and evaluating on the same noise draws."""
    dv_kms = 50.0
    n_total = 500
    fluxes, masks = _make_ensemble(n_total, npix=256, mask_frac=0.03, seed=100)

    n_train = 350
    flux_train, mask_train = fluxes[:n_train], masks[:n_train]
    flux_test, mask_test = fluxes[n_train:], masks[n_train:]

    # Ground truth: unmasked P1D of each realization (same underlying signal).
    k, p_clean_train = flux_power_1d(flux_train, dv_kms, mask=None, return_per_spectrum=True)
    _, p_clean_test = flux_power_1d(flux_test, dv_kms, mask=None, return_per_spectrum=True)

    # Fixed estimator (bugs 1+2 handled), no window correction yet -- calibration input.
    _, p_masked_fixed_train = flux_power_1d(
        flux_train, dv_kms, mask=mask_train, return_per_spectrum=True
    )
    _, p_masked_fixed_test = flux_power_1d(
        flux_test, dv_kms, mask=mask_test, return_per_spectrum=True
    )

    # Legacy (buggy) estimator on the same test spectra, for comparison.
    flux_test_zerofilled = flux_test.copy()
    flux_test_zerofilled[mask_test] = 0.0
    _, p_legacy_test = _legacy_buggy_flux_power_1d(flux_test_zerofilled, dv_kms)
    p_legacy_test = np.broadcast_to(p_legacy_test, p_clean_test.shape)
    # (legacy fn collapses to a single mean-over-spectra vector; broadcast for a
    # per-k comparison against the clean-test mean below)

    correction, _, _ = calibrate_window_correction(
        p_clean_train, p_masked_fixed_train, k, poly_degree=2
    )

    p_clean_test_mean = p_clean_test.mean(axis=0)
    p_masked_fixed_test_mean = p_masked_fixed_test.mean(axis=0)
    p_corrected_test_mean = p_masked_fixed_test_mean * correction
    p_legacy_test_mean = p_legacy_test.mean(axis=0)

    # Restrict the comparison to well-measured k-bins (clean power above 1% of its
    # peak). Bins far out on this synthetic field's power-law tail carry near-zero true
    # power, where a per-k relative-error metric is dominated by ensemble noise rather
    # than the masking artifact itself -- the same reason real P1D analyses (including
    # Ravoux et al. 2023) do not evaluate window corrections out to arbitrarily high k.
    sel = p_clean_test_mean > (0.01 * p_clean_test_mean.max())
    assert sel.sum() >= 10, "too few well-measured k-bins selected; check the test fixture"

    def agg_bias(estimate, truth):
        """Aggregate (power-weighted) relative bias: sum|est-truth| / sum|truth| over
        the selected bins. Robust to per-bin noise blowup near-zero-power bins would
        cause in a plain mean-of-ratios metric."""
        return np.sum(np.abs(estimate[sel] - truth[sel])) / np.sum(np.abs(truth[sel]))

    bias_legacy = agg_bias(p_legacy_test_mean, p_clean_test_mean)
    bias_fixed_uncorrected = agg_bias(p_masked_fixed_test_mean, p_clean_test_mean)
    bias_fixed_corrected = agg_bias(p_corrected_test_mean, p_clean_test_mean)

    assert bias_fixed_uncorrected < bias_legacy, (
        "Bug 2 fix alone (correct mean, still zero-fill contrast) must already reduce "
        "bias relative to the fully-buggy legacy estimator"
    )
    assert bias_fixed_corrected < bias_fixed_uncorrected, (
        "the mock-calibrated window correction must further reduce the residual bias "
        "left after fixing bugs 1+2 alone"
    )
    assert bias_fixed_corrected < 0.15, (
        f"fixed+corrected estimator's held-out relative bias ({bias_fixed_corrected:.3f}) "
        "should be small; if this creeps up, the correction calibration is not working"
    )

    # Stash numbers where the brief-writing step can read them back out via -s if needed.
    print(
        f"\n[WP-E6-P2C before/after] legacy={bias_legacy:.4f} "
        f"fixed_uncorrected={bias_fixed_uncorrected:.4f} "
        f"fixed_corrected={bias_fixed_corrected:.4f}"
    )


# Generated-by: Sonnet (Stream 3 agent, WP-E6-P2C) | Verified-by: pytest pipeline/tests/
# | Reviewed-by: pending T0 (Xavier)
