# Quick-Start Restart: Next Session (After V5.1 Pivot)

**For Claude sessions continuing the Cooper s₁₀ hypothesis program**

---

## What Happened Last Session (2026-07-14)

1. **Deep review found fabricated constants** in V5 Phase 1
   - Guideline's claimed OEIS A183204 ≠ true sequence (verified vs oeis.org)
   - Series evaluation was divergent (λ=25.87 < true λ=27)
   - Δ metric was k=0 (DC) normalization offset only
   - **All Phase 1 results are void** (archived to `archives/void_20260714_s7_fabricated/`)

2. **Strategic pivot to Cooper s₁₀** (OEIS A005260, λ=16)
   - True sequence from verified recurrence (in-repo: `hypothesis_comparison_t103_cooper.py`)
   - New certified kernel: `cooper_s10_kernel.py` (7 self-tests passing)
   - New estimator: `v5_estimator_s10.py` (3 synthetic tests passing)
   - Provenance gate: `v5_provenance_gate.py` (blocks synthetic data, 3/3 tests)

3. **Commit completed** (hash: 1626285c)
   - Push to GitHub blocked by large venv files (expected; not critical)
   - Local commit on main branch is permanent

4. **Lessons documented** in `LESSONS_LEARNED.md`
   - P1: No constant without provenance
   - P2: Tests are scientific, not smoke
   - P3: Pre-register before unblind
   - P4: Sibling families as control

---

## Your First Task (This Session)

### ALWAYS DO THESE FIRST (5 minutes)

```bash
# Read the key documents (in this order)
1. V5_SCIENTIFIC_REVIEW.md (findings F1–F9, gate conditions G1–G5)
2. V5_RIGOROUS_THEORY_PLAN.md (work packages overview + dependency graph)
3. PIVOT_MEMO.md (why s₁₀, not s₇)
4. RELEASE_NOTES.md (what's new, what's deprecated)
5. LESSONS_LEARNED.md (institutional practices P1–P4)

# Check the certified kernel still works
python3 cooper_s10_kernel.py
python3 v5_estimator_s10.py
python3 v5_provenance_gate.py

# Verify git state
git log --oneline -5
git status
```

### Then Pick Your Work Package

Based on the theory plan (`V5_RIGOROUS_THEORY_PLAN.md`), the next three work
packages are **independent and can be done in parallel**:

| WP | Title | Tier | Effort | Priority |
|----|-------|------|--------|----------|
| **WP-B1** | Chameleon z(ρ) derivation | Sonnet | 3h | HIGH (feeds B2, C3) |
| **WP-A3-t103** | t₁₀₃ control kernel | Haiku | 1.5h | MEDIUM (for discrimination test) |
| **WP-C2-design** | Mock ensemble + null bank | Sonnet | 4h | HIGH (feeds C3, D1, D2) |

**Recommended order** (if doing one per session):
1. WP-B1 (Sonnet: chameleon derivation) — unlocks physical understanding
2. WP-C2 (Sonnet+Haiku: mocks) — unlocks statistical testing
3. WP-B3 (Sonnet+Haiku: identifiability harness) — the discrimination test
4. WP-A3-t103 (Haiku: t₁₀₃ kernel) — sibling family for model comparison
5. WP-C3 (Haiku: redshift tomography) — See-Saw test on real data

Or **if you're a Haiku session**, jump straight to:
- WP-A3-t103 (1.5h, self-contained)
- Then WP-C2's Haiku part (mocks) once the Sonnet part ships the design

---

## Key Files & Their Roles

| File | Purpose | Read? |
|------|---------|-------|
| `cooper_s10_kernel.py` | Certified s₁₀ kernel (primary) | Run tests only |
| `v5_estimator_s10.py` | Estimator (WP-B2, done) | Reference only |
| `v5_provenance_gate.py` | Provenance gate (WP-C1, done) | Reference only |
| `V5_SCIENTIFIC_REVIEW.md` | **READ FIRST** — findings + gates | YES |
| `V5_RIGOROUS_THEORY_PLAN.md` | **READ SECOND** — all WP specs | YES |
| `PIVOT_MEMO.md` | Why s₁₀ | YES |
| `RELEASE_NOTES.md` | This release summary | YES |
| `LESSONS_LEARNED.md` | Institutional practices P1–P4 | YES (reference) |
| `LL.md` | (old file, may have prior context) | Skip for now |
| `V5_PHASE1_HANDOFF.md` | DEPRECATED (marked) | Skip |
| `PHASE2_QUICKSTART.md` | DEPRECATED (marked) | Skip |

---

## Gate Conditions (What Unlocks Public Claims)

These must **all** pass before any public claim or publication:

| Gate | Criterion | WP to unlock |
|------|-----------|---|
| **G1** | No fabricated constants; all via recurrence/formula/fetched | Already satisfied (WP-A3 review) |
| **G2** | Real survey data only; provenance field on every record | Already satisfied (WP-C1) |
| **G3** | Δ_{s10} beats derivative-matched controls AND siblings (ΔAIC ≥ 10) | WP-B3 (identifiability) |
| **G4** | Tomography on data-minus-mock residuals | WP-C3 (redshift) |
| **G5** | Significance from empirical mock null (look-elsewhere) | WP-C2 (mocks) |

**You can run code BEFORE gates pass. You CANNOT publish before gates pass.**

---

## Institutional Practices (P1–P4)

These are **non-negotiable** for every session:

**P1 — No constant without provenance**
- Number enters code via: recurrence formula, closed-form computation, or
  fetched external authority (with URL/date logged)
- Hardcoding raw values from unverified sources = automatic code review rejection

**P2 — Tests are scientific, not smoke**
- "Code runs" is not a passing test
- Pass = code produces correct output on known inputs (sequences, null data, signal injections)

**P3 — Pre-register before unblinding**
- Freeze analysis choices (k-band, mock count, thresholds, bins, corrections)
  in git *before* looking at real data significance
- Deviations in `DEVIATIONS.md`

**P4 — Sibling families as control**
- Cooper hypothesis is testable *only if* s₁₀ beats s₇ (if rebuilt) and
  t₁₀₃ and derivative-matched kernels in model selection (ΔAIC ≥ 10)
- If they fit equally, the result is null (not a weakness)

---

## Immediate Check (Do This Now)

```python
# Quick verification script (run this to validate the setup)
import sys
sys.path.insert(0, '.')
from cooper_s10_kernel import cooper_s10_terms, cooper_s10_binomial

# Verify s10 ground truth
s10_exact = cooper_s10_terms(15)
s10_binom = [cooper_s10_binomial(n) for n in range(16)]

print("s10 verification:")
for n in range(16):
    match = "✓" if s10_exact[n] == s10_binom[n] else "✗"
    print(f"  n={n:2d}: {match}")

# Expected: all ✓
```

---

## Commit Message Template (For Your Session)

When you finish a work package, commit with a message like:

```
WP-<id>: <Title> — <Short Summary>

TASK: <what you implemented>
STATUS: [DONE | BLOCKED] <if blocked, why>
TESTS: <which tests pass>
NEXT: <what unblocks the next WP>

Adhered to:
  P1 (no fabricated constants) ✓
  P2 (scientific tests, not smoke) ✓
  P3 (pre-registered before unblind) ✓ [or N/A]
  P4 (siblings as control) ✓ [or N/A]

Co-Authored-By: Claude <tier> <date> <noreply@anthropic.com>
```

---

## If You Get Stuck

1. **Check V5_RIGOROUS_THEORY_PLAN.md** — your WP card has the contract (inputs/outputs/invariants)
2. **Run the self-tests in the certified kernels** — `python3 cooper_s10_kernel.py` should pass
3. **Re-read LESSONS_LEARNED.md** — a past mistake might match your blocker
4. **Leave a BLOCKED note** in the work-package file with the exact error, don't try to push through

---

## Good Luck!

The program is salvageable and the path is clear. Adhere to the gate conditions
and institutional practices, and the discovery (if it exists) will be
defensible.

**You have everything you need. Go build it.**
