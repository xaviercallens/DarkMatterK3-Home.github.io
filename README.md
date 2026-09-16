# Stream-4 AlphaEvolve convergence diagnostics (auto-snapshot branch)

**EXPLORATORY SANDBOX — Stream-4 material (CLAUDE.md ledger item 5, T0 ruling DL-3,
2026-07-31). Not citable as evidence in Streams 1–3 or any Tier A/B/C claim.**

This orphan branch holds snapshots of the harvest daemon's convergence figures for the
AlphaEvolve evolutionary run(s) synced from the GCS datalake. Per T0 ruling 2026-09-16
(`briefs/T0_RULINGS_2026_09_16.md` §A4 on `main`), these figures are no longer refreshed on
`main`.

- Figures are labeled **PHENOMENOLOGICAL CONVERGENCE (F5b) — evolutionary population, not a
  Bayesian posterior**. A small χ² loss here means the optimizer converged, nothing more.
- The checkpoint field `kodaira_fiber_type` is ignored (E-008/E-009 retraction).
- Writer: `scripts/datalake_harvest_daemon.py` on `main` commits here only when the
  harvested state (run, checkpoint count, generation, best candidate) changes — not on every
  30-minute heartbeat.
- The last `main` copy of these figures is commit `11b6477` (generation 300,
  run `20260729_074350`).

Generated-by: Claude (Opus 5) | Verified-by: n/a | Reviewed-by: T0 Y (branch confirmed 2026-09-16)
