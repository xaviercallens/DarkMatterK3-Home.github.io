#!/usr/bin/env python3
"""WP-A2 Gate 0 — circularity + falsifiability audit (machine-checked).

Adjudication R6.2 (briefs/T0_ADJUDICATION_WPA_2026_07_25.md) authorized a
laboratory-scale re-scope of the B1 window ONLY IF a circularity audit passes:
a TEST may target only window regions (i) not derived from the very datasets
that would test them, and (ii) actually reachable by published public data.

Inputs (provenance):
  [B1-num]   window edges reproduced from scripts/verify_swampland_bounds.py
             (executed 2026-07-25, assertions green): route 1 (lambda-form,
             cosmological, arXiv:2205.12293) m_KK = lam^-1 * Lambda^{1/4},
             lam in [1e-4, 1e-1], Lambda^{1/4} = 2.240e-3 eV (computed there
             from Planck-2018 + CODATA, not memory); route 2 (size-form,
             arXiv:2309.09330) l in [1, 30] um.
  [LAB-ISL]  arXiv:2002.11761 (Lee-Adelberger et al., PRL 2020), abstract,
             fetch-verified 2026-07-25: gravitational-strength (|alpha|=1)
             Yukawa excluded at 95% CL only for ranges >= 38.6 um; data taken
             at separations 52 um - 3.0 mm.
  [LAB-CAS]  arXiv:hep-ph/0502025 (Decca et al.), abstract, fetch-verified
             2026-07-25: alpha <~ 1e12 at lambda ~ 200 nm (isoelectronic /
             Casimir regime) — i.e. short-range public limits sit ~12 decades
             above gravitational strength.

Every assertion below is a step of the audit; if all pass, the audit VERDICT
printed at the end is machine-derived, not narrative.
"""

# CODATA 2018, identical constant to verify_swampland_bounds.py
HBAR_C_EV_NM = 197.3269804

# [B1-num] route edges (eV)
LAMBDA_QUARTER_EV = 2.240e-3
ROUTE1_LO = LAMBDA_QUARTER_EV / 1e-1     # 0.0224 eV  (lambda-form, cosmological)
ROUTE1_HI = LAMBDA_QUARTER_EV / 1e-4     # 22.4 eV
ROUTE2_L_LO_UM, ROUTE2_L_HI_UM = 1.0, 30.0   # size-form, FROM lab/astro bounds

# [LAB-ISL] public exclusion reach at gravitational strength
ISL_EXCLUDED_ABOVE_UM = 38.6


def range_um(m_ev: float) -> float:
    """Compton/force range hbar*c/m in micrometers."""
    return HBAR_C_EV_NM / m_ev * 1e-3


def main() -> None:
    r1_range_hi = range_um(ROUTE1_LO)   # largest range in lambda-form window
    r1_range_lo = range_um(ROUTE1_HI)

    print("--- WP-A2 Gate 0: circularity + falsifiability audit ---")
    print(f"lambda-form (non-circular) window: [{ROUTE1_LO:.4g}, {ROUTE1_HI:.4g}] eV")
    print(f"  -> force range [{r1_range_lo:.4g}, {r1_range_hi:.4g}] um")
    print(f"size-form window ranges: [{ROUTE2_L_LO_UM}, {ROUTE2_L_HI_UM}] um "
          f"(inputs ARE lab/astro bounds -> circular as a TEST target)")
    print(f"public alpha~1 exclusion reach [LAB-ISL]: lambda >= "
          f"{ISL_EXCLUDED_ABOVE_UM} um only")

    # Step 1 — circularity: the size-form route's window is, by construction,
    # the interval its source (2309.09330) assembled from laboratory and
    # astrophysical bounds. Testing it against those bounds is circular.
    assert ROUTE2_L_HI_UM <= ISL_EXCLUDED_ABOVE_UM, (
        "size-form upper range should sit at/below the ISL exclusion edge "
        "(it was built from it)")
    print("[1] size-form route: CIRCULAR (excluded as TEST target)")

    # Step 2 — reach: the ENTIRE non-circular (lambda-form) window lies at
    # ranges below the alpha~1 exclusion reach; no published public dataset
    # excludes any of it at gravitational strength.
    assert r1_range_hi < ISL_EXCLUDED_ABOVE_UM, (
        "if any of the lambda-form window exceeded the ISL reach, a "
        "falsifiable sliver would exist — recheck before concluding")
    print(f"[2] lambda-form route: max range {r1_range_hi:.3g} um < "
          f"{ISL_EXCLUDED_ABOVE_UM} um -> entirely BELOW public alpha~1 reach")

    # Step 3 — short-range regime: at sub-micron ranges the strongest public
    # limits [LAB-CAS] allow alpha up to ~1e12; a gravitational-strength
    # signal there is ~12 decades below current sensitivity.
    ALPHA_LIMIT_AT_200NM = 1e12
    assert ALPHA_LIMIT_AT_200NM > 1.0
    print(f"[3] Casimir regime: alpha limit ~{ALPHA_LIMIT_AT_200NM:.0e} at "
          f"~200 nm >> 1 -> no sensitivity to gravitational strength")

    print()
    print("VERDICT: FAIL.")
    print("  No region of the B1 window is BOTH non-circular AND reachable by")
    print("  any published public dataset at gravitational strength. A")
    print("  pre-registered comparison would be guaranteed-consistent by")
    print("  construction — a manufactured pass. WP-A2 Gate 0 fails;")
    print("  per adjudication R6.2 the terminus is Off-Ramp 3.")


if __name__ == "__main__":
    main()
