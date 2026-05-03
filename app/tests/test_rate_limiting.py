import pytest


@pytest.mark.asyncio
async def test_register_rate_limit(client):
    """Test that register endpoint blocks after 5 requests per minute."""
    
    # Enable rate limiting for this test
    from app.core.limiter import limiter
    limiter.enabled = True

    responses = []
    for i in range(6):
        response = await client.post("/api/v1/auth/register", json={
            "email": f"user{i}@example.com",
            "username": f"user{i}",
            "password": "secret123",
        })
        responses.append(response.status_code)

    # First 5 should pass
    assert responses[:5].count(201) == 5
    # 6th should be rate limited
    assert responses[5] == 429

    # Re-disable for other tests
    limiter.enabled = False


@pytest.mark.asyncio
async def test_login_rate_limit(client, registered_user):
    """Test that login endpoint blocks after 10 requests per minute."""
    
    from app.core.limiter import limiter
    limiter.enabled = True

    responses = []
    for i in range(11):
        response = await client.post("/api/v1/auth/login", json={
            "username": registered_user["username"],
            "password": registered_user["password"],
        })
        responses.append(response.status_code)

    # First 10 should pass
    assert all(s == 200 for s in responses[:10])
    # 11th should be rate limited
    assert responses[10] == 429

    limiter.enabled = False