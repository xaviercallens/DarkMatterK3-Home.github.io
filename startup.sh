#!/usr/bin/env bash
set -euo pipefail

# Find the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Starting DarkMatterK3 server for processing and data collection..."
"$SCRIPT_DIR/manage_darkmatter.sh" start

echo "Startup complete. Services are running in the background."
