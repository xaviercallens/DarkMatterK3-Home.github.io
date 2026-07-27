# Deep Think (T0s) Alignment Brief — 2026-07-27 (evening update)

**To:** Deep Think, Scientific Companion (T0s) per EXECUTION_PLAN §1.1
**From:** T1 coordinator session, on T0 (Xavier) instruction
**Purpose:** update since this morning's `DEEPTHINK_ALIGNMENT_BRIEF_2026_07_27.md` — a
VM reboot interrupted and then a full recovery pass, five new results landed, and one
new manuscript effort started. Canonical copy: this repo
(`SocrateAI-Scientific-Agora-K3-DarkMatter`); mirrored to the other two repos.
**Ground rule reminder (unchanged):** LLM output is never evidence. Everything below
traces to checkers, kernel proofs, read-and-hash-pinned sources, or recorded T0
decisions.

---

## 0. What happened since this morning's brief

The session VM rebooted unexpectedly mid-work. Recovery was mechanical and complete: all
three repos verified clean (Stream 2's 11-command regression, now 13, all green; no data
loss). Six pieces of new work landed afterward, each T0-approved before or immediately
after filing. Nothing here is a correction to this morning's brief's content — it is
additive.

## 1. Stream 1 — U1 independently re-verified [B unchanged, stronger]

**New:** a *second*, independently-written exact-integer implementation
(`checkers/check_U1_splitting_independent.py`, this repo) re-derives its own GL₃(ℤ)
witness from the Gram alone (isotropic-vector search → Bezout hyperbolic completion →
orthogonal complement — not a replay of Stream 2's algorithm) and lands on the same
target `U⊕⟨14⟩`. 5 controls green, including a cross-family s10 discriminator. Record:
`briefs/STREAM1_U1_INDEPENDENT_VERIFICATION_2026_07_27.md`.

**Real finding, now closed:** the independent check surfaced that the v4 certificate
recorded only `det(P)` and `PᵀGP`, not the witness matrix P itself, forcing re-derivation.
T0 ruled: serialize it. Done — see §2.

**Adversarial value unchanged from this morning:** the two residual Tier-B links (§2 of
the morning brief — numerics→exact recognition; monodromy-lattice = T identification,
λ-rescaling branch excluded by framework shape not computation) are untouched by this.
Two independent implementations agreeing on the *arithmetic* does not touch either link.

## 2. Stream 2 — P-witness serialized, C2 v5 now LIVE [B, same tier, more auditable]

`data/certificates/C2_cooper_s7_v5.json` now carries the explicit base-change witness
`P = [[1,-252,84],[0,-6,1],[0,-1,0]]`, `det(P)=1`, and `PᵀGP` reproducing the certificate's
own `gram_after` — added as one new field, all prior derived/how/controls/tier values
unchanged from v4. v5 supersedes v4 as the LIVE lattice certificate (v3 unaffected,
remains the rank source; v4 and v4_DRAFT retained unchanged for audit — SHA256-verified
identical before and after promotion). Two witnesses now exist for the same Gram from two
independently written pipelines (Stream 1's `[[1,0,0],[0,0,-1],[0,-1,0]]`, Stream 2's
`[[1,-252,84],[0,-6,1],[0,-1,0]]`) — different matrices, same target, which is expected
(the witness is not unique) and is itself a mild three-way consistency point. New checker
`checkers/check_U1_witness_serialization.py` (3-way verdict: PASS / FAIL /
WITNESS_ABSENT, so v3/v4 correctly report absent rather than spuriously failing) + 7
controls, all green. T0 record: `briefs/T0_DECISIONS_2026_07_27_STREAM2.md` D5′.

**Nothing here changes any claim's tier or content** — this is auditability
infrastructure, not new mathematics.

## 3. Stream 3 — WP-E6b filed: Lyman-α P1D route is NOT closed (unlike DES-Y6)

Full record: `docs/WP_E6B_LYA_ADEQUACY_PREFLIGHT_2026_07_27.md` (Dark Home repo). Headline,
verbatim from the filed report:

> Under an explicitly optimistic linear-theory P1D-ratio forward model, confronted with
> DESI DR1's own published per-bin uncertainties, 221 of 260 (m, f) grid cells reach
> σ_equiv ≥ 2 against f=0 *and* remain open under the published mixed-fraction landscape.
> This is an ADEQUACY answer only — the same proxy, evaluated at the two masses where
> Liu, Gong & Zhou 2026 publish a 95% mixed-fraction bound, assigns σ_equiv ≈37 and ≈99
> where an emulator-grade analysis places its limit: optimistic there by 18.5× and 49.3×.

Contrast with the morning brief's WP-E6 (DES-Y6 broadband convergence): that route could
not reach 2σ even under a favorable toy model and is honestly closed. This route has only
*failed to be closed* — a materially weaker statement, kept weak on purpose in the report.

**Audit note (self-correction in-band, not from you):** the agent that filed this found
and fixed two defects in the interrupted predecessor's work before filing — the function
producing the 221-cell headline had zero test coverage, and one control could not fail by
construction. Both fixed; 473/473 tests green. Recorded in the same doc.

**Honesty flag still open:** 207 of the 221 decisive cells are open *only* because this
repo's own literature survey (`docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md` §4) lists no
mixed-fraction bound at their masses. Whether that reflects the literature or only this
survey's completeness is unverified. This is Phase 0 of the v2 proposal (§4 below) —
**your review of survey completeness here would be the single highest-value check on
this whole result.**

## 4. Stream 3 — WP-E6 v2 proposal filed (T0 D-f: proceed to drafting only)

`briefs/WP_E6_V2_PROPOSAL_LYA_P1D_2026_07_27.md` (Dark Home repo). Five phases, each
with an entry gate and a hard stop condition: **P0** literature re-survey (closes §3's
honesty flag; stop if <10 cells survive, or all survive only at f≥0.5, or it's already
published) → **P1** modeling adequacy, *source a public model, never build one* → **P2**
statistical design + re-derived sensitivity (full covariance, marginalized IGM nuisances,
not ratio-cancelled) → **P3** `PREDICTION` v2 pin → **P4** run-once real-data comparison.

**The load-bearing finding, stated as the report's own admission:** on this session's
survey, **no public flux-power emulator spans mixed (m, f) FDM parameter space** — LaCE/
cup1d/lym1d are ΛCDM-shaped and cannot carry a free-streaming cutoff; axionCAMB/AxiECAMB
fix only the linear transfer function (no flux power); axionHMcode is the wrong
observable and calibrated only up to 10⁻²¹ eV (below the region P0 would open); the
Liu/Gong/Zhou 2026 emulator that the optimism ledger is measured against has no found
code release. **P1's default is therefore STOP, by design.**

**Q1, explicitly flagged for adversarial input:** the report treats an author-held,
unreleased emulator as out of scope (CLAUDE.md rule 4: public products only; default
STOP rather than "ask the authors"). This is a judgment call, not a rule application —
**second opinion wanted on whether that's the right default**, and whether the survey in
§5 of the proposal actually missed a public option.

Only Phase 0 is authorized to execute; T0 sign-off on the full proposal is still pending.

## 5. Stream 3 — WP-E7 acquisition route found; large pull now running

`briefs/WP_E7_NOIRLAB_TAP_RECIPE_2026_07_27.md` (Dark Home repo): `data.desi.lbl.gov`
remains unreachable (connection-level) from this VM; NOIRLab Data Lab TAP is reachable
and, via `desi_dr1.zpix JOIN desi_dr1.photometry` on `targetid`, yields real (ra, dec, z)
DESI DR1 objects with tracer-bit selection (verified: 14.98M main-survey galaxies at
`spectype='GALAXY'`; a bitmask-filtered LRG count of 2.69M against a published
clustering-catalog N of 2.14M — a sane superset, since raw target-bit selection is
broader than the final science-ready catalog after fiber-assignment/veto cuts). **This
is not a substitute for the official LSS/BAO clustering catalogs** (no FKP weights, no
matched randoms) if a future work package needs BAO-grade systematics — it is sufficient
for WP-E7's actual purpose (real-field occupancy/resolvability geometry).

A background pull (BGS/LRG/ELG/QSO, `targetid, ra, dec, z` + tracer bits, z-cuts from
`data/derived/wp_e7_desi_preflight_2026_07_27.json`) is running now, unattended, writing
to the gitignored `data/raw/desi_dr1_noirlab/` (results and row-count cross-checks to be
reviewed and written up in `data/MANIFEST.md` next session — nothing here is committed
yet). Two items remain genuinely open regardless: the eBOSS DR16 LRG row-count mismatch
(174,816 fetched vs. 377,458 published — likely tangled with the pending eBOSS-sample-
identity T0 decision) and the occupancy-threshold ratification, neither of which blocks
acquisition, both of which gate interpretation.

## 6. Stream 1 — first pure-mathematics paper, drafting in progress

New, not previously mentioned to you: T0 approved drafting the program's first
peer-review-oriented manuscript, pure mathematics only (zero physics anywhere, including
motivation), under `paper/` in the Stream 1 repo. `paper/PLAN.md` gives an adversarial
legitimacy assessment (verdict: yes, publishable — *Experimental Mathematics* primary
venue recommendation) built on a 20-row claims-inventory table tagging every statement
LEAN / EXACT / NUM / CITED, tracing each to a repo artifact. Core contribution as framed:
a kernel-checked *uniform* Sym² structure theorem for the whole Cooper template (not
candidate-by-candidate, which is what the literature does), combined with exact
irreducibility/minimality and the now-doubly-verified `U⊕⟨14⟩` splitting — with full,
prominent tier disclosure of which parts are proven vs. numerically supported vs. cited.
Drafting of the remaining sections is in progress at time of writing.

**Two open scope questions where your read would matter, once sections are complete:**
(a) whether the paper's own anticipated referee objection ("Doran/Dolgachev already say
this") is adequately defused by the converse-direction framing (compute a concrete
operator's invariants, match against the framework, rather than deriving the framework);
(b) whether to include the Tier-B lattice material in this paper (Option A, drafted) or
defer it to a second, fully-unconditional paper (Option B) — PLAN.md §1.3.

## 7. Milestone map (updated)

| Milestone | State | T0s involvement wanted |
|---|---|---|
| U1 lattice certification | **DONE [B]**, now doubly-verified | Same two residual links as this morning (§1) |
| P-witness serialization / C2 v5 | **DONE, LIVE** | None — infrastructure only |
| WP-E6b Lyman-α adequacy | **FILED** | Survey completeness behind the 207-cell honesty flag (§3) |
| WP-E6 v2 proposal | **FILED, Phase-0-only authorized** | Q1: author-contact default, and public-emulator survey completeness (§4) |
| WP-E7 acquisition | **RUNNING** (background pull) | None yet — row-count review pending next session |
| Stream 1 first paper | **DRAFTING** | Novelty framing + scope A/B, once complete |
| WP-E7 occupancy ratification | still pending T0 | Unchanged from this morning |
| Monodromy-lattice = T identification | still Tier B | Unchanged from this morning (§2 of morning brief) |

---
Generated-by: Sonnet 5 (T1 coordinator) | Verified-by: all cited checkers re-run green
this session (13-command Stream 2 regression, 473 Stream 3 tests, 5 Stream 1 U1
controls); certificate hashes cross-checked before/after every promotion | Reviewed-by:
Xavier (T0) — commissioned this update in-session
