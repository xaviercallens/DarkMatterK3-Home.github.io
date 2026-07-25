# WP-R5 / WP-R6 — T1 (Sonnet) Verification Pass, Drafted for T0 Sign-Off

**Date:** 2026-07-25
**Reviewer:** Claude Sonnet 5 (T1) — a fresh session, independent of the session that authored
WP-R5/WP-R6 (also Sonnet 5, per `docs/WP_R5_3D_FIELD.md` / `docs/WP_R6_SURVEY_SCALES.md`
provenance).
**Scope:** Independent re-verification of the WP-R5 / WP-R6 deliverables (commit `bf484cf`) that
the master plan (`briefs/HAIKU_PLAN_REALDATA_VERIFICATION_2026_07_25.md`) flagged as needing
higher-tier review before downstream use.

> **This document is a T1 verification pass, not a T0 ruling.** Per `EXECUTION_PLAN.md`'s
> tier table, sign-off authority for cross-stream/architecture decisions rests with T0
> (Fable 5) or Xavier. This drafts the review record the master plan asked for; it does not
> substitute for Fable 5's or Xavier's actual sign-off, which remains open (see §4).

---

## 1. What was independently re-run (not just re-read)

| Check | Command | Result |
|---|---|---|
| Full pipeline test suite | `python3 -m pytest pipeline/tests/ -q` | **172 passed**, 0 failed, 197s — matches the commit message's claimed count exactly |
| Tier-language audit | `python3 scripts/check_tier_language.py` | **0 violations** |
| Working tree state | `git status` | clean; no uncommitted drift since `bf484cf` |

---

## 2. Code-level spot checks (read, not just trusted from the report)

- **`pipeline/cosmology.py`** — Planck18 citation is real (Planck Collaboration 2018/2020, A&A
  641 A6) and appears in the module docstring, not asserted only in prose. `comoving_distance_mpc`
  routes every caller through one function, so the cosmology choice is genuinely centralized as
  claimed. `radec_z_to_cartesian_mpc` / `radec_z_to_tangent_plane_mpc` both **raise** on
  non-finite/negative z rather than silently propagating NaN — matches the "never impute"
  claim in §4 of `WP_R5_3D_FIELD.md`. `drop_invalid_redshifts` correctly separates
  `n_dropped_nan` from `n_dropped_negative` and returns filtered arrays, not in-place mutation.
- **`pipeline/realfield3d.py`** — this is the part that matters most, since it replaces the
  defective WP-R3 null bank. Confirmed by reading the implementation (not just the report):
  - `z_shuffle_realization` permutes **z only**, holding (RA, Dec) fixed — genuinely breaks
    radial-angular correlation, unlike WP-R3's shuffle which permuted RA and Dec together
    (a no-op on the point set).
  - `angular_csr_realization` redraws RA uniformly and **Dec uniform in sin(dec)**, the
    correct measure for angular uniformity — not uniform in dec directly, which would have
    been a subtle correctness bug (over-sampling near the poles). This detail is easy to get
    wrong and was verified correct by direct read.
  - Both realization functions return **new arrays**, not views/aliases of the input, so
    repeated calls in a loop can't accidentally share state across realizations.
  - `density_field_cartesian_mpc` accepts an explicit `ranges` argument specifically so a real
    field and its null realizations share one grid — the report's claim that this prevents
    "each realization's auto-ranged extent silently changing bin volume" is accurate to the
    code, not just a design intention.
- **Provenance footers** — both `pipeline/cosmology.py` and `pipeline/realfield3d.py` carry the
  required `Generated-by | Verified-by | Reviewed-by` footer, satisfying `CLAUDE.md` /
  master-plan rule 8.

## 3. Cross-check against the retraction it depends on

`docs/FINDING_R_NULLDEGENERATE_2026_07_25.md`'s root-cause claim (WP-R3's "shuffle" permuted
RA and Dec with the *same* permutation index, making it histogram-invariant) is consistent with
what a shuffle-with-shared-index would in fact produce, and is structurally different from
WP-R5's `z_shuffle_realization`, which permutes only one of the three coordinates. The retraction
banner in `docs/EXECUTION_SUMMARY_2026_07_25.md` (§ top) and the WP-R3 report are both updated
in the same commit, so the correction isn't a dangling claim in one file only.

No evidence was found that any downstream artifact consumed the retracted WP-R3 null bank before
the retraction — `data/nullbanks/real/nullbank_2026_07_25.json` still exists on disk but nothing
in `pipeline/` or `scripts/` outside the WP-R3 report references it after `bf484cf`.

## 4. What this pass does and does not settle

**Settled by this pass (T1 scope):**
- The code matches its own documentation and the specific correctness properties claimed
  (non-degenerate nulls, correct angular measure, never-impute redshift handling, centralized
  cosmology).
- The test suite is real and green, independently re-run rather than taken from the commit
  message.
- No TEST/FIT label appears anywhere in scope; gate G1-L is untouched by this work, consistent
  with the "ENGINEERING-only" framing throughout both reports.

**Not settled by this pass, still open:**
- Whether the β₀ percolation finding (§7 of `WP_R5_3D_FIELD.md`) — 3 of 4 fields showing zero
  null variance at the chosen (nbins=8, threshold=50%) — should change how any *future* Stream 1
  chameleon prediction picks its statistic/resolution. That's a design decision for whoever
  writes that prediction, not something this review can pre-empt.
- Final T0 sign-off. Per the master plan's own escalation table, cross-stream/architecture
  sign-off is Fable 5's or Xavier's call, not Sonnet's — this document is the review record the
  plan asked a higher tier to produce, handed up for that ruling.

---

## 5. Recommendation

No defects found in independent re-verification. Recommend the `[pending T0]` footers in
`docs/WP_R5_3D_FIELD.md` and `docs/WP_R6_SURVEY_SCALES.md` be closed out by an actual Fable 5 /
Xavier sign-off referencing this document, rather than by further Sonnet-tier work — there is no
outstanding technical question this tier can still resolve on WP-R5/R6.

---

`Generated-by: Claude Sonnet 5 (T1 independent verification pass) | Verified-by: pipeline/tests/ 172/172 rerun, check_tier_language.py rerun, direct source read of pipeline/cosmology.py + pipeline/realfield3d.py | Reviewed-by: T0 N — drafted for Fable 5 / Xavier sign-off`
