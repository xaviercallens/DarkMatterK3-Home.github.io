# Stream 2 Brief — WP-A3-t103 K3 Candidate Adjudication (AutoEvolve + Checkers)

**Date:** 2026-07-25  
**Authority:** Fable 5 (T0-delegated)  
**Executor:** Claude Haiku 4.5 (T2 mechanics); decision escalates to Sonnet (T1) or Fable 5 (T0)  
**Governing docs:** `VISION.md` §2–§3, `EXECUTION_PLAN.md` §4, `K3_CRITERIA.md` v1.0 (frozen), `epistemic-guardrails` skill

---

## Context

The Dual-Scale pivot (2026-07-25) opens exploration of alternative K3 candidates beyond the current s7/s10 route. The **t103** candidate (a sporadic sequence from the taxicab literature, OEIS A247452 or related) is proposed as a geometrically simpler alternative with potentially better Kodaira properties.

**Gate:** WP-A3 applies the frozen `K3_CRITERIA.md` checkers (C1–C5) to t103 mechanically. If t103 passes C3b (Sym² structure), it becomes a Route B candidate. If it fails any criterion, it is logged in the F1 removal register with cause recorded.

**Outcome:** A boolean verdict (t103 PASS or t103 FAIL) and a technical memo if FAIL explaining which criteria blocked it.

---

## Work Package Scope

### What This WP Delivers

1. **Fetch t103 recurrence** from OEIS (A247452 or cited source) and verify the first 50 terms against published values  
   - Confirm the generating ODE / Picard-Fuchs operator exists in the literature
   - Record the source as a commit in `refs/`

2. **Run the five checkers** (`checkers/check_C{1,2,3,4,5}.py`) on t103 with the frozen criteria  
   - **C1:** Mirror-map integrality (q-series to q^20+)
   - **C2:** Kodaira fiber type (use published monodromy data or compute from Picard-Fuchs)
   - **C3:** Sym² structure (check if order-3 operator = symmetric square of an order-2)
   - **C3b:** Shioda-Inose moduli map F (extract from literature or compute symbolically)
   - **C4:** Picard rank ≥ 20 (use Hodge diamond / transcendental rank)
   - **C5:** Swampland bounds (apply frozen inequality bounds)

3. **Record the verdict** in a new row of `K3_SELECTION_REPORT.md` (or create `K3_SELECTION_REPORT_SUPPLEMENTARY.md` if main report is frozen)

4. **If t103 FAILS a criterion:**  
   - Log removal reason in `FALSIFICATION_BRANCHES.md` (F1 entry)
   - Record assumption tags: which [A-*] assumptions the failure depends on
   - **Do NOT attempt to tune parameters or re-run with relaxed bounds**

5. **If t103 PASSES C3b (critical):**  
   - Escalate to Fable 5 (T0) for decision: add t103 to candidate pool or wait for further theory work?
   - Provide a technical memo: t103's geometry summary, any novel features, integration into Dual-Scale picture

### What This WP Does NOT Do

- **No new criteria.** Frozen `K3_CRITERIA.md` v1.0 only.
- **No parameter tuning.** If a checker fails, document and stop; do not re-fit.
- **No physics prediction.** t103's K3 properties are mathematical facts; this WP does not compare them to data.

---

## Definition of Done

✅ **Five checker scripts run without error** on t103; all verdicts recorded  
✅ **Verdict table added** to report with columns: `[Candidate] [C1] [C2] [C3] [C3b] [C4] [C5] [Pass/Fail] [Failure reason if any]`  
✅ **Provenance audit:** every constant (mirror-map coefficients, Kodaira type, Picard rank) traces to a committed file or a fetched literature source with SHA256 checksum in `refs/`  
✅ **Assumption tags recorded:** every computed or fetched quantity carries [A-*] dependencies (e.g., C3b verdict tagged [A-SEQ, A-VOL])  
✅ **Escalation readiness:** if t103 PASS C3b, a one-page memo is ready for T0 decision  
✅ **Provenance footer:** commit message includes `Generated-by: Haiku | Verified-by: checker CI | Reviewed-by: [pending T1/T0]`

---

## Files to Create/Modify

| File | Action | Content |
|------|--------|---------|
| `refs/t103_recurrence_v1.json` | Create | t103 sequence definition, first 50 terms, source(s), OEIS link, SHA256 of source document |
| `data/K3_CANDIDATES_EXTENDED.md` | Create or update | t103 row with fetched/computed values for each criterion |
| `scripts/run_checker_on_t103.py` | Create | Entry point: load t103, run C1–C5 checkers, output JSON verdict + table |
| `logs/t103_checker_run_2026_07_25.json` | Create | Structured verdict output: per-checker results, timing, any warnings |
| `FALSIFICATION_BRANCHES.md` | Update (if FAIL) | F1 entry for t103 if any criterion fails; record criterion + assumption dependencies |
| `briefs/STREAM2_WP_A3_RESULTS.md` | Create | Summary table + escalation decision (if PASS C3b) |

---

## Validation Gate

**Mechanical gate:** Run `python3 scripts/run_checker_on_t103.py` → all five checkers execute → JSON verdict produced  
**Correctness gate:** For each checker, verify that the verdict matches a pre-committed golden case (e.g., s7 FAIL C3/C3b is known; applying the same checker to t103 must make sense in context)  
**Manual gate:** Sonnet (T1) reviews the verdict table for internal consistency (e.g., if C3b PASS but C2 FAIL, is the contradiction explained?)  
**Escalation:** If any checker crashes, log the error, do NOT skip the checker; escalate to Sonnet for debugging.

---

## Epistemic Tier Markers

- **t103 recurrence identity** [A] — published in OEIS or literature; machine-verifiable
- **t103 Kodaira fiber type** [B] — computable from Picard-Fuchs monodromy; candidate checkable, not proven
- **t103 Sym² structure (C3/C3b)** [B] — conjectural per candidate; this WP checks the conjecture
- **Interpretation of t103 pass/fail as "route B candidate"** [C] — only if criteria are truly predictive of real K3 geometry; otherwise a matter classification exercise

---

## Escalation Paths

| Event | Action | Contact |
|-------|--------|---------|
| Any checker crashes | Stop; report stderr + input | Sonnet (T1) debug |
| Verdict contradicts known good (e.g., s7 suddenly PASS C3) | Stop; suspect code drift | Fable 5 (T0) review |
| t103 PASS C3b but novel Kodaira fiber | Escalate for decision | Fable 5 (T0) + Stream 2 tech lead |
| Multiple criteria marginal (borderline PASS/FAIL) | Escalate with memo | Fable 5 (T0) judgment call |

---

## Next Handoffs

- **If t103 FAIL (F1):** closed; documented in falsification log.
- **If t103 PASS C3b:** decision to add to Route B pool or table as "interesting but not prioritized" goes to T0.
- **Stream 1 (if t103 added):** new candidate for S1-04 (Sym² proof attempt).
- **Stream 3 (if pool expands):** t103 becomes an alternate for S3-00 MVM derivation (only if current s7 route hits a blocker).

---

**Assigned to:** Haiku 4.5  
**Est. duration:** 8–15 hrs (checker runs are fast; interpretation can escalate)  
**Blocker escalation:** Sonnet (T1) on first code crash; Fable 5 (T0) on decision
