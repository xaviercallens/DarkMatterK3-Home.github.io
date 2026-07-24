# Correction — `sporadic_recurrences.json` order-3 entry (`az_eq14_level11`)

**Status:** defect confirmed; correction Sym²-verified; one term-confirmation item
open (NEEDS-HUMAN). **Date:** 2026-07-24. **Author tier:** T1 (Opus 4.8).

Per `epistemic-guardrails` F6 discipline (disclose, don't silently overwrite): the
frozen file `refs/sporadic_recurrences.json` (v1.4) is **left intact** for audit.
The corrected entry lives in a new file, `refs/sporadic_recurrences_v2.json`. This
document is the record of what was wrong and how it was fixed.

---

## 1. The defect (certain)

`sporadic_recurrences.json` is marked `status: FROZEN` but is imported by **zero**
code in the repo (grep-confirmed), so its order-3 entry was never executed. Its
`az_eq14_level11` recurrence string, evaluated faithfully with exact arithmetic,
is **non-integral at k=1**:

```
initial [1, 5];  ((2k+1)(11k²+11k+5)·s[-1] + k³·s[-2]) / (k+1)³
 → 1, 5, 25, 1015/4, …      (1015/4 is not an integer)
```

The tail term `+ k³·s[-2]` is wrong in both coefficient and sign. The order-2
partner `zagier_b_level11` is **fine** — it is Apéry `bₙ`, `(A,B,λ)=(11,−1,3)` — but
must be iterated with the `kstart=1` convention (compute `b_{n+1}` from `bₙ,b_{n-1}`
starting at n=1); iterating from k=0 yields a different, wrong sequence.

## 2. The correction (literature-grounded, Sym²-verified)

Source: **Gorodetsky, arXiv:2102.11839v2** (in `refs/papers/`, SHA256 recorded in
`refs/README.md`), the Almkvist–Zudilin / Cooper order-3 family, eq. (1.7):

```
(n+1)³ u_{n+1} = (2n+1)(a n² + a n + b) u_n − (c n³ + d n) u_{n-1},   u_0=1, u_1=b
```

The intended entry is the **η** row, `(a,b,c,d) = (11, 5, 125, 0)` — consistent with
the tabulated `(11,5,125)` already noted in `refs/README.md`, with `a=11, b=5`, and
initial `[1,5]` (since `u_1=b=5`). The `−125·n³` tail is the **only** sign that keeps
the sequence integral (a `+125` tail is non-integral at n=1). Corrected sequence:

```
1, 5, 35, 275, 2275, 19255, 163925, 1385725, 11483875, 91781375,
688658785, 4581861025, 22550427925, −8852899375, −2431720493125, …
```

**What is verified (Tier A/B, machine-checked):** this sequence is the correct
symmetric-square partner of Apéry `bₙ = (11,−1,3)` under the Gorodetsky identity
`Σ_n u'_n·wⁿ⁺¹ = (−x)·F_b(x)²`, `w=−x/(1−11x−x²)` — confirmed exact to x⁴⁰ by
`checkers/check_C3_sym2.py` (golden test `D↔eta`). This is the property the repo's
downstream C3/C3b criteria actually consume.

## 3. Open item (NEEDS-HUMAN / T0)

The recurrence sequence takes **negative** values from n=13, unlike a positive
sporadic combinatorial sequence. Two things could not be independently pinned here
and must not be guessed:

- No all-positive OEIS entry matches the prefix; the nearest match **A229111** is a
  *signed* g.f.-transform sequence that agrees for only 13 terms (it is **not** this
  sequence).
- The η closed form in the Gorodetsky table
  (`Σ_k (−1)^k C(n,k)³ (C((4n−5k)/3,n)+C((4n−5k−1)/3,n))`) could not be transcribed
  from the PDF into an integer-valued generator here (the naive transcription yields
  non-integers), so it did not serve as an independent cross-check.

**Action:** a human/T0 with the primary Almkvist–Zudilin source (or Cooper 2012,
already the paywalled NEEDS-HUMAN item in `refs/README.md`) should confirm the exact
η term values and whether the canonical η sporadic sequence is signed. Until then the
v2 entry is labeled `term_confirmation: PENDING`, and its *Sym²-partner* role — the
only thing C3/C3b use — stands on the x⁴⁰ machine check.

---

`Generated-by: Claude Opus 4.8 (T1) | Verified-by: exact-arithmetic defect reproduction; Sym² identity to x⁴⁰ (checkers/check_C3_sym2.py D↔eta); Gorodetsky arXiv:2102.11839 recurrence family | Reviewed-by: pending T0`
