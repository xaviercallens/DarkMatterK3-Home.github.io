import os
import sys
import pytest
from unittest.mock import patch, MagicMock
import torch

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import t4_worker

def test_simulate_k3_computation():
    # Provide a dummy chunk
    chunk_data = {"chunk_id": "test", "data_url": "gs://fake/url"}
    
    # Run the computation
    result = t4_worker.simulate_k3_computation(chunk_data)
    
    # Validate the keys
    assert "mean_asymmetry" in result
    assert "max_asymmetry" in result
    assert "s12" in result
    assert "s21" in result
    assert "wasserstein_distance" in result
    
    # Check types and basic constraints
    assert isinstance(result["mean_asymmetry"], float)
    assert isinstance(result["max_asymmetry"], float)
    assert isinstance(result["s12"], float)
    assert isinstance(result["s21"], float)
    assert isinstance(result["wasserstein_distance"], float)

@patch("t4_worker.requests.post")
def test_register_worker_success(mock_post):
    # Mocking successful API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Successfully registered"}
    mock_post.return_value = mock_response
    
    # Run
    t4_worker.register_worker()
    
    # Validate request
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert t4_worker.API_URL + "/users/register" in args[0]
    assert "json" in kwargs
    assert kwargs["json"]["user_id"] == t4_worker.USER_ID

@patch("t4_worker.requests.post")
def test_register_worker_failure(mock_post):
    # Mocking failed API response
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_post.return_value = mock_response
    
    t4_worker.register_worker()
    mock_post.assert_called_once()

@patch("t4_worker.requests.post")
def test_register_worker_exception(mock_post):
    # Mocking an exception
    mock_post.side_effect = Exception("Connection Refused")
    t4_worker.register_worker()
    mock_post.assert_called_once()

@patch("t4_worker.requests.post")
@patch("t4_worker.time.sleep", return_value=None)  # Prevent sleeping
def test_run_worker_job_failure_then_success(mock_sleep, mock_post):
    # We want run_worker to iterate a couple of times.
    # The while loop is infinite, so we need to raise an exception or modify the code slightly,
    # OR we can mock an exception that breaks out of the loop.
    
    # Let's simulate:
    # 1. register -> 200
    # 2. request_job -> 500
    # 3. request_job -> 200 (job provided)
    # 4. submit_job -> 200
    # 5. ConnectionError to exit loop
    
    # Register response
    reg_res = MagicMock()
    reg_res.status_code = 200
    reg_res.json.return_value = {"message": "OK"}
    
    # Request Job 500
    req_fail = MagicMock()
    req_fail.status_code = 500
    
    # Request Job 200
    req_success = MagicMock()
    req_success.status_code = 200
    req_success.json.return_value = {
        "job_id": "job_1234",
        "chunk_data": {"data_url": "test"}
    }
    
    # Submit 200
    submit_success = MagicMock()
    submit_success.status_code = 200
    submit_success.json.return_value = {"message": "Great", "points_earned": 10}
    
    # Submit failure (for coverage)
    submit_fail = MagicMock()
    submit_fail.status_code = 500
    submit_fail.text = "Error"
    
    import requests
    
    # Side effect for the main run_worker while loop:
    # We need to raise StopIteration to exit the loop after testing what we need
    # post calls in run_worker: register, request, (submit), request...
    def side_effect(*args, **kwargs):
        if "/register" in args[0]:
            return reg_res
        elif "/request" in args[0]:
            if side_effect.req_count == 0:
                side_effect.req_count += 1
                return req_fail
            elif side_effect.req_count == 1:
                side_effect.req_count += 1
                return req_success
            elif side_effect.req_count == 2:
                side_effect.req_count += 1
                return req_success # request again to test submit_fail
            else:
                raise KeyboardInterrupt("Exit loop")
        elif "/submit" in args[0]:
            if side_effect.sub_count == 0:
                side_effect.sub_count += 1
                return submit_success
            else:
                return submit_fail
                
    side_effect.req_count = 0
    side_effect.sub_count = 0
    mock_post.side_effect = side_effect
    
    try:
        t4_worker.run_worker()
    except KeyboardInterrupt:
        pass

@patch("t4_worker.requests.post")
@patch("t4_worker.time.sleep", return_value=None)
def test_run_worker_connection_error(mock_sleep, mock_post):
    import requests
    
    def side_effect(*args, **kwargs):
        if "/register" in args[0]:
            return MagicMock(status_code=200)
        elif "/request" in args[0]:
            if side_effect.req_count == 0:
                side_effect.req_count += 1
                raise requests.exceptions.ConnectionError("Connection Failed")
            else:
                raise KeyboardInterrupt("Exit loop")

    side_effect.req_count = 0
    mock_post.side_effect = side_effect

    try:
        t4_worker.run_worker()
    except KeyboardInterrupt:
        pass
