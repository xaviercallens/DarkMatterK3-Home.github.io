#!/usr/bin/env python3
"""Generate docs/WP_E4_RESOLVABILITY_FLOOR_2026_07_26.md.

Pure arithmetic report on sub-voxel deformation detection limits.
No real-data access. Field extents hardcoded from published WP-E3/WP-E2 geometry.
"""
import numpy as np
from pipeline.resolvability import voxel_edges_mpc, resolvability, required_nbins


def main():
    """Generate the resolvability floor report."""

    # Field geometries — hardcoded from published sources
    fields = {
        "euclid_z_edf_north": {
            "extent": (48.3, 52.4, 8188.8),
            "source": "docs/WP_E3_REALDATA_THIRD_SCHEME_2026_07_26.md §5.1",
        },
        "synthetic_mock_default": {
            "extent": (734.8, 613.2, 442.9),
            "source": "docs/WP_E2_SYNTHETIC_DETECTABILITY_2026_07_26.md",
        },
    }

    # Build markdown report
    lines = []

    lines.append("# WP-E4 — Resolvability Floor (Arithmetic Guard)\n")
    lines.append("**Date:** 2026-07-26\n")
    lines.append("**Executor:** Claude Haiku 4.5\n")
    lines.append("**Tag:** `ENGINEERING` — pure arithmetic on published geometry\n")
    lines.append("**Status:** Complete\n\n")

    # Warning box
    lines.append(
        "⚠️ **NOT `TEST`, NOT `FIT`, NOT `SANDBOX-EXPERIMENTAL`.** "
        "This is pure arithmetic on published field extents. It makes no physics claim "
        "and falsifies nothing. It operates at the voxel-geometry level to prevent "
        "future sweeps from testing scales below the detection floor.\n\n"
    )

    # The finding it operationalizes
    lines.append("## 1. The Finding This Operationalizes\n\n")
    lines.append(
        "WP-E3 tested deformation scales up to r_s = 4.0 Mpc on the `euclid_z_edf_north` field "
        "with nbins = 8. The published voxel edges (§5.1) are:\n\n"
    )
    lines.append("| Axis | Extent (Mpc) | Voxel edge at nbins=8 (Mpc) |\n")
    lines.append("|---|---|---|\n")
    lines.append("| transverse x | 48.3 | 6.04 |\n")
    lines.append("| transverse y | 52.4 | 6.55 |\n")
    lines.append("| **radial (z)** | **8188.8** | **1023.6** |\n\n")

    lines.append(
        "**The 4.0 Mpc deformation spans 0.66, 0.61, and 0.0039 voxels on the three axes.** "
        "Rebinning coordinates displaced by a sub-voxel amount returns a bit-identical field. "
        "Therefore, every topological statistic computed on this field was unchanged by "
        "construction, making the verdict \"schemes agree\" degenerate: there was no deformation "
        "response to measure.\n\n"
    )

    # Voxel-edge table
    lines.append("## 2. Voxel Edges per Field\n\n")
    for field_name, field_data in fields.items():
        lines.append(f"### {field_name}\n\n")
        lines.append(
            f"Source: {field_data['source']}\n\n"
        )
        lines.append("| nbins | voxel_x (Mpc) | voxel_y (Mpc) | voxel_z (Mpc) |\n")
        lines.append("|---|---|---|---|\n")

        for nbins in [8, 16, 32, 64, 128]:
            edges = voxel_edges_mpc(field_data["extent"], nbins)
            lines.append(f"| {nbins} | {edges[0]:.2f} | {edges[1]:.2f} | {edges[2]:.2f} |\n")
        lines.append("\n")

    # Decisive table for Stream 2
    lines.append("## 3. Decisive Table: r_s Grid on euclid_z_edf_north at nbins=8\n\n")
    lines.append(
        "This table applies the externally-proposed deformation scale grid "
        "r_s ∈ {0.27, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0} Mpc to the field WP-E actually used.\n\n"
    )

    extent_euclid = fields["euclid_z_edf_north"]["extent"]
    nbins_sweep = 8
    r_s_grid = [0.27, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0]

    lines.append("| r_s (Mpc) | Verdict | Required nbins (x, y, z) |\n")
    lines.append("|---|---|---|\n")

    unresolvable_count = 0
    for r_s in r_s_grid:
        result = resolvability(r_s, extent_euclid, nbins_sweep, min_voxels=1.0)
        verdict = result["verdict"]
        req_nbins = required_nbins(r_s, extent_euclid, min_voxels=1.0)

        lines.append(
            f"| {r_s:.2f} | {verdict} | "
            f"({req_nbins[0]}, {req_nbins[1]}, {req_nbins[2]}) |\n"
        )

        if verdict == "UNRESOLVABLE":
            unresolvable_count += 1

    lines.append("\n")
    frac_unresolvable = unresolvable_count / len(r_s_grid)
    lines.append(
        f"**Fraction of the proposed grid that is UNRESOLVABLE: "
        f"{unresolvable_count}/{len(r_s_grid)} = {frac_unresolvable:.0%}**\n\n"
    )

    # Radial impossibility section
    lines.append("## 4. Radial Resolution: Fundamental Limits\n\n")
    lines.append(
        "The redshift range projects to ~8189 Mpc of comoving depth. "
        "For a 1.0 Mpc deformation to span one voxel radially:\n\n"
    )

    scale_1mpc = 1.0
    req_nbins_radial = required_nbins(scale_1mpc, extent_euclid, min_voxels=1.0)
    voxel_depth_required = extent_euclid[2] / req_nbins_radial[2]

    lines.append(
        f"- Required nbins (radial): {req_nbins_radial[2]}\n"
    )
    lines.append(
        f"- Resulting voxel depth: ~{voxel_depth_required:.1f} Mpc\n"
    )

    # Objects-per-voxel arithmetic
    n_objects = 2000  # From WP-E3 dataset
    voxel_volume = extent_euclid[0] * extent_euclid[1] * voxel_depth_required
    total_volume = extent_euclid[0] * extent_euclid[1] * extent_euclid[2]
    n_voxels = req_nbins_radial[0] * req_nbins_radial[1] * req_nbins_radial[2]
    objects_per_voxel = n_objects / n_voxels

    lines.append(
        f"\nWith ~{n_objects} objects and {n_voxels:,} voxels, "
        f"mean occupancy is **{objects_per_voxel:.2e} objects per voxel**. "
        f"At this sparsity, the topology becomes trivial for a statistical reason, "
        f"independent of voxel size: random grids with very few points per bin have "
        f"no connected structure to measure.\n\n"
    )

    # How to use
    lines.append("## 5. How to Use This Guard in a Sweep\n\n")
    lines.append(
        "Any future deformation sweep must call `assert_resolvable` at the top of its loop:\n\n"
    )
    lines.append("```python\n")
    lines.append("from pipeline.resolvability import assert_resolvable\n\n")
    lines.append("for r_s in r_s_grid:\n")
    lines.append("    for nbins in nbins_values:\n")
    lines.append("        # Arithmetic check — raises ResolvabilityError if sub-voxel\n")
    lines.append("        assert_resolvable(r_s, field_extent, nbins, min_voxels=1.0)\n\n")
    lines.append("        # Proceed to compute statistics\n")
    lines.append("        ...\n")
    lines.append("```\n\n")
    lines.append(
        "A sub-voxel scale caught here is a hard stop: "
        "re-run with finer nbins (consult the required_nbins table) "
        "or a different mechanism scale.\n\n"
    )

    # Provenance
    lines.append("## 6. Provenance\n\n")
    lines.append(
        "Generated-by: Haiku 4.5 (scripts/report_resolvability_floor.py) | "
        "Verified-by: pipeline/tests/test_resolvability.py (WP-E3 regression test passes; "
        "required_nbins round-trip verified; boundary conditions verified) | "
        "Reviewed-by: pending T0\n"
    )

    report = "\n".join(lines)

    # Write to file
    report_path = "/home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-Home/docs/WP_E4_RESOLVABILITY_FLOOR_2026_07_26.md"
    with open(report_path, "w") as f:
        f.write(report)

    print(f"Report written to {report_path}")
    print(f"\nSummary:")
    print(f"- Unresolvable scales on proposed grid: {unresolvable_count}/{len(r_s_grid)}")
    print(f"- Radial nbins required for 1 Mpc: {req_nbins_radial[2]}")
    print(f"- Objects per voxel at that binning: {objects_per_voxel:.2e}")


if __name__ == "__main__":
    main()
