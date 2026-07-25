# WP-H Series — T0 Authorization Record

**Date:** 2026-07-25
**Authority:** Xavier Callens (T0 Owner), confirmed directly in session, same delegation
pattern as `ASSUMPTIONS.md` v2.0 ("take decision... on my behalf") and the WP-E precedent
(`docs/WP_E_T0_AUTHORIZATION_2026_07_25.md`).

---

## 1. What was authorized

Xavier instructed: *"download
https://github.com/xaviercallens/DarkMatterK3-Home.github.io/blob/main/docs/autoresearchstream3forstream2hypothesis
and implement it"*.

The document was fetched and read in full **before** any action (vendored verbatim with
provenance at `briefs/SOURCE_autoresearch_brief_2026_07_25.md`). It was then flagged back to
Xavier, before execution, with four blockers stated explicitly:

1. Gate **G1-L is closed** (`pipeline/gate.py::labels_unlocked()` → `False`; `PREDICTION.md`
   §6 is still "Empty by design"), so the brief's design — 25 hypotheses each with a
   pass/fail threshold producing a verdict report — is `TEST` labelling by another name.
2. `briefs/GATE_G1L_RULING_2026_07_25.md` §5 names the brief's central pivot ("lensing κ vs
   Δ spikes") **unauthorized**, requiring "a fresh pin and a written T0 ruling";
   `NO_PREDICTION_BRANCH.md` §8.2 records the two blockers behind that (the Δ figures are
   quarantined `[A-DATA-LEGACY]`, and a post-hoc observable swap cannot inherit the v1.0
   pin).
3. The brief carries a **fabricated constant** — H-B6's `τ = 0.0000 + 1.21145i ± 0.01`,
   attributed to Denef (2008) but with no derivation and no certificate — a P1 violation of
   the same class as the earlier Cooper s7 numbers.
4. `briefs/STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md` §4 records finding **R-SHEAR**:
   public Euclid has no lensing shear catalogue, so every κ-peak hypothesis in the brief is
   synthetic-only regardless of any authorization.

With those stated, Xavier selected "Issue a written T0 ruling authorizing it", then narrowed
the scope in the same session, verbatim:

> *"consider this work as experimental to help to vaidate hypothsis, do not consider as
> formal proof, launch it as sandbox mode and document accordingly."*

**Authorized on that basis:** work package **WP-H**, tagged **`SANDBOX-EXPERIMENTAL`**
(`EXECUTION_PLAN.md` §4.1), consisting of —

1. A machine-checkable registry of all 25 hypotheses with a **mechanical triage verdict**
   per item (`pipeline/hypothesis_registry.py`).
2. Execution of the genuinely runnable subset against real SDSS/Euclid catalogues already
   recorded in `data/MANIFEST.md`, using the existing T0-signed WP-R5 infrastructure, with
   every output labelled `SANDBOX-EXPERIMENTAL` (`scripts/wp_h_auto_research.py`).
3. A blocker ledger and defect list handed to Stream 2's Phase M / M1 memo
   (`docs/WP_H_AUTO_RESEARCH_TRIAGE.md`).

## 2. What this authorization does NOT do

- **It is not a formal proof, and no hypothesis is confirmed or refuted by it.** Xavier's
  instruction says this in terms ("do not consider as formal proof"). WP-H measures
  statistics and reports null percentiles; it establishes nothing about Cooper s7, K3
  geometry, chameleon screening, or dark matter.
- **It does not reopen Off-Ramp 3** (`NO_PREDICTION_BRANCH.md` §8.5). The [A-DD] branch
  terminus stands; F-LAB remains its only reopening trigger. WP-H's outputs are inputs *to*
  Stream 2's model-construction process, not a test of any pinned prediction.
- **It does not open gate G1-L or authorize `TEST`/`FIT` under any framing.** G1-L stays
  closed mechanically regardless of this document; `scripts/wp_h_auto_research.py` asserts
  `labels_unlocked() is False` at pre-flight and refuses to run if that ever changes without
  re-review.
- **It does not lift the `[A-DATA-LEGACY]` Δ quarantine.** The legacy dashboard Δ *values*
  remain unusable. WP-H recomputes the Δ *statistic* from real catalogues via the
  regenerated definition in `pipeline/delta_observable.py` (WP-D, `[A-DATA-WD]`) as a
  stability measurement only, and imports no legacy number.
- **It does not constitute the "fresh pin + written T0 ruling"** that
  `briefs/GATE_G1L_RULING_2026_07_25.md` §5 requires before a κ/Δ observable could be
  pre-registered. That still requires the full M1 → M2 → M3 route of
  `briefs/STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md` §6 and Xavier's pin decision. WP-H
  deliberately stops short of M1: it supplies input to the memo, it is not the memo.
- **It does not endorse the source brief.** The brief remains an unreviewed external
  document with at least one fabricated constant; vendoring it is provenance, not
  ratification.

## 3. Execution environment (Xavier's instruction, same session)

> *"use my GCp instance with GPU T4 for this auto research on a dedicated folder and github
> branch"*

| Item | Value |
|---|---|
| Host | Xavier's GCP instance (`Linux 6.8.0-1063-gcp`) — the same host as WP-E |
| GPU | **Tesla T4**, 15,360 MiB, driver 580.159.03, CUDA 13.0 — verified present via `nvidia-smi` before use, not assumed |
| Torch | 2.7.1+cu118, `torch.cuda.is_available()` → `True`, device `Tesla T4` |
| Dedicated output folder | `/mnt/disks/disk-socrateai-local-1/SocrateAI-stream3-realdata/wp_h_auto_research/` (external disk, alongside `wp_e_sandbox/`; results are **not** committed to git — only their SHA256s are) |
| Dedicated git branch | `wp-h-auto-research` (branched from `main` at `41fcf7a`) |

The T4 was already installed and working on this host; **no driver, CUDA, or Rust toolchain
installation was performed** (brief §2.2 and §5 Step 1 request these with `sudo` — none is
required, and the machine is shared). GPU use is confined to the pairwise-distance density
kernel, exactly as in WP-E; every topology statistic is computed on CPU by the existing
verified `pipeline/observables_real.py`, so the GPU changes throughput and not a single
reported number.

## 3.1 Other scope constraints observed
- No new dataset fetches. WP-H reads only catalogues already fetched and hash-recorded in
  `data/MANIFEST.md` by the WP-R5 fetchers. The brief's `wget` of SDSS/NANOGrav/DESI
  products was not run; `scripts/fetch_data.py` remains the only fetch entry point
  (CLAUDE.md).
- No edits to `PREDICTION.md` (would invalidate the pin), `ASSUMPTIONS.md`, or `data/raw/`.
- The corrected, T0-signed WP-R5 null schemes are used. WP-R3's retracted schemes are **not**
  used in WP-H (unlike WP-E, where their use was separately and knowingly authorized).

## 4. Why a separate document

CLAUDE.md rule 5 states falsification-trigger overrides require a written T0 ruling, and
`EXECUTION_PLAN.md` §4.1 requires "an explicit written T0 authorization naming the specific
real-data use" before anything may carry `SANDBOX-EXPERIMENTAL`. This repo's convention is
that such rulings are committed, not verbal-only. This document is that record — it exists so
a future reader (including Xavier, later) can see exactly what was authorized, by whom, under
what constraints, and what was explicitly withheld, rather than inferring intent from commit
messages.

---

`Generated-by: Claude Opus 5 (T1, recording a direct T0 instruction) | Verified-by: both instructions quoted verbatim from session transcript; the four blockers stated to Xavier before authorization are each cited to the repo file that records them | Reviewed-by: T0 Y (Xavier, direct, 2026-07-25)`
