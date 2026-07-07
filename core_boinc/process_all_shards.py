# core_boinc/process_all_shards.py
import os
import subprocess
import time

CDIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CDIR)
os.chdir(BASE_DIR)

WORKUNIT_DIR = "core_boinc/workunits"
RESULTS_DIR = "core_boinc/results"
BINARY_PATH = "core_boinc/dark3_s12_sieve"

os.makedirs(RESULTS_DIR, exist_ok=True)

# Find all shards
shards = [f for f in os.listdir(WORKUNIT_DIR) if f.endswith("_input.txt")]
print(f"🌌 BOEINC Batch Processing Engine: Found {len(shards)} shards to process.")

for shard in sorted(shards):
    shard_id = shard.replace("_input.txt", "")
    shard_path = os.path.join(WORKUNIT_DIR, shard)
    print(f"\n🚀 [PROCESSING] Shard: {shard_id}")
    
    is_raw = "raw" in shard
    cmd = [BINARY_PATH, shard_path]
    if is_raw:
        cmd.append("--raw")
         
    print(f"   Executing: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    
    # Check if receipt exists
    receipt_src = "receipt_boinc.txt"
    if os.path.exists(receipt_src):
        receipt_dst = os.path.join(RESULTS_DIR, f"{shard_id}_receipt.txt")
        os.rename(receipt_src, receipt_dst)
        print(f"   ✓ Generated and archived receipt: {receipt_dst}")
    else:
        print(f"   [ERROR] receipt_boinc.txt not found for {shard_id}!")

# Run Bridge Sync
print("\n🔄 [SYNC] Executing Federated Bridge Daemon Sync...")
bridge_cmd = ["python3", "core_boinc/boinc_bridge_daemon.py", "--single-run"]
subprocess.run(bridge_cmd, check=True)

print("\n🏆 Batch processing and ledger synchronization completed successfully!")
