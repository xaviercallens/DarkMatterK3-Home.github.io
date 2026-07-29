# T0 Pending Decisions — 2026-07-29 Evening Resume

**Status:** DECISION-REQUEST (no action taken on any item below without T0 sign-off)
**Scope:** everything left open after this session's resume-and-verify pass (session
disrupted, state reconstructed from git; see S3 `0db4db4`, S2 `f20ceda`). WP-TW0,
WP-TW1, WP-E6-PIN, WP-E6-P2A, WP-E6-P2C, and WP-P1 are all now landed on their
respective `main` branches — that work is **done** and not re-argued here except where
it produced an open question below.

Each item: the decision, the proposal, the rationale, and what happens on approval.

---

## D1. WP-E6-PIN's 3 real-data-contact gaps (blocks the pin, blocks WP-E6-SWEEP)

**Decision needed:** `briefs/PREDICTION_V2_AMENDMENT_DRAFT_2026_07_29.md` §8 flags three
unresolved items before any real-DESI-data comparison can be pinned: (1) how the real
DESI DR1 P1D CSV becomes the sweep's "observed" vector — no LIVE document says so;
`ANALYSIS_PROTOCOL`'s worked example uses a synthetic mock mean instead; (2) no k-bin
correspondence between the emulator's 16 native bins and the real CSV's own 85-bin
table; (3) whether the real comparison should use the synthetic `desisim`-mock covariance
or the real published DESI covariance.

**Proposal:** use the real DESI CSV as the observed vector (not the synthetic mean);
restrict the real-data comparison to whichever emulator bins fall inside both (a) this
pipeline's resolved range and (b) the real CSV's validity-cut range, rather than
inventing an interpolation scheme across the gap; use the **real published DESI
covariance** for the real-data result (the synthetic mock covariance is right for
engineering/validation, but a result labeled as touching real data should carry real
uncertainties, not synthetic ones).

**Rationale:** this keeps every number in the eventual exclusion/FIT result traceable to
an actual measurement rather than a hybrid of real central values and synthetic error
bars (which would be an unusual and hard-to-defend uncertainty budget). Restricting
rather than interpolating avoids manufacturing correlated structure across bins that
were never actually resolved by either grid (same logic already applied in P2A, D2
below). **This is the most consequential item in this brief — it is the actual
gate on whether WP-E6-SWEEP ever touches real data, and the proposal is a default to
edit, not a recommendation to accept verbatim.**

**On approval:** WP-E6-PIN's amendment gets revised to state this scheme explicitly and
becomes pin-eligible; a follow-up WP builds the actual k-bin restriction map and the
real covariance extraction before WP-E6-SWEEP runs.

---

## D2. WP-E6-P2A's K-bin range mismatch — adopt the 9-bin design

**Decision needed:** `briefs/WP_E6_P2A_COVARIANCE_RESULT_2026_07_29.md` found that only
9 of the emulator's 16 `K_BINS` fall inside this synthetic pipeline's resolved FFT range
(Nyquist k≈0.0516 s/km vs. `K_BINS` extending to ≈0.1995 s/km) — a property of the
pipeline's native pixel scale, not of `N` or seed choice. This blocks WP-E6-P2B's
originally-assumed 12-dof design.

**Proposal:** adopt the 9-bin sub-block as the working design going forward (not a
stopgap); document the resulting dof change in `ANALYSIS_PROTOCOL` rather than chasing a
finer-sampled camera output path for marginal gain.

**Rationale:** the 7 excluded bins sit beyond this simulated instrument's own resolvable
range — treating them as measurable would require a materially different (and more
expensive) mock-generation path with no guarantee the real DESI data resolves them
either. A documented 9-bin design is honest; a fabricated or interpolated 16-bin one
would not be. Ties directly into D1's "restrict rather than interpolate" proposal — one
consistent bin set should govern both the synthetic covariance and the real-data
comparison.

**On approval:** WP-E6-P2B builds its chi² design on the 9-bin covariance; downstream
docs stop citing "16-bin" as the working sweep dimensionality.

---

## D3. Correct `ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md` L290's masking-correction direction

**Decision needed:** L290 currently states "the ratio `p_masked / p_clean` **is** the
correction function." WP-E6-P2C (`briefs/WP_E6_P2C_MASKING_FIX_2026_07_29.md`)
implemented the opposite direction and verified it twice independently against the
actual Ravoux et al. 2023 paper (arXiv:2306.06311 eq. 22/23: A = P_unmasked/P_masked) —
once by the producing session, once by this session's coordinator pass, which fetched
and read the PDF directly (`pdftotext` on the fetched arXiv PDF; WebFetch on the
abstract-only URL returns metadata only, as both passes independently found). The
DRAFT document itself was never corrected.

**Proposal:** amend `ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md` L290 to state the
paper-verified direction (A = P_unmasked/P_masked, applied by multiplying the masked
power by A), citing eq. 22/23 directly.

**Rationale:** this is a documentation correction to match an independently
double-verified fact, not a new scientific claim — the code (`pipeline/compare_p1d.py`)
already implements and pins the correct direction with a dedicated regression test
(`test_calibrate_window_correction_recovers_known_bias`) that would fail if the direction
regressed. Leaving the DRAFT wrong risks a future reader or agent trusting the doc over
the code.

**On approval:** one-line correction to `ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md` L290 with
a dated correction note (matching this repo's convention elsewhere in the same document,
e.g. its own §3.2 verification-pending flag).

---

## D4. WP-TW0 confirms ℓ=2 — close ruling R5 (informational, no new action)

**Not really a decision — a closure.** T0 ruling R5 (2026-07-29, `S2 c4e6cd6`) set the
in-house ℓ computation as "THE gate task: ℓ=2 ⇒ Route A CLOSED program-wide, ℓ=1 ⇒
escalate discrepancy." WP-TW0 landed and was coordinator-verified this session (S2 main
`f20ceda`, `briefs/TW0_HODGE_DEGREE_RESULT_2026_07_29.md`): ℓ=2, independently
hand-re-derived from the L₂ Riemann scheme, confirming the value Deep Think supplied
externally. Route A was already closed by the same-day countermand ratifying ℓ=2 as
Tier B-external pending this non-blocking check — WP-TW0 is the check landing, not a new
gate. **Proposal: mark R5 CONFIRMED-CLOSED in the S2 decision log; no further action.**

---

## D5. WP-TW1 next step — authorize the M-polarization exhibition attempt?

**Decision needed:** WP-TW1 (S2 main `1e5164d`, coordinator-verified) found the
twisted-Weierstrass necessary-condition screen is a **mixed result**: P³ fails
(collision-forced), but disjoint-section bases (P¹×P², P¹-bundles over P² for n=0..18)
pass. The brief's own recommended next step: authorize (or not) the harder follow-on WP
attempting to actually exhibit the M-polarized f, g sections on the surviving
P¹-bundle-over-P² family — the part this WP explicitly did not attempt ("the honest hard
part").

**Proposal:** authorize it, scoped to the P¹-bundle-over-P² family with n≤18 (the exact
configuration WP-TW1 verified realizability for), as the next twisted-Weierstrass WP.

**Rationale:** twisted-Weierstrass is now the primary route (same-day countermand); the
necessary-condition screen passing on a specific, bounded family is the natural next
concrete step, and the family/bound are already pinned down rather than open-ended.

**On approval:** new WP filed against the P¹-bundle-over-P² (n≤18) family specifically,
not a re-scan of other bases.

---

Generated-by: coordinator resume session (2026-07-29 evening) | Reviewed-by: pending T0 (Xavier).
