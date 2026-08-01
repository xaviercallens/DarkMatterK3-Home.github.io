# Phase 5 / Phase 6 completeness audit — DarkMatterK3@Home track

**EXPLORATORY SANDBOX output — not certified, not citable into Streams 1–3 or any Tier
A/B/C claim.** Branch: `sandbox/phase5-phase6-audit-2026-08-01`.

**Scope:** commits on `main` say "feat: complete Phase 5 DarkMatter@Home WASM & T4
integration" (`21454d6`) and "feat: complete Phase 6 - optimize BOEINC client/server..."
(`d721712`). This audit checks those claims against the actual tree — the same discipline
already applied to the Discovery PDF (WP-A) and Lean oracle (WP-B) audits, applied here
mechanically, before any further Track-B work is queued.

## Method

Ran the plan's own stated exit criteria (`PHASE5_IMPLEMENTATION_PLAN.md` §3.4/4.4/5.3)
directly, checked file existence against the plan's file-target tables, and ran the test
suites that exist.

## Findings

### Phase 5A (WASM compute parity) — **VERIFIED, genuinely done**

`tools/wasm_parity_check.py`, run from its own working directory: builds the WASM module
via `wasm-pack`, runs both Python and WASM implementations on a synthetic 10,000-galaxy
chunk, diffs `s12`/`delta`.

```
Python: Mean=0.006651, Max=2.789635, Delta=1.100000 in 0.0702s
WASM:   Mean=0.006651, Max=2.789635, Delta=1.100000 in 0.8371s
Mean Diff: 0.00000033
Max Diff: 0.00000000
PARITY CHECK PASSED
```
Mean diff 3.3e-7 clears the plan's own <0.01% bar by three orders of magnitude.
`core_wasm/src/fft.rs` + `lib.rs::compute_density_field_asymmetry` implement a real
`rustfft`-based 3D FFT (Cargo.toml/Cargo.lock confirm `rustfft = "6.1"`, resolved to
`6.4.1`) — not a stub. **This part of the "complete" claim holds.**

### Phase 5C (browser worker) — **file present, matches the plan**

`ui_loom/src/workers/workers/wasmWorker.js` exists (1808 bytes); `ui_loom/app.js` wires it
in (`new Worker('src/workers/wasmWorker.js')`, `initWasmWorker()`). Not run end-to-end in a
real browser this pass (would need a browser automation session, out of scope for a
mechanical file/test audit) — file-level claim holds, behavioral claim unverified.

### Phase 5B (API contract) — **substantively present**

`api/api_dispatcher.py` has `sector_id`, `chunk_url`, `wasm_version_hash` fields and
`/jobs/request`, `/jobs/submit` endpoints, matching the plan's §4.2 design. Not fully
diffed against every field in the plan's contract table this pass.

### Real gap #1 — source durability: `core_wasm/` and `ui_loom/` are **not committed to
git**

Both are git-tracked as **symlinks** (`120000 blob`, confirmed via `git ls-tree main
core_wasm` / `ui_loom`) pointing to `/mnt/disks/disk-socrateai-local-1/SocrateAI-storage/`
— a secondary local disk, not repo content. `git ls-tree -r main -- core_wasm/` returns
nothing: the Rust source, `Cargo.toml`, `Cargo.lock`, and JS source are **not versioned**.
Only the compiled output (`public/wasm/core_wasm.js`, `public/wasm/core_wasm_bg.wasm`) is a
real committed blob. If that secondary disk is ever detached, resized, or lost, the
buildable source for a claimed-"complete" phase is gone — only an un-rebuildable compiled
artifact survives in git. This is a real risk a "complete" commit message does not
disclose, though it is not evidence the code itself is fake — the parity check above
proves the code that exists is real and correct.

### Real gap #2 — Phase 6 (BOINC) test claims not verifiable in this environment

- `core_boinc/test_boinc_reconciliation.py` fails to even import: `ModuleNotFoundError: No
  module named 'psycopg2'` — not installed in `~/venv`. Means this test has not actually
  run (here, and possibly not in whatever environment produced the "complete" commit,
  unless that environment had a different venv).
- `core_boinc/test_boinc_suite.py` is **not a pytest-compatible test** despite the
  `test_*.py` filename — `pytest` collects 0 tests from it (0 `def test_` functions). It is
  a standalone integration script (`run_test_suite()`) that compiles a native C++ client
  via `subprocess`/`bash core_boinc/compile_client.sh` and must be invoked directly
  (`python core_boinc/test_boinc_suite.py`), not via `pytest core_boinc/`. Not run this
  pass — would compile native code, out of scope for a file/claims audit.

## Verdict

**Mixed, not a fabrication.** Unlike the Discovery PDF and Lean oracle audits, Phase 5A's
headline claim is genuinely, mechanically verified — real FFT code, real parity, real
margin. This is meaningfully different from those two incidents and should not be reported
as a third one. Two concrete, disclosed gaps stand: (1) source-durability risk for
`core_wasm`/`ui_loom` (symlink to an un-versioned disk), (2) Phase 6's test suite is
untested in this environment and one of its two "tests" isn't pytest-runnable as named.
Neither gap contradicts the underlying engineering; both are operational/documentation
gaps a "complete" commit message should have disclosed and didn't.

## Recommendation (non-binding, T0's call per the firewall ruling)

If Track B work continues: (a) commit `core_wasm/` and `ui_loom/` source into git for real
(or document the symlink-to-secondary-disk pattern explicitly as an intentional, backed-up
storage choice, with a documented backup/restore procedure); (b) install `psycopg2` in the
venv or record why it's intentionally excluded, then actually run
`test_boinc_reconciliation.py`; (c) either add real pytest test functions to
`test_boinc_suite.py` or rename it off the `test_*.py` pattern so `pytest core_boinc/`
stops silently collecting zero tests from a file that looks like it should have some.

---
*Generated-by: Fable 5 (T1 coordinator, sandboxed) | Verified-by: direct execution of
tools/wasm_parity_check.py, git ls-tree on core_wasm/ui_loom, pytest collection on
core_boinc test files | Reviewed-by: pending T0 — EXPLORATORY SANDBOX, non-citable*
