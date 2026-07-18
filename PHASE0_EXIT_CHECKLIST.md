# Phase 0 Exit Checklist — GATE G0

**Current date:** 2026-07-18  
**Target:** Close GATE G0 and unlock Phase 1 / Stream 1 work  
**Blocking condition:** All items below must have checkmarks before G0 can close.

---

## Work Package Status — P0-A through P0-D

### ✅ P0-A — Formalize ASSUMPTIONS.md

**Status:** v0.3-T0 completed 2026-07-18

- [x] Draft assumptions (A-SEQ, A-VOL, A-ONT, A-REL) — T0 reauthored from T1 reconstructions
- [x] A-DE assumption (T0-drafted 2026-07-17, adopted in v0.3-T0)
- [x] A-DBI conditional assumption (status: CONDITIONAL, not assumed in Phase 0)
- [x] All five assumptions: statement, tier, discharge path, failure mode
- [x] Assumption-tagging audit contract specified
- [ ] **XAVIER REVIEW PENDING** — sign-off checklist in ASSUMPTIONS.md §Signature
- [ ] Commit hash-pinned in all three repos after Xavier signs

**Deliverable:** `/home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-Home/ASSUMPTIONS.md` v0.3-T0

---

### ✅ P0-B — Design Free-Parameter Ledger Schema

**Status:** Implemented (2026-07-17)

- [x] Template file: `templates/free_parameter_ledger.jinja`
- [x] Golden example in PREDICTION.md §1 (Free-Parameter Ledger table)
- [x] K3_CRITERIA.md §C4 cross-reference added
- [x] Ledger schema integrated into PREDICTION.md v0.9-T0

**Deliverable:** `/home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-Home/templates/free_parameter_ledger.jinja`

---

### ✅ P0-C — Update epistemic-guardrails Skill

**Status:** Implemented (2026-07-17)

- [x] CI rule Finding F-A: abstracts reviewed against tier ledger
- [x] Rule: claims may not appear in abstracts at a stronger tier than in their section
- [x] Automated grep checks for tier-language violations
- [x] CI integration in `.github/workflows/epistemic-guardrails.yml`

**Deliverable:** Skill `epistemic-guardrails` updated; rule + CI check in repo

---

### ✅ P0-D — Create TUNING_LOG.md Skeleton

**Status:** Implemented (2026-07-17)

- [x] Empty but initialized file
- [x] Entry format specified (date, commit, quantity, old/new value, justification)
- [x] CI rule: every post-pin PREDICTION.md assumption-tag change requires a TUNING_LOG entry
- [x] `scripts/check_tuning_log.py` implemented and wired into CI

**Deliverable:** `/home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-Home/TUNING_LOG.md` + CI enforcement

---

## Critical Documents — Xavier Review Checklist

### ASSUMPTIONS.md v0.3-T0

**File:** `/home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-Home/ASSUMPTIONS.md`

**Xavier's review items:**

1. **A-SEQ — Single-Sequence Dominance**
   - [ ] Statement correctly describes the risk (uncounted light modes)?
   - [ ] Discharge path realistic (explicit KK spectrum computation)?
   - [ ] Failure mode clear (blocks S3-00 if light mode found)?

2. **A-VOL — Volume-Modulus Stabilization**
   - [ ] Statement correctly captures the stabilization + stationarity requirements?
   - [ ] Discharge path realistic (explicit stabilization mechanism or RG argument)?
   - [ ] Failure mode clear (P1 → FIT, P2 → NULL if back-reaction found)?

3. **A-ONT — Ontological Realization (Compactification Existence)**
   - [ ] Statement honest about the gap ("we do not claim complete construction")?
   - [ ] Discharge path realistic (flux/tadpole construction is long-horizon)?
   - [ ] Failure mode clear (entire Tier C program → F5 if no compactification)?

4. **A-REL — Moduli Unification (Dual-Scale Coupling)**
   - [ ] Statement correctly formalizes the coupling hypothesis?
   - [ ] Discharge path realistic (blind re-derivation agreement as evidence)?
   - [ ] Failure mode clear (F5 branch if no relation survives elimination)?

5. **A-DE — Dark-Energy Identification**
   - [ ] Statement honest (three strong assumptions: positive sign, scaling, identification)?
   - [ ] Tier C attribution correct (strongest assumption in the chain)?
   - [ ] Failure mode clear (F5b if a_3 unbounded; adjacent to F5 if no identification)?

6. **A-DBI — Baryonic DBI Coupling (CONDITIONAL)**
   - [ ] Conditional status appropriate for Phase 0?
   - [ ] Triggers only if data suggests baryonic-coupling signature?
   - [ ] OK to remove from Phase 0 if preferred?

7. **Overall**
   - [ ] Assumption-tagging audit contract (CI section) sound?
   - [ ] All five assumptions form a coherent load-bearing structure for S3-00?
   - [ ] Ready to commit hash-pinned into all three repos?

**Sign-off:** Xavier provides date, initials, and answers to all 7 checkboxes in the Signature Block.

---

### K3_CRITERIA.md v1.0 (already frozen, verify status)

**File:** `/home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-Home/K3_CRITERIA.md`

**Status check:**

- [ ] Frozen v1.0 committed and tagged
- [ ] Criteria C1–C5 defined (C5 = Swampland checks)
- [ ] **C3b criterion fully specified** (Shioda-Inose moduli map)
- [ ] C3b checker (`checkers/check_c3b_moduli_map.py`) brief written
- [ ] Assumption dependencies documented (C2 depends on A-ONT; C3b depends on A-SEQ, A-VOL)
- [ ] Mirrored in all three repos with hash pin

---

## Stream 1 Unblocking (Lean 4 CI)

**Work Package:** S1-01 (Repo scaffold + CI)

**File:** `/home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-Home/.github/workflows/epistemic-guardrails.yml` (proxy for CI setup)

**Status:**

- [ ] CI checks running and passing:
  - [ ] Tier-language audit (Finding F-A)
  - [ ] TUNING_LOG consistency
  - [ ] Assumption-tag audit (every quantity in predictions carries assumption list)
- [ ] README updated with Phase 0 status
- [ ] Readme notes that Lean repo is a separate repository (`SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal`)

---

## Deliverables Summary (for G0 closure)

| Deliverable | File | Status | Xavier sign-off |
|---|---|---|---|
| ASSUMPTIONS.md v0.3-T0 | `ASSUMPTIONS.md` | ✅ Complete, T0-authored | [ ] Sign |
| K3_CRITERIA.md v1.0 | `K3_CRITERIA.md` | ✅ Frozen | [ ] Verify |
| Free-Parameter Ledger schema | `templates/free_parameter_ledger.jinja` | ✅ Implemented | [ ] Verify |
| epistemic-guardrails Finding F-A rule | `.github/workflows/` + skill | ✅ Implemented | [ ] Verify |
| TUNING_LOG.md + CI enforcement | `TUNING_LOG.md` + `scripts/check_tuning_log.py` | ✅ Implemented | [ ] Verify |
| Brief: S2-01b (C3b checker) | `briefs/S2-01b.md` | ✅ Completed | [ ] Review |
| PREDICTION_APPENDIX_A.md outline | `PREDICTION_APPENDIX_A.md` | ✅ Outline v0.1 | [ ] Review |
| PHASE0_EXIT_CHECKLIST.md | This file | ✅ Created | — |

---

## Next Steps (in order)

### 1. Xavier Review & Sign-Off (1 day)

Xavier opens ASSUMPTIONS.md, reviews all five + conditional A-DBI, answers the 7-item checklist in the Signature Block, appends signature (date + initials).

**Blocker:** If Xavier requests changes → revise, re-submit. If accepted → proceed to step 2.

### 2. Commit & Hash-Pin (1 day)

T0/T1 commits ASSUMPTIONS.md v0.3-signed and tags the commit as `PHASE0-READY`.

**Action:**
```bash
git add ASSUMPTIONS.md PHASE0_EXIT_CHECKLIST.md briefs/S2-01b.md PREDICTION_APPENDIX_A.md
git commit -m "Phase 0 completion: ASSUMPTIONS.md v0.3 signed, S2-01b brief, PREDICTION Appendix A outline

- ASSUMPTIONS.md v0.3-T0: all five assumptions (A-SEQ, A-VOL, A-ONT, A-REL, A-DE) authored; A-DBI conditional
- Xavier sign-off appended to signature block
- K3_CRITERIA.md v1.0 frozen with C3b criterion + dependencies
- S2-01b brief: C3b checker design (T1-ready)
- PREDICTION_APPENDIX_A.md v0.1: outline structure for MVM ansätze derivations
- Phase 0 exit checklist completed

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

### 3. Mirror to Partner Repos (1 day)

T0/T1 pushes ASSUMPTIONS.md v0.3-signed + K3_CRITERIA.md v1.0 (hash-pinned) to:
- `SocrateAI-Scientific-Agora-K3-DarkMatter`
- `SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal`

Each repo tags the commit `PHASE0-READY` for cross-repo verification.

### 4. Close GATE G0 (certification)

T0 writes a brief "GATE G0 CLOSED" entry in the README or a status document, noting:
- ASSUMPTIONS.md v0.3-signed is canonical
- K3_CRITERIA.md v1.0 is frozen
- S1-01 (Lean CI) can now proceed independently
- S2-01b brief is T1-ready
- S3-00 (MVM matching) is unblocked once S2-01b is implemented

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Xavier requests major revisions to assumptions | Treat as design feedback; revise and re-submit (no penalty; better to get it right now) |
| C3b checker brief is too vague for T1 | T0 schedules a brief working session with T1 to clarify algorithm and golden-test expectations |
| S2-01b implementation reveals missing literature data | Escalate to K3_CRITERIA.md amendment (requires adversarial-pass documentation); may delay S2-04 ranking but not G0 closure |
| Phase 0 exit delayed > 1 week | Proceed to Phase 1 with ASSUMPTIONS.md v0.3-unsigned (marked as interim); Xavier sign-off becomes a parallel track; S1/S2 work proceeds against the unsigned draft pending signature |

---

## Definition of G0 Closure

**GATE G0 is CLOSED when:**

1. Xavier has signed ASSUMPTIONS.md v0.3 (signature block completed)
2. All five assumptions + conditional A-DBI are Tier C, load-bearing, and pre-committed
3. K3_CRITERIA.md v1.0 is frozen and mirrored in all three repos
4. CI rules (epistemic-guardrails Finding F-A, TUNING_LOG enforcement) are active
5. S2-01b brief (C3b checker) is written and ready for T1 implementation
6. PREDICTION_APPENDIX_A.md outline is in place (template for MVM derivations at pin time)
7. README or status document records "GATE G0 CLOSED — <date>" with Xavier confirmation

**When G0 closes:**
- Phase 1 work (Streams 1, 2, 3) can proceed in parallel
- Stream 1: S1-01 Lean CI setup (T2-ready)
- Stream 2: S2-01b C3b checker implementation (T1-ready)
- Stream 3: S3-00 MVM matching design (T0-ready once C3b checker is done)

---

**Last updated:** 2026-07-18  
**Prepared by:** T0 (Fable 5 session)  
**Awaiting Xavier review:** ASSUMPTIONS.md v0.3-T0 signature block
