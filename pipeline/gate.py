"""Mechanical gate G1 check (prereg-pipeline skill, CLAUDE.md rule 1).

`PREDICTION.md` must carry a `PINNED: <sha256>` header before any real-data
comparison runs. Pre-pin, only synthetic-data infrastructure is permitted.
This module is the single source of truth other code calls to find out
which regime it's in — it does not itself decide policy, it reads the file.
"""
import hashlib
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PREDICTION_PATH = REPO_ROOT / "PREDICTION.md"
_PIN_RE = re.compile(r"^PINNED:\s*([0-9a-fA-F]{64})\s*$", re.MULTILINE)


class GateError(RuntimeError):
    """Raised when code tries to run a real-data path before gate G1 opens."""


def prediction_pin() -> str | None:
    """Return the pinned sha256 from PREDICTION.md, or None if unpinned."""
    if not PREDICTION_PATH.exists():
        return None
    text = PREDICTION_PATH.read_text(encoding="utf-8")
    m = _PIN_RE.search(text)
    return m.group(1) if m else None


def is_pinned() -> bool:
    return prediction_pin() is not None


def verify_pin_hash() -> bool:
    """Check the PINNED: hash actually matches PREDICTION.md's content
    (the header line itself excluded, since it can't hash itself)."""
    text = PREDICTION_PATH.read_text(encoding="utf-8") if PREDICTION_PATH.exists() else ""
    m = _PIN_RE.search(text)
    if not m:
        return False
    # Remove exactly the matched header line, then the newline that
    # separated it from the body, so `body` is byte-identical to what was
    # hashed when the pin was created.
    body = (text[:m.start()] + text[m.end():]).lstrip("\n")
    return hashlib.sha256(body.encode("utf-8")).hexdigest() == m.group(1).lower()


def require_pinned_for_real_data() -> None:
    """Call this at the top of any real-data-touching code path.

    Raises GateError if PREDICTION.md is not pinned — this is gate G1,
    mechanical and non-negotiable (CLAUDE.md rule 1, prereg-pipeline skill).
    """
    if not is_pinned():
        raise GateError(
            "Gate G1 not satisfied: PREDICTION.md has no PINNED: header. "
            "Real-data comparison code may not run. Synthetic-data "
            "infrastructure only (see prereg-pipeline skill)."
        )
