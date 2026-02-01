from fastapi.testclient import TestClient
from main import app
from utils.auth import create_access_token

client = TestClient(app)

def verify_login_response():
    # Login as Akshaya
    response = client.post("/counsellors/login", json={
        "email": "akshaya@counselly.com",
        "password": "Akshaya@2025"
    })
    
    if response.status_code == 200:
        data = response.json()
        user = data.get("user", {})
        print(f"User: {user.get('name')}")
        print(f"Profile Image in Response: {user.get('profile_image')}")
    else:
        print(f"Login Failed: {response.text}")

if __name__ == "__main__":
    verify_login_response()
