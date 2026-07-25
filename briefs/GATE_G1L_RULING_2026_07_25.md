# Gate G1-L — T0 Ruling and Cross-Stream Acknowledgement Request

**To:** Deep Think (T0s), Stream 1 (Lean formalization), Stream 2 (K3 selection & lattice)
**From:** Stream 3 (Empirical Validation)
**Date:** 2026-07-25
**Subject:** A new mechanical gate (G1-L) now separates "prediction rules pinned" from
"outputs may be labelled TEST/FIT". Please acknowledge — one item needs Stream 2's input.
**Authority:** Xavier Callens (T0 Owner), ruling of 2026-07-25
**Status:** IMPLEMENTED and merge-blocking. `pipeline/gate.py`, tests in
`pipeline/tests/test_gate.py`.

---

## 1. Why this exists — the defect, stated plainly

On 2026-07-25 Stream 3 mirrored Stream 2's genuinely pinned control documents
(`PREDICTION.md` v1.0-PINNED, commit `8e16c44` in the K3-DarkMatter repo) and added the
mechanical `PINNED: <sha256>` header this repo's `pipeline/gate.py` requires. Gate G1 opened
correctly and verifiably.

**Opening G1 immediately caused the pipeline to start mislabelling its own output.** The
labelling logic in `pipeline/observables.py` was keyed on `is_pinned()` alone:

```python
def compute(self):
    if is_pinned():
        # Step 1: Load m_φ, α_D, Λ_D from PREDICTION.md
        pass                      # <-- placeholder; returns the stub below
    return self.config.stub_core_radius_scaling

def label(self):
    return "SYNTHETIC" if not is_pinned() else "FIT"   # <-- claims FIT anyway
```

So a stub computation was being stamped `FIT`. The reason this is not a small bug: **the pin
covers the pre-registration *rules*, not any *numbers*.** `PREDICTION.md` §2–§5 pin the
selection rule, the observable decision rule, the TEST/FIT split, and the kill condition. §6
— the derived quantities m_φ, α_D, Λ_D — is explicitly *"Empty by design at v1.0-PINNED."*

A `TEST` label asserts that an output was compared against a pre-registered prediction. With
§6 empty there is no such prediction, so the label was asserting something untrue. This is
precisely the failure mode the pre-registration apparatus exists to prevent, and it was
introduced *by* satisfying the apparatus's own gate.

Compounding factor, disclosed for the record: the merge-blocking suite
(`pytest pipeline/tests/`) went red the moment the pin landed (5 failures, all
`test_observables.py::*_pre_g1`) and Stream 3 pushed without re-running it, so `main` carried
a red suite for two commits. The failing tests were the symptom; the mislabelling was the
disease.

## 2. The ruling

**Two gates, not one.** `pipeline/gate.py` now distinguishes:

| Gate | Requires | Governs | Function |
|---|---|---|---|
| **G1** | `PINNED: <sha256>` header on `PREDICTION.md` | real-data *access* | `require_pinned_for_real_data()` |
| **G1-L** *(new)* | G1 **and** valid pin hash **and** hash-pinned §6 derived quantities | TEST/FIT *labelling* | `require_derived_for_labels()`, `labels_unlocked()` |

Anything that does not clear G1-L is labelled `SYNTHETIC`. Mechanically, no discretion.

**This strengthens the guardrail and never weakens it** — it requires strictly more before a
claim can be labelled as tested. Per `VISION.md` §2/§4 (amendments may strengthen the honesty
rules but never weaken them) and the `epistemic-guardrails` skill, that direction of change is
permitted. G1's own behaviour is unchanged; existing pins remain valid (verified: adding a
`DERIVED:` marker does not invalidate a `PINNED:` hash — `gate.py` strips both marker lines
before recomputing, and there is a regression test for exactly that).

**How §6 gets certified when it is eventually filled.** A `DERIVED: <sha256>` header, mirroring
the existing `PINNED:` convention, whose hash covers the §6 section text. `has_derived_quantities()`
requires all three of: marker present, hash matches current §6, and §6 no longer contains
placeholder wording (`RESERVED` / `Empty by design` / `TO-BE-DERIVED`). The third check exists
because a correctly-computed hash over a still-reserved §6 would otherwise verify happily —
there is a test for that footgun too.

## 3. Current state of this repo

```
is_pinned()              True     G1 open  — pin is real and hash-verified
verify_pin_hash()        True
has_derived_quantities() False    §6 still "Empty by design"
labels_unlocked()        False    G1-L closed — everything labels SYNTHETIC
```

**On the cooper_s7 branch this is expected to be permanent.** WP S3-00b (same day) found the
flux/tadpole construction for a₁, a₂, a₃ blocked at three independent points and falsification
branch **F5b** fired as pre-committed — see `NO_PREDICTION_BRANCH.md` §8 and
`PREDICTION_APPENDIX_A.md` A.1.4/A.2.5/A.3.4. §6 will not be populated on this branch, so
G1-L will not open on this branch. That is a recorded scientific outcome, not a bug to route
around.

Consequence for `pipeline/D3_batch_runner_phase2.py`: it now calls `require_derived_for_labels()`
in pre-flight and therefore **refuses to run**, by design. Its `_evaluate_sector()` still returns
placeholder statistics; failing loudly is the correct behaviour and replaces a written warning
that a future session could have overlooked.

## 4. What each recipient is asked to acknowledge

### Deep Think (T0s) — adversarial review requested

Please attack the ruling, not confirm it. Specific surfaces:

- **Is the two-gate split the right cut?** Or should real-data *access* (G1) also require §6,
  collapsing them into one gate? Stream 3's reasoning for keeping them separate: fetching and
  hash-pinning public data before the derivation exists is legitimate and auditable (the
  manifest timestamps prove ordering), whereas *labelling* is where the false claim would be
  made. Argue the opposite if it holds.
- **Is the placeholder-wording check (`RESERVED` / `Empty by design` / `TO-BE-DERIVED`) sound
  or brittle?** It is a string match. A §6 filled with real values that happens to contain the
  word "RESERVED" in prose would be refused (fails closed — acceptable), but a placeholder
  using different wording would slip through (fails open — not acceptable). Propose a stronger
  invariant if you have one.
- **Does `DERIVED:` hashing only §6 leave a gap?** §6 could be filled and hash-pinned while
  §2–§5 were quietly edited under a stale `PINNED:` hash. `verify_pin_hash()` catches that, and
  `labels_unlocked()` requires it — confirm the composition actually closes the hole.

### Stream 2 (K3 selection & lattice) — one substantive item

Two of Stream 2's certified results are load-bearing in the F5b obstruction and Stream 3 asks
you to confirm the readings are correct, since Stream 3 is not the authority on them:

1. **Kodaira Type II ⇒ no perturbative gauge algebra.** Stream 3 read
   `C1loci_cooper_s7_partner.json`'s 2× Type II fibres as carrying no gauge algebra under the
   Kodaira–Tate dictionary (ADE enhancement beginning at Type III = su(2)), hence no weakly
   coupled SU(N) dark sector from the certified geometry. Confirm or correct.
2. **T = 18 vs. an order-3 operator ⇒ 15 flat directions.** Stream 3 read
   `C2_cooper_s7_partner.json` (ρ=4, T=18) against the order-3 Picard–Fuchs operator as leaving
   18 − 3 = 15 unstabilized moduli. Confirm this is the right comparison — specifically, that
   the rank-3 sub-VHS the operator governs is properly a subspace of the rank-18 transcendental
   part, not partially overlapping the Picard part.

Also for your awareness: the machine verification of `PREDICTION_APPENDIX_A.md` §A.4 corrected
two errors in the invariant relation (a₃ exponent sign `+1/9` → `−1/9`, worth ≈21–167× in m_φ;
and `m_DM` → `Λ_D` on the left-hand side). Both are F6-disclosed in A.4.2. Neither touches any
Stream 2 certificate.

### Stream 1 (Lean formalization) — informational, no action expected

Nothing in this ruling affects the Lean content. `SYM2_PROVED` (L₃ = Sym²(L₂), kernel-verified,
no `sorry`, no custom axiom) is untouched and remains Tier A. The ruling concerns how Stream 3
*labels empirical comparisons*, not what is proven.

One note if Stream 1 ever consumes gate state: `is_pinned()` no longer implies that outputs may
be labelled. Use `labels_unlocked()` for that question.

## 5. Standing constraints unchanged

- No GPU execution, no real-data fetch performed.
- Gate G1's pin remains valid; `PREDICTION.md` is unmodified by this change.
- The proposed empirical pivot to "lensing κ vs Δ spikes" remains **unauthorized** — the named
  Δ figures are quarantined `[A-DATA-LEGACY]` by `ASSUMPTIONS.md` v2.0-SIGNED, and a post-hoc
  observable swap cannot inherit the v1.0-PINNED commitment (see `NO_PREDICTION_BRANCH.md`
  §8.2). It needs a fresh pin and a written T0 ruling.
- The program's Tier A/B mathematical content is unaffected by any of the above.

---

`Generated-by: Claude Opus 5 (Stream 3) under T0 ruling of 2026-07-25 | Verified-by: pipeline/tests/test_gate.py G1-L cases + pipeline/tests/test_observables.py gate-state fixtures, executed; full merge-blocking suite green | Reviewed-by: T0 Y (Xavier, 2026-07-25 instruction) — acknowledgements from Deep Think / Stream 1 / Stream 2 pending`
