#!/usr/bin/env bash
# ==============================================================================
# 🌌 DarkMatterK3@Home BOEINC Client/Server Loop Automation (1 Hour Run)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
os_seconds=3600 # 1 hour run duration

echo -e "🚀 Starting 1-hour continuous BOEINC processing loop..."
echo -e "Base directory: $BASE_DIR"
echo -e "Processing will run in background for 1 hour (3600 seconds)."

START_TIME=$(date +%s)
END_TIME=$((START_TIME + os_seconds))

iteration=1

while [ "$(date +%s)" -lt "$END_TIME" ]; do
    CURRENT_TIME=$(date +%s)
    REMAINING=$((END_TIME - CURRENT_TIME))
    REMAINING_MIN=$((REMAINING / 60))
    
    echo -e "\n=========================================================="
    echo -e "🌟 [ITERATION $iteration] Starting loop sequence. Time remaining: ${REMAINING_MIN} minutes."
    echo -e "=========================================================="
    
    # 1. Generate new workunit shards (SDSS and Euclid raw/cartesian)
    echo -e "👉 [STEP 1/3] Spawning new BOEINC coordinate shards..."
    python3 "$BASE_DIR/core_boinc/boinc_work_generator.py"
    
    # 2. Process all shards with OpenMP HPC solver and generate verification receipts
    echo -e "👉 [STEP 2/3] Processing workunits using native C++ dark3_s12_sieve client..."
    python3 "$BASE_DIR/core_boinc/process_all_shards.py"
    
    # 3. Clean up processed results to prevent piling up of raw text files while keeping ledger updated
    echo -e "👉 [STEP 3/3] Archiving raw shard text files to keep storage clean..."
    find "$BASE_DIR/core_boinc/workunits/" -name "*_input.txt" -type f -delete || true
    
    echo -e "✓ Iteration $iteration complete. Sleeping for 180 seconds..."
    iteration=$((iteration + 1))
    
    # Sleep 3 minutes before the next batch sequence (giving ample time for results to stream in)
    sleep 180
done

echo -e "\n🏆 Continuous 1-hour simulation run completed successfully!"
