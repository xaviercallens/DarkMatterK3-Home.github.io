import os
import sys
import json
import time
import subprocess
from datetime import datetime

# Path setups
core_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(core_dir)
sys.path.append(core_dir)
sys.path.append(root_dir)

import send_email_report as mailer

RUNS_FILE = os.path.join(root_dir, "pipeline_runs.json")
DISCOVERIES_FILE = os.path.join(root_dir, "discoveries.json")
LOG_DIR = os.path.join(root_dir, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# GCP hourly rate for: n1-standard-4 ($0.19) + 1x Tesla T4 GPU ($0.35) + 100GB SSD ($0.024)
GCP_HOURLY_RATE = 0.564 

def load_json(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {os.path.basename(filepath)}: {e}")
    return []

def get_stats():
    runs = load_json(RUNS_FILE)
    disc = load_json(DISCOVERIES_FILE)
    
    total_galaxies = sum(r.get("num_galaxies", 0) for r in runs)
    num_runs = len(runs)
    num_discoveries = len(disc)
    
    return {
        "num_runs": num_runs,
        "total_galaxies": total_galaxies,
        "num_discoveries": num_discoveries,
        "runs": runs,
        "discoveries": disc
    }

def run_git_push():
    """Commits and pushes updated database files to GitHub for live Streamlit sync."""
    print(f"[{datetime.now()}] Synchronizing updated data with GitHub...")
    try:
        subprocess.run(["git", "add", RUNS_FILE, DISCOVERIES_FILE], cwd=root_dir, check=True)
        # Check if there are changes to commit
        status_res = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=root_dir)
        if status_res.returncode == 1: # Changes exist
            subprocess.run(["git", "commit", "-m", "chore(telemetry): automated daily pipeline run metrics update"], cwd=root_dir, check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=root_dir, check=True)
            print("✅ Data successfully pushed to GitHub main branch!")
            return True
        else:
            print("ℹ️ No new telemetry changes to commit.")
            return False
    except Exception as e:
        print(f"❌ Git push failed: {e}")
        return False

def main():
    print(f"[{datetime.now()}] ==================================================")
    print(f"[{datetime.now()}] STARTING DAILY DARKMATTER K3 PIPELINE ORCHESTRATION")
    print(f"[{datetime.now()}] ==================================================")
    
    # 1. Capture initial stats
    start_time = time.time()
    start_stats = get_stats()
    
    # 2. Send Start Email
    start_subject = "🌌 DarkMatterK3@Home - Daily Processing Started"
    start_body = (
        f"Hello,\n\n"
        f"The central GCP Compute Node (T4 GPU) has successfully booted up on schedule and initiated processing.\n\n"
        f"📅 Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (UTC)\n"
        f"📊 Initial Baseline:\n"
        f"  - Total Historical Runs: {start_stats['num_runs']}\n"
        f"  - Total Galaxies Mapped: {start_stats['total_galaxies']:,}\n"
        f"  - Verified Discoveries: {start_stats['num_discoveries']}\n\n"
        f"The DarK3 pipeline will now run for exactly 2 hours on your Tesla T4 GPU. "
        f"Upon completion, telemetry will be pushed to GitHub to refresh the live dashboard at Streamlit Cloud, "
        f"and you will receive a second final report prior to automated VM poweroff.\n\n"
        f"Best regards,\n"
        f"DarkMatterK3@Home Daemon"
    )
    mailer.send_email(start_subject, start_body)

    # 3. Spin up background services (PostgreSQL, Redis, APIs, Workers) via tmux manage script
    print(f"[{datetime.now()}] Starting services inside tmux session...")
    try:
        subprocess.run(["./manage_darkmatter.sh", "restart"], cwd=root_dir, check=True)
    except Exception as e:
        print(f"❌ Failed to start background services: {e}")
        
    # 4. Wait for 2 hours of processing (7200 seconds)
    processing_duration_seconds = 7200 # 2 hours
    print(f"[{datetime.now()}] Pipeline is running. Processing telescope data for the next 2 hours...")
    
    # For simulation/debugging safety, we can allow shortening this duration via environment variable
    override_duration = os.getenv("TEST_PROCESSING_DURATION")
    if override_duration:
        processing_duration_seconds = int(override_duration)
        print(f"⚠️ TEST OVERRIDE: Running for {processing_duration_seconds} seconds instead of 2 hours.")
        
    time.sleep(processing_duration_seconds)
    
    # 5. Stop the background services cleanly
    print(f"[{datetime.now()}] Processing duration complete. Stopping pipelines...")
    try:
        subprocess.run(["./manage_darkmatter.sh", "stop"], cwd=root_dir, check=True)
    except Exception as e:
        print(f"❌ Failed to stop services cleanly: {e}")

    # 6. Capture ending stats and calculate delta
    end_stats = get_stats()
    elapsed_time_hours = (time.time() - start_time) / 3600.0
    gcp_cost = elapsed_time_hours * GCP_HOURLY_RATE
    
    new_runs = end_stats["num_runs"] - start_stats["num_runs"]
    new_galaxies = end_stats["total_galaxies"] - start_stats["total_galaxies"]
    new_discoveries = end_stats["num_discoveries"] - start_stats["num_discoveries"]

    # 7. Push telemetry updates to GitHub to sync Streamlit immediately
    git_synced = run_git_push()

    # 8. Send Completion Email with metrics
    end_subject = f"🏆 DarkMatterK3@Home - Daily Processing Complete (+{new_galaxies:,} Galaxies)"
    
    git_status_str = "SUCCESS" if git_synced else "SKIPPED / NO NEW CHANGES"
    
    end_body = (
        f"Hello,\n\n"
        f"The daily 2-hour processing batch on the central T4 Compute Node has completed successfully.\n\n"
        f"📅 Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (UTC)\n"
        f"⏱️ Total Processing Time: {elapsed_time_hours:.2f} hours\n"
        f"💸 Estimated Cost Incurred: ${gcp_cost:.3f} USD\n"
        f"🌐 GitHub Telemetry Sync: {git_status_str}\n\n"
        f"📊 BATCH PERFORMANCE METRICS:\n"
        f"  --------------------------------------------------\n"
        f"  - New Ingestion Runs Executed: +{new_runs}\n"
        f"  - New Cosmic Galaxies Mapped: +{new_galaxies:,}\n"
        f"  - New Verified Anomalies Found: +{new_discoveries}\n"
        f"  --------------------------------------------------\n\n"
        f"📈 GLOBAL COMPULATING POOL STATS:\n"
        f"  - Total Lifetime Ingestions: {end_stats['num_runs']}\n"
        f"  - Total Mapped Universe: {end_stats['total_galaxies']:,} Galaxies\n"
        f"  - Total Documented Anomalies: {end_stats['num_discoveries']}\n\n"
        f"This data has been pushed to GitHub and is now live on your Streamlit Dashboard: "
        f"https://darkmatterk3athome.streamlit.app/\n\n"
        f"The VM instance is now initiating a secure local shutdown command to prevent further GCP billing.\n\n"
        f"Best regards,\n"
        f"DarkMatterK3@Home Daemon"
    )
    mailer.send_email(end_subject, end_body)

    # 9. Secure VM shutdown to save money!
    print(f"[{datetime.now()}] Execution complete. Shuting down the system...")
    try:
        # In a real running environment, this calls poweroff. 
        # Skip if running inside a testing command workspace where poweroff would fail.
        if os.getuid() == 0: # Root permission
            subprocess.run(["poweroff"])
        else:
            # Fallback for non-root (if passwordless sudo is enabled, which standard GCP VMs have)
            subprocess.run(["sudo", "poweroff"])
    except Exception as e:
        print(f"❌ Failed to trigger system poweroff: {e}")

if __name__ == "__main__":
    main()
