#!/usr/bin/env python3
"""WP-E2: Controlled-injection detectability sweep on synthetic catalogs.

**ALL RESULTS ARE SYNTHETIC CONTROLLED-INJECTION — NOT A MEASUREMENT OF ANY SURVEY,
NOT A TEST OF ANY HYPOTHESIS.**

Pre-registered decision rule (state verbatim in all output):

**Statistic:** β₁ and β₂ only. β₀ computed and reported for completeness but NOT used
for any verdict. Rationale: WP-R7 (docs/WP_R7_BETA_VARIANCE_SCAN.md) shows β₁/β₂ carry
nonzero null variance at 30/30 scanned (threshold, scheme) combinations vs β₀'s 14/30.

**Tail:** Two-sided test, committed in advance. Detection criterion per
(cell, statistic, scheme): abs(z) >= 3.0 where z = (deformed_statistic - null_mean) /
null_std. When null_std == 0, z is None (undefined), never coerced to a sentinel —
undefined z counts as NOT detected.

**Threshold:** Absolute density thresholds as multiples of the undeformed field mean,
via {0.5, 1.0, 1.5} × mean. No percentile ladders (WP-R7 §4: percentiles collapse on
sparse fields).

**Null hypothesis:** "No deformation". For each scheme, the null bank is built from the
**undeformed** catalog/field. The deformed field's statistic is scored against this bank.

This scientific question: **when a deformation of known scale and amplitude is
definitely present, do the three null schemes agree that it is detectable?**
"""
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

import numpy as np
from typing import Optional

from pipeline.synthetic_catalog import generate_mock_catalog
from pipeline.cosmology import radec_z_to_cartesian_mpc
from pipeline.realfield3d import (
    density_field_cartesian_mpc,
    z_shuffle_realization,
    angular_csr_realization,
    density_shuffle_realization,
)
from pipeline.observables_real import compute_betti_numbers
from pipeline.deformation import void_to_filament_deformation


def run_detectability_sweep(
    n_objects: int = 4000,
    n_clusters: int = 6,
    seed: int = 1,
    nbins: int = 16,
    R_voxels_list: Optional[list[float]] = None,
    amplitude_list: Optional[list[float]] = None,
    n_null_trials: int = 40,
    thresholds_x_mean: tuple = (0.5, 1.0, 1.5),
) -> dict:
    """Run a controlled-injection detectability sweep across (scale, amplitude).

    For each (R_voxels, amplitude) pair:
    1. Generate a single mock catalog (fixed seed).
    2. Bin to 3D field at nbins resolution.
    3. Apply void_to_filament_deformation at (R_voxels, amplitude).
    4. For each of three null schemes, independently:
       a. Build null bank from UNDEFORMED field/catalog.
       b. Compute deformed field's statistics against this bank.
       c. Compute z-scores per (threshold, statistic, scheme).
    5. Record detectability and cross-scheme agreement.

    Thresholds are absolute density values as multiples of the undeformed field mean.

    Parameters
    ----------
    n_objects : int
        Number of objects in the mock catalog. Default 4000.
    n_clusters : int
        Number of cluster cores per catalog. Default 6.
    seed : int
        Random seed for reproducibility. Default 1.
    nbins : int
        Number of bins per axis in the 3D field. Default 16.
    R_voxels_list : list[float], optional
        Gaussian filter sigma values (voxel units) to sweep.
        Default [0.5, 1.0, 2.0, 4.0].
    amplitude_list : list[float], optional
        Deformation amplitudes to sweep. Default [0.0, 0.1, 0.3, 0.5, 1.0].
        **amplitude=0.0 is the tautological-zero guard: deformed = undeformed,
        so a correct pipeline must report essentially no detection.**
    n_null_trials : int
        Number of null realizations per scheme. Default 40.
    thresholds_x_mean : tuple
        Threshold multipliers applied to the undeformed field mean.
        Default (0.5, 1.0, 1.5).

    Returns
    -------
    dict
        Nested structure:
        {
            "R_voxels": {
                float: {
                    "amplitude": {
                        float: {
                            "threshold_x_mean": {
                                float: {
                                    "statistic": {
                                        str: {
                                            "scheme": {
                                                str: {
                                                    "deformed": int,
                                                    "null_mean": float,
                                                    "null_std": float,
                                                    "z": float | None,
                                                    "detected": bool
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "meta": {
                "preregistered_rule": str,
                "n_null_trials": int,
                "nbins": int,
                "n_objects": int,
                "seed": int,
                "voxel_scale_mpc_per_axis": [float, float, float],
                "box_extent_mpc": [float, float, float],
            }
        }

        Per-cell dict keys:
        - "deformed": observed statistic value on the deformed field.
        - "null_mean", "null_std": empirical mean and std of null bank.
        - "z": z-score, or None if null_std == 0 (no variance to normalize).
        - "detected": True iff abs(z) >= 3.0 and z is not None.
    """
    if R_voxels_list is None:
        R_voxels_list = [0.5, 1.0, 2.0, 4.0]
    if amplitude_list is None:
        amplitude_list = [0.0, 0.1, 0.3, 0.5, 1.0]

    # Generate the undeformed catalog once
    catalog = generate_mock_catalog(
        n_objects=n_objects,
        n_clusters=n_clusters,
        seed=seed,
        ra_range=(150.0, 160.0),
        dec_range=(0.0, 10.0),
        z_range=(0.5, 0.7),
    )
    ra = catalog["ra"]
    dec = catalog["dec"]
    z = catalog["z"]

    # Convert to Cartesian
    x, y, z_cart = radec_z_to_cartesian_mpc(ra, dec, z)

    # Compute box extents and voxel scales
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()
    z_min, z_max = z_cart.min(), z_cart.max()
    x_extent = x_max - x_min
    y_extent = y_max - y_min
    z_extent = z_max - z_min

    voxel_scale_mpc_per_axis = [
        x_extent / nbins,
        y_extent / nbins,
        z_extent / nbins,
    ]
    box_extent_mpc = [x_extent, y_extent, z_extent]

    # Generate undeformed field (will be reused for all (R, amplitude) pairs)
    ranges = ((x_min, x_max), (y_min, y_max), (z_min, z_max))
    field_undeformed = density_field_cartesian_mpc(x, y, z_cart, nbins=nbins, ranges=ranges)
    field_mean = float(np.mean(field_undeformed))

    # Pre-register the rule as a string
    preregistered_rule = (
        "Statistic: β₁ and β₂ only (β₀ reported but not used; WP-R7). "
        "Tail: two-sided, abs(z) >= 3.0. "
        "Threshold: absolute density as multiples of undeformed mean. "
        "Null hypothesis: no deformation (null bank from undeformed field)."
    )

    results = {
        "meta": {
            "preregistered_rule": preregistered_rule,
            "n_null_trials": n_null_trials,
            "nbins": nbins,
            "n_objects": n_objects,
            "seed": seed,
            "voxel_scale_mpc_per_axis": voxel_scale_mpc_per_axis,
            "box_extent_mpc": box_extent_mpc,
        }
    }

    # Sweep over (R_voxels, amplitude)
    for R_voxels in R_voxels_list:
        r_results = {}

        for amplitude in amplitude_list:
            amp_results = {}

            # Deform the field
            field_deformed = void_to_filament_deformation(
                field_undeformed, R_voxels=R_voxels, amplitude=amplitude
            )

            # Create RNG once per (R, amplitude) pair for CSR/z_shuffle schemes
            rng = np.random.default_rng(seed)

            for threshold_x_mean in thresholds_x_mean:
                threshold_value = threshold_x_mean * field_mean
                thr_results = {}

                # Compute observed Betti numbers on deformed field
                observed_topo = compute_betti_numbers(
                    field_deformed, threshold_value=threshold_value
                )

                for statistic in ("beta_1", "beta_2"):
                    obs_value = observed_topo[statistic]
                    stat_results = {}

                    for scheme in ("csr", "z_shuffle", "density_shuffle"):
                        # Build null bank from UNDEFORMED field/catalog
                        null_values = []

                        if scheme == "density_shuffle":
                            # Density shuffle works on the binned field
                            for trial in range(n_null_trials):
                                trial_seed = int(seed * 10000 + R_voxels * 100 + amplitude * 1000 + trial)
                                shuffled_field = density_shuffle_realization(
                                    field_undeformed, seed=trial_seed
                                )
                                null_topo = compute_betti_numbers(
                                    shuffled_field, threshold_value=threshold_value
                                )
                                null_values.append(null_topo[statistic])

                        else:
                            # CSR and z-shuffle work on the catalog, then rebin
                            for trial in range(n_null_trials):
                                if scheme == "csr":
                                    ra_s, dec_s, z_s = angular_csr_realization(ra, dec, z, rng)
                                elif scheme == "z_shuffle":
                                    ra_s, dec_s, z_s = z_shuffle_realization(ra, dec, z, rng)

                                x_s, y_s, z_cart_s = radec_z_to_cartesian_mpc(ra_s, dec_s, z_s)
                                field_s = density_field_cartesian_mpc(
                                    x_s, y_s, z_cart_s, nbins=nbins, ranges=ranges
                                )
                                null_topo = compute_betti_numbers(
                                    field_s, threshold_value=threshold_value
                                )
                                null_values.append(null_topo[statistic])

                        null_values = np.array(null_values, dtype=np.float64)
                        null_mean = float(np.mean(null_values))
                        null_std = float(np.std(null_values))

                        # Compute z-score
                        if null_std > 0.0:
                            z_score = (obs_value - null_mean) / null_std
                        else:
                            z_score = None

                        # Detection: abs(z) >= 3.0 and z is not None
                        detected = z_score is not None and abs(z_score) >= 3.0

                        stat_results[scheme] = {
                            "deformed": int(obs_value),
                            "null_mean": null_mean,
                            "null_std": null_std,
                            "z": z_score,
                            "detected": detected,
                        }

                    thr_results[statistic] = stat_results

                amp_results[threshold_x_mean] = thr_results

            r_results[amplitude] = amp_results

        results[R_voxels] = r_results

    return results


def render_detectability_report(results: dict) -> str:
    """Render detectability sweep results as markdown.

    Includes: header with synthetic-only disclaimer, pre-registered rule,
    scale-honesty section (voxel Mpc scales, overlap check vs 0.22–0.27 Mpc),
    cross-scheme agreement table, amplitude floor table, and amplitude-0.0 guard note.
    """
    lines = []

    # Header with disclaimers
    lines.append("# WP-E2: Synthetic Controlled-Injection Detectability Sweep")
    lines.append("")
    lines.append("**ALL RESULTS ARE SYNTHETIC CONTROLLED-INJECTION — NOT A MEASUREMENT OF ANY SURVEY, NOT A TEST OF ANY HYPOTHESIS.**")
    lines.append("")
    lines.append("Engineering-only exploration on mock catalogs. Ground truth is known because we inject the deformation ourselves.")
    lines.append("")

    # Pre-registered rule
    meta = results["meta"]
    lines.append("## Pre-Registered Decision Rule")
    lines.append("")
    lines.append(meta["preregistered_rule"])
    lines.append("")

    # Scale honesty section
    lines.append("## Scale Honesty")
    lines.append("")
    voxel_scales = meta["voxel_scale_mpc_per_axis"]
    box_extent = meta["box_extent_mpc"]
    lines.append(f"**Box extent:** {box_extent[0]:.1f} × {box_extent[1]:.1f} × {box_extent[2]:.1f} Mpc (x, y, z)")
    lines.append("")
    lines.append(f"**Voxel scale (Mpc per axis):** {voxel_scales[0]:.3f} (x), {voxel_scales[1]:.3f} (y), {voxel_scales[2]:.3f} (z)")
    lines.append("")

    # Check overlap with 0.22–0.27 Mpc window
    survey_floor_mpc = 0.22
    survey_ceil_mpc = 0.27
    min_voxel_scale = min(voxel_scales)
    max_voxel_scale = max(voxel_scales)

    # For R_voxels in voxel units, physical scale in Mpc is approximately R_voxels * voxel_scale
    R_voxels_list = [r for r in results.keys() if isinstance(r, (int, float))]
    if R_voxels_list:
        min_R_voxels = min(R_voxels_list)
        max_R_voxels = max(R_voxels_list)
        min_physical_scale = min_R_voxels * min_voxel_scale
        max_physical_scale = max_R_voxels * max_voxel_scale

        lines.append(f"**Swept R_voxels range:** {min_R_voxels} to {max_R_voxels} voxels")
        lines.append("")
        lines.append(f"**Corresponding physical scale range:** {min_physical_scale:.3f} to {max_physical_scale:.3f} Mpc")
        lines.append("")

        # Check overlap
        overlap = (max_physical_scale >= survey_floor_mpc and min_physical_scale <= survey_ceil_mpc)
        if overlap:
            lines.append(f"**Overlap with survey-resolvable window [0.22–0.27 Mpc]:** YES")
        else:
            lines.append(f"**Overlap with survey-resolvable window [0.22–0.27 Mpc]:** NO")
            lines.append("")
            # Compute shrink factor
            if min_physical_scale < survey_floor_mpc:
                shrink_factor = min_physical_scale / survey_floor_mpc
            else:
                shrink_factor = survey_ceil_mpc / max_physical_scale
            lines.append(
                f"The default synthetic box cannot probe the resolvable window. "
                f"Reaching it requires a box smaller by a factor of ~{1.0/shrink_factor:.1f}x."
            )
    lines.append("")

    # Cross-scheme agreement table
    lines.append("## Cross-Scheme Agreement")
    lines.append("")
    lines.append(
        "Per (R_voxels, amplitude, threshold, statistic), count how many of 3 schemes "
        "detected the deformation. Disagreement cells are those where ≥1 scheme detected "
        "and ≥1 did not."
    )
    lines.append("")

    # Build agreement data
    agreement_data = {}
    total_cells = 0
    disagreement_cells = 0

    for R_voxels in R_voxels_list:
        R_dict = results[R_voxels]
        for amplitude in sorted(R_dict.keys()):
            amp_dict = R_dict[amplitude]
            for threshold_x_mean in sorted(amp_dict.keys()):
                thr_dict = amp_dict[threshold_x_mean]
                for statistic in ("beta_1", "beta_2"):
                    if statistic not in thr_dict:
                        continue
                    stat_dict = thr_dict[statistic]

                    detected_schemes = sum(
                        1 for scheme_result in stat_dict.values()
                        if scheme_result["detected"]
                    )
                    total_schemes = len(stat_dict)

                    key = (R_voxels, amplitude, threshold_x_mean, statistic)
                    agreement_data[key] = detected_schemes

                    total_cells += 1
                    if 0 < detected_schemes < total_schemes:
                        disagreement_cells += 1

    # Agreement table (sample a subset for readability)
    lines.append("| R_voxels | Amplitude | Threshold | Stat | Schemes Detected (0-3) |")
    lines.append("|----------|-----------|-----------|------|------------------------|")

    for (R, A, Thr, Stat), count in sorted(agreement_data.items()):
        lines.append(
            f"| {R:8.1f} | {A:9.1f} | {Thr:9.1f}× | {Stat:4s} | {count:22d} |"
        )

    lines.append("")
    lines.append(
        f"**Total cells:** {total_cells}. **Disagreement cells (≥1 detected, ≥1 not):** {disagreement_cells}. "
        f"(Agreement = {total_cells - disagreement_cells}/{total_cells})"
    )
    lines.append("")

    # Amplitude floor table
    lines.append("## Amplitude Sensitivity Floor")
    lines.append("")
    lines.append(
        "Per R_voxels and statistic, the smallest amplitude at which all three schemes "
        "agree on detection (at any threshold). If no tested amplitude shows all-three agreement, "
        "that R is listed as 'none'."
    )
    lines.append("")
    lines.append("| R_voxels | Beta Statistic | Floor Amplitude |")
    lines.append("|----------|----------------|-----------------|")

    for R_voxels in sorted(R_voxels_list):
        R_dict = results[R_voxels]
        for statistic in ("beta_1", "beta_2"):
            # Find the smallest amplitude where all 3 schemes detect (at any threshold)
            floor_amp = None
            for amplitude in sorted(R_dict.keys()):
                amp_dict = R_dict[amplitude]
                all_agree = False
                for threshold_x_mean in amp_dict.keys():
                    thr_dict = amp_dict[threshold_x_mean]
                    if statistic in thr_dict:
                        stat_dict = thr_dict[statistic]
                        detected_schemes = sum(
                            1 for scheme_result in stat_dict.values()
                            if scheme_result["detected"]
                        )
                        if detected_schemes == 3:
                            all_agree = True
                            break
                if all_agree:
                    floor_amp = amplitude
                    break

            floor_str = f"{floor_amp:.1f}" if floor_amp is not None else "none"
            lines.append(f"| {R_voxels:8.1f} | {statistic:14s} | {floor_str:15s} |")

    lines.append("")

    # Amplitude 0.0 guard note
    lines.append("## Amplitude 0.0 Tautological-Zero Guard")
    lines.append("")
    lines.append(
        "At amplitude=0.0, the deformed field IS the undeformed field, so a correct pipeline "
        "must report essentially no detection (all z-scores within ±3σ). The results below show "
        "whether the amplitude-0.0 guard held."
    )
    lines.append("")

    # Collect amplitude-0.0 results
    amp_0_detected = 0
    amp_0_total = 0
    for R_voxels in R_voxels_list:
        R_dict = results[R_voxels]
        if 0.0 in R_dict:
            amp_dict = R_dict[0.0]
            for threshold_x_mean in amp_dict.keys():
                thr_dict = amp_dict[threshold_x_mean]
                for statistic in ("beta_1", "beta_2"):
                    if statistic in thr_dict:
                        stat_dict = thr_dict[statistic]
                        for scheme_result in stat_dict.values():
                            amp_0_total += 1
                            if scheme_result["detected"]:
                                amp_0_detected += 1

    lines.append(
        f"Detections at amplitude=0.0: {amp_0_detected}/{amp_0_total} "
        f"({100*amp_0_detected/amp_0_total:.1f}% if > 0 cells)"
    )
    if amp_0_detected == 0:
        lines.append("✓ Guard held: no false detections in the tautological case.")
    else:
        lines.append(
            f"⚠ Guard violation: {amp_0_detected} cells showed detection when amplitude=0. "
            f"Investigate."
        )
    lines.append("")

    # Footer
    lines.append("---")
    lines.append(f"Generated by: Haiku 4.5 | Sweep config: n_objects={meta['n_objects']}, "
                 f"nbins={meta['nbins']}, n_null_trials={meta['n_null_trials']}")

    return "\n".join(lines)


if __name__ == "__main__":
    print("Running synthetic detectability sweep...")
    results = run_detectability_sweep()

    report = render_detectability_report(results)
    print(report)

    # Write to docs/
    output_path = Path(__file__).parent.parent / "docs" / "WP_E2_SYNTHETIC_DETECTABILITY_2026_07_26.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(report)
    print(f"\nReport saved to {output_path}")


# Generated-by: Haiku 4.5 | Verified-by: pipeline/tests/test_deformation.py
# (smoke test sweep, labeling) | Reviewed-by: pending T0
