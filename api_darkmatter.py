from fastapi import FastAPI, HTTPException
import json
import os
from typing import List, Dict

app = FastAPI(
    title="DarkMatterK3 Data API",
    description="Backend API for DarkMatterK3 simulation data. All data is fetched from local real Euclid/SDSS calculations.",
    version="1.1.0"
)

BASE_DIR = "/home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-Home"
PIPELINE_FILE = os.path.join(BASE_DIR, "pipeline_runs.json")

@app.get("/")
def read_root():
    return {"status": "DarkMatterK3 API Online", "docs": "/docs"}

@app.get("/api/v1/runs", response_model=List[Dict])
def get_pipeline_runs(limit: int = 50):
    """Fetch the latest physics pipeline runs. Returns real processed data."""
    if not os.path.exists(PIPELINE_FILE):
        raise HTTPException(status_code=404, detail="No pipeline runs found.")
    try:
        with open(PIPELINE_FILE, "r") as f:
            data = json.load(f)
        return data[-limit:]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/status")
def get_status():
    """Returns the current system status and latest metrics."""
    if not os.path.exists(PIPELINE_FILE):
        return {"status": "idle", "runs": 0}
    try:
        with open(PIPELINE_FILE, "r") as f:
            data = json.load(f)
        if data:
            latest = data[-1]
            return {
                "status": "running",
                "total_runs": len(data),
                "latest_asymmetry": latest.get("mean_asymmetry"),
                "latest_galaxies_processed": latest.get("num_galaxies"),
                "latest_device": latest.get("device"),
                "timestamp": latest.get("timestamp")
            }
        return {"status": "idle", "runs": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/backup")
def trigger_backup(label: str = "api_backup"):
    """Trigger a system backup via API."""
    import sys
    sys.path.append(BASE_DIR)
    try:
        from checkpoint_manager import create_backup
        success, msg, meta = create_backup(label)
        if success:
            return {"status": "success", "message": msg, "metadata": meta}
        else:
            raise HTTPException(status_code=500, detail=msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
