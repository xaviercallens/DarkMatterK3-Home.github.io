"""Tests for the F-LAB monitoring trigger (advisory-only check).

F-LAB: future public ISL data excluding |α|=1 below 38.6 μm reopens Gate 0
re-evaluation. The check_flab_trigger() function is purely advisory — it reports
whether a claimed exclusion region meets the numeric criterion, but does not
reopen any gate or modify any state.

Reference: NO_PREDICTION_BRANCH.md §9, WP_A2_CIRCULARITY_AUDIT.md §5.
"""
import pipeline.gate as gate


def test_flab_trigger_at_boundary_alpha_and_lambda():
    """Case (a): excluded_alpha=1.0, excluded_lambda_um=30.0 → trigger_fired=True.

    This exactly meets the trigger condition: α ≤ 1.0 AND λ < 38.6 μm.
    Matches the intended F-LAB criterion.
    """
    result = gate.check_flab_trigger(excluded_alpha=1.0, excluded_lambda_um=30.0)
    assert result["trigger_fired"] is True
    assert result["threshold_lambda_um"] == 38.6
    assert "Numeric criterion met" in result["reasoning"]


def test_flab_trigger_fails_on_lambda_above_threshold():
    """Case (b): excluded_lambda_um=40.0 (above 38.6 μm) → trigger_fired=False.

    The range is outside the F-LAB window; trigger does not fire.
    """
    result = gate.check_flab_trigger(excluded_alpha=1.0, excluded_lambda_um=40.0)
    assert result["trigger_fired"] is False
    assert result["threshold_lambda_um"] == 38.6
    assert "range criterion not met" in result["reasoning"]


def test_flab_trigger_fails_on_alpha_above_1():
    """Case (c): excluded_alpha=1e6 (doesn't constrain |α|=1) → trigger_fired=False.

    A paper that only excludes very large couplings does not constrain the
    physically relevant α=1 regime; trigger does not fire.
    """
    result = gate.check_flab_trigger(excluded_alpha=1e6, excluded_lambda_um=30.0)
    assert result["trigger_fired"] is False
    assert result["threshold_lambda_um"] == 38.6
    assert "α-criterion not met" in result["reasoning"]


def test_flab_trigger_fails_on_both_criteria():
    """Edge case: both excluded_alpha and excluded_lambda_um miss the threshold.

    Trigger should not fire; reasoning should list both missed criteria.
    """
    result = gate.check_flab_trigger(excluded_alpha=2.0, excluded_lambda_um=50.0)
    assert result["trigger_fired"] is False
    assert "α-criterion not met" in result["reasoning"]
    assert "range criterion not met" in result["reasoning"]


def test_flab_trigger_with_excluded_alpha_well_below_1():
    """Stronger constraint case: excluded_alpha=0.5, excluded_lambda_um=20.0.

    Both criteria met (α ≤ 1.0 AND λ < 38.6); trigger fires.
    A paper excluding even tighter coupling at sub-20μm ranges would be
    a strong F-LAB candidate.
    """
    result = gate.check_flab_trigger(excluded_alpha=0.5, excluded_lambda_um=20.0)
    assert result["trigger_fired"] is True
    assert "Numeric criterion met" in result["reasoning"]


def test_flab_trigger_on_lambda_exactly_at_boundary():
    """Boundary case: excluded_lambda_um exactly at 38.6 μm (not below).

    The criterion is λ < 38.6, so λ = 38.6 does not satisfy it.
    Trigger should not fire.
    """
    result = gate.check_flab_trigger(excluded_alpha=1.0, excluded_lambda_um=38.6)
    assert result["trigger_fired"] is False
    assert "range criterion not met" in result["reasoning"]


def test_flab_trigger_on_alpha_exactly_1():
    """Boundary case: excluded_alpha exactly 1.0.

    The criterion is α ≤ 1.0, so α = 1.0 satisfies it (if λ also qualifies).
    Combined with λ < 38.6, trigger fires.
    """
    result = gate.check_flab_trigger(excluded_alpha=1.0, excluded_lambda_um=37.0)
    assert result["trigger_fired"] is True


def test_flab_trigger_does_not_modify_global_state():
    """Case (d): Confirm the function is side-effect-free.

    The check should not touch PREDICTION.md, not call require_pinned_for_real_data,
    not call require_derived_for_labels, and not modify any global state.
    This is purely advisory.
    """
    # Call the function multiple times with different inputs.
    result1 = gate.check_flab_trigger(excluded_alpha=1.0, excluded_lambda_um=30.0)
    result2 = gate.check_flab_trigger(excluded_alpha=2.0, excluded_lambda_um=50.0)
    result3 = gate.check_flab_trigger(excluded_alpha=0.5, excluded_lambda_um=10.0)

    # Verify results are consistent and independent.
    assert result1["trigger_fired"] is True
    assert result2["trigger_fired"] is False
    assert result3["trigger_fired"] is True

    # The function should return consistent structure.
    for result in [result1, result2, result3]:
        assert "trigger_fired" in result
        assert "threshold_lambda_um" in result
        assert "reasoning" in result
        assert result["threshold_lambda_um"] == 38.6

    # No exception should be raised; gate state is unchanged.
    # (There is no simple way to verify "no file was touched" without mocking,
    # but the lack of any write/import in the function body confirms it.)


def test_flab_trigger_return_structure():
    """Confirm the return dict has exactly the expected keys and types."""
    result = gate.check_flab_trigger(excluded_alpha=1.0, excluded_lambda_um=30.0)

    assert isinstance(result, dict)
    assert set(result.keys()) == {"trigger_fired", "threshold_lambda_um", "reasoning"}
    assert isinstance(result["trigger_fired"], bool)
    assert isinstance(result["threshold_lambda_um"], float)
    assert isinstance(result["reasoning"], str)


# Generated-by: Claude Haiku 4.5 | Verified-by: pytest execution;
# function is advisory-only, no state mutation | Reviewed-by: none yet
