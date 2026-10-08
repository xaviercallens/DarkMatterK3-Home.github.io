"""Controls for scripts/render_stream3_note_tables.py: fragments on disk match a fresh render; tampered sources change the tables."""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts import render_stream3_note_tables as r  # noqa: E402


def test_P0_fragments_on_disk_are_fresh():
    for name, fn in r.TABLES.items():
        assert (r.OUT / name).read_text() == fn(), name


def _copy(tmp_path):
    c = tmp_path / "certs"; d = tmp_path / "derived"
    c.mkdir(); d.mkdir()
    for f in ("E1_aubry_andre_selfduality.json", "E1b_aubry_andre_localization_scaling.json"):
        shutil.copy(r.CERTS / f, c / f)
    shutil.copy(r.DERIVED / "wp_e6_v2_p0_resurvey_2026_10_08.json", d / "wp_e6_v2_p0_resurvey_2026_10_08.json")
    return c, d


def test_N1_tampered_sources_change_every_table(tmp_path, monkeypatch):
    base = {n: fn() for n, fn in r.TABLES.items()}
    c, d = _copy(tmp_path)
    monkeypatch.setattr(r, "CERTS", c)
    monkeypatch.setattr(r, "DERIVED", d)
    e1 = json.loads((c / "E1_aubry_andre_selfduality.json").read_text())
    e1["result"]["cases"][0]["pass"] = False
    (c / "E1_aubry_andre_selfduality.json").write_text(json.dumps(e1))
    e1b = json.loads((c / "E1b_aubry_andre_localization_scaling.json").read_text())
    e1b["result"]["scaling"][0]["near_critical_reported_not_claimed"] = True
    (c / "E1b_aubry_andre_localization_scaling.json").write_text(json.dumps(e1b))
    p0 = json.loads((d / "wp_e6_v2_p0_resurvey_2026_10_08.json").read_text())
    p0["strict"]["decisive_and_open"] = 9
    p0["strict"]["p0"]["fired"] = True
    (d / "wp_e6_v2_p0_resurvey_2026_10_08.json").write_text(json.dumps(p0))
    assert "FAIL" in r.render_e1() and r.render_e1() != base["s3_e1.tex"]
    assert r.render_e1b().count("not claimed") == base["s3_e1b.tex"].count("not claimed") + 1
    t = r.render_p0()
    assert "$9$ & yes" in t and t != base["s3_p0.tex"]


def test_N2_check_mode_catches_a_stale_fragment(tmp_path, monkeypatch):
    out = tmp_path / "tables"; out.mkdir()
    for n in r.TABLES:
        (out / n).write_text("stale\n")
    monkeypatch.setattr(r, "OUT", out)
    assert r.main(["--check"]) == 1
