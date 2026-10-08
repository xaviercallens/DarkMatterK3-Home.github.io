"""Tests for scripts/wp_e6_v2_p0_digitize_figures.py: refusal paths and the Liu text-limit control (no source PDFs needed)."""
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts import wp_e6_v2_p0_digitize_figures as dg  # noqa: E402


def test_N1_missing_pdfs_refused(tmp_path):
    with pytest.raises(dg.Refuse):
        dg.main([str(tmp_path)])


def test_N2_wrong_hash_refused(tmp_path):
    for n in dg.PDF_SHA256:
        (tmp_path / n).write_bytes(b"not the pinned pdf")
    with pytest.raises(dg.Refuse):
        dg.main([str(tmp_path)])


def test_N3_text_control_fails_when_reading_disagrees():
    fake = {m: {"f_max_95_allowed": 0.9} for m in dg.GRID_M}
    assert not all(v["within_reading_error"] for v in dg.liu_text_check(fake).values())


def test_P1_text_control_passes_for_stated_values():
    good = {m: {"f_max_95_allowed": 0.12 if abs(math.log10(m) + 22) < 1e-9 else 0.65} for m in dg.GRID_M}
    assert all(v["within_reading_error"] for v in dg.liu_text_check(good).values())


def test_P2_run_from_tolerates_short_gaps_but_not_long_ones():
    col = [True] * 5 + [False] * 4 + [True] * 3 + [False] * 10
    assert dg.run_from(col, 0, 1) == 11
    col2 = [True] * 5 + [False] * 8 + [True] * 3
    assert dg.run_from(col2, 0, 1) == 4
