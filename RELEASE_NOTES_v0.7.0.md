# Release v0.7.0 — Stream-3 Symbolic Checker Suite (C1 / C3 / C3b)

**Date:** 2026-07-24
**Scope:** pre-G1 mathematical verification infrastructure only. No observational
data is touched; milestone gate G1 remains **closed** (`pipeline/gate.py`
unchanged). Nothing in this release is a physical or empirical claim.

---

## What this is

Deterministic, exact-arithmetic checkers for three `K3_CRITERIA.md` criteria on
order-3 Apéry-like Picard–Fuchs operators. Every parameter traces to Gorodetsky
arXiv:2102.11839v2 (in `refs/`, checksum-verified); no sequence values or
constants come from model recall.

- **C1** — inverse mirror-map integrality (`check_C1_mirror_integrality.py`),
  exact Frobenius dual-number method.
- **C3** — symmetric-square generating-function identity between an order-3
  operator and an exhibited elliptic (Zagier) order-2 (`check_C3_sym2.py`).
- **C3b** — the explicit Shioda–Inose change-of-variable map F and its period
  correspondence (`check_C3b_moduli_map.py`).
- 46 golden/determinism tests (good + bad control per checker), all passing;
  machine-generated status matrix `docs/CRITERION_STATUS.md`
  (`scripts/render_criterion_status.py`).

## Result (Tier B — mathematics; no physical claim)

| Candidate | C1 | C3 | C3b |
|---|---|---|---|
| γ, α, δ, η (sporadic AZ) | PASS(40) | PASS(40) | PASS(40) |
| s7, s10, s18 (Cooper, d≠0) | PASS(40) | FAIL | FAIL |

Cooper s7/s10/s18 are genuine maximal-unipotent-monodromy period operators
(C1 passes) but are **not** symmetric squares of, nor Shioda–Inose-mapped to, any
elliptic order-2 operator in the tested family (C3/C3b fail). This is a recorded
negative result: any statement that s7/s10 are Sym²/Shioda–Inose K3 partners of an
elliptic family is unsupported by these checks.

## Data-integrity fix (WP-0)

`refs/sporadic_recurrences.json` v1.4 (`FROZEN`, consumed by zero code) had a
non-integral order-3 entry. It is **left intact for audit**; a Sym²-verified
correction is added in `refs/sporadic_recurrences_v2.json` with a documented,
still-open term-confirmation item flagged NEEDS-HUMAN
(`refs/RECURRENCE_CORRECTION_order3.md`).

## Governance

- Supersedes two non-executable directives (the "D-3 empirical rerun" and "V5 GPU"
  briefs) that referenced certificates, Lean output, and galaxy catalogs that do
  not exist in this repo, and asserted a G1 that is closed — see
  `CORRECTION_NETRUNNER_FABRICATION.md`.
- All artifacts carry `Reviewed-by: pending T0`. Review briefs:
  `briefs/STREAM3_CHECKER_SUITE_REVIEW.md` (Deep Think / T0s),
  `briefs/STREAM_ALIGNMENT_C3_C3b.md` (Streams 1 & 2).
- `scripts/check_tier_language.py`: 0 violations. `pytest pipeline/tests/
  checkers/tests/`: 137 passed.

## Remaining

WP-3 (C2 Kodaira fibers) is blocked on a `TBD-AT-FREEZE` constraint in
`K3_CRITERIA.md` C2 that requires a T0 ruling.

---

`Generated-by: Claude Opus 4.8 (T1) | Verified-by: 137 passing tests, tier-language CI clean, Gorodetsky arXiv:2102.11839 | Reviewed-by: pending T0`
