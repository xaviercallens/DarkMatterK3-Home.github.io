# WP-E6 lya-mfdm Emulator Extension — Feasibility/Costing Scoping (SCOPING ONLY, NOT EXECUTED)

Date: 2026-07-27
Repo scoped: https://github.com/jianxiangl-astro/lya-mfdm (cloned at
`phase1_work/agent1_emulator/lya-mfdm/`), paper arXiv:2606.06969 (Liu, Gong, Zhou 2026, JCAP).
Nothing was installed, built, or run beyond read-only inspection of code/data/pickled arrays and
`nproc`/`free`/`which`/`dpkg` checks on this VM. No simulation code was installed. `PREDICTION.md`
and `data/raw/` were not touched.

---

## 1. Training pipeline summary — what retraining actually needs

`emu_train.py` trains a **two-stage MLP emulator** (not a full re-simulation):

- Stage 1 ("CDM"): `(z_obs, z_rei, H_A, H_S, τ_eff) → log10 P_f,CDM(k_f)` (16 k-bins).
- Stage 2 ("residual"): `(z_obs, m_FDM, f_FDM, z_rei, H_A, H_S, τ_eff) → G(k_f)`, the
  FDM/CDM transfer-function residual (Eq. 3.1 of the paper).
- 3-layer, 256-hidden-unit `nn.Sequential` MLPs, SiLU activations, AdamW, 5-fold CV, up to 1200
  epochs with early stopping — this is a small network. `NUM_THREADS = 56` is set in the script
  (implying the authors' original machine had ≥56 cores), but this is CPU-only PyTorch training
  and needs no GPU. On this VM's 8 cores it would run, just slower (order minutes–low hours, not
  a blocker).
- Input format: `data/all_pk_num{0,1,2}[.pkl|_cdm.pkl]` — structured numpy arrays keyed by
  `index` (which LHS simulation), with per-index/per-τ_eff rows of thermal-history parameters and
  16 log-P1D values at fixed k-bins. `data/param.pkl` holds the 5D LHS design
  `(m_FDM, f_FDM, H_A, H_S, z_rei)` used to generate each `index`.

**Retraining on the existing z=5.0/4.6/4.2 data requires no new simulation** — that data is
already in the repo. **Extending to new redshifts requires new `all_pk_numN[.pkl]` files that do
not exist anywhere in this repo or upstream**, i.e. new hydrodynamical-simulation output,
post-processed through `fake_spectra`, in the same schema. There is no simulation-generation
script, config, or recipe checked into `lya-mfdm` itself — it only ships the already-computed P1D
summary statistics and the trained networks. Generating new z-slices means running the external
MP-Gadget → fake_spectra pipeline from scratch; `lya-mfdm` provides zero tooling for that step.

## 2. Simulation requirement — confirmed from data, not assumed

Both the paper text (§3.1, read directly from the arXiv PDF) and independent inspection of the
pickled arrays agree, and cross-check each other:

- **Box:** 10 Mpc/h comoving, 2×512³ particles (dark matter + gas) → ~268M particles total.
  DM particle mass 5.48×10⁵ M_sun/h, gas particle mass 1.02×10⁵ M_sun/h. This is a deliberately
  *small* box (10 Mpc/h side) — small enough that running O(100) of them is standard practice
  in this subfield, not an outlier choice.
- **5D LHS design:** `log10(m_FDM/eV) ∈ [-23,-19]`, `f_FDM ∈ [0,1]`, `H_A ∈ [0.05,4]`,
  `H_S ∈ [-1,1]`, `z_rei ∈ [6,15]`. 100 LHS training points + 10 independent test points.
- **Pairing:** each of the 100 training points is run as a **pair** — one full 5-parameter MFDM
  simulation and one CDM twin sharing the same thermal-history parameters (`f_FDM=0`) — to
  isolate the MFDM-induced relative effect. The 10 test points are MFDM-only (no CDM twin).
  → **100×2 + 10 = 210 separate MP-Gadget runs**, confirmed independently from the data:
  `data/param.pkl` has exactly 210 unique `index` values (0–209); `all_pk_num{0,1,2}_cdm.pkl`
  each have exactly 100 unique indices (0–99, the CDM half of the pairs); `all_pk_num{0,1,2}.pkl`
  each have exactly 110 unique indices (0–109, the 100 MFDM-training + 10 MFDM-test). This is
  **210 independent boxes**, not one box re-output — the earlier framing in the task ("one box vs
  many") is resolved: it is many (210), each a distinct initial-condition/parameter realization.
- **Within one `index`:** 31 rows, corresponding to a post-processing τ_eff (mean-flux) rescaling
  grid `0.30 → 1.80` step `0.05` — confirmed directly in the pickled data (`np.unique(taueff)`
  gives exactly those 31 values) and matches the paper's stated rescaling grid. **This is cheap,
  free post-processing, not additional simulations.**
- **Snapshots:** each run starts at z=99 (`MP-GenIC` initial conditions) and is **evolved to
  z=4.2**, with snapshots saved at z=5.0, 4.6, 4.2 — quoted directly from the paper: *"The
  simulations are evolved to z = 4.2, with snapshots saved at z = 5.0, 4.6, and 4.2."* **This is
  the critical finding for extension cost: the simulations physically stop integrating at z=4.2.**
  There is no "just output more snapshots" option from existing data — z<4.2 does not exist in
  any run, and the raw simulation snapshots/restart files themselves (which could in principle be
  restarted and continued to lower z without redoing z=99→4.2) are **not in this repo and not
  published anywhere the paper or repo points to** — only the derived P1D summary statistics were
  released. Per this project's public-products-only rule, contacting the authors for restart
  files is not an assumed fallback.
  → **Practical consequence: extending coverage requires re-running the full initial-conditions→
  z_target integration for however many LHS points are extended, not merely "resuming" existing
  runs.**
- MFDM initial conditions are generated via `axionCAMB` (modified linear P(k)), and the
  `Quick_Lya` MP-Gadget option (converts dense, cold gas particles to collisionless particles) is
  used specifically "for computational efficiency" — the authors already applied the standard
  cost-cutting trick for this kind of run; there is no more slack to extract from configuration.
- Spacing note: the existing z=5.0/4.6/4.2 (Δz=0.4) grid is **not motivated by any FDM-signal
  spacing logic** — it directly matches the Boera et al. (2019) VLT/UVES + Keck/HIRES
  observational P1D dataset's redshift bins, which is the only data this paper fits. There is no
  physical reason new z-slices must mirror that Δz=0.4 spacing; they should instead be chosen to
  match **DESI DR1's actual P1D bin centers** in z≈2.2–4.4 (DESI Lyα P1D analyses typically bin in
  ~Δz=0.2 steps), not an arbitrary geometric extrapolation of the old spacing.

## 3. MP-Gadget / fake_spectra compute requirements (from their own docs)

**MP-Gadget** (github.com/MP-Gadget/MP-Gadget, README fetched directly):
- Requires **MPI** for distributed-memory parallelism (README advertises domain decomposition
  scaling to "half a million cores" — built for HPC clusters) plus **OpenMP 4.5** threading
  within each MPI rank.
- Mandatory dependencies: **GSL**, **PFFT** (parallel FFT library, itself needs FFTW built with
  MPI support) — neither is a simple `pip install`; both are typically built from source on HPC
  systems, and platform-specific `Options.mk` tuning is expected.
- **No GPU support** is mentioned or implied — CPU/MPI only.
- The 10 Mpc/h, 2×512³ box used here is small by MP-Gadget's design envelope (which targets
  systems scaling to hundreds of thousands of cores); it would run on anywhere from a handful to
  a few dozen cores in practice, not the massive core counts the code is built to scale to.

**fake_spectra** (github.com/sbird/fake_spectra, README fetched directly):
- Post-processing tool only — reads existing Gadget/Arepo HDF5 snapshots and extracts mock
  spectra / P1D. **Does not run any physics of its own**, i.e. it is the cheap part of the
  pipeline relative to MP-Gadget.
- Lightweight: `pip3 install fake_spectra`, core deps are just numpy + h5py; OpenMP and optional
  MPI (mpi4py) speed things up but a single machine can run it. 10,000 mock spectra per snapshot
  (as used in this paper) is a modest post-processing job, not an HPC-scale one.
- **Conclusion: fake_spectra is not the bottleneck. MP-Gadget (the hydro sim itself) is 100% of
  the compute-cost question.**

## 4. This-VM feasibility (measured directly, not assumed)

```
nproc            → 8 cores
free -h           → 29 GiB RAM total, ~24 GiB free
nvidia-smi        → FAILS ("couldn't communicate with the NVIDIA driver") — no working GPU,
                     despite CUDA/cuDNN libraries present on disk (no device backing them)
df -h             → 107 GB free on / (root), 418 GB free on the 500GB data disk
mpirun/mpicc      → NOT FOUND (which returns nothing for either)
dpkg -l | mpi     → NO MPI package installed (openmpi/mpich absent entirely)
python3 -c "import mpi4py" → ModuleNotFoundError: No module named 'mpi4py'
OS                → Ubuntu 22.04.5 LTS; gcc/g++/gfortran 11 & 12 present (a real compiler
                     toolchain exists, just no MPI/GSL/PFFT stack on top of it)
```

This **confirms and extends** the prior finding (Cobaya/mpi4py investigation): there is **no MPI
of any kind on this VM** — not `mpi4py`, not system `openmpi`/`mpich`, not even the `mpicc`
compiler wrapper. MP-Gadget's mandatory MPI + GSL + PFFT stack is entirely absent. There is also
**no GPU** (driver-less; irrelevant anyway since MP-Gadget has no GPU path). 8 cores / 29 GB RAM
is a workstation-class allocation, not a cluster allocation.

**This VM cannot run MP-Gadget today.** Getting even one test run going would first require
installing (system-level, likely requiring sudo/apt or from-source builds not normally permitted
in this environment): an MPI implementation, GSL, FFTW-with-MPI, and PFFT. That is itself a
nontrivial systems-engineering task with no guarantee of clean success in a constrained VM
(PFFT in particular is not a standard Ubuntu apt package). Even after clearing that bar, 8 cores
is enough to run *one* small 10 Mpc/h box at a time, seriously slowly relative to any real HPC
allocation, and would need to do so 210 times serially (or however many runs the extension needs)
— not something a single VM should be doing regardless of whether MPI is installed.

## 5. Costed estimate (labeled ESTIMATE — no core-hour figure is stated anywhere in the paper
   or repo; the following is an order-of-magnitude engineering estimate from the confirmed box
   size/resolution/run count, not a sourced number)

- **Compute requirement class:** HPC cluster / cloud HPC allocation with MPI. **Not** achievable
  on this VM as-is; **not** GPU-acceleratable (MP-Gadget has no GPU path so buying/renting a GPU
  instance would not help — the correct spend is CPU-cluster core-hours + MPI-capable
  infrastructure, likely a cloud HPC cluster (e.g. GCP HPC-toolkit / AWS ParallelCluster) or a
  university/national HPC allocation, not a bigger single VM).
- **Simulation count needed:** To reproduce the existing design's statistical power at new
  z-slices, the natural approach is to **re-run the same 210-configuration LHS design**
  (100 paired MFDM+CDM + 10 MFDM-only test points) but with `z_end` extended down from 4.2 to the
  new lowest target z — since each run must integrate from z=99 anew (no restart files
  available), this is **not a `--continue-from-z=4.2` operation**; it is a full fresh 210-run
  campaign, now with a slightly longer/more nonlinear integration window. A reduced design (the
  paper itself tests emulator quality at `max_index` = 25/50/100 pairs, suggesting a 25–50-pair
  reduced set is a real, methodologically-supported cheaper fallback for a first-pass/proposal
  stage — see §6) would cut this roughly in proportion, e.g. ~50–130 runs instead of 210.
- **Wall-clock, per configuration:** rough estimate for a 10 Mpc/h, ~268M-particle Quick_Lya box
  integrated z=99→~2.2 (vs. the original z=99→4.2): tens to a few hundred CPU-core-hours per run
  is a plausible band for the *original* z=99→4.2 integration on typical HPC hardware, given how
  small/cheap the authors clearly engineered this box to be (small volume, Quick_Lya trick, 210×
  repeats implies each run was individually affordable to them). Continuing to z≈2.2 roughly
  doubles the simulated cosmic time (age of universe ~1.4 Gyr at z=4.2 vs ~2.5 Gyr at z=2.2) and
  enters a more nonlinear regime (smaller/more timesteps), so a **1.5–3× per-run cost increase**
  over the original z=4.2 stopping point is a reasonable engineering assumption. Net: **very
  roughly ~150–1,000+ core-hours per extended run**, **×~50–210 runs → order 10,000–200,000+
  core-hours total** for the hydro-simulation campaign alone (fake_spectra post-processing and NN
  retraining are comparatively negligible, hours to low-hundreds of core-hours in total).
- **"Start today on this VM" vs "needs new infrastructure/budget":** unambiguously the latter.
  This is a multi-tens-of-thousands-of-core-hours HPC campaign requiring an MPI-capable cluster
  this project does not currently have access to (cloud HPC rental or an institutional allocation
  would both need a budget/access decision, not an engineering one). It is **not startable on
  this VM today under any configuration** — the blocker is architectural (no MPI stack, single
  8-core node) as well as scale (a single 8-core VM running 50–210 serial multi-hundred-core-hour
  jobs would take weeks-to-months of VM-months even before considering MPI installation).
- **NN retraining/emulator work itself, once new sim data exists:** cheap and feasible on this VM
  or similar — CPU-only, small network, no GPU or MPI required for `emu_train.py` itself.

## 6. Cheaper-alternative check (quick, not exhaustive — per scope)

- A targeted web search ("public Lyman-alpha forest 1D flux power spectrum emulator fuzzy dark
  matter axion z=2.2 z=2.8 z=3.4 simulation suite") surfaced no public simulation suite or
  emulator covering mixed-FDM (m,f) parameters at DESI's low-z range. This is consistent with
  the WP-E6 v2 proposal's own P1 finding already on record in this project (LaCE/cup1d/lym1d are
  ΛCDM-shaped with no FDM axis; axionCAMB only fixes the linear transfer function, not a full
  hydro P1D emulator; axionHMcode is the wrong observable and calibrated only at 1e-21 eV; no
  code release was found for the Liu/Gong/Zhou 2026 emulator's would-be low-z extension). No new
  contradicting suite was found.
- Within `lya-mfdm` itself, a genuinely cheaper partial option is the **reduced-LHS fallback the
  paper's own code already exercises**: `emu_train.py`'s `max_index` loop over `[25, 50, 100]`
  training pairs, with accuracy-vs-N plotted in `plots/compare_10_validation_N100.pdf` and
  `plots/compare_CV_0_to_99_N80.pdf`. A first extension pass could plausibly target ~25–50 paired
  runs (50–100 sims) at one new z-slice only (e.g. the DESI bin nearest 4.2, working outward) to
  get an early accuracy/cost signal before committing to the full 210-run, 3-new-z-slice campaign
  — this would cut the core-hour estimate in §5 by roughly 2–4× for a first checkpoint, at the
  cost of wider emulator uncertainty (which is exactly the tradeoff the paper's own N=25/50/100
  comparison plot is designed to quantify).

## Bottom line

This is a **real HPC infrastructure decision, not a task this VM or project can start today**.
The technical scoping is unambiguous and independently cross-checked from both the paper text and
the raw pickled training data: extending z-coverage means re-running MP-Gadget's full z=99→z_target
hydrodynamical integration for on the order of 50–210 small-but-real (10 Mpc/h, ~268M-particle)
simulation configurations — because the existing runs physically stop at z=4.2 with no retained
restart state, there is no cheap "just output more snapshots" path. MP-Gadget mandates an
MPI+GSL+PFFT toolchain this VM entirely lacks (confirmed: no `mpirun`, no `mpicc`, no `mpi4py`, no
MPI packages at all — the same blocker already found for Cobaya, now confirmed to block the
simulation layer too), has no GPU acceleration path (irrelevant given the VM also has no working
GPU driver), and the estimated cost — very roughly 10,000–200,000+ core-hours, labeled explicitly
as an unsourced order-of-magnitude estimate since neither the paper nor repo states a compute
figure — sits squarely in cloud-HPC-cluster-rental or institutional-allocation territory. The one
methodologically real cost-reduction lever already visible in the codebase is running a reduced
25–50-pair LHS design at a single new z-slice first (the paper's own N=25/50/100 comparison
machinery) to get an early accuracy/cost signal before committing to the full campaign; there is
no public/existing FDM-aware low-z P1D simulation suite found that would let this be skipped
entirely. Recommendation: treat this as a **separate infrastructure/budget decision for T0**, not
something to fold into the current VM-based Stream 3 workflow.
