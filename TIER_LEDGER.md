# TIER_LEDGER.md — Epistemic-Tier Rulings and Ruling Requests

Per the `epistemic-guardrails` skill: claims of uncertain tier get an entry here
with status `RULING-REQUESTED` rather than a guessed tier; rulings and their
resolutions are recorded permanently. Append-only.

---

## TL-001 — Operator order of the certified s₁₀ recurrence (L₂ vs L₃)

- **Status:** `RESOLVED` (2026-07-17) — Tier A, machine-checked + literature-matched.
- **Question as originally flagged** (T1 session, 2026-07-17, pre-`refs/`): the
  docstring of `cooper_s10_kernel.py` calls its certified recurrence "the order-3
  Picard-Fuchs operator," but the flagging session claimed that a 3-term (order-2
  shift) recurrence corresponds to an order-2 ODE, making the certified object a
  candidate L₂ rather than the K3-side L₃, and blocking C1/C3 checker design until
  ruled.
- **Resolution: the flag's premise was wrong.** The ODE order corresponds to the
  *degree of the recurrence's polynomial coefficients* (under the θ = z d/dz
  correspondence), not to the number of terms in the recurrence. Two independent
  confirmations, neither from model memory:
  1. **Machine check (exact arithmetic, this repo):** the operator
     `L = θ³ − z·P1(θ−1) − z²·P0(θ)`, constructed mechanically from the certified
     A005260 recurrence `(n+2)³a(n+2) = P1(n)a(n+1) + P0(n)a(n)` (cubic P1, P0),
     annihilates F(z) = Σ a(n)zⁿ exactly — verified coefficient-by-coefficient for
     all m = 0..199 including the nontrivial m=1 boundary cancellation
     (1³·a(1) − P1(−1)·a(0) = 2 − 2 = 0). Leading term θ³: **order 3**.
  2. **Literature (fetched, `refs/`):** Gorodetsky, arXiv:2102.11839v2, §1 — the
     Apéry sequence's 3-term recurrence with cubic coefficients (eq. 1.2)
     corresponds to the *third-order* equation (1.3), explicitly identified there
     as "a symmetric square of a Picard-Fuchs equation," while the 3-term
     recurrence with quadratic coefficients corresponds to the second-order
     equation (1.4). Same structural pattern as s₁₀.
- **Consequence for checker design:** `cooper_s10_kernel.py`'s docstring is
  consistent with the literature pattern — the certified recurrence's operator is
  the order-3 L₃-side object. C1 (mirror-map integrality) targets this order-3
  operator; C3's job remains exhibiting an explicit order-2 L₂ with
  L₃ = Sym²(L₂) — the L₂ is the thing *not yet in hand*, which is what the C3
  checker must construct/verify per candidate, exactly as `K3_CRITERIA.md` §C3
  already states.
- **Method note (honesty record):** the first machine-check attempt FAILED because
  the checking code itself mis-indexed the θ-operator coefficients — the failure
  was caught precisely because the check was run rather than the conclusion
  asserted. The corrected derivation is recorded above and in this session's
  history. This is the P2 practice ("tests are scientific, not smoke") working as
  intended.

---

`Generated-by: Fable-tier session, 2026-07-17 | Verified-by: exact 200-coefficient annihilation check (in-session, reproducible from the entry above) + fetched Gorodetsky arXiv:2102.11839v2 §1 | Reviewed-by: pending Xavier`
