#!/usr/bin/env python3
"""
Debug script to test different Hedra API authentication methods
"""

import os
import requests
from dotenv import load_dotenv

def test_auth_methods():
    """Test different authentication approaches"""
    
    load_dotenv()
    api_key = os.getenv("HEDRA_API_KEY")
    
    if not api_key:
        print("❌ No API key found")
        return
    
    print(f"🔑 Testing API Key: {api_key[:20]}...")
    
    base_urls = [
        "https://mercury.dev.dream-ai.com/api",
        "https://mercury.dev.dream-ai.com",
        "https://api.hedra.com",
        "https://api.hedra.com/v1"
    ]
    
    auth_methods = [
        {"X-API-KEY": api_key},
        {"Authorization": f"Bearer {api_key}"},
        {"Authorization": f"Token {api_key}"},
        {"api-key": api_key},
        {"x-api-key": api_key}
    ]
    
    test_payload = {
        "aspectRatio": "16:9",
        "avatarImage": "6354fa44-f103-4430-9c9a-a98263357736",
        "audioInput": {
            "text": "Test",
            "voiceId": "tara"
        }
    }
    
    endpoints = ["/v1/characters", "/characters", "/generate", "/v1/generate"]
    
    for base_url in base_urls:
        print(f"\n🌐 Testing Base URL: {base_url}")
        
        for auth_method in auth_methods:
            print(f"  🔐 Auth: {list(auth_method.keys())[0]}")
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                **auth_method
            }
            
            for endpoint in endpoints:
                try:
                    url = f"{base_url}{endpoint}"
                    print(f"    📡 POST {endpoint}...", end=" ")
                    
                    response = requests.post(url, json=test_payload, headers=headers, timeout=10)
                    
                    if response.status_code == 200 or response.status_code == 201:
                        print(f"✅ SUCCESS ({response.status_code})")
                        result = response.json()
                        print(f"        Response: {result}")
                        return True
                    elif response.status_code == 403:
                        print(f"❌ 403 Forbidden")
                    elif response.status_code == 401:
                        print(f"❌ 401 Unauthorized")
                    elif response.status_code == 404:
                        print(f"⚠️ 404 Not Found")
                    else:
                        print(f"⚠️ {response.status_code}")
                        
                except requests.exceptions.Timeout:
                    print(f"⏰ Timeout")
                except requests.exceptions.ConnectionError:
                    print(f"🔌 Connection Error")
                except Exception as e:
                    print(f"💥 Error: {str(e)}")
    
    print(f"\n❌ No working authentication method found")
    return False

if __name__ == "__main__":
    test_auth_methods()
