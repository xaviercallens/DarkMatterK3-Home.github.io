import pytest
from fastapi.testclient import TestClient
from api_darkmatter import app
import os
import json

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "DarkMatterK3 API Online" in response.json()["status"]

def test_get_leaderboard():
    response = client.get("/leaderboard")
    assert response.status_code == 200
    data = response.json()
    assert "leaderboard" in data
    assert isinstance(data["leaderboard"], list)
    assert len(data["leaderboard"]) > 0
    assert data["leaderboard"][0]["node"] == "T4_Worker_Xavier"

def test_get_user_badges():
    user_id = "test_user"
    response = client.get(f"/badges/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert "badges" in data
    assert isinstance(data["badges"], list)
    assert len(data["badges"]) == 3
    assert data["badges"][0]["name"] == "First Blood"

def test_get_status():
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
