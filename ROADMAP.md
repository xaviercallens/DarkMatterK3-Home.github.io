# Stream 3 — Roadmap (as of session close, 2026-07-26)

> Previous content described the "NEON K3" browser-app architecture; preserved in git
> history (`git log -- ROADMAP.md`). This file now tracks the scientific program's road:
> where the empirical effort stands, what each next phase is conditioned on, and the
> pre-committed off-ramps. Governing docs: `VISION.md`, `EXECUTION_PLAN.md`,
> `NO_PREDICTION_BRANCH.md`, `briefs/CROSS_STREAM_CONSOLIDATED_2026_07_26.md`.

## Where the program actually is

```
[A-DD] empirical branch ──────────────── TERMINATED (Off-Ramp 3, 2026-07-25)
   └─ residue: F-LAB trigger only (ISL |α|=1 below 38.6 μm)
D-3 / Gate E path ─────────────────────── DEAD (T0 ruling 2026-07-26); runner de-fabricated, gated
WP-E phenomenological bounding box ────── REDIRECTED: 3D framing closed by measurement
   ├─ 3D verdict: deformations sub-voxel at nbins=8 (6.04×6.55×1023.6 Mpc voxels);
   │   WP-E's published window NOT ESTABLISHED; 6.33σ did not reproduce (2.48)
   └─ 2D transverse reframing (WP-E5) ── BUILT, unaudited, phases not run  ← YOU ARE HERE
Stream 2 Phase M (M1 mechanism memo) ──── theirs; bounded by directives E2.1–E2.17
Stream 1 (Lean) ───────────────────────── PARKED CLEAN by T0; D1.1 orphaned (needs owner)
```

## Phase map (each gate is mechanical, not judgment)

| Phase | What | Gate to proceed | Honest-negative exit |
|---|---|---|---|
| **Now → next session** | Audit WP-E5 scripts; run Phase 0 (2D pre-flight, Δz∈{0.01, 0.20}) | Scripts pass D-1 audit (no test that cannot fail) | Audit finds fabrication-class defect → fix or rebuild; record it |
| **Phase 0** | σ_mock–data(0) per slice/threshold on β₁(2D) | **GO iff** all \|σ\| ≤ 5 and not all-degenerate | NO-GO → file F5 honest negative; 2D framing joins 3D as closed; brief Stream 2 |
| **Phase 1** | S3-02 closure (inject → must recover >5σ) + null (FPR within binomial bound) | Both pass **and** the amplitude-0 negative control does NOT trigger | Closure misses → pipeline defect, stop |
| **Phase 2/3** | Resolvability-gated (r_s, α) sweep; Δσ zones | Phase 0 GO recorded in persisted JSON | Whole grid Zone-0 → untestable-by-construction is the finding |
| **Handoff** | `docs/WP_E_EMPIRICAL_BOUNDS_2D_2026_07_26.md` → Stream 2 M1 targets Zone 1 | T0 review | Zone 2 is `GENERIC_DEFORMATION_EXCLUDED` — never "vacuum falsified" |

## Conditioned futures (not scheduled — triggered)

- **Δσ formula revision** — if Deep Think sustains the moving-denominator objection, E2.11's
  prescription changes and any Δσ-based zone map is recomputed before use. E2.12
  (cosmic-variance ensemble null) issues only if Deep Think concurs.
- **PREDICTION.md annotation** — executes only on T0's pick of variant (a); otherwise the
  in-band line-151 retraction stands as the record.
- **Candidate ordering** — s7-vs-s10 T0 ruling propagates to `pipeline/siblings.py`,
  `K3_CRITERIA.md` scoring, and any WP-E5 candidate-specific run. Until then everything
  stays candidate-generic.
- **Gate 0 re-opening** — F-LAB only. `check_flab_trigger()` is advisory; a human reads
  the paper.
- **Real 3D data** — the program's largest gap (one spectroscopic field, n=50). If a
  genuine 3D volume ever lands in `data/MANIFEST.md`, the 3D branch of the revised
  protocol (Coma-style grid, r_s ≤ box scale) becomes live again.

## What is deliberately NOT on this roadmap

Re-running D-3 (dead, four blockers, T0-ruled) · any Mpc-scale chameleon mechanism
(~30 μm ceiling, two-model CLOSED-NEGATIVE) · t103 (vetoed by T0 2026-07-26 pending
certificates) · any `TEST`/`FIT` label while G1-L is closed · sweeps below the measured
resolvability floor (`assert_resolvable` is mandatory, E2.16).

<!-- Generated-by: Claude Fable 5 (Stream 3, session close 2026-07-26) | Verified-by: every
status traced to a committed artifact or ruling named inline | Reviewed-by: pending T0 -->
