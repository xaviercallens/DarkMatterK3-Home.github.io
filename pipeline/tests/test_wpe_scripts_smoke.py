#!/usr/bin/env python3
"""Smoke tests for the WP-E5 phase scripts.

WHY THIS FILE EXISTS
Two scripts (`wpe_closure_tests.py`, `wpe_transverse_sweep.py`) were committed with
`Verified-by:` footers claiming properties of code that had never been executed. Both
died on the identical defect the first time anyone ran them:

    density_shuffle_realization(field, rng=rng)   # signature is (field, seed)
    TypeError: got an unexpected keyword argument 'rng'

Nothing subtle was required to catch it — no statistical review, no domain knowledge.
Merely calling the function once would have done it. These tests do that, cheaply, so
a signature mismatch in a phase script fails in the suite rather than at the moment
someone tries to produce a deliverable.

They deliberately do NOT check scientific correctness; that is what the phase
artifacts, the negative controls and the audit are for. They check only that the code
paths execute and honour their contracts.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "scripts"
WPE_SCRIPTS = ["wpe_preflight_baseline.py", "wpe_closure_tests.py",
               "wpe_transverse_sweep.py"]


def _load(script_name):
    """Import a script by path without executing its __main__ block."""
    path = SCRIPTS / script_name
    if not path.exists():
        pytest.skip(f"{script_name} not present")
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    spec = importlib.util.spec_from_file_location(f"_wpe_smoke_{path.stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize("script_name", WPE_SCRIPTS)
def test_script_imports(script_name):
    """Every phase script must at least import. Catches syntax and import errors."""
    mod = _load(script_name)
    assert hasattr(mod, "main"), f"{script_name} has no main()"


@pytest.mark.parametrize("script_name,builder", [
    ("wpe_closure_tests.py", "compute_null_band"),
    ("wpe_transverse_sweep.py", "build_null_bank"),
])
def test_null_bank_builders_actually_run(script_name, builder):
    """Call each script's null-bank builder for real.

    This is the exact test that was missing. Both scripts passed their old
    'Verified-by: null-bank discipline' footers while this call raised TypeError.
    """
    mod = _load(script_name)
    fn = getattr(mod, builder, None)
    assert fn is not None, f"{script_name} has no {builder}()"

    rng = np.random.default_rng(0)
    field = rng.random((8, 8)) + 0.5

    if builder == "compute_null_band":
        vals = fn(field, 3, 50.0)
    else:
        vals = fn(field, float(np.median(field)), 3, 5001)

    vals = np.asarray(vals)
    assert vals.shape == (3,), vals.shape
    assert np.all(np.isfinite(vals))
    assert np.all(vals >= 0), "Betti numbers cannot be negative"


def test_sweep_converts_mpc_to_per_axis_voxels():
    """r_s must reach the deformation. The quarantined version hardcoded R_voxels=2.0."""
    mod = _load("wpe_transverse_sweep.py")
    sig = mod.mpc_to_voxels_per_axis(4.0, (48.32, 52.40), 32)
    assert len(sig) == 2
    # Non-square voxels => the two axis sigmas must differ, or the warp is
    # anisotropic in Mpc (WP-E5 self-review defect 1).
    assert sig[0] != sig[1]
    assert sig[0] == pytest.approx(4.0 / (48.32 / 32))
    assert sig[1] == pytest.approx(4.0 / (52.40 / 32))
    # And it must scale with r_s at all.
    assert mod.mpc_to_voxels_per_axis(8.0, (48.32, 52.40), 32)[0] == pytest.approx(
        2 * sig[0])


def test_sweep_threshold_modes_differ_on_a_deformed_field():
    """percentile keeps the threshold VALUE; matched_fill keeps the mask SIZE."""
    mod = _load("wpe_transverse_sweep.py")
    rng = np.random.default_rng(1)
    baseline = rng.random((32, 32))
    thr = float(np.percentile(baseline, 50.0))
    fill = float((baseline > thr).mean())
    deformed = baseline * 2.0          # a monotone rescale: shifts values, not order

    t_pct, f_pct = mod.threshold_for_deformed(deformed, "percentile", thr, fill)
    t_mat, f_mat = mod.threshold_for_deformed(deformed, "matched_fill", thr, fill)

    assert t_pct == thr, "percentile mode must reuse the baseline threshold value"
    assert f_pct > fill, "rescaling should push more cells over a fixed threshold"
    assert f_mat == pytest.approx(fill, abs=0.02), (
        "matched_fill must hold the mask size at the baseline fill")


def test_sweep_classifies_on_baseline_subtracted_delta_sigma():
    mod = _load("wpe_transverse_sweep.py")
    assert mod.classify(0.0)[0] == "ZONE_0_UNTESTABLE"
    assert mod.classify(4.0)[0] == "ZONE_1_DETECTABLE"
    assert mod.classify(-6.0)[0] == "ZONE_2_GENERIC_DEFORMATION_EXCLUDED"
    assert mod.classify(None)[0] == "ZONE_0_UNTESTABLE"
    # Zone 2 must not be worded as falsifying a mechanism (WP-E5 deviation 3).
    assert "GENERIC" in mod.classify(-6.0)[0]


def test_no_script_calls_density_shuffle_with_an_rng_kwarg():
    """Pin the exact defect class that took down two scripts.

    Uses the AST rather than a substring search: these files legitimately mention
    `rng=rng` in prose explaining the fix, and a text match flags that as a defect.
    Only real call sites count.
    """
    import ast

    offenders = []
    for name in WPE_SCRIPTS:
        path = SCRIPTS / name
        if not path.exists():
            continue
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            fn = node.func
            fname = getattr(fn, "id", None) or getattr(fn, "attr", None)
            if fname != "density_shuffle_realization":
                continue
            for kw in node.keywords:
                if kw.arg == "rng":
                    offenders.append(f"{name}:{node.lineno}")

    assert not offenders, (
        f"density_shuffle_realization called with rng= at {offenders}; "
        f"its signature is (field, seed)")
