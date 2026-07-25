#!/usr/bin/env python3
"""WP-R6: Survey scale characterization — pure data facts for Streams 1 & 2.

Bottom-up, simplest-possible extraction: measure what physical scales (length,
angular resolution, redshift depth, comoving volume, object density) the real
SDSS + Euclid data on hand actually resolve. No model, no hypothesis, no
comparison — just descriptive statistics of the real catalogs, tagged
ENGINEERING throughout.

Purpose: Stream 1 (chameleon screening-radius formalization, WP-B1) and
Stream 2 (K3 candidate selection) both eventually need to know what
observational regimes are empirically accessible with data already in hand.
This script answers that with measured numbers, not assumed ones.
"""
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

import pandas as pd
import numpy as np
import json
from datetime import datetime, timezone

from pipeline.cosmology import comoving_distance_mpc, drop_invalid_redshifts

OUTPUT_DIR = Path("/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/survey_characterization")

FIELDS = [
    {
        "name": "sdss_cosmos", "survey": "SDSS", "kind": "photometric",
        "path": "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/sdss/sdss_cosmos.csv",
        "ra_col": "ra", "dec_col": "dec", "box_arcmin": 10.0,
    },
    {
        "name": "sdss_stripe82_center", "survey": "SDSS", "kind": "photometric",
        "path": "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/sdss/sdss_stripe82_center.csv",
        "ra_col": "ra", "dec_col": "dec", "box_arcmin": 10.0,
    },
    {
        "name": "sdss_coma_cluster", "survey": "SDSS", "kind": "photometric",
        "path": "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/sdss/sdss_coma_cluster.csv",
        "ra_col": "ra", "dec_col": "dec", "box_arcmin": 10.0,
    },
    {
        "name": "euclid_edf_north", "survey": "Euclid", "kind": "photometric",
        "path": "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid/euclid_edf_north.csv",
        "ra_col": "right_ascension", "dec_col": "declination", "box_arcmin": 24.0,  # 0.2 deg radius cone
    },
    {
        "name": "sdss_z_coma_cluster", "survey": "SDSS", "kind": "spectroscopic",
        "path": "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/sdss_z/sdss_z_coma_cluster.csv",
        "ra_col": "ra", "dec_col": "dec", "z_col": "z", "box_arcmin": 10.0,
    },
    {
        "name": "euclid_z_edf_north", "survey": "Euclid", "kind": "photo-z",
        "path": "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid_z/euclid_z_edf_north.csv",
        "ra_col": "right_ascension", "dec_col": "declination", "z_col": "phz_median", "box_arcmin": 24.0,
    },
    {
        "name": "euclid_z_edf_fornax", "survey": "Euclid", "kind": "photo-z",
        "path": "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid_z/euclid_z_edf_fornax.csv",
        "ra_col": "right_ascension", "dec_col": "declination", "z_col": "phz_median", "box_arcmin": 24.0,
    },
    {
        "name": "euclid_z_edf_south", "survey": "Euclid", "kind": "photo-z",
        "path": "/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/euclid_z/euclid_z_edf_south.csv",
        "ra_col": "right_ascension", "dec_col": "declination", "z_col": "phz_median", "box_arcmin": 24.0,
    },
]


def nearest_neighbor_angular_sep_arcsec(ra, dec):
    """Median nearest-neighbor angular separation (arcsec) — a plain-vanilla
    measure of the catalog's effective angular resolution/sampling scale.
    Small-angle approximation (fields here are all < 1 deg)."""
    ra = np.asarray(ra)
    dec = np.asarray(dec)
    dec_rad = np.radians(dec.mean())
    n = len(ra)
    if n < 2:
        return None

    # Brute-force O(n^2) nearest neighbor; fine for n <= a few thousand
    seps = []
    x = ra * np.cos(dec_rad)
    y = dec
    for i in range(n):
        dx = x - x[i]
        dy = y - y[i]
        d2 = dx**2 + dy**2
        d2[i] = np.inf
        seps.append(np.sqrt(d2.min()))
    return float(np.median(seps) * 3600.0)  # deg -> arcsec


def characterize_field(field_info: dict) -> dict:
    df = pd.read_csv(field_info["path"])
    ra = df[field_info["ra_col"]].values
    dec = df[field_info["dec_col"]].values
    n_obj = len(df)

    ra_span_deg = float(ra.max() - ra.min())
    dec_span_deg = float(dec.max() - dec.min())
    box_arcmin = field_info["box_arcmin"]
    area_sq_arcmin = box_arcmin ** 2
    area_sq_deg = area_sq_arcmin / 3600.0
    surface_density_per_sqdeg = n_obj / area_sq_deg

    # Median nearest-neighbor angular scale (subsample if large, for O(n^2) cost)
    if n_obj > 2000:
        idx = np.random.default_rng(0).choice(n_obj, 2000, replace=False)
        nn_sep_arcsec = nearest_neighbor_angular_sep_arcsec(ra[idx], dec[idx])
    else:
        nn_sep_arcsec = nearest_neighbor_angular_sep_arcsec(ra, dec)

    result = {
        "field_name": field_info["name"],
        "survey": field_info["survey"],
        "kind": field_info["kind"],
        "n_objects": n_obj,
        "ra_span_deg": ra_span_deg,
        "dec_span_deg": dec_span_deg,
        "footprint_area_sq_deg": area_sq_deg,
        "surface_density_per_sq_deg": float(surface_density_per_sqdeg),
        "median_nearest_neighbor_sep_arcsec": nn_sep_arcsec,
    }

    # Redshift-dependent quantities, if this field has a z column
    if "z_col" in field_info:
        z_raw = df[field_info["z_col"]].values
        ra_v, dec_v, z_v, drop_report = drop_invalid_redshifts(ra, dec, z_raw)

        result["redshift_drop_report"] = drop_report
        result["z_min"] = float(z_v.min()) if len(z_v) else None
        result["z_max"] = float(z_v.max()) if len(z_v) else None
        result["z_median"] = float(np.median(z_v)) if len(z_v) else None

        if len(z_v) > 0:
            d_c_min = comoving_distance_mpc(result["z_min"])
            d_c_max = comoving_distance_mpc(result["z_max"])
            d_c_median = comoving_distance_mpc(result["z_median"])
            result["comoving_distance_min_mpc"] = float(d_c_min)
            result["comoving_distance_max_mpc"] = float(d_c_max)
            result["comoving_distance_median_mpc"] = float(d_c_median)

            # Transverse physical scale corresponding to the angular nearest-
            # neighbor separation, evaluated at the median redshift -- a
            # concrete "smallest resolved transverse physical scale" number.
            if nn_sep_arcsec is not None:
                nn_sep_rad = np.radians(nn_sep_arcsec / 3600.0)
                result["nn_transverse_physical_scale_mpc_at_median_z"] = float(
                    nn_sep_rad * d_c_median
                )

            # Comoving volume of the cone between z_min and z_max (small solid
            # angle approximation: dV = Omega * D_C^2 * dD_C, integrated
            # numerically over Planck18 D_C(z) via a simple trapezoid on a
            # fine z grid -- consistent with the cited cosmology, not a new one).
            solid_angle_sr = area_sq_deg * (np.pi / 180.0) ** 2
            z_grid = np.linspace(result["z_min"], result["z_max"], 200)
            d_c_grid = comoving_distance_mpc(z_grid)
            volume_mpc3 = float(
                solid_angle_sr / 3.0 * (d_c_grid[-1] ** 3 - d_c_grid[0] ** 3)
            )
            result["comoving_volume_mpc3"] = volume_mpc3
            result["number_density_per_mpc3"] = float(len(z_v) / volume_mpc3) if volume_mpc3 > 0 else None

    return result


def main():
    print("WP-R6: Survey Scale Characterization (bottom-up, pure data facts)")
    print("=" * 80)
    print("Scope: ENGINEERING only. No model, no hypothesis, no comparison.\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    all_results = {}

    for field_info in FIELDS:
        name = field_info["name"]
        print(f"Characterizing {name} ({field_info['survey']}, {field_info['kind']})...")
        result = characterize_field(field_info)
        all_results[name] = result

        print(f"  N={result['n_objects']}, area={result['footprint_area_sq_deg']:.4f} sq deg, "
              f"surface density={result['surface_density_per_sq_deg']:.0f}/sq deg")
        if result["median_nearest_neighbor_sep_arcsec"] is not None:
            print(f"  Median nearest-neighbor separation: "
                  f"{result['median_nearest_neighbor_sep_arcsec']:.2f} arcsec")
        if "z_median" in result and result["z_median"] is not None:
            print(f"  z range: [{result['z_min']:.3f}, {result['z_max']:.3f}], "
                  f"median={result['z_median']:.3f}")
            print(f"  Comoving distance range: [{result['comoving_distance_min_mpc']:.1f}, "
                  f"{result['comoving_distance_max_mpc']:.1f}] Mpc")
            if "nn_transverse_physical_scale_mpc_at_median_z" in result:
                print(f"  Transverse resolved scale at median z: "
                      f"{result['nn_transverse_physical_scale_mpc_at_median_z']:.4f} Mpc")
            print(f"  Comoving volume: {result['comoving_volume_mpc3']:.2e} Mpc^3, "
                  f"number density: {result['number_density_per_mpc3']:.2e} /Mpc^3")
        print()

    output_file = OUTPUT_DIR / "survey_scales_2026_07_25.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)

    import hashlib
    sha = hashlib.sha256(output_file.read_bytes()).hexdigest()
    print(f"Results: {output_file}\nSHA256: {sha}")

    metadata = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "fields": list(all_results.keys()),
        "output_file": str(output_file),
        "sha256": sha,
        "label": "ENGINEERING",
        "purpose": "Descriptive scale facts for Stream 1 (chameleon screening WP-B1) "
                   "and Stream 2 (K3 selection) — no hypothesis test.",
    }
    with open(OUTPUT_DIR / "SURVEY_SCALES_MANIFEST_2026_07_25.json", "w") as f:
        json.dump(metadata, f, indent=2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
