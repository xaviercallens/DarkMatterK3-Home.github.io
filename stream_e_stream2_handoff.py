#!/usr/bin/env python3
"""Stream E E6: Stream 2 handoff package — fast exact C1 oracle batch mode.

Provides Stream 2 with:
1. Fast exact C1 oracle in batch mode (shardable by candidate)
2. Certificate emission with determinism guarantees
3. High-order stress capability (N1 up to 300+)
4. Ranking grid support for candidate scoring

Usage:
  python stream_e_stream2_handoff.py --batch-file candidates.txt --N1 200 --output results.json
  python stream_e_stream2_handoff.py --rank-grid s7,s10 --N1 100 --output ranking.json

Output: JSON certificates with bit-exact determinism hashes for evidence.
"""
import json
import argparse
import sys
from pathlib import Path
from typing import Optional

from stream_e_c1_oracle import main as oracle_main
from stream_e_boinc_schema import create_work_unit_batch, execute_work_unit_batch
from checkers.check_C1_mirror_integrality import verify_c1, ORDER3_AZ_COOPER


def batch_oracle(batch_file: Path, n1: int, output_file: Optional[Path] = None) -> dict:
    """Execute batch C1 oracle from input file.
    
    Input file format: one candidate per line (name or a,b,c,d tuple).
    Output: JSON with array of certificates.
    """
    candidates = []
    with open(batch_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                candidates.append(line)
    
    print(f"[BATCH ORACLE] Processing {len(candidates)} candidates at N1={n1}")
    
    work_units = create_work_unit_batch(candidates, [n1])
    results = execute_work_unit_batch(work_units)
    
    # Extract certificates from work unit results
    certificates = []
    for wu_dict in results["work_units"]:
        if "result" in wu_dict and wu_dict["result"]:
            certificates.append(wu_dict["result"])
    
    output = {
        "handoff": "Stream E → Stream 2",
        "oracle": "C1 mirror-map integrality",
        "batch_size": len(candidates),
        "N1": n1,
        "certificates": certificates,
        "summary": {
            "total": len(certificates),
            "passed": sum(1 for c in certificates if c["status"] == "PASS"),
            "failed": sum(1 for c in certificates if c["status"] == "FAIL"),
        },
    }
    
    if output_file:
        output_file.write_text(json.dumps(output, indent=2))
        print(f"[OUTPUT] Written to {output_file}")
    
    return output


def ranking_grid(candidates: list[str], n1_values: list[int], output_file: Optional[Path] = None) -> dict:
    """Generate ranking grid: candidate × N1 matrix with verdicts.
    
    Useful for Stream 2 to assess candidate robustness across N1 scales.
    """
    print(f"[RANKING GRID] {len(candidates)} candidates × {len(n1_values)} N1 values")
    
    grid = {
        "handoff": "Stream E → Stream 2",
        "oracle": "C1 ranking grid",
        "candidates": candidates,
        "n1_values": n1_values,
        "matrix": {},
    }
    
    for candidate in candidates:
        grid["matrix"][candidate] = {}
        work_units = create_work_unit_batch([candidate], n1_values)
        
        for wu in work_units:
            wu.compute()
            if wu.status == "completed":
                grid["matrix"][candidate][wu.n1] = {
                    "verdict": wu.result["verdict"],
                    "margin": wu.result["margin_max_denominator"],
                    "hash": wu.validator_hash,
                }
            else:
                grid["matrix"][candidate][wu.n1] = {
                    "error": wu.error,
                }
    
    if output_file:
        output_file.write_text(json.dumps(grid, indent=2))
        print(f"[OUTPUT] Written to {output_file}")
    
    return grid


def high_order_stress(candidate: str, n1_max: int = 500, output_file: Optional[Path] = None) -> dict:
    """High-order stress test: push N1 to the limit for a single candidate.
    
    Useful for Stream 2 to assess how far integrality holds.
    """
    print(f"[HIGH-ORDER STRESS] {candidate} up to N1={n1_max}")
    
    # Binary search for the breaking point
    n1_values = [50, 100, 150, 200, 250, 300, 400, 500]
    results = []
    
    for n1 in n1_values:
        try:
            if candidate in ORDER3_AZ_COOPER:
                order3 = ORDER3_AZ_COOPER[candidate]
            else:
                parts = [int(x.strip()) for x in candidate.split(",")]
                order3 = tuple(parts)
            
            cert = verify_c1(order3, N1=n1)
            results.append({
                "N1": n1,
                "verdict": cert["verdict"],
                "margin": cert["margin_max_denominator"],
                "first_bad": cert["first_non_integral_order"],
            })
            print(f"  N1={n1:3d}: {cert['verdict']:20s}")
        except Exception as e:
            print(f"  N1={n1:3d}: ERROR {e}")
            break
    
    output = {
        "handoff": "Stream E → Stream 2",
        "oracle": "C1 high-order stress",
        "candidate": candidate,
        "results": results,
    }
    
    if output_file:
        output_file.write_text(json.dumps(output, indent=2))
        print(f"[OUTPUT] Written to {output_file}")
    
    return output


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Stream E E6: Stream 2 handoff — fast exact C1 oracle batch mode"
    )
    
    # Batch oracle mode
    ap.add_argument("--batch-file", type=Path, help="Batch input file (one candidate per line)")
    
    # Ranking grid mode
    ap.add_argument("--rank-grid", help="Comma-separated candidates for ranking grid")
    ap.add_argument("--rank-n1", default="50,100,150,200", help="Comma-separated N1 values for ranking")
    
    # High-order stress mode
    ap.add_argument("--stress", help="Single candidate for high-order stress test")
    ap.add_argument("--stress-max", type=int, default=500, help="Max N1 for stress test")
    
    # Common options
    ap.add_argument("--N1", type=int, default=200, help="Integrality order bound (batch mode)")
    ap.add_argument("--output", type=Path, help="Output JSON file")
    
    args = ap.parse_args()
    
    if args.batch_file:
        batch_oracle(args.batch_file, args.N1, args.output)
        return 0
    
    if args.rank_grid:
        candidates = args.rank_grid.split(",")
        n1_values = [int(x.strip()) for x in args.rank_n1.split(",")]
        ranking_grid(candidates, n1_values, args.output)
        return 0
    
    if args.stress:
        high_order_stress(args.stress, args.stress_max, args.output)
        return 0
    
    ap.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
