# ANALYSIS_PROTOCOL — DRAFT (WP-E6 Phase 2 Stats Design)

**Status: DRAFT. NOT a pin. Does not touch `PREDICTION.md`, `data/raw/`, or any pinned
artifact. Subject to T0 review before any downstream code depends on it.** Filename carries
the draft date deliberately (repo convention, cf. `T0_MF_GRID_DEFINITION_2026_07_27.md`
before its own T0 sign-off).

**Date:** 2026-07-28.
**Grid this protocol targets:** `briefs/T0_MF_GRID_DEFINITION_2026_07_27.md`, hash-anchor
commit `27cff4a`, 8×7 = 56 cells, z_str = "4.2" only. Grid controls PASSED
(`data/derived/wp_e6_grid_controls_report_2026_07_28.json`, commit `20c9494`).
**Epistemic label: ENGINEERING / DESIGN** (per `pipeline/wp_e6_sweep.py`'s docstring
convention). Nothing in this document is a `TEST` or a `FIT` (CLAUDE.md rule 3) — no
real-data comparison is proposed or performed here; Parts A and C operate entirely on
`desisim`-simulated synthetic spectra (CLAUDE.md rule 1, synthetic-data infra only, no G1
pin required). Part B operates on the emulator's own forward model plus the synthetic
covariance from Part A — also no real-data touch.

---

## 0. Correction to the task framing before design starts

The brief that requested this document states "the 10 k-bins (`K_BINS` in `emu_predict.py`)."
This is incorrect and the arithmetic in Part A depends on the true count, so it is corrected
here rather than silently carried through:

`phase1_work/agent1_emulator/emu_predict.py` L33–37:
```python
TARGET_COLS = [
    "-2.2", "-2.1", "-2.0", "-1.9", "-1.8", "-1.7", "-1.6", "-1.5",
    "-1.4", "-1.3", "-1.2", "-1.1", "-1.0", "-0.9", "-0.8", "-0.7",
]
K_BINS = 10.0 ** np.array([float(c) for c in TARGET_COLS])
```
This is **16** values (log₁₀k = −2.2 … −0.7 in steps of 0.1), not 10. Independently
confirmed by `data/derived/wp_e6_grid_controls_report_2026_07_28.json`, whose
`k_bins_s_per_km` arrays each have 16 entries. All of Part A (covariance dimension,
Hartlap scaling) and Part B (degrees-of-freedom bookkeeping) below use **p = 16**.

---

## 1. Part A — Covariance construction from desisim mock ensembles

### 1.1 What is being replaced and why

`integration_iminuit.py::load_obs()` (L23–33) currently builds `Cov_inv` from
`lya-mfdm/data/lya_data.pkl`. That covariance is the **emulator's own training-data
observational uncertainty** — whatever the upstream authors (arXiv:2606.06969) used to fit
their nuisance parameters against their own comparison dataset. It is not a DESI-realistic
uncertainty on *our* forward-simulated grid predictions, and reusing it would silently
import an unrelated survey's noise model into a DESI z=4.2 comparison. This is a distinct
quantity, not a refinement of the same one — the fix is not "use a better version of
`lya_data.pkl`," it is "build a new covariance from a forward simulation of the actual
target (DESI z∈[4.0,4.4], per grid brief A4)."

### 1.2 Mock ensemble generation — extending the existing NQSO=30 pattern

The building blocks already exist and work, per Phase 1 Agent A3:
- `phase1_work/agent3_synthetic/make_transmission_file.py` — `desisim.lya_mock_p1d.MockMaker`
  generates `Ns` Lyα transmission skewers.
- `phase1_work/agent3_synthetic/run_mock_and_compare.py` — the same `MockMaker`, plus
  `desisim.scripts.quickspectra.sim_spectra()` for resolution convolution + Poisson/read
  noise (the real specsim path `quickquasars` itself uses internally).
- `phase1_work/agent3_synthetic/compare_p1d.py` — computes P1D(k) via a per-spectrum FFT
  (`flux_power_1d()`, L54–62), currently averaged over the `NQSO` axis before returning.

**Key finding from reading `desisim.lya_mock_p1d.MockMaker.get_lya_skewers()`**
(`phase1_work/agent3_synthetic/desisim/py/desisim/lya_mock_p1d.py` L115–129):
```python
def get_lya_skewers(self,Ns=10,new_seed=None):
    ...
    delta, var_delta = self.get_gaussian_fields(Ns)   # Ns INDEPENDENT draws
    ...
```
`get_gaussian_fields(Ns)` draws `Ns` **independent** Gaussian-random-field realizations from
the running RNG stream — each of the `Ns` skewers in a single `MockMaker` call is already an
independent line of sight, not a shared box sliced `Ns` ways. This means the natural, correct
lever for growing the ensemble is **raising `NQSO` in a single call**, not re-running the
pipeline under many different `SEED` values. (Re-running with different seeds also produces
independent draws — the RNG stream is just being extended further — but is not *required*
for independence and adds bookkeeping for no statistical benefit here. Recommendation:
one `MockMaker(seed=SEED)` call with `Ns = N_realizations`, `SEED` fixed and recorded, as
today (`SEED = 42`).)

**This is independent-realization, not bootstrap**, and should not be described as
bootstrap in any downstream doc: each of the `N` synthetic quasars is a distinct draw of
the underlying Lyα density/transmission field plus (via `sim_spectra`, Poisson/read noise
per spectrum) a distinct instrument-noise realization. Bootstrap (resampling the same 30
skewers with replacement) would reuse the same field draws and underestimate large-scale
(cosmic-variance-like) scatter; that failure mode does not apply here because `Ns` skewers
in one call are already independent by construction of `get_gaussian_fields`.

**Concrete change required:** bump `NQSO` (rename to `N_REALIZATIONS` for clarity) from 30
to the target `N` (§1.5) in `make_transmission_file.py` and `run_mock_and_compare.py`, and
change `compare_p1d.py::flux_power_1d()` to **return the per-spectrum power array before
the `.mean(axis=0)`** (currently L60-62 collapses it), i.e. return shape `[N, 16]` instead
of `[16]`. The mean-over-realizations P1D and the sample covariance are then both computed
downstream from that `[N, 16]` array — the averaging step is not deleted, just moved out of
`flux_power_1d()` so both statistics can be built from the same raw ensemble.

### 1.3 Per-realization masking must use the corrected estimator, not the current one

Each of the `N` realizations must apply the DESI-like ~3% masking (`MASK_FRAC`) and the
**gap-handling fix from Part 3 below**, not the current zero-fill-then-FFT path — otherwise
the covariance itself inherits the +7% artifact bias in every diagonal (and, since the mask
draw differs per realization, off-diagonal) entry. Part A and Part C are therefore not
independent design choices: A consumes C's corrected estimator.

### 1.4 Sample covariance

For per-realization vectors `P_i(k) ∈ R^16`, `i = 1..N`, with mean `P̄(k) = (1/N) Σ_i P_i(k)`:
```
C_jk = (1/(N-1)) Σ_i (P_i(k_j) - P̄(k_j)) (P_i(k_k) - P̄(k_k))
```
a full **16×16** matrix, not a diagonal approximation — the task brief is explicit that
correlations across the 10 (corrected: 16) k-bins at fixed z=4.2 must be captured, and there
is no argument in this pipeline for assuming diagonality: masking-induced edge effects,
shared continuum-fitting-like normalization (here: the per-spectrum mean subtraction in
`flux_power_1d`), and the shared window function couple neighboring k-bins directly.

### 1.5 How large must N be — explicit noise-scaling statement

A 16×16 sample covariance is **singular** for `N ≤ 16` (rank ≤ N−1). Practical use of the
covariance requires *inverting* it (for the χ² in Part B), and the naive inverse of a
noisy sample covariance is itself a biased estimator of the true precision matrix — the
standard correction is the **Hartlap factor** (Hartlap, Simon & Schneider 2007, A&A 464,
399):
```
Ĉ⁻¹_unbiased = [(N - p - 2) / (N - 1)] · Ĉ⁻¹_naive ,   p = 16
```
valid (positive) only for `N > p + 2 = 18` — a **hard floor**, separate from the softer
"stable enough" floor below. Values of this correction factor at candidate N:

| N | Hartlap factor (N−18)/(N−1) | Effective χ² inflation if uncorrected |
|---|---|---|
| 20 | 0.11 | ~9× |
| 50 | 0.65 | ~1.5× |
| 100 | 0.828 | ~1.21× |
| 200 | 0.915 | ~1.09× |
| 300 | 0.943 | ~1.06× |
| 1000 | 0.982 | ~1.018× |

**Recommendation:** target `N ≈ 200` as the initial working ensemble (Hartlap factor
≈0.91, i.e. correcting for a ~9% inverse-covariance bias) as an ENGINEERING judgment call
balancing statistical stability against `desisim` wall-clock cost — **the per-realization
cost of `MockMaker` + `sim_spectra` at this N is not timed in this session** (unlike the
emulator, which the grid-controls report establishes as millisecond-scale; `desisim` mock
generation is orders of magnitude more expensive and was not benchmarked here). This
recommendation is provisional and should be revisited against an actual timing run of
`run_mock_and_compare.py` at, e.g., `N=50`, before committing to N=200 for the full
protocol; if the wall-clock cost is prohibitive, the fallback is documented under §5 (Open
items). Always apply the Hartlap correction regardless of the chosen N — it is cheap and
removes a real, quantified bias.

### 1.6 What this section does not claim

No real DESI spectra are touched (CLAUDE.md rule 1 stays satisfied — this is entirely
`desisim` synthetic infrastructure). No claim is made about whether N=200 or any other N is
"enough" in an absolute forecasting sense; only the Hartlap-factor bias is quantified.

---

## 2. Part B — Nuisance parameter profiling design

### 2.1 Extending `integration_iminuit.py`'s working chi2

The existing pattern (`build_chi2`, L36–51) is sound and should be kept structurally
identical, with two substitutions: (a) `obs[z_str]["Cov_inv"]` becomes the Part-A
Hartlap-corrected inverse for z="4.2" only, in place of `lya_data.pkl`'s covariance; (b) the
sum over `Z_ORDER` (3 redshifts) collapses to the single z="4.2" term, since the grid
(`T0_MF_GRID_DEFINITION_2026_07_27.md` §3) fixes z_str="4.2" only (A4).

```python
def chi2(m, f, zrei, ha, hs, taueff):
    pred = predict_pk(nn_pack, m, f, zrei, ha, hs, taueff, "4.2")
    diff = pred - p_bar_42          # Part A ensemble mean, N=200 realizations
    return float(diff @ cov_inv_42_hartlap @ diff)
```
Note this removes the *reason* for the existing docstring's caveat ("ONE shared set of
nuisance IGM parameters across all 3 z's... fine for a smoke test, not physics"): at a
single z there is nothing being shared across z's anymore — the simplification the current
code flags is not carried into this design, and the docstring caveat should not be copied
forward into whatever module implements this.

### 2.2 Bounds / initialization — and an unresolved provenance mismatch found while checking `param.pkl`

`data/param.pkl` (the 210-point training LHS) has fields
`('index','m','f','ha','hs','z','u_5.0','u_4.6','u_4.2')` — **no field literally named
`taueff`**. Checking where `integration_iminuit.py`'s Minuit `limits` (L70–73) actually come
from:

| Parameter | `integration_iminuit.py` limit | Traces to |
|---|---|---|
| `zrei` | (6.05, 14.91) | `param.pkl` column `z`, min/max (6.054, 14.960) — **trained LHS support** |
| `ha` | (0.066, 3.989) | `param.pkl` column `ha`, min/max (0.0577, 3.9893) — **trained LHS support** |
| `hs` | (−0.987, 0.996) | `param.pkl` column `hs`, min/max (−0.9958, 0.9956) — **trained LHS support** |
| `taueff` | (0.3, 1.8) | `lya-mfdm/mcmc.py` L55–57 `BOUNDS_BASE`, identical value repeated for all 3 z's — this is the **MCMC flat-prior box**, not a `param.pkl`-derived support range |

`param.pkl`'s `u_5.0`/`u_4.6`/`u_4.2` columns have ranges ≈(0.4–23.5), incompatible with
(0.3, 1.8) at any obvious rescaling — these are almost certainly a different physical
quantity than the MCMC nuisance `taueff`, not an unlabeled version of it. **Open item for
T0 / implementer:** the `taueff` bound this protocol inherits is a human-chosen prior box
from `mcmc.py`, not a verified trained-support extremum like the other three. Before this
protocol runs for real, either (a) locate the actual trained-support range for the
network's `taueff` input dimension (likely derivable from whichever `param.pkl`-adjacent
file feeds `x_res`'s 4th component at fit time — not resolved in this session), or (b)
explicitly document that `taueff` bounds are prior-box, not support-box, and accept that
Minuit could in principle push it toward an edge the network was never trained on. This is
flagged, not resolved, here.

Initialization: use the training-LHS medians already used as the grid-controls fixed point
(`zrei=10.5, ha=2.0, hs=0.0, taueff=1.0` — `wp_e6_grid_controls_report_2026_07_28.json`
`igm_nuisance_point`), consistent across all 56 grid cells as the Minuit starting guess.

### 2.3 Degrees of freedom

16 k-bins (§0), 4 profiled nuisance parameters (`zrei, ha, hs, taueff`) per (m,f) cell →
**12 degrees of freedom** per cell's minimized χ², relevant to any downstream
goodness-of-fit or exclusion-significance statement (none is made in this document — F3/F4
are mechanical triggers reserved for the gated, pinned comparison, CLAUDE.md rule 5).

### 2.4 Cost across 56 grid cells

`predict_pk()` is a millisecond-scale MLP forward pass (5-fold ensemble, established by the
grid-controls report's runtime behavior — no separate profiling timer, but consistent with
the check-1/2/3 battery over 56 cells completing without a reported runtime concern).
Minuit's `migrad()` calls `chi2` on the order of tens to a few hundred times per
minimization; at 56 cells × ~100 evaluations × ~ms-scale forward pass, total profiling cost
is expected to be seconds, not an engineering bottleneck — **unverified by an actual timed
run in this session**, flagged the same way as the desisim cost estimate in §1.5.

---

## 3. Part C — Masking gap-handling fix

### 3.1 Precise diagnosis (two distinct bugs in `compare_p1d.py`, not one)

`phase1_work/agent3_synthetic/compare_p1d.py`:
```python
44  rng = np.random.RandomState(SEED)
45  mask = rng.rand(*b_flux_f.shape) < MASK_FRAC
46  b_flux_masked = b_flux_f.copy()
47  b_ivar_masked = b_ivar_f.copy()
48  b_flux_masked[mask] = 0.0
49  b_ivar_masked[mask] = 0.0
...
58  d = flux - flux.mean(axis=1, keepdims=True)
59  fft = np.fft.rfft(d, axis=1)
```
- **Bug 1 (the one the task brief names):** zero-filling masked pixels (L48) before the FFT
  (L59) introduces spurious power at the mask-edge discontinuities — a sharp jump from the
  true flux value to exactly 0 at every masked pixel is not part of the physical signal and
  leaks power across all k via the implicit rectangular window on each gap.
- **Bug 2 (found while reading the same function, not previously flagged):** L58 computes
  the per-spectrum mean over **all** pixels including the zero-filled ones (`flux.mean(axis=1)`
  where `flux` is `b_flux_masked`), which biases the subtracted mean low by
  `MASK_FRAC × (true mean flux)` and compounds the edge-discontinuity artifact — the
  "d" that gets FFT'd is `(true_flux - biased_mean)` at good pixels and `(0 - biased_mean)`
  at masked pixels, i.e. an even sharper jump than zero-fill alone would cause.

### 3.2 What DESI/eBOSS actually do — real citation, not an invented method

The DESI DR1 Lyα P1D FFT-estimator paper, **Ravoux et al. 2023** ("The Dark Energy
Spectroscopic Instrument: One-dimensional power spectrum from first Lyman-α forest samples
with Fast Fourier Transform," MNRAS 526, 5118, arXiv:2306.06311), and its DR1 successors
(arXiv:2505.09493 FFT measurement, arXiv:2509.13593 estimator validation) describe the FFT
method's mask handling: masked pixels are set to zero in the flux-contrast field (the same
starting point as this pipeline's Bug 1), and the resulting bias — described as a survey
window function convolving all Fourier modes — is corrected **empirically, from mocks**:
the ratio of masked-mock P1D to unmasked-mock (or true-input) P1D is measured on
`quickquasars`-style synthetic realizations and fit (per redshift bin, with a polynomial in
this description) to give a multiplicative correction applied to the real measurement.

*Honesty note on this citation:* the recipe above is reconstructed from a search-engine
summary of the paper (WebSearch), not a verbatim read of the paper's own methods section —
`WebFetch` on the arXiv abstract page returned only metadata, not the method text. Treat
this as the correct paper and the correct general approach (mock-calibrated multiplicative
window correction, standard in this literature going back to Palanque-Delabrouille et al.
2013 and Chabanier et al. 2019's `quickquasars`-based corrections for the SDSS/eBOSS FFT
P1D), but an implementer should read arXiv:2306.06311's methods section directly before
coding the exact functional form of the correction (per-z polynomial vs. some other
parametrization) — same "inbound documents are prompts to verify" discipline as the rest of
this repo's intake protocol.

### 3.3 Recommendation and why, against the other two options

**Recommend: mock-calibrated multiplicative correction (DESI's approach), reusing Part A's
ensemble.** This pipeline is uniquely positioned to do this cheaply: `compare_p1d.py`
already computes `p_clean` and `p_masked` from the same underlying realization and writes
them to `p1d_comparison.npz` — the ratio `p_masked / p_clean` **is** the correction
function, and Part A's N-realization ensemble (§1) gives N independent draws of that ratio
at z=4.2 to average/fit, at zero additional simulation cost beyond what Part A already
requires.

- **Against (i) interpolation across gaps:** interpolated values are correlated with their
  neighbors by construction, which does not remove bias so much as relocate and reshape it,
  and a rigorous treatment of interpolation's own effect on P1D would itself require the
  same mock-calibration step — i.e., choosing interpolation does not avoid needing Part A's
  ensemble, it just adds a step before still needing it.
- **Against (iii) excluding affected k/regions:** with only 16 k-bins total (§0, not the
  10 in the original task framing), discarding any is expensive in resolution exactly where
  the grid brief concentrated cell density (near the published exclusion boundary, per
  `T0_MF_GRID_DEFINITION_2026_07_27.md` §3), and the masking artifact here is described as
  broadband (affecting a ratio across the reported k range, not one isolated bin) — so
  exclusion would not cleanly quarantine the bug's effect.

### 3.4 Where the fix belongs

`flux_power_1d()` in `phase1_work/agent3_synthetic/compare_p1d.py` (L54–62) is the function
that needs a `mask_correction: np.ndarray | None = None` argument (or a caller-side
multiplicative step) applied to `power.mean(axis=0)` before returning — do not fix the mean
subtraction (Bug 2) by changing the FFT's masking convention silently, since Part A's
ensemble-based correction is calibrated against whatever convention (zero-fill,
mean-computed-over-good-pixels-only, or otherwise) is actually shipped in the corrected
estimator; **Bug 2 must be fixed first** (compute `flux.mean(axis=1)` over unmasked pixels
only, e.g. via `np.ma.masked_array` or an explicit boolean-indexed mean) so the mock
calibration is measuring one clean artifact (the edge discontinuity), not two entangled
ones.

---

## 4. Summary recommendation

- **A:** Build covariance from an N≈200-realization `desisim` mock ensemble (independent
  per-skewer draws via `MockMaker.get_lya_skewers`, not bootstrap; Hartlap-corrected
  16×16 sample covariance at z=4.2), replacing `lya_data.pkl` entirely.
- **B:** Extend `integration_iminuit.py`'s chi2 to use Part A's covariance, single z=4.2
  term, 12 dof per cell; flag the `taueff` bound's prior-box (not trained-support)
  provenance as unresolved.
- **C:** Fix the two masking bugs (zero-fill edge discontinuity + biased mean) by adopting
  DESI's own mock-calibrated multiplicative window correction (Ravoux et al. 2023,
  arXiv:2306.06311), reusing Part A's ensemble at no extra simulation cost, applied in
  `compare_p1d.py::flux_power_1d()`.

---

## 5. Open items for T0

1. `taueff` Minuit bound (0.3, 1.8) provenance unresolved — prior-box vs. trained-support
   (§2.2).
2. N=200 for Part A is an untimed engineering guess against unbenchmarked `desisim` cost —
   needs a timing run before being treated as final (§1.5).
3. This document does not implement anything; no code changes are made by writing it.

---

*Generated-by: Sonnet (Stream 3 agent) | Reviewed-by: pending T0 (Xavier).*
