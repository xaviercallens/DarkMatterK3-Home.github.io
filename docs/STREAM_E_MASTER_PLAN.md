# Stream E — Engineering Scale-Out Master Plan (Rust Kernel + BOEINC Client/Server)

**Branch**: `feature/rust-kernel-boinc-scale`
**Status**: proposal, not merged. Runs in parallel with Stream 1/2 theory and Stream 3 D3 rerun.
**Author tier**: T1 plan for autonomous T2 execution.
**Generated-by**: Claude Opus 4.8 (T1 planner) | **Verified-by**: repository recon (file-level, see §2) | **Reviewed-by**: pending T0

---

## 1. Scope and non-goals

Stream E is **engineering only**. It adds no physics claim, no new candidate, and no new
observable. It makes the *existing* verification stack fast enough and parallel enough that a
large sweep becomes routine instead of a multi-day event.

**In scope**
- A native (non-WASM) Rust kernel for the exact-rational criterion checkers.
- A BOEINC work-unit schema for embarrassingly-parallel `candidate × N` sweeps.
- A full large run on the local Windows RTX 2070 as the reference capacity test.
- Bit-exact parity gating between Rust and the current Python checkers.

**Explicit non-goals**
- No change to any criterion definition (`K3_CRITERIA.md` is frozen for this stream).
- No change to `PREDICTION.md` (avoids the `check_tuning_log.py` gate entirely).
- No change to any Stream 3 file (see §7 "do-not-touch" list).
- No new physics-viability gate. G2/G3/G4 remain as reported by the companion project.

---

## 2. Recon: what already exists (verified file-by-file)

This plan is deliberately built on top of what is already in the repository. The following was
confirmed by direct inspection, not assumed.

### 2.1 Rust assets

| Path | State | Notes |
|---|---|---|
| `core_wasm/Cargo.toml` | **real** | crate `core_wasm`, `cdylib`+`rlib`, `wasm-bindgen`, `rustfft 6.1`, `wee_alloc` |
| `core_wasm/src/lib.rs` | **real, 342 lines** | `compute_density_field_asymmetry` (128³ FFT), `compute_nearest_neighbors_average` (KD-tree), `compute_weak_lensing_shear_fields` (128² FFT), `compute_comoving_distance`, `solve_asymmetric_3_2_check` |
| `core_wasm/src/fft.rs` | **real** | `fftn_3d` |
| `core/rusty_sundials_solver/` | **stub** | `main.rs` is 13 lines, prints two strings, solver calls commented out |
| `core/vendor/cvode`, `nvector`, `sundials-core`, `ai_runtime` | **real, vendored** | full SUNDIALS bindings incl. `arkode`, generated FFI |
| `core/runux_integration/` | **real** | has a committed `target/debug` tree |
| `core/lean4_anchor/K3PicardFuchs.lean` | **stub** | `BettiSignature`, `theorem s1_2_topology_verified` closed by `rfl` |

**Consequence**: there is a real Rust *field/FFT* kernel (`core_wasm`) and a real vendored ODE
stack, but **no** native Rust kernel for the exact-rational criterion checkers. That gap is the
subject of Stream E.

### 2.2 BOEINC assets

| Path | State |
|---|---|
| `core_boinc/boinc_work_generator.py` | real |
| `core_boinc/boinc_bridge_daemon.py` | real |
| `core_boinc/process_all_shards.py` | real |
| `core_boinc/project_xml/{config,workunit_template,result_template}.xml` | real |
| `core_boinc/src/main.cpp` | real native client |
| `core_boinc/test_boinc_suite.py`, `test_boinc_reconciliation.py` | real tests |
| `api/api_dispatcher.py` | real FastAPI dispatcher |
| `boeinc_deployment_plan.md` | real deployment plan (Hetzner/serverless/GCP options, $0–16/mo) |

**Consequence**: the server/client skeleton exists and has tests. Stream E extends the work-unit
schema; it does not rebuild the dispatcher.

### 2.3 Exact-rational checkers (the actual port target)

| Path | Role |
|---|---|
| `checkers/check_C1_mirror_integrality.py` | C1 inverse mirror-map integrality, exact `Fraction` + dual numbers, default `N1=50` |
| `checkers/check_C3_sym2.py` | C3, and owns `ORDER3_AZ_COOPER` + `CERT_DIR` |
| `checkers/check_C3b_moduli_map.py` | C3b moduli map |
| `checkers/certificates/C1_mirror_{gamma,alpha,delta,eta,s7,s10}.json` | existing certificates |
| `checkers/tests/test_c1_mirror_integrality.py` (+ C3, C3b, refs) | existing tests |

C1 internals worth noting, because they set the performance ceiling:

- `_mul(p,q,N)` — O(N²) `Fraction` multiplies.
- `_inv(p,N)`, `_exp(p,N)` — O(N²).
- `_revert(q,N)` — **O(N³)** and it calls `_mul` inside the inner loop, so the true cost is
  closer to O(N⁴) `Fraction` operations, each with unbounded numerator/denominator growth.
- `_frobenius` carries `_Dual` pairs of `Fraction`, so coefficient bit-length grows with `n`.

**Consequence**: C1 at `N1=50` is tolerable; `N1=200+` is not, and the blocker is `_revert`
plus rational bit-growth. This is the single highest-value Rust port in the repository: it is
pure, deterministic, allocation-heavy, and trivially parallel across candidates.

### 2.4 Parity precedent

`tools/wasm_parity_check.py` compares Torch-CPU against WASM with tolerance `1e-4`. That
tolerance is correct for float FFT work. It is **the wrong model for C1**: C1 is exact rational
arithmetic, so Stream E requires **bit-exact equality**, not a tolerance. See §5.

### 2.5 Toolchain and hardware (measured on this machine)

```
rustup      installed, but NO default toolchain configured
            ("rustup could not choose a version of cargo to run")
GPU         NVIDIA GeForce RTX 2070, 8192 MiB, driver 591.86
```

### 2.6 CI gates (merge-blocking)

`.github/workflows/epistemic-guardrails.yml` runs on every push and PR:

1. `python3 scripts/check_tuning_log.py --selftest`
2. `python3 scripts/check_tuning_log.py`
3. `python3 scripts/check_tier_language.py --selftest`
4. `python3 scripts/check_tier_language.py`
5. `python3 -m pytest pipeline/tests/ -v`  ← **merge-blocking, and it is Stream 3 territory**

Scope facts that matter for Stream E:
- `check_tier_language.py` scans **repo-root `*.md` only, non-recursive**, and only inside
  preamble / `Abstract` / `Summary` / `Overview` blocks. Stream E docs live in `docs/`, so they
  are out of scope — but keep root-level `*.md` edits to zero anyway.
- `check_tuning_log.py` only fires on `PREDICTION.md` edits. Stream E must not touch it.
- `pytest.ini` has `norecursedirs = ... core_wasm core_boinc tools ...` and
  `testpaths = . api core`. **`checkers/` is not in `testpaths`**, so checker tests are not
  currently run by the default `pytest` invocation. Stream E adds an explicit invocation rather
  than editing `pytest.ini` (editing it would change what Stream 3's CI runs).

---

## 3. The blocker that must be fixed first: broken symlinks on Windows

`git ls-files -s` shows mode `120000` (symlink) for:

```
core                 -> /mnt/disks/disk-socrateai-local-1/SocrateAI-storage/core
core_wasm            -> /mnt/disks/disk-socrateai-local-1/SocrateAI-storage/core_wasm
logs                 -> /mnt/disks/disk-socrateai-local-1/SocrateAI-storage/logs
archives             -> .../archives
ui_loom              -> .../ui_loom
EuclidClusterViz     -> .../EuclidClusterViz
additional_storage   -> .../additional_storage
```

These are absolute **Linux GCP paths**. In the main Windows working copy they happen to be
materialised as real directories, but in any fresh Windows clone or `git worktree` they are
dangling. Two hard consequences:

1. **`core_wasm` and `core` are unbuildable from a fresh Windows checkout.** Any Haiku task that
   assumes `cargo build -p core_wasm` works from a clean clone will fail for a reason that has
   nothing to do with its own code.
2. **`logs/` is not a safe output target.** Stream E must write to a real, committed,
   Windows-valid directory. This plan uses **`artifacts/stream_e/`**.

Therefore task **E0** is mandatory and blocking, and the new native crate is placed at
**`rust/k3_kernel/`** — a real in-repo path, *not* under the `core` symlink.

---

## 4. Architecture

### 4.1 Where each workload belongs

| Workload | Arithmetic | Home | Reason |
|---|---|---|---|
| C1 / C3 / C3b criterion checks | exact rational | **`rust/k3_kernel` (native Rust, `rayon`)** | pure, deterministic, allocation-bound, embarrassingly parallel over candidates |
| 3D density-field asymmetry, weak lensing | `f32`/`f64` FFT | **GPU via Torch CUDA** on the 2070; `core_wasm` stays the browser/CPU fallback | FFT is memory-bandwidth bound; already implemented twice |
| `candidate × N` sweep fan-out | n/a | **BOEINC** work units | trivially shardable, no shared state |
| Picard–Fuchs numeric integration | `f64` ODE | `core/vendor/cvode` (currently unused stub) | deferred to Stream E phase 3; not on the critical path |

### 4.2 Target layout (new files only)

```
rust/
  k3_kernel/
    Cargo.toml            # native lib + bin, no wasm-bindgen
    src/
      lib.rs              # public API
      series.rs           # exact Fraction power series: mul, inv, exp, revert
      dual.rs             # dual numbers in the indicial parameter rho
      frobenius.rs        # a_n(0), a_n'(0)
      c1_mirror.rs        # mirror_map_zq + verify_c1, certificate-compatible output
      operators.rs        # ORDER3_AZ_COOPER table mirrored from Python
    benches/
      c1_scaling.rs       # N1 sweep
    tests/
      parity_certificates.rs
tools/
  rust_parity_check.py    # bit-exact Rust vs Python gate
scripts/
  bootstrap_rust_toolchain.ps1
  run_stream_e_gpu_large_run.ps1
artifacts/
  stream_e/.gitkeep       # all Stream E output lands here (never logs/)
docs/
  STREAM_E_MASTER_PLAN.md         # this file
  STREAM_E_HAIKU_TASKCARDS.md     # executable task cards
  STREAM_E_STREAM2_SUPPORT.md     # Stream 2 assistance
```

Nothing above collides with an existing path, and nothing sits under a symlinked directory.

### 4.3 Rust dependency choice

Use `malachite` **or** `num-rational` + `num-bigint`. Recommendation: **`num-rational`/`num-bigint`**
for the first cut, because the Python semantics map 1:1 onto `BigRational` and correctness is
easier to argue than raw speed. Optimising to `malachite` (typically 2–5× faster on rational
GCD-heavy work) is a *later* task, gated on parity already being green. Do not start there.

`rayon` for the candidate-level parallel loop. No `unsafe`. No GPU in this crate.

---

## 5. Correctness model — the non-negotiable part

C1 is exact rational arithmetic. Any correct reimplementation must produce **identical
rationals**, not nearby floats. So the parity gate is:

1. For every name in `{gamma, alpha, delta, eta, s7, s10}` and every
   `N1 ∈ {8, 16, 24, 32, 40, 50}`:
   the Rust `z(q)` coefficient list must equal the Python list **as exact numerator/denominator
   string pairs**, elementwise.
2. `status`, `verdict`, `margin_max_denominator`, `first_non_integral_order` must match exactly.
3. `determinism_hash` must match, and must be stable across two consecutive Rust runs.
4. The golden-bad controls `Domb_perturbed_c63 = (10,4,63,0)` and `Apery_perturbed_c2 = (17,5,2,0)`
   must **FAIL** in Rust exactly as they FAIL in Python, with the same
   `first_non_integral_order`.

A tolerance-based comparison is an automatic **reject** for this stream. If Haiku finds itself
writing `abs(a-b) < eps` for a C1 quantity, the task is being done wrong.

**Tier discipline**: a Rust port changes *who computed* a number, not its epistemic status. C1
remains `Tier B → A(N₁-bounded) on pass`. Extending `N1` from 50 to 500 raises the bound, it does
not convert evidence into proof. Certificates emitted by Rust must carry
`"computed_by": "rust/k3_kernel@<git-sha>"` alongside the unchanged tier string, and must not be
written into `checkers/certificates/` until parity is green — they go to
`artifacts/stream_e/certificates/` first.

---

## 6. Full large run on the local RTX 2070 (Windows)

This is the reference capacity test. Two halves: a CPU half (the Rust kernel) and a GPU half
(the field pipeline). They are independent and can run concurrently, because the Rust kernel
never touches the GPU.

### 6.1 VRAM budget, 8192 MiB, `complex64` (8 bytes/cell)

| Grid | Cells | 1 grid | Live grids in `compute_density_field_asymmetry` | Peak |
|---|---|---|---|---|
| 128³ | 2.10 M | 16 MiB | ~5 | ~80 MiB |
| 256³ | 16.8 M | 128 MiB | ~5 | ~640 MiB |
| **384³** | 56.6 M | **432 MiB** | ~5 | **~2.1 GiB** |
| 512³ | 134.2 M | 1024 MiB | ~5 | ~5.0 GiB |
| 768³ | 452.9 M | 3456 MiB | ~5 | ~16.9 GiB ✗ |

The current Python reference (`tools/wasm_parity_check.py`) holds `density_grid`,
`k3_space_3d`, `S12_field`, `S21_field`, and the `ifftn` result concurrently — hence the
"~5 grids" column.

**Decisions**
- **Default large-run grid: 384³.** ~2.1 GiB peak leaves headroom for driver overhead, the
  display, and fragmentation on an 8 GiB consumer card.
- **512³ is a stretch target and requires fusion**: build `S12_field - S21_field` in place
  instead of materialising both, dropping live grids from ~5 to ~3 (~3.0 GiB).
- **768³ is out of reach** on this card. Do not attempt; it belongs on BOEINC fan-out or a
  larger device.
- Set `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` to reduce fragmentation across a
  multi-hour sweep.
- Parity comparisons stay on **CPU**, matching the existing harness comment
  (`device = torch.device('cpu') # For parity, ensure CPU to avoid precision diffs from CUDA`).
  GPU is for throughput; CPU is for adjudication.

### 6.2 CPU half — Rust kernel sweep

- Candidates: all 6 names in `ORDER3_AZ_COOPER`.
- `N1` ladder: `50 → 100 → 200 → 300 → 500`, stopping a rung early if wall-clock for a single
  candidate exceeds 30 min.
- `rayon` across candidates; single-threaded within a candidate (the series recurrences are
  inherently sequential in `n`).
- Record wall-clock and peak RSS per `(candidate, N1)` into
  `artifacts/stream_e/bench_c1_scaling.json`.
- Expected shape: Python is superlinear and rational-bit-growth dominated. Report the measured
  exponent; **do not pre-commit to a speedup number** in any document. The honest claim is
  "measured X× at N1=50 and Y× at N1=200 on this machine", written after the run.

### 6.3 Resilience — reuse, do not rebuild

The repository already has multi-day run machinery:
`checkpoint_manager.py`, `execute_phase4_multiday.ps1`, `test_v4b_resilience.ps1`,
`test_v4b_resilience.py`, `RUN_V4B_TESTS.md`, `PHASE4_MULTIDAY_GUIDE.md`.

Stream E's runner **wraps these**. It must not introduce a second checkpoint format. Concretely:
checkpoint after each `(candidate, N1)` cell completes, so a killed run resumes at cell
granularity, and the GPU half checkpoints after each shard.

### 6.4 Coexistence with the Stream 3 D3 rerun

The D3 rerun is on the GPU right now. Therefore:

- The GPU half of the large run is **gated**: the runner must refuse to start if another Python
  process is holding >1 GiB of VRAM, and must print what it found.
- The CPU half (Rust kernel) is **safe to run immediately** and is where Haiku should start.
- Default `--max-vram-fraction 0.5` so that even if both run, the 2070 is not oversubscribed.

---

## 7. Isolation contract (protecting Stream 3)

Work happens on `feature/rust-kernel-boinc-scale` in a **separate `git worktree`**, so the Stream 3
working directory is never checked out over. At the time of writing, Stream 3 had uncommitted
modifications to `checkpoint_run.pt`, `pipeline_runs.json`, `sector_state.json`,
`ALIXE_Discovery_Report.*`, and untracked files under `logs/` — a branch switch in the main
directory would have been disruptive.

**Do-not-touch list (hard stop for any Haiku task on this branch)**

```
pipeline/**                      # Stream 3 code + merge-blocking tests
stream3_pipeline.py
sector_state.json
k3_sector_state.json
v4c_sector_state.json
checkpoint_run.pt
pipeline_runs.json
k3_runs.json
discoveries*.json
PREDICTION.md                    # triggers check_tuning_log.py
TUNING_LOG.md
K3_CRITERIA.md                   # criterion definitions are frozen for Stream E
pytest.ini                       # changing testpaths changes Stream 3's CI
checkers/certificates/**         # read-only until parity is green
logs/**                          # broken symlink on Windows; use artifacts/stream_e/
sections/**                      # Stream 1/2 report text
```

Read freely. Write to nothing on that list.

---

## 8. Phasing

| Phase | Task cards | Gate to exit |
|---|---|---|
| **E-0 Unblock** | E0 | `cargo --version` works; `artifacts/stream_e/` exists; symlink hazard documented |
| **E-1 Port** | E1, E2 | Rust C1 bit-exact vs all 6 certificates and both golden-bad controls |
| **E-2 Measure** | E3 | `bench_c1_scaling.json` populated; N1=200 reached; measured speedup written down |
| **E-3 Fan-out** | E4 | work-unit schema + validator accepted by existing `test_boinc_suite.py` style tests |
| **E-4 Large run** | E5 | full 384³ GPU run + full CPU ladder complete, checkpoint/resume proven by a kill test |
| **E-5 Handoff** | E6 | Stream 2 support artifacts delivered (§9) |

E-1 must not be skipped or reordered. Everything downstream is meaningless if parity is not
established first.

---

## 9. Assistance offered to Stream 2

Detailed in `docs/STREAM_E_STREAM2_SUPPORT.md`. In one line: Stream E can give Stream 2 a
**fast, exact, certificate-emitting C1/C3/C3b oracle** so that theory iteration on candidate
operators stops being bounded by checker wall-clock, plus a reusable golden-fixture harness
built on the existing `scripts/s2_01b_golden_data/` loader.

---

## 10. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Rust rational arithmetic diverges from Python `Fraction` semantics (e.g. normalisation of sign, `0/1`) | **high** | bit-exact parity gate at 6 `N1` values before any other work; compare numerator/denominator strings, not values |
| `_revert` reimplemented with a different but "equivalent" algorithm, giving different intermediate rationals | medium | port `_revert` literally first, including its `ztrial`/`comp` structure; optimise only after green |
| Broken symlinks silently break a fresh-clone build | **high** | E0 is blocking and explicitly checks for dangling `core`/`core_wasm`/`logs` |
| GPU contention with the D3 rerun | medium | VRAM pre-flight gate + `--max-vram-fraction 0.5`; CPU half first |
| 8 GiB VRAM ceiling misjudged | medium | budget table in §6.1 derived from `complex64` × live-grid count; 384³ default with 512³ behind a flag |
| Scope creep into physics claims | medium | §1 non-goals; tier string unchanged; certificates quarantined in `artifacts/` until parity green |
| Accidental Stream 3 disruption | **high** | separate worktree + §7 do-not-touch list |
| Committed `core/runux_integration/target/debug` bloats the branch | low | never `cargo build` inside `core/`; new crate is at `rust/k3_kernel` with its own ignored `target/` |

---

## 11. What "done" means for Stream E as a whole

1. `rust/k3_kernel` reproduces C1 bit-exactly for all 6 sporadic operators and both golden-bad
   controls, at `N1 ∈ {8,16,24,32,40,50}`.
2. A measured scaling table exists at `artifacts/stream_e/bench_c1_scaling.json`, with `N1 ≥ 200`
   reached for at least `s7` and `s10`.
3. A BOEINC work-unit schema for `candidate × N1` exists, with an **exact-equality** validator
   (deterministic arithmetic makes replication cheap and adjudication exact).
4. A full 384³ GPU run and the full CPU ladder have completed on the RTX 2070, with a
   demonstrated kill-and-resume.
5. Zero diffs to any path in §7.
6. `epistemic-guardrails` CI green on the PR.
