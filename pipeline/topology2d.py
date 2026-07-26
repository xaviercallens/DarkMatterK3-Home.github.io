#!/usr/bin/env python3
"""2D projected topology: Betti numbers of a thresholded 2D density field.

Built for the revised WP-E protocol (T0 cross-stream consolidation, 2026-07-26,
§3–§4): photometric fields have no usable radial resolution (σ_z ≈ 0.05(1+z) ≈
10² Mpc; the measured radial voxel at nbins=8 is ~1 Gpc — see
docs/WP_E3_REALDATA_THIRD_SCHEME_2026_07_26.md §5.1), so topology on photo-z data
is computed on 2D transverse projections, deliberately and by declaration rather
than by accident.

Conventions (the 2D analogue of pipeline/observables_real.compute_betti_numbers):
  mask = field > threshold (strict)
  β₀ : 8-connected components of the mask (foreground squares touching even at a
       corner are one component — matches the closed-pixel cubical complex).
  β₁ : holes = 4-connected components of the complement that do NOT touch the
       array border (the outer region is not a hole). 4-connectivity for the
       background is the correct dual of 8-connectivity for the foreground.
  χ  : computed INDEPENDENTLY from the cubical complex (V − E + F over closed
       unit-square pixels), then asserted equal to β₀ − β₁. A disagreement means
       the labeling conventions and the complex disagree — that is a bug to
       crash on, never to paper over (same discipline as the 3D module's
       β₁ ≥ 0 assertion).
"""
import numpy as np
from scipy import ndimage

# 8-connectivity for foreground, 4-connectivity (cross) for background holes.
_CONN_8 = np.ones((3, 3), dtype=int)
_CONN_4 = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=int)


def _euler_characteristic_pixels(mask: np.ndarray) -> int:
    """Exact χ = V − E + F of the closed-pixel cubical complex.

    Each True pixel (i, j) is the closed unit square [i,i+1]×[j,j+1]. V counts
    grid vertices covered by ≥1 pixel, E covered unit edges, F pixels. Corner-
    touching squares share a vertex, which is exactly why foreground β₀ must use
    8-connectivity for χ = β₀ − β₁ to hold.
    """
    h, w = mask.shape
    f = int(mask.sum())

    # Vertices: (h+1)×(w+1) grid points; covered if any incident pixel is on.
    v_grid = np.zeros((h + 1, w + 1), dtype=bool)
    v_grid[:h, :w] |= mask
    v_grid[1:, :w] |= mask
    v_grid[:h, 1:] |= mask
    v_grid[1:, 1:] |= mask
    v = int(v_grid.sum())

    # Horizontal edges: (h+1)×w; covered if the pixel above or below is on.
    e_h = np.zeros((h + 1, w), dtype=bool)
    e_h[:h] |= mask
    e_h[1:] |= mask
    # Vertical edges: h×(w+1); covered if the pixel left or right is on.
    e_v = np.zeros((h, w + 1), dtype=bool)
    e_v[:, :w] |= mask
    e_v[:, 1:] |= mask
    e = int(e_h.sum()) + int(e_v.sum())

    return v - e + f


def compute_betti_numbers_2d(density_field: np.ndarray,
                             threshold_percentile: float = 50.0,
                             threshold_value: float | None = None) -> dict:
    """β₀, β₁ and exact χ of a thresholded 2D field's pixel complex.

    Thresholding matches the 3D module: `threshold_value` if given, else the
    `threshold_percentile` of the field; mask is strictly `field > threshold`.

    Returns {"beta_0": int, "beta_1": int, "euler_char": int}. There is no β₂
    in 2D; callers migrating from 3D must not expect one.
    """
    rho = np.asarray(density_field, dtype=np.float64)
    if rho.ndim != 2:
        raise ValueError(f"compute_betti_numbers_2d needs a 2D field, got ndim={rho.ndim}")
    thresh = (threshold_value if threshold_value is not None
              else float(np.percentile(rho, threshold_percentile)))
    mask = rho > thresh

    _, beta_0 = ndimage.label(mask, structure=_CONN_8)
    beta_0 = int(beta_0)

    # Holes: 4-connected background components not touching the border.
    bg_labels, n_bg = ndimage.label(~mask, structure=_CONN_4)
    border = np.unique(np.concatenate([
        bg_labels[0, :], bg_labels[-1, :], bg_labels[:, 0], bg_labels[:, -1]
    ]))
    border = set(int(x) for x in border if x != 0)
    beta_1 = int(n_bg - len(border))

    euler = _euler_characteristic_pixels(mask)
    assert beta_0 - beta_1 == euler, (
        f"inconsistent 2D topology bookkeeping: b0={beta_0}, b1={beta_1}, chi={euler}"
    )
    return {"beta_0": beta_0, "beta_1": beta_1, "euler_char": euler}


# Generated-by: Claude Fable 5 (Stream 3, T0-directed revised WP-E protocol
# 2026-07-26) | Verified-by: pipeline/tests/test_topology2d.py (golden shapes with
# hand-computed Betti numbers, independent Euler cross-check asserted on every
# call) | Reviewed-by: pending T0
