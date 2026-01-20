import requests
import json

url = "http://localhost:3000/api/logs"

# Test 1: Direct POST with JSON
print("=" * 60)
print("TEST LOGS AUTH")
print("=" * 60)

headers = {'Content-Type': 'application/json'}
payload = {'password': 'tg'}

print(f"\nTest 1: POST with JSON")
print(f"URL: {url}")
print(f"Payload: {payload}")

try:
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS!")
        print(f"Logs: {len(data['logs'])}")
        print(f"Stats: {data['stats']}")
    else:
        print(f"❌ FAILED")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Different password
print(f"\nTest 2: Wrong password")
payload2 = {'password': 'wrong'}
try:
    response = requests.post(url, json=payload2, headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
