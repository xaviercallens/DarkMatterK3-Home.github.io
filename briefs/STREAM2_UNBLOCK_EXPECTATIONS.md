# Brief — Stream 2: Execution Expectations to Unblock Stream 3

**To:** Stream 2 (K3 Theory & Candidate Selection, Xavier lead)
**From:** Stream 3 (Empirical Validation, Haiku orchestration)
**Date:** 2026-07-24
**Subject:** What Stream 2 must deliver to unblock S3-00 MVM matching + S3-01/S3-02 data pipeline
**Authority:** Derived from Stream 1 brief (EXECUTION_PLAN.md §5.1 routing) + v0.7.0-checker-suite verified results

---

## 1. Current State (No Surprises)

Stream 3 has built and tested the **symbolic checker infrastructure** (v0.7.0-checker-suite, committed and released):

- **C1 checker** (mirror-map integrality): All candidates tested ✓ (sporadics + Cooper family pass)
- **C3 checker** (symmetric-square g.f. identity): All candidates tested ✓
- **C3b checker** (Shioda–Inose map F + period correspondence): All candidates tested ✓

**Verified result** (`docs/CRITERION_STATUS.md`, machine-generated):

| Candidate | C1 | C3 | C3b |
|---|---|---|---|
| γ, α, δ, η (sporadic AZ) | PASS(40) | PASS(40) | PASS(40) |
| s7, s10, s18 (Cooper, d≠0) | PASS(40) | FAIL | FAIL |

**The honest finding:** s7 and s10 pass C1 (genuine maximal-unipotent-monodromy period operators) but **fail C3 and C3b** — they are not symmetric squares of, nor Shioda–Inose-mapped to, any elliptic (Zagier) order-2 operator. The Cooper extended family (d≠0) is outside the Almkvist–Zudilin symmetric-square bijection.

**This is not negotiable.** The checkers are deterministic, exact-rational, 46 tests green, tier-CI clean. Briefs for T0s review are published (pending review). Stream 3 cannot proceed on false mathematical assumptions.

---

## 2. What Stream 2 Must Do to Unblock S3-00

### 2.1 Mandatory Task: Execute C1/C2 on Candidates (Not Done Yet)

The **C1 and C3b checkers already exist** in the v0.7.0 release (see `checkers/check_C1_mirror_integrality.py`, `checkers/check_C3b_moduli_map.py`). What Stream 2 has **not** done:

- [ ] **Run C1 on all candidate order-3 operators**, with the actual Picard–Fuchs recurrence coefficients (a, b, c, d)
- [ ] **Run C2 on all candidates**, extracting Kodaira fiber data from the Weierstrass model (this is a specification work, not a checker — the C2 checker stub exists in `checkers/check_C2_kodaira.py` but the full fiber-classification pipeline is not yet implemented; you may need to build it or run it manually per K3_CRITERIA.md C2)
- [ ] **Identify the top C3b-passing candidate pair** (the one that survives both C1 integrality and C3b Shioda–Inose map closure)
- [ ] **Publish `K3_SELECTION_REPORT.md`** naming that pair and explaining why it was selected (criterion results, C1/C2/C3b verdicts, per-candidate fiber data, lattice consistency checks)

### 2.2 Decision Point: Which Candidate Pair?

**Three possible outcomes:**

**Option A (Preferred):** One of the sporadic AZ pairs (γ/F, α/C, δ/A, η/D) is designated as the S3-00 MVM input.
- All four pass C1, C3, C3b ✓
- C2 Kodaira fiber data + Picard lattice are deterministic for each
- **Action:** Run C2 on each, select the one with the best lattice properties (ρ tightness, transcendental rank for moduli freezing)
- **Deliverable:** `K3_SELECTION_REPORT.md` naming the selected sporadic pair and its C1/C2 verdicts

**Option B (Transparent):** Record that no C3b pair exists for the Cooper family (s7, s10, s18).
- s7/s10 fail C3 and C3b (mathematically certain, not a choice)
- **Action:** Document this explicitly in `K3_SELECTION_REPORT.md` as a negative result
- **Consequence:** proceed with Option A (sporadics)
- **Deliverable:** `K3_SELECTION_REPORT.md` explaining why Cooper family is excluded and which sporadic pair was selected instead

**Option C (Violates Pre-Registration):** Attempt to modify Stream 1 or the checkers to "make s7/s10 work."
- **Not permitted.** The checkers are frozen (v0.7.0 release); the C3/C3b verdicts are deterministic, exact-rational, verified 46 tests green. Rerunning checkers or modifying checker code after seeing results is the exact failure mode pre-registration exists to prevent.
- Any proposed modification must go through T0 review and be recorded in TUNING_LOG.md (which demotes downstream results to FIT, not TEST).
- **This is not a shortcut.** It costs more than choosing a valid candidate now.

**Recommendation:** Option A or B (transparent). Option C is the opposite of integrity.

### 2.3 Expected Deliverables

**File: `K3_SELECTION_REPORT.md`** (machine-generated tables + prose)

Required sections:
1. **Candidate Register** — all tested candidates (sporadic + Cooper) with (a,b,c,d) parameters
2. **Criterion Results Table** — C1 verdict per candidate (mirror-map integrality order, margin)
3. **C2 Kodaira Fiber Table** — fiber types (I_1, I_0*, etc.) at each singular locus per candidate
4. **Picard Lattice Summary** — Picard rank (ρ), transcendental rank (22−ρ), lattice invariants per candidate
5. **C3/C3b Status** — which candidates pass/fail (machine-generated from v0.7.0 checker output)
6. **Selection Rationale** (prose, T0-authored interpretation only) — why the selected pair was chosen
   - If sporadic: why this one over others (lattice properties, fiber stability, etc.)
   - If no C3b pair exists: explicit statement + why Cooper family was excluded
7. **Assumption Tags** — every C1/C2/C3b result carries [A-ONT] (contingent on compactification realization)

**Format:** Machine-generated tables (no hand-entered numbers); prose only in rationale section.

---

## 3. What Stream 3 is Ready to Receive

Once Stream 2 publishes `K3_SELECTION_REPORT.md`:

- **S3-00 MVM Matching:** T0/T0s can derive m_φ(𝒱, g_s), α_D, Λ_D using the selected candidate's period geometry + C2 Kodaira fiber data
- **S3-01 Data Acquisition:** Already staged (MANIFEST_S3.md template + fetch script) — awaits candidate selection to pass to S3-00
- **S3-02 Pipeline Scaffold:** Already green (3/3 golden tests pass) — awaits PREDICTION.md pin to parameterize

**No code changes needed in Stream 3.** Only configuration changes once PREDICTION.md freezes.

---

## 4. Gate Conditions (Hard Rules)

Per EXECUTION_PLAN.md §4 S3-00, Stream 3 cannot proceed to real data comparison until:

1. ✗ (blocked on Stream 2) Stream 2 publishes `K3_SELECTION_REPORT.md` naming a C3b-passing candidate pair
2. ✗ (T0 decision, not Stream 2) Xavier signs/authors ASSUMPTIONS.md v0.3 (currently DRAFT)
3. ✗ (T0 decision, not Stream 2) PREDICTION.md observable is pinned (currently DRAFT, three candidates)

**Stream 2's task unblocks #1.** Tasks #2–#3 are T0 governance.

---

## 5. Realistic Timeline & Effort (Haiku Estimate)

### Stream 2 Effort (In Parallel):
- **C1 execution** on candidates: ~1–2 hours (run checker, collate results)
- **C2 Kodaira fiber classification**: ~2–4 hours (either build full C2 checker or run manually per K3_CRITERIA.md C2 spec + literature)
- **C3/C3b verification** (results already in v0.7.0, no new computation): ~30 min (copy from v0.7.0 checker output)
- **Report writing** (tables machine-generated, prose by human): ~1 hour
- **Total:** 4–8 hours focused work

### Blockers:
- If C2 full checker is not yet built, you may need to run fiber classification manually (Kodaira-type classification from Weierstrass discriminant is textbook, but requires coding or CAS work)
- Access to verified recurrence coefficients (a, b, c, d) for candidates — assumed to be in refs/ or Cooper literature

### T0 Effort (Parallel, not Stream 2's task):
- ASSUMPTIONS.md signature: ~1 hour (review + sign)
- PREDICTION.md observable pin + MVM derivation: ~4–6 hours (T0/T0s work, depends on candidate selection)

---

## 6. Acceptance Criteria

Stream 3 will accept `K3_SELECTION_REPORT.md` iff:

1. ✓ All tested candidates listed with (a,b,c,d) parameters from verified literature/refs
2. ✓ C1 verdicts (mirror-map integrality order + margin) per candidate — matches or exceeds v0.7.0 checker output
3. ✓ C2 Kodaira fiber table (at least two candidates with full fiber classification)
4. ✓ C3/C3b verdicts match v0.7.0 checker results (sporadics PASS, Cooper family FAIL)
5. ✓ Selected candidate pair **passes C3b** (non-negotiable for S3-00 input)
6. ✓ If Cooper family excluded, explicitly stated (Option B transparency)
7. ✓ No hand-entered numbers in criterion tables; all traced to checker output or literature
8. ✓ Assumption tags present ([A-ONT] at minimum)

**Release:** `K3_SELECTION_REPORT.md` merged to main; Stream 3 immediately updates PREDICTION.md parametrization (awaiting T0 pin decision).

---

## 7. What Not To Do

- ❌ Do not re-run or modify the C3/C3b checkers after seeing results (pre-registration violation)
- ❌ Do not assert s7/s10 are valid MVM inputs without a C3b-verified Zagier order-2 partner (mathematical impossibility)
- ❌ Do not hand-enter numbers into the report (trace all to checker output or cited source)
- ❌ Do not write physics interpretation prose (that's T0 only) — focus on criterion results tables
- ❌ Do not skip C2 Kodaira fiber classification (it's required for S3-00 MVM derivation)

---

## 8. Communication Handoff

Once `K3_SELECTION_REPORT.md` is ready:

- **Stream 1:** receives the selected pair's C3b geometric data (for Lean verification, per briefs/STREAM_ALIGNMENT_C3_C3b.md)
- **Stream 3:** receives candidate + checkers verdicts; proceeds to S3-00 parametrization (awaiting T0 pin)
- **T0/T0s:** review report + sign-off, finalize PREDICTION.md pin + ASSUMPTIONS.md signature

---

## 9. Summary

**Stream 2's task:** Execute existing checkers (C1/C3b already built; C2 design exists) on candidates, select the top C3b-passing pair, publish `K3_SELECTION_REPORT.md`.

**Constraint:** Mathematical integrity — no fabrication, no post-hoc modification of checkers, no false claims about Cooper family Sym² (they fail C3/C3b; this is fact, not negotiable).

**Effort:** 4–8 hours, mostly parallel with T0 work.

**Unblocks:** S3-00 MVM derivation (T0 work), S3-03/S3-04 empirical comparison (Stream 3 data pipeline, ready to parameterize).

**Timeline:** Report published → T0 signatures → PREDICTION.md pin → S3-00 → S3-03/S3-04 → v0.4.0 release (full three-stream delivery).

---

`Generated-by: Stream 3 (Haiku, orchestrating unblock) | Based-on: v0.7.0 checker-suite verified results + Stream 1 brief routing | Reviewed-by: pending T0`
