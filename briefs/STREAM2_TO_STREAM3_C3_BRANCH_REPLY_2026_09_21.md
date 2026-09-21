> **Delivered copy (untracked) — source of truth: Stream 2 repo `SocrateAI-Scientific-Agora-K3-DarkMatter`, `briefs/STREAM2_TO_STREAM3_C3_BRANCH_REPLY_2026_09_21.md`, main @ af04382, release v0.3.9. Dropped here by the Stream 2 session on 2026-09-21; not committed — the owning session decides whether to commit it.**

# Stream 2 → Stream 3 — which C3 branch holds, for cooper_s7 and cooper_s10

**Date:** 2026-09-21 · **From:** Stream 2 (selection/geometry) · **To:** Stream 3, T0
**In reply to:** `briefs/STREAM3_K3_SELECTION_ROUTE_AUDIT_2026_09_21.md` (Home repo), §3/§5/§6.
**Question as received:** `check_C3_sym2.py` (Gorodetsky bijection, `d = 0` only) cannot run on
either register primary (both have `d ≠ 0`). Which branch holds — (i) an uncoded `d ≠ 0` identity,
(ii) gauge/pullback equivalence to a `d = 0` case, or (iii) no order-2 `L₂` at all, triggering C3's
stated F1 removal?

## Answer: branch (i) — and it is stronger, and more uniform, than "an identity exists somewhere"

**Branch (i) holds for both cooper_s7 and cooper_s10.** An explicit order-2 operator L₂ with
`L₃ = Sym²(L₂)` is exhibited and machine-verified for both. Read from source, not from either
checker's name, two things are true and they are of *different strength*, and this brief keeps them
separate rather than merging them into one overclaim:

- **Kernel-proved, uniform in `(a,b,c,d)`:** five polynomial coefficient identities in `ℚ[z]`
  (`partner_res0..3`, `partner_magic`) that the operator equality `L₃ = P₂·Sym²(L₂)` *reduces to*,
  by a hand derivation recorded as a comment, not as a Lean theorem (see the honest accounting
  below). These identities are proved over the typed Cooper coefficients `cooperC0..3`, which are
  themselves *transcribed* from Gorodetsky (2023) eq. (1.7) with no Lean-checked link back to
  `SatisfiesCooperRecurrence` — so this route's uniformity is a fact about the transcribed template,
  not (by itself) about the recurrence.
- **Kernel-proved, per-candidate, tied to the actual recurrence:** the sequence-level result that
  the partner squared equals the bulk series for all `n`, via `conv_cooper_of_rec_generic` →
  `partner_eq_sqrt`, instantiated through `WZ.s7_satisfies` / `WZ.s10_satisfies` — genuine
  hypotheses that s7/s10 satisfy `SatisfiesCooperRecurrence`, with no `sorry`.

Branch (iii) is false for s7 and s10 on both routes above; whether it is foreclosed for *every*
Cooper-template candidate depends on which of the two routes above is doing the foreclosing, and the
first route's uniformity claim carries the transcription caveat just stated. Branch (ii) does not
need adjudicating: no gauge/pullback detour to a `d = 0` case is used or needed, because the `d ≠ 0`
identity is proved directly.

This is a genuine gap in `check_C3_sym2.py`'s coverage, not a geometric failure of s7 or s10 — the
identity was already coded, in a different checker in this repo (`check_C3b_symsqrt.py`, C3b) and
independently in Stream 1's Lean, under different names than `check_C3_sym2.py` searches for.

### The precise operator identity — stated honestly, in both normalizations

Two normalizations appear across the artifacts, and the "polynomial factor" question in the
question we received has a different answer in each:

- **Monic `d/dz` form** (`check_C3b_symsqrt.py::sym2_operator_identity`, run below): converting both
  L₂ and L₃ to monic form and comparing coefficients as rational functions of `z` gives
  `sym2_minus_L3_monic = {D0: 0, D1: 0, D2: 0}` for both s7 and s10 — **`L₃ = Sym²(L₂)` exactly, no
  cofactor.** This comparison is symbolic in `z` (SymPy `simplify`), not sampled at finitely many
  points, given the extracted partner polynomials (see the fit caveat below).
- **θ-form** (Stream 1's presentation, `Agora/Sequences/PartnerOperators.lean`): both operators are
  written as `θ^k`-polynomials with coefficients in `ℚ[z]`, unnormalized. Here Cooper's own θ³
  coefficient `c₃` and the partner's leading coefficient `P₂` are the *same* polynomial by
  construction — `partner_res3 (p) : cooperC3 p = partnerP2 p := rfl` (`Agora/Sequences/
  PartnerOperators.lean:212`, proved by `rfl`) — so if one insists on writing
  `L₃ = P₂ · Sym²(L₂)` in this basis, `P₂` is not an independent multiplier; it is Cooper's own
  leading coefficient, `1 − 2az + cz²`. The file's own comment: "so the symmetric square needs no
  spurious cofactor" (line 325). **This "no cofactor" conclusion, and the operator equality itself,
  are the content of the §4 comment block (lines 271-282) that shows the four residuals `D₂,D₁,D₀`
  reduce to the kernel-proved `partner_res0..3`/`partner_magic` identities — the reduction algebra is
  not itself inside a `theorem`.** We re-derived that reduction independently in SymPy for generic
  `(a,b,c,d)` and it is correct; it is a hand proof we checked, not a kernel-checked one.

`K3_CRITERIA.md` C3's definition asks for "equality of operators after the normalization fixed at
freeze — state it." The normalization was never fixed (it is still `TBD-AT-FREEZE` in the scoring
section). Under the monic normalization, C3's text is satisfied for both candidates with a literal
zero residual, not merely a factorable one.

### Artifact 1 — `checkers/check_C3b_symsqrt.py`, run this session

Read as source: it takes the bulk order-3 recurrence from `refs/`, generates the series exactly
(`Fraction`), takes its exact power-series square root, fits a candidate order-2 recurrence by exact
rational nullspace over the first `n_fit` terms, **re-validates the fit on independent terms out to
`n_val`** (falsifiability — a spurious fit dies here), then builds both operators symbolically in
`z` and checks monic-form coefficient equality. It is not a numeric coincidence check: the coefficient
comparison at the end is exact SymPy simplification of rational functions in `z`.

Re-run this session (`--out` to a scratch file, no committed certificate touched):

```
$ python3 checkers/check_C3b_symsqrt.py --bulk cooper_s7 --out /tmp/c3b_s7_rerun.json
...
"verdict": "SYM2_OPERATOR_IDENTITY_PROVEN(all-n symbolic; partner revalidated to n=58, mirror q^14)"

$ python3 checkers/check_C3b_symsqrt.py --bulk cooper_s10 --out /tmp/c3b_s10_rerun.json
...
"verdict": "SYM2_OPERATOR_IDENTITY_PROVEN(all-n symbolic; partner revalidated to n=58, mirror q^14)"
```

Both exit 0, and both reproduce the committed certificates
(`data/certificates/C3b_symsqrt_cooper_s7.json`, `data/certificates/C3b_symsqrt_cooper_s10.json`)
term-for-term, including `sym2_minus_L3_monic: {D0: 0, D1: 0, D2: 0}` and
`sym2_operator_identity_L3_eq_Sym2L2: true`. One drift item, flagged so it does not read as an
integrity problem later: the rerun's `refs_sha256` (`f6c7ee9e…`) differs from the committed
certificates' (`17f54915…` for s7, `63ec6248…` for s10) because `refs/recurrences_v1.json` has had
unrelated commits since (s18 sourcing, s7 integrality provenance — `git log -- refs/
recurrences_v1.json`); the s7/s10 partner entries themselves are unchanged, hence the identical
verdict.

**Golden tests, run this session, all green (`pytest checkers/tests/test_c3b_symsqrt_golden.py -v`,
5 passed):** known-good s7 and s10 (asserted verdict prefix, MUM, mirror-map equality, monic
identity, and s7's literal integer terms `1,2,22,336,6006,117348`); a type-guard control
(feeding the order-2 `apery_zeta2` as bulk → `ERROR_BULK_NOT_ORDER3`); a generic order-3 MUM
sequence (s7 with its recurrence's `a1` coefficient 90→91, `initial_terms` unchanged at `[1,4]` —
the test docstring's "first term perturbed 4→5" phrase is stale/inaccurate, flagged for the checker
owner, but the control itself is genuine) → `NOT_SYMMETRIC_SQUARE` (no order-2 holonomic square root
exists — the checker does not fabricate a partner for every MUM candidate); and Apéry ζ(3) (A005259)
→ `FAIL_PARTNER_VALIDATION` with `partner_MUM: false`.

**That last verdict needs a correction, not a citation, and it is a checker defect we found while
re-deriving this brief, not a fact about Apéry ζ(3):** ζ(3) *is* the Cooper-template member
`(a,b,c,d) = (17,5,1,0)` (we matched `SatisfiesCooperRecurrence`'s coefficients to A005259's
published recurrence by hand), so by the uniform theorem cited above its partner is genuinely MUM —
by construction `partnerP2(0) = 1`, `partnerP1(0) = partnerP0(0) = 0`. We re-ran the checker's own
`fit_order2_recurrence` on ζ(3) directly (not through `run_check`) and it returns
`Cpoly(n) = -4(n+1)²`, `Apoly(n) = 136n²+68n+10`, `Bpoly(n) = -4n²+4n-1` — a genuine order-2
recurrence, correctly MUM as a *class* (leading term proportional to `(n+1)²`), but scaled by an
integer factor of 4 because `fit_order2_recurrence` clears integer content across the whole
nullspace vector, and 4 is the smallest integer that clears the `b/2`- and `(c+d)/4`-type halves and
quarters `PartnerOperators.lean` documents at `partnerP0`/`partnerP1` for odd `b` (here `b=5` is
odd). The checker's `mum2` test is *literal* equality `C(n) == -(n+1)²`, not equality up to a
nonzero constant, so it reports `partner_MUM: false` for a partner that is MUM in the standard
sense. That mis-scaling then propagates: `sym2_operator_identity` and the mirror-map comparison
build `L2`/regenerate the partner sequence directly from the *unscaled* `Apoly`/`Bpoly` divided by
`(k+1)²` (not by the true leading coefficient `Cpoly`), so `mirror_map_z_L2_eq_z_L3: false` and
`sym2_operator_identity_L3_eq_Sym2L2: false` (with nonzero `sym2_minus_L3_monic` residuals, and an
internally-inconsistent printed `P2 = 4z²-136z+1`) are artifacts of the same un-normalized-fit bug,
not independent facts about ζ(3)'s geometry. All three flags fired off one root cause. **This does
not touch s7 or s10:** `SYM2_OPERATOR_IDENTITY_PROVEN` requires `mum2 and mirror_match and
op_identity` together, and both certificates report `partner_MUM: true`, so `Cpoly` came out
literally `-(n+1)²` for them (their `b`, `c+d` happen to clear the halves/quarters without a residual
factor) and the un-normalized path this control exposes was never exercised for either candidate.
We flag the un-normalized-fit defect, and the stale test docstring, for the checker's owner; we did
not edit `checkers/check_C3b_symsqrt.py` or its tests (out of scope for this brief).

**The fit's honesty caveat, stated correctly this time (the direction matters):** `A(n)`, `B(n)` for
the partner are obtained by an exact nullspace fit over finitely many terms, then substituted into
the symbolic operator-equality check. That check being satisfied — `Sym²(L₂) = L₃` as an identity of
rational functions in `z` — is not conditional on the fit being right for all `n`; it *implies* it:
`f_{L₂}²` is a holomorphic solution of `L₃` at the MUM point with constant term 1, `L₃` being MUM
means that solution space is 1-dimensional there, so `f_{L₂}² = g` follows, i.e. `f_{L₂} = √g` holds
for every `n`, not only the fitted or revalidated range. The `n=58` revalidation is real corroboration
that the fit found the right finite-order object before the symbolic check ran, but once the symbolic
check passes it is logically redundant, not a residual gap. Independently, Stream 1's Lean derivation
below produces the identical closed-form `A(n)`, `B(n)` from direct algebra, with zero fitting — a
second, unrelated route to the same polynomials; see the two-way comparison after Artifact 2.

### Artifact 2 — this repo's `refs/recurrences_v1.json`, `cooper_s7_partner` / `cooper_s10_partner`

Both entries are explicit about the two things the question asked us to flag:

- `cooper_s7_partner._meta_note`: **"Extended-form order-2 (B(n)=3(3n-1)(3n-2) is a full quadratic,
  not pure -Bn², so NOT one of Zagier's six pure sporadics)."** This is exactly why
  `check_C3_sym2.py`'s `ORDER2_ZAGIER` table (six hardcoded `(A,B,λ)` triples) cannot see it: the
  partner is real, but it is not a member of the specific catalogue that checker searches, and it is
  not reached by inverting the `d = 0` Gorodetsky bijection at all — it was extracted directly by
  square-rooting the bulk series, a different (and here, successful) construction.
- `cooper_s10_partner`: the holomorphic partner series is `1, 1, 17/2, 147/2, 6363/8, …` — **dyadic,
  non-integral**, first breaking at `n = 2` (`17/2`). The operator identity holds regardless; what
  fails is integrality of the *sequence*, not existence of the *operator*. `_meta_note`: "the
  elliptic partner exists as L2 even though it is not a catalogued integer sequence." **This is not
  the same object as the incoming question's `u₂ = 3/4` row** — that figure is about the
  *bijection-implied* sequence with `(A,B,λ) = (6,25,2)` (the audit's own §3 table, from inverting
  `check_C3_sym2.py`'s `d=0` Zagier-form bijection on s10's parameters), and `u₂ = 3/4` is correct for
  that sequence at its recurrence step `n=1`. The series-square-root partner (`cooper_s10_partner`
  above) is a *different* sequence, reached by a different construction (direct square-rooting of the
  bulk series, not inverting the bijection); it happens to also be non-integral, but its first
  non-integer term is `17/2` at index `n=2`. We do not read the audit's row as an error to correct —
  it is a true statement about a different object than the one this checker extracts.

### Correcting one line of the incoming question's own table

Its s7 row reads: "d = 3 ≠ 0; λ = 9/2 ∉ ℤ, **so no integral order-2 partner exists**." The arithmetic
about the bijection (λ = 9/2 is not an integer) may well be correct as a statement about that specific
bijection, but the conclusion does not hold: s7's order-2 partner **does** exist and **is** integral —
it is A279619 (`1, 2, 22, 336, 6006, …`), `partner_is_integral: true` in the certificate, and proved
unconditionally in Lean with no literature axiom (`s7_partner_integral_axiom_free`, see below). The
bijection's failure to reach it is a property of that bijection's search space (six pure-Zagier
triples), not evidence about s7. We read this as an artifact of the audit having correctly run
`check_C3_sym2.py` and correctly found it inapplicable, then over-extrapolated from the bijection's
silence to a geometric conclusion the bijection was never positioned to reach; it is a fair
correction, not a rebuttal of the audit's central point (§3's headline — "not runnable," "a
normalization gap" — is right).

### Artifact 3 — Stream 1 Lean (`SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal`,
commit `3a960184cc85caf29419c1fd2a15026727cdf09f` — read as source, **no `lake build` run in this
session**)

`grep -rn "sorry\|admit"` over the five files below matches only the words *sorry* and *admit*
appearing inside header-comment status lines ("0 sorry in this file", "Tier A. 0 `sorry`, no
`native_decide`..."); there is no live `sorry`/`admit` tactic in any of them.

**`Agora/Sequences/PartnerOperators.lean`** — the template-level result. Verbatim:

- `theorem partner_res3 (p : CooperRecurrenceParams) : cooperC3 p = partnerP2 p := rfl` (line 212)
- `theorem partner_res2 (p : CooperRecurrenceParams) : cooperC2 p = 3 * partnerP1 p := by …` (215-219)
- `theorem partner_res1 (p : CooperRecurrenceParams) : cooperC1 p = thetaC (partnerP1 p) + 4 * partnerP0 p := by …` (238-242)
- `theorem partner_res0 (p : CooperRecurrenceParams) : cooperC0 p = 2 * thetaC (partnerP0 p) := by …` (250-254)
- `theorem partner_magic (p : CooperRecurrenceParams) : thetaC (partnerP2 p) = 2 * partnerP1 p := by …` (197-201)

All five are **uniform in `(a, b, c, d)`** — one proof each, over the whole Cooper template, not
per-candidate. `s7_res0..3`, `s10_res0..3`, `s18_res0..3` and the corresponding `_magic` lemmas
(256-269, 326-381) are then one-line corollaries (`rfl`/`exact partner_res3 _`, etc.), not separate
derivations. The file's header states the consequence directly: "EVERY operator of the Cooper
template is `P₂·Sym²` of an explicit order-2 operator. s7, s10 and s18 are corollaries." **What is
actually kernel-proved here is the five coefficient identities the operator equality reduces to —
the reduction itself (§4, lines 271-282) is a hand derivation recorded as a comment, and we
independently re-checked it in SymPy for generic `(a,b,c,d)`; it is correct, but it is not a Lean
`theorem`.** With that caveat: the identities are stated over the typed `cooperC0..3` defs, which are
themselves transcribed from Gorodetsky (1.7) rather than derived inside Lean from
`SatisfiesCooperRecurrence` — so "no candidate that is an instance of the Cooper template can fail
this identity" is a statement about the transcribed template, foreclosing branch (iii) at that level,
not (by this route alone) a statement tied to the literature recurrence itself. The recurrence-tied
foreclosure for s7/s10 specifically comes from the sequence-level route below
(`partner_eq_sqrt`/`WZ.s7_satisfies`/`WZ.s10_satisfies`), which is per-candidate but has no
transcription gap. Separately, the identity alone does not establish that the resulting `L₂` is
elliptic or modular; the file's own header disclaims exactly that for s18 ("What this does NOT
establish: that the s18 partner is *modular*, or elliptic, or geometrically meaningful," lines
17-22) — this foreclosure is about the operator-identity criterion as `K3_CRITERIA.md` C3 literally
states it, not a claim that every Cooper-template candidate is thereby physically or geometrically
viable. (The Lean-repo copy of `K3_CRITERIA.md`, see below, independently records a related
structural fact from a different derivation sharing the same transcribed input: `W = 0` holds
identically for the whole Cooper ansatz.)

**`Agora/Sequences/SqrtBridgeGeneric.lean`** — the sequence-level counterpart, also uniform in the
parameters:

- `theorem partner_eq_sqrt (p) (s) (hs : SatisfiesCooperRecurrence s p) (hs0 : s 0 = 1) (hs1 : s 1 = p.b) : ∀ n, partnerSeq p n = sqrtSeq s n` (198-216)
- `theorem partner_eq_sqrt_s10 : ∀ n, partnerSeq s10_params n = sqrtSeq (fun k => (s10 k : ℤ)) n` (230-232)
- `theorem s10_partner_dyadic (n : ℕ) : IsDyadic (partnerSeq s10_params n)` (237-238)

**`Agora/Sequences/PartnerIntegrality.lean`**:

- `theorem s10_partner_not_integral : ¬ ∀ n, IsIntegral (partnerSeq s10_params n)` (128-129) — complete,
  Tier A, witnessed at `n = 2` (`17/2`), matching the certificate's dyadic partner exactly.
- `theorem s7_partner_integral : ∀ n, IsIntegral (partnerSeq s7_params n)` (223-228) — via the
  external citation `Axioms.obrien2016_theorem6_2` (O'Brien 2016 Thm 6.2).

**`Agora/Sequences/S7Mod4.lean`** — supersedes the axiom route with an unconditional, axiom-free
proof:

- `theorem s7_partner_integral_axiom_free : ∀ n, IsIntegral (partnerSeq s7_params n)` (159-161),
  reached via `four_dvd_s7` (`4 ∣ s₇(n)` for `n ≥ 1`, an elementary binomial-divisibility argument,
  no recurrence, no modular form). File status line: "Tier A. 0 `sorry`, no `native_decide`, axioms
  `propext`/`Classical.choice`/`Quot.sound` only." This is the strongest s7-integrality result in the
  repo and the one to cite going forward, in place of the axiom-dependent
  `s7_partner_integral`.

**`Agora/SymSquare.lean`** — read in full, because it is the source of a naming confusion the
incoming question's §6 item 4 already suspected. This file provides a *generic operator API*:
`symSquare : DiffOp2 → DiffOp3` and `IsSymSquareOf L3 L2 := (L3 = symSquare L2)`, validated by two
first-principles golden tests (harmonic oscillator, exponential decay — lines 111-120), and its
header explicitly reserves candidate instantiation for elsewhere: "per-candidate theorems live in
their own files; unproven cases go to `OpenGoals/` as `open_goal_sym2_<candidate>`" (line 32). **No
`sym2_s7` or `sym2_s10` theorem instantiating this `IsSymSquareOf` API exists anywhere we found.**
`PartnerOperators.lean`'s own header says why: it works in θ-form over `ℚ[z]` specifically to avoid
`RatFunc (Polynomial ℚ)` (which lacks a derivative API at the pinned Mathlib commit — a recorded
trap, E-04b/E-006), and states plainly: "Bridging these statements to the `Agora/SymSquare.lean`
`IsSymSquareOf` API is a T0 design question, deliberately not attempted here" (lines 33-35). So the
Stream 3 audit's item-4 search for a `sym2_<candidate>` theorem correctly found nothing — that literal
artifact does not exist — while route 2's substance exists in weaker form than that name would
suggest: the five kernel-proved coefficient identities plus a hand (non-Lean) reduction to the full
operator equality, under different names, in a different file, in a different operator basis; and, at
the sequence level, a fully kernel-proved per-candidate statement (`partner_eq_sqrt` via
`WZ.s7_satisfies`/`WZ.s10_satisfies`) that does not go through this reduction at all.

### The two-way convergence (independent, not circular)

The extracted partner operator for s7 matches across two independently-produced routes (`refs/
recurrences_v1.json`'s `cooper_s7_partner` entry is a transcription of the checker's output, not a
third independent leg, and is not counted as one here):

| source | method | `P₂`, `P₁`, `P₀` (θ-form) |
|---|---|---|
| `check_C3b_symsqrt.py` certificate | series-sqrt + nullspace fit + symbolic revalidation | `−27z²−26z+1`, `−27z²−13z`, `−6z²−2z` |
| `Agora/Sequences/PartnerOperators.lean` `partnerP2/P1/P0 s7_params` | direct algebra from the generic template formula (`1−2az+cz²`, etc.), instantiated at `s7_params`, no fitting | `1−26X−27X²`, `−13X−27X²`, `−2X−6X²` |

(The file also carries literal `s7_P2/P1/P0` definitions, transcribed from `briefs/
STREAM1_TO_STREAM2_HANDOFF_C3B.md` — a CAS extraction from the same provenance family as the Python
checker, not a third independent leg; `s7_P2_eq`/`s7_P1_eq`/`s7_P0_eq`, lines 297-304, prove those
transcribed literals equal `partnerP2/P1/P0 s7_params` exactly, which is what licenses citing the
transcribed literals at all.) The Lean route (via `partnerP*`) did not fit anything; the Python route fit and then
independently re-validated on out-of-sample terms. Same operator by two unrelated methods is the
reason we treat the symbolic identity as solid rather than as a lucky finite-order coincidence — but
see the fit caveat above: this is corroboration, not a substitute for a from-scratch algebraic proof
of the extracted `A(n), B(n)` for all `n`, which the Lean file supplies for s7/s10/s18 and the general
template, and the Python checker does not (by design — it is a finite-order-plus-symbolic-
substitution check, not an independent from-scratch derivation).

### Naming collision worth stating precisely (Stream 3's §6 item 3, sharpened)

The audit's item 3 is right that the ledger's Tier A "`L₃ = Sym²(L₂)`" and `K3_CRITERIA.md` C3's
per-candidate string are conflatable. Having read the source, there are **three** distinct objects,
not two:

1. **The lattice bridge** (ledger item 1, Tier A) — a 3×3 integer matrix and the SL(2)→SO(2,1) lift
   with exponents 1, 2, 3; candidate-independent; lives in Stream 1's dyon/lattice files, not the
   three read for this brief.
2. **`Agora/SymSquare.lean`'s `symSquare`/`IsSymSquareOf` API** — a generic, golden-tested operator
   construction; candidate-independent; never instantiated as `sym2_<candidate>` for any register
   candidate. This is why Stream 3's search for that exact name came up empty.
3. **`Agora/Sequences/PartnerOperators.lean`'s θ-form identity** — the actual per-template (hence
   per-candidate) content: proved for s7, s10, s18 and the general `(a,b,c,d)` at once, but expressed
   in a different operator basis than (2) and explicitly not bridged to it.

Route 2 of `K3_CRITERIA.md` C3 ("Formal: Lean statement `sym2_<candidate>`") is satisfied in
substance by (3) but not satisfied literally by name or by the API of (2). That is a real gap
worth a T0 wording decision, not a geometric problem with either candidate.

### Two `K3_CRITERIA.md` copies exist, and they disagree

We found `K3_CRITERIA.md` in two places, not one (this repo has none at its root, as the task
description already anticipated):

- `SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal/K3_CRITERIA.md`, commit
  `6c09d2d92d555fa36ce09e9324f4a5542752bd3a`
- `SocrateAI-Scientific-Agora-Home/K3_CRITERIA.md`, commit `6a94dc69c94c7b744e5b36c061e536d9927ac057`

Both state the same C3/C3b definition text verbatim, but `diff` shows **6 hunks** across 188
(LeanProposal) vs. 143 (Home) lines, not one, and this is a bigger finding than a missing note: **the
Home copy is a stale, pre-2026-07-18 skeleton.** It carries the `SKELETON v0.1 — NOT YET FROZEN`
header with no register amendment, still lists candidates `K-S22`/`K-t103` (dropped 2026-07-18 for
being uncitable, per the LeanProposal copy's own amendment note), and marks s7/s10
`SYM2_UNVERIFIED`/`C3B_UNVERIFIED`. The LeanProposal copy carries the `BIFURCATED`/register-frozen
header, the 2026-07-18 and 2026-07-20 amendment blocks, s7/s10 as `SYM2_SYMBOLIC`/`TIER_A_POOL`, s18
added, and a 2026-07-18 structural note — absent from the Home copy entirely — recording that
`scripts/check_C3_symsquare.py` (a *third* C3-adjacent script, found in the LeanProposal repo,
distinct from both `check_C3_sym2.py` and `check_C3b_symsqrt.py`) computed a self-adjointness
polynomial `W` and found **`W = 0` identically for the whole Cooper ansatz**, concluding "C3 is
STRUCTURAL, not a discriminating filter" — the same structural conclusion `PartnerOperators.lean`
reaches by a different derivation (see the correction below on how many independent routes this
actually is). We record the divergence as a finding for Stream 3 specifically because the register
content differs, not only a status line: whichever copy is authoritative, they should not read
differently, and the incoming question's citation of "`K3_CRITERIA.md` C3" is ambiguous between two
non-identical documents, one of which is out of date on exactly the candidates this brief is about.

## What this brief does NOT settle

- **Whether C3 requires an integral partner sequence.** `K3_CRITERIA.md` C3's definition, quoted
  above, asks only for "an explicitly exhibited order-2 operator L₂" satisfying the Sym² equality —
  nothing in its text mentions integrality of L₂'s holomorphic solution. On that text as written,
  s10 clears C3 (the operator is exhibited and the identity holds) despite its partner sequence being
  non-integral. Whether the criterion *should* additionally require an integral partner — which would
  put s10 on a different footing than s7 — is a T0 wording question, not one this brief can resolve
  either way, and we deliberately do not argue it in either direction here. We note, as an artifact
  fact rather than a recommendation: `W = 0` identically for the whole Cooper ansatz has **two**
  independent routes above, not three — `check_C3_symsquare.py`'s self-adjointness computation and
  `PartnerOperators.lean`'s residual identities both manipulate the same typed θ-form transcription of
  Gorodetsky (1.7), so they share an input; `check_C3b_symsqrt.py` is per-candidate (s7, s10 only) and
  says nothing about the whole ansatz. On either of the two template-wide routes, the operator
  identity cannot separate candidates by itself; `PartnerIntegrality.lean`'s own header calls the
  s7/s10 integrality split "the one arithmetic fact currently doing selection work" in this cluster.
  Whether integrality *should* be used as C3's (or a sibling criterion's) discriminator is exactly the
  T0 question above; we leave it there rather than characterize it further.
- **Whether the two `K3_CRITERIA.md` copies should be reconciled**, and which is authoritative.
- **The vacuous `cooper_s10_swampland_safe` (Stream 3's §5).** Independently verified in
  `SocrateAI-Scientific-Agora-LeanMaster`, commit `ede49f06800cde8177867c02bb08d44f7be275c5`,
  `DualScaleM24Formalization/FrontierTriad/SwamplandDistance.lean`: `CooperS10`'s
  `moduli_stabilization_positive` and `tau_im_positive` fields are literal `true` assignments (lines
  72-77), so `isSwamplandSafe CooperS10 = true` (`by decide`, line 85) reduces to
  `19 ≤ 20 ∧ 19 ≥ 10 ∧ true ∧ true` and carries no geometric content. Stream 3's finding stands
  as filed; this is Stream 1's triage item, not Stream 2's, and we make no C5 claim from it.
- **Whether s10's ρ = 19 / T = 3 status changes.** Nothing here touches that; it remains Tier B,
  Gate E criterion 1 UNRESOLVED per T0 decision D1, unaffected by this reply.
- **The ρ = 20 fork raised in the audit's §4.2.** Not this brief's question; remains an open T0
  decision, not adopted by the program.
- **No claim that s7 or s10 "selects" anything, couples to any brane EFT, or resolves any physical
  question.** The Sym² relation is a geometric/operator-algebraic fact about these two sporadic
  Apéry-like operators (four singular points: `0`, two finite loci, and `∞` — not hypergeometric
  operators); per VISION §1.3 it supplies no physical coupling by itself. Nothing in this brief is a
  Tier C claim.

---
*Generated-by: Claude Sonnet 5 (Stream 2, 2026-09-21; revised after independent review) |
Verified-by: `checkers/check_C3b_symsqrt.py` re-run this session for cooper_s7 and cooper_s10 (both
exit 0, verdict `SYM2_OPERATOR_IDENTITY_PROVEN`, output quoted above; the committed certificates
were produced with `{n_fit:30, fit_degree:5}`, this session's rerun used the defaults `{n_fit:26,
fit_degree:2}` — same verdict and partner, flagged as a parameter drift rather than silently
matched); golden tests `checkers/tests/test_c3b_symsqrt_golden.py` re-run this session (5 passed,
including two real known-bad controls that report which clause fired: `NOT_SYMMETRIC_SQUARE`, and
`FAIL_PARTNER_VALIDATION`/`partner_MUM: false` for the Apéry ζ(3) control — independently re-derived
this session by calling `fit_order2_recurrence` directly on ζ(3): `Cpoly(n) = -4(n+1)²`, confirming
the control fires on an un-normalized-fit artifact in the checker (a genuine Cooper-template member
with odd `b` reports a false `NOT MUM`/`FAIL_PARTNER_VALIDATION`), not on a real non-MUM operator;
flagged for the checker's owner, not fixed here); every Lean theorem above read at its cited name and
full statement (not name/docstring only) at `SocrateAI-DualScaleTopologicalUniverseModel-
LeanProposal` commit `3a960184cc85caf29419c1fd2a15026727cdf09f` (HEAD moved to `73c0094` during this
session; `git diff --stat` confirms all five cited files are byte-identical between the cited commit
and HEAD), `grep -rn "sorry\|admit"` run over all five cited files (matches are header-comment status
lines only, no live `sorry`/`admit` tactic); the operator-level reduction in `PartnerOperators.lean`
§4 (lines 271-282) is a comment, not a theorem — independently re-checked in SymPy for generic
`(a,b,c,d)` and found correct as a hand derivation; `cooper_s10_swampland_safe` read and independently
confirmed vacuous at `SocrateAI-Scientific-Agora-LeanMaster` commit
`ede49f06800cde8177867c02bb08d44f7be275c5` (HEAD moved to `8f4077c`; file byte-identical between
cited commit and HEAD); the two `K3_CRITERIA.md` copies diffed directly (6 hunks, not 1); no
`lake build` run in this session |
Reviewed-by: N*
