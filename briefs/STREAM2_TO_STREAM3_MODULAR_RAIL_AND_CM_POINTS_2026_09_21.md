> **Delivered copy (untracked) — source of truth: Stream 2 repo `SocrateAI-Scientific-Agora-K3-DarkMatter`, `briefs/STREAM2_TO_STREAM3_MODULAR_RAIL_AND_CM_POINTS_2026_09_21.md`, main @ af04382, release v0.3.9. Dropped here by the Stream 2 session on 2026-09-21; not committed — the owning session decides whether to commit it.**

# Stream 2 → Stream 3 — the "modular rail" text (transmitted with review), and what is now computed on that curve

**Date:** 2026-09-21 · **From:** Stream 2 · **To:** Stream 3, T0 · **At T0's request** (Xavier
asked that Stream 3 be informed of the text in §1).
**Status:** information + review. No gate moved, no pinned document touched, nothing scored.
Companion to `briefs/STREAM2_TO_STREAM3_C3_BRANCH_REPLY_2026_09_21.md` (the C3 answer you asked for).

## 1. The text, as received (external, Deep Think; recorded in substance)

Title: *"L'Expérience de Pensée : Le Rail Modulaire"*. It is a follow-up to the "Crible de K3"
directive that Stream 2 returned on 2026-09-20
(`briefs/REVIEW_DEEPTHINK_K3_SIEVE_PROPOSAL_2026_09_20.md`), and it concedes that review's two
main points:

1. *"L'illusion du point rigide"* — believing that the integer isometry on U⊕⟨2N⟩ pins a unique
   K3 "confuses a necessary with a sufficient condition"; by Dolgachev Thm 7.1, fixing the
   transcendental lattice defines a one-parameter family, the modular curve X₀(N)⁺.
2. *"Le mythe du flux N"* — N is the modular level; identifying it with a tadpole flux without a
   base B₃ is an error.

It then adds a physical reading: the universe "is not a frozen crystal; it keeps a continuous
degree of freedom" and "evolves along this rail (the curve X₀(N)⁺)", along which the Fricke
involution stays an exact integer isometry; and this "explains exactly why the reverse-to-zero
loop could not descend to zero parameters".

## 2. Review against the ledger

| statement | status |
|---|---|
| Fixing T ≅ U⊕⟨2N⟩ gives a one-parameter family over X₀(N)⁺, not a point | **Correct.** Dolgachev 1996 Thm 7.1, fetched, read, hash-pinned (`docs/literature/MANIFEST.md`); Tier B for cooper_s7 (`C2_cooper_s7_v5.json`), DRAFT/advisory for cooper_s10. It is what your own audit §4.1 and LeanMaster G9 say. |
| N is the modular level, not a flux | **Correct**, and it is ledger item 4: WP S3-00b is BLOCKED (F5b), the tadpole is not posable without B₃. |
| Fricke acts by an exact integer isometry along the whole curve | **Correct and Tier A** (Stream 1 `swap_isometry`, `swap_is_fricke`, uniform in N) — but it is a property of the lattice, true for every M_N-polarized K3. It carries no information about where on the curve anything sits. |
| "The universe evolves along this rail" | **Tier C, unsupported, not adopted.** No dynamics on the moduli curve is defined anywhere in the program: no potential, no kinetic term, no EFT. VISION §1.3 applies — a geometric relation supplies no physical coupling. Do not cite. |
| "This explains exactly why reverse-to-zero could not reach zero parameters" | **Not established.** reverse-to-zero lives in the DualScaleSimulator repo; its own pre-registration addenda (A6–A9) close "zero-parameter" as *not derivable* on that repo's grounds. A one-dimensional moduli space is *compatible with* a leftover parameter; "explains exactly" asserts an identification of that parameter with the modular coordinate that nothing computes. Post-hoc narrative; treat as a conjecture at most, marked as such. |

**Net for Stream 3:** nothing in this text changes your audit's conclusions. The sweep stays
candidate-blind (§1 of your audit), F5b stands, and no (m, f) prior follows from "the rail".
Please do not import "evolves along the curve" wording into any Stream 3 document.

## 3. What Stream 2 has now actually computed on that curve (new today, Tier B)

Your audit §4.2 identified the ρ = 20 cut as the fork that turns selection into a finite
classification. We computed what that cut picks out **inside** the two register families. The
cut itself remains **not adopted** — it is the open T0 decision you named.

`checkers/check_CM_points_rho20.py` (46 controls), `checkers/check_A2_membership.py` (35 controls);
certificates `CM_POINTS_RHO20.json`, `A2_MEMBERSHIP.json`; each built by one agent and re-derived
by an independent verifier on a separate code path. Records:
`briefs/STREAM2_CM_POINTS_RHO20_2026_09_21.md`, `briefs/STREAM2_A2_MEMBERSHIP_2026_09_21.md`.

**3.1 All three singular points of the s7 operator are ρ = 20 (CM) points of the family.**

| z | vector v ∈ U⊕⟨14⟩ | −v² | T_X = v^⊥ (reduced) | D | what it is on the modular curve |
|---|---|---|---|---|---|
| 1/27 | (1, −1, 0) | 2 | (1, 0, 7) | −28 | Fricke fixed point, order-2 elliptic |
| −1 | (2, −4, 1) | 2 | (1, 1, 2) | −7 | second order-2 elliptic point (t = −1/7) |
| ∞ | (14, −14, ∓5) | 42 | (1, 1, 1) = A₂ | −3 | order-3 elliptic point (L₃ exponents 2/3, 1, 4/3) |

The first two rows were a prediction recorded before computing and are consistent with
Stream 1's `s7_singular_points_are_selfdual`. The third was **not** anticipated. This sharpens
ledger item 3 rather than contradicting it: the loci are elliptic points of X₀(7)⁺, *and* the
family members over them carry rank-2 transcendental lattices. It is not a Kodaira reading and
none is made. Tier statement: lattice arithmetic exact; z-values are numeric recognitions
(fit at 120 digits, re-checked at 200) through a Hauptmodul relation certified PASS(40); the step
"v·ω = 0 ⇒ ρ = 20, T_X = v^⊥" is the cited Dolgachev framework, not proved here.

**3.2 The A₂ surface — LeanMaster's minimal ρ = 20 case, your §4.2 — is in the s7 family and not
in the s10 family.** For n = 10 the negative covers *all* vectors, not a bounded search: a
discriminant D occurs iff D is a square mod 4n, and −3 ≡ 37 is not a square mod 40. For n = 7,
−3 ≡ 25 = 5² mod 28. (s10 side advisory: its lattice certificate is DRAFT by T0 ruling.)
Admitted discriminants with |D| ≤ 100: 27 for n = 7, 22 for n = 10, 10 in common.

**3.3 What this is not.** Not a selection: the ρ = 20 cut is unadopted, nothing is ranked. Not
independent corroboration of LeanMaster's route: by Shioda–Inose the binary-form side and the
modular side are the same computation (LeanMaster G10), so their agreement is forced. Not
complete: the enumeration window is not shown to be a fundamental domain, and 8 s10 rows at
D = −800 exceed the recognition cap. No physical reading of any kind.

## 4. The s7 / s10 results, side by side, and how Stream 3 can use them

| | cooper_s7 | cooper_s10 |
|---|---|---|
| lattice (T2) | T ≅ U⊕⟨14⟩, **LIVE** (`C2_cooper_s7_v5.json`), Tier B | U⊕⟨20⟩, **DRAFT** (T0 D6′) — every s10 row below is ADVISORY |
| modular coordinate (T1) | Hauptmodul of Γ₀(7)⁺, `1/z = 49t + 13 + 1/t`, PASS(40) | Hauptmodul of Γ₀(10)\*, `1/z = 16t + 8 + 1/t`, PASS(40) |
| T3 (lattice n = modular level) | AGREE(n = 7), no open flag | AGREE(n = 10); open: `LATTICE_CERT_DRAFT`, `ATKIN_LEHNER_ACTION_UNVERIFIED` |
| C3 (Sym² operator identity) | branch (i): holds; partner A279619 **integral** (Stream 1, axiom-free) | branch (i): holds; partner **dyadic, non-integral** — whether C3 needs integrality is a T0 question |
| ρ = 20 points at the singular loci | z = 1/27 (D −28), z = −1 (D −7), z = ∞ (D −3, **A₂**) | z = 1/16 (D −40), z = −1/4 (D −20), z = ∞ (D −4) |
| A₂ (D = −3) in the family? | **yes**, at z = ∞ | **no**, for all vectors (−3 not a square mod 40) |
| other rational CM z in the window | 1/2 (−12), −1/8 (−35), −1/64 (−91), 1/125 (−112) | 1 (−15), −1/2 (−16), 1/4 (−24), −1/9 (−60), −1/20 (−100), 1/36 (−120), 1/196 (−280) |
| distinct z found / unrecognised | 71 / 0 | 69 / 8 (all at D = −800, beyond the degree cap) |

**4.1 How to read the certificates (machine use).** `data/certificates/CM_POINTS_RHO20.json`:
`families.<candidate>.rows[]`, each with `v`, `minus_v2`, `div_v`, `tau` (exact), `T_X_reduced_form_abc`,
`D`, `z_recognised`, `z_value_if_rational` / `z_minpoly`, `singular_locus_match`, and per-row `flags` /
`advisory`. **Honor `advisory: true`** — it is set on every s10 row. `locus_hits` (a dict keyed by locus: "-1", "1/27", "infinity") holds the rows
landing on singular loci. `A2_MEMBERSHIP.json`: `families.<candidate>` carries the verdict and the
**clause that fired**; `discriminants_admitted_summary` is the |D| ≤ 100 table. Both certificates
carry `inputs.sha256` (pin them if you mirror) and `not_claimed` (mirror it with the data, not
without). Re-verify on your side before citing (producer ≠ verifier, your ruling A1 pattern):

```bash
python3 checkers/test_CM_points_rho20_controls.py     # 46 controls, ~30 s
python3 checkers/test_A2_membership_controls.py       # 35 controls, ~15 s
python3 checkers/check_A2_membership.py               # ~30 s; exact congruence leg + box leg
python3 checkers/check_CM_points_rho20.py             # ~2.5 min; full table
```

**4.2 What Stream 3 CAN do with this now.**
1. **Correct your audit's §3 table and close its branch (iii).** Branch (i) holds for both
   primaries (companion brief). Your s7 row's "no integral order-2 partner exists" refers to the
   bijection-implied sequence, a different object from the series-square-root partner A279619,
   which is integral. Your s10 figure (u₂ = 3/4) is right for the object you computed.
2. **Update DR-4's standing ask.** "Produce C1/C3/C3b for s7": C1 (mirror integrality, PASS(60)),
   C3b (`SYM2_OPERATOR_IDENTITY_PROVEN`), T1, T2, T3 now all exist for s7. For s10: same, minus a
   LIVE T2.
3. **Use the discriminant criterion as a candidate-dependent *label*, the first one you have.**
   Your audit §1 showed the sweep is bit-identical across candidates. `D is a square mod 4n` is an
   exact, cheap, candidate-dependent predicate; if T0 adopts the ρ = 20 cut, the pre-registration
   vocabulary for a PREDICTION v2 amendment becomes a finite list of `(candidate, D, z)` labels
   instead of a continuum. That is bookkeeping for hypotheses, not an observable.
4. **Wire a consistency smoke test**, as you did for the C3 applicability script: assert that the
   mirrored certificate's s7 `locus_hits` reproduce the ledger's loci {−1, 1/27} and that every
   s10 row is advisory. It fails closed if either repo drifts.

**4.3 What Stream 3 still CANNOT do with this.**
- **No (m, f) prior, no m_φ, no α_D, no Λ_D** from any row. There is no map from a point of the
  modular curve — CM or not — to an exact observable: that map is Tier C, BLOCKED under F5b, and
  the tadpole is unposable without B₃ (ledger item 4). WP-E6-SWEEP stays an exclusion
  instrument; its outputs stay exclusion/FIT, never TEST (ledger item 5).
- **No ranking of s7 over s10** from "A₂ is in s7". A minimum-|D| rule has no warrant in this
  program; LeanMaster's own scope note says no observable follows from it.
- **No completeness claim.** The window is not a fundamental domain; absence from the table is
  not absence from the family. Only the A₂/n = 10 negative and the discriminant criterion are
  all-vector statements.
- **No Kodaira language** for the loci (ledger item 3). "Elliptic point carrying a ρ = 20 member"
  is the supported phrase.

## 5. For T0, carried forward from your audit

Your item 1 (the ρ = 20 fork) can now be decided with the content of the cut in view: if adopted,
it yields, per family, a finite ordered list of named surfaces, and at its minimum (D = −3) it
distinguishes the two register primaries. Whether a minimum-|D| rule has any warrant is a separate
question that Stream 2 does not answer and that no artifact here supports.

---
*Generated-by: Claude (Fable 5.1), Stream 2 | Verified-by: P2/P3 numbers read from the emitted
certificates at code commit f091e43; §2 statuses checked against CLAUDE.md ledger items 3–4,
VISION §1.3, and Stream 1 `MnLattice.lean` statements (read as source, no Lean build run) |
Reviewed-by: N*
