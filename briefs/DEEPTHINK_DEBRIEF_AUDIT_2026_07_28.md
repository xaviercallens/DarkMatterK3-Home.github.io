# Audit — Deep Think (T0s) Debrief 2026-07-28 (G0 cross-check + G1 adversarial read)

**Inbound:** `DEEPTHINK_DEBRIEF_G0_G1_2026_07_28_VERBATIM.md` (archived verbatim).
**Auditor:** Fable 5 (coordinator), per standing intake protocol: every claim below was
re-derived or checked by hand this session before any verdict; cite this audit's verdicts,
never the inbound directly.
**Headline verdicts:** C1 **VERIFIED-AGREE** (G0 cross-model check now complete, two model
lineages). C2 **CORE VERIFIED with a scope caveat** (strict-pullback obstruction is real;
"ladder fails unconditionally" overreaches — the plan's own twist degree of freedom is
exactly what's untested). C3 **fixes NOT verified** — Enriques suggestion REJECTED as
internally inconsistent; dP₉ carries an uncomputed load-bearing assumption and a direct
tension with C4's own fix. C4 **shortcut plausible with three recorded caveats**. C5/C6
concur with decisions already taken; one recycled wrong rationale re-flagged.

---

## C1. G0 re-derivation (NS ≅ U⊕E8(-1)²⊕⟨-14⟩) — VERIFIED-AGREE

Deep Think's zero-shot route (invariant bookkeeping + Nikulin genus-uniqueness) was checked
step-by-step by the auditor:

- T = U⊕⟨14⟩: rank 3, signature (2,1) ✓. A_T ≅ Z/14, and for L = Ze with e² = 14 the dual
  generator e/14 gives q(e/14) = 14/196 = 1/14 (mod 2Z) ✓.
- Complement invariants in unimodular Λ (rank 22, sig (3,19)): rank 19, sig (1,18),
  q_NS = −q_T on A_NS ≅ Z/14 ✓ (standard Nikulin complement identities).
- Uniqueness: even indefinite, rank 19 ≥ ℓ(A)+2 = 3 → one class in the genus ✓ (the p=2
  refinements of Nikulin's criterion are comfortably satisfied for cyclic Z/14; and the
  in-house derivation independently carries a constructive integral-embedding witness, so
  nothing rests on the uniqueness bound alone).
- Candidate check: rank/signature/disc-form of U⊕E8(-1)²⊕⟨-14⟩ all match ✓.

**Standing achieved:** the G0 certificate has now been derived independently by (i) T1
Sonnet (two in-house routes, bit-identical Gram), (ii) coordinator reproduction + 5-control
suite, and (iii) a genuinely different model lineage (T0s, zero-shot). This is the
strongest cross-verification of any result in the program to date. Deep Think's "cleared to
promote" was already moot — T0 promoted it to LIVE earlier today (`T0_DECISIONS_2026_07_28_STREAM2.md`).
No action required.

## C2. Trap 1 — strict-pullback c₁=0 obstruction — CORE VERIFIED, SCOPE CAVEAT

**Verified by hand:** for a *strict* (untwisted) pullback of the 1-parameter family along
φ: B₂ → P¹_z, the CY condition forces K_{B₂} = −φ*(D) for a divisor class D pulled back
from the curve; any class pulled back along a map to a curve has self-intersection 0
(distinct fibers are disjoint), hence K²_{B₂} = 0 is necessary. The ladder's bases fail it:
K²(P²) = 9, K²(P¹×P¹) = 8, K²(F_n) = 8 — all correct values. **For the untwisted
construction, Trap 1 stands and would kill G1-a on all three current rungs.**

**Scope caveat (why "fails unconditionally" is not yet established):** the canonical plan's
G1-a bullet (`WP_S2G_X4_EXHIBITION_PLAN_2026_07_27.md` §1) never committed to strict
pullback — it explicitly frames the deliverable as finding "the right **twist data** for
the compactified pullback (the K3-fibration analogue of Weierstrass −4K/−6K twisting)."
Trap 1's derivation assumes ℒ = φ*ℒ_curve with no twist — assuming away precisely the
degree of freedom G1-a exists to compute. Whether a twist compatible with the M-polarized
family structure exists on K² ≠ 0 bases is an open computation, not settled either way by
the inbound. **Consequence: Trap 1 upgrades "may constrain or exclude" (plan's wording) to
"provably excludes unless a twist exists" — a real sharpening, not yet a death certificate.**

**Independent computational test in flight:** the T1 G1-a derivation over P² was launched
*before* this inbound arrived and has deliberately **not** been told about Trap 1. If sound,
it must independently hit the K²=0 wall for the untwisted case and/or exhibit the twist
structure. Its result lands as a clean two-model cross-check on C2 — the same discipline
that just closed G0.

## C3. Proposed fixes (dP₉ / Enriques) — NOT VERIFIED; one rejected, one conditional

- **Enriques: REJECTED (internally inconsistent with the inbound's own Trap-1 setup).**
  Strict pullback requires −K_{B₂} = φ*(D) with D of positive degree (the family is
  non-isotrivial — it has genuine singular loci and monodromy — so deg ℒ_curve > 0), i.e.
  −K_{B₂} must be a **nonzero effective** class. On an Enriques surface K is 2-torsion:
  numerically trivial, not effective, and torsion classes cannot equal the pullback of a
  positive-degree divisor. The suggestion fails by the same arithmetic Trap 1 itself uses.
- **dP₉ (rational elliptic surface): CONDITIONAL, two audit-found problems, both open:**
  1. −K_{dP₉} = F (fiber class, primitive when a section exists). Matching
     −K = φ*(D) = deg(D)·(φ-fiber class) forces **deg ℒ_curve = 1** — a number nobody has
     computed for the cooper_s7 family. If deg ℒ_curve ≥ 2, dP₉ is obstructed by the same
     divisibility argument. **This must be computed exactly before the dP₉ rung is trusted.**
  2. With deg 1, φ essentially *is* the elliptic fibration (up to Aut(P¹)) — leaving no
     freedom to impose C4's even-ramification constraint over z = −1, 1/27 (a dP₉ with
     section has no multiple fibers). Index-2 Halphen variants (multiple fibers = built-in
     even ramification, but no section) flip the problem: −K becomes a half-fiber while
     φ-pullbacks land in even multiples — a parity mismatch, sketch-level. **The two fixes,
     as stated, appear to be in tension with each other; neither is certified.**

  These are audit-level analyses (exact in the steps shown, but not machine-checked) —
  recorded as open questions **O1** (deg ℒ_curve = ?), **O2** (dP₉-section vs
  even-ramification incompatibility), **O3** (Halphen parity) for the G1-a exact derivation
  to settle.

## C4. Trap 2 — even-ramification shortcut — PLAUSIBLE, three caveats

The core mechanism is standard and correct in principle: base change locally of the form
t² = z squares the local monodromy; an involution squares to the identity, neutralizing the
Z/2 quotient structure transverse to φ⁻¹({−1, 1/27}). As a *design constraint* it is
attractive and is hereby recorded as a candidate global strategy for G1-b. Caveats that
block "resolution trivial or unnecessary" as stated: (a) a ramified base change introduces
its own singular locus along the ramification curve — the total space still needs
normalization/local analysis there, just of a milder kind; (b) the ∞-type boundary points
(third degeneration type in the plan, with genuinely infinite-order monodromy) are untouched
by this trick and remain the honest hard case; (c) the constraint interacts with C3's base
arithmetic (O2/O3 above).

## C5. WP-E7 concurrence — decision AGREE, rationale partly REJECTED (again)

Deep Think concurs with the LRGpCMASS choice (already executed and ratified). It repeats
the "artificially inflates shot-noise" argument that this program **already corrected** in
`T0_DECISIONS_2026_07_28_PENDING_ITEMS.md` D3: the two catalogs' surface densities are
comparable (≈39.8 vs ≈41.2 /deg²), so per-mode shot noise is roughly unchanged — the real
gains are doubled solid angle (sample variance) and doubled total counts. The corrected
rationale stands; the inbound's phrasing is not to be adopted into any document.

## C6. Paper scope concurrence — no action

Consistent with decisions already taken (D2.1–D2.5). Noted for the record.

---

## Disposition (what actually changes)

1. **G0**: cross-model verification recorded as complete (C1). S2 decision log updated.
2. **G1 ladder: NOT amended yet.** Deep Think's "final clearance only after altering the
   ladder" is T0s *advice*; gate and plan changes are T0's to rule, and the audit shows the
   proposed replacement ladder is itself unverified (C3). **Recommended sequence:** let the
   in-flight, uncontaminated G1-a derivation land → compare against C2 → put a
   ladder-amendment decision request to T0 with O1–O3 answered or explicitly open.
3. **C4's even-ramification constraint**: recorded as a candidate G1-b design element,
   pending the same T0 decision.
4. Nothing in this inbound touches Stream 3; the S3 firewall holds.

---
Generated-by: Fable 5 (coordinator) | Verified-by: every C1/C2 step re-derived by hand this
session; C3 counter-arguments derived in-audit (labeled sketch where not exact); plan
wording checked against WP_S2G_X4_EXHIBITION_PLAN_2026_07_27.md verbatim | Reviewed-by: T0 N (submitted for T0 review; disposition §2 needs a T0 ruling)
