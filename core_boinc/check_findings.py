# core_boinc/check_findings.py
import os
import json
from datetime import datetime, timedelta

BASE_DIR = "/home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-Home"
DISCOVERIES_FILE = os.path.join(BASE_DIR, "discoveries.json")
RUNS_FILE = os.path.join(BASE_DIR, "pipeline_runs.json")
LEDGER_FILE = os.path.join(BASE_DIR, "core_boinc", "boinc_offline_ledger.json")

def format_time_diff(dt_str):
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        now = datetime.now(dt.tzinfo)
        diff = now - dt
        minutes = int(diff.total_seconds() / 60)
        if minutes == 0:
            return "just now"
        return f"{minutes}m ago"
    except Exception:
        return dt_str

def check_findings():
    print("==============================================================================")
    print("🌌  DarkMatterK3@Home — COSMIC ANOMALY MONITOR")
    print("==============================================================================")
    
    # 1. Check Discoveries
    if os.path.exists(DISCOVERIES_FILE):
        try:
            with open(DISCOVERIES_FILE, "r") as f:
                discoveries = json.load(f)
            
            recent_disc = []
            now = datetime.now()
            for d in discoveries:
                try:
                    dt = datetime.fromisoformat(d["timestamp"])
                    # Check if within last 15 minutes
                    if now - dt < timedelta(minutes=15):
                        recent_disc.append(d)
                except Exception:
                    pass
            
            if recent_disc:
                print(f"🔥 [CRITICAL DISCOVERIES] Detected {len(recent_disc)} major anomalies in the last 15 mins:")
                for rd in recent_disc:
                    print(f"  📌 {rd['type']} (ID: {rd['id']})")
                    print(f"     └─ Sector: RA [{rd['ra_min']:.1f}-{rd['ra_max']:.1f}], DEC [{rd['dec_min']:.1f}-{rd['dec_max']:.1f}]")
                    print(f"     └─ Galaxies analyzed: {rd['num_galaxies']} | Max Asymmetry: {rd['max_asymmetry']:.3f} | S12-S21 Delta: {rd['delta']:.4f}")
                    print(f"     └─ Details: {rd['details']}")
                    print(f"     └─ Time: {format_time_diff(rd['timestamp'])}")
            else:
                print("🟢 No new major astrophysical discoveries logged in the last 15 minutes.")
                print(f"   (Total archived discoveries in catalog: {len(discoveries)})")
        except Exception as e:
            print(f"❌ Error reading discoveries: {e}")
    else:
        print("⚠️ Discoveries file not found.")

    # 2. Check Latest Pipeline Runs
    print("\n------------------------------------------------------------------------------")
    print("📈 LATEST SCIENCE PIPELINE SWEEPS:")
    if os.path.exists(RUNS_FILE):
        try:
            with open(RUNS_FILE, "r") as f:
                runs = json.load(f)
            if runs:
                latest_runs = runs[-5:]
                for idx, run in enumerate(reversed(latest_runs)):
                    print(f"  [{idx+1}] Run at {format_time_diff(run['timestamp'])} ({run['device']})")
                    print(f"      └─ Sector Index: {run['sector_index']} (RA:{run['ra_min']:.1f}-{run['ra_max']:.1f})")
                    print(f"      └─ Galaxies: {run['num_galaxies']} | S12-S21 Delta: {run['delta']:.4f} | Mean Asym: {run['mean_asymmetry']:.5f}")
            else:
                print("   No pipeline runs found.")
        except Exception as e:
            print(f"❌ Error reading runs: {e}")
    else:
        print("⚠️ Pipeline runs file not found.")

    # 3. Check BOEINC Decentralized Ledger
    print("\n------------------------------------------------------------------------------")
    print("🏆 BOEINC FEDERATED COMPUTING CONTRIBUTION LEDGER:")
    
    # Check if we can query the API server for the dynamic leaderboard
    api_leaders = []
    try:
        import requests
        r = requests.get("http://localhost:8000/leaderboard", timeout=2.0)
        if r.status_code == 200:
            lb_json = r.json()
            if isinstance(lb_json, dict) and "leaderboard" in lb_json:
                api_leaders = lb_json["leaderboard"]
            elif isinstance(lb_json, list):
                api_leaders = lb_json
    except Exception:
        pass

    if api_leaders:
        print("  🟢 Live API Leaderboard active and synced:")
        for idx, leader in enumerate(api_leaders[:5]):
            node_name = leader.get("node") or leader.get("user_id", "Anonymous")
            pts = leader.get("points") or leader.get("score", 0)
            gals = leader.get("galaxies", 0)
            print(f"      [{idx+1}] Node: {node_name} | Score: {pts} pts" + (f" | Galaxies: {gals}" if gals else ""))
    
    elif os.path.exists(LEDGER_FILE):
        try:
            with open(LEDGER_FILE, "r") as f:
                ledger = json.load(f)
            
            recent_ledger = []
            now = datetime.now()
            for wu_id, wu_info in ledger.items():
                try:
                    dt = datetime.fromisoformat(wu_info["synced_at"])
                    if now - dt < timedelta(minutes=15):
                        recent_ledger.append((wu_id, wu_info))
                except Exception:
                    pass
                    
            if recent_ledger:
                print(f"  🚀 Synced {len(recent_ledger)} HPC workunits in the last 15 mins:")
                for wu_id, info in recent_ledger:
                    metrics = info.get("metrics", {})
                    print(f"      🔹 {wu_id} by {info['user_id']}")
                    print(f"         └─ Galaxies Sieved: {metrics.get('Galaxies')} | Alignment Score: {metrics.get('AlignmentScore'):.4f}%")
                    print(f"         └─ Delta: {metrics.get('Delta'):.4f} | Points Earned: {info.get('points_earned')}")
                    print(f"         └─ Synced: {format_time_diff(info['synced_at'])}")
            else:
                print(f"  💤 No new BOEINC workunits synced in the last 15 mins. (Total active nodes: {len(set(wu['user_id'] for wu in ledger.values()))})")
        except Exception as e:
            print(f"❌ Error reading ledger: {e}")
    else:
        print("  💤 No pending offline ledger file. All data successfully synchronized to Redis/DB!")
    print("==============================================================================\n")

if __name__ == "__main__":
    check_findings()
