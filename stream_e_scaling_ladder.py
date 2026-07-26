#!/usr/bin/env python3
"""Stream E E3: Scaling ladder for C1 oracle.

Measures wall-clock performance of C1 verification across N1 ∈ {50, 100, 150, 200, 250, 300}.
Tests s7 and s10 (the two K3 candidates of interest).

Output: JSON scaling report to artifacts/stream_e/scaling_ladder_report.json
"""
import json
import subprocess
import time
from pathlib import Path

from checkers.check_C1_mirror_integrality import ORDER3_AZ_COOPER


def run_oracle_timed(name: str, n1: int) -> tuple[dict, float]:
    """Call stream_e_c1_oracle.py and return (certificate, wall_clock_seconds)."""
    start = time.perf_counter()
    result = subprocess.run(
        ["python", "stream_e_c1_oracle.py", "--order3", name, "--N1", str(n1)],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent,
    )
    elapsed = time.perf_counter() - start
    if result.returncode not in (0, 1):
        raise RuntimeError(f"oracle failed: {result.stderr}")
    cert = json.loads(result.stdout)
    return cert, elapsed


def run_scaling_ladder() -> dict:
    """Run scaling tests. Return report dict."""
    n1_values = [50, 100, 150, 200, 250, 300]
    candidates = ["s7", "s10"]

    report = {
        "test": "Stream E E3: Scaling Ladder",
        "candidates": candidates,
        "n1_values": n1_values,
        "results": {},
    }

    print("=" * 80)
    print("Stream E E3: Scaling Ladder")
    print("=" * 80)

    for name in candidates:
        print(f"\n[{name.upper()}]")
        print("-" * 80)
        report["results"][name] = []

        for n1 in n1_values:
            try:
                cert, elapsed = run_oracle_timed(name, n1)
                status = cert["status"]
                verdict = cert["verdict"]
                margin = cert["margin_max_denominator"]

                report["results"][name].append({
                    "N1": n1,
                    "status": status,
                    "verdict": verdict,
                    "margin_max_denominator": margin,
                    "wall_clock_seconds": round(elapsed, 3),
                })

                print(f"  N1={n1:3d}: {status:4s} {verdict:20s} margin={margin} time={elapsed:.3f}s")
            except Exception as e:
                print(f"  N1={n1:3d}: ERROR {e}")
                report["results"][name].append({
                    "N1": n1,
                    "error": str(e),
                })

    print("\n" + "=" * 80)

    artifacts_dir = Path(__file__).parent / "artifacts" / "stream_e"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    report_file = artifacts_dir / "scaling_ladder_report.json"
    report_file.write_text(json.dumps(report, indent=2))
    print(f"Report written to: {report_file}")

    return report


if __name__ == "__main__":
    run_scaling_ladder()
