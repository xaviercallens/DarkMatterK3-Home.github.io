#!/usr/bin/env python3
"""
v5_cooper_worker.py
===================

V5 Pipeline Worker: First-Principles Cooper s_7 K3 Analysis

Integrates the Phase 1 Cooper period integral engine (cooper_periods.py) with
the existing SDSS DR17 / Euclid data pipeline.

Key improvements over V4C:
  - Replaces phenomenological mu-scaling with true Picard-Fuchs period integrals
  - Computes Δ_{s7} directly from FFT difference (not linear calibration)
  - Enables Phase 2 tests (TDA alignment, redshift tomography, weak lensing)

Outputs:
  - logs/v5_cooper_pipeline.log (detailed execution log)
  - logs/v5_cooper_results.json (streaming results per sector)
  - discoveries_v5_cooper.json (high-Δ anomalies detected by V5)
"""

import time
import os
import json
import torch
import numpy as np
from datetime import datetime
from pathlib import Path
from scipy.fftpack import fftn
import sys

# Import Phase 1 Cooper engine
sys.path.insert(0, os.path.dirname(__file__))
from cooper_periods import (
    CooperS7Sequence,
    DensityModulusMapper,
    PeriodIntegralEvaluator,
    CooperAsymmetryMetric,
    create_synthetic_density_field
)

# Try to import real SDSS data fetcher
try:
    from real_euclid_worker import fetch_real_sdss_data, comoving_distance
    REAL_DATA_AVAILABLE = True
except ImportError:
    REAL_DATA_AVAILABLE = False
    print("[WARNING] real_euclid_worker not available; using synthetic fallback")

# ============================================================================
# CONFIGURATION
# ============================================================================

H0 = 71.92
Omega_m = 0.315
Omega_de = 0.685
c_light = 299792.458
GRID_SIZE = 128

BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

V5_LOG_FILE = LOGS_DIR / "v5_cooper_pipeline.log"
V5_RESULTS_FILE = LOGS_DIR / "v5_cooper_results.json"
V5_DISCOVERIES_FILE = BASE_DIR / "discoveries_v5_cooper.json"
STATE_FILE = BASE_DIR / "v5_sector_state.json"

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# ============================================================================
# SECTOR GRID DEFINITION
# ============================================================================

RA_STEPS = np.linspace(150.0, 220.0, 8)
DEC_STEPS = np.linspace(0.0, 50.0, 6)
SECTORS = []
for i in range(len(RA_STEPS) - 1):
    for j in range(len(DEC_STEPS) - 1):
        SECTORS.append({
            "sector_id": len(SECTORS),
            "ra_min": float(RA_STEPS[i]),
            "ra_max": float(RA_STEPS[i+1]),
            "dec_min": float(DEC_STEPS[j]),
            "dec_max": float(DEC_STEPS[j+1])
        })


# ============================================================================
# LOGGING
# ============================================================================

def log_v5(message, level="INFO"):
    """Log to V5-specific file and stdout."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] [{level}] {message}"
    print(log_msg)
    try:
        with open(V5_LOG_FILE, "a") as f:
            f.write(log_msg + "\n")
    except Exception as e:
        print(f"[ERROR] Failed to write log: {e}")


# ============================================================================
# GALAXY DATA INGESTION
# ============================================================================

def ingest_sector_data(sector, use_real_data=True):
    """
    Ingest galaxy data for a sector (real or synthetic fallback).

    Returns:
        tuple: (ra, dec, z, source_label)
    """
    if REAL_DATA_AVAILABLE and use_real_data:
        try:
            return fetch_real_sdss_data(
                sector["ra_min"],
                sector["ra_max"],
                sector["dec_min"],
                sector["dec_max"],
                limit=10000
            )
        except Exception as e:
            log_v5(f"Real SDSS query failed: {e}", "WARNING")

    # Synthetic fallback (physically motivated)
    log_v5(f"Using synthetic fallback for Sector {sector['sector_id']}", "INFO")
    np.random.seed(sector["sector_id"] + int(time.time()) % 1000)

    n_gal = np.random.randint(2000, 8000)
    ra = np.random.uniform(sector["ra_min"], sector["ra_max"], n_gal)
    dec = np.random.uniform(sector["dec_min"], sector["dec_max"], n_gal)
    z = np.random.normal(0.28, 0.07, n_gal)
    z = np.clip(z, 0.05, 0.6)

    source = f"Synthetic BOSS DR17 (Sector {sector['sector_id']})"
    return ra, dec, z, source


# ============================================================================
# VOXEL GRID CONSTRUCTION
# ============================================================================

def build_density_grid(ra, dec, z, grid_size=GRID_SIZE):
    """
    Build 3D voxel density field from galaxy catalog.

    Maps galaxy (RA, Dec, z) to 3D grid via comoving distance projection.

    Returns:
        tuple: (rho_grid, grid_metadata)
    """
    # Convert to comoving distances
    if REAL_DATA_AVAILABLE:
        comoving_z = np.array([comoving_distance(zi) for zi in z])
    else:
        # Simple z-distance mapping
        comoving_z = c_light * z / H0

    # Normalize coordinates to [0, grid_size)
    ra_norm = (ra - ra.min()) / (ra.max() - ra.min() + 1e-10)
    dec_norm = (dec - dec.min()) / (dec.max() - dec.min() + 1e-10)
    z_norm = (comoving_z - comoving_z.min()) / (comoving_z.max() - comoving_z.min() + 1e-10)

    ra_idx = (ra_norm * (grid_size - 1)).astype(int)
    dec_idx = (dec_norm * (grid_size - 1)).astype(int)
    z_idx = (z_norm * (grid_size - 1)).astype(int)

    # Bin galaxies into voxels
    rho_grid = np.zeros((grid_size, grid_size, grid_size), dtype=np.float32)
    np.add.at(rho_grid, (ra_idx, dec_idx, z_idx), 1.0)

    # Smooth with Gaussian kernel (3-pixel FWHM)
    from scipy.ndimage import gaussian_filter
    rho_grid = gaussian_filter(rho_grid, sigma=1.0)

    # Normalize to typical density scale
    rho_grid = rho_grid / (np.mean(rho_grid) + 1e-10)

    metadata = {
        "n_galaxies": len(ra),
        "grid_size": grid_size,
        "density_mean": np.mean(rho_grid),
        "density_max": np.max(rho_grid),
        "density_min": np.min(rho_grid)
    }

    return rho_grid, metadata


# ============================================================================
# COOPER S_7 ANALYSIS (PHASE 1)
# ============================================================================

def analyze_sector_cooper_s7(sector, rho_grid, max_terms=20):
    """
    Perform full Phase 1 Cooper s_7 analysis on sector density grid.

    Returns:
        dict: Analysis results including Δ_{s7}, grid properties, etc.
    """
    log_v5(f"Analyzing Sector {sector['sector_id']} with Cooper s_7 engine", "INFO")

    # Compute Δ_{s7} via FFT difference
    result = CooperAsymmetryMetric.compute_delta_s7(rho_grid, max_terms=max_terms)

    # Compute per-voxel Cooper-to-raw ratio (encodes K3 warping pattern)
    grid_cooper = result['grid_cooper']
    grid_raw = result['grid_raw']
    ratio_field = grid_cooper / (grid_raw + 1e-10)

    # Identify high-warping voxels (potential anomaly sites)
    top_percentile = np.percentile(ratio_field, 90)
    high_warping_mask = ratio_field > top_percentile
    n_high_warping = np.sum(high_warping_mask)

    analysis = {
        "sector_id": sector["sector_id"],
        "ra_range": [sector["ra_min"], sector["ra_max"]],
        "dec_range": [sector["dec_min"], sector["dec_max"]],
        "timestamp": datetime.now().isoformat(),

        # Phase 1 metrics
        "delta_s7": float(result['delta_s7']),
        "mean_delta_s7": float(result['mean_delta_s7']),
        "max_cooper_warping": float(np.max(ratio_field)),
        "mean_cooper_warping": float(np.mean(ratio_field)),
        "n_high_warping_voxels": int(n_high_warping),
        "high_warping_percentile": float(top_percentile),

        # Grid properties
        "grid_size": GRID_SIZE,
        "max_density": float(np.max(rho_grid)),
        "mean_density": float(np.mean(rho_grid)),
    }

    return analysis, result


# ============================================================================
# DISCOVERY CLASSIFICATION
# ============================================================================

def classify_discovery(analysis, threshold_s7=0.05):
    """
    Classify whether sector contains a notable anomaly based on Cooper s_7 metrics.

    Returns:
        tuple: (is_discovery, discovery_type, significance_score)
    """
    delta_s7 = analysis["delta_s7"]
    max_warping = analysis["max_cooper_warping"]

    # Thresholds (calibrated from Phase 1 tests)
    if delta_s7 > threshold_s7 * 2.0 and max_warping > 2.0:
        return True, "EXTREME_K3_WARPING", delta_s7 * max_warping
    elif delta_s7 > threshold_s7 and max_warping > 1.5:
        return True, "STRONG_GEOMETRIC_ANOMALY", delta_s7 * max_warping
    elif delta_s7 > threshold_s7 * 0.5:
        return True, "MODERATE_COOPER_SIGNAL", delta_s7
    else:
        return False, "BACKGROUND", 0.0


# ============================================================================
# PIPELINE EXECUTION
# ============================================================================

def process_sector(sector, use_real_data=True):
    """
    End-to-end processing of a single sector.

    Returns:
        dict: Complete analysis + metadata for sector
    """
    log_v5(f"Processing Sector {sector['sector_id']}: RA [{sector['ra_min']:.1f}, {sector['ra_max']:.1f}], Dec [{sector['dec_min']:.1f}, {sector['dec_max']:.1f}]", "INFO")

    # Step 1: Ingest data
    start_time = time.time()
    ra, dec, z, source = ingest_sector_data(sector, use_real_data)
    log_v5(f"  Ingested {len(ra)} galaxies from {source}", "INFO")

    # Step 2: Build voxel grid
    rho_grid, grid_metadata = build_density_grid(ra, dec, z)
    log_v5(f"  Built {GRID_SIZE}³ density grid (mean: {grid_metadata['density_mean']:.3f})", "INFO")

    # Step 3: Perform Cooper s_7 analysis
    analysis, result = analyze_sector_cooper_s7(sector, rho_grid, max_terms=20)

    # Step 4: Classify discovery
    is_discovery, disc_type, significance = classify_discovery(analysis)

    elapsed = time.time() - start_time

    # Compile results
    sector_result = {
        **analysis,
        "data_source": source,
        "n_galaxies": len(ra),
        "processing_time_s": float(elapsed),
        "is_discovery": is_discovery,
        "discovery_type": disc_type,
        "significance_score": float(significance)
    }

    log_v5(f"  Δ_s7={analysis['delta_s7']:.6f}, Discovery: {disc_type} (sig={significance:.3f}), Time: {elapsed:.2f}s", "INFO")

    return sector_result


def run_v5_pipeline(max_sectors=None, use_real_data=True):
    """
    Main V5 pipeline execution loop.

    Args:
        max_sectors (int or None): Max sectors to process (None = all)
        use_real_data (bool): Attempt real SDSS data vs synthetic fallback
    """
    log_v5("=" * 70, "INFO")
    log_v5("V5 COOPER S_7 PIPELINE: PHASE 1 EXECUTION", "INFO")
    log_v5("=" * 70, "INFO")
    log_v5(f"Device: {device}", "INFO")
    log_v5(f"Grid size: {GRID_SIZE}³ voxels", "INFO")
    log_v5(f"Sectors to process: {min(len(SECTORS), max_sectors or len(SECTORS))}", "INFO")
    log_v5("=" * 70, "INFO")

    results = []
    discoveries = []

    sectors_to_process = SECTORS[:max_sectors] if max_sectors else SECTORS

    for i, sector in enumerate(sectors_to_process):
        try:
            result = process_sector(sector, use_real_data)
            results.append(result)

            # Append discoveries
            if result["is_discovery"]:
                discoveries.append({
                    "sector_id": result["sector_id"],
                    "type": result["discovery_type"],
                    "delta_s7": result["delta_s7"],
                    "significance": result["significance_score"],
                    "ra": (result["ra_range"][0] + result["ra_range"][1]) / 2,
                    "dec": (result["dec_range"][0] + result["dec_range"][1]) / 2,
                    "timestamp": result["timestamp"]
                })

            # Periodically save results
            if (i + 1) % 5 == 0 or i == len(sectors_to_process) - 1:
                save_v5_results(results, discoveries)

        except Exception as e:
            log_v5(f"ERROR processing Sector {sector['sector_id']}: {e}", "ERROR")
            import traceback
            traceback.print_exc()

    log_v5("=" * 70, "INFO")
    log_v5(f"Pipeline complete. {len(sectors_to_process)} sectors processed.", "INFO")
    log_v5(f"Discoveries: {len(discoveries)}", "INFO")
    log_v5("=" * 70, "INFO")

    return results, discoveries


# ============================================================================
# PERSISTENCE
# ============================================================================

def save_v5_results(results, discoveries):
    """Save results to JSON files."""
    try:
        with open(V5_RESULTS_FILE, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "n_sectors": len(results),
                "sectors": results
            }, f, indent=2)

        with open(V5_DISCOVERIES_FILE, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "n_discoveries": len(discoveries),
                "discoveries": discoveries
            }, f, indent=2)

        log_v5(f"Saved {len(results)} sector results and {len(discoveries)} discoveries", "INFO")
    except Exception as e:
        log_v5(f"Error saving results: {e}", "ERROR")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="V5 Cooper s_7 Pipeline")
    parser.add_argument("--max-sectors", type=int, default=10, help="Max sectors to process (default: 10)")
    parser.add_argument("--use-real-data", action="store_true", help="Attempt real SDSS data")
    parser.add_argument("--synthetic-only", action="store_true", help="Use synthetic data only")
    args = parser.parse_args()

    use_real = args.use_real_data and not args.synthetic_only

    log_v5(f"Starting V5 pipeline with max_sectors={args.max_sectors}, use_real_data={use_real}", "INFO")

    results, discoveries = run_v5_pipeline(max_sectors=args.max_sectors, use_real_data=use_real)

    log_v5(f"Pipeline execution complete", "INFO")
