.PHONY: reproduce pipeline-tests guardrail-checks experiments experiments-quick

# One-command reproduction from a clean checkout (CLAUDE.md Commands).
# Currently: synthetic-data pipeline only — gate G1 blocks real-data fetch
# until PREDICTION.md is pinned, so this target does not call fetch_data.py.
reproduce: guardrail-checks pipeline-tests

pipeline-tests:
	python3 -m pytest pipeline/tests/ -v

# Run full parametric exploration and dual-scale analysis suite
# Logs to logs/experiments.json and auto-generates OBSERVATIONAL_REPORT.md
experiments:
	python3 scripts/run_experimentation_suite.py

# Quick experimentation (fewer trials, for fast iteration)
experiments-quick:
	python3 scripts/run_experimentation_suite.py --quick

guardrail-checks:
	python3 scripts/check_tuning_log.py
	python3 scripts/check_tier_language.py
