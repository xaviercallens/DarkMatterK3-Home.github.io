#!/usr/bin/env python3
"""stream3_comparison.py — WP S3-02: Generic comparison pipeline scaffold."""
import json
from dataclasses import dataclass
from typing import Literal

@dataclass
class PredictionBlock:
    candidate_pair: str
    observable: Literal["P1", "P2", "Lyman-alpha", "null-by-prediction"]
    assumptions: list[str]
    m_phi_range: tuple
    test_shape: dict

@dataclass
class ComparisonResult:
    observable: str
    label: Literal["TEST", "FIT"]
    assumptions: list[str]
    test_statistic: str
    value: float
    threshold: float
    excluded: bool
    metadata: dict

def load_prediction_block() -> PredictionBlock:
    return PredictionBlock(
        candidate_pair="TBD (awaiting Stream 2 selection)",
        observable="TBD (awaiting pin)",
        assumptions=["A-SEQ", "A-VOL", "A-ONT", "A-REL"],
        m_phi_range=(1e-23, 1e-22),
        test_shape={"lensing_exponent_beta": (1.0, 3.0)},
    )

_FIELD_N = 24
_NULL_TRIALS = 200


def closure_test(pred: PredictionBlock, n_samples: int = 100) -> ComparisonResult:
    """Recover a known injected signal (EXECUTION_PLAN.md S3-02 acceptance criterion).

    Rewritten 2026-07-26 under Stream 2 standing directive D-1 ("a test that cannot
    fail is not a test"). The previous body returned a hardcoded
    `overlap_sigma = 1.2` and a hardcoded `label="TEST"`: it generated no data,
    ignored `n_samples`, could not fail, and stamped `TEST` while gate G1-L is
    closed. Both defects are fixed here — the computation is real, and the label
    comes from `pipeline.core.run_comparison`, which derives it from gate state.
    """
    from pipeline.core import null_distribution, run_comparison
    from pipeline.synthetic import get_device, signal_field

    device = get_device()
    null_stats = null_distribution(_FIELD_N, n_trials=_NULL_TRIALS, seed=1000,
                                   device=device)
    field = signal_field(_FIELD_N, seed=1, amplitude=3.0, device=device)
    res = run_comparison(field, null_stats, alpha=0.05)

    return ComparisonResult(
        observable=pred.observable,
        label=res["label"],
        assumptions=pred.assumptions,
        test_statistic="injected_signal_p_value",
        value=res["p_value"],
        threshold=0.05,
        # Closure FAILS if the injected signal is not recovered.
        excluded=not res["reject_null"],
        metadata={"type": "closure", "n_samples": n_samples,
                  "observed_statistic": res["observed_statistic"],
                  "n_null_trials": _NULL_TRIALS},
    )

def null_test(pred: PredictionBlock, n_samples: int = 1000) -> ComparisonResult:
    """On signal-free data, report null (EXECUTION_PLAN.md S3-02 acceptance criterion).

    Rewritten 2026-07-26 under Stream 2 standing directive D-1; see `closure_test`.
    The previous body returned a hardcoded `mock_false_pos_rate = 0.03` and
    `label="TEST"`. This measures the false-positive rate over independent
    signal-free fields instead.
    """
    from pipeline.core import null_distribution, run_comparison
    from pipeline.synthetic import get_device, null_field

    device = get_device()
    alpha = 0.05
    reference_null = null_distribution(_FIELD_N, n_trials=_NULL_TRIALS, seed=2000,
                                       device=device)

    n_checks = 40
    false_positives = 0
    label = "SYNTHETIC"
    for k in range(n_checks):
        field = null_field(_FIELD_N, seed=5000 + k, device=device)
        res = run_comparison(field, reference_null, alpha=alpha)
        label = res["label"]
        if res["reject_null"]:
            false_positives += 1
    fpr = false_positives / n_checks

    # Binomial 3-sigma upper bound on the false-positive rate at `alpha` over
    # n_checks draws. Wide enough not to flake, narrow enough to catch a null
    # bank that has stopped behaving like a null.
    bound = alpha + 3.0 * (alpha * (1 - alpha) / n_checks) ** 0.5

    return ComparisonResult(
        observable=pred.observable,
        label=label,
        assumptions=pred.assumptions,
        test_statistic="false_positive_rate",
        value=fpr,
        threshold=bound,
        excluded=fpr > bound,
        metadata={"type": "null", "n_samples": n_samples,
                  "n_checks": n_checks, "false_positives": false_positives,
                  "alpha": alpha},
    )

def main() -> int:
    print("=== WP S3-02: Stream 3 Generic Pipeline Scaffold ===")
    pred = load_prediction_block()
    print(f"Closure test: {closure_test(pred).excluded} (should be False)")
    print(f"Null test: {null_test(pred).excluded} (should be False)")
    return 0

if __name__ == "__main__":
    import sys; sys.exit(main())
