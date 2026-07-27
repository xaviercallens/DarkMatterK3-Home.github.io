# Future Phase (deferred): Full-Range Lyα-MFDM Emulator Extension

**Status:** DEFERRED, not abandoned. Recorded 2026-07-27 per Xavier's decision: park this,
proceed now with Option 1 (z≈4.2 slice, see `PHASE1_DECISION_2026_07_27.md`).
**Owner:** T0, whenever infrastructure/budget for this is approved.
**Depends on:** Agent 4 scoping (`briefs/D0_VERIFICATION/PHASE1_A4_EMULATOR_EXTENSION_SCOPING.md`).

---

## What this is

WP-E6 v2 needs a Lyα P1D emulator across DESI DR1's full z≈2.2–4.4 range. The only public
mixed-(m,f) FDM emulator found (`jianxiangl-astro/lya-mfdm`, arXiv:2606.06969) is trained at
exactly 3 redshifts — z=5.0, 4.6, 4.2 — with no retained snapshots below z=4.2. Using DESI's
full range requires generating new training data at lower z, which the source paper's own
methodology shows means **new cosmological hydrodynamical simulations**, not a config tweak.

## Confirmed scope (from Agent 4, cross-checked against the paper + raw training data)

- Existing emulator: 210 separate MP-Gadget runs (100 paired MFDM+CDM + 10 MFDM-only test),
  10 Mpc/h box, 2×512³ particles (~268M particles), each integrated z=99 → z=4.2 and stopped.
- No lower-z restart snapshots exist publicly — extending coverage means fresh full reruns
  (z=99 → target z), on the order of 50–210 configurations depending on how many new z-slices
  and (m,f) points are wanted.
- MP-Gadget mandatorily needs MPI + GSL + PFFT (from its own README), no GPU path.
- **This VM has none of that**: 8 cores, 29GB RAM, no GPU driver, **no MPI at all** (no
  `mpirun`, `mpicc`, or MPI libraries) — the same blocker Agent 1 already hit trying to use
  Cobaya with `mpi4py` installed.
- fake_spectra (sim → mock spectra post-processing) is comparatively cheap; not the bottleneck.
- Order-of-magnitude estimate (unsourced, Agent 4's own): **~10,000–200,000+ core-hours**.
  This is cloud-HPC-cluster or institutional-allocation territory.
- No public FDM-aware low-z P1D simulation suite was found to substitute (quick check only,
  not exhaustive — worth a deeper literature pass if/when this phase is picked back up).

## Where Rust/RunuX optimization actually fits — and where it doesn't

**Does NOT apply:** the dominant cost (~10k–200k core-hours) is the MP-Gadget N-body/SPH
simulation itself — gravity solver + gas physics on a particle mesh. `runux-ai-runtime` is an
AI/LLM inference and training runtime (RISC-V/TPU/GPU/CPU HAL, `no_std` Rust) — it has no
relationship to cosmological N-body/hydro simulation codes. Running MP-Gadget faster is an MPI/
domain-decomposition/PFFT problem, not something a Rust AI runtime addresses. Recording this
plainly so a future revisit doesn't assume the compute problem is solved by tooling that
doesn't touch it.

**Plausibly DOES apply, later:** once new simulation snapshots exist (from wherever they're
sourced — new sims, a future public release, or a collaboration), the *emulator itself* is a
small PyTorch MLP (5-16-... architecture per `emu_train.py`) trained on ~100-210 points via a
5-fold ensemble. That training/inference step is a genuine ML workload, and this is exactly
the class of thing `runux-ai-runtime` targets (memory-safe Rust inference, HAL across CPU/GPU/
TPU/edge). If a next-generation emulator is built in-house rather than reusing the published
PyTorch one, doing the training/inference layer on RunuX instead of PyTorch could be a
legitimate efficiency angle — worth prototyping when this phase is revisited, but it only
touches the cheap 1% of the cost, not the expensive 99%.

## Cheapest real first step, if/when this is approved

Per Agent 4: a reduced 25–50-pair single-z-slice trial run, following the paper's own N=25/50
convergence-study methodology, rather than the full 210-run rebuild. Still requires MPI/GSL/
PFFT infrastructure this VM doesn't have — the first real decision is where that runs (cloud
HPC allocation, institutional cluster, etc.), not how many pairs.

## Reactivation checklist (for whoever picks this up later)

1. Secure HPC/cloud compute with working MPI + GSL + PFFT (this VM cannot run MP-Gadget as-is)
2. Confirm budget class: low end of the 10k-200k core-hour estimate would still be a
   nontrivial cloud spend — get a real quote before committing
3. Re-check for a public FDM-aware low-z P1D simulation suite (deeper search than Agent 4's
   quick pass) — might make new sims unnecessary
4. If proceeding: start with the 25-50 pair single-z trial, not the full 210-run rebuild
5. Only once new snapshots exist: evaluate whether a RunuX-based emulator re-implementation is
   worth prototyping vs. just retraining the existing PyTorch pipeline with more data

---

**This file is the durable record.** No further action on this phase until T0 explicitly
reopens it with a compute/budget answer.
