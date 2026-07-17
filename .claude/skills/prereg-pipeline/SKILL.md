---
name: prereg-pipeline
description: The pre-registration discipline for all empirical work in this repo — the V5 pipeline, data downloads, PTA/lensing/Lyman-alpha comparisons, and OBSERVATIONAL_REPORT.md. Use this skill for ANY task that touches data/, pipeline/, comparisons, plots, or result reporting — including "download the NANOGrav posteriors", "run the comparison", "add an observable", "make the exclusion plot", or "update the report". The audit trail lives in git; this skill is how it stays intact.
allowed-tools: Bash(python:*), Bash(pytest:*), Bash(sha256sum:*), Bash(git log:*), Bash(git status:*)
---

# Pre-Registered Pipeline (Stream 3)

The integrity mechanism of this entire stream is an ordering fact in git history:
**the hash-pinned `PREDICTION.md` commit predates every data-touching commit.**
Everything below protects that fact.

## Before writing ANY comparison code

1. Check the gate: `PREDICTION.md` must contain the `PINNED: <sha256>` header and its
   pin commit must predate your branch (`git log --follow PREDICTION.md`). If not pinned:
   the only permitted work is synthetic-data infrastructure (closure/null tests). Real
   data must not be touched — this is milestone gate G1.
2. If a task requires a model parameter not in the pinned `PREDICTION.md`, that is a
   tuning event: it goes to `TUNING_LOG.md` with date + justification, and every
   comparison using it is labeled `FIT`, not `TEST`, forever. No exceptions, including
   "it's obviously reasonable".

## Data discipline

- All datasets enter via `scripts/fetch_data.py` (idempotent, checksummed) and are
  recorded in `data/MANIFEST.md`: URL, release version, SHA256, retrieval date. Files
  under `data/raw/` are immutable — the hook blocks edits; corrections happen by
  fetching a new version with a new manifest entry.
- We compare against **published public products** (e.g., NANOGrav 15-yr / EPTA DR2
  free-spectrum posteriors, published stacked lensing profiles). Never phrase results
  as collaboration, submission, or endorsement.

## Pipeline rules

1. Pipeline reads model parameters from the pinned `PREDICTION.md` block — no free
   knobs, no CLI overrides of physics parameters.
2. Every comparison output carries a `label: TEST | FIT` field, set mechanically
   (TEST iff all parameters trace to the pin and no TUNING_LOG entry touches them).
3. **Closure + null tests are merge-blocking:** on synthetic data with injected signal,
   the pipeline recovers it within stated tolerance; on null synthetic data, it reports
   null at the stated false-positive rate. Both run in CI on every pipeline change.
4. Branch triggers are mechanical: an exclusion crossing the pre-stated threshold
   (≥3σ for F3; the pinned criterion for F4) auto-inserts the branch entry into the
   report draft. You do not get to reinterpret a trigger; only a T0 session can, in
   writing, and the default is that it stands.

## Reporting

- Results tables in `OBSERVATIONAL_REPORT.md` are machine-generated
  (`scripts/render_results.py`); prose interprets, never introduces numbers.
- Exclusions and nulls get the same prominence as positive results — a clean exclusion
  is a success of the program, not a failure to be buried.
- Interpretation prose is T0-only (EXECUTION_PLAN §4 S3-05): draft tables + a stub
  section, flag for the orchestrator session.

## Definition of done (any WP here)

- One-command reproduction from clean checkout (`make reproduce` or documented equivalent).
- Manifest checksums verify; closure/null CI green; every comparison labeled.
- Pre-registration audit intact: `git log` ordering pin → data → results.
