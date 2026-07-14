#!/bin/bash

# Phase 5 Implementation - Browser WebAssembly Simulation
# This script simulates the HTTP sequence a browser WebAssembly/WebGPU worker
# would perform to fetch a chunk, process it, and submit the discovery,
# triggering the system and allowing you to monitor the contribution.

API_URL="http://127.0.0.1:8000"
USER_ID="browser_wasm_sim_01"
USERNAME="WASM_Test_Node"

echo "============================================================"
echo " PHASE 5 SIMULATION: Browser Worker Contribution"
echo "============================================================"

# 1. Register the browser user
echo -e "\n[1] Registering Browser Node..."
curl -s -X POST "$API_URL/users/register" \
     -H "Content-Type: application/json" \
     -d "{\"user_id\": \"$USER_ID\", \"username\": \"$USERNAME\"}" | jq

# 2. Request a Job Chunk
echo -e "\n[2] Requesting Job Chunk for Processing..."
JOB_RES=$(curl -s -X POST "$API_URL/jobs/request" \
     -H "Content-Type: application/json" \
     -d "{\"user_id\": \"$USER_ID\"}")

echo "$JOB_RES" | jq
JOB_ID=$(echo "$JOB_RES" | jq -r '.job_id')

if [ "$JOB_ID" == "null" ] || [ -z "$JOB_ID" ]; then
    echo "Error: Could not retrieve a job id."
    exit 1
fi

sleep 1

# 3. Submit the result (Simulating high Δ K3 asymmetry finding)
echo -e "\n[3] Submitting high-Delta WASM Job Result..."
curl -s -X POST "$API_URL/jobs/submit" \
     -H "Content-Type: application/json" \
     -d "{
           \"job_id\": \"$JOB_ID\",
           \"user_id\": \"$USER_ID\",
           \"wasserstein_distance\": 245.5,
           \"delta\": 5.82,
           \"s12\": 1.95,
           \"wasm_version_hash\": \"a1b2c3d4e5f6\",
           \"result_metadata\": {
               \"calc_time_seconds\": 1.25,
               \"mean_asymmetry\": 4.12,
               \"s12\": 1.95,
               \"s21\": 0.45,
               \"device\": \"WebAssembly/CPU\"
           }
         }" | jq

sleep 1

# 4. Submit the actual Browser Discovery (Phase 5B specific)
echo -e "\n[4] Submitting Browser Discovery for Python/T4 verification..."
curl -s -X POST "$API_URL/api/v1/discoveries/browser" \
     -H "Content-Type: application/json" \
     -d "{
           \"sector_id\": 42,
           \"delta\": 5.82,
           \"s12\": 1.95,
           \"s21\": 0.45,
           \"mean_asymmetry\": 4.12,
           \"max_asymmetry\": 8.91,
           \"author\": \"$USERNAME\"
         }" | jq

echo -e "\n============================================================"
echo " MONITORING AND VERIFICATION "
echo "============================================================"

# 5. Monitor Leaderboard
echo -e "\n[5] Checking Leaderboard..."
curl -s -X GET "$API_URL/leaderboard" | jq '.[] | select(.user_id=="WASM_Test_Node" or .user_id=="browser_wasm_sim_01")'

# 6. Monitor Latest Discoveries
echo -e "\n[6] Checking Latest Browser Discoveries..."
curl -s -X GET "$API_URL/api/v1/discoveries" | jq '.[:2]'

echo -e "\nDone! The local system (and T4 worker if polling the same job queues) can now see the browser node's contribution."
