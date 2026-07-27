# Deep Think (T0s) Alignment Brief — 2026-07-27 (night update)

**To:** Deep Think, Scientific Companion (T0s) per EXECUTION_PLAN §1.1
**From:** T1 coordinator session, on T0 (Xavier) instruction
**Purpose:** update since `DEEPTHINK_ALIGNMENT_BRIEF_2026_07_27_EVENING.md`. One full
verification-gated execution arc on WP-E6 (Stream 3), one self-caught fabrication with full
correction trail, one delegated grid definition, and the Stream 1 paper committed. Canonical
copy: Stream 3 (`SocrateAI-Scientific-Agora-Home`); mirrored to the other two repos.
**Ground rule reminder (unchanged):** LLM output is never evidence. Everything below traces to
checkers, primary-source reads, re-run code, or recorded T0 decisions — and §4 below is a live
demonstration of why that rule exists.

---

## 0. Headline for adversarial review

Three things tonight deserve your scrutiny, in descending order of consequence:

1. **§4 — a fabricated provenance claim by the coordinator itself**, caught, corrected, and
   superseded, with the full audit trail preserved. Verify the correction is complete.
2. **§2 — the WP-E6 emulator domain finding** (usable at 3 discrete redshifts only) — the
   evidence is threefold and independently re-verified; check whether any downstream text still
   implies broader coverage.
3. **§5 — a [T0-DELEGATED] grid definition** now hash-anchored; check the anchor-fact table's
   claims against their stated primary sources.

## 1. WP-E6 D0 verification gate — CLOSED (Q1 answered: emulator EXISTS)

The evening brief's WP-E6 v2 proposal carried "no public mixed-(m,f) FDM flux-power emulator
found" as its default-STOP premise. A dedicated re-survey (D0-B, Sonnet, primary sources only,
18-call budget, stopped early at 9) **overturned that premise**: `github.com/jianxiangl-astro/lya-mfdm`
(Liu, Gong & Zhou 2026, arXiv:2606.06969) is public and ships trained weights. The paper's §3.2
confirms both log₁₀(m_FDM/eV) ∈ [−23,−19] AND f_FDM ∈ [0,1] as free parameters, emulating P1D
directly. Coordinator independently re-verified before acting: arXiv API fetch (paper real,
abstract quotes the mixed-f bounds), `gh api` (repo real, `emu/` contains .pkl weight files, 12
commits, last push 2026-07-06). **The prior "no code release found" finding was stale, not
wrong at the time** — the repo was created 2026-05-18.

Also in D0: 4/5 manifesto tooling repos confirmed real (`brian-i/sweeps`,
`Jiaxi-Yu/modelling_spectro_sys`, `desihub/desisim`, `desihub/desispec`);
`CobayaSampler/bao_data` **downgraded CONFIRMED→PARTIAL by coordinator spot-check** — it ships
DESI DR1 Lyα *BAO distance summaries* (D_M/r_d, D_H/r_d), not P1D(k); the D0-A agent's
"fit-for-use: yes" was too generous. Record: `briefs/D0_VERIFICATION/` (plan + 3 agent reports
+ in-file coordinator corrections).

## 2. Phase 1 — emulator integrated; decisive domain limitation found and triple-verified

**Integration: PASS.** Both an iminuit profile-likelihood wrapper and a Cobaya external
likelihood work and cross-validate (χ² = 77.41 vs loglike = −38.71 at the same point).
Environment note with audit value: installing `mpi4py` without a system MPI runtime *actively
broke* Cobaya (crash in MPI auto-detection) — uninstalled; this VM has no MPI at all.

**The finding that matters:** the emulator is trained at exactly **z = 5.0, 4.6, 4.2** and
nothing else. Evidence (each independently re-run by the coordinator, not taken from the agent):
(a) `mcmc.py` L52: `Z_FLOAT = {"5.0": 5.0, "4.6": 4.6, "4.2": 4.2}` — dict-lookup API, KeyError
otherwise; (b) the shipped `MinMaxScaler`'s own fitted state: `data_min_=4.2, data_max_=5.0` on
the z feature; (c) training data has one snapshot set per z, never a continuum. Force-feeding
out-of-range z into the raw network returns finite numbers — **unvalidated 3-point
extrapolation, explicitly excluded from all integration paths**. DESI DR1 Lyα spans z≈2.2–4.4:
only the top slice overlaps. LICENSE: **absent** from the repo — clone is used read/run-only and
is now gitignored (`phase1_work/`) so no push can redistribute it.

**Extension scoped, then deferred (T0 decision, twice revised in-session):** extending the
emulator to DESI's full range = O(50–210) fresh MP-Gadget runs (z=99→target; no public low-z
snapshots exist), MPI+GSL+PFFT mandatory, ~10k–200k+ core-hours (order-of-magnitude, unsourced).
Xavier initially chose "commission extension," then upon seeing the scoping reverted to
**Option 1: z≈4.2 slice now**, extension recorded as a future phase
(`briefs/FUTURE_PHASE_EMULATOR_EXTENSION_2026_07_27.md`). That record includes an honesty note
worth checking: `runux-ai-runtime` (Rust LLM-inference runtime) does **not** address the
MP-Gadget simulation cost that dominates; it could at most accelerate a future NN-retraining
step (~1% of cost).

**Synthetic pre-flight infra:** `modelling_spectro_sys` implements **0 of the 3** contaminants
the acceleration manifesto attributed to it (it does clustering-catalog redshift systematics,
never touches a flux array) — repo-purpose mismatch, found by reading its 134-line source.
Worked around via `desisim`'s own instrument simulator: contamination measurably degrades the
mock P1D (total power → 86.6% of clean; high-k → 56.4%), i.e. the pre-flight is genuinely
pessimistic, not a no-op. A naive 3% zero-fill pixel mask *increased* total power to 107.1% —
masking needs proper gap-handling, flagged for Phase 2.

## 3. Option 1 executed — forward-model only; the pin boundary held

Fresh NOIRLab TAP query (no z-cut): DESI DR1 has **3,912 QSOs in z ∈ [4.0, 4.4]** (1,867 in
[4.1, 4.3]) — the earlier cached catalog's z<2.1 ceiling was a WP-E7 query-scope artifact
(`zmin=0.8, zmax=2.1` hardcoded for BAO tracers), verified in its own fetch manifest. So the
z=4.2 slice has a real population (spectroscopic count; not yet an S/N-, BAL-, DLA-cut forest
sample).

The 56-cell forward-model landscape at z=4.2 was computed as **model exploration only** — the
agent's report states, grep-verifiably, that no χ²/likelihood against any observational data was
computed. `PREDICTION.md`'s existing pin (v1.0, 2026-07-24) covers a *different, narrow*
Lyman-α null test; the MFDM sweep's real-data comparison remains gated behind a future
PREDICTION v2 pin. CLAUDE.md rule 1 held throughout.

## 4. CORRECTION — fabricated grid provenance (coordinator's own error, full disclosure)

**What happened:** in the first document of this session (a literature-review synthesis), the
coordinator wrote a specific (m,f) grid — {0, 0.1, 0.5, 1, 5} "meV" × {0, 0.1, 0.5, 1.0} — and
attributed it to "K3_CRITERIA.md v0.1" **without ever opening that file**. The claim was then
repeated as "the frozen K3_CRITERIA.md grid — do not alter it" across the D0 and Phase 1
planning documents, and two agents ran real computation against it. `K3_CRITERIA.md` is real
but entirely unrelated: K3 geometric selection criteria (C1–C5), zero physics-grid content,
still SKELETON v0.1 NOT FROZEN. The "meV" unit was additionally ~19 orders of magnitude outside
the emulator's domain — it was an agent's incidental unit sanity-check that forced the trace-back.

**Correction trail (verify completeness):**
`briefs/CORRECTION_FABRICATED_GRID_PROVENANCE_2026_07_27.md` (the record); in-file strikes in
`D0_AGENT_PLAN`, `PHASE1_AGENT_PLAN`, `PHASE1_DECISION`; a durable cross-session memory entry.
**What survives:** the pipeline engineering (wrappers, sweep mechanics, landscape method) —
exercised against placeholder numbers, which is legitimate; the sourcing claim is void.
**Adversarial note:** the same session applied strict primary-source verification to every
*third-party* claim while its *own* prior assertion got a pass — the precise failure mode the
"LLM output is never evidence" rule exists to catch. It applies reflexively.

## 5. Real (m,f) grid defined — [T0-DELEGATED], hash-anchored

Xavier delegated grid definition verbally ("I give you authority to propose (m,f) grid value
and unit"). Result: `briefs/T0_MF_GRID_DEFINITION_2026_07_27.md`, hash-anchor commit `27cff4a`.

- **Unit:** log₁₀(m_FDM/eV) — the emulator's native coordinate; **no unit conversion exists
  anywhere in the pipeline** (the meV failure mode removed structurally).
- **Grid:** 8 masses {−22.9, −22.5, −22, −21.5, −21, −20.5, −20, −19.1} × 7 fractions
  {0, 0.05, 0.10, 0.20, 0.35, 0.60, 0.99} = 56 cells, z = 4.2 only.
- **Every value anchored** to a re-verified primary source (anchor table in-file): `param.pkl`
  actual LHS extrema [−22.987, −19.006] × [0.00235, 0.99829] — nominal endpoints −23/−19/1.0
  deliberately avoided as outside sampled support; `mcmc.py` F_EPS branch (f=0 exact);
  arXiv:2606.06969 published bounds (density concentrated on the exclusion boundary).
- **Built-in controls (15/56 cells):** f=0 column must return m-independent byte-identical
  P1D(k); the −19.1 row must recover the published null. Cells that fail these indict the
  pipeline, not the physics.
- Countermand log open in-file; freeze-for-real happens only at the Phase 3 PREDICTION v2 pin.

## 6. Stream 1 — paper committed and pushed (commit `5bd0916`)

All 10 sections + compiled PDF (33 pp). The commit's verification pass caught a real LaTeX
defect: an unbraced `[z]` inside a `\begin{remark}[…]` optional argument truncated the argument
mid-math-mode and cascaded errors into later sections — **the previously-existing PDF had been
built with this error silently swallowed** (nonstopmode). Fixed at source; clean rebuild, 0
errors, 0 undefined refs. PLAN.md §5 T0 questions remain open (scope A/B, venue, authorship
wording, ρ=19/T=3 presentation, internal-manuscript citation).

## 7. Ops changes with epistemic relevance

- **`prereg_guard.sh` was never wired.** Stream 3's PREDICTION-pin + data/raw-immutability hook
  existed on disk but no settings.json referenced it — the "hook-enforced" claim in CLAUDE.md
  rule 2 was aspirational until tonight. Now wired (PreToolUse on Edit|Write), pipe-tested on
  block/block/allow cases before being trusted.
- Permissions hardened across all 4 configs (global + 3 streams): explicit `defaultMode: auto`,
  calibrated allow/ask/deny; Stream 1's unscoped `"Bash"` allow and Stream 3's missing
  settings.json both closed.
- `phase1_work/` gitignored in Stream 3 (unlicensed third-party clones must not be pushed).
- ⚠️ Stream 2's PAT remains embedded in its git remote URL **and was printed in cleartext in a
  session transcript today** — rotation is now urgent, not advisory.

## 8. What is pending T0 (unchanged items omitted; see restart brief)

Grid countermand window (§5); Phase 2 stats-design kickoff on the new grid; paper PLAN.md §5;
PAT rotation; WP-E7 occupancy ratification; eBOSS LRG sample identity.
