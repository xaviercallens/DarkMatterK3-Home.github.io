# T0 Ratification & Directives — 2026-07-29 Evening (RECORD)

**Status:** RATIFIED. This document records, verbatim, T0's (Xavier Callens) rulings on
all five items of `T0_DECISIONS_2026_07_29_PM_RESUME.md`, followed by the Fable (T1
coordinator) review annotations made before execution. Per the standing autonomy mandate,
execution of the unblocked pipelines was authorized in the same message and proceeds
immediately after this record is committed.

**Decision summary:** D1 APPROVED (real DESI vector, 9-bin intersection, real published
covariance) · D2 APPROVED (9-bin design permanent, 5 dof) · D3 APPROVED (fix
ANALYSIS_PROTOCOL L290) · D4 CONFIRMED-CLOSED (ℓ=2, R5 closed) · D5 APPROVED
(M-polarization exhibition on the P¹-bundle-over-P² family, n ≤ 18).

---

## Part I — T0 directives (verbatim)

> **To:** Fable 5 (T1 Coordinator) & The SocrateAI Agora
> **From:** T0 (Xavier Callens)
> **Subject:** Decisions, Rationales, and Authorizations for Pending Items (Evening Resume)
>
> I have reviewed the decision-request brief. The pipeline's ability to self-diagnose
> resolution limits and correct document-to-code mismatches is exactly why the epistemic
> guardrails were established. Below are my formal ratifications and the scientific
> rationales to be committed to the project's decision ledger.
>
> ### D1. WP-E6-PIN's Real-Data-Contact Gaps
> **Decision: APPROVED. Use the real DESI CSV, restrict to the shared 9-bin intersection,
> and use the real published DESI covariance for the final exclusion constraint.**
>
> **Scientific & Engineering Rationale:**
> The entire purpose of WP-E6 is to generate a mathematically rigorous exclusion/FIT bound
> on Mixed-Fraction Fuzzy Dark Matter (f_FDM).
> 1. **The Vector:** Comparing our theoretical emulator against a *synthetic mock mean*
> defeats the purpose of an empirical test. The "observed" vector must be the actual DESI
> DR1 P1D measurement.
> 2. **The K-Bins:** Interpolating across mismatched k-bins introduces artificial,
> mathematically unconstrained covariance structures. We will strictly use the intersection
> of the emulator's natively resolved 9 k-bins and the DESI CSV's valid range.
> 3. **The Covariance:** While our `desisim` mock covariance was essential for pipeline
> engineering and verifying the masking fix (Part C), a final cosmological constraint must
> use the true instrument/survey uncertainties. The real published DESI covariance matrix
> naturally incorporates actual survey systematics (e.g., sky subtraction errors,
> spectrograph noise) that our synthetic pipeline cannot perfectly model.
>
> **Action:** Update `PREDICTION_V2_AMENDMENT_DRAFT`. Execute the follow-up WP to build the
> exact 9-bin restriction map and extract the true DESI covariance before running
> `WP-E6-SWEEP`.
>
> ### D2. WP-E6-P2A's K-bin Range Mismatch (16 vs. 9 Bins)
> **Decision: APPROVED. Adopt the 9-bin sub-block as the permanent design.**
>
> **Scientific & Engineering Rationale:**
> This is a standard Nyquist limit issue. The 7 excluded bins (≈ 0.1995 s/km) sit beyond
> the resolving power of our `desisim` pixel scale (≈ 0.0516 s/km). Forcing the pipeline to
> evaluate them would mean comparing sub-pixel noise against theoretical signal, rendering
> the χ² statistic meaningless at high-k. Truncating the analysis to the 9 cleanly resolved
> bins preserves statistical honesty and directly aligns with the restriction mandate in
> Decision D1.
>
> **Action:** WP-E6-P2B is authorized to build its χ² design on the 9-bin covariance
> (resulting in 9 − 4 = 5 degrees of freedom per cell). Update `ANALYSIS_PROTOCOL` to
> reflect the 9-bin geometry.
>
> ### D3. Correct `ANALYSIS_PROTOCOL_DRAFT` Masking-Correction Direction
> **Decision: APPROVED. Amend the document to match the code.**
>
> **Scientific & Engineering Rationale:**
> The code is correct; the document is wrong. Ravoux et al. 2023 (eq. 22/23) explicitly
> defines the multiplicative window correction as A = P_unmasked / P_masked. This ensures
> that when the raw, masked data is multiplied by A, the lost power is restored. Leaving
> the DRAFT inverted creates a dangerous epistemic hazard where future agents might "fix"
> working code to match broken documentation.
>
> **Action:** Apply the one-line correction to `ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md`
> L290, citing Ravoux et al. 2023 equations 22/23. Include a dated correction note.
>
> ### D4. WP-TW0 Confirms ℓ=2 (Closure)
> **Decision: CONFIRMED-CLOSED.**
>
> **Rationale:** The in-house symbolic derivation successfully reproduced the exact
> Hodge-bundle degree (ℓ=2) supplied earlier today by the Deep Think (T0s) adversarial
> review. This closes the loop mathematically. The strict-pullback ladder (Route A) remains
> unequivocally DEAD program-wide.
>
> ### D5. WP-TW1 Next Step: Authorize the M-Polarization Exhibition
> **Decision: APPROVED. Authorize the exhibition attempt, scoped strictly to the
> P¹-bundle over P² family with n ≤ 18.**
>
> **Scientific & Engineering Rationale:**
> The "Twisted-Weierstrass Trap-Check" worked perfectly. We mathematically proved that P³
> cannot support the required E₈ ⊕ E₈ singularities (the polynomials physically collide).
> However, finding that disjoint-section bases (P¹-bundles over P² for n ≤ 18) *pass* the
> necessary-condition screen is a massive structural green light.
> Since Route A is dead, this is the only mathematically viable path to exhibiting the
> Calabi-Yau fourfold (X₄) and unblocking Phase M (Dark Matter EFT couplings). The problem
> is now bounded and well-defined.
>
> **Action:** Launch the new WP. Instruct the agents to attempt the explicit construction
> of the f and g sections supporting the M₁₉-polarization specifically on the n ≤ 18
> family.
>
> ### FINAL AUTHORIZATION
> The T1 Coordinator (Fable) is authorized to commit these decisions and execute the
> corresponding unblocked pipelines across Stream 2 and Stream 3.

---

## Part II — Fable review annotations (verified before recording, per intake protocol)

Inbound documents are prompts to verify — including T0's. Every load-bearing number above
was checked against the repo before this record was committed. All directives stand as
issued; the annotations below record the verification results and four execution-shaping
notes, none of which contradicts a ruling.

**A1 (D1, VERIFIED): the "intersection" is exactly the 9 resolved bins — no further
truncation needed.** Checked numerically this session: the 9 resolved `K_BINS`
(log₁₀k = −2.2…−1.4, i.e. k ≈ 0.00631…0.03981 s/km) all lie inside the real CSV's k range
(max 0.0527412 s/km at every z, including z=4.2 — 85 k-bins × 12 z-bins = 1020 rows,
verified from the file, not the brief). Even the 9th bin's upper 0.05-dex band edge
(k ≈ 0.04467) is inside. So D1's restriction mandate resolves cleanly to the same 9-bin
set as D2 — one bin set governs both the synthetic and real sides, as intended.

**A2 (D2, VERIFIED): "9 − 4 = 5 dof" is correct against the LIVE protocol.** ANALYSIS_
PROTOCOL §2.3 fixes exactly 4 profiled nuisance parameters (`zrei, ha, hs, taueff`) per
(m,f) cell; the original 12-dof figure was 16 − 4. The arithmetic in the directive matches
the protocol's own parameter count — ratified as written, not assumed.

**A3 (D4, bookkeeping executed with this record):** ℓ=2's ledger standing upgrades from
"Tier B-external, non-blocking in-house check pending" (countermand annotation 1,
S2 `T0_COUNTERMAND_R2_2026_07_29.md`) to "Tier B — external derivation + independent
in-house symbolic verification (WP-TW0, coordinator-verified)". With T0's CONFIRMED-CLOSED,
the WP-TW0 certificate is promoted DRAFT → LIVE (T0 closure = the promotion authority the
DRAFT was waiting on). Recorded in the S2 decision log and CLAUDE.md ledger in the same
push as this document's commit.

**A4 (D5, scope note inherited from WP-TW1's own caveat):** the n ≤ 18 realizability bound
was verified *on the specific (C₀, C∞) disjoint-section configuration only* (WP-TW1 brief,
coordinator-verified). The exhibition WP inherits that scoping: it targets that
configuration, starts from the concretely-verified n = 0..3 cases before any general-n
argument, and treats the M-polarization target as the LIVE G0 lattice
NS ≅ U ⊕ E₈(−1) ⊕ E₈(−1) ⊕ ⟨−14⟩ (rank 19) — cited from the S2 certificate, not restated
from memory. An exhibition failure at all n ≤ 18 is a reportable result, not an error
state.

**A5 (sequencing consequence of D1, flagged not ruled):** choosing the real published DESI
covariance for the final constraint takes "regenerate P2A's synthetic covariance with
P2C's masking fix" **off the critical path** for WP-E6-SWEEP. It remains worth doing as
engineering validation of the synthetic pipeline (and P2A's brief still flags it), but it
no longer blocks the sweep. Execution below reflects this reprioritization.

**A6 (D1 pin mechanics):** executed as commit-as-pin on a standalone pinned file
(amendment §9's option 2), because `PREDICTION.md` v1.0 is immutability-hook-protected
(CLAUDE.md rule 2) — the hook blocking an append to the pinned v1.0 file is correct
behavior, not an obstacle to work around. The revised amendment carries the `PINNED:`
header, cites this ratification as its authority, and its introducing commit is the pin.
Per the prereg invariant, that pin commit predates any commit building the real-data
`obs` vector (WP-E6-BINMAP starts only after the pin is pushed).

## Part III — Execution launched with this record

- **D3 + D2 doc changes**: applied to `ANALYSIS_PROTOCOL_DRAFT_2026_07_28.md` (dated
  correction note at §3.3 L290; dated amendment note at §2.3), same commit as this file.
- **D1**: `PREDICTION_V2_AMENDMENT_DRAFT_2026_07_29.md` §8 items resolved per the ruling
  and the amendment pinned (see A6), same push.
- **D4 + A3**: S2 decision log + ledger updated, TW0 promoted LIVE, S2 push.
- **WPs launched in background** (no worktree isolation, per standing lesson;
  same-checkout git discipline instructions included per the PIN/P2A race precedent):
  - **WP-TW2** (S2, T1): M-polarization exhibition attempt, scope per A4.
  - **WP-E6-BINMAP** (S3, T1): 9-bin restriction map + real DESI covariance extraction,
    per D1 — launched only after the pin commit is pushed.
  - **WP-E6-P2B** (S3, T1): χ² profiling design on the 9-bin covariance, 5 dof per cell,
    per D2.
- **WP-E6-SWEEP** remains gated on: pin (done with this push) + P2B + BINMAP + coordinator
  verification of each. P2C is landed and verified; P2A's masking regeneration is
  descoped from the gate per A5.

---
Recorded-by: Fable 5 (T1 coordinator) | Authority: T0 ratification above, verbatim |
Verification: annotations A1–A2 checked against repo files this session | Reviewed-by: T0 (this IS the T0 record).
