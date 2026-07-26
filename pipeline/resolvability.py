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
