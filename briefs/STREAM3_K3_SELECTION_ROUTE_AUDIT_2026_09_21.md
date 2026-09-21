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

Three gaps found while checking this, none previously filed: criterion C3 cannot be run on either
register primary with the committed checker (§3); C3 is in any case satisfied by every member of that
family by the shape of the recurrence, so it cannot select among the register candidates drawn from
it, leaving C1 as the only committed checker with per-candidate discriminating power (§3.1); and the
one Lean statement that names a Cooper candidate is vacuous (§5). A fourth surfaced on verifying the
checker against its vendored source: two of the register's four candidates — K-S22 and K-t103 — have
no citable defining recurrence, and the source names only three Cooper sporadic sequences (§3.2).

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

## 3. New finding — `check_C3_sym2.py` cannot be run on either register primary

> **Correction note, 2026-09-21 (same day, F6 in-band).** This section was headed "criterion C3
> cannot be run on either register primary". That over-stated it. What cannot run is **this repo's
> `checkers/check_C3_sym2.py`**; the underlying Sym² identity for d ≠ 0 *is* coded elsewhere in the
> program — `checkers/check_C3b_symsqrt.py` in the K3-DarkMatter repo, and independently in Stream
> 1's Lean — under names this checker does not search for. Stream 2 established this in
> `briefs/STREAM2_TO_STREAM3_C3_BRANCH_REPLY_2026_09_21.md`. It is a **coverage gap in one
> checker**, not a program-wide inability. See §8.

`docs/T0_DELEGATED_RULINGS_2026_07_26.md` DR-4 records that neither s7 nor s10 has a C3/C3b
certificate. This brief adds the reason, which had not been established: **it is a normalization gap,
not a recorded geometric failure.**

`checkers/check_C3_sym2.py` tests Gorodetsky's identity through the bijection
(a, b, c) = (A, A − 2λ, A² − 4B), which emits order-3 operators with **d = 0 only**. Both primaries
have d ≠ 0, and inverting the bijection on them yields no usable order-2 partner:

| candidate | (a, b, c, d) | implied (A, B, λ) | why C3 is not runnable |
|---|---|---|---|
| s7 | (13, 4, −27, 3) | (13, 49, 9/2) | d = 3 ≠ 0; **λ = 9/2 ∉ ℤ**, so no integral order-2 partner exists *of the bijection-implied kind* — see the note below |
| s10 | (6, 2, −64, 4) | (6, 25, 2) | d = 4 ≠ 0; the implied partner is **non-integral at n = 1** (u₂ = 3/4) |
| s18 | (14, 6, 192, −12) | (14, 1, 4) | d = −12 ≠ 0; implied partner non-integral at n = 1 (127/4) |

> **Which object the table is about.** "No integral order-2 partner exists" refers to the sequence
> the Gorodetsky bijection would imply, and to that object the rows are correct. It is **a different
> object** from the order-2 partner obtained as the exact power-series square root of the bulk
> series, which for s7 is **A279619 and is integral** (Stream 1, axiom-free; Stream 2's reply §4).
> The s10 figure u₂ = 3/4 is right for the object computed here; s10's square-root partner is
> dyadic and non-integral, which is a separate and still-open question (§8).

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
than inferring it from an omission.

> **Correction note, 2026-09-21 (same day, F6 in-band).** This section first read: "Stream 3 takes no
> position on which branch holds; distinguishing them is Stream 2 mathematics, not a computation this
> repo can run." **The second clause was wrong.** The existence question is exactly computable here,
> by exact symbolic arithmetic, and §3.1 now resolves it. The original sentence is preserved in this
> note rather than silently rewritten. What remains Stream 2's is the normalization and integrality
> question, not the existence question.

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

### 3.1 Branch (iii) is excluded — and C3 cannot discriminate inside this family

Resolved 2026-09-21 by exact symbolic computation. An order-3 operator in projective normal form
`u''' + P u' + Q u` is the symmetric square of a second-order operator exactly when it is
anti-self-adjoint, i.e. when `2Q − P′` vanishes. Both ingredients are **derived at run time**, not
cited: `Sym²(∂² + r) = ∂³ + 4r∂ + 2r′` is obtained by substituting a generic product of solutions of
`y″ = −ry` (residual 0). The normal form is produced by executing the `y = w·u` substitution with
`w′/w = −p₂/3` and reading off P and Q, so no classical closed form is typed in (VISION §6.1). The
adjoint step is weaker and is labelled as such in the script: the formal adjoint is **hand-supplied**
as `−∂³ − (P·)′ + Q` and then confirmed to make `L* + L` collapse to `(2Q − P′)f`. That verifies the
algebra of the step, not its premise — it is a consistency check, not a derivation, and is recorded
that way rather than described as one.

**The result is stronger than a per-candidate verdict: `2Q − P′` vanishes identically in the symbolic
parameters (a, b, c, d) of the AZ/Cooper shape** `θ³ − z(2θ+1)(aθ²+aθ+b) + z²(c(θ+1)³ + d(θ+1))`.
Two consequences:

1. **Branch (iii) is excluded.** An order-2 L₂ exists for s7 and s10 — and for every member of the
   family — exhibited as `∂² + P/4`. So the missing C3 certificates are branch (i)/(ii): an L₂ exists
   and the committed checker's d = 0 normalization cannot see it. **No candidate is removed by C3 on
   existence grounds.**
2. **C3 has no discriminating power inside this family.** Every member satisfies the symmetric-square
   property by the *shape* of the recurrence, independently of (a, b, c, d). A criterion that every
   candidate passes by construction cannot rank or separate them. This is a finding about the
   criterion, not about any candidate, and it bears directly on the `K3_CRITERIA.md` freeze: C3 can
   serve as a well-formedness check on the family, but not as a selector within it. It agrees from an
   independent direction with the sandbox R2 result that ODE order 3 alone does not make a sequence
   K3-type.

   **Scope of consequence 2 — tightened 2026-09-21 (§3.2).** An earlier version of this paragraph
   left the scope open, because `K3_CRITERIA.md` §1 also registers **S22** and **t103** whose
   recurrences are `TBD-AT-FREEZE`. §3.2 closes it against the vendored source: the sporadic
   order-3 landscape is exactly the nine sequences already in `ORDER3_AZ_COOPER`, so **the identity
   covers every sporadic order-3 Apéry-like sequence there is** — not merely the register. S22 and
   t103 need no family-membership test; they need a citable recurrence or removal.

3. **C1 is left as the only committed checker with per-candidate discriminating power on this
   register.** C3 is non-discriminating here, and C3b is defined only for candidates that have
   cleared C3, so it inherits the problem. C1 certificates do exist and are candidate-specific —
   `PASS(40)` for s7, s10, alpha, gamma, delta, eta. Whether C1 alone can carry a selection is a
   freeze question for T0 and Stream 2, not one this brief answers.

**Independent corroboration from the framework literature.** The symbolic identity above was derived
here from the recurrence shape alone, with no appeal to the geometry. It agrees with what the
hash-pinned sources already say: Stream 2 recorded **Doran 1998 Thm 5.13 — the Picard–Fuchs operator
of an Mₙ-polarized family *is* the Sym² of a second-order Fuchsian operator** (read 2026-07-26,
`briefs/STREAM2_PHASE4_STEP2_SOURCES_READ_2026_07_26.md` leg 4, in the K3-DarkMatter repo). So the
symmetric-square property is a *consequence of Mₙ-polarization*, not a discriminating fact about any
member — which is exactly why C3 cannot separate candidates inside the family. Two independent
routes, one computational and one from the framework, reach the same conclusion.

- Script: `scripts/c3_sym2_gauge_existence_2026_09_21.py` · Artifact:
  `data/derived/c3_sym2_gauge_existence_2026_09_21.json`
- Label: `MATH-EXISTENCE` — gauge equivalence only; not a C3 verdict, not exclusion, not FIT, not TEST
- Verdict vocabulary is `SYM2_EXISTS_UP_TO_GAUGE` / `NO_SYM2_IN_ANY_GAUGE`, never PASS/FAIL, because
  the two directions are not symmetric: a nonzero defect would be decisive, whereas vanishing only
  **excludes** branch (iii) and is *not* a C3 pass — C3 requires equality in a fixed normalization,
  and the exhibited L₂'s integrality is a separate question already known to fail for the s10
  partner (6, 25, 2) at n = 1.
- Four enforced controls, all passing: **NC-0** the reconstructed operator annihilates each
  candidate's own committed power series, validating the θ → ∂/∂z conversion; **NC-1** breaking the
  shape two ways (`c(θ+1)³ → cθ³`, and dropping the `(2θ+1)` factor) makes the defect nonzero, so the
  family-wide vanishing is a property of the recurrence shape and not of the normal-form code;
  **NC-2** off-family operators with a hand-computed nonzero defect (e.g. `∂³ + z∂ + 1`, where
  `2Q − P′ = 1`) are correctly reported `NO_SYM2_IN_ANY_GAUGE`, so the criterion is falsifiable;
  **NC-3** *anchored to committed data* — every family carrying a committed `C3_sym2_*.json` whose
  own recorded status is `PASS` must come out `SYM2_EXISTS_UP_TO_GAUGE`, and at least three such
  certificates must be found. A first version of NC-3 asserted only that the six d = 0 families come
  out `SYM2_EXISTS`, which the symbolic identity makes true for *every* input in the family — a
  control that could not fail. It was rebuilt and now fails both when an anchoring certificate is
  removed (2 found, below the minimum) and when one's recorded status is altered; both were checked
  by mutation.
- **Documented expected non-match.** `P/4` does not equal the projective normal form R of the Zagier
  order-2 partner. This is expected rather than a defect, and is recorded in the artifact: the
  Gorodetsky identity carries the change of variable `w = −x/(1 − Ax + Bx²)`, so the Zagier L₂ lives
  in the w coordinate while `P/4` lives in z. Being a symmetric square is invariant under change of
  variable, so both readings stand. An earlier draft of this check treated the non-match as a control
  failure; that was a wrong expectation on Stream 3's part, not a defect in either operator.
- **Scope limit, stated rather than buried.** "Anti-self-adjoint ⟺ symmetric square" requires L₃
  irreducible. Irreducibility is **not** checked here and is not claimed; for a reducible L₃ the
  reading can degenerate.

### 3.2 The committed C3 checker is faithful to its source — and the register has two entries with nothing behind them

The §3/§3.1 findings all rest on `checkers/check_C3_sym2.py`'s parameter tables, so those tables
were checked against the vendored primary source rather than trusted. The source is
`refs/papers/Gorodetsky_sporadic_apery_like_sequences_2102.11839.pdf` (arXiv:2102.11839v2); its
SHA256 is read from `refs/README.md` and the file is hashed and compared **before any of its text is
parsed**, so a substituted PDF cannot feed the check.

All six verifications pass, each parsed out of the paper at run time and compared to the committed
Python — no expected value is typed in except as a control:

| | verified against the source |
|---|---|
| **V1** | SHA256 matches `refs/README.md` — `520da4b0…71ee1` |
| **V2** | Cooper's table: s7 = (13, 4, −27, 3), s10 = (6, 2, −64, 4), s18 = (14, 6, 192, −12) — matches `ORDER3_AZ_COOPER` exactly |
| **V3** | the Almkvist–van Straten–Zudilin bijection order — A–F ↦ δ, ζ, α, η, ε, γ *in this order* — matches the committed `BIJECTION` |
| **V4** | the paper's operator (1.7) is character-for-character the operator this session's scripts apply |
| **V5** | "Cooper found **3** additional sporadic solutions, named s7, s10 and s18" |
| **V6** | 15 sporadic = 6 Zagier (order 2) + 6 Almkvist–Zudilin (order 3) + 3 Cooper (order 3) |
| **V7** | "S22" occurs **zero times in the full text of both vendored papers** (Gorodetsky and the AESZ tables) |

- Script: `scripts/verify_checker_against_source_2026_09_21.py` · Artifact:
  `data/derived/checker_source_verification_2026_09_21.json` · Label: `SOURCE-VERIFICATION`
- Four enforced controls, all passing: a corrupted hash, a perturbed (a, b, c, d) expectation and a
  permuted bijection order must each be rejected; and the V7 search must *find* a token known to be
  present (`s7`), so that "zero hits for S22" cannot be confused with a search that never matches.
  Each re-runs the real comparator with one value altered, so a comparator that always returned true
  would be caught — and was, by mutation.
- **V5 and V7 are separate claims and are kept separate.** V5 establishes only that S22 is absent
  from the sentence enumerating Cooper's solutions. The stronger statement — that the vendored
  sources contain no such sequence at all — rests on V7's full-text search, and is scoped to what
  this repo holds. Cooper's primary paper is unfetched (Springer paywall, `refs/README.md` line 25),
  so nothing here rules on what that paper contains.

**Two consequences.**

1. **V6 tightens §3.1.** The nine order-3 sporadic sequences *are* `ORDER3_AZ_COOPER`. The family
   identity therefore covers every sporadic order-3 Apéry-like sequence, so C3's lack of
   discriminating power is not a fact about this register's particular choices — it is a fact about
   the whole sporadic order-3 landscape.
2. **V5 is a register finding.** `K3_CRITERIA.md` §1 registers four candidates. The source names
   **exactly three** Cooper sporadic solutions — s7, s10, s18 — and **no "Cooper S22" exists in it**.
   So the register entry **K-S22** has no citable defining recurrence behind it in anything this repo
   holds. **K-t103** is separately off the roadmap, quoted exactly: *"t103 (vetoed by T0 2026-07-26
   **pending certificates**)"* (`ROADMAP.md`) — a **conditional** veto, not an absolute one; it lifts
   if certificates are produced, and no certificate is possible without a citable recurrence. The
   register's own rule is explicit:
   *"a candidate without a citable defining recurrence at freeze time is dropped, not guessed."*
   Under that rule the register's effective content at freeze is **s7 and s10** — exactly the two
   candidates this brief's findings cover. Stream 3 takes no position on whether S22 was a
   mis-transcription of s18 or of something else; recovering or dropping it is Stream 2's, and the
   primary Cooper source is still unfetched (`refs/README.md` line 25: Springer paywall).

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
   falls due on the primary candidate.** — **Superseded the same day by §3.1: branch (iii) is
   excluded, so no candidate is removed by C3 on existence grounds, and this item is rescoped.**
   What remains for Stream 2 is narrower and purely about normalization: the exhibited L₂ is
   `∂² + P/4` in the projective normal form, so the open question is whether it can be brought to
   C3's fixed normalization and whether its associated sequence is integral — which for the s10
   partner (6, 25, 2) already fails at n = 1. Stream 2 should also record, for the freeze, that C3 is
   satisfied by every member of the family by construction and so cannot serve as a selector (§3.1).
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

7. **T0 — the candidate register may be down to two entries, and that is a freeze question.**
   If K-S22 and K-t103 both drop under `K3_CRITERIA.md`'s own rule (§3.2), the register goes from
   four candidates to two — s7 and s10. `K3_CRITERIA.md` is the document gating the freeze, and C3b
   gates `PREDICTION.md`'s S3-00 input, so this is a structural change to a freeze-blocking
   document, not a bookkeeping edit. It belongs with the ρ = 20 fork and items 3 and 6 rather than
   inside a Stream 2 task: **Stream 2** recovers the recurrence or confirms the drop; **T0** rules on
   what a two-entry register means for the freeze, and on whether a freeze is still the right
   instrument given §3.1 (C3 non-discriminating) and §3.2 (C1 the only per-candidate discriminator).

6. **T0 — ledger item 3's U1 line is stale.** CLAUDE.md records "The open geometric item is U1
   (is T ≅ U⊕⟨14⟩?)". U1 was closed Tier B on 2026-07-27 with an explicit det-1 base change and
   coordinator-verified controls (§7). The ledger's own rule is that a document contradicting it
   carries a dated correction note; here the contradiction runs the other way, and the ledger
   line is the stale one. A wording fix to CLAUDE.md is T0's call, raised for the same reason as
   item 3. Until it is fixed, ledger item 3 will keep propagating into new documents — it
   propagated into this one.

## 8. Stream 2's reply, and what it changes (2026-09-21, same day)

Stream 2 answered this brief the day it was filed, in
`briefs/STREAM2_TO_STREAM3_C3_BRANCH_REPLY_2026_09_21.md` and
`briefs/STREAM2_TO_STREAM3_MODULAR_RAIL_AND_CM_POINTS_2026_09_21.md` (K3-DarkMatter repo).
Stream 3 re-ran their controls before citing any of it, per ruling A1's producer ≠ verifier
pattern: **46/46** CM-point controls and **35/35** A₂ controls pass on this side, and
`check_A2_membership.py` independently re-verifies this brief's own §4.2 citation
(`reducedForms 3 = [(1, 1, 1)]`) against LeanMaster at commit `4109a51`.

**8.1 The branch question is answered: branch (i).** An explicit order-2 L₂ with L₃ = Sym²(L₂) is
exhibited and machine-verified for **both** primaries. Under the monic d/dz normalization the
residual is a literal zero — `{D0: 0, D1: 0, D2: 0}` — so there is no cofactor. This agrees with
§3.1 (branch (iii) excluded) and goes further: §3.1 established that *an* L₂ exists up to gauge,
Stream 2 exhibits it. Branch (ii) needs no adjudication, since the d ≠ 0 identity is proved directly
rather than by a detour through a d = 0 case.

**8.2 What §3.1 contributes back.** Stream 2 flags one honest gap in their uniform-in-(a, b, c, d)
route: it is proved over *transcribed* Cooper coefficients `cooperC0..3`, "with no Lean-checked link
back to `SatisfiesCooperRecurrence` — so this route's uniformity is a fact about the transcribed
template, not (by itself) about the recurrence." Two results here bear on exactly that:

- **§3.2 V4 closes the transcription leg from the source side.** The operator this repo applies was
  compared character-for-character with Gorodetsky eq. (1.7), parsed out of the vendored PDF behind
  a SHA256 gate. The template is the paper's operator.
- **§3.1 reaches the uniformity by a different route.** `2Q − P′ ≡ 0` is derived symbolically from
  the operator *shape* in (a, b, c, d), with no Lean template and no transcription step. Two
  independent derivations of the same uniformity, with disjoint failure modes.

What neither closes is the kernel-side link from the template to `SatisfiesCooperRecurrence`. That
is a Lean item and is routed to Stream 1 (§6 item 4).

**8.3 The ρ = 20 fork now has concrete content inside the register families.** Stream 2 computed
what the cut of §4.2 picks out. All three singular points of the s7 operator are ρ = 20 CM points —
z = 1/27 (D = −28), z = −1 (D = −7), and z = ∞ (D = −3), the last being **A₂ itself**, the minimal
case §4.2 named. **A₂ is in the s7 family and not in the s10 family**, the latter by an exact
all-vector congruence (−3 is not a square mod 40), not a bounded search. This *sharpens* ledger item
3 rather than contradicting it: the loci are elliptic points of X₀(7)⁺ **and** the members over them
carry rank-2 transcendental lattices. No Kodaira reading is made or implied.

Two cautions Stream 2 states and this brief adopts: the agreement between the binary-form side and
the modular side is **forced** by Shioda–Inose, so it is not independent corroboration; and **no
ranking of s7 over s10 follows** from "A₂ is in s7" — a minimum-|D| rule has no warrant.

**8.4 The first candidate-dependent label.** §1 showed the sweep is bit-identical across candidates.
Stream 2 observes that **`D is a square mod 4n`** is an exact, cheap, *candidate-dependent*
predicate — the first one this program has. It is bookkeeping vocabulary for hypotheses, **not an
observable**: §1's conclusion is unchanged, and no (m, f) prior, m_φ, α_D or Λ_D follows from any row
(Tier C, BLOCKED under F5b, tadpole unposable without B₃).

**8.5 DR-4's standing ask is largely discharged.** For s7, C1 (mirror integrality, PASS(60)), C3b
(`SYM2_OPERATOR_IDENTITY_PROVEN`), T1, T2 and T3 all now exist. For s10 the same, minus a LIVE T2 —
its lattice certificate is DRAFT by T0 ruling D6′, so **every s10 row is advisory**.

**8.6 Mirrored, with a drift detector.** Stream 2's certificates are mirrored at
`data/mirrors/stream2/` with `MIRROR_MANIFEST.json` pinning each SHA256 and carrying each
`not_claimed` block, alongside the source commit `4794e7d`.
`pipeline/tests/test_stream2_cm_mirror_consistency.py` (7 tests) implements their requested check:
s7's `locus_hits` must reproduce the ledger loci {−1, 1/27}, and every s10 row must stay advisory.
It fails closed on drift — verified by mutation (dropping one `advisory`, and altering a locus, each
trip it). A negative control asserts s7 rows are *not* advisory, so the flag still discriminates.

**8.7 Independent agreement on the "modular rail" text.** Stream 3 and Stream 2 reviewed it
separately and reached the same two verdicts: "the universe evolves along this rail" is **Tier C,
unsupported, not adopted** — no dynamics on the moduli curve is defined anywhere in the program; and
"this explains exactly why reverse-to-zero could not reach zero parameters" is **not established**.
One detail differs and Stream 2's is better sourced: they locate `reverse-to-zero` in the
**DualScaleSimulator** repo, where its own pre-registration addenda A6–A9 close "zero-parameter" as
*not derivable*; Stream 3's search found only a pointer in LeanMaster's `NEXT_DIRECTIONS.md`
attributing it to LeanFlow. Either way it is not in any repo on this disk, and the "explains exactly"
claim asserts an identification of that leftover parameter with the modular coordinate that nothing
computes.

## 7. What this brief does not claim

- It does not claim s7 or s10 fails C3. The criterion was not run; it is not runnable as committed
  (§3). Nor does it claim either passes C3: §3.1 establishes only that an order-2 L₂ exists up to
  gauge, which excludes branch (iii) and is not a pass in C3's fixed normalization.
- It does not claim ρ = 19 is wrong for cooper_s7. That value is Tier B and stands as recorded.
- It does not claim the K3 has been identified. On the ρ = 20 branch a smallest case exists
  (T_S = A₂); connecting that to this program's register is unstarted work, and no physical
  consequence follows from it absent the worked EFT matching that VISION §1.3 requires — the Sym²
  and Shioda-Inose structures supply a geometric relation and no physical coupling.
- ~~It does not reopen U1 (is T ≅ U⊕⟨14⟩?), which remains the open geometric item at
  `docs/U1_ROUTE_DESIGN_2026_07_26.md` in the Stream 2 repo.~~ **Corrected 2026-09-21, same day:
  U1 is CLOSED, not open.** Stream 2 executed it fresh-context on 2026-07-27 and the T1
  coordinator re-ran the pipeline and controls independently:
  `briefs/STREAM2_TO_STREAMS1_3_U1_CLOSED_2026_07_27.md`, record
  `briefs/STREAM2_U1_EXECUTION_2026_07_27.md`, pipeline `checkers/check_U1_lattice.py` in the
  K3-DarkMatter repo. The joint monodromy-invariant lattice of cooper_s7 is primitive even with
  det = −14, signature (2,1), and an **explicit det-1 integral base change realizing U ⊕ ⟨14⟩**
  was exhibited; the identical pipeline on cooper_s10 derives det = −20 / U ⊕ ⟨20⟩
  (computed-vs-computed, no hardcoded target). **Tier B**, with two named residual links — the
  numerics→exact monodromy recognition, and the identification of the computed lattice with T,
  where the λ-rescaling branch is excluded by the framework's shape rather than by computation.
  So the levels are n = 7 for cooper_s7 and n = 10 for cooper_s10. This brief's earlier sentence
  was drawn from CLAUDE.md ledger item 3, which still calls U1 "the open geometric item" and is
  **stale on that point** — flagged to T0 in §6 item 6.

---
*Generated-by: Claude Opus 5 (Stream 3, 2026-09-21) | Verified-by: grep of the sweep chain for
candidate-dependent inputs (zero hits); exact-arithmetic applicability artifact with two enforced
negative controls; every cited Lean theorem name and sorry-count read directly from
`DualScaleDyons/FrickeCriterion.lean`, `DualScaleDyons/AttractorCharges.lean` and
`DualScaleM24Formalization/FrontierTriad/SwamplandDistance.lean` | Reviewed-by: pending T0*
