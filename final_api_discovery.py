#!/usr/bin/env python3
"""
Final comprehensive API discovery for Synthesia
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def discover_synthesia_api():
    api_key = "30b81de224c745457d4f561ff623abab"
    
    print("🔍 Final Synthesia API Discovery")
    print("=" * 60)
    
    # Let's try to find ANY working endpoint
    base_domains = [
        "https://api.synthesia.io",
        "https://synthesia.io/api",
        "https://app.synthesia.io/api",
        "https://studio.synthesia.io/api"
    ]
    
    versions = ["", "/v1", "/v2", "/v3"]
    endpoints = [
        "",
        "/avatars", 
        "/videos",
        "/account",
        "/user",
        "/health",
        "/status"
    ]
    
    # Authentication methods
    auth_methods = [
        ("X-API-KEY", {"X-API-KEY": api_key}),
        ("Bearer", {"Authorization": f"Bearer {api_key}"}),
        ("Direct", {"Authorization": api_key})
    ]
    
    working_configs = []
    
    print("🌐 Scanning for working API endpoints...")
    
    for base in base_domains:
        print(f"\nTesting base: {base}")
        
        for version in versions:
            for endpoint in endpoints:
                url = f"{base}{version}{endpoint}"
                
                # Skip testing empty endpoints on base domains
                if endpoint == "" and version == "":
                    continue
                
                for auth_name, auth_header in auth_methods:
                    headers = {
                        **auth_header,
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": "SynthesiaClient/1.0"
                    }
                    
                    try:
                        response = requests.get(url, headers=headers, timeout=5)
                        status = response.status_code
                        
                        # Only report interesting responses
                        if status not in [404, 403]:
                            print(f"  {url} ({auth_name}): {status}")
                            
                            if status == 200:
                                print(f"    ✅ SUCCESS!")
                                print(f"    Response: {response.text[:100]}...")
                                working_configs.append({
                                    "url": url,
                                    "auth": auth_name,
                                    "headers": headers,
                                    "response": response.text[:200]
                                })
                            elif status == 401:
                                print(f"    🔑 Unauthorized (endpoint exists!)")
                            elif status in [400, 422]:
                                print(f"    📝 Bad Request (endpoint exists!)")
                                print(f"    Response: {response.text[:100]}...")
                            else:
                                print(f"    Response: {response.text[:100]}...")
                                
                    except requests.exceptions.Timeout:
                        continue
                    except requests.exceptions.RequestException:
                        continue
    
    print(f"\n📊 Discovery Results:")
    if working_configs:
        print(f"✅ Found {len(working_configs)} working configurations!")
        for i, config in enumerate(working_configs, 1):
            print(f"{i}. {config['url']} with {config['auth']}")
            print(f"   Response: {config['response'][:100]}...")
    else:
        print(f"❌ No working API endpoints discovered")
        
        print(f"\n🔧 This indicates:")
        print(f"1. API key might be completely invalid")
        print(f"2. Account doesn't have API access at all")
        print(f"3. Synthesia API structure has changed significantly")
        print(f"4. Regional restrictions or IP blocking")
        print(f"5. API service might be down")
        
        print(f"\n📞 Recommended actions:")
        print(f"1. Log into Synthesia dashboard and verify API key")
        print(f"2. Check if API access is enabled for your account")
        print(f"3. Look for any API documentation updates")
        print(f"4. Contact Synthesia support directly")
        print(f"5. Try creating a new API key")
    
    return working_configs

def test_manual_curl_equivalent():
    """Show equivalent curl commands for manual testing"""
    api_key = "30b81de224c745457d4f561ff623abab"
    
    print(f"\n🔧 Manual Testing Commands:")
    print(f"You can test these manually in terminal/command prompt:")
    print(f"")
    
    curl_commands = [
        f'curl -H "Authorization: Bearer {api_key}" -H "Content-Type: application/json" https://api.synthesia.io/v2/avatars',
        f'curl -H "X-API-KEY: {api_key}" -H "Content-Type: application/json" https://api.synthesia.io/v2/avatars',
        f'curl -H "Authorization: {api_key}" -H "Content-Type: application/json" https://api.synthesia.io/v2/avatars'
    ]
    
    for i, cmd in enumerate(curl_commands, 1):
        print(f"{i}. {cmd}")
    
    print(f"\nIf any of these work, we can update the Python client accordingly.")

if __name__ == "__main__":
    results = discover_synthesia_api()
    test_manual_curl_equivalent()
    
    if not results:
        print(f"\n⚠️  IMPORTANT: API Discovery Failed")
        print(f"This suggests a fundamental issue with:")
        print(f"- API key validity")
        print(f"- Account API access")
        print(f"- Synthesia API availability")
        print(f"\nPlease verify with Synthesia support before proceeding.")
