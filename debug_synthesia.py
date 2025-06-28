#!/usr/bin/env python3
"""
Debug Synthesia API - comprehensive endpoint and auth testing
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def debug_synthesia_api():
    api_key = "30b81de224c745457d4f561ff623abab"
    
    print("🔍 Debugging Synthesia API - Comprehensive Test")
    print("=" * 70)
    
    # First, let's check what the base domain returns
    print("1. Testing base domain accessibility...")
    try:
        response = requests.get("https://api.synthesia.io", timeout=10)
        print(f"   https://api.synthesia.io -> Status: {response.status_code}")
        if response.text:
            print(f"   Response: {response.text[:300]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test different API versions and endpoints
    print(f"\n2. Testing different API endpoints...")
    
    endpoints_to_test = [
        # Different versions
        "https://api.synthesia.io/v2/avatars",
        "https://api.synthesia.io/v1/avatars", 
        "https://api.synthesia.io/avatars",
        
        # Different endpoint names
        "https://api.synthesia.io/v2/avatar",
        "https://api.synthesia.io/v2/actors",
        "https://api.synthesia.io/v2/presenters",
        
        # Videos endpoint
        "https://api.synthesia.io/v2/videos",
        "https://api.synthesia.io/v2/video",
        
        # Account/user endpoints
        "https://api.synthesia.io/v2/account",
        "https://api.synthesia.io/v2/user",
        "https://api.synthesia.io/v2/me",
        
        # Health/status endpoints
        "https://api.synthesia.io/v2/health",
        "https://api.synthesia.io/v2/status",
        "https://api.synthesia.io/health",
        "https://api.synthesia.io/status"
    ]
    
    # Different authentication methods
    auth_methods = [
        ("Bearer Token", {"Authorization": f"Bearer {api_key}"}),
        ("X-API-KEY", {"X-API-KEY": api_key}),
        ("Direct Auth", {"Authorization": api_key}),
        ("API-Key", {"API-Key": api_key}),
        ("x-api-key (lowercase)", {"x-api-key": api_key})
    ]
    
    working_configs = []
    
    for endpoint in endpoints_to_test:
        print(f"\n   Testing endpoint: {endpoint}")
        
        for auth_name, auth_header in auth_methods:
            headers = {
                **auth_header,
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "AI-Sales-Video-Generator/1.0"
            }
            
            try:
                response = requests.get(endpoint, headers=headers, timeout=5)
                status = response.status_code
                
                if status == 200:
                    print(f"     ✅ SUCCESS with {auth_name}!")
                    print(f"        Response: {response.text[:100]}...")
                    working_configs.append({
                        "endpoint": endpoint,
                        "auth": auth_name,
                        "headers": headers,
                        "response": response.text[:200]
                    })
                elif status == 401:
                    print(f"     🔑 {auth_name}: Unauthorized")
                elif status == 403:
                    print(f"     🚫 {auth_name}: Forbidden")
                elif status == 404:
                    print(f"     ❌ {auth_name}: Not Found")
                elif status == 429:
                    print(f"     ⏰ {auth_name}: Rate Limited")
                else:
                    print(f"     ⚠️  {auth_name}: HTTP {status}")
                    if status not in [404, 401, 403]:
                        print(f"        Response: {response.text[:100]}...")
                        
            except requests.exceptions.Timeout:
                print(f"     ⏰ {auth_name}: Timeout")
            except requests.exceptions.RequestException as e:
                print(f"     ❌ {auth_name}: {str(e)[:50]}...")
    
    print(f"\n3. Summary:")
    if working_configs:
        print(f"   ✅ Found {len(working_configs)} working configurations!")
        for config in working_configs:
            print(f"   - {config['endpoint']} with {config['auth']}")
    else:
        print(f"   ❌ No working configurations found")
        
        print(f"\n🔧 Debugging suggestions:")
        print(f"   1. API key might be incorrect or expired")
        print(f"   2. Account might not have API access enabled")
        print(f"   3. Synthesia API structure might have changed")
        print(f"   4. Regional restrictions or IP blocking")
        print(f"   5. API might be in maintenance mode")
        
        print(f"\n📞 Next steps:")
        print(f"   1. Verify API key in Synthesia dashboard")
        print(f"   2. Check account status and API permissions")
        print(f"   3. Try regenerating the API key")
        print(f"   4. Contact Synthesia support with these test results")
    
    return working_configs

if __name__ == "__main__":
    results = debug_synthesia_api()
    
    if results:
        print(f"\n🎉 Ready to update synthesia_client.py with working configuration!")
        best_config = results[0]
        print(f"Best configuration:")
        print(f"  Endpoint: {best_config['endpoint']}")
        print(f"  Auth: {best_config['auth']}")
        print(f"  Headers: {best_config['headers']}")
    else:
        print(f"\n❌ Unable to establish API connection")
        print(f"Manual verification needed with Synthesia support")
