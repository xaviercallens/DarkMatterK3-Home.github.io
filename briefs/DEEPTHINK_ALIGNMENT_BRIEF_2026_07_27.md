# Deep Think (T0s) Alignment Brief — 2026-07-27

**To:** Deep Think, Scientific Companion (T0s) per EXECUTION_PLAN §1.1
**From:** T1 coordinator session, on T0 (Xavier) instruction
**Purpose:** bring T0s current since its last engagements (2026-07-25/26: S3-00b blind
re-derivation concurrence; C1 root-cause literature review; M1 adjudication), and name
the specific places where adversarial review is now wanted. Canonical copy: this repo
(`SocrateAI-Scientific-Agora-K3-DarkMatter`); mirrored to the other two repos.
**Ground rule reminder (unchanged):** LLM output is never evidence (EXECUTION_PLAN
§1.2.4). Everything below traces to checkers, kernel proofs, read-and-hash-pinned
sources, or recorded T0 decisions — the point of this brief is to hand you the pointers,
not to be believed.

---

## 1. Program state in five lines

- **Stream 1 (Lean):** parked clean; `L₃ = Sym²(L₂)` kernel-proven [A]; optional new
  items from U1 fan-out (independent verification + formalization candidate).
- **Stream 2 (this repo):** **U1 executed and CLOSED [Tier B]** — T ≅ U⊕⟨14⟩ by explicit
  integral splitting; C2 v4 accepted by T0; **M1′ filed: conditional negative,
  structural** — Phase M dormant, re-gated on an exhibited X₄/B₃ (T0 D3′).
- **Stream 3:** F5b stands (PREDICTION v1.1 pinned, untouched). New empirical track
  under way: data landscape surveyed, WP-E7 DESI resolvability pre-flight done, WP-E6
  mixed-fraction adequacy pre-flight in progress (synthetic-only, rule 1 intact).
- **All stale ρ=4/T=18 / "Type II" citations corrected at source** (A.1.4, A.2.5, A.3.4,
  NO_PREDICTION_BRANCH §2/§8) with dated correction notes; epistemic ledger now in
  CLAUDE.md of all three repos.
- **T0 decisions today:** Stream 3 D-a/D-b/D-c and Stream 2 D1′–D4′ (records:
  `briefs/T0_DECISIONS_2026_07_27.md` in Dark Home repo;
  `briefs/T0_DECISIONS_2026_07_27_STREAM2.md` here).

## 2. The U1 result — and how to attack it

**Claim [B]:** the joint monodromy-invariant lattice of the cooper_s7 family is
U ⊕ ⟨14⟩: primitive even Gram [[0,0,−1],[0,14,0],[−1,0,0]], det −14, signature (2,1),
disc form ℤ/14 (q = 1/14), derived 2n = 14 from (T_cusp−1)² divisibility, and an
**explicit GL₃(ℤ) base change realizing the splitting** (which made the planned
Eichler/Cassels genus route unnecessary — no 2-adic claim is made anywhere).

**Verify mechanically** (each < 10 min, exact arithmetic + 60-digit numerics):
```
python3 checkers/check_U1_lattice.py          # full pipeline, structural assertions
python3 checkers/test_U1_controls.py          # s10 control → det −20/U⊕⟨20⟩; 3 scrambles; Yukawa scramble
```
Full record: `briefs/STREAM2_U1_EXECUTION_2026_07_27.md`; certificate
`data/certificates/C2_cooper_s7_v4.json` (T0-accepted; DRAFT retained for audit).

**Where adversarial value is highest — the two residual Tier-B links (brief §4):**
1. **Numerics → exact:** monodromy entries recognized from ~60-digit analytic
   continuation (residuals ~1e−59 vs a 1e−35 gate), then verified against exact
   structural gates (involutions, ∞-relation, invariant form, closure). Attack: is there
   a consistent wrong recognition that survives all exact gates?
2. **Monodromy lattice = T identification:** rests on Dolgachev Thm 7.1/§7 + Doran
   Thm 5.13 (fetched, read, hash-pinned in `docs/literature/MANIFEST.md`). Invariant
   even overlattices were enumerated (none), but the **λ-rescaling branch (T carrying
   λ·G, λ>1) is excluded by the framework shape, not by computation** — this is the
   honest residual gap. Attack: exhibit a family realizing λ>1 consistent with all three
   n=7 fingerprints (level-7 Hauptmodul match, √7 in elliptic monodromies, det −14), or
   argue it impossible and close the gap.

## 3. M1′ — the mechanism verdict changed character

`briefs/STREAM2_M1PRIME_MECHANISM_MEMO_2026_07_27.md`: six routes enumerated; outcome a
**conditional negative, structural** — M1's negative was epistemic ("cannot tell, inputs
retracted"); M1′'s is "can tell, and it is no: every route reaching a coupling terminates
on the same unspecified fourfold X₄/base B₃, which no amount of K3 lattice work
supplies." Key sub-results: A.2.5's "15 unstabilized moduli" wall dissolves under T=3
(operative content — no G₄ potential without X₄ — survives, corrected at source);
M1's own re-entry test (lattice data fixing chameleon constants) was run and returned
negative (dimensionless arithmetic cannot fix dimensionful constants). T0 chose
**Option B**: Phase M dormant, re-gate = exhibited X₄/B₃ (+ flux vector; + NS promotion
and a fibration selection principle for the gauge route). **Adversarial ask: is the
route enumeration complete?** A missed route that avoids the X₄ terminus would change
the decision landscape; confirmation that none exists hardens it.

## 4. Empirical track — new since your last review

- **Data landscape** (Dark Home repo `docs/DATA_LANDSCAPE_RESEARCH_2026_07_27.md`, every
  number carries its URL): DESI DR1 clears the old 10⁴/slice floor ~30× (LRG 2.14M,
  ELG 2.43M spec-z); DESI DR2 spectra not yet public; published pure-FDM bounds already
  cover 10⁻²²–10⁻¹⁹ eV entirely (Lyman-α → 2×10⁻²⁰; UFDs → 8×10⁻¹⁸), so T0 decided
  (D-b, delegated) the WP-E6 sweep targets **mixed fractions f_FDM < 1**, the genuinely
  open territory above ~10⁻²¹ eV; lensing product: DES Y6 (D-c).
- **WP-E7 pre-flight** (`docs/WP_E7_DESI_RESOLVABILITY_PREFLIGHT_2026_07_27.md`): under
  a proposed (unratified) occupancy criterion, only BGS reaches RESOLVABLE, only at
  r_s = 25 Mpc on the largest boxes; 10× stricter threshold ⇒ nothing resolves.
  **Adversarial ask: what is the principled occupancy threshold?** The verdict's
  sensitivity to this one number is its weakest joint; a first-principles derivation
  (shot-noise floor for the topological statistic) would convert it from proposal to
  criterion before T0 ratifies.
- **WP-E6 adequacy pre-flight** (in progress, synthetic-only): Fisher-style map of
  which (m, f_FDM) cells DES-Y6-like noise can distinguish at 2σ, overlaid with the
  published-bounds map. **Adversarial ask when it lands:** the mixed-fraction
  suppression model (linear interpolation between f=0 and f=1 power suppression,
  flagged in-code as an ENGINEERING approximation) — is that adequate for an adequacy
  map, and what replaces it at pin time?

## 5. Milestone map + alignment protocol

| Milestone | State | T0s involvement wanted |
|---|---|---|
| U1 lattice certification | **DONE [B]** 2026-07-27 | Attack the two residual links (§2) |
| M1′ / Phase M decision | **DONE** (Option B) | Route-enumeration completeness (§3) |
| WP-E7 occupancy ratification | pending T0 | Principled threshold derivation (§4) |
| WP-E6 v2 amendment → pin | drafting after adequacy pre-flight | Blind review of the amendment BEFORE pin (two-model rule) |
| Any future X₄/B₃ exhibition | not scheduled (new scope) | Mandatory blind re-derivation (EXECUTION_PLAN §1.2.3) |
| Gate E / v0.4.0 | parked (D4′: meaning retained) | Re-scoring review if an empirical route revives criterion 1 |

**Protocol:** this brief pattern repeats at each milestone gate; anything you produce
enters via the established debrief pattern (`briefs/DEBRIEF_DEEPTHINK_*`), is verified
against sources before adoption (the 2026-07-26 correction to your Tate-algorithm causal
account is the precedent — conclusions survive, mechanisms get checked), and directives
citing artifacts are validated for existence before execution (T0 D3 standing rule).

---
Generated-by: Fable 5 (T1 coordinator) | Verified-by: all cited checkers re-run green
2026-07-27; tier language checker clean | Reviewed-by: Xavier (T0) — commissioned this
brief in-session
