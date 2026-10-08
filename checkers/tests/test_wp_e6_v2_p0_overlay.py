"""Merge-blocking tests for scripts/wp_e6_v2_p0_overlay.py (WP-E6 v2 Phase 0). Literature-table arithmetic only."""
import csv
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts import wp_e6_v2_p0_overlay as ov  # noqa: E402

FIELDS = ["id", "source", "arxiv", "probe", "kind", "m_lo_ev", "m_hi_ev", "f_max", "cl", "evidence", "locator", "quote"]


def table(tmp_path, rows):
    p = tmp_path / "b.csv"
    with p.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS} | {"id": r["id"]})
    return p


def row(id_, **kw):
    base = dict(source="s", arxiv="x", probe="p", kind="mixed_bound", m_lo_ev="1e-20", m_hi_ev="1e-20", f_max="0.5", cl="95%", evidence="text", locator="l", quote="q")
    return base | dict(id=id_) | kw


@pytest.fixture(scope="module")
def art():
    return json.loads(ov.ARTIFACT.read_text())


BASE = [row("BASE-1", m_lo_ev="1e-22", m_hi_ev="1e-22", f_max="0.12"), row("BASE-2", m_lo_ev="1e-21", m_hi_ev="1e-21", f_max="0.65")]


def test_P1_baseline_reproduces_the_artifacts_own_count(art):
    d, o, surv, _ = ov.recompute(art, BASE, ov.ACCEPT["strict"])
    assert (d, o) == (258, 221) == (258, art["n_decisive_cells"])


def test_P2_a_new_text_bound_closes_exactly_the_cells_it_covers(art):
    new = BASE + [row("N1", m_lo_ev="1e-20", m_hi_ev="1e-20", f_max="0.5")]          # closes f >= 0.5 at m = 1e-20 only
    _, o, _, closed = ov.recompute(art, new, ov.ACCEPT["strict"])
    n = sum(1 for c in art["columns"]["1.0000e-20"]["cells"] if c["reaches_2sigma"] and 0.5 <= c["f"] < 1.0)
    assert n > 0 and o == 221 - n and len(closed["N1"]) == n


def test_N1_unverified_forecast_compilation_and_figure_rows_are_not_applied_strictly(art):
    for kw in ({"evidence": "unverified"}, {"kind": "forecast"}, {"kind": "compilation"}, {"evidence": "figure"}):
        _, o, _, closed = ov.recompute(art, BASE + [row("N", **kw)], ov.ACCEPT["strict"])
        assert o == 221 and "N" not in closed


def test_P3_figure_rows_apply_only_in_the_with_figure_count(art):
    t = BASE + [row("F", evidence="figure")]
    assert ov.recompute(art, t, ov.ACCEPT["strict"])[1] == 221
    assert ov.recompute(art, t, ov.ACCEPT["with_figure"])[1] < 221


def test_N2_mass_outside_the_stated_range_is_not_closed(art):
    _, o, _, _ = ov.recompute(art, BASE + [row("R", m_lo_ev="3e-20", m_hi_ev="1e-19", f_max="0.05")], ov.ACCEPT["strict"])
    cells_covered = sum(1 for k, col in art["columns"].items() if 3e-20 * 0.995 <= col["m_ev"] <= 1e-19 * 1.005
                        for c in col["cells"] if c["reaches_2sigma"] and c["f"] < 1.0)
    assert o == 221 - cells_covered and cells_covered > 0


def test_P4_p0_fires_on_few_cells_on_high_f_only_and_on_secondary_trigger():
    assert ov.evaluate_p0(9, [("m", 0.1)] * 9, [])["fired"]
    assert ov.evaluate_p0(50, [("m", 0.5), ("m", 0.9)] * 25, [])["fired"]
    assert ov.evaluate_p0(50, [("m", 0.1)] * 50, [{"id": "T", "source": "s"}])["fired"]
    assert not ov.evaluate_p0(50, [("m", 0.1)] * 50, [])["fired"]


def test_N3_malformed_table_refused(tmp_path):
    p = tmp_path / "bad.csv"
    p.write_text("id,source\nx,y\n")
    with pytest.raises(ov.Refuse):
        ov.load_bounds(p)
    p2 = table(tmp_path, [row("K", kind="bogus")])
    with pytest.raises(ov.Refuse):
        ov.load_bounds(p2)


def test_N4_missing_bounds_table_refused(tmp_path):
    with pytest.raises(ov.Refuse):
        ov.load_bounds(tmp_path / "absent.csv")


def test_P5_real_table_baseline_reproduces_now():
    out = ov.run()
    assert out["baseline_reproduction"]["reproduces_artifact"] and out["baseline_reproduction"]["decisive_and_open"] == 221


# ---- additions 2026-10-08: strict fraction, computed figure rows, frequentist sensitivity, real-table invariants ----
def test_P6_strict_inequality_f_gt_0p3_does_not_close_f_equal_0p3(art):
    t = BASE + [row("K", m_lo_ev="1e-22", m_hi_ev="1e-22", f_max="0.3", f_strict="gt")]
    _, _, _, closed = ov.recompute(art, t, ov.ACCEPT["strict"])
    assert closed["K"] and all(f > 0.3 for _, f in closed["K"])
    t2 = BASE + [row("K", m_lo_ev="1e-22", m_hi_ev="1e-22", f_max="0.3", f_strict="ge")]
    _, _, _, closed2 = ov.recompute(art, t2, ov.ACCEPT["strict"])
    assert len(closed2["K"]) == len(closed["K"]) + 1          # exactly the f = 0.3 cell differs


def test_P7_figure_rows_are_computed_and_shifted_toward_less_closing(tmp_path):
    fj = tmp_path / "f.json"
    fj.write_text(json.dumps({"kobayashi_fig1": {"1.0000e-21": {"F_max_2sigma_allowed": 0.345}, "1.0000e-20": {"F_max_2sigma_allowed": 0.997}},
                              "liu_fig6": {"1.0000e-21": {"f_max_95_allowed": None}}}))
    rows = ov.figure_rows(fj)
    assert [r["id"] for r in rows] == ["FIG-KOB-1.0000e-21"]
    assert float(rows[0]["f_max"]) == pytest.approx(0.345 + ov.FIG_MARGIN) and rows[0]["evidence"] == "figure"


def test_N5_figure_rows_never_apply_in_the_strict_count(art, tmp_path):
    fj = tmp_path / "f.json"
    fj.write_text(json.dumps({"kobayashi_fig1": {"1.0000e-21": {"F_max_2sigma_allowed": 0.2}}, "liu_fig6": {}}))
    rows = ov.figure_rows(fj)
    assert ov.recompute(art, BASE + rows, ov.ACCEPT["strict"])[1] == 221
    assert ov.recompute(art, BASE + rows, ov.ACCEPT["with_figure"])[1] < 221


def test_P8_real_table_invariants():
    out = ov.run()
    s, w = out["strict"]["decisive_and_open"], out["with_figure"]["decisive_and_open"]
    assert w <= s <= 221
    assert out["frequentist_sensitivity_strict"]["decisive_and_open"] >= s
    assert not out["strict"]["p0"]["fired"] and not out["with_figure"]["p0"]["fired"]
    assert not [r for r in ov.load_bounds() if r["kind"] == "secondary_trigger"]


def test_N6_unaudited_and_marsh_rows_are_never_applied():
    out = ov.run()
    applied = set(out["strict"]["closed_by_row"]) | set(out["with_figure"]["closed_by_row"])
    assert "MARSH-ERI2-FIGONLY" not in applied and "SURVEY-UNAUDITED" not in applied
