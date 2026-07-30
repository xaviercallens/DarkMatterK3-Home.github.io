#!/usr/bin/env python3
"""Data-lake harvest: poll GCS AlphaEvolve checkpoints, regenerate live convergence figures.

T0 Directive 1 (2026-07-30). Epistemic labeling per ratified F5b block:
figures are labeled PHENOMENOLOGICAL CONVERGENCE, never "posterior" in the
Bayesian sense. The checkpoint field `kodaira_fiber_type` is deliberately
ignored: Kodaira readings for this family are RETRACTED (E-008/E-009,
Stream 2 ledger) and must not propagate into any figure or caption.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

BUCKET = "gs://socrateai-datalake-gen-lang-client-0625573011/checkpoints/"
REPO = Path(__file__).resolve().parent.parent
LOCAL = REPO / "data" / "datalake_checkpoints"
OUT = REPO / "figures" / "live"

PARAMS = ["w0", "omega_m", "h0", "pta_f_monopole", "s8_gradient"]
PARAM_LABELS = {
    "w0": r"$w_0$",
    "omega_m": r"$\Omega_m$",
    "h0": r"$H_0$",
    "pta_f_monopole": r"$f_{\rm PTA}$ [Hz]",
    "s8_gradient": r"$S_8$ grad",
}
F5B_TAG = "PHENOMENOLOGICAL CONVERGENCE (F5b) — evolutionary population, not a Bayesian posterior"


def sync():
    LOCAL.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["gsutil", "-m", "-q", "rsync", BUCKET, str(LOCAL)],
        check=True,
        timeout=600,
    )


def load():
    gens = []
    for p in sorted(LOCAL.glob("*_gen_*.json")):
        try:
            gens.append(json.loads(p.read_text()))
        except (json.JSONDecodeError, OSError) as e:
            print(f"skip {p.name}: {e}", file=sys.stderr)
    gens.sort(key=lambda d: d.get("generation", 0))
    return gens


def fig_loss(gens, run_id):
    g = [d["generation"] for d in gens]
    total = [d["best_candidate"]["chi2_loss"] for d in gens]
    comps = {}
    for key in ("chi2_w0", "chi2_om", "chi2_h0"):
        vals = [d["best_candidate"].get("likelihood", {}).get(key) for d in gens]
        if all(v is not None for v in vals):
            comps[key] = vals

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.semilogy(g, np.maximum(total, 1e-12), "o-", color="#1f77b4", label=r"total $\chi^2$", lw=2)
    for key, vals in comps.items():
        ax.semilogy(g, np.maximum(vals, 1e-12), "--", alpha=0.6, label=key.replace("chi2_", r"$\chi^2$ "))
    ax.set_xlabel("Generation")
    ax.set_ylabel(r"best-candidate $\chi^2$ loss (log)")
    ax.set_title(f"AlphaEvolve run {run_id} — best-candidate loss\n{F5B_TAG}", fontsize=9)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "chi2_loss_curve.png", dpi=200)
    plt.close(fig)


def fig_corner(gens, run_id, last_n=10):
    pts = {p: [] for p in PARAMS}
    for d in gens[-last_n:]:
        for cand in d.get("population", []):
            ph = cand.get("phenotype", {})
            if all(p in ph for p in PARAMS):
                for p in PARAMS:
                    pts[p].append(ph[p])
    n = len(PARAMS)
    if not pts[PARAMS[0]]:
        print("no phenotype points; corner skipped", file=sys.stderr)
        return
    arr = {p: np.asarray(v, dtype=float) for p, v in pts.items()}

    fig, axes = plt.subplots(n, n, figsize=(2.2 * n, 2.2 * n))
    for i, pi in enumerate(PARAMS):
        for j, pj in enumerate(PARAMS):
            ax = axes[i, j]
            if j > i:
                ax.set_visible(False)
                continue
            if i == j:
                ax.hist(arr[pi], bins=25, color="#1f77b4", alpha=0.8)
            else:
                ax.scatter(arr[pj], arr[pi], s=4, alpha=0.4, color="#1f77b4")
            if i == n - 1:
                ax.set_xlabel(PARAM_LABELS[pj], fontsize=8)
            else:
                ax.set_xticklabels([])
            if j == 0 and i > 0:
                ax.set_ylabel(PARAM_LABELS[pi], fontsize=8)
            else:
                ax.set_yticklabels([])
            ax.tick_params(labelsize=6)
    fig.suptitle(
        f"AlphaEvolve run {run_id} — population phenotypes, last {last_n} generations\n{F5B_TAG}",
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(OUT / "phenotype_corner.png", dpi=200)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sync()
    gens = load()
    if not gens:
        print("no checkpoints found")
        return 1
    run_id = gens[-1].get("run_id", "unknown")
    fig_loss(gens, run_id)
    fig_corner(gens, run_id)
    status = {
        "harvested_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "run_id": run_id,
        "n_checkpoints": len(gens),
        "latest_generation": gens[-1]["generation"],
        "best_chi2_loss": gens[-1]["best_candidate"]["chi2_loss"],
        "best_candidate_id": gens[-1]["best_candidate"].get("candidate_id"),
        "f5b_label": F5B_TAG,
        "kodaira_field_policy": "ignored per E-008/E-009 retraction",
    }
    (OUT / "last_harvest.json").write_text(json.dumps(status, indent=2) + "\n")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
