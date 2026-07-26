#!/usr/bin/env python3
"""WP-E4: Resolvability guard against sub-voxel deformation sweeps.

Arithmetic check to prevent future sweeps from testing scales smaller than the
voxel size — the WP-E3 error class where deformations cannot move the binned
field at all, making all topological statistics degenerate by construction.

All quantities are in float64.

Cf. docs/WP_E3_REALDATA_THIRD_SCHEME_2026_07_26.md §5.1 for the incident.
"""
import numpy as np
from typing import Tuple


class ResolvabilityError(Exception):
    """Raised when a deformation scale is unresolvable at a given binning."""

    pass


def null_degeneracy(null_values, min_std_counts: float = 1.0, min_distinct: int = 3) -> dict:
    """Is a null bank able to support a Gaussian sigma at all?

    The spatial sibling of `resolvability()`. That guard catches deformations too
    small to move the binned field; this one catches null banks too degenerate to
    measure a shift against, which is the other half of the same problem and has
    now produced spurious detections five times (WP-R3, WP-H, WP-E3, the
    quarantined WP-E5 sweep, and the WP-E5 fixed-fill mode).

    Two criteria, both mechanical:

    1. **std below `min_std_counts`.** Betti numbers are integer counts. If the
       null's standard deviation is under one count, then a single-unit change in
       the statistic is already more than 1 sigma — the sigma is reporting
       quantization, not variation. Measured instances: a null with std 0.218 and
       values in {0, 1} turned a one-unit shift into 4.59 sigma.
    2. **fewer than `min_distinct` distinct values.** A null taking one or two
       values has no shape for a tail probability to be read from, so the Gaussian
       interpretation of sigma does not apply however large the sample.

    Returns a dict with `degenerate` (bool), `verdict`, the measured statistics,
    and a plain-language `note`. Callers should record the verdict rather than
    silently dropping cells, so that "untestable" stays visible as an outcome.
    """
    vals = np.asarray(null_values, dtype=np.float64)
    if vals.size == 0:
        return {"degenerate": True, "verdict": "DEGENERATE_NULL", "std": 0.0,
                "n_distinct": 0, "n_realizations": 0,
                "note": "empty null bank; nothing to measure against"}

    std = float(np.std(vals))
    n_distinct = int(np.unique(vals).size)
    reasons = []
    if std < min_std_counts:
        reasons.append(f"null std {std:.3f} < {min_std_counts} count(s), so a "
                       f"one-unit change in the statistic exceeds 1 sigma")
    if n_distinct < min_distinct:
        reasons.append(f"null takes only {n_distinct} distinct value(s) "
                       f"(< {min_distinct}); sigma is not Gaussian-interpretable")

    degenerate = bool(reasons)
    return {
        "degenerate": degenerate,
        "verdict": "DEGENERATE_NULL" if degenerate else "USABLE",
        "std": std,
        "n_distinct": n_distinct,
        "n_realizations": int(vals.size),
        "min_std_counts": float(min_std_counts),
        "min_distinct": int(min_distinct),
        "note": ("; ".join(reasons) if degenerate
                 else f"null std {std:.3f} over {n_distinct} distinct values"),
    }


def assert_null_usable(null_values, min_std_counts: float = 1.0,
                       min_distinct: int = 3) -> dict:
    """Raise if a null bank cannot support a Gaussian sigma. Returns the verdict."""
    v = null_degeneracy(null_values, min_std_counts, min_distinct)
    if v["degenerate"]:
        raise ValueError(f"degenerate null bank: {v['note']}")
    return v


def voxel_edges_mpc(extent_mpc: Tuple[float, float, float], nbins: int) -> Tuple[float, float, float]:
    """Voxel edge length per axis.

    Parameters
    ----------
    extent_mpc : tuple of float
        Field extent on each axis (x, y, z) in Mpc.
    nbins : int
        Number of bins per axis.

    Returns
    -------
    voxel_x, voxel_y, voxel_z : tuple of float
        Voxel edge length per axis (Mpc).
    """
    extent_mpc = tuple(float(e) for e in extent_mpc)
    nbins = int(nbins)
    return tuple(e / nbins for e in extent_mpc)


def resolvability(
    scale_mpc: float, extent_mpc: Tuple[float, float, float], nbins: int, min_voxels: float = 1.0
) -> dict:
    """Check whether a deformation scale is resolvable at a given binning.

    Parameters
    ----------
    scale_mpc : float
        Deformation scale in Mpc.
    extent_mpc : tuple of float
        Field extent (x, y, z) in Mpc.
    nbins : int
        Number of bins per axis.
    min_voxels : float, optional
        Minimum number of voxels the scale must span (default 1.0).
        A scale spanning < min_voxels voxels is unresolvable: it cannot
        change the binned field. min_voxels=1.0 is a necessary but
        NOT sufficient condition for genuine sensitivity.

    Returns
    -------
    dict
        Keys:
        - 'scale_mpc': input scale
        - 'nbins': input bins per axis
        - 'voxel_edges_mpc': tuple (voxel_x, voxel_y, voxel_z) in Mpc
        - 'scale_in_voxels': tuple (scale_in_voxel_x, scale_in_voxel_y, scale_in_voxel_z)
        - 'resolvable_per_axis': tuple (bool, bool, bool) for (x, y, z)
        - 'verdict': one of "UNRESOLVABLE", "PARTIALLY_RESOLVABLE", "RESOLVABLE"
        - 'note': plain-language explanation
    """
    scale_mpc = float(scale_mpc)
    extent_mpc = tuple(float(e) for e in extent_mpc)
    nbins = int(nbins)
    min_voxels = float(min_voxels)

    voxel_edges = voxel_edges_mpc(extent_mpc, nbins)
    scale_in_voxels = tuple(scale_mpc / voxel for voxel in voxel_edges)
    resolvable_per_axis = tuple(siv >= min_voxels for siv in scale_in_voxels)

    n_resolvable = sum(resolvable_per_axis)

    if n_resolvable == 0:
        verdict = "UNRESOLVABLE"
        note = f"Deformation scale {scale_mpc:.2f} Mpc is smaller than min_voxels={min_voxels} on all axes; cannot move the binned field."
    elif n_resolvable == 3:
        verdict = "RESOLVABLE"
        note = f"Deformation scale {scale_mpc:.2f} Mpc spans >= {min_voxels} voxels on all axes."
    else:
        verdict = "PARTIALLY_RESOLVABLE"
        note = f"Deformation scale {scale_mpc:.2f} Mpc is resolvable on {n_resolvable}/3 axes."

    return {
        "scale_mpc": scale_mpc,
        "nbins": nbins,
        "voxel_edges_mpc": voxel_edges,
        "scale_in_voxels": scale_in_voxels,
        "resolvable_per_axis": resolvable_per_axis,
        "verdict": verdict,
        "note": note,
    }


def required_nbins(
    scale_mpc: float, extent_mpc: Tuple[float, float, float], min_voxels: float = 1.0
) -> Tuple[int, int, int]:
    """Smallest integer nbins per axis to make scale_mpc span min_voxels voxels.

    Parameters
    ----------
    scale_mpc : float
        Deformation scale in Mpc.
    extent_mpc : tuple of float
        Field extent (x, y, z) in Mpc.
    min_voxels : float, optional
        Target number of voxels to span (default 1.0).

    Returns
    -------
    nbins_x, nbins_y, nbins_z : tuple of int
        Minimum nbins per axis: ceil(min_voxels * extent / scale).
    """
    scale_mpc = float(scale_mpc)
    extent_mpc = tuple(float(e) for e in extent_mpc)
    min_voxels = float(min_voxels)

    return tuple(int(np.ceil(min_voxels * e / scale_mpc)) for e in extent_mpc)


def assert_resolvable(
    scale_mpc: float, extent_mpc: Tuple[float, float, float], nbins: int, min_voxels: float = 1.0
) -> None:
    """Raise ResolvabilityError if scale is unresolvable.

    Call this at the top of a deformation sweep loop to catch sub-voxel scales
    before any statistics are computed.

    Parameters
    ----------
    scale_mpc : float
        Deformation scale in Mpc.
    extent_mpc : tuple of float
        Field extent (x, y, z) in Mpc.
    nbins : int
        Number of bins per axis.
    min_voxels : float, optional
        Minimum voxels to span (default 1.0).

    Raises
    ------
    ResolvabilityError
        If verdict is "UNRESOLVABLE".
    """
    result = resolvability(scale_mpc, extent_mpc, nbins, min_voxels=min_voxels)

    if result["verdict"] == "UNRESOLVABLE":
        req_nbins = required_nbins(scale_mpc, extent_mpc, min_voxels=min_voxels)
        voxel_edges = result["voxel_edges_mpc"]

        raise ResolvabilityError(
            f"Scale {scale_mpc:.2f} Mpc is unresolvable at nbins={nbins}. "
            f"Voxel edges: ({voxel_edges[0]:.2f}, {voxel_edges[1]:.2f}, {voxel_edges[2]:.2f}) Mpc. "
            f"Required nbins per axis to reach min_voxels={min_voxels}: "
            f"({req_nbins[0]}, {req_nbins[1]}, {req_nbins[2]}). "
            f"See docs/WP_E3_REALDATA_THIRD_SCHEME_2026_07_26.md §5.1."
        )


# Generated-by: Haiku 4.5 | Verified-by: pipeline/tests/test_resolvability.py | Reviewed-by: pending T0
