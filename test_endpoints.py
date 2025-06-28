#!/usr/bin/env python3
"""
Test different Hedra API endpoints to find the correct one
"""

import requests
import json

def test_endpoints():
    """Test various endpoint combinations"""
    
    api_key = "sk_hedra_oFeYm70KluaFM0OXKlcjyLqip2QwyE4wjQ5s4o6YcLnSTwJ7s0NG-ej0sq8iSqxf"
    
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    base_url = "https://api.hedra.com"
    
    # Test different endpoints
    endpoints_to_test = [
        "/v1/characters",
        "/v1/generate", 
        "/v1/videos",
        "/v1/projects",
        "/characters",
        "/generate",
        "/videos",
        "/projects",
        "/api/v1/characters",
        "/api/v1/generate"
    ]
    
    test_payload = {
        "aspectRatio": "16:9",
        "audioInput": {
            "text": "Test",
            "voiceId": "tara"
        }
    }
    
    print("🔍 Testing Hedra API Endpoints...")
    print("=" * 60)
    
    for endpoint in endpoints_to_test:
        full_url = f"{base_url}{endpoint}"
        
        try:
            # Test POST
            response = requests.post(full_url, json=test_payload, headers=headers, timeout=10)
            
            if response.status_code != 404:
                print(f"✅ POST {endpoint}: {response.status_code}")
                try:
                    result = response.json()
                    print(f"   Response: {json.dumps(result, indent=2)[:300]}...")
                except:
                    print(f"   Response: {response.text[:200]}...")
            else:
                print(f"❌ POST {endpoint}: 404 Not Found")
                
        except Exception as e:
            print(f"💥 POST {endpoint}: {str(e)}")
    
    # Test GET on base endpoints
    print(f"\n🔍 Testing GET endpoints...")
    get_endpoints = [
        "/",
        "/v1",
        "/api",
        "/api/v1",
        "/health",
        "/status"
    ]
    
    for endpoint in get_endpoints:
        full_url = f"{base_url}{endpoint}"
        
        try:
            response = requests.get(full_url, headers=headers, timeout=5)
            
            if response.status_code != 404:
                print(f"✅ GET {endpoint}: {response.status_code}")
                try:
                    result = response.json()
                    print(f"   Response: {json.dumps(result, indent=2)[:200]}...")
                except:
                    print(f"   Response: {response.text[:100]}...")
            else:
                print(f"❌ GET {endpoint}: 404")
                
        except Exception as e:
            print(f"💥 GET {endpoint}: {str(e)}")

if __name__ == "__main__":
    test_endpoints()
