#!/usr/bin/env python3
"""
Publication-quality figures for the t103/Cooper-s7/Cooper-s10 vs legacy
S12/S21 hypothesis comparison. Reads results from
logs/hypothesis_comparison_t103_cooper.json (produced by
hypothesis_comparison_t103_cooper.py) and discoveries_with_sources.json.
"""

import json
import math
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT = Path(__file__).parent.parent
RESULTS_FILE = REPO_ROOT / "logs" / "hypothesis_comparison_t103_cooper.json"
DISCOVERIES_FILE = REPO_ROOT / "discoveries_with_sources.json"
OUT_DIR = Path(__file__).parent
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.size": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "axes.grid": True,
    "grid.alpha": 0.3,
})

COLORS = {
    "t103_A276536": "#1f77b4",
    "cooper_s7_A183204": "#ff7f0e",
    "cooper_s10_A005260": "#2ca02c",
    "legacy_s12_s21": "#d62728",
}


def load_results():
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def fig_sequence_growth(results):
    """Log-scale plot of the three candidate sequences vs n."""
    seqs = results["sequences"]
    fig, ax = plt.subplots(figsize=(7, 5))
    for name, seq in seqs.items():
        n_vals = list(range(len(seq)))
        y_vals = [float(v) for v in seq]
        ax.semilogy(n_vals, y_vals, marker="o", markersize=3,
                    label=name.replace("_", " "), color=COLORS.get(name, "gray"))
    ax.set_xlabel("n")
    ax.set_ylabel("a(n)  (log scale)")
    ax.set_title("GATE-C K3-Type Candidate Sequences\n(exact big-integer terms, n=0..20)")
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig_hypothesis_sequence_growth.png")
    plt.close(fig)


def fig_growth_constants(results):
    """Bar chart of estimated growth constants mu with legacy reference line."""
    growth = results["growth_constants"]
    names = list(growth.keys())
    values = [growth[n] for n in names]

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    bars = ax.bar([n.replace("_A", "\n(A").replace("A276536", "A276536)")
                   .replace("A183204", "A183204)").replace("A005260", "A005260)")
                   for n in names],
                  values, color=[COLORS.get(n, "gray") for n in names], edgecolor="black")
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v + max(values) * 0.02,
                 f"{v:.2f}", ha="center", fontweight="bold", fontsize=9)
    ax.set_ylabel(r"Growth constant $\mu$  (a(n) ~ $\mu^n$)")
    ax.set_title("Asymptotic Growth Constants: GATE-C K3-Type Finalists")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig_hypothesis_growth_constants.png")
    plt.close(fig)


def fig_recurrence_verification(results):
    """Visual confirmation panel: recurrence verified range per candidate."""
    rec = results["recurrence_verification"]
    names = list(rec.keys())
    statuses = [rec[n]["status"] for n in names]
    colors = ["#2ca02c" if s == "VERIFIED" else "#d62728" for s in statuses]

    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    y_pos = np.arange(len(names))
    ax.barh(y_pos, [1] * len(names), color=colors, edgecolor="black", height=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([n.replace("_", " ") for n in names])
    for i, (n, s) in enumerate(zip(names, statuses)):
        rng = rec[n].get("verified_range", "")
        ax.text(0.5, i, f"{s}  ({rng})", ha="center", va="center",
                 fontweight="bold", color="white", fontsize=9)
    ax.set_xlim(0, 1)
    ax.set_xticks([])
    ax.set_title("Independent Exact-Arithmetic Recurrence Verification\n"
                  "(order-2, degree-3, leading coeff. $(n+2)^3$)")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig_hypothesis_recurrence_verification.png")
    plt.close(fig)


def fig_delta_vs_source(results):
    """Real-data Delta comparison across independent surveys, with the
    3.4x reference elevation line, contextualizing where the empirical
    signal sits relative to the theoretical candidate framework."""
    stats = results["real_data_delta_stats"]
    sources = [k for k in stats.keys() if k != "overall"]
    means = [stats[s]["mean"] for s in sources]
    stds = [stats[s]["std"] for s in sources]

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    x_pos = np.arange(len(sources))
    ax.bar(x_pos, means, yerr=stds, capsize=5, color="#4c72b0",
           edgecolor="black", alpha=0.85)
    ax.axhline(0.327, color="green", linestyle=":", label="Reference $\\Delta$ = 0.327")
    ax.axhline(stats["overall"]["mean"], color="red", linestyle="--",
               label=f"Overall mean = {stats['overall']['mean']:.4f}")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(sources, rotation=20, ha="right")
    ax.set_ylabel("$\\Delta$ (K3 asymmetry metric)")
    ax.set_title("Real-Data $\\Delta$ by Independent Survey\n(Euclid Q1, SDSS BOSS DR17, Gaia DR3, Pan-STARRS)")
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig_hypothesis_delta_by_source.png")
    plt.close(fig)


def fig_scorecard(results):
    """Summary scorecard: K3-type validity per candidate."""
    scorecard = results["scorecard"]
    names = [row["candidate"] for row in scorecard]
    k3_type = [row["k3_type"] for row in scorecard]
    colors = ["#d62728" if not v else "#2ca02c" for v in k3_type]
    labels = ["REJECTED\n(elliptic)" if not v else "K3-TYPE\nVALIDATED" for v in k3_type]

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    y_pos = np.arange(len(names))
    ax.barh(y_pos, [1] * len(names), color=colors, edgecolor="black", height=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names)
    for i, lbl in enumerate(labels):
        ax.text(0.5, i, lbl, ha="center", va="center", fontweight="bold",
                 color="white", fontsize=10)
    ax.set_xlim(0, 1)
    ax.set_xticks([])
    ax.invert_yaxis()
    ax.set_title("Hypothesis Scorecard: K3-Type Classification Status\n"
                 "(Part VIII: The Hypothesis Foundry, corrected 2026-07-14)")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig_hypothesis_scorecard.png")
    plt.close(fig)


def main():
    results = load_results()
    fig_sequence_growth(results)
    fig_growth_constants(results)
    fig_recurrence_verification(results)
    fig_delta_vs_source(results)
    fig_scorecard(results)
    print(f"Generated 5 hypothesis-comparison figures in {OUT_DIR}")


if __name__ == "__main__":
    main()
