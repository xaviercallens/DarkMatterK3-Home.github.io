# TUNING_LOG.md — Record of Post-Pin Parameter and Assumption Changes

**Status:** Initialized (Phase 0, WP P0-D). Empty — no tuning events recorded yet.

## Purpose

Per `VISION.md` §5 and the `prereg-pipeline` skill: once `PREDICTION.md` carries a
`PINNED:` header (GATE G1 / M1), any change to a model parameter, an assumption's
statement, or an assumption-ID tag list attached to a prediction or Free-Parameter
Ledger row is a **tuning event**. It is logged here, and every comparison that used
the old value is demoted (mechanically, forever) from `TEST` to `FIT`.

This file has no privileged authors — anyone (any tier) who makes a post-pin change
appends an entry in the same commit as the change. A commit that touches a pinned
assumption tag without a matching entry here is an integrity incident (`VISION.md` F6
spirit), not a stylistic omission.

## Entry format

Append one row per tuning event, oldest first. Never edit or delete a past row —
corrections are new rows referencing the one being corrected.

| Date | Commit | Quantity | Old assumption/value | New assumption/value | Justification |
|---|---|---|---|---|---|
| 2026-07-17 | c62f1ef | C_0 (lensing amplitude) | None | 1.010000e+00 | Stream 3 Initial Anchor Fit |
| 2026-07-17 | (this commit — see `git blame` for the hash) | C_0 (lensing amplitude) | 1.010000e+00 (row above) | **VOID — see `CORRECTION_NETRUNNER_FABRICATION.md`** | The row above logs a fit against a synthetic mock density grid (`v6_continuous_netrunner.py`), not real data, while `PREDICTION.md` was and remains unpinned — there was no valid baseline to tune away from. It is kept per this file's own "never edit or delete a past row" rule; this row is the correction, not a deletion. |

- **Date** — ISO 8601, date of the commit.
- **Commit** — short SHA of the commit making the change (self-referential: the commit
  that adds this row also makes the change).
- **Quantity** — the `PREDICTION.md` prediction or Free-Parameter Ledger row name
  (e.g. `m_φ`, `P1 (PTA)`, or an assumption ID `A-SEQ` if the assumption's statement
  itself changed, not just a downstream use of it).
- **Old / New assumption or value** — exact prior and new text/number. Copy, don't
  paraphrase.
- **Justification** — why the change was needed. "It's obviously reasonable" is not
  a justification (`prereg-pipeline` skill).

## Enforcement

`scripts/check_tuning_log.py` runs in CI (`.github/workflows/epistemic-guardrails.yml`)
on every push: for each commit that edits `PREDICTION.md` *after* that file carries a
`PINNED:` header, the same commit must also edit `TUNING_LOG.md`. Pre-pin edits to the
draft are exempt (no tuning event possible before a value is frozen). Run locally:

```
python3 scripts/check_tuning_log.py
```

## Related Documents

- **VISION.md** §5 — tuning-event definition and TEST/FIT demotion rule.
- **PREDICTION.md** — the pinned document this log tracks changes against.
- **prereg-pipeline** skill (`.claude/skills/prereg-pipeline/SKILL.md`) — the workflow
  discipline this file enforces.

---

`Generated-by: Claude Sonnet 5 (T1) | Verified-by: scripts/check_tuning_log.py (selftest + CI) | Reviewed-by: T0 N`

## ⚠️ VOID entries below (2026-07-17) — see `CORRECTION_NETRUNNER_FABRICATION.md`

The seven raw lines below were appended directly by an unguarded process
(`v5_continuous_netrunner.py` / `v6_continuous_netrunner.py`), not through
`scripts/check_tuning_log.py`, and are not in this file's own table format.
Every one of them logs a re-fit of C0 against a **synthetic mock density grid**
labeled as real data, while `PREDICTION.md` had (and has) no `PINNED:` header —
there was no valid pin for any of these to tune away from, so none of them is a
real tuning event. Kept in place, unedited, as the historical record of the
incident; treat every value below as void, not as a candidate for C0.

```
[c62f1ef084266191ba1afec95b17f3fa5492452f] FIT: Anchored C0 = 1.0100e+00 over median mass 1.0e+11 M_sun
[0a9866c586cfd1c85f2a9c72309d07fcf39831a2] FIT: Anchored C0 = 2.2616e-02 over median mass 1.0e+11 M_sun
[0a9866c586cfd1c85f2a9c72309d07fcf39831a2] FIT: Anchored C0 = 2.2549e-02 over median mass 1.0e+11 M_sun
[0a9866c586cfd1c85f2a9c72309d07fcf39831a2] FIT: Anchored C0 = 5.6956e-04 over median mass 1.0e+11 M_sun
[d3a147d9e75accc29b3a0b2f95496324ec549a67] FIT: Anchored C0 = 4.7033e-04 over median mass 1.0e+11 M_sun
[d3a147d9e75accc29b3a0b2f95496324ec549a67] FIT: Anchored C0 = 3.3035e-04 over median mass 1.0e+11 M_sun
[d3a147d9e75accc29b3a0b2f95496324ec549a67] FIT: Anchored C0 = 1.6125e-03 over median mass 1.0e+11 M_sun
```
