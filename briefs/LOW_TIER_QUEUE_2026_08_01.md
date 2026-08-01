# Low-tier (T2/Haiku) execution queue — Stream 2 (K3 selection) & Stream 3 (experimentation, citizen science, large-scale processing)

**Date:** 2026-08-01. **Authority:** T0 request ("continue... for low tier model"), scope
decision "both tracks, kept explicitly separate" (2026-08-01, recorded in
`briefs/COORDINATOR_PASS_E6PIN_2026_08_01.md`'s sibling session and mirrored in this brief).
**Executor tiers per the canonical roster** (`EXECUTION_PLAN.md` §1.1): T2 = Haiku/Gemini
Flash, bulk/mechanical, every output coordinator-re-derivable; T1 = Sonnet, capable worker;
T0 = Fable 5/Xavier, rulings and sign-off.

## 0. Prerequisite: two tracks exist in these repos, now formally separated

Investigation this session found that "K3 selection" and "citizen science / large-scale
processing" — the user's literal words — match a **second, pre-ledger track** living in the
same two repos as the certified cooper_s7/s10 program, not that program itself. Both are now
real, both continue, explicitly separated:

- **Track A — cooper_s7/s10 Sym²/lattice program.** Governed by the live Tier A/B/C ledger
  (`CLAUDE.md` in both repos). This is the track this session's earlier work (G0-s10
  certificate, C2_cooper_s10_v4_DRAFT, coordinator passes) belongs to.
- **Track B — DarkMatterK3@Home / "AutoEvolve R2 Hypothesis Foundry" / K3-T2-Chameleon.**
  Pre-ledger (commits 2026-07-05–2026-07-26), just firewalled as EXPLORATORY SANDBOX in both
  repos' `CLAUDE.md` (rule 7/S3, rule 7/S2, this session, 2026-08-01) after finding 35 live,
  un-firewalled `K3-DISC-*` claims in `api/discoveries.json` (S3) plus a shipped WASM/BOINC
  compute stack (`ui_loom/`, `core_wasm/`, `public/wasm/`) — the same overclaiming shape as
  three prior fabrication incidents this project already caught (Discovery PDF, Lean oracle,
  datalake table). **No output from Track B queue items below may be cited into Track A's
  certificates or Streams 1–3's Tier A/B/C claims.** Track B work happens on a
  `sandbox/`-prefixed branch, never directly on `main`.

Three similarly-named-but-unrelated systems exist across the program — see the disambiguation
block in each repo's `CLAUDE.md` rule 7 before touching anything named "AutoEvolve" or
"AlphaEvolve." Do not skip that block; conflating them is the easiest way to mis-scope a task.

---

## 1. Track A queue (un-firewalled, continues exactly as before)

### S2 (K3-DarkMatter)

| # | Task | Tier | Notes |
|---|---|---|---|
| A-S2-1 | **[BLOCKER, flag don't fix]** `K3_CRITERIA.md` is cited as "frozen" and authoritative by `VISION.md`, `EXECUTION_PLAN.md`, and the `criteria-checkers` skill, but does not exist in the repo. `K3_CRITERIA_INTERFACE.md` (2026-07-24) looks like an earlier, superseded draft — it mixes in Track-B language ("Δ asymmetry alignment," "Weak Lensing correlation," "Swampland/F-theory alignment" as ranking weights) that doesn't belong in Track A's criteria. **Do not author `K3_CRITERIA.md` at T2 or T1 tier** — EXECUTION_PLAN's own P0-A/P0-B rows require "T1 drafts; T0 reviews" for exactly this kind of schema. Flag to T0; do not invent criteria. | T2 (flag only) | Implemented this session: `certificate_status.py` below works without it. **RESOLVED (mystery, not the gap) 2026-08-01, continuation part 3**: the file DOES exist — in S1 (`~/SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal/K3_CRITERIA.md`), not S2. Its own header names S2 as "repo of record" with a hash-pinned copy promised "at freeze," but the full v1.0 freeze (§7 thresholds/weights) never completed — only §1 (candidate register) froze 2026-07-20 — so the promised copy-to-S2 never triggered. **Also found the register itself is stale**: it DROPPED t103 (2026-07-18, "order-4 CY3, category error"), but S2's own later `ESCALATIONS.md` E-014 (2026-07-26, thorough 9-artifact+git-history search) found no T0 veto ever existed and the disqualifying property belongs to a different candidate (`cooper_s18`). Flagged to T0 in S1 `briefs/T0_FLAG_K3_CRITERIA_T103_STALE_2026_08_01.md` (S1 `a5a3e01`) — not amended, candidate-register changes are T0-owned. S22 (same 07-18 drop) checked separately, found uncontested, left as-is. |
| A-S2-2 | **DONE this session**: `scripts/certificate_status.py` — mechanical aggregation over `data/certificates/*.json`, no criteria file needed. Regenerate on every new certificate. | T2 | See §3.1 |
| A-S2-3 | Run the full regression suite (`TODO.md` §Regression command block) from clean shell; report pass/fail table. Baseline health check, no judgment calls. | T2 | **DONE 2026-08-01** (continuation): all 12 commands green at S2 `2c6d87e` — `test_refs_self_regenerate`, `test_L3_irreducible_minimal_controls`, `check_L3_irreducible_minimal`, `check_C2_transcendental_rank`, `check_s7_partner_integrality_modular`, `check_neron_severi_ambient`, `check_s7_hauptmodul_gamma07plus`, `test_gate_e_verdict_controls`, `check_tier_language` (0 violations/118 files), `check_U1_lattice`, `test_U1_controls`, `test_U1_witness_serialization_controls` + `check_U1_witness_serialization.py --all` (witness PASS). No regressions from this session's G0-s10/C2-s10-v4 work. |
| A-S2-4 | Root-doc archive triage: everything in S2 root dated 2026-06-25 through 2026-07-18 (`K3_DISCOVERY_REPORT.md`, `K3_SELECTION_REPORT.md`, `AGORA_IMPLEMENTATION_PLAN.md`, `scientificplan.md`, `VALIDATION_GUIDE.md`, `LL.md`, `K3xT2_DEEP_IMPROVEMENT_PLAN.md`, `MILESTONE_v2.1.0_RELEASE_NOTES.md`, etc. — full list via `git log -1 --format=%ad --date=short -- <file>` per root `.md`) predates the ledger and has not been triaged for Track-B contamination the way `AUTORESEARCH_IMPLEMENTATION_GUIDE.md` was. Mechanical task: for each file, read it, classify as (a) superseded-historical (move to `archive/pre-ledger/` with a one-line dated note), (b) still-current (leave, note why), or (c) Track-B material needing its own firewall citation. No judgment beyond that three-way sort; escalate anything ambiguous rather than deciding. | T2 | Queued, not started — flagged as real but non-blocking |

### S3 (Home / Experimentation)

| # | Task | Tier | Notes |
|---|---|---|---|
| A-S3-1 | **DONE this session**: systemd unit for `datalake_harvest_daemon.py` — closes the reboot-durability gap flagged repeatedly in session logs (daemon found dead after VM/session restarts on 07-30, 07-31, 08-01). | T2 | See §3.2 |
| A-S3-2 | Full v1.0 SHA-256 datalake manifest — `scripts/audit_datalake.py` times out on 1155 objects (known gap since 07-31). Batch/chunk it (e.g. resumable checkpoint file, N objects per invocation) so it completes without a single long-running call. | T2 | **DONE 2026-08-01, S3 `4156f5d`.** Checkpointed rewrite + `gcloud storage stat`→`objects describe` fix (see prior entries) held up across the full background run: **1155/1155 objects reached, 0 PENDING** (1112 AUDITED, 41 PRESENT, 2 QUARANTINED, 4 ABSENT). One more real bug found reviewing the completed output and fixed before committing: both QUARANTINED seed files were appearing twice (real record + an unconditional synthetic "N/A"-size seed row) — pre-existing, only visible once a run actually completed; fixed to skip the synthetic seed row when the URI is already in the real bucket listing. Totals now reconcile exactly (1112+41+2=1155, +4 synthetic ABSENT markers for files confirmed not in the bucket). |
| A-S3-3 | Planck plik_lite fetch (DL-2 P1, T0-ratified 2026-07-31) — was gated on manifest v1.0 completion. | T2 | **DONE 2026-08-01, S3 `cf1a49a`+follow-up.** New `scripts/fetch_planck_plik_lite_staging.py`: downloads the ESA PLA baseline likelihood release (60MB, not multi-GB as feared), extracts only `plc_3.0/hi_l/plik_lite/` (both TT and TTTEEE variants — 24 files incl. `cl_cmb_plik_v22.dat` bandpowers + `c_matrix_plik_v22.dat` covariance), uploads to `gs://.../planck_2018/` staging. **One real bug caught by the script's own loud-failure design**: the PLA wiki's documented path (`plc_3.0/hi_l/...`) omits a `baseline/` wrapper directory the actual tarball uses — first run correctly refused to guess and failed loudly ("no members found... do not guess, re-check"); confirmed the real layout via `tar tzf` before fixing the prefix, not by re-guessing. **Second gap found+fixed**: `audit_datalake.py`'s `ANALYSIS_RELEVANT_PATTERNS` didn't include `planck_2018/`, so the newly staged files came back `PRESENT` (no hash) instead of the WP-required `AUDITED` (SHA-256) — added the pattern, re-ran, verified the manifest's SHA-256 for `cl_cmb_plik_v22.dat`/`c_matrix_plik_v22.dat` matches the fetch script's own independently-computed hash exactly (two independent computations agreeing). Per WP scope: staging only, does NOT enter `data/raw/`, no `fetch_data.py` entry, until a Planck channel amendment is pinned (DL-3). Final manifest: 1136 AUDITED (was 1112), 41 PRESENT, 0 PENDING. |
| A-S3-4 | SWEEP still blocked on T0's 66→9 aggregation ruling (`7ca1846`) — not a T2 task, listed here only so this queue doesn't imply it's actionable. | — | Blocked on T0, unchanged |

---

## 2. Track B queue (sandboxed — `sandbox/` branch only, non-citable outputs)

Per the firewall ruling, every item below stays off `main`, and every output document must
carry the same disclosure line: *"EXPLORATORY SANDBOX output — not certified, not citable
into Streams 1–3 or any Tier A/B/C claim."*

### S3 — completeness audit (do this one first; it's the safest possible Track-B task)

| # | Task | Tier | Notes |
|---|---|---|---|
| B-S3-1 | **DONE this session**: audit whether "Phase 5 DarkMatter@Home WASM complete" and "Phase 6 BOINC complete" commit-message claims match what's actually in the tree (tests present? do they pass? does `core_wasm` build?). Mechanical claims-vs-artifact check, same discipline as WP-A/WP-B — produces value without extending any physics claim. | T2 | See §3.3 |
| B-S3-2 | If B-S3-1 finds gaps, file them the same way WP-A/WP-B filed the Discovery-PDF/Lean-oracle gaps — a dated audit brief, no editorializing beyond what's checked. | T2 | Queued, contingent on B-S3-1 findings |

### S2 — AutoEvolve R2 Hypothesis Foundry, Phase A only (per `AUTORESEARCH_IMPLEMENTATION_GUIDE.md` §2, all explicitly HAIKU-tier in the source doc)

Only the lowest-risk Phase A items — pure literature/data tabulation, no candidate selection,
no physics-viability claims, no new "Discoveries":

| # | Task | Tier | Notes |
|---|---|---|---|
| B-S2-1 | LR-4 (archive reference documents: Lee & Tsai 2026, El Naschie 2013) — pure citation + honest epistemic classification, the guide's own text already flags El Naschie as "explicitly NOT load-bearing." Lowest-risk item in the whole guide. | T2 | **DONE 2026-08-01 continuation** — S2 branch `sandbox/autoevolve-r2-phase-a-2026-08-01` (pushed, `341caf5`). Both citations independently re-verified via WebSearch+WebFetch against primary sources (arXiv abstract page, SCIRP page) rather than trusted from the guide's paraphrase — found and corrected the exact paper title Lee & Tsai's content-only description had left unstated ("Naturally Resonant Dark Matter from Extra Dimensions," arXiv:2504.00076). |
| B-S2-2 | LR-1 (OEIS cross-match for $S_{1,2}$/$S_{2,1}$) — needs live OEIS API access. | T2 | **NOT EXECUTED, premise found stale 2026-08-01 continuation.** LR-1's own table already lists $S_{2,1}$ correctly as "Elliptic (Apéry ζ2)"; its one open cell is whether $S_{1,2}$ is K3. But `archive/pre-ledger/CAVEATS.md`'s "2026-07-14 Phase 8 rectification" (same date as the guide, S2 repo) already answered this **definitively**: both $S_{1,2}$/$S_{2,1}$ are elliptic (order-2 generating-function ODE, not order-3), and $S_{1,2}$'s mirror map has a non-integral second coefficient $q_2=81/8$ — a specific, checkable reason, stronger evidence than an OEIS term-match would produce. Running LR-1 as scoped would re-litigate an already-closed question with weaker evidence, and risk re-introducing "K3 (conjectural)" language for something already retracted. Per S2's own Standing Rule 4 ("verify a directive's artifacts before executing it") — this is exactly that check, applied to a Track-B source doc same as any other. If OEIS cross-matching is still wanted, retarget it at the **current** GATE-C finalist pool (A005259 Apéry ζ(3), A183204 Cooper s7, A005260 Cooper s10, A276536 t103, A002895 Domb, A125143 Almkvist-Zagier second — per `CAVEATS.md`'s own replacement pool), which is really LR-2's task, not LR-1's. |
| B-S2-3 | LR-2 (enumerate classified sporadics into a CSV, ≥15 sequences with OEIS IDs/weights/modularity) — pure tabulation from already-cited literature (Zagier 2009, Cooper 2012, AESZ). | T2 | **Deliberately deferred, not attempted** — every one of ~15 entries needs the same per-citation verification rigor as B-S2-1 (2 citations) took real effort for; rushing a 15-row table without that would violate the exact "no numbers from memory" discipline this queue is supposed to model. Left for a dedicated pass, not rushed. |

**Explicitly NOT queued yet, pending T0 review of B-S3-1's findings and this queue itself:**
Phase B (G1-4 monodromy, G2-2 No-Go check, G2-3 superradiance — these produce
physics-viability verdicts, higher stakes), Phase C (real-data QT tests), Phase D (Lean
modules, manuscript), Phase E (dispatching jobs to the live volunteer network at
`DarkMatterK3-Home.github.io`, i.e. actually running citizen-science compute against real
users) and any code change to `ui_loom/`/`core_wasm/`/`api/api_dispatcher.py`. These are
larger, higher-consequence, and per the guide's own timeline (~3–4 weeks for the WASM pivot
alone) do not fit a single low-tier queue turn. Re-scope after B-S3-1/B-S2-1..3 land and T0
has seen the firewall ruling.

---

## 2.5 Track A completeness health checks (added mid-continuation, all three repos)

Not originally scoped, added once the written queue was exhausted (all items done/blocked/
deferred) — rounds out Track A verification across all three repos rather than leaving S1/S3
untouched while S2 got a regression pass.

| # | Task | Result |
|---|---|---|
| A-S3-5 | `pytest pipeline/tests/` (S3) — full pipeline test suite, not run yet this session. | **DONE 2026-08-01**: 492 passed, 0 failed, 280s. |
| A-S1-1 | `lake build Agora` + `lake build Tests` (S1) — not run yet this session. | **DONE 2026-08-01**: both green (3114 / 3000 jobs, matching `TODO.md`'s last recorded 3106/3000 — small expected increase, not a regression). Only lint warnings (unused simp args, deprecated `push_neg`, unused variable bindings), zero errors. `sorry` count confirmed exactly 1 (`OpenGoals/PartnerIntegrality.lean:201`, the disclosed open goal) — the other grep hit (`GrowthBounds.lean:31`) is a docstring sentence ("PROVED (0 sorry), not open."), not a real tactic, checked in context before counting it. |

**All three repos now have a fresh, clean baseline as of this continuation**: S1 (Lean build +
tests), S2 (13-command regression suite), S3 (492 pipeline tests). No regressions found
anywhere from this session's work (G0-s10 cert, C2-s10-v4, archive move, script fixes).

## 3. What was implemented this session (2026-08-01)

### 3.1 `scripts/certificate_status.py` (S2, Track A)
Reads every `data/certificates/*.json`, extracts `certificate`/`operator`/`tier`/`status`/
`date`, and prints a sorted table. No dependency on `K3_CRITERIA.md`. Does not invent any
criteria weighting — purely lists what exists. Closes part of the gap the `criteria-checkers`
skill flagged ("no `scripts/render_status_table.py` — has never existed") without overstepping
into authoring the frozen criteria file itself.

### 3.2 `datalake-harvest-daemon.service` (S3, Track A)
A systemd user unit wrapping `scripts/datalake_harvest_daemon.py --interval 1800`, with
`Restart=on-failure` and `WantedBy=default.target`, so the daemon survives VM/session
restarts without a manual relaunch. Installed under `~/.config/systemd/user/`; enabled via
`systemctl --user enable --now`. (Requires `loginctl enable-linger` for the unit to run
without an active login session — documented in the unit file's header comment; not enabled
automatically since it changes system-level session behavior, flagged for Xavier.)

### 3.3 Track-B completeness audit (S3, Track B, sandboxed)
Checked "Phase 5"/"Phase 6" completeness claims against the actual tree: see
`sandbox/PHASE5_PHASE6_COMPLETENESS_AUDIT_2026_08_01.md` for the finding.

---
*Generated-by: Fable 5 (T1 coordinator) | Reviewed-by: pending T0*
