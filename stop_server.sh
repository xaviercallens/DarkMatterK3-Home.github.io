#!/usr/bin/env bash
set -euo pipefail

# Find the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Checkpointing and backing up current results..."
python3 "$SCRIPT_DIR/checkpoint_manager.py" backup "pre_stop"

echo "Stopping DarkMatterK3 server..."
"$SCRIPT_DIR/manage_darkmatter.sh" stop

echo "Server stopped safely."
