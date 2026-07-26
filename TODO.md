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

## 🔶 WP-E5 (revised WP-E protocol, T0-directed) — AUDITED; Phase 0 RUN → NO-GO; sweep QUARANTINED

- [x] **Audit** — done, `docs/WP_E5_AUDIT_2026_07_26.md`. 9 findings. `topology2d.py` and
  `wpe_preflight_baseline.py` PASS; `wpe_transverse_sweep.py` is **BLOCKED**.
- [x] **Run Phase 0** (both Δz=0.01 and Δz=0.20) → **NO-GO at both**.
  `docs/WP_E5_PHASE0_PREFLIGHT_2026_07_26.md`, artifact
  `data/derived/wp_e5_preflight_2026_07_26.json`. The 2D framing failed independently of the
  3D one; β₁ spans {0,1,2} against a null that is ~always 0.
- [x] **Sweep quarantined** — `scripts/wpe_transverse_sweep.py::main` now raises. It never
  ran (calls `density_shuffle_realization(field, rng=…)`; signature is `(field, seed)`), and
  repairing only that would emit a `ZONE_1_BOUNDING_BOX` map for an **undeformed** field
  (r_s never reaches the deformation; σ=+3.00 at amplitude 0, unsubtracted). 4th occurrence
  of the tautological-pass class.
- [x] **A-8 fixed** — `resolvable_2d` failed *open* on a degenerate field (zero extent →
  inf voxels → `RESOLVABLE`). Now fails closed; 2 regression tests (13/13 transverse).
- [ ] **Phase 2/3 rewrite** — only if T0 wants it. Requirements in audit §3: derive
  `R_voxels` from `r_s`, subtract the α=0 baseline per E2.11, measure extent via
  `transverse_extent_mpc()`, label `SYNTHETIC`, merge-blocking negative control asserting
  Δσ=0 at α=0, and raise mock occupancy (A-7). **Phase 0 is NO-GO, so this is not on the
  critical path.**
- [ ] **Phase 1** (closure + null) — not run; unblocked but moot while Phase 0 is NO-GO.
- [x] **Brief Stream 2** — Phase 0 NO-GO is in the correction brief and the Phase 0 doc.

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
green: **373 = 327 `pipeline/tests/` + 46 `checkers/tests/`** (371 at previous close + 2 new
A-8 regression tests). Verified at 2026-07-26 close. Note: a repo-wide `pytest` also collects
the `EuclidClusterViz/` app layer, which has 14 pre-existing collection errors unrelated to
the scientific pipeline — run the two directories above, not the repo root.

<!-- Generated-by: Claude Fable 5 (Stream 3, session close 2026-07-26) | Verified-by: every
item traced to its committed artifact | Reviewed-by: pending T0 -->
