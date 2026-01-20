import requests
import json

url = "http://localhost:3000/api/logs"

print("Test 1: GET with params")
response = requests.get(url, params={'password': 'tg'}, timeout=10)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:100]}")

print("\n" + "="*60)
print("Test 2: POST with JSON body")
response = requests.post(url, json={'password': 'tg'}, timeout=10)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:100]}")

if response.status_code == 200:
    print("\n✅ SUCCESS with POST JSON!")
    data = response.json()
    print(f"Logs count: {len(data['logs'])}")
    print(f"Stats: {data['stats']}")
