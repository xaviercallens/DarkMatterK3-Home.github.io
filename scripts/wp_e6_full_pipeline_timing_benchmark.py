#!/usr/bin/env python
"""
Extended timing benchmark for desisim full pipeline at N=50.

This benchmark includes the COMPLETE pipeline per ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md §1:
1. MockMaker.get_lya_skewers() - Gaussian-field transmission generation
2. desispec.resample_flux() - convert to uniform wavelength grid
3. sim_spectra() - instrument resolution convolution + Poisson/read noise

This corrects the scope gap in the initial N=50 benchmark, which measured only step 1.

FIXED SEED: 12345 (for reproducibility; this is only for timing, not a physics run)
Reference configuration from phase1_work/agent3_synthetic/run_mock_and_compare.py
"""
import sys
import json
import time
import resource
import platform
from pathlib import Path
import tempfile
import shutil

import numpy as np

# Import pipeline components per the reference script
from desisim.lya_mock_p1d import MockMaker
from desisim.scripts.quickspectra import sim_spectra
from desispec.interpolation import resample_flux

def get_memory_usage_mb():
    """Get current peak RSS memory in MB."""
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return usage.ru_maxrss / 1024  # Convert from KB to MB (on Linux)

def benchmark_full_pipeline_n50():
    """
    Benchmark full N=50 pipeline: MockMaker + resampling + sim_spectra.

    Returns:
        dict: timing statistics and metadata
    """
    FIXED_SEED = 12345
    N_SKEWERS = 50

    # Record Python and desisim versions
    import desisim
    import desispec
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    # Attempt to get versions from package metadata
    try:
        import importlib.metadata
        desisim_version = importlib.metadata.version('desisim')
        desispec_version = importlib.metadata.version('desispec')
    except Exception:
        desisim_version = getattr(desisim, '__version__', 'unknown')
        desispec_version = getattr(desispec, '__version__', 'unknown')

    print(f"Python version: {py_version}")
    print(f"desisim path: {desisim.__file__}")
    print(f"desispec path: {desispec.__file__}")
    print(f"Platform: {platform.platform()}")
    print()

    # Initialize MockMaker (one-time cost)
    print(f"Initializing MockMaker with seed={FIXED_SEED}...")
    t_init_start = time.time()
    mm = MockMaker(N2=12, dv_kms=20.0, seed=FIXED_SEED, white_noise=False)
    t_init_end = time.time()
    init_time = t_init_end - t_init_start
    print(f"  MockMaker initialization: {init_time:.4f} s")
    print()

    # Timing measurements
    mem_before = get_memory_usage_mb()
    t_pipeline_start = time.time()

    # Step 1: Generate transmission skewers
    print(f"Step 1: get_lya_skewers(Ns={N_SKEWERS})...")
    t_step1_start = time.time()
    wave_native, trans_native = mm.get_lya_skewers(Ns=N_SKEWERS, new_seed=FIXED_SEED)
    t_step1_end = time.time()
    step1_time = t_step1_end - t_step1_start
    print(f"  Step 1 elapsed: {step1_time:.4f} s")
    print(f"  Wave shape: {wave_native.shape}, Trans shape: {trans_native.shape}")

    # Step 2: Resample to uniform wavelength grid
    print(f"Step 2: resample_flux() to uniform grid...")
    t_step2_start = time.time()
    dwave = 0.2  # matches quickquasars internal default
    wave = np.arange(wave_native.min(), wave_native.max(), dwave)
    trans = np.array([resample_flux(wave, wave_native, trans_native[i])
                      for i in range(N_SKEWERS)])
    t_step2_end = time.time()
    step2_time = t_step2_end - t_step2_start
    print(f"  Step 2 elapsed: {step2_time:.4f} s")
    print(f"  Uniform grid size: {wave.size} cells, dwave={dwave}")

    # Step 3: Create continuum and combine with transmission
    print(f"Step 3: create clean flux...")
    t_step3_start = time.time()
    continuum_level = 6.0  # 1e-17 erg/s/cm2/A units
    continuum = continuum_level * (wave / wave.mean()) ** (-0.5)
    clean_flux = continuum[None, :] * trans  # [N_SKEWERS, npix]
    t_step3_end = time.time()
    step3_time = t_step3_end - t_step3_start
    print(f"  Step 3 elapsed: {step3_time:.4f} s")
    print(f"  Clean flux shape: {clean_flux.shape}")

    # Step 4: Instrument simulation (resolution + noise) via sim_spectra
    print(f"Step 4: sim_spectra() instrument simulation...")
    t_step4_start = time.time()

    # Create temporary directory for spectra output (sim_spectra writes FITS files)
    tmpdir = tempfile.mkdtemp(prefix="wp_e6_timing_", dir="/tmp")
    output_file = f"{tmpdir}/spectra-timing.fits"

    try:
        sourcetype = np.array(["qso"] * N_SKEWERS)
        redshift = np.full(N_SKEWERS, 3.0)

        resolution = sim_spectra(
            wave, clean_flux, program="DARK",
            spectra_filename=output_file,
            sourcetype=sourcetype, redshift=redshift, seed=FIXED_SEED,
            use_poisson=True, save_resolution=False,
        )
        t_step4_end = time.time()
        step4_time = t_step4_end - t_step4_start
        print(f"  Step 4 elapsed: {step4_time:.4f} s")
        print(f"  Output FITS: {output_file}")
        print(f"  Resolution matrices: {list(resolution.keys())}")

    finally:
        # Clean up temporary directory
        if Path(tmpdir).exists():
            shutil.rmtree(tmpdir)

    t_pipeline_end = time.time()
    mem_after = get_memory_usage_mb()

    total_elapsed = t_pipeline_end - t_pipeline_start
    per_skewer_full = total_elapsed / N_SKEWERS
    peak_memory = mem_after

    print()
    print(f"=== PIPELINE TIMING SUMMARY ===")
    print(f"Total (all steps): {total_elapsed:.4f} s")
    print(f"  Step 1 (skewer generation): {step1_time:.4f} s ({100*step1_time/total_elapsed:.1f}%)")
    print(f"  Step 2 (resampling): {step2_time:.4f} s ({100*step2_time/total_elapsed:.1f}%)")
    print(f"  Step 3 (continuum): {step3_time:.4f} s ({100*step3_time/total_elapsed:.1f}%)")
    print(f"  Step 4 (instrument sim): {step4_time:.4f} s ({100*step4_time/total_elapsed:.1f}%)")
    print(f"Per-skewer marginal: {per_skewer_full:.6f} s/skewer")
    print(f"Peak RSS memory: {peak_memory:.2f} MB")
    print()

    # Linear extrapolation to N=200
    N_target = 200
    extrapolated_time = total_elapsed * (N_target / N_SKEWERS)

    print(f"Linear extrapolation to N={N_target}:")
    print(f"  Estimated wall-clock: {extrapolated_time:.2f} s ({extrapolated_time/60:.2f} min)")
    print()

    # Build result dict
    result = {
        "benchmark_metadata": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "python_version": py_version,
            "desisim_version": desisim_version,
            "desispec_version": desispec_version,
            "desisim_path": str(desisim.__file__),
            "platform": platform.platform(),
            "fixed_seed": FIXED_SEED,
            "pipeline_version": "FULL (MockMaker + resample + sim_spectra)",
            "reference_config": "phase1_work/agent3_synthetic/run_mock_and_compare.py",
        },
        "n50_results": {
            "n_skewers": N_SKEWERS,
            "total_wall_clock_seconds": round(total_elapsed, 6),
            "per_skewer_marginal_seconds": round(per_skewer_full, 8),
            "peak_rss_mb": round(peak_memory, 2),
            "initialization_time_seconds": round(init_time, 4),
            "step_breakdown": {
                "step1_mockmaker_seconds": round(step1_time, 6),
                "step1_percent": round(100 * step1_time / total_elapsed, 1),
                "step2_resample_seconds": round(step2_time, 6),
                "step2_percent": round(100 * step2_time / total_elapsed, 1),
                "step3_continuum_seconds": round(step3_time, 6),
                "step3_percent": round(100 * step3_time / total_elapsed, 1),
                "step4_sim_spectra_seconds": round(step4_time, 6),
                "step4_percent": round(100 * step4_time / total_elapsed, 1),
            },
            "command_used": "Full pipeline: MockMaker.get_lya_skewers + resample_flux + sim_spectra",
        },
        "n200_extrapolation": {
            "n_skewers": N_target,
            "extrapolation_method": "linear",
            "assumption_note": "Linear scaling; assumes per-skewer cost is constant across all pipeline steps",
            "estimated_wall_clock_seconds": round(extrapolated_time, 2),
            "estimated_wall_clock_minutes": round(extrapolated_time / 60, 2),
        }
    }

    return result


if __name__ == "__main__":
    try:
        result = benchmark_full_pipeline_n50()

        # Ensure output directory exists
        output_dir = Path("/home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-Home/data/derived")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "wp_e6_desisim_timing_2026_07_28.json"

        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)

        print(f"\nResults written to: {output_file}")

    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
