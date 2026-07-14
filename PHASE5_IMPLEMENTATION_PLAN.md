# Phase 5 Implementation Plan: Pivot to DarkMatter@Home (WebAssembly/WebGPU)

**Date**: 2026-07-14
**Status**: PLANNING ONLY — Not yet implemented
**Precondition**: V4 mock calibration (35/35 sectors) complete; local GPU data collection considered finished
**Objective**: Pivot engineering effort from the local RTX 2070 pipeline to the **Crowdsourced Browser Supercomputer** described in `TODO.md` — turn every visitor's browser tab into a K3/T2 anomaly-hunting compute node.

---

## 0. Guiding Principle

> "Local GPU data collection is a *proof of concept*. Planet-scale discovery requires planet-scale compute." — pivot from 1 GPU to N browsers.

This plan does **not** modify any code. It defines the exact sequence of engineering steps, file targets, APIs, and acceptance criteria for the next implementation session(s).

---

## 1. Current State Inventory (What Already Exists)

| Component | Path | Status |
|---|---|---|
| Rust WASM crate (skeleton) | `core_wasm/Cargo.toml`, `core_wasm/src/lib.rs` | Bootstrapped: `compute_comoving_distance()`, `solve_asymmetric_3_2_check()` implemented, but **no FFT, no 3D density-field, no K3 Δ metric matching the V3/V4 Python pipeline** |
| FastAPI dispatcher | `api/api_dispatcher.py` | Has `/users/register`, `/jobs/request`, `/jobs/submit`, `/leaderboard`, `/badges/{user_id}` — job/points system already scaffolded, **not yet wired to WASM sector chunks** |
| Frontend shell | `ui_loom/app.js`, `ui_loom/index.html` | Cyberpunk UI shell exists; **no WebAssembly worker integration yet** |
| Reference Python implementation | `topology.py`, `mock_catalog.py`, `real_euclid_worker_v3.py` | Authoritative Δ / s12 / T2_proxy computation — the "ground truth" WASM must match |
| Data slicing | `tools/dataset_slicer/` (per ROADMAP.md) | Referenced but needs verification of current implementation state |

**Gap**: The WASM module computes a *toy* 3:2 variance-ratio check, not the actual K3 asymmetry (`s12`, `delta`, topology Betti numbers) used by the V3/V4 real pipeline. This must be ported faithfully before any browser result can be scientifically trusted.

---

## 2. Phase 5 Scope (Four Sequential Sub-Phases)

### 5A — WASM Core Compute Parity (CPU, `core_wasm/`)
### 5B — FastAPI Chunk/Result Contract (Backend)
### 5C — Browser Worker Integration & Single-Tab Proof (Frontend)
### 5D — Gamification & Viral Discovery Loop (Frontend + Backend)

Each sub-phase has a hard **exit criterion** before starting the next.

---

## 3. Phase 5A — WASM Core Compute Parity

**Goal**: A single browser tab can take a 10,000-galaxy JSON chunk and compute the *same* `Δ` (delta), `s12`, and asymmetry classification as the Python V3 pipeline — verified bit-for-bit (within float tolerance) against `real_euclid_worker_v3.py` output.

### 3.1 Files to Create/Modify (planning only, no edits yet)

| File | Change |
|---|---|
| `core_wasm/src/lib.rs` | Add `pub fn compute_density_field_asymmetry(coords_json: &str) -> String` — port of the 3D FFT / density-field anisotropy logic from `real_euclid_worker_v3.py` |
| `core_wasm/src/fft.rs` (new) | Minimal 3D FFT (or reuse `rustfft` crate) sized for chunks up to ~10k points, gridded density estimate |
| `core_wasm/src/topology.rs` (new) | Port simplified Betti-number / persistence proxy from `topology.py` (genus, betti_0, betti_1, T2_proxy) — CPU WASM budget permitting; may be deferred to WebGPU (Phase 5C+) if too slow |
| `core_wasm/Cargo.toml` | Add `rustfft`, keep `wasm-bindgen`, `serde`, `serde_json` |
| `tools/wasm_parity_check.py` (new) | Python script: runs N random sectors through both `real_euclid_worker_v3.py` logic and a `wasm-pack test` / node harness, diffs `s12`/`delta`/`T2_proxy` within tolerance (e.g. 1e-4) |

### 3.2 Algorithm Porting Checklist

- [ ] Port comoving distance conversion (already done — verify constants match `config.py` cosmological parameters exactly)
- [ ] Port 3D density-field gridding (bin galaxies into voxel grid, same bin count/extent as Python)
- [ ] Port FFT-based anisotropy ratio (`s12`, `s21`) computation
- [ ] Port `delta` calculation formula exactly as used in `discoveries.json` schema
- [ ] Port (or stub with documented approximation) topology proxy (`T2_proxy`, `betti_0`, `betti_1`, `euler_characteristic`)
- [ ] Add unit tests inside `core_wasm` using `wasm-bindgen-test`

### 3.3 Performance Budget

- Target: process 10,000-galaxy chunk in **<2 seconds** on mid-range mobile CPU (single WASM thread, no SIMD requirement for v1)
- Memory ceiling: **<64MB** per worker (per `TODO.md` constraint)
- Fallback: if FFT/topology proves too slow in pure WASM, defer topology proxy to server-side confirmation and have WASM emit only `s12`/`delta` for v1 (topology added in 5A.2 iteration)

### 3.4 Exit Criterion for 5A

✅ `wasm-pack build core_wasm --target web` compiles cleanly
✅ `tools/wasm_parity_check.py` shows <0.01% relative error between WASM and Python `s12`/`delta` on 10 held-out real sectors
✅ Single Node.js harness call processes a 10k-galaxy chunk in <2s

---

## 4. Phase 5B — FastAPI Chunk/Result Contract

**Goal**: Define and implement the API contract so a browser can request a sector chunk and submit back a verified result, reusing the existing `/jobs/request` and `/jobs/submit` scaffolding in `api/api_dispatcher.py`.

### 4.1 Files to Modify

| File | Change |
|---|---|
| `api/api_dispatcher.py` | Extend `JobRequest`/`JobResult` Pydantic models with `sector_id`, `chunk_url` (signed GCS URL or local path), `delta`, `s12`, `wasm_version_hash` |
| `tools/dataset_slicer/` | Verify/implement slicer that pre-chops the 35 (then 1,620) sectors into ≤500KB JSON chunks of ~10,000 galaxies matching WASM input schema |
| `discoveries.json` schema | No change to schema; browser-submitted discoveries append via same fields as GPU-pipeline discoveries, tagged `"source": "browser_wasm"` |

### 4.2 New/Updated Endpoints (design only)

```
GET  /jobs/request          → existing; extend response with chunk_url + expected schema version
POST /jobs/submit           → existing; extend to validate delta/s12 against server-side spot-check
POST /api/v1/discoveries/browser   → NEW: records a browser-sourced high-Δ discovery separately for audit
GET  /api/v1/wasm/manifest         → NEW: returns current WASM build hash + cosmological params for cache-busting/parity
```

### 4.3 Quorum / Anti-Cheat Design Notes

- Reuse existing quorum consensus logic (`submit_result` already mentions "waiting for quorum consensus")
- Each chunk dispatched to ≥2 independent browser sessions; results must agree within tolerance before being marked "confirmed"
- Server retains authority to re-verify any Δ > discovery threshold using the Python pipeline before public "Discovery #N" announcement (prevents WASM float-precision false positives from becoming public claims)

### 4.4 Exit Criterion for 5B

✅ API contract documented in `DISCOVERY_NED_CROSSMATCH.md`-style spec doc (new `WASM_JOB_CONTRACT.md`)
✅ `/jobs/request` returns a real signed chunk URL from GCS (or local dev equivalent)
✅ `/jobs/submit` persists browser results into `pipeline_runs.json`/`discoveries.json` with `source: browser_wasm` tag

---

## 5. Phase 5C — Browser Worker Integration & Single-Tab Proof

**Goal**: Prove end-to-end: browser tab → download chunk → WASM compute → POST result → backend accepts it.

### 5.1 Files to Create/Modify

| File | Change |
|---|---|
| `ui_loom/src/workers/wasmWorker.js` (new) | Web Worker wrapping compiled `core_wasm` module; receives chunk, returns `{delta, s12, sector_id}` |
| `ui_loom/app.js` | Wire "Start Compute" button → fetch chunk from `/jobs/request` → dispatch to Web Worker → POST to `/jobs/submit` |
| `ui_loom/index.html` | Add minimal compute status UI (progress bar, current sector, last Δ found) |
| `public/wasm/` (new, build output) | Compiled `.wasm` + `.js` glue from `wasm-pack build --target web` |

### 5.2 Single-Tab Proof-of-Concept Script

1. Load `core_wasm` in a Web Worker (keeps main thread responsive)
2. Fetch one real 10,000-galaxy chunk via `/jobs/request`
3. Run `compute_density_field_asymmetry()` in worker
4. Display computed Δ in UI within 2 seconds
5. POST result to `/jobs/submit`, confirm 200 response and points awarded

### 5.3 Exit Criterion for 5C

✅ Manual browser test (Chrome + Firefox) processes 1 real sector end-to-end without page reload
✅ Network tab shows correct request/response cycle (chunk fetch, worker compute, result submit)
✅ Backend log confirms received result matches WASM parity test tolerance

---

## 6. Phase 5D — Gamification & Viral Discovery Loop

**Goal**: When a browser finds a high-Δ anomaly, create a moment worth screenshotting and sharing — this is the viral growth mechanism.

### 6.1 Discovery Threshold & Flow

- Reuse existing `significance_score` / `significance` classification (`INTERESTING`, etc. — see `discoveries.json` schema) to decide when to trigger the "discovery" UI moment
- Threshold candidates (to be tuned against V4 mock-calibrated `2σ`/`3σ` values once available): Δ above calibrated sector threshold → trigger; otherwise silent "sector cleared, no anomaly" state

### 6.2 Files to Create/Modify

| File | Change |
|---|---|
| `ui_loom/app.js` | Add `triggerDiscoveryFlash(anomalyId, delta)` — full-screen flash animation + sound cue |
| `ui_loom/style.css` | Add `.discovery-flash` gold/cyan flash keyframe animation (reuses existing cyberpunk visual language per `TODO.md` §3) |
| `ui_loom/index.html` | Add discovery toast/banner: *"You discovered K3 Anomaly #{id}! Δ = {value}"* |
| `api/api_dispatcher.py` | `/jobs/submit` response includes `discovery_id` + shareable permalink when threshold exceeded |
| `public/` | Add Open Graph / social share meta template for discovery permalinks (e.g. `discovery.html?id=402`) for viral link previews |

### 6.3 Gamification Mechanics (design, ties into existing leaderboard/badges endpoints)

- **Instant feedback**: screen flash + audio + toast within <500ms of server confirmation
- **Named discovery**: `"K3 Anomaly #{sequential_id}"` — sequential ID drawn from a server-side counter, not client-generated (prevents spoofing)
- **Points**: reuse existing points system in `request_job`/`submit_result`; award bonus points for first-to-find vs. quorum-confirming
- **Leaderboard**: existing `/leaderboard` endpoint surfaces top discoverers
- **Badges**: existing `/badges/{user_id}` endpoint — add new badge tiers (`First Discovery`, `10 Sectors Cleared`, `Anomaly Hunter`)
- **Shareability**: each discovery gets a permalink + auto-generated social card (image with Δ value, sector coordinates, cyberpunk styling) to drive organic sharing → viral loop

### 6.4 Exit Criterion for 5D

✅ Full-screen flash + toast fires correctly on a real (or forced test) high-Δ result
✅ Discovery permalink page renders with correct anomaly data and social preview card
✅ Leaderboard/badge endpoints reflect new browser-sourced discoveries

---

## 7. Cross-Cutting Concerns (Apply to All Sub-Phases)

| Concern | Plan |
|---|---|
| **Scientific integrity** | All browser-sourced discoveries flagged `source: browser_wasm` and pending server-side Python re-verification before being counted toward any public K3/T2 claim (per existing `SCIENTIFIC_AUDIT_REPORT.md` caution) |
| **WASM/Python parity drift** | `tools/wasm_parity_check.py` becomes a CI gate — re-run on every `core_wasm` change |
| **Mobile constraints** | <64MB memory, <2s compute time per chunk enforced from 5A onward |
| **WebGPU upgrade path** | 5A/5C ship CPU-WASM first (per user's explicit instruction: "Focus on... CPU WebAssembly... first"); WebGPU Netrunner engine (`TODO.md` §2) is a *future* sub-phase (5E, not in this plan) once CPU path is proven and viral loop validated |
| **Backward compatibility** | Existing local V3/V4 GPU pipeline keeps running independently; browser compute is additive, not a replacement, until scale is proven |

---

## 8. Sequencing & Estimated Effort (Planning Estimate Only)

| Sub-Phase | Description | Rough Effort |
|---|---|---|
| 5A | WASM compute parity | 1–2 weeks (FFT + parity testing is the hard part) |
| 5B | FastAPI contract | 3–5 days |
| 5C | Browser integration + single-tab proof | 3–5 days |
| 5D | Gamification loop | 1 week |
| **Total** | | **~3–4 weeks** to viral-ready single-tab proof |

---

## 9. Immediate Next Actions (When Implementation Begins)

1. Confirm V4 mock calibration is 35/35 complete (gate condition from user's Action 4 preamble)
2. Start with **5A.1**: add `rustfft` dependency and port density-field gridding into `core_wasm/src/lib.rs` (or new `fft.rs`)
3. Build `tools/wasm_parity_check.py` early — this is the safety net that prevents shipping a scientifically-wrong browser pipeline
4. Do not touch `ui_loom/` (5C/5D) until 5A parity check passes

---

## 10. Explicit Non-Goals for Phase 5 (v1)

- ❌ WebGPU/Netrunner compute engine (deferred to Phase 5E)
- ❌ BOINC native client changes (`core_boinc/` — separate track, unaffected)
- ❌ Full 1,620-sector footprint dispatch (start with the same 35 sectors already validated in V3/V4)
- ❌ Public "discovery" claims from browser data alone (always require server-side Python re-verification)

---

## Summary

This plan sequences the pivot from local single-GPU data collection to a browser-based crowdsourced compute network in four gated sub-phases (5A–5D), each with explicit files, exit criteria, and scientific-integrity guardrails. **No code has been changed as part of this planning document** — implementation begins only after V4 mock calibration completes and this plan is approved.
