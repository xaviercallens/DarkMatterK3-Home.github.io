#!/usr/bin/env python3
"""
WP-E6 (m,f) grid — built-in structural controls, run standalone.

Relocated from phase1_work/grid_controls/ (gitignored scratch) into pipeline/
so this result is part of the tracked audit trail. The emulator wrapper it
imports (emu_predict.py) stays under phase1_work/agent1_emulator/ and stays
gitignored — that directory also holds the cloned lya-mfdm repo (NO LICENSE
upstream, never redistributed); only the wrapper's *output* is tracked here,
not the wrapper or the cloned weights themselves.

label: CONTROL (NOT TEST, NOT FIT — see prereg-pipeline skill / CLAUDE.md rule 3).
This script exercises the emulator's own internal consistency. It makes no
comparison against any real/observational dataset and touches no pinned
prediction, so the TEST/FIT labeling regime (reserved for comparisons against
PREDICTION.md post-G1-pin) does not apply. It is a pipeline diagnostic.

Grid source: briefs/T0_MF_GRID_DEFINITION_2026_07_27.md (hash-anchored,
[T0-DELEGATED], commit 27cff4a). Two built-in controls defined there, §3:

  1. f=0 column byte-identity check (§3, f-axis row "0"): at f_FDM=0 the
     CDM-only branch of predict_pk() is taken (f <= F_EPS -> logp = cdm_st),
     and cdm_st depends only on x_cdm = [z, zrei, ha, hs, taueff] -- no m.
     So for fixed IGM nuisance point and z, all 8 grid mass values must
     produce byte-identical P1D(k) vectors.

  2. m=-19.1 null row check (§3, mass-axis row "-19.1"): published paper
     (arXiv:2606.06969) reports no effective 95% CL bound on f_FDM at this
     mass (A3 in the brief). Running all 7 grid f values at m=-19.1 should
     show small/negligible suppression relative to the f=0 baseline at the
     same mass -- a large suppression here would indicate a pipeline defect
     (e.g. sign error, wrong branch, misapplied scaler), not physics.

Both checks use z_str="4.2" (A4, the only usable redshift slice) and the
representative IGM nuisance point from emu_predict.py's own __main__ smoke
test: zrei=10.5, ha=2.0, hs=0.0, taueff=1.0 (medians of the training LHS).
These nuisance parameters are NOT part of the (m,f) grid; they are held
fixed here purely to exercise checks 1 and 2, not as any kind of estimate
or profiled/marginalized value (that is a later, separate Phase 2 task).

This is a structural/pipeline diagnostic, not a physics result. Do not cite
the printed suppression numbers as constraining anything.
"""
import json
import os
import pickle
import sys
from datetime import datetime, timezone

import numpy as np
import sklearn

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "..", "phase1_work", "agent1_emulator"))
from emu_predict import load_nn_system, predict_pk, K_BINS, NN_EMU_DIR  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_ROOT, "data", "derived")

# Grid axes, verbatim from briefs/T0_MF_GRID_DEFINITION_2026_07_27.md §3.
MASS_GRID = [-22.9, -22.5, -22.0, -21.5, -21.0, -20.5, -20.0, -19.1]
FRAC_GRID = [0.0, 0.05, 0.10, 0.20, 0.35, 0.60, 0.99]
Z_STR = "4.2"

# Representative IGM nuisance point, verbatim from emu_predict.py __main__.
ZREI, HA, HS, TAUEFF = 10.5, 2.0, 0.0, 1.0

# Judgment threshold for check 2 (see rationale printed alongside the result).
NULL_ROW_SUPPRESSION_THRESHOLD = 0.10  # 10% relative suppression


def load_nn_system_with_provenance():
    """Load the NN system while capturing any sklearn pickle-version
    mismatch warning, so the coordinator has environment provenance for
    this diagnostic. The mismatch (if any) is a MinMaxScaler affine
    transform re-hydrated under a newer sklearn -- low risk, but recorded
    rather than silently swallowed, per this repo's provenance discipline."""
    import warnings
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        nn_pack = load_nn_system()
        messages = [str(w.message) for w in caught
                    if "sklearn" in str(w.message).lower()
                    or "version" in str(w.message).lower()]
    provenance = {
        "runtime_sklearn_version": sklearn.__version__,
        "pickle_load_warnings": messages,
    }
    return nn_pack, provenance


def check1_f0_byte_identity(nn_pack):
    """f=0 column: P1D(k) must be byte-identical across all 8 mass values."""
    print("=" * 78)
    print("CHECK 1: f=0 column byte-identity (m-independence at CDM-only branch)")
    print("=" * 78)

    pk_by_mass = {}
    for m in MASS_GRID:
        pk = predict_pk(nn_pack, m, 0.0, ZREI, HA, HS, TAUEFF, Z_STR)
        pk_by_mass[m] = pk

    ref_m = MASS_GRID[0]
    ref_pk = pk_by_mass[ref_m]
    all_equal = True
    per_mass_results = []
    for m in MASS_GRID:
        pk = pk_by_mass[m]
        equal = bool(np.array_equal(pk, ref_pk))
        max_abs_diff = float(np.max(np.abs(pk - ref_pk)))
        all_equal = all_equal and equal
        per_mass_results.append({
            "m": m,
            "byte_identical_to_ref": equal,
            "max_abs_diff_vs_ref": max_abs_diff,
        })
        print(f"  m={m:>7.1f}: byte_identical_to_ref(m={ref_m})={equal}  "
              f"max|diff|={max_abs_diff:.3e}")

    print(f"\n  PASS (all 8 byte-identical): {all_equal}")

    return {
        "check": "f0_column_byte_identity",
        "label": "CONTROL",
        "reference_mass": ref_m,
        "grid_mass_values": MASS_GRID,
        "per_mass": per_mass_results,
        "all_byte_identical": all_equal,
        "verdict": "PASS" if all_equal else "FAIL",
        "k_bins_s_per_km": K_BINS.tolist(),
        "pk_reference": ref_pk.tolist(),
    }


def check2_null_row_suppression(nn_pack):
    """m=-19.1 row: suppression relative to f=0 baseline should be small."""
    print()
    print("=" * 78)
    print("CHECK 2: m=-19.1 null row (published: no effective bound at this mass)")
    print("=" * 78)

    m = -19.1
    pk_baseline = predict_pk(nn_pack, m, 0.0, ZREI, HA, HS, TAUEFF, Z_STR)

    per_f_results = []
    max_abs_suppression_overall = 0.0
    for f in FRAC_GRID:
        pk = predict_pk(nn_pack, m, f, ZREI, HA, HS, TAUEFF, Z_STR)
        suppression = 1.0 - pk / pk_baseline  # per k-bin, relative to f=0; signed
        max_abs_suppression = float(np.max(np.abs(suppression)))
        mean_abs_suppression = float(np.mean(np.abs(suppression)))
        signed_min = float(np.min(suppression))
        signed_max = float(np.max(suppression))
        max_abs_suppression_overall = max(max_abs_suppression_overall, max_abs_suppression)
        per_f_results.append({
            "f": f,
            "suppression_per_k": suppression.tolist(),
            "signed_min_suppression": signed_min,
            "signed_max_suppression": signed_max,
            "max_abs_suppression": max_abs_suppression,
            "mean_abs_suppression": mean_abs_suppression,
        })
        print(f"  f={f:>5.2f}: max|1-P/P0|={max_abs_suppression:.4f}  "
              f"mean|1-P/P0|={mean_abs_suppression:.4f}  "
              f"signed range=[{signed_min:.4f}, {signed_max:.4f}]")

    verdict = "PASS" if max_abs_suppression_overall < NULL_ROW_SUPPRESSION_THRESHOLD else "FAIL"
    print(f"\n  Threshold: max|1-P/P0| < {NULL_ROW_SUPPRESSION_THRESHOLD} "
          f"across all 7 f values and all k-bins")
    print(f"  Observed max|1-P/P0| over all f, all k: {max_abs_suppression_overall:.4f}")
    print(f"  Verdict: {verdict}")
    print(
        "\n  Threshold rationale: 10% relative suppression is an unanchored order-of-\n"
        "  magnitude pipeline-defect detector, not a physics tolerance -- no claim\n"
        "  about the paper's reported suppression scale at any mass is made or relied\n"
        "  on here. It is anchored instead against CHECK 3 below, which measures the\n"
        "  emulator's own suppression at the maximum-discrimination mass (-22.9) at\n"
        "  the same f: if that measured contrast is >> this threshold while this row\n"
        "  stays << threshold, the null row is behaving as a null should. If CHECK 3\n"
        "  also comes back near this row's magnitude, that is a discriminating\n"
        "  failure signal (see CHECK 3) and this PASS should be read as vacuous, not\n"
        "  as physics confirmation."
    )

    return {
        "check": "null_row_m_minus_19_1_suppression",
        "label": "CONTROL",
        "m": m,
        "grid_frac_values": FRAC_GRID,
        "threshold_max_abs_suppression": NULL_ROW_SUPPRESSION_THRESHOLD,
        "per_f": per_f_results,
        "max_abs_suppression_overall": max_abs_suppression_overall,
        "verdict": verdict,
        "k_bins_s_per_km": K_BINS.tolist(),
    }


def check3_mass_contrast_positive_control(nn_pack):
    """Positive control: at fixed f=0.10, measure suppression relative to
    each mass's own f=0 baseline, across ALL 8 grid mass values. Per the
    brief, -22.9 is the maximum-discrimination cell and -22.0 carries the
    published f<0.12 bound; -19.1 is the null cell used in check 2. If m is
    actually plumbed into the emulator's residual branch, suppression at
    -22.9/-22.0 should be materially larger than at -19.1 (check 2's row).
    If it is NOT -- if all masses show ~the same tiny suppression as
    check 2 -- that means m is not doing anything (e.g. dropped/misindexed
    upstream of the scaler), and check 2's PASS is vacuous, not a genuine
    null-recovery result. This check exists to make that failure mode
    visible; it is not a reproduction of the paper's bound."""
    print()
    print("=" * 78)
    print("CHECK 3: mass contrast, positive control (f=0.10 fixed, m swept)")
    print("=" * 78)

    f = 0.10
    per_mass_results = []
    for m in MASS_GRID:
        pk_baseline = predict_pk(nn_pack, m, 0.0, ZREI, HA, HS, TAUEFF, Z_STR)
        pk = predict_pk(nn_pack, m, f, ZREI, HA, HS, TAUEFF, Z_STR)
        suppression = 1.0 - pk / pk_baseline
        max_abs_suppression = float(np.max(np.abs(suppression)))
        mean_abs_suppression = float(np.mean(np.abs(suppression)))
        per_mass_results.append({
            "m": m,
            "max_abs_suppression": max_abs_suppression,
            "mean_abs_suppression": mean_abs_suppression,
        })
        print(f"  m={m:>7.1f}: max|1-P/P0|={max_abs_suppression:.4f}  "
              f"mean|1-P/P0|={mean_abs_suppression:.4f}")

    null_row_value = next(r["max_abs_suppression"] for r in per_mass_results if r["m"] == -19.1)
    max_discrim_value = next(r["max_abs_suppression"] for r in per_mass_results if r["m"] == -22.9)
    ratio = max_discrim_value / null_row_value if null_row_value > 0 else float("inf")

    # Discriminating verdict: m must actually move the output. If the
    # maximum-discrimination mass (-22.9) doesn't show materially more
    # suppression than the null mass (-19.1) at the same f, m is not
    # plumbed through and check 2's PASS is vacuous.
    m_is_discriminating = ratio > 3.0
    verdict = "PASS" if m_is_discriminating else "FAIL"

    print(f"\n  -22.9 (max-discrimination) max|1-P/P0| = {max_discrim_value:.4f}")
    print(f"  -19.1 (null row, from check 2 logic)  max|1-P/P0| = {null_row_value:.4f}")
    print(f"  Ratio = {ratio:.2f}x")
    print(f"  Verdict (m is discriminating, ratio > 3x): {verdict}")

    return {
        "check": "mass_contrast_positive_control",
        "label": "CONTROL",
        "f_fixed": f,
        "grid_mass_values": MASS_GRID,
        "per_mass": per_mass_results,
        "max_discrimination_mass_value": max_discrim_value,
        "null_row_mass_value": null_row_value,
        "ratio_max_discrim_over_null": ratio,
        "verdict": verdict,
        "verdict_rule": "PASS iff ratio(-22.9 suppression / -19.1 suppression) > 3.0",
    }


def main():
    print("Loading NN emulator system...")
    nn_pack, sklearn_provenance = load_nn_system_with_provenance()
    print("Loaded.\n")
    if sklearn_provenance["pickle_load_warnings"]:
        print("  NOTE: sklearn pickle-version warning(s) captured (see report JSON):")
        for msg in sklearn_provenance["pickle_load_warnings"]:
            print(f"    {msg}")
        print()

    result1 = check1_f0_byte_identity(nn_pack)
    result2 = check2_null_row_suppression(nn_pack)
    result3 = check3_mass_contrast_positive_control(nn_pack)

    if result3["verdict"] == "FAIL":
        print(
            "\n  WARNING: CHECK 3 FAILED -- mass does not discriminate at the "
            "expected margin. CHECK 2's PASS should be treated as VACUOUS, not "
            "as evidence of a genuine null. See CHECK 3 output above."
        )

    report = {
        "label": "CONTROL",
        "purpose": (
            "Built-in structural/pipeline controls for the WP-E6 (m,f) grid "
            "defined in briefs/T0_MF_GRID_DEFINITION_2026_07_27.md, plus one "
            "additional positive control (check 3) added to make sure checks "
            "1/2 aren't vacuously passing because m isn't plumbed through at "
            "all. NOT a physics result, NOT a comparison against real data, "
            "NOT gated by the PREDICTION.md pin (rule 1 in CLAUDE.md) -- this "
            "exercises only the emulator's own internal consistency."
        ),
        "grid_source": "briefs/T0_MF_GRID_DEFINITION_2026_07_27.md",
        "z_str": Z_STR,
        "igm_nuisance_point": {"zrei": ZREI, "ha": HA, "hs": HS, "taueff": TAUEFF},
        "igm_nuisance_point_source": (
            "emu_predict.py __main__ smoke test (training-LHS medians); "
            "NOT a profiled/marginalized value -- that is a separate, later "
            "Phase 2 task."
        ),
        "environment_provenance": sklearn_provenance,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "checks": [result1, result2, result3],
        "overall_verdict": (
            "PASS" if all(r["verdict"] == "PASS" for r in (result1, result2, result3))
            else "FAIL"
        ),
        "overall_verdict_note": (
            "check2's PASS is only meaningful if check3 also PASSes (i.e. mass "
            "measurably discriminates elsewhere on the grid); overall_verdict "
            "requires all three."
        ),
    }

    out_path = os.path.join(OUT_DIR, "wp_e6_grid_controls_report_2026_07_28.json")
    with open(out_path, "w") as fh:
        json.dump(report, fh, indent=2)

    print()
    print("=" * 78)
    print(f"OVERALL VERDICT: {report['overall_verdict']}")
    print(f"Report written to: {out_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
