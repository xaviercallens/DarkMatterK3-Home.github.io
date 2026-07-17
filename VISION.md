# VISION — F-Theory Dual-Scale Topological Dark Sector Model

**Status:** Living document — v1.2 (July 2026)

**Applies to all three repositories:**

| Repository | Stream | Role |
|---|---|---|
| `SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal` | 1 — Theory | Formal mathematics (Lean 4) |
| `SocrateAI-Scientific-Agora-K3-DarkMatter` | 2 — Selection | AutoEvolve K3 candidate ranking |
| `DarkMatterK3-Home.github.io` | 3 — Experimentation | Empirical confrontation with public data |

This file is mirrored in all three repos. The canonical copy lives in the LeanProposal repo; changes propagate by PR. Execution details live in `EXECUTION_PLAN.md`.

---

## 1. The Physical Architecture — Stated at Its Honest Strength

*(Rewritten in v1.2 per amendments A1–A3. Every clause below carries its epistemic tier inline: **[A]** established mathematics, **[B]** checkable-but-unproven, **[C]** physical conjecture. See §2 for tier definitions.)*

### 1.1 The mathematical substrate

Cooper's sporadic sequences exist, with documented recurrences, generating Picard-Fuchs-type ODEs, and modular parametrizations **[A]**. For certain families, order-3 operators arising as symmetric squares of order-2 operators are associated with one-parameter families of K3 surfaces, via constructions of Shioda-Inose type **[A, as a general mechanism]**. Whether each specific candidate in our list (s7, s10, S22, t103) realizes this structure — i.e., whether its order-3 operator is *exactly* the symmetric square of an order-2 operator, and whether the associated family satisfies every geometric property required downstream — is a **per-candidate checkable claim, not a global fact** **[B]**. It is criterion **C3** of `K3_CRITERIA.md`; candidates carry the flag `SYM2_UNVERIFIED` until Stream 1 discharges it (kernel-checked proof or symbolic verification).

### 1.2 The physical conjecture — clearly labeled

**We conjecture** **[C]** a dual-scale structure for the dark sector within an F-theory compactification:

- **Global sector (conjectured):** the UV-complete vacuum is governed by the closed-string moduli of a K3 geometry selected from the candidate list, with flux stabilization on this geometry accounting for dark-energy-like behavior. *No explicit flux stabilization for any candidate has been exhibited yet; producing one, or an honest obstruction, is Stream 1/2 work* **[C, unconstructed]**.
- **Local sector (conjectured):** dark matter halos are modeled by a local effective field theory associated with the elliptic-curve geometries (S12/S21). One possible string-theoretic realization is via localized 7-branes wrapping the relevant curves — but **this realization is currently a candidate mechanism, not a construction**. No worked matching from geometric data to 4D fields, masses, and couplings exists yet **[C, unconstructed]**.

### 1.3 What the mathematics does and does not buy us

If criterion C3 holds for a candidate, the symmetric-square relation establishes a **geometric relation between the K3 family and the elliptic family** **[A/B, per candidate]**. **It does not, by itself, imply any physical coupling, "locking," or dynamical relation between a bulk vacuum and a brane EFT** **[ruling, binding]**. Any claim that the global and local sectors are physically linked requires an explicit EFT matching — fields identified, couplings computed from geometric data, regime of validity stated. Producing at least one such worked matching (or documenting the obstruction) is the **Phase 1 blocker**: `PREDICTION.md` cannot be finalized without it, and if it cannot be produced, falsification branch **F5** (§4) triggers.

### 1.4 What would make this real

The conjecture earns physical standing only through the chain: *worked EFT matching → quantitative prediction differing from ΛCDM → survival against public data* (§3). Until the first link exists, §1.2 is a research program, not a model of the universe, and must be described as such in every repo, talk, and abstract.

---

## 2. Epistemic Status — Read This First

Intellectual honesty is a design requirement of this project, not a disclaimer. Every claim in this program falls into exactly one of three tiers:

**Tier A — Exact Arithmetic Geometry.** Cooper's sporadic sequences exist; their generating ODEs and modular parametrizations are documented in the literature. The general mechanism relating symmetric-square order-3 operators to K3 families (Shioda-Inose-type constructions) is established mathematics. Work in this tier can be formalized and machine-certified. *(v1.2: the per-candidate Sym² claims are explicitly excluded from this tier until verified — they are Tier B, tracked as criterion C3.)*

**Tier B — String Vacuum Consistency (checkable, unproven).** That specific candidates (s7, s10, S22, t103) satisfy every criterion required for the physical construction — Sym² structure (C3), mirror-map integrality, physical Kodaira fiber content, Picard-rank conditions, Swampland bounds — is *conjectured*, not proven. Streams 1 and 2 exist to move claims from Tier B to Tier A (proof) or to falsification branch F1 (disproof).

**Tier C — Cosmological Phenomenology.** The identification of any of these geometries with the actual dark sector of our universe is a **speculative physical hypothesis**, currently unsupported by observational evidence and currently lacking even a worked EFT matching (§1.3). It earns the right to be taken seriously only by generating 4D predictions that (a) differ from ΛCDM and (b) survive confrontation with data. Stream 3 exists to test — and potentially falsify — Tier C.

No document, README, talk, or manuscript produced under this program may present a Tier C claim in Tier A language. Reviewers of any PR are asked to enforce this. Epistemic-tier rulings are logged in `TIER_LEDGER.md` (see `EXECUTION_PLAN.md` §5.1).

---

## 3. North Star: One Falsifiable Prediction

**The single most important deliverable of this program — before any pipeline, proof, or paper — is a short technical note (`PREDICTION.md`) stating at least one quantitative prediction of the 4D EFT that differs from ΛCDM at a level current or near-term public data can resolve.**

`PREDICTION.md` must contain, as a precondition (amendment A3), **the worked EFT matching of §1.3**: the derivation chain from geometric data to observable, with every step's assumptions listed.

Candidate observables (to be narrowed to at least one concrete number with error budget):

1. **Halo profile shape.** If the local elliptic EFT mediates dark-sector self-interactions, the predicted cross-section (possibly velocity-dependent) must yield a specific cored departure from NFW in a specified radial range and halo-mass regime, testable against published weak-lensing stacked profiles (SDSS, DES, Euclid DR).
2. **Stochastic background spectral shape.** If the global sector sources an ultra-light scalar contribution to the nHz background, its spectral index and amplitude must be stated and compared against published NANOGrav 15-yr / EPTA DR2 free-spectrum posteriors. We compare against *public data products*; we do not claim collaboration or submission.
3. **Small-scale power.** Any ultra-light degrees of freedom modifying the matter power spectrum at Lyman-α scales must be quantified and checked against published constraints.

**Rule:** if after honest effort no such prediction can be extracted — i.e., the model is observationally degenerate with ΛCDM everywhere we can currently measure — that is itself a documented result (`NO_PREDICTION_BRANCH.md`), and the program's ambition contracts to its Tier A mathematical content, which remains publishable on its own merits.

---

## 4. Falsification Branches

Each branch below is a *pre-committed* response to a possible outcome. Writing them down now prevents post-hoc rationalization later.

| ID | If we find… | Then we… |
|---|---|---|
| F1 | A Cooper candidate fails a K3 criterion (non-integral mirror map, wrong Kodaira content) | Remove it from the candidate list permanently; document in `K3_SELECTION_REPORT.md`. No re-admission without a new proof. |
| F2 | No candidate survives all K3 criteria | The "global K3 vacuum" hypothesis is dead in its current form. The math results still publish; the physics claim is retracted from all repos. |
| F3 | The halo-profile prediction is excluded by weak-lensing data at ≥3σ | The local elliptic EFT sector is falsified. Document in `OBSERVATIONAL_REPORT.md`; no post-hoc parameter tuning to evade the exclusion. |
| F4 | The PTA spectral prediction is excluded by published posteriors | The global scalar channel is falsified. Same rule: no post-hoc tuning. |
| F5 | No worked EFT matching can be produced (§1.3 blocker), or the model is degenerate with ΛCDM on all accessible observables | Trigger `NO_PREDICTION_BRANCH.md` (§3). Reframe project as mathematics + methodology. |
| F6 | Lean formalization uncovers an error in a claimed Tier A/B result | The error is announced in the affected repo's README within one week. Formal verification only has value if its failures are as public as its successes. |

**Parameter-tuning policy:** any change to a model parameter made *after* seeing the data it is compared against must be logged in `TUNING_LOG.md` with date and justification, and the affected comparison is demoted from "test" to "fit" in all reporting.

---

## 5. The Three Streams

### Stream 1 — Theory (Lean 4 formalization)
**Repo:** `SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal`

Goal: machine-certify the Tier A mathematics and push Tier B claims into Tier A (or into F1).

Honest scoping: Mathlib does not currently contain the algebraic-geometric machinery (K3 surfaces, Weierstrass fibrations, Kodaira classification) needed for a direct proof of a statement like `cooper_s7_is_K3`. Realistic near-term targets are **arithmetic and analytic**:

- Formalize the Cooper recurrences and their defining ODEs as holonomic objects, with literature citations attached to every definition.
- Prove structural properties per candidate: the Sym² relation (criterion C3), integrality of solution sequences, congruence properties. Unproven cases are exported as named open goals — never silently assumed.
- State (with `sorry`-free *statements* and quarantined, documented axioms) the bridge conjectures linking the arithmetic to K3 geometry, making the proof obligations machine-readable.

Full geometric formalization is a long-horizon goal (12–24 months+), possibly a Mathlib contribution in its own right — publishable independently of any physics outcome. Work packages, model routing, and validation gates: `EXECUTION_PLAN.md` §2.

### Stream 2 — K3 Candidate Selection (AutoEvolve)
**Repo:** `SocrateAI-Scientific-Agora-K3-DarkMatter`

Goal: rank candidates (s7, s10, S22, t103) against the **frozen `K3_CRITERIA.md`**.

The criteria list is frozen in week 1, *before* any ranking runs, so that Streams 1 and 3 proceed against a stable interface and the ranking cannot be quietly re-weighted toward a preferred answer. Criteria changes require a versioned amendment with rationale. Every criterion has a symbolic checker computing values from first principles; AutoEvolve searches and scores strictly through these checkers. "The model preferred it" is never, by itself, evidence. Work packages: `EXECUTION_PLAN.md` §3.

### Stream 3 — Experimentation (public-data confrontation)
**Repo:** `DarkMatterK3-Home.github.io`

Goal: confront the predictions of §3 with **published, public datasets** — SDSS/DES/Euclid lensing products, NANOGrav 15-yr / EPTA DR2 posteriors, Lyman-α constraints.

Design rules:
- The V5 pipeline consumes the frozen `K3_CRITERIA.md` and `PREDICTION.md`; it does not define them.
- Every comparison is a **pre-registered test** (prediction hash-pinned before data contact, auditable in git history) or explicitly labeled a **fit**.
- Null results and exclusions are first-class outputs, reported with the same prominence as positive results.

Work packages: `EXECUTION_PLAN.md` §4.

---

## 6. Roadmap (sequenced, realistic for a solo effort)

**Phase 0 — Interfaces (weeks 1–2):** this file (v1.2) mirrored; `K3_CRITERIA.md` frozen; `EXECUTION_PLAN.md` adopted; Stream 1 CI skeleton green.

**Phase 1 — The prediction gate (months 1–2):** the worked EFT matching (§1.3) and `PREDICTION.md`, hash-pinned. If the matching cannot be produced: F5, documented. Milestone **M1**.

**Phase 2 — The mathematics (months 2–8):** Stream 1 arithmetic formalization (C3 per candidate, integrality, congruences); Stream 2 ranking → `K3_SELECTION_REPORT.md`; arXiv preprint on the mathematics alone. Milestone **M2**. Publishes regardless of physics outcome.

**Phase 3 — The confrontation (months 8–14):** Stream 3 pre-registered comparisons; `OBSERVATIONAL_REPORT.md` with mechanical pass/fail against §3–§4. Milestone **M3**.

**Phase 4 — Reporting (months 14–18):** manuscripts, venue chosen by result strength. A clean exclusion is a paper; a degenerate model is a shorter paper plus the math paper; a surviving prediction is a bigger paper.

Horizon for a single owner: **~18–24 months**. Compression comes from de-scoping via the falsification branches, never from weakening §§2–4.

---

## 7. Collaboration & External Review

- **Mathematics:** seek review from the modular-forms / mirror-symmetry community and the Lean/Mathlib community (Zulip) before claiming Tier A status for any nontrivial result.
- **Astrophysics:** OCA Nice / SYRTE contacts are invited as *critics first* — the most valuable external contribution at this stage is someone trying to break the prediction, not endorse it.
- **PTA comparisons** use only published data products; we cite the collaborations' releases and do not imply endorsement or joint work.

---

## 8. Governance of This Document

- Amendments by PR to the canonical copy (LeanProposal repo), with a changelog entry below.
- The falsification branches (§4) and the honesty rules (§2) may be *strengthened* by amendment but never weakened.

**Changelog**
- v1.0 (2026-07-17): Initial version. Reordered roadmap to put falsifiable prediction first; rescoped Lean targets to arithmetic; replaced "submit to NANOGrav" with comparison against public posteriors; added tuning policy and falsification branches.
- v1.1 (2026-07-17): String-theoretic terminology pass (F-theory, Swampland framing).
- **v1.2 (2026-07-17): Amendments A1–A3 applied.** §1 fully rewritten with inline tier labels: physical "locking" claims removed and replaced by the explicit ruling that the Sym² relation implies no physical coupling absent a worked EFT matching (§1.3); Sym² demoted from asserted fact to per-candidate criterion C3 with `SYM2_UNVERIFIED` flag; 7-brane realization marked as candidate mechanism, unconstructed; the worked EFT matching designated the Phase 1 blocker, with F5 extended to cover its failure.
