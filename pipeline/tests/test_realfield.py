#!/usr/bin/env python3
"""Golden tests for realfield.py (WP-R2).

Tests on hand-built tiny catalogs with known properties:
1. Uniform distribution → flat field
2. Single cluster → one peak
3. Two clusters → two peaks
"""

import pytest
import numpy as np
from pipeline.realfield import density_field_from_catalog


def test_uniform_distribution():
    """Uniform random distribution → flat field (all cells ≈ 1)."""
    np.random.seed(42)
    n = 1000
    ra = np.random.uniform(0, 10, n)
    dec = np.random.uniform(-10, 0, n)

    field = density_field_from_catalog(ra, dec, nbins=8)
    assert field.shape == (8, 8)
    assert field.mean() == pytest.approx(1.0, abs=0.05)
    # Uniform field should have all cells close to 1 (within ~2x due to Poisson noise)
    assert (field < 3.0).all()
    assert (field > 0.1).all()


def test_single_cluster():
    """Catalog with all objects in one bin → single peak."""
    # All objects at (RA=5.0±0.1, Dec=-5.0±0.1)
    np.random.seed(42)
    n = 500
    ra = np.random.normal(5.0, 0.1, n)
    dec = np.random.normal(-5.0, 0.1, n)

    field = density_field_from_catalog(ra, dec, nbins=8)
    # Peak should be at central bin (high value)
    max_val = field.max()
    assert max_val > 5.0  # Concentrated distribution


def test_two_clusters_3d():
    """3D catalog with two clusters (RA, Dec, z) → two peaks."""
    np.random.seed(42)
    # Cluster 1: (RA=2, Dec=-5, z=0.1)
    n1 = 200
    ra1 = np.random.normal(2.0, 0.1, n1)
    dec1 = np.random.normal(-5.0, 0.1, n1)
    z1 = np.random.normal(0.1, 0.01, n1)

    # Cluster 2: (RA=8, Dec=5, z=0.5)
    n2 = 200
    ra2 = np.random.normal(8.0, 0.1, n2)
    dec2 = np.random.normal(5.0, 0.1, n2)
    z2 = np.random.normal(0.5, 0.05, n2)

    ra = np.concatenate([ra1, ra2])
    dec = np.concatenate([dec1, dec2])
    z = np.concatenate([z1, z2])

    field = density_field_from_catalog(ra, dec, z, nbins=8)
    assert field.shape == (8, 8, 8)
    # Field should have two prominent regions
    assert field.max() > 3.0
    assert field.min() < 0.2


def test_mean_normalization():
    """Field is normalized to mean 1."""
    np.random.seed(42)
    n = 500
    ra = np.random.uniform(0, 10, n)
    dec = np.random.uniform(-10, 0, n)

    field = density_field_from_catalog(ra, dec, nbins=10)
    assert field.mean() == pytest.approx(1.0, abs=1e-5)


def test_empty_catalog():
    """Empty catalog → all-ones field (no objects, uniform prior)."""
    ra = np.array([])
    dec = np.array([])

    field = density_field_from_catalog(ra, dec, nbins=4)
    assert field.shape == (4, 4)
    assert (field == 1.0).all()  # Empty → ones


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
