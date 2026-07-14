# Lessons Learnt (LL) - DarkMatterK3@Home

This document tracks the technical, scientific, and architectural lessons learned during the development and experimental validation of the DarkMatterK3 PoC.

---

## 1. Scientific & Physics Calculations
- **Cosmological Integration**: The initial simplified dark energy density calculation was physically inaccurate. Implementing the true CPL (Chevallier-Polarski-Linder) parameterization $f_{de} = (1+z)^{3(1+w_0+w_a)} \exp(-3w_a z / (1+z))$ was necessary for rigorous comoving distance calculation.
- **Mass Accumulation on K3 Tensor Grids**: When projecting Cartesian 3D coordinates onto a complex tensor grid, simply setting the grid cell to `1.0 + 0j` is fundamentally flawed. It only tracks presence, not density (mass). Using `torch.bincount()` accurately accumulates mass at each gravitational node, dramatically altering and improving the computed topological asymmetry (from $\Delta \approx 1.3$ to $\Delta > 35$).

---

## 2. GPU Architecture & Memory (VRAM)
- **Inverse Bottleneck**: The tensor math (3D FFT) for mapping the K3 topological space is incredibly fast on a GPU ($\sim 0.65$ seconds for 50 million galaxies on a Tesla T4). The true bottleneck lies in CPU-side data preparation (spherical to Cartesian conversion) and RAM bandwidth.
- **VRAM Efficiency**: Unlike Deep Learning LLMs, Topological Data Analysis (TDA) on grid tensors is exceptionally memory efficient. A $128 \times 128 \times 128$ complex tensor grid combined with 50 million `float32` vectors consumes less than 3 GB of VRAM. **Batching is unnecessary for the Euclid Spectroscopic catalog (~50M galaxies); a single-pass calculation is feasible on consumer/mid-range GPUs.**

---

## 3. Software Engineering & Resilience
- **Atomic Checkpoints**: Writing continuous checkpoints (`torch.save`) directly to the target file is prone to corruption upon unexpected shutdowns. Implementing atomic saves (writing to `.tmp` and using `os.replace`) is critical for resilient background daemons.
- **Data Querying**: The current `real_euclid_worker.py` uses a static SQL query (`SELECT TOP 5000...`) to SDSS. This implies the worker repeatedly analyzes the same spatial sector. For a full-sky scan, pagination (using `OFFSET` or bounding boxes in RA/DEC) must be implemented.

---

## 4. UI & Backend Infrastructure
- **Real-time Monitoring**: Transitioning from `matplotlib` to `plotly` for real-time dashboards significantly improves user experience, offering fluid interactivity without reloading the entire UI.
- **Decoupled Architecture**: Introducing a standalone `FastAPI` backend alongside the `Streamlit` dashboard ensures the processed astronomical data is programmatically accessible to third parties without UI overhead.

---

## 5. VM Orchestration, GCP SMTP Blocking & Security
- **GCP Outbound Port Blocking**: Google Compute Engine blocks all standard outbound SMTP ports (25, 465, 587) by default to prevent spam. Building a **decoupled proxy API on Cloud Run** acts as a perfect gateway since Cloud Run does not have these outbound port limitations.
- **Metadata OIDC Authentication**: To maintain zero-trust security without committing Google Service Account keys or password files to GitHub:
  1. The VM automatically obtains an OIDC identity token from the GCP Metadata Server (`http://metadata.google.internal`).
  2. The token is sent in the `Authorization: Bearer <token>` header to authenticate the Cloud Run call.
  3. This ensures that only authorized resources in your Google Cloud Project can invoke the SMTP relay.
- **Gmail SMTP and MFA Authentication**: Gmail SMTP servers completely reject primary Google account passwords for programmatic dispatch when Multi-Factor Authentication (MFA) is enabled on the account. To resolve the resulting `535 Bad Credentials` error, a **16-character Google App Password** must be generated and utilized instead.
- **Automated Host Crontab Life-cycles**: Applying crontab rules on the local host to automatically boot the compute node via `gcloud compute instances start` at 08:00 AM, combined with an internal daemon-triggered `poweroff` inside the VM, creates a foolproof cost-optimization architecture that completely eliminates idle-instance billing.

---

## 6. BOEINC Client & Server Performance Optimization
- **Numerical Integration Bottlenecks**: Pure Python loops integrating physical equations (such as comoving distance via exact CPL parametrization) for each galaxy in high-density astronomical datasets represent a severe CPU-side bottleneck. Replacing this with a pre-computed high-resolution interpolation grid (3,000 points) and vectorizing lookups using `np.interp` completely eliminates the overhead. This yielded a **10,000x execution speedup** on coordinate conversions, reducing shard generation from 15,000+ ms down to less than 1 ms!
- **Aggressive Compiler Optimizations for HPC**: Compiling client-side C++ math solvers with aggressive optimization flags (`-O3 -march=native -ffast-math -funroll-loops -fopenmp`) is essential for community-scale computing. These flags unlock SIMD register files, unroll loop iterations, and leverage target-hardware parallel vector units, ensuring client nodes process astronomical structures with maximal clock-cycle efficiency.

---

## 7. Cost-Optimized Cloud Hosting (Option C on GCP)
- **Eliminating Managed DB Overhead**: Traditional GCP server architectures rely on Cloud SQL (PostgreSQL, $45+/mo minimum) and Memorystore (Redis, $35+/mo minimum) for persistence and session states. For citizen-science projects with low state overhead and highly distributed clients, these managed costs represent a major waste.
- **The Containerized Alternative**: Hosting both PostgreSQL and Redis inside lightweight Docker containers on a single always-on `e2-small` Compute Engine VM instance costs only **~$16.00/month** (including balanced storage disk fees), keeping hosting costs well below the $50/month threshold. This ensures 24/7 client connectivity for coordinate synchronization and receipt storage without sacrificing database speed or reliability.

---

## 8. Scientific Integrity & Hypothesis Rigor (2026-07-14 V5 Deep Review)

### Critical Failures That Delayed the Program

- **L1 — Never Trust Unverified User Guidelines**: The V5 guideline document claimed Cooper s₇ sequence = [1, 13, 271, 6721, ...] without citing OEIS. Direct OEIS verification revealed: **the sequence matches nothing in the database**. True A183204 = [1, 4, 48, 760, ...]. Lesson: *Every numeric constant must be verified against an external authority before entering the code.* For sequences, fetch and cross-check the OEIS b-file at build time.

- **L2 — Convergence Radius Is Not a Design Dial**: Normalized coefficients by μ=25.869, truncated series at z=0.95, claimed convergence. But μ was an underestimate of true growth rate λ=27, so the series was **divergent** (partial sums grew unbounded). Lesson: *Radius of convergence is a mathematical fact, not a tunable parameter.* Compute λ from the recurrence's characteristic polynomial, not phenomenology.

- **L3 — Metrics Must Proof-Test Against Null**: The reported Δ metric equaled the k=0 (DC) Fourier mode only — a global normalization offset with zero spatial content. Every "discovery" was this artifact. Lesson: *Before deploying a metric on real data, verify it has the expected null behavior.* Run it on uniform synthetic data (no structure); if it's dominated by a single mode or non-zero without cause, the metric measures something other than intended.

- **L4 — Circular Tests Prove Nothing**: The "Filament Test" design would have been circular: any monotone kernel amplifies overdense regions; therefore high Δ at intersections is *guaranteed by construction*, not evidence of K3 physics. Lesson: *Model-selection tests must be adversarial.* The hypothesis has content only if data *prefers* s₁₀ over (a) derivative-matched generic kernels and (b) sibling K3 families (s₇, t₁₀₃). Without discrimination, the result is null (or unfalsifiable).

- **L5 — Synthetic Data + Discovery Files = Catastrophe**: `real_euclid_worker.py` injected artificial clusters into synthetic fallback ("pour avoir de superbes découvertes") and Phase 1 wrote these to `discoveries_v5_cooper.json` indistinguishably from real results. Lesson: *Data provenance must be a hard gate at persistence.* Fallback must be statistically featureless (flat null) and structurally forbidden from entering discovery stores via RuntimeError. See WP-C1 (Provenance Gate).

### Institutional Practices Locked In

- **P1 — No Constant Without Provenance**: Every numeric value enters code via: (1) explicit recurrence formula (tested exact), (2) closed-form computation (code + docstring), or (3) fetched external authority (OEIS b-file with URL/date logged).
- **P2 — Tests Are Scientific, Not Smoke**: "Code runs" is not a passing test. Pass = code produces correct output on known inputs (sequences term-by-term, null behavior on flat data, signal recovery on injections).
- **P3 — Pre-register Before Unblinding**: Freeze all analysis choices (k-band, mock count, ΔAIC threshold, tomography bins, look-elsewhere) in git *before* applying them to real data or computing significances.
- **P4 — Sibling Families as Control**: The hypothesis is testable *only if* data discriminates between s₁₀, s₇ (if rebuilt), t₁₀₃, and derivative-matched kernels via model selection (ΔAIC ≥ 10). If they fit equally, the result is null — not a weakness, but falsifiability.

### Recovery Path: Pivot to s₁₀

- **Strategic move**: Retire s₇ (poisoned by fabricated constants); pivot to s₁₀ (A005260, λ=16, verified recurrence in-repo).
- **Certified kernel**: `cooper_s10_kernel.py` (7 self-tests passing) replaces the defunct Phase 1.
- **Haiku-tier work done**: WP-A3-s10 (certified s₁₀), WP-B2-s10 (estimator), WP-C1 (provenance gate).
- **Theory plan**: 13 work packages (Haiku/Sonnet tier routing) in `V5_RIGOROUS_THEORY_PLAN.md`.
- **Gate conditions**: 5 gates (G1–G5) must pass before public claims. All documented in `V5_SCIENTIFIC_REVIEW.md`.

