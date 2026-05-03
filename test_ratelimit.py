import requests

BASE_URL = "https://glistening-flexibility-production.up.railway.app"

print("Testing register rate limit (5/minute)...")
for i in range(7):
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json={
        "email": f"ratelimituser{i}@test.com",
        "username": f"ratelimituser{i}",
        "password": "secret123"
    })
    print(f"Request {i+1}: Status {response.status_code}")
    if response.status_code == 429:
        print(f"Rate limited! Response: {response.json()}")
        break