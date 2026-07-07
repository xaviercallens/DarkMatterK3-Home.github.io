# core_boinc/boinc_bridge_daemon.py
import os
import sys
import json
import time
from datetime import datetime
import psycopg2
import redis

# Add parent directory to sys.path to allow imports if needed
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "darkmatter"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            port=os.getenv("DB_PORT", 5432),
            connect_timeout=3
        )
        return conn
    except Exception as e:
        print(f"[BOEINC Bridge] Database connection error: {e}")
        return None

def get_redis_client():
    """Establish a connection to the Redis cache."""
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True, socket_timeout=2)
        r.ping()
        return r
    except Exception as e:
        print(f"[BOEINC Bridge] Redis connection error: {e}")
        return None

def parse_boinc_receipt(receipt_path):
    """Parses a C++ client generated BOINC verification receipt file."""
    metrics = {}
    try:
        with open(receipt_path, "r") as f:
            lines = f.readlines()
            
        if not lines or "BOINC_WU_RECEIPT" not in lines[0]:
            print(f"[BOEINC Bridge] Warning: File {receipt_path} is not a valid BOINC receipt.")
            return None
            
        for line in lines[1:]:
            line = line.strip()
            if not line or "=" not in line:
                continue
            key, val = line.split("=", 1)
            try:
                if key in ["Galaxies", "ComputationTimeMs"]:
                    metrics[key] = int(float(val))
                elif key in ["AsymmetryRatio", "Delta", "Score", "KnotDistance", "AlignmentScore"]:
                    metrics[key] = float(val)
                else:
                    metrics[key] = val
            except ValueError:
                metrics[key] = val
        return metrics
    except Exception as e:
        print(f"[BOEINC Bridge] Error parsing receipt {receipt_path}: {e}")
        return None

def synchronize_receipt_to_db(receipt_path, wu_id, user_id="boinc_worker_node"):
    """
    Synchronizes a parsed BOEINC workunit receipt directly into the main Cloud SQL
    PostgreSQL ledger (users, jobs tables) and updates Redis Leaderboard.
    """
    metrics = parse_boinc_receipt(receipt_path)
    if not metrics:
        return False
        
    print(f"[BOEINC Bridge] Synchronizing {wu_id} for user {user_id}...")
    
    # Calculate gamified score/points earned
    # Base 15 points + bonus points proportional to the alignment score
    base_points = 15
    alignment_score = metrics.get("AlignmentScore", 0.0)
    bonus_points = int(alignment_score * 0.5)
    points_earned = base_points + bonus_points
    
    # Connect to database and sync
    conn = get_db_connection()
    db_synced = False
    
    if conn:
        try:
            cursor = conn.cursor()
            
            # Ensure the user exists in PostgreSQL
            cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO users (user_id, username, score, chunks_processed) VALUES (%s, %s, %s, %s)",
                    (user_id, "BOEINC Native Contributor", points_earned, 1)
                )
                print(f"  └─ Created new user node '{user_id}' in PostgreSQL.")
            else:
                cursor.execute(
                    "UPDATE users SET score = score + %s, chunks_processed = chunks_processed + 1 WHERE user_id = %s",
                    (points_earned, user_id)
                )
                print(f"  └─ Updated user node '{user_id}' scores in PostgreSQL.")
                
            # Create or complete the job entry
            chunk_data = {"chunk_id": wu_id, "type": "boinc_native_hpc"}
            result_data = {
                "galaxies_processed": metrics.get("Galaxies", 0),
                "asymmetry_ratio": metrics.get("AsymmetryRatio", 0.0),
                "delta": metrics.get("Delta", 0.0),
                "score": metrics.get("Score", 0.0),
                "knot_distance_mpc": metrics.get("KnotDistance", 0.0),
                "alignment_score": alignment_score,
                "computation_time_ms": metrics.get("ComputationTimeMs", 0),
                "points_earned": points_earned,
                "synced_at": datetime.now().isoformat()
            }
            
            cursor.execute("SELECT job_id FROM jobs WHERE job_id = %s", (wu_id,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO jobs (job_id, status, assigned_to, chunk_data, result_data, completed_at) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)",
                    (wu_id, "completed", user_id, json.dumps(chunk_data), json.dumps(result_data))
                )
            else:
                cursor.execute(
                    "UPDATE jobs SET status = 'completed', result_data = %s, completed_at = CURRENT_TIMESTAMP WHERE job_id = %s",
                    (json.dumps(result_data), wu_id)
                )
                
            # Also award high topological alignment badges if score is extreme
            if alignment_score > 75.0:
                cursor.execute(
                    "INSERT INTO badges (user_id, badge_name) VALUES (%s, %s)",
                    (user_id, "Golden Ratio")
                )
                print(f"  └─ Awarded 'Golden Ratio' badge to {user_id} in PostgreSQL.")
                
            conn.commit()
            cursor.close()
            conn.close()
            print("  └─ Successfully synchronized transactions to Cloud SQL PostgreSQL ledger.")
            db_synced = True
        except Exception as e:
            print(f"  └─ [ERROR] Failed to commit Postgres SQL transaction: {e}")
            if conn:
                conn.close()
    else:
        print("  └─ [DATABASE OFFLINE] Falling back to filesystem backup ledger...")
        # Write to local file ledger for full resilience
        ledger_path = os.path.join(BASE_DIR, "core_boinc", "boinc_offline_ledger.json")
        ledger = {}
        if os.path.exists(ledger_path):
            try:
                with open(ledger_path, "r") as f:
                    ledger = json.load(f)
            except Exception:
                pass
        
        ledger[wu_id] = {
            "user_id": user_id,
            "metrics": metrics,
            "points_earned": points_earned,
            "synced_at": datetime.now().isoformat()
        }
        
        with open(ledger_path, "w") as f:
            json.dump(ledger, f, indent=2)
        print("  └─ Successfully logged receipt to local offline ledger.")
        db_synced = True
        
    # Synchronize into Redis streaming leaderboard
    r_client = get_redis_client()
    if r_client:
        try:
            r_client.zincrby("leaderboard", points_earned, user_id)
            print(f"  └─ Synchronized {points_earned} points to Redis 'leaderboard' cache.")
        except Exception as re:
            print(f"  └─ Redis update failed: {re}")
            
    return db_synced

def reconcile_offline_ledger():
    """Attempts to synchronize any cached offline results when database connectivity is restored."""
    ledger_path = os.path.join(BASE_DIR, "core_boinc", "boinc_offline_ledger.json")
    if not os.path.exists(ledger_path):
        return
        
    conn = get_db_connection()
    if not conn:
        return  # Database is still offline, nothing to do
        
    conn.close()  # Close the test connection
    
    print("\n🔄 [BOEINC Bridge] Database connection detected! Reconciling offline ledger...")
    
    try:
        with open(ledger_path, "r") as f:
            ledger = json.load(f)
    except Exception as e:
        print(f"[BOEINC Bridge] Error reading offline ledger: {e}")
        return
        
    if not ledger:
        return
        
    synced_ids = []
    
    for wu_id, entry in list(ledger.items()):
        user_id = entry.get("user_id", "boinc_worker_node")
        metrics = entry.get("metrics", {})
        
        # Create a temporary receipt file to feed into standard pipeline
        os.makedirs("core_boinc/results", exist_ok=True)
        temp_receipt = f"core_boinc/results/temp_reconcile_{wu_id}.txt"
        try:
            with open(temp_receipt, "w") as f:
                f.write("BOINC_WU_RECEIPT\n")
                for key, val in metrics.items():
                    f.write(f"{key}={val}\n")
                    
            # Synchronize using standard logic
            success = synchronize_receipt_to_db(temp_receipt, wu_id, user_id)
            if success:
                synced_ids.append(wu_id)
                # Archive the temporary receipt to marked synced
                archive_path = f"core_boinc/results/synced_{wu_id}_receipt.txt"
                if os.path.exists(temp_receipt):
                    os.rename(temp_receipt, archive_path)
            else:
                # If sync failed, clean up the temp file
                if os.path.exists(temp_receipt):
                    os.remove(temp_receipt)
        except Exception as e:
            print(f"[BOEINC Bridge] Error reconciling {wu_id}: {e}")
            if os.path.exists(temp_receipt):
                try:
                    os.remove(temp_receipt)
                except:
                    pass
                    
    # Remove synchronized entries from ledger and save
    for wu_id in synced_ids:
        del ledger[wu_id]
        
    try:
        if ledger:
            with open(ledger_path, "w") as f:
                json.dump(ledger, f, indent=2)
            print(f"[BOEINC Bridge] Reconciled {len(synced_ids)} entries. {len(ledger)} remaining in offline ledger.")
        else:
            if os.path.exists(ledger_path):
                os.remove(ledger_path)
            print(f"✅ [BOEINC Bridge] All offline ledger entries successfully reconciled & synchronized!")
    except Exception as e:
        print(f"[BOEINC Bridge] Error updating offline ledger after reconciliation: {e}")

def run_bridge_polling_loop():
    """Bridging daemon process that scans for newly written receipts and syncs them."""
    print("🚀 BOEINC FEDERATED SYNC BRIDGE DAEMON RUNNING...")
    print("   Scanning core_boinc directory for client verification receipts...")
    
    os.makedirs("core_boinc/results", exist_ok=True)
    
    while True:
        # Reconcile any offline ledger entries if database has come online
        reconcile_offline_ledger()
        
        # Check standard receipt location
        std_receipt = "core_boinc/receipt_boinc.txt"
        if os.path.exists(std_receipt):
            wu_id = f"boinc_wu_interactive_{int(time.time())}"
            # Copy to results directory to archive
            archive_path = f"core_boinc/results/{wu_id}_receipt.txt"
            try:
                os.rename(std_receipt, archive_path)
                print(f"\n[Bridge] Detected new interactive result receipt: {std_receipt}")
                synchronize_receipt_to_db(archive_path, wu_id)
            except Exception as e:
                print(f"[Bridge] Error archiving receipt: {e}")
                
        # Scan core_boinc/results directory for incoming workunit receipts
        for filename in os.listdir("core_boinc/results"):
            if filename.endswith("_receipt.txt") and not filename.startswith("synced_") and not filename.startswith("temp_"):
                receipt_path = os.path.join("core_boinc/results", filename)
                wu_id = filename.replace("_receipt.txt", "")
                
                print(f"\n[Bridge] Detected completed workunit result: {filename}")
                success = synchronize_receipt_to_db(receipt_path, wu_id)
                
                if success:
                    # Mark receipt as synced to prevent reprocessing
                    new_path = os.path.join("core_boinc/results", f"synced_{filename}")
                    os.rename(receipt_path, new_path)
                    print(f"  └─ Archived result to {os.path.basename(new_path)}")
                    
        time.sleep(5)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--single-run":
        # Reconcile offline ledger first if DB is online
        reconcile_offline_ledger()
        # Run a single synchronization pass on the main receipt if it exists
        std_receipt = "core_boinc/receipt_boinc.txt"
        if os.path.exists(std_receipt):
            print("[Single Run] Found active receipt. Syncing...")
            synchronize_receipt_to_db(std_receipt, f"boinc_wu_single_run_{int(time.time())}")
        else:
            print("[Single Run] No receipt found to synchronize.")
    else:
        run_bridge_polling_loop()
