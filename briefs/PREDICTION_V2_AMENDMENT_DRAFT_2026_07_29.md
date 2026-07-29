# PREDICTION v2 Amendment — DRAFT (WP-E6-PIN)

**Status: DRAFT. NOT PINNED.** This document is a proposal for a `PREDICTION.md` v2
amendment. It carries no `PINNED:` header, is not itself hash-anchored as a pin, and
authorizes nothing by its own existence. Per `CLAUDE.md` rule 5 and the `prereg-pipeline`
skill, real-data comparison for the WP-E6 (m, f) sweep remains gated (synthetic-data infra
only) until a T0 session pins this amendment (or a revised version of it). **WP-E6-SWEEP may
not start before that pin — see §7.**

**Date:** 2026-07-29.
**Authority:** drafted per `briefs/EXECUTION_PLAN_2026_07_29_TWISTED_AND_WPE6.md` WP-E6-PIN
directive (T0 Action 4, executing S2-ledger-rule-5-equivalent discipline for Stream 3).
**Amends:** `PREDICTION.md` v1.0-PINNED (dated 2026-07-24 in the document, pin commit
`23b947e`, `git blame` L1 — content sha256 digest `854fa31ac559befd05ef77fc685effc6d22b7a57
ebc01449539ed58a14442a94` is the `PINNED:` header value, not a commit hash; the two are
distinct and this document does not conflate them). Does not alter §§1–6 of v1.0; adds a new
pinned branch alongside them, exactly as v1.0 §6 ("Derived quantities — RESERVED")
anticipated a later, separately-dated addition.
**Validation required before pin:** coordinator cross-check against `ANALYSIS_PROTOCOL` +
the grid pin (per WP-E6-PIN DoD); then T0 pin. Not self-promoting.

---

## 0. F5b guard — binding on this amendment and every output it authorizes

**This amendment authorizes a standalone (m, f) astrophysical constraint from Lyman-α forest
data. It does not authorize, claim, or imply any K3-derived observable, coupling, or
physical scale.** WP S3-00b (F-theory flux/tadpole derivation, "F5b") remains BLOCKED
(`CLAUDE.md` §"Epistemic boundaries", item 4). No output produced under this amendment —
table, figure, brief, or downstream citation — may state or imply a linkage between the
fuzzy/mixed dark matter mass–fraction grid tested here and any quantity from the K3
geometry program (m_φ, α_D, Λ_D, ρ, T, or any Tier B/C proposition in the S1/S2 ledgers).
This sweep's (m, f) axes are generic phenomenological dark-matter parameters, unconnected by
this amendment to any derivation chain in this program. Any future document that wants to
draw such a connection needs its own, separately-argued pin — this amendment does not supply
one, even implicitly.

---

## 1. What this amendment is, and is not

- **Is:** the pre-registration event required by `CLAUDE.md` rule 5 before the WP-E6 (m, f)
  exclusion/FIT sweep may touch real DESI data. It fixes, in advance of running the sweep,
  which grid, which data, which statistic, and which output labels apply — the ordering
  discipline the `prereg-pipeline` skill exists to protect.
- **Is not:** a new physics model, a new grid, a new statistical method, or a resolution of
  any open design question. Every choice below traces to an already-LIVE or already-pinned
  document, cited inline. Where a choice is not yet fixed anywhere, it is listed in §8 as an
  open item for T0 — not decided here.
- **Is not:** a modification to `PREDICTION.md` v1.0's existing branches (§§2–5, the
  K3-derived P1/P2/companion-Lyman-α-null-test structure). That structure is untouched and
  orthogonal; see §6 for the explicit disambiguation between v1.0's Lyman-α companion test
  and this amendment's sweep.

---

## 2. The pinned grid

The (m, f) grid is **already pinned** at commit `27cff4a` ("T0-DELEGATED: define real (m,f)
grid for WP-E6 v2 Phase 2"), defined in `briefs/T0_MF_GRID_DEFINITION_2026_07_27.md`. This
amendment does not restate the grid's numeric contents — read that file directly for the 8
mass values (log₁₀(m_FDM/eV), the emulator's native coordinate) × 7 fraction values (f_FDM),
56 cells total, z_str = "4.2" only.

**Status of the grid itself:** countermand window CLOSED 2026-07-28 with no amendments
(`briefs/T0_MF_GRID_DEFINITION_2026_07_27.md` §5 countermand log; ratified in
`briefs/T0_DECISIONS_2026_07_28_PENDING_ITEMS.md` D1). All three built-in grid controls
(f=0 column m-independence, −19.1-row null recovery, trained-support containment) PASS per
`data/derived/wp_e6_grid_controls_report_2026_07_28.json`. The grid stands exactly as
anchored at `27cff4a`. This amendment adopts it as-is; it does not reopen or re-derive it.

---

## 3. Data source

**Target observable class:** DESI DR1 Lyman-α forest 1D flux power spectrum, per the grid's
own redshift anchor (`T0_MF_GRID_DEFINITION_2026_07_27.md` A4: z = 4.2 slice, DESI DR1
QSO availability).

**Analysis design:** per the LIVE `ANALYSIS_PROTOCOL` document,
`briefs/ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md` (filename retains its draft date by repo
convention — the file itself is LIVE, not its name). Promoted DRAFT → LIVE by T0 commit
`7d0b2ce` ("chore(T0): ratify WP-E6 Phase 2 stats design protocol"; decision record
`briefs/T0_DECISIONS_2026_07_28_STREAM3.md` item 1). This governs:
- **Part A** (§1): 16×16 sample covariance construction from an N≈200 independent-realization
  `desisim` mock ensemble at z=4.2 (per-realization masking + Part C's corrected estimator),
  Hartlap-corrected.
- **Part C** (§3): the masking-bug fix (zero-fill edge discontinuity + biased-mean bug) and
  the mock-calibrated multiplicative window correction, methodology anchored to Ravoux et
  al. 2023 (MNRAS 526, 5118, arXiv:2306.06311) — T0-authorized in the same ratification
  (`T0_DECISIONS_2026_07_28_STREAM3.md` item 4: "Implement the mock-calibrated multiplicative
  window correction... Do not interpolate across gaps").

**k-bins:** p = 16 (log₁₀k = −2.2 … −0.7 in steps of 0.1, s/km), per `emu_predict.py`
`K_BINS`/`TARGET_COLS`, corrected in `ANALYSIS_PROTOCOL` §0 from an earlier "10 k-bins"
misstatement and independently confirmed by
`data/derived/wp_e6_grid_controls_report_2026_07_28.json`'s `k_bins_s_per_km` arrays.

**Real published data on hand:** `data/literature/desi_dr1_lya_p1d_2026_07_27.csv` — DESI
DR1 Lyα P1D, baseline QMLE estimator, metal(SB1)-subtracted, continuum-corrected
(arXiv:2505.07974), 1020 rows = 12 z-bins (2.2–4.4, Δz=0.2, includes z=4.2) × 85 k-bins,
fetched from the paper's own Zenodo release (DOI 10.5281/zenodo.16943723), checksummed in
`data/MANIFEST.md`. This file exists and is committed but **has so far been used only for
an ENGINEERING pre-flight** (`pipeline/wp_e6b_lya.py`, published *uncertainties* only, never
central values as a fit target, explicitly labeled ENGINEERING/not TEST/FIT). See §8 open
item 1 for why this amendment does not yet treat this file as the sweep's "observed" vector.

---

## 4. Statistic

Hartlap-corrected 16×16 covariance χ², four profiled nuisance parameters, per
`ANALYSIS_PROTOCOL` Part B (§2), extending the existing `integration_iminuit.py::build_chi2`
pattern:

```
chi2(m, f, zrei, ha, hs, taueff) = (pred - obs) @ Cov_inv_hartlap @ (pred - obs)
```
restricted to the single z="4.2" term (grid A4), Hartlap factor
`(N − p − 2)/(N − 1)` with N=200, p=16 → 182/199 (`ANALYSIS_PROTOCOL` §1.5 formula). N=200 was
provisional in `ANALYSIS_PROTOCOL` §1.5 pending a `desisim` timing run; that run is now
closed — `briefs/WP_P2t_DESISIM_TIMING_2026_07_28.md` reports full-pipeline N=200 ≈ 48s
(GO), authorized by `T0_DECISIONS_2026_07_28_STREAM3.md` item 3. N=200 is therefore treated
as settled here, not provisional.

**Degrees of freedom:** 12 per cell (16 k-bins − 4 profiled nuisance parameters),
`ANALYSIS_PROTOCOL` §2.3.

**Nuisance parameters and bounds provenance (`ANALYSIS_PROTOCOL` §2.2 table) — stated
explicitly per the T0 ruling below:**

| Parameter | Bound | Provenance |
|---|---|---|
| `zrei` | (6.05, 14.91) | Trained-support extremum, `param.pkl` column `z` |
| `ha` | (0.066, 3.989) | Trained-support extremum, `param.pkl` column `ha` |
| `hs` | (−0.987, 0.996) | Trained-support extremum, `param.pkl` column `hs` |
| `taueff` | (0.3, 1.8) | **PRIOR-BOX** — `lya-mfdm/mcmc.py` `BOUNDS_BASE`, a human-chosen MCMC flat-prior box, **not** a verified trained-support extremum of the network's input domain |

**`taueff` (0.3, 1.8) is a PRIOR-BOX, not a trained-support extremum.** This is a specific,
explicit T0 ruling (2026-07-28, `T0_DECISIONS_2026_07_28_STREAM3.md` item 2, made in the same
commit `7d0b2ce` that promoted `ANALYSIS_PROTOCOL` to LIVE): *"The (0.3, 1.8) bound is
explicitly accepted as a prior-box, not a trained-support limit. Ensure downstream
documentation explicitly states this to maintain epistemic honesty."* Any downstream code,
brief, or figure produced under this amendment must carry this distinction verbatim where
`taueff` bounds appear — in particular, Minuit converging with `taueff` pinned at 0.3 or 1.8
is a prior-box edge, not evidence the network's trained domain has been exhausted, and must
not be reported as the latter.

---

## 5. Output labeling

**Every output artifact this amendment authorizes — table, JSON, figure, or brief — is
labeled `exclusion` or `FIT`, never `TEST`, anywhere in the amendment text or in any output
it authorizes.** This is `CLAUDE.md` rule 5, verbatim on the labeling clause: *"Parameter
sweeps / exclusion-bound pipelines enter only via a pre-registered PREDICTION v2
amendment... and every output is labeled exclusion/FIT — never TEST — until pinned."*
(Note: CLAUDE.md's adjacent sentence "a sweep does not reopen it" refers to the separately
CLOSED WP-E5 2D transverse route, not to the TEST/FIT rule — not quoted here, to avoid that
conflation.) `prereg-pipeline`'s FIT-forever rule applies identically: any parameter not in
the pinned amendment (including any choice T0 resolves from §8) is a tuning event, logged in
`TUNING_LOG.md`, and demotes every comparison using it from `TEST` to `FIT` — permanently, no
exceptions. Under that rule `exclusion`/`FIT` is the *only* pair of labels this sweep's
outputs may ever carry; `TEST` is not merely deferred pending the pin, it is foreclosed by
the amendment's own design (§8's open items guarantee at least one post-pin choice, hence at
least one tuning event, on the very first real-data run). No amendment output may be
relabeled `TEST` retroactively. **Every other occurrence of the string `TEST` in this
document is prohibition-context only** (stating what a label must never be) — no output
artifact this amendment authorizes carries that label, under any circumstance.

---

## 6. Disambiguation from `PREDICTION.md` v1.0's existing Lyman-α branch

`PREDICTION.md` v1.0 §3 already names a "Lyman-α null test" (SDSS DR12 / DESI) as a
**Companion** branch to the K3-derived P1/P2 observable — that test is *tied to* the
eventual S3-00 K3 derivation (a detection there is evidence against the K3-linked model,
feeding v1.0 §5's kill condition). **This amendment's sweep is a different, unrelated
analysis**: a generic (m, f) fuzzy/mixed-dark-matter exclusion grid with no K3 linkage
(§0 guard). The two must not be conflated in any report: v1.0 §3's companion test is
Tier-C-adjacent and currently has no computable target (F5b blocks m_φ); this amendment's
sweep is deliberately K3-free and proceeds independently of F5b's status.

---

## 7. Sequencing — this pin does not start the sweep alone

Per `briefs/EXECUTION_PLAN_2026_07_29_TWISTED_AND_WPE6.md` §1 dependency graph,
WP-E6-SWEEP requires **all** of: this amendment pinned, WP-E6-P2A (Hartlap covariance,
not yet executed — Part A's design is LIVE, its N=200 run is a separate deliverable),
WP-E6-P2B (nuisance profiling code, depends on P2A), and WP-E6-P2C (masking fix,
paper-verified against Ravoux et al. 2023 directly, not yet executed). **A T0 pin on this
document authorizes the mechanism (grid + data class + statistic + labels); it does not by
itself supply the covariance, profiling code, or masking fix that the sweep needs to run.**
Escalation trigger carried from the execution plan: "amendment not yet pinned (DO NOT
START)" — restated here as binding on this amendment's own downstream WP.

**Separately, and just as binding: a pin on this text as currently written authorizes the
mechanism only, not real-data contact.** §8 items 1–2 mean this draft does not yet specify
what the sweep's real "observed" vector *is* or how it maps onto the emulator's k-grid. If
T0 pins this document unrevised, that pin freezes the grid/statistic/labels but a subsequent
implementer still may NOT build an `obs` vector for a real chi² — using Part A's synthetic
mock-ensemble mean, or any ad hoc reading of `data/literature/desi_dr1_lya_p1d_2026_07_27.csv`,
would each be exactly the kind of free choice this WP's hard rule prohibits picking silently.
WP-E6-SWEEP is blocked on §8 items 1–2 being resolved in the pinned text (or a superseding
pinned revision) in addition to the P2A/P2B/P2C code deliverables above — both blockers must
clear, not just the latter.

---

## 8. Open items — NOT resolved here, flagged for T0

Per the WP-E6-PIN hard rule ("every analysis choice... must trace to an ALREADY-LIVE or
ALREADY-PINNED document... do not introduce any new free analysis choice"), the following
were found, during drafting, to be **not yet fixed by any LIVE or pinned document**. They are
listed, not decided:

1. **Real "observed" P1D vector provenance is unresolved.** `ANALYSIS_PROTOCOL` Part B's
   worked example uses `p_bar_42` = Part A's *synthetic mock ensemble mean* as the `obs` in
   `chi2(...)` — explicitly a null-cell sanity/self-consistency construction, not real DESI
   data. The one real, published DESI DR1 P1D product on disk
   (`data/literature/desi_dr1_lya_p1d_2026_07_27.csv`) has, to date, been used only for an
   ENGINEERING pre-flight (`pipeline/wp_e6b_lya.py`) that confronts its *uncertainties*
   against a linear-theory ratio model — never its central values, and never via the NN
   emulator this sweep uses. **No LIVE document specifies whether/how the actual pinned
   sweep's `obs` vector for a real exclusion/FIT result is to be built from this real CSV
   (versus continuing to use a synthetic-ensemble stand-in, which would not be a real-data
   comparison at all).** This must be resolved by T0 before WP-E6-SWEEP computes anything
   claiming contact with real data.
2. **k-bin correspondence between the two grids is unspecified.** The emulator's native grid
   is 16 log-spaced k-bins (log₁₀k = −2.2…−0.7, s/km). The real published CSV is tabulated on
   its own, different 85-bin grid (k = 2.5×10⁻⁴–5.27×10⁻² s/km, narrower and differently
   spaced), restricted by the source paper's own recommended validity cuts (§4.1 of
   arXiv:2505.07974, per `data/MANIFEST.md`'s entry). No document specifies a
   rebinning/interpolation/restriction scheme mapping the published table onto the
   emulator's 16 native bins (or vice versa) for a real chi² term. This is a prerequisite of
   open item 1, not a separate later step — the two must be resolved together.
3. **Covariance source for the real comparison is ambiguous.** `ANALYSIS_PROTOCOL` Part A
   argues the synthetic `desisim`-mock covariance is preferable to reusing the emulator's own
   training-data covariance (`lya_data.pkl`) because the latter is "not a DESI-realistic
   uncertainty on our forward-simulated grid predictions." It does not, however, state
   whether the *actual* pinned sweep should use (a) this synthetic mock covariance, or (b)
   the real published DESI covariance/uncertainty (`e_total_kms`, or the full `COVARIANCE`
   HDU referenced in `data/MANIFEST.md`) that ships with the real data itself. Both are
   defensible design choices; neither is currently fixed as *the* one to use for a real-data
   result under this pin.

**This amendment recommends none of the three options above and picks none of them.** Per
the WP-E6-PIN escalation trigger, they are listed for a T0 ruling; whichever is chosen must
be recorded (in this file, on amendment, or in a superseding pinned version) before
WP-E6-SWEEP treats any output as touching real data.

---

## 9. Pin mechanics (for when T0 pins this)

Following the `PREDICTION.md` v1.0 precedent (pin commit `23b947e`, "the git commit
introducing this version IS the hash-pin" — v1.0's `PINNED:` header carries a content
sha256 digest, `854fa31...`, distinct from the commit hash; both conventions are available,
implementer's choice, but must not be conflated as this draft's own §1 note flags): pinning
this amendment means committing it (or a T0-revised
version resolving §8) with a `PINNED:` header analogous to `PREDICTION.md`'s, and recording
the pin as a new dated entry appended to `PREDICTION.md` itself (a v2 branch, alongside
v1.0's existing §§2–5) or as a standalone pinned file cross-referenced from `PREDICTION.md` —
implementer's choice of mechanics, T0's choice of content. The pin commit's timestamp must
predate any commit that builds the real-data `obs` vector resolved in §8 item 1, per the
`prereg-pipeline` skill's core invariant (pin predates data-touching commits).

---

*Generated-by: Sonnet (Stream 3, WP-E6-PIN) | Verified-by: every cited parameter traces
inline to `27cff4a` (grid), `7d0b2ce` (ANALYSIS_PROTOCOL LIVE + taueff ruling), and
`data/MANIFEST.md` (real data provenance) — no numeric value restated from memory | Three
open items flagged in §8, not resolved | Reviewed-by: pending T0 (Xavier) — DRAFT, not
pinned.*
