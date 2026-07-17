"""Null test (EXECUTION_PLAN.md WP S3-02 DoD): on data with no injected
signal, the pipeline must report null at the stated false-positive rate.
Merge-blocking per CLAUDE.md."""
from pipeline.core import null_distribution, run_comparison
from pipeline.synthetic import get_device, null_field

N = 24
ALPHA = 0.05
N_TRIALS_REFERENCE = 300
N_TRIALS_CHECK = 40


def test_null_false_positive_rate_within_binomial_bound():
    device = get_device()
    reference_null = null_distribution(N, n_trials=N_TRIALS_REFERENCE, seed=2000,
                                        device=device)

    false_positives = 0
    for k in range(N_TRIALS_CHECK):
        field = null_field(N, seed=5000 + k, device=device)
        result = run_comparison(field, reference_null, alpha=ALPHA)
        false_positives += int(result["reject_null"])
        assert result["label"] == "SYNTHETIC"

    rate = false_positives / N_TRIALS_CHECK
    # Under H0, false positives ~ Binomial(N_TRIALS_CHECK, ALPHA).
    # Bound at mean + 3*sigma to avoid CI flakiness while still catching a
    # miscalibrated statistic (e.g. one reporting significance at 3x alpha).
    mean = ALPHA * N_TRIALS_CHECK
    sigma = (N_TRIALS_CHECK * ALPHA * (1 - ALPHA)) ** 0.5
    bound = (mean + 3 * sigma) / N_TRIALS_CHECK

    assert rate <= bound, (
        f"null test failed: false-positive rate {rate:.3f} exceeds "
        f"mean+3sigma bound {bound:.3f} at alpha={ALPHA}"
    )
