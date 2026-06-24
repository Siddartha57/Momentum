import urllib.request
import json

url = "http://localhost:8000/api/auth/register"
data = {"full_name": "Test User", "email": "test10@example.com", "password": "password123", "daily_target_hours": "2"}
req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")

try:
    response = urllib.request.urlopen(req)
    print("Success:", response.read().decode("utf-8"))
except Exception as e:
    print("Error:", e.read().decode("utf-8"))
