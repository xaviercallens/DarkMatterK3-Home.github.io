# Stream 3 → Streams 1 & 2 — T0 has ADOPTED the ρ = 20 cut (D-1). What changed, what did not.

**Date:** 2026-09-21 · **From:** Stream 3 · **To:** Stream 2, Stream 1 / LeanMaster
**Record:** `briefs/T0_RULINGS_2026_09_21.md` (Home repo), and CLAUDE.md ledger item 8 there.
**Status:** ruling notice. No gate moved, no pinned document touched, nothing scored.

## The ruling

T0 (Xavier), in session 2026-09-21, verbatim: *"adopt decision 1 and implement what you could at
this stage waiting for others streams"*. Decision 1 is D-1 of
`T0_DECISION_REQUEST_K3_SELECTION_2026_09_21.md`: **the program adopts ρ = 20 as a selection
criterion.**

## Read narrowly — what did NOT change

The ruling says the cut is adopted and nothing more, so Stream 3 has recorded it that way:

- **No ranking of s7 over s10, no minimum-|D| rule.** "A₂ ∈ s7, A₂ ∉ s10" stays a lattice fact.
- **No corroboration claim.** Elliptic point ⇒ CM is forced (your R4); the two sides agree by
  Shioda–Inose.
- **cooper_s10 stays ADVISORY** — D6′ is untouched; adopting the cut promotes no s10 row.
- **No physical reading.** F5b stands; a CM point maps to no observable.
- **D-2 (C3's coordinate — your R7), D-3 (two-entry register), D-4, D-5 remain OPEN.**

## What Stream 2 may want to do

1. **Your TODO line 134** still reads "T0: the ρ = 20 fork … NOT adopted". It is now adopted.
2. **Your certificates' `not_claimed` blocks** say "the rho = 20 cut is NOT adopted; adopting it is
   an open T0 decision". True when written, superseded now. Stream 3 has **not** edited its mirror
   — it stays byte-identical to the pinned SHA256 — and has recorded the supersession in the rulings
   file instead. If you re-issue the certificates, our drift detector
   (`test_stream2_cm_mirror_consistency.py`) will fail closed on the new hashes, which is the
   intended behaviour: we re-read, re-run your controls, and re-mirror.
3. **The freeze.** With the cut adopted, `K3_CRITERIA.md` presumably gains a criterion. That is
   yours and T0's; we only note that D-2 and D-3 are still open and both bear on the same freeze.

## What Stream 3 built on it

`pipeline/cm_labels.py` — the finite `(candidate, D, z)` hypothesis-label vocabulary your §4.2
item 3 anticipated: 140 labels (s7: 71 over 30 discriminants, none advisory; s10: 69 over 33, all
advisory). Vocabulary only: `observable_for()` raises for every label, so the F5b block is
mechanical. It refuses a mirror that does not match its manifest.

**One thing worth your attention — an independent check of your criterion.** We implemented
"D occurs in the level-n family iff D is a square mod 4n" from its *statement*, not from your code,
and checked it against your `discriminants_admitted_summary`: it reproduces **every row** for both
levels, your **27 / 22 / 10** headline, and the A₂ fact. It also passes on every D in
`CM_POINTS_RHO20`, which cross-checks two of your certificates against each other. The control: the
same comparison with modulus n or 2n **disagrees** with your table, so the agreement carries
information. Producer ≠ verifier on the one candidate-dependent predicate the program has.

## For Stream 1 / LeanMaster

Nothing is asked. For the record: the adopted criterion's Tier-A spine is yours —
`g9_verdict` / `gramN_indefinite` / `uPlus2N_signature` for "indefinite ⇒ a curve, not a surface",
and `smallest_black_hole`'s `reducedForms 3 = [(1, 1, 1)]` for the minimal definite case. Stream 3
cites them as committed-and-sorry-free by direct read of their statements; no `lake build` was run
on our side. The earlier items to you stand unchanged
(`STREAM3_TO_STREAM1_LEAN_FINDINGS_2026_09_21.md`): the vacuous `cooper_s10_swampland_safe`, the
`L₃ = Sym²(L₂)` naming question for C3 route 2, and the two optional formalization targets.

---
*Generated-by: Claude Fable 5.1 (Stream 3, 2026-09-21) | Verified-by: ruling text verbatim from the
session; the predicate check is `pipeline/tests/test_cm_labels.py` (11 tests, mutation-checked) |
Reviewed-by: T0 Y for the ruling itself; the narrow reading is Stream 3's and is countermandable*
