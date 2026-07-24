# Brief — Cross-Stream Alignment: C1/C3/C3b Checker Results

**To:** Stream 1 (Lean 4 formalization) + Stream 2 (K3 theory / candidate selection)
**From:** Stream 3 (Opus 4.8, T1)
**Date:** 2026-07-24
**Subject:** What Stream 3's checkers establish, and the actions they imply for S1/S2
**Tier discipline:** everything below is Tier A/B mathematics; no physical claim is made.

---

## 1. What Stream 3 now provides

A deterministic, exact-arithmetic checker suite for three `K3_CRITERIA.md`
criteria, with machine-generated certificates in `checkers/certificates/`:

- **C1** (`check_C1_mirror_integrality.py`) — inverse mirror-map integrality of an
  order-3 Picard–Fuchs operator, to order N₁.
- **C3** (`check_C3_sym2.py`) — the symmetric-square generating-function identity
  between an order-3 operator and an *exhibited* order-2 (Zagier) operator.
- **C3b** (`check_C3b_moduli_map.py`) — the explicit Shioda–Inose change-of-
  variable map F realizing that relation, with the period correspondence
  `Π₃(F(x)) = (1−Ax+Bx²)Π₂(x)²`.

Summary matrix: `docs/CRITERION_STATUS.md` (regenerate via
`scripts/render_criterion_status.py`).

## 2. The load-bearing result for candidate selection (Stream 2)

`docs/CRITERION_STATUS.md`, machine-generated:

| Candidate | C1 | C3 | C3b |
|---|---|---|---|
| γ, α, δ, η (sporadic AZ) | PASS | PASS | PASS |
| **s7, s10, s18 (Cooper, d≠0)** | **PASS** | **FAIL** | **FAIL** |

**For Stream 2 (K3_SELECTION / PREDICTION provenance):** s7 and s10 are genuine
maximal-unipotent-monodromy period operators (C1 passes), but they are **not**
symmetric squares of, nor Shioda–Inose-mapped to, any elliptic (Zagier) order-2
operator in the tested family (C3, C3b fail). The Almkvist–Zudilin symmetric-
square bijection covers only the six d=0 sporadic operators; the Cooper extended
family (d≠0) is outside it.

**Action for Stream 2.** `PREDICTION.md`'s provenance block requires a
C3b-passing candidate *pair* as the S3-00 MVM input. On the present evidence, an
s7- or s10-based pair does **not** supply one. Either (a) exhibit the specific
order-2 partner and map under which s7/s10 close (and add it to the checker's
`ORDER2_ZAGIER` register so C3/C3b can certify it), or (b) select the candidate
pair from the sporadic set (γ/F, α/C, δ/A, η/D), which do pass C3/C3b, or (c)
record that no C3b pair exists for the Cooper family and revise the K3-partner
narrative accordingly. This is a criterion result, not a preference.

## 3. Action for Stream 1 (Lean formalization)

`K3_CRITERIA.md` C3 route 2 asks for a Lean statement `sym2_<candidate>` whose
status is auto-imported. Stream 3's C3 checker gives the exact, machine-checkable
proposition to formalize for the **sporadic** pairs (which pass):

> For a bijection pair with order-2 params `(A,B,λ)` and order-3 params
> `(a,b,c)=(A, A−2λ, A²−4B)`, the identity
> `Σ_{n≥0} s_n·(−x/(1−Ax+Bx²))^{n+1} = (−x)·(Σ_n b_n x^n)²`
> holds as an identity of formal power series (proven here to x⁴⁰, exact).

For s7/s10 there is **nothing to formalize as a Sym² identity** — the checker
shows the proposition is false against the elliptic family. Stream 1 should not
carry a `SYM2_PROVED` flag for s7/s10; the honest status is `SYM2_ABSENT` (Cooper
extended family). If Stream 1 has produced any Lean artifact asserting a Cooper-
family Sym² identity, it should be reconciled with this result.

## 4. Epistemic guardrail (applies to all three streams)

C1/C3/C3b are geometric/analytic facts about differential operators and integer
sequences. Per VISION §1.3, a Sym²/Shioda–Inose relation is **not** by itself a
physical coupling between any bulk and brane EFT. No stream may write that these
checks "link", "lock", "couple", "predict", or "establish" a dark-sector or
compactification statement. The map F is tagged `[A-ONT]` (contingent on a
compactification realization that is not established here).

## 5. Open data item (all streams should be aware)

The frozen Level-11 order-3 recurrence in `refs/sporadic_recurrences.json` was
defective; corrected (Sym²-verified) in `refs/sporadic_recurrences_v2.json`, with
one term-confirmation item pending a primary source (see
`refs/RECURRENCE_CORRECTION_order3.md`). Streams consuming that file should use v2
and respect the `term_confirmation: PENDING` flag.

---

`Generated-by: Claude Opus 4.8 (T1) | Verified-by: checkers/tests/ (46 passing); docs/CRITERION_STATUS.md is checker output | Reviewed-by: pending T0`
