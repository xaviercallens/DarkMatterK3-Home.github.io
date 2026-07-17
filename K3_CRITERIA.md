# K3_CRITERIA — Frozen Selection Criteria for K3 Vacuum Candidates

**Status:** SKELETON v0.1 — **NOT YET FROZEN**  
**Freeze target:** end of Phase 0 (week 2), as v1.0, jointly signed per the two-model rule (`EXECUTION_PLAN.md` §1.2.3) and by Xavier.  
**Repo of record:** `SocrateAI-Scientific-Agora-K3-DarkMatter`; hash-pinned copies in the other two repos at freeze.

> **Freeze semantics.** After v1.0 is frozen: (1) AutoEvolve may score candidates *only* through the checker scripts listed here; (2) no criterion, threshold, or weight may change except by a versioned amendment (§6) recorded *before* re-running any ranking; (3) every `TBD-AT-FREEZE` field below must be resolved with a literature citation or a first-principles computation — an unfilled TBD blocks the freeze.

---

## 1. Candidate Register

| ID | Sequence / family | Defining recurrence (source) | Order-2 partner claimed | Initial flags |
|---|---|---|---|---|
| K-s7 | Cooper s7 | TBD-AT-FREEZE: cite exact recurrence + paper/eqn | TBD-AT-FREEZE | `SYM2_UNVERIFIED` |
| K-s10 | Cooper s10 | TBD-AT-FREEZE | TBD-AT-FREEZE | `SYM2_UNVERIFIED` |
| K-S22 | Cooper S22 | TBD-AT-FREEZE | TBD-AT-FREEZE | `SYM2_UNVERIFIED` |
| K-t103 | t103 | TBD-AT-FREEZE | TBD-AT-FREEZE | `SYM2_UNVERIFIED` |

*Rule: a candidate without a citable defining recurrence at freeze time is dropped, not guessed.*

---

## 2. Criteria

Template per criterion: **Definition** (mathematically exact) · **Checking procedure** (first-principles, no LLM recall) · **Checker script** · **Pass threshold** · **Failure consequence** · **Tier**.

### C1 — Mirror-Map Integrality
- **Definition:** the mirror map q-expansion coefficients of the candidate's Picard-Fuchs operator, in the normalization fixed at freeze (state it explicitly), are integers up to order N₁.
- **Checking procedure:** compute the holomorphic solution and mirror map symbolically (Sage/sympy, exact rational arithmetic — no floats), expand to N₁ terms, test integrality.
- **Checker:** `checkers/check_C1_mirror_integrality.py` — deterministic; emits per-coefficient certificate JSON.
- **Threshold:** all coefficients integral for n ≤ N₁. **N₁ = TBD-AT-FREEZE** (proposed: 200; justify choice at freeze). *Note: finite-order integrality is evidence, not proof; report as `PASS(N₁)`, never `PASS`.*
- **Failure:** F1 removal.
- **Tier:** B → A(N₁-bounded) on pass.

### C2 — Kodaira Fiber Content
- **Definition:** the Weierstrass model associated to the candidate family (construction fixed at freeze, with citation) has singular fibers whose Kodaira types are all on the physical list, and the total fiber data is consistent with the Euler-characteristic/K3 constraint used downstream (state the exact constraint at freeze).
- **Checking procedure:** compute the discriminant and j-invariant of the Weierstrass model symbolically; apply Tate's algorithm at each discriminant component; tabulate types.
- **Checker:** `checkers/check_C2_kodaira.py` — outputs the fiber table as machine-readable JSON (this table is the *only* admissible source for fiber claims in any report).
- **Threshold:** exact — all fibers classified, none of excluded type, constraint identity satisfied.
- **Failure:** F1 removal.
- **Tier:** B → A on pass.

### C3 — Symmetric-Square Structure (from VISION §1.1, amendment A2)
- **Definition:** the candidate's order-3 operator L₃ equals Sym²(L₂) for an explicitly exhibited order-2 operator L₂ (equality of operators after the normalization fixed at freeze — state it).
- **Checking procedure (two independent routes, both required to clear the flag):**
  1. *Symbolic:* construct Sym²(L₂) explicitly and verify operator equality by exact coefficient comparison (`checkers/check_C3_sym2.py`).
  2. *Formal:* Lean statement `sym2_<candidate>` from Stream 1 WP S1-04; status auto-imported from the open-goal export.
- **Threshold:** route 1 pass clears `SYM2_UNVERIFIED` → `SYM2_SYMBOLIC`; route 2 kernel proof upgrades to `SYM2_PROVED`.
- **Failure:** symbolic route fails ⇒ F1 removal *for the dual-scale role* (the candidate may remain of independent mathematical interest, outside this program's physics).
- **Tier:** B → A on kernel proof.

### C4 — Lattice / Picard Data Consistency
- **Definition:** the candidate family's generic Picard rank and transcendental lattice data (as computable from the Sym²/Shioda-Inose structure, with the method fixed and cited at freeze) are consistent with the structural requirements the physics construction imposes. **The requirements themselves are TBD-AT-FREEZE and must be derived from the EFT-matching draft, not chosen to fit preferred candidates.**
- **Checking procedure:** TBD-AT-FREEZE — specify the computation (e.g., via the exhibited L₂'s modular parametrization) and its tool.
- **Checker:** `checkers/check_C4_lattice.py`.
- **Threshold:** exact match to the stated requirement.
- **Failure:** F1 removal.
- **Tier:** B.

### C5 — Swampland / Consistency Bounds
- **Definition:** the candidate's moduli-space data satisfies each listed bound, with **every inequality written out explicitly at freeze** (bound, normalization, O(1) constant convention, and citation). No bound may be invoked by name alone.
  - C5.1 — Distance-conjecture-type bound: statement TBD-AT-FREEZE.
  - C5.2 — (Optional) additional consistency conditions: enumerate or delete at freeze.
- **Checking procedure:** compute the relevant moduli-space quantities from the Picard-Fuchs data symbolically; evaluate each inequality with stated conventions.
- **Checker:** `checkers/check_C5_swampland.py` — reports margin, not just pass/fail.
- **Threshold:** per-inequality, stated at freeze. *Honesty note: Swampland bounds are themselves conjectural; a C5 result is always reported as "consistent/inconsistent with conjecture X under convention Y," Tier B ceiling — never Tier A.*
- **Failure:** flag `SWAMPLAND_TENSION`, score penalty per §4; removal only if the freeze designates the bound as hard.
- **Tier:** B (ceiling).

---

## 3. Checker Contract (applies to every `checkers/*.py`)

1. Exact arithmetic wherever mathematically possible; floats only with stated error bounds.
2. No network access; no LLM calls; inputs are the candidate register + fixed literature data files in `refs/` (each with SHA256 and source citation).
3. Deterministic and seeded; identical inputs ⇒ bit-identical certificate JSON.
4. Each checker ships with golden tests: one known-good control, one known-bad control (`EXECUTION_PLAN.md` S2-02).
5. Certificates are the only admissible evidence source for any table in any report.

---

## 4. Scoring (consumed by AutoEvolve)

- Hard criteria (fail ⇒ F1): **C1, C2, C3-symbolic** — TBD-AT-FREEZE: confirm the hard set.
- Soft criteria (margin-scored): C4, C5 — weights TBD-AT-FREEZE, fixed before any ranking run, hash-pinned with this file.
- Score formula: TBD-AT-FREEZE (proposed: lexicographic — hard criteria as gates, then weighted soft margins). AutoEvolve may not modify weights at runtime.

---

## 5. Live Status Table (auto-generated — do not edit by hand)

| Candidate | C1 | C2 | C3 | C4 | C5 | Flags | Verdict |
|---|---|---|---|---|---|---|---|
| K-s7 | — | — | — | — | — | `SYM2_UNVERIFIED` | pending |
| K-s10 | — | — | — | — | — | `SYM2_UNVERIFIED` | pending |
| K-S22 | — | — | — | — | — | `SYM2_UNVERIFIED` | pending |
| K-t103 | — | — | — | — | — | `SYM2_UNVERIFIED` | pending |

*Regenerated by `scripts/render_status_table.py` from checker certificates + the Stream 1 open-goal export. A hand edit here is a reportable integrity incident (VISION F6 spirit).*

---

## 6. Amendment Protocol

1. Amendments by PR with: motivation, exact diff, and an impact statement listing every prior ranking invalidated.
2. Any amendment adopted *after* a ranking run demotes that run's outputs from "selection" to "exploratory" in all reports.
3. Amendments arising from Deep Think adversarial memos (`EXECUTION_PLAN.md` S2-05) cite the memo.
4. Version history:

| Version | Date | Change | Rankings invalidated |
|---|---|---|---|
| v0.1 | 2026-07-17 | Skeleton | n/a (no runs permitted pre-freeze) |
| v1.0 | (freeze) | All TBD-AT-FREEZE resolved with citations; signed | — |

---

## 7. Pre-Freeze Checklist (blocks v1.0)

- [ ] Every `TBD-AT-FREEZE` resolved with citation or first-principles derivation — **no value entered from any model's memory** (`EXECUTION_PLAN.md` §6.1).
- [ ] All five checkers pass their golden tests in CI.
- [ ] C4 requirements derived from the EFT-matching draft (not reverse-engineered from candidates).
- [ ] Two-model sign-off (Fable 5 + Deep Think, independent readings) + Xavier signature.
- [ ] Hash pinned in all three repos.

---

## Related Documents

- **VISION.md** §2–§4: Epistemic framework (Tier A/B/C) and falsification branches.
- **EXECUTION_PLAN.md** §3: Stream 2 work packages (S2-01 through S2-05).
- **K3_SELECTION_REPORT.md** (to be generated in Phase 2): Results of ranking all candidates against these criteria.
