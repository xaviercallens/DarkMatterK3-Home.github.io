#!/usr/bin/env bash
set -euo pipefail

# Find the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Starting DarkMatterK3 Automated Daily Orchestrator..."
mkdir -p "$SCRIPT_DIR/logs"

# Execute the daily orchestrator. It baselines stats, emails startup, runs the pipelines, stops them, pushes results, emails metrics, and powers off.
python3 "$SCRIPT_DIR/core/daily_orchestrator.py" >> "$SCRIPT_DIR/logs/daily_orchestration.log" 2>&1
