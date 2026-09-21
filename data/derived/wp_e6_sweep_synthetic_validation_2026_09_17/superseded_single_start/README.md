# Superseded: single-start profiler runs (2026-09-17)

These sweeps used `Chi2Profiler.profile_likelihood()` with ONE Migrad start at the nuisance medians.
A multi-start check on 6 invalid-minimum cells of `S2_noisy_fdm_seed1` found χ²_min overestimated
by up to **0.9975** (CDM cells m = −22.9 / −22.5, f = 0), and by 0.095, 0.009, 0.0003, 0.0 elsewhere.
Against a 95 % Δχ² threshold of 5.99, that is enough to flip a cell's exclusion status. The driver now uses
a deterministic 9-start set (`pipeline/sweep.py` PROFILE_STARTS). Kept as evidence of the defect; not results.
Label: SYNTHETIC-VALIDATION (no real data).

## Correction note, 2026-09-21 — `summary.json` moved in here, where it belongs

`summary.json` was sitting at the top level of the parent directory, untracked, reading `pass: true`
— where any reader would take it as the verdict of the *current* run. It is not. It summarizes the
**single-start** sweeps in this folder, and that is mechanically provable rather than inferred: the
current `scripts/wp_e6_sweep_synthetic_validation_2026_09_17.py` writes an
`optimizer_max_residual_per_sweep` key, and that file has only `{label, checks, pass}` — it was
produced by a script version predating the multi-start fix. Its mtime (07:01) also matches this
folder's last single-start file exactly, ten hours before the one multi-start sweep that existed.

At the time of the move the parent directory held exactly one multi-start sweep — `S1_noiseless_fdm`
(9 starts, re-run 17:30) — and no others: the multi-start re-run had been started and not finished.
A `pass: true` summary of superseded runs, sitting beside one finished scenario out of eight, is the
shape of the WP-E3 defect this repo has already recorded once ("a printed summary has contradicted
persisted data"). Moved rather than deleted, so the evidence stays auditable.

`run_S1_multistart_partial.log` is the partial log from that interrupted multi-start attempt. It
records `all minima valid False` for the S1 sweep — a fact the superseded summary does not mention
at all, because it never saw that run.

Nothing in this folder is a result. Label: SYNTHETIC-VALIDATION (no real data).

