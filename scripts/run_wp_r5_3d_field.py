#!/usr/bin/env python3
"""WP-R5: Real 3D comoving density field + corrected null bank.

Loads real Euclid photo-z fields (MER JOIN phz_photo_z, fetched by
scripts/fetch_survey_redshifts.py), drops invalid redshifts explicitly
(counted, never imputed), converts to a tangent-plane comoving Mpc frame
(Planck18 cosmology, cited in pipeline/cosmology.py; tangent-plane projection
because these are narrow pencil-beam cones — see
radec_z_to_tangent_plane_mpc's docstring for why global Cartesian wastes
>90% of bins on empty space), builds a 3D density field, and reports its
topology ALWAYS alongside a null distribution built from the two
methodologically valid schemes in pipeline/realfield3d.py (z-shuffle,
angular CSR) — never a bare number.

Also runs the SDSS Coma cluster spectroscopic field (best real-spectro-z
coverage among the WP-R5 SDSS fetches) as a second, independent field.

ENGINEERING ONLY. No TEST/FIT label (gate G1-L closed). No interpretation of
any topology number as evidence for or against any hypothesis — that
interpretation is T0-only and gated, and explicitly out of scope here
(HAIKU_PLAN_REALDATA_VERIFICATION_2026_07_25.md, WP-R5 STOP AND FLAG clause).
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

NBINS = 8  # coarser than WP-R2's angular fields; genuine 3D bins are far sparser
THRESHOLD_PERCENTILE = 50.0
N_NULL_REALIZATIONS = 200

OUTPUT_DIR = Path("/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/wp_r5_3d_field")

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


def process_field(field_info: dict) -> dict:
    name = field_info["name"]
    df = pd.read_csv(field_info["path"])
    n_input = len(df)

    ra_raw = df[field_info["ra_col"]].values
    dec_raw = df[field_info["dec_col"]].values
    z_raw = df[field_info["z_col"]].values

    # Explicit drop, never impute (WP-R5 hard rule)
    ra, dec, z, drop_report = drop_invalid_redshifts(ra_raw, dec_raw, z_raw)

    # Tangent-plane comoving conversion (Planck18, cited in pipeline/cosmology.py).
    # Not global Cartesian: for a narrow pencil-beam cone, global (x,y,z)
    # embeds as a thin sliver in a mostly-empty bounding box (see
    # docs/WP_R5_3D_FIELD.md "binning frame" section for the empirical
    # comparison). The tangent-plane + radial frame aligns bins with the
    # survey's actual footprint.
    ra0, dec0 = float(np.mean(ra)), float(np.mean(dec))
    x, y, z_cart = radec_z_to_tangent_plane_mpc(ra, dec, z, ra0_deg=ra0, dec0_deg=dec0)
    ranges = ((x.min(), x.max()), (y.min(), y.max()), (z_cart.min(), z_cart.max()))

    # Real-field topology
    field = density_field_cartesian_mpc(x, y, z_cart, nbins=NBINS, ranges=ranges)
    real_topo = compute_betti_numbers(field, threshold_percentile=THRESHOLD_PERCENTILE)
    occupied_bins = int(np.count_nonzero(field))
    total_bins = int(NBINS ** 3)

    # Null bank: z-shuffle scheme (operates in ra/dec/z BEFORE Cartesian conversion,
    # since it needs to permute z independently of angular position)
    rng_zshuffle = np.random.default_rng(101)
    null_zshuffle = []
    for k in range(N_NULL_REALIZATIONS):
        ra_s, dec_s, z_s = z_shuffle_realization(ra, dec, z, rng_zshuffle)
        x_s, y_s, zc_s = radec_z_to_tangent_plane_mpc(ra_s, dec_s, z_s, ra0_deg=ra0, dec0_deg=dec0)
        field_s = density_field_cartesian_mpc(x_s, y_s, zc_s, nbins=NBINS, ranges=ranges)
        topo_s = compute_betti_numbers(field_s, threshold_percentile=THRESHOLD_PERCENTILE)
        null_zshuffle.append(topo_s)

    # Null bank: angular CSR scheme
    rng_csr = np.random.default_rng(102)
    null_csr = []
    for k in range(N_NULL_REALIZATIONS):
        ra_s, dec_s, z_s = angular_csr_realization(ra, dec, z, rng_csr)
        x_s, y_s, zc_s = radec_z_to_tangent_plane_mpc(ra_s, dec_s, z_s, ra0_deg=ra0, dec0_deg=dec0)
        field_s = density_field_cartesian_mpc(x_s, y_s, zc_s, nbins=NBINS, ranges=ranges)
        topo_s = compute_betti_numbers(field_s, threshold_percentile=THRESHOLD_PERCENTILE)
        null_csr.append(topo_s)

    # Nonzero-variance check (the check WP-R3 was missing)
    zshuffle_b0_var = float(np.var([r["beta_0"] for r in null_zshuffle]))
    csr_b0_var = float(np.var([r["beta_0"] for r in null_csr]))

    # Percentile rank of real data within each null
    def percentile_rank(value, distribution):
        arr = np.array(distribution)
        return float(np.mean(arr <= value) * 100)

    zshuffle_b0_dist = [r["beta_0"] for r in null_zshuffle]
    csr_b0_dist = [r["beta_0"] for r in null_csr]

    result = {
        "field_name": name,
        "survey": field_info["survey"],
        "cosmology": "Planck18 (astropy.cosmology.Planck18; Planck Collaboration 2018/2020, A&A 641, A6)",
        "n_input": n_input,
        "redshift_drop_report": drop_report,
        "comoving_ranges_mpc": {
            "x": [float(ranges[0][0]), float(ranges[0][1])],
            "y": [float(ranges[1][0]), float(ranges[1][1])],
            "z": [float(ranges[2][0]), float(ranges[2][1])],
        },
        "real_topology": real_topo,
        "bin_occupancy": {
            "occupied_bins": occupied_bins,
            "total_bins": total_bins,
            "fraction_occupied": occupied_bins / total_bins,
        },
        "null_zshuffle": {
            "n_realizations": N_NULL_REALIZATIONS,
            "beta_0_mean": float(np.mean(zshuffle_b0_dist)),
            "beta_0_std": float(np.std(zshuffle_b0_dist)),
            "beta_0_variance": zshuffle_b0_var,
            "beta_0_percentile_rank_of_real": percentile_rank(real_topo["beta_0"], zshuffle_b0_dist),
            "nonzero_variance_check": "PASS" if zshuffle_b0_var > 0 else "FAIL",
        },
        "null_csr": {
            "n_realizations": N_NULL_REALIZATIONS,
            "beta_0_mean": float(np.mean(csr_b0_dist)),
            "beta_0_std": float(np.std(csr_b0_dist)),
            "beta_0_variance": csr_b0_var,
            "beta_0_percentile_rank_of_real": percentile_rank(real_topo["beta_0"], csr_b0_dist),
            "nonzero_variance_check": "PASS" if csr_b0_var > 0 else "FAIL",
        },
        "label": "ENGINEERING",
    }

    return result


def main():
    print("WP-R5: Real 3D Comoving Density Field + Corrected Null Bank")
    print("=" * 80)
    print(f"Cosmology: Planck18 (cited, pipeline/cosmology.py)")
    print(f"Config: nbins={NBINS}, threshold={THRESHOLD_PERCENTILE}%, "
          f"null realizations={N_NULL_REALIZATIONS} per scheme")
    print("Scope: ENGINEERING only (no TEST/FIT; gate G1-L closed)\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_results = {}
    for field_info in FIELDS:
        name = field_info["name"]
        print(f"Processing {name} ({field_info['survey']})...")
        result = process_field(field_info)
        all_results[name] = result

        print(f"  n_input={result['n_input']}, "
              f"dropped={result['redshift_drop_report']['n_dropped']} "
              f"(nan={result['redshift_drop_report']['n_dropped_nan']}, "
              f"neg={result['redshift_drop_report']['n_dropped_negative']})")
        print(f"  Bin occupancy: {result['bin_occupancy']['occupied_bins']}/"
              f"{result['bin_occupancy']['total_bins']} "
              f"({result['bin_occupancy']['fraction_occupied']:.1%})")
        print(f"  Real topology: β₀={result['real_topology']['beta_0']}, "
              f"β₁={result['real_topology']['beta_1']}, "
              f"β₂={result['real_topology']['beta_2']}")
        print(f"  Null (z-shuffle): mean={result['null_zshuffle']['beta_0_mean']:.2f}, "
              f"std={result['null_zshuffle']['beta_0_std']:.2f}, "
              f"variance_check={result['null_zshuffle']['nonzero_variance_check']}, "
              f"real_percentile={result['null_zshuffle']['beta_0_percentile_rank_of_real']:.1f}%")
        print(f"  Null (CSR):      mean={result['null_csr']['beta_0_mean']:.2f}, "
              f"std={result['null_csr']['beta_0_std']:.2f}, "
              f"variance_check={result['null_csr']['nonzero_variance_check']}, "
              f"real_percentile={result['null_csr']['beta_0_percentile_rank_of_real']:.1f}%")
        print()

    # Save
    output_file = OUTPUT_DIR / "wp_r5_results_2026_07_25.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)
    sha = _sha256_file(output_file)

    metadata = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cosmology": "Planck18",
        "nbins": NBINS,
        "threshold_percentile": THRESHOLD_PERCENTILE,
        "n_null_realizations": N_NULL_REALIZATIONS,
        "fields": list(all_results.keys()),
        "output_file": str(output_file),
        "sha256": sha,
        "label": "ENGINEERING",
        "supersedes": "data/nullbanks/real/nullbank_2026_07_25.json (WP-R3, "
                       "retracted per docs/FINDING_R_NULLDEGENERATE_2026_07_25.md)",
    }
    metadata_file = OUTPUT_DIR / "WP_R5_MANIFEST_2026_07_25.json"
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=2)

    print("=" * 80)
    print(f"Results: {output_file}")
    print(f"SHA256:  {sha}")
    print(f"Metadata: {metadata_file}\n")

    # Overall nonzero-variance validation
    all_pass = all(
        r["null_zshuffle"]["nonzero_variance_check"] == "PASS"
        and r["null_csr"]["nonzero_variance_check"] == "PASS"
        for r in all_results.values()
    )
    print(f"Nonzero-variance check (all fields, both schemes): "
          f"{'✅ ALL PASS' if all_pass else '❌ SOME FAILED'}")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
