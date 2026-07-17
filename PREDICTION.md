# PREDICTION.md — Falsifiable Predictions of the Dual-Scale Model

**Status:** Draft v1.0 (July 2026)  
**Scope:** Applies to Stream 3 observational testing (`SocrateAI-Scientific-Agora-Home`)  
**Frozen date:** TBD (target: end of Phase 1, ~2026-09-17)  
**Last amendment:** None  

---

## Overview

This document states **at least one quantitative, falsifiable prediction** that distinguishes the dual-scale model from ΛCDM at a level resolvable by current or near-term public data.

**Status note (2026-07-17):** This is a **draft** document. The contents below are preliminary outlines; the prediction(s) will be finalized and frozen after careful consultation with astrophysics contacts (OCA Nice, SYRTE) in Phase 1.

The finalized version will be tagged with a frozen date, and any subsequent changes will require an amendment (see §5).

---

## 1. The Challenge

The dual-scale model posits:
- A global K3 vacuum (order-3 Picard-Fuchs, dark-energy-like).
- A local elliptic EFT (order-2 Picard-Fuchs, governing dark-matter halos).

**For this model to earn the right to be taken seriously**, it must make at least one prediction that:
1. Differs quantitatively from ΛCDM.
2. Can be tested against published data or data forthcoming within 12–18 months.
3. Is not a fitted parameter (i.e., stated *before* looking at the relevant data).

If no such prediction can be extracted, the model is **observationally degenerate** with ΛCDM (Tier C failure), and the project contracts to its mathematics (Tier A/B), which remains publishable.

---

## 2. Candidate Observables (To Be Narrowed)

The following observables are under consideration. **One or more will be selected and quantified in Phase 1.**

### 2.1 — Halo Profile Shape (Local Elliptic Sector)

**Motivation:** If the S12/S21 elliptic EFT governs the interior structure of dark-matter halos, the predicted density profile should deviate from NFW or Einasto in a measurable range.

**Observable:** The logarithmic slope of the density profile as a function of radius:
$$\frac{d \log \rho}{d \log r} \Big|_{r \in [0.1, 10] \, r_s}$$

**Data source:** Published weak-lensing stacked profiles from:
- SDSS (Mandelbaum et al., 2013, 2020)
- DES Y3 (Leauthaud et al., 2024)
- Euclid Early Release Observations (when available)

**Pre-registration:** The specific radial range and tolerance will be locked in before comparing to data.

### 2.2 — Stochastic Gravitational-Wave Background (Global K3 Sector)

**Motivation:** If the global K3 vacuum sources a scalar-induced contribution to the nHz stochastic background, its spectral index and amplitude must differ from a pure tensor background.

**Observable:** The spectral index $\alpha$ of the power-law fit to the free-spectrum posterior in the nHz band:
$$P(f) \propto f^\alpha$$

**Data source:** Published posteriors from:
- NANOGrav 15-year dataset (Agazie et al., 2023)
- EPTA Data Release 2 (Liu et al., 2023)
- Joint analysis (IPTA, when finalized)

**Pre-registration:** The predicted range for $\alpha$ (and 1σ error budget) will be stated before comparing to published posteriors.

### 2.3 — Matter Power Spectrum at Lyman-α Scales

**Motivation:** Any modification to dark-matter dynamics (local elliptic EFT) must preserve or only mildly suppress small-scale power.

**Observable:** The ratio of the predicted matter power spectrum $P(k)$ to the Λ-CDM template at $k \sim 0.1 \text{–} 1 \, h/\text{Mpc}$:
$$\frac{P_{\text{model}}(k)}{P_{\Lambda\text{CDM}}(k)} \quad \text{for} \quad k \in [0.1, 1] \, h/\text{Mpc}$$

**Data source:** Published Lyman-α constraints from:
- SDSS DR12 (Palanque-Delabrouille et al., 2015)
- DESI Early Data Release (2024)

**Pre-registration:** The allowed tolerance (e.g., ±5% or ±10%) will be stated and locked in Phase 1.

---

## 3. Selection Rationale (Draft)

**Currently under discussion with external reviewers:**

- **Halo profile** is the "hardest" test — it requires the elliptic EFT to make a specific, non-trivial prediction about structure on scales where dark matter is the dominant component. If this test fails, the local sector is falsified (VISION.md §4, F3).

- **Stochastic background** is more speculative (depends on whether the K3 vacuum couples to gravity in a way that produces scalars), but has the advantage of being the most different from ΛCDM if it exists.

- **Lyman-α power** is a "null test" — if the model cannot preserve small-scale power, it is disfavored, though not necessarily falsified at 3σ. This is a robustness check rather than a primary discriminant.

**Phase 1 task:** Consult with astrophysicists to narrow to one or two observables with clear error budgets.

---

## 4. No-Prediction Branch

If, after honest effort in Phase 1, no observable can be formulated that differs from ΛCDM by more than the statistical uncertainty in current/near-term data, the **no-prediction branch** (VISION.md §3) is triggered:

- The dual-scale model is documented as **observationally degenerate** with Λ-CDM.
- The project is reframed as a **mathematical investigation**: the formal properties of K3/elliptic geometries and their arithmetic (Tier A/B results).
- All Tier C (physics) claims are removed from the repositories or clearly marked as speculative.
- The mathematical results are submitted for peer review in the modular-forms community.

This outcome is not a failure — it is a documented result that contributes to our understanding of the boundary between mathematics and physics.

---

## 5. Amendment Procedure

**Before freezing (status = draft):**
- Predictions may be added, removed, or substantially revised without a formal amendment, provided rationale is documented in the git log.

**After freezing (status = frozen):**
- Any change to a frozen prediction (quantitative value, error budget, data source) requires a PR with external review.
- Parameter changes made *after* comparing to data are logged in `TUNING_LOG.md` (VISION.md §4) and the affected comparison is demoted from "test" to "fit".
- **Predictions cannot be weakened** (error bars cannot be widened, null regions cannot be retracted) without a major version bump.

---

## 6. Changelog

- **v1.0-draft (2026-07-17):** Initial draft. Three candidate observables outlined (halo profile, stochastic background, Lyman-α power). Data sources and pre-registration strategy sketched. Ready for Phase 1 consultation with external reviewers. Author: Xavier Callens.

---

## Related Documents

- **VISION.md** §3–§4: Why falsifiable predictions are essential; falsification branches (F1–F6).
- **K3_CRITERIA.md:** Frozen criteria for K3 candidate ranking (Stream 2).
- **PREDICTION_REVIEW_LOG.md** (to be generated in Phase 1): Notes from consultation with external reviewers, rationale for final selection.
- **OBSERVATIONAL_REPORT.md** (to be generated in Phase 3): Results of comparing predictions to public data.
- **NO_PREDICTION_BRANCH.md** (conditional): If no observable can be extracted, this document is generated to formalize the transition to a mathematics-only project.
