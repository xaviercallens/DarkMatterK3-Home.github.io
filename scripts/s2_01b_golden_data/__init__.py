"""S2-01b Golden Test Data Package

Golden fixtures for the C3b (Shioda-Inose moduli map) checker implementation.
Provides reference Picard-Fuchs recurrence pairs with known outcomes.

Usage:
    from scripts.s2_01b_golden_data import load_golden_fixtures

    golden = load_golden_fixtures()
    for test_case in golden.passing_tests():
        # T1's C3b checker must PASS on these
        ...
"""

from scripts.s2_01b_golden_data.loader import (
    GoldenFixtures,
    RecurrenceFixture,
    TestCase,
    load_golden_fixtures,
)

__all__ = [
    "load_golden_fixtures",
    "GoldenFixtures",
    "TestCase",
    "RecurrenceFixture",
]
