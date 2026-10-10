#!/usr/bin/env python3
"""WP-E6-SWEEP — the pinned R-KEFF-2 pre-check (K2), re-run on the C4 aggregation artifacts.

The v1 script (`wp_e6_sweep_keff_emulator_precheck_2026_09_17.py`) is imported unchanged; only its input and output
paths are redirected. The threshold (0.1 σ_b), the controls and the emulator are the v1 ones, so this run can tune nothing.
ENGINEERING / DESIGN (not TEST, not FIT); no data vector is used (σ_b from the C₉ diagonal, k_eff from the artifact).

    ~/venv/bin/python scripts/wp_e6_sweep_keff_emulator_precheck_c4_2026_10_10.py
Writes data/derived/wp_e6_sweep_keff_emulator_precheck_c4_2026_10_10.json
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V1 = ROOT / "scripts" / "wp_e6_sweep_keff_emulator_precheck_2026_09_17.py"

spec = importlib.util.spec_from_file_location("precheck_v1", V1)
mod = importlib.util.module_from_spec(spec)
sys.argv = [str(V1)]
spec.loader.exec_module(mod)
mod.AGG = ROOT / "data/derived/wp_e6_sweep_cov_agg9_c4_z4p2_2026_10_10.json"
mod.OUT = ROOT / "data/derived/wp_e6_sweep_keff_emulator_precheck_c4_2026_10_10.json"

if __name__ == "__main__":
    sys.exit(mod.main())
