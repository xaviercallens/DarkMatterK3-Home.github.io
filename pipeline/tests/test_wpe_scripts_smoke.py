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
               "wpe_transverse_sweep.py",
               "c3_normalization_applicability_2026_09_21.py",
               "c3_sym2_gauge_existence_2026_09_21.py",
               "verify_checker_against_source_2026_09_21.py"]


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


# ---------------------------------------------------------------------------
# C3 normalization applicability (2026-09-21). Same reason this module exists:
# the script ships a `Verified-by:` footer citing two negative controls, and
# those controls only execute when someone invokes it by hand. Here they run.
# ---------------------------------------------------------------------------
C3_APPLICABILITY = "c3_normalization_applicability_2026_09_21.py"


def test_c3_applicability_negative_controls_run_for_real():
    """Drive main(): it returns 0 only if NC-1 and NC-2 both pass inside the script."""
    mod = _load(C3_APPLICABILITY)
    assert mod.main() == 0, "NC-1/NC-2 failed inside the applicability script"


def test_c3_applicability_discriminates_d0_from_dnonzero():
    """Module code — not this test — must separate the two classes.

    Negative control for the script's own conclusion: if `applicability` called
    everything INAPPLICABLE, the s7/s10 finding would be worthless. The six d=0
    sporadic families must come out APPLICABLE against the same function.
    """
    mod = _load(C3_APPLICABILITY)
    order3 = mod.ORDER3_AZ_COOPER

    for name in mod.BIJECTION.values():
        assert mod.applicability(name, order3[name])["verdict"] == "APPLICABLE", name

    for name in ("s7", "s10"):
        res = mod.applicability(name, order3[name])
        assert res["verdict"] == "INAPPLICABLE_NORMALIZATION", name
        assert res["reasons"], f"{name} inapplicable with no reason recorded"


def test_c3_applicability_never_emits_a_c3_certificate():
    """The artifact must not land in checkers/certificates/, whose contents are the
    only admissible evidence for a C3 claim (K3_CRITERIA.md 3.5), and must not carry
    a bare FAIL that would read as a geometric falsification."""
    mod = _load(C3_APPLICABILITY)
    assert "certificates" not in mod.OUT.parts
    assert mod.OUT.parts[-2:][0] == "derived"
    for name in ("s7", "s10"):
        assert mod.applicability(name, mod.ORDER3_AZ_COOPER[name])["verdict"] != "FAIL"


# ---------------------------------------------------------------------------
# C3 Sym^2 gauge existence (2026-09-21). Same rule: the script's `Verified-by:`
# footer cites five controls, so the controls must run somewhere other than a
# hand invocation.
# ---------------------------------------------------------------------------
C3_GAUGE = "c3_sym2_gauge_existence_2026_09_21.py"


def test_c3_gauge_existence_all_controls_run_for_real():
    """main() returns 0 only if D1, D3, the family identity and NC-0..NC-3 all hold."""
    pytest.importorskip("sympy")
    mod = _load(C3_GAUGE)
    assert mod.main() == 0, "a derivation or negative control failed inside the script"


def test_c3_gauge_criterion_can_say_no():
    """The criterion must be falsifiable: an operator that is provably NOT a symmetric
    square must be detected. d^3 + z d + 1 has P = z, Q = 1, so 2Q - P' = 1 != 0.

    Without this the family-wide identity would be indistinguishable from a criterion
    that returns SYM2_EXISTS for every input.
    """
    sp = pytest.importorskip("sympy")
    mod = _load(C3_GAUGE)
    one = sp.Integer(1)
    _, P, Q = mod.normal_form(one, sp.Integer(0), mod.z, one)
    defect = sp.cancel(2 * Q - sp.diff(P, mod.z))
    assert not mod.rational_is_zero(defect), "criterion failed to reject d^3 + z d + 1"


def test_c3_gauge_family_identity_is_a_property_of_the_shape():
    """Breaking the AZ/Cooper shape must break the identity — otherwise the family-wide
    result is an artifact of the normal-form code rather than of the recurrence shape."""
    sp = pytest.importorskip("sympy")
    mod = _load(C3_GAUGE)
    y = sp.Function("y")(mod.z)
    a, b, c, d = sp.symbols("a b c d")

    intact = mod.classify(mod.l3_applied(a, b, c, d, y), y, "intact")
    assert intact["verdict"] == "SYM2_EXISTS_UP_TO_GAUGE"

    for fn in (mod.l3_shape_broken_cube, mod.l3_shape_broken_factor):
        broken = mod.classify(fn(a, b, c, d, y), y, fn.__name__)
        assert broken["verdict"] == "NO_SYM2_IN_ANY_GAUGE", fn.__name__


def test_c3_gauge_verdicts_are_never_pass_or_fail():
    """A C3 PASS/FAIL must not be emitted: this tests gauge equivalence, not C3's
    fixed-normalization equality, and the artifact must stay out of certificates/."""
    sp = pytest.importorskip("sympy")
    mod = _load(C3_GAUGE)
    y = sp.Function("y")(mod.z)
    assert "certificates" not in mod.OUT.parts
    for name in ("s7", "s10"):
        v = mod.classify(mod.l3_applied(*mod.ORDER3_AZ_COOPER[name], y), y, name)["verdict"]
        assert v in ("SYM2_EXISTS_UP_TO_GAUGE", "NO_SYM2_IN_ANY_GAUGE")


# ---------------------------------------------------------------------------
# Source verification of the C3 checker against the vendored PDF (2026-09-21).
# ---------------------------------------------------------------------------
SRC_VERIFY = "verify_checker_against_source_2026_09_21.py"


def _need_pdftotext():
    import shutil
    if shutil.which("pdftotext") is None:
        pytest.skip("pdftotext not installed")


def test_source_verification_runs_and_controls_fire():
    """main() returns 0 only if V1-V6 and NC-A/B/C all hold against the vendored PDF."""
    _need_pdftotext()
    mod = _load(SRC_VERIFY)
    if not mod.PDF.exists():
        pytest.skip("vendored Gorodetsky PDF not present")
    assert mod.main() == 0


def test_source_verification_hash_gate_actually_compares():
    """V1 must reject a wrong hash — otherwise the whole parse is ungated."""
    _need_pdftotext()
    mod = _load(SRC_VERIFY)
    if not mod.PDF.exists():
        pytest.skip("vendored Gorodetsky PDF not present")
    assert mod.check_hash(mod.actual_sha()) is True
    assert mod.check_hash("0" * 64) is False


def test_source_verification_table_comparison_can_fail():
    """V2's comparator must reject a perturbed expectation, so a PASS means agreement
    with the paper rather than a function that returns True."""
    _need_pdftotext()
    mod = _load(SRC_VERIFY)
    if not mod.PDF.exists():
        pytest.skip("vendored Gorodetsky PDF not present")
    parsed = mod.parse_cooper_table(mod.pdf_text())
    assert mod.compare_table(parsed, mod.ORDER3_AZ_COOPER) is True
    bad = dict(mod.ORDER3_AZ_COOPER)
    bad["s10"] = (6, 2, -64, 5)          # d: 4 -> 5
    assert mod.compare_table(parsed, bad) is False


def test_source_says_cooper_has_exactly_three_sporadic_solutions():
    """The register lists K-S22; the source names only s7, s10, s18. Guards the finding
    that K-S22 has no citable recurrence behind it."""
    _need_pdftotext()
    mod = _load(SRC_VERIFY)
    if not mod.PDF.exists():
        pytest.skip("vendored Gorodetsky PDF not present")
    import re
    text = mod.pdf_text()
    m = re.search(r"Cooper found (\w+) additional sporadic solutions, named ([^.]+)\.", text)
    assert m is not None and m.group(1) == "3"
    assert "s22" not in m.group(2).lower()
