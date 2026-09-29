# Stream 3 — ACTIVATION, 2026-09-29 (read this first, then `TODO.md`)

**From:** Stream 2, on T0's instruction ("go for stream 3 work activation", in session 2026-09-29) ·
**Delivered untracked** (a Stream 2 session does not commit in this repo) · **Ruling record:**
K3-DarkMatter `briefs/T0_DECISIONS_2026_09_29_STREAM2_DELEGATED.md` (D14′–D18′; D17′ is this restart).

This file is the ordered work list for the next Stream 3 session. Every artifact it names was verified to
exist, with its sha256, at the time of writing (standing rule 4: verify a directive's artifacts before
executing it — six phantom-artifact occurrences to date; do the verification again yourself).

## State of this repo as found (2026-09-29)

- Last commit `7797028` (2026-09-21). `TODO.md` last updated 2026-07-27.
- Four untracked deliveries have been waiting unread:
  `briefs/STREAM2_TO_STREAM3_FABLE_REVIEW_DIRECTIONS_2026_09_27.md`,
  `briefs/STREAM2_TO_STREAM3_NOTICE_PR55_MERGED_2026_09_27.md` (§1–§9; §9 is today's),
  `briefs/DUALSCALE_TO_STREAMS_DECISIONS_2026_09_28.md`, and this file.
- `K3_CRITERIA.md` here: `2b6bae44f08aaf7e4d06488ae3093b0bb84c1f3f46891e78b8e6b1c0c81c4dfb` — older than every
  re-pin target sent since 2026-09-21. Current canonical (K3-DarkMatter, after today's §5 regeneration):
  `bcafe8025d6752d11624d72d0e548ab6f1dc7924bfd5b3b4dbae61fdfd829643` — **recompute at your own merge**;
  the PR carrying it is open at the time of writing (branch `stream2/status-table-renderer-2026-09-27`).
- `data/mirrors/stream2/` holds 2 of the 12 files owed (both current): `CM_POINTS_RHO20.json`
  (`1ef6d622…`), `A2_MEMBERSHIP.json` (`2aa105ea…`). Missing: the ten below.

## W0 — orient (10 min)

`bash scripts/session_orientation.sh`; `git status` (the untracked briefs are the inbox); read
`STREAM2_TO_STREAM3_NOTICE_PR55_MERGED_2026_09_27.md` §5, §7, §9 and
`DUALSCALE_TO_STREAMS_DECISIONS_2026_09_28.md` (their D1/D2: no level chosen, modular potential gated —
nothing there moves a gate here). Load the `epistemic-guardrails` and `prereg-pipeline` skills.

## W1 — file the inbox (one commit, your authorship)

Commit the four untracked briefs the way `7797028` filed the 2026-09-21 deliveries. Add a dated line to
`TODO.md` §"inbox" (or create it) listing them. Do not edit their content.

## W2 — re-pin and re-mirror (one commit; every hash recomputed by you at that commit)

| file (K3-DarkMatter `data/certificates/` unless noted) | sha256 (first 16) at 2026-09-29 | status here |
|---|---|---|
| `K3_CRITERIA.md` (repo root) | `bcafe8025d6752d1` | re-pin |
| `CM_POINTS_RHO20.json` | `1ef6d622af22a648` | present, current |
| `A2_MEMBERSHIP.json` | `2aa105eae60ebd5e` | present, current |
| `CM_POINTS_RHO20_LATTICE_TIER.json` | `882a866c0a01e718` | missing |
| `CM_COMPLETENESS.json` | `c9749d68a1d06d62` | missing |
| `C2_cooper_s7_v6.json` | `789fec2ac3d7fd3c` | missing |
| `C2_cooper_s10_v5.json` (LIVE today, D15′) | `bc1f1ebc76dfedd2` | missing |
| `CERTIFIED_MONODROMY_L2_cooper_s7.json` | `69626f35d45d1ecf` | missing |
| `CERTIFIED_MONODROMY_L2_cooper_s10.json` (re-emitted today against v5) | `d811432f513e98b2` | missing |
| `C6_SELECTOR_COMPARISON.json` | `92e05bf175688692` | missing |
| `C6_SELECTED_CANDIDATE.json` | `8ef469c152febbd9` | missing |
| `INOSE_MODEL_M7.json` | `96abd41a9cd36ed2` | missing |
| `INOSE_FIBRATION_MULTIPLICITIES.json` | `e75d3ff3633443a9` | missing |

Update `data/mirrors/stream2/MIRROR_MANIFEST.json` from the files, not from this table. A mirrored
certificate that still says `LATTICE_CERT_DRAFT` for s10 is *dated, not wrong* — see the D15′ brief's
stale-flag list; do not "fix" it locally.

## W3 — what changed in the rulings, in one paragraph each (for your own prose)

- **D14′:** no Kodaira labels for the explicit Inose/CDLW model either (K3 ledger item 10). Orders may be
  reported; fibre types may not appear in any document, including yours.
- **D15′:** `C2_cooper_s10_v5.json` LIVE, value-identical to the 2026-08-01 draft. The ADVISORY label is
  lifted on that ground only. Still: no ranking of s7 over s10; "this lattice is T" stays Tier B; no
  physical reading; no CM point maps to an observable.
- **D16′:** K3-DarkMatter CI was red on every run since #65 (root causes fixed today); "CI green is a
  release gate" is now K3 standing rule 6. Consider adopting the same rule here (`pipeline/tests/` is
  already merge-blocking).
- **D18′:** LeanMaster is closed for K3-DarkMatter; its MCP server (`mcp__leanmaster__*`) stays available
  to you.

## W4 — the laboratory approach (D12′, unchanged; this is the work)

In order, all under the pin protocol (K3 ledger item 5), all synthetic/model-level until `PREDICTION.md`
carries `PINNED:` (your rule 1):

1. **E1 — Aubry–André calibration arm.** Build `checkers/check_aubry_andre_selfduality.py`: hopping J,
   quasiperiodic potential λ on N sites; verify the exact duality λ ↦ 4J²/λ (dual spectrum E′ = (2J/λ)E; at
   λ = 2J every eigenstate has IPR_x = IPR_k). **Negative control before the positive run:** a random
   potential of matched strength must break both identities; if it does not, the checker is not a test.
   Exact where possible; report `PASS(N)`. This is a model check, not a measurement, and makes no K3 claim.
2. **E2 — pre-register the SIT noise duality before touching any dataset.** Draft `PREDICTION.md` v2
   amendment: statement (shot noise at g equals voltage/phase-slip noise at the dual g′ divided by R_Q²,
   R_Q = h/(2e)²; Fano factors 2e ↔ h/2e), named public datasets, decision rule and thresholds, disclosed
   prior knowledge (the 2016 mean-level reflection; the 2022 dual Shapiro steps), Arm V / Arm P / Arm 0,
   kill rule (Arm P reflecting as well as Arm V kills the symmetry claim). Freeze under a git tag; only then
   fetch data via `scripts/fetch_data.py`. Labels exclusion/FIT, never TEST, until T0 pins.
3. **E3/E4** stay as designed appendices until E1 and E2 exist.
4. **Guardrail in every sentence:** the K3 surface is the mathematical shadow of the duality, not the target;
   no laboratory result is evidence for cooper_s7/s10 or any Tier A/B certificate; any sentence linking
   σ = i or σ = (1+i)/2 to ⟨2⟩⊕⟨2⟩ carries a Tier C marker in the same sentence — the LIVE s10 lattice
   certificate does not change this.

## W5 — report back

One brief in K3-DarkMatter `briefs/` (`STREAM3_TO_STREAM2_…`) or a message to the Stream 2 session if one
is live, with: the two commit hashes (W1, W2), the recomputed `K3_CRITERIA.md` hash, and E1's `PASS(N)`
line with its negative-control line beside it. Anything that needs a ruling goes to T0 as a brief, not as a
question in prose.

## Not in scope, by rule

Any level choice (DualScale D2), any observable, any dark-sector sentence, any Kodaira label, any ranking of
the two families, anything from the AutoEvolve-R2/DarkMatterK3@Home sandbox (K3 ledger item 7).

Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: paths and sha256 listed above, computed 2026-09-29 | Reviewed-by: N
