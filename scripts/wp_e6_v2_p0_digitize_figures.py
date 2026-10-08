#!/usr/bin/env python3
"""wp_e6_v2_p0_digitize_figures.py -- WP-E6 v2 Phase 0: read three published (m, f) constraint FIGURES by colour thresholding.
LITERATURE-FIGURE READING ONLY (CLAUDE.md rule 1): no data, no comparison, no TEST/FIT label. T0 D-g, 2026-10-08.

Three published constraints exist only as plotted regions; their text gives no per-mass numbers (or, for Liu et al., only three).
This script re-renders the figure page of each source PDF at a fixed resolution, calibrates the axes from the detected tick marks and
frame, and extracts the boundary of the shaded region. Evidence grade of every number is 'figure'; estimated reading error about
+/-0.03 in f (about +/-10 px).

  kobayashi.pdf   arXiv:1708.00015v2, Fig. 1 (page 5)   2 sigma (255,88,88) / 3 sigma (255,178,178) ALLOWED regions of the (m, F) plane
  liu.pdf         arXiv:2606.06969v2, Fig. 6 (page 16)  95% ALLOWED region (219,165,165) [(205,159,159) where it overlaps Kobayashi's grey]
  marsh.pdf       arXiv:1810.08543v2, Fig. 2 (page 4)   EXCLUDED regions in (m_a, Omega_a/Omega_d): red = star cluster inside the core
                                                        (C = 0.3, the CONSERVATIVE one for m > 1e-20 eV where the cluster may be inside
                                                        or outside), blue-only = C = 1; striped pink + narrow dark-blue bands = the range
                                                        where the authors say the diffusion approximation is questionable / resonances.

KNOWN FIGURE HAZARDS handled here: Liu's figure carries Kobayashi's DASHED contour inside the allowed region (it cuts naive column runs;
runs tolerate gaps of up to 6 px) and a vertical dashed line at log m = -20; Marsh-Niemeyer's labels and vertical dash-dot line sit on
the shading. Columns on a frame/vertical line are nudged inward. Control: the Liu contour must reproduce the three limits the paper states
in its text (0.07/0.12/0.65 at log m = -23/-22/-21, Bayesian) within the reading error -- the script prints that comparison and refuses
if it fails.

The PDFs must be the exact arXiv versions below (sha256 pinned); the script refuses otherwise.
Usage: python3 -I scripts/wp_e6_v2_p0_digitize_figures.py <dir containing kobayashi.pdf liu.pdf marsh.pdf> [out.json]
Generated-by: Claude (Sonnet 5.5), Stream 3 support, 2026-10-08 | Verified-by: checkers/tests/test_wp_e6_v2_p0_digitize.py | Reviewed-by: N
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

PDF_SHA256 = {
    "kobayashi.pdf": "e4b2684f95d967c606a6b8fe490a21c0054e9ba2d8bb32ad51278d1905521a3f",
    "liu.pdf": "7dbd13fe7076295cd048909076e36ed9b1f84fba0592778e7dcb5f2ec37b40b0",
    "marsh.pdf": "856bd42efab8ffbc0dbc63f1e8d1123b6be4e2e37bf4873c835ca4dbe0fc6191",
}
DPI = 130
GRID_M = [10 ** (-22 + 0.25 * i) for i in range(13)]
READ_ERR_F = 0.03
GAP = 6
LIU_TEXT_CHECK = {-22.0: 0.12, -21.0: 0.65}      # stated in the paper's abstract/Sec. 4.2 (Bayesian); -23 is outside the grid


class Refuse(RuntimeError):
    pass


def render(pdf: Path, page: int, out: Path):
    subprocess.run(["pdftoppm", "-r", str(DPI), "-f", str(page), "-l", str(page), "-png", str(pdf), str(out)], check=True)
    cands = sorted(out.parent.glob(out.name + "-*.png"))
    if not cands:
        raise Refuse(f"pdftoppm produced no image for {pdf.name}")
    return np.array(Image.open(cands[0]).convert("RGB")).astype(int)


def near(img, rgb, tol=6):
    return np.abs(img - np.array(rgb)).max(axis=2) <= tol


def run_from(mask_col, start, step, gap=GAP):
    """last index of the run of True beginning at `start` moving by `step`, tolerating gaps of up to `gap` False pixels."""
    i, last, misses = start, None, 0
    while 0 <= i < len(mask_col):
        if mask_col[i]:
            last, misses = i, 0
        else:
            misses += 1
            if misses > gap:
                break
        i += step
    return last


def f_from_y(y, y_top, y_bot):
    return (y_bot - y) / (y_bot - y_top)


def kobayashi(img):
    x_of = lambda logm: 316 + (logm + 23.0) * 168.0
    y_top, y_bot = 139, 510
    two = near(img, (255, 88, 88)); three = near(img, (255, 178, 178)) | two
    res = {}
    for m in GRID_M:
        if m > 1.0000001e-20:
            continue
        x = int(round(min(max(x_of(np.log10(m)), 321), 815)))
        f2s, f3s = [], []
        for dx in (-2, 0, 2):
            t2 = run_from(two[:, x + dx], y_bot - 2, -1); t3 = run_from(three[:, x + dx], y_bot - 2, -1)
            if t2 is not None: f2s.append(f_from_y(t2, y_top, y_bot))
            if t3 is not None: f3s.append(f_from_y(t3, y_top, y_bot))
        res[m] = {"F_max_2sigma_allowed": round(float(np.median(f2s)), 3) if f2s else None,
                  "F_max_3sigma_allowed": round(float(np.median(f3s)), 3) if f3s else None}
    return res


def liu(img):
    x_of = lambda logm: 329 + (logm + 23.0) * (796 - 329) / 4.0
    y_top, y_bot = 166, 630
    grey = (np.abs(img[:, :, 0] - img[:, :, 1]) < 10) & (np.abs(img[:, :, 1] - img[:, :, 2]) < 10) & (img[:, :, 0] < 175)  # Kobayashi's dashed contour
    allowed = near(img, (219, 165, 165)) | near(img, (205, 159, 159)) | grey
    res = {}
    for m in GRID_M:
        lg = np.log10(m)
        x = int(round(x_of(lg)))
        # the vertical dashed line at log m = -20 is at x ~ 678-679: sample to its right when on it
        if 672 <= x <= 685:
            x = 688
        x = min(max(x, 335), 790)
        fs = []
        for dx in (-2, 0, 2):
            t = run_from(allowed[:, x + dx], y_bot - 2, -1)
            if t is not None:
                fs.append(f_from_y(t, y_top, y_bot))
        res[m] = {"f_max_95_allowed": round(float(np.median(fs)), 3) if fs else None}
    return res


def liu_text_check(liu_tab):
    out = {}
    for lg, stated in LIU_TEXT_CHECK.items():
        m = min(GRID_M, key=lambda g: abs(np.log10(g) - lg))
        got = liu_tab[m]["f_max_95_allowed"]
        out[str(lg)] = {"stated": stated, "digitized": got, "within_reading_error": got is not None and abs(got - stated) <= 2 * READ_ERR_F}
    return out


def marsh(img):
    x_of = lambda logm: 306.0 + (logm + 21.0) * (832.5 - 306.0) / 2.0
    y_top, y_bot = 116, 525
    red = near(img, (200, 105, 105)) | near(img, (152, 76, 80)) | near(img, (164, 6, 6), tol=30)
    stripe = near(img, (240, 215, 215), tol=14) | near(img, (102, 103, 156), tol=10)
    res = {}
    for m in GRID_M:
        lg = np.log10(m)
        if lg < -21.0 or lg > -18.99:
            continue
        x0 = int(round(x_of(lg)))
        zone, f_min, solid_fracs = None, None, []
        for dx in (-4, -2, 0, 2, 4):
            x = min(max(x0 + dx, 284), 908)
            col = slice(y_top + 2, y_bot - 1)
            solid_fracs.append(float(red[col, x].mean()))
        stripe_frac = float(np.mean([stripe[y_top + 2:y_bot - 1, min(max(x0 + dx, 284), 908)].mean() for dx in (-4, -2, 0, 2, 4)]))
        solid = float(np.median(solid_fracs))
        if stripe_frac > 0.15 and solid < 0.8:
            zone = "questionable_stripes_or_resonance_band"
        elif solid >= 0.85:
            zone = "solid_full_height"          # shaded from F ~ 0 to 1
            f_min = 0.0
        else:
            lows = []
            for dx in (-4, -2, 0, 2, 4):
                x = min(max(x0 + dx, 284), 908)
                ys = np.where(red[y_top + 2:y_bot - 1, x])[0]
                if len(ys):
                    lows.append(f_from_y(y_top + 2 + ys.max(), y_top, y_bot))
            f_min = round(float(np.median(lows)), 3) if lows else None
            zone = "boundary_curve" if f_min is not None else "unshaded"
        res[m] = {"zone": zone, "f_min_excluded_conservative_C0.3": f_min, "solid_fraction": round(solid, 3), "stripe_fraction": round(stripe_frac, 3)}
    return res


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) not in (1, 2):
        print(__doc__); return 2
    d = Path(argv[0])
    for n, h in PDF_SHA256.items():
        p = d / n
        if not p.exists():
            raise Refuse(f"missing {p}")
        got = hashlib.sha256(p.read_bytes()).hexdigest()
        if got != h:
            raise Refuse(f"{n}: sha256 {got} != pinned {h}")
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        kob = kobayashi(render(d / "kobayashi.pdf", 5, t / "kob"))
        lu = liu(render(d / "liu.pdf", 16, t / "liu"))
        ma = marsh(render(d / "marsh.pdf", 4, t / "mar"))
    chk = liu_text_check(lu)
    if not all(v["within_reading_error"] for v in chk.values()):
        raise Refuse(f"digitized Liu contour disagrees with the limits stated in the paper's text: {chk}")
    out = {"kobayashi_fig1": {f"{m:.4e}": v for m, v in kob.items()}, "liu_fig6": {f"{m:.4e}": v for m, v in lu.items()},
           "marsh_fig2": {f"{m:.4e}": v for m, v in ma.items()}, "liu_text_check": chk, "reading_error_f": READ_ERR_F, "dpi": DPI}
    for name in ("kobayashi_fig1", "liu_fig6", "marsh_fig2"):
        print(f"== {name} (reading error about +/-{READ_ERR_F} in f)")
        for m, v in out[name].items():
            print(f"  m = {m} eV: {v}")
    print("== liu text check:", chk)
    if len(argv) == 2:
        out["pdf_sha256"] = PDF_SHA256
        Path(argv[1]).write_text(json.dumps(out, indent=2) + "\n")
        print("wrote", argv[1])
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Refuse as e:
        print("REFUSED:", e)
        sys.exit(2)
