#!/usr/bin/env python3
"""
Find correct Hedra API endpoints
"""

import requests
import json

def test_hedra_endpoints():
    """Test various endpoint combinations"""
    
    api_key = "sk_hedra_oFeYm70KluaFM0OXKlcjyLqip2QwyE4wjQ5s4o6YcLnSTwJ7s0NG-ej0sq8iSqxf"
    
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    base_urls = [
        "https://api.hedra.com",
        "https://api.hedra.com/v1",
        "https://api.hedra.com/api",
        "https://api.hedra.com/api/v1"
    ]
    
    endpoints = [
        "",
        "/",
        "/characters",
        "/v1/characters", 
        "/generate",
        "/v1/generate",
        "/projects",
        "/v1/projects",
        "/health",
        "/status"
    ]
    
    test_payload = {
        "aspectRatio": "16:9",
        "avatarImage": "6354fa44-f103-4430-9c9a-a98263357736",
        "audioInput": {
            "text": "Test",
            "voiceId": "tara"
        }
    }
    
    print("🔍 Testing Hedra API Endpoints...")
    print("=" * 60)
    
    for base_url in base_urls:
        print(f"\n🌐 Base URL: {base_url}")
        
        for endpoint in endpoints:
            full_url = f"{base_url}{endpoint}"
            
            # Test GET first
            try:
                response = requests.get(full_url, headers=headers, timeout=5)
                if response.status_code != 404:
                    print(f"  ✅ GET {endpoint}: {response.status_code}")
                    if response.status_code == 200:
                        try:
                            result = response.json()
                            print(f"      Response: {json.dumps(result, indent=2)[:200]}...")
                        except:
                            print(f"      Response: {response.text[:100]}...")
                else:
                    print(f"  ❌ GET {endpoint}: 404")
            except Exception as e:
                print(f"  💥 GET {endpoint}: {str(e)}")
            
            # Test POST for generation endpoints
            if "characters" in endpoint or "generate" in endpoint:
                try:
                    response = requests.post(full_url, json=test_payload, headers=headers, timeout=5)
                    if response.status_code != 404:
                        print(f"  ✅ POST {endpoint}: {response.status_code}")
                        if response.status_code in [200, 201]:
                            try:
                                result = response.json()
                                print(f"      Response: {json.dumps(result, indent=2)[:200]}...")
                            except:
                                print(f"      Response: {response.text[:100]}...")
                        elif response.status_code == 422:
                            print(f"      422 - Validation Error (endpoint exists!)")
                    else:
                        print(f"  ❌ POST {endpoint}: 404")
                except Exception as e:
                    print(f"  💥 POST {endpoint}: {str(e)}")

if __name__ == "__main__":
    test_hedra_endpoints()
