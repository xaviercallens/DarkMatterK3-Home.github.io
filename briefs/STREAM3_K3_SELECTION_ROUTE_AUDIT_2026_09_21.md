# Stream 3 → Streams 1 & 2 — Which route can select the K3 of K3×T², and which cannot

**Date:** 2026-09-21 · **From:** Stream 3 (experimentation) · **To:** Stream 1, Stream 2, T0
**Question as received:** find the K3 for K3×T² by leveraging a real dataset (DESI) and the T4 GPU,
in support of Streams 1 and 2.
**Status:** audit + one new machine-checked artifact. No gate moved. No pinned document edited.

## Summary

The requested route does not reach the target, and the reason is mechanical rather than a matter of
effort or compute. A DESI Lyman-α sweep cannot discriminate between K3 candidates, because no input
in the sweep chain depends on which K3 is chosen (§1), and the map from a K3 to any exact observable
is Tier C and BLOCKED under F5b (CLAUDE.md ledger item 4). The T4 GPU cannot help either, because
criteria C1–C5 are exact rational arithmetic (§2).

Separately, the arithmetic route *does* have a determinate answer already recorded, and it is a
negative one: the rank-3 lattice carrying the symmetric-square action is indefinite, so it singles
out a one-parameter family — a modular curve — and not a surface (§4, Tier A in Lean). Under the
added condition ρ = 20 the classification would instead be finite, with a smallest case
T_S = A₂ at discriminant −3 (§4.2). That condition is the fork worth a T0 decision, and the
register's primary candidates sit on the other branch of it (ρ = 19, Tier B).

Two gaps found while checking this, both recorded below and neither previously filed: criterion C3
cannot be run on either register primary with the committed checker (§3), and the one Lean statement
that names a Cooper candidate is vacuous (§5).

## 1. A DESI sweep is candidate-blind — checked, not argued

`pipeline/sweep.py`, `pipeline/chi2_profile.py`, `pipeline/keff.py` and `pipeline/binmap.py` contain
no reference to `s7`, `s10`, `cooper`, `K3_CRITERIA`, `candidate`, `sym2`, `picard` or `lattice`
(grep, 2026-09-21, zero hits). The pinned grid spans two axes only:

- `M_GRID` — eight values of log₁₀(m/eV), −22.9 … −19.1
- `F_GRID` — seven mass fractions, 0.0 … 0.99

(`briefs/T0_MF_GRID_DEFINITION_2026_07_27.md` §3.) The consequence is checkable and worth stating in
its strongest form: **a fully unblocked, GPU-accelerated, real-data WP-E6-SWEEP run would emit a
(m, f) exclusion contour that is bit-identical for every candidate in the K3_CRITERIA register.** A
result that is identical across candidates carries no selection information about them.

Making the sweep candidate-sensitive would require a map from a specific K3 to a predicted m_φ. That
map is exactly what ledger item 4 places under F5b: the tadpole condition is not posable until a
threefold base B₃ is specified, and no exact observable (m_φ, α_D, Λ_D) may be assumed, generated or
backfilled until then. Ledger item 6 independently forecloses the shortcut: no pipeline may depend on
a single predicted scalar mass, because none exists under F5b.

Real-data mode is in any case still blocked upstream of all of this:
`pipeline/sweep.py::REAL_DATA_RULING_PIN is None`, pending a T0 ruling on theory corrections C1–C5
(`briefs/T0_DECISION_REQUEST_SWEEP_THEORY_CORRECTIONS_2026_09_17.md`). That blocker is about Si III
modelling, patchy reionization, the band-8 k cut and χ²_ν — none of which is a K3-selection question.

## 2. The T4 GPU is the wrong instrument for C1–C5

Two independent reasons, the second load-bearing:

1. The DarkMatterK3@Home worker that ran on the T4 computed a data-independent constant: it generated
   galaxies with `torch.rand`, never fetched `data_url`, and its `S12−S21` collapsed to a constant
   times the counts, so every job reported mean_asymmetry ≈ 0.0220. Its systemd service was stopped
   and disabled on 2026-09-16. Its outputs are sandbox material under ledger item 7 and are not
   citable in Streams 1–3 in any case.
2. More fundamentally: the K3 selection criteria are **exact rational arithmetic**. C1 carries
   Frobenius coefficients as exact dual numbers in ρ with `Fraction` power series
   (`checkers/check_C1_mirror_integrality.py`); C3/C3b compare integer sequences and q-expansions
   term by term with integrality asserted at every step. There is no float kernel to accelerate, and
   a GPU cannot represent the arithmetic these checkers depend on. Selection work here is
   CPU-and-exactness bound, not throughput bound.

## 3. New finding — criterion C3 cannot be run on either register primary

`docs/T0_DELEGATED_RULINGS_2026_07_26.md` DR-4 records that neither s7 nor s10 has a C3/C3b
certificate. This brief adds the reason, which had not been established: **it is a normalization gap,
not a recorded geometric failure.**

`checkers/check_C3_sym2.py` tests Gorodetsky's identity through the bijection
(a, b, c) = (A, A − 2λ, A² − 4B), which emits order-3 operators with **d = 0 only**. Both primaries
have d ≠ 0, and inverting the bijection on them yields no usable order-2 partner:

| candidate | (a, b, c, d) | implied (A, B, λ) | why C3 is not runnable |
|---|---|---|---|
| s7 | (13, 4, −27, 3) | (13, 49, 9/2) | d = 3 ≠ 0; **λ = 9/2 ∉ ℤ**, so no integral order-2 partner exists |
| s10 | (6, 2, −64, 4) | (6, 25, 2) | d = 4 ≠ 0; the implied partner is **non-integral at n = 1** (u₂ = 3/4) |
| s18 | (14, 6, 192, −12) | (14, 1, 4) | d = −12 ≠ 0; implied partner non-integral at n = 1 (127/4) |

(6, 25, 2) is not among the six Zagier sporadic cases coded in the checker
(`ORDER2_ZAGIER`: (7,−8,2), (9,27,3), (10,9,3), (11,−1,3), (12,32,4), (17,72,6)). Zagier's
degenerate/hypergeometric families were **not** searched here; that check is not claimed.

**Three branches follow, and one of them is not a bookkeeping outcome.** Either (i) a d ≠ 0 Sym²
identity exists and is simply not coded — a normalization gap; or (ii) the d ≠ 0 operators are
gauge/pullback-equivalent to d = 0 ones, also a gap but a different repair; or (iii) **no order-2 L₂
exists for these candidates at all.** Branch (iii) is not a gap: `K3_CRITERIA.md` C3 requires
"an explicitly exhibited order-2 operator L₂", so no such L₂ is a C3 failure, whose stated
consequence is **F1 removal for the dual-scale role**. Since DR-4 records "s10 stays primary", branch
(iii) is a live path to removing the primary candidate, and it is named here so that T0 sees it rather
than inferring it from an omission. Stream 3 takes no position on which branch holds; distinguishing
them is Stream 2 mathematics, not a computation this repo can run.

Feeding either primary to the committed checker would be a test that *cannot pass* — the mirror image
of the "test that cannot fail" class this repo has caught five times. A `FAIL` certificate from it
would read downstream as a geometric falsification of the primary candidate while recording only a
normalization mismatch, and under `K3_CRITERIA.md` §3.5 certificates are the only admissible evidence
for a C3 claim. Accordingly the artifact is written to `data/derived/`, **not** to
`checkers/certificates/`, and its verdict field reads `INAPPLICABLE_NORMALIZATION`, never `FAIL`.

- Script: `scripts/c3_normalization_applicability_2026_09_21.py`
- Artifact: `data/derived/c3_normalization_applicability_2026_09_21.json`
- Label: `MATH-APPLICABILITY` — not a C3 verdict, not exclusion, not FIT, not TEST
- Negative controls, both enforced in-process (exit 1 on failure), both PASS: **NC-1** the six d = 0
  sporadic families come out APPLICABLE and reproduce the committed `ORDER2_ZAGIER` parameters
  exactly; **NC-2** mutating d: 0 → 1 on each known-good family flips it to INAPPLICABLE. NC-1 guards
  against a wrong inverse bijection; NC-2 against a script that calls everything inapplicable.

## 4. What the arithmetic route already answers (Tier A, Stream 1)

`DualScaleDyons/FrickeCriterion.lean` in the LeanMaster repo tested, in advance, a proposal of exactly
the shape the incoming question assumes — that the K3 of our universe is the unique surface whose
transcendental lattice aligns with the lattice carrying the Sym² action of the modular group.

**4.1 The recorded outcome is no selection.** The lattice carrying the action has signature (2,1) and
is indefinite: `gramN_indefinite` exhibits vectors of norm +1 and −4N, and `uPlus2N_signature` /
`uPlus2N_diagonalises` diagonalise U ⊕ ⟨2N⟩ as diag(2, 2N, −2) via an explicit index-2 basis, closing
a caveat that had been asserted rather than proved on both sides. `g9_verdict` collects the result.
A rank-3 transcendental lattice corresponds to Picard number ρ = 19, not 20; the surfaces classified
by their transcendental lattice are the ρ = 20 ones, which this construction does not reach. What it
picks out is a one-parameter family — a modular curve — rather than a surface.

This agrees with Stream 3's own ledger item 3 from an independent direction: the finite singular loci
of the cooper families are order-2 elliptic points of the X₀(n)+ modular curve, not Kodaira
degenerations. Both statements say the object at the end of this route is a curve, not a point.

**4.2 The stated repair, and the fork it creates.** Adding a definiteness condition — demanding
ρ = 20 — makes the transcendental lattice rank 2 and positive definite, and the classification then
runs by positive-definite binary quadratic forms: finite at each discriminant, with a smallest case.
Two distinct Lean results carry this, and they must not be merged:
`AttractorCharges.discriminant_gap` gives the **bound and a parity condition only** —
`3 ≤ 4ac − b² ∧ (4ac − b² = 3 → b odd)`. The **uniqueness** is a separate theorem,
`AttractorCharges.smallest_black_hole`, whose operative conjunct is `reducedForms 3 = [(1, 1, 1)]`:
the reduced forms of discriminant 3 are exactly the single class (1, 1, 1), giving
(p², p·q, q²) = (2, 1, 2), T_S = A₂ and D = −3. Proved by `decide +kernel`, so kernel-checked
without the `native_decide` compiler-trust caveat.

So there is a determinate answer to "which K3" — but only on the ρ = 20 branch, and the register's
primary candidates are on the other one: ρ = 19, T = 3 for the cooper_s7 family is **Tier B**
(derived via E-011 / Zarhin 1983 Thm 1.6(a), independently verified by Stream 1, and a derived prior
is not a measurement — Gate E criterion 1 remains UNRESOLVED per T0 decision D1). Whether the program
adopts the ρ = 20 condition is a T0 question, not one Stream 3 can settle, and it is the single
highest-leverage decision available on the selection problem.

**Verification status of the citations in §4.** Both files contain zero occurrences of `sorry` or
`admit`, and every theorem named above exists at the cited name with its **statement** read, not only
its name and docstring (checked 2026-09-21 by direct read). That distinction is load-bearing: a
name-existence check would not have caught this brief's own first draft, which attributed the
(1, 1, 1) uniqueness to `discriminant_gap` — a theorem that states a bound and a parity condition and
no uniqueness at all. A fresh `lake build` was **not** run in this session, so these are cited as
committed-and-sorry-free, not as re-verified-today; the full five-gate check is `lean-proof-gate`'s
to run.

## 5. New finding — the one Lean statement naming a Cooper candidate is vacuous

`DualScaleM24Formalization/FrontierTriad/SwamplandDistance.lean`:

```lean
def CooperS10 : ModuliGeometry := { picard_number := 19,
  moduli_stabilization_positive := true, tau_im_positive := true }
theorem cooper_s10_swampland_safe : isSwamplandSafe CooperS10 = true := by decide
```

`isSwamplandSafe` conjoins ρ ≤ 20, ρ ≥ 10 and the two booleans. Those booleans are asserted as
literal record fields, so the theorem reduces to `19 ≤ 20 ∧ 19 ≥ 10 ∧ true ∧ true`. It carries no
geometric content about the Cooper S10 family and **must not be cited as a C5 pass, nor as any
evidence about that candidate.** This is the vacuous-oracle shape named in the ledger preamble as one
of the prior incidents this program caught. Filed here for Stream 1 to triage; no edit made to the
LeanMaster repo from this session.

## 6. Named next actions

Routed, with the owner each already has in the record:

1. **T0 — the ρ = 20 fork (§4.2).** Decide whether the program adopts the definiteness condition that
   makes K3 selection a finite classification. Everything else on the selection problem is downstream
   of this. Highest leverage item in this brief.
2. **Stream 2 — supply a d ≠ 0 Sym² identity, with a citation, or record that none is known (§3).**
   This is the mechanical unblock for DR-4's standing ask ("produce C1/C3/C3b for s7"). Until it
   exists, C3 is not a runnable criterion for any register primary, and `K3_CRITERIA.md` cannot be
   frozen on the C3 axis — which independently blocks C3b, since C3b is defined only for candidates
   that have cleared C3. **If the answer is that no order-2 L₂ exists (§3 branch iii), that is a C3
   failure and not a gap, and C3's own stated consequence — F1 removal for the dual-scale role —
   falls due on the primary candidate.** Stream 2 should return which branch holds, not only whether
   an identity is coded.
3. **T0 — disambiguate the two `L₃ = Sym²(L₂)` statements in the ledger.** Ledger item 1 licenses
   that string as Tier A fact. What is kernel-proven under it is the **lattice** bridge: `sym2` is a
   3×3 integer matrix, `G0` is the discriminant form b² − 4ac, and the content is the SL(2) → SO(2,1)
   lift with its exponents 1, 2, 3 — candidate-independent. `K3_CRITERIA.md` C3 uses the *identical
   string* for the **operator** identity, which has no certificate for any register candidate (§3).
   A reader moving from CLAUDE.md to C3 can therefore license Tier A for a per-candidate claim that
   nothing certifies. This is the conflation class the ledger preamble exists to catch, and it is a
   wording fix to CLAUDE.md, which is T0's call and not Stream 3's to make. Raised here under F6
   discipline as a disclosure rather than left inside another stream's action item.
4. **Stream 1 — triage `cooper_s10_swampland_safe` (§5)**, and confirm whether any Lean statement
   instantiates `sym2_<candidate>` for a register candidate as `K3_CRITERIA.md` C3 route 2 requires.
   Stream 3's search found none: the proved `sym2_*` results are lattice-and-matrix level and
   candidate-independent (the SL(2) → SO(2,1) lift and its exponents 1, 2, 3). Ledger item 1's Tier A
   statement is correct as written and is not weakened by this brief — but it certifies the lattice
   bridge, and it does not supply a C3 certificate for s7 or s10 (see item 3).
5. **Stream 3 — no action available on selection.** The WP-E6-SWEEP line stays blocked on C1–C5 and
   remains, when unblocked, an (m, f) exclusion instrument rather than a selection instrument.

## 7. What this brief does not claim

- It does not claim s7 or s10 fails C3. The criterion was not run; it is not runnable (§3).
- It does not claim ρ = 19 is wrong for cooper_s7. That value is Tier B and stands as recorded.
- It does not claim the K3 has been identified. On the ρ = 20 branch a smallest case exists
  (T_S = A₂); connecting that to this program's register is unstarted work, and no physical
  consequence follows from it absent the worked EFT matching that VISION §1.3 requires — the Sym²
  and Shioda-Inose structures supply a geometric relation and no physical coupling.
- It does not reopen U1 (is T ≅ U⊕⟨14⟩?), which remains the open geometric item at
  `docs/U1_ROUTE_DESIGN_2026_07_26.md` in the Stream 2 repo.

---
*Generated-by: Claude Opus 5 (Stream 3, 2026-09-21) | Verified-by: grep of the sweep chain for
candidate-dependent inputs (zero hits); exact-arithmetic applicability artifact with two enforced
negative controls; every cited Lean theorem name and sorry-count read directly from
`DualScaleDyons/FrickeCriterion.lean`, `DualScaleDyons/AttractorCharges.lean` and
`DualScaleM24Formalization/FrontierTriad/SwamplandDistance.lean` | Reviewed-by: pending T0*
