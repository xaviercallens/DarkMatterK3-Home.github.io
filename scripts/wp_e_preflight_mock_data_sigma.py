#!/usr/bin/env python3
"""WP-E pre-flight: sigma_mock-data(0) go/no-go gate (Stream 2 fix 3, 2026-07-26).

Stream 2's consolidated guidelines (2026-07-26) require, before any GPU sweep:

    "pre-flight sigma_mock-data(0) as a go/no-go -- Zone 2 lacks E2.11's baseline
     subtraction; if the undeformed mock already sits >5 sigma from data, Zone 2
     swallows the whole grid."

That is the right gate and this script is it. If an UNDEFORMED mock already sits
far from the real field, then a Zone-2 boundary defined as "deviation from real
data > 5 sigma" is crossed before any deformation is applied, and the resulting
Zone map would report mock-vs-data systematics as if they were physics.

METHOD, and its deliberate limits:

- The real comparison value is read from the COMMITTED artifact
  data/derived/wp_e3_results_2026_07_26.json (`real_topology_baseline`), produced
  under the WP-E3 T0 authorization. This script performs NO new real-data access:
  no catalogue read, no fetch. Only an already-published data product is consumed.
- Mocks are generated geometry-matched to the real field using only published
  numbers: extent (48.3, 52.4, 8188.8) Mpc from
  docs/WP_E3_REALDATA_THIRD_SCHEME_2026_07_26.md section 5.1, and n = 1983 valid
  objects from the same artifact. Points are drawn directly in comoving Cartesian
  space, so no ra/dec/z round-trip and no cosmology assumption enters.
- Binning is nbins=8 with absolute thresholds {0.5, 1.0, 1.5} x field mean, matching
  WP-E/WP-E3 exactly so the comparison is apples-to-apples.
- Statistic is beta_2 (Stream 2 fix / directive E2.10: beta_2 preferred; beta_1 is
  baseline-artifact-prone). beta_0 and beta_1 are recorded for completeness only.

sigma_mock-data(0) = (real_value - mock_mean) / mock_std, reported per threshold.
When mock_std == 0 the sigma is UNDEFINED and reported as None -- never coerced
(WP-R5 discipline). An undefined sigma is treated as NO-GO, because an
undefined baseline separation cannot be shown to be small.

WHAT THIS DOES NOT DO: it does not test any hypothesis, produce any TEST/FIT
label, or measure physics. A large sigma here is a statement about mock realism
versus the real field's selection function, mask, and photo-z smearing -- not
about any mechanism. That is precisely why it must gate the sweep rather than
feed it.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import numpy as np

from pipeline.observables_real import compute_betti_numbers
from pipeline.realfield3d import density_field_cartesian_mpc

RESULTS_JSON = REPO_ROOT / "data" / "derived" / "wp_e3_results_2026_07_26.json"
OUT_JSON = REPO_ROOT / "data" / "derived" / "wp_e_preflight_mock_data_sigma_2026_07_26.json"

# Published geometry (docs/WP_E3_REALDATA_THIRD_SCHEME_2026_07_26.md section 5.1)
EXTENT_MPC = (48.3, 52.4, 8188.8)
NBINS = 8
THRESHOLDS_X_MEAN = (0.5, 1.0, 1.5)
N_MOCKS = 40
GO_NO_GO_SIGMA = 5.0  # Stream 2's stated Zone 2 boundary


def generate_matched_mock(n_objects: int, extent_mpc, seed: int,
                          n_clusters: int = 6, clustered_fraction: float = 0.7):
    """Uniform background + Gaussian clusters, drawn directly in comoving Mpc.

    Geometry-matched to the real field by construction. Deterministic per seed
    (np.random.default_rng only, never bare np.random).
    """
    rng = np.random.default_rng(seed)
    ex, ey, ez = extent_mpc
    n_clustered = int(clustered_fraction * n_objects)
    n_bg = n_objects - n_clustered

    centers = np.column_stack([
        rng.uniform(0, ex, n_clusters),
        rng.uniform(0, ey, n_clusters),
        rng.uniform(0, ez, n_clusters),
    ])
    # Cluster scale: 2% of each axis, so clustering is scale-matched per axis
    sigma = np.array([ex, ey, ez], dtype=np.float64) * 0.02

    idx = rng.integers(0, n_clusters, n_clustered)
    clustered = centers[idx] + rng.normal(0.0, 1.0, (n_clustered, 3)) * sigma
    background = np.column_stack([
        rng.uniform(0, ex, n_bg),
        rng.uniform(0, ey, n_bg),
        rng.uniform(0, ez, n_bg),
    ])
    pts = np.vstack([clustered, background])
    return np.clip(pts, 0.0, np.array([ex, ey, ez]))


def main() -> int:
    if not RESULTS_JSON.exists():
        print(f"ABORT: required committed artifact missing: {RESULTS_JSON}")
        return 2

    wp_e3 = json.loads(RESULTS_JSON.read_text())
    real_baseline = wp_e3["real_topology_baseline"]
    n_valid = int(wp_e3["n_valid"])
    field_name = wp_e3["field_name"]

    ranges = ((0.0, EXTENT_MPC[0]), (0.0, EXTENT_MPC[1]), (0.0, EXTENT_MPC[2]))

    mock_stats = {f"thr_{t}": {"beta_0": [], "beta_1": [], "beta_2": []}
                  for t in THRESHOLDS_X_MEAN}

    for k in range(N_MOCKS):
        pts = generate_matched_mock(n_valid, EXTENT_MPC, seed=7000 + k)
        field = density_field_cartesian_mpc(
            pts[:, 0], pts[:, 1], pts[:, 2], nbins=NBINS, ranges=ranges
        )
        for t in THRESHOLDS_X_MEAN:
            topo = compute_betti_numbers(field, threshold_value=float(t))
            for stat in ("beta_0", "beta_1", "beta_2"):
                mock_stats[f"thr_{t}"][stat].append(int(topo[stat]))

    out = {
        "purpose": "WP-E pre-flight go/no-go: sigma_mock-data at zero deformation",
        "requested_by": "Stream 2 consolidated guidelines 2026-07-26, fix 3",
        "label": "SYNTHETIC (mock ensemble) vs committed real baseline; not TEST/FIT",
        "real_source": str(RESULTS_JSON.relative_to(REPO_ROOT)),
        "real_field": field_name,
        "no_new_real_data_access": True,
        "extent_mpc": list(EXTENT_MPC),
        "extent_source": "docs/WP_E3_REALDATA_THIRD_SCHEME_2026_07_26.md section 5.1",
        "n_objects_matched": n_valid,
        "nbins": NBINS,
        "n_mocks": N_MOCKS,
        "go_no_go_sigma": GO_NO_GO_SIGMA,
        "per_threshold": {},
    }

    verdicts = []
    for t in THRESHOLDS_X_MEAN:
        key = f"thr_{t}"
        entry = {}
        for stat in ("beta_0", "beta_1", "beta_2"):
            vals = np.asarray(mock_stats[key][stat], dtype=np.float64)
            mean = float(vals.mean())
            std = float(vals.std())
            real = float(real_baseline[key][stat])
            if std == 0.0:
                sigma = None
            else:
                sigma = float((real - mean) / std)
            entry[stat] = {
                "real": real,
                "mock_mean": mean,
                "mock_std": std,
                "sigma_mock_data_0": sigma,
            }
        # Verdict uses beta_2 only (E2.10)
        s = entry["beta_2"]["sigma_mock_data_0"]
        if s is None:
            v = "NO-GO (sigma undefined: zero-variance mock ensemble)"
        elif abs(s) > GO_NO_GO_SIGMA:
            v = f"NO-GO (|sigma|={abs(s):.2f} > {GO_NO_GO_SIGMA})"
        else:
            v = f"GO (|sigma|={abs(s):.2f} <= {GO_NO_GO_SIGMA})"
        entry["verdict_beta_2"] = v
        verdicts.append(v)
        out["per_threshold"][key] = entry

    out["overall_verdict"] = (
        "NO-GO" if any(v.startswith("NO-GO") for v in verdicts) else "GO"
    )

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=2))

    print("=" * 78)
    print("WP-E PRE-FLIGHT: sigma_mock-data(0)  [Stream 2 fix 3]")
    print("=" * 78)
    print(f"real field   : {field_name} (from committed artifact; no new data access)")
    print(f"geometry     : extent {EXTENT_MPC} Mpc, nbins={NBINS}, n={n_valid}")
    print(f"mock ensemble: {N_MOCKS} realizations, geometry- and count-matched")
    print()
    for t in THRESHOLDS_X_MEAN:
        e = out["per_threshold"][f"thr_{t}"]["beta_2"]
        s = e["sigma_mock_data_0"]
        s_str = "None (undefined)" if s is None else f"{s:+.2f}"
        print(f"  thr={t}x mean  beta_2: real={e['real']:.0f}  "
              f"mock={e['mock_mean']:.2f}+/-{e['mock_std']:.2f}  "
              f"sigma_mock-data(0)={s_str}")
        print(f"                 -> {out['per_threshold'][f'thr_{t}']['verdict_beta_2']}")
    print()
    print(f"OVERALL: {out['overall_verdict']}")
    print(f"persisted: {OUT_JSON.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())


# Generated-by: Claude Opus 5 (Stream 3) | Verified-by: consumes only the committed
# WP-E3 artifact for real values (no new real-data access); geometry and n from
# published WP-E3 section 5.1; deterministic per seed; undefined sigma reported as
# None and treated as NO-GO | Reviewed-by: pending T0
