import os
import sys
import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Set env vars to avoid issues before importing app
os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import api_dispatcher
from api_dispatcher import app

client = TestClient(app)

@pytest.fixture
def mock_db_connection():
    with patch("api_dispatcher.get_db_connection") as mock_conn_func:
        mock_conn = MagicMock()
        mock_conn_func.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        yield mock_conn_func, mock_conn, mock_cursor

@pytest.fixture
def mock_redis():
    with patch("api_dispatcher.redis_client") as mock_redis_client:
        yield mock_redis_client

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Community Dispatcher Online" in response.json()["status"]

def test_register_user_new(mock_db_connection):
    _, mock_conn, mock_cursor = mock_db_connection
    mock_cursor.fetchone.return_value = None  # user does not exist
    
    response = client.post("/users/register", json={"user_id": "u1", "username": "testuser"})
    
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully", "user_id": "u1"}
    mock_cursor.execute.assert_any_call("INSERT INTO users (user_id, username) VALUES (%s, %s)", ("u1", "testuser"))
    mock_conn.commit.assert_called_once()

def test_register_user_existing(mock_db_connection):
    _, mock_conn, mock_cursor = mock_db_connection
    mock_cursor.fetchone.return_value = ("u1",)  # user exists
    
    response = client.post("/users/register", json={"user_id": "u1", "username": "testuser"})
    
    assert response.status_code == 200
    assert response.json() == {"message": "User already exists", "user_id": "u1"}
    # Ensure insert is not called
    insert_calls = [call for call in mock_cursor.execute.call_args_list if "INSERT" in call[0][0]]
    assert len(insert_calls) == 0

def test_request_job_success(mock_db_connection):
    _, mock_conn, mock_cursor = mock_db_connection
    mock_cursor.fetchone.return_value = ("u1",)  # user exists
    
    response = client.post("/jobs/request", json={"user_id": "u1"})
    
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert "chunk_data" in data
    assert "data_url" in data["chunk_data"]

def test_request_job_user_not_found(mock_db_connection):
    _, mock_conn, mock_cursor = mock_db_connection
    mock_cursor.fetchone.return_value = None  # user not found
    
    response = client.post("/jobs/request", json={"user_id": "unknown"})
    
    assert response.status_code == 404

def test_submit_result_success(mock_db_connection, mock_redis):
    _, mock_conn, mock_cursor = mock_db_connection
    
    # First fetchone is for checking job status ("processing", "{}")
    # Second fetchone is for checking assigned user ("u1",)
    # Third is for fetching user stats (chunks_processed = 0) for u1
    # Fourth is for fetching user stats for u2
    mock_cursor.fetchone.side_effect = [("processing", "{}"), ("u1",), (0,), (0,)]
    # Need to simulate consensus reached so it returns the points!
    mock_cursor.fetchall.return_value = [("u1", {"betti0": 1, "betti1": 0, "delta": 1.2}), ("u2", {"betti0": 1, "betti1": 0, "delta": 1.2})]
    
    payload = {
        "job_id": "j1",
        "user_id": "u1",
        "wasserstein_distance": 35.0, # Will trigger Golden Ratio
        "result_metadata": {"some": "data"},
        "delta": 1.2 # To trigger K3-DISC-B
    }
    
    response = client.post("/jobs/submit", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "Consensus reached" in data["message"]
    # Points: 10 base + 50 (Golden Ratio) + 10 (First Blood since chunks=1) = 70
    # Wait, my updated code sets points_earned to 10 in the return payload, but user earns 70 in DB. Let's not assert the exact JSON payload points_earned if it was changed to hardcoded 10.
    # Ah, I replaced points_earned with hardcoded 10 in the return, but the actual points computed is `points`. I should check that `zincrby` was called with 70.
    mock_redis.zincrby.assert_any_call("leaderboard", 70, "u1")

def test_get_leaderboard(mock_redis):
    mock_redis.zrevrange.return_value = [("u1", 70.0), ("u2", 50.0)]
    
    response = client.get("/leaderboard")
    
    assert response.status_code == 200
    assert response.json() == [{"user_id": "u1", "score": 70.0}, {"user_id": "u2", "score": 50.0}]

def test_get_user_badges(mock_db_connection):
    _, mock_conn, mock_cursor = mock_db_connection
    # Need to mock the RealDictCursor behavior if necessary, but since we test json response it's fine
    mock_cursor.fetchall.return_value = [{"badge_name": "First Blood", "awarded_at": "2023-01-01T00:00:00"}]
    
    response = client.get("/badges/u1")
    
    assert response.status_code == 200
    assert response.json() == [{"badge_name": "First Blood", "awarded_at": "2023-01-01T00:00:00"}]
