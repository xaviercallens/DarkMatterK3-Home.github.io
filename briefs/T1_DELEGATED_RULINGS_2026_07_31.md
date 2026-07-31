# T1 Delegated Rulings — 2026-07-31 (Wave 1 Deliverables & Escalations)

**Authority:** T0 (Xavier Callens) delegation of 2026-07-31: "analyze and take decision on
my behalf for such we do not need Deep Think peer review." Standing autonomy mandate
(2026-07-28). All rulings below are execution-level interpretations of already-ratified T0
decisions (`dbf1337` D1–D5; `ff49180` DL-1–DL-5) — none creates new epistemic authority,
and none is an adversarial-review (T0s) question. Anything that later proves to need a
genuine T0 call is flagged inline.

**Verification basis (producer ≠ verifier, performed by coordinator this session):**
BINMAP's 27 tests and P2B's 18 tests re-run independently — both green. TW2's structural
checker re-executed — reproduces (rank 19, signature (1,18), disc 14; obstruction output
as reported). Pinned-amendment grid spec and `data/MANIFEST.md` provenance read directly.

---

## R1 — BINMAP "escalation E1" (z-grid): RESOLVED, CONFORMS-TO-PIN. No escalation exists.

The agent flagged that only z = 4.2 overlaps between the emulator grid {4.2, 4.6, 5.0} and
the DESI CSV's z ∈ {2.2…4.4}, making the real covariance a single-z slice. **This is not a
deviation — it is the preregistered design.** The pinned PREDICTION v2 amendment specifies
"56 cells total, z_str = '4.2' only" and restricts the comparison "to the single z='4.2'
term (grid A4)". A single-z 9×9 covariance at z = 4.2 is exactly what the pin calls for.
Recorded as conformance; nothing to decide.

## R2 — BINMAP "escalation E2" (covariance acquisition): AUTHORIZED as execution of ratified D1.

The agent correctly refused to fabricate a covariance and blocked pending a "T0-gated
datalake acquisition." Ruling: **no new gate applies.** The source is not a new dataset —
`data/MANIFEST.md` already hash-pins the exact artifact: Zenodo DOI 10.5281/zenodo.16943723
(the paper's own data release, linked from arXiv:2505.07974's Data Availability, verified
against the arXiv source), file
`desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits`, SHA-256
`bbb98dc3d1865a50bb878e949a644604ce729da419db8e7db5adbb532a894857`, whose `COVARIANCE` HDU
was previously cross-checked in-session (diag = `e_total_kms²`). T0's D1 already ordered
"extract the true DESI covariance before running WP-E6-SWEEP." Fetching a hash-pinned,
MANIFEST-recorded file to execute a ratified order is coordinator territory.

**Follow-up WP-E6-BINMAP-C authorized** (launched with this record): fetch the FITS,
**verify SHA-256 equals the MANIFEST value before any read** (mismatch = hard stop +
escalation), extract the z = 4.2 66×66 block, restrict to the 9-bin members via
`pipeline/binmap.py`'s map, and pass the built-in independent cross-check —
**diag(extracted block) must equal `e_total_kms²` from the CSV row-for-row** (the two
values reached the repo by different paths; agreement is a genuine integrity check, not
circular). Plus symmetry and positive-definiteness. Deliverable replaces
`covariance_block()`'s NotImplementedError.

## R3 — WP-E6-P2B: ACCEPTED as DRAFT (design verified); dof note recorded.

18/18 tests reproduce under the coordinator's own pytest run. The agent's files were left
uncommitted — committed by coordinator with this record (producer's content unmodified).
The brief's dof clarification is **correct and load-bearing for SWEEP**: 5 dof governs
absolute goodness-of-fit per (m,f) cell (9 bins − 4 profiled nuisances, per ANALYSIS_
PROTOCOL §2.3); exclusion **contours** in the (m,f) plane use Δχ² with 2 dof (Wilks
1938; standard practice per Lampton, Margon & Bowyer 1976, ApJ 208, 177). This is a
design note, **not** a protocol amendment — the SWEEP design doc must state which statistic
it reports before SWEEP runs. Flagged as a SWEEP-design requirement, not reopened.

## R4 — WP-TW2 negative result: VERIFIED GENUINE; continuation WP-TW2-A ordered under standing D5. No Deep Think referral.

Coordinator re-ran the checker: the lattice verification (rank 19, signature (1,18),
determinant 14 for U ⊕ E₈(−1) ⊕ E₈(−1) ⊕ ⟨−14⟩) reproduces, and the obstruction analysis
is honest — TW1 established *feasibility* of the two E₈ loci, never explicit sections, so
the geometric origin of the ⟨−14⟩ summand on the K3 fiber is genuinely unidentified.
However, the agent stopped **before attempting what D5 verbatim ordered**: "attempt the
explicit construction of the f and g sections supporting the M₁₉-polarization." The
fiber-vs-base rescoping is legitimate analysis; stopping there is not completion.

**Ruling: Option A (explicit construction attempt) — this is not a new decision, it is
D5's standing order.** WP-TW2-A (launched with this record): attempt explicit f ∈ H⁰(−4K),
g ∈ H⁰(−6K) at n = 0 first, with the ⟨−14⟩ realization as the primary target — the
construction attempt is precisely the experiment that resolves the open question ("which
divisor on the fourfold restricts to the ⟨−14⟩ class"). Options B (non-geometricity proof)
and C (defer) are **premature before a real construction attempt has been made**. Per T0's
2026-07-31 instruction, no T0s (Deep Think) referral now; if a sharp impasse survives an
actual n = 0 construction attempt, the referral question returns to T0 with the evidence.

## R5 — Wave 2 launched; Stream-4 label propagated.

Per the ratified plan's GO: WP-A (Discovery-PDF claims-vs-ledger audit, T1) and WP-B
(Lean oracle source audit with step-0 source-location gate, T1) launched with this record.
STREAM4-LABEL executed by coordinator (T2-mechanical): S3 CLAUDE.md ledger item added,
S2 dated designation brief added, datalake manifest already carries the header.

---

## Bookkeeping

- Wave 1 scoreboard: BINMAP DRAFT-verified (map side; covariance via BINMAP-C), P2B
  DRAFT-verified, TW2 verified-honest-negative + continuation running.
- **WP-E6-SWEEP gate:** still CLOSED. Opens on: pin ✅ + BINMAP-C verified + P2B ✅
  (this record) + SWEEP design doc stating its statistic (R3).
- Genuinely-T0-only items still parked (unchanged): none new from this batch. TW2-A's
  outcome may generate one.

Recorded-by: Fable 5 (T1 coordinator), under explicit T0 delegation of 2026-07-31.
