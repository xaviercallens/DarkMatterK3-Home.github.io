# WP_A2_CIRCULARITY_AUDIT.md — Gate 0 of the Laboratory-Scale Re-Scope: FAIL

**Work package:** WP-A2 (authorized by `briefs/T0_ADJUDICATION_WPA_2026_07_25.md` R6.2)
**Agent:** Fable 5 (T0-DELEGATED)
**Date:** 2026-07-25
**Machine verification:** `scripts/verify_wpa2_circularity.py` — executed 2026-07-25,
assertions green; the verdict below is printed by the script, not asserted in prose.
**Honest outcome up front:** **FAIL.** No region of the B1 window is simultaneously
(i) non-circular and (ii) reachable by any published public dataset at gravitational
strength. Per R6.2, the terminus is **Off-Ramp 3** — recorded in
`NO_PREDICTION_BRANCH.md` §8.5. This closes the empirical program for the current
hypothesis; a clean negative, reported with the same prominence as a positive.

---

## 1. What was audited

The adjudication left exactly one scale-coherent observable class: short-range
fifth-force / inverse-square-law (ISL) public data, where a scalar in B1's window
(range ~8.8 nm–30 μm) physically acts. Gate 0 asks: **is there any part of that window
a public dataset could falsify without circularity?**

## 2. Inputs (all fetch-verified 2026-07-25, or reproduced from executed scripts)

| Tag | Content | Source |
|---|---|---|
| [B1-num] | λ-form route m_KK ∈ [0.0224, 22.4] eV (cosmological); size-form route l ∈ [1, 30] μm | `scripts/verify_swampland_bounds.py` (executed); arXiv:2205.12293; arXiv:2309.09330 |
| [LAB-ISL] | Gravitational-strength (\|α\|=1) Yukawa excluded at 95% CL **only for ranges ≥ 38.6 μm**; data at separations 52 μm–3.0 mm | arXiv:2002.11761 (Lee–Adelberger et al.), abstract, fetch-verified |
| [LAB-CAS] | α ≲ 10¹² at λ ~ 200 nm (isoelectronic/Casimir regime) — short-range public limits ~12 decades above gravitational strength | arXiv:hep-ph/0502025 (Decca et al.), abstract, fetch-verified |

Fetch-discipline note (F6 spirit): two candidate arXiv IDs recalled from memory for the
short-range citation resolved to unrelated papers (an information-theory paper and the
MEG μ→eγ search) and were discarded; the [LAB-CAS] citation above was located by arXiv
API search and abstract-verified. This is why the no-numbers-from-memory rule exists.

## 3. The three audit steps (machine-checked)

1. **Size-form route is circular.** Its window [1, 30] μm *is* the interval its source
   assembled from laboratory and astrophysical bounds. Testing it against those same
   bounds tests the inputs against themselves. **Excluded as a TEST target.**
2. **λ-form route (non-circular) is out of reach.** Its entire window maps to force
   ranges [8.8 nm, 8.81 μm] — wholly below the 38.6 μm gravitational-strength exclusion
   reach of the best published ISL data. No public dataset excludes any of it.
3. **The short-range regime has no gravitational-strength sensitivity.** At sub-micron
   ranges, the strongest public limits allow α up to ~10¹²; a KK-graviton-tower signal
   (gravitational strength by construction of the scenario, Tier C [A-DD]) sits ~12
   decades below sensitivity.

## 4. Verdict and why it is final for this scope

**FAIL.** A pre-registered comparison against any existing public dataset would be
guaranteed-consistent by construction — the mirror image of the guaranteed-pass FIT that
gap G-1 blocked at cosmological scales. Both failure modes manufacture agreement; both
are forbidden. Combined with G-1-CLOSED-NEGATIVE (no Mpc-scale test in principle), the
B1/B3 window is untestable at **every** scale with data that exists today:

| Scale | Status | Blocker |
|---|---|---|
| Mpc (κ-peaks, Δ spikes, Betti) | Dead in principle under [A-DD] | G-1-CLOSED-NEGATIVE (adjudication R3) |
| 8.8–38.6 μm | Circular | Window region derived *from* the testing data (this audit, step 1) |
| < 8.8 μm | Unreachable | Public α~1 sensitivity absent (this audit, steps 2–3) |

## 5. Honest residue — a monitoring trigger, not a test

The scenario is not unfalsifiable *forever*: a future public ISL release excluding
gravitational-strength Yukawa interactions at ranges below 38.6 μm would begin to bite
into the non-circular window's low-mass end, and reach below 8.81 μm would exclude its
lower edge outright. Recorded as **monitoring trigger F-LAB** (a documented condition
for *future re-evaluation*, explicitly not a pre-registered TEST — there is no data to
compare today): *if a future public ISL dataset excludes \|α\|=1 for λ < 38.6 μm, WP-A2
Gate 0 must be re-run against it before any other use.*

## 6. What "experimentation" remains in scope

- **Synthetic-only pipeline infrastructure** (G1 scope): the WP-E observables (κ-peak,
  exact Betti), closure/null tests (135 passing), gate logic, pin tooling. All remain
  valid engineering for any future, differently-anchored hypothesis.
- **Nothing else.** No fetch of comparison data, no TEST/FIT labels, no v2.0 pin.

---

`Generated-by: Fable 5 (T0-DELEGATED) WP-A2 Gate 0, 2026-07-25 | Verified-by: scripts/verify_wpa2_circularity.py executed (assertions green); citations arXiv:2002.11761 + hep-ph/0502025 abstract-fetch-verified same day; window edges reproduced from scripts/verify_swampland_bounds.py | Reviewed-by: T0 Y (delegated); Deep Think (T0s) concurrence invited, non-blocking (negative result); Xavier countermand window open`
