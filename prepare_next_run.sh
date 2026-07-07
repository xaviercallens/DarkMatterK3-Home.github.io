#!/usr/bin/env bash
# ==============================================================================
# 🚀 prepare_next_run.sh - DarkMatterK3@Home Research Preparation Script
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "\033[1;36m====================================================================\033[0m"
echo -e "\033[1;35m🛸 DARKMATTERK3@HOME: PREPARATION PIPELINE FOR THE NEXT RUN\033[0m"
echo -e "\033[1;36m====================================================================\033[0m"

# 1. Clean up stale logs and temp files
echo -e "\033[1;32m[STEP 1/4] Clearing stale local runtime artifacts...\033[0m"
rm -f "$SCRIPT_DIR/core_boinc/receipt_boinc.txt"
rm -rf "$SCRIPT_DIR/core_boinc/workunits/*"
echo -e "  \033[1;32m✓ Stale workunits and receipt cleared.\033[0m"

# 2. Re-compile native client with maximum speedup flags
echo -e "\n\033[1;32m[STEP 2/4] Triggering hardware-native C++ solver compilation...\033[0m"
if [ -f "$SCRIPT_DIR/core_boinc/speedup_next_run.sh" ]; then
    bash "$SCRIPT_DIR/core_boinc/speedup_next_run.sh"
else
    echo -e "  \033[1;33m⚠️ Warning: core_boinc/speedup_next_run.sh not found. Compiling manually...\033[0m"
    g++ -O3 -march=native -ffast-math -funroll-loops -fopenmp -o "$SCRIPT_DIR/core_boinc/dark3_s12_sieve" "$SCRIPT_DIR/core_boinc/src/main.cpp"
    echo -e "  \033[1;32m✓ Manual compilation complete.\033[0m"
fi

# 3. Generate a fresh set of coordinate shards
echo -e "\n\033[1;32m[STEP 3/4] Running optimized vectorized work generator to slice catalogs...\033[0m"
python3 "$SCRIPT_DIR/core_boinc/boinc_work_generator.py"

# 4. Display Quickstart Instructions
echo -e "\033[1;32m[STEP 4/4] Next-Run environment is completely configured!\033[0m"
echo -e "\n\033[1;33m📋 QUICKSTART LAUNCH GUIDE:\033[0m"
echo -e "  1. To start the background daemons (FastAPI + Streamlit + Workers):"
echo -e "     \033[1;34m./manage_darkmatter.sh start\033[0m"
echo -e "  2. To monitor real-time progress of the BOEINC client loop:"
echo -e "     \033[1;34m./manage_darkmatter.sh attach\033[0m (Switch to window 4: BOEINC-Loop)"
echo -e "  3. To run a quick 10-second end-to-end integration test:"
echo -e "     \033[1;34mpython3 core_boinc/test_boinc_suite.py\033[0m"
echo -e "  4. To stop and archive the entire system at any time:"
echo -e "     \033[1;34m./stop_server.sh\033[0m"

echo -e "\033[1;36m====================================================================\033[0m"
echo -e "\033[1;32m🎉 PREPARATION PIPELINE COMPLETED SUCCESSFULLY! READY FOR DISCOVERY.\033[0m"
echo -e "\033[1;36m====================================================================\033[0m"
