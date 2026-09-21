# T0 decision request — K3 selection: five items, none of which Stream 3 can close

**Date:** 2026-09-21 · **From:** Stream 3 (experimentation) · **To:** T0 (Xavier)
**Records:** `briefs/STREAM3_K3_SELECTION_ROUTE_AUDIT_2026_09_21.md` (Home),
`STREAM2_TO_STREAM3_C3_BRANCH_REPLY_2026_09_21.md` and
`STREAM2_TO_STREAM3_MODULAR_RAIL_AND_CM_POINTS_2026_09_21.md` (K3-DarkMatter).
**Status:** decision request. No gate moved, no pinned document touched, nothing scored.
Every item below is T0's because it changes a ledger, a freeze-blocking document, or a criterion's
meaning — none is a computation either stream can settle.

## Context in three sentences

Stream 3 was asked to find the K3 of K3×T² using DESI data and the T4 GPU. Neither can: the sweep
chain contains no candidate-dependent input, so an unblocked real-data run would emit an (m, f)
contour bit-identical for every candidate, and the K3 → observable map is Tier C and BLOCKED under
F5b. Checking why turned up four things about the *criteria* rather than the data, and Stream 2's
same-day reply added a fifth.

---

## D-1. The ρ = 20 fork — adopt the definiteness cut, or not?

**The question.** The arithmetic route cannot select a K3, and this is a theorem, not a gap: the
rank-3 lattice is indefinite (`g9_verdict`, Tier A), so it picks out a modular curve, not a surface.
Adding ρ = 20 makes T rank-2 positive definite and the classification finite, with a smallest case
T_S = A₂ at D = −3 (`smallest_black_hole`'s `reducedForms 3 = [(1, 1, 1)]`, `decide +kernel`).

**What is new since the audit.** Stream 2 computed what the cut picks out inside the register
families (Stream 3 re-ran their controls: 46/46 and 35/35). All three singular points of the s7
operator are ρ = 20 CM points — D = −28, −7, and **−3 at z = ∞, which is A₂ itself**. **A₂ is in the
s7 family and not in s10**, the latter by an exact all-vector congruence (−3 is not a square mod 40).

**What T0 is asked.** Whether the program adopts ρ = 20 as a criterion. Two cautions belong in the
decision and both come from Stream 2: the agreement between the binary-form and modular sides is
**forced** by Shioda–Inose, so it is not independent corroboration; and **no ranking of s7 over s10
follows** from "A₂ is in s7" — a minimum-|D| rule has no warrant in this program. Stream 3 takes no
position. This is the highest-leverage item here: every other selection question is downstream.

## D-2. Does C3 require integrality of the order-2 partner?

**Why it is now decisive.** Stream 3 derived that the AZ/Cooper operator shape is anti-self-adjoint
**identically in (a, b, c, d)**, so every family member is a symmetric square by construction —
and the sporadic order-3 landscape is exactly the nine sequences in `ORDER3_AZ_COOPER`
(15 sporadic = 6 Zagier order-2 + 6 AZ + 3 Cooper, verified against the hash-gated source). Stream
2's Doran Thm 5.13 record says the same from the framework side. **So C3 as written cannot
discriminate between candidates — it is passed by construction.**

But Stream 2's table records that s7's square-root partner **A279619 is integral** while **s10's is
dyadic and non-integral**, and asks whether C3 requires integrality.

**What T0 is asked.** Rule on it, because the two readings have opposite consequences:

- **If C3 requires integrality**, it stops being non-discriminating: it separates s7 from s10, and
  becomes the second candidate-dependent predicate in the program.
- **If it does not**, C3 is a well-formedness check on the family and nothing more, C3b inherits
  that (being defined only for C3-cleared candidates), and **C1 is left as the only committed
  checker with per-candidate discriminating power**.

Either way `K3_CRITERIA.md` C3's normalization is still `TBD-AT-FREEZE` and must be fixed at freeze.

## D-3. The candidate register may be down to two entries

**The finding.** Verified against the vendored sources behind a SHA256 gate: Cooper's sporadic
solutions number **exactly three** — s7, s10, s18 — and **"S22" occurs zero times in the full text
of both vendored papers**. So `K3_CRITERIA.md`'s **K-S22 has no citable defining recurrence**.
**K-t103** is separately off the roadmap — quoted exactly, *"vetoed by T0 2026-07-26 **pending
certificates**"* — a conditional veto that cannot lift without a recurrence either.

The register's own rule: *"a candidate without a citable defining recurrence at freeze time is
dropped, not guessed."* Under it the register's effective content is **s7 and s10**.

**What T0 is asked.** `K3_CRITERIA.md` gates the freeze and C3b gates `PREDICTION.md`'s S3-00 input,
so four-entries-to-two is a structural change to a freeze-blocking document, not bookkeeping. Rule
on what a two-entry register means for the freeze — and, given D-2, whether a freeze built around
C3/C3b is still the right instrument. (Stream 2 is separately asked to recover S22's recurrence or
confirm the drop. Cooper's primary paper is unfetched — Springer paywall — so neither repo can rule
on what *that* paper contains.)

## D-4. Ledger item 1 — the `L₃ = Sym²(L₂)` notation collision

Item 1 licenses that string as Tier A fact. What is kernel-proven under it is the **lattice** bridge
(`sym2` a 3×3 integer matrix, `G0` the discriminant form, the SL(2) → SO(2,1) lift with exponents
1, 2, 3) — candidate-independent, and correct as written. `K3_CRITERIA.md` C3 uses the **identical
string** for the **operator** identity. A reader moving from CLAUDE.md to C3 can license Tier A for
a per-candidate claim on the strength of a lattice theorem.

The mathematics is fine — Stream 2 has shown the operator identity is proved in Stream 1's Lean
under other names. **The hazard is purely in the wording**, and the fix is T0's: disambiguate the
two statements in the ledger. Stream 1 is separately asked which Lean name C3 route 2 should cite.

## D-5. Ledger item 3's U1 line is stale

Item 3 records *"The open geometric item is U1 (is T ≅ U⊕⟨14⟩?)"*. **U1 was closed Tier B on
2026-07-27** — Stream 2 executed it fresh-context, the T1 coordinator re-ran the pipeline and all
controls, and an explicit det-1 integral base change realizing U ⊕ ⟨14⟩ was exhibited (s10:
U ⊕ ⟨20⟩, DRAFT).

The ledger's own rule is that a document contradicting it carries a dated correction note; here the
contradiction runs the other way and the **ledger line is the stale one**. A wording fix is T0's.

**The evidence that this matters:** the stale line propagated into a filed Stream 3 brief on
2026-09-21 — ours — and had to be corrected in-band. It will keep doing that until it is fixed.

---

## What is not being asked

- **No empirical decision.** WP-E6-SWEEP stays blocked on C1–C5 (`REAL_DATA_RULING_PIN = None`);
  that is a separate, earlier request (`T0_DECISION_REQUEST_SWEEP_THEORY_CORRECTIONS_2026_09_17.md`)
  and none of the above touches it.
- **No physical reading.** No (m, f) prior, m_φ, α_D or Λ_D follows from any CM row or any lattice
  fact: that map is Tier C, BLOCKED under F5b, and the tadpole is unposable without B₃. The sweep
  stays an exclusion instrument and its outputs stay exclusion/FIT, never TEST.
- **No adoption of the "modular rail" reading.** Stream 3 and Stream 2 reviewed that text
  independently and agree on two points: "the universe evolves along this rail" is Tier C and
  unsupported — no dynamics on the moduli curve is defined anywhere in the program — and "this
  explains exactly why reverse-to-zero could not reach zero parameters" is not established; that
  loop is in neither repo here, and the claim identifies the leftover parameter with the modular
  coordinate, which nothing computes. The two *correct* points in that text — that fixing T gives a
  family over X₀(N)⁺ rather than a point, and that N is the modular level and not a flux — are
  already the audit §4.1 and ledger item 4 respectively.

---
*Generated-by: Claude Opus 5 (Stream 3, 2026-09-21) | Verified-by: D-1 re-ran Stream 2's controls
(46/46, 35/35) on this side; D-2/D-3 rest on a SHA256-gated parse of the vendored source with four
mutation-checked controls; D-5 read against the K3-DarkMatter U1 records directly |
Reviewed-by: pending T0*
