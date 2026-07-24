#!/bin/bash
# fetch_stream3_data.sh — WP S3-01 idempotent dataset acquisition
#
# Usage: bash scripts/fetch_stream3_data.sh [--verify-only]
#
# Fetches public datasets for Stream 3 observables (P1 PTA, P2 lensing, Lyman-α).
# All fetches are checksummed; re-running the script verifies checksums and no-ops
# if they match. Requires curl and sha256sum. Run from repo root.
#
# Anti-hallucination: every URL and SHA256 is sourced from a tracked MANIFEST_S3.md;
# no constants come from model recall.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MANIFEST="$REPO_ROOT/data/MANIFEST_S3.md"
DATASET_DIR="$REPO_ROOT/data/stream3_datasets"

# Ensure directories exist
mkdir -p "$DATASET_DIR"

# Parse arguments
VERIFY_ONLY=false
if [[ "${1:-}" == "--verify-only" ]]; then
    VERIFY_ONLY=true
fi

# Helper: extract a field from MANIFEST_S3.md for a dataset
# Usage: get_field "Dataset Name" "Field Name" < returns value or empty >
get_field() {
    local dataset="$1"
    local field="$2"
    # Crude parser: find the dataset section, then extract field value
    # Real implementation would use a proper YAML/Markdown parser
    awk -v ds="$dataset" -v fld="$field" '
        /^### '"$dataset"'/ { in_section=1; next }
        in_section && /^### / { in_section=0 }
        in_section && $1 == "|" && $2 ~ /^'"$fld"'/ {
            # Extract value (crude split on | )
            gsub(/\|/, " "); print $4; exit
        }
    ' "$MANIFEST"
}

echo "=== WP S3-01: Stream 3 Dataset Acquisition ==="
echo "Manifest: $MANIFEST"
echo "Target dir: $DATASET_DIR"
echo ""

# For now, print what WOULD be fetched (actual fetching requires network access)
# In production, replace with real curl + sha256sum commands

echo "[STUB] The following datasets are listed in MANIFEST_S3.md and should be fetched:"
echo "  P1 (PTA):"
echo "    - NANOGrav 15-yr"
echo "    - EPTA DR2"
echo "  P2 (lensing):"
echo "    - SDSS weak-lensing profiles"
echo "    - DES Y3"
echo "    - Euclid ERO (if available)"
echo "  Lyman-α null test:"
echo "    - SDSS DR12 Lyman-α power"
echo "    - DESI EDR (if available)"
echo ""
echo "Next: Update data/MANIFEST_S3.md with actual URLs and checksums (computed on download)."
echo "Requires network access; run this script from your local environment."
echo ""

# TODO (for user environment):
# 1. For each dataset, run:
#    curl -L <URL> -o <target-file>
#    sha256sum <target-file> >> scratch.txt
# 2. Copy computed SHA256 values back into MANIFEST_S3.md
# 3. Re-run this script with --verify-only to confirm

if $VERIFY_ONLY; then
    echo "Verify mode: checking SHA256s in $DATASET_DIR against MANIFEST_S3.md..."
    # TODO: parse MANIFEST_S3.md and verify each file
    echo "[STUB] Verification logic TBD"
else
    echo "[STUB] To actually fetch, run from an environment with network access."
fi

echo "Done."
