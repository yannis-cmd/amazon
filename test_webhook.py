import requests
import json

url = "https://discord.com/api/webhooks/1462917224154005647/eDTFaXGmuPFZlGJMLxJukL1f6qroMX7kDHGepF_WEaMw5cu0EHG9isxk8FclBcpum1_1"

print("=" * 60)
print("TESTING DISCORD WEBHOOK")
print("=" * 60)

# Test 1: Message simple
print("\nTest 1: Simple message...")
try:
    data1 = {"content": "Test 1: Simple message from Amazon Tracker"}
    r1 = requests.post(url, json=data1, timeout=10)
    print(f"Status: {r1.status_code}")
    if r1.text:
        print(f"Response: {r1.text}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Message avec embed
print("\nTest 2: Message with embed...")
try:
    data2 = {
        "embeds": [{
            "title": "TEST EMBED",
            "description": "This is a test message from the webhook",
            "color": 3447003
        }]
    }
    r2 = requests.post(url, json=data2, timeout=10)
    print(f"Status: {r2.status_code}")
    if r2.text:
        print(f"Response: {r2.text}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Validation de l'URL
print("\nTest 3: URL validation...")
parts = url.split("/")
if len(parts) >= 2:
    webhook_id = parts[-2]
    webhook_token = parts[-1]
    print(f"Webhook ID: {webhook_id}")
    print(f"Webhook Token length: {len(webhook_token)}")
    print(f"Full URL valid: {len(url) > 50}")

print("\n" + "=" * 60)
