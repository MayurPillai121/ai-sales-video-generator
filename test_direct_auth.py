#!/usr/bin/env python3
"""
Direct test of Synthesia API with exact authentication formats
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_direct_auth():
    api_key = "30b81de224c745457d4f561ff623abab"  # Direct API key for testing
    
    print("🧪 Direct Synthesia API Authentication Test")
    print("=" * 60)
    
    # Test different base URLs and authentication combinations
    test_configs = [
        # Standard v2 API with Bearer
        {
            "url": "https://api.synthesia.io/v2/avatars",
            "headers": {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        },
        # Standard v2 API with X-API-KEY
        {
            "url": "https://api.synthesia.io/v2/avatars", 
            "headers": {
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            }
        },
        # Try v1 API
        {
            "url": "https://api.synthesia.io/v1/avatars",
            "headers": {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        },
        # Try without version
        {
            "url": "https://api.synthesia.io/avatars",
            "headers": {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        },
        # Try different endpoint structure
        {
            "url": "https://api.synthesia.io/v2/avatar",
            "headers": {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        },
        # Try with different content type
        {
            "url": "https://api.synthesia.io/v2/avatars",
            "headers": {
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json"
            }
        }
    ]
    
    for i, config in enumerate(test_configs, 1):
        print(f"\n{i}. Testing: {config['url']}")
        print(f"   Headers: {config['headers']}")
        
        try:
            response = requests.get(
                config['url'],
                headers=config['headers'],
                timeout=10
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ SUCCESS!")
                try:
                    data = response.json()
                    print(f"   Response: {str(data)[:200]}...")
                    return config
                except:
                    print(f"   Response text: {response.text[:200]}...")
                    return config
                    
            elif response.status_code == 401:
                print(f"   ❌ Unauthorized")
            elif response.status_code == 403:
                print(f"   ❌ Forbidden")
            elif response.status_code == 404:
                print(f"   ❌ Not Found")
            else:
                print(f"   ❌ HTTP {response.status_code}")
                print(f"   Response: {response.text[:100]}...")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error: {str(e)}")
    
    print(f"\n❌ No working configuration found")
    
    # Let's also try to check if the API is accessible at all
    print(f"\n🌐 Testing basic connectivity to api.synthesia.io...")
    try:
        response = requests.get("https://api.synthesia.io", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    return None

if __name__ == "__main__":
    result = test_direct_auth()
    
    if result:
        print(f"\n🎉 Working configuration found!")
        print(f"URL: {result['url']}")
        print(f"Headers: {result['headers']}")
    else:
        print(f"\n🔧 Possible issues:")
        print(f"1. API endpoints may have changed")
        print(f"2. API key format might be different")
        print(f"3. Account may need additional verification")
        print(f"4. Regional API differences")
        print(f"5. Synthesia API may be temporarily unavailable")
