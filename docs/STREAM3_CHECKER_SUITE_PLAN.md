# Stream 3 — Symbolic Checker Suite Implementation Plan (low-tier autonomous)

**Audience:** Haiku / low-tier executor working autonomously.
**Scope:** Build the mechanical checkers that let Stream 3 *verify Stream 1/2's
mathematical claims* — the honest meaning of "Stream 3 validates the theory."
**Hard boundary:** This is **pre-G1 mathematical work only** (exact symbolic
arithmetic on integer sequences and differential operators). It touches **no
observational data**. Do NOT write, fetch, or label anything with SDSS / Euclid
/ DES / weak-lensing / galaxy-catalog content — that path is gated by G1 and G1
is **closed** (`PREDICTION.md` has no `PINNED:` header; `pipeline/gate.py`
enforces it). See "Guardrails" at the bottom before writing a single line.

---

## 0. Why this plan exists (read once)

Stream 3's job is to confirm, by independent machine computation, the criteria
frozen in `K3_CRITERIA.md` (C1–C5). The reference implementation to copy is
already in the repo and passing:

- `checkers/check_C3_sym2.py` + `checkers/tests/test_c3_sym2.py` (C3, done).

Every checker in this suite follows that exact template:
1. Parameters/inputs come **only** from `refs/` literature (cite the file) or
   from another checker's certificate — **never** from model memory.
2. **Exact arithmetic** (`fractions.Fraction` or `sympy`, rational only; no
   floats except an explicitly error-bounded final margin).
3. Deterministic; identical input ⇒ bit-identical certificate JSON.
4. Ships a **known-good** and a **known-bad** golden control.
5. Reports finite-order results as `PASS(N)`, never bare `PASS`.
6. Emits a certificate JSON to `checkers/certificates/`; that certificate is the
   **only** admissible evidence for the criterion in any report.
7. Carries the provenance footer (see Guardrails).

Definition of done for the whole suite: `pytest checkers/tests/ pipeline/tests/`
green, every checker has both controls, and each criterion has at least one
certificate on disk. No prose interpretation — tables/certs only; flag T0 for
any interpretation.

---

## Work Package WP-0 — Fix the frozen order-3 recurrence (BLOCKER, do first)

**Definition.** `refs/sporadic_recurrences.json` (marked `FROZEN`, consumed by
zero code) has a defective order-3 entry `az_eq14_level11`: evaluated exactly it
produces `1, 5, 25, 1015/4, …` — non-integer at k=1. Its order-2 entry
`zagier_b_level11` is fine (it is Apéry `b_n`, `(A,B,λ)=(11,−1,3)`) but needs the
`kstart=1` iteration convention.

**Task.**
1. Do **not** silently edit a frozen provenance file. Instead write
   `refs/RECURRENCE_CORRECTION_order3.md` documenting: the exact defect, the
   literature-correct form from Gorodetsky arXiv:2102.11839 (in `refs/papers/`),
   and the corrected entry.
2. The literature-correct order-3 family (Gorodetsky eq. 1.7) is
   `(n+1)^3 u_{n+1} = (2n+1)(a n^2+a n+b)u_n − (c n^3 + d n) u_{n-1}`.
   The intended `(a,b,c)` for a Level-11 Apéry-like partner of `b_n` is the
   η row `(11,5,125)` (AZ, `d=0`). **Open subtlety to record, not paper over:**
   that recurrence produces `1,5,35,…,22550427925` then goes **negative** at
   n=13, so it is the signed *symmetric-square transform* sequence, not a
   positive sporadic sequence; there is no all-positive OEIS entry for the
   prefix. State this explicitly; do not assert a clean identification you
   cannot back with a term-by-term OEIS b-file cross-check.
3. Add a corrected JSON entry in a **new** file
   `refs/sporadic_recurrences_v2.json` (bump version, keep v1.4 intact for
   audit), with a `correction_of` field pointing at the defect and a
   `source` field citing the Gorodetsky table.

**Validation.** A test `checkers/tests/test_refs_recurrences.py` that: (a)
asserts the v1.4 `az_eq14_level11` is non-integral at k=1 (documents the defect
as a regression guard); (b) asserts the corrected recurrence is integral through
n=12 and matches `1,5,35,275,2275,19255,163925,1385725,11483875,91781375,
688658785,4581861025,22550427925`; (c) asserts `zagier_b_level11` with
`kstart=1` equals Apéry `b_n = 1,3,19,147,1251`.

**Note.** C3 (`check_C3_sym2.py`) already uses correct built-in parameters, so it
is **not** blocked by this WP. WP-0 is data-hygiene for the `refs/` file itself.

---

## Work Package WP-1 — C1: Mirror-map integrality checker

**Definition (K3_CRITERIA.md C1).** For a candidate order-3 operator, the
mirror-map q-expansion coefficients (in a fixed normalization) are integers up
to order N₁. Finite-order integrality is **evidence, not proof** → `PASS(N₁)`.

**Task.** `checkers/check_C1_mirror_integrality.py`:
1. From the candidate's Picard–Fuchs operator (build it from the recurrence
   parameters, same `theta = z d/dz` construction shown in
   `check_C3_sym2.py`'s docstring and in `refs/`), compute the holomorphic
   solution `y_0(z) = Σ a_n z^n` and a second solution `y_1 = y_0 log z + Σ …`.
2. Mirror map `q = exp(y_1/y_0)`; invert to `z(q) = q + Σ_{n≥2} m_n q^n`.
3. Test `m_n ∈ ℤ` for `n ≤ N₁`. Use exact `sympy.Rational` throughout; the only
   float allowed is `0` (exact). Emit per-coefficient certificate.

**Golden controls.** Known-good: a candidate whose mirror map is known integral
in the literature (cite it). Known-bad: a perturbed operator (change one
coefficient) whose mirror map has a non-integer at low order.

**Validation.** `PASS(N₁)` with `N₁` from `K3_CRITERIA.md` (default proposal 200,
justify in the certificate). Test: integrality holds for good, fails for bad,
determinism hash stable, margin (max denominator) reported.

---

## Work Package WP-2 — C3b: Shioda–Inose / mirror-map comparison checker

**Definition (K3_CRITERIA.md C3b).** For a C3-passing candidate, there is an
explicit map `F` (the change of variable `z = −x/(1 − A x + B x²)` already used
inside `check_C3_sym2.py`) relating the order-3 and order-2 families. C3b makes
that map a first-class, separately-certified object.

**Task.** `checkers/check_C3b_moduli_map.py`:
1. Given the exhibited order-2 `(A,B,λ)` and the order-3 `(a,b,c,d)`, construct
   `F: x ↦ z = −x/(1−A x+B x²)` as an exact rational function / q-series.
2. Verify the two families' mirror maps agree under `F` to order N (exact).
3. Emit certificate with `F` (as coefficients), agreement order, exact margin,
   tag `[A-ONT]` (the map is the *geometric* relation; per VISION §1.3 it is
   **not** by itself a physical coupling — say so in the certificate `note`).

**Golden controls.** Good: a bijection pair (e.g. `C↔alpha`, `D↔eta`) where the
map exists and closes. Bad: a non-bijection pair where no closing `F` exists →
`FAIL — no Shioda–Inose map`. Reuse the good/bad pair list from
`check_C3_sym2.py`.

**Validation.** Matching pairs `PASS(N)`, mismatches `FAIL`, determinism stable.
This is the checker the original `briefs/S2-01b.md` contract specifies; that
brief is the authority for edge cases (CONDITIONAL at order N, re-run at 2N).

---

## Work Package WP-3 — C2: Kodaira fiber content checker (heavier; sympy)

**Definition (K3_CRITERIA.md C2).** The Weierstrass model associated to the
candidate (construction fixed + cited at freeze) has singular fibers whose
Kodaira types are all on the physical list, consistent with the K3 Euler-
characteristic constraint.

**Task.** `checkers/check_C2_kodaira.py`: compute discriminant Δ and j-invariant
of the Weierstrass model symbolically; apply Tate's algorithm at each
discriminant component; tabulate types. Output the fiber table as JSON — this
table is the **only** admissible source for any fiber claim in any report.

**Golden controls.** A curve with a textbook fiber configuration (cite it) as
known-good; a smooth/degenerate control as known-bad. `TBD-AT-FREEZE` fields in
K3_CRITERIA.md C2 (the exact constraint identity) must be resolved with a
citation **before** this WP can report a real verdict — if still `TBD`, stop and
flag T0; do not invent the constraint.

---

## Sequencing

WP-0 (unblock refs) → WP-1 (C1) ∥ WP-2 (C3b) → WP-3 (C2). Each WP is
independently mergeable once its two golden controls and determinism test pass.

**Progress (2026-07-24):**
- **C3 — DONE.** `checkers/check_C3_sym2.py` + `test_c3_sym2.py`.
- **WP-0 — DONE.** `refs/RECURRENCE_CORRECTION_order3.md`, `refs/sporadic_recurrences_v2.json`,
  `checkers/tests/test_refs_recurrences.py`. (Open NEEDS-HUMAN item: independent
  term confirmation of the η sporadic sequence — see the correction doc §3.)
- **WP-2 (C3b) — DONE.** `checkers/check_C3b_moduli_map.py` + `test_c3b_moduli_map.py`;
  emits the explicit map F. (F is unique given the exhibited order-2, so no
  CONDITIONAL branch.)
- **WP-1 (C1) — DONE.** `checkers/check_C1_mirror_integrality.py` +
  `test_c1_mirror_integrality.py`; exact Frobenius dual-number mirror map,
  integrality of z(q). Golden-good = sporadic operators; golden-bad = perturbed
  operators (non-integral at q³).
- **Criterion matrix — DONE.** `scripts/render_criterion_status.py` →
  `docs/CRITERION_STATUS.md` (machine-generated C1/C3/C3b table).
- **WP-3 (C2 Kodaira) — TODO, BLOCKED** on the `TBD-AT-FREEZE` constraint in
  K3_CRITERIA.md C2 (needs a T0 ruling; do not invent it).

Full suite status: `pytest checkers/tests/` → 46 passed. Tier-language CI clean.

---

## Guardrails (violating any of these fails review)

- **G1 gate.** No observational-data code, filenames, or labels. If you find
  yourself importing anything that reads a survey catalog, stop — wrong plan.
- **No numbers from memory.** Every constant traces to a `refs/` file, a checker
  certificate, or a `sympy`/`Fraction` computation in-file. If you can't cite
  it, don't write it.
- **Tier discipline (`epistemic-guardrails`).** These checkers verify
  *mathematics* (Tier A/B). Do **not** write that a Sym²/Shioda–Inose relation
  "links", "locks", "couples", or "maps" bulk to brane physics, or that any
  result "predicts/establishes/shows/proves" a dark-matter statement. The
  geometric relation is not a physical coupling (VISION §1.3).
- **`PASS(N)` always.** Never bare `PASS` for a finite-order check.
- **Provenance footer** on every file you create:
  `Generated-by: <model/tier> | Verified-by: <verifier> | Reviewed-by: <T0 Y/N>`.
- **If a criterion FAILs or a needed value is `TBD-AT-FREEZE`,** that is a
  result to report, not a problem to code around. Emit the FAIL certificate and
  flag T0. A clean negative is a success of the program.

---

`Generated-by: Claude Opus 4.8 (T1) | Verified-by: C3 reference checker passing (checkers/tests/test_c3_sym2.py, 16/16); plan cross-checked vs K3_CRITERIA.md + briefs/S2-01b.md | Reviewed-by: pending T0`
