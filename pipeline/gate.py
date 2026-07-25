"""Mechanical gates on `PREDICTION.md` (prereg-pipeline skill, CLAUDE.md rules 1 & 3).

Two distinct gates live here. Keeping them separate is the whole point:

**G1 — real-data access.** `PREDICTION.md` must carry a `PINNED: <sha256>` header
before any real-data comparison runs. Pre-pin, only synthetic-data infrastructure
is permitted. This is what `require_pinned_for_real_data()` enforces.

**G1-L — TEST/FIT labelling.** A pin alone does NOT make a comparison meaningful.
The pin covers the pre-registration *rules* (`PREDICTION.md` §2–§5: the selection
rule, the observable decision rule, the TEST/FIT split, the kill condition). It does
not supply the *numbers* — m_φ, α_D, Λ_D live in §6, which is "Empty by design at
v1.0-PINNED" and is populated only by a completed, two-model-agreed S3-00 derivation.
Labelling an output `TEST` claims it tests a pre-registered prediction; with §6 empty
there is no such prediction, so the honest label is `SYNTHETIC`. That is what
`labels_unlocked()` / `require_derived_for_labels()` enforce.

Why this exists: WP S3-00b (2026-07-25) hit falsification branch F5b — the flux/tadpole
construction needed for a₁, a₂, a₃ is blocked, so §6 will not be populated on the
cooper_s7 branch at all. Before this module distinguished the two gates, opening G1
caused `observables.py` to stamp placeholder computations `FIT`/`TEST` with nothing
behind them. See `NO_PREDICTION_BRANCH.md` §8 and `briefs/GATE_G1L_RULING_2026_07_25.md`.

This module reads files and reports state; it does not decide policy.
"""
import hashlib
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PREDICTION_PATH = REPO_ROOT / "PREDICTION.md"

_PIN_RE = re.compile(r"^PINNED:\s*([0-9a-fA-F]{64})\s*$", re.MULTILINE)
_DERIVED_RE = re.compile(r"^DERIVED:\s*([0-9a-fA-F]{64})\s*$", re.MULTILINE)

# §6 runs from its own heading to the next top-level heading (or EOF).
_SECTION6_RE = re.compile(r"^##\s*6\.\s.*?(?=^##\s|\Z)", re.MULTILINE | re.DOTALL)

# Placeholder wording that means §6 has not actually been filled in. A `DERIVED:`
# hash computed over a still-reserved §6 would otherwise verify happily.
_RESERVED_MARKERS = ("RESERVED", "Empty by design", "TO-BE-DERIVED")


class GateError(RuntimeError):
    """Raised when code tries to run a gated path before that gate opens."""


def _text() -> str:
    if not PREDICTION_PATH.exists():
        return ""
    return PREDICTION_PATH.read_text(encoding="utf-8")


def _strip_header_lines(text: str) -> str:
    """Remove the `PINNED:`/`DERIVED:` header lines and the blank line that
    separated them from the body, so what remains is byte-identical to what was
    hashed when a pin was created.

    Both markers are stripped so that adding `DERIVED:` later does not
    retroactively invalidate an existing `PINNED:` hash — the two are set at
    different times (§6 arrives in a later commit than the rules pin).
    """
    for pattern in (_PIN_RE, _DERIVED_RE):
        m = pattern.search(text)
        if m:
            text = text[:m.start()] + text[m.end():]
    return text.lstrip("\n")


# ---------------------------------------------------------------------------
# G1 — real-data access (pin on the pre-registration rules)
# ---------------------------------------------------------------------------

def prediction_pin() -> str | None:
    """Return the pinned sha256 from PREDICTION.md, or None if unpinned."""
    m = _PIN_RE.search(_text())
    return m.group(1) if m else None


def is_pinned() -> bool:
    return prediction_pin() is not None


def verify_pin_hash() -> bool:
    """Check the PINNED: hash actually matches PREDICTION.md's body."""
    pin = prediction_pin()
    if pin is None:
        return False
    body = _strip_header_lines(_text())
    return hashlib.sha256(body.encode("utf-8")).hexdigest() == pin.lower()


def require_pinned_for_real_data() -> None:
    """Call this at the top of any real-data-touching code path.

    Raises GateError if PREDICTION.md is not pinned — this is gate G1,
    mechanical and non-negotiable (CLAUDE.md rule 1, prereg-pipeline skill).

    NOTE: passing this gate permits real-data *access*. It does not license a
    TEST/FIT label — see require_derived_for_labels().
    """
    if not is_pinned():
        raise GateError(
            "Gate G1 not satisfied: PREDICTION.md has no PINNED: header. "
            "Real-data comparison code may not run. Synthetic-data "
            "infrastructure only (see prereg-pipeline skill)."
        )


# ---------------------------------------------------------------------------
# G1-L — TEST/FIT labelling (derived quantities present in §6)
# ---------------------------------------------------------------------------

def derived_pin() -> str | None:
    """Return the sha256 from the DERIVED: header, or None if absent."""
    m = _DERIVED_RE.search(_text())
    return m.group(1) if m else None


def section6_text() -> str:
    """Return the §6 'Derived quantities' section verbatim, or '' if absent."""
    m = _SECTION6_RE.search(_text())
    return m.group(0) if m else ""


def verify_derived_hash() -> bool:
    """Check the DERIVED: hash matches the current §6 section text."""
    pin = derived_pin()
    if pin is None:
        return False
    section = section6_text()
    if not section:
        return False
    return hashlib.sha256(section.encode("utf-8")).hexdigest() == pin.lower()


def has_derived_quantities() -> bool:
    """True only when §6 carries real, hash-pinned derived quantities.

    Requires all three, so that neither a stray marker nor a hash computed over
    an un-filled section can open this gate:
      1. a `DERIVED: <sha256>` header is present,
      2. it matches the current §6 text,
      3. §6 no longer carries reserved/placeholder wording.
    """
    if not verify_derived_hash():
        return False
    section = section6_text()
    return not any(marker in section for marker in _RESERVED_MARKERS)


def labels_unlocked() -> bool:
    """True when an output may legitimately be labelled TEST or FIT.

    Both gates must hold: the rules are pinned with an intact hash (G1) *and*
    §6 carries hash-pinned derived quantities (G1-L). Anything else is SYNTHETIC.
    """
    return is_pinned() and verify_pin_hash() and has_derived_quantities()


def require_derived_for_labels() -> None:
    """Call this before emitting any TEST/FIT-labelled comparison output.

    Raises GateError when the pin exists but §6 has no derived quantities — the
    state that produced the WP S3-00b mislabelling defect.
    """
    if labels_unlocked():
        return
    if not is_pinned():
        raise GateError(
            "Gate G1-L not satisfied: PREDICTION.md is unpinned, so no output "
            "may carry a TEST or FIT label."
        )
    if not verify_pin_hash():
        raise GateError(
            "Gate G1-L not satisfied: PREDICTION.md's PINNED: hash does not "
            "match its body. The pin is not trustworthy; refusing to label."
        )
    raise GateError(
        "Gate G1-L not satisfied: PREDICTION.md is pinned, but §6 (derived "
        "quantities: m_phi, alpha_D, Lambda_D) carries no hash-pinned values. "
        "The pin covers the pre-registration RULES (§2-§5), not any numbers, so "
        "there is no pre-registered prediction for an output to TEST. Every "
        "comparison must stay labelled SYNTHETIC. On the cooper_s7 branch this "
        "is expected and permanent: falsification branch F5b fired (see "
        "NO_PREDICTION_BRANCH.md §8) because the flux/tadpole construction for "
        "a_1, a_2, a_3 is blocked."
    )


# Generated-by: Claude Opus 5 (T2) under T0 ruling of 2026-07-25 | Verified-by:
# pipeline/tests/test_gate.py (control-example pinned/unpinned/tampered +
# G1-L cases), executed | Reviewed-by: T0 Y (Xavier, 2026-07-25 instruction)
