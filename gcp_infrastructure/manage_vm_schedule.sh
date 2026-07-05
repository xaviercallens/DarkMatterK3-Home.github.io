#!/bin/bash
# ==============================================================================
# DarkMatterK3@Home - Cost Optimization Schedule Script
# ==============================================================================
# This script manages the lifecycle of the central GCP Compute Node to minimize 
# costs while still ensuring the dispatcher is available for at least 1 hour 
# per day to collect end-user browser contributions (GPU/CPU).
# ==============================================================================

PROJECT_ID="gen-lang-client-0625573011"
ZONE="europe-west1-b"
INSTANCE_NAME="darkmatter-k3-t4-node"

# 1. Start the VM
start_vm() {
    echo "[$(date)] Starting $INSTANCE_NAME..."
    gcloud compute instances start $INSTANCE_NAME --project=$PROJECT_ID --zone=$ZONE
    echo "[$(date)] $INSTANCE_NAME is now running."
}

# 2. Stop the VM
stop_vm() {
    echo "[$(date)] Stopping $INSTANCE_NAME to save costs..."
    gcloud compute instances stop $INSTANCE_NAME --project=$PROJECT_ID --zone=$ZONE
    echo "[$(date)] $INSTANCE_NAME is stopped."
}

# 3. Setup the Local Cron Schedule
setup_cron() {
    echo "Setting up cron schedule..."
    SCRIPT_PATH=$(realpath $0)
    
    # Backup existing crontab
    crontab -l > /tmp/current_cron 2>/dev/null || true
    
    # Remove any existing entries for this script to prevent duplicates
    grep -v "$SCRIPT_PATH" /tmp/current_cron > /tmp/new_cron
    
    # Add the new schedule:
    # - Start everyday at 08:00 AM
    # - Stop everyday at 10:00 AM (runs for exactly 2 hours)
    echo "0 8 * * * /bin/bash $SCRIPT_PATH start >> /tmp/darkmatter_vm_schedule.log 2>&1" >> /tmp/new_cron
    echo "0 10 * * * /bin/bash $SCRIPT_PATH stop >> /tmp/darkmatter_vm_schedule.log 2>&1" >> /tmp/new_cron
    
    crontab /tmp/new_cron
    rm /tmp/current_cron /tmp/new_cron
    
    echo "✅ Success! The central node will now automatically turn on at 08:00 AM and turn off at 10:00 AM daily."
    echo "This reduces compute costs by ~95% while keeping the project alive!"
}

case "$1" in
    start)
        start_vm
        ;;
    stop)
        stop_vm
        ;;
    setup-cron)
        setup_cron
        ;;
    *)
        echo "Usage: $0 {start|stop|setup-cron}"
        echo "  start       - Manually spin up the VM"
        echo "  stop        - Manually spin down the VM"
        echo "  setup-cron  - Configure the system to automatically run the VM for 1 hour/day"
        exit 1
esac
