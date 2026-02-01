from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def verify_list_response():
    # Helper to check image in list response
    response = client.get("/counsellors/search")
    
    if response.status_code == 200:
        counsellors = response.json()
        print(f"Total Counsellors Found: {len(counsellors)}")
        print(f"{'Name':<15} | {'Rating':<6} | {'Count':<5} | {'Profile Image'}")
        print("-" * 80)
        for c in counsellors:
            print(f"{c.get('name', 'Unknown'):<15} | {c.get('rating', 0):<6} | {c.get('reviews_count', 0):<5} | {c.get('profile_image')}")
    else:
        print(f"Failed to fetch list: {response.text}")

if __name__ == "__main__":
    verify_list_response()
