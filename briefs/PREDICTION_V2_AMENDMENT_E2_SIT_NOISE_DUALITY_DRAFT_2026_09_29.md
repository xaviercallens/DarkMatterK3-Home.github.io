# PREDICTION v2 amendment — E2, superconductor–insulator noise duality (DRAFT, UNPINNED)

**Status:** DRAFT. Not pinned. Carries no `PINNED:` header and must not be merged into `PREDICTION.md`
(pinned, immutable, hook-enforced) by anyone but T0. Written under D12′ (Stream 3 laboratory approach,
`briefs/STREAM2_TO_STREAM3_NOTICE_PR55_MERGED_2026_09_27.md` §5 item 2) and W4.2 of
`briefs/STREAM3_ACTIVATION_2026_09_29.md`. **No dataset has been fetched, named from memory, or looked at**
while writing this; rule 1 of `CLAUDE.md` (no comparison code before `PINNED:`) is observed.

**Guardrail (in force for every sentence of this document and of any result it produces):** the K3
surface is the mathematical shadow of the duality, not its target. No laboratory result under this
amendment is evidence for cooper_s7, cooper_s10, or any Tier A/B certificate in `K3_CRITERIA.md`. Any
sentence that links the self-dual point σ = i or σ = (1+i)/2 to the lattice ⟨2⟩⊕⟨2⟩ is **Tier C** and
carries that marker in the same sentence. Every output is labeled `exclusion` or `FIT`, never `TEST`,
until T0 pins.

---

## 1. Statement to be pre-registered (verbatim candidate text for T0)

> **E2 (charge–phase noise duality at the superconductor–insulator transition).** Let g denote the
> dimensionless conductance of a thin-film or Josephson-array sample and g′ its dual under the
> charge–vortex map. The claim under test is that the low-frequency current (shot) noise measured at g
> equals the voltage (phase-slip) noise measured at the dual point g′ divided by R_Q², with
> R_Q = h/(2e)², and that the two Fano factors map as 2e ↔ h/2e. We do **not** conjecture that any sample
> is exactly self-dual; the claim is the reflection of one noise spectrum into the other across the
> transition, within the tolerance stated in §4.

Everything else in this file exists to make that sentence falsifiable before any data is seen.

## 2. Inputs — `RESERVED` (T0 names them at pin time)

| field | value |
|---|---|
| dataset(s), public products only | `RESERVED` — named by T0 at pin; entered only via `scripts/fetch_data.py`, recorded in `data/MANIFEST.md` with URL, release, SHA256, retrieval date |
| quantity read from each | noise spectral density vs. bias, at stated conductance g; sample resistance; dissipation channel |
| dual pairing rule | g ↔ g′ with g·g′ = 1 in units of 1/R_Q (`RESERVED` if T0 prefers the sheet-resistance form) |

Prior-knowledge disclosure (required by the pin protocol): the directive records that two results in
this area are already public — a 2016 mean-level "reflection" observation and 2022 "dual Shapiro steps".
Both are **known to the authors of this draft by description only**; neither has been fetched, read,
or cited here. Before pin, T0 (or a session T0 delegates) fetches both, hash-pins them under
`docs/literature/`, and records in §2 whether either one *is* one of the datasets of the test (in which
case E2 is at best a `FIT` on it and the TEST-capable data must be different).

## 3. Arms

- **Arm V (dual pair).** Sample pairs (g, g′) related by the duality map. Prediction: reflection within δ (§4).
- **Arm P (non-dual pair, matched).** Sample pairs with the *same* resistance and dissipation as an Arm-V
  pair but *not* related by the duality. Prediction under the symmetry claim: **no** reflection beyond
  the null band.
- **Arm 0 (null).** Shuffled pairings drawn from the pooled samples; establishes the false-positive
  rate of the reflection statistic at the stated threshold.

## 4. Decision rule — thresholds `RESERVED`

Let ρ be the pre-stated reflection statistic (a normalized distance between the measured spectrum at g
and the R_Q²-rescaled spectrum at g′; the exact form is chosen and frozen at pin, not after).

1. Arm V reflects if ρ_V ≤ δ, with δ = `RESERVED` (chosen at pin from the Arm-0 null band at a stated
   false-positive rate α = `RESERVED`).
2. Arm P must **not** reflect: ρ_P > δ at the same α.
3. **Kill rule.** If Arm P reflects as well as Arm V (ρ_P ≤ δ), the symmetry claim is dead as stated; the
   result is filed as an exclusion of E2 and the amendment is closed, not re-tuned.
4. Any change to ρ, δ, α, the pairing rule, or the dataset list after the pin is a tuning event:
   `TUNING_LOG.md` entry, and every downstream comparison is labeled `FIT` forever.

## 5. What a pass would and would not mean

- A pass is a statement about a laboratory duality in a one-parameter family of samples. It would be
  reported as `exclusion`/`FIT` until T0 pins, then as whatever label the mechanical rule assigns.
- It would **not** be evidence for any K3 surface, any Cooper family, any transcendental lattice, or any
  dark-sector statement; we conjecture no such link, and the ledger (CLAUDE.md item 4) blocks one.
- A fail (kill rule) is a success of the programme and gets the same prominence as a pass.

## 6. Freeze procedure (T0's act)

1. T0 fills every `RESERVED` field, fetches and hash-pins the two prior-knowledge items, and decides
   whether this becomes a section of `PREDICTION.md` v2 or a standalone pinned file.
2. Commit; tag `prereg/E2-sit-noise-duality-<date>`; only after the tag exists may `scripts/fetch_data.py`
   touch any E2 dataset. `git log` ordering (tag → fetch → results) is the audit record.
3. E3 (self-dual JJ/QPS circuit) and E4 (Γ₀(2) flow) stay designed appendices until E1 and this file
   both exist in pinned form. E1 exists (`checkers/certificates/E1_aubry_andre_selfduality.json`).

*Generated-by: Claude (Fable 5.1), Stream 3 activation 2026-09-29 | Verified-by: nothing to verify —
this file contains no number that is not a definition or a placeholder | Reviewed-by: N (T0 pins or
rejects)*

---

## Addendum 2026-10-07 — prior-knowledge items located and hash-pinned; E2 is not pinnable as a TEST on public data

1. The two prior-knowledge items are now fetched and hash-pinned (not read) in
   `docs/literature/e2_prior_knowledge/MANIFEST.md`: the 2022 dual Shapiro steps are Shaikhaidarov et al.
   (arXiv:2208.05811, Nature 608) and/or Crescini et al. (arXiv:2207.09381, Nat. Phys. 19); the "2016
   mean-level reflection" is most plausibly Breznay et al. (arXiv:1504.08115, PNAS 113) — **identification
   uncertain**; the reviewer who named it should confirm before pin.
2. **No open SIT noise dataset exists** (search 2026-09-29). The E2 statement is about noise spectra; the
   only open data found (Zenodo 6913393, Crescini et al.) is dc I–V under microwave drive. Therefore E2
   cannot be pinned as a TEST against public data today. Options for T0: (a) hold E2 unpinned until a noise
   dataset is public; (b) re-scope the pre-registration to the dual-Shapiro I–V data (that is E3-adjacent,
   a different claim, and needs its own statement); (c) retire E2 as not posable on public products
   (CLAUDE.md rule 4). This file takes none of these; the `RESERVED` fields stay reserved.
3. Nothing fetched touches `data/` or `pipeline/`; rule 1 still observed.
