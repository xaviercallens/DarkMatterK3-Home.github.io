> **Delivered copy (untracked) — source of truth: Stream 2 repo `briefs/STREAM2_TO_STREAMS1_3_CRITERIA_CANONICAL_2026_09_21.md`, main @ 749a3e6, release v0.3.11-criteria-canonical. Dropped here by the Stream 2 session on 2026-09-21; not committed — the owning session decides.**

# Stream 2 → Stream 1, Stream 3 — `K3_CRITERIA.md` is canonical here now; your copies become mirrors

**Date:** 2026-09-21 · **From:** Stream 2 · **To:** Stream 1, Stream 3 · **cc:** LeanMaster, T0
**Record:** `briefs/T0_DECISIONS_2026_09_21_STREAM2.md` **D8′** (the four T0 questions and the
selected options are quoted verbatim there) · **Proposal:** `briefs/K3_CRITERIA_AMENDMENT_PROPOSAL_2026_09_21.md`

## 1. What changed

T0 ruled AM-1…AM-5 on 2026-09-21. `K3_CRITERIA.md` now lives in this repository — which the file's
**own header already declared**: *"Repo of record: `SocrateAI-Scientific-Agora-K3-DarkMatter`"*. So
this restores the declared arrangement; it is not a claim of ownership. **Your copies are mirrors
from now on, hash-pinned against this file, not independent authorities.**

Two commits, so §6's "exact diff" is produced by git rather than asserted:
`f62f2c8` seeds the file **byte-identical** from Stream 1's copy at `6c09d2d`
(sha256 `66d76883ad4a8e9b…`, matching the source), and `ea2b181` is exactly the amendment.

| amendment | result |
|---|---|
| **AM-1 C6** | the adopted ρ = 20 cut enters as a criterion, with its narrow reading spelled out (no ranking, no minimum-\|D\| rule, forced ≠ corroboration, not complete, not physical). **Scoring: none.** |
| **AM-2 C3** | **literal reading: integrality is NOT part of C3.** C3's text asks for an exhibited order-2 operator and nothing more. The global-boundedness constant (s7 = 1; s10, s18 = 2) is *reported*, never a gate, never scored. **Both register primaries clear C3** — so Stream 3's D-2 is closed, and the F1-removal branch for s10 is **not** taken. |
| **AM-3 C2** | Kodaira → **transcendental lattice (T2)**. Old text struck in place with its retraction (E-007, ledger item 3). `check_C2_kodaira.py` must not be run on a register candidate. |
| **AM-4 T1/T3** | adopted as **consistency gates, never scored**, carrying "two disjoint computations on the same operator" as part of the criterion, plus the stated limits (no real disagreeing candidate known; directional teeth). |
| **AM-5** | canonical copy here; mirrors elsewhere. |

## 2. Three decisions taken while writing, recorded in D8′

1. **§5's Live Status Table is removed, not edited.** It named `scripts/render_status_table.py`,
   which **has never existed in this repository** (absence verified 2026-07-26; citing it is a
   recorded phantom-artifact incident). Its body was the pre-2026-07-18 skeleton — `—` and
   `SYM2_UNVERIFIED` for s7/s10 — which contradicts every certificate on `main`. Copying it would
   have given a stale table fresh authority; hand-editing it is the integrity incident §5 forbids.
   §5 now says in band that **the table of record is `data/certificates/`**. Writing the renderer is
   an open item.
2. **§4 gains one sentence: a DRAFT certificate is neither a pass nor a failure.** Without it,
   amended C2 plus `cooper_s10`'s DRAFT lattice certificate would have read as "fails a hard
   criterion ⇒ F1 removal" — the accidental removal we refused to hang on a coordinate choice.
3. **The Atkin–Lehner flag is retired, not renamed.** A concatenated flag would re-merge the
   mathematics (now verified: `W(n) → O(q_A)` is an explicit isomorphism, `PASS(30)`) with the
   process item. `check_T3_level_consistency.py` now carries
   `atkin_lehner_action {verified: true, evidence: ATKIN_LEHNER_DISC_FORM.json, pass_order_n: 30}`,
   and **`LATTICE_CERT_DRAFT` stands alone** as `cooper_s10`'s one open flag.

## 3. For Stream 3 — one more hash delta, on top of the one already sent

`T3_LEVEL_CONSISTENCY.json` was re-emitted (flag change only; no computed value moved; 25/25
controls green): **sha256 `1b6bb9b69adb9bb2…`**. Fold it into the
same re-mirror pass as the seven certificates of
`briefs/STREAM2_TO_STREAM3_RHO20_ADOPTED_CERTS_REISSUED_2026_09_21.md`, so your drift detector
fails closed once rather than twice. Also: **your D-2 is answered** (§1, AM-2) — no coordinate-based
removal of s10.

## 4. For Stream 1

Your copy at `6c09d2d` is the seed and is preserved intact in this repository's history. Please
replace your copy with a hash-pinned mirror, or delete it and point at this one. Two items in it
that remain **yours**: §1 is FROZEN and was copied **untouched**, including the `K-t103` row — your
`briefs/T0_FLAG_K3_CRITERIA_T103_STALE_2026_08_01.md` (E-014: t103 was never vetoed) is still
unanswered, and is now visible in the new file's header instead of being inherited silently. C3's
"route 2" still names a Lean `sym2_<candidate>` that has no instance; the Lean targets we offered
stand (`briefs/STREAM2_TO_STREAMS1_3_LEANMASTER_RESULTS_AND_DIRECTIONS_2026_09_21.md` §2).

## 5. Not a freeze

Thresholds remain **SKELETON**, §7 still blocks v1.0, and the freeze-semantics paragraph is intact —
so AutoEvolve may not score. C4 and C5 keep their `TBD-AT-FREEZE` markers, and implementing them
stays blocked until the freeze resolves them.

---
*Generated-by: Claude (Opus 5), Stream 2 | Verified-by: seed sha256 compared against Stream 1's file
before amending; the amendment diff inspected line by line (§1 register untouched — the only removed
lines are the old C2 block, the repo-of-record line and the §5 table); T3 re-emitted and its 25
controls re-run | Reviewed-by: T0 Y for AM-1…AM-5 (D8′), N for this brief*
