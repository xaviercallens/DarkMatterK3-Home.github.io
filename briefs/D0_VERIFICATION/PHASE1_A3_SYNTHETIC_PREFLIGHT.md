# Phase 1 — Agent 3: Synthetic Pre-Flight Infrastructure

**Date:** 2026-07-27
**Agent:** Phase-1 Agent 3 (Sonnet), synthetic pre-flight infra
**Working dir:** `phase1_work/agent3_synthetic/`
**Web-tool calls used:** 0 / 8 (all work done via local `git clone` / `pip install` / `svn export`, no WebFetch/WebSearch needed)

## Bottom line

1. **`modelling_spectro_sys` does NOT implement any of the three named DESI contaminants**
   (resolution damping, masked pixels, spectrograph noise). It implements redshift-space
   peculiar-velocity systematics + catastrophic-redshift failures for LSS *galaxy clustering
   catalogs* (LRG/ELG/QSO), an entirely different observable (Δz/Δv per object) from Lyα
   forest flux-vs-wavelength pixels. **Coverage of the named list: 0/3.**
2. The clean-vs-contaminated comparison **was still completed**, using `desisim`'s own real
   specsim-based instrument simulator (the same code `quickquasars` calls internally) in place
   of `modelling_spectro_sys`. Result: **real, measurable degradation** — total P1D power
   suppressed to **86.6%** of clean by resolution convolution + noise, with a much sharper
   **56.4%** suppression at high-k (small scales) from resolution damping specifically. This is
   not a no-op.
3. The literal `quickquasars` CLI tool could **not** be run to completion with a realistic QSO
   continuum model within budget — both its continuum sources (`DESI_BASIS_TEMPLATES`,
   `simqso`) are blocked for reasons detailed below (one is auth-walled DESI-collaboration
   data, the other is a genuinely broken/outdated dependency). This is reported as a **partial
   FAIL** for the CLI tool specifically, worked around (not silently ignored) using desisim's
   own lower-level simulation code.

---

## 1. Repos cloned, actual capabilities read from code

### `desisim` (commit `a21914c`, 2026-03-18)
- `bin/quickquasars` exists and is a thin wrapper around
  `desisim.scripts.quickquasars.main()` (1078 lines). Confirmed: reads CoLoRe-format
  Lyα transmission-skewer FITS files (`WAVELENGTH`/`TRANSMISSION`/`METADATA` HDUs), builds
  a QSO continuum via `desisim.templates.QSO` (needs `$DESI_BASIS_TEMPLATES`) or
  `desisim.templates.SIMQSO` (needs the external `simqso` package), multiplies by
  transmission, then calls `desisim.scripts.quickspectra.sim_spectra()` which wraps
  **specsim** (real DESI spectrograph simulator: resolution-matrix convolution + Poisson
  source/sky noise + read noise), all real, working code once its inputs are supplied.
- `desisim.lya_mock_p1d.MockMaker` — a self-contained, documented synthetic Lyα transmission
  generator (McDonald et al. 2006 lognormal P1D model), no external data required. This is
  what was actually used to generate the forest absorption (see §2).
- No `DESI_BASIS_TEMPLATES` data ships with the repo or with `desimodel`'s public data
  (checked: `desimodel`'s own svn-exported `data/` — 260 MB, see §3 — has only individual
  reference spectra for S/N calcs, not the full QSO PCA basis-template ensemble
  `desisim.templates.QSO` needs).

### `modelling_spectro_sys` (commit `76ff1a6`, 2024-11-05)
Entire repo is 3 files: `README.md`, `spectroscopic_sys_simple.py` (134 lines),
`spectroscopic_systematics.ipynb`. Read in full. Actual behavior, confirmed by running it
(see §4):
- Takes `--tracer {LRG,ELG,QSO}`, a redshift, a mock size, and DESI/SDSS-measured
  Gaussian/Lorentzian/log-normal parameters, and outputs a **flat text file of Δv (km/s)
  velocity offsets** — one scalar per galaxy/quasar — meant to be added to a mock's peculiar
  velocity in a box or lightcone LSS catalog, to simulate redshift-measurement error and
  (for ELG) catastrophic redshift failures.
- It never touches a flux array, a wavelength grid, a resolution matrix, or an inverse-variance
  array. There is no code path in this repo for spectral pixels at all.
- README references a `DESI_lightcone` subdirectory with "WEIGHT_FKP recomputing" — this
  directory **does not exist in the repo**; it lives in a separate, NERSC/`cosmodesi`-environment-
  gated repo (`Jiaxi-Yu/LSS`, `catastrophics` branch) not accessible here and out of scope.
- The tutorial notebook confirms the same: every worked example is "galaxy catalogue in a box
  with peculiar velocity," never a spectrum.

**Verdict: repo-purpose mismatch.** The Acceleration Manifesto's assumption that this repo
injects resolution/masking/noise into Lyα *spectra* is wrong. It is a large-scale-structure
redshift-systematics tool, not a spectral-systematics tool.

---

## 2. Mock generation: what was actually done, errors + fixes

**N spectra: 30 mock quasars** (`NQSO=30`, well within the 10–50 target).

**Method (documented desisim code only, no assumptions):**
1. `desisim.lya_mock_p1d.MockMaker(N2=12, dv_kms=20.0, seed=42)` → 30 synthetic Lyα
   transmission skewers, `4096` cells each, observed-frame wavelength `4260.9–5601.9 Å`
   (centered at `z_c=3.0`), transmission range `[0.0, 1.0]`, mean `0.723`. This *is* desisim's
   own documented Lyα-forest generator (McDonald et al. 2006 P1D), used exactly as shipped.
2. Wrote these into a proper CoLoRe-format transmission-skewer FITS file
   (`WAVELENGTH`/`TRANSMISSION`/`METADATA` with `RA`/`DEC`/`Z`/`MOCKID`) so `desisim`'s own
   reader (`read_lya_skewers`) could consume it — this was necessary because no real CoLoRe
   mock skewer file is bundled with `desisim` or downloadable (DESI data portal down, see
   below) and the one test fixture shipped in the repo (`test/data/simpleLyaSpec.fits.gz`) is
   in a *different* format (`get_spectra()`'s per-object LAMBDA/FLUX tables), not the
   transmission-skewer format `quickquasars` needs.

**Errors encountered on the literal `quickquasars` CLI, in order, with fixes attempted:**

| # | Attempt | Failure | Root cause |
|---|---|---|---|
| 1 | `quickquasars --no-simqso ...` (QSO() basis-template continuum) | `KeyError: 'DESI_BASIS_TEMPLATES'`, then after supplying `desimodel` data (below), confirmed the template FITS files themselves are not obtainable: `svn ls https://desi.lbl.gov/svn/code/desisim/` → **`Authentication failed`** | `DESI_BASIS_TEMPLATES` is DESI-collaboration-only data behind auth, not a public product. Correctly out of scope per repo rule "public data products only." |
| 2 | `pip install simqso` (default) | `ModuleNotFoundError: No module named 'numpy'` during isolated build | `simqso`'s `setup.py` imports `numpy` at build time inside pip's isolated build env |
| 3 | `pip install --no-build-isolation simqso` | `ImportError: cannot import name 'simps' from 'scipy.integrate'` | `simqso` v1.2.4 (2018) uses a scipy API (`scipy.integrate.simps`) removed in the modern scipy required by `desisim`'s other 2026-era dependencies |
| 3b | Patched `simps`→`simpson` in the cloned `simqso` source, retried | `ModuleNotFoundError: No module named 'astropy.modeling.blackbody'` (then `astropy.analytic_functions`) | Same story, second API break: `simqso` also uses a pre-4.0 astropy `blackbody_lambda` location, removed in the modern astropy already installed | 

Per the stop condition ("3 distinct fix attempts → report FAIL"), the `quickquasars` CLI's
QSO-continuum step is reported as **FAIL**: `DESI_BASIS_TEMPLATES` is genuinely inaccessible
(auth-walled, correctly out of scope), and `simqso` v1.2.4 (desisim's own pinned fallback) is
incompatible with the modern astropy/scipy that had to be installed for `desisim` itself to
import — a real, unresolved-in-repo dependency rot, not a configuration mistake on our end.

**Side finding (not a failure, worth flagging for Agent 1 / future infra work):** the
`desimodel` package's own runtime data (throughput curves, PSF params — needed by
`sim_spectra`/specsim regardless of continuum source) is genuinely missing from a fresh
`pip install`, but **is** obtainable: `svn export https://desi.lbl.gov/svn/code/desimodel/trunk/data`
worked (260 MB, ~60s, no auth needed) once `subversion` was `apt-get install`ed (not present by
default). `desi.lbl.gov` (svn/code host) is reachable; `data.desi.lbl.gov` (confirmed down
elsewhere in this project's connectivity log) is a *different* host. Set `$DESIMODEL` to the
export directory.

**Workaround used to still deliver the actual scientific check (§4):** called
`desisim.scripts.quickspectra.sim_spectra()` directly — the exact same specsim-wrapping
function `quickquasars` calls internally for resolution+noise — on
`(simple power-law continuum) × (real MockMaker transmission)`, since `sim_spectra()` does
not require `DESI_BASIS_TEMPLATES`. This is real desisim/specsim instrument-simulation code,
not a hand-rolled substitute for the resolution/noise physics; only the QSO continuum shape
(flat/mild power law, not a real quasar PCA template) is a stand-in, and is labeled as such.
Resampling the `MockMaker` native (non-uniform, `dv`-spaced) grid onto specsim's required
uniform-`dwave` grid needed `desispec.interpolation.resample_flux` at `dwave=0.2 Å`
(quickquasars's own documented internal step size) — an earlier attempt at `dwave=1.0 Å` and
`0.4 Å` failed specsim's camera-pixel-multiple check (`ValueError: Invalid output_pixel_size`).

Output: `qq_manual_out/spectra-manual.fits` (30 spectra × 3 cameras b/r/z, with
`{B,R,Z}_FLUX`/`{B,R,Z}_IVAR`/`{B,R,Z}_MASK`), real specsim resolution matrices generated for
all three cameras.

---

## 3. Systematics actually applied

| Named contaminant | Source | Applied? | How |
|---|---|---|---|
| Resolution damping | `desisim`/specsim (native, via `sim_spectra`) | **Yes** | Real DESI b/r/z-camera resolution matrix convolution, part of `simulate_spectra`/specsim, not from `modelling_spectro_sys` |
| Spectrograph noise | `desisim`/specsim (native, via `sim_spectra`) | **Yes** | Poisson source+sky noise and read noise, `generate_random_noise(use_poisson=True)`, DARK program reference conditions (1000s exptime), not from `modelling_spectro_sys` |
| Masked pixels | Hand-rolled (neither repo covers it) | **Yes, but hand-rolled** | 3% random pixel zeroing (flux and ivar) applied post-hoc on the specsim output, chosen to approximate a DESI-like cosmic-ray/sky-residual masking rate; **not sourced from either repo** |
| Redshift-space Δv systematics (LRG/ELG/QSO) | `modelling_spectro_sys` (its actual feature) | Demonstrated separately, **not merged into the spectra** | Ran `spectroscopic_sys_simple.py --tracer QSO --redshift 1.8 --size 1000 --source DESI --geometry box` → 1000 Δv draws, mean −3.3 km/s, std 549 km/s, range [−1984, +1993] km/s (Lorentzian, σ=273 km/s per DESI QSO 1.6<z≤2.1 calibration, capped at maxdv=2000). This output is a velocity-space catalog quantity, structurally incompatible with a per-pixel flux array — merging it would require translating it into a forest-window wavelength shift, which is a different (if related) systematic than any of the three named ones, and was out of scope to hand-roll on top of an already-hand-rolled masking step. |

---

## 4. Clean-vs-contaminated comparison — real numbers

Method: `P1D(k)` computed as the mean `|FFT|²` (mean-subtracted, per spectrum, averaged over
the 30 mocks) in velocity space, on the actual DESI-b-camera pixel grid
(`Δλ=1.0 Å`, `Δv≈61 km/s/pixel`), restricted to the Lyα forest window
`4266.1–5596.1 Å` (1331 pixels/spectrum).

| Quantity | Clean | Contaminated (specsim res+noise) | Ratio |
|---|---|---|---|
| Total power (Σ P(k)) | 9.449×10⁴ | 8.183×10⁴ | **0.866** |
| High-k (top quartile, small scales) mean P(k) | 42.57 | 24.02 | **0.564** |
| Low-k (bottom decile) mean P(k) | 600.8 | 620.1 | **1.032** |

With the additional 3% hand-rolled pixel masking applied on top of the specsim output:

| Quantity | Clean | Masked+contaminated | Ratio |
|---|---|---|---|
| Total power | 9.449×10⁴ | 1.012×10⁵ | **1.071** |

**Interpretation (the judgment call):** the contamination is **not a no-op**. Resolution
convolution measurably suppresses small-scale power (high-k ratio 0.564 — the classic
resolution-damping signature, physically correct direction and magnitude for a
DESI-like resolution matrix), while noise adds a modest amount of power at low-k (ratio
1.032, consistent with read/sky noise being closer to white in this regime). Net effect on
total integrated power is a **13.4% suppression** — resolution damping dominates over the
noise-power addition in this configuration. Naive zero-value pixel masking (the hand-rolled
addition) *increases* apparent power (ratio 1.071) rather than suppressing it, because
zero-filling introduces sharp discontinuities that inject spurious power across k — a
real and useful finding in its own right: **naive masking, done wrong, is not conservative**;
a production pre-flight would need proper gap-handling (e.g. masked-pixel weighting in the
FFT/estimator, not zero-fill), which neither repo provides.

Numbers are reproducible: `run_mock_and_compare.py` → `compare_p1d.py`,
seed=42 throughout, output saved to `p1d_comparison.npz`.

**Conclusion on "rigorously pessimistic":** the *desisim-native* resolution+noise path is a
real, non-trivial degradation and is suitable as a pessimism source. `modelling_spectro_sys`
contributes **nothing** to this — using it alone, as the Manifesto assumed, would have been a
silent no-op for exactly the failure mode this check exists to catch (its 0/3 coverage isn't
just "not everything," it's "none of the named list").

---

## 5. Gap list — Manifesto's claimed systematics vs what `modelling_spectro_sys` covers

- **Resolution damping: 0% covered by `modelling_spectro_sys`.** Fully covered instead by
  `desisim`'s own native specsim resolution matrix (used in §4).
- **Masked pixels: 0% covered by `modelling_spectro_sys`.** Not covered by `desisim` either
  in a documented, physically-motivated way (no README-documented masking-rate model found).
  Hand-rolled here (3% uniform random) purely as a placeholder; a real pre-flight needs a
  DESI-calibrated masking-rate/pattern model (e.g. from sky-line and cosmic-ray hit-rate
  statistics), which would need separate implementation or a different source repo entirely.
- **Spectrograph noise: 0% covered by `modelling_spectro_sys`.** Fully covered instead by
  `desisim`'s native specsim Poisson+read-noise model (used in §4).
- **What `modelling_spectro_sys` *does* cover, not on the original named list at all:**
  redshift-space peculiar-velocity/Δz systematics and catastrophic-redshift failure rates for
  LRG/ELG/QSO clustering catalogs — real, documented, runnable (demonstrated in §3), but
  **orthogonal to Lyα P1D flux-spectrum contamination** and not mergeable into a per-pixel
  flux/ivar array without separate translation work that was out of this agent's scope.

**Net: 0/3 of the named systematics list is implemented by `modelling_spectro_sys`.**
Everything usable for the pre-flight (resolution + noise) came from `desisim`'s own native
simulator; masked pixels needed fully hand-rolled placeholder logic from neither repo.

---

## Files in this working directory

- `make_transmission_file.py` — builds the synthetic CoLoRe-format transmission skewer FITS
- `run_mock_and_compare.py` — generates clean flux + runs desisim's real `sim_spectra()`
- `compare_p1d.py` — clean-vs-contaminated P1D comparison, numbers above
- `qq_manual_out/spectra-manual.fits` — output DESI-format spectra (b/r/z cameras)
- `p1d_comparison.npz` — saved P(k) arrays
- `modelling_spectro_sys/Delta_v_QSO_demo.txt` — demo output of the repo's actual (unrelated)
  feature
- `desimodel_data_test/data/` — 260 MB `desimodel` runtime data (svn-exported from
  `desi.lbl.gov`, public, no auth needed); referenced via `$DESIMODEL` env var, not committed
- `desisim/`, `modelling_spectro_sys/`, `simqso/` — cloned repos (`simqso` patched locally,
  still non-functional past the two API-break points listed above)

No `git add`/`commit`/`push` performed. `PREDICTION.md` and `data/raw/` untouched.
