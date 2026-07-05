# DarkMatterK3@Home
## Distributed Topological Analysis of the Cosmic Web via K3 Moduli Spaces

DarkMatterK3@Home is a planetary-scale distributed computing project aiming to prove that the macroscopic large-scale structure of the universe (the Cosmic Web) is homologically equivalent to the microscopic algebraic geometry of K3 surface moduli spaces (specifically the $S_{1,2}$ Picard-Fuchs integration path).

By crowdsourcing dormant compute power across standard web browsers and high-performance native computers, we are building a decentralized, elastic supercomputer to hunt for the topological signatures of Dark Energy and Chameleon Gravitino knots.

---

## 🗺️ Multi-Phase Project Architecture

This project is structured in five progressive phases to establish our baseline theoretical verification and scale out to global citizen-science execution:

### 1. **Phase 1: Streamlit PoC & Baseline (Fully Deployed)**
- **Dashboard**: Live interactive portal hosted on [Streamlit Cloud](https://darkmatterk3athome.streamlit.app/) delivering telemetry views, 3D Plotly space visualizations, and global node analytics.
- **Infrastructure**: Powered by an auto-scaling **FastAPI Dispatcher** on GCP Cloud Run, a relational PostgreSQL ledger on **Cloud SQL**, a high-speed telemetry feed on **Memorystore Redis**, and an optional PyTorch background VM node (Tesla T4 GPU).
- **Static Dataset Baking**: Pre-baked simulations are compiled directly inside the git repo (`pipeline_runs.json`, `discoveries.json`) so the dashboard displays all 29-sector cosmological telemetry offline with zero VM dependencies.

### 2. **Phase 2 & 3: Web-Based Federated Computing (WASM & WebGPU)**
- **WASM Engine Core (`core_wasm/`)**: Packages our core physics equations and SDSS comoving calculations into an optimized Rust crate compiled directly to WebAssembly (`wasm-pack`) to enable CPU multithreading inside user browser sandboxes.
- **Web Frontend Migration (`ui_loom/`)**: Launches a premium, cyberpunk-stylized SPA (using Vite, React, or Next.js and Three.js/WebGL for 3D mapping).
- **Netrunner Console**: Direct WebGPU context pipelines that execute weak lensing cosmic shear tensor contractions and stellarator loss calculations directly in the viewer's browser VRAM.
- **Federated Orchestration**: Clients request 500KB JSON shards via Cloud Run, compute locally, and return cryptographic receipts to GCS/SQL.

### 3. **Phase 4: Gamification & The Legacy Chain**
- **Community Engagement**: Leaderboards mapping contributions (Bounty Boards) and Cyber-Guilds (e.g. *Squad Zebroloss* vs. *Squad Lisoir*).
- **Legacy Chain Appendix**: Cryptographically links completed task receipts to user profiles, compiling contributor credentials directly into LaTeX templates for research publication appendices.

### 4. **Phase 5: Advanced Observational Platform (BOINC Integration)**
- **Native Compute Client (`core_boinc/`)**: Build an installable, native C++/CUDA daemon for Windows, Linux, and macOS supporting extreme-precision math and high-performance GPU tensor cores.
- **BOINC Project Server**: Host a dedicated node registered on the **Berkeley Open Infrastructure for Network Computing (BOINC)** platform ([boinc.berkeley.edu](https://boinc.berkeley.edu/)) to let advanced scientists allocate dedicated hardware blocks.

---

## 📂 Repository Layout

```
agora2home/
├── api/                 # Phase 1: FastAPI Cloud Run dispatcher microservice
├── frontend/            # Phase 1: Streamlit dashboard and localized UI elements
├── core/                # Phase 1: Native VM worker services and legacy submodules
│   ├── t4_worker.py     # Background PyTorch computation daemon
│   └── lean4_anchor/    # Lean 4 mathematically verified theoretical baselines
├── core_wasm/           # Phase 2/3: Rust-to-WebAssembly browser-side CPU engine
├── core_boinc/          # Phase 5: Native C++/CUDA compute client and BOINC config files
├── ui_loom/             # Phase 2/3: High-fidelity Vite + Three.js + WebGPU SPA frontend
└── gcp_infrastructure/  # Terraform configurations for serverless elastic deployment
```

---

## 🛠️ General Development Guidelines

To contribute to this codebase, developers must adhere to the following principles:

### 1. **Sandbox Performance & Memory Constraints (WASM/WebGPU)**
- Web Workers must keep their memory footprint strictly **under 64MB** to prevent browser crashes on smartphones.
- Check and handle adapter capabilities gracefully; browser clients must fall back immediately to the multi-threaded CPU-WASM solver if WebGPU is unavailable or VRAM bounds are exceeded.

### 2. **Verification Integrity & Anti-Spoofing**
- Every computation result submitted to the Dispatcher must include a cryptographically signed task receipt.
- The Dispatcher uses spot-checking (assigning identical shards to random nodes and matching outputs) to verify result integrity before logging anomalies.

### 3. **Documentation & Quality Standards**
- Keep markdown documents (`TODO.md`, `ROADMAP.md`, `README.md`) in perfect alignment across phases.
- Retain all scientific docstrings, LaTeX formulas, and math references intact. Avoid code simplifications that could degrade mathematical precision.

---

## 🚀 Local Development Setup (Phase 1)

### 1. Clone with Submodules
To pull the core bound submodules (bindings, solvers):
```bash
git clone --recurse-submodules https://github.com/xaviercallens/DarkMatterK3-Home.github.io.git
```

### 2. Environment Configuration
Create a `.env` file in the root directory based on `.env.example`:
```env
API_URL=http://localhost:8000
DB_HOST=34.79.45.15
DB_NAME=darkmatter
DB_USER=postgres
DB_PASSWORD=YOUR_PASSWORD
DB_PORT=5432
```

### 3. Running the API Dispatcher (Local)
```bash
cd api
pip install -r requirements.txt
python api_dispatcher.py
```

### 4. Running the Streamlit Frontend (Local)
```bash
cd frontend
pip install -r requirements.txt
streamlit run app_darkmatter.py
```
