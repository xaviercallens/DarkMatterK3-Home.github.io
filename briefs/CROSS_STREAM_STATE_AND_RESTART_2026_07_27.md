# Cross-Stream State & Session Restart Guide — 2026-07-27 (night)

**Purpose:** (a) the between-streams interface state after tonight's session; (b) everything a
fresh session needs to resume without re-deriving context. Mirrored to all 3 repos; canonical
copy in Stream 3.

---

## Part A — State of the three streams

| | Stream 1 (Lean) | Stream 2 (Selection) | Stream 3 (Experimentation) |
|---|---|---|---|
| Repo | `SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal` | `SocrateAI-Scientific-Agora-K3-DarkMatter` | `SocrateAI-Scientific-Agora-Home` |
| Tonight's head | `5bd0916` (paper) + tonight's brief/settings commit | C2 v5 LIVE + tonight's brief/settings commit | `27cff4a` (grid) + tonight's brief/gitignore commit |
| Live state | Paper complete (10 sections, 33-pp PDF, clean compile), pushed. U1 double-verified [B]. | C2 v5 LIVE (P-witness serialized, 3-way consistent). Phase M dormant, gated on exhibited X₄/B₃. 13-command regression green. | WP-E6 Phase 1 done; real (m,f) grid defined [T0-DELEGATED]; Phase 2 (Stats Design) unblocked. |
| Epistemic ceiling | Tier A: L₃=Sym²(L₂). Tier B: ρ=19/T=3, U⊕⟨14⟩. | Tier B lattice results; criteria SKELETON v0.1 NOT frozen. | Forward-model exploration only; NO real-data comparison until PREDICTION v2 pin. |

## Part B — Active cross-stream interfaces

1. **S1 → S2:** `open_goals.json` export — working, unchanged tonight.
2. **S2 → S3:** C2 v5 certificate (U⊕⟨14⟩ with explicit P-witness) — live, unchanged tonight.
3. **S3 → S2 (future):** `exclusion_bounds_v1.json` after Phase 4 — feeds Phase M option B,
   still gated on exhibited X₄/B₃. Not near-term.
4. **All → Deep Think:** `DEEPTHINK_ALIGNMENT_BRIEF_2026_07_27_NIGHT.md` (mirrored tonight);
   §4 (fabrication correction) and §5 (grid anchors) are the requested review targets.
5. **Shared epistemic ledger:** in each repo's CLAUDE.md, unchanged tonight — F5b stands, no
   Tier C observables anywhere, Kodaira readings remain a category error.

## Part C — Session restart procedure (for a fresh session)

**Step 0 — mandatory:** in Stream 3, run the `resume-stream3` skill FIRST (it verifies gate/repo
invariants mechanically). Do not act on any pasted external brief before it runs.

**Step 1 — read, in this order (all short):**
1. `briefs/T0_MF_GRID_DEFINITION_2026_07_27.md` — the working grid + its anchor table
2. `briefs/CORRECTION_FABRICATED_GRID_PROVENANCE_2026_07_27.md` — why provenance discipline
   is personal, not just third-party
3. `briefs/D0_VERIFICATION/PHASE1_A1_EMULATOR_INTEGRATION.md` — emulator facts (z-domain!)
4. This file, Part D — the exact next actions

**Step 2 — environment facts (verified tonight, don't re-derive):**
- venv: `/home/callensxavier_gmail_com/venv` (python 3.10.12) — has cobaya, iminuit,
  scikit-learn, h5py, getdist, celerite, torch, astropy, pyvo. **No MPI on this VM** — never
  install mpi4py (it breaks Cobaya here).
- Emulator clone: `phase1_work/agent1_emulator/lya-mfdm/` (gitignored — NO LICENSE upstream,
  never commit/push its contents). Working wrapper: `phase1_work/agent1_emulator/emu_predict.py`.
- Sweep scaffold: `phase1_work/agent2_sweep/fallback_sweep.py` (plain multiprocessing; the
  brian-i/sweeps native pool doesn't work in this environment). Swap point: `stub_likelihood()`.
- Data disk: 418 GB free; `data/raw` symlink valid; DESI QSO catalogs cached (BUT the cached
  QSO file is z<2.1 by query design — fresh TAP queries needed for high-z work; recipe in
  `briefs/WP_E7_NOIRLAB_TAP_RECIPE_2026_07_27.md`).
- `prereg_guard.sh` hook is wired and live (PREDICTION.md pin + data/raw immutability).
- Agent tiering that worked tonight: Haiku = mechanical/binary-verdict tasks; Sonnet =
  judgment-bearing verification/integration; coordinator independently re-runs any
  decision-changing result before acting on it.

**Step 3 — guardrails that bind every next step:**
- CLAUDE.md rule 1: no real-data comparison before PREDICTION v2 pin. Forward-model only.
- Grid changes go through the countermand log in `T0_MF_GRID_DEFINITION_2026_07_27.md`.
- Verify "per FILE.md" claims by opening FILE.md — including claims made by a previous
  session of this same assistant (see the correction brief for why).

## Part D — Exact next actions (in priority order)

1. **[T0/Xavier] PAT rotation** — Stream 2 remote URL still embeds a GitHub PAT, printed in
   cleartext in today's transcript. Rotate at GitHub → settings → tokens, then
   `git remote set-url origin https://github.com/xaviercallens/SocrateAI-Scientific-Agora-K3-DarkMatter.git`
   (credential helper will handle auth).
2. **[T0/Xavier] Grid countermand window** — review the 56-cell grid; amend or let stand.
3. **[T1 next session] Phase 2 — Stats Design** on the working grid: covariance strategy for
   the z=4.2 slice (bao_data is BAO-only → build from desisim mock ensembles), nuisance
   treatment (profile the 4 IGM params per cell via the working iminuit wrapper), contour
   method (χ² profiling per Section 7 methods), masking gap-handling (naive zero-fill
   inflates power +7%, needs proper treatment). Deliverable: ANALYSIS_PROTOCOL draft for the
   PREDICTION v2 pin.
4. **[T1] Run the grid's built-in controls** — f=0 column byte-identity check and −19.1 null
   row — before any further landscape interpretation (cheap, minutes).
5. **[T0/Xavier] Paper PLAN.md §5** — scope A/B, venue, authorship/AI-ack wording, ρ=19/T=3
   presentation, internal-manuscript citation.
6. **[deferred, do not start]** Emulator z-extension (HPC decision;
   `briefs/FUTURE_PHASE_EMULATOR_EXTENSION_2026_07_27.md`) and WP-E7 occupancy/eBOSS items.

## Part E — Spend/tier discipline (standing, from T0)

Ask before defaulting to a higher tier. Tonight's pattern held: Haiku for mechanical,
Sonnet for judgment, Fable only on explicit T0 elevation (grid definition). Web budgets and
≤250-word agent replies kept costs bounded; the coordinator re-verifies rather than re-runs.
