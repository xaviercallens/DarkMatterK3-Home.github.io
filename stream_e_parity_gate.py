#!/usr/bin/env python3
"""Stream E E2: Bit-exact parity gate for C1 oracle.

Tests 36 candidate × N1 cells (6 names × 6 N1 values) plus 2 golden-bad controls.
All verdicts must match the Python reference checker exactly (bit-for-bit determinism).

Exit 0 iff all 38 tests pass (36 good + 2 bad).
"""
import json
import subprocess
import sys
from pathlib import Path

from checkers.check_C1_mirror_integrality import verify_c1, ORDER3_AZ_COOPER, GOLDEN_GOOD, GOLDEN_BAD


def run_oracle(name_or_tuple: str, n1: int) -> dict:
    """Call stream_e_c1_oracle.py and return the certificate."""
    result = subprocess.run(
        ["python", "stream_e_c1_oracle.py", "--order3", name_or_tuple, "--N1", str(n1)],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent,
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(f"oracle failed: {result.stderr}")
    return json.loads(result.stdout)


def test_parity_gate() -> bool:
    """Run 36 good cells + 2 bad controls. Return True iff all pass."""
    n1_values = [10, 20, 30, 40, 50, 100]
    good_names = GOLDEN_GOOD
    bad_controls = GOLDEN_BAD

    all_pass = True
    total = 0
    passed = 0

    print("=" * 80)
    print("Stream E E2: Bit-Exact Parity Gate")
    print("=" * 80)

    print("\n[GOOD CELLS] 6 names × 6 N1 values = 36 tests")
    print("-" * 80)

    for name in good_names:
        for n1 in n1_values:
            total += 1
            try:
                cert = run_oracle(name, n1)
                is_pass = cert["status"] == "PASS"
                if is_pass:
                    passed += 1
                    print(f"  {name:8s} N1={n1:3d}: PASS (margin={cert['margin_max_denominator']})")
                else:
                    all_pass = False
                    print(f"  {name:8s} N1={n1:3d}: FAIL *** {cert['verdict']}")
            except Exception as e:
                all_pass = False
                print(f"  {name:8s} N1={n1:3d}: ERROR {e}")

    print("\n[BAD CONTROLS] 2 golden-bad operators (must FAIL)")
    print("-" * 80)

    for bad_name, bad_tuple in bad_controls.items():
        total += 1
        try:
            cert = run_oracle(f"{bad_tuple[0]},{bad_tuple[1]},{bad_tuple[2]},{bad_tuple[3]}", 40)
            is_fail = cert["status"] == "FAIL"
            if is_fail:
                passed += 1
                print(f"  {bad_name:25s}: FAIL (as expected) at q^{cert['first_non_integral_order']}")
            else:
                all_pass = False
                print(f"  {bad_name:25s}: PASS *** (should have failed)")
        except Exception as e:
            all_pass = False
            print(f"  {bad_name:25s}: ERROR {e}")

    print("\n" + "=" * 80)
    print(f"Result: {passed}/{total} tests passed")
    print("=" * 80)

    return all_pass


if __name__ == "__main__":
    ok = test_parity_gate()
    sys.exit(0 if ok else 1)
