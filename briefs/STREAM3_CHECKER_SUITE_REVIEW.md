# Brief — Deep Think (T0s) Adversarial Review: Stream-3 Symbolic Checker Suite

**To:** Deep Think (T0s, two-model rule) + Xavier (T0 Owner)
**From:** Stream 3 (Opus 4.8, T1)
**Date:** 2026-07-24
**Subject:** Review of the C1/C3/C3b symbolic checker suite and the s7/s10 negative result
**Status:** built, tested (46 passing), tier-CI clean; **Reviewed-by: pending T0s**

---

## 0. What this is (and is not)

This is **pre-G1 mathematical verification infrastructure only** — exact symbolic
arithmetic on integer sequences and Picard–Fuchs operators. It touches **no
observational data** (gate G1 remains closed; `pipeline/gate.py` unchanged). It
is the honest form of "Stream 3 verifies Stream 1/2": mechanical checkers for the
`K3_CRITERIA.md` criteria, not an empirical claim.

It explicitly **supersedes** two directives that asked for a real-data GPU
pipeline (the "D-3 empirical rerun" and the "V5 GPU" briefs). Both described
artifacts that do not exist in this repo (no Lean output, no C1/C2/C3b
certificates, no galaxy catalog — only `data/nullbanks/mock_lensing_sdss.json`,
a mock) and asserted a cleared G1 that is still closed. See
`CORRECTION_NETRUNNER_FABRICATION.md` for the prior instance of this pattern.
Nothing in this suite consumes those directives.

## 1. Deliverables to review

| File | What it verifies |
|---|---|
| `checkers/check_C3_sym2.py` | C3: symmetric-square g.f. identity `Σ sₙwⁿ⁺¹=(−x)F(x)²`, `w=−x/(1−Ax+Bx²)` |
| `checkers/check_C3b_moduli_map.py` | C3b: period correspondence through explicit map F, `Π₃(F(x))=(1−Ax+Bx²)Π₂(x)²` |
| `checkers/check_C1_mirror_integrality.py` | C1: inverse mirror map `z(q)` integrality (Frobenius dual-number method) |
| `checkers/tests/test_c{1,3,3b}_*.py`, `test_refs_recurrences.py` | 46 golden/determinism tests |
| `scripts/render_criterion_status.py` → `docs/CRITERION_STATUS.md` | machine-generated C1/C3/C3b matrix |
| `refs/RECURRENCE_CORRECTION_order3.md`, `refs/sporadic_recurrences_v2.json` | WP-0 data fix (see §4) |

All parameters trace to Gorodetsky arXiv:2102.11839v2 (in `refs/papers/`,
checksum-verified). No sequence values are hard-coded; all are generated from
recurrence parameters and integrality-checked. Exact `Fraction`/dual-number
arithmetic throughout; deterministic; golden good+bad controls per checker.

## 2. The result to attack (Tier B — mathematics, no physical claim)

From `docs/CRITERION_STATUS.md` (machine-generated):

- Sporadic AZ pairs (γ, α, δ, η) **PASS** C1, C3, C3b.
- **Cooper s7, s10, s18 PASS C1** (integral mirror map → genuine MUM period
  operators) but **FAIL C3 and C3b**: as extended-family operators (d≠0) they
  have no Zagier order-2 partner under the Almkvist–Zudilin symmetric-square
  bijection. No closing Shioda–Inose map to the elliptic family exists (to the
  tested order).

**Consequence for the program:** any downstream statement that s7/s10 are
symmetric-square / Shioda–Inose K3 partners of an elliptic order-2 family is
**unsupported by these checks**. This directly bears on `PREDICTION.md`'s C3b
provenance requirement and on the K3-candidate story.

## 3. Adversarial targets (please try to break)

1. **Is the C3 identity the right formalization of "L₃=Sym²(L₂)"?** Note the
   *same-variable* operator equality fails even for known Sym² pairs — the
   variable change `w` is load-bearing. Attack whether the g.f. identity +
   variable change is the correct/complete C3 statement, or whether C3 should be
   split from the map more cleanly.
2. **Could s7/s10 be Sym²/Shioda–Inose partners under a map this suite does not
   test?** The suite tests the AZ-bijection order-2 family only. Is there a
   different order-2 object (not in `ORDER2_ZAGIER`) for which s7/s10 close? If
   so, C3/C3b as implemented is too narrow — propose the missing partner.
3. **Normalization of C1.** The mirror-map normalization is fixed in-file (`z(q)`
   integrality). K3_CRITERIA.md C1 leaves `N₁` and the normalization
   `TBD-AT-FREEZE`. Confirm or amend the chosen normalization; set `N₁`.
4. **Golden-bad realism.** C1 bad controls are perturbed operators; C3/C3b bad
   controls are wrong-partner pairs. Are these strong enough negative controls,
   or is a checker passing something it should reject?

## 4. Open item requiring a ruling (NEEDS-HUMAN / T0)

`refs/sporadic_recurrences.json` v1.4 (`FROZEN`, consumed by zero code) had a
defective order-3 entry (non-integral at k=1). WP-0 documents it and adds a
Sym²-verified correction (η=(11,5,125)) in `refs/sporadic_recurrences_v2.json`,
**keeping v1.4 intact** (F6 discipline). Unresolved: the corrected recurrence
takes negative values from n=13 and no all-positive OEIS entry matches; the η
closed form could not be transcribed reliably from the PDF. **Needs** the primary
Almkvist–Zudilin source (or Cooper 2012, already the paywalled NEEDS-HUMAN item)
to confirm exact η term values. Labeled `term_confirmation: PENDING`.

## 5. Acceptance criteria (T0s sign-off)

- [ ] C3/C3b/C1 formalizations match the intended `K3_CRITERIA.md` criteria (or
      amendments logged, versioned).
- [ ] s7/s10 negative result confirmed or refuted by an independent route.
- [ ] C1 `N₁` and normalization fixed for the freeze.
- [ ] WP-0 η identification resolved or accepted as PENDING with the ruling
      recorded.
- [ ] No tier violations (already: `scripts/check_tier_language.py` clean).

---

`Generated-by: Claude Opus 4.8 (T1) | Verified-by: checkers/tests/ (46 passing), tier-language CI clean, Gorodetsky arXiv:2102.11839 | Reviewed-by: pending T0s`
