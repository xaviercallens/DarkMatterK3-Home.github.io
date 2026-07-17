#!/usr/bin/env python3
"""CI checker for epistemic-guardrails Finding F-A (EXECUTION_PLAN.md WP P0-C).

Rule: a claim may not appear in an abstract/summary section at a stronger
tier than its own section states. Enforced mechanically as a blunt grep,
by design (see skill: this is the "honest, checkable version", not a full
tier-inference engine):

1. The phrases "Rigidly locks", "Rigidity Theorem", "zero continuous" are
   forbidden unconditionally in abstract/summary blocks.
2. A forbidden Tier-C verb (predicts, establishes, shows, implies, locks,
   governs, determines, demonstrates, proves) used in an abstract/summary
   sentence with no conjecture marker ("we conjecture", "would", "if the
   matching exists") in the same sentence is flagged.

Usage:
    python3 scripts/check_tier_language.py            # scan repo *.md files
    python3 scripts/check_tier_language.py --selftest  # unit tests, no repo scan
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN_PHRASES = ["rigidly locks", "rigidity theorem", "zero continuous"]
FORBIDDEN_VERBS = ["predicts", "establishes", "shows", "implies", "locks",
                   "governs", "determines", "demonstrates", "proves"]
CONJECTURE_MARKERS = ["we conjecture", "would", "if the matching exists"]

SECTION_HEADING_RE = re.compile(r"^#{1,6}\s+(.*)$", re.MULTILINE)
ABSTRACT_HEADINGS = {"abstract", "summary", "overview"}


def extract_abstract_blocks(text: str) -> list:
    """Return [(section_label, block_text), ...] for the preamble (before the
    first heading) and any heading matching ABSTRACT_HEADINGS."""
    headings = list(SECTION_HEADING_RE.finditer(text))
    blocks = []

    preamble_end = headings[0].start() if headings else len(text)
    if text[:preamble_end].strip():
        blocks.append(("<preamble>", text[:preamble_end]))

    for i, h in enumerate(headings):
        label = h.group(1).strip().lower()
        # Strip markdown emphasis/punctuation for matching ("## Abstract" etc.)
        label_clean = re.sub(r"[^a-z ]", "", label).strip()
        if label_clean in ABSTRACT_HEADINGS:
            start = h.end()
            end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
            blocks.append((h.group(1).strip(), text[start:end]))
    return blocks


def split_sentences(block: str) -> list:
    # Deliberately simple: this is a blunt lint, not an NLP tool.
    flat = " ".join(block.split())
    return re.split(r"(?<=[.!?])\s+", flat)


def check_block(label: str, block: str) -> list:
    violations = []
    lower = block.lower()
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower:
            violations.append(f"[{label}] forbidden phrase: '{phrase}'")

    for sentence in split_sentences(block):
        s_lower = sentence.lower()
        has_marker = any(m in s_lower for m in CONJECTURE_MARKERS)
        if has_marker:
            continue
        for verb in FORBIDDEN_VERBS:
            if re.search(rf"\b{verb}\b", s_lower):
                violations.append(
                    f"[{label}] forbidden verb '{verb}' with no conjecture "
                    f"marker: \"{sentence.strip()}\""
                )
    return violations


def check_text(text: str) -> list:
    violations = []
    for label, block in extract_abstract_blocks(text):
        violations.extend(check_block(label, block))
    return violations


def iter_markdown_files():
    """Scope: repo-root markdown only (non-recursive).

    This is where the physics-program documents live (VISION.md,
    PREDICTION.md, EXECUTION_PLAN.md, K3_CRITERIA.md, ASSUMPTIONS.md,
    README.md, release notes, ...). Subdirectories like EuclidClusterViz/
    or frontend/ hold unrelated engineering docs (UI guides, deployment
    notes) that were never in scope for tier-language review and would
    otherwise drown real flags in noise.
    """
    for path in sorted(REPO_ROOT.glob("*.md")):
        yield path


def run_selftest() -> int:
    bad = (
        "# README\n\n"
        "## Abstract\n"
        "This structure rigidly locks the bulk vacuum to the brane EFT, "
        "and predicts a specific self-interaction cross-section.\n"
    )
    good = (
        "# README\n\n"
        "## Abstract\n"
        "We conjecture that this structure would relate the bulk vacuum to "
        "the brane EFT if the matching exists; no such matching has been "
        "constructed yet.\n"
    )
    unrelated = (
        "# README\n\n"
        "## Setup\n"
        "This installer rigidly locks the config file permissions to 600.\n"
    )

    bad_violations = check_text(bad)
    assert any("rigidly locks" in v for v in bad_violations), bad_violations
    assert any("predicts" in v for v in bad_violations), bad_violations

    good_violations = check_text(good)
    assert good_violations == [], good_violations

    # A forbidden phrase outside any abstract/summary/overview section (and
    # outside the preamble) must not be flagged — scope is abstracts only.
    unrelated_violations = check_text(unrelated)
    assert unrelated_violations == [], unrelated_violations

    print("check_tier_language.py self-test: PASS (3/3 control cases)")
    return 0


def run_check() -> int:
    total_violations = []
    for path in iter_markdown_files():
        text = path.read_text(encoding="utf-8")
        for v in check_text(text):
            total_violations.append(f"{path.relative_to(REPO_ROOT)}: {v}")

    if total_violations:
        print("BLOCKED by check_tier_language (epistemic-guardrails Finding F-A):")
        for v in total_violations:
            print(f"  {v}")
        return 1
    print(f"check_tier_language.py: OK (0 violations)")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(run_selftest())
    sys.exit(run_check())
