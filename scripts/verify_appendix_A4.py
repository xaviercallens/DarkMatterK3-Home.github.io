#!/usr/bin/env python3
"""Symbolic verification of PREDICTION_APPENDIX_A.md §A.4 elimination algebra.

WP S3-00b deliverable (2026-07-25). Fable 5 (T0) primary derivation, Deep Think
(T0s) adversarial concurrence.

Scope and epistemic status: this script verifies ONLY the algebra of eliminating
(V, g_s) between the three ansatz scalings of Appendix A.1-A.3. It does not
derive, bound, or validate a1, a2, a3 themselves -- those require an explicit
flux/tadpole construction which WP S3-00b found to be blocked (F5b stands; see
NO_PREDICTION_BRANCH.md). Consequently this script produces a *relation between
symbols*, never a number. There is deliberately no numeric evaluation path here.

Per .agents/AGENTS.md Rule 2 and institutional practice P2 (tests are scientific,
not smoke), the expected closed forms are asserted, not merely printed.
"""
import sympy as sp

# Positive reals: all of these are physical magnitudes (volumes, couplings,
# masses, densities), so sign branches from sp.solve are unwanted here.
a1, a2, a3 = sp.symbols("a1 a2 a3", positive=True)
V, gs, Mpl, L_D = sp.symbols("V g_s M_Pl Lambda_D", positive=True)
m_phi, rho_DE, C_flux = sp.symbols("m_phi rho_DE C_flux", positive=True)

# C_flux stands for |d^2 V_flux(F(z*))|^(1/2) from Appendix A.2 -- the one factor
# that would come from a certified (Tier A/B) geometric input. It is carried
# symbolically precisely because the flux potential it derives from was NOT
# constructible (see A.2 status).

# --- The three ansatz scalings (Appendix A.1, A.2, A.3) --------------------
eq1 = sp.Eq(sp.log(Mpl / L_D), a1 * V ** sp.Rational(2, 3) / gs)   # A.1
eq2 = sp.Eq(m_phi, a2 * (gs / V) * Mpl * C_flux)                    # A.2
eq3 = sp.Eq(rho_DE, a3 * V ** -3 * Mpl ** 4)                        # A.3

# --- Mechanical elimination of (V, g_s) -----------------------------------
V_sol = sp.solve(eq3, V)[0]
gs_sol = sp.solve(eq1, gs)[0].subs(V, V_sol)
m_phi_expr = sp.simplify(eq2.rhs.subs({gs: gs_sol, V: V_sol}))

print("--- Appendix A.4 Symbolic Verification ---")
print(f"Volume (V) scaling:            {V_sol}")
print(f"String coupling (g_s) scaling: {gs_sol}")
print(f"Mediator mass (m_phi) scaling: {m_phi_expr}")

# --- Assertions: the derived forms are what A.4 claims ---------------------
V_expected = (a3 * Mpl ** 4 / rho_DE) ** sp.Rational(1, 3)
assert sp.simplify(V_sol - V_expected) == 0, f"V mismatch: {V_sol}"

gs_expected = a1 * V_expected ** sp.Rational(2, 3) / sp.log(Mpl / L_D)
assert sp.simplify(gs_sol - gs_expected) == 0, f"g_s mismatch: {gs_sol}"

# A.4.2 pre-registration form, rearranged as an invariant relation:
#     m_phi * ln(M_Pl/Lambda_D) = C_0 * M_Pl * (rho_DE/M_Pl^4)^(1/9) * C_flux
# Solve for the C_0 the derivation actually implies, and confirm it is a pure
# product of the a_i with no residual dependence on M_Pl, rho_DE, or Lambda_D.
lhs = m_phi_expr * sp.log(Mpl / L_D)
C0_implied = sp.simplify(
    lhs / (Mpl * (rho_DE / Mpl ** 4) ** sp.Rational(1, 9) * C_flux)
)
print(f"\nImplied C_0 (from the derivation): {C0_implied}")

residual = {Mpl, rho_DE, L_D, C_flux, m_phi} & C0_implied.free_symbols
assert not residual, f"C_0 is not moduli-free; residual dependence on {residual}"

# The exponent on a3 is the load-bearing detail: it decides whether a3's
# 4-order-of-magnitude uncertainty (A.3.2) amplifies or suppresses in m_phi.
a3_exponent = C0_implied.as_powers_dict().get(a3)
print(f"Exponent on a3 in C_0:             {a3_exponent}")
assert a3_exponent == sp.Rational(-1, 9), (
    f"a3 exponent is {a3_exponent}, expected -1/9. NOTE: Appendix A.4.2 as "
    "written states C_0 = a1*a2*a3^(+1/9); the derivation gives a3^(-1/9). "
    "See the F6 disclosure in PREDICTION_APPENDIX_A.md A.4.2."
)

assert sp.simplify(C0_implied - a1 * a2 * a3 ** sp.Rational(-1, 9)) == 0, (
    f"C_0 is not a1*a2*a3^(-1/9): got {C0_implied}"
)

print("\nAll assertions passed.")
print("Note: this is a relation among symbols. No value for a1, a2, or a3 is")
print("derived or implied here -- see NO_PREDICTION_BRANCH.md (F5b).")

# Generated-by: Fable 5 (T0) under WP S3-00b | Verified-by: executed, assertions
# green; Deep Think (T0s) adversarial concurrence on the A.4.2 C_0 correction |
# Reviewed-by: T0 N (pending Xavier)
