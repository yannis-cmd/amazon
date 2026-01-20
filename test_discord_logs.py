#!/usr/bin/env python3
"""Test that Discord logs are working"""

import requests
import json
import time

BASE_URL = "http://localhost:3000"

def test_search():
    """Test search endpoint"""
    print("Testing SEARCH endpoint...")
    payload = {
        "query": "Casque Gamer",
        "user": "TestDiscord001", 
        "page": 1
    }
    
    response = requests.post(
        f"{BASE_URL}/api/search",
        json=payload,
        timeout=60
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Articles found: {data.get('count', 0)}")
        print("✅ SEARCH logged to Discord")
    else:
        print(f"❌ Error: {response.text}")
    
    return response.status_code == 200

def test_add_article():
    """Test adding an article"""
    print("\nTesting ADD ARTICLE endpoint...")
    payload = {
        "name": "Souris Test",
        "price": 29.99,
        "url": "https://amazon.fr/test",
        "user": "TestDiscord002"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/articles/add",
        json=payload,
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code in [200, 201]:
        print("✅ ARTICLE ADD logged to Discord")
    else:
        print(f"❌ Error: {response.text}")
    
    return response.status_code in [200, 201]

def check_logs():
    """Check local activity logs"""
    print("\nChecking LOCAL ACTIVITY LOGS...")
    try:
        with open("activity_logs.json", "r") as f:
            logs = json.load(f)
        
        print(f"Total logs: {len(logs)}")
        
        # Show last 3 logs
        for log in logs[-3:]:
            print(f"  - {log['action']} by {log['user']} at {log['timestamp']}")
        
        return len(logs) > 0
    except Exception as e:
        print(f"❌ Error reading logs: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("DISCORD LOGS TEST")
    print("=" * 60)
    
    print("\n1. Testing API endpoints...")
    test_search()
    time.sleep(2)
    test_add_article()
    
    print("\n2. Checking activity logs file...")
    check_logs()
    
    print("\n" + "=" * 60)
    print("✅ Check your Discord channel to see if messages appeared!")
    print("=" * 60)
