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
