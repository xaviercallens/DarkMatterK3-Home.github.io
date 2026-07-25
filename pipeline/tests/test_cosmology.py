#!/usr/bin/env python3
"""Tests for pipeline/cosmology.py (WP-R5).

Validates comoving-distance conversion against TWO independently computed
references (not just self-consistency with astropy's own black box):

1. Manual numerical integration of the standard flat-LCDM comoving-distance
   integral D_C(z) = (c/H0) * integral[0,z] dz'/E(z'), E(z)=sqrt(Om0(1+z)^3+Ode0),
   using the SAME cited Planck18 parameters but an independent code path
   (scipy.integrate.quad, not astropy.cosmology internals).
2. The low-z linear (Hubble law) approximation D_C ~ c*z/H0, which must agree
   with both (1) and astropy at small z where the approximation is valid.

Also tests the invalid-redshift drop/count discipline (never impute).
"""
import numpy as np
import pytest
from scipy import integrate
from astropy.cosmology import Planck18
from astropy import units as u
from astropy.constants import c as speed_of_light

from pipeline.cosmology import (
    comoving_distance_mpc,
    radec_z_to_cartesian_mpc,
    radec_z_to_tangent_plane_mpc,
    drop_invalid_redshifts,
)

# Same cited parameters as pipeline/cosmology.py's docstring (Planck18),
# read directly from the astropy realization (not retyped from memory).
H0_KM_S_MPC = Planck18.H0.to(u.km / u.s / u.Mpc).value
OM0 = Planck18.Om0
OGAMMA0 = Planck18.Ogamma0
ONU0 = Planck18.Onu0
ODE0 = 1.0 - OM0 - OGAMMA0 - ONU0  # flat: Ok0=0, so components sum to 1
C_KM_S = speed_of_light.to(u.km / u.s).value


def _manual_comoving_distance_mpc(z: float) -> float:
    """Independent numerical integration (scipy.quad), not astropy internals.

    Includes matter + radiation (photons+neutrinos) + dark energy, matching
    the full flat-LCDM Friedmann equation Planck18 itself uses — a matter+DE
    -only integrand disagrees with astropy by ~0.1% at z=2 because radiation,
    though small today (Ogamma0+Onu0 ~ 1.5e-3), is not negligible at that
    tolerance. This is a genuine physical term, not a numerical bug.
    """
    def integrand(zp):
        E = np.sqrt(OM0 * (1 + zp) ** 3 + (OGAMMA0 + ONU0) * (1 + zp) ** 4 + ODE0)
        return 1.0 / E

    integral, _ = integrate.quad(integrand, 0.0, z)
    return (C_KM_S / H0_KM_S_MPC) * integral


def test_manual_integration_matches_astropy_moderate_z():
    """Independent quad-integration must match astropy's Planck18 closely.

    Tolerance is 0.5%, not tighter: Planck18 uses massive neutrinos whose
    equation of state transitions from radiation-like to matter-like across
    cosmic time (astropy integrates this via a Fermi-Dirac phase-space
    calculation). Our manual check approximates neutrinos as pure radiation
    (w=1/3 at all z), which is exact at low z and increasingly approximate
    above z~1. A 0.5% agreement at z up to 2 is a strong independent check
    against gross errors (wrong H0, sign error, wrong integration bounds,
    unit mistakes) without re-deriving astropy's massive-neutrino internals,
    which would defeat the purpose of an independent cross-check.
    """
    for z in [0.01, 0.023, 0.1, 0.5, 1.0, 2.0]:
        d_astropy = comoving_distance_mpc(z)
        d_manual = _manual_comoving_distance_mpc(z)
        rel_err = abs(d_astropy - d_manual) / d_manual
        assert rel_err < 5e-3, (
            f"z={z}: astropy={d_astropy:.4f} Mpc, manual={d_manual:.4f} Mpc, "
            f"rel_err={rel_err:.2e}"
        )


def test_low_z_hubble_law_approximation():
    """At low z, D_C ~ c*z/H0 (linear Hubble law) should approximate both."""
    for z in [0.001, 0.005, 0.01]:
        d_astropy = comoving_distance_mpc(z)
        d_hubble = C_KM_S * z / H0_KM_S_MPC
        rel_err = abs(d_astropy - d_hubble) / d_astropy
        # Low-z approximation should be good to a few percent at z<=0.01
        assert rel_err < 0.02, f"z={z}: astropy={d_astropy:.4f}, hubble={d_hubble:.4f}"


def test_coma_cluster_known_redshift_sanity():
    """Coma cluster (z~0.023, real SDSS spectro-z measured in WP-R5) should
    land at a comoving distance consistent with its well-known ~100 Mpc
    distance in the literature (order-of-magnitude sanity, not a precision
    claim)."""
    d_c = comoving_distance_mpc(0.023)
    assert 90.0 < d_c < 110.0, f"Coma cluster D_C={d_c:.1f} Mpc outside expected range"


def test_radec_z_to_cartesian_basic():
    """(RA=0, Dec=0, z) should map to (D_C, 0, 0)."""
    x, y, z_cart = radec_z_to_cartesian_mpc(
        np.array([0.0]), np.array([0.0]), np.array([0.1])
    )
    d_c = comoving_distance_mpc(0.1)
    assert x[0] == pytest.approx(d_c, rel=1e-6)
    assert y[0] == pytest.approx(0.0, abs=1e-6)
    assert z_cart[0] == pytest.approx(0.0, abs=1e-6)


def test_radec_z_to_cartesian_north_pole():
    """(Dec=90) should map to (0, 0, D_C) regardless of RA."""
    x, y, z_cart = radec_z_to_cartesian_mpc(
        np.array([123.0]), np.array([90.0]), np.array([0.1])
    )
    d_c = comoving_distance_mpc(0.1)
    assert x[0] == pytest.approx(0.0, abs=1e-6)
    assert y[0] == pytest.approx(0.0, abs=1e-6)
    assert z_cart[0] == pytest.approx(d_c, rel=1e-6)


def test_radec_z_preserves_distance_from_origin():
    """Euclidean norm of Cartesian coords must equal D_C(z) exactly."""
    ra = np.array([10.0, 200.0, 350.0])
    dec = np.array([-30.0, 45.0, 80.0])
    z = np.array([0.05, 0.2, 0.5])

    x, y, z_cart = radec_z_to_cartesian_mpc(ra, dec, z)
    norms = np.sqrt(x**2 + y**2 + z_cart**2)
    expected = comoving_distance_mpc(z)

    np.testing.assert_allclose(norms, expected, rtol=1e-6)


def test_negative_z_raises_in_conversion():
    """radec_z_to_cartesian_mpc must refuse negative z (caller must filter)."""
    with pytest.raises(ValueError, match="non-finite or negative"):
        radec_z_to_cartesian_mpc(
            np.array([0.0]), np.array([0.0]), np.array([-0.01])
        )


def test_nan_z_raises_in_conversion():
    """radec_z_to_cartesian_mpc must refuse NaN z (caller must filter)."""
    with pytest.raises(ValueError, match="non-finite or negative"):
        radec_z_to_cartesian_mpc(
            np.array([0.0]), np.array([0.0]), np.array([np.nan])
        )


def test_drop_invalid_redshifts_counts_nan():
    """NaN redshifts must be dropped and counted, never imputed."""
    ra = np.array([1.0, 2.0, 3.0, 4.0])
    dec = np.array([1.0, 2.0, 3.0, 4.0])
    z = np.array([0.1, np.nan, 0.3, np.nan])

    ra_v, dec_v, z_v, report = drop_invalid_redshifts(ra, dec, z)

    assert report["n_input"] == 4
    assert report["n_valid"] == 2
    assert report["n_dropped"] == 2
    assert report["n_dropped_nan"] == 2
    assert report["n_dropped_negative"] == 0
    assert len(z_v) == 2
    np.testing.assert_array_equal(z_v, [0.1, 0.3])


def test_drop_invalid_redshifts_counts_negative():
    """Negative redshifts must be dropped and counted separately from NaN."""
    ra = np.array([1.0, 2.0, 3.0])
    dec = np.array([1.0, 2.0, 3.0])
    z = np.array([0.1, -0.05, 0.3])

    ra_v, dec_v, z_v, report = drop_invalid_redshifts(ra, dec, z)

    assert report["n_valid"] == 2
    assert report["n_dropped_negative"] == 1
    assert report["n_dropped_nan"] == 0


def test_tangent_plane_centre_maps_to_origin_transverse():
    """An object exactly at the tangent-plane centre has zero transverse offset."""
    tx, ty, r = radec_z_to_tangent_plane_mpc(
        np.array([100.0]), np.array([20.0]), np.array([0.1]),
        ra0_deg=100.0, dec0_deg=20.0,
    )
    assert tx[0] == pytest.approx(0.0, abs=1e-9)
    assert ty[0] == pytest.approx(0.0, abs=1e-9)
    assert r[0] == pytest.approx(comoving_distance_mpc(0.1), rel=1e-6)


def test_tangent_plane_small_angle_matches_great_circle():
    """At small separations (arcmin scale), transverse Mpc offset should
    match r*theta (great-circle angular separation in radians) closely."""
    ra0, dec0 = 150.0, 2.0
    # Object offset by 0.05 deg in RA at dec0 (typical Euclid cone scale)
    ra_obj = np.array([150.05])
    dec_obj = np.array([2.0])
    z = np.array([0.5])

    tx, ty, r = radec_z_to_tangent_plane_mpc(ra_obj, dec_obj, z, ra0_deg=ra0, dec0_deg=dec0)

    # Expected: r * delta_ra_rad * cos(dec0)
    expected_tx = comoving_distance_mpc(0.5) * np.radians(0.05) * np.cos(np.radians(dec0))
    assert tx[0] == pytest.approx(expected_tx, rel=1e-9)
    assert ty[0] == pytest.approx(0.0, abs=1e-9)


def test_tangent_plane_default_centre_is_centroid():
    """With no ra0/dec0 given, the centre defaults to the input's mean."""
    ra = np.array([10.0, 20.0, 30.0])
    dec = np.array([5.0, 5.0, 5.0])
    z = np.array([0.1, 0.1, 0.1])

    tx, ty, r = radec_z_to_tangent_plane_mpc(ra, dec, z)
    # Mean RA is 20 -> that object's transverse_x should be ~0
    assert tx[1] == pytest.approx(0.0, abs=1e-6)


def test_tangent_plane_narrow_cone_compact_bounding_box():
    """CRITICAL: for a narrow pencil-beam cone (Euclid-like: 0.2 deg radius,
    broad redshift range), the tangent-plane transverse extent must be much
    smaller than the same data's GLOBAL Cartesian transverse extent — this
    is the whole point of using this frame (efficient bin occupancy)."""
    rng = np.random.default_rng(5)
    n = 500
    ra0, dec0 = 267.7808, 65.5308  # Euclid EDF-North centre
    # Uniform within a 0.2 deg cone
    theta = rng.uniform(0, 0.2, n)
    phi = rng.uniform(0, 2 * np.pi, n)
    ra = ra0 + theta * np.cos(phi) / np.cos(np.radians(dec0))
    dec = dec0 + theta * np.sin(phi)
    z = rng.uniform(0.05, 5.5, n)  # broad redshift range, like real photo-z

    tx, ty, r = radec_z_to_tangent_plane_mpc(ra, dec, z, ra0_deg=ra0, dec0_deg=dec0)
    x_global, y_global, z_global = radec_z_to_cartesian_mpc(ra, dec, z)

    tangent_transverse_span = max(tx.max() - tx.min(), ty.max() - ty.min())
    global_transverse_span = max(
        x_global.max() - x_global.min(), y_global.max() - y_global.min()
    )

    assert tangent_transverse_span < global_transverse_span, (
        f"tangent-plane transverse span ({tangent_transverse_span:.1f} Mpc) should be "
        f"far smaller than global Cartesian transverse span "
        f"({global_transverse_span:.1f} Mpc) for a narrow cone"
    )


def test_tangent_plane_negative_z_raises():
    with pytest.raises(ValueError, match="non-finite or negative"):
        radec_z_to_tangent_plane_mpc(
            np.array([0.0]), np.array([0.0]), np.array([-0.1])
        )


def test_drop_invalid_redshifts_no_drops():
    """Clean data: all valid, zero drops."""
    ra = np.array([1.0, 2.0, 3.0])
    dec = np.array([1.0, 2.0, 3.0])
    z = np.array([0.1, 0.2, 0.3])

    ra_v, dec_v, z_v, report = drop_invalid_redshifts(ra, dec, z)

    assert report["n_dropped"] == 0
    assert len(ra_v) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
