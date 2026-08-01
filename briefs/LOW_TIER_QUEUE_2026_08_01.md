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
| A-S2-1 | **[BLOCKER, flag don't fix]** `K3_CRITERIA.md` is cited as "frozen" and authoritative by `VISION.md`, `EXECUTION_PLAN.md`, and the `criteria-checkers` skill, but does not exist in the repo. `K3_CRITERIA_INTERFACE.md` (2026-07-24) looks like an earlier, superseded draft — it mixes in Track-B language ("Δ asymmetry alignment," "Weak Lensing correlation," "Swampland/F-theory alignment" as ranking weights) that doesn't belong in Track A's criteria. **Do not author `K3_CRITERIA.md` at T2 or T1 tier** — EXECUTION_PLAN's own P0-A/P0-B rows require "T1 drafts; T0 reviews" for exactly this kind of schema. Flag to T0; do not invent criteria. | T2 (flag only) | Implemented this session: `certificate_status.py` below works without it. |
| A-S2-2 | **DONE this session**: `scripts/certificate_status.py` — mechanical aggregation over `data/certificates/*.json`, no criteria file needed. Regenerate on every new certificate. | T2 | See §3.1 |
| A-S2-3 | Run the full regression suite (`TODO.md` §Regression command block) from clean shell; report pass/fail table. Baseline health check, no judgment calls. | T2 | **DONE 2026-08-01** (continuation): all 12 commands green at S2 `2c6d87e` — `test_refs_self_regenerate`, `test_L3_irreducible_minimal_controls`, `check_L3_irreducible_minimal`, `check_C2_transcendental_rank`, `check_s7_partner_integrality_modular`, `check_neron_severi_ambient`, `check_s7_hauptmodul_gamma07plus`, `test_gate_e_verdict_controls`, `check_tier_language` (0 violations/118 files), `check_U1_lattice`, `test_U1_controls`, `test_U1_witness_serialization_controls` + `check_U1_witness_serialization.py --all` (witness PASS). No regressions from this session's G0-s10/C2-s10-v4 work. |
| A-S2-4 | Root-doc archive triage: everything in S2 root dated 2026-06-25 through 2026-07-18 (`K3_DISCOVERY_REPORT.md`, `K3_SELECTION_REPORT.md`, `AGORA_IMPLEMENTATION_PLAN.md`, `scientificplan.md`, `VALIDATION_GUIDE.md`, `LL.md`, `K3xT2_DEEP_IMPROVEMENT_PLAN.md`, `MILESTONE_v2.1.0_RELEASE_NOTES.md`, etc. — full list via `git log -1 --format=%ad --date=short -- <file>` per root `.md`) predates the ledger and has not been triaged for Track-B contamination the way `AUTORESEARCH_IMPLEMENTATION_GUIDE.md` was. Mechanical task: for each file, read it, classify as (a) superseded-historical (move to `archive/pre-ledger/` with a one-line dated note), (b) still-current (leave, note why), or (c) Track-B material needing its own firewall citation. No judgment beyond that three-way sort; escalate anything ambiguous rather than deciding. | T2 | Queued, not started — flagged as real but non-blocking |

### S3 (Home / Experimentation)

| # | Task | Tier | Notes |
|---|---|---|---|
| A-S3-1 | **DONE this session**: systemd unit for `datalake_harvest_daemon.py` — closes the reboot-durability gap flagged repeatedly in session logs (daemon found dead after VM/session restarts on 07-30, 07-31, 08-01). | T2 | See §3.2 |
| A-S3-2 | Full v1.0 SHA-256 datalake manifest — `scripts/audit_datalake.py` times out on 1155 objects (known gap since 07-31). Batch/chunk it (e.g. resumable checkpoint file, N objects per invocation) so it completes without a single long-running call. | T2 | **DONE (implementation) 2026-08-01 continuation, run in progress.** Rewrote with a per-object checkpoint (`data/.audit_datalake_checkpoint.json`, gitignored) + `--batch-size`; new `PENDING` status for not-yet-processed objects (not silently merged into `PRESENT`). Root-cause measured, not guessed: 1114/1155 objects are analysis-relevant+≤100MB, i.e. genuinely need a real download+hash — this was never a "bug," just too much work for one bounded call. Also found and fixed a real pre-existing bug while in the function: `get_gcs_metadata()` called `gcloud storage stat`, which **is not a valid subcommand in this gcloud version** (`Invalid choice: 'stat'`) — it has silently failed and returned `None,None` on every call since it was written; fixed to `gcloud storage objects describe --format=csv[no-heading](md5_hash,crc32c_hash)`, field names verified directly against a real object before use. Verified: 20-object two-batch test showed correct resume (10→20 checkpointed, no reprocessing) and real, non-null md5/crc32c in the manifest. Full 1155-object run launched in background (checkpointed, safe to interrupt); manifest + checkpoint commit to follow once it completes. |
| A-S3-3 | Planck plik_lite fetch (DL-2 P1, T0-ratified 2026-07-31) — was gated on manifest v1.0 completion; re-check gating once A-S3-2 lands. | T2 | Still queued — blocked on A-S3-2's background run finishing |
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
| B-S2-2 | LR-1 (OEIS cross-match for $S_{1,2}$/$S_{2,1}$) — needs live OEIS API access. | T2 | Queued — sandbox branch workflow now proven by B-S2-1, ready to pick up |
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
