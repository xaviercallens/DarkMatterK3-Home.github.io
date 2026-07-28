# Deep Think (T0s) Alignment Brief — 2026-07-28

**To:** Deep Think, Scientific Companion (T0s) per `EXECUTION_PLAN.md` §1.1
**From:** T0 orchestrator session (Fable 5), on T0 (Xavier) instruction
**Purpose:** update since `DEEPTHINK_ALIGNMENT_BRIEF_2026_07_27_NIGHT.md`. One gate opened
(S2 G1), two T0 ratification rounds, one empirical mystery formally closed with verified
numbers, one paper's open questions all resolved. Canonical copy: Stream 3
(`SocrateAI-Scientific-Agora-Home`).
**Ground rule reminder (unchanged):** LLM output is never evidence. Everything below traces
to checkers, primary-source reads, re-run code, or recorded T0 decisions.

---

## 0. Headline for adversarial review

**The specific ask this time: an independent, cross-model re-derivation.** Per your role
definition (T0s: "independent re-derivation of any T0 result, two-model cross-check"), the
G0 NS-genus certificate (§1 below) has so far only been checked *within* the Claude family
(Sonnet derivation → coordinator/Fable reproduction + controls). It has never had a genuinely
independent model lineage touch it. It now gates a live, resourced execution phase (G1), which
raises the cost of a latent error. Two concrete requests:

1. **Re-derive G0 from scratch** (fresh session, do not read `checkers/check_NS_genus_G0.py`
   first): given K3 lattice Λ = U³⊕E8(-1)², and certified transcendental lattice
   T ≅ U⊕⟨14⟩ (rank 3, U1 result — see §1), compute NS = T^⊥ via Nikulin's theory of
   primitive embeddings into a unimodular lattice. Does your route reproduce
   NS ≅ U⊕E8(-1)⊕E8(-1)⊕⟨-14⟩ (rank 19, disc. group cyclic order 14, U-summand present)?
2. **Adversarial read of the G1-b resolution strategy** (§2 below) before the workshop commits
   T1 effort to it — the plan's own document calls G1-b "the most likely honest stop-point."
   Any pitfall you can name now is cheaper than one found after execution starts.

Also flagged, lower stakes: §3 (WP-E7 closure) and §4 (paper scope) are decisions, not
derivations — sanity-check only if something reads as wrong, not for re-derivation.

## 1. G0 → G1: what's now LIVE and what it rests on

**G0 result (promoted DRAFT→LIVE by T0 2026-07-28):** NS ≅ U⊕E8(-1)⊕E8(-1)⊕⟨-14⟩, rank 19,
computed as the Nikulin orthogonal complement of T inside Λ = U³⊕E8(-1)². Two independent
in-house derivation routes (constructive integral-embedding witness; genus-uniqueness
argument) agreed bit-for-bit on the literal Gram matrix. Coordinator independently re-ran the
checker and a 5-control negative-test suite (all PASS) before promotion. Rank 19 cross-checks
ρ=19 (E-011) via a route independent of Zarhin's direct computation.

**Caveats T0 was shown before ratifying, still standing:**
- **Weak discriminating power** — both cooper_s7 (d=14, the certified family) and cooper_s10
  (d=20, a sibling candidate) pass G0 with a U summand; the genus construction places a U in
  front for this NS shape essentially regardless of n. G0 rules out one failure mode; it is
  not strong evidence G1 succeeds.
- **Fiberwise, not relative** — G0 certifies the abstract generic fiber admits an elliptic
  fibration with section. G1-c needs the *relative* structure (monodromy-invariant isotropic
  NS class along the whole family) — not checked here.

**G1 gate opened 2026-07-28 (T0 ratification, `S2 256017d`):** authorized to proceed to
G1-a (CY/twist condition), G1-b (crepant resolution), G1-c (F-theory posability), pulling
back the certified K3 family over a B₂ ladder (P², P¹×P¹, Hirzebruch Fₙ), exact symbolic
computation only. Canonical plan: S2 `briefs/WP_S2G_X4_EXHIBITION_PLAN_2026_07_27.md`.

## 2. G1-b — the plan's own flagged main risk

Verbatim from the canonical plan: over φ⁻¹ of the family's singular loci ({−1, 1/27} —
fixed by the epistemic ledger as order-2 elliptic points of X₀(7)+, explicitly **not**
Kodaira degenerations, E-008/E-009 — and over the ∞-type boundary points) the pullback
degenerates, and crepant resolvability keeping c₁ = 0 must be established case-by-case.
"This is the plan's main mathematical risk and the most likely honest stop-point."

The plan's own model-routing table (§ "Delicate algebraic geometry: design Opus/Fable") puts
G1-b's design work above T1 (Sonnet) — it is exactly the class of problem your role exists
for. We are not asking you to solve it; we are asking whether the proposed case-by-case
resolvability approach (classify singularities per base, per boundary stratum, exact) has an
obvious structural trap — e.g. a base choice that makes crepant resolution provably impossible
for reasons not visible from the local analysis, or a cheaper global argument that would save
the ladder from being walked rung by rung.

## 3. WP-E7 eBOSS/LRGpCMASS — closed with verified numbers, not a decision needing review

Previously flagged as an open row-count "mismatch." Root cause found (a filename/comment bug
in `scripts/data_fetchers.py`, not a data problem) and the two catalogs are now both fetched
and integrity-checked against their correct published counts:
LRGpCMASS 255,741+121,717=377,458=published (MATCH); eBOSS-only 107,500+67,316=174,816
(MATCH). T0 selected LRGpCMASS as WP-E7's primary sample (SDSS's own documented
recommendation for z>0.6 clustering, matching WP-E7's stated purpose); eBOSS-only retained as
labeled secondary. No open question here — noted for completeness only.

## 4. Paper PLAN.md §5 — all five resolved by T0, Stream 1 (context only)

Scope Option A (unified paper, lattice sections conditional); venue *Experimental
Mathematics*; sole-author "Independent Researcher" with a mandated verbatim AI-acknowledgment
paragraph; ρ=19/T=3 stays a conditional Tier-B proposition (this is where §1's re-derivation
request matters most — if your G0 check disagrees, the proposition's hypotheses need
revisiting before submission); internal manuscript cited hash-pinned. S1 commit `e621f6a`.

## 5. What starts now (context, not a request)

Per T0's final authorization, a T1/T2 workshop is starting on the unblocked work: S2 G1-a
(T1), S3 desisim timing benchmark P2-t (T2), S3 WP-E7 occupancy ratification (T2/T1). G1-b
execution is deliberately **held for your §0.2 read** before T1 effort is committed to it —
everything else proceeds in parallel per `briefs/MULTI_AGENT_WORKFLOW_PLAN_2026_07_28.md`.

## 6. Sources

- `briefs/T0_DECISIONS_2026_07_28_STREAM2.md`, `T0_DECISIONS_2026_07_28_STREAM3.md`,
  `T0_DECISIONS_2026_07_28_PENDING_ITEMS.md` — this session's three T0 decision records.
- S2 `briefs/WP_S2G_X4_EXHIBITION_PLAN_2026_07_27.md`, `briefs/G0_NS_GENUS_RESULT_2026_07_28.md`,
  `data/certificates/G0_NS_genus_cooper_s7.json`, `checkers/check_NS_genus_G0.py`.
- `briefs/WP_E7_EBOSS_LRG_SAMPLE_IDENTITY_INVESTIGATION_2026_07_28.md`, `data/MANIFEST.md`.
- S1 `paper/PLAN.md` (post-ratification), commit `e621f6a`.

---
Generated-by: Fable 5 (T0 orchestrator session) | Verified-by: every number and commit hash
checked against its named source this session | Reviewed-by: T0 Y (relayed on Xavier's
instruction; content is the orchestrator's, framing decisions are Xavier's per §3/§4)
