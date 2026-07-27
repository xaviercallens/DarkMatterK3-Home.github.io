# Stream 3 — TODO (last updated 2026-07-27, WP-E6b filing)

> Previous content of this file described the "NEON K3" browser-app layer; it is preserved
> in git history (`git log -- TODO.md`) and several of its checked items describe artifacts
> this repo's record has since retracted or never held (see `docs/WP_H_AUTO_RESEARCH_TRIAGE.md`).
> This file now tracks the **scientific program's** live task state. One item = one truth.

## ✅ Formerly blocked on T0 — CLOSED 2026-07-26 under delegated authority

All six ruled in `docs/T0_DELEGATED_RULINGS_2026_07_26.md`. Countermand window open on all.

- [x] **DR-1 Ruling 1 → variant (b)**, body untouched. **A re-hash is declined on principle**
  even though authority was granted: a pin's value is that it cannot be edited by whoever
  currently holds authority, so a grant of authority is exactly when not to exercise it.
  Variant (a) needs an explicit, personally-issued "re-hash authorized" from T0.
- [x] **DR-2 E2.2 stands** — chameleon adjudication not reopened; memo Step 2 must be rewritten.
  Reopening an adjudication needs new evidence, not a new deadline.
- [x] **DR-3 Roadmap Step 1 withdrawn** — the (r_s, α) bounding box is not producible.
- [x] **DR-4 s10 stays primary; s7 may supply no parameter** (P1). No position taken on Stream
  1's mathematics. Neither s7 nor s10 has a C3/C3b certificate — stated narrowly for that
  reason. Unblocking action sits with Stream 1: produce C1/C3/C3b for s7. No code change.
- [x] **DR-5 one ρ/T line** — ρ ≤ 19, T ≥ 3, Tier [B] pending Stienstra–Beukers 1985, no prior
  emitted, no code path consumes a numeric ρ or T. Whether S-B 1985 supports it still needs
  someone to read the paper; delegation cannot substitute for a citation.
- [x] **DR-6 D1.1 deferred**, no owner. Nothing live consumes C2; assigning an owner inside a
  parked stream would read as progress that is not happening.

## 🔶 WP-E5 — COMPLETE. All three phases audited and run; every phase says the same thing.

**Net:** Phase 0 NO-GO on real data · Phase 1 closure FAIL (cannot recover its own injected
signal at real occupancy) · Phase 2/3 quantifies why — detection needs ~5000 objects/slice
and r_s ≥ 2 Mpc, against 188 available. No bounding box on any mechanism exists or can be
produced from this data.

- [x] **Audit** — done, `docs/WP_E5_AUDIT_2026_07_26.md`. 9 findings. `topology2d.py` and
  `wpe_preflight_baseline.py` PASS; `wpe_transverse_sweep.py` is **BLOCKED**.
- [x] **Run Phase 0** (both Δz=0.01 and Δz=0.20) → **NO-GO at both**.
  `docs/WP_E5_PHASE0_PREFLIGHT_2026_07_26.md`, artifact
  `data/derived/wp_e5_preflight_2026_07_26.json`. The 2D framing failed independently of the
  3D one; β₁ spans {0,1,2} against a null that is ~always 0.
- [x] **Sweep quarantined, then rewritten** — the original never ran (called
  `density_shuffle_realization(field, rng=…)`; signature is `(field, seed)`), and repairing
  only that would have emitted a `ZONE_1_BOUNDING_BOX` map for an **undeformed** field
  (r_s never reached the deformation; σ=+3.00 at amplitude 0, unsubtracted). 4th occurrence
  of the tautological-pass class. Rebuilt from scratch rather than patched — see below.
- [x] **A-8 fixed** — `resolvable_2d` failed *open* on a degenerate field (zero extent →
  inf voxels → `RESOLVABLE`). Now fails closed; 2 regression tests (13/13 transverse).
- [x] **Phase 1 run** — audited (3 more findings, audit §5) and executed: **FAIL, exit 1**,
  correctly. Closure fails (β₁ identical deformed vs undeformed at 200 objects — the pipeline
  cannot recover its own injected signal); null FPR fails on a 2-distinct-value null. B-2 was
  another cannot-fail test: it declared α=0.05 while cutting at 5σ (α≈5.7e-7), a bound 5
  orders of magnitude too loose. Artifact `data/derived/wp_e5_closure_2026_07_26.json`.
- [x] **Phase 2/3 rewritten and run** — `scripts/wpe_transverse_sweep.py` rebuilt against
  audit §3 (r_s→R_voxels live, Δσ baseline-subtracted per E2.11, provenanced extent,
  `SYNTHETIC`, resolvability before statistics, enforced α=0 control that exits nonzero).
  576 cells, deliverable `docs/WP_E_EMPIRICAL_BOUNDS_2D_2026_07_26.md`.
  **Result (after self-review revision): robust detection (5/5 realizations) needs n ≈ 10000
  objects/slice at r_s ≈ 6–8 Mpc; the real slice has 188 (~50× short) and sits in the
  degenerate-null regime where σ has no meaning. Nothing below the ~1.6 Mpc voxel is
  measurable at any occupancy.** The earlier "n ≈ 5000 / 32 detectable cells / detection at
  n=188" numbers are **retracted in-band** in §6 of that doc.
- [x] **`void_to_filament_deformation` α=0 identity fixed** — the negative control caught a
  real 2-ulp violation from the mass renormalization at n=5000 (β₁ unaffected, no result
  changed). Short-circuit + 2 regression tests.
- [x] **Brief Stream 2** — `briefs/STREAM3_TO_STREAM2_EXPERIMENTAL_FINDINGS_2026_07_26.md`.
  Two floors (~1.6 Mpc scale, ~10⁴ objects/slice), the four artifact mechanisms measured,
  two cheap artifact tests, and directives **E2.18–E2.23**. All three phases agree from
  three independent directions.
- [x] **Self-review of the rewrite** — found 4 more defects in Stream 3's *own* code:
  scalar σ made the warp anisotropic in Mpc; a single mock realization per cell (averaging
  over 5 cut detections 32→12); the percentile threshold filled 8.4%–48% so occupancy was
  confounded with mask geometry; and — the big one — thresholding deformed fields at the
  baseline's *value* made β₁ track mask SIZE via tie-breaking, producing a spurious +5.06σ at
  α=0.01. `matched_fill` mode removes it (every α=0.01 cell → +0.00).
- [x] **`null_degeneracy()` / `assert_null_usable()` added to `pipeline/resolvability.py`** —
  the statistical sibling of the resolvability guard: refuses a null with std < 1 count or
  < 3 distinct values. Removes 60 cells/mode and is the **mechanical** fix for the artifact
  class that has now appeared 5 times. 5 tests against the real artifact banks.
- [x] **Script smoke tests added** — `pipeline/tests/test_wpe_scripts_smoke.py` (9 tests).
  Calls each phase script's null-bank builder for real, which is precisely the check that was
  missing when two scripts shipped with `Verified-by:` footers while raising `TypeError`. The
  `rng=` lint uses the **AST**, not a substring match — the first version false-positived on
  the docstring explaining the fix. Negative control confirms it catches the real defect.
- [x] **A-9 closed** — `transverse_extent_mpc` no longer takes an unused `z` (signature changed,
  caller updated); `generate_mock_slice` **resamples** instead of clipping stray draws onto the
  box boundary, which was piling an artificial ridge along the frame of the null-baseline mocks;
  redundant import removed. Sweep re-run so the artifact matches the code — **both floors
  unchanged**, robust r_s band 6–8 → 4–8 Mpc (envelope §6.1).

## 🟥 Correction issued to T0 / Stream 2 (2026-07-26)

`briefs/STREAM3_CORRECTION_PROJECT_HEALTH_MEMO_2026_07_26.md` — the project-health memo's
Stream 3 section is wrong on all 8 operational claims (source vendored,
`briefs/SOURCE_project_health_memo_2026_07_26.md`, SHA256 `b8b546fc…`). Five open requests:

- [ ] **R-1** rule on E2.2 vs. the memo's Step 2 — the M2 mechanism routes through an
  Mpc-scale chameleon, which is adjudicated CLOSED-NEGATIVE and **Binding**. Highest cost.
- [ ] **R-2** withdraw or restate roadmap Step 1 — the (r_s, α) bounding box is not
  producible; Phase 0's NO-GO now confirms this on the 2D route too.
- [ ] **R-3** Ruling 1 variant pick (also governs the memo's "populate §6 + re-pin").
- [ ] **R-4** s7-vs-s10 — memo treats s7 as settled/load-bearing; repo has it rejected and
  uncertified for C3/C3b (no `C3_sym2_*_s7`, no `C3b_map_*_s7`).
- [ ] **R-5** confirm the single ρ/T status line: [B]-pending-S-B-1985, no prior emitted.

## 🔶 WP-E6 line — DES-Y6 negative FILED, statistic re-scoped, WP-E6b FILED (2026-07-27)

**Net:** the broadband-lensing route is closed by its own stop condition; the Lyman-α P1D
route is *not* closed, but its pre-flight is optimistic by a factor of 18.5–49.3 at the only
two points where an independent published answer exists. **WP-E6 v2 drafting is blocked on a
T0 decision** (below).

- [x] **WP-E6 (DES-Y6 broadband convergence) — HONEST NEGATIVE, filed.**
  `docs/WP_E6_SYNTHETIC_ADEQUACY_PREFLIGHT_2026_07_27.md`, artifact
  `data/derived/wp_e6_adequacy_preflight_2026_07_27.json`. **0 of 260 cells reach 2σ**;
  best σ ≈ 0.49, and ≈ 1.48 even at full sky. Filed per the proposal's own stop condition.
- [x] **T0 D-e** (`briefs/T0_DECISIONS_2026_07_27.md`, commit `c4171f0`) re-scoped the WP-E6
  statistic to DESI DR1 Lyman-α P1D, with WP-E6b required *before* any v2 drafting.
- [x] **Pure-FDM exclusion-direction bug found and fixed** — `pure_fdm_exclusion_status()`
  compared `m > threshold`; every cited bound is a **lower** limit on mass, so the excluded
  region is *below* the threshold. Both the function and its two (equally inverted) tests
  were wrong. Correction note appended in-band to the WP-E6 report; the §2 status column is
  superseded (under the corrected direction the whole 10⁻²²–10⁻¹⁹ eV grid is pure-FDM
  excluded at f=1). No effect on the DES-Y6 negative itself — σ reachability is independent
  of that label.
- [x] **WP-E6b (DESI DR1 Lyman-α P1D) — ADEQUACY PRE-FLIGHT FILED.**
  `docs/WP_E6B_LYA_ADEQUACY_PREFLIGHT_2026_07_27.md`, artifact
  `data/derived/wp_e6b_lya_adequacy_preflight_2026_07_27.json`, module
  `pipeline/wp_e6b_lya.py`, data `data/literature/desi_dr1_lya_p1d_2026_07_27.csv`
  (arXiv:2505.07974 via Zenodo DOI 10.5281/zenodo.16943723; SHA256 in `data/MANIFEST.md`).
  **221 of 260 cells reach σ_equiv ≥ 2 and are open under the published landscape** — the
  opposite outcome to WP-E6, hence a decision point rather than an automatic stop. **The
  number carries no sensitivity content:** at the two masses where Liu, Gong & Zhou 2026
  publish a mixed-fraction bound, the same proxy assigns σ_equiv ≈ 37 and ≈ 99 where they
  place their 95% limit — **18.5× and 49.3×** this pre-flight's own 2σ threshold. Computed
  in the artifact (`optimism_calibration_vs_published_anchors`), not asserted in prose.
- [x] **WP-E6b audit — two real defects in the interrupted work.** (1) The filed headline had
  **no checker**: `run_grid` was never invoked by any test. (2) One negative control **could
  not fail** — it computed `sum((zeros/σ)²)` inside the test itself, with no module code
  between the injected null and the asserted zero. That control was deleted; six end-to-end
  controls now drive `run_grid` (zero-suppression injection, errors inflated ×10⁶, errors
  shrunk ×10⁻⁶, scrambled error-to-bin correspondence, all-bins-invalid fail-closed, inert-cut
  guard) plus four filed-artifact tests. Each control was checked against a deliberate
  mutation of `run_grid` and fires. `pipeline/tests/test_wp_e6b_lya.py`: 34 tests.
- [x] **Validity cuts re-verified at source** — arXiv:2505.07974 **§4.1** (not §4.3 as
  previously recorded in `data/MANIFEST.md`); both arms of the cut are checked to actually
  remove bins (755 of 1020 survive).
- [x] **T0 D-f — WP-E6b decision ANSWERED: option (A) PROCEED.** Verbal ruling via the T1
  coordinator, 2026-07-27, recorded in `briefs/T0_DECISIONS_2026_07_27.md` **D-f**. Scope:
  **proposal DRAFTING only.** Deliverable filed:
  `briefs/WP_E6_V2_PROPOSAL_LYA_P1D_2026_07_27.md` — 5 gated phases (P0 literature re-survey
  → P1 modeling adequacy → P2 statistical design + calibrated sensitivity re-derivation → P3
  `PREDICTION` v2 pin → P4 pre-registered comparison), each with its own mechanical stop
  condition. **EXECUTION of every phase remains gated on a separate T0 sign-off of the
  proposal**, and Phases 3–4 additionally on the pin. Nothing was executed.
- [ ] **Open, cheap, and worth doing either way** (now formalized as the proposal's **Phase 0**,
  do-first, with stop condition P0): 207 of the 221 decisive cells are open only
  because `docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md` §4 lists no mixed-fraction bound at
  their masses. Whether that reflects the literature or only this repo's survey of it is
  unverified. A targeted check on published f_FDM constraints above 10⁻²¹ eV would move the
  openness overlay materially.

## 🔷 Awaiting external returns

- [ ] **Deep Think verdict** on the Δσ moving-denominator objection
  (`briefs/DEEPTHINK_REVIEW_REQUEST_BASELINE_2026_07_26.md` §4.1). E2.11's formula may change;
  WP-E3's 52 jitter-driven nonzero Δσ are a live instance. **E2.12 remains drafted-and-withheld**
  pending this.
- [ ] **Stream 2 register corrections + M1 memo** (must satisfy E2.1–E2.17; the resolvability
  guard `pipeline.resolvability.assert_resolvable` is mandatory pre-statistics per E2.16).
- [ ] **F-LAB monitoring** (the only path back to Gate 0): future public ISL data excluding
  |α|=1 below 38.6 μm → `pipeline.gate.check_flab_trigger()` → T0. Nothing else reopens it.
- [ ] **T0 (Xavier) — WP-E6 v2 decision, the live blocker on the WP-E6 line.**
  `docs/WP_E6B_LYA_ADEQUACY_PREFLIGHT_2026_07_27.md` §7 states the ask in two options:
  **(A) PROCEED** — authorize drafting a WP-E6 v2 proposal on the Lyman-α P1D statistic,
  scoped to that report's §5 list (hydro-simulation-calibrated or emulator-anchored modeling,
  IGM nuisance marginalization, full covariance, a real mixed-fraction transfer function) plus
  the `PREDICTION` v2 pre-registration text, with **no real-data comparison before the pin**;
  or **(B) STOP** — file WP-E6b as the terminal artifact of the WP-E6 line, on the ground that
  the 18.5×–49.3× overstatement means no headroom has been exhibited that survives realistic
  modeling. Neither option is exercised; WP-E6b stops at the filing. **No v2 drafting until
  this returns** (T0 D-e made the pre-flight a precondition).

## ✅ Standing invariants (verify at every session start — `python3 -c` one-liner in the skill)

G1 pin `True` · G1-L `False` (closed) · Off-Ramp 3 terminus stands · no `TEST`/`FIT` labels ·
`docs/WP_E_EMPIRICAL_BOUNDS.md` (3D, T0-signed) immutable · tier-language clean · full suite
green: **396 = 350 `pipeline/tests/` + 46 `checkers/tests/`** (371 at previous close, +14 from
this session: resolvability fail-closed, amplitude-0 identity, fill-fraction thresholding,
per-axis σ, the null-degeneracy guard, script smoke tests, and mock edge-resampling). Verified at 2026-07-26 close.
**Count moved 2026-07-27** to **473 = 427 `pipeline/tests/` + 46 `checkers/tests/`** (+77 from
WP-E6, WP-E7 and WP-E6b). **473/473 passing, verified at the 2026-07-27 WP-E6b filing**
(`python3 -m pytest pipeline/tests/ checkers/tests/ -q`, 244 s).
Note: a repo-wide `pytest` also collects
the `EuclidClusterViz/` app layer, which has 14 pre-existing collection errors unrelated to
the scientific pipeline — run the two directories above, not the repo root.

<!-- Generated-by: Claude Fable 5 (Stream 3, session close 2026-07-26); WP-E6 line section and
the WP-E6 v2 T0 ask added by Claude Opus 5 (Stream 3, WP-E6b, 2026-07-27) | Verified-by: every
item traced to its committed artifact | Reviewed-by: pending T0 -->
