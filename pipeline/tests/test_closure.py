"""Closure test (EXECUTION_PLAN.md WP S3-02 DoD): the pipeline must recover
a known, injected synthetic signal. Merge-blocking per CLAUDE.md."""
from pipeline.core import null_distribution, run_comparison
from pipeline.synthetic import get_device, signal_field

N = 24
ALPHA = 0.05


def test_recovers_injected_signal():
    device = get_device()
    null_stats = null_distribution(N, n_trials=200, seed=1000, device=device)
    field = signal_field(N, seed=1, amplitude=3.0, device=device)

    result = run_comparison(field, null_stats, alpha=ALPHA)

    assert result["reject_null"] is True, (
        f"closure test failed: injected signal not recovered "
        f"(p={result['p_value']}, statistic={result['observed_statistic']})"
    )
    assert result["label"] == "SYNTHETIC"


def test_larger_amplitude_gives_smaller_p_value():
    """Sanity check on statistic monotonicity: more signal -> more significant."""
    device = get_device()
    null_stats = null_distribution(N, n_trials=200, seed=1000, device=device)

    weak = run_comparison(signal_field(N, seed=2, amplitude=0.5, device=device),
                           null_stats, alpha=ALPHA)
    strong = run_comparison(signal_field(N, seed=2, amplitude=4.0, device=device),
                             null_stats, alpha=ALPHA)

    assert strong["observed_statistic"] >= weak["observed_statistic"]
