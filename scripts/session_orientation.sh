#!/bin/bash
# session_orientation.sh — Quick orientation for next session across all three streams
#
# Run from repo root: bash scripts/session_orientation.sh
# Provides: gate status, blocker summary, key files, recent commits, next actions
#
# This script is NOT authoritative (git status/log are) but provides a quick mental model.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "=========================================="
echo "STREAM 3: EMPIRICAL VALIDATION ORIENTATION"
echo "=========================================="
echo "Date: $(date -u +'%Y-%m-%d %H:%M:%S UTC')"
echo "Repo: $(git remote get-url origin 2>/dev/null || echo 'local only')"
echo ""

# ============================================================================
# GATE STATUS
# ============================================================================
echo "GATE STATUS (Blocking S3-00 empirical execution)"
echo "============================================================================"

gate_1_blocked=true
gate_2_blocked=true
gate_3_blocked=true

# Check for K3_SELECTION_REPORT.md (Stream 2 unblock)
if [ -f "briefs/K3_SELECTION_REPORT.md" ]; then
  echo "✓ Gate 1 (Stream 2 candidate selection): CLEARED"
  echo "  File: briefs/K3_SELECTION_REPORT.md"
  gate_1_blocked=false
else
  echo "✗ Gate 1 (Stream 2 candidate selection): BLOCKED"
  echo "  Stream 2 is executing C1/C2 checkers on candidates."
  echo "  Awaiting: briefs/K3_SELECTION_REPORT.md (machine-generated tables + rationale)"
  echo "  Reference: briefs/STREAM2_UNBLOCK_EXPECTATIONS.md (full task spec)"
fi

# Check for ASSUMPTIONS.md signature
if grep -q "Signed-by:" ASSUMPTIONS.md 2>/dev/null; then
  echo "✓ Gate 2 (ASSUMPTIONS.md Xavier signature): CLEARED"
  gate_2_blocked=false
else
  echo "✗ Gate 2 (ASSUMPTIONS.md Xavier signature): BLOCKED"
  echo "  Currently: ASSUMPTIONS.md v0.1 (DRAFT)"
  echo "  Next: T0 review + Xavier formal signature"
fi

# Check for PREDICTION.md pin
if grep -q "^PINNED:" PREDICTION.md 2>/dev/null; then
  echo "✓ Gate 3 (PREDICTION.md observable pin): CLEARED"
  echo "  Observable: $(grep '^PINNED:' PREDICTION.md | head -1)"
  gate_3_blocked=false
else
  echo "✗ Gate 3 (PREDICTION.md observable pin): BLOCKED"
  echo "  Currently: PREDICTION.md (DRAFT, three candidates listed)"
  echo "  Next: T0 selects observable (P1/P2/Lyman-α) and derives m_φ range"
fi

echo ""

# ============================================================================
# BLOCKER SUMMARY
# ============================================================================
echo "BLOCKER SUMMARY"
echo "============================================================================"

if [ "$gate_1_blocked" = false ] && [ "$gate_2_blocked" = false ] && [ "$gate_3_blocked" = false ]; then
  echo "✓ ALL GATES CLEAR — Ready to proceed to S3-03/S3-04 (real data comparison)"
elif [ "$gate_1_blocked" = false ]; then
  echo "⏳ Gate 1 cleared. Awaiting Gates 2–3 (T0 signatures + PREDICTION.md pin)"
else
  echo "⏳ Awaiting Gate 1 (Stream 2 K3_SELECTION_REPORT.md), then Gates 2–3"
fi

echo ""

# ============================================================================
# STREAM 3 READINESS
# ============================================================================
echo "STREAM 3 READINESS (Haiku-completed deliverables)"
echo "============================================================================"

if [ -f "pipeline/stream3_comparison.py" ]; then
  echo "✓ WP S3-02 (pipeline scaffold): READY"
  if bash -c "cd pipeline && python -m pytest tests/test_stream3_golden.py -q 2>/dev/null" > /dev/null 2>&1; then
    echo "  Status: Golden tests PASS (3/3) ✓"
  else
    echo "  Status: Golden tests (run: pytest pipeline/tests/test_stream3_golden.py)"
  fi
else
  echo "✗ WP S3-02 (pipeline scaffold): NOT FOUND"
fi

if [ -f "data/MANIFEST_S3.md" ]; then
  echo "✓ WP S3-01 (data acq manifest): READY"
  echo "  Datasets: PTA (NANOGrav/EPTA), lensing (SDSS/DES/Euclid), Lyman-α"
  echo "  Next: Run bash scripts/fetch_stream3_data.sh in your local environment"
else
  echo "✗ WP S3-01 (data acq manifest): NOT FOUND"
fi

echo ""

# ============================================================================
# KEY FILES (Quick Reference)
# ============================================================================
echo "KEY FILES (Quick Reference)"
echo "============================================================================"
echo ""
echo "Strategy & Planning:"
echo "  - EXECUTION_PLAN.md (overall roadmap)"
echo "  - VISION.md (F-theory frame, tier discipline)"
echo "  - PREDICTION.md (pre-registered observables, awaiting pin)"
echo ""
echo "Stream 2 (K3 Candidate Selection):"
echo "  - briefs/STREAM2_UNBLOCK_EXPECTATIONS.md (definitive task spec)"
echo "  - briefs/K3_SELECTION_REPORT.md (AWAITED: from Stream 2 execution)"
echo ""
echo "Stream 3 (Empirical Validation):"
echo "  - docs/WP_S301_S302_STATUS.md (Haiku prep work summary)"
echo "  - pipeline/stream3_comparison.py (generic scaffold, zero hard-coded numbers)"
echo "  - pipeline/tests/test_stream3_golden.py (closure + null golden tests)"
echo "  - data/MANIFEST_S3.md (dataset template)"
echo "  - scripts/fetch_stream3_data.sh (idempotent fetch, awaits network)"
echo ""
echo "Checker Suite (v0.7.0):"
echo "  - checkers/check_C1_mirror_integrality.py"
echo "  - checkers/check_C3_sym2.py"
echo "  - checkers/check_C3b_moduli_map.py"
echo "  - docs/CRITERION_STATUS.md (machine-generated verdicts)"
echo ""
echo "Guardrails & Discipline:"
echo "  - CLAUDE.md (binding rules: no real-data before PREDICTION.md pinned)"
echo "  - scripts/check_tier_language.py (CI enforcement: tier markers)"
echo "  - TUNING_LOG.md (records any post-hoc parameter changes → demotes to FIT)"
echo ""

# ============================================================================
# RECENT COMMITS
# ============================================================================
echo "RECENT COMMITS (Last 5)"
echo "============================================================================"
git log --oneline -5
echo ""

# ============================================================================
# NEXT ACTIONS
# ============================================================================
echo "NEXT ACTIONS (Prioritized)"
echo "============================================================================"

if [ "$gate_1_blocked" = true ]; then
  echo "1. [Stream 2] Monitor progress on K3_SELECTION_REPORT.md"
  echo "   - Verify acceptance criteria (briefs/STREAM2_UNBLOCK_EXPECTATIONS.md §6)"
  echo "   - Confirm C3b verdict matches checker output"
  echo "   - Once merged: proceed to Gate 2"
  echo ""
  echo "2. [Parallel] Prepare ASSUMPTIONS.md for T0 review"
  echo "   - Current: ASSUMPTIONS.md v0.1 (DRAFT)"
  echo "   - T0 to finalize + Xavier to sign"
  echo ""
  echo "3. [Parallel] Prepare PREDICTION.md pin for T0 derivation"
  echo "   - Current: PREDICTION.md (DRAFT, three observables)"
  echo "   - T0/T0s to select one and derive m_φ range"
else
  if [ "$gate_2_blocked" = true ] || [ "$gate_3_blocked" = true ]; then
    echo "1. Finalize T0 gates (ASSUMPTIONS.md signature + PREDICTION.md pin)"
    echo ""
  fi
  echo "2. Parameterize pipeline/stream3_comparison.py with real PREDICTION.md values"
  echo "   - Update load_prediction_block() to read pinned values"
  echo "   - Run: bash scripts/fetch_stream3_data.sh (from local environment)"
  echo "   - Populate data/MANIFEST_S3.md with downloaded SHA256s"
  echo ""
  echo "3. Run S3-03/S3-04 (real data comparison) — escalate to Sonnet/Opus tier"
  echo "   - Execute: python pipeline/stream3_comparison.py (real datasets)"
  echo "   - Generate: OBSERVATIONAL_REPORT.md (T0 interpretation)"
fi

echo ""
echo "=========================================="
echo "For more details, see:"
echo "  - docs/WP_S301_S302_STATUS.md (current progress)"
echo "  - briefs/STREAM2_UNBLOCK_EXPECTATIONS.md (Stream 2 task spec)"
echo "  - memory/session_2026_07_24_stream3_s301_s302.md (session summary)"
echo "=========================================="
