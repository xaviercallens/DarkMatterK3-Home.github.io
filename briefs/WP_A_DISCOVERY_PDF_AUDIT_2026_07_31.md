# WP-A — "Discovery" PDF claims-vs-ledger audit (T0 ruling DL-4)

**Date:** 2026-07-31 · **Commissioned by:** `briefs/T0_RATIFICATION_2026_07_31_DATALAKE.md`
DL-4 ("Audit WP-A: Diff the PDF. Strip out any hallucinated conclusions regarding
`cooper_s10` or unrun empirical data.")

## 0. Artifact identity and audit scope

- **Artifact:** `gs://socrateai-datalake-gen-lang-client-0625573011/publications/SocrateAI_K3_T2_Discovery_Final.pdf`
- **SHA-256:** `320b09b446b8e31738e8401c5f0c9d15f292b84547f4334aabf15c6e380f2df6` (812,390 bytes, 9 pages, dated "July 30, 2026")
- **Status:** QUARANTINED (DL-4). Fetched to session scratch only; **NOT copied into any repo, NOT edited, NOT redistributed.** This audit report is the sole deliverable.
- **Ledgers diffed against:** S3 `CLAUDE.md` §"Epistemic boundaries" (items L1–L6 below), S2 `CLAUDE.md` §"Epistemic boundaries" (items S2-L1–L6), S2 `PREDICTION.md` v1.1-PINNED (esp. §6 F5b record), S2 `K3_SELECTION_REPORT.md` (refs/decision tables), S1 `paper/PLAN.md` (claims inventory + T0 framing rulings), S3 `PREDICTION.md` (PINNED, hash verified live this session: `verify_pin_hash() == True`, `labels_unlocked() == False`).
- **Verdict vocabulary:** **LEDGER-SUPPORTED** (exact ledger sentence quoted) / **UNSUPPORTED** (no certified basis in any ledger) / **RETRACTED-CONTRADICTING** (conflicts with the E-007/E-008/E-009 retractions or the F5b record).

**Headline: zero claims in this PDF earn LEDGER-SUPPORTED.** Per the WP-A mandate, that
absence is itself the finding — nothing below was force-fitted to a ledger line.

## 1. Standing ledger facts used throughout (exact quotes)

- **[L-ρ19]** S2 `CLAUDE.md` item 2: "**Tier B (derived, not measured):** ρ = 19, T = 3 for the **cooper_s7 family** — derived (E-011, Zarhin 1983 Thm 1.6(a) + Huybrechts, fetched and read), independently verified by Stream 1. A derived prior is not a measurement". *(Emphasis on cooper_s7 added.)*
- **[L-KOD]** S2 `CLAUDE.md` item 3: "**Kodaira readings are a category error for this family.** … The old ρ = 4, T = 18 and the '2× Type II' Kodaira labels are **RETRACTED (E-007)** — never use, cite, or 'confirm' them." (S2 item 2 wording; item 3 adds: "Do NOT classify Kodaira fibres from L₂ or L₃ exponents at any locus, under any normalization.")
- **[L-F5B]** S2 `CLAUDE.md` item 4: "**Tier C (blocked physics):** WP S3-00b (F-theory flux/tadpole) is BLOCKED (F5b). Do not assume, generate, or backfill exact observables (m_φ, α_D, Λ_D) or coefficients (a₁, a₂, a₃). The tadpole condition is not posable until a threefold base B₃ is specified; until then no dark-energy / vacuum-energy claim". Reinforced by S2 `PREDICTION.md` §6: "**No derived quantities. S3-00 ran, reached an honest obstruction, and triggered F5b.** … its outcome is that **no prediction can be extracted**." and "**Observable branch (§3): NOT SELECTED.** … No data contact has occurred for either."
- **[L-S4]** S3 `CLAUDE.md` item 5: "**Stream-4 ('K4 Oligon'/CAG) is an EXPLORATORY SANDBOX** (T0 ruling DL-3, 2026-07-31): no claim originating from Stream 4 — including the 24.18 nHz 'Oligon resonance' and any AlphaEvolve S₈ evaluation — may be cited as evidence in Streams 1–3."
- **[L-GATE]** S3 `CLAUDE.md` item 6: "**Empirical pivot is T0-gated.** No pipeline may depend on a single predicted scalar mass — none exists under F5b. Parameter sweeps / exclusion-bound pipelines enter only via a pre-registered PREDICTION v2 amendment under the pin protocol". The pre-registered sweep (WP-E6-SWEEP) **has not run**; as of this audit BINMAP/P2B are DRAFT-stage design artifacts (S3 `38665e9`, `89efd8e`, `a49be26`).
- **[L-AE]** T0 ratification DL-1: "AlphaEvolve outputs are explicitly labeled **PHENOMENOLOGICAL CONVERGENCE**. They cannot be used as empirical proof."
- **[L-S10]** WP-A mandate + session record 2026-07-30: cooper_s10 lattice/selection claims (incl. U⊕⟨20⟩) appear in **no** ledger — AlphaEvolve-reported only. Anything resting on cooper_s10 selection is automatically UNSUPPORTED.

## 2. Claim table

| # | PDF location | Claim (verbatim or condensed) | Verdict | Basis |
|---|---|---|---|---|
| C1 | Title | "Cosmological **Discovery**" | **UNSUPPORTED** | DL-4 verbatim: "A compiled PDF titled 'Discovery' before the empirical sweep has even touched real data is academic malpractice." [L-GATE]: the pre-registered sweep has not run; no empirical result of any tier exists. |
| C2 | Abstract | "We present a **resolution to the S8 weak lensing tension** and the recent NANOGrav 15-year … detection" | **UNSUPPORTED** | Empirical claim with no data product under the pin protocol [L-GATE]; S₈/PTA channels are Stream-4/AlphaEvolve material barred as evidence [L-S4][L-AE]. |
| C3 | Abstract, §2, §4.3 | "300-generation phenomenological scan", "12,000 candidate geometries", population 40 | **UNSUPPORTED** | AlphaEvolve-reported run metadata; in no ledger or manifest [L-AE][L-S10]. |
| C4 | Abstract, §4.1–4.3, §5, Fig 4, Concl. | "Cooper s10 … **uniquely characterized by** Picard number P = 19"; "Picard number remained locked at P = 19 across all 300 generations"; "Algebraic classification of Cooper s10 yields an identical Picard number P = 19" | **UNSUPPORTED** | Mandatory cooper_s10 flag [L-S10]. The only ledgered ρ = 19 is [L-ρ19], which (a) is for the **cooper_s7 family**, (b) is Tier B *derived, not measured*, and (c) derives from Zarhin/E-011 — not from any MCMC, "algebraic classification of s10", or hypergraph sieve. No certificate assigns ρ = 19 to cooper_s10 as a selection result; S1 `paper/PLAN.md` §1.1 item 4 in fact records the lattice pipeline "discriminating against the s10 family (det -20)". |
| C5 | Abstract | "Hodge number h2,1 = 19" for a K3 surface | **UNSUPPORTED** (and mathematically false) | A K3 surface has no h^{2,1} = 19; its Hodge diamond (1,0,0,1,20,1,0,0,1) is shown correctly in the PDF's **own Figure 4**, which the abstract contradicts. No ledger contact. |
| C6 | Abstract, §4.1–4.4, Tables 1–2, Fig 3 | χ² = 1.20×10⁻⁶ (also 4.91×10⁻⁶, 1.98×10⁻⁶, "4.1× improvement"), posterior Table 1 | **UNSUPPORTED** | AlphaEvolve loss-function values, exploratory channel only [L-AE][L-S4]. Not a goodness-of-fit against any manifest-tracked dataset; a χ² of 10⁻⁶ against real heterogeneous data is a degenerate-pass signature (cf. E2.16 discipline), not a result. |
| C7 | Abstract, §4.3, Fig 6, Concl. | w₀ = −0.99992, Ωₘ = 0.300, H₀ = 67.40 km/s/Mpc, S₈ = 0.830 as model outputs/predictions | **RETRACTED-CONTRADICTING** (F5b) | [L-F5B]: "Do not assume, generate, or backfill exact observables"; S2 `PREDICTION.md` §6: "no prediction can be extracted". The model has no constructed compactification, no stabilized moduli, no observable branch selected — exact cosmological outputs cannot exist at any tier. |
| C8 | Abstract | "topological defect monopole frequency of 1.07×10⁻⁹ Hz within the NANOGrav detection band" | **UNSUPPORTED** | Stream-4 material [L-S4]; no ledger basis; additionally an exact observable barred by [L-F5B]. |
| C9 | Abstract, §4.3 | "100% Lean 4 pass rate", "formal Lean 4 Swampland verification" of the scan | **UNSUPPORTED** | The only Lean artifact in the datalake is the compiled `lean_oracle_v5.tar.gz` — QUARANTINED by the same DL-4 ruling ("A compiled Lean binary without auditable source code violates the core tenet of formal verification"). WP-B (source rebuild + `#print axioms`) is pending with an explicit "UNVERIFIABLE — remains QUARANTINED, tier NONE" branch (ratification annotation A2). None of the program's actual Tier-A Lean results (L₃ = Sym²(L₂)) is what this PDF cites. |
| C10 | §3, §3.1, Fig 2 | K4-in-11-node-ring hypergraph; W(n)=Tr(Mⁿ); λ₁ = 3.0 "**uniquely isolates** the Cooper s10 sequence …, terminating the search space deterministically" | **UNSUPPORTED** | Stream-4 ("K4 Oligon") sandbox material [L-S4]. No ledger, checker, or certificate contains any spectral-radius→Cooper-sequence selection theorem. Also misattributes cooper_s10 to "OEIS A291898"; the repo reference registry (S2 `K3_SELECTION_REPORT.md` refs table) records cooper_s10 = **OEIS A005260**. |
| C11 | §4 | "**exact convergence** of both the empirical MCMC track and the deterministic topological track" on "identical topological invariants" | **UNSUPPORTED** | Both "tracks" are the same barred exploratory channel [L-S4][L-AE]; the shared invariant (P = 19 for s10) is itself unledgered (C4). |
| C12 | §4.4 | ln Z_K3T2 = −7.38 vs ln Z_ΛCDM = −2.69, ln B₁₀ = −4.69; then informed priors + resonance term "swinging the Bayes factor strongly in favor of the Oligon framework" | **UNSUPPORTED** | Stream-4/AlphaEvolve [L-S4][L-AE]. Methodological note for T0: the maneuver derives priors from the same AutoEvolve MAP the evidence then rewards, and inserts the model's own "resonance bump" into the likelihood to make ΛCDM "plummet" — circular by construction, on top of being ledger-barred. |
| C13 | §4.4, §4.6, Fig 5 | "predictive topological resonance bump at **24.18 nHz**" / "Compton resonance" | **UNSUPPORTED** | Named verbatim in [L-S4] as barred: "including the 24.18 nHz 'Oligon resonance'". |
| C14 | §4.5 | Fisher information F = 100.00 at τ = 0.50 "confirms … a mathematically stable, attractive topological **vacuum state**" | **UNSUPPORTED**; vacuum-state reading **RETRACTED-CONTRADICTING** (F5b) | Curvature of an AlphaEvolve loss slice [L-AE]. Calling it a *vacuum state* contradicts [L-F5B]/S2 `PREDICTION.md` §6 obstruction 1: no flux stabilization or moduli fixing exists for this candidate ("nobody has chosen flux quanta, fixed (𝒱, g_s) …"). |
| C15 | §4.6 | Hexadecapole Cℓ ratio 16.07 at l=4; γ_Oligon = 4.847; Δγ ≈ 0.51 | **UNSUPPORTED** | Stream-4 anisotropy outputs [L-S4]; no ledger basis. |
| C16 | §4.6 | SKA split test: "the Bayes factor completely inverts, yielding Δχ² ≫ 9.0 and **decisively confirming** the Oligon hypothesis" | **UNSUPPORTED** | Projection on top of C12/C13 (both barred); "decisively confirming" applied to a Tier-C construct with no conjecture marker — forbidden-verb violation of the epistemic-guardrails rules on its face. |
| C17 | §4.7, Fig 6 | "Observational Validation via Real ESA Euclid Q1 Open Data": 80,376 galaxies processed, "measured S8 constraint of S8 = 0.828 ± 0.011", "aligns … to within 0.18σ", certificate "AUDIT-EUCLID-Q1-1785441737" | **UNSUPPORTED** (and a protocol violation if the processing occurred) | The pre-registered sweep has not run [L-GATE]; the pinned S3 observable branches (PTA / halo-profile lensing / Lyman-α, gated on the never-derived m_φ) never fired — S2 `PREDICTION.md` §6: "No data contact has occurred for either." No Euclid Q1 catalog appears in `data/MANIFEST.md`; no S₈ weak-lensing observable is pinned anywhere. The claimed "0.18σ alignment" is against the unledgered "prediction" C7. The "audit certificate" ID appears in no repo. Additionally implausible on its face: ±0.011 on S₈ from 80,376 objects of two deep-field *detection/morphology* catalogs (no shear pipeline) is beyond what the full Euclid survey targets. |
| C18 | §5 | "The convergence uniquely selects the **Kodaira fiber type II**." | **RETRACTED-CONTRADICTING** (E-007/E-008/E-009) | [L-KOD] verbatim: "The old ρ = 4, T = 18 and the '2× Type II' Kodaira labels are **RETRACTED (E-007)** — never use, cite, or 'confirm' them." and "Kodaira readings are a category error for this family." This sentence resurrects the retracted Type II label. |
| C19 | §5 | "Our Lean 4 formalization verified that this exact geometry simultaneously satisfies the Swampland Distance Conjecture and the refined de Sitter Conjecture, providing a **stable flux vacuum** with χ = 24." | **UNSUPPORTED** (Lean claim, per C9); flux-vacuum clause **RETRACTED-CONTRADICTING** (F5b) | No auditable Lean source (C9). "Stable flux vacuum" contradicts [L-F5B]: the tadpole condition "is not posable until a threefold base B₃ is specified"; no flux stabilization exists. (χ = 24 for a K3 surface is textbook mathematics and carries no program content.) |
| C20 | §5 | Dark-sector decoupling "mediated by the volume hierarchy" between K3 and T² | **UNSUPPORTED** | Tier-C physical mechanism stated as fact with no conjecture marker; sectors are recorded "[C, unconstructed]" (`VISION.md` §1.2 via S2 `PREDICTION.md` §6). |
| C21 | §6.2–6.3 | Codebase incl. "Lean 4 Swampland theorem provers" at `github.com/xaviercallens/SocrateAI-Scientific-AutoEvolve-K3xT2`; figures "rendered verbatim from live production telemetry" | **UNSUPPORTED** as a verification claim | Repo exists (checked live: public, pushed 2026-07-31) but is **not** one of the three governed program repos; nothing in it is covered by any ledger, manifest, or checker regime. Repository existence is not verification; "live telemetry" provenance is unauditable. |
| C22 | §7 | "we **prove** that the parameters necessary to resolve the S8 tension (P = 19) are identical to those generated by a λ₁ = 3.0 causal hypergraph" | **UNSUPPORTED** | "Prove" applied to an unconstructed Tier-C mechanism — forbidden verb, no marker; both sides of the claimed identity are unledgered (C4, C10). |
| C23 | §7.2 | "The universe, at its core, is computationally determined." | **UNSUPPORTED** | Tier-C metaphysical assertion presented as conclusion; no ledger contact possible. |
| C24 | Byline | Authors: "Xavier Callens **and The SocrateAI AutoEvolve System**" | Protocol flag (not a quantitative claim) | Contradicts the T0 framing ruling for program publications (ratification D2, 2026-07-28; S1 `paper/PLAN.md` §5: "**RESOLVED:** sole author Xavier Callens" with mandated verbatim AI-acknowledgment wording instead of AI co-authorship). |

**LEDGER-SUPPORTED claims found: none.** The only true statements in the PDF are textbook
mathematics (K3 Hodge diamond h^{1,1} = 20, χ = 24 — contradicted by the PDF's own abstract,
see C5) and literature background (the existence of the S₈/H₀ tensions), neither of which is
a program claim.

## 3. Mandatory-flag checklist (per WP-A commission)

- **cooper_s10 / U⊕⟨20⟩:** flagged — C3, C4, C6, C10, C11 (U⊕⟨20⟩ itself is not named in the PDF; the s10-selection story that produced it is the PDF's spine). All automatically UNSUPPORTED [L-S10].
- **Empirical/exclusion claims with the sweep unrun:** flagged — C1, C2, C7, C8, C12, C13, C16, C17. The pre-registered WP-E6 sweep has NOT run; no data contact has occurred under the pin protocol.
- **Kodaira fiber-type statements:** flagged — C18 (RETRACTED-CONTRADICTING, E-007/E-008/E-009 category error).
- **Exact observables under F5b:** flagged — C7, C8, C14, C19 (m_φ-class exact-observable/vacuum claims are Tier-C blocked; PREDICTION.md §6 records "NOT DERIVED … forbidden to write").
- **Title word "Discovery":** flagged — C1 (UNSUPPORTED; DL-4 already ruled on it verbatim).

## 4. Overall verdict for T0

The PDF is a Stream-4/AlphaEvolve artifact wearing the program's name: of its 24 audited
claims, **zero are LEDGER-SUPPORTED**, four are **RETRACTED-CONTRADICTING** (the Kodaira
Type II resurrection C18, and the exact-observable/flux-vacuum claims C7/C14/C19 against the
F5b record), and the remainder are **UNSUPPORTED**, resting on the exploratory channel that
DL-1/DL-3 bar from evidentiary use, on an unledgered cooper_s10 selection story, or on a
claimed real-data Euclid contact (C17) that occurred — if it occurred at all — entirely
outside the pinned pre-registration protocol and its manifests, and whose headline precision
is not credible for the inputs described. The document also violates the program's
authorship ruling (C24) and its own internal mathematics (C5). Recommendation: the PDF
**remains QUARANTINED with tier NONE**; it is not repairable by striking individual
sentences, because every load-bearing result (title claim, χ², cosmological parameters,
convergence narrative, Lean verification, Euclid validation) fails the ledger independently
— any future publication along these lines would need to be rebuilt from ledgered artifacts
from scratch. If T0 wishes, the claim table above doubles as the DL-4 "strip list"; no strip
was performed, per the WP-A no-edit constraint.

---
Generated-by: Fable 5 (WP-A audit agent) | Verified-by: every verdict traced to a quoted
ledger sentence or a live-checked repo artifact this session (pin hash verified True;
tier-language checker green; PDF SHA-256 recorded above); producer≠verifier pass still owed
per standing rule | Reviewed-by: T0 N (this brief is the review request)
