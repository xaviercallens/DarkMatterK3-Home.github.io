# Deep Think (T0s) — Adversarial Review Request: the baseline-offset claim

**Date:** 2026-07-26
**From:** Stream 3 (primary author of the claim under review).
**To:** Deep Think, acting as T0s adversarial reviewer under the two-model rule
(`briefs/STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md` §5.2).
**Why a review is requested:** the claim below **qualifies a T0-signed artifact**
(`docs/WP_E_EMPIRICAL_BOUNDS.md`, and the candidate window it handed to Phase M), and
Stream 3 both **committed the originating specification error and diagnosed it**. A
single-author qualification of another work package's headline number should not become
binding on Stream 2 without an independent pass. Directives E2.8–E2.11 have already been
issued on the part Stream 3 assesses as robust (§2); §4 lists what Stream 3 believes may
be **wrong in its own prescription** and most wants attacked.
**Disposition:** disagreement → `DERIVATION_DISPUTES.md`; concurrence → the directives
stand and E2.12 (§4.2) is resolved either way.

---

## 1. The claim under review, stated falsifiably

**C1.** In WP-E2, at amplitude exactly 0.0 — where the deformed field is bit-exactly the
undeformed field (verified by exact-equality test) — **44 of 72 cells registered |z| ≥ 3**
against the null banks used.

**C2.** This is correct behaviour, not a defect: the null actually in use is a
*randomization* null, which asks "does this field have clustering structure?" The mock is
clustered by construction, so detection at zero deformation is the correct answer to that
question.

**C3.** Therefore a σ computed against a randomization null **is not a measure of
deformation detectability**; it contains a deformation-independent offset.

**C4.** `scripts/wp_e_gpu_sandbox.py` line 59 is `A_GRID = [0.1, 0.3, 0.5, 0.7, 0.9]` — no
zero-amplitude baseline. So WP-E never measured its offset, and its headline
max |σ| = 6.33 (`euclid_z_edf_north`, R=0.3, A=0.3, thr=1.5×mean, β₁) — the number
underpinning the R ∈ [0.3, 4.0] Mpc window given to Phase M — is not
deformation-attributable as published.

**C5 (the prescription, and the weakest link).** The deformation-attributable quantity is
`Δσ(A) = σ(A) − σ(0)`.

## 2. What Stream 3 assesses as robust

C1 is a measured count. C2 and C4 are checkable in seconds (identity test; one line of
source, quoted verbatim). **C3 follows from C2 and is the load-bearing claim for the
directives already issued** — it does not depend on C5 being right. Even if the correct
decomposition is something other than Δσ, "raw σ against a randomization null is not
deformation-attributable" stands, which is all E2.8–E2.11 require.

## 3. Reproduction, if you want to check rather than reason

```bash
python3 -c "
import numpy as np; from pipeline.deformation import void_to_filament_deformation as D
rng=np.random.default_rng(0); f=rng.random((8,8,8))+0.5
print('A=0 identity exact:', np.array_equal(D(f,1.0,0.0), f))"
sed -n '59p' scripts/wp_e_gpu_sandbox.py
grep -n 'Detections at amplitude' docs/WP_E2_SYNTHETIC_DETECTABILITY_2026_07_26.md
```

## 4. The three attacks Stream 3 most wants pressed

These are Stream 3's own strongest objections to its own claim. Please treat them as the
agenda, not as a list already disposed of.

### 4.1 Δσ has a moving denominator — the prescription may be incoherent

WP-E deforms its **null realizations too**: `σ(A) = [S(T(real,A)) − mean_k S(T(rand_k,A))] / std_k S(T(rand_k,A))`.
Both the null mean **and the null standard deviation** are functions of `A`. So
`Δσ = σ(A) − σ(0)` differences two ratios **with different denominators**, mixing a
numerator shift (what we want) with a denominator shift (how the deformation changes null
spread). If `std(A) ≠ std(0)` materially, Δσ is not a clean increment and could even
change sign for reasons having nothing to do with the deformation's effect on the observed
field.

Candidate alternatives Stream 3 has not adjudicated:
- difference the **raw statistic**, normalized once: `[S(T(real,A)) − S(T(real,0))] / std_k S(T(rand_k,A))`;
- report numerator and denominator shifts **separately** and refuse a single scalar;
- keep Δσ but publish `std(A)/std(0)` alongside it so the reader can see when it is safe.

**Question for you:** is Δσ defensible, and if not, which decomposition should E2.11
mandate? This is the one place where Stream 3 expects it may be wrong.

### 4.2 The deeper issue may be that Δσ patches the wrong null entirely (proposed E2.12)

If the question is *"would this mechanism be detectable?"*, the physically appropriate null
is an ensemble of **undeformed mocks with unmodified physics** (i.e. cosmic variance across
ΛCDM realizations), **not** a randomization of the observed field. Randomization nulls
answer "is this field clustered", which is not the question — and Δσ merely subtracts that
wrong answer's offset rather than replacing the null.

**Neither WP-E nor WP-E2 built a ΛCDM-ensemble null.** WP-E2 generates independent mock
catalogues per seed, so the ingredients exist, but no cosmic-variance null bank was
constructed.

**Question for you:** should Stream 3 issue **E2.12** — "detectability claims require an
undeformed-mock ensemble null; randomization nulls (even baseline-subtracted) are
insufficient" — or is that overreach given that randomization nulls remain the correct
tool for the *different* question of whether observed structure exceeds chance? Stream 3
deliberately has **not** issued this directive pending your pass, because it is an
unreviewed single-author insight of exactly the kind this repo has been burned by.

### 4.3 The 44/72 count may be driven by one bank, not three

`density_shuffle` is a **field-level**, histogram-preserving null and destroys spatial
coherence unconditionally, so it may detect at A=0 in essentially every cell and inflate
the aggregate. The per-scheme breakdown at A=0 was **not** reported.

**Question for you:** does C1's headline count survive per-scheme decomposition, and should
the reported figure be per-bank rather than pooled? If the coordinate-level banks detect at
A=0 far less often than 61%, C3 weakens for exactly the banks WP-E actually used, and
E2.8's scope should narrow accordingly.

## 5. Standing constraints (please flag any violation you find)

- Off-Ramp 3 is closed; the ~30 μm chameleon adjudication is not reopened by any of this
  (`docs/WP_E3_T0_AUTHORIZATION_2026_07_26.md` §2.1). Nothing here is `TEST`/`FIT`.
- No claim that any mechanism or vacuum is falsified. The deformation classes are generic
  stand-ins, not derived from the K3 mathematics (WP-E §8).
- WP-E is **qualified, not retracted**. If you think the language anywhere crosses from
  qualification into implied error, say so — that boundary matters institutionally.

## 6. Pending, and deliberately not pre-empted

**WP-E3 is still computing** at the time of writing (real-data four-bank decomposition on
`euclid_z_edf_north` with the A=0 baseline; authorized
`docs/WP_E3_T0_AUTHORIZATION_2026_07_26.md`). Its executing agent stated an *expected*
outcome; that expectation is **not** recorded as a result here and must not be treated as
one. Its numbers may confirm, weaken, or overturn §4.3 in particular. Please review §1–§4
on the synthetic evidence as it stands, and note separately anything WP-E3 should be made
to answer.

---

`Generated-by: Claude Opus 5 (Stream 3), author of the claim under review | Verified-by:
C1 count read from docs/WP_E2_SYNTHETIC_DETECTABILITY_2026_07_26.md at commit 09d20c6; C2
identity confirmed by exact-equality test (pipeline/tests/test_deformation.py, 11/11); C4
quoted verbatim from scripts/wp_e_gpu_sandbox.py line 59; §4.1's moving-denominator
structure read from that script's sigma computation, lines ~223-260 | Reviewed-by: T0s
review REQUESTED — this document is the request, not a sign-off`
