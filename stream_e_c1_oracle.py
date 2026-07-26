#!/usr/bin/env python3
"""Stream E: C1 Oracle CLI — exact-parity wrapper for mirror-map integrality checks.

This is a thin CLI wrapper around checkers/check_C1_mirror_integrality.py,
providing batch and single-check modes for Stream E task cards E1–E6.

Maintains bit-exact parity with the Python reference implementation.
Output: JSON certificates to stdout (one per line for batch mode).
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from checkers.check_C1_mirror_integrality import verify_c1, ORDER3_AZ_COOPER


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Stream E C1 Oracle: batch and single-check modes for mirror-map integrality"
    )
    ap.add_argument(
        "--order3",
        help="AZ/Cooper name or comma-separated (a,b,c,d) tuple",
    )
    ap.add_argument("--N1", type=int, default=50, help="Integrality order bound")
    ap.add_argument(
        "--batch",
        action="store_true",
        help="Batch mode: read (name or a,b,c,d) from stdin, one per line",
    )
    ap.add_argument(
        "--output",
        help="Write JSON certificates to file (batch mode only)",
    )
    args = ap.parse_args()

    if args.batch:
        certs = []
        for line in sys.stdin:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                if line in ORDER3_AZ_COOPER:
                    order3 = ORDER3_AZ_COOPER[line]
                else:
                    parts = [int(x.strip()) for x in line.split(",")]
                    if len(parts) != 4:
                        print(f"ERROR: invalid tuple {line}", file=sys.stderr)
                        return 1
                    order3 = tuple(parts)
                cert = verify_c1(order3, N1=args.N1)
                certs.append(cert)
                print(json.dumps(cert), flush=True)
            except Exception as e:
                print(f"ERROR: {line}: {e}", file=sys.stderr)
                return 1

        if args.output:
            Path(args.output).write_text(json.dumps(certs, indent=2))

        return 0

    if not args.order3:
        ap.print_help()
        return 1

    try:
        if args.order3 in ORDER3_AZ_COOPER:
            order3 = ORDER3_AZ_COOPER[args.order3]
        else:
            parts = [int(x.strip()) for x in args.order3.split(",")]
            if len(parts) != 4:
                print(f"ERROR: invalid tuple {args.order3}", file=sys.stderr)
                return 1
            order3 = tuple(parts)

        cert = verify_c1(order3, N1=args.N1)
        text = json.dumps(cert, indent=2)
        print(text)

        if args.output:
            Path(args.output).write_text(text)

        return 0 if cert["status"] == "PASS" else 1
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
