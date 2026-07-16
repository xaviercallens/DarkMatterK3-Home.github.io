# Unified Vision: Dual-Scale Topological Universe Model

**Date**: 2026-07-16
**Status**: Program-level vision. Governs three parallel streams across three
repositories. Subordinate to the integrity practices P1–P4 and gates G1–G5
(`V5_SCIENTIFIC_REVIEW.md`, `LESSONS_LEARNED.md`) — no stream may make a
public claim that has not passed its gates.
**Companion plan**: `V5_RIGOROUS_THEORY_PLAN.md` (work packages; amended
2026-07-16 with the stream mapping and Track F).

---

## 1. The Dual Theory

The **Dual-Scale Topological Universe Model** unifies the project's two
theory layers into a single F-theory geometry:

> **F-theory compactification with a K3 × T² base and an elliptic fiber.**

- **Base (K3 × T²)** — the *dark-sector geometry*. Its complex-structure
  moduli are probed by order-3 Picard-Fuchs periods: the Cooper families
  **s₁₀ (OEIS A005260, λ = 16, PRIMARY)** and **s₇ (OEIS A183204, λ = 27,
  retired as primary — see `PIVOT_MEMO.md`; usable only via the certified
  `cooper_exact.py` kernel)**.
- **Fiber (elliptic curve)** — the *visible/coupling geometry*. The legacy
  **S₁₂/S₂₁** operators, which failed the GATE-C K3 integrality criterion,
  are reinterpreted here: they were never K3 periods — they are candidates
  for **order-2 Picard-Fuchs operators of the elliptic fiber**. The GATE-C
  "failure" becomes a classification datum, not a dead end.
- **Discriminant locus (7-branes)** — where the elliptic fiber degenerates
  over the base. Macroscopically this is hypothesized to appear as localized
  spikes in the Δ_obs asymmetry statistic.

"Dual-scale" means the same geometry is read at two scales: microscopic
(period integrals, mirror maps, brane loci — Streams 1–2) and macroscopic
(large-scale-structure statistics from SDSS/Euclid/PTA — Stream 3).

---

## 2. Three Parallel Streams

| # | Stream | Repository | Focus | Goal |
|---|--------|------------|-------|------|
| 1 | **Theory** | `SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal` | F-theory formalization in Lean 4 | Mathematically certify the Dual-Scale Model: formalize the K3 × T² base + elliptic fiber structure, the Picard-Fuchs order classification, and the perturbative bounds. |
| 2 | **K3 Selection** | `SocrateAI-Scientific-Agora-K3-DarkMatter` | AutoEvolve for K3 sequence selection | Classify candidate families by Picard-Fuchs order: test whether Cooper s₇/s₁₀ are genuine order-3 (K3) operators and S₁₂/S₂₁ genuine order-2 (elliptic) operators. |
| 3 | **Experimentation** | `DarkMatterK3-Home.github.io` | GPU-based distributed validation (SDSS, Euclid, PTA) | Empirically test the model: measure Δ_band with the certified kernels on provenance-gated real survey data; hunt discriminant-locus signatures. |

The streams run **in parallel** and are **mutually falsifying**:

- Stream 1 certifies what Stream 2 is allowed to call "a K3" (definitions and
  order-classification proofs, not numerics).
- Stream 2 selects which kernels Stream 3 is allowed to fit (only families
  that pass certified order/integrality classification enter the pipeline).
- Stream 3's measured Δ_band spectra feed back model-selection verdicts
  (ΔAIC vs sibling and matched controls) that can kill any specific family
  without killing the framework — and can kill the framework if *no* family
  beats the controls.

---

## 3. Key Hypotheses (pre-registered form)

Each hypothesis is stated with its test and its failure condition, per
practice P3 (pre-register before unblind).

### H-DT1 — Base identification (Order-3 ⇒ K3)
**Claim**: Cooper s₇ and s₁₀ satisfy **order-3 Picard-Fuchs ODEs** and are
therefore periods of genuine K3 surfaces, eligible as the F-theory base.
**Test** (Stream 2, WP-F1): derive the ODE order mechanically from the
certified recurrences (`cooper_exact.py`, `cooper_s10_kernel.py`); confirm
mirror-map integrality (WP-A2 criterion). Stream 1 formalizes the
order-classification statement in Lean 4.
**Fails if**: either operator is not order-3, or the mirror map is
non-integral — that family exits the base candidate list.

### H-DT2 — Fiber identification (Order-2 ⇒ elliptic curve)
**Claim**: the legacy S₁₂/S₂₁ operators satisfy **order-2 Picard-Fuchs
ODEs** and are periods of elliptic curves — the F-theory fiber, not the base.
This retro-explains S₁₂'s GATE-C K3-integrality failure.
**Test** (Stream 2): same mechanical order derivation applied to S₁₂/S₂₁;
elliptic (weight-2 modular) integrality check instead of K3 integrality.
**Fails if**: the operators are not order-2, or fail elliptic integrality —
then S₁₂/S₂₁ are generic ansätze with no geometric home, and any pipeline
result built on them stays legacy-only.

### H-DT3 — Discriminant locus (Δ_obs spikes ⇒ 7-brane intersections)
**Claim**: localized spikes in Δ_obs correspond to intersections of the
elliptic fibration's discriminant locus (7-branes) projected into the
macroscopic density field.
**Test** (Stream 3): only on provenance-gated real-survey sectors
(WP-C1 gate), with empirical-null significance (WP-C2) and kernel-specific
model selection (WP-B3).
**Caveat — provenance**: the historical exemplar **K3-DISC-0003** was
produced by the legacy Phase 4 max-asymmetry metric, which review finding F7
classifies as an uncalibrated internal metric, and it predates the WP-C1
provenance gate. It is a *motivating illustration only* and **must not** be
cited as evidence until the sector is re-measured under the gated pipeline
(WP-F4 in the plan).
**Fails if**: spike positions are not kernel-specific (controls correlate
equally), or do not exceed the empirical null after look-elsewhere
correction.

---

## 4. Cross-Stream Contracts

What flows between streams — and what is forbidden to flow:

1. **Stream 1 → 2**: formal definitions (what counts as order-3 / K3 /
   elliptic) and proved bounds. Lean artifacts are the arbiter in
   classification disputes.
2. **Stream 2 → 3**: the *kernel allowlist*. Stream 3 may only fit kernels
   that Stream 2 has classified and certified (currently: `cooper_s10_kernel.py`
   primary; `cooper_exact.py` s₇ as control/sibling; t₁₀₃ as backup;
   matched-log/matched-power as non-geometric controls).
3. **Stream 3 → 1&2**: measured Δ_band spectra, null banks, and ΔAIC
   rankings — *after* pre-registration (WP-C4), never before.
4. **Forbidden**: numeric constants crossing streams without provenance
   (P1); Stream 3 "discoveries" flowing anywhere without the
   `data_provenance == "real_survey"` gate (WP-C1); prose claims flowing to
   any public surface before gates G1–G5 pass.

---

## 5. Governing Practices (apply to all three streams)

- **P1** — no constant without provenance (derive, execute, or fetch — never
  transcribe).
- **P2** — tests are scientific, not smoke (exactness, null behavior,
  known-input recovery).
- **P3** — pre-register before unblind (`PREREGISTRATION.md`, WP-C4).
- **P4** — sibling families as control (s₇/s₁₀/t₁₀₃ mutual controls; now
  extended: the *elliptic* S₁₂/S₂₁ fiber kernels serve as cross-scale
  controls for the K3 base kernels, and vice versa).
- **Gates G1–G5** (`V5_SCIENTIFIC_REVIEW.md`, Part III) must all pass before
  outreach. A null result is a publishable outcome of this vision, not a
  failure of it.

---

## 6. Near-Term Stream Milestones

| Stream | Next milestone | Where |
|--------|----------------|-------|
| 1 Theory | Lean 4 proposal skeleton: PF-order classification statement + LVS perturbative bound (S ≤ 1.177 regime) | LeanProposal repo |
| 2 K3 Selection | WP-F1: mechanical PF-order derivation for s₇, s₁₀, S₁₂, S₂₁; AutoEvolve harness spec | this repo → K3-DarkMatter repo |
| 3 Experimentation | WP-B1 (chameleon z(ρ)) + WP-C2 (mock null bank) so gated real-data runs can resume; then H-DT3 spike census | this repo → github.io deployment |
