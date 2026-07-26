# Cross-Stream Consolidated Brief — 2026-07-26

**From:** Stream 3.
**To:** Stream 1 (Geometric Theory / Lean) and Stream 2 (K3 Theory & Candidate Selection,
Phase M / M1 memo).
**Location:** `briefs/CROSS_STREAM_CONSOLIDATED_2026_07_26.md`, **`main` branch** — this is
the single authoritative entry point for everything Stream 3 issued on 2026-07-26.
**Supersedes as an index:** the four separate briefs dated today. Their reasoning stands and
remains the citable provenance; **this document is where the directives are consolidated**,
with supersessions marked.

> **Read §1 and §5 before acting on anything.** §1 is the interpretation that makes the
> directives coherent. §5 states what is **not yet settled** — including one directive that
> is drafted but deliberately withheld, and one that may be revised under review.

---

## 1. Interpretation — one lesson, three findings

Three independent findings landed today. They are not separate cautions; they are the same
problem seen three times.

| Finding | Where | What it showed |
|---|---|---|
| **F-SYN-1** — separation is scheme- and tail-relative | `briefs/STREAM3_AUDIT_DIRECTIVES_2026_07_26.md` §3 | The *same* observed β₁ sat at the **100th percentile against CSR and z-shuffle nulls and the 0th against density-shuffle**, in all three seeds |
| **Baseline offset** — randomization σ is not deformation-attributable | `docs/WP_E2_SYNTHETIC_DETECTABILITY_2026_07_26.md` | At **exactly zero deformation** (field bit-identical to undeformed), **44/72 cells still registered \|z\| ≥ 3** |
| **Scale gap** — the synthetic box cannot reach the resolvable window | same report | Swept scales 13.8–183.7 Mpc vs a 0.22–0.27 Mpc resolvable floor; a **~680× smaller box** would be needed |

**The unifying interpretation:** every significance number this program has produced so far
has been **under-specified about what it is significant *against***. Not miscalculated —
under-specified. F-SYN-1 shows the *scheme* was unstated; the baseline offset shows the
*zero point* was unstated; the scale gap shows the *resolvable range* was unstated. In each
case the arithmetic was correct and the claim it appeared to support was not the claim it
actually supported.

This is why every directive below is, at bottom, the same instruction: **state your null.**

A fourth observation belongs here because it is institutional rather than numerical. The
baseline finding surfaced **only because an executing agent reported a contradiction with
its own specification instead of adapting to it** — the specification (Stream 3's own) had
called the zero-amplitude cell a "tautological-zero guard" and predicted ~0 detections. The
practice worth keeping is not the finding; it is that a contradiction was escalated rather
than smoothed.

## 2. Directives — Stream 2 (Phase M / M1 memo)

Consolidated and de-duplicated. **E2.8 supersedes E2.3.** Where two directives overlapped,
the stronger is kept and the weaker marked.

| # | Directive | Status |
|---|---|---|
| **D2.1 / E2.1** | Pre-register the **null scheme AND the tail** together (e.g. "β₁ above the CSR 95th percentile"), never "β₁ separates from null". The same value can sit at opposite extremes under different valid schemes. | **Binding** |
| **D2.2** | Any β₂-based signature must state its **resolution regime** (nbins / voxel scale at which cavities survive at the target field's density) in its own §1. | **Binding** |
| **D2.3** | State **null-bank size** matching the claimed significance, and the **percentile convention** including tie handling and `None`-on-zero-variance. 30 trials caps granularity at ~3.3%; p < 0.01 needs ≥100 or exact machinery. | **Binding** |
| **D2.4** | Annotate or correct the "certified" premise line per **F-AUD-1** (§4 below). | **Binding** |
| **E2.2** | Any mechanism whose scale-setting routes through an **Mpc-scale chameleon is dead on arrival** and must say so in its own §1 — the ~30 μm ceiling is adjudicated, two-model, CLOSED-NEGATIVE (`NO_PREDICTION_BRANCH.md` §8.5). | **Binding** |
| **E2.8** | Do **not** cite WP-E's **R ∈ [0.3, 4.0] Mpc window**, or any σ in `docs/WP_E_EMPIRICAL_BOUNDS.md` §4, as a **deformation-attributable** design constraint. Those σ may be cited only as *"structured-vs-randomized after deformation"*, with that phrase attached. | **Binding — supersedes E2.3** |
| **E2.9** | State the **null hypothesis explicitly**. "No clustering structure" and "no deformation" are different claims; the first registers detection at zero mechanism strength. | **Binding** |
| **E2.10** | Prefer **β₂ over β₁** for deformation-attributable statements on this class of field. β₁ detected at zero deformation at every R tested — its apparent "0.0 sensitivity floor" is a baseline artifact and **must not be quoted as a floor**. β₂ was not detected at zero deformation and showed a genuine floor near amplitude ≈ 0.5. This **refines** the standing β₁/β₂-over-β₀ guidance (WP-R7): β₁ and β₂ are **not interchangeable** for this purpose. | **Binding** |
| **E2.11** | Quoted significances must be **baseline-subtracted**. | **Binding, but the prescribed formula is under review — see §5.2** |
| **E2.4** | State predicted signatures as **(scale, amplitude)**, amplitude in units of the field mean, each with the null it is detectable against. | **Binding** |

**Net practical effect on M1:** the R ∈ [0.3, 4.0] Mpc window may still be used to argue a
mechanism is **untestable-by-construction** (that direction is safe — it only needs the
resolvable envelope). It may **not** be used to argue a mechanism **would be detected**, and
it can never be used to argue one is **falsified** (the deformation classes are generic
stand-ins, not K3-derived — WP-E's own §8).

## 3. Directives — Stream 1 (Geometric Theory / Lean)

| # | Directive | Status |
|---|---|---|
| **D1.1** | **Resolve `K3_CRITERIA.md` C2's `TBD-AT-FREEZE`** — the exact Kodaira/Euler-characteristic consistency identity, with citation. This is the **single blocker** on `check_C2_kodaira.py` and therefore on any computed certificate for ρ=4/T=18 or fibre content. Outstanding since 2026-07-24. | **Binding, unchanged, still the top item** |
| **D1.2** | Until D1.1 lands, do **not** describe ρ=4/T=18 or fibre content as *"certified"*. Honest wording: *"certificate-backed: C1 (s7, s10); pending certificate: C2, and C3/C3b for the Cooper candidates."* Fibre-type claims trace to Stream 2's `C1loci` certificate, **never to a brief** — WP-H found a brief contradicting that certificate. | **Binding** |
| **D1.3 / E2.7** | Route every inbound and outbound brief through **`pipeline/triage.py`** before acting or circulating. Today's pasted protocol was the **fifth** brief in four days whose factual predicates did not survive checking. | **Binding** |
| **E2.6** | Do not cite any *"K3 order-3 Picard-Fuchs recurrence ⇒ chameleon screening radius"* linkage as established. No artifact in either repo connects them. The geometric relation is not a physical coupling (VISION §1.3). | **Binding** |

## 4. F-AUD-1 — the cross-stream certificate gap (unchanged, still open)

The Phase M directive's §1 describes *"certified K3 mathematics (Tier A/B: Sym² identity,
ρ=4/T=18 Shioda–Tate, 2× Type II Kodaira fibres)"*. What is actually certificate-backed
**in this repo**:

- **C1** (mirror integrality): `PASS(40)` for s7 and s10 ✅
- **C3 / C3b**: only for the **golden AZ control pairs** (A↔δ, C↔α, D↔η) — **not** for either Cooper candidate
- **C2**: **no certificate exists at all** — blocked on D1.1

So ρ=4/T=18 and the fibre content have **no computed artifact here**, which is why
`pipeline/D3_batch_runner_phase2.py` now reports them as honest `NaN` gaps rather than
constants. This is a provenance-wording gap, not an allegation of error — but P1 (no
constant without provenance) applies to directives too.

## 5. What is NOT settled — do not act on these as if they were

### 5.1 WP-E3 has no results
The authorized real-data four-bank decomposition on `euclid_z_edf_north`
(`docs/WP_E3_T0_AUTHORIZATION_2026_07_26.md`) is **still computing**. Zero σ values exist.
Its executing agent stated an *expected* outcome; that expectation is **not** recorded as a
result anywhere in this repo and must not be cited as one. Its numbers may confirm, weaken,
or overturn parts of §1.

### 5.2 E2.11's formula is under adversarial review
E2.11 mandates baseline subtraction. The **prescribed** form, `Δσ(A) = σ(A) − σ(0)`, may be
incoherent: WP-E deforms its null realizations too, so the null **mean and standard
deviation both depend on A**, and differencing two ratios with different denominators mixes
the numerator shift we want with a denominator shift — it could even change sign for reasons
unrelated to the deformation. Submitted to Deep Think
(`briefs/DEEPTHINK_REVIEW_REQUEST_BASELINE_2026_07_26.md` §4.1) with three candidate
alternatives. **The requirement to baseline-subtract stands; the formula may change.**

### 5.3 E2.12 is drafted and deliberately withheld
Candidate directive: *"detectability claims require an undeformed-mock ensemble
(cosmic-variance) null; randomization nulls, even baseline-subtracted, are insufficient."*
If correct, Δσ patches the wrong null rather than fixing it — the physically appropriate
null for *"would this mechanism be detectable"* is an ensemble of undeformed mocks with
unmodified physics, and **neither WP-E nor WP-E2 built one**. This is **not issued**,
pending Deep Think (§4.2 of that brief), because it is an unreviewed single-author insight
of exactly the kind this repo has been burned by. Stream 2 should be aware it may arrive.

### 5.4 Branch location
The WP-E2/WP-E3 artifacts referenced above live on branch
**`wp-e2-synthetic-detectability`** (6 commits ahead of `main`), **not yet merged**. They are
deliberately unmerged while §5.2 is under review. This brief and
`briefs/STREAM3_AUDIT_DIRECTIVES_2026_07_26.md` are on `main`. To read the artifacts:
`git checkout wp-e2-synthetic-detectability`.

## 6. Standing constraints (unchanged by anything today)

- **Off-Ramp 3 is closed.** The empirical [A-DD] programme is terminated; the ~30 μm
  chameleon adjudication is not reopened. Overriding a falsification trigger requires a
  **written T0 ruling** (CLAUDE.md rule 5); no authorization granted today constitutes one.
- **G1-L is closed**, mechanically (`pipeline/gate.py`). Nothing today is `TEST` or `FIT`.
- **Only residue:** monitoring trigger **F-LAB** (`NO_PREDICTION_BRANCH.md` §9) — future
  public ISL data excluding |α|=1 below 38.6 μm, and nothing else.
- **No falsification claims** from generic deformations. WP-E's classes are stand-ins, not
  derived from the K3 mathematics.

## 7. Provenance index

| Artifact | Branch | Contains |
|---|---|---|
| `briefs/STREAM3_AUDIT_DIRECTIVES_2026_07_26.md` | `main` | F-SYN-1…4, F-AUD-1, D1.1–D1.3, D2.1–D2.4 |
| `briefs/STREAM3_WPE2_TRIAGE_AND_DIRECTIVES_2026_07_26.md` | `wp-e2-…` | Triage of the re-pasted protocol, E2.1–E2.7 |
| `briefs/STREAM2_DIRECTIVE_ADDENDUM_BASELINE_2026_07_26.md` | `wp-e2-…` | Baseline finding, E2.8–E2.11 |
| `briefs/DEEPTHINK_REVIEW_REQUEST_BASELINE_2026_07_26.md` | `wp-e2-…` | Review request; §4 attack agenda; withheld E2.12 |
| `docs/WP_E2_SYNTHETIC_DETECTABILITY_2026_07_26.md` | `wp-e2-…` | The sweep and its numbers |
| `docs/WP_E3_T0_AUTHORIZATION_2026_07_26.md` | `wp-e2-…` | T0 grant + explicit scope limits |
| `docs/STREAMS_STATUS_2026_07_26.md` | `main` | WP-T1–T6 record, two defects caught |

---

`Generated-by: Claude Opus 5 (Stream 3) | Verified-by: every directive traced to its
originating brief and renumbered without alteration of meaning; supersession of E2.3 by E2.8
stated explicitly; certificate inventory in §4 from ls checkers/certificates/; branch
divergence (6 commits) from git log main..wp-e2-synthetic-detectability; WP-E3 confirmed
still running with zero sigma rows on disk at time of writing | Reviewed-by: T0 N — pending
Xavier`
