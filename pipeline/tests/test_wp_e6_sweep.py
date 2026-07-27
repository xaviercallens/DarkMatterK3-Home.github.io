#!/usr/bin/env python3
"""Regression + sanity tests for pipeline/wp_e6_sweep.py and
scripts/wp_e6_adequacy_preflight.py (WP-E6 synthetic sweep harness).

No network access; fully deterministic (no random seeds needed -- the
forward model has no stochastic step). SYNTHETIC DATA ONLY, ENGINEERING
pre-flight -- see pipeline/wp_e6_sweep.py module docstring.

Covers (per the WP-E6 build spec):
  1. Known-answer sanity checks:
     - suppression S(k; m, f) -> 1 (no suppression) as f -> 0, for all k, m.
     - T_F(k) (Hu-Barkana-Gruzinov) -> 1 as k -> 0 (large scales).
     - T(k) (Eisenstein-Hu no-wiggle) -> 1 as k -> 0 (large scales).
     - the HBG00 "half-power point" k_1/2 = 4.5 m22^(4/9) Mpc^-1 (their
       eq. 9) reproduces T_F(k_1/2)^2 close to 0.5, as stated in the paper.
  2. Monotonicity: mixed-fraction suppression is monotone in f at fixed k,
     m; the Delta-chi2 distinguishability statistic is monotone in f at
     fixed m (the property scripts/wp_e6_adequacy_preflight.py's own
     monotone_in_f check also verifies on the real grid).
  3. Negative controls: a zero-signal injection (f=0 vs f=0 baseline) must
     report exactly zero distinguishability, never a false exclusion; a
     scrambled/corrupted covariance must SUPPRESS (not manufacture) a
     reported exclusion relative to the correct covariance.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.wp_e6_sweep import (  # noqa: E402
    des_y6_synthetic_convergence_bandpowers,
    eisenstein_hu_no_wiggle_transfer,
    hu_barkana_gruzinov_fdm_transfer,
    linear_matter_power_mpc3,
    mixed_fraction_power_suppression,
    smail_source_distribution,
)
from scripts.wp_e6_adequacy_preflight import (  # noqa: E402
    delta_chi2_vs_baseline,
    pure_fdm_exclusion_status,
)


# ---------------------------------------------------------------------------
# 1. Known-answer sanity checks
# ---------------------------------------------------------------------------
class TestKnownAnswerSanity:
    def test_eh98_transfer_approaches_one_at_large_scales(self):
        """T(k) -> 1 as k -> 0 (super-horizon / large scales), by
        construction of the EH98 no-wiggle fit (q -> 0 => L0/C0 -> ln(2e)/
        (ln(2e)+...) -> 1 since the q^2 term vanishes and L0 dominates)."""
        t_k = eisenstein_hu_no_wiggle_transfer(np.array([1e-6, 1e-5]))
        assert np.all(t_k > 0.9999), f"T(k->0) should be ~1, got {t_k}"

    def test_eh98_transfer_decreases_with_k(self):
        """Small-scale power suppression: T(k) monotonically decreases with
        increasing k (standard CDM+baryon transfer function shape)."""
        k = np.logspace(-4, 1, 50)
        t_k = eisenstein_hu_no_wiggle_transfer(k)
        assert np.all(np.diff(t_k) <= 1e-12), "EH98 T(k) should be monotone non-increasing"

    def test_hbg_transfer_approaches_one_at_large_scales(self):
        """T_F(k) -> 1 as k -> 0, Hu Barkana & Gruzinov 2000 eq. (8): x -> 0
        => cos(0)/(1+0) = 1, for any m22."""
        for m22 in [0.01, 1.0, 100.0]:
            t_f = hu_barkana_gruzinov_fdm_transfer(np.array([1e-8, 1e-7]), m22)
            assert np.allclose(t_f, 1.0, atol=1e-6), (
                f"T_F(k->0) should be 1 for m22={m22}, got {t_f}"
            )

    def test_hbg_half_power_point_matches_paper(self):
        """Hu, Barkana & Gruzinov 2000 (arXiv:astro-ph/0003365) state (text
        following their eq. 9) that the power drops by a factor of 2 at
        k_1/2 = 4.5 m22^(4/9) Mpc^-1. T_F(k_1/2)^2 should therefore sit
        close to 0.5 (the paper's own description is qualitative -- "drops
        by a factor of 2" -- so this checks a broad band, not exact
        equality, and the value must be IDENTICAL across m22 since x(k_1/2)
        is m22-independent by construction of the fit)."""
        values = []
        for m22 in [0.1, 1.0, 10.0, 100.0]:
            k_half = 4.5 * m22 ** (4.0 / 9.0)
            t_f = hu_barkana_gruzinov_fdm_transfer(np.array([k_half]), m22)[0]
            values.append(t_f**2)
            assert 0.4 < t_f**2 < 0.6, (
                f"T_F(k_1/2)^2 at m22={m22} should be close to 0.5 per HBG00, got {t_f**2}"
            )
        assert np.allclose(values, values[0], atol=1e-9), (
            "T_F(k_1/2)^2 must be identical across m22 (x(k_1/2) is m22-independent "
            "by construction: x = 1.61 m22^(1/18) k_1/2 / k_Jeq with k_1/2, k_Jeq "
            "both power laws in m22 that cancel the m22 dependence)"
        )

    def test_suppression_approaches_one_as_f_approaches_zero(self):
        """S(k; m, f) -> 1 (no suppression) as f -> 0, for ALL k and ALL m
        (task-required sanity property; also the module's own docstring
        guarantee)."""
        k = np.logspace(-3, 2, 30)
        for m22 in [0.1, 1.0, 10.0]:
            s = mixed_fraction_power_suppression(k, m22, f=0.0)
            assert np.allclose(s, 1.0), f"S(k, m22={m22}, f=0) should be exactly 1, got {s}"

    def test_suppression_equals_pure_fdm_at_f_one(self):
        """S(k; m, 1) == T_F(k)^2 exactly (the f=1 endpoint of the linear
        interpolation is the pure Hu-Barkana-Gruzinov suppression)."""
        k = np.logspace(-3, 2, 30)
        m22 = 3.7
        s = mixed_fraction_power_suppression(k, m22, f=1.0)
        t_f_sq = hu_barkana_gruzinov_fdm_transfer(k, m22) ** 2
        assert np.allclose(s, t_f_sq)

    def test_smail_distribution_nonnegative_and_zero_at_origin(self):
        z = np.linspace(0.0, 3.0, 50)
        n = smail_source_distribution(z)
        assert np.all(n >= 0.0)
        assert n[0] == 0.0

    def test_linear_matter_power_positive_and_decreasing_shape(self):
        """P(k) should be strictly positive over the range used by the
        Limber integral, and its EH98-shaped decline at large k should
        survive the sigma8 normalization (order-of-magnitude sanity, not a
        fit)."""
        k = np.logspace(-3, 1, 30)
        p = linear_matter_power_mpc3(k)
        assert np.all(p > 0)
        assert p[0] > p[-1], "P(k) should decline from large to small scales here"


# ---------------------------------------------------------------------------
# 2. Monotonicity
# ---------------------------------------------------------------------------
class TestMonotonicity:
    def test_suppression_monotone_in_f_at_fixed_k_m(self):
        """1 - S(k; m, f) (the suppression MAGNITUDE) must be non-decreasing
        in f at fixed (k, m), since S = 1 - f*(1 - T_F^2) is linear in f
        with a non-negative slope (T_F^2 <= 1 always)."""
        k = np.logspace(-2, 2, 20)
        m22 = 2.0
        prev_suppression_mag = -1.0
        for f in np.linspace(0.0, 1.0, 11):
            s = mixed_fraction_power_suppression(k, m22, f)
            mag = np.sum(1.0 - s)
            assert mag >= prev_suppression_mag - 1e-12, (
                f"suppression magnitude should be non-decreasing in f, "
                f"failed going into f={f}"
            )
            prev_suppression_mag = mag

    def test_distinguishability_monotone_in_f_at_fixed_m(self):
        """Delta-chi2 vs. the f=0 baseline must be non-decreasing in f at
        fixed m (task-required sanity property), computed on the actual
        forward model + Knox covariance, not just the suppression factor
        alone."""
        ell_bands = np.array([100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0])
        baseline = des_y6_synthetic_convergence_bandpowers(ell_bands=ell_bands)
        c_base = np.asarray(baseline["c_ell"])
        cov = np.asarray(baseline["cov_diag"])

        for m22 in [0.5, 1.0, 5.0]:
            prev_chi2 = -1.0
            for f in np.linspace(0.0, 1.0, 6):
                result = des_y6_synthetic_convergence_bandpowers(
                    m22=m22, f=float(f), ell_bands=ell_bands
                )
                dchi2 = delta_chi2_vs_baseline(np.asarray(result["c_ell"]), c_base, cov)
                assert dchi2 >= prev_chi2 - 1e-12, (
                    f"Delta-chi2 should be non-decreasing in f at m22={m22}, "
                    f"failed going into f={f} (dchi2={dchi2}, prev={prev_chi2})"
                )
                prev_chi2 = dchi2


# ---------------------------------------------------------------------------
# 3. Negative controls
# ---------------------------------------------------------------------------
class TestNegativeControls:
    def test_zero_signal_injection_reports_no_exclusion(self):
        """f=0 vs. the f=0 baseline is IDENTICAL by construction (S=1
        regardless of m when f=0) -- Delta-chi2 must be EXACTLY zero, never
        a false positive from floating-point noise or a broken subtraction."""
        ell_bands = np.array([100.0, 300.0, 1000.0, 3000.0])
        baseline = des_y6_synthetic_convergence_bandpowers(ell_bands=ell_bands)
        c_base = np.asarray(baseline["c_ell"])
        cov = np.asarray(baseline["cov_diag"])

        zero_signal = des_y6_synthetic_convergence_bandpowers(
            m22=1.0, f=0.0, ell_bands=ell_bands
        )
        dchi2 = delta_chi2_vs_baseline(np.asarray(zero_signal["c_ell"]), c_base, cov)
        assert dchi2 == pytest.approx(0.0, abs=1e-15), (
            f"zero-signal injection (f=0) must give Delta-chi2 == 0, got {dchi2}"
        )
        assert np.sqrt(dchi2) < 2.0, "zero-signal injection must NOT report a 2-sigma exclusion"

    def test_scrambled_covariance_suppresses_false_exclusion(self):
        """A genuinely large synthetic signal (handcrafted, not from the
        physical model, to isolate the statistic's own behavior) DOES cross
        3-sigma under its correct (small) covariance -- a positive control
        proving the statistic can detect something. The SAME signal, scored
        against a scrambled/corrupted (artificially huge) covariance, must
        NOT report an exclusion: a scrambled covariance suppresses false
        detections rather than manufacturing them. This is the mechanical
        check that delta_chi2_vs_baseline() cannot be fooled into reporting
        significance independent of the covariance it is given."""
        c_baseline = np.array([1.0, 1.0, 1.0])
        c_model = np.array([1.5, 1.5, 1.5])  # 50% deviation, handcrafted
        correct_small_cov = np.array([0.01, 0.01, 0.01])
        scrambled_huge_cov = np.array([1.0e6, 1.0e6, 1.0e6])

        dchi2_correct = delta_chi2_vs_baseline(c_model, c_baseline, correct_small_cov)
        dchi2_scrambled = delta_chi2_vs_baseline(c_model, c_baseline, scrambled_huge_cov)

        assert np.sqrt(dchi2_correct) > 3.0, (
            "positive control: a large signal under a correctly small "
            f"covariance should clear 3-sigma, got sigma={np.sqrt(dchi2_correct)}"
        )
        assert np.sqrt(dchi2_scrambled) < 2.0, (
            "negative control: the SAME signal under a scrambled/corrupted "
            f"(huge) covariance must NOT report a 2-sigma exclusion, got "
            f"sigma={np.sqrt(dchi2_scrambled)}"
        )

    def test_pure_fdm_exclusion_status_excluded_below_lowest_bound(self):
        """CORRECTED 2026-07-27 (WP-E6b audit): published FDM mass bounds are
        LOWER limits (m > threshold is the allowed region; verified against
        the arXiv abstracts of Liu Gong & Zhou 2026 and Rogers & Peiris 2021
        this session) -- so a mass BELOW even the lowest published threshold
        (1.9e-21 eV) must be EXCLUDED, not open. This test previously
        asserted the opposite (a since-fixed direction bug in both this test
        and pure_fdm_exclusion_status itself)."""
        status = pure_fdm_exclusion_status(1e-22)
        assert status["excluded"] is True
        assert len(status["excluded_by"]) >= 1

    def test_pure_fdm_exclusion_status_open_above_highest_bound(self):
        """Above the HIGHEST published pure-FDM threshold in the landscape
        survey (8e-18 eV, May, Dalal & Kravtsov 2025), the status must be
        OPEN (not excluded) -- a negative control on the exclusion-status
        lookup itself. Note this point sits above the WP-E6/E6b grid's own
        span (1e-22-1e-19 eV): within that grid, every mass is excluded at
        f=1 under the corrected direction (consistent with
        docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md Sec.4's explicit "Net
        position": the 1e-22-1e-19 eV window is fully covered by published
        pure-FDM exclusions)."""
        status = pure_fdm_exclusion_status(1e-17)
        assert status["excluded"] is False
        assert status["excluded_by"] == []


# ---------------------------------------------------------------------------
# Basic input validation (guards against silent misuse)
# ---------------------------------------------------------------------------
class TestInputValidation:
    def test_negative_f_rejected(self):
        with pytest.raises(ValueError):
            mixed_fraction_power_suppression(np.array([1.0]), 1.0, f=-0.1)

    def test_f_above_one_rejected(self):
        with pytest.raises(ValueError):
            mixed_fraction_power_suppression(np.array([1.0]), 1.0, f=1.1)

    def test_nonpositive_m22_rejected(self):
        with pytest.raises(ValueError):
            hu_barkana_gruzinov_fdm_transfer(np.array([1.0]), m22=0.0)
