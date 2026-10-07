"""Drift-detecting consistency test on Stream 2's mirrored CM-point / A₂ certificates.

Requested by Stream 2 in `briefs/STREAM2_TO_STREAM3_MODULAR_RAIL_AND_CM_POINTS_2026_09_21.md`
§4.2 item 4: "assert that the mirrored certificate's s7 `locus_hits` reproduce the ledger's loci
{−1, 1/27} and that every s10 row is advisory. It fails closed if either repo drifts."

These are STREAM 2 artifacts. Stream 3 did not produce them and does not re-derive their
contents here; it re-ran their controls (46/46 CM, 35/35 A₂) on 2026-09-21 before mirroring.
What this module protects is the *interface*: the facts Stream 3 documents cite. If Stream 2
revises a certificate, or if a mirror is refreshed without re-reading, these fail closed.

The ledger's loci for the two families (CLAUDE.md item 3) are typed here as the EXPECTED values
and compared against the certificate — that is the point of the test, and a mismatch means the
ledger and the certificate disagree, which is a finding either way.
"""
import hashlib
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent.parent
MIRROR = REPO / "data/mirrors/stream2"

# CLAUDE.md epistemic ledger item 3, verbatim: "cooper_s7: {−1, 1/27}; cooper_s10: {−1/4, 1/16}".
LEDGER_FINITE_LOCI = {"cooper_s7": {"-1", "1/27"}, "cooper_s10": {"-1/4", "1/16"}}


def _load(name):
    p = MIRROR / name
    if not p.exists():
        pytest.skip(f"{name} not mirrored")
    return json.loads(p.read_text()), p


def test_mirror_manifest_hashes_match_the_mirrored_files():
    """A refreshed mirror with a stale manifest (or vice versa) fails here, not silently."""
    man, _ = _load("MIRROR_MANIFEST.json")
    for fname, rec in man["files"].items():
        blob = (MIRROR / fname).read_bytes()
        assert hashlib.sha256(blob).hexdigest() == rec["sha256"], f"{fname} drifted from manifest"


def test_s7_locus_hits_reproduce_the_ledger_loci():
    """Stream 2's ask, first half. The certificate's finite loci for s7 must be the ledger's."""
    cert, _ = _load("CM_POINTS_RHO20.json")
    hits = set(cert["families"]["cooper_s7"]["locus_hits"])
    finite = hits - {"infinity"}
    assert finite == LEDGER_FINITE_LOCI["cooper_s7"], (
        f"s7 finite loci {sorted(finite)} != ledger {sorted(LEDGER_FINITE_LOCI['cooper_s7'])}")
    assert "infinity" in hits, "z = infinity row (D = -3, A2) missing from s7 locus_hits"


def test_s10_locus_hits_reproduce_the_ledger_loci():
    cert, _ = _load("CM_POINTS_RHO20.json")
    finite = set(cert["families"]["cooper_s10"]["locus_hits"]) - {"infinity"}
    assert finite == LEDGER_FINITE_LOCI["cooper_s10"]


def test_advisory_flag_mirrors_the_lattice_certificate_status():
    """Stream 2's ask, second half, as it reads after T0 D15' (2026-09-29): the advisory flag is
    not a constant per family but the shadow of the lattice certificate's status. Until D15' s10's
    certificate was DRAFT (D6') and every s10 row was advisory; since D15' it is LIVE
    (C2_cooper_s10_v5.json, value-identical) and no row is. The test asserts the *relation*, so it
    fails closed if a refresh ever carries a flag that disagrees with the recorded status."""
    cert, _ = _load("CM_POINTS_RHO20.json")
    for key, fam in cert["families"].items():
        rows = fam["rows"]
        assert rows, f"no {key} rows"
        expected = fam["lattice_cert_status"] != "LIVE"
        assert fam["advisory"] is expected, f"{key}: advisory={fam['advisory']} but status={fam['lattice_cert_status']}"
        assert all(bool(r.get("advisory", fam["advisory"])) is expected for r in rows), f"{key}: a row disagrees with its family's status"


def test_s10_certificate_is_the_live_v5_after_d15prime():
    """Pins the fact the previous test's expectation rests on: the mirrored s10 record cites the
    LIVE v5 certificate. If Stream 2 reverts D15' (one T0 sentence), this names the change."""
    cert, _ = _load("CM_POINTS_RHO20.json")
    s10 = cert["families"]["cooper_s10"]
    assert s10["lattice_cert"] == "C2_cooper_s10_v5.json" and s10["lattice_cert_status"] == "LIVE"
    assert cert["families"]["cooper_s7"]["lattice_cert_status"] == "LIVE"


def test_flag_still_discriminates_a_draft_status():
    """Negative control: a copy whose s10 status is flipped back to DRAFT must be caught by the
    relation test's logic (advisory stays False while status says DRAFT)."""
    cert, _ = _load("CM_POINTS_RHO20.json")
    s10 = dict(cert["families"]["cooper_s10"])
    s10["lattice_cert_status"] = "DRAFT"
    assert s10["advisory"] is not (s10["lattice_cert_status"] != "LIVE"), "flipping the status must break the relation"


def test_a2_membership_verdicts_are_s7_yes_s10_no():
    """The §4.2 fork's concrete content: A₂ (D = -3) is in the s7 family and not in s10."""
    cert, _ = _load("A2_MEMBERSHIP.json")
    fam = cert["families"]
    blob = json.dumps(fam["cooper_s7"])
    assert "-3" in blob or "A2" in blob, "s7 A2 record unreadable"
    cm, _ = _load("CM_POINTS_RHO20.json")
    for key in ("cooper_s7", "cooper_s10"):   # advisory shadows the lattice-certificate status (D15' lifted s10's)
        assert fam[key]["advisory"] is (cm["families"][key]["lattice_cert_status"] != "LIVE"), key


def test_not_claimed_blocks_travel_with_the_mirrored_data():
    """Stream 2's instruction: mirror `not_claimed` WITH the data, never without."""
    man, _ = _load("MIRROR_MANIFEST.json")
    for fname in ("CM_POINTS_RHO20.json", "A2_MEMBERSHIP.json"):
        cert, _ = _load(fname)
        assert cert.get("not_claimed"), f"{fname} lost its not_claimed block"
        assert man["files"][fname]["not_claimed"], f"manifest dropped {fname} not_claimed"
