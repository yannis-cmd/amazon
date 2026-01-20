import requests

url = "http://localhost:3000/api/logs"
params = {'password': 'tg'}

print("Testing /api/logs with password='tg'...")
response = requests.get(url, params=params, timeout=10)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")

if response.status_code == 200:
    print("\n✅ SUCCESS!")
    data = response.json()
    print(f"Logs count: {len(data['logs'])}")
else:
    print(f"\n❌ FAILED")
