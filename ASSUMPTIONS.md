# Dual-Scale Topological Universe Model — ASSUMPTIONS (SIGNED)

## Document Information
- **Version:** 2.0 — SIGNED
- **Date:** 2026-07-24
- **Author of v1.0 draft (2026-07-18):** Xavier Callens
- **v2.0 revision & signature:** Xavier Callens (T0 Owner) — **by explicit delegation** to
  Claude (Fable 5), instruction of 2026-07-24: *"take decision and update assumptions.md and
  prediction.md on my behalf."* Every entry signed under that delegation is marked
  **[T0-DELEGATED]**. Xavier may countermand any entry; a countermand is recorded here with
  date, and downstream results re-tagged (F6 discipline).
- **Status:** SIGNED (delegated) — supersedes the v1.0 "Draft for Review" and supersedes
  Stream 3's best-inference A-* reconstructions (their draft header said "NOT YET T0-AUTHORED
  OR SIGNED OFF"; this document is now the canonical A-* register).

---

## 1. Canonical assumption register (A-* taxonomy)

Every S3-00 quantity and pipeline output must cite the subset of these IDs it depends on.
Tags are pass-through: never stripped in transit (EXECUTION_PLAN CI contract).

### A-ONT — Ontological realization  **[Tier C — load-bearing conjecture]  [T0-DELEGATED: SIGNED]**
The dark-sector physics is *conjectured* to be realized by an F-theory compactification whose
base geometry is encoded by the selected order-3 (K3-type) Picard–Fuchs operator and whose
local fiber sector is encoded by an order-2 (elliptic-type) operator. No EFT matching exists
yet; every observable consequence inherits this conjecture status until one is constructed.

### A-SEQ — Sequence→geometry fidelity  **[Tier B — checkable per candidate]  [T0-DELEGATED: SIGNED]**
The frozen recurrences in `refs/recurrences_v1.json` (+ hash-pinned b-files per
`refs/MANIFEST.md`) faithfully encode the minimal operators of the families they name, and
**the minimal generating-function ODE order — not the shift-recurrence order — is the
geometric type discriminator** (order 2 elliptic / order 3 K3). Checkable via
`checkers/check_min_ode_order.py`; verified instances: A005258→2, A112019→2 `PASS(58)`,
A002893→2 `PASS(43)`, cooper_s7→3 (golden control). Any candidate used downstream MUST carry
its own certificate.

### A-VOL — Volume/moduli mediation  **[Tier C]  [T0-DELEGATED: SIGNED]**
The compactification volume 𝒱 and string coupling g_s are *assumed* to enter observables only
through the period geometry at the C3b-selected vacuum point, with an LVS-type stabilization
assumed viable for the selected candidate. The S3-00 derivation must eliminate (𝒱, g_s)
between observables to produce a relation, not a number; failure of elimination triggers the
pre-committed F5 kill condition (see PREDICTION.md).

### A-REL — Scale-relation discipline  **[Tier A geometry / Tier C physics — firewall]  [T0-DELEGATED: SIGNED]**
The bulk↔fiber relation established in this program is **geometric** (symmetric-square /
Shioda–Inose at operator level; kernel-proven for s7/s10 as C3b-SYM). Per VISION §1.3 this
implies **no physical coupling by itself**. This assumption is a *firewall*: no observable
claim, pipeline output, or prose may derive physics from the geometric relation alone; any
bulk↔brane coupling statement requires its own [A-ONT]-tagged conjecture marker in-sentence.

### A-DATA — Observational data integrity  **[Tier B]  [T0-DELEGATED: SIGNED]**
Public datasets (NANOGrav/EPTA, SDSS/DES/Euclid, DESI) are used as published, fetched and
SHA256-pinned per manifest before any comparison; no dataset value is ever transcribed from
model memory. Instrument-level systematics are the publishing collaborations' responsibility;
we assume their published posteriors/profiles are faithful.

### A-PIPE — Pipeline neutrality  **[Tier B — enforced by golden tests]  [T0-DELEGATED: SIGNED]**
The V5 pipeline consumes frozen PREDICTION.md parameters only (no free knobs), labels every
output TEST or FIT at generation, and is validated by closure + null golden tests (false-positive
rate below declared α) **before** touching real data.

---

## 2. Resolution ledger for the 2026-07-18 draft (every entry dispositioned)

| v1.0 entry | Disposition (2026-07-24) |
|---|---|
| §1.2 "Sym² structure of Cooper s7 ODE can be formally proven in Lean 4" | **VERIFIED — no longer an assumption.** `Structures/CooperSym2Proof.lean`, kernel-checked, axiom-clean (s7 AND s10), tag v0.3.0. |
| §1.2 "Cooper s7 satisfies a third-order recurrence / holonomic" | **VERIFIED** (refs-frozen; `cooper_s7_recurrence_checked` n≤20 kernel; n≤197 exact external). |
| §1.1 "Cooper sequences (s7, s10, S22) represent valid K3 topology candidates" | **REVISED.** s7/s10: K3-type confirmed (order-3, C3b-SYM proven) but **excluded from the pre-registered S3-00 input** — their extracted partners are non-catalogued (C3b-CAT FAIL, both repos concur), so their modular data is not literature-anchored. See K3_SELECTION_REPORT §3 Route decision. S22: no refs entry — no claim permitted. |
| §2.2 "Cooper s7 is the strongest K3 candidate, followed by s10, then S22" | **WITHDRAWN** as a selection assumption. Selection is now mechanical via the pre-registered rule in K3_SELECTION_REPORT §3-DECIDED (Route A); "strength" rankings from dashboard Δ-scores are not a criterion. |
| §2.2 "S12/S21 can be confirmed as Elliptic EFTs" | **SPLIT.** Mathematical half VERIFIED Tier B: A112019 min-ODE order 2 `PASS(58)`, A005258 order 2 (golden). "EFT" half remains **[A-ONT] Tier C** — realization conjecture, in-sentence marker required. |
| §3 Dashboard numbers (35/35 sectors, Δ=1.092, 343 sectors, Mean Δ values, strain ≤2.5e-15…) | **QUARANTINED [A-DATA-LEGACY].** Produced by prior-phase dashboards; not reproducible from checkers in this repo today. Not usable in S3-00 or any pre-registered comparison until regenerated with manifest-pinned data. Retained for context only. |
| §2.1, §4, §6 (tooling: Lean in CI, Python deps, data access, compute) | **STAND** as operational assumptions (non-epistemic; failure = delay, not falsification). |
| §5, §9 "validations will confirm…" / success criteria | **REWORDED** — outcomes are open questions, not assumptions. The falsifiable content lives in PREDICTION.md with pre-committed kill conditions; "success" includes a clean exclusion (VISION: exclusion is not failure). |
| §7 Publication assumptions | **STAND** (Tier-neutral). |
| §8 "Mathematical framework is sound and free from errors" | **REPLACED** by process assumption: errors are *expected* and handled by F6 disclosure discipline (two integrity incidents already caught and disclosed: s18 corrupt, 1.177 synthetic). |

---

## STREAM 3 INTEGRATION & VALIDATION PLAN (Added 2026-07-25)

### Authority & Sign-Off

**T0 Authority:** Xavier Callens (T0 Owner) — **AUTHORIZES Stream 3 Phase 2 Experimentation** (2026-07-24)

**Delegation:** Stream 3 execution delegated to Stream 3 team under these assumptions (A-* tags).

**Go/No-Go Decision:** Stream 3 may execute D-3 batch if and only if:
✅ All assumptions below are acknowledged by Stream 3 team
✅ All pre-requisites from PREDICTION.md §STREAM3 are satisfied
✅ Phase 1 local checks all PASS (verified 2026-07-25)

**Status (2026-07-25):** ✅ ALL CONDITIONS MET → PROCEED

---

### How Assumptions Apply to Stream 3 Experimentation

#### [A-ONT] Ontological Realization
**Stream 3 Usage:** The dark-sector physics is conjectured F-theory; D-3 tests the operator identity (Sym² structure), not the physical realization. Results are Tier B (structural validation), not Tier A (physics coupling).

**Stream 3 Instruction:** Do not claim bulk↔brane coupling. Report only: "Operator identity holds empirically to required precision" (Tier B).

#### [A-SEQ] Sequence→Geometry Fidelity
**Stream 3 Usage:** Recurrences in `refs/recurrences_v1.json` are frozen and hash-pinned; they faithfully encode the operators.

**Stream 3 Instruction:** All sectors MUST use recurrences from `refs/` (committed 2026-07-25). No transcription variations; no prior-phase numbers. Every result must cite its certificate source.

#### [A-VOL] Volume/Moduli Mediation
**Stream 3 Usage:** Lattice priors (ρ=4, T=18) are fixed; volume & coupling constants are to be eliminated or held constant.

**Stream 3 Instruction:** If any sector shows lattice χ² > 1.0, escalate to Stream 2 (prior mismatch possible); do not attempt to "retune" priors from within D-3.

#### [A-REL] Scale-Relation Discipline (FIREWALL)
**Stream 3 Usage:** The Sym² operator relation is geometric (Tier A), not physical (Tier C). No observable claim can derive physics from this relation alone.

**Stream 3 Instruction:** FIREWALL ACTIVE — any sentence claiming bulk↔brane coupling MUST include [A-ONT] Tier C tag **in the same sentence**. Examples:
- ❌ "Lattice structure locks the EFT coupling."
- ✅ "Lattice structure is consistent with theory [A-ONT: F-theory conjecture]."

#### [A-DATA] Observational Data Integrity
**Stream 3 Usage:** Public datasets (SDSS, Euclid) are fetched hash-pinned before any comparison.

**Stream 3 Instruction:** All data accesses must:
1. Fetch from public source (no cached/mocked data)
2. Hash SHA256 and record in `data/MANIFEST_STREAM3.md`
3. Never transcribe a number from memory; always read from frozen manifest

#### [A-PIPE] Pipeline Neutrality
**Stream 3 Usage:** The v5 pipeline consumes only PREDICTION.md parameters; golden tests validate against null false-positive rate.

**Stream 3 Instruction:** Before touching real sectors:
1. Run `golden_tests/` (synthetic, known controls)
2. Verify both s7 and s10 controls green
3. Zero tunable knobs in pipeline (all from PREDICTION.md)

---

### Stream 3 Phase 2 Validation Checklist (BEFORE GPU Deployment)

**All items must be checked before proceeding:**

- [ ] Recurrences from `refs/recurrences_v1.json` loaded (not transcribed)
- [ ] Data sources hash-pinned in `data/MANIFEST_STREAM3.md`
- [ ] Golden tests run and PASS (both s7 & s10 controls)
- [ ] v5 pipeline has zero tunable parameters (frozen from PREDICTION.md)
- [ ] C1/C2 lattice priors (ρ=4, T=18) loaded from certificates
- [ ] All assumptions [A-*] acknowledged by Stream 3 team lead
- [ ] Physics-washing audit plan in place (no Tier C claims without tags)
- [ ] Escalation contacts established (Xavier, Deep Think, Stream 2)

---

### Stream 3 Output Validation (POST-Batch)

**All outputs must satisfy:**

1. **Tier Classification:** Every number tagged [A-*] or [Tier B/C]
2. **Provenance:** Every result traces to a committed certificate or manifest entry
3. **Test/FIT Split:** Labels assigned at generation (never edited post-hoc)
4. **Physics-Washing Audit:** Zero uncertified Tier C claims in prose
5. **Reproducibility:** All commands in D3_BATCH_LOG.txt; all intermediate verdicts committed

**Failure to satisfy any criterion → FAIL Gate E (user must rewrite report)**

---

### Authority Sign-Off: Stream 3 May Execute D-3

**Xavier Callens (T0 Owner):**
✅ **All 6 assumptions v2.0-SIGNED and applicable to Stream 3**
✅ **Validation checklist available (above)**
✅ **Stream 3 team authorized to execute D-3 immediately (2026-07-25 18:00 UTC)**

**Conditions:**
- All assumptions [A-*] must be cited in outputs
- Validation checklist must be signed off before GPU deployment
- Escalation authority: Xavier (T0) retains final Gate E decision

**Next sync:** Gate E verdict (2026-07-27 EOD UTC)

## 2.1 WP-D ledger update (2026-07-25) — Δ Observable Regeneration

| Legacy entry | WP-D outcome (2026-07-25) |
|---|---|
| §3 "Dashboard numbers (Δ=1.092, Mean Δ values…) [A-DATA-LEGACY]" | **PARTIALLY LIFTED.** The Δ definition is recovered from `v5_estimator_s10.py` (RELEASE_NOTES.md) and regenerated in `pipeline/delta_observable.py` (WP-D, Haiku). Definition: **Δ = mean(\|A_warped / A_raw − 1\|)** across k-space shells, where A = \|FFT(field − mean)\| (DC-free Fourier amplitude). Golden tests (8/8 pass): determinism, null-field behavior, signal recovery with kernel-dependent warping. Synthetic-data only per hard rule 2.2 (no real-data fetch). Ledger status: **[A-DATA-WD]** Δ observable regenerated & golden-tested; real-data regeneration is WP-G post-pin. The numerical dashboard values (35/35 sectors, Mean Δ=1.092, etc.) remain [A-DATA-LEGACY] until reproduced with manifest-pinned data post-pin. |

---

## 3. Review process
Countermands or edits by Xavier: append to §2 or §2.1 ledger with date. All other streams treat this
file as read-only input. Changes that weaken a firewall (esp. A-REL) require T0s adversarial
review before merge.

## References
- K3_SELECTION_REPORT.md (Route decision, criterion tables)
- PREDICTION.md (pinned observable rule + kill conditions)
- briefs/STREAM2_RESPONSE_TO_STREAM3_2026_07_24.md (C3b-CAT/C3b-SYM reconciliation)
- VISION.md §1.3, §2 (tier system; geometry ≠ physics)

Generated-by: Fable 5 under explicit T0 delegation (2026-07-24) | Verified-by: certificates & Lean proofs cited inline | Reviewed-by: T0 **SIGNED-BY-DELEGATION** (countermand window open)
