#!/usr/bin/env python3
"""WP-H hypothesis registry — the 25 hypotheses of the auto-research brief, triaged.

Source of the hypotheses: `briefs/SOURCE_autoresearch_brief_2026_07_25.md` (vendored
verbatim, SHA256 19eafed983e75523...). That document is an **unreviewed external input**;
this module is where each of its claims meets the repo's actual state.

Authorization for this work package: `docs/WP_H_T0_AUTHORIZATION_2026_07_25.md`.
Label for every WP-H output: `SANDBOX-EXPERIMENTAL` (`EXECUTION_PLAN.md` §4.1) — never
`TEST`, never `FIT`. Gate G1-L is closed and this module does not change that.

What a triage verdict means
---------------------------
`RUNNABLE` does **not** mean "the hypothesis is testable". It means: the *statistic* the
brief names can be computed from data this repo already has, using verified code. Whether
computing it says anything about the hypothesis is a separate question, answered by the
`claim_gap` field — which is non-empty on every single RUNNABLE record, because F5b fired
and no derivation links Cooper s7 to any of these observables. Reading a RUNNABLE verdict
as "hypothesis confirmed/refuted" is exactly the error this module exists to prevent.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Literal

# The only label WP-H may ever emit. See EXECUTION_PLAN.md §4.1.
TAG = "SANDBOX-EXPERIMENTAL"

# Labels that WP-H is mechanically forbidden from producing (gate G1-L closed).
FORBIDDEN_LABELS = ("TEST", "FIT")

Status = Literal["RUNNABLE", "BLOCKED_DATA", "BLOCKED_PROVENANCE", "OUT_OF_SCOPE"]

_BLOCKED = ("BLOCKED_DATA", "BLOCKED_PROVENANCE", "OUT_OF_SCOPE")


@dataclass(frozen=True)
class Constant:
    """A numeric constant a hypothesis depends on, with its provenance.

    P1 (LESSONS_LEARNED.md): no constant without provenance. `provenance` must say where
    the value actually comes from — a certificate path, a literature citation with a
    locator, or the honest string that it has none.
    """

    symbol: str
    value: str
    provenance: str
    is_traced: bool  # True iff provenance resolves to a certificate or a checkable citation


@dataclass(frozen=True)
class Hypothesis:
    """One hypothesis from the source brief, plus this repo's mechanical verdict on it."""

    hid: str
    statement: str
    source_section: str          # where in the vendored brief it appears
    claimed_script: str          # the script the brief says will validate it
    claimed_data: str            # the dataset the brief names
    claimed_criterion: str       # the brief's pass/fail threshold
    status: Status
    blocker: str                 # required non-empty iff status != RUNNABLE
    claim_gap: str               # what computing this does NOT establish (always non-empty)
    constants: tuple[Constant, ...] = field(default_factory=tuple)
    runner_key: str = ""         # dispatch key in scripts/wp_h_auto_research.py, if RUNNABLE

    @property
    def is_blocked(self) -> bool:
        return self.status in _BLOCKED

    def to_dict(self) -> dict:
        d = asdict(self)
        d["label"] = TAG
        return d


# --------------------------------------------------------------------------------------
# Shared blocker texts. Each cites the repo file that actually records the obstruction, so
# a future reader can check the claim rather than take this module's word for it.
# --------------------------------------------------------------------------------------

_B_SHEAR = (
    "No weak-lensing shear or convergence (κ) product exists in data/MANIFEST.md, and none "
    "is publicly available: finding R-SHEAR, briefs/STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md "
    "§4 — 'public Euclid has no lensing shear catalogue; any κ-peak-based proposal is "
    "synthetic-only until that changes.' pipeline/observables_real.py::compute_kappa_peak_statistic "
    "exists and is golden-tested, but has no real map to consume."
)

_B_DELTA_QUARANTINE = (
    "The Δ figures this hypothesis compares against are quarantined [A-DATA-LEGACY] by "
    "ASSUMPTIONS.md v2.0-SIGNED §2: 'not reproducible from checkers in this repo today. Not "
    "usable in S3-00 or any pre-registered comparison until regenerated with manifest-pinned "
    "data.' NO_PREDICTION_BRANCH.md §8.2 names this as blocker 1 of 2 on exactly this pivot."
)

_B_NO_PTA_DATA = (
    "No PTA product in data/MANIFEST.md. The 7 manifested datasets are SDSS + Euclid "
    "catalogues only. Fetching NANOGrav would additionally require a predicted spectral "
    "location to compare against, which F5b removed (NO_PREDICTION_BRANCH.md §8)."
)

_B_NO_STREAM_DATA = (
    "No tidal-stream (GD-1/Pal 5) or JWST product in data/MANIFEST.md, and ΔAIC against "
    "'Chameleon EFT' presupposes a constructed EFT. No such EFT exists: the flux/tadpole "
    "construction is blocked at three independent points (NO_PREDICTION_BRANCH.md §8, "
    "PREDICTION_APPENDIX_A.md A.1.4/A.2.5/A.3.4), which is why F5b fired."
)

_B_NO_S7_PREDICTION = (
    "Requires a Cooper-s7 predicted value to compare the measurement against. There is none: "
    "PREDICTION.md §6 is 'Empty by design', gate G1-L is closed "
    "(pipeline/gate.py::labels_unlocked() is False), and F5b fired as pre-committed. The "
    "measurement half is runnable; the comparison half has no second operand."
)

_B_THEORY_SCOPE = (
    "Theoretical/mathematical claim with no empirical content for Stream 3. Belongs to "
    "Stream 2 (K3 selection & lattice) or Stream 1 (Lean formalization); the brief itself "
    "marks the 'data' column 'Theoretical'. Routing it here would be scope drift."
)

_G_NO_LINK = (
    "Computing this statistic says nothing about Cooper s7, K3 geometry, or chameleon "
    "screening. No derivation connects the model to this observable — that construction is "
    "precisely what failed (F5b, NO_PREDICTION_BRANCH.md §8). The number is a description "
    "of the galaxy catalogue, full stop."
)


# --------------------------------------------------------------------------------------
# The registry. Ordering follows the brief's own consolidated list (§3 of file 1).
# --------------------------------------------------------------------------------------

HYPOTHESES: tuple[Hypothesis, ...] = (
    # ---- Tier A: the brief's "Certified Mathematics (K3/F-Theory)" ----
    Hypothesis(
        hid="H-A1",
        statement="Cooper s7's order-3 Picard-Fuchs ODE implies a Swampland-compliant K3 "
                  "base, predicting beta_1 > beta_0 + beta_2 in the cosmic web.",
        source_section="File 1 §2.1 / §3 Tier A; File 2 §4.1",
        claimed_script="cosmic_web_topology.py",
        claimed_data="SDSS/DESI",
        claimed_criterion="beta_1 > beta_0 + beta_2",
        status="RUNNABLE",
        blocker="",
        claim_gap=_G_NO_LINK + " In particular, beta_1 > beta_0 + beta_2 is a generic "
                  "property of filamentary point distributions (Cautun et al. 2014 report it "
                  "for LambdaCDM itself), so satisfying it discriminates nothing.",
        runner_key="betti_dominance",
    ),
    Hypothesis(
        hid="H-A2",
        statement="The Shioda-Tate formula (rho=4/T=18) holds for Cooper s7, making "
                  "chi(X_4) computable if B_3 = K3 x T^2.",
        source_section="File 1 §2.1 / §3 Tier A",
        claimed_script="chi_x4_validation.py",
        claimed_data="Theoretical",
        claimed_criterion="chi(X_4) defined",
        status="OUT_OF_SCOPE",
        blocker=_B_THEORY_SCOPE + " rho=4/T=18 is already certified in Stream 2's "
                "C2_cooper_s7_partner.json; re-deriving it here would duplicate, not verify.",
        claim_gap="No empirical content; nothing about this is settled by galaxy catalogues.",
    ),
    Hypothesis(
        hid="H-A3",
        statement="F-theory on CY4 over K3 x T^2 provides a UV-complete background.",
        source_section="File 1 §2.1 / §3 Tier A",
        claimed_script="DUAL_SCALE_HYPOTHESIS.md",
        claimed_data="Theoretical",
        claimed_criterion="No dark energy claim",
        status="OUT_OF_SCOPE",
        blocker=_B_THEORY_SCOPE + " The brief's own 'validation method' column names a "
                "markdown file, not a computation — there is nothing here to run.",
        claim_gap="No empirical content: UV completeness is not a property any galaxy "
                  "catalogue can bear on. The stated criterion ('no dark energy claim') is "
                  "a restriction on what the program may say, not a measurable outcome, so "
                  "satisfying it is a matter of prose discipline rather than evidence.",
    ),
    Hypothesis(
        hid="H-A4",
        statement="K3 surfaces satisfy Swampland constraints; moduli stabilize at infinite "
                  "distance.",
        source_section="File 1 §2.7 / §3 Tier A",
        claimed_script="swampland_validation.py",
        claimed_data="Theoretical",
        claimed_criterion="Moduli stabilize at infinite distance",
        status="OUT_OF_SCOPE",
        blocker=_B_THEORY_SCOPE + " Partially addressed already by "
                "SWAMPLAND_BOUNDS_A123.md (Off-Ramp 2), which reached a partial closure "
                "rather than the clean 'satisfied' this hypothesis asserts.",
        claim_gap="No empirical content, and the existing partial result points the other "
                  "way: Off-Ramp 2 recorded a partial closure plus a new obstruction (Gap "
                  "G-1), not the clean satisfaction this hypothesis states as its expected "
                  "outcome. Restating it as settled would overwrite a recorded negative.",
    ),
    Hypothesis(
        hid="H-A5",
        statement="Type III fibers in Cooper s7 enable non-Lagrangian Argyres-Douglas "
                  "sectors, predicting beta_2 suppression in small-scale voids.",
        source_section="File 1 §2.1 / §3 Tier A; File 2 §4.1",
        claimed_script="void_suppression_validation.py",
        claimed_data="SDSS/Euclid",
        claimed_criterion="beta_2 (Cooper s7) < beta_2 (LambdaCDM)",
        status="BLOCKED_PROVENANCE",
        blocker="The premise contradicts Stream 2's certificate. "
                "C1loci_cooper_s7_partner.json records **Type II** fibres, not Type III; "
                "briefs/GATE_G1L_RULING_2026_07_25.md §4 documents the reading that Type II "
                "carries no perturbative gauge algebra (ADE enhancement begins at Type III), "
                "which is the 'Type II veto' wall (a_1). The brief asserts the fibre type "
                "that would dissolve the wall, without a certificate saying so. " + _B_NO_S7_PREDICTION,
        claim_gap="Any beta_2 measurement made under this heading would be attributed to a "
                  "fibre type the geometry does not have.",
    ),

    # ---- Tier B: the brief's "Checkable Conjectures (Chameleon/EFT)" ----
    Hypothesis(
        hid="H-B1",
        statement="A chameleon scalar field (rank-3 subspace) screens in high-density "
                  "regions, with screening radius r_s >= 0.27 Mpc in cosmic voids.",
        source_section="File 1 §2.2 / §3 Tier B; File 2 §4.2, §6",
        claimed_script="chameleon_screening_validation.py",
        claimed_data="SDSS/Euclid",
        claimed_criterion="r_s >= 0.27 Mpc (KS test, p < 0.05)",
        status="BLOCKED_PROVENANCE",
        blocker="Circular threshold. The brief attributes 'r_s >= 0.27 Mpc' to Brax et al. "
                "(2012) as a chameleon prediction, but 0.22-0.27 Mpc is this repo's own "
                "measured *survey resolution floor* (docs/WP_R6_SURVEY_SCALES.md, restated "
                "as the design envelope in briefs/STREAM2_ASTRO_MODEL_DIRECTIVE_2026_07_25.md "
                "§4). A 'prediction' equal to the finest scale the instrument can resolve is "
                "unfalsifiable by construction: nothing below it is observable, so the test "
                "can only ever pass. This is the same circularity that failed WP-A2 "
                "(WP_A2_CIRCULARITY_AUDIT.md).",
        constants=(
            Constant(
                symbol="r_s",
                value="0.27 Mpc",
                provenance="Brief cites Brax et al. (2012) arXiv:1203.1089. Not verified; "
                           "and the identical figure is this repo's measured resolution "
                           "floor (WP_R6_SURVEY_SCALES.md), which is where it is far more "
                           "likely to have come from.",
                is_traced=False,
            ),
        ),
        claim_gap="A pass would measure the instrument, not the universe.",
    ),
    Hypothesis(
        hid="H-B2",
        statement="beta_2 is suppressed in small-scale voids for Cooper s7 relative to "
                  "LambdaCDM.",
        source_section="File 1 §2.2, §2.4 / §3 Tier B; File 2 §4.2, §6",
        claimed_script="void_suppression_validation.py",
        claimed_data="SDSS/Euclid",
        claimed_criterion="beta_2 (Cooper s7) < beta_2 (LambdaCDM), p < 0.05",
        status="RUNNABLE",
        blocker="",
        claim_gap="Runnable only in its descriptive half: beta_2 can be measured in low- "
                  "versus high-density regions of the real fields, against the WP-R5 null "
                  "bank. The comparative half is not runnable — there is no Cooper-s7 "
                  "beta_2 prediction to be less than anything (" + _B_NO_S7_PREDICTION + "). "
                  "What is reported is a density-split contrast with null percentiles, "
                  "labelled as such, and it is not evidence for or against suppression.",
        runner_key="beta2_density_split",
    ),
    Hypothesis(
        hid="H-B3",
        statement="Tidal stream anomalies (GD-1, Pal 5) fit Chameleon EFT better than "
                  "LambdaCDM.",
        source_section="File 1 §2.2, §2.3 / §3 Tier B; File 2 §4.2",
        claimed_script="tidal_stream_validation.py",
        claimed_data="SDSS/JWST",
        claimed_criterion="Delta-AIC > 10",
        status="BLOCKED_DATA",
        blocker=_B_NO_STREAM_DATA,
        claim_gap="No stream data and no EFT: both operands of the AIC comparison are absent.",
    ),
    Hypothesis(
        hid="H-B4",
        statement="A scalar monopole signal for Cooper s7 is present in NANOGrav PTA data.",
        source_section="File 1 §2.2, §2.5 / §3 Tier B; File 2 §4.2, §6",
        claimed_script="NANOGrav_prediction.py",
        claimed_data="NANOGrav 15-yr",
        claimed_criterion="p-value < 0.05",
        status="BLOCKED_DATA",
        blocker=_B_NO_PTA_DATA,
        claim_gap="The pinned P1 branch of PREDICTION.md §3 would have tested a PTA "
                  "signature at f = m_phi/pi — but m_phi was never derived (§6 empty), which "
                  "is the whole content of the F5b outcome.",
    ),
    Hypothesis(
        hid="H-B5",
        statement="Delta spikes from S12/S21 align with weak-lensing kappa peaks at > 80%.",
        source_section="File 1 §2.3, §2.6 / §3 Tier B; File 2 §4.2, §6",
        claimed_script="weak_lensing_overlay.py",
        claimed_data="Euclid/SDSS",
        claimed_criterion="Alignment score > 0.8",
        status="BLOCKED_DATA",
        blocker=_B_SHEAR + " " + _B_DELTA_QUARANTINE + " This is the specific pivot that "
                "briefs/GATE_G1L_RULING_2026_07_25.md §5 rules unauthorized without a fresh "
                "pin; note that the WP-H authorization deliberately does not supply that pin.",
        claim_gap="Both operands are unavailable: no real kappa map, and the Delta values "
                  "named are quarantined legacy numbers.",
    ),
    Hypothesis(
        hid="H-B6",
        statement="The 7-brane coupling is tau = 0.0000 + 1.21145i in high-density regions.",
        source_section="File 1 §2.3 / §3 Tier B; File 2 §4.2",
        claimed_script="7brane_coupling_validation.py",
        claimed_data="SDSS",
        claimed_criterion="tau ~= 0.0000 + 1.21145i +/- 0.01",
        status="BLOCKED_PROVENANCE",
        blocker="FABRICATED CONSTANT — P1 violation, refused. The brief states tau to six "
                "significant figures and attributes it to Denef (2008) hep-th/0801.1074, a "
                "review of F-theory 7-brane physics that fixes no such numerical value for "
                "this or any specific compactification. No certificate in checkers/ contains "
                "it. This is the exact defect class that invalidated the earlier Cooper s7 "
                "constants (LESSONS_LEARNED.md, [[cooper-s7-ground-truth]]): a plausible-"
                "looking number with a citation that does not contain it. Additionally "
                "incoherent on its face — a 7-brane axio-dilaton is not a quantity a galaxy "
                "catalogue can measure 'in high-density regions'.",
        constants=(
            Constant(
                symbol="tau",
                value="0.0000 + 1.21145i +/- 0.01",
                provenance="NONE. Attributed to Denef (2008) hep-th/0801.1074; the value does "
                           "not appear there and no repo certificate contains it.",
                is_traced=False,
            ),
        ),
        claim_gap="Nothing may be computed under this hypothesis. It is retained in the "
                  "registry as a regression marker so the value cannot be quietly reimported.",
    ),
    Hypothesis(
        hid="H-B7",
        statement="Cooper s7's V4C pipeline results are consistent with Chameleon EFT.",
        source_section="File 1 §2.3 / §3 Tier B; File 2 §4.2",
        claimed_script="v4c_consistency_validation.py",
        claimed_data="SDSS",
        claimed_criterion="|dElev| < 0.2",
        status="BLOCKED_PROVENANCE",
        blocker="No V4C pipeline exists in this repo. The brief cites 'V4C Pipeline' as its "
                "own theoretical basis — a circular citation to an artifact it does not "
                "locate. The legacy V4/V5 dashboard scripts it likely refers to are the "
                "deprecated, fabrication-flagged ones ([[dual-scale-brief-2026-07-25]]), and "
                "their outputs are quarantined [A-DATA-LEGACY].",
        constants=(
            Constant(
                symbol="dElev",
                value="< 0.2",
                provenance="NONE. Threshold asserted with no derivation; the quantity itself "
                           "is undefined in this repo.",
                is_traced=False,
            ),
        ),
        claim_gap="Undefined quantity, absent pipeline, quarantined inputs.",
    ),
    Hypothesis(
        hid="H-B8",
        statement="S12/S21 act as Elliptic EFTs for dark matter subhalos.",
        source_section="File 1 §2.3 / §3 Tier B; File 2 §4.2",
        claimed_script="weak_lensing_overlay.py",
        claimed_data="Euclid/SDSS",
        claimed_criterion="Delta spikes align with kappa peaks > 80%",
        status="BLOCKED_DATA",
        blocker=_B_SHEAR + " " + _B_DELTA_QUARANTINE + " Duplicate of H-B5's criterion "
                "under a different heading; the brief lists both, which inflates its "
                "'25 hypotheses' count.",
        claim_gap="Same two missing operands as H-B5 (no real kappa map, quarantined Delta "
                  "values). Separately, 'S12/S21 as Elliptic EFTs' is an ontological claim "
                  "that a peak-alignment score could not establish even with both operands "
                  "in hand — alignment is not identification.",
    ),
    Hypothesis(
        hid="H-B9",
        statement="Delta spikes from S12/S21 are stable across SDSS sectors (sigma_Delta < 0.1).",
        source_section="File 1 §2.3 / §3 Tier B; File 2 §4.2",
        claimed_script="delta_spike_stability.py",
        claimed_data="SDSS",
        claimed_criterion="sigma_Delta < 0.1",
        status="RUNNABLE",
        blocker="",
        claim_gap="Runnable as a *stability measurement of the estimator*, using the "
                  "regenerated Delta definition in pipeline/delta_observable.py (WP-D, "
                  "[A-DATA-WD]) recomputed from manifested catalogues. It imports no legacy "
                  "[A-DATA-LEGACY] value and compares against none. Field-to-field scatter "
                  "of a statistic is a property of the fields and the estimator; it is not "
                  "evidence about S12/S21, which are not implemented here at all. The "
                  "brief's 'S12/S21' attribution is dropped as unsupported.",
        constants=(
            Constant(
                symbol="sigma_Delta threshold",
                value="0.1",
                provenance="Brief asserts it with no derivation. Recorded, NOT applied — the "
                           "runner reports sigma_Delta and does not evaluate it against this "
                           "threshold, since doing so would be a pass/fail verdict (TEST-shaped).",
                is_traced=False,
            ),
        ),
        runner_key="delta_stability",
    ),
    Hypothesis(
        hid="H-B10",
        statement="Cosmic web topology is scale-dependent over 0.22-0.27 Mpc.",
        source_section="File 1 §2.4 / §3 Tier B; File 2 §4.2",
        claimed_script="cosmic_web_topology.py",
        claimed_data="SDSS/DESI",
        claimed_criterion="beta_1/beta_2 vary with scale",
        status="RUNNABLE",
        blocker="",
        claim_gap=_G_NO_LINK + " Scale dependence of Betti numbers is expected for any "
                  "point process whatsoever, so observing it excludes nothing. Note also "
                  "that 0.22-0.27 Mpc is the resolution floor, not a window inside the data: "
                  "the runner scans upward from it (per WP-E's R >= 0.3 Mpc floor) rather "
                  "than inside it, which is the only direction the data supports.",
        constants=(
            Constant(
                symbol="scale window",
                value="0.22-0.27 Mpc",
                provenance="docs/WP_R6_SURVEY_SCALES.md — measured transverse resolution "
                           "floor at median z~1.4-1.5. Traced, but it is a survey property, "
                           "not the model prediction the brief presents it as.",
                is_traced=True,
            ),
        ),
        runner_key="scale_scan",
    ),
    Hypothesis(
        hid="H-B11",
        statement="kappa peaks correlate with beta_1/beta_2 in the cosmic web (Pearson r > 0.7).",
        source_section="File 1 §2.6 / §3 Tier B; File 2 §4.2",
        claimed_script="kappa_betti_correlation.py",
        claimed_data="Euclid/SDSS",
        claimed_criterion="Pearson r > 0.7",
        status="BLOCKED_DATA",
        blocker=_B_SHEAR,
        claim_gap="One of the two correlands does not exist as real data.",
    ),
    Hypothesis(
        hid="H-B12",
        statement="Cooper s7 satisfies the Swampland Distance Conjecture.",
        source_section="File 1 §2.7 / §3 Tier B",
        claimed_script="swampland_validation.py",
        claimed_data="Theoretical",
        claimed_criterion="Moduli stabilize at infinite distance",
        status="OUT_OF_SCOPE",
        blocker=_B_THEORY_SCOPE + " Duplicate of H-A4 at a different tier.",
        claim_gap="No empirical content. The brief files the same claim at Tier A (H-A4) "
                  "and Tier B (here) with the same criterion and the same script, which "
                  "means its tier assignment carries no information about how checkable "
                  "the claim is.",
    ),
    Hypothesis(
        hid="H-B13",
        statement="Cooper s7's moduli decouple from observables; no fifth-force violations.",
        source_section="File 1 §2.7 / §3 Tier B",
        claimed_script="fifth_force_validation.py",
        claimed_data="SDSS",
        claimed_criterion="No fifth-force violations",
        status="BLOCKED_DATA",
        blocker="Fifth-force constraints come from laboratory inverse-square-law "
                "experiments, not SDSS galaxy catalogues; the brief's data column is simply "
                "wrong for the observable. This ground was covered by WP-A2, which found the "
                "reachable region circular and the non-circular region beyond every "
                "published dataset (WP_A2_CIRCULARITY_AUDIT.md, Off-Ramp 3). The live "
                "monitoring trigger F-LAB already covers any future data that would change "
                "this.",
        claim_gap="Superseded by an existing, more careful negative result.",
    ),
    Hypothesis(
        hid="H-B14",
        statement="Stochastic GWB in PTA data aligns with Chameleon EFT (correlation with "
                  "Delta spikes).",
        source_section="File 1 §2.5 / §3 Tier B; File 2 §4.2",
        claimed_script="pta_gwb_correlation.py",
        claimed_data="NANOGrav",
        claimed_criterion="r > 0.7",
        status="BLOCKED_DATA",
        blocker=_B_NO_PTA_DATA + " " + _B_DELTA_QUARANTINE,
        claim_gap="Neither operand is available. Even given both, a correlation between a "
                  "nHz gravitational-wave background and a galaxy-morphology statistic has "
                  "no stated mechanism connecting them in this program; the brief supplies "
                  "a threshold (r > 0.7) but no reason such a correlation should exist.",
    ),

    # ---- Tier C: the brief's "Null Tests (Alternative Models)" ----
    Hypothesis(
        hid="H-C1",
        statement="Fuzzy Dark Matter (m ~ 1e-22 eV) does not explain Delta spikes.",
        source_section="File 1 §2.8 / §3 Tier C; File 2 §4.3",
        claimed_script="fdm_comparison.py",
        claimed_data="SDSS",
        claimed_criterion="Delta spikes mismatch FDM predictions",
        status="BLOCKED_PROVENANCE",
        blocker="No FDM predictive model is implemented in this repo, so 'FDM predictions' "
                "has no referent. " + _B_DELTA_QUARANTINE + " A null test that the favoured "
                "model cannot fail is not a null test; P4 (sibling families) is served "
                "properly by pipeline/siblings.py, which the runner does use.",
        claim_gap="Nothing to compare against, and the framing is the problem: the brief "
                  "states the expected outcome as the alternative model *failing*, which "
                  "makes it a confirmation exercise rather than a null test. A genuine null "
                  "test states in advance what result would favour the alternative.",
    ),
    Hypothesis(
        hid="H-C2",
        statement="SIDM does not fit tidal streams better than Chameleon EFT (Delta-AIC < 10).",
        source_section="File 1 §2.8 / §3 Tier C; File 2 §4.3",
        claimed_script="sidm_comparison.py",
        claimed_data="SDSS/JWST",
        claimed_criterion="Delta-AIC < 10 vs Chameleon EFT",
        status="BLOCKED_DATA",
        blocker=_B_NO_STREAM_DATA + " Neither SIDM nor the Chameleon EFT is implemented.",
        claim_gap="Nothing to compare against. Same confirmation-shaped framing as H-C1: "
                  "the expected outcome is stated as the alternative losing, and SIDM is a "
                  "developed model with published fits while the Chameleon EFT it is "
                  "matched against does not exist in constructed form.",
    ),
    Hypothesis(
        hid="H-C3",
        statement="Modified gravity f(R) does not explain beta_1/beta_2 dominance.",
        source_section="File 1 §2.8 / §3 Tier C; File 2 §4.3",
        claimed_script="modified_gravity_validation.py",
        claimed_data="SDSS/DESI",
        claimed_criterion="beta_1 <= beta_0 + beta_2 for f(R) models",
        status="BLOCKED_PROVENANCE",
        blocker="No f(R) simulation or prediction exists in this repo; predicting Betti "
                "numbers under f(R) requires an N-body suite that is not present and is not "
                "in Stream 3's scope.",
        claim_gap="Nothing to compare against. Also note the criterion is the exact negation "
                  "of H-A1's: the brief predicts beta_1 > beta_0 + beta_2 for the favoured "
                  "model and beta_1 <= beta_0 + beta_2 for f(R), without deriving either, "
                  "so the pair is a coin flip labelled as two predictions.",
    ),
    Hypothesis(
        hid="H-C4",
        statement="A LambdaCDM synthetic mock matches Cooper s7's beta_1/beta_2 "
                  "(null test: beta_1 <= beta_0 + beta_2).",
        source_section="File 1 §3 Tier C; File 2 §4.3",
        claimed_script="cosmic_web_topology.py",
        claimed_data="SDSS/DESI",
        claimed_criterion="beta_1 <= beta_0 + beta_2",
        status="RUNNABLE",
        blocker="",
        claim_gap="Runnable as the *null-bank comparison it should have been in the first "
                  "place*: the real field's Betti numbers against the T0-signed WP-R5 null "
                  "schemes (z-shuffle and angular CSR), reported as percentile ranks. It is "
                  "not a LambdaCDM N-body mock — the repo has none, and the runner says so "
                  "rather than substituting one silently. A structure-destroying "
                  "randomization is a weaker control than a LambdaCDM mock, and the "
                  "percentile it yields must be read accordingly.",
        runner_key="null_percentiles",
    ),
    Hypothesis(
        hid="H-C5",
        statement="A LambdaCDM synthetic mock matches Cooper s7's beta_2.",
        source_section="File 1 §3 Tier C; File 2 §4.3",
        claimed_script="void_suppression_validation.py",
        claimed_data="SDSS/Euclid",
        claimed_criterion="beta_2 (Cooper s7) = beta_2 (LambdaCDM)",
        status="RUNNABLE",
        blocker="",
        claim_gap="Same as H-C4, restricted to beta_2. Reported as a null percentile, never "
                  "as an equality verdict — 'matches' is not a testable relation without a "
                  "tolerance, and the brief states none.",
        runner_key="null_percentiles",
    ),

    # ---- Additional themed hypotheses the brief lists in File 1 §2 but omits from its
    # ---- own consolidated Tier A/B/C list. Included so the registry covers the document.
    Hypothesis(
        hid="H-K3-3",
        statement="Kulikov degenerations stabilize 15 moduli in Cooper s7, giving "
                  "tau_imag ~= 0.972 in high-density voids.",
        source_section="File 1 §2.1",
        claimed_script="moduli_locking_validation.py",
        claimed_data="SDSS",
        claimed_criterion="tau_imag ~= 0.972 in high-density voids",
        status="BLOCKED_PROVENANCE",
        blocker="Unprovenanced constant (tau_imag = 0.972, no derivation, no certificate) "
                "plus an incoherent target region ('high-density voids' is a contradiction "
                "in terms). The '15 moduli' figure does trace — it is 18 - 3 from "
                "C2_cooper_s7_partner.json against the order-3 operator "
                "(briefs/GATE_G1L_RULING_2026_07_25.md §4) — but that count is the "
                "flat-direction wall (a_2), i.e. the *problem*, and this hypothesis asserts "
                "it as the solution without supplying the Kulikov argument.",
        constants=(
            Constant(
                symbol="tau_imag",
                value="0.972",
                provenance="NONE. Attributed to Friedman & Morgan (1994); no value given "
                           "there for this compactification, and no repo certificate.",
                is_traced=False,
            ),
            Constant(
                symbol="n_flat_directions",
                value="15",
                provenance="C2_cooper_s7_partner.json (rho=4, T=18) minus order-3 operator "
                           "rank: 18 - 3 = 15. Traced; recorded in "
                           "briefs/GATE_G1L_RULING_2026_07_25.md §4 as the a_2 wall.",
                is_traced=True,
            ),
        ),
        claim_gap="Asserts the wall is cleared without clearing it.",
    ),
    Hypothesis(
        hid="H-CM-5",
        statement="Long-range forces in cosmic voids from chameleon screening; kappa peaks "
                  "align with Delta spikes > 80%.",
        source_section="File 1 §2.2",
        claimed_script="weak_lensing_overlay.py",
        claimed_data="Euclid",
        claimed_criterion="kappa peaks align with Delta spikes > 80%",
        status="BLOCKED_DATA",
        blocker=_B_SHEAR + " " + _B_DELTA_QUARANTINE + " Third restatement of H-B5's "
                "criterion in the same document.",
        claim_gap="Same two missing operands as H-B5. That the same alignment criterion "
                  "appears three times (H-B5, H-B8, here) under three different theoretical "
                  "motivations is itself informative: one measurement is being asked to "
                  "support several distinct claims, which no single number can do.",
    ),
)


# --------------------------------------------------------------------------------------
# Accessors
# --------------------------------------------------------------------------------------

def runnable() -> tuple[Hypothesis, ...]:
    """Hypotheses whose named statistic can actually be computed from manifested data."""
    return tuple(h for h in HYPOTHESES if h.status == "RUNNABLE")


def blocked() -> tuple[Hypothesis, ...]:
    """Hypotheses that cannot be run, each carrying a specific cited reason."""
    return tuple(h for h in HYPOTHESES if h.is_blocked)


def by_id(hid: str) -> Hypothesis:
    for h in HYPOTHESES:
        if h.hid == hid:
            return h
    raise KeyError(f"no hypothesis {hid!r} in registry")


def status_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    for h in HYPOTHESES:
        counts[h.status] = counts.get(h.status, 0) + 1
    return counts


def runner_keys() -> tuple[str, ...]:
    """Distinct dispatch keys the runner must implement, in registry order."""
    seen: list[str] = []
    for h in runnable():
        if h.runner_key and h.runner_key not in seen:
            seen.append(h.runner_key)
    return tuple(seen)


def assert_label_permitted(label: str) -> None:
    """Refuse any label WP-H may not emit. Called by the runner before writing output.

    This is belt-and-braces on top of gate G1-L: even if the gate were opened, WP-H's own
    authorization (docs/WP_H_T0_AUTHORIZATION_2026_07_25.md §2) withholds TEST/FIT, so the
    restriction has to live here too rather than being inherited.
    """
    if label in FORBIDDEN_LABELS:
        raise ValueError(
            f"label {label!r} is forbidden for WP-H outputs. WP-H is "
            f"{TAG} by T0 authorization (docs/WP_H_T0_AUTHORIZATION_2026_07_25.md §2); "
            "gate G1-L governs TEST/FIT independently and is closed."
        )
    if label != TAG:
        raise ValueError(f"WP-H emits only {TAG!r}, got {label!r}")


# Generated-by: Claude Opus 5 (T1) under T0 authorization of 2026-07-25 |
# Verified-by: pipeline/tests/test_hypothesis_registry.py (status/blocker integrity,
# manifest+module existence for RUNNABLE, constant provenance, R-SHEAR guard,
# no-TEST/FIT invariant), executed | Reviewed-by: T0 N — pending Xavier
