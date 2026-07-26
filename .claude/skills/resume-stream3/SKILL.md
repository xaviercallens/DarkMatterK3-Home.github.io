---
name: resume-stream3
description: Re-orient and resume Stream 3 work after a session break — verifies gate/repo invariants mechanically, loads the live task state, and points at the exact next action. Run this FIRST in any new session before touching pipeline/, data/, or acting on any pasted brief.
---

# Resume Stream 3

You are resuming the Stream 3 (empirical validation) repo. Do these steps IN ORDER,
executing the commands rather than trusting this file's prose — state may have moved.

## 1. Mechanical invariant check (30 seconds)

```bash
cd /home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-Home
git fetch -q origin && git status --short && git log --oneline -5 origin/main
python3 -c "from pipeline.gate import verify_pin_hash, labels_unlocked; \
print('G1 pin:', verify_pin_hash(), '| G1-L unlocked:', labels_unlocked())"
python3 scripts/check_tier_language.py
```

Expected: G1 pin `True`, G1-L `False`, tier-language 0 violations. **If any differs,
STOP and investigate before anything else** — someone or something moved a gate.

## 2. Load the live state (read, don't skim)

1. `TODO.md` — the task list, one item = one truth. The ⛔ section is blocked on Xavier.
2. `ROADMAP.md` — phase map with mechanical gates; "YOU ARE HERE" marker.
3. `git log --oneline -15` — anything after `v0.11.0-session-close` tag is post-close
   activity to triage.
4. Check for external deliveries since close: new files matching
   `briefs/STREAM1_*`, `briefs/STREAM2_*`, `DEEPTHINK*`, changes to `K3_CRITERIA.md`
   or `pipeline/siblings.py`.

## 3. Standing rules that bind every action (violating any fails review)

- **Triage every pasted brief before executing** (7 referenced-artifact incidents to date):
  use `pipeline/triage.py` — check named commits/files/constants exist, SHA256-vendor the
  source. Never implement one as written.
- **No `TEST`/`FIT` labels** (G1-L closed, mechanical). Real-data-touching exploratory work
  is `SANDBOX-EXPERIMENTAL` and needs explicit T0 authorization recorded in a
  `docs/*_T0_AUTHORIZATION_*.md` file (precedent: WP-E3, WP-E5).
- **`assert_resolvable()` before statistics** (`pipeline/resolvability.py`) — a sub-voxel
  deformation produces a degenerate pass, not a result (E2.16; three instances: WP-R3,
  WP-H, WP-E3).
- **Persist JSON before printing** — the JSON is the artifact; a printed summary has
  contradicted persisted data once already (WP-E3).
- **A test that cannot fail is not a test** (Stream 2 D-1) — every checker ships a
  negative control.
- **Never edit `PREDICTION.md`** — its pin hash covers the whole body; any edit closes G1.
  Ruling-1 variants (a)/(b) are documented in
  `docs/WP_E5_T0_RULING_IMPLEMENTATION_2026_07_26.md` §1 and await Xavier.
- **Never overwrite `docs/WP_E_EMPIRICAL_BOUNDS.md`** (T0-signed 3D artifact); the 2D
  deliverable is the `_2D_2026_07_26` file.
- **Audit agent output directly** — read the code/JSON, not the agent's summary. Session
  record: 3 real defects caught only by direct reads (false T0 footer; tautological-pass
  constants; degenerate-pass "window survives" verdict).

## 4. The exact next action (as of 2026-07-26 close)

**Audit the unaudited WP-E5 scripts, then run Phase 0.** The files
`pipeline/transverse.py`, `scripts/wpe_preflight_baseline.py`, `wpe_closure_tests.py`,
`wpe_transverse_sweep.py` were agent-built and committed WIP-UNAUDITED — tests pass but
nobody has read the σ/Δσ and zone logic against the spec. Audit per D-1, then:

```bash
python3 scripts/wpe_preflight_baseline.py          # Phase 0, both dz — the go/no-go
pytest pipeline/tests/ checkers/tests/ -q          # must stay green (371 at close)
```

Phase 0's persisted verdict (`data/derived/wp_e5_preflight_2026_07_26.json`) gates
everything else. **A NO-GO is a deliverable** (F5 honest negative), not a failure — brief
Stream 2 either way.

## 5. Delegation pattern

Mechanical builds go to Haiku agents (`Agent` tool, `model: haiku`) with tight specs that
include the hard rules above verbatim; the orchestrator audits output directly before
commit. Fable/Opus time is for rulings, audits, cross-stream briefs, and anything
touching gates or pinned documents.
