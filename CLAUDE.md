# CLAUDE.md — Stream 3: Experimentation

Empirical confrontation repo. Governing docs: `VISION.md` §3–§4, `EXECUTION_PLAN.md` §4,
pinned `PREDICTION.md`. Read the **prereg-pipeline** skill before touching data/, pipeline/,
or any comparison; **epistemic-guardrails** for all prose.

## Commands
- Fetch data: `python scripts/fetch_data.py` (only entry point for datasets; updates data/MANIFEST.md)
- Pipeline tests: `pytest pipeline/tests/` (closure + null tests; merge-blocking)
- Full reproduction: `make reproduce` (one command, clean checkout)
- Results tables: `python scripts/render_results.py`

## Non-negotiable rules
1. No real-data comparison code before `PREDICTION.md` carries `PINNED:` (gate G1). Synthetic-data infra only.
2. Pinned prediction and `data/raw/` are immutable (hook-enforced). Parameter changes → `TUNING_LOG.md` → label FIT.
3. Every comparison output labeled `TEST` or `FIT`, mechanically.
4. Public data products only; never phrase results as collaboration/submission/endorsement.
5. Falsification triggers (F3/F4) are mechanical; overriding one requires a written T0 ruling.
6. Interpretation prose in OBSERVATIONAL_REPORT.md is T0-only — draft tables + stub, then flag.

## 🛑 Epistemic boundaries — post-F5b/F6 ledger (added 2026-07-27)

This ledger supersedes any older number in briefs, reports, or certificates. When a document
in this repo contradicts it, the document carries (or needs) a dated correction note.

1. **Tier A (established):** `L₃ = Sym²(L₂)` is kernel-proven in Lean 4 (Stream 1) and may be
   stated as fact. The Sym² relation supplies no physical coupling by itself (VISION §1.3).
2. **Tier B (derived, not measured):** ρ = 19, T = 3 for the cooper_s7 family — derived
   (E-011, Zarhin 1983 Thm 1.6(a) route), independently verified by Stream 1. A derived prior
   is not a measurement: Gate E criterion 1 stays UNRESOLVED (T0 decision D1). The old
   ρ = 4, T = 18 and the "2× Type II" Kodaira labels are **RETRACTED (E-007)** — never use,
   cite, or "confirm" them.
3. **Kodaira readings are a category error for this family.** The finite singular loci are
   confirmed — cooper_s7: {−1, 1/27}; cooper_s10: {−1/4, 1/16} — but they are order-2
   elliptic points of the X₀(n)+ modular curve, not Kodaira degenerations (E-008/E-009;
   Dolgachev/Doran, fetched and read). Do NOT classify Kodaira fibres from L₂ or L₃
   exponents at any locus, under any normalization. The open geometric item is U1
   (is T ≅ U⊕⟨14⟩?): `docs/U1_ROUTE_DESIGN_2026_07_26.md` in the Stream 2 repo.
4. **Tier C (blocked physics):** WP S3-00b (F-theory flux/tadpole) is BLOCKED (F5b). Do not
   assume, generate, or backfill exact observables (m_φ, α_D, Λ_D) or coefficient values
   (a₁, a₂, a₃). The A.4 elimination relation is symbols-only (`scripts/verify_appendix_A4.py`
   must stay green). The tadpole condition is not posable until a threefold base B₃ is
   specified; until then no dark-energy / vacuum-energy claim (T0 decision D4, A-DE).
5. **Empirical pivot is T0-gated.** No pipeline may depend on a single predicted scalar mass —
   none exists under F5b. Parameter sweeps / exclusion-bound pipelines enter only via a
   pre-registered PREDICTION v2 amendment under the pin protocol (rule 1 above applies:
   synthetic-data infra only until pinned), and every output is labeled exclusion/FIT — never
   TEST — until pinned. The WP-E5 2D transverse route stays CLOSED by its data floors
   (~1.6 Mpc, ~10⁴ objects per slice); a sweep does not reopen it.
