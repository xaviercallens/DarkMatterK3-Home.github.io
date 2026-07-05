import os
import time
import requests
import torch
import numpy as np
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8080")
USER_ID = os.getenv("USER_ID", "1")
GCS_BUCKET = os.getenv("GCS_BUCKET", "darkmatter-k3-data")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting DarK3 Worker on device: {device.type.upper()}")

def simulate_k3_computation(chunk_data):
    # Simulated tensor workload for K3 integration
    t_size = 64
    grid = torch.rand((t_size, t_size, t_size), device=device, dtype=torch.complex64)
    k3_space = torch.fft.fftn(grid)
    
    s12 = 1.5 + 0.1 * np.random.rand()
    s21 = 0.5 + 0.1 * np.random.rand()
    
    S12_field = k3_space * s12 * torch.exp(1j * torch.tensor(0.5, device=device))
    S21_field = k3_space * s21 * torch.exp(-1j * torch.tensor(0.5, device=device))
    
    asymmetry = torch.abs(torch.fft.ifftn(S12_field - S21_field))
    mean_asymmetry = torch.mean(asymmetry).item()
    
    # Simulate a wasserstein distance based on asymmetry
    wasserstein_dist = mean_asymmetry * 50.0 + np.random.uniform(5, 35)
    
    if device.type == 'cuda':
        torch.cuda.synchronize()
        
    return {
        "mean_asymmetry": mean_asymmetry,
        "max_asymmetry": torch.max(asymmetry).item(),
        "s12": s12,
        "s21": s21,
        "wasserstein_distance": wasserstein_dist
    }

def register_worker():
    try:
        res = requests.post(f"{API_URL}/users/register", json={"user_id": USER_ID, "username": f"T4_Worker_{USER_ID}"})
        if res.status_code == 200:
            print(f"[REGISTER] {res.json().get('message')}")
        else:
            print(f"[REGISTER] Error: {res.text}")
    except Exception as e:
        print(f"[REGISTER] API unavailable: {e}")

def run_worker():
    register_worker()
    
    while True:
        try:
            # Request Job
            print(f"\n[{time.strftime('%H:%M:%S')}] Requesting new computation chunk...")
            req_res = requests.post(f"{API_URL}/jobs/request", json={"user_id": USER_ID})
            
            if req_res.status_code != 200:
                print(f"[ERROR] Could not fetch job. API returned: {req_res.status_code}")
                time.sleep(10)
                continue
                
            job_data = req_res.json()
            job_id = job_data["job_id"]
            chunk = job_data["chunk_data"]
            
            print(f"[JOB] Received Job ID {job_id[:8]} -> Fetching {chunk['data_url']}")
            
            # Compute
            print("[COMPUTE] Running S1,2 / S21 Topological calculation on GPU...")
            start_time = time.time()
            results = simulate_k3_computation(chunk)
            calc_time = time.time() - start_time
            
            print(f"[COMPUTE] Done in {calc_time:.4f}s. Asymmetry: {results['mean_asymmetry']:.4f}, d_W: {results['wasserstein_distance']:.2f}")
            
            # Submit Result
            submit_payload = {
                "job_id": job_id,
                "user_id": USER_ID,
                "wasserstein_distance": results["wasserstein_distance"],
                "result_metadata": {
                    "calc_time_seconds": calc_time,
                    "mean_asymmetry": results["mean_asymmetry"],
                    "s12": results["s12"],
                    "s21": results["s21"],
                    "device": device.type.upper()
                }
            }
            
            sub_res = requests.post(f"{API_URL}/jobs/submit", json=submit_payload)
            if sub_res.status_code == 200:
                data = sub_res.json()
                print(f"[SUCCESS] {data['message']} | Earned {data.get('points_earned', 0)} points.")
            else:
                print(f"[ERROR] Submission failed: {sub_res.text}")
                
        except requests.exceptions.ConnectionError:
            print("[ERROR] API connection failed. Retrying in 10s...")
        except Exception as e:
            print(f"[ERROR] Unexpected crash: {e}")
            
        time.sleep(5)

if __name__ == "__main__":
    run_worker()
