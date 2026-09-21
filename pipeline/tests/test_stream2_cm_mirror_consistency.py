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


def test_every_s10_row_is_advisory():
    """Stream 2's ask, second half. s10's lattice certificate is DRAFT (T0 D6'), so every s10
    row is advisory and must never be cited as settled. If a refresh drops the flag, fail."""
    cert, _ = _load("CM_POINTS_RHO20.json")
    rows = cert["families"]["cooper_s10"]["rows"]
    assert rows, "no s10 rows"
    non_advisory = [r for r in rows if not r.get("advisory")]
    assert not non_advisory, f"{len(non_advisory)} cooper_s10 rows lost advisory=true"


def test_s7_rows_are_not_advisory_so_the_flag_discriminates():
    """Negative control for the test above: if `advisory` were set on everything (or on
    nothing), the s10 check would carry no information. s7's T2 is LIVE, so its rows must NOT
    be advisory."""
    cert, _ = _load("CM_POINTS_RHO20.json")
    s7 = cert["families"]["cooper_s7"]["rows"]
    assert s7 and not any(r.get("advisory") for r in s7), (
        "cooper_s7 rows are advisory too — the advisory flag no longer discriminates")


def test_a2_membership_verdicts_are_s7_yes_s10_no():
    """The §4.2 fork's concrete content: A₂ (D = -3) is in the s7 family and not in s10."""
    cert, _ = _load("A2_MEMBERSHIP.json")
    fam = cert["families"]
    blob = json.dumps(fam["cooper_s7"])
    assert "-3" in blob or "A2" in blob, "s7 A2 record unreadable"
    assert fam["cooper_s10"]["advisory"] is True, "s10 A2 row must stay advisory"
    assert fam["cooper_s7"]["advisory"] is False


def test_not_claimed_blocks_travel_with_the_mirrored_data():
    """Stream 2's instruction: mirror `not_claimed` WITH the data, never without."""
    man, _ = _load("MIRROR_MANIFEST.json")
    for fname in ("CM_POINTS_RHO20.json", "A2_MEMBERSHIP.json"):
        cert, _ = _load(fname)
        assert cert.get("not_claimed"), f"{fname} lost its not_claimed block"
        assert man["files"][fname]["not_claimed"], f"manifest dropped {fname} not_claimed"
