# tests/test_live_api.py
import pytest
import requests

BASE_URL = "https://glistening-flexibility-production.up.railway.app"

def test_health_check():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_register_and_login():
    # Register
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json={
        "email": "smoketest@example.com",
        "username": "smoketest",
        "password": "secret123"
    })
    assert response.status_code in [201, 400]  # 400 if already exists

    # Login
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
        "username": "smoketest",
        "password": "secret123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_rate_limit():
    for i in range(6):
        response = requests.post(f"{BASE_URL}/api/v1/auth/register", json={
            "email": f"ratelimit{i}@test.com",
            "username": f"ratelimituser{i}",
            "password": "secret123"
        })
    assert response.status_code == 429