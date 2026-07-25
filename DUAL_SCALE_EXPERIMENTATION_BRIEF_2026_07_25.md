# DUAL_SCALE_EXPERIMENTATION_BRIEF_2026_07_25.md — Brief for Deep Think (T0s) Direction and Xavier Sign-off

**Date:** 2026-07-25
**Author:** Fable 5 (T0-delegated), Stream 3
**Requested by:** Xavier Callens — "analyze the real data available... leverage what could be
experimented on the new Dual theory and create a brief for deep think direction and signoff"
**Status:** ANALYSIS COMPLETE. No experiment has started, no data has been fetched, nothing is
pinned. This document requests a Deep Think blind pass on one specific open question (§4) before
any T0 pivot ruling, following the two-model protocol that resolved WP-A.
**Companion actions taken during this analysis (not experimentation, hygiene):** three scripts
found to contain live fabrication defects were quarantined with in-file banners, not deleted —
see §5.

---

## 1. What "the new Dual theory" actually is

It is **not** an external or newly-discovered theory. It is **Stream 1** of this project —
`SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal`, on the external disk at
`/mnt/disks/disk-socrateai-local-1/callensxavier_home_data/`. Its own `VISION.md` (mirrored
canonically there) tables the three-repo structure explicitly:

| Repository | Stream | Role |
|---|---|---|
| `SocrateAI-DualScaleTopologicalUniverseModel-LeanProposal` | 1 — Theory | Formal mathematics (Lean 4) |
| `SocrateAI-Scientific-Agora-K3-DarkMatter` | 2 — Selection | Candidate ranking |
| This repo (`...-Home`) | 3 — Experimentation | Empirical confrontation |

**The "dual scale" is the same cooper_s7/cooper_s10 sibling-operator duality already in this
repo**, not a different geometric construction. Confirmed directly: `Agora/Sequences/
WZCertificates.lean` uses `s7_params = (13, 4, −27, 3)` and `s10_params = (6, 2, −64, 4)`,
identical to `checkers/check_C3_sym2.py:79` here. The framing is: order-2 Picard–Fuchs operator
(elliptic fiber) ↔ dark-matter-halo local EFT; order-3 operator (Cooper s7/s10, symmetric square)
↔ dark-energy global vacuum; wrapped in an F-theory elliptic-fibration picture with a **chameleon**
mediator (not the "Dark Dimension" scenario that Off-Ramp 3 just closed). **This is the same
underlying K3 geometry that just terminated once, re-dressed in different physics language.**
Whether the reasons for that termination transfer is the open question this brief exists to
raise (§4) — I did not resolve it myself; it needs the same two-model treatment WP-A got.

### 1.1 What Stream 1 has actually built (verified directly, not from memory)

- **Genuine self-correction discipline is present.** `Agora/Axioms/PipelineBound.lean` (read in
  full): an axiom asserting a GPU-pipeline bound `S12_max ≤ 1.177` was found vacuous (witnessed
  trivially by `S12_max = 1`, "encodes NO pipeline data"), relocated to a quarantine namespace
  under a documented decision (D3/E-005, Xavier-authorized 2026-07-24), and is explicitly marked
  **"No prose may cite `pipeline_upper_bound`... as data-carrying."** This is the same discipline
  this repo uses (compare: the STREAM3_AUTHORIZATION suspension banner from yesterday). Not a red
  flag — evidence the epistemic-guardrails process is doing its job there too.
- **One live physics-washing pattern, confirmed by direct read.** `Agora/Phenomenology/
  ChameleonRescue.lean` lines 180–227: an M87* superradiance claim hardcodes
  `alpha_bare := 0.155`, `rho_ratio := 1000000` as a structure instance with no derivation in
  the file, then proves `m87_numerical_certificate` — a pure real-arithmetic inequality
  (`10^(1/4) > 2.905`-type statement) on those assumed inputs. Prose nearby calls this
  "consistent with EHT," but the Lean kernel only certifies algebra on numbers that were typed
  in, not a comparison to the actual EHT spin measurement (`a* ≈ 0.90 ± 0.05`, EHT 2019, cited
  correctly as a comment but not consumed by any proof term). Tier C by this project's own
  scheme; the "consistent with EHT" framing is not currently earned.
- **No frozen prediction exists yet.** Stream 1's own `PREDICTION.md`, read directly: `**Status:**
  Draft v1.0`, `**Frozen date:** TBD (target: end of Phase 1, ~2026-09-17)`, "preliminary...
  will be finalized... after careful consultation with astrophysics contacts (OCA Nice, SYRTE)."
  It does list three candidate observables tied to real data — halo-profile log-slope vs.
  weak-lensing (§2.1), PTA spectral index vs. NANOGrav/EPTA (§2.2), Lyman-α P(k) vs. SDSS/DESI
  (§2.3) — but **no worked EFT matching from geometry to a physical number exists yet** for any
  of them (VISION §1.3 there: "[C, unconstructed]"). This mirrors exactly where cooper_s7's
  F5b/Off-Ramp-3 finding started before the swampland-bounds detour.

## 2. Real data actually available (inventory, not analysis)

| Location | Contents | Provenance status |
|---|---|---|
| This repo's `data/` | Empty except labeled-synthetic mock banks (`data/nullbanks/`) | Clean — correctly empty, gate G1 has nothing to leak |
| `data/MANIFEST_S3.md` | Real template listing 7 target datasets (NANOGrav 15yr, EPTA DR2, SDSS weak-lensing, DES Y3, Euclid ERO, SDSS DR12 Lyα, DESI EDR) | **Every row SHA256: TBD, Retrieved: pending** — a plan, not a completed fetch |
| `bulk_astronomy_data/` (external disk) | 100 `sdss_ra*_dec*.csv` files (ra/dec/z only), 39 MB | **Unmanifested** — no README, no checksums, no recorded query/version/date |
| `NANOGrav15yr_PulsarTiming_v2.1.0/` (external disk, two copies, ~2.4–3.0 GB) | Genuine official release: `.par`/`.tim`, real README citing Zenodo DOI 10.5281/zenodo.16051178, Agazie et al. 2023 ApJL 951 L9 | **The one dataset with real provenance on disk today** — but no SHA256 recorded and not yet entered in any MANIFEST here |
| SDSS/Euclid survey imagery/FITS | **None found anywhere on the external disk.** All `.fits` hits are library test fixtures; "euclid" hits are Lean/mathlib or the `astroquery` library, not data | Euclid-observable work (§2.1) has **zero real data to draw on** right now |
| K3-DarkMatter repo `scientific_protocol/datasets/` | `GD1_constraints.csv`, `M87_spin_bounds.csv`, `SPARC_IC2574.csv` — plausible real astrophysical constraint tables | **Unmanifested** — no README/checksum found |

**Bottom line: NANOGrav 15yr pulsar timing is the only dataset on disk today with real, checkable
public provenance (an official DOI'd release).** Everything else is either absent (Euclid) or
present without the manifest/checksum discipline this project's own rules require before any
comparison. This is a data-acquisition-and-manifesting task (WP-S3-01-style engineering), not a
finding that blocks anything — it just means P2/P3 (lensing, Lyman-α) aren't currently
executable and P1 (PTA) is the nearest to executable.

## 3. Prior code and lessons — what's reusable, what's a landmine

`LESSONS_LEARNED.md` (L1–L5) and `V5_SCIENTIFIC_REVIEW.md` (9 findings, 5 gates, institutional
practices P1–P4) are unchanged and still binding; no new lesson type was found beyond what's on
record. **The one documented scale-mismatch failure mode in this repo's history is exactly the
Off-Ramp 3 / gap G-1 finding** (meV–eV KK window vs. Mpc-scale weak lensing) — there is no
second instance on file, which makes it important to check whether the Dual-Scale/chameleon
reframing repeats it (§4) rather than assume it's a one-off.

**Reusable, hypothesis-agnostic:** `pipeline/gate.py` (G1/G1-L), the closure/null test harness
(`pipeline/tests/test_closure.py`, `test_null.py`, `test_comparison.py`, `test_gate.py`), the pin
tool (`scripts/pin_prediction.py`), and today's exact κ-peak/Betti observables
(`pipeline/observables_real.py`). None of this is Cooper-s7-specific; all of it works for any
future pinned observable. `pipeline/D3_batch_runner_phase2.py` is real orchestration with an
honest, gate-enforced kill-switch on its placeholder physics (`_evaluate_sector()` is
`np.random`, and `require_pinned_for_real_data()` refuses to let it run on real data) — reusable
skeleton, not usable as-is.

**Confirmed live landmines — quarantined this session (§5), not previously flagged:**
- `real_euclid_worker.py` — its documented SDSS-fetch fallback path injects a fabricated cluster
  into `discoveries.json` indistinguishable from a real detection when a sector's `ra_min`/
  `dec_min` satisfy a modulo-20 condition. Comment, verbatim: *"Injecter un puits de gravité
  aléatoire (amas) dans certains secteurs pour avoir de superbes découvertes."* This is Lesson
  L5 (`LESSONS_LEARNED.md`), live in committed code today, not a historical artifact.
- `ned_cross_validator.py` — defines `NED_API_BASE` but never calls it anywhere in the file;
  `generate_validation_report()` hardcodes `"VALIDATED AND CONFIRMED"` / `"Ready for
  Publication: YES"` regardless of input. A placeholder masquerading as a completed validation.
- `process_nanograv.py` — genuinely parses real `.par` files for some fields, but silently
  substitutes `np.random.uniform()` for RNAMP/RNIDX when absent, with **no flag in the output
  distinguishing parsed from fabricated values**. Partially real, dangerously so — the real parts
  make the fake parts easy to miss.

None of these three were touched or discovered by any prior Stream 3 session's audits; they
predate the current epistemic-guardrails discipline and were never swept.

## 4. The open question — request for Deep Think blind derivation

**This is the actual ask.** Before any T0 ruling on whether Stream 1's Dual-Scale/chameleon
reframing is worth pre-registering, the following needs the same two-model treatment that
resolved WP-A (`briefs/WP_A_BLIND_REDERIVATION_BRIEF_2026_07_25.md` pattern) — Deep Think should
derive independently, then compare:

1. **Mass/length scale.** From `ChameleonRescue.lean`'s construction (`alpha_bare`, `rho_ratio`,
   the `alpha_effective` density-boost mechanism at lines 130–198), what physical mass or length
   scale does the chameleon mediator imply — is it anchored to the same meV–eV Kaluza–Klein
   window that Off-Ramp 3's gap G-1 found incoherent with Mpc-scale observables, or is it
   genuinely different (e.g., because the chameleon density-boost here is a *different*
   mechanism than the bare-mass argument that killed the Dark Dimension pivot)? **Do not assume
   either answer** — this is exactly the kind of claim this repo's own history says needs
   independent derivation, not inheritance from the prior finding by analogy.
2. **Per-observable scale coherence.** Check the derived scale against each of Stream 1's own
   three candidate observables (§2.1 lensing/Mpc, §2.2 PTA spectral index/light-year-to-parsec
   GW wavelengths, §2.3 Lyman-α P(k)/Mpc) — does the same G-1-style incoherence recur for any,
   all, or none of them?
3. **M87* claim audit.** Is `alpha_bare = 0.155`, `rho_ratio = 10⁶` derivable from the certified
   K3/lattice data (ρ, T, Kodaira type) anywhere in Stream 1 or Stream 2, or is it an assumed
   input dressed as a derived consequence — the same pattern this brief already flags in §1.1?
4. **PipelineBound axiom reach.** Does the disclosed-vacuous `pipeline_upper_bound` axiom (now
   correctly quarantined there) block any content that would otherwise flow into a real
   prediction, or is it decorative exactly like the two axioms already discharged before it?

**If Deep Think's derivation finds the same scale incoherence as G-1**, the honest outcome is
recording that explicitly and this reframing dies alongside the Dark Dimension one — a second
data point for the "this K3 geometry doesn't reach cosmological/PTA scales under any physics
dressing tried so far" pattern, which would itself be a useful, publishable negative finding.
**If it finds genuine coherence**, that opens a real WP-A2-equivalent path, most plausibly
against **NANOGrav 15yr** (§2.2, PTA) since it's the only dataset with real provenance already
on disk — subject to the same circularity-audit discipline that killed the prior lab-scale
re-scope (does the derived PTA target window depend on data that would also be used to test it?).

## 5. Hygiene actions taken during this analysis (not experimentation)

Under standing T0-delegated authority and consistent with this session's precedent (the
`STREAM3_AUTHORIZATION_SIGN_OFF` suspension banner), the three landmine scripts in §3 were given
in-file quarantine banners — **not deleted, not modified in logic** — stating why they must not
be run or cited, and pointing back to this document. This is faithful execution of P1/P4
(`LESSONS_LEARNED.md`), not a scope expansion: L5 is a locked-in institutional lesson and finding
it live in committed code is the kind of thing that gets flagged the moment it's found, the same
way the D-3 brief and the Off-Ramp-2-vs-ruling gaps were flagged on sight in prior sessions.

## 6. What is explicitly NOT being requested or done here

- No data fetch. No `scripts/fetch_data.py` run. No manifest entries created.
- No PREDICTION.md (this repo's, v1.0-PINNED) touched. No new v2.0 draft.
- No claim that Stream 1's theory is correct, viable, or physically anchored — §4 is a genuine
  open question, not a foregone conclusion in either direction.
- No pipeline code written against the Dual-Scale framing. §4's blind derivation is paper-only.

---

`Generated-by: Fable 5 (T0-delegated), 2026-07-25 | Verified-by: three parallel Explore-agent investigations (Dual-theory repo audit, real-data inventory, prior-code/lessons assessment) cross-checked by direct file reads (VISION.md, ChameleonRescue.lean, PipelineBound.lean, PREDICTION.md in the LeanProposal repo; real_euclid_worker.py, ned_cross_validator.py, process_nanograv.py, data/MANIFEST_S3.md in this repo) | Reviewed-by: T0 N — this document IS the request for Deep Think (§4) and Xavier sign-off; not yet reviewed by either`
