#!/usr/bin/env python3
"""WP-E6-SWEEP — run the pinned K3 gate with the live emulator and write C₉,sys (design §4, Option B).

ENGINEERING / DESIGN label (CLAUDE.md rule 3); no model–data comparison. Consuming comparisons: exclusion/FIT.
Pin: briefs/WP_E6_SWEEP_KEFF_RULING_PINNED_2026_09_17.md (57a6065). Needs the gitignored emulator.
    ~/venv/bin/python scripts/wp_e6_sweep_keff_gate_2026_09_17.py
Writes (gate record first, before any print; C₉,sys only if the gate passes):
    data/derived/wp_e6_sweep_keff_gate_2026_09_17.json
    data/derived/wp_e6_sweep_cov_agg9_sys_z4p2_2026_09_17.npy
"""
import sys, warnings
from pathlib import Path
import numpy as np
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline")); sys.path.insert(0, str(ROOT / "phase1_work" / "agent1_emulator"))
import keff  # noqa: E402

GATE_OUT = ROOT / "data/derived/wp_e6_sweep_keff_gate_2026_09_17.json"
COV_OUT = ROOT / "data/derived/wp_e6_sweep_cov_agg9_sys_z4p2_2026_09_17.npy"


def main():
    try:
        import emu_predict as E
        emulator = (E.predict_pk, E.load())
    except Exception as exc:  # recorded by the gate as NOT_RUN
        print(f"emulator unavailable: {type(exc).__name__}: {exc}")
        emulator = None
    rec = keff.sweep_gate(emulator=emulator, out_path=GATE_OUT)
    if rec["passes"]:
        np.save(COV_OUT, keff.augmented_covariance(np.load(keff.AGG_NPY)))
    print(f"gate written: {GATE_OUT}")
    for name, item in rec["items"].items():
        print(f"  {name}: {'PASS' if item['pass'] else 'FAIL'} {({k: v for k, v in item.items() if k != 'pass'})}")
    print(f"GATE: {'PASS' if rec['passes'] else 'FAIL'}" + (f" — wrote {COV_OUT.name}" if rec["passes"] else " — C₉,sys not written"))
    return 0 if rec["passes"] else 1


if __name__ == "__main__":
    sys.exit(main())
