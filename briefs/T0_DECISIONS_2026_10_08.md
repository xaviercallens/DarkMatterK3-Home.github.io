# T0 decisions 2026-10-08 — Stream 3 (recorded by Stream 2 support session, relayed from T0's in-session instruction)

## D-g — WP-E6 v2: Phase 0 (literature re-survey) AUTHORIZED; nothing else

**T0, verbatim (2026-10-08, in session):** "I give you the sign-off and take decision on my behalf and continue"

**What was being answered.** The message immediately before it (Stream 2 → T0) offered exactly one Stream-3 sign-off, with this suggested
text: *"Approved: WP-E6 v2 Phase 0 only (literature re-survey); Phases 1–4 remain gated on their predecessors' filed artifacts and on the
pin."* (`briefs/STREAM2_TO_STREAM3_NUMERIC_EVALUATION_GUIDANCE_2026_10_08.md` §3). The sign-off is therefore read as approving that text
and nothing wider; the interpretation is recorded here so it can be corrected by one T0 sentence.

**Authorized:** Phase 0 of `briefs/WP_E6_V2_PROPOSAL_LYA_P1D_2026_07_27.md` §4 — the targeted literature re-survey of published
mixed-fraction (f_FDM < 1) constraints above 10⁻²¹ eV, the dated addendum to `docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md` §4, the revised
openness overlay and recomputed decisive-and-open cell count, and the explicit statement of what was searched. Phase 0's own stop
condition P0 and secondary trigger apply mechanically (fewer than 10 decisive-and-open cells, or survivors only at f ≥ 0.5, or a published
DESI DR1 P1D mixed-fraction analysis already exists → file the re-survey as the terminal artifact and STOP).

**NOT authorized (unchanged):** Phases 1–4; any `PREDICTION` v2 pin (T0's alone); any real-data comparison; any `TEST`/`FIT` label; the
proposal's §8(a) scope approval and §8(b) questions Q1–Q5 remain **unanswered**; E2 stays HELD; E3/E4 stay appendices.

**Conduct note.** Phase 0 as written says "no downloads, no code": the survey reads papers (no datasets are fetched, and no PDFs are added
to this repository's data directories); the recomputed overlay is produced by a small separate literature-table script that reads the
existing pre-flight artifact and a new bounds table, leaving `pipeline/` untouched.

*Recorded by Claude (Sonnet 5.5), Stream 2 support, on T0's instruction; Reviewed-by: T0 (the instruction above).*
