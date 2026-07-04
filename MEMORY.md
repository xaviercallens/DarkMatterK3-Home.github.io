# Memory & Quick Restart Guide - DarkMatterK3@Home

## Project Overview
DarkMatterK3@Home is a PoC mapping the topological asymmetry ($\Delta = |S_{12} - S_{21}|$) of Calabi-Yau K3 manifolds to detect dark matter signatures using real SDSS/Euclid astronomical data.

## 🚀 Quick Start
To launch the entire suite (Dashboard + GPU Worker + API Backend) in an isolated `tmux` background session:
```bash
./startup.sh
# or
./manage_darkmatter.sh start
```

## 🛑 Stopping the System
To safely kill all background processes and tunnels:
```bash
./stop_server.sh
# or
./manage_darkmatter.sh stop
```

## 📂 Core Components
- **`app_darkmatter.py`**: Streamlit interactive dashboard (Port **8501**).
- **`real_euclid_worker.py`**: Background GPU daemon fetching SDSS data and computing K3 tensors.
- **`api_darkmatter.py`**: FastAPI backend serving the pipeline results (Port **8000**).
- **`checkpoint_manager.py`**: CLI and module to safely backup and restore `.pt` and `.json` states.
- **`euclid_validation_run.py`**: Stress-test script to validate the architecture against 50M simulated Euclid galaxies.

## 💾 Data & Logs
- **Physics Output**: `pipeline_runs.json` (Time-series data of computed asymmetries).
- **Checkpoints**: `checkpoint_run.pt` (Last valid state of the sky vectors).
- **Logs**: Located in the `./logs/` directory (`worker.log`, `streamlit.log`, `api.log`).
- **Backups**: Located in `./backups/`. Can be archived to GCS via `./archive_to_gcs.sh`.

## 🚧 Next Steps / Future Dev
1. **Sky Scanning**: Update the SQL query in `real_euclid_worker.py` to paginate through the SDSS dataset using RA/DEC bounding boxes instead of a static `LIMIT 5000`.
2. **Resolution Bump**: Currently using $64^3$ grid for live tracking. The $128^3$ grid is proven to work in the validation script and could be merged into the main worker.
