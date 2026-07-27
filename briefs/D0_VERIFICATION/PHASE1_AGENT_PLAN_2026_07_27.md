# Phase 1 — Emulator Integration, Sweep Scaffolding, Synthetic Pre-Flight Infra

**Date:** 2026-07-27
**Gate:** D0 CLOSED (see `D0_AGENT_PLAN_2026_07_27.md`). Q1 emulator resolved: EMULATOR_AVAILABLE
(`github.com/jianxiangl-astro/lya-mfdm`, arXiv:2606.06969). Packages installed
(`h5py getdist iminuit cobaya scikit-learn celerite`).

**Scope of this file:** implements Directives 1–4 of the WP-E6 Acceleration Manifesto, corrected
per D0 findings. Directive 5 (SBP/ShapeFit) stays deferred — it compresses around a P1D model
that doesn't exist as a working integration until Agent 1 below finishes.

**What this phase explicitly does NOT do:** run the real (m,f) sweep against DESI data, touch
`PREDICTION.md` or `data/raw/` (both hook-protected now — see D0 close-out), commit, or push.
Every agent below writes to its own output file only.

---

## Tiering rationale

- **Agent 1 (emulator integration + adequacy check):** Sonnet. This is the highest-stakes item —
  it decides whether Directive 4's "major unblock" survives contact with actual code, and requires
  judging domain overlap (trained z=5.0/4.6/4.2 vs DESI's z≈2.2–4.4), not just running a script.
- **Agent 2 (grid sweep scaffolding):** Haiku. Mechanical: clone a confirmed-real repo, follow its
  documented JSON-config pattern, wire in a PLACEHOLDER (m,f) grid for pipeline-validation only -- NOT sourced from K3_CRITERIA.md, see correction note. No physics judgment.
- **Agent 3 (synthetic pre-flight infra):** Sonnet. Mechanical repo use, but "keep the pre-flight
  pessimistic, not optimistic" (per the Manifesto's own stated failure mode) requires judgment
  about what systematics are realistic and whether they're actually being applied, not just
  whether the script exits 0.

No Opus/Fable — nothing here is physics interpretation or epistemically delicate; it's
engineering verification of already-vetted-as-real dependencies.

---

## Shared rules for all three agents

1. Filesystem is shared with the coordinator (this session) — no need to reinstall
   `cobaya/iminuit/scikit-learn/celerite/h5py/getdist`; they're already in
   `/home/callensxavier_gmail_com/venv`. Use `/home/callensxavier_gmail_com/venv/bin/python` /
   `/home/callensxavier_gmail_com/venv/bin/pip` explicitly — do not assume `python`/`pip` on PATH
   resolves to the venv.
2. **No git commit, no git push, no git add.** Write output files only. The coordinator reviews
   and commits.
3. **Do not touch `PREDICTION.md` or anything under `data/raw/`.** A `prereg_guard.sh` hook now
   blocks this mechanically, but do not attempt to route around it either.
4. Do not read `/home/callensxavier_gmail_com/literature_review/` in bulk — same reason as D0.
5. Work under `/home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-Home/phase1_work/<agent>/`
   — create this directory, keep your outputs contained there, don't scatter files across the repo.
6. Web-call budgets are per-agent, stated below. `UNVERIFIED` / `BLOCKED` / `PARTIAL` are valid
   honest outcomes — do not strain to report success.
7. Final chat reply to coordinator: ≤ 250 words. The output file is the deliverable.

---

## Agent 1 — Emulator integration + adequacy check

- **Tier:** Sonnet
- **Web budget:** ≤ 10 calls (mostly git clone + local execution, not web research)
- **Working dir:** `phase1_work/agent1_emulator/`
- **Output:** `briefs/D0_VERIFICATION/PHASE1_A1_EMULATOR_INTEGRATION.md`

### Scope

1. `git clone https://github.com/jianxiangl-astro/lya-mfdm` into your working dir.
2. Check for a LICENSE file. State clearly present/absent — this was flagged unresolved by D0-B.
3. Inspect `environment.yml` — diff its dependencies against what's already installed in
   `/home/callensxavier_gmail_com/venv`. Install anything missing **into that same venv**
   (`/home/callensxavier_gmail_com/venv/bin/pip install ...`), not a new environment — do not
   create a conda env, this project uses one shared venv.
4. Load the trained emulator (`emu/emu_N100` or similar, `interpolator.py` / `tgu_interpolator.pkl`
   per the README) and run ONE smoke-test prediction: pick a benchmark point from within the
   paper's own stated training grid (log10(m_FDM/eV) and f_FDM — pick something like
   log10(m)=-21, f=0.1) and confirm you get back a P1D(k) array that is (a) finite, (b) positive,
   (c) roughly the right order of magnitude for a Lyα flux power spectrum (~1e-2 to 1 in the
   units the repo itself uses — check its own plots/README for scale, don't assume).
5. **Domain check (this is the decisive part):** the paper trains at z = 5.0, 4.6, 4.2. DESI DR1
   Lyα spectra span z ≈ 2.2–4.4 (per WP-E7 recon). Determine, from the repo's own code/data
   (not by assumption): does the emulator only predict at its three trained redshifts, or does it
   interpolate/extrapolate to other z? If it's fixed to those three z-bins, that is a REAL
   constraint on WP-E6 v2's usable DESI redshift range — say so explicitly, don't paper over it.
   Also report the trained (m,f) grid resolution/coverage from the actual data files, not the
   paper abstract.
6. Attempt a minimal integration test: wrap ONE emulator call as a Cobaya external likelihood
   function (a Python function returning log-likelihood given data + emulator prediction is
   enough — full MCMC run is NOT required) OR, if that proves nontrivial within budget, wrap it
   as a plain Python function callable from `iminuit.Minuit` for profile-likelihood at a single
   grid point. Report which one you achieved and why, if not both.

### Definition of Done

Output file must state, unambiguously:
- LICENSE: present/absent (+ terms if present)
- Install: clean / required N additional packages (list them) / failed (+ error)
- Smoke test: PASS (with the actual P1D(k) values returned) / FAIL (+ full traceback)
- Domain check: exact answer on z-coverage (fixed 3 bins vs interpolable), exact (m,f) grid
  resolution from the data files
- Integration: iminuit-wrapped / Cobaya-wrapped / neither-achieved-because-X, with the actual code
  that works (paste it in the report, it should be re-runnable)
- **One-paragraph verdict**: is this emulator actually usable for WP-E6 v2 as originally hoped, or
  does the domain/z-coverage finding change the scope? Be blunt if it does.

### Validation

Coordinator will re-run your smoke-test code verbatim before trusting the PASS verdict.

### Stop conditions

- Hit 10 web calls → write up what you have.
- If the emulator fails to load after 3 distinct fix attempts (dependency issues, path issues,
  API mismatches vs README) → report FAIL with full detail, do not keep guessing indefinitely.

---

## Agent 2 — Grid sweep scaffolding (`brian-i/sweeps`)

- **Tier:** Haiku
- **Web budget:** ≤ 6 calls
- **Working dir:** `phase1_work/agent2_sweep/`
- **Output:** `briefs/D0_VERIFICATION/PHASE1_A2_SWEEP_SCAFFOLD.md`

### Scope

1. `git clone https://github.com/brian-i/sweeps` into your working dir.
2. Follow its own documented usage (README) to build a JSON grid config for exactly this
   parameter space (this is a PLACEHOLDER grid for pipeline-validation, falsely attributed to K3_CRITERIA.md in earlier docs -- that file contains no such grid, see correction note; values kept for continuity across agents, not because they are physically approved):
   - `m` (axion mass, meV): `[0, 0.1, 0.5, 1, 5]`
   - `f` (FDM fraction): `[0.0, 0.1, 0.5, 1.0]`
   - 20 total (m,f) cells
3. Wire it against a **placeholder likelihood function** — a stub Python function that takes
   (m, f) and returns a dummy scalar (e.g. `-((m-1)**2 + (f-0.3)**2)`, just something that varies
   smoothly so the sweep has something real to iterate over). Do NOT attempt to call the real
   emulator — that's Agent 1's territory and isn't ready yet.
4. Run the sweep end-to-end against the stub and confirm all 20 cells produce output.
5. Write a short "how to plug in the real likelihood" note: exactly which file/function a future
   step would edit to swap the stub for Agent 1's emulator-backed likelihood.

### Definition of Done

- Confirm `brian-i/sweeps` cloned and its actual documented invocation command (paste it)
- The JSON config file you built (paste its contents)
- Proof of a full run: all 20 cells present in the output, no missing/failed cells
- The one-paragraph "how to swap in the real likelihood" note

### Validation

Coordinator checks: does the JSON config's (m,f) values exactly match the list above (no
rounding drift, no reordering)? Does the output genuinely have 20 entries?

### Stop conditions

- 6 web calls → write up what you have.
- If `brian-i/sweeps` turns out to require something not achievable in this environment (e.g. a
  job scheduler that doesn't exist here) → report that plainly and fall back to demonstrating the
  same 20-cell sweep via plain Python `multiprocessing.Pool`, noting the fallback was used.

---

## Agent 3 — Synthetic pre-flight infrastructure

- **Tier:** Sonnet
- **Web budget:** ≤ 8 calls
- **Working dir:** `phase1_work/agent3_synthetic/`
- **Output:** `briefs/D0_VERIFICATION/PHASE1_A3_SYNTHETIC_PREFLIGHT.md`

### Scope

1. `git clone https://github.com/desihub/desisim` and
   `git clone https://github.com/Jiaxi-Yu/modelling_spectro_sys` into your working dir.
2. Using `desisim`'s documented `quickquasars` tool (confirmed by D0-A to generate Lyα forest
   mocks), generate a SMALL synthetic baseline — a handful of mock quasar spectra (10–50 is
   plenty; this is a feasibility/infra check, not a production run) with Lyα forest absorption.
3. Using `modelling_spectro_sys`'s documented systematics injection, inject realistic DESI
   contaminants into those mocks: resolution damping, masked pixels, spectrograph noise — whatever
   the repo actually supports (check its README/code, don't assume it has everything the
   Manifesto listed).
4. **Judgment call, not a formality:** after injection, compare the contaminated vs clean mock
   power spectrum. Confirm the contamination measurably degrades/biases the signal (i.e. it's
   doing something, not a no-op). If the injected systematics have ~0 effect, say so — that would
   mean the "rigorously pessimistic" requirement from the Manifesto is NOT being met, and using
   this as a WP-E6b-style pre-flight would understate real systematics (exactly the failure mode
   the Manifesto itself warned against).
5. Report what fraction of the Manifesto's claimed systematics list (resolution damping, masked
   pixels, spectrograph noise) `modelling_spectro_sys` actually implements versus what's missing
   and would need hand-rolling.

### Definition of Done

- Confirm both repos cloned; report their actual (not assumed) capabilities from reading the code
- Mock generation: N spectra produced, method used, any errors encountered + how resolved
- Systematics injection: which contaminants were actually applied (from the repo's real feature
  set, not the Manifesto's wishlist)
- The clean-vs-contaminated comparison result (numbers, not just "it worked")
- Gap list: which claimed systematics are NOT covered by `modelling_spectro_sys` and would need
  separate implementation

### Validation

Coordinator checks the clean-vs-contaminated comparison is a real before/after number, not an
assertion.

### Stop conditions

- 8 web calls → write up what you have.
- If mock generation fails after 3 distinct fix attempts → report FAIL with detail, don't loop
  indefinitely.

---

## Coordinator follow-up (after all three land)

1. Re-run Agent 1's smoke-test code verbatim (verification, not trust)
2. (SUPERSEDED -- K3_CRITERIA.md does not contain this grid; see correction note. Cross-check instead against whatever real grid T0 eventually approves.)
3. Decide whether Agent 1's domain-check finding (z-coverage) requires a T0 escalation before
   Phase 2 (Stats Design) proceeds
4. Only after review: decide what (if anything) gets committed
