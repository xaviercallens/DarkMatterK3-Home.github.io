# Three-Stream Status (2026-07-24)

> ⚠️ **SUPERSEDED (2026-07-25).** All three Stream 3 gates this document calls "BLOCKED" or
> "DRAFT" cleared the same day this was written. The empirical path they unblocked (S3-00) was
> then attempted and reached **Off-Ramp 3 terminus** — untestable at every scale with data that
> exists today (`NO_PREDICTION_BRANCH.md` §8.5). Current status:
> `docs/STREAMS_STATUS_2026_07_25.md`. Left here for history; do not act on the gate/blocker
> tables below as if they still describe the present.

**Summary:** Stream 3 Haiku prep work complete (S3-01/S3-02); Stream 2 now executing C1/C2 candidate selection (K3_SELECTION_REPORT pending); all three gates defined and locked.

**Quick Links:**
- [Session orientation script](../scripts/session_orientation.sh) — run for current gate/blocker status
- [Stream 2 unblock brief](../briefs/STREAM2_UNBLOCK_EXPECTATIONS.md) — task spec for K3 candidate selection
- [Stream 3 status](../docs/WP_S301_S302_STATUS.md) — Haiku-completed deliverables

---

## Stream 1: Geometric Theory (Lean)

**Status:** Completed (v5 rigorous theory verified). Awaiting coordination with Streams 2–3 for joint release.

**Deliverables:**
- Certified kernel (`cooper_s10_kernel.py`): s₁₀ (A005260, λ=16) verified to order 40
- WP-A3-s10, WP-B2-s10, WP-C1 (Haiku-tier theory work done)
- V5_SCIENTIFIC_REVIEW.md: 9 findings + 5 gates identified

**Current Blocker:**
- Awaiting joint coordination: once Stream 2 selects K3 candidate pair + Stream 3 publishes OBSERVATIONAL_REPORT.md, Stream 1 to encode geometric data in Lean for v0.4.0 release

**Files:**
- `VISION.md` §1–§2: F-theory frame, tier discipline
- `V5_RIGOROUS_THEORY_PLAN.md`: theory roadmap
- `LESSONS_LEARNED.md`: V5 retrospective
- `briefs/STREAM_ALIGNMENT_C3_C3b.md`: instructions for Stream 1 (don't encode false SYM2_PROVED claims)

---

## Stream 2: K3 Theory & Candidate Selection

**Status:** IN PROGRESS (executing C1/C2 checkers on candidates). K3_SELECTION_REPORT.md expected.

**Task (from STREAM2_UNBLOCK_EXPECTATIONS.md):**
1. Run C1 checker on all candidates → extract mirror-map integrality order
2. Run C2 checker on all candidates → extract Kodaira fiber data + Picard lattice
3. Verify C3/C3b verdicts match v0.7.0 checker output (sporadics PASS; Cooper family FAIL)
4. **Select and publish:** K3_SELECTION_REPORT.md naming top C3b-passing candidate pair

**Options:**
- **Option A (preferred):** Select one sporadic AZ pair (γ/F, α/C, δ/A, η/D) — all pass C3b ✓
- **Option B (transparent):** Record that Cooper family fails C3b, proceed with A
- **Option C (forbidden):** Re-run or modify checkers post-hoc — violates pre-registration

**Effort:** 4–8 hours focused work

**Acceptance Criteria (§6 of STREAM2_UNBLOCK_EXPECTATIONS.md):**
- All candidates listed with (a,b,c,d) parameters from verified literature
- C1 verdicts match v0.7.0 checker output
- C2 Kodaira fiber table for ≥2 candidates
- C3/C3b verdicts match checker results (sporadics PASS, Cooper FAIL)
- **Selected pair passes C3b** (non-negotiable)
- If Cooper excluded, explicitly stated
- No hand-entered numbers; all traced to checker output or literature
- Assumption tags present ([A-ONT] at minimum)

**Unblocks:** S3-00 MVM derivation (T0 work) + S3-03/S3-04 empirical comparison (Stream 3 data pipeline)

**Files:**
- `briefs/STREAM2_UNBLOCK_EXPECTATIONS.md` (definitive task spec)
- `briefs/K3_SELECTION_REPORT.md` (AWAITED: deliverable)
- `docs/CRITERION_STATUS.md` (v0.7.0 checker output: machine-generated verdicts)

---

## Stream 3: Empirical Validation (MVM Matching)

**Status:** WP S3-01/S3-02 complete (data acq + pipeline scaffold, 3/3 golden tests PASS). Awaiting three gate blockers before S3-03/S3-04 execution.

### Gate Status

| Gate | Blocker | Status | Unblocks |
|------|---------|--------|----------|
| G1.a | K3_SELECTION_REPORT.md (Stream 2 C1/C2 execution) | BLOCKED | S3-00 step 2/3 |
| G1.b | ASSUMPTIONS.md Xavier signature (T0 decision) | BLOCKED | All S3-00 quantities |
| G1.c | PREDICTION.md observable pin (T0 derivation) | BLOCKED | S3-00 step 3 |

**Once all three clear:** Proceed to S3-00 MVM matching → S3-03/S3-04 empirical execution → OBSERVATIONAL_REPORT.md (T0 interpretation)

### Completed Deliverables

**WP S3-01 (Data Acquisition):**
- `data/MANIFEST_S3.md`: Checksummed dataset template (PTA, lensing, Lyman-α)
- `scripts/fetch_stream3_data.sh`: Idempotent fetch (awaits user to run in network environment)
- Datasets: NANOGrav 15-yr, EPTA DR2, SDSS weak-lensing, DES Y3, SDSS DR12, DESI EDR (pending)
- **Next:** User runs fetch script locally, populates SHA256s in MANIFEST_S3.md

**WP S3-02 (Pipeline Scaffold):**
- `pipeline/stream3_comparison.py`: Generic pipeline (zero hard-coded candidates, reads PREDICTION.md template)
- `pipeline/tests/test_stream3_golden.py`: Golden tests (3/3 PASS)
  - Closure: inject signal, recover within 3σ ✓
  - Null: no signal, report null at α=0.05 FPR ✓
  - Assumption pass-through ✓
- **Constraints:** No free knobs, TEST/FIT labels mechanical, assumptions carry through
- **Next:** Once PREDICTION.md pins, update load_prediction_block() (config-only change) → parameterize pipeline

### Pending Deliverables

**S3-00 (MVM Matching):** Derive m_φ(𝒱, g_s), α_D, Λ_D from selected K3 + C2 data (T0/T0s work, awaits G1.a–c)

**S3-03/S3-04 (Real Data Comparison):** Run pipeline against public datasets, generate results tables (higher tier: Sonnet/Opus)

**S3-05 (Observational Report):** T0 interprets results (VISION.md §4: prose-only, no new tables)

### Key Files

- `docs/WP_S301_S302_STATUS.md`: Haiku prep work summary + tier escalation guidance
- `pipeline/stream3_comparison.py`: Generic pipeline scaffold (ready to parameterize)
- `pipeline/tests/test_stream3_golden.py`: 46 tests, 3 golden PASS (merge-blocking)
- `data/MANIFEST_S3.md`: Dataset template (awaits SHA256 population)
- `scripts/fetch_stream3_data.sh`: Idempotent fetch (stub, awaits network execution)
- `checkers/check_C1_mirror_integrality.py`, `check_C3_sym2.py`, `check_C3b_moduli_map.py`: v0.7.0 symbolic checkers

---

## Gate Blockers (Hard Rules)

### Gate 1: K3_SELECTION_REPORT.md (Stream 2)
- **Required:** Machine-generated C1/C2 verdict table for all candidates
- **Required:** C3/C3b status matches v0.7.0 checker output
- **Required:** Selected pair passes C3b (non-negotiable for S3-00)
- **Verification:** acceptance criteria §6 of STREAM2_UNBLOCK_EXPECTATIONS.md
- **Status:** IN PROGRESS (Stream 2 executing C1/C2 checkers)

### Gate 2: ASSUMPTIONS.md Xavier Signature (T0)
- **Required:** ASSUMPTIONS.md v0.1 reviewed + Xavier formal signature added
- **Status:** DRAFT (awaiting T0 review)

### Gate 3: PREDICTION.md Observable Pin (T0)
- **Required:** One of P1/P2/Lyman-α selected, hash-pinned, m_φ range derived
- **Required:** Pre-registration commit predates all data-touching commits
- **Status:** DRAFT (three observables listed, awaiting T0 selection + S3-00 derivation)

**All three must clear before S3-03/S3-04 can touch real data.** No exceptions, no shortcuts (VISION.md §3 enforcement).

---

## Timeline & Effort Estimate

| Phase | Owner | Effort | Blocker | Unblocks |
|-------|-------|--------|---------|----------|
| S3-01/S3-02 (prep) | Haiku | ✓ Complete | — | S3-00 parameterization |
| Stream 2 (C1/C2) | Stream 2 | 4–8h | — | G1 |
| G1 verification | Haiku | ~30min | Stream 2 report | — |
| S3-00 (MVM match) | T0/T0s | 4–6h | G1 + G2 + G3 | S3-03/S3-04 |
| S3-03/S3-04 (real data) | Sonnet/Opus | TBD | S3-00 complete | S3-05 |
| S3-05 (interpret) | T0 | TBD | S3-03/S3-04 complete | v0.4.0 release |

---

## How to Quickly Orient on Next Session

**Run:**
```bash
bash scripts/session_orientation.sh
```

**Outputs:**
- Gate status (clear/blocked with reason)
- Stream 3 readiness (WP S3-01/S3-02 status)
- Key files (quick reference)
- Recent commits (what changed)
- Prioritized next actions

**For detailed context:**
- `memory/session_2026_07_24_stream3_s301_s302.md` (session summary)
- `briefs/STREAM2_UNBLOCK_EXPECTATIONS.md` (Stream 2 task spec)
- `docs/WP_S301_S302_STATUS.md` (Haiku work summary)

---

## Institutional Knowledge Locked In

Per [[institutional-practices-locked-in]] and VISION.md §2–§4:

- **P1 (No constant without provenance):** Every numeric value must trace to checker output, Lean #eval, or cited refs/ file
- **P2 (Tests are scientific not smoke):** Golden tests (closure + null) are merge-blocking; verify statistical properties, not smoke
- **P3 (Pre-register before unblind):** PREDICTION.md must be hash-pinned before any real-data commit; no post-hoc parameter changes
- **P4 (Sibling families as control):** Comparisons use published data products (NANOGrav posteriors, stacked lensing profiles), never collaboration/submission framing
- **Tier discipline (epistemic-guardrails):** Every claim carries its tier marker; Tier C must have conjecture marker; numbers must be traced

**No exceptions.** These are the guardrails that protect credibility. Violations go through EXECUTION_PLAN.md §4 T0 review only.

---

**Generated-by:** Stream 3 (Haiku orchestration) | **Reviewed-by:** pending T0 | **Date:** 2026-07-24
