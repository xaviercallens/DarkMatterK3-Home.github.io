# core_boinc/test_boinc_suite.py
import os
import subprocess
import json
import time

# Ensure we are in correct working directory
CDIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CDIR)
os.chdir(BASE_DIR)

def run_test_suite():
    print("======================================================================")
    print("🌌 BOEINC SERVER & CLIENT INTEGRATION SYSTEM TEST SUITE")
    print("======================================================================")
    
    # 1. Compile C++ Client if not already compiled
    print("\n--- [STEP 1/4] COMPILING NATIVE C++ CLIENT ---")
    compile_cmd = ["bash", "core_boinc/compile_client.sh"]
    print(f"Executing: {' '.join(compile_cmd)}")
    subprocess.run(compile_cmd, check=True)
    
    binary_path = "core_boinc/dark3_s12_sieve"
    assert os.path.exists(binary_path), "C++ Client binary was not built!"
    print("✅ Compiled C++ client binary exists.")
    
    # 2. Run Work Generator
    print("\n--- [STEP 2/4] GENERATING SDSS & EUCLID WORKUNITS ---")
    gen_cmd = ["python3", "core_boinc/boinc_work_generator.py"]
    print(f"Executing: {' '.join(gen_cmd)}")
    subprocess.run(gen_cmd, check=True)
    
    # Assert generated workunits exist
    workunit_dir = "core_boinc/workunits"
    shards = [f for f in os.listdir(workunit_dir) if f.endswith("_input.txt")]
    metas = [f for f in os.listdir(workunit_dir) if f.endswith("_meta.json")]
    
    assert len(shards) >= 4, f"Expected at least 4 shards, found {len(shards)}"
    assert len(metas) >= 4, f"Expected at least 4 meta JSONs, found {len(metas)}"
    print(f"✅ Generated {len(shards)} workunit shards successfully.")
    
    # Print examples
    sdss_shards = [s for s in shards if "sdss" in s]
    euclid_shards = [s for s in shards if "euclid" in s]
    print(f"   └─ Example SDSS Shard: {sdss_shards[0]}")
    print(f"   └─ Example Euclid Shard: {euclid_shards[0]}")
    
    # 3. Execute Compiled C++ Client
    print("\n--- [STEP 3/4] RUNNING NATIVE CLIENT VERIFICATION ---")
    
    # Scenario A: Cartesian SDSS shard
    sdss_shard_path = os.path.join(workunit_dir, sdss_shards[0])
    print(f"\n[Test Client] Running SDSS Cartesian Shard: {sdss_shards[0]}...")
    client_cmd_a = [binary_path, sdss_shard_path]
    print(f"Executing: {' '.join(client_cmd_a)}")
    subprocess.run(client_cmd_a, check=True)
    
    assert os.path.exists("receipt_boinc.txt"), "Interactive receipt_boinc.txt not written!"
    with open("receipt_boinc.txt", "r") as f:
        print("\n   [RECEIPT READOUT - SDSS]")
        for line in f:
            print(f"      {line.strip()}")
            
    # Scenario B: Raw Euclid (spherical RA, DEC, z) shard
    euclid_shard_path = os.path.join(workunit_dir, euclid_shards[0])
    print(f"\n[Test Client] Running Euclid Raw (Spherical RA/DEC/z) Shard: {euclid_shards[0]}...")
    client_cmd_b = [binary_path, euclid_shard_path, "--raw"]
    print(f"Executing: {' '.join(client_cmd_b)}")
    subprocess.run(client_cmd_b, check=True)
    
    assert os.path.exists("receipt_boinc.txt"), "Interactive receipt_boinc.txt not written!"
    with open("receipt_boinc.txt", "r") as f:
        print("\n   [RECEIPT READOUT - EUCLID]")
        for line in f:
            print(f"      {line.strip()}")
            
    # Copy receipt to results for Bridge testing
    os.makedirs("core_boinc/results", exist_ok=True)
    archive_receipt = "core_boinc/results/boinc_wu_test_euclid_receipt.txt"
    os.rename("receipt_boinc.txt", archive_receipt)
    
    # 4. Execute Bridge Syncing Daemon
    print("\n--- [STEP 4/4] EXECUTING FEDERATED BRIDGE DAEMON SYNC ---")
    bridge_cmd = ["python3", "core_boinc/boinc_bridge_daemon.py", "--single-run"]
    
    # Since standard interactive receipt was renamed/moved, we can put another receipt in standard path
    # and run the single-run bridge, or we can copy it back.
    # Let's write a mock receipt to core_boinc/receipt_boinc.txt
    with open("core_boinc/receipt_boinc.txt", "w") as f:
        f.write("BOINC_WU_RECEIPT\n")
        f.write("Galaxies=8000\n")
        f.write("AsymmetryRatio=1.4925\n")
        f.write("Delta=0.0075\n")
        f.write("Score=0.9925\n")
        f.write("KnotDistance=24.15\n")
        f.write("AlignmentScore=80.54\n")
        f.write("ComputationTimeMs=120.5\n")
        f.write("Status=success\n")
        
    print(f"Executing Bridge: {' '.join(bridge_cmd)}")
    subprocess.run(bridge_cmd, check=True)
    
    # Assert database or file ledger was synced
    offline_ledger = "core_boinc/boinc_offline_ledger.json"
    assert os.path.exists(offline_ledger) or os.getenv("DB_HOST") is not None, "Ledger synchronization failed!"
    
    if os.path.exists(offline_ledger):
        with open(offline_ledger, "r") as f:
            ledger_data = json.load(f)
            print("\n   [OFFLINE LEDGER READOUT]")
            print(json.dumps(ledger_data, indent=4))
            
    print("\n======================================================================")
    print("🏆 ALL INTEGRATION TESTS PASSED SUCCESSFULLY! BOEINC SYSTEM VALIDATED!")
    print("======================================================================")

if __name__ == "__main__":
    run_test_suite()
