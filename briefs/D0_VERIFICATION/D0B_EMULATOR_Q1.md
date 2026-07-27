# D0-B — Q1 Emulator Re-Survey (Independent Verification)

**Date:** 2026-07-27
**Agent:** D0-B (Sonnet)
**Question:** Is there a publicly obtainable Lyman-α 1D flux power spectrum (P1D) emulator in
which BOTH the axion/FDM particle mass m_φ AND the FDM mass fraction f_FDM are free parameters?

## HEADLINE VERDICT: EMULATOR_AVAILABLE

The prior internal finding ("no code release found" for Liu/Gong/Zhou 2026) is **REVALIDATED AS
STALE / WRONG**. The paper's own Acknowledgments section states the code, data, and trained
emulators are public.

**Primary evidence:**
- Paper: Liu, Gong & Zhou, "Lyman-α forest constraints on pure and mixed fuzzy dark matter,"
  arXiv:2606.06969 (submitted 2026-06-05). Fetched directly (arxiv.org/html/2606.06969).
- Exact quote from the paper's Acknowledgments: *"Some of the main code, data, and trained
  emulators used in this work are available at
  https://github.com/jianxiangl-astro/lya-mfdm"*
- Repo verified to exist and load (fetched directly, 2026-07-27): public, owned by
  `jianxiangl-astro`, 12 commits on main. README: "Code and data for Lyman-alpha forest
  constraints on pure and mixed fuzzy dark matter" (Liu et al. 2026). Contains an `emu/`
  directory holding **trained emulator model files** (not just training scripts), and an
  `environment.yml`. No explicit LICENSE file was visible in the fetched excerpt — flag this
  for whoever attempts to install/use it.
- Free-parameter confirmation, quoted from paper §3.2: *"The second stage emulator additionally
  takes two dark matter parameters, log₁₀(m_FDM/eV) and f_FDM, and predicts the response
  function."* Ranges: log₁₀(m_FDM/eV) ∈ [−23, −19], f_FDM ∈ [0, 1].
- Observable: the emulator's stage 1 predicts the **CDM 1D flux power spectrum** and stage 2
  predicts the **mixed-FDM response relative to that CDM baseline** — i.e. it emulates the
  target observable (P1D) directly, not the matter power spectrum.

This satisfies the decisive criterion in full: both m_φ and f_FDM are free, and the emulated
observable is P1D itself, not a proxy.

**Caveat / what D0-B did NOT verify (out of budget/scope, flag for Phase 1 if this proceeds):**
installation success, whether the trained weights actually load and run, whether the
calibration domain (k-range, z ∈ {5.0, 4.6, 4.2}, mass/fraction grid) covers the WP-E6
Phase-0 surviving region and the DESI z = 2.2–4.4 range, license terms, and numerical accuracy
claims. These are exactly what a Phase-1-style adequacy check would need to establish before
any reliance on it. D0-B confirms **public existence and parameter coverage only.**

---

## Per-Candidate Table

| candidate | code public? | observable | m_φ free? | f_FDM free? | verdict | evidence URL |
|---|---|---|---|---|---|---|
| **Liu/Gong/Zhou 2026 (lya-mfdm)** | **YES** — github.com/jianxiangl-astro/lya-mfdm, cited in-paper | Lyman-α 1D flux power spectrum (P1D), two-stage NN (CDM baseline + mixed-FDM response) | **YES** (log₁₀ m ∈ [−23,−19]) | **YES** (f ∈ [0,1]) | **EMULATOR_AVAILABLE** | arxiv.org/abs/2606.06969 (paper); github.com/jianxiangl-astro/lya-mfdm (repo, fetched directly) |
| LaCE (igmhub/LaCE) | yes, github.com/igmhub/LaCE | Lyman-α 1D flux power spectrum | effectively no — compressed ΛCDM basis (Δ²_p, n_p + 4 IGM params), no axion mass channel | no | wrong-shape / not applicable | github.com/igmhub/LaCE |
| cup1d (igmhub/cup1d) | yes | P1D cosmology/MCMC layer on LaCE | no | no | wrong-shape / not applicable | github.com/igmhub/cup1d |
| lym1d (schoeneberg/lym1d) | yes | P1D likelihood, GP over Lyssa sims | no | no | wrong-shape / not applicable | github.com/schoeneberg/lym1d |
| ForestFlow (igmhub/ForestFlow) | yes | 3D flux power spectrum (not P1D) | no | no | wrong observable | github.com/igmhub/ForestFlow |
| axionCAMB (dgrin1/axionCAMB) | yes | linear matter transfer function (Boltzmann code, not P1D, not an emulator) | yes | yes | **PARTIAL** — both params free but wrong observable class (linear transfer function, not flux power; not an emulator) | github.com/dgrin1/axionCAMB; arxiv 2104.07802 |
| axionHMcode (SophieMLV/axionHMcode) | yes | non-linear **matter** power spectrum (halo model), not flux/P1D | yes | yes, but calibrated/validated only to f ≤ 0.3 (accuracy degrades beyond) | **PARTIAL** — both params technically free, but wrong observable (matter power, not P1D) and narrow calibrated fraction range | github.com/SophieMLV/axionHMcode; arXiv:2409.11469 |
| Axion-Emulator (frdennis/Axion-Emulator) — **new candidate found this session** | yes, github.com/frdennis/Axion-Emulator, stated in-paper | non-linear **matter** power spectrum (NOT P1D) | yes (log₁₀ m_ax/eV ∈ [−28,−22]) | yes (f_ax ∈ [0.001, 1]) | **PARTIAL** — both params free, matches the decisive criterion on parameters, but emulates the wrong observable (3D matter power, not Lyman-α P1D) | aanda.org/articles/aa/full_html/2025/10/aa54621-25/aa54621-25.html (A&A, fetched directly, confirms availability statement) |
| arXiv:2604.06038 (mixed FDM+CDM Lyα, hybrid Schrödinger-Poisson + N-body) | not established as an emulator release — single parameter point (m₂₂=0.01, f_A=0.1), not a trained model spanning a grid | Lyman-α forest flux statistics | fixed at single value, not free | fixed at single value, not free | not an emulator (single forward-model point) | arxiv.org/abs/2604.06038 |

**The decisive column is f_FDM.** Only two candidates have it genuinely free: Liu/Gong/Zhou 2026
(lya-mfdm) and the newly found Axion-Emulator. Of those, **only lya-mfdm emulates the correct
observable (P1D)** — Axion-Emulator emulates the 3D matter power spectrum, which is exactly the
"wrong observable" failure mode this survey was designed to catch (cf. axionHMcode). Every other
LCDM-shaped P1D tool (LaCE/cup1d/lym1d/ForestFlow) has neither parameter free at all.

---

## Conclusion for D0 gate

**Q1 is answered: EMULATOR_AVAILABLE.** Per the coordinator gate table in
`D0_AGENT_PLAN_2026_07_27.md`, this is the "major unblock" branch — Directive 4 (mixed-(m,f)
FDM emulator) is potentially a real drop-in, not absent. Per the plan's own validation rule,
**the coordinator should independently open
`https://github.com/jianxiangl-astro/lya-mfdm` before acting on this** — D0-B confirmed the repo
loads and its stated contents, but did not clone it, run it, or verify the trained weights
execute. No Option-B costing is included because the verdict is not CONFIRMED_ABSENT.

No author contact was needed or attempted (rule 4 compliant — the code is already public, cited
directly in the paper's own text).

---

**Web calls used:** 9 of 18 budgeted (2 WebSearch scoping + 2 WebFetch primary-source abstract
checks + 1 WebFetch full-text code-availability check + 1 WebFetch A&A paper + 1 WebFetch GitHub
repo + 2 WebSearch for axionCAMB/axionHMcode). Stopped early per stop-condition: a clear
EMULATOR_AVAILABLE case with both parameters free was found.
