# Deep Think ML-for-X₄ Proposal — Archive & T1 Disposition

**Date:** 2026-07-27, night
**Source:** Deep Think (T0s), via Xavier (correct paste; an earlier mispaste is recorded in
`~/literature_review/phase2_geometry/ANALYSIS_MF_GRID_AUDIT_2026_07_27.md`, re-receipt note).
**Authority:** T1 under Xavier's standing "audit and make your own decisions"; Phase-M gate
ownership stays with T0 throughout.

---

## 1. The proposal (faithful summary)

Deep Think proposes to attack Stream 2's M1′ structural blocker (no exhibited Calabi-Yau
fourfold X₄) with ML-assisted algebraic geometry:

- **Step 1 (X₄ search):** use `Tancredi-Schettini-Gherardini/P5CY4ML` (ML on CY 4/5/6-folds as
  hypersurfaces in weighted ℙ⁵) + `CYTools` to scan weight systems / Kreuzer–Skarke-class data
  for an X₄ admitting a K3 fibration whose fiber matches the certified lattice data
  (T ≅ U⊕⟨14⟩, ρ=19). Explicitly grounds on the certificate and explicitly repudiates the
  Kodaira Type II framing (its own F6 guardrail).
- **Step 2 (metrics → 𝒱):** feed the found X₄ into `cyjax` / `cymetric` (ML Ricci-flat metric
  approximation), extract volume 𝒱 and intersection ratios for the flux potential.
- **Step 3 (bridge + constrained sweep):** emit `eft_geometric_priors.json` mapping 𝒱 to FDM
  mass via m_φ ≈ M_P(W₀/𝒱^x); Stream 3 then **restricts** the DESI (m,f) sweep grid to those
  theory-derived mass bounds.

## 2. Disposition — per step

### Step 1: ACCEPT AS CANDIDATE WORK PACKAGE (WP S2-G), pending verification + T0 gate

This is the strongest inbound idea of the night, because it fits the house pattern **"ML
proposes, checker certifies"**: an ML-guided *search* is epistemically harmless if every hit
is then certified by exact methods — and the certification step here (does a candidate's K3
fiber carry the right lattice polarization?) is exact integer lattice arithmetic, squarely
inside Stream 2's demonstrated competence (the same machinery that produced the U⊕⟨14⟩
witnesses). An exhibited, exactly-certified X₄ is precisely what the M1′ gate asks for; the
search being ML-guided taints nothing, exactly as an LLM-suggested Lean proof taints nothing
once the kernel accepts it.

**Held back pending two things:**
1. **D0-G repo verification (launched tonight, read-only):** existence, maintenance, licenses,
   and three fitness questions the proposal glosses:
   - Does CYTools actually operate on **fourfolds**? Its home turf is the Kreuzer–Skarke 4d-
     polytope database → CY **threefolds**. The proposal may contain a dimension error at its
     load-bearing joint; if CY4 support is absent, the toolchain is P5CY4ML-only, which (per
     its own title) does Hodge-number ML — not fibration-lattice analysis.
   - Can any cited tool filter fibrations by **lattice polarization** at U⊕⟨14⟩ specificity,
     or only detect that *some* K3 fibration exists? If the latter, the exact-certification
     layer must be built in-house (scoping impact, not a blocker).
   - A technical subtlety the proposal elides and T0/checkers must pin before any scan: the
     fibration-matching datum is the fiber's **Néron–Severi/polarization lattice** (rank-19 M
     with M⊥ ≅ T), not T itself. "Fiber matches U⊕⟨14⟩" is shorthand that would be wrong if
     implemented literally. The WP definition must state the match criterion in NS terms,
     from Nikulin-style genus arithmetic — exact, certifiable, but it must be *designed*, not
     assumed.
2. **T0 sign-off:** M1′/D2′ made Phase M dormancy a T0 ruling; a search WP aimed at
   satisfying its gate condition should be opened by T0, not by me. The WP S2-G proposal doc
   goes to T0 with D0-G results attached.

### Step 2: PARTIALLY REJECT — confused as written, and F5b-circular where it matters

- **𝒱 does not come from ML metrics.** In the moduli-space sense used by flux
  compactifications, the classical volume is a polynomial in Kähler moduli with **exact
  integer intersection numbers** — which polytope tools compute exactly. ML Ricci-flat
  metrics (cymetric/cyjax) are for quantities that genuinely need the metric (e.g. matter
  Yukawas); invoking them for 𝒱 is repo-name-dropping beyond need, and their outputs are
  numerical approximations without error certificates — "tight bounded interval" is not a
  thing they emit. Anything from this route is Tier (N) at best, labeled as such.
- **The F5b circle:** 𝒱 is not a *number* until Kähler moduli are stabilized; stabilization
  needs the flux potential; the tadpole/flux problem "is not posable until a threefold base
  B₃ is specified" (ledger, T0 D4). Exhibiting X₄ (Step 1) is what makes the problem
  *posable* — it does not by itself produce a stabilized 𝒱. Step 2 as written skips from
  "metric exists" to "volume number" across the exact gap F5b marks as open.

### Step 3: REJECT OUTRIGHT — this would dismantle the program's falsification architecture

The bridge formula **m_φ ≈ M_P(W₀/𝒱^x) has an unspecified exponent and an unspecified W₀** —
a formula with a free power is not a prior, it is numerology-shaped, and generating m_φ from
it is verbatim the Tier-C move the ledger blocks ("do not assume, generate, or backfill exact
observables (m_φ, …)").

Worse is what it would do to Stream 3: **restricting the empirical grid to theory-preferred
masses welds prediction to measurement.** The three-stream design derives its entire
adversarial value from their separation — F3/F4 falsification triggers only mean something if
the data sweep is *able* to land outside the theory's preferred region. The correct geometry-
empirics interaction is an **overlay at comparison time**: the 56-cell sweep runs on the full
emulator-supported domain (hash-anchored at `27cff4a`; changes via countermand only), and any
future certified geometric bound is drawn on top of the finished exclusion plot. That costs
nothing (cells are independent), preserves independence, and makes agreement — if it occurs —
*evidence* rather than construction. Also noted: the directive's target file
`pipeline/transverse.py` belongs to the WP-E5 transverse route, CLOSED by data floors —
stale reference.

## 3. Actions taken tonight

1. **D0-G verification agent launched** (Sonnet, read-only, web-capped): the four repos +
   the three fitness questions above. Output: `briefs/D0_VERIFICATION/D0G_CY_ML_REPOS.md`.
2. This disposition filed and pushed; grid definition untouched; no scan, no clone-into-repo,
   no Phase M action.
3. Next (after D0-G returns): draft **WP S2-G proposal** for T0 — search-and-certify design,
   NS-lattice match criterion, tier labeling ((N) for ML screens, (E) for exact
   certifications), explicit non-goals (no 𝒱→m_φ bridge, no grid coupling).

## 4. One-line summary for T0 (pre-verification)

Deep Think's Step 1 is the right idea wearing two wrong siblings: ML-guided search with exact
certification could genuinely open the M1′ gate and deserves a verified, T0-gated WP; the
volume-to-mass bridge and the constrained sweep are F5b violations that would trade the
program's falsifiability for the *appearance* of top-down constraint, and are declined.

---

## 5. ADDENDUM — D0-G verification returned (same night): the toolchain claim FAILED

Full report: `briefs/D0_VERIFICATION/D0G_CY_ML_REPOS.md` (coordinator spot-checked the fitness
sections against the cited primary sources' quoted text).

**All four repos are real. None can do what the proposal assigned them.**

| Repo | Verdict | Fitness for the X₄ search |
|---|---|---|
| CYTools (`LiamMcAllisterGroup/cytools`, GPL-3.0, maintained) | CONFIRMED | **CY3-only.** Built on the Kreuzer–Skarke 4d-polytope list → threefolds by construction; its own README example is "the quintic Calabi-Yau *threefold*"; zero matches for "fourfold" or "fibrat" in README/docs. Using it to search for an X₄ is a load-bearing dimension error, exactly as suspected in §2 |
| P5CY4ML (arXiv:2311.17146, **no LICENSE**) | CONFIRMED | Does handle CY4 weight systems — but is Hodge-number regression only; **zero fibration or lattice logic**. Also unlicensed → same non-redistribution handling as lya-mfdm |
| cyjax (Apache-2.0) | CONFIRMED | CY3-shaped examples only, no CY4 evidence; **stale since 2023-07** |
| cymetric | CONFIRMED, canonicity ambiguous | Two variants (paper-linked GPL-3.0 vs Ruehle's MIT fork); no CY4 evidence; CY3-scoped in practice |

**Fitness B (the decisive capability):** *no repo among the four computes fiber lattice /
Picard / polarization data* — the actual match criterion against the certified U⊕⟨14⟩ result.
That layer would have to be built in-house regardless of which search tool ran underneath.

**One incidental lead, honestly labeled:** D0-G surfaced arXiv:2511.10601 ("Classifying Fibers
and Bases in Toric Hypersurface Calabi-Yau *Threefolds*") — adjacent research doing toric
K3/elliptic-fibration classification, but on CY3s, existence/type-level, unopened and
unverified here. Filed as a future-diligence pointer only.

## 6. FINAL RULING (T1, delegated authority)

**WP S2-G is NOT opened on the basis of this proposal.** The recommendation to T0 changes
from "verified toolchain, your gate" to: **the proposed ML shortcut does not exist as
described.** The load-bearing tool is dimension-wrong (CY3 vs CY4), the CY4-capable tool has
no fibration/lattice capability, and the one capability the search actually turns on — exact
fiber-polarization matching — exists in no off-the-shelf tool and would be an in-house build
sitting on top of a largely classical (non-ML) polytope analysis. That is a genuine research
work package with real cost, not a clone-and-scan acceleration; if T0 wants the X₄ hunt, it
should be scoped as such, on its own merits, with the in-house exact-lattice layer as the
core deliverable and any ML component as optional pre-filtering at (N) tier.

Steps 2–3 remain rejected per §2–§3 (unchanged by verification — they failed on ledger
grounds, not tooling grounds).

**Net effect of tonight's Deep Think proposal:** one good architectural idea (ML proposes,
checker certifies) retained for whenever the X₄ hunt is genuinely scoped; zero repos adopted;
the falsification firewall between Streams 2 and 3 explicitly reaffirmed; the D0 gate caught
a dimension error *before* any agent cloned a repo or wrote a line of integration code —
which is the intake protocol doing precisely what it was built to do, at the cost of one
read-only verification agent.
