import pytest


@pytest.mark.asyncio
async def test_create_task(client, auth_headers):
    response = await client.post("/api/v1/tasks/", json={
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["is_completed"] is False


@pytest.mark.asyncio
async def test_create_task_unauthenticated(client):
    response = await client.post("/api/v1/tasks/", json={"title": "No auth task"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_tasks(client, auth_headers):
    await client.post("/api/v1/tasks/", json={"title": "Task 1"}, headers=auth_headers)
    await client.post("/api/v1/tasks/", json={"title": "Task 2"}, headers=auth_headers)

    response = await client.get("/api/v1/tasks/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_task_by_id(client, auth_headers):
    created = await client.post("/api/v1/tasks/", json={"title": "Find me"}, headers=auth_headers)
    task_id = created.json()["id"]

    response = await client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Find me"


@pytest.mark.asyncio
async def test_get_task_not_found(client, auth_headers):
    response = await client.get("/api/v1/tasks/9999", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_task(client, auth_headers):
    created = await client.post("/api/v1/tasks/", json={"title": "Old title"}, headers=auth_headers)
    task_id = created.json()["id"]

    response = await client.put(f"/api/v1/tasks/{task_id}", json={
        "title": "New title",
        "is_completed": True,
    }, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New title"
    assert data["is_completed"] is True


@pytest.mark.asyncio
async def test_delete_task(client, auth_headers):
    created = await client.post("/api/v1/tasks/", json={"title": "Delete me"}, headers=auth_headers)
    task_id = created.json()["id"]

    response = await client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204

    get_response = await client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_cannot_access_other_users_task(client, auth_headers):
    created = await client.post("/api/v1/tasks/", json={"title": "Private task"}, headers=auth_headers)
    task_id = created.json()["id"]

    await client.post("/api/v1/auth/register", json={
        "email": "user2@example.com", "username": "user2", "password": "pass2"
    })
    login = await client.post("/api/v1/auth/login", json={"username": "user2", "password": "pass2"})
    user2_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    response = await client.get(f"/api/v1/tasks/{task_id}", headers=user2_headers)
    assert response.status_code == 404
