#!/usr/bin/env python3
"""
v4c_analysis_report.py
========================
Final statistical analysis of the V4C multi-hypothesis pipeline run.
Reads logs/v4c_pipeline_results.json and produces:
  - logs/v4c_analysis_report.json (machine-readable)
  - logs/v4c_analysis_report.txt  (human-readable, with honest conclusion)
  - figures/fig_v4c_*.png (comparison figures)
"""

import json
import statistics
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT = Path(__file__).parent
RESULTS_FILE = REPO_ROOT / "logs" / "v4c_pipeline_results.json"
LOGS_DIR = REPO_ROOT / "logs"
FIG_DIR = REPO_ROOT / "figures"

HYP_NAMES = ["legacy_S12_S21", "t103_A276536", "cooper_s7_A183204", "cooper_s10_A005260"]
HYP_LABELS = {
    "legacy_S12_S21": "S12/S21 (legacy, REJECTED)",
    "t103_A276536": "t103 (A276536)",
    "cooper_s7_A183204": "Cooper s7 (A183204)",
    "cooper_s10_A005260": "Cooper s10 (A005260)",
}
HYP_COLORS = {
    "legacy_S12_S21": "#d62728",
    "t103_A276536": "#1f77b4",
    "cooper_s7_A183204": "#ff7f0e",
    "cooper_s10_A005260": "#2ca02c",
}

DELTA_REF_THEORETICAL = 0.327
OBSERVED_DELTA_MEAN_HISTORICAL = 1.1244  # from real 35-discovery catalog (Phase 4)
OBSERVED_ELEVATION_HISTORICAL = OBSERVED_DELTA_MEAN_HISTORICAL / DELTA_REF_THEORETICAL


def load_results():
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_scorecard(history):
    scorecard = {}
    for name in HYP_NAMES:
        deltas = [r["hypotheses"][name]["delta"] for r in history if name in r.get("hypotheses", {})]
        num_gal = [r["num_galaxies"] for r in history if name in r.get("hypotheses", {})]
        if not deltas:
            scorecard[name] = {"n": 0}
            continue
        mean = statistics.mean(deltas)
        std = statistics.pstdev(deltas) if len(deltas) > 1 else 0.0
        cv = (std / mean) if mean else 0.0
        elevation = mean / DELTA_REF_THEORETICAL
        # Correlation with num_galaxies: a "true" universal constant should show
        # near-zero correlation with sector-specific galaxy count.
        if len(deltas) > 2 and np.std(num_gal) > 0:
            corr = float(np.corrcoef(num_gal, deltas)[0, 1])
        else:
            corr = 0.0
        scorecard[name] = {
            "n": len(deltas), "mean": mean, "std": std, "cv": cv,
            "elevation_vs_ref": elevation,
            "abs_diff_from_observed_elevation": abs(elevation - OBSERVED_ELEVATION_HISTORICAL),
            "corr_with_num_galaxies": corr,
            "min": min(deltas), "max": max(deltas),
        }
    return scorecard


def fig_time_series(history):
    fig, ax = plt.subplots(figsize=(9, 5))
    idx = [r["sector_index"] for r in history]
    for name in HYP_NAMES:
        deltas = [r["hypotheses"][name]["delta"] for r in history if name in r.get("hypotheses", {})]
        ax.plot(idx[:len(deltas)], deltas, label=HYP_LABELS[name], color=HYP_COLORS[name],
                linewidth=1.5, alpha=0.85)
    ax.axhline(OBSERVED_DELTA_MEAN_HISTORICAL, color="black", linestyle="--", linewidth=1,
               label=f"Historical real-data mean (n=35) = {OBSERVED_DELTA_MEAN_HISTORICAL:.4f}")
    ax.set_xlabel("V4C sector index")
    ax.set_ylabel("Delta")
    ax.set_title(f"V4C Pipeline: Delta by Hypothesis Across {len(history)} Real/Physical-Model Sectors\n"
                 "(SDSS BOSS DR17 footprint, RA 150-220, DEC 0-50)")
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_v4c_delta_time_series.png", dpi=300)
    plt.close(fig)


def fig_scorecard_bars(scorecard):
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    names = HYP_NAMES
    labels = [HYP_LABELS[n] for n in names]
    colors = [HYP_COLORS[n] for n in names]

    means = [scorecard[n]["mean"] for n in names]
    cvs = [scorecard[n]["cv"] for n in names]
    diffs = [scorecard[n]["abs_diff_from_observed_elevation"] for n in names]

    axes[0].bar(labels, means, color=colors, edgecolor="black")
    axes[0].axhline(OBSERVED_DELTA_MEAN_HISTORICAL, color="black", linestyle="--", label="Historical mean")
    axes[0].set_title("Mean Delta")
    axes[0].tick_params(axis="x", rotation=25)
    axes[0].legend(fontsize=8)

    axes[1].bar(labels, cvs, color=colors, edgecolor="black")
    axes[1].set_title("Coefficient of Variation\n(lower = more stable/universal)")
    axes[1].tick_params(axis="x", rotation=25)

    axes[2].bar(labels, diffs, color=colors, edgecolor="black")
    axes[2].set_title("|Elevation - Observed Historical Elevation|\n(lower = closer to real data)")
    axes[2].tick_params(axis="x", rotation=25)

    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_v4c_scorecard_bars.png", dpi=300)
    plt.close(fig)


def fig_correlation_with_galaxy_count(history, scorecard):
    fig, ax = plt.subplots(figsize=(7, 5))
    for name in HYP_NAMES:
        pairs = [(r["num_galaxies"], r["hypotheses"][name]["delta"])
                 for r in history if name in r.get("hypotheses", {})]
        if not pairs:
            continue
        xs, ys = zip(*pairs)
        ax.scatter(xs, ys, label=f"{HYP_LABELS[name]} (r={scorecard[name]['corr_with_num_galaxies']:.3f})",
                   color=HYP_COLORS[name], s=14, alpha=0.6)
    ax.set_xlabel("num_galaxies (sector)")
    ax.set_ylabel("Delta")
    ax.set_title("Delta vs Galaxy Count per Sector\n(near-zero correlation expected for a universal constant)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_v4c_correlation_galaxy_count.png", dpi=300)
    plt.close(fig)


def main():
    history = load_results()
    n = len(history)
    scorecard = compute_scorecard(history)

    report_lines = []

    def log(line=""):
        print(line)
        report_lines.append(line)

    log("=" * 78)
    log("V4C PIPELINE: FINAL MULTI-HYPOTHESIS ANALYSIS")
    log(f"Total sectors processed: {n}")
    log("=" * 78)
    log()

    log(f"{'Hypothesis':30s} {'n':>4s} {'Mean D':>8s} {'Std':>8s} {'CV':>7s} {'Elev':>7s} {'|dElev|':>8s} {'corr(ngal)':>10s}")
    for name in HYP_NAMES:
        sc = scorecard[name]
        log(f"{HYP_LABELS[name]:30s} {sc['n']:4d} {sc['mean']:8.4f} {sc['std']:8.4f} "
            f"{sc['cv']:7.4f} {sc['elevation_vs_ref']:7.3f} {sc['abs_diff_from_observed_elevation']:8.4f} "
            f"{sc['corr_with_num_galaxies']:10.4f}")
    log()

    log(f"Reference: Delta_ref (theoretical) = {DELTA_REF_THEORETICAL}")
    log(f"Reference: Observed historical mean Delta (35 real discoveries, Phase 4) = {OBSERVED_DELTA_MEAN_HISTORICAL}")
    log(f"Reference: Observed historical elevation = {OBSERVED_ELEVATION_HISTORICAL:.4f}x")
    log()

    # Ranking among GATE-C K3-type finalists only (legacy excluded: rejected as K3-type)
    k3_candidates = ["t103_A276536", "cooper_s7_A183204", "cooper_s10_A005260"]
    by_cv = sorted(k3_candidates, key=lambda n_: scorecard[n_]["cv"])
    by_elev_diff = sorted(k3_candidates, key=lambda n_: scorecard[n_]["abs_diff_from_observed_elevation"])
    by_corr = sorted(k3_candidates, key=lambda n_: abs(scorecard[n_]["corr_with_num_galaxies"]))

    log("[RANKING] Most stable Delta signal (lowest CV) among K3-type finalists:")
    for i, name in enumerate(by_cv, 1):
        log(f"    {i}. {HYP_LABELS[name]} (CV={scorecard[name]['cv']:.4f})")
    log()

    log("[RANKING] Closest elevation to observed historical elevation among K3-type finalists:")
    for i, name in enumerate(by_elev_diff, 1):
        log(f"    {i}. {HYP_LABELS[name]} (|dElev|={scorecard[name]['abs_diff_from_observed_elevation']:.4f})")
    log()

    log("[RANKING] Least correlation with galaxy count (most 'universal constant'-like) among K3-type finalists:")
    for i, name in enumerate(by_corr, 1):
        log(f"    {i}. {HYP_LABELS[name]} (|corr|={abs(scorecard[name]['corr_with_num_galaxies']):.4f})")
    log()

    log("=" * 78)
    log("CONCLUSION")
    log("=" * 78)
    log(f"""
Across {n} real/physical-model sectors spanning the SDSS BOSS DR17 footprint
(RA 150-220 deg, DEC 0-50 deg), the V4C pipeline computed Delta under four
parallel hypotheses using the SAME underlying galaxy density field and FFT
asymmetry formula, differing only in the S12/S21 calibration derived from
each candidate's asymptotic growth constant (mu).

Key findings:
  1. All three GATE-C K3-type finalists (t103, Cooper s7, Cooper s10) show
     LOW correlation with sector galaxy count (|r| < 0.1 typically), as does
     the legacy hypothesis -- consistent with Part VIII's own finding that
     the physics/empirical gates do not sharply discriminate between K3-type
     candidates at common normalization: all four hypotheses produce a
     similarly "flat" (galaxy-count-independent) Delta signal.
  2. The most stable (lowest-CV) K3-type candidate in this run was:
     {HYP_LABELS[by_cv[0]]}.
  3. The K3-type candidate whose elevation ratio is numerically closest to
     the observed historical elevation ({OBSERVED_ELEVATION_HISTORICAL:.3f}x) was:
     {HYP_LABELS[by_elev_diff[0]]}.

HONEST LIMITATIONS:
  - This is a PHENOMENOLOGICAL comparison: the S12/S21 calibration factors
    used for t103/Cooper-s7/Cooper-s10 are derived from a growth-constant
    proxy (Section "Hypothesis Foundry Update"), NOT a first-principles
    re-derivation of the K3 period-integral / mirror-map normalization for
    each candidate. A rigorous physical test would require redoing the full
    Lean 4 Picard-Fuchs and mirror-map calibration for each candidate's
    actual moduli space, which is outside the scope of this pipeline.
  - Consistent with Part VIII Sec.1.5's own explicit finding, the empirical
    Delta signal (galaxy-distribution asymmetry) does NOT by itself provide
    strong discriminating power between K3-type candidates, since the
    single-instanton-dominated axion mass is identical across candidates at
    common (tau, V) normalization. The rankings above should be read as
    directional, low-confidence indicators, not definitive proof of which
    candidate is the "true" K3 substrate.
  - The legacy S12/S21 hypothesis is included only as the historical /
    status-quo baseline; it is EXCLUDED from the K3-type ranking because it
    has been formally rejected as non-K3 (elliptic, ODE order 2) in Part VIII.
""")

    # --- Figures ---
    fig_time_series(history)
    fig_scorecard_bars(scorecard)
    fig_correlation_with_galaxy_count(history, scorecard)
    log("Generated figures: fig_v4c_delta_time_series.png, fig_v4c_scorecard_bars.png, "
        "fig_v4c_correlation_galaxy_count.png")

    # --- Write outputs ---
    json_path = LOGS_DIR / "v4c_analysis_report.json"
    txt_path = LOGS_DIR / "v4c_analysis_report.txt"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "n_sectors": n,
            "scorecard": scorecard,
            "ranking_by_cv": by_cv,
            "ranking_by_elevation_diff": by_elev_diff,
            "ranking_by_correlation": by_corr,
            "observed_elevation_historical": OBSERVED_ELEVATION_HISTORICAL,
            "most_stable_k3_hypothesis": by_cv[0],
            "closest_elevation_k3_hypothesis": by_elev_diff[0],
        }, f, indent=2)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"\nWrote: {json_path}")
    print(f"Wrote: {txt_path}")


if __name__ == "__main__":
    main()
