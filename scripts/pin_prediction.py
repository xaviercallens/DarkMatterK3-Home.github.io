#!/usr/bin/env python3
"""Generate PINNED: and DERIVED: headers for PREDICTION.md (WP-B, Haiku).

Uses the exact stripping/hashing logic from pipeline/gate.py. Modes:
  --pin      Generate PINNED: header for PREDICTION.md (rules §2-§5)
  --derive   Generate DERIVED: header for §6 section only
  --both     Generate both (in sequence: PINNED, then DERIVED)
  --check    Dry-run: print hashes without writing (default if no mode given)
  --force    Overwrite existing headers (default: refuse if valid header exists)

Exit codes:
  0 = success (or --check reported hashes)
  1 = header exists and valid (use --force to overwrite)
  2 = file not found or unreadable
  3 = parse error
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path

# Import the gate logic so we don't duplicate it
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from pipeline.gate import (
    PREDICTION_PATH,
    _PIN_RE,
    _DERIVED_RE,
    _SECTION6_RE,
    _strip_header_lines,
    verify_pin_hash,
    verify_derived_hash,
)


def generate_pin_hash(file_path: Path) -> str:
    """Compute sha256 of the file body (stripped of both PINNED: and DERIVED: lines)."""
    if not file_path.exists():
        return None
    text = file_path.read_text(encoding="utf-8")
    body = _strip_header_lines(text)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def generate_derived_hash(file_path: Path) -> str:
    """Compute sha256 of the §6 section only."""
    if not file_path.exists():
        return None
    text = file_path.read_text(encoding="utf-8")
    m = _SECTION6_RE.search(text)
    if not m:
        return None
    section6 = m.group(0)
    return hashlib.sha256(section6.encode("utf-8")).hexdigest()


def add_pin_header(file_path: Path, force: bool = False) -> bool:
    """Add PINNED: header to file. Returns True on success; False if header exists and not --force."""
    if not file_path.exists():
        print(f"Error: {file_path} not found", file=sys.stderr)
        return False

    text = file_path.read_text(encoding="utf-8")

    # Check if valid pin already exists
    if _PIN_RE.search(text) and verify_pin_hash() and not force:
        print(f"Error: {file_path} already has a valid PINNED: header. Use --force to overwrite.", file=sys.stderr)
        return False

    # Strip existing headers and recompute
    body = _strip_header_lines(text)
    pin_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()

    # Check if DERIVED: already exists and preserve it
    derived_match = _DERIVED_RE.search(text)
    derived_header = ""
    if derived_match:
        derived_header = text[derived_match.start():derived_match.end()] + "\n"

    # Remove old headers and write new ones
    text_no_headers = _strip_header_lines(text)
    new_text = f"PINNED: {pin_hash}\n{derived_header}{text_no_headers}"

    file_path.write_text(new_text, encoding="utf-8")
    print(f"Added PINNED: {pin_hash}")
    return True


def add_derived_header(file_path: Path, force: bool = False) -> bool:
    """Add DERIVED: header to file. Returns True on success."""
    if not file_path.exists():
        print(f"Error: {file_path} not found", file=sys.stderr)
        return False

    text = file_path.read_text(encoding="utf-8")

    # Check if valid derived pin already exists
    if _DERIVED_RE.search(text) and verify_derived_hash() and not force:
        print(f"Error: {file_path} already has a valid DERIVED: header. Use --force to overwrite.", file=sys.stderr)
        return False

    # Extract §6
    m = _SECTION6_RE.search(text)
    if not m:
        print(f"Error: No §6 section found in {file_path}", file=sys.stderr)
        return False

    section6 = m.group(0)
    derived_hash = hashlib.sha256(section6.encode("utf-8")).hexdigest()

    # Remove old DERIVED: header if present
    text_no_derived = _DERIVED_RE.sub("", text).lstrip("\n")

    # Extract PINNED: line to preserve it
    pin_match = _PIN_RE.search(text_no_derived)
    if pin_match:
        pin_line = text_no_derived[pin_match.start():pin_match.end()] + "\n"
        body = text_no_derived[pin_match.end():].lstrip("\n")
        new_text = f"{pin_line}DERIVED: {derived_hash}\n{body}"
    else:
        new_text = f"DERIVED: {derived_hash}\n{text_no_derived}"

    file_path.write_text(new_text, encoding="utf-8")
    print(f"Added DERIVED: {derived_hash}")
    return True


def check_hashes(file_path: Path) -> int:
    """Print current and computed hashes without writing. Returns 0 on success, 2 on error."""
    if not file_path.exists():
        print(f"Error: {file_path} not found", file=sys.stderr)
        return 2

    text = file_path.read_text(encoding="utf-8")

    # PINNED hash
    pin_match = _PIN_RE.search(text)
    computed_pin = generate_pin_hash(file_path)
    if pin_match:
        existing_pin = pin_match.group(1)
        print(f"PINNED (existing): {existing_pin}")
        print(f"PINNED (computed): {computed_pin}")
        print(f"PINNED matches:    {existing_pin.lower() == computed_pin.lower()}")
    else:
        print(f"PINNED (existing): [none]")
        print(f"PINNED (computed): {computed_pin}")

    print()

    # DERIVED hash
    derived_match = _DERIVED_RE.search(text)
    computed_derived = generate_derived_hash(file_path)
    if derived_match:
        existing_derived = derived_match.group(1)
        print(f"DERIVED (existing): {existing_derived}")
        print(f"DERIVED (computed): {computed_derived}")
        if computed_derived:
            print(f"DERIVED matches:   {existing_derived.lower() == computed_derived.lower()}")
    else:
        print(f"DERIVED (existing): [none]")
        print(f"DERIVED (computed): {computed_derived}")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--pin",
        action="store_true",
        help="Generate PINNED: header for rules (§2-§5)"
    )
    parser.add_argument(
        "--derive",
        action="store_true",
        help="Generate DERIVED: header for §6 section"
    )
    parser.add_argument(
        "--both",
        action="store_true",
        help="Generate both PINNED: and DERIVED: headers"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Dry-run: print hashes without writing (default if no mode)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing valid headers"
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=PREDICTION_PATH,
        help=f"Target file (default: {PREDICTION_PATH})"
    )

    args = parser.parse_args()

    # Default to --check if no mode specified
    if not (args.pin or args.derive or args.both):
        args.check = True

    if args.check:
        return check_hashes(args.file)

    success = True
    if args.both or args.pin:
        success = add_pin_header(args.file, force=args.force) and success
    if args.both or args.derive:
        success = add_derived_header(args.file, force=args.force) and success

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
