# Real-Data Verification Startup — WP-R Series Kickoff

**Date:** 2026-07-25  
**Authority:** Fable 5 (T0-delegated); plan written by Fable 5  
**Executor:** Claude Haiku 4.5 (T2 mechanical work)  
**Governing docs:** `HAIKU_PLAN_REALDATA_VERIFICATION_2026_07_25.md` (master plan), `CLAUDE.md` (6 hard rules), `NO_PREDICTION_BRANCH.md` (context), `LESSONS_LEARNED.md` (failure modes)

---

## Context & Scope

**The situation:** PREDICTION.md is pinned (2026-07-24), real data fetched (SDSS + Euclid, 2026-07-25), but gate G1-L is **closed** — no derived observable exists to test (`NO_PREDICTION_BRANCH.md`, F5b triggered). Experimentation cannot run.

**The opportunity:** Real data legitimately enables five engineering tasks — **none of which are physics tests:**
1. Re-verify that certified mathematics still holds (regression safety)
2. Characterize what real data actually contains
3. Validate data-handling machinery survives real-world conditions
4. Build realistic null distributions from actual survey structure
5. Construct infrastructure for sibling-family controls (P4 discipline)

**Hard blocker:** Euclid public data does **not** include weak-lensing shear; only morphological ellipticity (MER catalogue). Therefore `κ-peak` machinery stays synthetic-only. (Finding R-SHEAR, recorded.)

**No WP-R output carries `TEST` or `FIT` labels.** Everything is `SYNTHETIC` or `ENGINEERING`.

---

## WP-R Series Sequence

| WP | Task | Data | Complexity | Est. | Blocker if fail? |
|----|------|------|------------|------|-----------------|
| **R0** | Re-verify math checkers (no data needed) | — | Trivial | 15 min | YES — abort series |
| **R1** | Real-data integrity scan + summary stats | SDSS + Euclid | Low | 2 hrs | YES — diagnose data corruption |
| **R2** | Test photo-z/spectro redshift matching | SDSS spec + Euclid photo-z | Low | 3 hrs | YES — if no joinable 3D positions |
| **R3** | Construct real density field (3D Voronoi) | Redshifts from R2 | Medium | 6 hrs | Non-blocking; defer if time tight |
| **R4** | Compute Betti numbers / topology invariants | Density field from R3 | Medium | 8 hrs | Non-blocking; infrastructure only |
| **R5** | Sibling-family control harness (P4) | Synthetic + real catalogs | Medium | 10 hrs | Non-blocking; not data-critical |

**Stopping rule:** If R0 fails OR R1 finds data corruption, stop and escalate. Otherwise, proceed depth-first (R0 → R1 → R2 → R3 → R4/R5 in parallel).

---

## Hard Rules (Every WP Must Follow)

1. **Never pin.** No `PINNED:` / `DERIVED:` headers written or modified.
2. **Never label.** No output `TEST` or `FIT`. Gate enforces it; do not work around.
3. **No memory numbers.** Every constant has a source: certificate JSON, committed file, or `data/MANIFEST.md`.
4. **Never re-fetch to fix.** Checksum failure = report + escalate; never silently re-download.
5. **No synthetic fallback.** Missing data → stop and flag; never substitute random values.
6. **No deprecated code.** Do NOT run `D3_batch_runner_phase2.py`; do NOT import QUARANTINED files (see `LEGACY_CODE_DISPOSITION_2026_07_25.md`).
7. **Tier language audit.** Run `python3 scripts/check_tier_language.py` before every commit; must print 0 violations.
8. **Provenance footer.** Every generated file: `Generated-by | Verified-by | Reviewed-by` in footer.

---

## What Success Looks Like

✅ **R0 PASS:** Math checkers reproduce committed verdicts; confidence that Stream 1/2 foundation is solid.  
✅ **R1 PASS:** Real SDSS/Euclid catalogs load; checksums match; data structure characterized; no silent corruption.  
✅ **R2 PASS:** Photo-z and spectroscopic redshifts can be matched on 3D position; joinable row counts recorded.  
✅ **R3 PASS:** Density field built from 3D positions; Voronoi mesh computes without crashes; structure is reasonable.  
✅ **R4 PASS:** Betti numbers computed from synthetic control; real-data Betti numbers computed without crashing.  
✅ **R5 PASS:** P4 control harness instantiated; can load sibling geometries and compute dummy statistics.

**Each WP produces a short report (<300 words) + tables + one or two plots if applicable.**

---

## Critical Findings That Block Progression

| Finding | Code | Action |
|---------|------|--------|
| Math checker verdict differs from committed matrix | R0-FAIL | Stop. Escalate to Fable 5 (code drift suspected). |
| SDSS/Euclid CSV checksum mismatch | R1-CORRUPT | Stop. Escalate to compute ops (data corruption). |
| Photo-z/spec-z matching rate < 50% in overlap region | R2-NOMATCH | Escalate; may defer or retry with looser ra/dec tolerance. |
| Density field Voronoi fails to converge | R3-NUMERICS | Escalate; may indicate catalog boundary issues. |
| R-SHEAR (no public shear catalogue) confirmed again | R-SHEAR | Non-blocking; documented constraint; κ-peak stays synthetic. |

---

## Execution Checklist

- [ ] Read `HAIKU_PLAN_REALDATA_VERIFICATION_2026_07_25.md` in full (master plan § 1–§ 6 covers R0–R5 in detail)
- [ ] Verify repo is clean: `git status` clean
- [ ] Confirm data on external disk: `ls -l /mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/`
- [ ] Confirm `data/MANIFEST.md` lists all expected datasets with SHA256
- [ ] Run `python3 scripts/check_tier_language.py` on current codebase; should print 0 violations
- [ ] Start with WP-R0 (read instructions in master plan)

---

## Token Budget & Pacing

- Each WP session: read only files named by the master plan; no repo exploration.
- Do not read raw CSVs in full (>14k rows); use pandas/astropy summaries.
- Report: ~300 words + tables + findings.
- One WP per session where possible.
- If a WP blocks, stop and file an escalation; do not attempt next WP.

---

## Escalation Contacts

| Issue | Contact | Via |
|-------|---------|-----|
| Code crashes / unexpected errors | Sonnet (T1) | Slack / direct brief |
| Math checker verdicts drift | Fable 5 (T0) | Escalation memo + code diff |
| Data integrity / infrastructure | Xavier (T0) + compute ops | Formal incident report |
| Deciding whether to skip non-blocking WP | Fable 5 (T0) | Brief after R2/R3 complete |

---

**Master plan location:** `briefs/HAIKU_PLAN_REALDATA_VERIFICATION_2026_07_25.md` (read WPs R0–R5 §1 before starting)  
**Status tracking:** Update this file after each WP with date + pass/fail + escalations  
**Assigned to:** Haiku 4.5  
**Start date:** 2026-07-25 (immediately after commit)  
**Target completion:** WP-R0/R1 by 2026-07-26; R2–R5 by 2026-07-27 (if no blockers)
