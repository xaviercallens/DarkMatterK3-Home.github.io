# S21 DarK3CosmicWeb@Home (Codename: NEON K3)
## Master Task List (TODO.md)

This document maps out the specific, engineering-level tasks required to transition the K3 Dark Matter mathematical theories (verified in `SocrateAI-Scientific-Agora-K3-DarkMatter`) into a planetary-scale, crowdsourced browser supercomputer.

> [!NOTE]
> All tasks are indexed by project subsystems to facilitate clean developer tracking and continuous integration.

---

## 🛠️ 1. Core WebAssembly Engine (`core_wasm/`)
*Mathematical logic and client-side processing algorithms compiled to WASM.*

- [ ] **Initialize Crate**
  - [ ] Bootstrap the Rust project under `core_wasm/` with a static/dynamic library configuration targetable by `wasm-pack`.
  - [ ] Configure `Cargo.toml` to import geometric equations and physics modules from the local `DarkMatter` crate.
- [ ] **Implement Archive 01 (SDSS DR17) Calculations**
  - [ ] Implement comoving distance conversion functions from astronomical redshift ($z$) utilizing exact cosmological parameters ($w_0 = -0.5485$, $w_a = -0.3968$, $H_0 = 71.92$ km/s/Mpc).
  - [ ] Write 3D nearest-neighbor search algorithms optimized for CPU WebAssembly.
  - [ ] Implement the Picard-Fuchs $S_{1,2}$ recurrence relation verification checker to identify clusters displaying the characteristic 3:2 asymmetric expansion.
- [ ] **Implement Archive 02 (Euclid Deep Sieve) Calculations**
  - [ ] Write weak gravitational lensing shear tensor mapping algorithms ($\gamma_1, \gamma_2$ field calculations).
  - [ ] Implement asymmetric lensing detection criteria to sweep for Chameleon Gravitino knots.
- [ ] **Optimize WASM Performance**
  - [ ] Implement multi-threading within WASM using modern Web Workers.
  - [ ] Ensure strict memory constraints are met (e.g., maximum memory footprint per worker < 64MB) to prevent smartphone crashes.

---

## ⚡ 2. WebGPU Netrunner Compute Engine (`ui_loom/src/compute/`)
*Direct-to-metal browser computations utilizing WebGPU and VRAM/Tensor Cores.*

- [ ] **WebGPU Initialization**
  - [ ] Establish fallback checks to gracefully downgrade to CPU-WASM if the client's browser does not support WebGPU.
  - [ ] Request GPU adapters and setup logical device bounds configured for massive floating-point matrix calculations.
- [ ] **Neural-FGMRES Preconditioner Implementation**
  - [ ] Write WGSL (WebGPU Shading Language) compute shaders to execute high-dimensional matrix-vector multiplications.
  - [ ] Implement parallel training steps for the neural network preconditioner.
  - [ ] Interface shader outputs with the core `rusty-SUNDIALS` MHD plasma simulation engine to accelerate Stellarator reactor stabilization metrics.

---

## 🎨 3. Cyberpunk WebGL Frontend (`ui_loom/`)
*The browser user experience, visualizer canvas, and cyberpunk styling.*

- [ ] **Configure Project Workspace**
  - [ ] Scaffold the web app structure using Vite + TypeScript + TailwindCSS/Vanilla CSS.
  - [ ] Define the core cyberpunk color palette and dark glassmorphic components in CSS variables (Gold accents `#FFD700`, Cyan accents `#00FFFF`, Deep background `#0A0E17`, Glass panels `rgba(255, 255, 255, 0.05)`).
- [ ] **Implement "The Cosmic Loom" (WebGL Canvas)**
  - [ ] Initialize Three.js canvas mapping the cosmic web.
  - [ ] Create dynamic particle systems where stars/galaxies physically assemble on-screen in real-time as CPU nodes complete SDSS shards.
  - [ ] Write a custom WebGL shader to flash the screen Gold with high-tech concentric rings on detecting a verified $S_{1,2}$ expansion anomaly.
- [ ] **Implement "The Netrunner Terminal" (GPU Dashboard)**
  - [ ] Build a sleek dashboard displaying scrolling command logs and active matrix computation status.
  - [ ] Draw real-time, high-octane 2D Canvas charts mapping tensor loss rates, VRAM thermal approximations, and floating-point throughput.
- [ ] **State & Shard Management**
  - [ ] Build a robust queuing mechanism to load shards sequentially from the Dispatcher backend.
  - [ ] Manage local client storage (IndexDB) to cache completed shards and avoid re-downloading identical payloads.

---

## ☁️ 4. GCP Serverless Infrastructure (`gcp_infrastructure/` & `tools/`)
*The underlying cloud framework designed to handle extreme concurrent load.*

- [ ] **FITS Slicing pipeline (`tools/dataset_slicer/`)**
  - [ ] Write `slice.py` in Python using `astropy.io.fits` to load massive 3D sky maps.
  - [ ] Partition raw FITS into indexed, 500KB JSON files containing coordinate lists and cosmic shear matrix arrays.
- [ ] **Dispatcher Actix-web Backend**
  - [ ] Build the Cloud Run endpoint mapping for assigning shards to workers.
  - [ ] Implement secure GCS short-lived signed URL generation to permit client browsers to download JSON slices directly without traversing the central backend.
  - [ ] Build the anomaly report receiver endpoint that verifies the cryptographic hash of client calculations to prevent fraudulent results.
- [ ] **Database & Telemetry Systems**
  - [ ] Write schema migrations for PostgreSQL to support user profiles, team guilds, and anomalous coordinate registries.
  - [ ] Set up Redis data streams to collect real-time heartbeats and aggregate transaction stats from active browsers.
- [ ] **Terraform Configuration**
  - [ ] Write `main.tf` to spin up Firebase Hosting, Cloud Run instances, GCS buckets, Cloud SQL PostgreSQL database, and Memorystore Redis.

---

## 🏆 5. Gamification & Publication Loop (`ui_loom/src/features/`)
*The cyber-guilds, achievement rewards, and cryptographic legacy records.*

- [ ] **The Bounty Board Leaderboard**
  - [ ] Design high-tech tables showing user ranking based on aggregate FLOPS contributed and sectors mapped.
  - [ ] Set up "Cyber-Guild" registration (Squad Zebroloss vs. Squad Lisoir).
- [ ] **Topological Achievements System**
  - [ ] Create localized achievements logic in the browser.
  - [ ] Draw styled SVGs representing badges ("First Blood", "The Golden Ratio", "Plasma Weaver") to display on user profiles.
- [ ] **The Legacy Chain Pipeline**
  - [ ] Write a script that signs completed computation receipts with the user's private key.
  - [ ] Create a utility that outputs a single combined SHA-256 cryptographic hash of all successful contributor receipts.
  - [ ] Design an exporter format that transforms this list into a clean LaTeX table template to easily drop into the appendix of academic papers.

---

## 🎯 6. Testing, Load Benchmarking, and Deployment
*Ensuring stability under extreme viral traffic ("Zebroloss Hug of Death").*

- [ ] **Simulated Load Testing**
  - [ ] Write a mock worker script in Go or Node.js to spin up 100,000 headless browsers.
  - [ ] Execute stress-tests against the GCS signed URL generator and the Cloud Run Dispatcher, ensuring latency stays below 150ms.
- [ ] **Scientific Proof Verification**
  - [ ] Run mathematical comparisons between local Python results and compiled WebAssembly/WebGPU results to guarantee absolute precision.
- [ ] **Production Deployment**
  - [ ] Deploy frontend bundles to Firebase Hosting.
  - [ ] Initialize global Cloud CDN cache.

---

## 🌌 7. Advanced Observational Client & BOINC Integration (`core_boinc/`)
*Installable native background computing using BOINC for advanced research.*

- [x] **Initialize Native C++ Core Client**
  - [x] Bootstrap the C++ compute daemon leveraging CPU multi-threading and OpenMP modules, with structural support for OpenCL/CUDA.
  - [x] Port Picard-Fuchs integration math and complex matrix solvers to native C++ for extreme performance.
- [x] **Deploy BOINC Project Server**
  - [x] Set up and configure XML-based workunit templates and work distribution protocols matching BOINC API specifications.
- [x] **Establish Federated Sync**
  - [x] Build a bridging daemon that synchronizes completed BOINC workunit receipts directly into the main Cloud SQL PostgreSQL ledger.

---

## 🔧 8. Phase 6: Integration, HPC Validation & Cost-Optimized Cloud Federation
*Graceful shutdown, data preservation, performance tuning, and low-cost multi-cloud planning.*

- [x] **Safe Termination & Data Archiving**
  - [x] Gracefully stop all active `tmux` daemon worker threads.
  - [x] Package and compress all validated ledger receipts, discoveries catalogs, and run telemetry into `archives/boinc_run_archive_20260707_1753.tar.gz`.
- [x] **Client & Work Generator Performance Optimization**
  - [x] Vectorize Python comoving distance numerical integration equations using grid-based linear interpolation (`np.interp`), speeding up shard generation 15x.
  - [x] Configure hardware-native C++ compilation scripts utilizing aggressive compiler optimizations (`-O3 -march=native -ffast-math -funroll-loops -fopenmp`).
- [x] **Low-Cost Always-On Deployment Architecture**
  - [x] Map out Zero-Dollar Serverless (Option A) and Cheap VPS (Option B) architectures.
  - [x] Design **Option C** under GCP ($16.00/mo) utilizing local Docker containers for PostgreSQL and Redis to bypass Cloud SQL/Memorystore minimum fees and remain fully compliant with the under $50/mo budget limit.

---

## 🔬 9. Phase 7: Scientific Rigor & Academic Adoption (Phase 2 Research Roadmap)
*Resolve spatial boundary biases and coordinate-pinned template artifacts to secure academic journal acceptance.*

- [ ] **Implement Translation-Invariant Topological Data Analysis (TDA)**
  - [ ] Integrate Minkowski functionals and multi-scale Euler Characteristics calculation into the native C++ solver.
  - [ ] Implement persistence diagram generators tracing Betti numbers ($\beta_0, \beta_1$) to search for $S_{1,2}$ manifolds without geocentric coordinate bias.
- [ ] **Develop 6-Parameter Template Moduli Fitting**
  - [ ] Refactor the Picard-Fuchs knot template in `core_boinc/src/main.cpp` from static geocentric coordinates to a free-moving mathematical path.
  - [ ] Add 6 degrees of freedom to the fitting solver: 3 translation offsets $(\Delta x, \Delta y, \Delta z)$, 2 rotational Euler angles $(\theta, \phi)$, and 1 scale factor $S$.
  - [ ] Implement a localized minimization algorithm (e.g., Levenberg-Marquardt or FGMRES preconditioner adjustments) to fit the free-moving loop to local density spikes.
- [ ] **Slicing De-biasing & Data Normalization**
  - [ ] Add coordinate standardizations (z-score normalization or min-max $[0,1]^3$ unit cube mapping) inside the preprocessing pipeline (`tools/dataset_slicer/slice.py`).
  - [ ] Ensure the 3:2 asymmetry ratio solver evaluates normalized coordinates, isolating physical galaxy cluster configurations from bounding-box rectangular prism boundaries.
- [ ] **Establish Open-Science Anomaly Registry**
  - [ ] Build a public, cryptographic, reproducible portal for candidate coordinate submissions to integrate with the SDSS/Euclid scientific consortium.


