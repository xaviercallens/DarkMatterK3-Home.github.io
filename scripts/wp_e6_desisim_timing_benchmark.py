#!/usr/bin/env python
"""
Timing benchmark for desisim MockMaker.get_lya_skewers() at N=50.

Measures wall-clock and peak memory for N=50 mock realization generation.
Records environment versions and timing stats for extrapolation to N=200.

FIXED SEED: 12345 (for reproducibility; this is only for timing, not a physics run)
"""
import sys
import json
import time
import resource
import platform
from pathlib import Path

# Ensure we can import desisim from the venv
from desisim.lya_mock_p1d import MockMaker

def get_memory_usage_mb():
    """Get current peak RSS memory in MB."""
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return usage.ru_maxrss / 1024  # Convert from KB to MB (on Linux)

def benchmark_n50():
    """
    Benchmark N=50 skewer generation.

    Returns:
        dict: timing statistics and metadata
    """
    FIXED_SEED = 12345
    N_SKEWERS = 50

    # Record Python and desisim versions
    import desisim
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    # Attempt to get desisim version from package metadata
    try:
        import importlib.metadata
        desisim_version = importlib.metadata.version('desisim')
    except Exception:
        # If that fails, try from package itself
        desisim_version = getattr(desisim, '__version__', 'unknown')

    print(f"Python version: {py_version}")
    print(f"desisim path: {desisim.__file__}")
    print(f"Platform: {platform.platform()}")
    print()

    # Initialize MockMaker (this is a one-time cost)
    print(f"Initializing MockMaker with seed={FIXED_SEED}...")
    t_init_start = time.time()
    mm = MockMaker(N2=12, dv_kms=20.0, seed=FIXED_SEED, white_noise=False)
    t_init_end = time.time()
    init_time = t_init_end - t_init_start
    print(f"  Initialization time: {init_time:.4f} s")
    print()

    # Benchmark get_lya_skewers(Ns=50)
    print(f"Running get_lya_skewers(Ns={N_SKEWERS})...")
    mem_before = get_memory_usage_mb()
    t_start = time.time()

    wave, trans = mm.get_lya_skewers(Ns=N_SKEWERS, new_seed=FIXED_SEED)

    t_end = time.time()
    mem_after = get_memory_usage_mb()

    elapsed = t_end - t_start
    per_skewer = elapsed / N_SKEWERS
    peak_memory = mem_after

    print(f"  Total elapsed: {elapsed:.4f} s")
    print(f"  Per-skewer marginal: {per_skewer:.6f} s/skewer")
    print(f"  Peak RSS memory: {peak_memory:.2f} MB")
    print(f"  Wave shape: {wave.shape}, Trans shape: {trans.shape}")
    print()

    # Linear extrapolation to N=200
    N_target = 200
    extrapolated_time = elapsed * (N_target / N_SKEWERS)

    print(f"Linear extrapolation to N={N_target}:")
    print(f"  Estimated wall-clock: {extrapolated_time:.2f} s ({extrapolated_time/60:.2f} min)")
    print()

    # Build result dict
    result = {
        "benchmark_metadata": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "python_version": py_version,
            "desisim_version": desisim_version,
            "desisim_path": str(desisim.__file__),
            "platform": platform.platform(),
            "fixed_seed": FIXED_SEED,
        },
        "n50_results": {
            "n_skewers": N_SKEWERS,
            "total_wall_clock_seconds": round(elapsed, 6),
            "per_skewer_marginal_seconds": round(per_skewer, 8),
            "peak_rss_mb": round(peak_memory, 2),
            "initialization_time_seconds": round(init_time, 4),
            "command_used": f"MockMaker.get_lya_skewers(Ns={N_SKEWERS}, new_seed={FIXED_SEED})",
        },
        "n200_extrapolation": {
            "n_skewers": N_target,
            "extrapolation_method": "linear",
            "assumption_note": "Linear scaling; assumes per-skewer cost is constant",
            "estimated_wall_clock_seconds": round(extrapolated_time, 2),
            "estimated_wall_clock_minutes": round(extrapolated_time / 60, 2),
        }
    }

    return result


if __name__ == "__main__":
    try:
        result = benchmark_n50()

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
