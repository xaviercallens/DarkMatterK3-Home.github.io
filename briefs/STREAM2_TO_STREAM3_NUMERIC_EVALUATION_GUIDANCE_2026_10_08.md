# Stream 2 → Stream 3 — what Dark Home can and cannot evaluate numerically now (2026-10-08)

**From:** Stream 2, answering T0's question "could we run more numeric evaluation with Dark Home?" and passing on the result
of the K3 selection. **Short answer:** yes, in three bounded ways that need no new ruling, and one larger way that needs a
single T0 sentence. **Nothing in the K3 selection feeds an observable** (ledger item 4), so no number below is a prediction.

## 1. Result of the K3 selection, for your records

The AM-8 picks (s7: z = ∞, D = −3, T = A₂, lattice half Tier A from two independent kernel sources, unique on the curve;
s10: D = −4, T = ⟨2⟩⊕⟨2⟩) are now one cross-checked record, `SELECTED_K3_DOSSIER.json` (K3 `main` ≥ `f5a7280`, seven source
certificates must agree or the checker refuses). WP-TW2: the selected K3 has NS ≅ U ⊕ E8² ⊕ A₂, Mordell–Weil rank 0 (no
section), confirmed on the explicit model; the generic member needs a height-14 section with P̄·Ō = 5; the degree-7
endomorphism √−7 at z = 1/27 is exhibited exactly (now as a full map of curves). **Mirror refreshed on your side**
(17 files, manifest regenerated, `--check` green; Home PR below). Guardrails unchanged: lattice language only, no Kodaira
label, no observable, no ranking of the two families.

## 2. What you can run NOW, with no further ruling

1. **Standing invariants.** Verified today at Home `main`: `pytest pipeline/tests checkers/tests` → **604 passed, 0 failed**
   (10 min 47 s) with two modules excluded, because **`iminuit` is not installed on this machine**:
   `pipeline/tests/test_chi2_profile.py` and `pipeline/tests/test_sweep.py` cannot be collected here. That is an environment
   gap, not a regression; installing `iminuit` (into a venv, per your `requirements`) restores the full count, and the
   `chi2_profile`/`sweep` code paths are **unverified on this host until then**. Please record that in your TODO invariants.
2. **E1b — the calibration arm, second layer** (done today, `checkers/check_aubry_andre_localization_scaling.py`,
   certificate `E1b_aubry_andre_localization_scaling.json`, 8 tests): mean-IPR duality across the coupling range
   (worst gap 9.5e-13 on the non-degenerate cells; **26 of 36 cells are exactly degenerate at θ = 0 and excluded, counted,
   not averaged**); extended regime N·mean IPR_x constant to ≤ 1.06× for λ ≤ 1.5; localized regime (generic θ = 0.7)
   mean IPR_x constant in N for λ ≥ 2.5; crossing sign flips exactly at λ = 2J. **Two recorded revisions:** the first run's
   localized failures at θ = 0 were an eigenbasis artifact of exact n → −n degeneracy (diagnosed: 268 mirror pairs at
   λ = 3, N = 610); and λ = 2.1 (and 1.9) is *reported, not claimed* — still N-dependent at N ≤ 987 near the transition.
   The acceptance criteria were not retuned. This is a model check; it makes no K3 claim.
3. **Synthetic-only infrastructure** (closure/null tests, adequacy pre-flights, mock fields) — anything that never touches
   `data/raw/` and never emits a `TEST`/`FIT` label stays within your CLAUDE.md rule 1. New synthetic numerics are fine;
   they must ship negative controls and be mutation-checked as your WP-E6b audit did.

## 3. What needs one T0 sentence (and what does not change)

- **WP-E6 v2, Phase 0 only** (`briefs/WP_E6_V2_PROPOSAL_LYA_P1D_2026_07_27.md`): the literature re-survey of published
  mixed-fraction f_FDM bounds above 10⁻²¹ eV. It is a read-only survey (no data, no pipeline code, no labels) that your TODO
  already calls "open, cheap, worth doing either way" — but the proposal's own §8 reserves *all* execution for a separate T0
  sign-off, so **Stream 3 should not start it on Stream 2's say-so**. Suggested T0 text: *"Approved: WP-E6 v2 Phase 0 only
  (literature re-survey); Phases 1–4 remain gated on their predecessors' filed artifacts and on the pin."*
- **Unchanged and still closed:** E2 (HELD, no open noise dataset), E3/E4 (appendices until E2), WP-E5 2D route, any
  PREDICTION v2 pin, any comparison against real data before `PINNED:`, any sentence tying a lab result to the K3.

## 4. Direction

Prefer item 2.1 first (restore `iminuit`, re-verify the full count), then Phase 0 once T0 signs, then P1 modeling adequacy.
Do **not** try to make the K3 selection produce a mass, coupling, or exclusion — the ledger blocks it, and the selected K3
having no Mordell–Weil section is a statement about NS(X), not about physics.

*Generated-by: Claude (Sonnet 5.5), Stream 2 | Verified-by: the 604-test run, the E1b checker and its 8 tests, `refresh_stream2_mirror_manifest.py --check` | Reviewed-by: N*
