#!/usr/bin/env python3
"""
Test authentication on base Synthesia API endpoint
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_base_auth():
    api_key = "30b81de224c745457d4f561ff623abab"
    
    print("🔍 Testing Base Synthesia API Authentication")
    print("=" * 60)
    
    # Test authentication on base endpoint first
    base_urls = [
        "https://api.synthesia.io",
        "https://api.synthesia.io/v2",
        "https://api.synthesia.io/v1"
    ]
    
    auth_methods = [
        ("Bearer Token", {"Authorization": f"Bearer {api_key}"}),
        ("X-API-KEY", {"X-API-KEY": api_key})
    ]
    
    for base_url in base_urls:
        print(f"\n🌐 Testing base URL: {base_url}")
        
        for auth_name, auth_header in auth_methods:
            headers = {
                **auth_header,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            try:
                response = requests.get(base_url, headers=headers, timeout=10)
                print(f"   {auth_name}: Status {response.status_code}")
                
                if response.status_code == 200:
                    print(f"   ✅ SUCCESS! Response: {response.text[:200]}...")
                elif response.status_code == 403:
                    print(f"   🔑 Forbidden: {response.text[:100]}...")
                elif response.status_code == 401:
                    print(f"   🔑 Unauthorized: {response.text[:100]}...")
                else:
                    print(f"   📄 Response: {response.text[:100]}...")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
    
    # Now test specific endpoints that might exist
    print(f"\n🎯 Testing specific endpoints with authentication...")
    
    # Common API endpoints for video generation services
    endpoints = [
        "/avatars",
        "/videos", 
        "/templates",
        "/voices",
        "/account",
        "/user",
        "/projects",
        "/generations"
    ]
    
    working_endpoints = []
    
    for endpoint in endpoints:
        full_url = f"https://api.synthesia.io/v2{endpoint}"
        print(f"\n   Testing: {full_url}")
        
        # Try Bearer token first (most common)
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            response = requests.get(full_url, headers=headers, timeout=10)
            status = response.status_code
            
            print(f"     Status: {status}")
            
            if status == 200:
                print(f"     ✅ SUCCESS!")
                print(f"     Response: {response.text[:150]}...")
                working_endpoints.append(endpoint)
            elif status == 401:
                print(f"     🔑 Unauthorized - try X-API-KEY")
                
                # Try X-API-KEY method
                headers_alt = {
                    "X-API-KEY": api_key,
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
                
                response_alt = requests.get(full_url, headers=headers_alt, timeout=10)
                if response_alt.status_code == 200:
                    print(f"     ✅ SUCCESS with X-API-KEY!")
                    print(f"     Response: {response_alt.text[:150]}...")
                    working_endpoints.append(f"{endpoint} (X-API-KEY)")
                else:
                    print(f"     ❌ X-API-KEY also failed: {response_alt.status_code}")
                    
            elif status == 403:
                print(f"     🚫 Forbidden: {response.text[:100]}...")
            elif status == 404:
                print(f"     ❌ Not Found")
            else:
                print(f"     ⚠️  HTTP {status}: {response.text[:100]}...")
                
        except Exception as e:
            print(f"     ❌ Error: {str(e)}")
    
    print(f"\n📊 Results Summary:")
    if working_endpoints:
        print(f"   ✅ Working endpoints found:")
        for endpoint in working_endpoints:
            print(f"     - {endpoint}")
    else:
        print(f"   ❌ No working endpoints found")
        print(f"   🔧 This suggests:")
        print(f"     1. API key might be invalid or expired")
        print(f"     2. Account doesn't have API access")
        print(f"     3. Different authentication method needed")
        print(f"     4. API structure has changed significantly")

if __name__ == "__main__":
    test_base_auth()
