# Stream 3 — TODO (session close 2026-07-26)

> Previous content of this file described the "NEON K3" browser-app layer; it is preserved
> in git history (`git log -- TODO.md`) and several of its checked items describe artifacts
> this repo's record has since retracted or never held (see `docs/WP_H_AUTO_RESEARCH_TRIAGE.md`).
> This file now tracks the **scientific program's** live task state. One item = one truth.

## ⛔ Blocked on T0 (Xavier) — nothing below moves without these

- [ ] **Ruling 1 variant pick** — annotate `PREDICTION.md` ρ=4/T=18 line via **(a)** annotate+re-hash
  (one recorded commit) or **(b)** leave body untouched (in-band retraction already exists at
  line 151). Default (b) until ruled. `docs/WP_E5_T0_RULING_IMPLEMENTATION_2026_07_26.md` §1.
- [ ] **s7 vs s10 primary-candidate ruling** — Stream 1's S1-10/11/12 makes s7 the anomaly and
  load-bearing; this repo's V5 record has s7 rejected / s10 primary. One line settles it;
  Stream 3 then updates `pipeline/siblings.py`. `briefs/STREAM3_TO_STREAM1_CORRECTIONS_2026_07_26.md` §4.
- [ ] **D1.1 owner** — `K3_CRITERIA.md` C2 `TBD-AT-FREEZE` (the sole blocker on any ρ/T/fibre
  certificate) is assigned to a parked stream. Needs a new owner or an explicit deferral.

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
- [ ] **Add CI that executes each `scripts/wpe_*.py` once** — two committed scripts had never
  been run and both died on the same `rng=`/`seed=` TypeError. Audit §6.
- [ ] A-9 (cosmetic: unused `z` param in `transverse_extent_mpc`, mock edge-clipping pile-up,
  redundant import) — open, low priority.

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

## 🔷 Awaiting external returns

- [ ] **Deep Think verdict** on the Δσ moving-denominator objection
  (`briefs/DEEPTHINK_REVIEW_REQUEST_BASELINE_2026_07_26.md` §4.1). E2.11's formula may change;
  WP-E3's 52 jitter-driven nonzero Δσ are a live instance. **E2.12 remains drafted-and-withheld**
  pending this.
- [ ] **Stream 2 register corrections + M1 memo** (must satisfy E2.1–E2.17; the resolvability
  guard `pipeline.resolvability.assert_resolvable` is mandatory pre-statistics per E2.16).
- [ ] **F-LAB monitoring** (the only path back to Gate 0): future public ISL data excluding
  |α|=1 below 38.6 μm → `pipeline.gate.check_flab_trigger()` → T0. Nothing else reopens it.

## ✅ Standing invariants (verify at every session start — `python3 -c` one-liner in the skill)

G1 pin `True` · G1-L `False` (closed) · Off-Ramp 3 terminus stands · no `TEST`/`FIT` labels ·
`docs/WP_E_EMPIRICAL_BOUNDS.md` (3D, T0-signed) immutable · tier-language clean · full suite
green: **385 = 339 `pipeline/tests/` + 46 `checkers/tests/`** (371 at previous close, +14 from
this session: resolvability fail-closed, amplitude-0 identity, fill-fraction thresholding,
per-axis σ, and the null-degeneracy guard). Verified at 2026-07-26 close. Note: a repo-wide `pytest` also collects
the `EuclidClusterViz/` app layer, which has 14 pre-existing collection errors unrelated to
the scientific pipeline — run the two directories above, not the repo root.

<!-- Generated-by: Claude Fable 5 (Stream 3, session close 2026-07-26) | Verified-by: every
item traced to its committed artifact | Reviewed-by: pending T0 -->
