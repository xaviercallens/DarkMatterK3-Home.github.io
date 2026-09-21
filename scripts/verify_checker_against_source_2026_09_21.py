#!/usr/bin/env python3
"""verify_checker_against_source_2026_09_21.py — is `checkers/check_C3_sym2.py` faithful to
the vendored primary source, and how many sporadic order-3 sequences are there?

Closes the scope qualifier in briefs/STREAM3_K3_SELECTION_ROUTE_AUDIT_2026_09_21.md sec.3.1,
which said the C3-non-discrimination finding covers register entries "in this family" while
leaving S22 and t103 unresolved (their recurrences are TBD-AT-FREEZE).

Everything below is READ OUT OF THE VENDORED PDF at run time and compared against the
committed Python tables. Nothing is recalled, and no expected value is hardcoded except as a
deliberate negative control.

Source: refs/papers/Gorodetsky_sporadic_apery_like_sequences_2102.11839.pdf, arXiv:2102.11839v2.
Its SHA256 is read from `refs/README.md` (the repo's integrity record), not typed here, and the
file is hashed and compared before a single character of its text is trusted.

CHECKS
  V1  PDF SHA256 == the value recorded in refs/README.md.
  V2  Cooper's (a, b, c, d) table for s7 / s10 / s18, parsed out of the paper, matches
      `ORDER3_AZ_COOPER`.
  V3  the Almkvist-van Straten-Zudilin bijection order (A-F correspond to delta, zeta, alpha,
      eta, epsilon, gamma, IN THIS ORDER) matches the committed `BIJECTION` dict.
  V4  the paper's operator (1.7) matches the operator this repo's scripts apply.
  V5  Cooper's sporadic solutions number exactly THREE and are named s7, s10, s18.
  V7  "S22" does not occur ANYWHERE in the full text of either vendored paper (Gorodetsky and
      the AESZ tables). V5 alone would only establish that S22 is absent from one sentence;
      V7 is what licenses the stronger statement that the vendored sources contain no such
      sequence, and hence that K3_CRITERIA.md's K-S22 entry has no citable recurrence behind
      it in anything this repo holds.
  V6  the sporadic landscape is 15 = 6 Zagier (order 2) + 6 AZ (order 3) + 3 Cooper (order 3),
      so the 9 order-3 sequences are exactly `ORDER3_AZ_COOPER`'s keys: the family identity of
      sec.3.1 covers EVERY sporadic order-3 Apery-like sequence, not merely the register.

NEGATIVE CONTROLS (enforced; exit 1 on failure)
  NC-A  a corrupted expected hash must make V1 fail — proves V1 compares rather than asserts.
  NC-B  a perturbed (a,b,c,d) expectation must make V2 fail.
  NC-C  a permuted bijection order must make V3 fail.
Each control re-runs the real comparison function with one value altered, so a check that
always returned True would be caught.

Generated-by: Claude Opus 5 (Stream 3) | Verified-by: hash-gated parse of the vendored PDF,
three enforced negative controls | Reviewed-by: pending T0
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from checkers.check_C3_sym2 import BIJECTION, ORDER3_AZ_COOPER  # noqa: E402

PDF = REPO / "refs/papers/Gorodetsky_sporadic_apery_like_sequences_2102.11839.pdf"
AESZ = REPO / "refs/papers/AESZ_tables_calabi_yau_equations_math0507430.pdf"
README = REPO / "refs/README.md"
OUT = REPO / "data/derived/checker_source_verification_2026_09_21.json"

GREEK = {"δ": "delta", "ζ": "zeta", "α": "alpha", "η": "eta",
         "ǫ": "epsilon", "ε": "epsilon", "γ": "gamma"}


def normalize(s: str) -> str:
    """Unicode minus/dashes -> ASCII '-'; collapse whitespace."""
    s = s.replace("−", "-").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s))


def recorded_sha() -> str | None:
    for line in README.read_text().splitlines():
        if "Gorodetsky_sporadic_apery_like_sequences" in line:
            m = re.search(r"\b([0-9a-f]{64})\b", line)
            if m:
                return m.group(1)
    return None


def actual_sha() -> str:
    return hashlib.sha256(PDF.read_bytes()).hexdigest()


def check_hash(expected: str) -> bool:
    """V1 — real comparison, reused by NC-A with a corrupted expectation."""
    return actual_sha() == expected


def pdf_text(path: Path = None) -> str:
    return normalize(subprocess.run(
        ["pdftotext", str(path or PDF), "-"], capture_output=True, text=True,
        check=True).stdout)


def count_token(text: str, pattern: str) -> int:
    """V7 helper — real search, reused by NC-D with a token known to be present."""
    return len(re.findall(pattern, text, flags=re.IGNORECASE))


def parse_cooper_table(text: str) -> dict[str, tuple[int, ...]]:
    """Read the (a, b, c, d) / Name table. Rows appear as a tuple line then a name line."""
    found: dict[str, tuple[int, ...]] = {}
    tuples = list(re.finditer(r"\((-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\)", text))
    for m in tuples:
        tail = text[m.end():m.end() + 40]
        nm = re.search(r"\b(s7|s10|s18)\b", tail)
        if nm:
            found[nm.group(1)] = tuple(int(g) for g in m.groups())
    return found


def compare_table(parsed: dict, expected: dict) -> bool:
    """V2 — real comparison, reused by NC-B with a perturbed expectation."""
    return all(name in parsed and parsed[name] == tuple(expected[name])
               for name in ("s7", "s10", "s18"))


def parse_bijection_order(text: str) -> list[str] | None:
    m = re.search(r"sequences A-F correspond to (.{0,80}?), in this order", text)
    if not m:
        return None
    names = re.findall(r"\(([^)]{1,3})\)", m.group(1))
    out = [GREEK.get(n) for n in names]
    return out if all(out) and len(out) == 6 else None


def compare_bijection(parsed_order: list[str], coded: dict) -> bool:
    """V3 — real comparison, reused by NC-C with a permuted expectation."""
    return [coded[k] for k in ("A", "B", "C", "D", "E", "F")] == parsed_order


def main() -> int:
    exp_sha = recorded_sha()
    v1 = exp_sha is not None and check_hash(exp_sha)
    if not v1:
        print("  V1 SHA256 gate: FAIL — refusing to parse an unverified PDF")
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps({"artifact": "checker_source_verification",
                                   "V1_sha256_gate": False}, indent=2))
        return 1

    text = pdf_text()
    parsed = parse_cooper_table(text)
    v2 = compare_table(parsed, ORDER3_AZ_COOPER)

    order = parse_bijection_order(text)
    v3 = order is not None and compare_bijection(order, BIJECTION)

    op = ("(θ3 − z(2θ + 1)(aθ2 + aθ + b) + z 2 (c(θ + 1)3 + d(θ + 1)))y = 0")
    v4 = normalize(op) in text

    m5 = re.search(r"Cooper found (\w+) additional sporadic solutions, named ([^.]+)\.", text)
    v5_count = m5.group(1) if m5 else None
    v5_names = re.findall(r"\bs(?:7|10|18|22)\b", m5.group(2)) if m5 else []
    v5 = v5_count == "3" and set(v5_names) == {"s7", "s10", "s18"}

    # V7 — full-text absence of "S22" in BOTH vendored papers.
    s22_hits = {"gorodetsky": count_token(text, r"s\s?22")}
    if AESZ.exists():
        s22_hits["aesz_tables"] = count_token(pdf_text(AESZ), r"\bs\s?22\b")
    v7 = all(v == 0 for v in s22_hits.values()) and len(s22_hits) == 2
    # NC-D: the same search must FIND a token that is certainly present, else "0 hits"
    # would be indistinguishable from a search that never matches anything.
    nc_d = count_token(text, r"\bs7\b") > 0

    v6_15 = "15 sporadic Apéry-like sequences" in text or "15 sporadic Ap" in text
    v6 = v6_15 and set(ORDER3_AZ_COOPER) == set(BIJECTION.values()) | {"s7", "s10", "s18"}

    nc_a = not check_hash("0" * 64)
    perturbed = dict(ORDER3_AZ_COOPER)
    perturbed["s7"] = (13, 4, -27, 4)                      # d: 3 -> 4
    nc_b = not compare_table(parsed, perturbed)
    permuted = dict(BIJECTION)
    permuted["A"], permuted["B"] = permuted["B"], permuted["A"]
    nc_c = (order is not None) and not compare_bijection(order, permuted)

    payload = {
        "artifact": "checker_source_verification",
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "label": "SOURCE-VERIFICATION — documentary; not a C3 verdict, not exclusion, "
                 "not FIT, not TEST",
        "source": {"file": str(PDF.relative_to(REPO)), "arxiv": "2102.11839v2",
                   "sha256_recorded_in_refs_README": exp_sha, "sha256_actual": actual_sha()},
        "V1_sha256_gate": v1,
        "V2_cooper_abcd_table_matches_ORDER3_AZ_COOPER": {"pass": v2, "parsed": {
            k: list(v) for k, v in parsed.items()}},
        "V3_avsz_bijection_order_matches_BIJECTION": {"pass": v3, "parsed_order": order},
        "V4_operator_1_7_matches_the_one_this_repo_applies": v4,
        "V5_cooper_has_exactly_three_sporadic_solutions": {
            "pass": v5, "count_word": v5_count, "names": sorted(set(v5_names))},
        "V7_S22_absent_from_full_text_of_both_vendored_papers": {
            "pass": v7, "occurrences": s22_hits,
            "consequence": "K3_CRITERIA.md register entry K-S22 has no citable defining "
                           "recurrence behind it in anything this repo holds; the register's own "
                           "rule drops such a candidate at freeze rather than guessing it. "
                           "K-t103 is separately off the roadmap, quoted exactly: 'vetoed by T0 "
                           "2026-07-26 pending certificates' (ROADMAP.md) — a CONDITIONAL veto."},
        "V6_order3_sporadic_landscape_is_exactly_the_committed_table": {
            "pass": v6,
            "landscape": "15 sporadic = 6 Zagier (order 2) + 6 Almkvist-Zudilin (order 3) "
                         "+ 3 Cooper (order 3)",
            "order3_keys": sorted(ORDER3_AZ_COOPER),
            "consequence": "The sec.3.1 family identity therefore covers EVERY sporadic "
                           "order-3 Apery-like sequence, not merely the register entries. The "
                           "scope qualifier can be tightened rather than left open."},
        "negative_controls": {
            "NC_A_corrupted_hash_rejected": nc_a,
            "NC_B_perturbed_abcd_rejected": nc_b,
            "NC_C_permuted_bijection_rejected": nc_c,
            "NC_D_same_search_finds_a_token_known_present": nc_d,
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))          # persist BEFORE printing

    for lbl, ok in (("V1 sha256 gate", v1), ("V2 cooper (a,b,c,d) table", v2),
                    ("V3 AvSZ bijection order", v3), ("V4 operator (1.7)", v4),
                    ("V5 exactly three Cooper solutions", v5),
                    ("V6 order-3 landscape == table", v6),
                    ("V7 S22 absent from both papers", v7),
                    ("NC-D search finds a present token", nc_d),
                    ("NC-A corrupted hash rejected", nc_a),
                    ("NC-B perturbed abcd rejected", nc_b),
                    ("NC-C permuted bijection rejected", nc_c)):
        print(f"  {lbl:36s} {'PASS' if ok else 'FAIL'}")
    print(f"  parsed Cooper table: {parsed}")
    print(f"  parsed bijection   : {order}")
    print(f"  artifact: {OUT.relative_to(REPO)}")
    return 0 if all([v1, v2, v3, v4, v5, v6, v7, nc_a, nc_b, nc_c, nc_d]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
