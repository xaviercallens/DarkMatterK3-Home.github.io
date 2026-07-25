#!/usr/bin/env python3
"""Real observable computations (WP-E; corrected under Fable-tier review 2026-07-25).

Two observables for the pivoted pipeline:

* **κ-peak statistic** — counts of local maxima above threshold in a 2D
  weak-lensing convergence map. Standard peak-counting estimator of the lensing
  literature (peaks = pixels that are strict local maxima of their neighborhood,
  not connected super-threshold regions — a single blob with two summits is two
  peaks).
* **Betti numbers** — β₀, β₁, β₂ of the thresholded density field's voxel
  (cubical) complex. β₀ and β₂ come from connected-component labeling with the
  standard dual-connectivity pairing (26-connectivity for the foreground,
  6-connectivity for the complement). The Euler characteristic is computed
  EXACTLY as χ = V − E + F − C over the cubical complex (vertices, edges,
  faces, cubes of occupied voxels), and β₁ follows exactly from
  β₁ = β₀ + β₂ − χ. No approximations, no tuned constants.

  History note (F6 spirit): the first WP-E implementation estimated χ with a
  heuristic (`β₀ − boundary_voxels // 10`) and derived β₁ from it. Review
  against ground-truth phantoms (ring, hollow shell, single cube) showed every
  β₁/χ it returned was wrong. Since the pivot's candidate topology criterion is
  β₁ > β₀ + β₂, that quantity must be exact; this version is, and the phantom
  tests in test_observables_real.py enforce it.

Golden/synthetic data only pre-pin (hard rule 2.2); real sector evaluation is
WP-G, post-pin, behind gate G1-L.
"""
import numpy as np
from scipy import ndimage

# Dual connectivity pairing (standard digital topology): if the foreground uses
# 26-connectivity, the background must use 6-connectivity, or components/cavities
# are miscounted at diagonal contacts.
_CONN_26 = np.ones((3, 3, 3), dtype=bool)
_CONN_6 = ndimage.generate_binary_structure(3, 1)


def compute_kappa_peak_statistic(convergence_map: np.ndarray,
                                 threshold: float = 0.5) -> dict:
    """Count local maxima above `threshold` in a 2D convergence map.

    A peak is a pixel whose value equals the maximum of its 3×3 neighborhood
    and exceeds `threshold`. Plateau maxima (ties across adjacent pixels) are
    counted once per plateau via connected-component labeling of the maximum
    set — so a flat-topped peak is one peak, not several.

    Returns dict: peak_count, peak_density (peaks per map, area normalization
    deferred to WP-G when a real map with survey geometry exists),
    mean_peak_value, std_peak_value.
    """
    kappa = np.asarray(convergence_map, dtype=np.float64)

    local_max = (ndimage.maximum_filter(kappa, size=3, mode="nearest") == kappa)
    candidates = local_max & (kappa > threshold)

    labeled, n_peaks = ndimage.label(candidates)
    if n_peaks == 0:
        return {"peak_count": 0, "peak_density": 0.0,
                "mean_peak_value": 0.0, "std_peak_value": 0.0}

    peak_values = ndimage.maximum(kappa, labels=labeled,
                                  index=np.arange(1, n_peaks + 1))
    peak_values = np.atleast_1d(peak_values)

    return {
        "peak_count": int(n_peaks),
        "peak_density": float(n_peaks),
        "mean_peak_value": float(np.mean(peak_values)),
        "std_peak_value": float(np.std(peak_values)),
    }


def _euler_characteristic_cubical(mask: np.ndarray) -> int:
    """Exact Euler characteristic of the cubical complex of occupied voxels.

    χ = V − E + F − C, where a vertex/edge/face belongs to the complex iff at
    least one voxel containing it is occupied. Computed by OR-ing shifted
    copies of the zero-padded mask (padding makes every boundary cell interior
    to the array, so no special-casing).
    """
    m = np.pad(np.asarray(mask, dtype=bool), 1)

    C = int(m.sum())

    # Faces: 3 orientations; a face between two axis-adjacent cells exists iff
    # either cell is occupied.
    F = int((m[:-1] | m[1:]).sum()
            + (m[:, :-1] | m[:, 1:]).sum()
            + (m[:, :, :-1] | m[:, :, 1:]).sum())

    # Edges: 3 orientations; an edge is shared by 4 cells across the two
    # transverse axes.
    E = int((m[:, :-1, :-1] | m[:, 1:, :-1] | m[:, :-1, 1:] | m[:, 1:, 1:]).sum()
            + (m[:-1, :, :-1] | m[1:, :, :-1] | m[:-1, :, 1:] | m[1:, :, 1:]).sum()
            + (m[:-1, :-1, :] | m[1:, :-1, :] | m[:-1, 1:, :] | m[1:, 1:, :]).sum())

    # Vertices: shared by 8 cells.
    V = int((m[:-1, :-1, :-1] | m[1:, :-1, :-1] | m[:-1, 1:, :-1] | m[:-1, :-1, 1:]
             | m[1:, 1:, :-1] | m[1:, :-1, 1:] | m[:-1, 1:, 1:] | m[1:, 1:, 1:]).sum())

    return V - E + F - C


def compute_betti_numbers(density_field: np.ndarray,
                          threshold_percentile: float = 50.0,
                          threshold_value: float | None = None) -> dict:
    """β₀, β₁, β₂ and exact χ of the thresholded field's voxel complex.

    Thresholding: `threshold_value` if given, else the `threshold_percentile`
    of the field. Mask is `field > threshold` (strict; note this empties the
    mask if the percentile lands on the max — pass threshold_value for binary
    fields).

    β₀: 26-connected components of the mask.
    β₂: 6-connected components of the complement, minus components touching
        the array boundary (the outer "void" is not a cavity).
    χ:  exact cubical-complex Euler characteristic (see helper).
    β₁: exactly β₀ + β₂ − χ.

    Citation: cosmic-web TDA via Betti numbers / Euler characteristic
    (persistent-homology literature); exact voxel χ is the standard
    inclusion–exclusion count over the cubical complex.
    """
    rho = np.asarray(density_field, dtype=np.float64)
    thresh = (threshold_value if threshold_value is not None
              else float(np.percentile(rho, threshold_percentile)))
    mask = rho > thresh

    _, beta_0 = ndimage.label(mask, structure=_CONN_26)
    beta_0 = int(beta_0)

    # Cavities: 6-connected complement components not touching the boundary.
    labeled_c, n_c = ndimage.label(~mask, structure=_CONN_6)
    boundary_labels = set(np.unique(labeled_c[0, :, :])) | set(np.unique(labeled_c[-1, :, :])) \
        | set(np.unique(labeled_c[:, 0, :])) | set(np.unique(labeled_c[:, -1, :])) \
        | set(np.unique(labeled_c[:, :, 0])) | set(np.unique(labeled_c[:, :, -1]))
    boundary_labels.discard(0)
    beta_2 = int(n_c - len(boundary_labels))

    euler_char = _euler_characteristic_cubical(mask)
    beta_1 = beta_0 + beta_2 - euler_char

    # beta_1 < 0 would mean the labeling conventions and chi disagree — that is
    # a bug, not a topology, and must surface loudly rather than be clamped.
    assert beta_1 >= 0, (
        f"inconsistent topology bookkeeping: b0={beta_0}, b2={beta_2}, chi={euler_char}"
    )

    return {"beta_0": beta_0, "beta_1": int(beta_1),
            "beta_2": beta_2, "euler_char": int(euler_char)}


# Generated-by: Haiku 4.5 (WP-E draft) + Fable 5 (corrective rewrite, same day) |
# Verified-by: phantom golden tests in pipeline/tests/test_observables_real.py
# (ring/shell/cube ground truths), executed | Reviewed-by: T0 N (pending)
