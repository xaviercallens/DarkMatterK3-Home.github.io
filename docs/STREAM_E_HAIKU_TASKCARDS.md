# Stream E — Autonomous Task Cards (T2 / Haiku execution)

**Branch**: `feature/rust-kernel-boinc-scale`
**Worktree**: `D:\xdev\DarkMatterK3@Home\DMK3-wt-rust-boinc`
**Companion plan**: `docs/STREAM_E_MASTER_PLAN.md` (read §3, §5, §7 before starting anything)
**Generated-by**: Claude Opus 4.8 (T1 planner) | **Reviewed-by**: pending T0

---

## How to use this document

Each card is self-contained and ordered. Execute **E0 → E1 → E2 → E3 → E4 → E5 → E6**.
Do not reorder. Do not start a card whose *Preconditions* are unmet.

Every card has the same five sections:

- **Directive** — what to do, imperatively.
- **Files** — exact paths you may create or modify. Touching anything else is out of contract.
- **Definition of Done (DoD)** — objective, machine-checkable conditions. All must hold.
- **Validate** — copy-pastable PowerShell. Every command must exit `0`.
- **Stop conditions** — when to halt and report instead of improvising.

### Global rules (apply to every card)

1. **All commands run from the worktree root** `D:\xdev\DarkMatterK3@Home\DMK3-wt-rust-boinc`.
   Never use `cd` inside a command; set the working directory instead.
2. **Never modify any path in the do-not-touch list** (`STREAM_E_MASTER_PLAN.md` §7). The list
   includes `pipeline/**`, `pytest.ini`, `PREDICTION.md`, `K3_CRITERIA.md`,
   `checkers/certificates/**`, `logs/**`, and all `*sector_state.json`.
3. **All output goes to `artifacts/stream_e/`.** Never write to `logs/` — it is a dangling
   symlink to a Linux path on this machine.
4. **Never run `cargo build` with a working directory inside `core/`.** That tree contains a
   committed `target/debug` and is reached through a symlink.
5. **Exact arithmetic is compared exactly.** If you are about to write a floating-point
   tolerance for a C1/C3/C3b quantity, stop — you are doing the task wrong.
6. **One card, one commit.** Commit message prefix `stream-e(E<N>):`.
7. If a DoD item cannot be met, **do not weaken the DoD**. Halt and report under *Stop
   conditions*.
8. Do not add or remove comments in files you did not otherwise need to change.

---

## E0 — Unblock the Windows toolchain and output paths  `[BLOCKING]`

### Preconditions
None. This is the entry point.

### Directive
1. Configure a default Rust toolchain. `rustup` is installed on this machine but has **no
   default toolchain set**, so bare `cargo`/`rustc` currently fail with
   *"rustup could not choose a version of cargo to run"*.
2. Create `scripts/bootstrap_rust_toolchain.ps1`: idempotent, sets the stable toolchain if
   absent, then prints `cargo`/`rustc` versions and the detected host triple. It must succeed
   when run twice in a row.
3. Create the output directory `artifacts/stream_e/` with a `.gitkeep`.
4. Create `artifacts/stream_e/ENV_REPORT.md` recording, as measured (not assumed): `cargo`
   version, `rustc` version, host triple, `nvidia-smi` name/VRAM/driver, and the result of the
   dangling-symlink probe below.
5. Add a dangling-symlink probe to the bootstrap script. For each of
   `core`, `core_wasm`, `logs`, `archives`, `ui_loom`, `EuclidClusterViz`, `additional_storage`,
   report whether the path resolves to a real directory in *this* worktree. Expect several to be
   dangling — that is the known hazard from `STREAM_E_MASTER_PLAN.md` §3. **Record it; do not
   try to fix it by rewriting the symlinks or by committing junctions.**
6. Ensure `.gitignore` ignores `rust/**/target/` and `artifacts/stream_e/**` except `.gitkeep`
   and `*.md`/`*.json` results you intend to commit. Append only; do not reorder existing lines.

### Files
- create `scripts/bootstrap_rust_toolchain.ps1`
- create `artifacts/stream_e/.gitkeep`
- create `artifacts/stream_e/ENV_REPORT.md`
- modify `.gitignore` (append-only)

### Definition of Done
- [ ] `cargo --version` and `rustc --version` both exit `0` from the worktree root.
- [ ] `scripts/bootstrap_rust_toolchain.ps1` exits `0` on two consecutive runs.
- [ ] `artifacts/stream_e/ENV_REPORT.md` exists and contains a real `rustc` version string, the
      GPU name `NVIDIA GeForce RTX 2070`, and one line per probed symlink path.
- [ ] `git status --short` shows **no** modification to any do-not-touch path.

### Validate
```powershell
$wt = "D:\xdev\DarkMatterK3@Home\DMK3-wt-rust-boinc"
powershell -NoProfile -File "$wt\scripts\bootstrap_rust_toolchain.ps1"; if ($LASTEXITCODE) { throw "run 1 failed" }
powershell -NoProfile -File "$wt\scripts\bootstrap_rust_toolchain.ps1"; if ($LASTEXITCODE) { throw "not idempotent" }
cargo --version; rustc --version
Select-String -Path "$wt\artifacts\stream_e\ENV_REPORT.md" -Pattern "RTX 2070"
git -C $wt status --short
```

### Stop conditions
- `rustup` itself is missing → report; do not attempt a silent network install of a toolchain.
- Any do-not-touch path appears in `git status` → revert it immediately and report.

---

## E1 — Native Rust C1 kernel, ported literally  `[CORE]`

### Preconditions
E0 DoD fully met.

### Directive
Create the crate `rust/k3_kernel` and port `checkers/check_C1_mirror_integrality.py` to native
Rust. **Port it literally.** The goal of this card is bit-exact agreement, not elegance and not
speed.

1. `rust/k3_kernel/Cargo.toml`: a native `lib` plus a `bin` named `k3c1`. Dependencies:
   `num-rational`, `num-bigint`, `num-traits`, `serde`, `serde_json`, `sha2`, `rayon`, `clap`.
   **Do not** add `wasm-bindgen`. Do not add this crate to any existing workspace — give it its
   own `[workspace]` table so it does not get pulled into `core/`.
2. `src/series.rs` — port `_mul`, `_inv`, `_exp`, `_revert` from the Python, preserving structure
   one-to-one, including `_revert`'s `ztrial` / `comp` / `zp` construction and its use of `_mul`
   in the inner loop. Keep the same truncation length semantics (`N+1` coefficients, index =
   power).
3. `src/dual.rs` — port `_Dual` (fields `v`, `d`) with `add`, `sub`, `mul`, `div`, `neg`, `cube`,
   matching the Python operator definitions exactly, in particular
   `div = ((d*o.v - v*o.d) / (o.v * o.v))`.
4. `src/frobenius.rs` — port `_frobenius(a,b,c,d,N)`, returning `(y0, h)` with `h[0]` forced to
   zero, and `a_0(rho) = 1` exactly.
5. `src/c1_mirror.rs` — port `mirror_map_zq` and `verify_c1`. Emit a JSON object with the **same
   keys and same value formats** as the Python certificate, including `criterion`, `check`,
   `normalization`, `source`, `order3_abcd`, `holomorphic_first_terms`,
   `mirror_map_first_coeffs` (as strings), `N1`, `status`, `verdict`,
   `margin_max_denominator`, `first_non_integral_order`, `determinism_hash`, `assumptions`,
   `tier`. Add exactly two new keys: `computed_by` = `"rust/k3_kernel@<git-sha>"` and
   `wall_clock_seconds`.
6. `determinism_hash` must be `sha256` over `json.dumps({"order3": [...], "N1": N}, sort_keys=True)`.
   Reproduce Python's `json.dumps` output byte-for-byte — note Python's default separators emit
   `", "` and `": "`. Verify against the committed certificates rather than guessing.
7. `src/operators.rs` — mirror the `ORDER3_AZ_COOPER` table. Read the authoritative values from
   `checkers/check_C3_sym2.py`; do not invent them. Cover at least
   `gamma, alpha, delta, eta, s7, s10`.
8. `src/lib.rs` — re-export a public API: `verify_c1(order3: (i64,i64,i64,i64), n1: usize) -> C1Result`
   and `mirror_map_zq(...) -> Vec<BigRational>`.
9. `bin k3c1` CLI: `--order3 <name>` or `--abcd a,b,c,d`, `--N1 <usize>`, `--output <path>`,
   `--golden`. Mirror the Python CLI's exit codes: `0` on PASS, `1` on FAIL.
10. `tests/parity_certificates.rs` — for each of the 6 names, load
    `checkers/certificates/C1_mirror_<name>.json` and assert the Rust output matches on
    `status`, `verdict`, `margin_max_denominator`, `first_non_integral_order`,
    `mirror_map_first_coeffs`, and `determinism_hash`. Use the `N1` recorded inside each
    certificate, not a hardcoded one.
11. Golden-bad controls as Rust tests: `(10,4,63,0)` and `(17,5,2,0)` must yield `status == "FAIL"`
    with the same `first_non_integral_order` as Python reports.

### Files
- create `rust/k3_kernel/Cargo.toml`
- create `rust/k3_kernel/src/{lib,series,dual,frobenius,c1_mirror,operators}.rs`
- create `rust/k3_kernel/src/bin/k3c1.rs` (or `[[bin]]` path of your choice, declared in Cargo.toml)
- create `rust/k3_kernel/tests/parity_certificates.rs`
- **read-only**: `checkers/check_C1_mirror_integrality.py`, `checkers/check_C3_sym2.py`,
  `checkers/certificates/*.json`

### Definition of Done
- [ ] `cargo build --release` and `cargo test` both exit `0` in `rust/k3_kernel`.
- [ ] `cargo test` covers all 6 sporadic names **and** both golden-bad controls.
- [ ] For every name, Rust `determinism_hash` equals the value in the committed certificate.
- [ ] `mirror_map_first_coeffs` match the certificates as **strings**, elementwise.
- [ ] Running `k3c1 --golden` twice produces byte-identical output (determinism).
- [ ] No `unsafe` block anywhere in the crate.
- [ ] No floating-point type (`f32`/`f64`) appears in any C1 code path. `wall_clock_seconds` is
      the only permitted float, and it is metadata.
- [ ] `git status --short` shows no do-not-touch path.

### Validate
```powershell
$wt = "D:\xdev\DarkMatterK3@Home\DMK3-wt-rust-boinc"
$k  = "$wt\rust\k3_kernel"
cargo build --release --manifest-path "$k\Cargo.toml"; if ($LASTEXITCODE) { throw "build failed" }
cargo test --manifest-path "$k\Cargo.toml"; if ($LASTEXITCODE) { throw "tests failed" }

# determinism: two runs, byte-identical
& "$k\target\release\k3c1.exe" --golden | Out-File -Encoding utf8 "$wt\artifacts\stream_e\g1.txt"
& "$k\target\release\k3c1.exe" --golden | Out-File -Encoding utf8 "$wt\artifacts\stream_e\g2.txt"
if ((Get-FileHash "$wt\artifacts\stream_e\g1.txt").Hash -ne (Get-FileHash "$wt\artifacts\stream_e\g2.txt").Hash) { throw "non-deterministic" }

# forbidden constructs
if (Select-String -Path "$k\src\*.rs" -Pattern '\bunsafe\b' -Quiet) { throw "unsafe found" }
if (Select-String -Path "$k\src\series.rs","$k\src\dual.rs","$k\src\frobenius.rs" -Pattern '\bf64\b|\bf32\b' -Quiet) { throw "float in exact path" }
git -C $wt status --short
```

### Stop conditions
- A coefficient mismatches the certificate → **halt on the first mismatch**. Report the name,
  the `N1`, the coefficient index, and both numerator/denominator pairs. Do not "fix" it by
  changing the comparison, widening a type, or rounding.
- `determinism_hash` cannot be reproduced → report the exact Python `json.dumps` byte string you
  are trying to match and the one you produced. Do not drop the hash from the output.

---

## E2 — Bit-exact parity gate (Rust vs Python)

### Preconditions
E1 DoD fully met.

### Directive
1. Create `tools/rust_parity_check.py`. For every name in `{gamma, alpha, delta, eta, s7, s10}`
   and every `N1 ∈ {8, 16, 24, 32, 40, 50}`:
   - compute the Python result by importing
     `checkers.check_C1_mirror_integrality.verify_c1` and `mirror_map_zq` directly (do not
     shell out, do not re-derive);
   - compute the Rust result by invoking the `k3c1` binary with `--output`;
   - compare **exact rationals as `numerator/denominator` string pairs**, elementwise, plus
     `status`, `verdict`, `margin_max_denominator`, `first_non_integral_order`,
     `determinism_hash`.
2. Model the report on `tools/wasm_parity_check.py`'s structure and console style, but **replace
   its `1e-4` tolerance with exact equality**. There is no tolerance in this gate.
3. Write `artifacts/stream_e/parity_c1.json` containing per-cell `PASS`/`FAIL`, the first
   mismatching index when failing, and the Python/Rust wall-clock for each cell.
4. Exit `0` only if all 36 cells pass. Exit `1` otherwise. Print a one-line summary
   `PARITY: 36/36 cells exact` on success.
5. Add the golden-bad controls as two extra cells that must both be `FAIL`-in-both.

### Files
- create `tools/rust_parity_check.py`
- create (output) `artifacts/stream_e/parity_c1.json`
- **read-only**: `checkers/**`, `tools/wasm_parity_check.py`

### Definition of Done
- [ ] `python tools/rust_parity_check.py` exits `0` and prints `PARITY: 36/36 cells exact`.
- [ ] `artifacts/stream_e/parity_c1.json` has 36 candidate cells + 2 control cells, all passing.
- [ ] The string `1e-4` does not appear in `tools/rust_parity_check.py`.
- [ ] The script exits `1` when fed a deliberately perturbed operator (prove it once by hand
      with `--selftest`, mirroring the golden-bad pattern used across `checkers/`).

### Validate
```powershell
$wt = "D:\xdev\DarkMatterK3@Home\DMK3-wt-rust-boinc"
python "$wt\tools\rust_parity_check.py" --selftest; if ($LASTEXITCODE) { throw "selftest failed" }
python "$wt\tools\rust_parity_check.py"; if ($LASTEXITCODE) { throw "parity failed" }
Select-String -Path "$wt\tools\rust_parity_check.py" -Pattern "1e-4"   # must return nothing
Get-Content "$wt\artifacts\stream_e\parity_c1.json" | Select-Object -First 20
```

### Stop conditions
- Any cell fails → halt. This is the gate for the whole stream; **E3 onward must not start.**
  Report the failing `(name, N1, index)` triple.

---

## E3 — Measured scaling ladder (no pre-committed numbers)

### Preconditions
E2 green (36/36).

### Directive
1. Add `rust/k3_kernel/benches/c1_scaling.rs` (or a `--bench` mode on `k3c1`; either is fine,
   but it must be scriptable and must not require `cargo bench` nightly features).
2. Run the ladder `N1 ∈ {50, 100, 200, 300, 500}` for all 6 names, in Rust. Parallelise
   **across candidates** with `rayon`; keep each candidate single-threaded, since the series
   recurrences are sequential in `n`.
3. Run the same ladder in Python for `N1 ∈ {50, 100, 200}` only — going further in Python is
   expected to be impractical and is not required. If a Python cell exceeds **30 minutes**,
   abort that cell, record `"timeout_s": 1800`, and move on.
4. Record per cell: `n1`, `name`, `impl`, `wall_clock_seconds`, `peak_rss_bytes`,
   `max_denominator_bitlength`. Write `artifacts/stream_e/bench_c1_scaling.json`.
5. Write `artifacts/stream_e/SCALING_REPORT.md` with a table and the **measured** speedup per
   `N1`. State the machine (RTX 2070 host, Windows), the toolchain version, and that these are
   single-machine measurements.
6. **Do not write any speedup figure that you did not measure.** The master plan deliberately
   contains no predicted speedup; do not import one from anywhere.

### Files
- create `rust/k3_kernel/benches/c1_scaling.rs`
- create `artifacts/stream_e/bench_c1_scaling.json`
- create `artifacts/stream_e/SCALING_REPORT.md`

### Definition of Done
- [ ] `bench_c1_scaling.json` contains Rust cells for all 6 names at `N1 ≥ 200`, and at least
      `s7` and `s10` at `N1 = 500`.
- [ ] Every reported speedup in `SCALING_REPORT.md` is traceable to two cells in the JSON.
- [ ] `max_denominator_bitlength` is recorded and increases with `N1` (sanity: rational growth
      is the expected cost driver).
- [ ] No claim of asymptotic complexity is made without showing the fitted exponent and the
      points it was fitted on.

### Validate
```powershell
$wt = "D:\xdev\DarkMatterK3@Home\DMK3-wt-rust-boinc"
$j = Get-Content "$wt\artifacts\stream_e\bench_c1_scaling.json" -Raw | ConvertFrom-Json
$rust200 = $j.cells | Where-Object { $_.impl -eq 'rust' -and $_.n1 -ge 200 }
if (($rust200 | Select-Object -ExpandProperty name -Unique).Count -lt 6) { throw "missing rust N1>=200 coverage" }
if (-not ($j.cells | Where-Object { $_.impl -eq 'rust' -and $_.n1 -eq 500 -and $_.name -in @('s7','s10') })) { throw "missing N1=500" }
"OK"
```

### Stop conditions
- Rust cannot reach `N1 = 200` within 30 min for some candidate → record it, do not silently
  drop the candidate, and report which one.

---

## E4 — BOEINC work-unit schema for `candidate × N1` fan-out

### Preconditions
E2 green. E3 complete (you need real timings to size a work unit).

### Directive
1. Read `core_boinc/boinc_work_generator.py`, `core_boinc/process_all_shards.py`,
   `core_boinc/project_xml/workunit_template.xml`, `core_boinc/project_xml/result_template.xml`,
   and `core_boinc/test_boinc_suite.py` first. **Extend** the existing generator; do not write a
   parallel one.
2. Define a work unit as exactly one `(operator_name_or_abcd, N1)` cell. Justify the chosen
   `N1` granularity from the E3 timings so a unit lands in roughly the 5–30 min range on a
   typical volunteer CPU.
3. Because C1 is deterministic exact arithmetic, the validator is **exact equality of the
   result JSON** (excluding the `wall_clock_seconds` and `computed_by` metadata keys). A quorum
   of 2 bit-identical results is sufficient. Implement that, not a numeric-tolerance validator.
4. Add `core_boinc/tests/test_stream_e_workunits.py` in the style of the existing
   `test_boinc_suite.py`: schema round-trip, validator accepts two identical results, validator
   rejects a single-bit-flipped result, validator ignores metadata-only differences.
5. Document the schema in `docs/STREAM_E_WORKUNIT_SCHEMA.md` with one worked example work unit
   and one worked example result.
6. Do **not** deploy a server. Deployment options already exist in `boeinc_deployment_plan.md`;
   reference it rather than duplicating it.

### Files
- modify `core_boinc/boinc_work_generator.py` (extend)
- create `core_boinc/tests/test_stream_e_workunits.py`
- create `docs/STREAM_E_WORKUNIT_SCHEMA.md`
- **read-only**: `core_boinc/project_xml/**`, `api/api_dispatcher.py`, `boeinc_deployment_plan.md`

### Definition of Done
- [ ] `python -m pytest core_boinc/tests/test_stream_e_workunits.py -v` exits `0`.
- [ ] The existing BOEINC tests still pass: `python -m pytest core_boinc/test_boinc_suite.py -v`
      exits `0` (note: `pytest.ini` excludes `core_boinc` from the default run, so invoke it
      explicitly — **do not edit `pytest.ini`**).
- [ ] Validator rejects a single-character mutation of a result payload.
- [ ] Validator treats `wall_clock_seconds` / `computed_by` differences as equal.
- [ ] Work-unit sizing in the schema doc cites specific E3 timing cells.

### Validate
```powershell
$wt = "D:\xdev\DarkMatterK3@Home\DMK3-wt-rust-boinc"
python -m pytest "$wt\core_boinc\tests\test_stream_e_workunits.py" -v; if ($LASTEXITCODE) { throw "new wu tests failed" }
python -m pytest "$wt\core_boinc\test_boinc_suite.py" -v;             if ($LASTEXITCODE) { throw "regressed existing boinc tests" }
git -C $wt diff --name-only -- pytest.ini    # must return nothing
```

### Stop conditions
- Existing BOEINC tests were already failing before your change → record the pre-existing
  failure, do not fix it on this branch, and report.

---

## E5 — Full large run on the local RTX 2070  `[CAPACITY TEST]`

### Preconditions
E2 green, E3 complete. **Check GPU occupancy first** — the Stream 3 D3 rerun may be using the
card.

### Directive
1. Create `scripts/run_stream_e_gpu_large_run.ps1` with parameters
   `-GridSize` (default `384`), `-MaxVramFraction` (default `0.5`), `-Resume`, `-DryRun`.
2. **Pre-flight gate, mandatory.** Query `nvidia-smi --query-compute-apps=pid,used_memory`.
   If any process holds more than **1024 MiB**, refuse to start, print the offending PIDs and
   their usage, and exit non-zero with a clear message naming the Stream 3 rerun as the likely
   owner. Provide `-Force` to override, but default to refusing.
3. VRAM budget is fixed by `STREAM_E_MASTER_PLAN.md` §6.1 and derived from `complex64` at
   8 bytes/cell with ~5 live grids:
   - `384³` → ~2.1 GiB peak — **default**
   - `512³` → ~5.0 GiB peak — allowed only with in-place fusion of `S12_field - S21_field`
   - `768³` → ~16.9 GiB — **reject with an explicit error**; it does not fit an 8 GiB card
   The script must refuse `-GridSize 768` rather than OOM.
4. Set `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` for the run.
5. Reuse the existing resilience machinery — `checkpoint_manager.py` and the patterns in
   `execute_phase4_multiday.ps1` / `PHASE4_MULTIDAY_GUIDE.md`. **Do not invent a second
   checkpoint format.** Checkpoint after each shard.
6. Run the CPU half concurrently: the full Rust `N1` ladder from E3. It never touches the GPU,
   so it is safe alongside the D3 rerun.
7. Prove resilience with a **kill test**: start the run, let at least two shards complete, kill
   the process, restart with `-Resume`, and confirm it continues from the last checkpoint rather
   than restarting. Record the evidence.
8. Emit `artifacts/stream_e/LARGE_RUN_REPORT.md`: grid size, shard count, wall-clock, peak VRAM
   sampled from `nvidia-smi`, peak RSS, checkpoint/resume evidence, and the pre-flight decision.

### Files
- create `scripts/run_stream_e_gpu_large_run.ps1`
- create `artifacts/stream_e/LARGE_RUN_REPORT.md`
- create `artifacts/stream_e/checkpoints/` (runtime, git-ignored)
- **read-only**: `checkpoint_manager.py`, `execute_phase4_multiday.ps1`, `core_wasm/**`

### Definition of Done
- [ ] `-DryRun` prints the full plan and the VRAM budget without allocating GPU memory.
- [ ] `-GridSize 768` is rejected with a message citing the 8 GiB ceiling.
- [ ] Pre-flight refuses to start when >1024 MiB of VRAM is already in use, and says so clearly.
- [ ] A full `384³` run completes and peak sampled VRAM is below `MaxVramFraction × 8192 MiB`.
- [ ] Kill-and-`-Resume` demonstrably continues from the last checkpoint; the report shows the
      shard index before and after.
- [ ] The Rust CPU ladder completed in the same window.
- [ ] No file in the do-not-touch list changed. In particular `checkpoint_run.pt` and
      `sector_state.json` are **untouched** — Stream E checkpoints live under
      `artifacts/stream_e/checkpoints/`.

### Validate
```powershell
$wt = "D:\xdev\DarkMatterK3@Home\DMK3-wt-rust-boinc"
# 1. GPU occupancy, recorded before anything starts
nvidia-smi --query-compute-apps=pid,used_memory --format=csv

# 2. dry run allocates nothing
powershell -NoProfile -File "$wt\scripts\run_stream_e_gpu_large_run.ps1" -DryRun; if ($LASTEXITCODE) { throw "dry run failed" }

# 3. oversized grid must be refused
powershell -NoProfile -File "$wt\scripts\run_stream_e_gpu_large_run.ps1" -GridSize 768 -DryRun
if ($LASTEXITCODE -eq 0) { throw "768 grid was not rejected" }

# 4. Stream 3 state untouched
git -C $wt status --short -- checkpoint_run.pt sector_state.json pipeline_runs.json pipeline/
```

### Stop conditions
- The D3 rerun is occupying the GPU → **do not use `-Force`.** Run the CPU half only, record
  that the GPU half is deferred, and report. Stream 3 has priority on the card.
- An OOM occurs at `384³` → stop, record the actual peak, and report. Do not escalate to
  `512³`; investigate the live-grid count instead.

---

## E6 — Stream 2 support handoff

### Preconditions
E2 green (Stream 2 gets no benefit from an unverified kernel).

### Directive
Execute the deliverables in `docs/STREAM_E_STREAM2_SUPPORT.md`. Summary: expose the fast exact
checker as a batch oracle Stream 2 can call over a list of candidate operators, reusing the
existing golden-fixture loader at `scripts/s2_01b_golden_data/loader.py`, and emit certificates
into `artifacts/stream_e/certificates/` (**not** `checkers/certificates/`).

### Definition of Done
- [ ] A batch mode exists: given a JSON list of `abcd` tuples and an `N1`, it emits one
      certificate per operator plus a summary index.
- [ ] The summary index reports `PASS(N1)` / `FAIL(first non-integral order)` per operator.
- [ ] All emitted certificates land under `artifacts/stream_e/certificates/`.
- [ ] `checkers/certificates/` is unmodified (`git status` clean for that path).
- [ ] The batch path is covered by at least one test using the existing golden fixtures.

### Validate
```powershell
$wt = "D:\xdev\DarkMatterK3@Home\DMK3-wt-rust-boinc"
git -C $wt status --short -- checkers/certificates/   # must return nothing
Get-ChildItem "$wt\artifacts\stream_e\certificates\" | Select-Object -First 10
```

### Stop conditions
- A batch result disagrees with an existing committed certificate → that is an E2 parity
  regression. Halt and reopen E2.

---

## Final PR checklist (run before requesting review)

```powershell
$wt = "D:\xdev\DarkMatterK3@Home\DMK3-wt-rust-boinc"

# CI gates, exactly as GitHub runs them
python "$wt\scripts\check_tuning_log.py" --selftest;   if ($LASTEXITCODE) { throw }
python "$wt\scripts\check_tuning_log.py";              if ($LASTEXITCODE) { throw }
python "$wt\scripts\check_tier_language.py" --selftest; if ($LASTEXITCODE) { throw }
python "$wt\scripts\check_tier_language.py";            if ($LASTEXITCODE) { throw }
python -m pytest "$wt\pipeline\tests\" -v;              if ($LASTEXITCODE) { throw }

# Stream E's own gates
python "$wt\tools\rust_parity_check.py";                if ($LASTEXITCODE) { throw }
cargo test --manifest-path "$wt\rust\k3_kernel\Cargo.toml"; if ($LASTEXITCODE) { throw }

# isolation contract: this must print NOTHING
git -C $wt diff --name-only origin/main -- pipeline/ pytest.ini PREDICTION.md TUNING_LOG.md K3_CRITERIA.md checkers/certificates/ sector_state.json checkpoint_run.pt pipeline_runs.json
```

`pipeline/tests/` is Stream 3's merge-blocking suite. It must stay green, and Stream E must
produce **zero** diff against it.
