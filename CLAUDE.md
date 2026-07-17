# CLAUDE.md — Stream 3: Experimentation

Empirical confrontation repo. Governing docs: `VISION.md` §3–§4, `EXECUTION_PLAN.md` §4,
pinned `PREDICTION.md`. Read the **prereg-pipeline** skill before touching data/, pipeline/,
or any comparison; **epistemic-guardrails** for all prose.

## Commands
- Fetch data: `python scripts/fetch_data.py` (only entry point for datasets; updates data/MANIFEST.md)
- Pipeline tests: `pytest pipeline/tests/` (closure + null tests; merge-blocking)
- Full reproduction: `make reproduce` (one command, clean checkout)
- Results tables: `python scripts/render_results.py`

## Non-negotiable rules
1. No real-data comparison code before `PREDICTION.md` carries `PINNED:` (gate G1). Synthetic-data infra only.
2. Pinned prediction and `data/raw/` are immutable (hook-enforced). Parameter changes → `TUNING_LOG.md` → label FIT.
3. Every comparison output labeled `TEST` or `FIT`, mechanically.
4. Public data products only; never phrase results as collaboration/submission/endorsement.
5. Falsification triggers (F3/F4) are mechanical; overriding one requires a written T0 ruling.
6. Interpretation prose in OBSERVATIONAL_REPORT.md is T0-only — draft tables + stub, then flag.
