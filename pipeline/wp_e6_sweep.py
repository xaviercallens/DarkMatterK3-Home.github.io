#!/usr/bin/env python3
"""WP-E6: synthetic-data sweep harness (forward model only).

SYNTHETIC DATA ONLY (CLAUDE.md rule 1). This module makes no real-data touch
and is not gated by G1/G1-L: it is `ENGINEERING` pre-flight arithmetic, not a
`TEST` or `FIT` (WP-E7 labeling precedent, docs/WP_E7_DESI_RESOLVABILITY_
PREFLIGHT_2026_07_27.md). T0 authorization: briefs/T0_DECISIONS_2026_07_27.md
D-b (mixed-fraction framing, T1-delegated ruling) and D-c (DES Y6 as the
lensing product). See docs/WP_E6_SYNTHETIC_ADEQUACY_PREFLIGHT_2026_07_27.md
for the adequacy table this module feeds.

What this computes, top to bottom:
  1. `eisenstein_hu_no_wiggle_transfer` — a ΛCDM linear matter transfer
     function, Eisenstein & Hu 1998 (ApJ 496, 605; arXiv:astro-ph/9709112)
     "zero-baryon" / no-wiggle fitting form, their eqs. (26), (28), (29),
     (30), (31). Exact coefficients transcribed from the paper (verified via
     the arXiv PDF this session), not invented.
  2. `hu_barkana_gruzinov_fdm_transfer` — the pure-FDM (f=1) suppression of
     the *matter power spectrum* relative to CDM, Hu, Barkana & Gruzinov
     2000 (PRL 85, 1158; arXiv:astro-ph/0003365) eqs. (8)-(9): T_F(k) =
     cos(x^3)/(1+x^8), x = 1.61 m22^(1/18) k/k_Jeq, k_Jeq = 9 m22^(1/2)
     Mpc^-1, m22 = m/1e-22 eV. P_FCDM(k) = T_F(k)^2 P_CDM(k).
  3. `mixed_fraction_power_suppression` — extends (2) to a fraction f < 1 of
     the dark matter being the ultralight component by LINEAR INTERPOLATION
     of the power suppression T_F^2(k) between f=0 (S=1, no suppression) and
     f=1 (S=T_F^2(k)). *** ENGINEERING APPROXIMATION, NOT A DERIVED MIXING
     LAW *** — see the docstring on that function for exactly what this
     assumes and does not assume. The reference treatment of genuine
     mixed-fraction constraints is Liu, Gong & Zhou 2026 (arXiv:2606.06969),
     who solve the coupled linear Boltzmann/fluid equations for a two-
     component (CDM + FDM) dark sector rather than interpolating a
     suppression factor; this module's f-interpolation is a placeholder to
     be ratified or replaced against that (or an equivalent) treatment at
     PREDICTION v2 pin time, not before.
  4. `des_y6_synthetic_convergence_bandpowers` — a toy DES-Y6-like projected
     convergence power spectrum in a few broad ell bands via the Limber
     approximation, with a Gaussian (Knox 1995-form) covariance built from
     the survey parameters T0 pinned in D-c: n_eff = 8.22 arcmin^-2,
     sigma_e = 0.29, area = 4422 deg^2 (arXiv:2501.05665, DES Y6
     Metadetection, via docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md).

Fidelity is explicitly NOT the point of this module (task framing, WP-E6
proposal precedent). What it must get right is *ordering*: whether a
DES-Y6-like survey could in principle distinguish a given (m, f) from f=0 at
some formal significance, not the numerical value of that significance to
high precision. See the report's caveats section for the itemized list of
what is and is not modeled (linear theory only; no baryons; no photo-z
systematics; toy n(z); diagonal Gaussian covariance; z-independent
suppression).
"""
from __future__ import annotations

import functools

import numpy as np

from pipeline.cosmology import comoving_distance_mpc

# ---------------------------------------------------------------------------
# Cosmology — Planck 2018 TT,TE,EE+lowE+lensing+BAO headline values, matching
# pipeline/cosmology.py's astropy.cosmology.Planck18 choice (same citation:
# Planck Collaboration 2018/2020, A&A 641, A6, Table 2). A FREE INPUT to this
# toy pipeline, not a prediction — same status as WP-E7's fiducial cosmology.
# ---------------------------------------------------------------------------
H0_KM_S_MPC = 67.66
HUBBLE_LITTLE_H = H0_KM_S_MPC / 100.0
OMEGA_M = 0.30966
OMEGA_B_H2 = 0.02242  # Planck 2018 baryon density Omega_b h^2 (Table 2)
OMEGA_B = OMEGA_B_H2 / HUBBLE_LITTLE_H**2
NS = 0.9665  # Planck 2018 scalar spectral index
SIGMA8 = 0.8102  # Planck 2018 sigma8 (derived parameter, Table 2)
THETA_CMB_27 = 2.7255 / 2.7  # T_CMB/2.7 K (Fixsen 2009 COBE/FIRAS T_CMB)
C_KM_S = 299792.458


# ---------------------------------------------------------------------------
# 1. Eisenstein & Hu 1998 no-wiggle ("zero-baryon") transfer function.
# ---------------------------------------------------------------------------
def _eh98_sound_horizon_mpc(omega_m_h2: float, omega_b_h2: float) -> float:
    """Sound horizon s (Mpc), EH98 eq. (26). Approximates the exact eq. (6)
    integral to ~2% over 0.0125 <~ Omega_b h^2 and 0.025 <~ Omega_0 h^2 <~ 0.5."""
    return 44.5 * np.log(9.83 / omega_m_h2) / np.sqrt(1.0 + 10.0 * omega_b_h2**0.75)


def _eh98_alpha_gamma(omega_m_h2: float, omega_b_over_omega_m: float) -> float:
    """EH98 eq. (31)."""
    fb = omega_b_over_omega_m
    return (
        1.0
        - 0.328 * np.log(431.0 * omega_m_h2) * fb
        + 0.38 * np.log(22.3 * omega_m_h2) * fb**2
    )


def eisenstein_hu_no_wiggle_transfer(
    k_mpc: np.ndarray,
    omega_m: float = OMEGA_M,
    omega_b: float = OMEGA_B,
    hubble: float = HUBBLE_LITTLE_H,
    theta_cmb_27: float = THETA_CMB_27,
) -> np.ndarray:
    """ΛCDM linear matter transfer function T(k), Eisenstein & Hu 1998
    no-wiggle fitting form (their eqs. 26, 28, 29, 30, 31 — "A User's Guide",
    Appendix A: "the form given in equation (29) and (28)-(31)" for the
    non-oscillatory transfer function). T(k->0) = 1 by construction.

    Parameters
    ----------
    k_mpc : array-like
        Comoving wavenumber(s), PHYSICAL Mpc^-1 (not h/Mpc).
    omega_m, omega_b : float
        Density parameters (dimensionless, Omega_x = rho_x/rho_crit today).
    hubble : float
        Dimensionless Hubble parameter h = H0/(100 km/s/Mpc).
    theta_cmb_27 : float
        T_CMB / 2.7 K.

    Returns
    -------
    ndarray
        T(k), same shape as k_mpc.
    """
    k_mpc = np.asarray(k_mpc, dtype=np.float64)
    omega_m_h2 = omega_m * hubble**2
    omega_b_h2 = omega_b * hubble**2
    fb = omega_b / omega_m

    s_mpc = _eh98_sound_horizon_mpc(omega_m_h2, omega_b_h2)  # eq. 26
    alpha_g = _eh98_alpha_gamma(omega_m_h2, fb)  # eq. 31

    # eq. 30: Gamma_eff(k), "k" here is PHYSICAL Mpc^-1 (k*s must be
    # dimensionless with s in Mpc; cross-checked against eq. 28's q against
    # the ORIGINAL q of eq. (10), which is manifestly k[Mpc^-1] * Theta_2.7^2
    # / (Omega_0 h^2) — algebraically identical to eq. 28's
    # k[h/Mpc] * Theta_2.7^2 / Gamma with Gamma = Omega_0 h).
    gamma_eff = omega_m * hubble * (
        alpha_g + (1.0 - alpha_g) / (1.0 + (0.43 * k_mpc * s_mpc) ** 4)
    )

    k_h_mpc = k_mpc / hubble  # physical Mpc^-1 -> h/Mpc, for eq. 28's q
    q = k_h_mpc * theta_cmb_27**2 / gamma_eff  # eq. 28, Gamma -> Gamma_eff(k)

    l0 = np.log(2.0 * np.e + 1.8 * q)  # eq. 29
    c0 = 14.2 + 731.0 / (1.0 + 62.5 * q)  # eq. 29
    return l0 / (l0 + c0 * q**2)  # eq. 29


# ---------------------------------------------------------------------------
# 2. Hu, Barkana & Gruzinov 2000 pure-FDM transfer function fit.
# ---------------------------------------------------------------------------
def hu_barkana_gruzinov_fdm_transfer(k_mpc: np.ndarray, m22: float) -> np.ndarray:
    """Pure-FDM (f=1) suppression amplitude T_F(k), Hu, Barkana & Gruzinov
    2000 (PRL 85, 1158; arXiv:astro-ph/0003365) eqs. (8)-(9):

        T_F(k) = cos(x^3) / (1 + x^8),   x = 1.61 * m22^(1/18) * k / k_Jeq
        k_Jeq = 9 * m22^(1/2) Mpc^-1

    P_FCDM(k) = T_F(k)^2 * P_CDM(k) is the paper's eq. (8); this function
    returns T_F(k) itself (amplitude, not squared), so callers explicitly
    square it where the power-spectrum relation is used — this keeps the
    sign of T_F (which oscillates through zero for x >~ 1) visible rather
    than silently squared away at this layer.

    Parameters
    ----------
    k_mpc : array-like
        Comoving wavenumber(s), physical Mpc^-1.
    m22 : float
        Ultralight particle mass in units of 1e-22 eV (m22 = m / 1e-22 eV).

    Returns
    -------
    ndarray
        T_F(k), same shape as k_mpc.
    """
    k_mpc = np.asarray(k_mpc, dtype=np.float64)
    m22 = float(m22)
    if m22 <= 0.0:
        raise ValueError(f"m22 must be positive, got {m22}")
    k_jeq = 9.0 * np.sqrt(m22)  # Mpc^-1, HBG00 eq. (9) sentence ("k_Jeq = 9 m22^1/2")
    x = 1.61 * m22 ** (1.0 / 18.0) * k_mpc / k_jeq
    return np.cos(x**3) / (1.0 + x**8)


def mixed_fraction_power_suppression(k_mpc: np.ndarray, m22: float, f: float) -> np.ndarray:
    """Matter-power suppression factor S(k; m, f) for a MIXED ultralight
    fraction f (0 <= f <= 1 of the dark matter is the m22 ultralight
    component; the rest behaves as standard CDM), such that:

        P_mixed(k) = S(k; m, f) * P_LCDM(k)

    *** ENGINEERING APPROXIMATION — linear interpolation, not a derived
    mixing law; to be ratified or replaced at PREDICTION v2 pin time ***

        S(k; m, f) = 1 - f * (1 - T_F(k; m)^2)

    i.e. linear interpolation of the POWER suppression T_F(k)^2 between
    f=0 (S=1, pure CDM, no suppression at any k) and f=1 (S=T_F(k)^2, the
    Hu-Barkana-Gruzinov pure-FDM case). This is NOT how a physical
    two-component (CDM + FDM) linear Boltzmann/fluid calculation actually
    mixes power — the true mixed-fraction transfer function requires
    solving coupled perturbation equations for the two components jointly
    (their relative growth rates differ below the FDM Jeans scale), which
    is what Liu, Gong & Zhou 2026 (arXiv:2606.06969) do to derive their
    published f_FDM bounds. Linear interpolation of the single-component
    suppression is a placeholder that reproduces the correct f=0 and f=1
    endpoints and a monotone-in-f ordering, which is all that is needed for
    an ADEQUACY (can-we-tell-cells-apart) pre-flight — it is explicitly not
    asserted to reproduce the correct suppression shape or amplitude at
    intermediate f, and any downstream exclusion claim must not treat this
    interpolation as a fit result.

    Parameters
    ----------
    k_mpc : array-like
        Comoving wavenumber(s), physical Mpc^-1.
    m22 : float
        Ultralight particle mass in units of 1e-22 eV.
    f : float
        Ultralight fraction of the dark matter, 0 <= f <= 1.

    Returns
    -------
    ndarray
        S(k; m, f), same shape as k_mpc. S -> 1 (no suppression) as f -> 0,
        for ALL k and ALL m (task-required sanity property).
    """
    f = float(f)
    if not (0.0 <= f <= 1.0):
        raise ValueError(f"f must be in [0, 1], got {f}")
    t_f = hu_barkana_gruzinov_fdm_transfer(k_mpc, m22)
    return 1.0 - f * (1.0 - t_f**2)


# ---------------------------------------------------------------------------
# 3. Toy DES-Y6-like synthetic convergence power spectrum + covariance.
# ---------------------------------------------------------------------------
# Survey parameters, T0 decision D-c (briefs/T0_DECISIONS_2026_07_27.md):
# DES Y6 Metadetection, arXiv:2501.05665, via
# docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md.
DES_Y6_N_EFF_ARCMIN2 = 8.22
DES_Y6_SIGMA_E = 0.29
DES_Y6_AREA_DEG2 = 4422.0

_ARCMIN2_PER_STERADIAN = (180.0 * 60.0 / np.pi) ** 2  # arcmin^2 per steradian
_DEG2_PER_STERADIAN = (180.0 / np.pi) ** 2


def _growth_factor_carroll_press_turner(z: np.ndarray, omega_m: float = OMEGA_M) -> np.ndarray:
    """Linear growth factor D(z), normalized D(0)=1, flat LCDM approximation
    of Carroll, Press & Turner 1992 (ARA&A 30, 499), their eq. (29)-(31)
    fitting formula (also given in Lahav et al. 1991, MNRAS 251, 128):

        D(a) propto (5/2) Om(a) / [Om(a)^(4/7) - OL(a) + (1+Om(a)/2)(1+OL(a)/70)]

    A standard, widely-used approximation (~1% accurate for flat LCDM); not
    an exact growth-factor solution. Used here only to weight the lensing
    kernel across source redshift -- the FDM suppression itself is treated
    as z-independent in this toy model (an explicit caveat, see report).
    """
    z = np.asarray(z, dtype=np.float64)
    omega_l = 1.0 - omega_m
    a = 1.0 / (1.0 + z)
    om_a = omega_m / (omega_m + omega_l * a**3)
    ol_a = 1.0 - om_a
    d_unnorm = (2.5 * a * om_a) / (
        om_a ** (4.0 / 7.0) - ol_a + (1.0 + om_a / 2.0) * (1.0 + ol_a / 70.0)
    )
    d0 = (2.5 * 1.0 * omega_m) / (
        omega_m ** (4.0 / 7.0) - omega_l + (1.0 + omega_m / 2.0) * (1.0 + omega_l / 70.0)
    )
    return d_unnorm / d0


def smail_source_distribution(z: np.ndarray, z0: float = 0.5, alpha: float = 2.0,
                               beta: float = 1.5) -> np.ndarray:
    """Toy Smail et al. 1994-type redshift distribution n(z) propto
    z^alpha exp(-(z/z0)^beta), UNNORMALIZED here (callers normalize). The
    (z0, alpha, beta) values are illustrative of a DES-Y6-like broad source
    sample (mean z ~ 0.6-0.7), NOT fit to or read from the actual released
    DES Y6 n(z) -- this is exactly the kind of survey-shaped-but-synthetic
    input the rule-1 discipline (no real-data touch) requires, and is
    flagged as such in the adequacy report's caveats.
    """
    z = np.asarray(z, dtype=np.float64)
    return np.where(z > 0, z**alpha * np.exp(-((z / z0) ** beta)), 0.0)


@functools.lru_cache(maxsize=4)
def _normalize_pk_to_sigma8(
    sigma8_target: float = SIGMA8, ns: float = NS, n_k: int = 4000,
) -> float:
    """Solve for the primordial-power amplitude A such that
    P(k) = A * k^ns * T(k)^2 gives the target sigma8 (top-hat variance in
    R8 = 8/h Mpc spheres), the standard sigma8-normalization convention
    (e.g. Dodelson & Schmidt, "Modern Cosmology" 2nd ed., ch. 7). Returns A.

    Depends only on the fixed LCDM shape (eisenstein_hu_no_wiggle_transfer,
    always evaluated at the module's fiducial cosmology) and (sigma8_target,
    ns, n_k) -- never on (m22, f) -- so it is cached: a (m, f) grid sweep
    would otherwise repeat an identical 4000-point integral at every cell.
    """
    r8_mpc = 8.0 / HUBBLE_LITTLE_H
    k = np.logspace(-4, 2, n_k)  # Mpc^-1
    t_k = eisenstein_hu_no_wiggle_transfer(k)
    x = k * r8_mpc
    w_th = 3.0 * (np.sin(x) - x * np.cos(x)) / x**3

    # sigma8^2 = (1/2 pi^2) int dk k^2 P(k) W_TH(k R8)^2, P(k) = k^ns T(k)^2
    # (amplitude A factored out). Integrated over d(ln k), so the measure
    # picks up one extra power of k: integrand = k^3 * P_shape(k) * W^2.
    integrand_logk = k**3 * (k**ns * t_k**2) * w_th**2
    sigma8_sq_unnorm = np.trapezoid(integrand_logk, np.log(k)) / (2.0 * np.pi**2)
    return sigma8_target**2 / sigma8_sq_unnorm


def linear_matter_power_mpc3(
    k_mpc: np.ndarray, m22: float | None = None, f: float = 0.0,
    sigma8_target: float = SIGMA8, ns: float = NS,
) -> np.ndarray:
    """Linear matter power spectrum P(k) [Mpc^3] at z=0, EH98 no-wiggle
    LCDM shape, sigma8-normalized, with the mixed-FDM suppression S(k;m,f)
    applied (f=0 or m22=None gives pure LCDM, S=1 identically).
    """
    k_mpc = np.asarray(k_mpc, dtype=np.float64)
    t_k = eisenstein_hu_no_wiggle_transfer(k_mpc)
    amplitude = _normalize_pk_to_sigma8(sigma8_target, ns)
    p_lcdm = amplitude * k_mpc**ns * t_k**2
    if m22 is None or f <= 0.0:
        return p_lcdm
    s = mixed_fraction_power_suppression(k_mpc, m22, f)
    return s * p_lcdm


@functools.lru_cache(maxsize=4)
def _lensing_geometry(n_z: int, z_max: float):
    """Precompute the (m22, f)-INDEPENDENT parts of the Limber projection:
    the redshift/comoving-distance grid, growth factor, and lensing
    efficiency kernel. Cached because a full (m, f) grid sweep would
    otherwise recompute identical geometry (including a comoving-distance
    call per z) at every one of ~hundreds of cells.
    """
    z_grid = np.linspace(1e-3, z_max, n_z)
    n_z_unnorm = smail_source_distribution(z_grid)
    n_z_norm = n_z_unnorm / np.trapezoid(n_z_unnorm, z_grid)

    chi_grid = comoving_distance_mpc(z_grid)  # Mpc, Planck18 (pipeline.cosmology)
    d_growth = _growth_factor_carroll_press_turner(z_grid)

    # Lensing efficiency kernel g(chi) = int_chi^chi_max n(z') (chi'-chi)/chi' dz'
    # (integrated directly in z against n(z') dz', avoiding an explicit
    # dz/dchi Jacobian since n_z_norm is already normalized against dz).
    g_of_chi = np.zeros_like(chi_grid)
    for i, chi_i in enumerate(chi_grid):
        mask = chi_grid >= chi_i
        if not np.any(mask):
            continue
        integrand = n_z_norm[mask] * (chi_grid[mask] - chi_i) / np.maximum(chi_grid[mask], 1e-8)
        g_of_chi[i] = np.trapezoid(integrand, z_grid[mask])

    h0_over_c = H0_KM_S_MPC / C_KM_S  # Mpc^-1
    lensing_kernel = (
        1.5 * OMEGA_M * h0_over_c**2 * chi_grid * (1.0 + z_grid) * g_of_chi
    )  # standard convergence kernel, e.g. Bartelmann & Schneider 2001 eq. 2.68 form

    return z_grid, chi_grid, d_growth, lensing_kernel


def des_y6_synthetic_convergence_bandpowers(
    m22: float | None = None,
    f: float = 0.0,
    ell_bands: np.ndarray | None = None,
    n_z: int = 60,
    z_max: float = 2.5,
) -> dict:
    """Toy DES-Y6-like synthetic convergence power spectrum C_ell in a few
    broad ell bands via the flat-sky Limber approximation (e.g. Kaiser 1992,
    ApJ 388, 272; standard weak-lensing formalism, see LoVerde & Afshordi
    2008 for the Limber-approximation validity discussion), plus a Gaussian
    (Knox 1995, PRD 52, 4307) band-diagonal covariance built from the DES Y6
    survey parameters (D-c). Fidelity is explicitly not the point (module
    docstring); this exists to ORDER (m, f) cells by distinguishability, not
    to forecast DES Y6 to publication accuracy.

    Returns
    -------
    dict with keys 'ell', 'c_ell', 'n_ell' (shape-noise power), 'cov_diag'
    (Knox-formula variance per band), 'f_sky', all as plain floats/lists.
    """
    if ell_bands is None:
        ell_bands = np.array([100.0, 300.0, 1000.0, 3000.0, 10000.0, 30000.0])
    ell_bands = np.asarray(ell_bands, dtype=np.float64)

    _, chi_grid, d_growth, lensing_kernel = _lensing_geometry(n_z, z_max)

    c_ell = np.zeros_like(ell_bands)
    for b, ell in enumerate(ell_bands):
        k_of_chi = (ell + 0.5) / np.maximum(chi_grid, 1e-8)  # Limber k(chi), Mpc^-1
        p_k = linear_matter_power_mpc3(k_of_chi, m22=m22, f=f) * d_growth**2
        integrand = lensing_kernel**2 / np.maximum(chi_grid**2, 1e-8) * p_k
        c_ell[b] = np.trapezoid(integrand, chi_grid)

    n_eff_per_sr = DES_Y6_N_EFF_ARCMIN2 * _ARCMIN2_PER_STERADIAN
    n_ell = DES_Y6_SIGMA_E**2 / n_eff_per_sr  # shape-noise power, standard convention
    f_sky = DES_Y6_AREA_DEG2 / (4.0 * np.pi * _DEG2_PER_STERADIAN)

    delta_ell = np.gradient(ell_bands)
    delta_ell = np.maximum(delta_ell, 1.0)
    cov_diag = (2.0 / ((2.0 * ell_bands + 1.0) * f_sky * delta_ell)) * (c_ell + n_ell) ** 2

    return {
        "ell": ell_bands.tolist(),
        "c_ell": c_ell.tolist(),
        "n_ell": float(n_ell),
        "cov_diag": cov_diag.tolist(),
        "f_sky": float(f_sky),
    }


# Generated-by: Sonnet (Stream 3 agent) | Verified-by: pipeline/tests/test_wp_e6_sweep.py
# | Reviewed-by: pending T0 (Xavier)
