# WP-H — Auto-Research Hypothesis Triage (SANDBOX-EXPERIMENTAL)

**Date:** 2026-07-25
**Executor:** Claude Opus 5 (T1)
**Tag:** `SANDBOX-EXPERIMENTAL` — see `EXECUTION_PLAN.md` §4.1 for the label definition
**Authorization:** `docs/WP_H_T0_AUTHORIZATION_2026_07_25.md` (Xavier, direct, 2026-07-25)
**Source triaged:** `briefs/SOURCE_autoresearch_brief_2026_07_25.md`
(sha256 `19eafed983e75523…`, vendored verbatim, unreviewed external input)
**Compute:** Xavier's GCP instance, Tesla T4 (driver 580.159.03, torch 2.7.1+cu118)
**Branch:** `wp-h-auto-research` · **Results:**
`/mnt/disks/…/wp_h_auto_research/wp_h_results_2026_07_25.json`
(sha256 `eb15a63953a4888a132f846589ecfc5579b3b0d95752955efc1ae62c6b4f11c4`)
**Status:** ✅ COMPLETE

> ⚠️ **Not `TEST`, not `FIT`, not a formal proof, and no hypothesis is confirmed or refuted
> here.** Gate G1-L is closed (`pipeline/gate.py::labels_unlocked()` → `False`), F5b fired,
> and **no derivation connects Cooper s7 to any statistic in this document**. Every number
> below is a description of four galaxy catalogues. Off-Ramp 3
> (`NO_PREDICTION_BRANCH.md` §8.5) is unaffected.

---

## 1. What was asked, and what was done

The instruction was to download and implement an auto-research document from the
`DarkMatterK3-Home.github.io` repo. That document proposes 25 hypotheses, ~11 new validation
scripts, GPU/Rust/driver installation, fresh SDSS/Euclid/NANOGrav/DESI downloads, and a
`*_REPORT.md` pass/fail verdict per hypothesis.

Implementing it as written was not possible: producing per-hypothesis pass/fail verdicts is
`TEST` labelling, which gate G1-L forbids. Xavier authorized the work instead as
`SANDBOX-EXPERIMENTAL` — *"consider this work as experimental to help to vaidate hypothsis,
do not consider as formal proof, launch it as sandbox mode and document accordingly."*

So each hypothesis was given a **mechanical triage verdict** against real repo state
(`pipeline/hypothesis_registry.py`), the genuinely computable subset was executed against
already-manifested catalogues, and the rest produced a blocker ledger for Stream 2. The
registry is merge-blocking-tested (`pipeline/tests/test_hypothesis_registry.py`, 25 tests).

**A `RUNNABLE` verdict means only that the named statistic can be computed.** It does not
mean the hypothesis is testable. Every runnable record carries a mandatory non-empty
`claim_gap` field stating what computing it does *not* establish, and that text is copied
into the results JSON alongside the numbers so the caveat cannot be separated from them.

---

## 2. Triage outcome

26 records: the brief's consolidated list (24 — the brief calls it 25, see §4.6) plus two it
lists only in its thematic sections (H-K3-3, H-CM-5).

| Verdict | Count | Meaning |
|---|---|---|
| `RUNNABLE` | **6** | Statistic computable from manifested data with verified code |
| `BLOCKED_DATA` | **9** | Named dataset does not exist in `data/MANIFEST.md` and is not obtainable |
| `BLOCKED_PROVENANCE` | **7** | Fabricated/untraceable constant, contradicted premise, or circular threshold |
| `OUT_OF_SCOPE` | **4** | Pure theory — belongs to Stream 2/1, no empirical content |

### 2.1 Runnable (6)

| ID | Brief's claim | What was actually computed |
|---|---|---|
| H-A1 | β₁ > β₀ + β₂ in cosmic web | β₀/β₁/β₂ on 4 real fields × 4 absolute thresholds |
| H-B2 | β₂ suppressed in voids vs ΛCDM | β₂ density-split contrast + null percentiles (no ΛCDM operand exists) |
| H-B9 | Δ spikes stable across sectors, σ_Δ<0.1 | σ_Δ across 4 fields, threshold **reported not applied** |
| H-B10 | Topology scale-dependent over 0.22–0.27 Mpc | β₁/β₂ vs grid resolution, bin sizes reported in Mpc |
| H-C4 | ΛCDM mock matches β₁/β₂ | Real vs T0-signed null bank, percentile ranks |
| H-C5 | ΛCDM mock matches β₂ | Same, β₂ only |

### 2.2 Blocked — the four recurring reasons

- **R-SHEAR (κ peaks):** H-B5, H-B8, H-B11, H-CM-5. Public Euclid has no lensing shear
  catalogue (`briefs/STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md` §4). `compute_kappa_peak_statistic`
  exists and is golden-tested but has no real map to consume. This is the brief's single
  most-repeated criterion and none of its instances can run.
- **Δ quarantine `[A-DATA-LEGACY]`:** any hypothesis comparing against the legacy dashboard
  Δ figures (`ASSUMPTIONS.md` v2.0-SIGNED §2, `NO_PREDICTION_BRANCH.md` §8.2).
- **Absent datasets:** NANOGrav/EPTA (H-B4, H-B14), tidal streams + JWST (H-B3, H-C2),
  DESI. The 7 manifested datasets are SDSS + Euclid catalogues only.
- **Absent models:** "Chameleon EFT", FDM, SIDM, f(R), and a ΛCDM N-body mock are all named
  as comparison operands; none is implemented in this repo.

---

## 3. Results of the runnable subset

All on the four WP-R5 redshift fields, SHA256-verified against `data/MANIFEST.md` before
use. Settings inherited from WP-R5/R7 rather than chosen here: `nbins=8`, 50 null
realizations, absolute thresholds (×mean density) not percentiles (WP-R7 §4), and the
corrected T0-signed null schemes (WP-R3's retracted schemes are **not** used).

### 3.1 H-A1 — β₁ > β₀ + β₂ holds in 1 of 16 (field, threshold) cells

| Field | thr 0.5 | thr 1.0 | thr 1.5 | thr 2.0 |
|---|---|---|---|---|
| `euclid_z_edf_north` | β=(1,1,1) ✗ | (1,1,0) ✗ | **(1,2,0) ✓** | (1,0,0) ✗ |
| `euclid_z_edf_fornax` | (1,0,1) ✗ | (1,1,0) ✗ | (1,0,0) ✗ | (1,0,0) ✗ |
| `euclid_z_edf_south` | (1,0,0) ✗ | (1,0,0) ✗ | (2,0,0) ✗ | (2,2,0) ✗ |
| `sdss_z_coma_cluster` | (5,0,0) ✗ | (5,0,0) ✗ | (5,0,0) ✗ | (5,0,0) ✗ |

*(β = (β₀, β₁, β₂); ✓ = β₁ > β₀+β₂ satisfied.)*

**Read this as a statement about resolution, not about the model.** At `nbins=8` the fields
sit in the percolation regime WP-R5 §7 identified: β₀ is pinned at 1 for the Euclid cones,
and β₁/β₂ are 0–2. These are not the rich filament counts the brief's premise (Cautun et al.
2014) refers to; those come from surveys with vastly larger contiguous volume. The statistic
is in a degenerate corner here, so the ✗s carry no evidential weight either way — and
critically, **even a clean ✓ would not have supported H-A1**, because β₁ > β₀+β₂ is a
generic property of filamentary point sets, reported for ΛCDM itself.

### 3.2 H-B10 — strong scale dependence, but far above the claimed window

`euclid_z_edf_north`, threshold 1.0×mean:

| nbins | transverse bin | radial bin | β₀ | β₁ | β₂ |
|---|---|---|---|---|---|
| 4 | 12.08 Mpc | 2047 Mpc | 1 | 0 | 0 |
| 6 | 8.05 Mpc | 1365 Mpc | 1 | 0 | 0 |
| 8 | 6.04 Mpc | 1024 Mpc | 1 | 1 | 0 |
| 12 | 4.03 Mpc | 682 Mpc | 2 | 10 | 4 |
| 16 | 3.02 Mpc | 512 Mpc | 6 | 37 | 18 |

β₁/β₂ vary strongly with resolution (0 → 37 / 0 → 18), so the *stated* criterion ("β₁/β₂
vary with scale") is satisfied — trivially, as it would be for any point process.

**The substantive finding is the scale itself.** The accessible transverse bin sizes are
**2.5–12 Mpc**, one to two orders of magnitude *coarser* than the 0.22–0.27 Mpc window the
brief names, and the radial bins are 500–2000 Mpc because the photo-z cones are Gpc-deep
with ~2000 objects. The one field reaching sub-0.27 Mpc transverse bins is
`sdss_z_coma_cluster` (0.016–0.062 Mpc), which has 50 objects and shows β₁=β₂=0 at every
resolution — no topology to measure. **There is no configuration in this data where the
brief's stated scale window and a non-degenerate statistic coexist.** This is the binding
constraint for Stream 2 and it tightens WP-R6's envelope rather than restating it.

### 3.3 H-B2 / H-C4 / H-C5 — null percentiles, mostly degenerate

β₂ density split (0.5× vs 2.0× mean) with percentile rank against 50 nulls per scheme:

| Field | β₂ low | β₂ high | pct low (z-shuffle / CSR) | pct high |
|---|---|---|---|---|
| `euclid_z_edf_north` | 1 | 0 | 46.0 / 32.0 | 0.0 / 0.0 |
| `euclid_z_edf_fornax` | 1 | 0 | 74.0 / 62.0 | 0.0 / 0.0 |
| `euclid_z_edf_south` | 0 | 0 | 0.0 / 0.0 | 0.0 / 0.0 |
| `sdss_z_coma_cluster` | 0 | 0 | 0.0 / **None** | 0.0 / **None** |

`None` means the null distribution had **zero variance**, so a percentile against it is
undefined — reported as `None` rather than as 0 or 100, which would have been a fabricated
number. The real β₂ values sit comfortably inside the null distributions (32nd–74th
percentile where a percentile exists at all): **the real fields are not distinguishable
from structure-destroying randomizations by β₂ at this resolution.**

Note the control is CSR/z-shuffle randomization, **not** a ΛCDM N-body mock — the repo has
none. A percentile against CSR is a materially weaker statement than the brief's H-C4/H-C5
intend, and substituting one silently would have been the misrepresentation.

### 3.4 H-B9 — σ_Δ = 0.0339 (and a degeneracy caught mid-run)

| Field | Δ (identity kernel) | Δ (generic warp) |
|---|---|---|
| `euclid_z_edf_north` | 0.000000 | 0.860622 |
| `euclid_z_edf_fornax` | 0.000000 | 0.855207 |
| `euclid_z_edf_south` | 0.000000 | 0.873010 |
| `sdss_z_coma_cluster` | 0.000000 | 0.939875 |

**σ_Δ = 0.033930**, mean Δ = 0.882178. The brief's 0.1 threshold is **reported, not
applied** — evaluating against it would be a pass/fail verdict, and the threshold is
unprovenanced besides.

**Disclosed defect, found and fixed during this WP.** The first run passed
`kernel_func=None`, which sets `warped == raw` and makes Δ **identically zero by
construction** — the module's own test `test_delta_null_field_with_identity_kernel_is_zero`
asserts exactly that. It produced σ_Δ = 0.000000 across all four fields, which read as
flawless stability and was in fact a tautology. This is the same no-op failure mode that got
WP-R3's null bank retracted (`docs/FINDING_R_NULLDEGENERATE_2026_07_25.md`). The executor
now computes both branches, asserts the identity branch is zero as a standing degeneracy
guard, and **raises** if the warped branch is constant across four different real fields.
The warp kernel `k(ρ) = 1/(1 + ρ/ρ̄)` is a generic screening-*shaped* stand-in, not an EFT
and not the s7/s10 kernel — it encodes no model and no constant needing provenance.

### 3.5 GPU

The T4 computed the 3D histograms for the null banks; all topology stayed on CPU in the
existing verified `pipeline/observables_real.py`. Before use, the GPU field was checked
against the numpy field on every one of the four catalogues: **exact match** (`np.array_equal`,
max |diff| = 0.0), and the run aborts if that ever fails. The GPU changed throughput and not
a single reported number.

---

## 4. Defects found in the source brief

Reported because the brief is being circulated as a Stream 2 input and these would propagate.

**4.1 A fabricated constant (P1 violation).** H-B6 states the 7-brane coupling as
`τ = 0.0000 + 1.21145i ± 0.01`, to six significant figures, attributed to Denef (2008)
`hep-th/0801.1074`. That is a general review of F-theory 7-brane physics and fixes no such
value for this or any specific compactification; no certificate in `checkers/` contains it.
This is the same defect class that invalidated the earlier Cooper s7 constants. A regression
test (`test_fabricated_7brane_tau_stays_blocked`) now prevents the value being reimported.
H-K3-3's `τ_imag ≈ 0.972` is a second instance.

**4.2 A circular threshold.** H-B1's "screening radius r_s ≥ 0.27 Mpc", attributed to Brax
et al. (2012), is numerically this repo's own *measured survey resolution floor*
(`docs/WP_R6_SURVEY_SCALES.md`). A prediction equal to the finest scale the instrument can
resolve cannot be failed: nothing below it is observable, so the test only ever passes. This
is the failure mode that ended WP-A2 (`WP_A2_CIRCULARITY_AUDIT.md`). §3.2 above shows the
data is in fact ~10–40× coarser than that floor in the fields that have any topology at all.

**4.3 A premise contradicted by Stream 2's own certificate.** H-A5 asserts **Type III**
fibres in Cooper s7. `C1loci_cooper_s7_partner.json` records **Type II**. The difference is
load-bearing: Type II carries no perturbative gauge algebra, which *is* the a₁ "Type II veto"
wall (`briefs/GATE_G1L_RULING_2026_07_25.md` §4). The brief asserts the fibre type that
would dissolve the wall, without a certificate.

**4.4 Circular self-citation.** H-B7 cites "V4C Pipeline" as its own theoretical basis. No
V4C pipeline exists here; the legacy V4/V5 dashboard scripts it likely means are the
deprecated, fabrication-flagged ones, whose outputs are quarantined `[A-DATA-LEGACY]`.

**4.5 Confirmation-shaped "null tests".** H-C1/H-C2/H-C3 each state the expected outcome as
the *alternative* model failing. A null test that the favoured model cannot fail is not a
null test. Note also H-C3's criterion (β₁ ≤ β₀+β₂ for f(R)) is the exact negation of H-A1's,
with neither derived — the pair is a coin flip presented as two predictions. Genuine
adversarial control is served by `pipeline/siblings.py` (P4), which wires **s7 and s10 only**
— not the 3+ families the brief's usage example implies.

**4.6 Miscount and triple-counting.** The brief calls its consolidated list "25 hypotheses";
it contains 24. The same κ-peak alignment criterion appears three times (H-B5, H-B8, H-CM-5)
under three different theoretical motivations — one measurement asked to support several
distinct claims, which no single number can do.

**4.7 Infrastructure requests that were declined.** Driver/CUDA/Rust installs via `sudo` on
a shared machine (unnecessary — the T4 already works); `wget` of SDSS/NANOGrav/DESI outside
`scripts/fetch_data.py` (CLAUDE.md names it the only fetch entry point). Neither was run.

---

## 5. Hand-off to Stream 2 (Phase M, M1 memo)

WP-H is **hypothesis input only** — it is not the M1 memo and does not start it
(`briefs/STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md` §6: M1 is the only authorized step,
and it is Stream 2's).

What Stream 2 can take from this:

1. **The scale wall is tighter than WP-R6 stated.** §3.2: no configuration in current data
   gives both the 0.22–0.27 Mpc window and a non-degenerate β₁/β₂. Deep fields have 2.5–12
   Mpc transverse bins; the one field reaching sub-0.27 Mpc has 50 objects and zero
   topology. A mechanism whose signature lives at the resolution floor is not reachable with
   this data, whatever its theoretical merits.
2. **β₂ does not currently separate real fields from randomized ones** (§3.3, 32nd–74th
   percentile). Any proposed β₂-based observable needs to argue for a regime where it does.
3. **17 of the brief's hypotheses are unreachable**, with the specific reason recorded per
   record in `pipeline/hypothesis_registry.py`. Nine fail on data that does not exist; the
   κ-peak family fails on R-SHEAR and cannot be rescued by any amount of compute.
4. **Do not import the brief's constants.** §4.1 — two are fabricated, one is circular.
5. Anything from here reaching `PREDICTION v2.0` must go through M1 → M2 → M3 and Xavier's
   pin decision. WP-H results **cannot be inherited directly as a result**
   (`EXECUTION_PLAN.md` §4.1).

---

## 6. Reproduction

```bash
git checkout wp-h-auto-research
python3 scripts/wp_h_auto_research.py --dry-run   # triage table, touches no data
python3 scripts/wp_h_auto_research.py             # full run (T4 GPU; --cpu to disable)
python3 -m pytest pipeline/tests/                  # merge-blocking suite
```

Pre-flight asserts G1 open (pin valid) and **G1-L closed**; the run refuses to proceed if
G1-L ever opens, so a future gate change forces re-review instead of silent relabelling.

---

`Generated-by: Claude Opus 5 (T1) under T0 authorization of 2026-07-25 | Verified-by: GPU/CPU exact-agreement check on all 4 fields at runtime; catalogue SHA256s verified against data/MANIFEST.md before compute; Δ degeneracy guard added after a self-caught no-op; pipeline/tests/test_hypothesis_registry.py (25 tests) + full merge-blocking suite executed | Reviewed-by: T0 N — pending Xavier`
