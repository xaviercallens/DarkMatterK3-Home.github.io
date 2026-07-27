#!/usr/bin/env python3
"""Tests for pipeline/wp_e6b_lya.py and
scripts/wp_e6b_lya_adequacy_preflight.py (WP-E6b Lyman-alpha P1D adequacy
pre-flight).

ENGINEERING pre-flight, SYNTHETIC/PUBLISHED-TABLE ONLY -- see
pipeline/wp_e6b_lya.py module docstring. No network access; deterministic.

Covers (per the WP-E6b build spec):
  1. P1D integral known-answer on a power-law P3D (analytic result).
  2. R -> 1 as f -> 0.
  3. Monotone suppression in f (R non-increasing in f).
  4. Unit-conversion round-trip (k [s/km] <-> k [Mpc^-1]).
  5. Negative control: zero-suppression injection reports zero cells.
  6. Negative control: scrambled sigma must not produce spurious exclusions.
  Plus: the linear-in-f closed form cross-checked against direct numerical
  integration (the load-bearing simplification that makes the full grid
  tractable), and basic data-loading / validity-range sanity on the actual
  committed DESI DR1 table.

WP-E6b AUDIT ADDITIONS (2026-07-27, same day): the original suite exercised
only the low-level primitives -- `run_grid`, the function that produces the
FILED headline, was never called by any test, so the headline number had no
checker; and the original "scrambled sigma under a null signal" control did
its arithmetic entirely inside the test (`sum((zeros/sigma)**2)`), with no
module code between the injected null and the asserted zero, so it could not
fail. Added: `TestEndToEndGridControls` (zero-suppression injection,
inflated/degenerate published errors, shrunk-error positive complement,
scrambled error-to-bin correspondence, all-bins-invalid fail-closed, and an
inert-cut guard -- all driven THROUGH `run_grid`) and `TestFiledArtifact`
(headline internal consistency, the linear-in-f closed form as stored, a
full-resolution recomputation of one mass column, and the optimism
calibration). The unfalsifiable control was deleted rather than kept.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.wp_e6b_lya import (  # noqa: E402
    DEFAULT_DESI_DR1_P1D_CSV,
    K_MIN_VALID_SKM,
    desi_dr1_k_max_valid_skm,
    desi_dr1_validity_mask,
    i_lcdm_integral_mpc,
    i_suppression_integral_mpc,
    k_comoving_to_velocity_skm,
    k_velocity_to_comoving_mpc,
    load_desi_dr1_p1d_table,
    p1d_integral_general,
    p1d_ratio_mixed_over_lcdm,
    rho_shape_factor,
    sigma_rel_from_table,
)
from pipeline.wp_e6_sweep import linear_matter_power_mpc3
from scripts.wp_e6b_lya_adequacy_preflight import (  # noqa: E402
    genuinely_open_cell,
    mixed_fdm_bound_at_mass,
)


# ---------------------------------------------------------------------------
# 1. P1D integral known-answer on a power-law P3D (analytic result)
# ---------------------------------------------------------------------------
class TestKnownAnswerP1DIntegral:
    def test_power_law_p3d_matches_analytic_result(self):
        """P3D(k) = A*k^n (n < -2 for convergence) has an exact analytic 1D
        projection:

            P1D(k_par) = (1/2pi) * integral_{k_par}^inf A*k^(n+1) dk
                       = A / (2*pi * (-(n+2))) * k_par^(n+2)

        Checked here for n=-3 (P1D(k_par) = A/(2*pi*k_par)) and n=-4
        (P1D(k_par) = A/(2*pi*2*k_par^2)), at several k_par, against the
        module's general numeric integrator -- not the closed-form shortcut,
        which is tested separately against this same integrator below."""
        for n, analytic_fn in [
            (-3.0, lambda A, k: A / (2.0 * np.pi * k)),
            (-4.0, lambda A, k: A / (2.0 * np.pi * 2.0 * k**2)),
        ]:
            A = 3.7
            p3d = lambda k, n=n, A=A: A * k**n  # noqa: E731
            for k_par in [1e-3, 1e-2, 1e-1, 1.0]:
                analytic = analytic_fn(A, k_par)
                numeric = p1d_integral_general(p3d, k_par)
                rel_err = abs(numeric - analytic) / analytic
                assert rel_err < 1e-8, (
                    f"n={n}, k_par={k_par}: analytic={analytic}, numeric={numeric}, "
                    f"rel_err={rel_err}"
                )

    def test_power_law_diverges_for_shallow_index_is_not_silently_wrong(self):
        """Sanity: for n >= -2 the integral does not converge (diverges);
        this is a property of the physical setup (a real P3D always falls
        off faster than k^-2 at large k), not something the module needs to
        guard against, but worth pinning down that our EH98+HBG00 P3D
        (used everywhere else) is nowhere near this regime -- P(k) falls
        as ~k^(ns-4)*(log k)^2 at large k, ns~0.97, safely n<-2."""
        k = np.logspace(1, 3, 20)  # deep into the high-k tail
        p = linear_matter_power_mpc3(k)
        # local power-law slope should be well below -2 at large k
        log_slope = np.diff(np.log(p)) / np.diff(np.log(k))
        assert np.all(log_slope[-5:] < -2.0), (
            f"expected steep (< -2) large-k slope for convergence, got {log_slope[-5:]}"
        )


# ---------------------------------------------------------------------------
# Closed-form (linear-in-f) cross-checked against direct numerical
# integration -- the load-bearing simplification, NOT merely assumed.
# ---------------------------------------------------------------------------
class TestClosedFormMatchesDirectIntegration:
    def test_ratio_closed_form_matches_direct_numeric_integration(self):
        for k_par in [1e-3, 1e-2, 3e-2]:
            for m22 in [0.5, 5.0, 100.0]:
                for f in [0.0, 0.3, 0.7, 1.0]:
                    p_mixed = p1d_integral_general(
                        lambda k, m22=m22, f=f: linear_matter_power_mpc3(
                            np.array([k]), m22=m22, f=f
                        )[0],
                        k_par,
                    )
                    p_lcdm = p1d_integral_general(
                        lambda k: linear_matter_power_mpc3(np.array([k]))[0], k_par
                    )
                    r_numeric = p_mixed / p_lcdm
                    r_closed = p1d_ratio_mixed_over_lcdm(k_par, m22, f)
                    rel_err = abs(r_numeric - r_closed) / abs(r_closed)
                    assert rel_err < 1e-6, (
                        f"k_par={k_par}, m22={m22}, f={f}: numeric={r_numeric}, "
                        f"closed={r_closed}, rel_err={rel_err}"
                    )


# ---------------------------------------------------------------------------
# 2. R -> 1 as f -> 0
# ---------------------------------------------------------------------------
class TestRApproachesOneAsFApproachesZero:
    def test_ratio_is_exactly_one_at_f_zero(self):
        """R(k_par; m, 0) must be exactly 1 for ALL k_par and ALL m -- falls
        out of the closed form R = 1 - f*rho with f=0, but checked directly
        (not merely asserted from the algebra) since rho itself involves two
        independent quad integrals that could in principle disagree at f=0
        due to floating-point noise."""
        for k_par in [1e-3, 1e-2, 3e-2, 0.1]:
            for m22 in [0.1, 1.0, 50.0]:
                r = p1d_ratio_mixed_over_lcdm(k_par, m22, f=0.0)
                assert r == pytest.approx(1.0, abs=1e-9), (
                    f"k_par={k_par}, m22={m22}: R(f=0)={r}, expected 1.0"
                )


# ---------------------------------------------------------------------------
# 3. Monotone suppression in f
# ---------------------------------------------------------------------------
class TestMonotonicity:
    def test_ratio_non_increasing_in_f_at_fixed_k_m(self):
        """R(k_par; m, f) must be non-increasing in f at fixed (k_par, m):
        rho = I_supp/I_LCDM >= 0 always (T_F^2 <= 1, HBG00's own
        construction), so R = 1 - f*rho has a non-positive slope in f."""
        k_par = 0.01
        for m22 in [0.5, 5.0, 50.0]:
            prev_r = 2.0  # above any possible R
            for f in np.linspace(0.0, 1.0, 6):
                r = p1d_ratio_mixed_over_lcdm(k_par, m22, float(f))
                assert r <= prev_r + 1e-12, (
                    f"m22={m22}: R should be non-increasing in f, "
                    f"failed going into f={f} (r={r}, prev={prev_r})"
                )
                prev_r = r

    def test_rho_shape_factor_nonnegative(self):
        """rho(k_par; m) >= 0 always -- the property that MAKES R
        non-increasing in f; checked directly across a range of (k, m)."""
        for k_par in np.logspace(-3, 0, 8):
            for m22 in [0.1, 1.0, 10.0, 100.0]:
                rho = rho_shape_factor(float(k_par), m22)
                assert rho >= -1e-12, f"k_par={k_par}, m22={m22}: rho={rho} < 0"


# ---------------------------------------------------------------------------
# 4. Unit-conversion round-trip
# ---------------------------------------------------------------------------
class TestUnitConversionRoundTrip:
    def test_velocity_to_comoving_round_trip(self):
        k_skm = np.array([0.001, 0.005, 0.01, 0.03, 0.05])
        z = np.array([2.2, 2.8, 3.4, 4.0, 4.4])
        k_mpc = k_velocity_to_comoving_mpc(k_skm, z)
        k_back = k_comoving_to_velocity_skm(k_mpc, z)
        assert np.allclose(k_back, k_skm, rtol=1e-10)

    def test_conversion_factor_increases_with_z(self):
        """H(z)/(1+z) (the conversion factor) should increase with z over
        DESI's redshift range (matter domination -> H(z) grows faster than
        (1+z) at these z) -- so the SAME k_par [s/km] maps to a LARGER
        comoving k_par [Mpc^-1] at higher z, the mechanism by which the
        HBG00 suppression curve (fixed in comoving k) is sampled
        differently at each z bin (module docstring section 3)."""
        k_skm = np.array([0.01, 0.01, 0.01])
        z = np.array([2.2, 3.3, 4.4])
        k_mpc = k_velocity_to_comoving_mpc(k_skm, z)
        assert np.all(np.diff(k_mpc) > 0), f"expected increasing k_mpc with z, got {k_mpc}"

    def test_k_max_valid_increases_with_z(self):
        z = np.array([2.2, 3.0, 4.4])
        kmax = desi_dr1_k_max_valid_skm(z)
        assert np.all(np.diff(kmax) > 0)
        # sanity range check against the values computed in-session
        assert 0.02 < kmax[0] < 0.03
        assert 0.04 < kmax[-1] < 0.05


# ---------------------------------------------------------------------------
# Data loading + validity-range sanity (the actual committed DESI DR1 table)
# ---------------------------------------------------------------------------
class TestDesiDr1TableLoading:
    def test_table_loads_and_has_expected_shape(self):
        assert DEFAULT_DESI_DR1_P1D_CSV.exists()
        table = load_desi_dr1_p1d_table()
        assert len(table["z"]) == 1020
        assert set(np.unique(table["z"]).round(1)) == set(
            [round(2.0 + 0.2 * i, 1) for i in range(1, 13)]
        )

    def test_validity_mask_matches_expected_bin_count(self):
        """The paper's own recommended cuts (k > 1e-3 s/km, k < 0.5pi/R_z)
        leave 755 of the 1020 tabulated bins -- pinned here so a future
        accidental change to the cut constants or the table itself is
        caught mechanically."""
        table = load_desi_dr1_p1d_table()
        mask = desi_dr1_validity_mask(table["z"], table["k_s_per_km"])
        assert int(mask.sum()) == 755

    def test_sigma_rel_positive_in_valid_range(self):
        table = load_desi_dr1_p1d_table()
        mask = desi_dr1_validity_mask(table["z"], table["k_s_per_km"])
        sigma_rel = sigma_rel_from_table(table)
        assert np.all(sigma_rel[mask] > 0.0)
        assert np.all(np.isfinite(sigma_rel[mask]))


# ---------------------------------------------------------------------------
# 5 & 6. Negative controls
# ---------------------------------------------------------------------------
def _delta_chi2_shape(k_mpc_valid: np.ndarray, sigma_rel_valid: np.ndarray, m22: float) -> float:
    """Minimal re-implementation-free helper: Delta-chi2_shape(m) = sum
    (rho/sigma_rel)^2, using the module's own rho_shape_factor (not
    reimplemented -- this loop just drives it, mirroring what
    scripts/wp_e6b_lya_adequacy_preflight.py::run_grid does internally)."""
    from pipeline.wp_e6b_lya import rho_shape_factor_cached

    rho = np.array([rho_shape_factor_cached(float(k), m22) for k in k_mpc_valid])
    return float(np.sum((rho / sigma_rel_valid) ** 2))


class TestNegativeControls:
    def test_zero_suppression_injection_reports_zero_cells(self):
        """f=0 for every mass in the grid means R=1 identically at every
        (k,z) bin, so Delta-chi2_shape(m) computed from rho=0 must be
        exactly zero, and NO cell (any f, since Delta-chi2(m,f)=f^2*0=0)
        can ever reach 2-sigma. Checked directly on a small subset of the
        real valid bins + grid masses, not merely inferred from the f=0
        algebra."""
        table = load_desi_dr1_p1d_table()
        mask = desi_dr1_validity_mask(table["z"], table["k_s_per_km"])
        z_valid = table["z"][mask][:20]
        k_skm_valid = table["k_s_per_km"][mask][:20]
        k_mpc_valid = k_velocity_to_comoving_mpc(k_skm_valid, z_valid)
        sigma_rel_valid = sigma_rel_from_table(table)[mask][:20]

        for m22 in [1.0, 100.0]:
            # Zero-suppression injection: force rho=0 by using f=0 in the
            # ratio directly (rather than trusting the shape-factor path),
            # an independent check that R=1 => zero statistic regardless of
            # which mass column is asked.
            r_values = np.array([
                p1d_ratio_mixed_over_lcdm(float(k), m22, f=0.0) for k in k_mpc_valid
            ])
            assert np.allclose(r_values, 1.0, atol=1e-9)
            delta_chi2 = np.sum(((r_values - 1.0) / sigma_rel_valid) ** 2)
            assert delta_chi2 == pytest.approx(0.0, abs=1e-15)
            assert np.sqrt(delta_chi2) < 2.0

    def test_scrambled_sigma_changes_result_under_real_signal(self):
        """Positive-control complement: with a GENUINE (non-null) signal,
        scrambling sigma_rel's correspondence to bins DOES change the
        Delta-chi2 value relative to the correctly-paired computation --
        confirming sigma actually matters (the statistic is not silently
        ignoring its covariance/error input, the failure mode the negative
        control above is designed to catch)."""
        rng = np.random.default_rng(20260727)
        table = load_desi_dr1_p1d_table()
        mask = desi_dr1_validity_mask(table["z"], table["k_s_per_km"])
        z_valid = table["z"][mask]
        k_skm_valid = table["k_s_per_km"][mask]
        k_mpc_valid = k_velocity_to_comoving_mpc(k_skm_valid, z_valid)
        sigma_rel_valid = sigma_rel_from_table(table)[mask]

        m22 = 1.0  # m = 1e-22 eV, the grid's most-sensitive column
        r_values = np.array([
            p1d_ratio_mixed_over_lcdm(float(k), m22, f=1.0) for k in k_mpc_valid
        ])
        r_minus_one = r_values - 1.0
        assert np.any(r_minus_one != 0.0), "test setup: expected a genuine nonzero signal"

        delta_chi2_correct = np.sum((r_minus_one / sigma_rel_valid) ** 2)
        perm = rng.permutation(len(sigma_rel_valid))
        delta_chi2_scrambled = np.sum((r_minus_one / sigma_rel_valid[perm]) ** 2)

        assert delta_chi2_correct != pytest.approx(delta_chi2_scrambled, rel=1e-6), (
            "scrambling sigma's bin correspondence should change Delta-chi2 "
            "under a real signal -- if it doesn't, sigma isn't being used"
        )


# ---------------------------------------------------------------------------
# END-TO-END negative controls on run_grid -- the function that actually
# produces the filed headline (n_decisive_cells). Added during the WP-E6b
# audit: before these, NO test invoked run_grid at all, so the headline
# number had no checker, and the one "scrambled sigma under a null signal"
# control could not fail (it computed sum((0/sigma)^2) in the test's own
# arithmetic, with no module code between the injected null and the asserted
# zero -- a test that cannot fail is not a test). It has been replaced by
# controls 2/3/5 below, which inject the same failure modes THROUGH run_grid.
#
# Cost note: each rho evaluation is two quad integrations (~27 ms), and the
# filed full grid is 13 masses x 755 valid bins (~4 min). These controls
# therefore run a 2-mass x 3-fraction grid over a 25x-downsampled table; the
# filed artifact itself is checked separately below.
# ---------------------------------------------------------------------------
_SMALL_M_GRID = np.array([1e-22, 1e-20])
_SMALL_F_GRID = np.array([0.05, 0.5, 1.0])


def _downsampled_table(step: int = 25) -> dict:
    table = load_desi_dr1_p1d_table()
    return {key: value[::step].copy() for key, value in table.items()}


def _n_open_cells(results: dict) -> int:
    return sum(
        1 for col in results["columns"].values()
        for cell in col["cells"] if cell["genuinely_open"]
    )


class TestEndToEndGridControls:
    def test_baseline_run_finds_decisive_cells(self):
        """Precondition for every negative control below: with the ACTUAL
        published DESI DR1 errors, the reduced grid does report decisive
        cells. If this ever went to zero, the negative controls would pass
        vacuously and prove nothing."""
        from scripts.wp_e6b_lya_adequacy_preflight import run_grid

        results = run_grid(table=_downsampled_table(),
                           m_ev_grid=_SMALL_M_GRID, f_grid=_SMALL_F_GRID)
        assert results["data_source"]["n_valid_bins"] > 0
        assert results["n_decisive_cells"] > 0

    def test_zero_suppression_injection_yields_zero_decisive_cells(self, monkeypatch):
        """Negative control (zero-signal injection, END TO END): force
        rho(k, m) = 0 everywhere -- i.e. the mixed model is identical to
        LCDM at every bin -- and the grid must report sigma_equiv = 0 in
        every cell and ZERO decisive cells, regardless of how open the
        published landscape leaves those cells.

        This CAN fail: if run_grid ever stopped routing the suppression
        through rho (a hardcoded significance, a stale cached column, an
        openness-only decisive criterion), the injected null would still
        come back decisive and this assertion would fire."""
        import scripts.wp_e6b_lya_adequacy_preflight as preflight

        monkeypatch.setattr(preflight, "rho_shape_factor_cached",
                            lambda k_mpc, m22: 0.0)
        results = preflight.run_grid(table=_downsampled_table(),
                                     m_ev_grid=_SMALL_M_GRID, f_grid=_SMALL_F_GRID)

        assert results["n_decisive_cells"] == 0
        for col in results["columns"].values():
            assert col["chi2_shape"] == pytest.approx(0.0, abs=1e-15)
            assert col["smallest_f_reaching_2sigma"] is None
            for cell in col["cells"]:
                assert cell["sigma_equiv"] == pytest.approx(0.0, abs=1e-15)
                assert cell["reaches_2sigma"] is False

    def test_inflated_published_errors_erase_all_decisive_cells(self):
        """Negative control (degenerate covariance, END TO END): scale the
        published total errors up by 1e6 and every decisive cell must
        disappear. This is the check that the PUBLISHED measurement
        precision is genuinely load-bearing in the headline -- a statistic
        that ignored its error bars would return the same 'decisive' cells
        against an arbitrarily uninformative measurement."""
        from scripts.wp_e6b_lya_adequacy_preflight import run_grid

        table = _downsampled_table()
        table["e_total_kms"] = table["e_total_kms"] * 1e6
        results = run_grid(table=table, m_ev_grid=_SMALL_M_GRID, f_grid=_SMALL_F_GRID)

        assert results["n_decisive_cells"] == 0
        for col in results["columns"].values():
            for cell in col["cells"]:
                assert cell["reaches_2sigma"] is False

    def test_shrunk_published_errors_make_every_open_cell_decisive(self):
        """Positive complement to the inflated-error control: scale the
        published errors DOWN by 1e6 and the decisive count must rise to
        exactly the number of genuinely-open cells (reachability stops
        binding; only the published-landscape openness overlay does). Pins
        the two criteria as independent -- neither one silently determines
        the headline on its own."""
        from scripts.wp_e6b_lya_adequacy_preflight import run_grid

        table = _downsampled_table()
        table["e_total_kms"] = table["e_total_kms"] * 1e-6
        results = run_grid(table=table, m_ev_grid=_SMALL_M_GRID, f_grid=_SMALL_F_GRID)

        n_open = _n_open_cells(results)
        assert n_open > 0
        assert results["n_decisive_cells"] == n_open

    def test_scrambled_published_errors_change_the_statistic(self):
        """Negative control (scrambled error-to-bin correspondence, END TO
        END): permuting which published error is attached to which (k, z)
        bin must CHANGE the per-mass chi2_shape. If it did not, the
        statistic would not actually be using the per-bin published
        precision it claims to use."""
        from scripts.wp_e6b_lya_adequacy_preflight import run_grid

        rng = np.random.default_rng(20260727)
        table = _downsampled_table()
        correct = run_grid(table=table, m_ev_grid=_SMALL_M_GRID, f_grid=_SMALL_F_GRID)

        scrambled_table = {key: value.copy() for key, value in table.items()}
        perm = rng.permutation(len(scrambled_table["e_total_kms"]))
        scrambled_table["e_total_kms"] = scrambled_table["e_total_kms"][perm]
        scrambled = run_grid(table=scrambled_table,
                             m_ev_grid=_SMALL_M_GRID, f_grid=_SMALL_F_GRID)

        changed = [
            key for key in correct["columns"]
            if correct["columns"][key]["chi2_shape"]
            != pytest.approx(scrambled["columns"][key]["chi2_shape"], rel=1e-6)
        ]
        assert changed, (
            "scrambling the published error-to-bin correspondence left every "
            "chi2_shape unchanged -- the per-bin published precision is not "
            "being used"
        )

    def test_all_bins_outside_validity_range_fails_closed(self):
        """Negative control on the validity cut itself: hand the grid a
        table whose every k sits below the paper's own continuum-contamination
        floor. The cut must drop all of them (0 valid bins) and the grid must
        fail CLOSED -- zero statistic, zero decisive cells -- rather than
        silently falling back to the full, uncut table."""
        from scripts.wp_e6b_lya_adequacy_preflight import run_grid

        table = _downsampled_table()
        table["k_s_per_km"] = np.full_like(table["k_s_per_km"], K_MIN_VALID_SKM / 10.0)
        results = run_grid(table=table, m_ev_grid=_SMALL_M_GRID, f_grid=_SMALL_F_GRID)

        assert results["data_source"]["n_valid_bins"] == 0
        assert results["n_decisive_cells"] == 0
        for col in results["columns"].values():
            assert col["chi2_shape"] == pytest.approx(0.0, abs=1e-15)

    def test_both_validity_cut_arms_actually_exclude_bins(self):
        """Guard against an inert cut: on the REAL table both arms of the
        paper's recommended range must remove bins (low-k continuum floor
        and high-k resolution ceiling). A cut that excluded nothing would
        make the 'restricted to the paper's validity range' claim in
        data/MANIFEST.md and the report vacuous."""
        table = load_desi_dr1_p1d_table()
        k = table["k_s_per_km"]
        below = int(np.sum(k <= K_MIN_VALID_SKM))
        above = int(np.sum(k >= desi_dr1_k_max_valid_skm(table["z"])))
        assert below > 0, "low-k continuum-contamination cut excludes nothing"
        assert above > 0, "high-k resolution cut excludes nothing"
        assert below + above == len(k) - 755


# ---------------------------------------------------------------------------
# The FILED artifact: its headline must be reproducible from the code, and
# internally consistent with its own per-cell records.
# ---------------------------------------------------------------------------
ARTIFACT_JSON = (
    REPO_ROOT / "data" / "derived" / "wp_e6b_lya_adequacy_preflight_2026_07_27.json"
)


def _load_artifact() -> dict:
    import json

    with open(ARTIFACT_JSON) as fh:
        return json.load(fh)


class TestFiledArtifact:
    def test_headline_is_internally_consistent_and_pinned(self):
        """The filed headline (221 decisive cells of 260) must equal what
        the artifact's own per-cell records say, under the artifact's own
        stated criterion (reaches 2 sigma AND genuinely open). Pins the
        number quoted in
        docs/WP_E6B_LYA_ADEQUACY_PREFLIGHT_2026_07_27.md against silent
        drift in either the artifact or the criterion."""
        art = _load_artifact()
        assert art["grid"]["n_cells"] == 260
        assert art["data_source"]["n_valid_bins"] == 755
        assert art["data_source"]["n_total_bins"] == 1020

        recomputed = sum(
            1 for col in art["columns"].values() for cell in col["cells"]
            if cell["reaches_2sigma"] and cell["genuinely_open"]
        )
        assert recomputed == art["n_decisive_cells"] == 221
        assert len(art["decisive_cells_reachable_and_open"]) == 221

    def test_artifact_cells_obey_the_linear_in_f_closed_form(self):
        """Every stored cell must satisfy sigma_equiv = f * sigma_shape and
        delta_chi2 = sigma_equiv^2 -- the closed form the whole grid is
        built on (module docstring section 2). A cell that did not would
        mean the artifact was assembled by something other than the stated
        statistic."""
        art = _load_artifact()
        for col in art["columns"].values():
            for cell in art_cells(col):
                assert cell["sigma_equiv"] == pytest.approx(
                    cell["f"] * col["sigma_shape"], rel=1e-12)
                assert cell["delta_chi2"] == pytest.approx(
                    cell["sigma_equiv"] ** 2, rel=1e-12)
                assert cell["reaches_2sigma"] == (cell["sigma_equiv"] >= 2.0)

    def test_artifact_chi2_shape_reproduced_from_code_at_one_mass(self):
        """Tie the filed artifact to the code: recompute chi2_shape from
        scratch, over the FULL 755-bin valid set, at the grid's lightest
        mass, and require it to match the stored value. This is the only
        test that re-derives a filed headline input end-to-end at full
        resolution (~20 s); the negative controls above run reduced grids."""
        art = _load_artifact()
        table = load_desi_dr1_p1d_table()
        mask = desi_dr1_validity_mask(table["z"], table["k_s_per_km"])
        k_mpc = k_velocity_to_comoving_mpc(table["k_s_per_km"][mask], table["z"][mask])
        sigma_rel = sigma_rel_from_table(table)[mask]

        from pipeline.wp_e6b_lya import rho_shape_factor_cached

        rho = np.array([rho_shape_factor_cached(float(k), 1.0) for k in k_mpc])
        chi2 = float(np.sum((rho / sigma_rel) ** 2))

        stored = art["columns"]["1.0000e-22"]["chi2_shape"]
        assert chi2 == pytest.approx(stored, rel=1e-9)

    def test_optimism_calibration_is_present_and_exceeds_unity(self):
        """The report's optimistic-proxy caveat is quantitative, so it must
        come from the artifact, not from prose: at each published
        mixed-fraction anchor mass in the grid, this proxy's own sigma_equiv
        evaluated AT the published bound must be recomputable from the
        stored column, and must exceed this pre-flight's 2-sigma threshold
        (overstatement factor > 1) -- which is the mechanical statement that
        the linear-theory ratio is more optimistic than the emulator-based
        analysis behind the bound."""
        art = _load_artifact()
        calibration = art["optimism_calibration_vs_published_anchors"]
        assert len(calibration) == 2, "expected the 1e-22 and 1e-21 eV anchors"
        for entry in calibration:
            col = next(c for c in art["columns"].values()
                       if abs(c["m_ev"] - entry["m_ev"]) / entry["m_ev"] < 1e-9)
            expected = entry["published_f_fdm_bound"] * col["sigma_shape"]
            assert entry["proxy_sigma_equiv_at_published_bound"] == pytest.approx(
                expected, rel=1e-12)
            assert entry["overstatement_factor_vs_2sigma"] == pytest.approx(
                expected / 2.0, rel=1e-12)
            assert entry["overstatement_factor_vs_2sigma"] > 1.0


def art_cells(col: dict):
    return col["cells"]


# ---------------------------------------------------------------------------
# Overlay logic (genuinely-open determination) -- input validation +
# known-anchor checks.
# ---------------------------------------------------------------------------
class TestOverlayLogic:
    def test_mixed_bound_matches_at_1e22_anchor(self):
        anchor = mixed_fdm_bound_at_mass(1e-22)
        assert anchor is not None
        assert anchor["f_fdm_bound"] == pytest.approx(0.12)

    def test_mixed_bound_matches_at_1e21_anchor(self):
        anchor = mixed_fdm_bound_at_mass(1e-21)
        assert anchor is not None
        assert anchor["f_fdm_bound"] == pytest.approx(0.65)

    def test_no_mixed_bound_away_from_anchors(self):
        assert mixed_fdm_bound_at_mass(1e-20) is None
        assert mixed_fdm_bound_at_mass(3.162e-21) is None

    def test_f_one_never_open_when_pure_excluded(self):
        result = genuinely_open_cell(1e-22, 1.0, pure_excluded=True)
        assert result["open"] is False

    def test_f_below_mixed_bound_is_open_at_anchor_mass(self):
        result = genuinely_open_cell(1e-22, 0.05, pure_excluded=True)
        assert result["open"] is True

    def test_f_above_mixed_bound_is_excluded_at_anchor_mass(self):
        result = genuinely_open_cell(1e-21, 0.70, pure_excluded=True)
        assert result["open"] is False

    def test_f_below_one_open_by_default_away_from_anchors(self):
        result = genuinely_open_cell(1e-20, 0.5, pure_excluded=True)
        assert result["open"] is True


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------
class TestInputValidation:
    def test_negative_f_rejected(self):
        with pytest.raises(ValueError):
            p1d_ratio_mixed_over_lcdm(0.01, 1.0, f=-0.1)

    def test_f_above_one_rejected(self):
        with pytest.raises(ValueError):
            p1d_ratio_mixed_over_lcdm(0.01, 1.0, f=1.1)
