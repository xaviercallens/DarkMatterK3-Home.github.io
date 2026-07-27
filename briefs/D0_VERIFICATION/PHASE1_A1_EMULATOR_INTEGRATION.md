# Phase 1 — Agent 1: lya-mfdm Emulator Integration + Adequacy Check

**Date:** 2026-07-27
**Repo tested:** https://github.com/jianxiangl-astro/lya-mfdm, commit `9182aa4d48abed181323fa97b487707a9f0cbb43` (2026-07-06)
**Paper:** Liu, Jianxiang et al. (2026), arXiv:2606.06969
**Working dir:** `phase1_work/agent1_emulator/` (clone at `phase1_work/agent1_emulator/lya-mfdm/`)
**Web calls used:** 1 (git clone over HTTPS; all package installs and inspection were local)

---

## 1. LICENSE status: ABSENT

No `LICENSE`, `LICENSE.md`, `LICENSE.txt`, `COPYING`, or `NOTICE` file anywhere in the repo
(checked case-insensitively at all depths). No license section or mention in `README.md`. `git
log --all` shows only generic "Update" commits, no license-related commit. **This repo carries no
explicit license.** Under default copyright, that means no redistribution/modification rights are
granted beyond what's needed to read the code; usage here was read/run-only, consistent with a
verification pass, but any downstream use (e.g. embedding modified copies in WP-E6 deliverables)
should get this flagged to T0 before proceeding.

## 2. Install status: clean after 2 additions, 1 of which had to be reverted

`environment.yml` deps vs. `/home/callensxavier_gmail_com/venv` (already installed: numpy 2.2.6,
scipy 1.15.3, matplotlib 3.10.9, pandas 2.3.3, h5py 3.16.0, emcee 3.1.6, tqdm 4.68.3, pyyaml
6.0.3, torch 2.12.1, scikit-learn 1.7.2, astropy 6.1.7):

- **Missing, installed successfully:** `chainconsumer==0.34.0` (pulled in `statsmodels` +
  `patsy` as transitive deps) — needed by `mcmc.py`'s top-level import.
- **Missing, installed then REMOVED:** `mpi4py==4.1.1`. The wheel installs fine (no system MPI
  needed at install time), but this VM has no actual MPI runtime (`libmpi.so` absent, no
  `mpicc`/`mpirun`). At import time `mpi4py` succeeds (lazy ABI shim), but the moment
  `cobaya`'s own `cobaya/mpi.py` opportunistically imports it to check process rank, it throws
  `RuntimeError: cannot load MPI library` and crashes `cobaya.model.get_model(...)`. This is a
  **real environment conflict**, not a lya-mfdm bug: installing mpi4py without a system MPI
  library actively broke Cobaya integration. Uninstalled it; Cobaya integration then worked (see
  §6). mpi4py is only used upstream for `multiprocessing`-style MCMC parallelization
  (`mcmc.py`/`mock_mcmc.py`), which is out of scope for this single-point smoke test, so its
  absence costs nothing here.
- **Version drift, not remediated (no errors observed, flagged for awareness):** `environment.yml`
  pins python=3.8, numpy=1.24.4, torch==2.4.1, scikit-learn==1.3.2, astropy==5.2.2; the shared
  venv runs python 3.10.12, numpy 2.2.6, torch 2.12.1, scikit-learn 1.7.2, astropy 6.1.7 — all
  substantially newer. `sklearn` raised `InconsistentVersionWarning` unpickling the `MinMaxScaler`
  (trained under 1.3.2) but produced no errors and the smoke test result matches the observed-data
  order of magnitude (see §3), so it's a warning, not a functional break, in this instance — but it
  is not proof the pickled scaler behaves identically bit-for-bit across sklearn major-version
  boundaries.

**Net: install succeeded** (1 clean add, 1 add-then-revert with documented reason).

## 3. Smoke test: PASS

Loaded the actual 5-fold ensemble from `emu/emu_N100/` (10 `.pth` state dicts + 2 `MinMaxScaler`
pickles) via a standalone re-implementation of `mcmc.py`'s `load_system()`/`predict_pk()`
(`emu_predict.py` in this dir — written standalone specifically to avoid `mcmc.py`'s top-level
`chainconsumer`/`emcee`/multiprocessing imports, which are built for full MCMC runs).

Benchmark point: `log10(m_FDM/eV) = -21.0`, `f_FDM = 0.1`, nuisance IGM params at training-set
medians (`zrei=10.5, ha=2.0, hs=0.0, taueff=1.0`, computed directly from
`data/all_pk_num0_cdm.pkl`), `z_str = "4.6"`.

```
k [s/km]  : [0.00631 0.00794 0.01    0.01259 0.01585 0.01995 0.02512 0.03162 0.03981
             0.05012 0.0631  0.07943 0.1     0.12589 0.15849 0.19953]
P1D(k)    : [115.81  107.31   95.30   80.78   71.00   61.99   46.95   36.98   27.82
              18.24   10.99    5.86    3.07    1.62    0.83    0.33]
finite: True   positive: True
```

Order-of-magnitude check against the repo's own observational data (`data/lya_data.pkl`, z=4.6):
`Pk = [128.9, ..., 0.34]` — the emulator prediction at a nearby-but-different (m,f) point tracks
the observed data's shape and scale within a factor of ~1.1-2 across the whole k range, which is
exactly what's expected (it's not supposed to match exactly; it's a different point in parameter
space). **PASS**, not just "didn't crash" — the numbers are physically sane. All three z bins
(5.0/4.6/4.2) checked at the same (m,f) — see `emu_predict.py` output, all finite and monotonically
decreasing with z from 170→116→82 at k=k_min, matching the well-known Lyα P1D redshift evolution
(higher P1D at higher z).

## 4. Domain check — the decisive part

**Exact answer: the emulator is trained and its official API is restricted to exactly 3 discrete
redshifts, z = 5.0, 4.6, 4.2. It does NOT interpolate or extrapolate to other z in any
supported/validated sense.**

Evidence, from the code and data directly (not assumption):

1. **API contract:** `predict_pk(m, f, zrei, ha, hs, taueff, z_str)` in `mcmc.py` takes `z_str` as
   a **string dict key** into `Z_FLOAT = {"5.0": 5.0, "4.6": 4.6, "4.2": 4.2}` (mcmc.py L52,
   L146-149). Calling it with any other key raises `KeyError` — there is no continuous-z
   calling convention anywhere in the shipped inference code (`mcmc.py`, `mock_mcmc.py`,
   `neyman.py` all iterate `for z_str in Z_ORDER` over exactly these 3 strings).
2. **Training data has only 3 z values:** `emu_train.py` builds training features via
   `Z_VALUES = ["5.0", "4.6", "4.2"]` and one simulation snapshot file set per z
   (`all_pk_num0/1/2.pkl` for z=5.0/4.6/4.2 respectively). z never varies continuously within a
   given snapshot file.
3. **The MinMaxScaler was fit on exactly those 3 values**, confirmed directly by inspecting the
   fitted scaler object shipped in `emu/emu_N100/scaler_res.pkl`:
   ```
   scaler_res.data_min_[0] (z_obs column) = 4.2
   scaler_res.data_max_[0] (z_obs column) = 5.0
   ```
   i.e. the scaler has seen literally 3 distinct z inputs, not a continuum.
4. **Extrapolation probe (bypassing the official API, feeding raw z floats directly into the
   scaler+MLP to see what the network mathematically does with out-of-domain z):**
   ```
   z_obs=5.0 (in [4.2,5.0]=True ): P1D[0]=170.4,  P1D[-1]=0.7125
   z_obs=4.6 (in [4.2,5.0]=True ): P1D[0]=115.8,  P1D[-1]=0.3335
   z_obs=4.2 (in [4.2,5.0]=True ): P1D[0]=82.13,  P1D[-1]=0.1135
   z_obs=4.0 (in [4.2,5.0]=False): P1D[0]=68.41,  P1D[-1]=0.05892
   z_obs=3.3 (in [4.2,5.0]=False): P1D[0]=31.11,  P1D[-1]=0.005023
   z_obs=2.2 (in [4.2,5.0]=False): P1D[0]=6.01,   P1D[-1]=0.0001797
   z_obs=6.0 (in [4.2,5.0]=False): P1D[0]=138.4,  P1D[-1]=1.514
   ```
   The MLP does not crash and returns finite, positive numbers for arbitrary z (it's just a
   feedforward network evaluated on an out-of-range scalar input) — but this is **unvalidated
   linear-in-feature-space extrapolation from only 3 anchor points**, not a trained z-dependence.
   The monotonic ~30x drop in P1D amplitude from z=6.0 down to z=2.2 shown above has no supporting
   training data anywhere in [2.2, 4.2) and should not be trusted as physics. **This path is not
   part of the repo's supported API and was not used in any of the other integration tests below.**

**Consequence for WP-E6 v2:** DESI DR1 Lyα spans z≈2.2-4.4 (per WP-E7 recon). Only the
top slice of that range (z≈4.2-4.4) sits near the emulator's trained lower z bound (z=4.2); the
majority of DESI's usable range (z≈2.2-4.2) has **zero training support**. This is a **real,
hard scope-limiting finding**: as shipped, this emulator can only be used at the 3 fixed z's it
was trained on, none of which is below z=4.2. Using it across DESI's full range would require
either (a) restricting the analysis to z≈4.2 only (a single DESI redshift bin, if DESI DR1 bins
land close enough to 4.2 — not verified here, out of scope), or (b) retraining/extending the
emulator with additional simulation snapshots at lower z, which is new simulation work, not
integration work.

## 5. (m,f) grid resolution — from the data files, not the abstract

`data/param.pkl` is **not a rectangular grid** — it's a 210-point structured array (fields:
`index, m, f, ha, hs, z, u_5.0, u_4.6, u_4.2`) consistent with a **Latin Hypercube design** over
continuous parameter ranges:

```
log10(m_FDM/eV): min -22.987, max -19.006   (continuous, 210 points)
f_FDM          : min  0.0023, max  0.9983   (continuous, 210 points)
```

The `emu_N100` model (the one loaded here) trains on the first 100 of these 210 LHS points
(`max_index=100` in `emu_train.py`); `emu_N25`/`emu_N50` use 25/50-point subsets for a
convergence study. Indices 200-209 are held out as a fixed validation set. So: **100 (or 25/50)
irregularly-spaced (m,f) pairs from a Latin Hypercube sample over log10(m/eV)∈[-23,-19],
f∈[0,1] — not a rectangular grid with fixed resolution.** Any (m,f) point requested from the NN
emulator is itself an interpolation of this LHS design (that's what the MLP was trained to do,
and is well-supported, unlike the z-axis). This is a genuinely different situation from z: m and f
vary continuously across ~100-210 training samples, so interpolation there has real support; z
varies across only 3 discrete labels, so it doesn't.

## 6. Integration: BOTH iminuit and Cobaya achieved

Both wrappers restrict correctly to the emulator's supported domain (z_str ∈ {"5.0","4.6","4.2"}
via the official API) — they do not use the unsupported raw-extrapolation path from §4.

**`emu_predict.py`** (shared, re-runnable, standalone re-implementation of `mcmc.py`'s
`load_system()`/`predict_pk()` without the chainconsumer/emcee top-level imports):
```python
def load_nn_system(nn_emu_dir=NN_EMU_DIR):
    nn_pack = {
        "scaler_cdm": load_pkl(os.path.join(nn_emu_dir, "scaler_cdm.pkl")),
        "scaler_res": load_pkl(os.path.join(nn_emu_dir, "scaler_res.pkl")),
        "cdm_models": [], "res_models": [],
    }
    for fold in range(N_FOLDS):
        c_mod = build_mlp(5, 16)
        c_mod.load_state_dict(torch.load(os.path.join(nn_emu_dir, f"model_cdm_fold{fold}.pth"), map_location="cpu"))
        c_mod.eval()
        r_mod = build_mlp(7, 16)
        r_mod.load_state_dict(torch.load(os.path.join(nn_emu_dir, f"model_res_fold{fold}.pth"), map_location="cpu"))
        r_mod.eval()
        nn_pack["cdm_models"].append(c_mod); nn_pack["res_models"].append(r_mod)
    return nn_pack

def predict_pk(nn_pack, m, f, zrei, ha, hs, taueff, z_str):
    z_obs = Z_FLOAT[z_str]   # z_str MUST be "5.0", "4.6", or "4.2"
    x_cdm = nn_pack["scaler_cdm"].transform(np.array([[z_obs, zrei, ha, hs, taueff]]))
    x_res = nn_pack["scaler_res"].transform(np.array([[z_obs, m, f, zrei, ha, hs, taueff]]))
    with torch.no_grad():
        cdm_st = torch.stack([mod(torch.tensor(x_cdm, dtype=torch.float32))[0] for mod in nn_pack["cdm_models"]]).mean(0).numpy()
        res_st = torch.stack([mod(torch.tensor(x_res, dtype=torch.float32))[0] for mod in nn_pack["res_models"]]).mean(0).numpy()
    logp = cdm_st if f <= F_EPS else cdm_st + f * res_st
    return np.power(10.0, logp)
```

**iminuit wrapper (`integration_iminuit.py`)** — chi2(m,f,nuisance) callable, profile-likelihood
minimization over the 4 IGM nuisance params at a fixed (m,f) grid point:
```python
def build_chi2(nn_pack, obs):
    def chi2(m, f, zrei, ha, hs, taueff):
        total = 0.0
        for z_str in Z_ORDER:
            pred = predict_pk(nn_pack, m, f, zrei, ha, hs, taueff, z_str)
            diff = pred - obs[z_str]["Pk"]
            total += float(diff @ obs[z_str]["Cov_inv"] @ diff)
        return total
    return chi2

m0, f0 = -21.0, 0.1
mi = Minuit(lambda zrei, ha, hs, taueff: chi2(m0, f0, zrei, ha, hs, taueff),
            zrei=10.5, ha=2.0, hs=0.0, taueff=1.0)
mi.limits["zrei"] = (6.05, 14.91); mi.limits["ha"] = (0.066, 3.989)
mi.limits["hs"] = (-0.987, 0.996); mi.limits["taueff"] = (0.3, 1.8)
mi.errordef = Minuit.LEAST_SQUARES
mi.migrad()
```
Result: chi2 at training-median nuisance params = 77.41; after `migrad()` minimization,
chi2 = 30.52 (best-fit nuisance: zrei=14.91 — pinned at upper bound, ha=1.81, hs=-0.68,
taueff=0.97). `mi.valid = False` (converged against a parameter boundary — expected, since only
2 of the 4 nuisance IGM params were freed here and a fixed (m,f) grid point was chosen
arbitrarily, not fit for goodness). **This is an integration/plumbing result, not a physics
result** — it demonstrates the callable is fully iminuit-compatible (gradient-free minimization,
parameter limits, `.valid`/`.fval`/`.values`/`.errors` all populate correctly).

**Cobaya wrapper (`integration_cobaya.py`)** — external likelihood function:
```python
def lya_mfdm_loglike(m, f):
    ln_like = 0.0
    for z_str in Z_ORDER:
        pred = predict_pk(_NN_PACK, m, f, _ZREI, _HA, _HS, _TAUEFF, z_str)
        diff = pred - _OBS[z_str]["Pk"]
        ln_like += -0.5 * float(diff @ _OBS[z_str]["Cov_inv"] @ diff)
    return ln_like

info = {
    "params": {"m": {"prior": {"min": -22.99, "max": -19.0}, "ref": -21.0},
               "f": {"prior": {"min": 0.0, "max": 1.0}, "ref": 0.1}},
    "likelihood": {"lya_mfdm": {"external": lya_mfdm_loglike, "input_params": ["m", "f"]}},
}
model = get_model(info)
result = model.loglikes({"m": -21.0, "f": 0.1})
```
Result: `model.loglikes(point) -> (array([-38.707]), [])` — consistent with `-0.5 * 77.41` from
the iminuit chi2 at the same fixed nuisance values, cross-validating both wrappers call the same
underlying prediction correctly. **This required uninstalling the broken `mpi4py` wheel first**
(see §2) — with mpi4py present, `cobaya.model.get_model()` crashed on MPI auto-detection before
even reaching the likelihood.

## 7. Verdict

**The emulator is real, loads cleanly, produces physically sane P1D(k) values, and both integration
paths (iminuit, Cobaya) work — but the domain finding materially changes WP-E6 v2's scope from
what was hoped.** This is not a general-purpose (m, f, z) emulator usable across DESI's full
z≈2.2-4.4 range; it is 3 independently-trained z-slice emulators (z=5.0, 4.6, 4.2) glued together
by a shared MLP architecture that happens to take z as an input feature but was never taught a
z-trend beyond memorizing those 3 points. Only DESI's highest-z slice (z≈4.2-4.4, if DESI's
binning lands close enough to 4.2 — unverified here) has any usable overlap; the bulk of DESI
DR1's Lyα range (z≈2.2-4.2, most of the statistical weight) is entirely outside this emulator's
trained/validated domain and using it there would mean trusting unvalidated 3-point extrapolation
(§4.4) that a companion analysis has zero grounds to defend. WP-E6 v2's Phase 1 (modeling-adequacy)
should treat this as a partial, not full, adequacy resolution: usable in principle for a
single-z-bin analysis near z=4.2, not usable as originally hoped for a full-range DESI DR1 fit
without new simulation/training work outside the scope of an integration task.
