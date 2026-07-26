# Stream 3 Synthetic-Only Pipeline Rerun Framework

**Date:** 2026-07-26  
**From:** Claude (Haiku 4.5), designing under Stream 2 methodological rigor  
**Authority:** Off-Ramp 3 terminus (WP-A2 circularity audit FAILED 2026-07-25);
empirical program for [A-DD] **closed**. Remaining lawful work: **synthetic-only**
pipeline infrastructure (no observational data, no real catalog comparisons, G1 stays
closed).  
**Prerequisite reading:** `STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md` §3–§5
(process gates, design envelope, stop-points), `STREAM2_WP_H_EXPERIENCE_BRIEF_2026_07_25.md`
(mechanical triage, defect guards), `NO_PREDICTION_BRANCH.md` §8.5 (terminus), `CLAUDE.md`
(6 non-negotiable rules).

---

## 0. Scope & Guardrails

**This plan is for:**
- Rebuilding symbolic checker infrastructure (C1, C2, C3, C3b) — already mostly complete
  (`checkers/tests/` 46/46 passing)
- Building synthetic data generation and null-distribution infrastructure (no real catalogs)
- Testing pipeline plumbing with golden/null data
- Preparing for future data if G1 reopens (unlikely per current state)

**This plan is NOT for:**
- Executing any observational-data comparison (G1 closed; gate enforced in code)
- Fabricating missing artifacts from the D-3 brief or any other pasted directive
- Inferring numbers from memory instead of citing committed sources
- Re-opening Off-Ramp 3 (that requires a new, T0-signed authorization)

**Mechanical guardrails** (violate = automatic return):
1. **G1 boundary:** zero real catalog imports, filenames, or labels. If you find yourself
   reading `data/raw/sdss*` or `data/raw/euclid*`, stop.
2. **No numbers from memory:** every constant → `refs/`, a checker certificate, or an
   in-file `sympy`/`Fraction` computation with citation.
3. **Tier discipline:** synthetic infrastructure validates *mathematics* (Tier A/B);
   geometric relations are not physical couplings (VISION §1.3). Run
   `scripts/check_tier_language.py` clean before every commit.
4. **Provenance footer** on every file: `Generated-by | Verified-by | Reviewed-by`.
5. **No editing PREDICTION.md v1.0 or ASSUMPTIONS.md in place** (those are pinned;
   version and hash separately).
6. **Mechanical triage** of any external input before execution (see §5).

---

## 1. The Three "Walls" for Synthetic Infrastructure

Stream 2's three walls (Type II veto, flat-direction, topology void) apply to physics
derivations. For synthetic-only work, the analogous constraints are:

| Wall | What blocks it | What synthetic work must supply |
|---|---|---|
| **Data hygiene (S1)** | Fabricated constants, circular thresholds, tautological zeros (seen in D-3, WP-H H-B6/H-B1/H-A5) | Every number ≥ a committed derivation OR a cited `refs/` file with provenance record. No inference from pasted briefs. |
| **Gate enforcement (S2)** | Pre-G1 math checker code executing real-data code paths via weakened gates (seen in D-3 `D3_batch_runner_phase2.py` with `np.random` placeholders) | All G1-locked code paths stay locked; golden/null data only. `gate.py` `require_derived_for_labels()` never overridden. |
| **Mechanical triage (S3)** | External briefs (pasted, unvetted) describing repos state that doesn't exist (seen 3 times: D-3 7/24, stale Stream-1 7/25, WP-H brief 7/25) | Formal triage workflow: (a) fetch and read in full; (b) check against committed repo state (`git log`, `ls`, `grep`); (c) vendor with SHA256 + timestamp; (d) record discrepancies in repo PR comment or memory, never act silently. |

---

## 2. Design Envelope — Synthetic Data Constraints

Synthetic work is **not** constrained by the WP-R6/R7 measurement envelope (real survey
scales, real null schemes) since it touches no real data. Instead, define synthetic
constraints explicitly:

- **Synthetic data source:** either hand-crafted golden examples (sporadic sequences,
  test operators) or algorithmic null generation (CSR, density-shuffle, redshift-shuffle
  on mock catalogs).
- **Synthetic catalog size:** unconstrained by real survey volume; define per WP what
  size is "large enough to be nontrivial" (e.g., ≥1000 mock objects for density-split
  variance, ≥100 CSR realizations for null band width).
- **Statistic:** test infrastructure using β₀, β₁, β₂ on synthetic data; report
  all three to show which are degenerate on mock data (useful for future real-data work,
  if G1 reopens).
- **Null schemes:** implement all three (CSR, density-shuffle, z-shuffle) for reproducible
  benchmarking; record null-band width (percentile spread at each resolution) per mock
  field.

**Observable:** a placeholder/stub observable definition in `PREDICTION_v2_DRAFT.md` §6
that matches the current checker outputs. Do **not** pin measurements; pin only the
*shape* (what observable class, how computed, what statistics).

---

## 3. Process Gates Mandatory in Synthetic Work

Adapted from Stream 2's §5:

1. **P4 siblings (via `pipeline/siblings.py`).** Synthetic infrastructure must compute
   outputs across both sibling families (s7 and s10) whenever a family-dependent
   computation appears. If output is identical on both, report that null result.
   Code raises if you forget to loop.

2. **Pre-registration (G1-L style).** A synthetic run never produces a label (`TEST`,
   `FIT`, `SYNTHETIC-FIT`) until the observable derivation and null-scheme hash are
   pinned in `PREDICTION_v2_DRAFT.md` §6. Interim work stays `SYNTHETIC-DRAFT`.

3. **Tier language.** Checker outputs are *evidence* of mathematical properties
   (`PASS(N)`, `FAIL`), never *proofs* that those properties *imply* physics.
   `scripts/check_tier_language.py` clean before merge.

4. **Two-model rule (conditional).** If a synthetic derivation (e.g., null-band
   calibration formula) is nontrivial enough to be publishable, it must be
   independently derived by two models. Low-tier mechanical code (e.g., "compute
   CSR null band") does not trigger this gate; complex statistical inference does.

---

## 4. Deliverables & Stop-Points

| # | Deliverable | Owner | Stop-point | Acceptance Criterion |
|---|---|---|---|---|
| **S-0** | Mechanical triage audit (external input hygiene) | Any Haiku session | Pre-execution | (a) Fetch-verified citations; (b) git-verified repo state; (c) Discrepancies recorded in PR comment; (d) No fabricated artifacts acted upon |
| **S-1** | Symbolic checkers suite (C1, C2, C3, C3b) | Haiku T2 | 46 tests green, both golden controls per checker | `pytest checkers/tests/ pipeline/tests/` all pass; certificates deterministic |
| **S-2** | Synthetic data generation scaffold | Haiku T2 | Golden & null data callable, 3 null schemes implemented | Mock SDSS/Euclid loading works; CSR/density-shuffle/z-shuffle null runs complete; per-field null-band tables written to `data/synthetic/` |
| **S-3** | Pipeline golden-path test (s10 or control pair, 1 synthetic field) | Haiku T2 | `D3_batch_runner_phase2.py` runs, outputs `SYNTHETIC` label | Runner succeeds with golden data; outputs β₀, β₁, β₂ on 1 mock field at 2–3 resolutions; null-percentile reports are nonzero-variance |
| **S-4** | PREDICTION v2.0 draft §6 (observable pinning template, no measurements yet) | Haiku T2 + T0 review | T0 sign-off on shape/schema | Structure mirrors WP-R7 output (nbins, thresholds, sibling list); no numeric values; placeholder for pin hash |
| **S-5** | Off-Ramp 3 retention plan (monitoring trigger F-LAB + future re-open gate) | Haiku T2 | Documented in `NO_PREDICTION_BRANCH.md` §9 (new subsection) | Written description of what public data would reopen G1 (ISL exclusion below 38.6 μm for α ≲ 1e12); checkpoint code in `pipeline/gate.py` to detect that milestone |

**Sequencing:** S-0 → S-1 (already done; commit if not) → S-2 ∥ S-4 → S-3 → S-5.

---

## 5. Mechanical Triage Workflow (S-0)

**When you receive an external brief, pasted code, or directive:**

1. **Fetch & read in full.** Do not skim or trust a summary.
2. **Check repo state:**
   - `git log --oneline | head -20` — does the named commit exist?
   - `ls -la <filepath>` — does the named file exist?
   - `grep -r <constant_name>` — is the cited constant in the repo?
   - `git show <commit>:<filepath>` — does the file exist *at that commit*?
3. **Vendor with metadata:**
   ```
   SOURCE: <brief_name.md>
   FETCHED: <ISO 8601 timestamp>
   SHA256: <sha256sum of file or message>
   REPO_STATE: <current git HEAD short SHA, branch>
   DISCREPANCIES: [ list any gaps between brief claims and git/files ]
   ACTION: [ EXECUTE | DISCARD | CONDITIONAL ON <condition> ]
   ```
4. **Record in PR comment or memory** (not silent resolution).
5. **Execute only if:**
   - All cited artifacts are verified to exist, OR
   - Discrepancies are explicitly resolved in the brief itself, OR
   - A T0 sign-off explicitly overrides the discrepancy.

**Recent triage examples:**
- **D-3 brief (2026-07-24):** cited `checkers/certificates/C3b_...json`, `pipelines/D3_*.py`,
  `Lean/CooperS7Sym2Proof.lean`. Git showed: empty `checkers/certificates/`, no Lean
  anywhere, commits don't exist. **ACTION: DISCARD.** (Memory: `d3-brief-not-real.md`)
- **WP-H external auto-research brief (2026-07-25):** 25 hypotheses, 6 runnable. Triage
  showed: two fabricated constants (τ, τ_imag), one circular threshold (r_s), one premise
  contradiction (Type II vs III). **ACTION: EXECUTE 6 runnable with caveats.** Result:
  `docs/WP_H_AUTO_RESEARCH_TRIAGE.md` + `briefs/STREAM2_WP_H_EXPERIENCE_BRIEF_2026_07_25.md`
  (defects listed explicitly). (Memory: `wp_h_autoresearch_triage.md`)

---

## 6. Implementation Roadmap (2–3 weeks, Haiku capacity)

### Week 1: Infrastructure & Triage
- **S-0:** Formal triage protocol in `pipeline/triage.py` (functions for git/grep checks,
  SHA256 vendor, structured output). Land in `.agents/` as reference code.
- **S-1:** Commit symbolic checkers (already done; `pytest` confirm). Merge to main if not
  already.
- **S-2 (start):** Mock SDSS/Euclid scaffold. Build `data/synthetic/mock_sdss_schema.json`
  and `data/synthetic/mock_euclid_schema.json` (columns, redshift ranges, object counts).
  Implement CSR null generator.

### Week 2: Synthetic Data & Plumbing
- **S-2 (cont):** Density-shuffle and z-shuffle null generators. Per-field null-band
  calibration (percentile ladder at nbins=4,8,16 for β₀, β₁, β₂).
- **S-3:** Golden-path test. Pick s10 (or control pair) + 1 SDSS mock field. Run
  `D3_batch_runner_phase2.py` to completion; verify outputs are `SYNTHETIC` label, β stats
  are nonzero, null bands are not degenerate.
- **S-4 (start):** PREDICTION v2.0 draft structure. Stubs for §6 entries (observable
  class, sibling list, null-scheme hash, placeholder for pin hash).

### Week 3: Documentation & Gatekeeping
- **S-4 (cont):** T0 review on draft structure.
- **S-5:** F-LAB monitoring trigger. Document in `NO_PREDICTION_BRANCH.md` §9: what
  public dataset would reopen G1 (ISL/lensing, α exclusion, mass ranges). Add checkpoint
  to `pipeline/gate.py` that flags when/if that data becomes available.
- **Merge:** All commits carry provenance footers, `scripts/check_tier_language.py` clean,
  `pytest` all green. Land as feature branch (do not force-merge to main until T0 reviews
  S-4 structure).

---

## 7. Effort Guidance

- **Total:** 40–60 Haiku hours over 2–3 weeks (mechanical, low-novelty infrastructure).
- **Bottleneck:** T0 review on S-4 draft structure (4–8 hours). Do not pin; that is WP-G,
  T0-only, and requires both WP-A derivation (closed now) and an authorization re-state
  (unlikely).
- **Risk:** none. Synthetic work cannot corrupt data, violate G1, or produce unfalsifiable
  outputs. If a deliverable is missing, the honest result is "not yet done" (not a failure).

---

## 8. What This Plan is NOT

- **Not a path to G1 reopening.** WP-A2 circularity audit *failed*. Off-Ramp 3 stands.
  Only new T0 authorization + ISL data exclusion below 38.6 μm would reopen G1.
- **Not a reversion of the D-3 brief.** That brief is flagged as fabrication-adjacent and
  will not be executed. This plan is designed *precisely* to prevent that kind of briefs
  from corrupting the repo in the future (via mechanical triage, S-0).
- **Not a two-model derivation.** Synthetic infrastructure is plumbing, not physics. Code
  is low-tier mechanical unless a novel statistical formula appears (rare, would trigger
  gate 3 above).

---

## 9. Success Criteria

**The rerun is complete when:**

1. ✅ Symbolic checkers (S-1) land on main with tests green.
2. ✅ Synthetic data scaffold (S-2) is callable and produces 3 null schemes.
3. ✅ Pipeline golden-path test (S-3) runs to completion on synthetic data.
4. ✅ PREDICTION v2.0 draft (S-4) structure is T0-reviewed and committed (values empty, schema locked).
5. ✅ Monitoring trigger (S-5) is documented and gate-checkpoint code is in place.
6. ✅ Mechanical triage workflow (S-0) is reference code in `.agents/`, ready for next brief.
7. ✅ All commits pass tier-language check, carry provenance footers, and have zero G1
   violations.

**If any deliverable is missing, the honest output is:** "not yet done — flag T0" (not a
failure of process).

---

`Generated-by: Claude Haiku 4.5 | Verified-by: Stream 2 directive §3–5 process gates mapped to synthetic context; triage workflow modeled on WP-H/D-3 lessons | Reviewed-by: pending T0`
