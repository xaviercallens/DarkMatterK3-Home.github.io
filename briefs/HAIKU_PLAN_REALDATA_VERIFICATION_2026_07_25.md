# Real-Data Verification Plan (WP-R series) — Low-Tier Execution

**Date:** 2026-07-25
**Author:** Fable 5 (T0-delegated)
**Executor:** Haiku 4.5 sessions (T2 mechanical work). Every WP below is Haiku-tier
unless marked otherwise.
**Governing docs:** `CLAUDE.md` (6 rules), `prereg-pipeline` + `epistemic-guardrails`
skills, `pipeline/gate.py` (G1/G1-L), `LESSONS_LEARNED.md` (P1–P4).
**Inputs now available:** real SDSS + Euclid catalogs fetched 2026-07-25
(`data/MANIFEST.md`, external disk), Stream 2 certificates, Stream 1 Lean sources.

---

## 0. Read this before planning any work package

### 0.1 What can and cannot be verified with data

Stream 1 and Stream 2's **verified** outcomes are Tier A *mathematics*: ρ=4, T=18
(Shioda–Tate), 2× Type II Kodaira fibres, L₃ = Sym²(L₂) (Lean 4, kernel-verified),
mirror-map integrality to finite order. **None of these makes contact with survey
data.** There is no derived mass, coupling, or length scale — that is exactly what F5b
found missing and what Off-Ramp 3 closed (`NO_PREDICTION_BRANCH.md` §8.5).

So "verify Stream 1/2 outcomes against real data" **cannot mean a physics test**. There
is nothing pinned to test against, and gate G1-L is closed. Attempting one would
manufacture a result — the precise failure this project has already documented twice.

What real data legitimately enables, and what this plan covers:

| Goal | Legitimate? | Why |
|---|---|---|
| Re-verify the certified mathematics | ✅ | Deterministic, no data needed; regression safety |
| Characterize what the real data actually contains | ✅ | Pure measurement of the data itself |
| Validate our machinery survives real data | ✅ | Engineering: masks, holes, non-uniform sampling |
| Build realistic null distributions from real data | ✅ | Upgrades P2/P3 discipline; hypothesis-agnostic |
| Sibling-family control harness (P4) | ✅ | Infrastructure, computes nothing physical |
| Compare a Stream 1/2 quantity to data as TEST/FIT | ❌ | G1-L closed; no derived observable exists |

**Everything in this plan is G1-scope engineering. No WP produces a TEST or FIT label.**

### 0.2 Hard finding that constrains the plan — κ-peaks are blocked on public data

Verified 2026-07-25 by enumerating the Euclid public TAP schema: the available
catalogues are **MER** (morphology/photometry), **PHZ** (photo-z), and **SPE**
(spectroscopy). **There is no shear / SHE / lensing catalogue in the public release.**

Consequence: **a real weak-lensing convergence map cannot be built from the public
Euclid data on hand.** The `ellipticity` column in `catalogue.mer_catalogue` (which we
fetched) is a **morphological** ellipticity of the light profile — it is *not*
calibrated weak-lensing shear. Using it as shear would be a methodological fabrication
of exactly the kind `LESSONS_LEARNED.md` L3/L4 document.

**Therefore:** `compute_kappa_peak_statistic()` stays synthetic-only until a genuine
public shear catalogue is identified. It is not to be run on MER ellipticity under any
framing. This is recorded as finding **R-SHEAR** and is a stop-and-flag condition below.

What *is* viable: photo-z (`catalogue.phz_photo_z`: `phz_median`, `phz_mode_1`, joinable
on `object_id`) and SDSS spectroscopic redshifts give **real 3D positions** → a real
density field → the Betti/topology machinery has a legitimate real-data input.

### 0.3 Hard rules for every WP (non-negotiable)

1. **Never pin.** Do not add or modify `PINNED:` / `DERIVED:` headers.
2. **Never label.** No output may carry `TEST` or `FIT`. Everything is `SYNTHETIC` or
   `ENGINEERING`. The gate enforces this; do not work around it.
3. **No numbers from memory.** Every constant traces to a certificate, a committed file,
   or `data/MANIFEST.md`. If you cannot point at the source, stop and flag.
4. **Never re-fetch data to "fix" a mismatch.** If a checksum fails, that is a finding —
   report it, do not silently re-download.
5. **No synthetic fallback, ever.** If real data is missing or a query fails, the WP
   reports the failure. Never substitute random values (Lesson L5 — this repo shipped
   that bug three times; six scripts are quarantined for it).
6. **Do not run `D3_batch_runner_phase2.py`** and do not import any file carrying a
   `DEPRECATED / EXPERIMENTAL` or `QUARANTINED` banner (see
   `LEGACY_CODE_DISPOSITION_2026_07_25.md` for the list of six).
7. Run `python3 scripts/check_tier_language.py` before every commit; it must print 0
   violations.
8. Every generated file carries the provenance footer
   (`Generated-by | Verified-by | Reviewed-by`).

### 0.4 Token-efficiency protocol for Haiku sessions

- Each WP lists **exactly** the files to read. Read those and nothing else; do not
  explore the repo. The repo is large and mostly irrelevant to any single WP.
- Do not read `.tex`, `.pdf`, `logs/`, `archives/`, `frontend/`, `ui_loom/`, or any
  `RELEASE_NOTES*`, `PHASE*`, or `V5_*` file unless a WP names it.
- Do not read the fetched CSVs in full — they have up to 14,007 rows. Load them with
  pandas/astropy and print summaries. Never paste raw rows into your reply.
- One WP per session where possible. Report in under 300 words: what you did, the
  numbers you measured, what you flagged, test status.
- If a WP's validation fails, **stop and report**. Do not attempt the next WP.

---

## 1. Work packages, simplest first

### WP-R0 — Re-verify the certified mathematics (no data at all)

**Complexity:** trivial. **Est:** 15 min. **Depends on:** nothing.
**Why first:** it is the cheapest possible check, it needs no data, and it establishes
that the Tier A foundation is intact before anything is built on top of it.

**Read only:** `checkers/check_C3_sym2.py`, `checkers/check_C3b_moduli_map.py`,
`checkers/check_C1_mirror_integrality.py` (skim signatures/CLI only), `docs/CRITERION_STATUS.md`.

**Do:**
1. Run each checker as its CLI documents, plus `python3 -m pytest checkers/tests/ -q`.
2. Record for each candidate the C1/C3/C3b verdict actually printed.
3. Compare against the committed `docs/CRITERION_STATUS.md` matrix.

**Validation:** every result reproduces the committed matrix exactly, including the
known negatives (Cooper s7/s10 **fail** C3/C3b — that is the expected, correct outcome;
a suddenly-passing s7 is a red flag, not good news).
**DoD:** short report `docs/WP_R0_MATH_REVERIFY.md` with the verdict table and the
pytest line. **STOP AND FLAG if:** any verdict differs from the committed matrix in
either direction.

---

### WP-R1 — Real-data integrity and characterization

**Complexity:** trivial. **Est:** 30 min. **Depends on:** nothing.

**Read only:** `data/MANIFEST.md`, `scripts/fetch_survey_astroquery.py`.

**Do:** write `scripts/verify_realdata_integrity.py` that, for each of the 7 datasets in
the MANIFEST full-fidelity appendix:
1. Confirms the file exists at the recorded path on the external disk.
2. Recomputes SHA256 and compares to the recorded hash (exact match required).
3. Loads it and reports: row count (vs. the recorded count), column list, per-column
   null fraction, and min/max of `ra`/`dec` (SDSS) or `right_ascension`/`declination`
   (Euclid).
4. Sanity-checks coordinate ranges: RA ∈ [0,360], Dec ∈ [−90,90], and that each field's
   centroid is within ~1° of the query centre recorded in the MANIFEST.

**Validation:** all 7 checksums match; all 7 row counts match; no coordinate out of
range. Print a table; write it to `docs/WP_R1_REALDATA_INTEGRITY.md`.
**DoD:** script + report committed; script is re-runnable and idempotent.
**STOP AND FLAG if:** any checksum or row count mismatches (that means the data changed
under us — a provenance incident, not a bug to patch).

---

### WP-R2 — Observable machinery smoke-test on a real-derived field

**Complexity:** easy. **Est:** 1–2 h. **Depends on:** WP-R1 green.
**Why it matters:** every existing test of `observables_real.py` uses smooth synthetic
fields. Real catalogs have survey masks, holes, and wildly non-uniform sampling. This WP
asks only: *does the code behave sanely on that?* It is not a physics measurement.

**Read only:** `pipeline/observables_real.py`, `pipeline/tests/test_observables_real.py`,
`docs/WP_R1_REALDATA_INTEGRITY.md`.

**Do:**
1. Add `pipeline/realfield.py` with `density_field_from_catalog(ra, dec, z=None,
   nbins=...)` — a plain 2D (or 3D if z given) histogram of object counts on a regular
   grid, normalized to mean 1. No smoothing, no kernels, no tuned constants. Document
   that binning choice is a free parameter and therefore **any** result from it is
   engineering-only.
2. Run `compute_betti_numbers()` on fields built from each real SDSS field at 3 grid
   resolutions and 3 thresholds (a 3×3 grid of settings).
3. Record β₀, β₁, β₂, χ and runtime for each. Check the exact identity β₁ = β₀ + β₂ − χ
   holds in every single case (it must — it is exact by construction).

**Validation:** the Euler identity holds in all 9×N cases; no crashes, no NaNs; runtime
recorded. **Do NOT** run `compute_kappa_peak_statistic()` on any real data (finding
R-SHEAR, §0.2).
**DoD:** `pipeline/realfield.py` + `pipeline/tests/test_realfield.py` (golden tests on a
tiny hand-built catalog with known counts) + report `docs/WP_R2_REALFIELD_SMOKE.md`.
**STOP AND FLAG if:** the Euler identity fails anywhere, or if you find yourself wanting
to tune the binning to make numbers "look better" — that impulse is the finding.

---

### WP-R3 — Real-data null bank (the highest-value item in this plan)

**Complexity:** medium. **Est:** 2–4 h. **Depends on:** WP-R2 green.
**Why it matters:** the current null bank (`data/nullbanks/`) is synthetic Gaussian —
unrealistically clean. A null built by **randomizing real catalogs** preserves the true
survey geometry, mask, and number density while destroying any genuine spatial
structure. That is the correct null for any future topology statistic, and it is
hypothesis-agnostic, so it stays valid no matter what Stream 1/2 eventually predict.

**Read only:** `pipeline/realfield.py`, `data/nullbanks/README.md`,
`pipeline/tests/test_null.py`, `docs/WP_R2_REALFIELD_SMOKE.md`.

**Do:**
1. Add `scripts/build_realdata_nullbank.py` implementing **two independent**
   randomization schemes (agreement between them is the check that neither is broken):
   - **Shuffle:** keep the exact (ra, dec) positions, randomly permute any per-object
     quantity across objects.
   - **Rotate:** apply a random rigid rotation in RA to all positions, wrapping at 360°.
2. Generate ≥200 realizations per real field, compute β₀/β₁/β₂ for each at one fixed
   setting chosen in WP-R2 (fix it **before** running — write it down first).
3. Store the resulting distributions as JSON + SHA256 in `data/nullbanks/real/`, with a
   README recording the source dataset checksums they derive from.
4. Report the null distribution summary (mean, sd, 90/95/99th percentiles) per field per
   statistic, and confirm the two schemes agree within their own sampling error.

**Validation:** ≥200 realizations each; both schemes produce statistically consistent
nulls; every output file checksummed and traceable to a MANIFEST source row.
**DoD:** script + null bank + `docs/WP_R3_REAL_NULLBANK.md`.
**STOP AND FLAG if:** the two schemes disagree beyond sampling error (that means one is
wrong, and *which* one is a real finding), or if any realization reuses a random seed.

---

### WP-R4 — Sibling-family control harness (practice P4)

**Complexity:** medium. **Est:** 2–3 h. **Depends on:** WP-R0 green. Independent of R1–R3.
**Why it matters:** P4 (`LESSONS_LEARNED.md`) requires sibling K3 families as an
adversarial control: *if every sibling fits equally well, the result is null.* Today
nothing enforces that. This WP builds the harness — it computes no physics, it just
guarantees any future statistic is automatically computed for all siblings at once, so
the control cannot be skipped later.

**Read only:** `checkers/check_C3_sym2.py` (for the params dict shape),
`docs/CRITERION_STATUS.md`, `LESSONS_LEARNED.md` §P4 only.

**Do:** add `pipeline/siblings.py` exposing `SIBLING_FAMILIES` (s7, s10, t103 — read
their parameters **from the committed certificates**, never typed from memory) and
`evaluate_across_siblings(fn, *args)` returning a dict keyed by family. Add tests
proving: all families are evaluated, a missing family raises rather than silently
skipping, and results carry the certificate path each parameter set came from.

**Validation:** `pytest` green; attempting to evaluate a single family without the
control raises. **DoD:** module + tests + a short docstring explaining P4.
**STOP AND FLAG if:** any sibling's parameters cannot be traced to a committed
certificate file (do not fill the gap from memory — that is Lesson L1 exactly).

---

### WP-R5 — Real 3D density field from catalogs (the genuinely missing piece)

**Complexity:** hard. **Est:** 4–8 h. **Tier:** Haiku may build it; **a Sonnet/Opus
session must review before anything downstream uses it.**
**Depends on:** WP-R2, WP-R3 green.

**Read only:** `pipeline/realfield.py`, `scripts/fetch_survey_astroquery.py`,
`data/MANIFEST.md`, `docs/WP_R2_REALFIELD_SMOKE.md`.

**Do:**
1. Extend the fetcher with a **new, separately-manifested** query joining Euclid MER to
   `catalogue.phz_photo_z` on `object_id` (columns `phz_median`, `phz_mode_1`), and an
   SDSS variant with `spectro=True` for spectroscopic redshifts. Same rules: gate check,
   no fallback, checksum + timestamp into the MANIFEST, files to the external disk.
2. Convert (ra, dec, z) → comoving Cartesian coordinates. **The cosmology used is a free
   input, not a prediction** — take Planck-2018 values *from a cited source recorded in
   the module docstring*, never from memory, and state plainly that varying it changes
   the field.
3. Build a 3D density field on a regular grid; feed it to `compute_betti_numbers()`.
4. Report topology per field, **always alongside the WP-R3 null distribution** — never a
   bare number.

**Validation:** photo-z nulls handled explicitly (the `phz_photo_z` sample query returns
`--` for some objects — they must be dropped and counted, never imputed); comoving
conversion unit-tested against at least two independently computed reference distances;
Euler identity holds throughout.
**DoD:** module + tests + `docs/WP_R5_3D_FIELD.md` stating explicitly that every number
in it is engineering-only, with no TEST/FIT label and no comparison to any prediction.
**STOP AND FLAG if:** you are tempted to interpret any topology number as evidence for
or against any hypothesis. That interpretation is T0-only and G1-L-gated, and it is not
what this WP is for.

---

## 2. Sequencing

```
WP-R0 (math, no data) ──┬──> WP-R4 (sibling harness)
                        │
WP-R1 (integrity) ──> WP-R2 (smoke) ──> WP-R3 (null bank) ──> WP-R5 (3D field) [Sonnet review]
```

R0 and R1 are independent and can run in either order. R4 is independent of the data
chain entirely. R5 is the only one needing higher-tier review.

## 3. Definition of done — whole phase

- [ ] Certified mathematics reproduces the committed matrix, negatives included (R0)
- [ ] All 7 real datasets checksum-verified and characterized (R1)
- [ ] Observable machinery exercised on real-derived fields; Euler identity exact
      everywhere; κ-peaks untouched by real data per R-SHEAR (R2)
- [ ] Real-data null bank ≥200 realizations, two schemes agreeing, fully checksummed (R3)
- [ ] Sibling control harness in place, parameters certificate-traced (R4)
- [ ] Real 3D density field built with explicit, cited cosmology; reviewed by a
      higher-tier session (R5)
- [ ] Zero TEST/FIT labels produced anywhere in the phase; G1-L still closed
- [ ] `check_tier_language.py` clean on every commit

## 4. What this phase deliberately does NOT do

- It does not test any hypothesis, Stream 1's or otherwise.
- It does not pin or draft any prediction.
- It does not build a convergence map or run κ-peak statistics on real data (R-SHEAR).
- It does not interpret any measured topology number.

Those steps require a derived, pre-registered observable, which does not exist
(`NO_PREDICTION_BRANCH.md` §8.5) and which the pending Deep Think blind pass
(`DUAL_SCALE_EXPERIMENTATION_BRIEF_2026_07_25.md` §4) may or may not produce.

---

`Generated-by: Fable 5 (T0-delegated), 2026-07-25 | Verified-by: Euclid TAP schema enumerated live (no shear catalogue present — finding R-SHEAR); catalogue.phz_photo_z columns and queryability confirmed live; checker/observable APIs read from source | Reviewed-by: T0 N — pending Xavier`
