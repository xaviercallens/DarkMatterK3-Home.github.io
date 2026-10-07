#!/usr/bin/env python3
"""
ρ = 20 hypothesis-label vocabulary (T0 ruling R1, 2026-09-21: the ρ = 20 cut is ADOPTED).

WHAT THIS IS. With the definiteness cut adopted, a selection hypothesis is no longer a point on a
continuum (a modular curve) but one of a FINITE list of CM points. This module turns Stream 2's
mirrored certificate into that list: `(candidate, D, z)` labels. It is pre-registration
VOCABULARY — names for hypotheses, so that a future PREDICTION v2 amendment can enumerate what it
is about. Authority: `briefs/T0_RULINGS_2026_09_21.md` R1/R2.

WHAT THIS IS NOT. A label is not an observable and carries none. There is no map from a CM point
to (m, f), m_φ, α_D or Λ_D: that map is Tier C, BLOCKED under F5b, and the tadpole is unposable
without a base B₃ (CLAUDE.md ledger item 4). `observable_for()` exists only to make that block
mechanical — it raises, always, until a pinned ruling says otherwise. Nothing here ranks a
candidate, prefers a discriminant, or reads real data. The ADVISORY flag on a label shadows the
lattice-certificate status recorded in the mirrored certificate (cooper_s10 was DRAFT under T0 D6′
until D15′, 2026-09-29, made C2_cooper_s10_v5 LIVE); the flag travels with every label either way.

INDEPENDENT LEG. `admits_discriminant` implements Stream 2's criterion ("D occurs in the level-n
family iff D is a square mod 4n") from its statement, not from their code, and the test suite
checks it against every row of their `discriminants_admitted_summary` table — producer ≠ verifier
on the one candidate-dependent predicate this program has.

Inputs are the SHA256-pinned mirror at `data/mirrors/stream2/`; `load_labels` refuses a mirror
whose files do not match `MIRROR_MANIFEST.json`.
"""
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
MIRROR_DIR = REPO_ROOT / "data/mirrors/stream2"

LABEL_KIND = ("HYPOTHESIS-LABEL — rho=20 CM-point vocabulary; not an observable, "
              "not exclusion, not FIT, not TEST")
RULING = "briefs/T0_RULINGS_2026_09_21.md R1 (rho=20 cut ADOPTED); ranking and min-|D| NOT adopted"

# Modular level per candidate: lattice n = modular level (Stream 2 T3, AGREE(7) / AGREE(10)).
LEVELS = {"cooper_s7": 7, "cooper_s10": 10}


class MirrorIntegrityError(RuntimeError):
    """A mirrored certificate does not match its pinned SHA256."""


class TierCBlockedError(PermissionError):
    """An observable was requested from a hypothesis label. None exists under F5b."""


def admits_discriminant(D: int, n: int, modulus_multiplier: int = 4) -> bool:
    """True iff the negative discriminant D occurs in the level-n family: D is a square mod 4n.

    `modulus_multiplier` is 4 in the criterion; it is a parameter ONLY so the negative control can
    run the same comparison with a wrong modulus and show the table check discriminates.
    """
    if D >= 0 or D % 4 not in (0, 1):
        return False
    mod = modulus_multiplier * n
    target = D % mod
    return any((x * x) % mod == target for x in range(mod))


@dataclass(frozen=True)
class HypothesisLabel:
    candidate: str
    n: int
    D: int
    z: Optional[str]              # rational value, "infinity", a minimal polynomial, or None
    z_kind: str                   # "rational" | "infinity" | "algebraic" | "unrecognised"
    T_X_reduced_form_abc: tuple
    singular_locus: Optional[str]
    advisory: bool
    usable: bool                  # False when z is unrecognised: the label is incomplete
    flags: tuple
    kind: str = LABEL_KIND

    @property
    def key(self) -> str:
        return f"{self.candidate}|D={self.D}|z={self.z}"


def _verify_mirror(mirror_dir: Path) -> dict:
    manifest = json.loads((mirror_dir / "MIRROR_MANIFEST.json").read_text())
    for fname, rec in manifest["files"].items():
        actual = hashlib.sha256((mirror_dir / fname).read_bytes()).hexdigest()
        if actual != rec["sha256"]:
            raise MirrorIntegrityError(
                f"{fname}: sha256 {actual[:16]}… != pinned {rec['sha256'][:16]}… — "
                f"refusing to build labels from an unpinned certificate")
    return manifest


def _z_of(row: dict) -> tuple:
    if not row.get("z_recognised"):
        return None, "unrecognised"
    if str(row.get("z_numeric")) == "infinity":
        return "infinity", "infinity"
    if row.get("z_value_if_rational") is not None:
        return str(row["z_value_if_rational"]), "rational"
    return str(row.get("z_minpoly")), "algebraic"


def load_labels(mirror_dir: Path = MIRROR_DIR) -> list:
    """All (candidate, D, z) hypothesis labels from the pinned mirror, advisory flags preserved."""
    _verify_mirror(Path(mirror_dir))
    cert = json.loads((Path(mirror_dir) / "CM_POINTS_RHO20.json").read_text())
    labels = []
    for cand, fam in cert["families"].items():
        n = LEVELS[cand]
        if int(fam["n"]) != n:
            raise ValueError(f"{cand}: certificate level {fam['n']} != expected {n}")
        for row in fam["rows"]:
            z, z_kind = _z_of(row)
            locus = row.get("singular_locus_match")
            labels.append(HypothesisLabel(
                candidate=cand, n=n, D=int(row["D"]), z=z, z_kind=z_kind,
                T_X_reduced_form_abc=tuple(row["T_X_reduced_form_abc"]),
                singular_locus=None if locus in (None, False, "") else str(locus),
                advisory=bool(row.get("advisory")) or bool(fam.get("advisory")),
                usable=z is not None,
                flags=tuple(row.get("flags") or ()),
            ))
    return labels


def observable_for(label: HypothesisLabel):
    """There is none. Raises, always — the F5b block made mechanical (ledger item 4)."""
    raise TierCBlockedError(
        f"no observable exists for {label.key}: the map from a CM point to (m, f), m_phi, alpha_D "
        f"or Lambda_D is Tier C and BLOCKED under F5b; the tadpole is unposable without a base B3. "
        f"A hypothesis label names a hypothesis; it predicts nothing.")


def vocabulary_record(labels: list) -> dict:
    """The persisted artifact: every label, with counts that make advisory status impossible to miss."""
    per = {}
    for lab in labels:
        p = per.setdefault(lab.candidate, {"n": lab.n, "labels": 0, "advisory": 0, "unusable": 0,
                                           "distinct_D": set()})
        p["labels"] += 1
        p["advisory"] += int(lab.advisory)
        p["unusable"] += int(not lab.usable)
        p["distinct_D"].add(lab.D)
    for p in per.values():
        p["distinct_D"] = len(p["distinct_D"])
    return {
        "label": LABEL_KIND,
        "authority": RULING,
        "not_claimed": [
            "that any label is preferred, ranked, or selected: no minimum-|D| rule is adopted",
            "that any label maps to an observable: observable_for() raises by design (F5b)",
            "that the list is complete: Stream 2's enumeration window is not shown to be a "
            "fundamental domain, and their own not_claimed blocks travel with the mirror",
            "that any label is settled beyond Tier B: the advisory flag shadows the mirrored lattice-certificate "
            "status (s10 DRAFT under D6' until D15', 2026-09-29); 'this lattice is T' stays Tier B for both families",
        ],
        "per_candidate": per,
        "labels": [asdict(l) | {"key": l.key} for l in labels],
    }
