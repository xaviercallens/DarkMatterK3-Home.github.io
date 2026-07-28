# T0 Decision Record: Stream 3 (WP-E6 Phase 2)
**Date:** 2026-07-28 | **Authority:** T0 (Xavier)

1. **Analysis Protocol Ratified:** The `ANALYSIS_PROTOCOL` draft for Phase 2 Stats Design is officially APPROVED and promoted to LIVE.
2. **Resolution on Open Item 1 (taueff bounds):** The (0.3, 1.8) bound is explicitly accepted as a *prior-box*, not a trained-support limit. Ensure downstream documentation explicitly states this to maintain epistemic honesty.
3. **Resolution on Open Item 2 (Timing Run):** Authorized. Run `desisim` mock generation at N=50 to benchmark wall-clock cost. If feasible, scale to the recommended N=200 for the full 16x16 Hartlap-corrected covariance matrix.
4. **Part C Execution (Masking):** Authorized. Fix Bug 2 (biased mean). Implement the mock-calibrated multiplicative window correction (Ravoux et al. 2023). Do not interpolate across gaps.
