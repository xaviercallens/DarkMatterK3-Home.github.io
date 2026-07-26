"""Golden tests for pipeline/topology2d.py — hand-computed Betti numbers.

Every case's expected values were derived by hand from the definitions
(8-connected foreground, 4-connected non-border background holes, cubical χ),
not from running the code. The in-function assertion β₀ − β₁ == χ additionally
cross-checks every call against the independent V−E+F computation.
"""
import numpy as np
import pytest

from pipeline.topology2d import compute_betti_numbers_2d


def _field(mask):
    """Binary mask -> float field where mask==1.0, else 0.0; threshold at 0.5."""
    return np.asarray(mask, dtype=np.float64)


def _betti(mask):
    return compute_betti_numbers_2d(_field(mask), threshold_value=0.5)


def test_empty_field():
    r = _betti(np.zeros((5, 5)))
    assert r == {"beta_0": 0, "beta_1": 0, "euler_char": 0}


def test_full_field():
    r = _betti(np.ones((5, 5)))
    assert r == {"beta_0": 1, "beta_1": 0, "euler_char": 1}


def test_solid_block():
    m = np.zeros((5, 5)); m[1:4, 1:4] = 1
    r = _betti(m)
    assert r == {"beta_0": 1, "beta_1": 0, "euler_char": 1}


def test_ring_has_one_hole():
    m = np.zeros((5, 5)); m[1:4, 1:4] = 1; m[2, 2] = 0
    r = _betti(m)
    assert r == {"beta_0": 1, "beta_1": 1, "euler_char": 0}


def test_two_separate_blocks():
    m = np.zeros((7, 7)); m[1:3, 1:3] = 1; m[4:6, 4:6] = 1
    r = _betti(m)
    # Blocks at (1:3,1:3) and (4:6,4:6) do not touch, even diagonally.
    assert r == {"beta_0": 2, "beta_1": 0, "euler_char": 2}


def test_diagonal_touch_is_connected():
    # Two pixels sharing only a corner: one 8-connected component, chi=1
    # (V=7, E=8, F=2 -> 7-8+2=1), so beta_1=0.
    m = np.zeros((4, 4)); m[1, 1] = 1; m[2, 2] = 1
    r = _betti(m)
    assert r == {"beta_0": 1, "beta_1": 0, "euler_char": 1}


def test_diagonal_gap_is_not_a_hole():
    # A 2x2 block with one pixel missing: the notch touches the outside via
    # 4-connectivity? The missing corner of a 2x2 is border-adjacent here, so
    # no hole. Explicit small case: L-shape.
    m = np.zeros((4, 4)); m[1, 1] = 1; m[1, 2] = 1; m[2, 1] = 1
    r = _betti(m)
    assert r == {"beta_0": 1, "beta_1": 0, "euler_char": 1}


def test_two_rings():
    m = np.zeros((5, 9))
    m[1:4, 1:4] = 1; m[2, 2] = 0
    m[1:4, 5:8] = 1; m[2, 6] = 0
    r = _betti(m)
    assert r == {"beta_0": 2, "beta_1": 2, "euler_char": 0}


def test_big_ring_thick_walls():
    m = np.zeros((8, 8)); m[1:7, 1:7] = 1; m[3:5, 3:5] = 0
    r = _betti(m)
    assert r == {"beta_0": 1, "beta_1": 1, "euler_char": 0}


def test_percentile_thresholding_matches_3d_convention():
    rng = np.random.default_rng(0)
    f = rng.random((16, 16))
    r_pct = compute_betti_numbers_2d(f, threshold_percentile=50.0)
    r_val = compute_betti_numbers_2d(f, threshold_value=float(np.percentile(f, 50.0)))
    assert r_pct == r_val


def test_rejects_3d_input():
    with pytest.raises(ValueError):
        compute_betti_numbers_2d(np.zeros((4, 4, 4)))


def test_negative_control_shuffle_changes_topology():
    """D-1: the statistic must respond to spatial rearrangement. A structured
    field (one big ring) and a shuffle of its pixels must not share topology
    for every seed — if they always did, the statistic would be reading the
    histogram, not the arrangement."""
    m = np.zeros((12, 12)); m[2:10, 2:10] = 1; m[5:7, 5:7] = 0
    base = _betti(m)
    rng = np.random.default_rng(3)
    diffs = 0
    for _ in range(10):
        flat = m.flatten(); rng.shuffle(flat)
        r = _betti(flat.reshape(m.shape))
        if r != base:
            diffs += 1
    assert diffs > 0, "shuffled fields never changed topology — statistic is degenerate"


# Generated-by: Claude Fable 5 | Verified-by: expected values hand-computed from
# the definitions before the module was run | Reviewed-by: pending T0
