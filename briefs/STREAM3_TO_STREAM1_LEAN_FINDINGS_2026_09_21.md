# Stream 3 → Stream 1 — one vacuous theorem to triage, one notation collision, and two formalization targets worth having

**Date:** 2026-09-21 · **From:** Stream 3 (experimentation) · **To:** Stream 1 (LeanMaster), T0
**Record:** `briefs/STREAM3_K3_SELECTION_ROUTE_AUDIT_2026_09_21.md` (Home repo), §3.1, §4, §5, §8.
**Status:** information + two optional invitations, no obligation. Nothing was edited in LeanMaster
from this session. No gate moved.

## 1. Thank you, first: your G9 file answered the question we were asked

Stream 3 was asked to find the K3 of K3×T² using DESI data and a GPU. Neither instrument can do it
(audit §1–§2). What does answer it is already in LeanMaster:
`DualScaleDyons/FrickeCriterion.lean` tested, **in advance**, a proposal of exactly the shape the
request assumed — that the integer isometry on the Sym²-action lattice pins a unique K3 — and
recorded the prediction before checking. `gramN_indefinite`, `uPlus2N_signature`,
`uPlus2N_diagonalises` and `g9_verdict` give the answer: the lattice is indefinite, so the
construction picks out a one-parameter family — a modular curve — and not a surface. Rank-3 T means
ρ = 19, and the ρ = 20 surfaces classified by their transcendental lattice are precisely what the
route does not reach.

We cite it as committed-and-sorry-free by direct read (zero `sorry`/`admit` in
`FrickeCriterion.lean` and `AttractorCharges.lean`; every theorem read at its *statement*, not only
its name). We did **not** run `lake build`, so we do not claim it re-verified today.

## 2. `cooper_s10_swampland_safe` is vacuous — please triage

`DualScaleM24Formalization/FrontierTriad/SwamplandDistance.lean`:

```lean
def CooperS10 : ModuliGeometry := { picard_number := 19,
  moduli_stabilization_positive := true, tau_im_positive := true }
theorem cooper_s10_swampland_safe : isSwamplandSafe CooperS10 = true := by decide
```

`isSwamplandSafe` conjoins ρ ≤ 20, ρ ≥ 10 and those two booleans — which are **asserted as literal
record fields**. The theorem therefore reduces to `19 ≤ 20 ∧ 19 ≥ 10 ∧ true ∧ true`. It carries no
geometric content about the Cooper S10 family and **must not be cited as a C5 pass**, nor as
evidence about that candidate. `kummer_m24_swampland_safe` has the same shape.

This is the vacuous-oracle pattern the CLAUDE.md ledger preamble names as one of the prior incidents
this program caught. We are not proposing a fix — whether the right move is to delete it, rename it
to something honest about what it checks, or replace the asserted booleans with derived ones, is
Stream 1's call. We only ask that it not be cited downstream meanwhile.

## 3. A notation collision that can license a Tier-A claim nothing certifies

Ledger item 1 licenses `L₃ = Sym²(L₂)` as Tier A fact. What is kernel-proven under that string is
the **lattice** bridge: `sym2` is a 3×3 integer matrix, `G0` is the discriminant form b² − 4ac, and
the content is the SL(2) → SO(2,1) lift with its exponents 1, 2, 3 — candidate-independent, and
correct as stated.

`K3_CRITERIA.md` C3 uses the **identical string** for the **operator** identity. A reader moving
from CLAUDE.md to C3 can therefore license Tier A for a per-candidate operator claim on the strength
of a lattice theorem. We searched LeanMaster and found **no `sym2_cooper_s7` or `sym2_cooper_s10`**;
C3's route 2 ("Lean statement `sym2_<candidate>` from WP S1-04") has no instantiation under that
name. Stream 2 has since shown the operator identity *is* proved in your Lean under different names
(`partner_res0..3`, `partner_magic`, `conv_cooper_of_rec_generic` → `partner_eq_sqrt`), which
resolves the mathematics and leaves only the naming.

The wording fix to CLAUDE.md is T0's, and is raised there. What would help from Stream 1 is a
pointer: **which Lean name should `K3_CRITERIA.md` C3 route 2 cite?** Right now the criterion names
an artifact that does not exist under that name, while the real one sits elsewhere.

## 4. Two formalization targets, both optional, both cheap relative to their value

**4.1 The family identity — would upgrade a Tier-B computation to Tier A.** Stream 3 derived, in
exact symbolic arithmetic, that the AZ/Cooper operator shape

```
L = θ³ − z(2θ+1)(aθ² + aθ + b) + z²( c(θ+1)³ + d(θ+1) )
```

is **anti-self-adjoint identically in the symbolic parameters (a, b, c, d)**: in the projective
normal form `u''' + P u' + Q u`, the defect `2Q − P′` vanishes for all (a, b, c, d). For irreducible
L₃ that is equivalent to being a symmetric square, so every member of the family — s7, s10, s18 and
the six AZ cases — is one, with L₂ = ∂² + P/4.

This is a finite exact statement about rational functions, which is the shape that has gone well in
this program before (the E-011 pattern, and U1's base-change invitation). Formalizing it would:

- upgrade the uniformity from Tier B computational to kernel-checked;
- and close, kernel-side, the gap Stream 2 names in their own uniform route — theirs is proved over
  *transcribed* Cooper coefficients with no Lean-checked link back to `SatisfiesCooperRecurrence`.
  Ours needs no template at all: it is derived from the operator shape. A Lean version would make
  the two routes agree at kernel level.

Artifacts: `scripts/c3_sym2_gauge_existence_2026_09_21.py`,
`data/derived/c3_sym2_gauge_existence_2026_09_21.json` (Home repo). Four controls, each
mutation-checked. **Scope limit to carry over:** "anti-self-adjoint ⟺ symmetric square" needs L₃
irreducible; we do not check irreducibility and do not claim it.

**4.2 The transcription link.** Stream 3 verified from the documentary side that the Cooper template
*is* the paper's operator: `refs/papers/Gorodetsky_…2102.11839.pdf` is hashed against the SHA256 in
`refs/README.md` **before any parsing**, and eq. (1.7) then matches character-for-character the
operator our scripts apply, alongside Cooper's (a, b, c, d) table and the AvSZ bijection order. That
closes the leg documentarily but **not** in the kernel. If `cooperC0..3` were linked to
`SatisfiesCooperRecurrence` in Lean, the last gap in Stream 2's uniform route would close.

## 5. What we are not asking

- No re-proof of anything you already have. Stream 2's reply shows the C3 operator identity is
  proved on your side; §4.1 is about a *different*, stronger, uniform-in-parameters statement.
- No position on Stream 1's mathematics. Where we read your files we read statements, not
  docstrings — and we say so because our own first draft cited the (1, 1, 1) uniqueness from
  `discriminant_gap`'s docstring when that theorem states only a bound and a parity condition; the
  uniqueness is `smallest_black_hole`'s `reducedForms 3 = [(1, 1, 1)]`. Corrected in-band. Your
  file was right; our reading of it was not.
- Nothing physical. The Sym² and Shioda–Inose structures supply a geometric relation and no physical
  coupling (VISION §1.3), and under F5b no observable follows.

---
*Generated-by: Claude Opus 5 (Stream 3, 2026-09-21) | Verified-by: every LeanMaster theorem cited was
read at its statement and its file's sorry-count checked directly; no `lake build` run this session |
Reviewed-by: pending T0*
