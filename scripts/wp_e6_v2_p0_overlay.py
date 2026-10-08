#!/usr/bin/env python3
"""wp_e6_v2_p0_overlay.py -- WP-E6 v2 Phase 0 (literature re-survey): revised openness overlay and recomputed
decisive-and-open cell count. LITERATURE-TABLE ARITHMETIC ONLY (CLAUDE.md rule 1): no data, no comparison, no
TEST/FIT label. Authorized by T0 D-g (briefs/T0_DECISIONS_2026_10_08.md): Phase 0 only.

It does NOT touch pipeline/. It reads
  * the existing pre-flight artifact data/derived/wp_e6b_lya_adequacy_preflight_2026_07_27.json (the 13 x 20 (m, f) grid and each
    cell's reaches_2sigma flag under the pre-flight's OPTIMISTIC proxy -- the 'generous filter' of the proposal's stop condition P0), and
  * a bounds table data/literature/fdm_mixed_fraction_bounds_2026_10_08.csv, one published statement per row, with its locator and quote.

Rule (identical to scripts/wp_e6b_lya_adequacy_preflight.genuinely_open_cell for the rows it already knew):
  a cell (m, f), f < 1, is CLOSED by a row iff the row is kind == 'mixed_bound', its evidence is accepted, m_lo <= m <= m_hi (0.5% grid
  tolerance), and f >= f_max.  f = 1 cells are governed by the pure-FDM flag stored in the artifact (unchanged).
Evidence grades: 'text' (number stated in text/abstract/table), 'figure' (read off a figure), 'unverified' (never applied).
Two counts are reported: STRICT (text rows only) and WITH_FIGURE (text + figure rows). Forecasts and compilations are never applied.

STOP CONDITION P0 (proposal sec. 4): fewer than 10 decisive-and-open cells, OR survivors entirely at f >= 0.5, OR (secondary trigger)
a published DESI DR1 P1D mixed-fraction analysis already exists -- the last is a documented finding, passed in by the table's
'secondary_trigger' row, never inferred here.

Usage: python3 scripts/wp_e6_v2_p0_overlay.py [--emit]
Generated-by: Claude (Sonnet 5.5), Stream 3 support, 2026-10-08 | Verified-by: checkers/tests/test_wp_e6_v2_p0_overlay.py | Reviewed-by: N
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARTIFACT = REPO / "data" / "derived" / "wp_e6b_lya_adequacy_preflight_2026_07_27.json"
BOUNDS = REPO / "data" / "literature" / "fdm_mixed_fraction_bounds_2026_10_08.csv"
FIGURES = REPO / "data" / "literature" / "fdm_figure_readings_2026_10_08.json"
OUT = REPO / "data" / "derived" / "wp_e6_v2_p0_resurvey_2026_10_08.json"
GRID_TOL = 0.005
EPS = 1e-9
FIG_MARGIN = 0.03        # figure rows are shifted toward LESS closing by the reading error, so they cannot over-close cells
ACCEPT = {"strict": {"text"}, "with_figure": {"text", "figure"}}
P0_MIN_CELLS = 10
P0_F_FLOOR = 0.5


class Refuse(RuntimeError):
    pass


def load_bounds(path=BOUNDS):
    if not path.exists():
        raise Refuse(f"bounds table missing: {path}")
    rows = list(csv.DictReader(path.open()))
    need = {"id", "source", "arxiv", "probe", "kind", "m_lo_ev", "m_hi_ev", "f_max", "cl", "evidence", "locator", "quote"}
    if rows and not need <= set(rows[0]):
        raise Refuse(f"bounds table columns missing: {need - set(rows[0])}")
    for r in rows:
        if r["kind"] not in {"mixed_bound", "pure_bound", "forecast", "compilation", "secondary_trigger", "no_bound_found"}:
            raise Refuse(f"unknown kind {r['kind']!r} in row {r['id']}")
        if r["evidence"] not in {"text", "figure", "unverified", "n/a"}:
            raise Refuse(f"unknown evidence grade {r['evidence']!r} in row {r['id']}")
    return rows


def applies(row, m_ev, f, accepted):
    if row["kind"] != "mixed_bound" or row["evidence"] not in accepted:
        return False
    lo, hi, fmax = float(row["m_lo_ev"]), float(row["m_hi_ev"]), float(row["f_max"])
    in_m = lo * (1 - GRID_TOL) <= m_ev <= hi * (1 + GRID_TOL)
    in_f = f > fmax + EPS if row.get("f_strict", "ge") == "gt" else f >= fmax - EPS
    return in_m and in_f


def figure_rows(path=FIGURES):
    """figure-grade rows COMPUTED from the digitizer's JSON (numbers are never typed). f_max = reading + FIG_MARGIN (conservative)."""
    if not path.exists():
        return []
    d = json.loads(path.read_text())
    rows = []
    for tag, key, field, src, arxiv in (("KOB", "kobayashi_fig1", "F_max_2sigma_allowed", "Kobayashi et al. 2017 Fig. 1 (2 sigma)", "1708.00015"),
                                        ("LIU", "liu_fig6", "f_max_95_allowed", "Liu, Gong & Zhou 2026 Fig. 6 (95% credible)", "2606.06969")):
        for mk, v in d[key].items():
            r = v[field]
            if r is None or r >= 0.99:
                continue
            fm = round(min(1.0, r + FIG_MARGIN), 3)
            rows.append({"id": f"FIG-{tag}-{mk}", "source": src, "arxiv": arxiv, "probe": "Lyman-alpha P1D", "kind": "mixed_bound",
                         "m_lo_ev": mk, "m_hi_ev": mk, "f_max": str(fm), "cl": "figure", "evidence": "figure", "f_strict": "ge",
                         "method_grade": "analysis", "variant": "primary", "locator": f"digitized {key}, reading {r} + margin {FIG_MARGIN}",
                         "quote": "(figure reading; see data/literature/fdm_figure_readings_2026_10_08.json)"})
    return rows


def recompute(artifact, rows, accepted):
    """returns (decisive_total, decisive_and_open, survivors list of (m_key, f), closed_by dict id->cells)"""
    decisive = 0
    survivors = []
    closed_by = {}
    for key, col in artifact["columns"].items():
        m = float(col["m_ev"])
        for c in col["cells"]:
            if not c["reaches_2sigma"]:
                continue
            decisive += 1
            f = float(c["f"])
            if f >= 1.0:
                if not col["pure_fdm_exclusion"]["excluded"]:
                    survivors.append((key, f))
                continue
            hit = [r["id"] for r in rows if applies(r, m, f, accepted)]
            if hit:
                for h in hit:
                    closed_by.setdefault(h, []).append((key, f))
            else:
                survivors.append((key, f))
    return decisive, len(survivors), survivors, closed_by


def evaluate_p0(n_open, survivors, secondary_trigger_rows):
    reasons = []
    if n_open < P0_MIN_CELLS:
        reasons.append(f"fewer than {P0_MIN_CELLS} decisive-and-open cells ({n_open})")
    if survivors and min(f for _, f in survivors) >= P0_F_FLOOR:
        reasons.append(f"survivors lie entirely at f >= {P0_F_FLOOR}")
    if secondary_trigger_rows:
        reasons.append("secondary trigger: " + "; ".join(r["id"] + " (" + r["source"] + ")" for r in secondary_trigger_rows))
    return {"fired": bool(reasons), "reasons": reasons}


def run(artifact_path=ARTIFACT, bounds_path=BOUNDS):
    art = json.loads(artifact_path.read_text())
    rows = load_bounds(bounds_path)
    baseline_rows = [r for r in rows if r["id"].startswith("BASE-")]
    out = {"label": "WP-E6 v2 Phase 0 re-survey overlay -- LITERATURE-TABLE ARITHMETIC ONLY; not a comparison, not TEST/FIT",
           "artifact": str(artifact_path.name), "bounds_table": str(bounds_path.name), "n_bounds_rows": len(rows)}
    d0, o0, s0, _ = recompute(art, baseline_rows, ACCEPT["strict"])
    out["baseline_reproduction"] = {"decisive": d0, "decisive_and_open": o0, "artifact_n_decisive_cells_field": art["n_decisive_cells"],
                                    "reproduces_artifact": o0 == art["n_decisive_cells"]}
    fig_rows = figure_rows()
    primary = [r for r in rows if not r.get("variant", "").startswith("sens")]
    for name, acc in ACCEPT.items():
        d, o, surv, closed = recompute(art, primary + fig_rows, acc)
        per_m = {}
        for k, f in surv:
            per_m.setdefault(k, []).append(f)
        out[name] = {"decisive": d, "decisive_and_open": o, "survivors_by_mass": {k: {"n": len(v), "f_min": min(v), "f_max": max(v)} for k, v in per_m.items()},
                     "closed_by_row": {i: len(c) for i, c in closed.items()},
                     "p0": evaluate_p0(o, surv, [r for r in rows if r["kind"] == "secondary_trigger"])}
    # sensitivity: swap the Bayesian Liu text rows for the weaker frequentist ones (same paper, same data)
    sens = [r for r in rows if r.get("variant") != "primary_bayes" and not r.get("variant", "").startswith("sens") or r.get("variant", "").startswith("sens_freq")]
    ds, os_, ss, _ = recompute(art, sens + fig_rows, ACCEPT["strict"])
    out["frequentist_sensitivity_strict"] = {"decisive_and_open": os_, "note": "Liu et al. frequentist limits (weaker) replace the Bayesian text rows; figure rows (Bayesian contour) are NOT swapped, so with-figure counts are unaffected"}
    sens_nofig = recompute(art, sens, ACCEPT["strict"])
    out["frequentist_sensitivity_strict"]["decisive_and_open_text_rows_only"] = sens_nofig[1]
    out["searched_and_not_found"] = [{"id": r["id"], "source": r["source"], "probe": r["probe"], "quote": r["quote"]} for r in rows if r["kind"] == "no_bound_found"]
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    a = ap.parse_args(argv)
    out = run()
    b = out["baseline_reproduction"]
    print(f"baseline (3 original anchors only): decisive {b['decisive']}, decisive-and-open {b['decisive_and_open']} "
          f"(artifact says {b['artifact_n_decisive_cells_field']}) reproduces: {b['reproduces_artifact']}")
    if not b["reproduces_artifact"]:
        raise Refuse("baseline does not reproduce the artifact's own count: the overlay logic disagrees with the pre-flight")
    for name in ("strict", "with_figure"):
        r = out[name]
        print(f"{name:11}: decisive-and-open {r['decisive_and_open']}  P0 fired: {r['p0']['fired']} {r['p0']['reasons']}")
    if a.emit:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
        print("wrote", OUT)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Refuse as e:
        print("REFUSED:", e)
        sys.exit(2)
