#!/usr/bin/env bash
set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="$SCRIPT_DIR/backups"
ARCHIVE_DIR="$SCRIPT_DIR/archives"
GCS_BUCKET="gs://your-gcs-bucket-name/darkmatter-backups"

mkdir -p "$ARCHIVE_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ARCHIVE_NAME="darkmatter_backups_${TIMESTAMP}.tar.gz"
ARCHIVE_PATH="$ARCHIVE_DIR/$ARCHIVE_NAME"

echo "Creating archive of backups at $ARCHIVE_PATH..."
tar -czf "$ARCHIVE_PATH" -C "$SCRIPT_DIR" backups

echo "Uploading archive to Google Cloud Storage ($GCS_BUCKET)..."
if command -v gsutil &> /dev/null; then
    gsutil cp "$ARCHIVE_PATH" "$GCS_BUCKET/"
    echo "Archive successfully uploaded."
elif command -v gcloud &> /dev/null; then
    gcloud storage cp "$ARCHIVE_PATH" "$GCS_BUCKET/"
    echo "Archive successfully uploaded."
else
    echo "Error: Neither 'gsutil' nor 'gcloud' command found. Please install the Google Cloud SDK."
    exit 1
fi
