# Superseded: single-start profiler runs (2026-09-17)

These sweeps used `Chi2Profiler.profile_likelihood()` with ONE Migrad start at the nuisance medians.
A multi-start check on 6 invalid-minimum cells of `S2_noisy_fdm_seed1` found χ²_min overestimated
by up to **0.9975** (CDM cells m = −22.9 / −22.5, f = 0), and by 0.095, 0.009, 0.0003, 0.0 elsewhere.
Against a 95 % Δχ² threshold of 5.99, that is enough to flip a cell's exclusion status. The driver now uses
a deterministic 9-start set (`pipeline/sweep.py` PROFILE_STARTS). Kept as evidence of the defect; not results.
Label: SYNTHETIC-VALIDATION (no real data).
