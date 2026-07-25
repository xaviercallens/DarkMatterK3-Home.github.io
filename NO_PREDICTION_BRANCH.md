# NO_PREDICTION_BRANCH.md — F5b Triggered at S3-00 (2026-07-25)

**Status:** RECORDED — falsification-relevant result, not a failure of process
**Trigger:** F5b (`PREDICTION_APPENDIX_A.md §A.3.3`); consistent with F5 (`VISION.md §4`,
`PREDICTION.md §5`)
**Authority:** Xavier Callens (T0 Owner) — recorded following T0 review, 2026-07-25
**Scope:** WP S3-00 (MVM matching), gate M1 (`EXECUTION_PLAN.md`)

---

## 1. What was attempted

Following Stream 2's real, git-verified pin of `PREDICTION.md` (v1.0-PINNED,
`SocrateAI-Scientific-Agora-K3-DarkMatter` commit `8e16c44`, mirrored into this repo at
commit [this commit]) and Stream 3's authorization to proceed to Phase 2 (D-3 empirical
rerun), an attempt was made to complete WP S3-00: derive m_φ, α_D, Λ_D from the K3 period
geometry of the selected candidate (cooper_s7 / OEIS A183204, order-2 partner A279619),
per the MVM (Minimal Viable Matching) procedure specified in `EXECUTION_PLAN.md` and
templated in `PREDICTION_APPENDIX_A.md`.

This derivation is the pre-registered, mandatory prerequisite for any real-data
comparison (P1 PTA or P2 lensing, `PREDICTION.md §3`): without m_φ, there is no way to
select an observable branch or compute a predicted signal to compare against SDSS,
Euclid, NANOGrav, or EPTA data.

## 2. What is certified (Tier A/B) vs. what is missing (Tier C, unconstructed)

The candidate's **pure mathematics** is genuinely certified:

| Quantity | Status | Certificate |
|---|---|---|
| L₃ = Sym²(L₂) operator identity | PROVEN (Lean 4, kernel-verified) | `C3b_symsqrt_cooper_s7.json` |
| Picard rank ρ, transcendental rank T | ρ=4, T=18 (Shioda–Tate, exact) | `C2_cooper_s7_partner.json` |
| Kodaira fibre classification | 2× Type II, exponents [0, 1/2] | `C1loci_cooper_s7_partner.json` |
| Mirror map F(z_e) | Certified to q¹⁴ | `C3b_symsqrt_cooper_s7.json` |

None of this is in question. What `PREDICTION_APPENDIX_A.md` requires *beyond* this
geometric data are three physical coefficients, each needing an **explicit string
compactification** (flux quanta, brane wrapping, moduli stabilization) that has never
been constructed for this candidate — only its abstract K3/elliptic lattice data has been
computed:

| Ansatz | Needs | Status |
|---|---|---|
| **a₁** (Λ_D, confinement scale) | Explicit D7-brane gauge-kinetic normalization | Not constructed — no brane wrapping number fixed |
| **a₂** (m_φ, mediator mass) | Flux superpotential V_flux(z) built from actual flux quanta, so ∂²V can be taken at the certified z* | Only the map F(z_e) is certified; V_flux itself requires flux data not present |
| **a₃ / A-DE** (Λ_D vacuum energy, dark-energy identification) | Explicit flux/tadpole quanta satisfying D3-tadpole cancellation for this compactification, sign-checked ρ_vac > 0, magnitude-checked against ρ_DE,obs | Not constructed. `PREDICTION_APPENDIX_A.md §A.3.1` calls this "the most speculative part... an active research problem in string theory" and its own placeholder interval a₃ ∈ [10⁻¹⁰, 10⁻⁶] spans four orders of magnitude |

**No flux/tadpole data for this candidate exists in this repo, the Stream 2 repo
(`SocrateAI-Scientific-Agora-K3-DarkMatter`), or any document reviewed.** Nobody has
constructed an actual compactification — chosen flux integers, fixed (𝒱, g_s) via
genuine moduli stabilization, or verified tadpole cancellation — around the cooper_s7 K3.
Only its lattice and Sym² data have been certified.

## 3. Why a value cannot be honestly picked

Picking a specific number from a₃'s four-order-of-magnitude placeholder interval (or
similarly under-constrained a₁, a₂) to plug into a GPU batch run and label the result
`TEST` would be exactly the failure mode `PREDICTION.md §1` itself forbids:

> "Writing values here before that derivation would be numbers-from-memory — forbidden."

`PREDICTION_APPENDIX_A.md` is explicit that these are conjectural bounds awaiting real
derivation, not usable inputs: *"numbers are computed only at S3-00 pin time, using this
appendix as the formula template"* — and that template has not been filled in because the
underlying physics construction does not exist.

## 4. Mechanical trigger

Per `PREDICTION_APPENDIX_A.md §A.3.3` (A-DE discharge path):

> "If unavailable before M1 → **F5b** (no prediction), documented honestly in
> `NO_PREDICTION_BRANCH.md`."

a₃'s explicit flux/tadpole data is unavailable before M1. **F5b triggers.** This is
consistent with `VISION.md §4`'s F5 row (*"No worked EFT matching can be produced...
Trigger `NO_PREDICTION_BRANCH.md`. Reframe project as mathematics + methodology"*) and
`PREDICTION.md §5`'s kill condition (no observable relation survives (𝒱, g_s) elimination
without the missing coefficients).

## 5. What this is NOT

- **Not a failure of Streams 1/2's work.** The Sym² proof, Kodaira classification, and
  lattice computation are real, certified, and remain valid Tier A/B mathematical
  results regardless of this outcome.
- **Not a refutation of the physical hypothesis.** F5b means no prediction could be
  *extracted*, not that a tested prediction failed. The dark-sector-as-K3-compactification
  idea is neither confirmed nor falsified by this outcome — it is simply
  under-constructed at the level needed for an empirical test.
- **Not grounds to proceed with D-3 on placeholder/synthetic coefficients labeled as
  real.** Per gate G1 discipline, no such run occurred; no SDSS/Euclid data was fetched
  for this purpose; no GPU batch was executed.

## 6. What would unblock this

Per `VISION.md`'s own stated rule, this contracts the program's empirical ambition to its
Tier A mathematical content (Sym² proof, lattice classification), which "remains
publishable on its own merits" independent of any dark-matter physical claim. To reopen
S3-00, one of the following would need to exist:

1. **Explicit flux/tadpole construction** for a genuine F-theory compactification
   realizing the cooper_s7 K3 with D7-brane content — a substantial, separate piece of
   string-theory model-building, not a data-fetching or engineering task.
2. **Swampland-literature bound** on a₃ in place of explicit construction
   (`PREDICTION_APPENDIX_A.md §A.3.2`, third option) — weaker evidence, wide interval,
   but a real bound rather than a placeholder, requiring genuine literature-grounded
   derivation work (not fabrication of a plausible-sounding number).
3. **A different candidate** whose compactification *has* been explicitly constructed
   elsewhere in the literature, if one exists with a certified Sym² structure.

**Update 2026-07-25 (same day):** T0 elected to pursue option (1). Work package
`briefs/WP_S3-00b_FLUX_TADPOLE_CONSTRUCTION_BRIEF_2026_07_25.md` prepared and handed to
Deep Think (T0s, adversarial blind re-derivation) and Fable 5 (T0, primary construction)
per the project's Two-Model Rule. This section will be updated with the outcome.

## 7. Disposition

- `data/d3_runs/`, GPU T4 execution, and real SDSS/Euclid data fetch: **not performed**.
- `pipeline/D3_batch_runner_phase2.py`: remains in the repo as validated
  infrastructure/scaffolding (compiles, CLI tested) but its `_evaluate_sector()` method
  uses placeholder statistics and must not be run against real data or reported as a
  Gate E result until S3-00 is genuinely completed.
- Gate G1 (`PREDICTION.md` pin) remains open and valid — the pin itself is real and
  correctly records the pre-registration commitments (§2–§5); only the derived-quantities
  section (§6, reserved for v1.1) remains empty, as designed.

---

---

## 8. Resolution of F5b — WP S3-00b outcome (2026-07-25)

**Agents:** Fable 5 (T0, primary construction), Deep Think (T0s, adversarial blind
re-derivation). **Outcome:** Honest Off-Ramp 3 invoked — explicit construction failed after
genuine effort. **F5b stands.**

The attempt to construct exact values for a₁, a₂, a₃ from the certified cooper_s7 geometry
(ρ=4, T=18, 2× Type II fibres) was obstructed at three independent points. Full detail per
coefficient is in `PREDICTION_APPENDIX_A.md` A.1.4, A.2.5, A.3.4:

1. **The Type II veto (a₁).** The certified fibres are 2× Type II (cuspal), which under the
   Kodaira–Tate dictionary carry no gauge algebra — perturbative ADE enhancement starts at
   Type III. They do not supply the weakly coupled SU(N) dark sector the ansatz requires, and
   engineering one elsewhere needs the global fourfold X₄, which is unspecified.
2. **The flat-direction wall (a₂).** The order-3 Picard–Fuchs operator governs a rank-3
   sub-VHS, while the C2 certificate gives T = 18. Fluxing only the controlled subspace leaves
   18 − 3 = 15 moduli unstabilized — massless scalars that fifth-force bounds exclude.
3. **The topology void (a₃).** χ(X₄) depends on a threefold base B₃ that this program never
   specifies, so the D3 tadpole condition N_flux + N_D3 = χ(X₄)/24 is not merely unsatisfied
   but not posable. Choosing χ(X₄) to permit a KKLT-style uplift would be a fit dressed as a
   derivation (`.agents/AGENTS.md` Rule 7).

**Two-model status:** unified concurrence, no dispute — logged in `DERIVATION_DISPUTES.md`.
Deep Think's independent pass reached the same three obstructions and confirmed no numerical
fabrication was attempted.

### 8.1 What this work package *did* produce

One real, machine-checked result: the A.4 elimination algebra is now verified by
`scripts/verify_appendix_A4.py` (executed, assertions green). That verification **corrected two
errors** in A.4.2 as it had stood since 2026-07-18 — the sign of the a₃ exponent
(a₃^{+1/9} → a₃^{−1/9}, worth ≈60× in m_φ at mid-range a₃, against a one-decade branch window)
and the left-hand-side quantity (m_DM → Λ_D). Both are disclosed as F6 items in A.4.2. Neither
affected any published result, because F5b had already blocked every path to a number.

This is worth stating plainly: the verification found the errors *because* it was executed
rather than asserted. The relation had been carried as settled algebra for a week.

### 8.2 Proposed empirical pivot — NOT authorized, two blockers flagged

WP S3-00b proposed that the empirical pipeline pivot to testing parameterized correlations
(suggested example: weak-lensing κ peaks against Δ spikes) instead of exact mass targets.
**This is recorded as a proposal only.** Two blockers must clear first:

- **The suggested Δ observable is quarantined.** `ASSUMPTIONS.md` (v2.0-SIGNED) classifies the
  dashboard Δ figures as `[A-DATA-LEGACY]`: *"not reproducible from checkers in this repo
  today. Not usable in S3-00 or any pre-registered comparison until regenerated with
  manifest-pinned data."* Any pivot naming Δ collides with that quarantine directly.
- **A post-hoc pivot needs its own pin.** Substituting a new observable *after* the
  pre-registered path failed is precisely the move pre-registration exists to prevent. It
  cannot inherit the v1.0-PINNED commitment, which pinned a branch on m_φ. It would require a
  fresh pre-registration, pinned before contact with the data it proposes to use, and a
  written T0 ruling.

Neither blocker is cleared. Pivoting on the current basis would convert a clean negative
result into an unfalsifiable one.

### 8.3 Standing disposition (unchanged)

No GPU execution. No real-data fetch. Gate G1's pin remains valid and correctly records the
pre-registration commitments; `PREDICTION.md` §6 (derived quantities) remains empty, as
designed — and now for a documented reason.

**Update, same day — the constraint is now mechanical, not advisory.** This section previously
said `pipeline/D3_batch_runner_phase2.py` "must not be run." A written warning is exactly the
kind of thing a later session overlooks, and opening gate G1 had in fact already started
causing the pipeline to stamp placeholder computations `FIT`/`TEST`. Under a T0 ruling of
2026-07-25 a second gate now enforces this in code: **G1-L** requires *both* a valid pin *and*
hash-pinned §6 derived quantities before any output may carry a TEST or FIT label. Everything
else is `SYNTHETIC`, mechanically. The batch runner calls `require_derived_for_labels()` in
pre-flight and therefore now **refuses to start** (`GateError`, exit 1) rather than relying on
anyone reading this paragraph. Full ruling and cross-stream acknowledgement request:
`briefs/GATE_G1L_RULING_2026_07_25.md`.

Because F5b means §6 will not be populated on the cooper_s7 branch, G1-L will not open on this
branch. That is the recorded outcome, not an obstacle to be routed around.

The program's Tier A/B mathematical content — the kernel-verified Sym² identity, the Kodaira
classification, the Shioda–Tate lattice computation — is untouched by this outcome and stands
on its own merits, exactly as `VISION.md` §3 anticipated for this branch.

---

`Generated-by: Fable 5 (T0) WP S3-00b, session 2026-07-25 | Verified-by: cross-reference to
certificate files (C1/C2/C3b, both repos), PREDICTION_APPENDIX_A.md, VISION.md §4,
EXECUTION_PLAN.md S3-00, ASSUMPTIONS.md [A-DATA-LEGACY] entry; scripts/verify_appendix_A4.py
executed; Deep Think (T0s) adversarial concurrence | Reviewed-by: T0 N — pending Xavier review
of §8.2's two flagged blockers`
