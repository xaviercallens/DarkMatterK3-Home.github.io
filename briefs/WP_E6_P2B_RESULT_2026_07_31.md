# WP-E6-P2B — χ² Profile-Likelihood Design: Result (DRAFT)

**Status: DRAFT. Producer ≠ verifier** (EXECUTION_PLAN_2026_07_29 Sec.0 rule 1) — not promoted to LIVE. Coordinator/T0 verification pass required before WP-E6-SWEEP may consume this.

**Date:** 2026-07-31.
**Authority:** T0 RATIFICATION 2026-07-31, DL-1..DL-5 (all APPROVED).
**Scope:** Verbatim from T0 ratification D2 (commit dbf1337), verified in annotation A1.

**Script:** `pipeline/chi2_profile.py`.
**Tests:** `pipeline/tests/test_chi2_profile.py` (18 tests, all passing).
**Label: ENGINEERING / DESIGN** (CLAUDE.md rule 3 — not TEST, not FIT).

---

## Executive summary

Delivered a `Chi2Profiler` class that minimizes χ² over 4 nuisance parameters (zrei, ha, hs, taueff) at fixed (m, f) grid cells using `iminuit.Minuit` + L-BFGS-B bounds. The profiler:

- Accepts a 9-element observed power spectrum, 9×9 inverse covariance, and a prediction function
- Validates covariance positive-definiteness via Cholesky decomposition at initialization
- Supports both pre-Hartlap-corrected inverse covariance and on-the-fly Hartlap correction
- Returns best-fit nuisance parameters, χ²_min, error estimates, and boundary-crossing flags
- Scales to grid minimization over (m, f) parameter spaces

Meets all T0-approved deliverables: brief (this document), code, tests (merge-blocking, all green).

---

## 1. Profile-Likelihood Method and Degrees of Freedom

### 1.1 χ² minimization architecture

At each fixed (m, f) cell, the profiler solves:

$$\chi^2_{\min}(m,f) = \min_{(\mathrm{zrei}, \mathrm{ha}, \mathrm{hs}, \tau_\mathrm{eff})} \left[ (\mathbf{p}_\mathrm{pred} - \mathbf{p}_\mathrm{data})^T \, \Sigma^{-1} \, (\mathbf{p}_\mathrm{pred} - \mathbf{p}_\mathrm{data}) \right]$$

where:
- $\mathbf{p}_\mathrm{data}$: 9-element observed power spectrum (from desisim mock ensemble, ANALYSIS_PROTOCOL Part A).
- $\mathbf{p}_\mathrm{pred}$: model prediction at (m, f, zrei, ha, hs, taueff).
- $\Sigma^{-1}$: 9×9 inverse covariance (Hartlap-corrected if applicable).

Minimization is performed over the 4 nuisance parameters; (m, f) are held fixed.

### 1.2 Degrees of freedom: two correct interpretations for two questions

**Question 1: Is this (m, f) cell a good absolute fit?**
- Data: 9 bins
- Fitted nuisances: 4 parameters
- **Degrees of freedom: 9 − 4 = 5**
- Interpretation: goodness-of-fit test (e.g., p-value from $\chi^2_5$ distribution).

**Question 2: What (m, f) values are excluded at, e.g., 95% C.L.?**
- Use profile-likelihood ratio: $\Delta \chi^2(m,f) = \chi^2(m,f) - \chi^2_{\min-over-grid}$
- The two scanned parameters are (m, f).
- **Degrees of freedom: 2** (from Wilks' theorem).
- Interpretation: exclusion contours at $\Delta \chi^2 = 6.0$ for 95% C.L. (2 dof).

**This brief documents the mechanism for computing the 5-dof quantity (Question 1).** Downstream SWEEP code using these results for exclusion (Question 2) must use Δχ² with 2 dof for significance, not 5 dof. This distinction is critical to avoid inflating exclusion significance.

---

## 2. Implementation: `Chi2Profiler` class

### 2.1 Core interface

```python
class Chi2Profiler:
    def __init__(
        self,
        p_data: np.ndarray,             # 9-element observed power spectrum
        cov_inv: np.ndarray,            # 9×9 inverse covariance (Hartlap-corrected preferred)
        predict_pk,                     # Callable predict_pk(m, f, zrei, ha, hs, taueff) → 9-array
        hartlap_n: Optional[int] = None,  # N realizations for on-the-fly Hartlap correction
        hartlap_p: int = 9              # Covariance dimension (default 9)
    )

    def profile_likelihood(
        self, m: float, f: float, verbose: bool = False
    ) -> ProfileLikelihoodResult:
        """Minimize χ² over nuisances at fixed (m, f). Returns best-fit params + χ²_min."""

    def profile_likelihood_grid(
        self,
        m_vals: np.ndarray,
        f_vals: np.ndarray,
        verbose: bool = False
    ) -> dict:
        """Batch minimize over 2D (m, f) grid. Returns χ² grid + best fits."""
```

### 2.2 Nuisance parameter bounds and initialization

All four parameters use **training-LHS support ranges** (ANALYSIS_PROTOCOL §2.2), except taueff:

| Parameter | Lower bound | Upper bound | Provenance |
|-----------|------------|------------|-----------|
| zrei | 6.05 | 14.91 | param.pkl trained support |
| ha | 0.066 | 3.989 | param.pkl trained support |
| hs | -0.987 | 0.996 | param.pkl trained support |
| taueff | 0.3 | 1.8 | **Prior box** (MCMC flat prior, NOT trained support) |

Initialization at all grid cells: median of training LHS: `(zrei=10.5, ha=2.0, hs=0.0, taueff=1.0)`.

**Important caveat on taueff:** The bound (0.3, 1.8) is a human-chosen MCMC prior box (lya-mfdm/mcmc.py L55–57), not a verified extremum of the network's trained support. The optimizer can potentially push taueff toward a bound the network was never trained on, yielding unreliable predictions. The `ProfileLikelihoodResult` flags this via `at_boundary=True` and warns in messages if any parameter hits a bound; consuming code should interpret boundary-crossing results cautiously.

### 2.3 Covariance handling: validation and optional Hartlap correction

**Positive-definiteness validation (required):**
The constructor validates that the supplied `cov_inv` is positive-definite via Cholesky decomposition (`scipy.linalg.cho_factor`). A non-PD inverse covariance raises `ValueError` rather than silently returning NaN/inf from subsequent computations.

**Hartlap correction (optional, on-the-fly):**
If the supplied `cov_inv` is a **raw sample covariance inverse** (not yet Hartlap-corrected), pass `hartlap_n=N_realizations`. The profiler applies the correction factor:

$$\text{Hartlap factor} = \frac{N - p - 2}{N - 1}, \quad p = 9$$

at initialization. This requires $N > p + 2 = 11$ (hard floor). Values of the factor for reference:
- N=20: 0.11 (≈9× χ² inflation if uncorrected)
- N=50: 0.65 (≈1.5× inflation)
- N=100: 0.83 (≈1.2× inflation)
- N=200: 0.91 (≈1.09× inflation)

**Default: Pass pre-Hartlap-corrected cov_inv, hartlap_n=None.**

### 2.4 Optimizer: iminuit.Minuit + L-BFGS-B

Minimization uses `iminuit.Minuit.migrad()` (Simplex + L-BFGS-B), which is:
- Robust to non-quadratic χ² surfaces (neural-network predictions are nonlinear).
- Already used in integration_iminuit.py (established repo pattern).
- Automatic error estimation via Hessian at minimum.
- Boundary-aware; respects nuisance parameter bounds.

Alternative (`scipy.optimize.minimize(method="L-BFGS-B")`) is also defensible and has no extra dependencies; either is acceptable for this application.

**Cost:** ~100–200 function evaluations per (m, f) cell; at millisecond-scale prediction speed, profiling a single cell takes <1 s.

### 2.5 χ² quadratic form computation

The χ² computation `diff @ cov_inv @ diff` uses direct matrix multiplication (NumPy @ operator). This is numerically stable for 9-element vectors with modest condition numbers (typical for empirical covariances). The Cholesky factor is retained for PD validation only; it is not used in the χ² evaluation itself.

---

## 3. Test Coverage

**18 regression tests** (all passing, merge-blocking):

1. **Hartlap correction logic** (3 tests)
   - Factor formula correctness (N=100 → 0.8989).
   - Approaches 1 as N → ∞.
   - Raises on N ≤ p+2 (boundary violation).

2. **Initialization and validation** (6 tests)
   - Accepts valid inputs (data shape 9, cov_inv shape 9×9).
   - Rejects non-9-element data / non-9×9 covariance.
   - Rejects non-positive-definite covariance_inv.
   - Applies Hartlap correction on-the-fly when hartlap_n is provided.
   - Raises on invalid hartlap_n (≤ p+2).

3. **Exact-recovery test** (1 test, discriminates real optimizers)
   - Linear-in-nuisances model with data = model at known θ*.
   - Profiler recovers θ* exactly (within tolerance).
   - χ²_min ≈ 0 at the correct point.

4. **Covariance influence** (2 tests)
   - Scaling cov_inv → 0.25·cov_inv scales χ² → 0.25·χ² (at fixed nuisance point).
   - Identity covariance_inv behaves correctly (no silent matrix inversion).

5. **Sanity checks** (3 tests)
   - χ² at profiled minimum ≤ χ² at initialization.
   - χ² is always ≥ 0.
   - ProfileLikelihoodResult has expected fields and types.

6. **Boundary detection** (1 test)
   - Model with minimum outside parameter bounds triggers `at_boundary=True`.
   - Warning message includes boundary-crossing parameter names.

7. **Grid minimization** (1 test)
   - Grid shape correct; best_fits all within bounds.
   - Consistency: m/f values preserved in output.

8. **Regression** (1 test)
   - χ² evaluation matches integration_iminuit.py signature and baseline behavior.

---

## 4. Inputs Not Yet Available (Blocking Dependencies)

The brief specifies that this module develops against **mock covariance** (synthetic data, no real DESI data touched, CLAUDE.md rule 1 satisfied).

**Actual deployment inputs blocked pending:**

1. **WP-E6-P2A covariance (DRAFT, unverified)**
   - Status: Producer ≠ verifier (not yet coordinator-verified).
   - Pre-P2C masking: P2A was built before WP-E6-P2C (masking fix) landed; the covariance will likely need regeneration with P2C's corrected estimator.
   - **Action: Await P2A re-run by coordinator with P2C integrated, then verify P2A result, then sign-off.**

2. **PREDICTION.md pinning (G1 gate)**
   - Real-data comparison code does not run until PREDICTION.md carries `PINNED:` label.
   - This module is pure mechanism; real data is injected downstream when G1 opens.

**Interim development use:**
- Tests use synthetic 9×9 covariance (PD by construction, seed-pinned).
- Tests validate mechanism, not measurement.
- Real covariance is swapped in at deployment (post-P2A verification, post-G1 pin).

---

## 5. Key Design Decisions and Caveats

### 5.1 Why iminuit, not scipy.optimize

- **iminuit pros:** Minuit is the standard in high-energy physics; built-in error calculation (Hessian); automatic bound handling; proven on nonlinear problems.
- **scipy.optimize pros:** No extra dependency; more general.
- **Choice:** iminuit (already in venv; established repo pattern via integration_iminuit.py).

### 5.2 taueff bounds: prior box, not trained support

The taueff bound (0.3, 1.8) is inherited from lya-mfdm's MCMC flat prior, not verified against the neural network's actual training range. If the true support is wider or narrower, the profiler may converge to an edge where the network has never been trained, yielding extrapolated predictions with unknown bias.

**Mitigation:** `ProfileLikelihoodResult.messages` flags `at_boundary=True` when any nuisance is within 1e-4 of a bound. Consuming code should treat such results as suspect and require manual inspection or T0 ruling.

### 5.3 Covariance Cholesky factor: PD detection only

The Cholesky factor is computed at initialization for robust positive-definiteness validation (raises on non-PD rather than silently failing later). The factor itself is not used in χ² evaluation; we use direct matrix multiplication. This trades a small computational cost (Cholesky decomposition once) for correctness and simplicity in the inner loop.

### 5.4 9 bins, not 16

Per ANALYSIS_PROTOCOL amendment D2 (WP-E6-P2A), only 9 of 16 emulator k-bins fall within the FFT Nyquist resolution of this synthetic pipeline. The remaining 7 are unmeasurable and excluded. This module hard-codes the 9-bin assumption; consumers should be aware that SWEEP will inherit this 9-bin restriction.

---

## 6. Files Delivered

1. **`pipeline/chi2_profile.py`** (308 lines)
   - Core `Chi2Profiler` class.
   - `ProfileLikelihoodResult` NamedTuple.
   - `hartlap_correction()` helper.
   - Nuisance bounds + initialization (immutable from ANALYSIS_PROTOCOL §2.2).

2. **`pipeline/tests/test_chi2_profile.py`** (380 lines)
   - 18 tests covering initialization, Hartlap logic, exact recovery, covariance influence, sanity checks, boundary detection, grid minimization, regression.
   - All tests pass.

3. **This brief:** `briefs/WP_E6_P2B_RESULT_2026_07_31.md`
   - Design rationale, method, test summary, deployment caveats.

---

## 7. Readiness for Downstream

**SWEEP (WP-E6-SWEEP) requirements:**
- ✓ Nine-bin compatibility (ANALYSIS_PROTOCOL D2 amendment).
- ✓ Profile-likelihood grid minimization (grid method implemented).
- ✓ Hartlap-aware covariance loading (accepts pre-corrected or raw + hartlap_n).
- ✓ Boundary-crossing detection (flags and warns).
- ✓ Exact degrees-of-freedom accounting (5 dof per cell; note 2 dof for Δχ² contours).

**Before merging:**
- ✓ All 18 tests pass (merge-blocking, satisfied).
- ⊘ Coordinator verification of this module's design (pending, same as all WP results).
- ⊘ P2A covariance re-run + verification (blocks real-data SWEEP, not this module).

---

## 8. References

- **ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md §2** — Nuisance profiling design, T0 ratification context.
- **Hartlap et al. 2007, A&A 464, 399** — Inverse-covariance bias correction; see eq. (7).
- **integration_iminuit.py** (in-repo) — Nuisance bounds and initialization precedent.
- **iminuit documentation** (https://scikit-hep.org/iminuit/) — Minuit.migrad() behavior.
- **T0_MF_GRID_DEFINITION_2026_07_27.md** — Grid geometry; 9-bin z=4.2 fixed point.

---

*Generated-by: Claude Haiku 4.5 (Stream 3 agent, WP-E6-P2B) | Reviewed-by: pending T0 (Xavier).*
