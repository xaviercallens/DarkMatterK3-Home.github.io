# WP S2-G — X₄ Exhibition Plan (Proposal; NOT YET IMPLEMENTED)

**Date:** 2026-07-27, night
**Status:** PROPOSAL awaiting T0 sign-off. Nothing herein is authorized to run until T0 opens
the gate, phase by phase. Canonical copy: Stream 2; mirrored to Streams 1 and 3.
**Provenance:** salvages the one sound idea from Deep Think's ML-for-X₄ proposal
(disposition: S3 `briefs/DEEPTHINK_PROPOSAL_ML_X4_DISPOSITION_2026_07_27.md`; toolchain
verification: S3 `briefs/D0_VERIFICATION/D0G_CY_ML_REPOS.md`) and replaces its failed
toolchain with a derivation-first design grounded in the project's own certified assets.
**Epistemic frame:** every deliverable carries a tier label; ML appears only as optional
(N)-tier pre-filtering in the contingency route; no step emits a physical observable — F5b
stands throughout; Stream 3's empirical independence is untouched by design.

---

## 0. What this plan is for

The M1′ gate: Phase M option B stays dormant until an X₄/B₃ is **exhibited**. This plan is a
phased, stop-conditioned route to exhibiting one — or to establishing, honestly, that the
natural construction is obstructed (itself a publishable structural result, per house style:
a documented dead end beats an undocumented detour).

**The design inversion that makes this legitimate where the inbound proposal was not:**
Deep Think proposed *searching* databases for a fourfold whose K3 fiber happens to match the
certified lattice data — using tools that verification showed cannot do this (CYTools is
CY3-only; nothing off-the-shelf computes fiber polarization). But the project already
possesses the exact object the search would hope to find: **the cooper_s7 family itself is a
1-parameter, lattice-polarized K3 family with certified ρ = 19, T ≅ U⊕⟨14⟩ [B, double-
verified].** A fourfold with precisely the right generic fiber can therefore be **built from
the family by construction** — fiber the known family over a base surface — rather than found
by scanning. The matching problem that dominated the inbound proposal's cost *vanishes*: the
fiber is right because it is the certified family, not because a scan said so.

## 1. Route A (primary) — fiber the certified family over a base surface

**Idea (classical algebraic geometry, no ML anywhere):** the cooper_s7 family is a K3 family
over its z-line (the X₀(7)+ modular curve). Choose a base surface B₂ and a map
φ: B₂ → (z-line); pull the family back along φ and compactify/resolve to a total space X₄.
The generic fiber of X₄ → B₂ is a member of the certified family — right lattice data by
construction.

**What must be verified exactly (each item is a checker deliverable, not an assumption):**
- **(G1-a) CY condition:** c₁(X₄) = 0 requires the right twist data for the compactified
  pullback (the K3-fibration analogue of Weierstrass −4K/−6K twisting). May constrain or
  exclude candidate (B₂, φ) pairs. Symbolic computation, tier (E) on pass.
- **(G1-b) Degenerate fibers:** over φ⁻¹ of the family's singular loci ({−1, 1/27} — which the
  ledger fixes as order-2 elliptic points of X₀(7)+, NOT Kodaira degenerations; E-008/E-009
  applies inside this plan too) and over the ∞-type boundary points, the pullback degenerates.
  Crepant resolvability keeping c₁ = 0 must be established case-by-case. This is the plan's
  main mathematical risk and the most likely honest stop-point.
- **(G1-c) F-theory posability:** for the tadpole to become *posable* (ledger, T0 D4), an
  elliptic fibration with section over a threefold base B₃ is needed. Design expectation, to
  be certified not asserted: the fiber's NS lattice (computed in Phase G0 as the Nikulin
  complement of the certified T) is expected to contain a hyperbolic-plane summand U, which
  gives each K3 fiber an elliptic fibration with section over P¹ — composing to X₄ elliptic
  over a B₃ that is a P¹-fibration over B₂. If G0's certified NS genus lacks the U summand,
  this expectation dies and the plan halts at G0 — cheaply.

**Candidate B₂ ladder (simplest first, per three-strikes house rule):** P², P¹×P¹, Hirzebruch
F_n, with φ of low degree; escalate only on documented obstruction.

## 2. Route B (contingency only) — weight-system scan with in-house certifier

Activated ONLY if Route A hits a documented stop condition at G1. Uses the CY4 weight-system
dataset domain that P5CY4ML operates on (the dataset's own provenance/license to be checked —
P5CY4ML repo itself has NO LICENSE and is read-only reference, never redistributed, same
handling as lya-mfdm). The load-bearing component is **ours regardless**: the Phase-G0 exact
NS/polarization checker, applied to scan candidates. ML (Hodge-number regression, P5CY4ML-
style) may serve as (N)-tier pre-filtering to cut the candidate list — hits mean nothing
until the exact checker certifies them. CYTools is NOT part of this route (CY3-only, D0-G).

## 3. Corrected Step 2 — "exact geometric data package" (replaces the ML-metrics/volume plan)

If and only if a certified X₄ exists (either route), the follow-on deliverable is exact and
symbolic — no ML metrics, no numerical volumes presented as bounds:

- **(G2-a)** Intersection numbers, c₂·(divisors), h^{p,q}, and **χ(X₄)** — exact integers from
  the toric/algebraic data. Tier (E).
- **(G2-b)** **Tadpole posability certificate:** with B₃ exhibited and χ(X₄) computed, the
  D3-tadpole condition (χ/24 arithmetic) becomes *posable* — the precise unblocking the
  ledger names for WP S3-00b. Posing ≠ solving: moduli stabilization, W₀, and any m_φ remain
  Tier-C-blocked future work requiring their own T0 gates. This plan promises NO observable.
- **(G2-c)** Volume as an exact *polynomial in Kähler moduli* (from G2-a intersection
  numbers), explicitly NOT evaluated to a number — evaluation requires stabilization (F5b).
- **ML metrics (cymetric-class) are OUT of this plan.** They become relevant only if a
  metric-dependent coupling is someday needed, behind its own T0 gate, at (N) tier.

## 4. Stream 3 directions — unchanged, plus one future hook

- **Phase 2 (Stats Design) proceeds exactly as planned** on the anchored 56-cell grid
  (`27cff4a`). Nothing in WP S2-G feeds the sweep. The firewall stands: geometry never
  constrains the empirical grid.
- **Overlay hook (deferred, trivial):** at comparison time — after the PREDICTION v2 pin and
  the real-data run — any certified geometric statement from WP S2-G may be drawn as an
  overlay on the finished exclusion plot. Implementation: a plotting-layer addition only,
  scheduled with Phase 4/5 of WP-E6, never earlier.

## 5. Phases, gates, tiering, and agent assignments

| Phase | Content | Tier of work | Agents (when implemented) | Gate to proceed | Stop condition |
|---|---|---|---|---|---|
| **G0** | Compute + certify the fiber NS genus as Nikulin complement of certified T ≅ U⊕⟨14⟩; state the match criterion in NS terms; regression-test the checker (incl. s10 cross-family control → expected different genus) | Exact lattice arithmetic → (E) | Design + math statement: coordinator (Fable/Opus). Checker implementation: **Sonnet**. Regression/controls: **Haiku** | T0 signs the certified NS statement | NS genus lacks U summand → G1-c expectation dies → HALT, report |
| **G1** | Route A construction over the B₂ ladder: G1-a twist/CY condition, G1-b resolution analysis, G1-c elliptic structure | Delicate algebraic geometry: design **Opus/Fable**; symbolic verification scripts: **Sonnet**; controls/regressions: **Haiku** | Per-rung: exact certificates for a/b/c | T0 reviews the exhibited candidate | Three B₂ rungs obstructed with documented reasons → file structural-negative brief; T0 decides Route B |
| **G1′** | Route B (contingency): dataset provenance + license diligence (**Haiku**), NS-checker application at scale (**Sonnet**), optional (N)-tier ML pre-filter | Scan = (N) until certified | As listed | Same certificate standard as G1 | Dataset legally unusable or checker-negative across dataset → HALT |
| **G2** | Exact geometric data package + tadpole-posability certificate | Symbolic, (E) | **Sonnet** computation, **Haiku** controls, coordinator verification | T0 accepts; ONLY THEN may a separate WP S3-00b retry be proposed (unblock-tier-c sequence, its own gate) | — |

**Standing rules bound into every phase:** no commits by agents (coordinator reviews and
commits); every decision-changing result independently re-run by the coordinator before
acting (tonight's practice, now policy); web/budget caps per agent; `UNVERIFIED`/`BLOCKED`
are valid outcomes; all prose through epistemic-guardrails tiering; inbound suggestions enter
via the intake protocol (archive → audit → D0-style gate).

## 6. Cost honesty

G0 is cheap (days; one Sonnet + one Haiku agent + coordinator verification — same scale as
tonight's D0/Phase-1 passes, all on this VM). G1 is genuinely uncertain: the mathematics may
cooperate in weeks or obstruct immediately — which is why it is rung-laddered with stop
conditions rather than estimated with false precision. Nothing here needs HPC, MPI, or any
resource this VM lacks. Route B's scan cost is bounded by dataset size and is contingent
anyway. **No spend is authorized by this document** — T0 opens G0 explicitly or this remains
a filed proposal.

## 7. What this plan explicitly does NOT do

- Does not run anything tonight (proposal only, per instruction)
- Does not produce, estimate, or gesture at m_φ, α_D, Λ_D, W₀, or a stabilized 𝒱 (F5b)
- Does not touch Stream 3's grid, pipeline, PREDICTION.md, or data/ (firewall + pin protocol)
- Does not adopt CYTools, cymetric, or cyjax (D0-G: wrong dimension / out of scope), and
  touches P5CY4ML's dataset only under Route B after license diligence
- Does not reopen E-007/E-008/E-009 — no Kodaira readings anywhere in this plan

## 8. Decision requested from T0 (tomorrow)

**Open Phase G0: yes/no.** G0 is the cheap, load-bearing first step — it certifies the NS
match criterion every route needs, and its own stop condition can kill the plan for days'
cost before any construction work begins. Recommendation: open G0; defer the G1 decision
until the G0 certificate is on the table.

*Countermand/decision log: (empty — awaiting T0)*
