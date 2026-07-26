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

## 🔶 WP-E5 (revised WP-E protocol, T0-directed) — BUILT, NOT AUDITED, NOT RUN

Agent-built files landed just before session close; **treat every printed conclusion in them
as absent until audited** (session precedent: three agent outputs contained real defects).

- [ ] **Audit** `pipeline/transverse.py`, `scripts/wpe_preflight_baseline.py`,
  `wpe_closure_tests.py`, `wpe_transverse_sweep.py` (11/11 transverse tests pass; safety
  checks done: no phase outputs written, SHA-gate present, deliverable path is the
  `_2D_` file, gates untouched). Audit = read the σ/Δσ computation and zone logic against
  the spec in the agent prompt; check for tautological passes per D-1.
- [ ] **Run Phase 0** (pre-flight, both Δz=0.01 and Δz=0.20) → persisted JSON is the artifact.
  Verdict gates everything downstream. NOTE: the 3D pre-flight already returned **NO-GO**
  (`data/derived/wp_e_preflight_mock_data_sigma_2026_07_26.json`); the 2D framing gets its
  own verdict and inherits nothing.
- [ ] **Run Phase 1** (closure + null, must be able to fail; exits nonzero on failure).
- [ ] **Run Phase 2/3 sweep** only if Phase 0 = GO; deliverable
  `docs/WP_E_EMPIRICAL_BOUNDS_2D_2026_07_26.md` (never overwrite the T0-signed 3D original).
- [ ] Brief Stream 2 with the Phase 0 verdict either way (a NO-GO is a deliverable — F5 path).

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
green (371 at close: 360 + 11 unaudited transverse).

<!-- Generated-by: Claude Fable 5 (Stream 3, session close 2026-07-26) | Verified-by: every
item traced to its committed artifact | Reviewed-by: pending T0 -->
