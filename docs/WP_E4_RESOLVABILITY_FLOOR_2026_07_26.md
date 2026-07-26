# WP-E4 — Resolvability Floor (Arithmetic Guard)

**Date:** 2026-07-26

**Executor:** Claude Haiku 4.5

**Tag:** `ENGINEERING` — pure arithmetic on published geometry

**Status:** Complete


⚠️ **NOT `TEST`, NOT `FIT`, NOT `SANDBOX-EXPERIMENTAL`.** This is pure arithmetic on published field extents. It makes no physics claim and falsifies nothing. It operates at the voxel-geometry level to prevent future sweeps from testing scales below the detection floor.


## 1. The Finding This Operationalizes


WP-E3 tested deformation scales up to r_s = 4.0 Mpc on the `euclid_z_edf_north` field with nbins = 8. The published voxel edges (§5.1) are:


| Axis | Extent (Mpc) | Voxel edge at nbins=8 (Mpc) |

|---|---|---|

| transverse x | 48.3 | 6.04 |

| transverse y | 52.4 | 6.55 |

| **radial (z)** | **8188.8** | **1023.6** |


**The 4.0 Mpc deformation spans 0.66, 0.61, and 0.0039 voxels on the three axes.** Rebinning coordinates displaced by a sub-voxel amount returns a bit-identical field. Therefore, every topological statistic computed on this field was unchanged by construction, making the verdict "schemes agree" degenerate: there was no deformation response to measure.


## 2. Voxel Edges per Field


### euclid_z_edf_north


Source: docs/WP_E3_REALDATA_THIRD_SCHEME_2026_07_26.md §5.1


| nbins | voxel_x (Mpc) | voxel_y (Mpc) | voxel_z (Mpc) |

|---|---|---|---|

| 8 | 6.04 | 6.55 | 1023.60 |

| 16 | 3.02 | 3.27 | 511.80 |

| 32 | 1.51 | 1.64 | 255.90 |

| 64 | 0.75 | 0.82 | 127.95 |

| 128 | 0.38 | 0.41 | 63.98 |



### synthetic_mock_default


Source: docs/WP_E2_SYNTHETIC_DETECTABILITY_2026_07_26.md


| nbins | voxel_x (Mpc) | voxel_y (Mpc) | voxel_z (Mpc) |

|---|---|---|---|

| 8 | 91.85 | 76.65 | 55.36 |

| 16 | 45.92 | 38.33 | 27.68 |

| 32 | 22.96 | 19.16 | 13.84 |

| 64 | 11.48 | 9.58 | 6.92 |

| 128 | 5.74 | 4.79 | 3.46 |



## 3. Decisive Table: r_s Grid on euclid_z_edf_north at nbins=8


This table applies the externally-proposed deformation scale grid r_s ∈ {0.27, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0} Mpc to the field WP-E actually used.


| r_s (Mpc) | Verdict | Required nbins (x, y, z) |

|---|---|---|

| 0.27 | UNRESOLVABLE | (179, 195, 30329) |

| 0.50 | UNRESOLVABLE | (97, 105, 16378) |

| 1.00 | UNRESOLVABLE | (49, 53, 8189) |

| 2.00 | UNRESOLVABLE | (25, 27, 4095) |

| 4.00 | UNRESOLVABLE | (13, 14, 2048) |

| 6.00 | UNRESOLVABLE | (9, 9, 1365) |

| 8.00 | PARTIALLY_RESOLVABLE | (7, 7, 1024) |

| 10.00 | PARTIALLY_RESOLVABLE | (5, 6, 819) |



**Fraction of the proposed grid that is UNRESOLVABLE: 6/8 = 75%**


## 4. Radial Resolution: Fundamental Limits


The redshift range projects to ~8189 Mpc of comoving depth. For a 1.0 Mpc deformation to span one voxel radially:


- Required nbins (radial): 8189

- Resulting voxel depth: ~1.0 Mpc


With ~2000 objects and 21,266,833 voxels, mean occupancy is **9.40e-05 objects per voxel**. At this sparsity, the topology becomes trivial for a statistical reason, independent of voxel size: random grids with very few points per bin have no connected structure to measure.


## 5. How to Use This Guard in a Sweep


Any future deformation sweep must call `assert_resolvable` at the top of its loop:


```python

from pipeline.resolvability import assert_resolvable


for r_s in r_s_grid:

    for nbins in nbins_values:

        # Arithmetic check — raises ResolvabilityError if sub-voxel

        assert_resolvable(r_s, field_extent, nbins, min_voxels=1.0)


        # Proceed to compute statistics

        ...

```


A sub-voxel scale caught here is a hard stop: re-run with finer nbins (consult the required_nbins table) or a different mechanism scale.


## 6. Provenance


Generated-by: Haiku 4.5 (scripts/report_resolvability_floor.py) | Verified-by: pipeline/tests/test_resolvability.py (WP-E3 regression test passes; required_nbins round-trip verified; boundary conditions verified) | Reviewed-by: pending T0
