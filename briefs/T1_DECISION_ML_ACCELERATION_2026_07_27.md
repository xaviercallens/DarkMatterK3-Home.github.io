# T1 Decision — ML / External-Repo Acceleration for Streams 2 & 3

**Date:** 2026-07-27, night
**Authority:** Xavier (T0), this session: "audit and make your own decisions" — standing
delegation for intake audits and the decisions they gate. Countermand open, as always.
**Trigger:** request to review "the proposal from Deep Think to leverage existing GitHub repos
and machine learning techniques to speed up Stream 2 and Stream 3." The attached document was
a verbatim re-paste of the already-audited-and-declined (m,f)-grid synthesis
(`~/literature_review/phase2_geometry/ANALYSIS_MF_GRID_AUDIT_2026_07_27.md`, re-receipt note
therein). **No new proposal content was received.** This memo therefore answers the framing
question on the merits, from verified project state only.

---

## Decision: NO new ML or external-repo adoption now. Two named reactivation gates.

## Stream 3 (empirical, live) — not compute-bound; the ML component already exists

The one ML technique this stream genuinely needs is **already integrated and verified**: the
Liu/Gong/Zhou two-stage neural-network P1D emulator (millisecond forward passes, iminuit- and
Cobaya-wrapped, cross-validated 2026-07-27). The full 56-cell grid evaluates in seconds.

What actually gates Phase 2 (Stats Design) is not speed but **decisions**: covariance strategy
(desisim mock ensembles — hundreds of mocks, comfortably within this VM's 8 cores), nuisance
treatment (profiling 4 IGM params via the working wrapper), and masking gap-handling (the
+7% naive-zero-fill artifact). Adding ML tooling to a non-bottleneck adds surface area for
error — in a program whose entire value is auditability — while speeding up nothing. Declined.

## Stream 2 (selection) — ML surrogates are epistemically inadmissible where they'd apply

Stream 2's outputs are **certificates from exact symbolic checkers** (rational arithmetic,
kernel proofs; house rule: numbers about candidates come ONLY from checkers). A neural
surrogate cannot emit a certificate — approximating an exact computation converts Tier A/B
artifacts into Tier-nothing guesses. This is not a performance question; ML is *categorically*
the wrong tool for the certificate pipeline, and the pipeline is not slow anyway (13-command
regression runs green in minutes; the candidate register holds four entries — nothing to
"search-accelerate"). Stream 2's real bottlenecks are T0 decisions (criteria freeze) and a
construction problem (exhibiting X₄/B₃), neither of which any repo or model speeds up. Declined.

## The two gates where this decision reopens

1. **Deferred emulator z-extension** (`FUTURE_PHASE_EMULATOR_EXTENSION_2026_07_27.md`): if T0
   funds the HPC phase, candidate tools — GAMER (already queued on that brief's checklist,
   wave-DM capable), transfer-learning on the existing NN, RunuX for the retraining layer —
   get a **D0-style verification gate** before adoption. Not before.
2. **Phase M / X₄-B₃ exhibition** (T0 D2′/M1′): if that hunt ever opens, a real
   ML-for-Calabi-Yau-geometry literature exists (metric/moduli learning on Kreuzer–Skarke-class
   data). Per the intake protocol, **no specific repos are named here** — naming-without-
   verifying is the precise failure mode tonight's three audits documented. If the gate opens,
   candidates get named and D0-vetted in the same motion.

## Standing rule (restating tonight's intake protocol as it applies to acceleration proposals)

Any future "leverage repo X / technique Y to speed up stream Z" proposal — from any source,
including Deep Think, including this coordinator — enters via: **archive → per-claim audit →
D0-style existence/fitness verification → tier-appropriate integration test → only then
adoption.** The manifesto→D0→Phase-1 arc earlier tonight is the template; it caught one
misdescribed dependency (bao_data), one purpose-mismatched repo (modelling_spectro_sys), and
one scope-limiting surprise (emulator z-domain) *before* they contaminated results. That is
the speed-up: verification is cheaper than retraction.

*Countermand log: (empty)*
