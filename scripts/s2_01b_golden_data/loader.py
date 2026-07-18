#!/usr/bin/env python3
"""Loader for S2-01b golden test fixtures (Shioda-Inose moduli map checker).

Usage in T1's test suite:
    from scripts.s2_01b_golden_data.loader import load_golden_fixtures

    golden = load_golden_fixtures()
    for test_case in golden.passing_tests():
        # T1's C3b checker must PASS on these
        result = verify_c3b(test_case.order_2, test_case.order_3)
        assert result["status"] == "PASS"
"""
import json
from pathlib import Path
from typing import List


class RecurrenceFixture:
    """Represents a Picard-Fuchs recurrence (order-2 or order-3)."""

    def __init__(self, data: dict):
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.order = data.get("order", 0)
        self.lambda_rate = data.get("lambda", 0.0)
        self.first_terms = data.get("first_terms", [])
        self.recurrence_poly = data.get("recurrence_polynomial", "")

    def __repr__(self):
        return f"Recurrence({self.name}, order={self.order}, λ={self.lambda_rate})"


class TestCase:
    """A single golden test case for C3b checker."""

    def __init__(self, data: dict):
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.expected_status = data.get("status", "UNKNOWN")
        self.rationale = data.get("rationale", "")

        self.order_2 = RecurrenceFixture(data.get("order_2_recurrence", {}))
        self.order_3 = RecurrenceFixture(data.get("order_3_recurrence", {}))

        map_data = data.get("shioda_inose_map", {})
        self.map_exists = map_data.get("status", "") == "expected_to_exist"
        self.verification_order = map_data.get("verification_order", 50)

    def __repr__(self):
        return f"TestCase({self.name}, expected={self.expected_status})"


class GoldenFixtures:
    """Container for all golden test fixtures."""

    def __init__(self, data: dict):
        self.description = data.get("description", "")
        self.generated = data.get("generated", "")

        self.test_cases: List[TestCase] = [
            TestCase(tc) for tc in data.get("test_cases", [])
        ]

        self.expected_behavior = data.get("expected_checker_behavior", {})
        self.references = data.get("references", {})

    def passing_tests(self) -> List[TestCase]:
        """Return test cases expected to PASS."""
        return [tc for tc in self.test_cases if tc.expected_status == "PASS"]

    def failing_tests(self) -> List[TestCase]:
        """Return test cases expected to FAIL."""
        return [tc for tc in self.test_cases if tc.expected_status == "FAIL"]

    def get_test(self, name: str) -> TestCase:
        """Get a specific test case by name."""
        for tc in self.test_cases:
            if tc.name == name:
                return tc
        raise KeyError(f"Test case '{name}' not found")

    def __repr__(self):
        return f"GoldenFixtures({len(self.test_cases)} test cases)"


def load_golden_fixtures() -> GoldenFixtures:
    """Load S2-01b golden test fixtures from golden_test_fixtures.json.

    Returns:
        GoldenFixtures instance with all test cases, organized by expected status.
    """
    fixture_file = Path(__file__).parent / "golden_test_fixtures.json"

    if not fixture_file.exists():
        raise FileNotFoundError(f"Golden fixture file not found: {fixture_file}")

    with open(fixture_file) as f:
        data = json.load(f)

    return GoldenFixtures(data)


if __name__ == "__main__":
    # Quick sanity check
    golden = load_golden_fixtures()
    print(f"Loaded {golden}")
    print(f"  Passing tests: {len(golden.passing_tests())}")
    print(f"  Failing tests: {len(golden.failing_tests())}")
    print()
    for tc in golden.passing_tests():
        print(f"  {tc.name}: {tc.order_3.name} (order={tc.order_3.order}, λ={tc.order_3.lambda_rate})")
    print()
    for tc in golden.failing_tests():
        print(f"  {tc.name}: EXPECT FAIL ({tc.rationale[:50]}...)")
