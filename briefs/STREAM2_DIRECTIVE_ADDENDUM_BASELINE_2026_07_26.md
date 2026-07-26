# Addendum to the WP-E2 directives — the baseline-offset qualification (interim, act on this now)

**Date:** 2026-07-26
**From:** Stream 3.
**To:** Stream 2 (Phase M / M1 memo, actively drafting), cc Stream 1, T0.
**Extends:** `briefs/STREAM3_WPE2_TRIAGE_AND_DIRECTIVES_2026_07_26.md` (directives E2.1–E2.7).
**Status:** **Interim.** The finding below is complete and actionable on its own. The
per-scheme verdict on WP-E's window (WP-E3, real data, authorized
`docs/WP_E3_T0_AUTHORIZATION_2026_07_26.md`) is **still running** and will be appended
when it lands. Nothing here waits on it.

---

## 1. The finding

WP-E2 (`docs/WP_E2_SYNTHETIC_DETECTABILITY_2026_07_26.md`, commit `09d20c6`) ran a
**zero-amplitude** cell, where the deformed field is bit-exactly the undeformed field
(verified by an exact-identity test). Against the coordinate-level randomization nulls,
**44 of 72 zero-amplitude cells still registered |z| ≥ 3.**

That is correct behaviour, not a defect. Two null hypotheses had been conflated:

| Null actually used | Question it answers | Behaviour at zero deformation |
|---|---|---|
| Coordinate randomization (CSR, z-shuffle) | *does this field have clustering structure?* | **detection expected** — the field is clustered by construction, randomization destroys clustering |
| (what the phrase "detectability" implies) | *is this field deformed?* | would need a null that re-deforms the same point set — none of these schemes do that |

**Therefore: a σ measured against a randomization null is not a measure of deformation
detectability.** It is dominated by a deformation-independent offset — the field is
clustered. The deformation-attributable quantity is the increment over the zero-amplitude
baseline, `Δσ(A) = σ(A) − σ(0)`, not the raw `σ(A)`.

**Disclosure:** the erroneous expectation was Stream 3's own — the WP-E2 specification
called the zero-amplitude cell a "tautological-zero guard" and predicted ~0 detections.
The executing agent reported the contradiction rather than adapting to the spec, which is
how it surfaced. Two sections of the generated report carried that wrong framing and were
corrected in `09d20c6`.

## 2. Why this changes what Stream 2 may cite today

`scripts/wp_e_gpu_sandbox.py` line 59 reads:

```python
A_GRID = [0.1, 0.3, 0.5, 0.7, 0.9]  # dimensionless coupling amplitude
```

**There is no zero-amplitude baseline.** WP-E therefore never measured its own offset, so
its published σ values — including the headline **max |σ| = 6.33** for `euclid_z_edf_north`
at (R=0.3, A=0.3, thr=1.5×mean, β₁), which is the number underpinning the
**R ∈ [0.3, 4.0] Mpc primary candidate window** handed to Phase M — cannot be attributed
to the deformation without one.

This is a **methodological qualification, not an error and not a retraction.** WP-E's σ is
a valid *structured-vs-randomized-after-deformation* statistic, computed correctly. It is
simply not the *deformation-attributable* statistic, and the window was described as
though it were.

## 3. Directives (extending E2.1–E2.7)

| # | Directive | Basis |
|---|---|---|
| **E2.8** | Do **not** cite WP-E's R ∈ [0.3, 4.0] Mpc window, or any σ from `docs/WP_E_EMPIRICAL_BOUNDS.md` §4, as a **deformation-attributable** design constraint. Until baseline-subtracted values exist, those σ may be cited only as "structured-vs-randomized after deformation", with that phrase attached. This supersedes the softer wording of E2.3. | §1, §2 |
| **E2.9** | Any M1 detectability argument must state its **null hypothesis explicitly** — "no clustering structure" versus "no deformation" are different claims with different nulls, and the first will register detection even at zero mechanism strength. A memo that reports a σ without naming which null it is against is under-specified in the same way E2.1/D2.1 flagged for scheme-and-tail. | §1 |
| **E2.10** | Prefer **β₂** over β₁ for deformation-attributable statements on this class of field. In WP-E2, β₁ registered detection at zero deformation across every R tested (so its apparent "sensitivity floor" of 0.0 is a baseline artifact and must not be quoted as a floor), whereas β₂ was not detected at zero deformation and showed a genuine floor at amplitude ≈ 0.5. This **refines** the standing β₁/β₂-over-β₀ guidance (WP-R7): among β₁ and β₂, they are not interchangeable for this purpose. | WP-E2 floor + baseline tables |
| **E2.11** | When M1 states a predicted signature as (scale, amplitude) per E2.4, the amplitude must be accompanied by the **null it is detectable against** and, if a σ or significance is quoted, a **baseline-subtracted** figure. | E2.4 + §1 |

## 4. Scale note (unchanged conclusion, now quantified on synthetic data)

WP-E2's mock box measured 734.8 × 613.2 × 442.9 Mpc, giving voxels of ≈45.9 / 38.3 / 27.7
Mpc per axis; the swept deformation scales spanned **13.8–183.7 Mpc physical**. That range
does **not** overlap the 0.22–0.27 Mpc survey-resolvable window (`docs/WP_R6_SURVEY_SCALES.md`);
reaching it would require a box smaller by a factor of ≈680. Reported as measured — the
configuration was not adjusted to manufacture an overlap. This corroborates the WP-H scale
wall from a second, independent direction and reinforces directive D2.2.

## 5. What is still pending

WP-E3 — the authorized real-data, four-bank decomposition on `euclid_z_edf_north`
(`mixed_r5` reproduction control, `z_shuffle_only`, `csr_only`, and the field-level
`density_shuffle`), now extended mid-run to include the zero-amplitude baseline and report
`Δσ`. Its pre-committed kill condition
(`docs/WP_E3_T0_AUTHORIZATION_2026_07_26.md` §5) is judged on `Δσ`, not raw σ. Its verdict
will be appended here.

---

`Generated-by: Claude Opus 5 (Stream 3) | Verified-by: zero-amplitude identity confirmed by
exact-equality test (pipeline/tests/test_deformation.py, 11/11); WP-E's A_GRID quoted
verbatim from scripts/wp_e_gpu_sandbox.py line 59 read this session; WP-E2 counts read from
the generated report at commit 09d20c6 | Reviewed-by: T0 N — pending Xavier`
