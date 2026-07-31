# T0 Ratification & Directives — 2026-07-31 Datalake Governance (RECORD)

**Status:** RATIFIED. This document records, verbatim, T0's (Xavier Callens) rulings on all
five items of `T0_DECISION_BRIEF_DATALAKE_2026_07_31.md` (commit `5a33666`, release
v5.10.0), followed by the Fable (T1 coordinator) review annotations made before execution.

**Execution status at time of this record: PLAN ONLY.** Per T0's explicit instruction with
this ratification, the execution plan is proposed and committed
(`EXECUTION_PLAN_2026_07_31_DATALAKE_GOVERNANCE.md`) but **nothing is launched** — no
scripts deployed, no daemon restarted, no agents started — pending T0's GO on the plan and
its T1/T2 model-tier assignments.

**Decision summary:** DL-1 APPROVED (Option A: manifest protocol, GCS staging-only,
firewall locked) · DL-2 APPROVED (Planck plik_lite P1; DES-Y3 conditional; IPTA DR2
DEFERRED/struck) · DL-3 APPROVED (no contact before WP-E6-SWEEP + per-channel amendment;
Stream-4 designated EXPLORATORY SANDBOX) · DL-4 APPROVED (immediate QUARANTINE; audit
WP-A + WP-B commissioned) · DL-5 APPROVED (repairs under autonomy mandate).

---

## Part I — T0 directives (verbatim)

> **To:** Fable 5 (T1 Coordinator) & The SocrateAI Agora
> **From:** T0 (Xavier Callens)
> **Subject:** Ratification of Datalake Audit, Data Acquisition, and Quarantine Actions
>
> I have reviewed the `T0 Decision Brief` (2026-07-31). The coordinator's verification
> pass is exemplary. The hallucinated 9-row status table is a severe epistemic failure by
> the agent session that produced it. The swift detection and quarantine of these
> fabricated claims proves our guardrails are functioning exactly as intended.
>
> Below are my formal decisions and execution authorizations.
>
> ### DL-1. Datalake Governance
> **Decision: APPROVED (Option A).**
> * **Rationale:** Google Cloud Storage (GCS) is officially admitted as a staging/mirror
> layer, but it does NOT bypass the `data/MANIFEST.md` repository hook.
> * **Action:** Deploy `scripts/audit_datalake.py`. Implement the `GCS_DATALAKE_MANIFEST.md`
> with strict cryptographic (SHA-256) tracking.
> * **Epistemic Enforcement:** The firewall between exploratory (AlphaEvolve/Vertex) and
> confirmatory (WP-E6-SWEEP) channels is locked. AlphaEvolve outputs are explicitly labeled
> **PHENOMENOLOGICAL CONVERGENCE**. They cannot be used as empirical proof.
>
> ### DL-2. The Three Absent Datasets
> **Decision: APPROVED.**
> * **Rationale:** We do not hoard data we cannot properly test.
> * **Action (P1):** Acquire Planck 2018 high-ℓ (`plik_lite`). This is the gold standard
> for early-universe amplitude calibration and is required.
> * **Action (P2 & P3):** DES-Y3 is conditional (Acquire only). IPTA DR2 is DEFERRED
> (strike from manifest).
>
> ### DL-3. Multi-Probe Contact Protocol
> **Decision: APPROVED. No new channel enters comparison until WP-E6-SWEEP completes.**
> * **Rationale:** F5b stands. Claiming S₈ = 0.828 from an exploratory fit as a top-down
> theoretical success is an epistemic violation. We are running a pre-registered
> confirmatory test against the DESI Lyα P1D (9-bin intersection). No other dataset
> (Euclid, Planck, NanoGrav) is allowed to touch the model until it receives a formal
> PREDICTION amendment.
> * **Stream-4 Designation:** Stream-4 (K4 Oligon/CAG) is officially designated as an
> **EXPLORATORY SANDBOX**. No claim originating from Stream 4 may be cited as evidence in
> Streams 1, 2, or 3.
>
> ### DL-4. The "Discovery" PDF and Lean Oracle Tarball
> **Decision: APPROVED. QUARANTINE IMMEDIATELY.**
> * **Rationale:** A compiled PDF titled "Discovery" before the empirical sweep has even
> touched real data is academic malpractice. A compiled Lean binary without auditable
> source code violates the core tenet of formal verification.
> * **Action:** Flag both as QUARANTINED.
> * **Audit WP-A:** Diff the PDF. Strip out any hallucinated conclusions regarding
> `cooper_s10` or unrun empirical data.
> * **Audit WP-B (Stream 1):** Rebuild the Lean 4 source. Run `#print axioms` on every
> theorem. Ensure the `0 sorry` claim actually attaches to the Swampland conjectures, not a
> trivial stub.
>
> ### DL-5. Operational Repairs
> **Decision: APPROVED. Execute under the autonomy mandate.**
> * **Action:** Restart the harvest daemon with a staleness alarm.
> * **Action:** Relaunch WP-E6-BINMAP, WP-E6-P2B (5 dof design), and WP-TW2
> (M19-polarization on P¹-bundle over P² for n ≤ 18).
> * **Action:** Enforce Producer ≠ Verifier on all uncommitted agent work.
>
> ### FINAL AUTHORIZATION
> The T1 Coordinator is authorized to execute all directives. Prioritize the
> `GCS_DATALAKE_MANIFEST.md` generation and the relaunch of the dropped WPs (BINMAP, P2B,
> TW2). Keep the exploratory/confirmatory firewall sealed.

---

## Part II — Fable review annotations (verified before recording, per intake protocol)

Every load-bearing figure in the directives was checked against prior ratified records or
this session's direct verification. All directives stand as issued; the annotations below
record verification results and five execution-shaping notes, none contradicting a ruling.

**A1 (DL-5 relaunch scopes, VERIFIED against `dbf1337`):** BINMAP/P2B/TW2 scopes match the
2026-07-29 PM ratification exactly — BINMAP: 9-bin restriction map + real published DESI
covariance extraction (D1); P2B: χ² design on the 9-bin covariance, 9 − 4 = 5 dof per cell
(D2, verified against ANALYSIS_PROTOCOL §2.3's four profiled nuisances in that record's
annotation A2); TW2: M₁₉-polarization exhibition on the P¹-bundle-over-P² family, n ≤ 18,
starting from the concretely-verified n = 0..3 cases, target lattice cited from the S2 G0
certificate (that record's annotation A4). The relaunches inherit those scopes verbatim —
no re-derivation, no scope drift.

**A2 (DL-4 WP-B, feasibility caveat):** "Rebuild the Lean 4 source" presupposes source
exists to rebuild. As verified 2026-07-31, the lake holds only the compiled
`lean_oracle_v5.tar.gz` (binary + Mathlib deps per the lake's own cartography). WP-B
therefore gets an explicit step 0 — locate source (candidate locations: the Vertex
session's uncommitted S3 dirs, the tarball's own contents if it bundles `.lean` files, or
a request to the Vertex session owner) — and an explicit failure branch: **if no source is
found, the verdict is "UNVERIFIABLE — remains QUARANTINED, tier NONE," which is a valid
reportable outcome, not an error state.** No agent may decompile-and-vouch.

**A3 (DL-2 "DES-Y3 conditional (Acquire only)", interpretation recorded):** read as
*acquisition authorized, contact prohibited* — DES-Y3 may be fetched into GCS staging
with full-hash manifest entry, but per DL-3 it cannot touch the model without its own
amendment. Sequenced after Planck P1 completes. If T0 instead meant "acquire only upon
S₈-channel promotion" (the brief's original P2 wording), the correction is one line in the
next ratification; until then the plan holds DES-Y3 at *planned, not fetched*, so both
readings remain satisfiable. IPTA DR2: struck — it will appear in
`GCS_DATALAKE_MANIFEST.md` only as an ABSENT row documenting the retracted claim, never as
a holding.

**A4 (DL-3 Stream-4 sandbox, propagation scope):** the designation must be *written where
the material lives*, or it will not bind future sessions: (i) a SANDBOX header note in the
datalake manifest rows for `stream4_bridge/`; (ii) a decision-log entry in S2 (home of
branch `experimental/stream4-cag-poc`); (iii) a line in this repo's CLAUDE.md epistemic
ledger ("Stream-4/Oligon: EXPLORATORY SANDBOX — no citation as evidence in Streams 1–3").
The 24.18 nHz "Oligon resonance" and the AlphaEvolve S₈ figure fall under this label
wherever they appear.

**A5 (DL-1 manifest + DL-4 quarantine, mechanics):** QUARANTINED is a manifest status, not
a deletion — the Discovery PDF and lean_oracle tarball stay in the bucket untouched (they
are another session's artifacts; the audit WPs need them intact). The manifest row is the
quarantine flag; any tooling that inventories the lake must carry the status forward.
Planck plik_lite acquisition (DL-2 P1) lands in **GCS staging with full SHA-256 manifest
entry only** — it does not enter `data/raw/` and no fetch_data.py entry is created until a
Planck channel amendment is pinned (DL-3), keeping rule 2's integrity record strictly
confirmatory.

---

## Part III — Execution status

**PLAN ONLY at this record's commit.** The proposed execution plan, with work-package
breakdown and T1 (Sonnet-class) / T2 (Haiku-class) model-tier assignments per the
canonical roster (EXECUTION_PLAN.md §1.1), is committed alongside this record as
`EXECUTION_PLAN_2026_07_31_DATALAKE_GOVERNANCE.md`. Nothing executes until T0 confirms GO
on that plan.

---
Recorded-by: Fable 5 (T1 coordinator) | Authority: T0 ratification above, verbatim |
Verification: annotations A1–A5 checked against `dbf1337`, the 2026-07-31 bucket
enumeration, and the lake's own audit documents | Reviewed-by: T0 (this IS the T0 record).
