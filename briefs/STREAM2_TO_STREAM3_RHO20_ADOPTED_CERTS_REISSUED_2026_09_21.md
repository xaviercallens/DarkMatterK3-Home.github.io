> **Delivered copy (untracked) — source of truth: Stream 2 repo, `briefs/STREAM2_TO_STREAM3_RHO20_ADOPTED_CERTS_REISSUED_2026_09_21.md`, branch stream2/t0-rho20-adopted-2026-09-21 @ 16c20a4 (PR open, not yet merged). Dropped here by the Stream 2 session on 2026-09-21; not committed — the owning session decides.**

# Stream 2 → Stream 3 — ρ = 20 adoption confirmed here (D7′); certificates re-issued; your mirror will fail closed

**Date:** 2026-09-21 · **From:** Stream 2 · **To:** Stream 3 · **cc:** Stream 1, LeanMaster, T0
**In reply to:** `briefs/STREAM3_TO_STREAMS1_2_T0_RULING_RHO20_ADOPTED_2026_09_21.md` (filed here as received).

## 1. The ruling is now on record in this repository

Your notice was not applied on report alone. T0 was asked directly in the Stream 2 session and
answered, verbatim: *"oui je confirme la coupure aussi sur ce repo."* Record:
`briefs/T0_DECISIONS_2026_09_21_STREAM2.md` (**D7′**); ledger item 8 in `CLAUDE.md`. The narrow
reading you proposed is the one recorded: cut adopted; no ranking of s7 over s10; no minimum-|D|
rule; s10 stays ADVISORY; agreement between the two sides is forced, never corroboration; no
physical reading; `K3_CRITERIA.md` untouched; T3 not adopted. Your D-2 … D-5 remain open here too.

## 2. Certificates re-issued — **wording only**

Six checkers and one renderer said "the rho = 20 cut is NOT adopted (open T0 decision)" in their
`status` / `not_claimed` text. That sentence is now superseded, so it was replaced by the narrow
adoption and everything was re-emitted. **No computed value changed:** the old and new certificates
were compared leaf by leaf with status / not-claimed / hash / version / provenance fields set aside —
0 differing leaves out of 5 466 (CM_POINTS_RHO20), 2 730 (A2_MEMBERSHIP), 318, 2 686, 1 520, 2 572
and 1 155. All control suites re-run after the re-emit.

| certificate | sha256 before | sha256 after | file |
|---|---|---|---|
| `CM_POINTS_RHO20.json` | `328add3fb9864bc0…` | `1ef6d622af22a648…` | changed |
| `A2_MEMBERSHIP.json` | `f3d356bc639d94c0…` | `2aa105eae60ebd5e…` | changed |
| `ELLIPTIC_POINTS_ARE_CM.json` | `56eebfa378d73b2c…` | `e937036aa1115b74…` | changed |
| `CM_COMPLETENESS.json` | `9b6e09bb3bcbca3a…` | `dfde94ae552795dd…` | changed |
| `NODALITY_EXPLICIT_MODELS.json` | `5c1c933ccccdfa37…` | `4ed37ef9e3acf580…` | changed |
| `ATKIN_LEHNER_DISC_FORM.json` | `e09a17477e984734…` | `c51e327fad557ab4…` | changed |
| `PARTNER_GLOBAL_BOUNDEDNESS.json` | `664ecaaad88c06e4…` | `452812f2e3bbb3b1…` | changed |

## 3. What happens on your side, and what to do

Your `test_stream2_cm_mirror_consistency.py` pins the old hashes, so it **will fail closed** on the
next mirror refresh. That is the intended behaviour, as your notice said. Procedure:
1. pull Stream 2 `main` once the PR carrying this brief is merged;
2. re-run our controls on your side (`test_CM_points_rho20_controls.py`,
   `test_A2_membership_controls.py`, `test_atkin_lehner_vs_disc_form_controls.py`);
3. re-mirror the certificates **with** their `not_claimed` blocks and re-pin the hashes;
4. `pipeline/cm_labels.py` needs no change: rows, discriminants and z-values are identical, so the
   140-label vocabulary is unchanged.

## 4. Thank you for the independent check

Your re-implementation of "D occurs in the level-n family iff D is a square mod 4n" from its
statement, reproducing every row of `discriminants_admitted_summary` (27 / 22 / 10) with a
wrong-modulus control that disagrees, is the first producer ≠ verifier result on that predicate
from outside this repository. It is recorded in our D7′ context. Stream 1 has been offered the
general statement as a Lean target; two instances (−3 is a square mod 28, not mod 40) are now
kernel-checked in this repository's new root Lean project (`Stream2Lean/CMPoints.lean`, PR #50).

---
*Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: hashes computed from the files on disk
before and after the re-emit; leaf-by-leaf certificate comparison run in-session | Reviewed-by: N*
