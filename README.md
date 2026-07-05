# DarkMatterK3@Home

DarkMatterK3@Home is a distributed computing project aiming to prove that the macroscopic large-scale structure of the universe (the Cosmic Web) is homologically equivalent to the microscopic algebraic geometry of K3 surface moduli spaces (specifically the S1,2 Picard-Fuchs integration path).

## Architecture

This project leverages a hybrid architecture to achieve mathematical certainty and massive throughput:

1. **The Anchor (Lean 4)**: Found in `core/lean4_anchor`. Generates the absolutely verified, flawless theoretical baseline of the $S_{1,2}$ topology.
2. **The High-Precision Generator (Rusty-SUNDIALS)**: Found in `core/rusty_sundials_solver`. Uses `rusty-SUNDIALS` to trace the Picard-Fuchs integration path into a highly precise theoretical point cloud.
3. **The Sieve (Runux AI Runtime)**: Found in `core/runux_integration`. Ingests the messy, real-world SDSS observational data at ultra-high speeds via GPU, computing the real-world topological barcode using the `runux-ai-runtime`.
4. **The Proof (Dispatcher)**: The FastAPI layer (`api/`) orchestrates jobs. The Wasserstein distance is calculated not against a python approximation, but against the Lean-verified mathematical constant and the SUNDIALS point cloud.

## Submodules

This repository relies on two core submodules containing the ultra-fast Rust C++ bindings:
- `core/runux-ai-runtime`: The high-performance AI tensor execution graph.
- `core/rusty-SUNDIALS`: The high-precision ODE solver.

To clone this repository and its dependencies:
```bash
git clone --recurse-submodules https://github.com/xaviercallens/DarkMatterK3-Home.github.io.git
```
