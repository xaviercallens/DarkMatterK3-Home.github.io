#!/usr/bin/env python3
"""Machine verification for WP-A (Off-Ramp 2): swampland-bound derivations.

Verifies the derivable parts of SWAMPLAND_BOUNDS_A123.md:

  [B2-core] The canonical-field exponent of the volume-scaling ansatz
            V ∝ 𝒱⁻³ (Appendix A.3.1) is λ_vol = 3·sqrt(3/2), and it exceeds
            every candidate swampland lower bound (dS conjecture c ~ O(1);
            TCC in both the interior 2/sqrt((d-1)(d-2)) and asymptotic
            2/sqrt(d-2) readings, d=4) — so the ansatz is
            swampland-consistent under any of those readings.
  [B1-num]  The Dark Dimension window for m_KK, computed two independent
            ways from the cited literature inputs, and the conservative
            union window adopted for pre-registration.
  [Λ-num]   Λ^{1/4} (dark-energy scale) computed from Planck-2018 cited
            cosmological parameters and CODATA constants — never written
            from memory — with a sanity assertion on the known ballpark.

What this script does NOT do: derive a₃'s magnitude (declared assumption
[A-NAT], see SWAMPLAND_BOUNDS_A123.md §3), derive a chameleon m_eff at cosmic
density (open gap G-1, §4), or validate the ruling's α ∈ (0, 0.5] window
(not derivable from De Giorgi–Nash–Moser alone, §4).

Sources (verified by fetch 2026-07-25, see SWAMPLAND_BOUNDS_A123.md §8):
  arXiv:2205.12293 (Montero–Vafa–Valenzuela), arXiv:2309.09330,
  arXiv:1806.08362 (Obied–Ooguri–Spodyneiko–Vafa), arXiv:1909.11063
  (Bedroya–Vafa), arXiv:1807.06209 (Planck 2018), CODATA 2018.
"""
import math

import sympy as sp

# ---------------------------------------------------------------------------
# [B2-core] Exponent of V ∝ 𝒱⁻³ in canonical-field variables — symbolic
# ---------------------------------------------------------------------------
# Standard single-Kähler-modulus setup: K = -3 ln(T + T̄), 𝒱 = (Re T)^{3/2}.
# Canonically normalize the real direction t = Re T and express V ∝ 𝒱⁻³ as
# exp(-λ_vol φ/M_Pl). Everything below is exact symbolic manipulation.
t, phi = sp.symbols("t phi", positive=True)

K = -3 * sp.log(2 * t)                      # K(T,T̄) on the real slice
K_TTbar = sp.diff(K, t, t) / 4              # ∂_T∂_T̄ K = (1/4)∂_t² K on the slice
kinetic_coeff = sp.simplify(K_TTbar)        # coefficient of (∂t)² is K_TT̄
assert kinetic_coeff == sp.Rational(3, 4) / t**2, kinetic_coeff

# ½(∂φ)² = K_TT̄ (∂t)²  ⇒  dφ/dt = sqrt(2 K_TT̄)
dphi_dt = sp.sqrt(2 * kinetic_coeff)
phi_of_t = sp.integrate(dphi_dt, t)         # = sqrt(3/2) ln t
assert sp.simplify(phi_of_t - sp.sqrt(sp.Rational(3, 2)) * sp.log(t)) == 0

# 𝒱 = t^{3/2} ⇒ V ∝ 𝒱⁻³ = t^{-9/2} = exp(-(9/2) ln t) = exp(-λ_vol φ)
lam_vol = sp.Rational(9, 2) / sp.sqrt(sp.Rational(3, 2))
lam_vol = sp.simplify(lam_vol)
assert sp.simplify(lam_vol - 3 * sp.sqrt(sp.Rational(3, 2))) == 0
lam_vol_num = float(lam_vol)

# Swampland lower bounds to compare against (d = 4):
d = 4
tcc_interior = 2 / math.sqrt((d - 1) * (d - 2))   # 2/sqrt(6) ≈ 0.816
tcc_asymptotic = 2 / math.sqrt(d - 2)             # 2/sqrt(2) ≈ 1.414
ds_conjecture_c = 1.0                              # "c ~ O(1)" reading

print("--- [B2-core] volume-scaling exponent ---")
print(f"lambda_vol = 3*sqrt(3/2) = {lam_vol_num:.6f}")
print(f"  vs dS-conjecture c ~ O(1):        {ds_conjecture_c:.3f}")
print(f"  vs TCC interior  2/sqrt(6):       {tcc_interior:.3f}")
print(f"  vs TCC asymptotic 2/sqrt(2):      {tcc_asymptotic:.3f}")
assert lam_vol_num > ds_conjecture_c
assert lam_vol_num > tcc_interior
assert lam_vol_num > tcc_asymptotic
print("  PASS: exponent exceeds all candidate bounds -> ansatz swampland-consistent")

# ---------------------------------------------------------------------------
# [Λ-num] Dark-energy scale from cited constants (never from memory)
# ---------------------------------------------------------------------------
# Planck 2018 (arXiv:1807.06209, TT,TE,EE+lowE+lensing): H0, Omega_Lambda.
H0_km_s_Mpc = 67.4          # arXiv:1807.06209
Omega_Lambda = 0.685        # arXiv:1807.06209
G_N = 6.67430e-11           # m^3 kg^-1 s^-2, CODATA 2018
c_light = 2.99792458e8      # m/s, exact (SI)
hbar_c_eV_nm = 197.3269804  # eV·nm, CODATA 2018
eV_J = 1.602176634e-19      # J, exact (SI)
Mpc_m = 3.0856775814913673e22  # m (IAU definition of parsec)

H0_si = H0_km_s_Mpc * 1e3 / Mpc_m                      # s^-1
rho_crit = 3 * H0_si**2 / (8 * math.pi * G_N)          # kg/m^3
u_Lambda = Omega_Lambda * rho_crit * c_light**2        # J/m^3
u_Lambda_eV_m3 = u_Lambda / eV_J                       # eV/m^3
hbar_c_eV_m = hbar_c_eV_nm * 1e-9                      # eV·m
Lambda4 = u_Lambda_eV_m3 * hbar_c_eV_m**3              # eV^4
Lambda_quarter_eV = Lambda4**0.25                      # eV

print("\n--- [Λ-num] dark-energy scale ---")
print(f"rho_crit = {rho_crit:.4e} kg/m^3")
print(f"Lambda^(1/4) = {Lambda_quarter_eV*1e3:.3f} meV")
# Sanity envelope only — the literature ballpark is ~2.2-2.3 meV; a value far
# outside means a unit error above, not new physics.
assert 2.0e-3 < Lambda_quarter_eV < 2.5e-3, Lambda_quarter_eV

# ---------------------------------------------------------------------------
# [B1-num] Dark Dimension window for m_KK, two cited routes + union
# ---------------------------------------------------------------------------
# Route (i): m_KK = lambda^{-1} * Lambda^{1/4}, 1e-4 <= lambda <= 1e-1
#            (arXiv:2205.12293 and follow-ups).
lam_lo, lam_hi = 1e-4, 1e-1
mkk_route1_lo = Lambda_quarter_eV / lam_hi   # smallest m_KK (largest lambda)
mkk_route1_hi = Lambda_quarter_eV / lam_lo

# Route (ii): effective size l ~ 1-30 micron (arXiv:2309.09330); m_KK = ħc/l.
l_lo_nm, l_hi_nm = 1e3, 3e4                  # 1 μm .. 30 μm in nm
mkk_route2_lo = hbar_c_eV_nm / l_hi_nm
mkk_route2_hi = hbar_c_eV_nm / l_lo_nm

union_lo = min(mkk_route1_lo, mkk_route2_lo)
union_hi = max(mkk_route1_hi, mkk_route2_hi)

print("\n--- [B1-num] Dark Dimension m_KK window ---")
print(f"route (i)  lambda-form : [{mkk_route1_lo:.4g}, {mkk_route1_hi:.4g}] eV")
print(f"route (ii) size-form   : [{mkk_route2_lo:.4g}, {mkk_route2_hi:.4g}] eV")
print(f"conservative UNION     : [{union_lo:.4g}, {union_hi:.4g}] eV"
      f"  ({math.log10(union_hi/union_lo):.1f} decades)")
# The two cited routes must at least overlap; if they didn't, the scenario
# inputs would be mutually inconsistent and no window could be quoted.
assert mkk_route1_lo < mkk_route2_hi and mkk_route2_lo < mkk_route1_hi, \
    "cited Dark-Dimension routes do not overlap"

# ---------------------------------------------------------------------------
# Scale-coherence flag (gap G-1) — printed, deliberately NOT an assertion:
# an unscreened scalar in the union window has micron-to-mm range, which is
# irrelevant to weak-lensing kappa peaks unless chameleon density-dependence
# lowers the cosmic m_eff by many decades. That bridge is NOT derived here.
# ---------------------------------------------------------------------------
range_hi_m = hbar_c_eV_m / union_lo
range_lo_m = hbar_c_eV_m / union_hi
print("\n--- gap G-1 (not an assertion; see SWAMPLAND_BOUNDS_A123.md §4) ---")
print(f"unscreened force range across union window: "
      f"[{range_lo_m:.3g}, {range_hi_m:.3g}] m")
print("=> cosmologically negligible unless chameleon screening lowers the")
print("   cosmic-density m_eff by many decades. That derivation DOES NOT")
print("   EXIST YET; kappa-peak observables cannot be pinned against this")
print("   window until gap G-1 is closed or the observable is re-scoped.")

print("\nAll assertions passed.")

# Generated-by: Fable 5 (T0) WP-A, 2026-07-25 | Verified-by: executed, assertions
# green; citation inputs verified by web fetch same day | Reviewed-by: T0 N
# (pending Deep Think blind pass + Xavier)
