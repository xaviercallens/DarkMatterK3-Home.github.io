# Stream 2 → Streams 1 & 3: U1 CLOSED [Tier B] — coordinator-verified

**Date:** 2026-07-27 · **From:** Stream 2 (fresh-context execution agent) via T1
coordinator · **Verified:** coordinator re-ran the full pipeline + all controls
independently and read the checker source (standing rule 2) before this fan-out.
**Record:** `briefs/STREAM2_U1_EXECUTION_2026_07_27.md` · commit `dfbd2a9` (Stream 2).

## What was derived (computed at runtime, never typed)

The joint monodromy-invariant lattice of the cooper_s7 family: primitive even Gram
[[0,0,−1],[0,14,0],[−1,0,0]], **det = −14**, signature (2,1), disc form ℤ/14 (q = 1/14),
derived 2n = 14, and an **explicit integral base change (det 1) realizing U ⊕ ⟨14⟩** —
a constructive isometry, making the planned Eichler/Cassels genus route unnecessary
(Cassels not fetched; no 2-adic claim made). Controls all pass: the identical pipeline on
cooper_s10 derives det = −20 / U ⊕ ⟨20⟩ (computed-vs-computed discrimination, no
hardcoded targets); three scrambled-matrix modes and a Yukawa-scramble all fail loudly.

## Epistemic status (do not overstate downstream)

**Tier B**, with two named residual links (brief §4): numerical recognition of monodromy
entries (~1e−59 residuals vs 1e−35 gate, then exact structural verification), and the
framework identification of the computed lattice with the transcendental lattice T
(Dolgachev/Doran, read and hash-pinned; invariant overlattices enumerated: none; the
λ-rescaling branch is excluded by the framework shape, not by computation). NOT changed:
ρ = 19 / T = 3 [B] stands as-is; no Kodaira claims (E-007/8/9 stand); no physical
coupling (VISION §1.3); Gate E criterion 1 remains UNRESOLVED (T0 D1);
`C2_cooper_s7_v4_DRAFT.json` is DRAFT — **v3 stays live until T0 accepts**.

## Stream 1 (Lean) — two optional items, no obligation

1. **Independent verification invitation** (the E-011 pattern): the U-splitting claim is
   a finite exact statement — a specific GL₃(ℤ) matrix conjugating the derived Gram to
   U ⊕ ⟨14⟩ — and is mechanically checkable from `data/certificates/C2_cooper_s7_v4_DRAFT.json`.
2. **Formalization candidate:** verifying that base change in Lean (exact integer
   arithmetic) would upgrade the lattice-arithmetic portion of Link 1 toward kernel-checked;
   the numerics→exact recognition step and Link 2 would remain Tier B regardless.
   Standing rule for any golden test: derive the expected Gram from the certificate at
   runtime; never hardcode −14 outside a control.

## Stream 3 — what this does and does not change

- **No empirical consequence today.** PREDICTION.md v1.1 (F5b) untouched; no Gate E
  re-scoring; the WP-E7/WP-E6 track proceeds independently.
- If T0 accepts v4 and re-scopes S3-00 §2(b), a future derivation route would be
  M₇-polarized/modular, not Kodaira-based — any inbound directive still phrased in
  Kodaira terms remains stale (CLAUDE.md ledger).

## T0 decisions now open (Xavier)

1. **Accept `C2_cooper_s7_v4_DRAFT.json` as live v4?** (upgrades H-M7 to [B]).
2. **S3-00 §2(b):** re-scope onto the derived M₇-polarized geometry, or strike.
3. **Phase M:** T0 D2 gated M2 on "Route γ-derived lattice data + T0 reopening against a
   revised M1′". The lattice data now exists (as U1/C2v4-DRAFT rather than the
   pre-E-009 "C1v3/C2v3" wording — T0 to rule whether intent is satisfied). An M1′ draft
   is being prepared to make this decision concrete.
4. (Standing, unchanged:) does v0.4.0 still mean "Gate E PASS"?

---
Generated-by: Fable 5 (T1 coordinator) | Verified-by: independent re-run of
check_U1_lattice.py + test_U1_controls.py + full v0.3.4 regression (all green,
2026-07-27) + source read of both checkers | Reviewed-by: pending T0 (Xavier)
