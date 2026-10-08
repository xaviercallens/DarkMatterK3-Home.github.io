# WP-E6 v2 — Phase 0 report (literature re-survey of mixed-fraction fuzzy-DM bounds), 2026-10-08

Authority: T0 D-g (`briefs/T0_DECISIONS_2026_10_08.md`) — Phase 0 only. Label: **literature-table arithmetic**. No data were compared, nothing is TEST or FIT,
no PREDICTION v2 amendment was pinned, `pipeline/` is untouched, no dataset or PDF was added to a data directory (the source PDFs were read from a scratch
directory and are hash-pinned in `scripts/wp_e6_v2_p0_digitize_figures.py`).

## Result

| Quantity | Value |
|---|---|
| Decisive cells under the pre-flight's optimistic proxy (13 masses × 20 fractions grid) | 258 |
| Decisive-and-open before Phase 0 (reproduced by the overlay, check against the stored artifact) | 221 |
| Decisive-and-open after Phase 0, text-grade rows only | 182 |
| Decisive-and-open after Phase 0, text plus figure-read rows | 152 |
| Same as the text-only count if Liu's weaker frequentist limits replace its Bayesian ones | 188 |

Numbers are read from `data/derived/wp_e6_v2_p0_resurvey_2026_10_08.json`; they are computed, not typed.

**Stop condition P0: does not fire.** Both counts are far above 10, and survivors reach down to f = 0.05 (f = 0.10 at the two highest masses) at every mass in the grid, not only at f ≥ 0.5.
**Secondary trigger (a published DESI DR1 P1D mixed-fraction analysis): NO.** The cosmological analysis of DESI DR1 P1D (arXiv:2601.21432, Sec. 7) says
constraining the nature of dark matter is beyond its scope; the measurement paper (arXiv:2505.07974) mentions dark matter only as a downstream use.

Where the grid stays open: above about 10^-20 eV the Lyα mixed-fraction data give no effective limit (Liu et al., stated in text), and between about
10^-21 and 10^-20 eV only the high-f cells are closed. At the lowest fractions (about 0.1) every mass in the grid still has surviving cells.

## What Phase 0 changed in the earlier picture

The repo's earlier table held exact-mass anchors only (Liu et al. at 10^-22 and 10^-21 eV). The re-survey adds Kobayashi et al. 2017 (text: more than 30% of
the dark matter in fuzzy form requires m ≳ 10^-21 eV, which closes 52 cells by itself) and the full contours of Kobayashi Fig. 1 and Liu Fig. 6 (figure grade,
shifted by the reading error toward closing fewer cells). The two Lyα contours differ from each other: Liu's is tighter below about 3×10^-22 eV and looser above
it (at 10^-21 eV the readings are about 0.35 and 0.63), which is one reason the figure-grade count is reported separately.

## What was searched, and what "no bound found" is worth

Searched (agents plus my own reads): Lyα forest, CMB and large-scale structure, dwarf-galaxy and star-cluster dynamics, lensing, reviews and compilations,
and the DESI DR1 P1D papers. My own audit reads, against the sources: Kobayashi 2017, Liu–Gong–Zhou 2026, Marsh & Niemeyer 2019 (figure only), and both DESI DR1
P1D papers. **Not audited by me:** the individual numbers reported by the four survey agents for CMB/LSS, dwarf galaxies and reviews. They are recorded in the
table as one `unverified` row and never applied. "No bound found" therefore means "not found by this survey", which is weaker than "no bound exists"; it
supports an upper bound on how open the grid is only in the direction that matters here: every unaudited item, if real, could only close more cells.

## What this does not decide

- It does not recommend or start Phase 1. Phases 1–4 stay gated on their predecessors' filed artifacts and on the pin, and on T0's answers to proposal
  §8(a) and Q1–Q5, which remain unanswered.
- Marsh & Niemeyer (Eridanus II) is recorded but not applied; resonance bands and a stated diffusion-approximation caveat sit in the range of a few 10^-21 eV.
- "Decisive" is the pre-flight's optimistic proxy, not a forecast.

## Reproduce

```
python3 scripts/wp_e6_v2_p0_digitize_figures.py <dir with kobayashi.pdf liu.pdf marsh.pdf> data/literature/fdm_figure_readings_2026_10_08.json
python3 scripts/wp_e6_v2_p0_overlay.py --emit
python3 -m pytest checkers/tests/test_wp_e6_v2_p0_overlay.py checkers/tests/test_wp_e6_v2_p0_digitize.py
```

*Prepared by Claude (Sonnet 5.5), Stream 3 support, 2026-10-08; Reviewed-by: N (T0 review pending; the sign-off covers the survey, not this report's wording).*
