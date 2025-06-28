#!/usr/bin/env python3
"""
Validate Hedra API key with different approaches
"""

import requests
import json

def validate_api_key():
    """Test API key validation"""
    
    api_key = "sk_hedra_oFeYm70KluaFM0OXKlcjyLqip2QwyE4wjQ5s4o6YcLnSTwJ7s0NG-ej0sq8iSqxf"
    
    print(f"🔑 Validating API Key: {api_key[:30]}...")
    print(f"   Full length: {len(api_key)} characters")
    
    # Test different header formats
    header_formats = [
        {"x-api-key": api_key},
        {"X-API-KEY": api_key},
        {"Authorization": f"Bearer {api_key}"},
        {"api-key": api_key}
    ]
    
    base_urls = [
        "https://api.hedra.com/web-app/public",
        "https://api.hedra.com",
        "https://api.hedra.com/v1"
    ]
    
    # Test simple endpoints that might validate the key
    test_endpoints = [
        "/me",
        "/user",
        "/account", 
        "/profile",
        "/assets",
        "/generations",
        ""
    ]
    
    for base_url in base_urls:
        print(f"\n🌐 Testing base URL: {base_url}")
        
        for header_format in header_formats:
            header_name = list(header_format.keys())[0]
            print(f"  🔐 Header format: {header_name}")
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                **header_format
            }
            
            for endpoint in test_endpoints:
                try:
                    url = f"{base_url}{endpoint}"
                    response = requests.get(url, headers=headers, timeout=5)
                    
                    if response.status_code == 200:
                        print(f"    ✅ GET {endpoint}: SUCCESS!")
                        try:
                            result = response.json()
                            print(f"        Response: {json.dumps(result, indent=2)[:200]}...")
                        except:
                            print(f"        Response: {response.text[:100]}...")
                        return True
                    elif response.status_code == 401:
                        print(f"    ❌ GET {endpoint}: 401 Unauthorized")
                    elif response.status_code == 403:
                        print(f"    ❌ GET {endpoint}: 403 Forbidden")
                    elif response.status_code == 404:
                        print(f"    ⚠️ GET {endpoint}: 404 Not Found")
                    else:
                        print(f"    ⚠️ GET {endpoint}: {response.status_code}")
                        if response.status_code != 404:
                            try:
                                error = response.json()
                                print(f"        Error: {error}")
                            except:
                                print(f"        Text: {response.text[:100]}")
                        
                except Exception as e:
                    print(f"    💥 GET {endpoint}: {str(e)}")
    
    print(f"\n❌ No valid endpoint found for API key validation")
    return False

if __name__ == "__main__":
    validate_api_key()
