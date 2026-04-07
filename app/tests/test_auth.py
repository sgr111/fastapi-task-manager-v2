import pytest


@pytest.mark.asyncio
async def test_register_success(client):
    response = await client.post("/api/v1/auth/register", json={
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "password123",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client, registered_user):
    response = await client.post("/api/v1/auth/register", json={
        "email": registered_user["email"],
        "username": "differentuser",
        "password": "password123",
    })
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_register_duplicate_username(client, registered_user):
    response = await client.post("/api/v1/auth/register", json={
        "email": "different@example.com",
        "username": registered_user["username"],
        "password": "password123",
    })
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_success(client, registered_user):
    response = await client.post("/api/v1/auth/login", json={
        "username": registered_user["username"],
        "password": registered_user["password"],
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client, registered_user):
    response = await client.post("/api/v1/auth/login", json={
        "username": registered_user["username"],
        "password": "wrongpassword",
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client):
    response = await client.post("/api/v1/auth/login", json={
        "username": "ghost",
        "password": "password",
    })
    assert response.status_code == 401
