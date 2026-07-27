# T0 Decision Record — 2026-07-27 (Stream 3 empirical program)

**Authority:** Xavier Callens (T0), in-session 2026-07-27, responding to the decision list
in `briefs/WP_E6_DATA_LANDSCAPE_2026_07_27.md` §4. Recorded by the coordinator session
(T1). Scope: exactly the three decisions D-a/D-b/D-c; nothing broader is inferred.

## D-a — Data acquisition & resolvability pre-flight: APPROVED

T0 approves DESI data acquisition, "and leverage additionally of Euclid and SDSS and
others that could provide experimental insights." Execution scope (T1 reading, per the
landscape brief): DESI DR1 as primary target, SDSS/eBOSS DR16 LSS as secondary, Euclid Q1
as a watch/exploratory item (63.1 deg² only), others as the survey identifies them.
Discipline unchanged: all fetches through `scripts/fetch_data.py` with MANIFEST hashes;
`data/raw/` immutable; the resolvability pre-flight (WP-E7) is geometry arithmetic and
precedes any comparison design.

## D-b — WP-E6 framing: DELEGATED to T1; ruling = MIXED-FRACTION

T0 delegated the framing choice in-session ("take decision on my behalf which seems the
more logical"). **T1 ruling: the mixed-fraction framing (f_FDM < 1).** Rationale, recorded
for review: it is the only framing that targets parameter space published bounds leave
genuinely open (f < 0.65 at 10⁻²¹ eV; effectively unconstrained at higher masses,
arXiv:2606.06969); a pure-FDM sweep would re-derive known exclusions, and a
robustness-only program produces no new constraint. Reproduction/robustness runs are
retained as a validation tier inside WP-E6, not as its headline. Outputs remain labeled
exclusion/FIT until a PREDICTION v2 amendment is pinned; this ruling does not itself
amend any pinned document. T0 may overrule at v2-pin time; the delegation and this ruling
are both recorded per the project's authorization discipline.

## D-c — Lensing product: DES Y6

DES Y6 Metadetection is the primary weak-lensing product for WP-E6 (151,922,791
galaxies, 4,422 deg², n_eff = 8.22 arcmin⁻², arXiv:2501.05665), subject to the
outstanding file-availability check; KiDS-Legacy is the fallback if Y6 shear files are
not yet posted.

## Also directed by T0 (same exchange, operational)

Model-tier economy for delegated agents: mechanical/well-specified work runs on smaller
tiers (Haiku/Sonnet), delicate derivations and gate decisions on larger tiers
(Opus/Fable). Coordination remains in the single T1 session.

---
Generated-by: Fable 5 (T1 coordinator) | Verified-by: n/a (decision record) |
Reviewed-by: Xavier (T0) — records his own in-session decisions; D-b ruling pending his
review at v2-pin time

## D-e — WP-E6 statistic re-scoped to Lyman-α P1D (decided 2026-07-27, later same day)

Following the filed negative of the DES-Y6 broadband adequacy pre-flight
(`docs/WP_E6_SYNTHETIC_ADEQUACY_PREFLIGHT_2026_07_27.md`: no (m, f) cell reaches 2σ;
best case σ≈0.49, full-sky check σ≈1.48), T0 directed: "rescope WP-E6 as proposed."
Effect: the WP-E6 observable statistic becomes the **DESI DR1 Lyman-α 1D flux power
spectrum** (the landscape brief's (b)-primary; >300,000 forests, arXiv:2505.07974), with
eBOSS DR14 P1D (Chabanier et al. 2019) as the fallback error-bar source. Mixed-fraction
framing (D-b) and the pre-flight-before-pin discipline are unchanged: a NEW adequacy
pre-flight on synthetic data precedes any v2 amendment drafting; if it also returns
negative, WP-E6 stops there and the negatives are banked. The DES Y6 result stands as
filed; D-c (DES Y6 as lensing product) is superseded for WP-E6's statistic but retained
as the lensing reference if a lensing-based observable ever re-enters via its own
pre-registration.
