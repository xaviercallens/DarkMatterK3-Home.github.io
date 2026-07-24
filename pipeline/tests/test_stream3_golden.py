"""test_stream3_golden.py — WP S3-02 golden tests (closure + null)."""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from pipeline.stream3_comparison import load_prediction_block, closure_test, null_test

def test_closure_passes():
    pred = load_prediction_block()
    result = closure_test(pred, n_samples=100)
    assert result.label == "TEST"
    assert result.value < result.threshold
    assert not result.excluded

def test_null_passes():
    pred = load_prediction_block()
    result = null_test(pred, n_samples=1000)
    assert result.label == "TEST"
    assert result.value < result.threshold
    assert not result.excluded

def test_assumption_passthrough():
    pred = load_prediction_block()
    closure_result = closure_test(pred)
    null_result = null_test(pred)
    assert closure_result.assumptions == pred.assumptions
    assert null_result.assumptions == pred.assumptions
