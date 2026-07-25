#!/usr/bin/env python3
"""WP-R7: beta_1/beta_2 discriminating-power scan (follow-on to WP-R5 Section 7).

WP-R5 (docs/WP_R5_3D_FIELD.md Section 7) found that beta_0 has near-zero
discriminating power for 3/4 real fields at (nbins=8, threshold=50th
percentile): the top-density region generically percolates into a single
connected component, so both null schemes correctly show zero beta_0
variance at that setting -- a genuine statistical-power limit of the
(statistic, threshold, resolution) triple, not a broken null. That report
flagged beta_1/beta_2 as worth a dedicated variance study (edf_north already
showed a real beta_2=2 -- two cavities -- in its actual data) but explicitly
left it out of WP-R5's scope.

This script runs that study: for each field, scan threshold_percentile across
a range and record beta_0/beta_1/beta_2 null variance under BOTH valid
schemes (z-shuffle, angular CSR; pipeline/realfield3d.py), at nbins fixed to
WP-R5's value for comparability. It answers one question only: at which
(threshold) settings do beta_1 and/or beta_2 carry nonzero null variance,
i.e. could in principle discriminate real data from CSR at this resolution?

ENGINEERING ONLY. No TEST/FIT label (gate G1-L closed, Off-Ramp 3 terminus
recorded in NO_PREDICTION_BRANCH.md Section 8.5). No comparison to any
prediction; no interpretation of any topology number as evidence for or
against any hypothesis. This characterizes the STATISTIC, not the DATA.
"""
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

import pandas as pd
import numpy as np
import json
import hashlib
from datetime import datetime, timezone

from pipeline.cosmology import radec_z_to_tangent_plane_mpc, drop_invalid_redshifts
from pipeline.realfield3d import (
    density_field_cartesian_mpc,
    z_shuffle_realization,
    angular_csr_realization,
)
from pipeline.observables_real import compute_betti_numbers

NBINS = 8  # matches WP-R5, for direct comparability
THRESHOLDS = [50.0, 60.0, 70.0, 80.0, 90.0]  # matches WP-R5's own power scan
N_NULL_REALIZATIONS = 50  # matches WP-R5's power-scan precedent (Section 7)

OUTPUT_DIR = Path("/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/wp_r7_beta_variance")

FIELDS = [
    {
        "name": "euclid_z_edf_north",
        "path": "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid_z/euclid_z_edf_north.csv",
        "ra_col": "right_ascension", "dec_col": "declination", "z_col": "phz_median",
        "survey": "Euclid MER x phz_photo_z (photometric redshift)",
    },
    {
        "name": "euclid_z_edf_fornax",
        "path": "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid_z/euclid_z_edf_fornax.csv",
        "ra_col": "right_ascension", "dec_col": "declination", "z_col": "phz_median",
        "survey": "Euclid MER x phz_photo_z (photometric redshift)",
    },
    {
        "name": "euclid_z_edf_south",
        "path": "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid_z/euclid_z_edf_south.csv",
        "ra_col": "right_ascension", "dec_col": "declination", "z_col": "phz_median",
        "survey": "Euclid MER x phz_photo_z (photometric redshift)",
    },
    {
        "name": "sdss_z_coma_cluster",
        "path": "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/sdss_z/sdss_z_coma_cluster.csv",
        "ra_col": "ra", "dec_col": "dec", "z_col": "z",
        "survey": "SDSS spectroscopic (spectro=True, real spec-z)",
    },
]


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def _load_field_coords(field_info: dict):
    df = pd.read_csv(field_info["path"])
    ra_raw = df[field_info["ra_col"]].values
    dec_raw = df[field_info["dec_col"]].values
    z_raw = df[field_info["z_col"]].values
    ra, dec, z, drop_report = drop_invalid_redshifts(ra_raw, dec_raw, z_raw)
    ra0, dec0 = float(np.mean(ra)), float(np.mean(dec))
    x, y, z_cart = radec_z_to_tangent_plane_mpc(ra, dec, z, ra0_deg=ra0, dec0_deg=dec0)
    ranges = ((x.min(), x.max()), (y.min(), y.max()), (z_cart.min(), z_cart.max()))
    return ra, dec, z, ra0, dec0, ranges, len(df), drop_report


def scan_field(field_info: dict) -> dict:
    name = field_info["name"]
    ra, dec, z, ra0, dec0, ranges, n_input, drop_report = _load_field_coords(field_info)

    per_threshold = []
    for threshold in THRESHOLDS:
        x, y, zc = radec_z_to_tangent_plane_mpc(ra, dec, z, ra0_deg=ra0, dec0_deg=dec0)
        field = density_field_cartesian_mpc(x, y, zc, nbins=NBINS, ranges=ranges)
        real_topo = compute_betti_numbers(field, threshold_percentile=threshold)

        schemes = {}
        for scheme_name, realization_fn, seed in [
            ("z_shuffle", z_shuffle_realization, 201),
            ("angular_csr", angular_csr_realization, 202),
        ]:
            rng = np.random.default_rng(seed)
            null_topos = []
            for _ in range(N_NULL_REALIZATIONS):
                ra_s, dec_s, z_s = realization_fn(ra, dec, z, rng)
                x_s, y_s, zc_s = radec_z_to_tangent_plane_mpc(
                    ra_s, dec_s, z_s, ra0_deg=ra0, dec0_deg=dec0
                )
                field_s = density_field_cartesian_mpc(x_s, y_s, zc_s, nbins=NBINS, ranges=ranges)
                null_topos.append(compute_betti_numbers(field_s, threshold_percentile=threshold))

            stats = {}
            for stat in ("beta_0", "beta_1", "beta_2"):
                dist = [t[stat] for t in null_topos]
                variance = float(np.var(dist))
                stats[stat] = {
                    "mean": float(np.mean(dist)),
                    "std": float(np.std(dist)),
                    "variance": variance,
                    "nonzero_variance": variance > 0,
                    "real_value": real_topo[stat],
                    "real_percentile_rank": float(np.mean(np.array(dist) <= real_topo[stat]) * 100),
                }
            schemes[scheme_name] = stats

        per_threshold.append({
            "threshold_percentile": threshold,
            "real_topology": real_topo,
            "n_null_realizations": N_NULL_REALIZATIONS,
            "schemes": schemes,
        })

    return {
        "field_name": name,
        "survey": field_info["survey"],
        "nbins": NBINS,
        "n_input": n_input,
        "redshift_drop_report": drop_report,
        "per_threshold": per_threshold,
        "label": "ENGINEERING",
    }


def summarize_discriminating_power(all_results: dict) -> list[str]:
    """Which (field, threshold, statistic, scheme) combinations show nonzero
    null variance -- i.e. which settings could in principle discriminate real
    data from a null, as opposed to being saturated/degenerate (WP-R5 Section
    7's percolation finding). This is a statement about statistical power,
    not a claim about the real data."""
    lines = []
    for field_name, result in all_results.items():
        for entry in result["per_threshold"]:
            thr = entry["threshold_percentile"]
            for scheme_name, stats in entry["schemes"].items():
                nonzero = [s for s in ("beta_0", "beta_1", "beta_2") if stats[s]["nonzero_variance"]]
                if nonzero:
                    lines.append(
                        f"{field_name} @ thr={thr:.0f}% [{scheme_name}]: "
                        f"nonzero variance in {', '.join(nonzero)}"
                    )
    return lines


def main():
    print("WP-R7: beta_1/beta_2 Discriminating-Power Scan (follow-on to WP-R5 Section 7)")
    print("=" * 80)
    print(f"Config: nbins={NBINS}, thresholds={THRESHOLDS}%, "
          f"null realizations={N_NULL_REALIZATIONS} per scheme per threshold")
    print("Scope: ENGINEERING only (no TEST/FIT; gate G1-L closed; Off-Ramp 3 terminus stands)\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_results = {}
    for field_info in FIELDS:
        name = field_info["name"]
        print(f"Scanning {name} ({field_info['survey']})...")
        result = scan_field(field_info)
        all_results[name] = result
        for entry in result["per_threshold"]:
            thr = entry["threshold_percentile"]
            rt = entry["real_topology"]
            zs = entry["schemes"]["z_shuffle"]
            csr = entry["schemes"]["angular_csr"]
            print(f"  thr={thr:5.1f}%  real(b0,b1,b2)=({rt['beta_0']},{rt['beta_1']},{rt['beta_2']})  "
                  f"z-sh var(b0,b1,b2)=({zs['beta_0']['variance']:.3f},{zs['beta_1']['variance']:.3f},{zs['beta_2']['variance']:.3f})  "
                  f"csr var(b0,b1,b2)=({csr['beta_0']['variance']:.3f},{csr['beta_1']['variance']:.3f},{csr['beta_2']['variance']:.3f})")
        print()

    output_file = OUTPUT_DIR / "wp_r7_results_2026_07_25.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)
    sha = _sha256_file(output_file)

    metadata = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "nbins": NBINS,
        "thresholds": THRESHOLDS,
        "n_null_realizations": N_NULL_REALIZATIONS,
        "fields": list(all_results.keys()),
        "output_file": str(output_file),
        "sha256": sha,
        "label": "ENGINEERING",
        "follows_on_from": "docs/WP_R5_3D_FIELD.md Section 7 (flagged, out of scope there)",
    }
    metadata_file = OUTPUT_DIR / "WP_R7_MANIFEST_2026_07_25.json"
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=2)

    print("=" * 80)
    print(f"Results: {output_file}")
    print(f"SHA256:  {sha}")
    print(f"Metadata: {metadata_file}\n")

    print("DISCRIMINATING-POWER SUMMARY (nonzero null variance found):")
    print("-" * 80)
    lines = summarize_discriminating_power(all_results)
    if lines:
        for line in lines:
            print(f"  {line}")
    else:
        print("  None -- every (field, threshold, scheme) combination scanned was degenerate.")

    return 0


if __name__ == "__main__":
    sys.exit(main())


# Generated-by: Claude Sonnet 5 (T1) | Verified-by: reuses pipeline/tests/
# test_cosmology.py + test_realfield3d.py (24 tests); Coma percentile degeneracy
# + empty-bin fraction independently recomputed at T0 review | Reviewed-by: T0 Y
# (Fable 5, 2026-07-25, docs/T0_SIGNOFF_WP_R5_R6_R7_2026_07_25.md)
