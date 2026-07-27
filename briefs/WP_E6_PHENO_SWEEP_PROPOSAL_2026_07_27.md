# WP-E6 Proposal — Phenomenological Parameter Sweep (Exclusion Bounds)

**Status:** DRAFT — requires T0 (Xavier) sign-off before any code or any PREDICTION
amendment. Nothing in this document authorizes a real-data comparison.
**Date:** 2026-07-27
**Origin:** external strategic recommendation ("Phenomenological Pivot", Step 4), received
from T0 2026-07-27; reconciled in
`briefs/EXTERNAL_UNBLOCK_PLAN_RECONCILIATION_2026_07_27.md` (Stream 2 repo). T0 has also
indicated new data/experimentation has been identified (specifics pending — see Open
Question Q1).

---

## 1. What is proposed

F5b established that no exact top-down observable (m_φ, α_D, Λ_D) is derivable on current
state, and WP-E5 closed the 2D transverse route on data floors. This proposal pivots the
empirical program from *testing a single predicted mass* (impossible under F5b) to
*producing exclusion bounds*: a grid sweep over a mediator-mass interval, confronted with
public weak-lensing data products, outputting exclusion masks/contours.

- **Sweep variable:** mediator mass m_φ, log-spaced grid. Proposed placeholder interval
  10⁻²² – 10⁻¹⁹ eV (fuzzy-dark-matter-motivated; we conjecture its relevance [C] — the
  interval is an input choice to be fixed at pin time, not a derived quantity).
- **Output:** exclusion bounds ("masses in [X, Y] excluded at N σ by dataset D"), labeled
  **exclusion/FIT** — never TEST — because no pinned prediction selects a mass.
- **Honest framing (binding):** this is a phenomenological constraint program. It does not
  test the dual-scale hypothesis, it does not lift F5b, and a fully excluded grid would
  constrain the parameter space, not falsify the Tier A/B mathematics.

## 2. What this proposal is NOT

1. **Not a reopening of WP-E5.** The 2D transverse route's floors (~1.6 Mpc resolution,
   ~10⁴ objects per slice; best real field 50 objects) are unaffected by sweeping a
   parameter. Weak lensing is a different observable with its own (to-be-assessed) data
   adequacy question.
2. **Not a derivation.** Every run logs: "Parameters scanned phenomenologically (sweep);
   not derived (F5b stands)."
3. **Not an edit of any pinned document.** PREDICTION.md v1.1-PINNED (F5b, §6) stays as
   is. The sweep enters via a v2 amendment populated in `PREDICTION_v2_DRAFT.md` and
   pinned by T0 under the pin protocol, or not at all.
4. **Not a dark-energy program.** T0 decision D4 / A-DE stands: no vacuum-energy claims.

## 3. Preconditions before any code

1. **T0 sign-off on this proposal** (scope + interval + dataset).
2. **Data adequacy pre-flight** (the WP-E5 lesson, applied in advance): compute the
   floor — what mass range can dataset D actually exclude at what significance — on
   synthetic data BEFORE any real-data touch. If the answer is "none of the grid", that
   pre-flight result is filed and the WP stops there.
3. **Pre-registration:** the exclusion statistic, the grid, the dataset version/DOI, and
   the significance threshold are fixed in the v2 amendment before real data is read
   (gate G1 discipline; `prereg-pipeline` skill governs).

## 4. Open questions for T0

- **Q1 — the new data.** Which dataset(s) did you identify (survey, N objects, geometry,
  resolution, public product/DOI)? This determines the pre-flight and whether weak
  lensing is even the right observable to target first.
- **Q2 — dataset choice if weak lensing:** DES Y3, KiDS-1000, HSC — which public product?
- **Q3 — statistic:** what exclusion statistic (e.g. profile-likelihood on a halo-profile
  observable)? Must be fixed at pin time.
- **Q4 — relation to A.4.3:** the appendix's robustness protocol (β interval over the aᵢ
  box) could bound the sweep interval better than the FDM placeholder — worth deciding
  before pinning the grid.

## 5. Decision requested

T0 to: (a) approve/amend/reject this scope; (b) answer Q1–Q4; (c) if approved, authorize
building the synthetic-data sweep harness (rule 1-compliant) while the v2 amendment is
drafted.

---
Generated-by: Fable 5 (T1 coordinator) | Verified-by: consistency-checked against
NO_PREDICTION_BRANCH.md (F5b), WP-E5 floors (TODO.md Stream 2, WP_E5 docs), CLAUDE.md
rules 1–3, T0 decisions D2/D4 | Reviewed-by: pending T0 (Xavier)
