#!/usr/bin/env python3
"""
Test different authentication formats for Hedra API
"""

import os
import requests
from dotenv import load_dotenv

def test_auth_formats():
    """Test different authentication header formats"""
    
    load_dotenv()
    api_key = os.getenv("HEDRA_API_KEY")
    
    if not api_key:
        print("❌ No API key found")
        return
    
    print(f"🔑 Testing API Key: {api_key[:20]}...")
    
    base_url = "https://mercury.dev.dream-ai.com/api"
    
    # Test different authentication formats
    auth_formats = [
        {"X-API-KEY": api_key},
        {"x-api-key": api_key},
        {"API-KEY": api_key},
        {"api-key": api_key},
        {"Authorization": f"Bearer {api_key}"},
        {"Authorization": f"Token {api_key}"},
        {"Authorization": api_key},
    ]
    
    test_payload = {
        "aspectRatio": "16:9",
        "avatarImage": "6354fa44-f103-4430-9c9a-a98263357736",
        "audioInput": {
            "text": "Test",
            "voiceId": "tara"
        }
    }
    
    for i, auth_headers in enumerate(auth_formats):
        print(f"\n🔐 Test {i+1}: {list(auth_headers.keys())[0]} = {list(auth_headers.values())[0][:30]}...")
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            **auth_headers
        }
        
        try:
            url = f"{base_url}/v1/characters"
            response = requests.post(url, json=test_payload, headers=headers, timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200 or response.status_code == 201:
                print(f"   ✅ SUCCESS! This authentication format works!")
                result = response.json()
                print(f"   Response: {result}")
                return True
            elif response.status_code == 403:
                try:
                    error_detail = response.json()
                    print(f"   ❌ 403 Forbidden: {error_detail}")
                except:
                    print(f"   ❌ 403 Forbidden: {response.text}")
            elif response.status_code == 401:
                try:
                    error_detail = response.json()
                    print(f"   ❌ 401 Unauthorized: {error_detail}")
                except:
                    print(f"   ❌ 401 Unauthorized: {response.text}")
            else:
                try:
                    error_detail = response.json()
                    print(f"   ⚠️ {response.status_code}: {error_detail}")
                except:
                    print(f"   ⚠️ {response.status_code}: {response.text}")
                        
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout")
        except requests.exceptions.ConnectionError:
            print(f"   🔌 Connection Error")
        except Exception as e:
            print(f"   💥 Error: {str(e)}")
    
    print(f"\n❌ No working authentication format found")
    
    # Also test if the API key itself might be the issue
    print(f"\n🔍 API Key Analysis:")
    print(f"   Length: {len(api_key)} characters")
    print(f"   Starts with: {api_key[:10]}")
    print(f"   Contains spaces: {'Yes' if ' ' in api_key else 'No'}")
    print(f"   Contains newlines: {'Yes' if '\\n' in api_key else 'No'}")
    
    return False

if __name__ == "__main__":
    test_auth_formats()
