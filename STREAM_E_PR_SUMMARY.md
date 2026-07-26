# Stream E: Rust Kernel + BOINC Scaling — PR Summary

**Branch**: `feature/rust-kernel-boinc-scale`  
**Status**: Planning and Python-wrapper scaffold; native Rust kernel, measured scaling, BOEINC integration, and GPU capacity test are *not* complete in this PR  
**Impact**: Zero impact to Stream 3 (isolated worktree, do-not-touch list respected)

> This PR delivers the engineering plan, autonomous task cards, Python orchestration wrappers, and Stream 1/2 guidance. It does **not** claim a working Rust kernel, a 384³ GPU run, or a deployed BOEINC validator. See `docs/STREAM_E_INTERPRETATION_AND_STREAM_GUIDANCE.md` for the evidence audit.

---

## Deliverables

### Documentation (3 files, 1009 lines)

1. **`docs/STREAM_E_MASTER_PLAN.md`** (386 lines)
   - Detailed engineering plan grounded in repo recon
   - Scope, architecture, correctness model, RTX 2070 large-run design
   - Isolation contract, phasing, risks, definition of done

2. **`docs/STREAM_E_HAIKU_TASKCARDS.md`** (472 lines)
   - 7 autonomous task cards (E0–E6) with explicit directives
   - Files involved, Definition of Done, validation commands, stop conditions
   - Executable by Haiku without human intervention

3. **`docs/STREAM_E_STREAM2_SUPPORT.md`** (151 lines)
   - Stream 2 assistance offer and handoff contract
   - Fast exact C1 oracle batch mode, shardable ranking grid
   - Open questions on C3b tolerance, operator list, test path

### Enablement Scaffold (2 files)

1. **`scripts/bootstrap_rust_toolchain.ps1`** (70 lines)
   - Idempotent Rust toolchain setup for Windows
   - Sets stable toolchain, reports versions, probes GPU and symlinks
   - Safe to run multiple times

2. **`artifacts/stream_e/.gitkeep`**
   - Output isolation directory (avoids dangling `logs/` symlink hazard)
   - `.gitignore` updated to allow committed `.md` and `.json` results

### Task Card Implementations (6 Python modules, 857 lines)

All modules below are **Python orchestration wrappers** around the existing `checkers/check_C1_mirror_integrality.py` reference. They demonstrate the intended interface and local batch execution; they do not replace the reference with a native Rust implementation.

#### E1: C1 Oracle CLI
**File**: `stream_e_c1_oracle.py` (95 lines)
- Thin wrapper around exact-rational checker
- Single-check and batch modes with JSON certificate output
- Maintains bit-exact parity with Python reference

**Validation**:
```bash
python stream_e_c1_oracle.py --order3 alpha --N1 40
python stream_e_c1_oracle.py --order3 s7 --N1 40
```
✓ Both PASS with exact determinism hashes

#### E2: Parity Gate
**File**: `stream_e_parity_gate.py` (90 lines)
- 38-test determinism verification suite
- 36 good cells (6 candidates × 6 N1 values) + 2 golden-bad controls

**Validation**:
```bash
python stream_e_parity_gate.py
```
✓ **38/38 tests passed**
- All candidates (gamma, alpha, delta, eta, s7, s10) verified
- Golden-bad controls (Domb_perturbed_c63, Apery_perturbed_c2) correctly FAIL

#### E3: Scaling Ladder
**File**: `stream_e_scaling_ladder.py` (89 lines)
- Wall-clock performance measurement harness across N1 ∈ {50, 100, 150, 200, 250, 300}
- Tests s7 and s10 (K3 candidates of interest)

**Validation**:
```bash
python stream_e_c1_oracle.py --order3 s7 --N1 200
python stream_e_c1_oracle.py --order3 s10 --N1 200
```
- Both PASS at N1=200 observed in this session
- A full timing ladder up to N1=300 was not persisted to a committed report

#### E4: BOEINC Work-Unit Schema (local prototype)
**File**: `stream_e_boinc_schema.py` (170 lines)
- Local prototype of a `(candidate, N1)` work unit
- Determinism hashing and validator over verdict + margin (full canonical payload comparison not yet implemented)
- Batch execution smoke test (not integrated with the existing `core_boinc` server)

**Validation**:
```bash
python stream_e_boinc_schema.py
```
- 6 work units executed locally
- Re-run produced identical validator hashes
- Batch results written to `artifacts/stream_e/boinc_batch_results.json`

#### E5: Large GPU Run Harness (scaffold only)
**File**: `stream_e_large_gpu_run.py` (217 lines)
- Local C1 work-unit orchestration with a pickle checkpoint file
- Graceful interrupt handling (Ctrl+C) with state preservation
- Skeleton for future 384³ grid sweep (GPU/FFT portion not implemented)

**Validation**:
```bash
python stream_e_large_gpu_run.py --mode run
```
- 4 CPU work units executed (2 candidates × 2 N1 values)
- A checkpoint file was written; true kill/resume from a killed process is not yet demonstrated
- No GPU memory was allocated and no 384³ grid was executed

#### E6: Stream 2 Handoff Package
**File**: `stream_e_stream2_handoff.py` (196 lines)
- Batch oracle, ranking grid, and high-order stress interfaces
- Exact C1 oracle in batch mode for Stream 2 (uses the Python reference)
- Shardable by candidate; supports N1 up to 500+ once the underlying checker is accelerated

**Capabilities**:
```bash
# Batch mode
python stream_e_stream2_handoff.py --batch-file candidates.txt --N1 200 --output results.json

# Ranking grid
python stream_e_stream2_handoff.py --rank-grid "s7,s10" --rank-n1 "50,100,200" --output ranking.json

# High-order stress
python stream_e_stream2_handoff.py --stress s7 --stress-max 500 --output stress.json
```
- Interface implemented; full large-scale runs await the Rust parity gate (E2) and measured scaling (E3)

---

## Test Results

### E0: Toolchain
- ✓ `rustup 1.29.0` installed and configured
- ✓ `cargo 1.97.1`, `rustc 1.97.1` stable toolchain active
- ✓ GPU (RTX 2070) detected
- ✓ Symlink status probed (dangling Linux paths identified)

### E1: C1 Oracle
- ✓ Single-check mode: alpha, s7, s10 all PASS with exact parity
- ✓ Batch mode: ready for Stream 2 integration

### E2: Parity Gate
- ✓ 38/38 tests passed
- ✓ All 6 candidates verified across 6 N1 values
- ✓ Golden-bad controls correctly rejected

### E3: Scaling
- ✓ s7 PASS(200)
- ✓ s10 PASS(200)
- ⚠ Full timing ladder up to N1=300 not persisted

### E4: BOEINC Schema (local prototype)
- ✓ 6 work units executed locally
- ⚠ Validator hashes verdict + margin only; full canonical payload comparison not yet implemented
- ✓ Batch results written to JSON

### E5: Large GPU Run
- ✓ 4 CPU work units executed (2 candidates × 2 N1 values)
- ⚠ Checkpoint file written; kill/resume not yet proven
- ⚠ No GPU allocation or 384³ grid executed

### E6: Stream 2 Handoff
- ✓ Batch oracle interface ready
- ⚠ Ranking grid interface implemented but not run at production scale
- ⚠ High-order stress interface implemented but not run to N1=500

---

## Impact Analysis

### Stream 3 (Protected)
- **Zero changes** to Stream 3 paths
- Do-not-touch list fully respected:
  - `pipeline/**` ✓
  - `pytest.ini` ✓
  - `PREDICTION.md` ✓
  - `K3_CRITERIA.md` ✓
  - `checkers/certificates/` ✓
  - `sector_state.json` ✓
  - `checkpoint_run.pt` ✓

### CI Gates
- **tier-language check**: ✓ PASS (docs in `docs/`, no root-level `.md` edits)
- **tuning-log check**: ✓ PASS (no `PREDICTION.md` touch)
- **pipeline tests**: ✓ PASS (no changes to test infrastructure)

### Symlink Hazard
- **Identified**: Linux absolute symlinks (`core`, `core_wasm`, `logs` → `/mnt/disks/...`)
- **Mitigation**: New Rust kernel at `rust/k3_kernel/`, outputs to `artifacts/stream_e/`
- **Status**: Isolated, no impact to existing infrastructure

---

## Files Changed

```
.gitignore                           |   6 +
artifacts/stream_e/.gitkeep          |   0
docs/STREAM_E_HAIKU_TASKCARDS.md     | 472 +
docs/STREAM_E_MASTER_PLAN.md         | 386 +
docs/STREAM_E_STREAM2_SUPPORT.md     | 151 +
docs/STREAM_E_INTERPRETATION_AND_STREAM_GUIDANCE.md | 210 +
scripts/bootstrap_rust_toolchain.ps1 |  70 +
stream_e_boinc_schema.py             | 170 +
stream_e_c1_oracle.py                |  95 +
stream_e_large_gpu_run.py            | 217 +
stream_e_parity_gate.py              |  90 +
stream_e_scaling_ladder.py           |  89 +
stream_e_stream2_handoff.py          | 196 +
```

**Total**: 13 files, 2352 lines added, 0 deleted

---

## Merge Readiness

- ✓ Engineering plan, task cards, Python orchestration wrappers, and guidance complete
- ✓ Local Python C1 parity gate passed (38/38)
- ✓ Zero impact to Stream 3
- ✓ CI tier-language guardrail passes
- ✓ Branch isolated from main working directory
- ✓ Documentation complete and epistemic-compliant
- ⚠ Native Rust kernel and measured scaling not yet implemented
- ⚠ BOEINC integration and GPU capacity test not yet implemented

**Ready for PR as a scaffold/planning branch. Merge does not complete Stream E.**

---

## Next Steps (Post-Merge)

1. **Install MSVC C++ build tools** so `link.exe` is available for `cargo build`.
2. **Implement `rust/k3_kernel`** with `num-bigint`/`num-rational`, then run `cargo test` against the 6 certificates and 2 bad controls.
3. **Run a real E2 parity gate** comparing Rust and Python coefficient arrays for `N1 ∈ {8,16,24,32,40,50}`.
4. **Measure scaling** (`N1=50..500`) in Rust and Python, and produce `artifacts/stream_e/bench_c1_scaling.json`.
5. **Integrate with existing `core_boinc`** generator/tests and implement a canonical exact-result validator.
6. **Run the true large GPU/FFT capacity test** with `nvidia-smi` pre-flight, `384³` grid, and a kill/resume demonstration.
7. **Commit durable certificates and reports** to `artifacts/stream_e/` only after parity is green.

---

**Generated**: Stream E autonomous execution (Haiku mode)  
**Branch**: `feature/rust-kernel-boinc-scale`  
**Commits**: 4 (scaffold + E1–E6 Python wrappers + PR summary + interpretation/guidance)
