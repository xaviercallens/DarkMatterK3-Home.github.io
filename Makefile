.PHONY: reproduce pipeline-tests guardrail-checks

# One-command reproduction from a clean checkout (CLAUDE.md Commands).
# Currently: synthetic-data pipeline only — gate G1 blocks real-data fetch
# until PREDICTION.md is pinned, so this target does not call fetch_data.py.
reproduce: guardrail-checks pipeline-tests

pipeline-tests:
	python3 -m pytest pipeline/tests/ -v

guardrail-checks:
	python3 scripts/check_tuning_log.py
	python3 scripts/check_tier_language.py
