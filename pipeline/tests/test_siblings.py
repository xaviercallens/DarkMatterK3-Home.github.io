#!/usr/bin/env python3
"""Tests for sibling-family control harness (WP-R4).

Validates P4 discipline:
1. All siblings evaluated when requested
2. Missing certificate raises rather than silently skips
3. Results carry certificate source path
"""

import pytest
from pipeline.siblings import (
    SIBLING_FAMILIES,
    evaluate_across_siblings,
    _load_certificate,
)


def test_sibling_families_defined():
    """At least two sibling families should be defined."""
    assert len(SIBLING_FAMILIES) >= 2
    assert "s7" in SIBLING_FAMILIES
    assert "s10" in SIBLING_FAMILIES


def test_certificates_loaded():
    """All defined sibling families should have certificates loaded."""
    for family_name, family_info in SIBLING_FAMILIES.items():
        # Certificate should exist
        assert family_info["certificate"] is not None, (
            f"{family_name} has no certificate"
        )
        # Should have order_abcd parameters
        assert family_info["order_abcd"] is not None, (
            f"{family_name} has no order_abcd"
        )


def test_order_abcd_shape():
    """Each family's order_abcd should be a 4-tuple."""
    for family_name, family_info in SIBLING_FAMILIES.items():
        order = family_info["order_abcd"]
        assert isinstance(order, tuple), f"{family_name} order_abcd not a tuple"
        assert len(order) == 4, f"{family_name} order_abcd length != 4"


def test_evaluate_across_siblings_basic():
    """Evaluate a simple function across all siblings."""

    def simple_fn(candidate_name):
        """Return the order_abcd tuple for this candidate."""
        family = SIBLING_FAMILIES[candidate_name]
        return family["order_abcd"]

    results = evaluate_across_siblings(simple_fn)

    # Should have results for all families
    assert len(results) == len(SIBLING_FAMILIES)
    assert all(k in results for k in SIBLING_FAMILIES.keys())

    # Each result should have "result", "certificate_path", "status"
    for family_name, result_dict in results.items():
        assert "result" in result_dict
        assert "certificate_path" in result_dict
        assert "status" in result_dict
        assert result_dict["status"] == "ok"
        # Result should be the order_abcd
        assert result_dict["result"] == SIBLING_FAMILIES[family_name]["order_abcd"]


def test_evaluate_across_siblings_with_args():
    """Test passing additional arguments through evaluate_across_siblings."""

    def fn_with_args(candidate_name, multiplier):
        """Multiply the first element of order_abcd by multiplier."""
        family = SIBLING_FAMILIES[candidate_name]
        a, b, c, d = family["order_abcd"]
        return a * multiplier

    results = evaluate_across_siblings(fn_with_args, 2)

    # s7 order_abcd is (13, 4, -27, 3)
    assert results["s7"]["result"] == 13 * 2
    assert results["s10"]["result"] == 6 * 2  # s10 order_abcd is (6, 2, -64, 4)


def test_evaluate_preserves_certificate_path():
    """Results should carry the certificate path of each family."""

    def dummy_fn(candidate_name):
        return 42

    results = evaluate_across_siblings(dummy_fn)

    for family_name, result_dict in results.items():
        # Certificate path should be a non-empty string
        assert isinstance(result_dict["certificate_path"], str)
        assert len(result_dict["certificate_path"]) > 0
        # Should mention the certificate file
        assert "certificates" in result_dict["certificate_path"]


def test_missing_family_in_siblings_raises():
    """If a certificate is somehow missing, P4 harness should raise."""

    # Temporarily inject a missing family (to test error handling)
    from pipeline import siblings

    original_families = dict(siblings.SIBLING_FAMILIES)

    try:
        # Create a mock missing family
        siblings.SIBLING_FAMILIES["nonexistent"] = {
            "certificate": None,
            "certificate_path": "fake/path.json",
            "error": "test missing certificate",
        }

        def dummy_fn(candidate_name):
            return 42

        # Should raise RuntimeError because the certificate is missing
        with pytest.raises(RuntimeError, match="Cannot evaluate nonexistent"):
            evaluate_across_siblings(dummy_fn)

    finally:
        # Restore original families
        siblings.SIBLING_FAMILIES.clear()
        siblings.SIBLING_FAMILIES.update(original_families)


def test_error_in_function_raises():
    """If the function raises an error, evaluate_across_siblings should propagate it."""

    def failing_fn(candidate_name):
        if candidate_name == "s10":
            raise ValueError("Intentional test error")
        return 42

    # Should raise because the function failed for s10
    with pytest.raises(RuntimeError, match="Error evaluating s10"):
        evaluate_across_siblings(failing_fn)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
