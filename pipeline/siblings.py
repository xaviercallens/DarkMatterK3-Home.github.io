#!/usr/bin/env python3
"""WP-R4: Sibling-family control harness (P4 discipline enforcement).

P4 (LESSONS_LEARNED.md): Any statistic computed on one K3 candidate must be
computed on all sibling families as an adversarial control. If every sibling
fits equally well, the result is null.

This module enforces P4 by:
1. Defining SIBLING_FAMILIES: dict of candidates with parameters loaded from
   committed certificate files (never from memory).
2. Providing evaluate_across_siblings(fn, *args, **kwargs) which
   automatically computes fn(candidate) for all siblings, returning a dict.
3. Raising if any certificate is missing (rather than silently skipping).

Usage:
    from pipeline.siblings import evaluate_across_siblings, SIBLING_FAMILIES

    # Compute some statistic on all siblings
    results = evaluate_across_siblings(some_observable_fn, arg1, arg2)

    # results = {
    #   "s7": { "statistic": ..., "certificate": ... },
    #   "s10": { "statistic": ..., "certificate": ... },
    #   "t103": { "statistic": ..., "certificate": ... },
    # }
"""

import json
from pathlib import Path
from typing import Callable, Any, Dict


def _load_certificate(candidate_name: str, criterion: str = "C1") -> dict:
    """Load a candidate's certificate from disk.

    Parameters
    ----------
    candidate_name : str
        Candidate family name (s7, s10, gamma, alpha, etc.)
    criterion : str
        Criterion to load (C1, C3b, etc.). Default C1 (mirror integrality).

    Returns
    -------
    dict
        Certificate content (contains order3_abcd, status, verdict, etc.)

    Raises
    ------
    FileNotFoundError
        If certificate does not exist (candidate parameters not available).
    """
    # Map candidates to their certificate files (using C1 as base, which exists for most)
    cert_mapping = {
        "s7": "checkers/certificates/C1_mirror_s7.json",
        "s10": "checkers/certificates/C1_mirror_s10.json",
        "gamma": "checkers/certificates/C1_mirror_gamma.json",
        "alpha": "checkers/certificates/C1_mirror_alpha.json",
        "delta": "checkers/certificates/C1_mirror_delta.json",
        "eta": "checkers/certificates/C1_mirror_eta.json",
    }

    if candidate_name not in cert_mapping:
        raise ValueError(f"Unknown candidate: {candidate_name}")

    cert_path = Path(cert_mapping[candidate_name])
    if not cert_path.exists():
        raise FileNotFoundError(
            f"Certificate not found for {candidate_name}: {cert_path.absolute()}\n"
            "Parameters cannot be accessed without a committed certificate file.\n"
            "Do not fill this gap from memory (LESSONS_LEARNED.md L1)."
        )

    with open(cert_path) as f:
        return json.load(f)


# Define sibling families: candidates to be evaluated as a set
# (Controls: s7/s10 against each other; additional families added as they pass WP-A3)
SIBLING_FAMILIES = {
    "s7": {
        "name": "cooper_s7",
        "oeis": "A183204",
        "certificate_path": "checkers/certificates/C1_mirror_s7.json",
        "description": "Primary route (Cooper sporadic s7)",
    },
    "s10": {
        "name": "cooper_s10",
        "oeis": "A005260",
        "certificate_path": "checkers/certificates/C1_mirror_s10.json",
        "description": "Primary control (Cooper sporadic s10)",
    },
}

# Load and cache certificates with parameters on module import
for family_name, family_info in SIBLING_FAMILIES.items():
    try:
        cert = _load_certificate(family_name)
        # Extract order-(a,b,c,d) parameters
        order_abcd = cert.get("order3_abcd", None)
        family_info["certificate"] = cert
        family_info["order_abcd"] = tuple(order_abcd) if order_abcd else None
    except FileNotFoundError as e:
        # Allow graceful degradation if some certificates are missing
        # (WP-R4 will flag this)
        family_info["certificate"] = None
        family_info["order_abcd"] = None
        family_info["error"] = str(e)


def evaluate_across_siblings(
    fn: Callable,
    *args,
    **kwargs
) -> Dict[str, Any]:
    """Evaluate a function across all sibling families (P4 enforcement).

    Applies the given function to each sibling candidate, ensuring that if a
    result is computed, it is computed for all siblings (not selectively).

    Parameters
    ----------
    fn : callable
        Function signature: fn(candidate_name, **kwargs) → result
        The function receives the candidate name and all kwargs; it is
        responsible for using candidate-specific parameters (e.g., via
        SIBLING_FAMILIES[candidate_name]).
    *args, **kwargs
        Additional arguments passed to fn (beyond candidate_name).

    Returns
    -------
    dict
        Keyed by candidate family name; values are dicts containing:
        - "result": output of fn(candidate)
        - "certificate_path": path to the parameters source
        - "status": "ok" or error message

    Raises
    ------
    RuntimeError
        If any candidate's certificate is missing (parameters unavailable).
        This forces users to address the gap rather than silently skipping.

    Example
    -------
    >>> def compute_mass(candidate_name):
    ...     family = SIBLING_FAMILIES[candidate_name]
    ...     order_abcd = family["order_abcd"]
    ...     # ... compute something from order_abcd ...
    ...     return m_phi
    >>> results = evaluate_across_siblings(compute_mass)
    >>> # results["s7"]["result"] = m_phi for s7
    >>> # results["s10"]["result"] = m_phi for s10
    >>> # results["t103"]["result"] = m_phi for t103 (or error if cert missing)
    """
    results = {}

    for family_name, family_info in SIBLING_FAMILIES.items():
        if family_info["certificate"] is None:
            # Certificate missing: raise rather than silently skip
            error_msg = family_info.get("error", "Certificate not found")
            results[family_name] = {
                "result": None,
                "certificate_path": family_info["certificate_path"],
                "status": "error",
                "error": error_msg,
            }
            # Raise immediately to force user to fix
            raise RuntimeError(
                f"Cannot evaluate {family_name}: {error_msg}\n"
                "P4 discipline requires all siblings. Do not proceed without all certificates."
            )

        try:
            # Call the function with this candidate
            result = fn(family_name, *args, **kwargs)
            results[family_name] = {
                "result": result,
                "certificate_path": str(family_info["certificate_path"]),
                "status": "ok",
            }
        except Exception as e:
            results[family_name] = {
                "result": None,
                "certificate_path": str(family_info["certificate_path"]),
                "status": "error",
                "error": str(e),
            }
            raise RuntimeError(
                f"Error evaluating {family_name}: {e}"
            )

    return results


# Generated-by: Haiku 4.5 | Verified-by: tests/test_siblings.py | Reviewed-by: [pending T0]
