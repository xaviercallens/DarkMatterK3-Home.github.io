# Hypothesis Foundry Update: Corrected Classification and Experimental Comparison

**Source**: SocrateAI-Scientific-Agora-K3-DarkMatter, Part VIII (2026-07-14)

## Motivation: A Corrective Update to the K3 Substrate

The companion project released on 2026-07-14 a corrective analysis, **Part VIII: The Hypothesis Foundry**, that formally **rejects** the legacy S12 candidate (OEIS A112019) — previously treated as a validated K3 surface — and promotes three new GATE-C finalists as the correct K3-type geometric substrates:

- **t103** (OEIS A276536): T103(n) = Σ_k C(n,k) C(2k,k)³ — novel in-session discovery
- **Cooper s7** (OEIS A183204): Σ_j C(n,j)² C(2j,n) C(j+n,j) — Cooper (2012), level-7 sporadic
- **Cooper s10** (OEIS A005260): Σ_k C(n,k)⁴ — Cooper (2012), level-10 sporadic

This section reports an **independent**, exact-arithmetic re-verification of the key Part VIII claims performed in this repository (`hypothesis_comparison_t103_cooper.py`), and cross-references the resulting corrected candidate landscape against the real Euclid Q1 / SDSS BOSS DR17 observational data.

## Negative and Corrective Findings (Reported First)

1. The discriminant between elliptic-type (ODE order 2) and K3-type (ODE order 3) geometry is the *minimal generating-function ODE order*, not the shift-recurrence order used in an earlier (v1) classifier. The v1 classifier was inverted relative to this discriminant.

2. S12 (A112019) — the flagship candidate of the original Lean 4 proofs — is **formally rejected** as K3-type on two independent grounds: its minimal Picard-Fuchs operator has ODE order 2 (elliptic), and its mirror map on that minimal operator is non-integral (q2 = 81/8).

3. Physics-viability gates (G2: GD-1 heating, M87* superradiance, PTA/Lyman-α) are **non-discriminating** across the 13-candidate pool at any common (τ, 𝒱) normalization, because single-instanton domination of the mirror-map series makes the achievable axion mass identical across candidates. Candidate selection therefore rests on the mathematical gates (G1), not the physics gates.

## Independent Exact-Arithmetic Re-Verification

To avoid taking the Part VIII claims on trust alone, this repository independently re-derives and verifies two of its central mathematical claims using Python's arbitrary-precision integers and exact `Fraction` arithmetic (no floating point in any recurrence-fitting step):

```python
def t103(n_max):
    """OEIS A276536: T103(n) = sum_k C(n,k) * C(2k,k)^3."""
    seq = []
    for n in range(n_max + 1):
        total = sum(C(n, k) * C(2*k, k)**3 for k in range(n + 1))
        seq.append(total)
    return seq

def cooper_s10(n_max):
    """OEIS A005260: sum_k C(n,k)^4."""
    return [sum(C(n, k)**4 for k in range(n + 1)) for n in range(n_max + 1)]
```

**Claim under test** (Part VIII, §4.2-4.3): both Cooper s7 and Cooper s10 satisfy a *minimal* order-2, degree-3 shift recurrence with leading coefficient P2(n) = (n+2)³ exactly:

```
(n+2)^3 * a(n+2) = P1(n) * a(n+1) + P0(n) * a(n)
```

This repository fits P1, P0 (degree-3 polynomials, 8 unknowns) using exact Gaussian elimination over Fractions on n=0..7, then verifies the fitted recurrence holds *exactly* on all held-out terms up to n=38:

| Sequence | Fitted Recurrence | Verification |
|----------|-------------------|---------------|
| Cooper s7 | P1(n)=26n³+117n²+177n+90 | VERIFIED, n=0..38 (39/39 exact matches) |
| | P0(n)=27n³+81n²+78n+24 | |
| Cooper s10 | P1(n)=12n³+54n²+82n+42 | VERIFIED, n=0..38 (39/39 exact matches) |
| | (analogous P0, see logs/hypothesis_comparison_t103_cooper.json) | |

**Result**: both recurrences hold exactly across every computed term with zero failures, independently corroborating the Part VIII claim without relying on the Lean 4 kernel itself.

## Asymptotic Growth Constants

For each GATE-C finalist, the asymptotic growth constant μ (where a(n) ~ C μⁿ n^-α) is estimated via the exact ratio a(40)/a(30), raised to the power 1/10:

| Candidate | Growth constant μ | 1/μ |
|-----------|-------------------|-----|
| t103 (A276536) | 62.273 | 0.01606 |
| Cooper s7 (A183204) | 25.869 | 0.03866 |
| Cooper s10 (A005260) | 15.331 | 0.06523 |

The legacy S12/S21 mass-ratio reference value, √(1014/336) ≈ 1.7372, is retained here **only as a historical comparison point** — it is no longer interpreted as a validated K3 modulus ratio, since S12 itself has been reclassified as elliptic-type.

## Cross-Reference with Real Euclid Q1 / SDSS BOSS DR17 Data

| Source | n | Mean Δ | Std | Range |
|--------|---|--------|-----|-------|
| SDSS BOSS DR17 | 9 | 1.1252 | 0.0111 | [1.1030, 1.1334] |
| Euclid Q1 | 17 | 1.1252 | 0.0125 | [1.1055, 1.1423] |
| Gaia DR3 | 5 | 1.1216 | 0.0121 | [1.1068, 1.1336] |
| Pan-STARRS | 4 | 1.1229 | 0.0097 | [1.1065, 1.1312] |
| **Overall** | **35** | **1.1244** | **0.0119** | **[1.1030, 1.1423]** |

Consistency across four independent surveys (1.1216-1.1252) supports a systematic, not source-specific, origin. The observed elevation over the theoretical reference is 1.1244 / 0.327 = 3.438× — unchanged from prior analysis, since this is a direct measurement of galaxy-distribution asymmetry and does not depend on which K3 modulus pair is postulated as the underlying geometric substrate.

## Candidate Scorecard

| Candidate | K3-type | ODE Order | Status |
|-----------|---------|-----------|--------|
| S12/S21 (A112019-type) | **No** | 2 | REJECTED: elliptic, q2=81/8 non-integral |
| t103 (A276536) | **Yes** | 3 | GATE-C finalist; novel discovery, held-out to 62 terms |
| Cooper s7 (A183204) | **Yes** | 3 | GATE-C finalist; literature-anchored, recurrence re-verified |
| Cooper s10 (A005260) | **Yes** | 3 | GATE-C finalist; literature-anchored, recurrence re-verified |

## Figures

1. `figures/fig_hypothesis_sequence_growth.png` — Exact big-integer terms of the three candidate sequences (log scale)
2. `figures/fig_hypothesis_growth_constants.png` — Estimated asymptotic growth constants μ
3. `figures/fig_hypothesis_recurrence_verification.png` — Recurrence verification status
4. `figures/fig_hypothesis_delta_by_source.png` — Real-data Δ by independent survey source
5. `figures/fig_hypothesis_scorecard.png` — Summary scorecard

## Limitations and Scope

- The real-data Δ signal is a measurement of galaxy-distribution asymmetry; it does **not** by itself distinguish which K3-type modulus pair among t103/Cooper-s7/Cooper-s10 is the correct geometric substrate. Per Part VIII §1.5, the physics gates are non-discriminating at common moduli-space normalization.
- The growth-constant ratios are a phenomenological proxy for relative instanton/period scale, not a substitute for the full Lean 4 Picard-Fuchs classification performed in the companion repository.
- This section's independent re-verification corroborates the specific recurrence-structure claim for Cooper s7/s10 exactly and independently of the Lean kernel, but does not re-derive the full G1-G4 gate battery (modularity, integrality, Fuchs/monodromy) applied in Part VIII; those results are taken from the companion project as reported.
