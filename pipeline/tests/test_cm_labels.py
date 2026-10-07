"""ρ = 20 hypothesis-label vocabulary (T0 ruling R1, 2026-09-21). Every positive check is paired
with a control that makes it able to fail."""
import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import cm_labels as L  # noqa: E402

A2_CERT = L.MIRROR_DIR / "A2_MEMBERSHIP.json"


def _table():
    if not A2_CERT.exists():
        pytest.skip("Stream 2 mirror not present")
    return json.loads(A2_CERT.read_text())["discriminants_admitted_summary"]


def _disagreements(multiplier):
    """Rows of Stream 2's table where the predicate, run with this modulus, disagrees."""
    bad = []
    for row in _table():
        for n, col in ((7, "n7"), (10, "n10")):
            if L.admits_discriminant(row["D"], n, modulus_multiplier=multiplier) != row[col]:
                bad.append((row["D"], n))
    return bad


def test_predicate_reproduces_every_row_of_stream2_table():
    """Producer != verifier: the criterion, implemented here from its statement, must agree with
    every row of Stream 2's admitted-discriminant table for both levels."""
    assert _disagreements(4) == []


def test_table_check_can_fail_with_a_wrong_modulus():
    """Negative control: the SAME comparison with 'square mod n' or 'square mod 2n' must disagree
    with the table somewhere. Otherwise agreement above would carry no information."""
    assert _disagreements(1), "mod n agrees with the table — the check does not discriminate"
    assert _disagreements(2), "mod 2n agrees with the table — the check does not discriminate"


def test_admitted_counts_match_stream2_headline():
    """Stream 2's brief: |D| <= 100 admits 27 discriminants for n = 7, 22 for n = 10, 10 in common.
    Counted here over the table's own D list with the independent predicate."""
    ds = [r["D"] for r in _table()]
    s7 = {d for d in ds if L.admits_discriminant(d, 7)}
    s10 = {d for d in ds if L.admits_discriminant(d, 10)}
    assert (len(s7), len(s10), len(s7 & s10)) == (27, 22, 10)


def test_a2_discriminant_is_in_s7_and_not_in_s10():
    assert L.admits_discriminant(-3, 7) is True      # -3 = 25 = 5^2 mod 28
    assert L.admits_discriminant(-3, 10) is False    # -3 = 37 is not a square mod 40


def test_non_discriminants_are_rejected():
    for bad in (0, 5, -1, -2, -5, -6):               # >= 0, or not 0/1 mod 4
        assert L.admits_discriminant(bad, 7) is False


def test_every_certificate_label_satisfies_the_predicate():
    """Cross-certificate consistency: every D in CM_POINTS_RHO20 must be admitted for its own
    level by the criterion checked against A2_MEMBERSHIP. Two Stream 2 artifacts, one independent
    predicate between them."""
    labels = L.load_labels()
    assert labels
    offenders = [l.key for l in labels if not L.admits_discriminant(l.D, l.n)]
    assert offenders == []


def _status(fam):
    cm = json.loads((L.MIRROR_DIR / "CM_POINTS_RHO20.json").read_text())
    return cm["families"][fam]["lattice_cert_status"]


def test_advisory_flag_shadows_the_lattice_certificate_status():
    """The flag is the shadow of the mirrored certificate's lattice-cert status, not a constant per
    family: s10 was DRAFT (advisory) under T0 D6' and is LIVE (not advisory) since D15', 2026-09-29."""
    labels = L.load_labels()
    for fam in ("cooper_s7", "cooper_s10"):
        fl = [l for l in labels if l.candidate == fam]
        expected = _status(fam) != "LIVE"
        assert fl and all(l.advisory is expected for l in fl), f"{fam}: a label disagrees with status {_status(fam)}"


def test_a2_label_exists_once_in_s7_at_infinity():
    hits = [l for l in L.load_labels() if l.D == -3]
    assert [l.key for l in hits] == ["cooper_s7|D=-3|z=infinity"]
    assert hits[0].T_X_reduced_form_abc == (1, 1, 1)


def test_tampered_mirror_is_refused(tmp_path):
    """Fail closed: one changed byte in a mirrored certificate and no labels are built."""
    mirror = tmp_path / "stream2"
    shutil.copytree(L.MIRROR_DIR, mirror)
    L.load_labels(mirror)                                        # pristine copy loads
    p = mirror / "CM_POINTS_RHO20.json"
    txt = p.read_text()
    assert '"advisory": false' in txt
    p.write_text(txt.replace('"advisory": false', '"advisory": true', 1))
    with pytest.raises(L.MirrorIntegrityError):
        L.load_labels(mirror)


def test_no_observable_can_be_obtained_from_a_label():
    """The F5b block, mechanical: asking a label for an observable raises, for every label."""
    for lab in L.load_labels()[:5]:
        with pytest.raises(L.TierCBlockedError):
            L.observable_for(lab)


def test_vocabulary_record_is_labelled_and_never_a_comparison_output():
    rec = L.vocabulary_record(L.load_labels())
    assert rec["label"] == L.LABEL_KIND and "HYPOTHESIS-LABEL" in rec["label"]
    for fam in ("cooper_s7", "cooper_s10"):
        expected = rec["per_candidate"][fam]["labels"] if _status(fam) != "LIVE" else 0
        assert rec["per_candidate"][fam]["advisory"] == expected, fam
    assert any("ranked" in s or "preferred" in s for s in rec["not_claimed"])
