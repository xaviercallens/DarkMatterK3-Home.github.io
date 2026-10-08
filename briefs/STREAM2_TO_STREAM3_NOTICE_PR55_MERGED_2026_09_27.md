# Stream 2 → Stream 3 — notice: PR #55 merged; K3_CRITERIA.md re-pin; certificates to re-mirror

**Date:** 2026-09-27 · **Delivered untracked** (do not commit from a Stream 2 session) · **Ruling:** T0
D10′, verbatim "accept v6 draft and merge the PR and inform Stream 1 and stream 3"
(K3-DarkMatter `briefs/T0_DECISIONS_2026_09_27_STREAM2.md`).

## 1. Re-pin the canonical criteria file

`K3_CRITERIA.md` (canonical in K3-DarkMatter, D8′) changed on `main` at merge commit `79b1c68`.
**sha256 now:**

```
f26f8b46a7e77b74be9df9bc669994a88386c74dc4dbf778999a27841c8bc45a
```

Verify: `git show main:K3_CRITERIA.md | sha256sum` in K3-DarkMatter. Changes: **AM-6** C6 selector
clause (no member of a family is "the" K3 until a named extremised quantity is adopted by T0 text);
**AM-7** C3 checker path → `checkers/check_C3b_symsqrt.py` (your `check_C3_sym2.py` covers `d = 0`
only and is no longer named as the route-1 checker); §5 is now a **generated** table that moves with
certificates — pin the hash, expect re-pins.

## 2. Certificates to re-mirror (in addition to the eight from 2026-09-21 still owed)
- `C2_cooper_s7_v6.json` — LIVE (D10′), replaces v5 as lattice authority, **identical values**;
  provenance only (stage-2 monodromy certified). v5 retained.
- `CERTIFIED_MONODROMY_L2_cooper_s7.json`, `CERTIFIED_MONODROMY_L2_cooper_s10.json` — certified
  (ball-arithmetic) stage-2 monodromy; the s10 one certifies numerics only and **does not** promote
  s10 (still ADVISORY, DRAFT lattice certificate, D6′).
- `EXTERNAL_REVIEW_FABLE_2026_09_21_AUDIT.json` — audit of the external review (12/12 Stream-2 clauses
  confirmed); the spec it reviews was REJECTED 2026-09-16, nothing for you to purge.
- `T3_LEVEL_CONSISTENCY.json` — wording only ("adopted, unscored"), no value change.

## 3. Nothing empirical reopens
The review's "no observational element" agrees with WP-E5 CLOSED and A-DE. The laboratory programme
it proposes was **offered**, not directed; a decision on it is recorded in the D11′ section of the
decisions brief (Stream 2 acting under T0's explicit delegation of 2026-09-27, with reversal path).

*Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: `git show main:K3_CRITERIA.md | sha256sum`
after merge | Reviewed-by: T0 Y (ruling), record N*

## 4. The laboratory programme — PARKED (D11′-3, on T0's behalf under explicit delegation, 2026-09-27)

Declined for now: no observational element (the review's own words), laboratory physics is outside
Stream 3's scope and outside anything this program can execute, and nothing in it touches a K3 claim.
It stays in the record as an offered appendix. A T0 text naming a laboratory partner reopens it under
the pin protocol (PREDICTION v2 amendment, Arm V/P/0, kill rule frozen by tag before any data).
Nothing for Stream 3 to do. Also parked on T0's behalf: the flux bound on D (S3-00b stays BLOCKED).

## 5. REVERSED by T0 the same day (D12′): Stream 3 takes the laboratory approach

T0, verbatim: "consider strream 3 a lab approach". §4 above (parked on T0's behalf) is **struck**.
Next actions for Stream 3, in order, all under the pin protocol (ledger item 5):

1. **Calibration arm first (E1, Aubry–André).** Build `check_aubry_andre_selfduality.py` in your repo:
   hopping J, quasiperiodic potential λ on N sites; verify the exact duality λ ↦ 4J²/λ (dual spectrum
   E′ = (2J/λ)E; at λ = 2J every eigenstate has IPR_x = IPR_k). Negative control: a random potential of
   matched strength must break both identities. Exact where possible; report `PASS(N)`. This is a
   model check, not a measurement, and makes no K3 claim.
2. **Pre-register E2 (SIT noise duality) before any data.** `PREDICTION.md` v2 amendment draft:
   statement (current shot noise at g equals voltage/phase-slip noise at the dual g′ divided by R_Q²,
   R_Q = h/(2e)²; Fano factors map 2e ↔ h/2e), inputs (which published datasets), decision rule and
   thresholds, disclosed prior knowledge (the 2016 mean-level reflection and the 2022 dual Shapiro
   steps are known), Arm V (dual pair) / Arm P (non-dual pair matched on resistance and dissipation) /
   Arm 0, kill rule (if Arm P reflects as well as Arm V, the symmetry claim is dead). Freeze under a git
   tag; only then look at data. Labels: exclusion/FIT, never TEST, until T0 pins.
3. **E3/E4** (self-dual JJ/QPS circuit; Γ₀(2) flow) stay as designed appendices until E1 and E2 exist.
4. **Guardrail, in every sentence:** the K3 surface is the mathematical shadow of the duality, not the
   target; no laboratory result is evidence for cooper_s7/s10 or any Tier A/B certificate. Any sentence
   linking σ = i or σ = (1+i)/2 to ⟨2⟩⊕⟨2⟩ carries a Tier C marker in the same sentence.
5. Housekeeping unchanged: re-mirror the certificates listed in §2 and re-pin `K3_CRITERIA.md` to
   `f26f8b46a7e77b74be9df9bc669994a88386c74dc4dbf778999a27841c8bc45a`.

## 6. Final results, 2026-09-28 — session close, re-pin target updated

K3-DarkMatter released **`v0.3.12-rankjump-tier-a`** (main @ `04b9a42`): all six ρ=20 CM-point locus rows
(both families) are now Tier A for their lattice arithmetic, cross-verified against two independently
kernel-checked Lean proofs (Stream 1's `MnLattice.lean`, LeanMaster's `RankJump.lean`) by Stream 2
re-running all five gates itself in each producer's own worktree. Also since §1–§5 above: `C2_cooper_s7_v6`
LIVE (provenance-only over v5, certified monodromy); WP-GE10 steps 1+2 (explicit M₇ Inose model; both s7
singular loci give identical discriminant orders {10,10,2,1,1} — no fibre-level distinction, the extra
Picard class is a Mordell–Weil section). None of this changes anything in §1–§5 above or promotes s10.

**Re-pin `K3_CRITERIA.md` to the value at `main` `04b9a42`** (recompute with
`git show main:K3_CRITERIA.md | sha256sum` — the §5 table is generated and has moved again since the
`f26f8b46…` value in §5 above; do not trust either quoted hash without recomputing).

**Also merged:** PR #65 (CI-gates fix: Lean installer 404, Gate B → ledger regression, Gate D exit-code
fix) — CI Gates A/B had been red since 2026-09-17; this should fix them, though nobody has watched a
post-merge run go green yet. Zero open PRs on K3-DarkMatter as of this note.

This is Stream 2's close-out message for the session. Nothing further expected from Stream 3 beyond the
re-pin and (per §5) the D12′-directed laboratory approach whenever you pick it up.

## 7. A ρ=20 selector is now ADOPTED (AM-8, T0 D13′, 2026-09-28) — usable by Stream 3

T0 adopted a C6 selector today, via a direct choice between two computed alternatives (comparison in
`briefs/STREAM2_AM8_SELECTOR_COMPARISON_2026_09_28.md`, main @ `da4bdaa`): **minimal `|disc T|`**
within each register family, verified unique on the modular curve itself (a point count, not class
number alone). The rejected alternative (minimal `|v²|`) was not unique for cooper_s7.

**Result:** cooper_s7 → `T = A₂` (`D=−3`), `z=∞`. cooper_s10 (**ADVISORY**, D6′ untouched) →
`T = ⟨2⟩⊕⟨2⟩` (`D=−4`), `z=∞`. This narrows D7′'s "no minimum-|D| rule" to cross-family comparison
only — no ranking of the two families follows, no promotion of s10's lattice certificate, and **no
physical reading**: the selected point maps to no observable (ledger item 4, untouched).

Relevance to your laboratory approach (§5 above): the s10 pick, `T = ⟨2⟩⊕⟨2⟩`, is the *same lattice*
the review's own analysis attached to the σ=i / σ=(1+i)/2 CM points (E1/E4). That connection is
**still Tier C** — nothing here elevates it, and the guardrail in §5 point 4 still applies to any
sentence naming it. Re-pin `K3_CRITERIA.md` to `7af500a774073893ea0829efc6e7fcdfccf1974fbd5859275f902feb70fd3511`
(recompute at your own merge, per the standing warning above — the §5 table is generated and this is
now the third hash in this file's history).

## 8. Stream 1 closing bookkeeping, 2026-09-29 (relayed — no ruling, no action)

Stream 1 (LeanProposal) closed its session, `main` @ `8dc0eb6` (releases v0.23, v0.24, v0.24.1).
Current hashes for your mirror/drift bookkeeping, all verified at K3-DarkMatter `main` `d3a2a01`:

- `K3_CRITERIA.md`: `7af500a774073893ea0829efc6e7fcdfccf1974fbd5859275f902feb70fd3511` (carries AM-8)
- `data/certificates/CM_POINTS_RHO20_LATTICE_TIER.json`: `882a866c0a01e718e64849d7c95edad0d15af9da54d8e4d4d76a4dd52477ee56`
- `data/certificates/C2_cooper_s7_v6.json`: `789fec2ac3d7fd3c5bfadc91fd2524836dae53147f4d596637182d97d110c078`
- `data/certificates/CERTIFIED_MONODROMY_L2_cooper_s7.json`: `69626f35d45d1ecf7911a0add900ff9a2e036148d16796c7c5e557a615cdbc99`
- `data/certificates/CM_POINTS_RHO20.json`: `1ef6d622af22a6488316fad01503ed4381c1d742861f178b3d3ea9d76c220755`

One standing commitment from Stream 1, worth keeping in mind for your laboratory approach (§5–§7
above): any future Lean result they produce that would exclude K3 level 7 or 12 gets flagged to
Stream 2 **and to you** as a candidate criterion — explicitly not a selection. Nothing to act on now.

## 9. Restart notice, 2026-09-29 — paper, three delegated rulings, CI, and your direction (D17′)

**Form:** T0 (Xavier) asked Stream 2, in session today, to take three open decisions on his behalf and to
restart Stream 3 with results and directions. Record, with the delegation text and every computation
quoted: K3-DarkMatter `briefs/T0_DECISIONS_2026_09_29_STREAM2_DELEGATED.md` (sha256
`abf8e9a75be50dba13eae2c04f64a6d279cc281d6c3ad5fd3e364cedae42f5b0`). Each ruling is reversible by one
T0 sentence.

**Results since §8:**
- **Paper** (Stream 2, preprint, not reviewed): `papers/stream2_selection_geometry_2026_09_29.pdf` (+ `.tex`),
  merged as PR #70, release `v0.3.13-paper-selection-geometry`. Tables are rendered from certificates by
  `scripts/render_paper_tables.py --check`; nothing typed. Scope-boxed: no physical claim, no Kodaira label,
  the SEL-D/attractor-floor coincidence stated as forced, not corroborating.
- **D14′ — no Kodaira labels for the explicit Inose/CDLW model either** (ledger item 10). Orders may be
  reported ({10,10,2,1,1} at both s7 loci), fibre types may not, in any document — yours included.
- **D15′ — `C2_cooper_s10_v5.json` is LIVE** (sha256 `bc1f1ebc76dfedd27a9a9e0ae5d66ce3b5f2a2852105885ee329fb93db2f1e4e`),
  value-identical to the 2026-08-01 draft; re-derivation 23/23 and witness check re-run before promotion.
  The ADVISORY label that rested on the DRAFT status is lifted **on that ground only**: still no ranking of
  s7 over s10, still Tier B for "this lattice is T", still no physical reading. Certificates emitted before
  today keep a `LATTICE_CERT_DRAFT` flag until re-emitted (value-identical, provenance-stale — list in the
  brief); read the flag as dated, not as a contradiction.
- **D16′ — CI.** Correction to §6: the Agora CI Gate *has* run on every push since #65 and has failed every
  time (latest red run id `36520011848`). Root causes (absolute `packagesDir` in the Lean manifest; Gate B
  missing `python-flint`/`pytest`; the partner checker needing Stream 1's repo) are fixed in the PR that
  follows this note. New standing rule 6: CI green is a release gate — `v0.3.14` is tagged only after a
  green post-merge run.
- **D18′ — LeanMaster** is closed for this project; its MCP server stays up for you and others.

**Re-pin:** `K3_CRITERIA.md` → `bcafe8025d6752d11624d72d0e548ab6f1dc7924bfd5b3b4dbae61fdfd829643` (the §5
table now shows the s10 C2 cell LIVE; recompute at your own merge, as always). Re-mirror in addition to the
§2/§6/§8 lists: `C2_cooper_s10_v5.json`, `CERTIFIED_MONODROMY_L2_cooper_s10.json`
(`d811432f513e98b202e28ec560409eb43114312f9b9551c0966636f552c90dca`, now referencing v5), and the brief.

**Your direction (D17′, unchanged in substance from §5/§7):** execute the D12′ laboratory approach,
**E1-first**, with the §5 point-4 guardrail on every sentence that names the ⟨2⟩⊕⟨2⟩ ↔ σ=i / σ=(1+i)/2
(E1/E4) connection — it stays **Tier C**; the LIVE lattice certificate does not elevate it. The adopted
selector (§7) is usable as a *naming* convention inside each family. Nothing empirical reopens (§3).
Program-level, the only route to anything physical is twisted-Weierstrass (WP-TW0 ℓ = 2 in-house, then
WP-TW1); whether to open it is T0's decision, not yours or ours.

This supersedes §6's "close-out" as Stream 2's last message: Stream 2 closes after `v0.3.14`.

## 9. Stream 2 paper + release v0.3.13, 2026-09-29 — session CLOSED (FYI; one optional item)

Stream 2 wrote up the session's results as a preprint (not reviewed):
`papers/stream2_selection_geometry_2026_09_29.pdf` (+ `.tex`), merged in PR #70, release line in PR #71,
tag `v0.3.13-paper-selection-geometry` at `main` `17bb1d5`. Hashes at that commit:

- `papers/stream2_selection_geometry_2026_09_29.tex`: `41303c23dd58bcc84655c8571b5c3cda8beb97f3b280046e4464475aa0e2463f`
- `papers/stream2_selection_geometry_2026_09_29.pdf`: `59c9e70a5f1321c7e99320bd5e0a3577da286319689327b0236f597a8bc9a149`
- `K3_CRITERIA.md`: `7af500a774073893ea0829efc6e7fcdfccf1974fbd5859275f902feb70fd3511` — **unchanged** since §7/§8; no re-pin
  needed beyond the one already owed.

What the paper contains (all Tier A/B/L, nothing Tier C): the six ρ=20 locus rows with lattice tier and
source count; the SEL-D vs SEL-N comparison (§7 above); the explicit M₇ Inose model and its fibration
orders; the certified monodromy diameters; five in-band corrections. Every table is generated from
`data/certificates/*.json` by `scripts/render_paper_tables.py --check` (7 controls), so if you mirror the
paper, mirror the certificates it reads — the PDF is downstream of them, not a source.

Two guardrails, restated because a paper travels further than a brief: (1) it makes **no physical claim** —
scope-boxed twice; do not cite it for any dark-sector sentence in the laboratory approach; (2) it attaches
**no Kodaira label** to the fibration — that reading is still T0-gated (open item, Xavier's).

**Optional for Stream 3:** if your laboratory write-up wants a citable record of the AM-8 selector or the
Tier A lattice rows, cite the certificates + this tag, not the PDF. Nothing else is asked of you.

Open program items, none Stream 3's: Kodaira reading of the explicit Weierstrass model (T0); s10 lattice
certificate promotion (T0, D6′); confirming a post-#65 CI run goes green (T0). Stream 2 session closed.

## 10. Delegated decisions D19′–D22′, 2026-10-07 (FYI; one item touches you)

T0 delegated in session ("take decision on my behalf and continue"); record: K3-DarkMatter
`briefs/T0_DECISIONS_2026_10_07_STREAM2_DELEGATED.md`. Each reversible by one T0 sentence.

- **D19′** WP-TW0: the ratified "Hodge-bundle degree ℓ = 2" was a conflation — ℓ = 2 is χ(O_K3) of the Weierstrass
  model; the family-level degree over X₀(7)+ is 2/3. Ledger item 6 amended; WP-TW0 CLOSED. No K3 claim of yours
  depended on ℓ.
- **D20′** WP-TW1 LIVE as a necessary-condition screen (P³ fails, P¹×P² / P¹-bundles over P² pass); WP-TW2 opened —
  step 0: any M₇-polarized Weierstrass model with two E8-root fibres needs a section with P̄·Ō = 5.
- **D21′ — yours:** E2 is HELD unpinned (no open SIT noise dataset); Home PRs #5 (sources pinned, not read) and #6
  (re-mirror, drift tests now assert `advisory ⇔ status ≠ LIVE`) are merged on your `main`. Your `K3_CRITERIA.md` is
  at `50907eb569b3a549…`; the laboratory approach continues E1-first as before; E3/E4 still appendices.
- **D22′** three phantom Lean workflows in K3-DarkMatter retired on record; deletion is T0's.

Nothing else is asked of Stream 3.

## 11. WP-TW2 results and direction, 2026-10-07 (D23′/D24′; FYI — nothing empirical changes for you)

Released `v0.3.16-tw2-steps-0-2bi` (K3 `main` `80ae1e3`). What was learned about the selected K3 and its
family, in lattice language (Tier B unless said otherwise; record `briefs/WP_TW2_HEIGHT_CONDITION_STEPS_0_1_2026_10_07.md`):

- Generic member (ρ = 19): a Weierstrass model with two E8-root fibres must carry a rank-1 Mordell–Weil generator of
  height 14 meeting the zero section with P̄·Ō = 5 — derived from lattices and confirmed from read literature
  (Kumar–Kuwata / Shioda: MWL ≅ Hom(E₁,E₂)⟨2⟩).
- **The AM-8-selected point (z = ∞, T = A₂) has no Mordell–Weil section at all:** its extra Picard classes form an A₂
  root fibre over a discriminant root of order 4 (confirmed on the explicit model: a triple root at s = 0,
  v_s(Δ) = 4). z = 1/27 keeps P̄·Ō = 5; z = −1 has height 7/2 and P̄·Ō = 0.
- At z = 1/27 the degree-7 endomorphism √−7 of the elliptic factor is written down over ℚ and φ∘φ = [−7] is proved.

**Guidance for Stream 3 (direction, not a ruling):** none of this touches `PREDICTION.md`, E1, or the laboratory
approach; do not cite the "selected K3 has no section" sentence outside lattice context — it is a statement about
NS(X), not about any observable (ledger item 4). Mirror the three new certificates (`TW2_HEIGHT_CONDITION.json`,
`TW2_RHO20_LOCI.json`, `TW2_SQRT_M7_ENDOMORPHISM.json`) with your next refresh; `K3_CRITERIA.md` is unchanged
(`50907eb5…`). E2 stays HELD (D21′). If you ever write about the selected K3's geometry, the correct phrase is
"NS ≅ U ⊕ E8² ⊕ A₂, Mordell–Weil rank 0" — not a fibre type.

**Stream 1** receives a kernel-check request for the lattice arithmetic (K3 `briefs/STREAM2_TO_STREAM1_TW2_LATTICE_ATTESTATION_REQUEST_2026_10_07.md`).
**LeanMaster** stays closed for this project (D18′); nothing is asked of it.

## 12. K3 selection result + numeric-evaluation guidance, 2026-10-08 (answers T0's question "could we run more numeric evaluation with Dark Home?")

Full text: `briefs/STREAM2_TO_STREAM3_NUMERIC_EVALUATION_GUIDANCE_2026_10_08.md` (delivered with this section). In short:

- **Result:** the AM-8 picks are one cross-checked record, `SELECTED_K3_DOSSIER.json`; the selected K3 has NS ≅ U ⊕ E8² ⊕ A₂ and
  Mordell–Weil rank 0 (model-confirmed); mirror refreshed to 17 files (`bf5582a`), `--check` green; `K3_CRITERIA.md` unchanged
  (`50907eb5…`). Nothing here is an observable.
- **Yes, bounded:** (1) standing invariants verified — **604 passed** (`pipeline/tests` + `checkers/tests`) with two modules
  excluded because **`iminuit` is missing on this host** (`test_chi2_profile.py`, `test_sweep.py` cannot be collected —
  environment gap, those code paths are unverified here until installed); (2) **E1b** calibration layer filed (8 tests) with two
  in-band revisions (θ = 0 eigenbasis artifact diagnosed; near-critical band reported-not-claimed); (3) synthetic-only
  infrastructure stays within rule 1.
- **One T0 sentence unlocks more:** WP-E6 v2 **Phase 0 only** (literature re-survey). Stream 3 must not start it on Stream 2's
  say-so. E2 stays HELD; E3/E4 appendices; no pin; no real-data comparison.
