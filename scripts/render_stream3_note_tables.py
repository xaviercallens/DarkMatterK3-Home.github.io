#!/usr/bin/env python3
"""render_stream3_note_tables.py -- LaTeX table fragments for papers/stream3_status_note_2026_10_08.tex, read from certificates.

Numbers are computed, never typed: every value in every table is read at run time from
  checkers/certificates/E1_aubry_andre_selfduality.json
  checkers/certificates/E1b_aubry_andre_localization_scaling.json
  data/derived/wp_e6_v2_p0_resurvey_2026_10_08.json
Usage: python3 scripts/render_stream3_note_tables.py [--check]   (--check exits 1 if a fragment is stale)
Controls: checkers/tests/test_render_stream3_note_tables.py (tampered inputs must change the tables).
Generated-by: Claude (Opus 5.5), Stream 3 support, 2026-10-08 | Verified-by: the controls above | Reviewed-by: N
"""
import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CERTS = REPO / "checkers" / "certificates"
DERIVED = REPO / "data" / "derived"
OUT = REPO / "papers" / "tables"


def sci(x):
    m, e = f"{x:.1e}".split("e")
    return f"${m}\\times10^{{{int(e)}}}$"


def render_e1():
    d = json.loads((CERTS / "E1_aubry_andre_selfduality.json").read_text())["result"]
    ctl = {c["N"]: c for c in d["negative_controls"]}
    lines = [r"\begin{tabular}{rrlllll}", r"\toprule",
             r"$N$ & $p$ & max duality gap & max intertwiner gap & control gap (random) & controls fail? & verdict \\", r"\midrule"]
    for c in d["cases"]:
        n = c["N"]
        k = ctl[n]
        lines.append(f"${n}$ & ${c['p']}$ & {sci(max(c['A_spectral_duality_gap'].values()))} & {sci(max(c['C_intertwiner_gap'].values()))} & "
                     f"{sci(min(k['N1_random_potential_spectral_gap'].values()))} & {'yes' if k['all_controls_fail_as_required'] else 'NO'} & "
                     f"{'PASS' if c['pass'] else 'FAIL'} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def render_e1b():
    d = json.loads((CERTS / "E1b_aubry_andre_localization_scaling.json").read_text())["result"]
    ns = ",".join(str(c[0]) for c in d["cases"])
    lines = [r"\begin{tabular}{rlllp{4.2cm}}", r"\toprule",
             f"$\\lambda/J$ & regime & statistic over $N\\in\\{{{ns}\\}}$ & criterion met & status \\\\", r"\midrule"]
    for s in d["scaling"]:
        if s["regime"] == "extended":
            stat = f"$\\max/\\min$ of $N\\cdot\\mathrm{{IPR}}$ $={s['ratio_largest_over_smallest']:.3f}$"
        else:
            v = s["IPR_x"]
            stat = f"$\\mathrm{{IPR}}\\in[{min(v):.3f},{max(v):.3f}]$"
        status = "near-critical: reported, not claimed" if s["near_critical_reported_not_claimed"] else "claimed"
        lines.append(f"${s['lam']}$ & {s['regime']} & {stat} & {'yes' if s['pass'] else 'no'} & {status} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def render_p0():
    d = json.loads((DERIVED / "wp_e6_v2_p0_resurvey_2026_10_08.json").read_text())
    b = d["baseline_reproduction"]
    rows = [("decisive cells (optimistic proxy)", b["decisive"], "---"),
            ("decisive and open, before Phase 0", b["decisive_and_open"], "---"),
            ("decisive and open, text-grade bounds", d["strict"]["decisive_and_open"], "yes" if d["strict"]["p0"]["fired"] else "no"),
            ("decisive and open, text and figure reads", d["with_figure"]["decisive_and_open"], "yes" if d["with_figure"]["p0"]["fired"] else "no"),
            ("text-grade, frequentist limits instead of Bayesian", d["frequentist_sensitivity_strict"]["decisive_and_open"], "---")]
    lines = [r"\begin{tabular}{lrl}", r"\toprule", r"Count & cells & P0 fires? \\", r"\midrule"]
    lines += [f"{a} & ${n}$ & {p} \\\\" for a, n, p in rows]
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


TABLES = {"s3_e1.tex": render_e1, "s3_e1b.tex": render_e1b, "s3_p0.tex": render_p0}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    OUT.mkdir(parents=True, exist_ok=True)
    stale = []
    for name, fn in TABLES.items():
        content = fn()
        p = OUT / name
        if a.check:
            if not p.exists() or p.read_text() != content:
                stale.append(name)
        else:
            p.write_text(content)
    if a.check:
        print("STALE: " + ", ".join(stale) if stale else "OK: all Stream 3 note tables match their sources")
        return 1 if stale else 0
    print("wrote", ", ".join(TABLES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
