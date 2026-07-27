# D0-G Verification: ML-for-Algebraic-Geometry Toolchain for X₄ K3-Fibration Search

**Agent:** D0-G (read-only verification gate)
**Date:** 2026-07-27
**Scope:** Verify existence/fitness of 4 named repos for a proposal to search for a Calabi-Yau
FOURFOLD (X₄) admitting a K3 fibration with prescribed fiber lattice data, using ML-for-AG tools.
**Method:** Primary sources only (GitHub API/README, cy.tools docs, linked arXiv abstracts).
14 web calls used (WebSearch + WebFetch) + unlimited local `curl` to GitHub REST API (not counted
against web-call budget). No repos cloned, nothing installed, nothing committed.

---

## Repo Table

| # | Named path | Verdict | Canonical URL | Last commit (pushed_at) | Stars | License | Actual purpose (from repo's own README) | Companion arXiv |
|---|---|---|---|---|---|---|---|---|
| 1 | `Tancredi-Schettini-Gherardini/P5CY4ML` | **CONFIRMED** (exists exactly as named; title claim slightly imprecise) | https://github.com/Tancredi-Schettini-Gherardini/P5CY4ML | 2024-05-08 | 3 | **None** (no LICENSE file in repo) | "Statistical analysis and machine learning applied to the dataset of Calabi-Yau four-folds as hypersurfaces in weighted projective spaces; including symbolic regression" — regresses/approximates Hodge numbers from 6-weight systems (generalized to P5/P6/P7 for 4-/5-/6-folds); PCA on weight systems. **No** geometric/fibration analysis. | 2311.17146 ("Calabi-Yau Four/Five/Six-folds as ℙ_w^n Hypersurfaces: Machine Learning, Approximation, and Generation") |
| 2 | `CYTools` / `cy.tools` | **CONFIRMED**, canonical GitHub org is `LiamMcAllisterGroup/cytools` (not stated in the proposal, but this is the repo cy.tools points to) | https://github.com/LiamMcAllisterGroup/cytools ; site https://cy.tools | **2026-07-27** (actively maintained, pushed today) | 45 | GPL-3.0 | "A software package for analyzing Calabi-Yau manifolds arising from the Kreuzer-Skarke database" — polytope/triangulation engine computing topological data (Hodge numbers, intersection numbers) of Calabi-Yau hypersurfaces in toric varieties. README's own quick-start example computes h11/h21 for **"the quintic Calabi-Yau **threefold**"**. | 2211.03823 ("CYTools: A Software Package for Analyzing Calabi-Yau Manifolds") |
| 3 | `ml4physics/cyjax` | **CONFIRMED** exact match | https://github.com/ml4physics/cyjax ; docs https://cyjax.readthedocs.io | 2023-07-12 (**3 years stale** relative to today) | 19 | Apache-2.0 | "Machine learning Calabi-Yau metrics with JAX" — numerically approximates Ricci-flat CY metrics via Donaldson's algorithm + ML curve-fitting; README states implementation is "limited to varieties defined by a single defining equation on one complex projective space" (single hypersurfaces). Worked examples: quintic, Dwork family (both CY3). | 2211.12520 |
| 4 | `ruehlef/cymetric` | **CONFIRMED but ambiguous canonicity** — this is Fabian Ruehle's personally maintained variant, not the org the companion paper cites | https://github.com/ruehlef/cymetric (variant); canonical project org appears to be https://github.com/pythoncymetric/cymetric | ruehlef fork: 2026-06-06; pythoncymetric/cymetric: 2026-06-12 (both actively maintained) | ruehlef: 5; pythoncymetric: 28 | ruehlef: **MIT**; pythoncymetric: **GPL-3.0** ⚠ different licenses — matters for adoption, pick one deliberately | "A package to compute Calabi-Yau metrics in pytorch, jax, or tensorflow, with mathematica support" (ruehlef) / "A python library for studying Calabi-Yau metrics" (pythoncymetric) — moduli-dependent CY metric learning via neural nets, self-supervised loss functions. Examples center on CICY and Kreuzer-Skarke CY manifolds (standard string-phenom usage = CY3), quintic tutorials. | 2111.01436 ("Learning Size and Shape of Calabi-Yau Spaces") |

---

## Fitness Questions

### A. Dimension check on CYTools — does it operate on CY FOURFOLDS or threefolds only?

**Finding: CYTools is documented and evidenced as CY-THREEFOLD-only. No primary source checked
shows native CY4 support.**

- CYTools is built on "the Kreuzer-Skarke database" (README, about page, arXiv:2211.03823 abstract).
  The Kreuzer-Skarke list is, by definition and universally in the literature, the classification
  of the **473,800,776 reflexive polytopes in 4 (lattice) dimensions**. Standard toric-hypersurface
  construction: an anticanonical hypersurface in the toric variety of an *n*-dimensional reflexive
  polytope has **complex dimension n−1**. A 4-dimensional reflexive polytope therefore yields a
  **Calabi-Yau THREEFOLD**, not a fourfold. (This is the textbook KS setup — confirmed independently
  by the WebSearch summary: "Kreuzer and Skarke tabulated all 473,800,776 reflexive polyhedra in four
  dimensions... a four-dimensional toric variety can be constructed in which the anticanonical
  hypersurface is a Calabi-Yau variety" — i.e. CY3.)
- CYTools's own README "Quick example" is explicit: it constructs a polytope from a 4×5 vertex set
  and states in plain text: *"compute the Hodge numbers of the quintic Calabi-Yau **threefold**"*.
- Grepped the full README (`raw.githubusercontent.com/LiamMcAllisterGroup/cytools/main/README.md`)
  for "fibrat" and "four-fold/fourfold" — **zero matches** for either. The `about` page and
  `docs/getting-started` page (fetched directly) likewise make no dimension statement beyond the
  general "Calabi-Yau manifolds arising from the Kreuzer-Skarke database" framing.
- A **separate** Julia project exists, `Julia-meets-String-Theory/CYTools.jl`, whose own description
  explicitly flags 4-fold support as future/separate work: *"Specialized algorithms for CICYs, 3 and
  **4-dimensional** reflexive polytopes... will be collected"* — i.e., even the community's own
  forward-looking description treats 4-fold-capable tooling as not-yet-delivered, distinct from the
  core Python CYTools.
- No CY4-capable function, flag, or example was found in any fetched primary source.

**Conclusion: if the proposal uses CYTools to search for an X₄ (complex dim 4), that is a load-bearing
dimension error as written.** CYTools operates on the standard 4D-reflexive-polytope Kreuzer-Skarke
list, which produces CY3s, not CY4s.

### B. Fibration filtering — can CYTools / P5CY4ML detect K3-fibration structure, and if so, does it characterize the fiber's lattice/polarization, or only detect that a fibration exists?

**Finding: UNVERIFIED / NOT CONFIRMED at the precision the proposal needs, for either named tool.**

- P5CY4ML's README (fetched) makes **no mention** of fibration detection or lattice/Picard data of
  any kind — it is purely a Hodge-number regression / symbolic-regression / PCA tool over weight
  systems. Not applicable to fibration filtering at all.
- For CYTools: no fibration-related function turned up in the README (grep for "fibrat" = 0 hits),
  the `about` page, or the `docs/getting-started` page. A site-restricted search (`site:cy.tools
  fibration`) returned no indexed hits on the fibration topic either — a weak negative signal
  (could reflect incomplete indexing rather than true absence), but converges with the README grep.
- A **separate, adjacent** research paper turned up in search — "Classifying Fibers and Bases in
  Toric Hypersurface Calabi-Yau **Threefolds**" (arXiv:2511.10601) — which does perform toric
  elliptic/K3-fibration classification over 4D reflexive polytopes, plausibly using CYTools as
  underlying infrastructure. This is a **research result / dataset**, not a documented built-in
  CYTools API, and — critically — it operates on **CY3s**, not CY4s (consistent with finding A).
  I did not open this paper (outside the 4-repo scope and budget); its precise capability
  (existence-only vs. fiber-lattice/polarization computation) is unverified here and would need
  separate diligence if the team pivots the target to CY3.
- **No evidence in any of the four named repos of fiber lattice / Picard / polarization computation.**
  At most, adjacent unverified research exists for fibration *classification* (type/existence) on
  CY3s — a materially weaker capability than "characterize the fiber's lattice/polarization data,"
  which the proposal requires.

### C. Dimension check on cymetric and cyjax — CY4 or CY3 only?

**Finding: UNVERIFIED explicit statement either way in fetched material; all available evidence
(worked examples, companion papers) is CY3-shaped, with zero CY4 evidence found.**

- **cyjax** (arXiv:2211.12520 / README): implementation is explicitly stated as "limited to
  varieties defined by a single defining equation on one complex projective space" — i.e.,
  hypersurfaces in a single P^n. This phrasing is dimension-agnostic in principle (a hypersurface
  in P^n could be dimension n−1 for any n), but every worked example found (quintic, Dwork family)
  is the classical CY3 quintic-type construction. No CY4 example, flag, or statement found. Last
  commit 2023-07-12 — 3 years stale, itself a fitness concern independent of dimension.
- **cymetric** (arXiv:2111.01436 / pythoncymetric+ruehlef READMEs): scoped to "CICY and
  Kreuzer-Skarke Calabi-Yau manifolds at any point in Kähler/complex-structure moduli space."
  CICYs (complete intersection CYs) *can* in principle be constructed at CY4 dimension, but the
  paper title ("Learning **Size and Shape** of Calabi-Yau **Spaces**") and all referenced tutorials
  (Fermat quintic) target CY3. No explicit CY4 statement or example found in the material fetched.
- Neither repo's primary sources explicitly rule CY4 in or out; the honest verdict is
  **UNVERIFIED for CY4**, with the balance of evidence (100% of worked examples across both tools
  being CY3) weighing against a working CY4 pipeline existing today without nontrivial extension work.

---

## Bottom Line (5 lines)

The proposed toolchain is **NOT capable** of the X₄-with-K3-fibration-lattice search as described.
CYTools — the only tool with actual fibration-adjacent capability — is documented, evidenced (README
quick-example, arXiv abstract, community fork description) as **CY3-only** via the standard
Kreuzer-Skarke 4D-polytope list; using it for an X₄ search is a load-bearing dimension error, not a
minor gap. No repo among the four was found to compute fiber lattice/Picard/polarization data — at
best, unverified adjacent CY3 research (arXiv:2511.10601, not one of the four named repos) does
fibration *classification*, a strictly weaker capability. cymetric/cyjax show zero CY4 evidence
either, so even the metric-learning half of the pipeline is unconfirmed for X₄. Recommendation:
either (a) re-scope the search to CY3 (where the toolchain's evidenced capabilities actually match),
or (b) before adopting for CY4, get a direct answer from the CYTools maintainers/paper authors on
whether/how the package extends beyond 4D reflexive polytopes — do not proceed on the assumption
that CY3-oriented documentation silently generalizes.
