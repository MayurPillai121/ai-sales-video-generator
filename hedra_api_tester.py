#!/usr/bin/env python3
"""
Comprehensive Hedra API Tester - Tests multiple endpoints and configurations
"""

import os
import requests
import time
from dotenv import load_dotenv

def test_api_endpoint(base_url, headers, endpoint="/v1/voices", timeout=10):
    """Test a specific API endpoint"""
    try:
        print(f"Testing: {base_url}{endpoint}")
        print(f"Headers: {headers}")
        
        response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=timeout)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.text
            
    except requests.exceptions.Timeout:
        print(f"❌ TIMEOUT: Request timed out after {timeout} seconds")
        return False, "Timeout"
    except requests.exceptions.ConnectionError as e:
        print(f"❌ CONNECTION ERROR: {str(e)}")
        return False, "Connection Error"
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False, str(e)

def main():
    print("🔍 COMPREHENSIVE HEDRA API TESTER")
    print("=" * 50)
    
    # Load API key
    load_dotenv()
    api_key = os.getenv("HEDRA_API_KEY")
    
    if not api_key:
        print("❌ No HEDRA_API_KEY found in environment")
        return
    
    print(f"✅ API Key loaded: {api_key[:20]}...")
    print()
    
    # Test configurations
    test_configs = [
        {
            "name": "Mercury API (Official OpenAPI Spec)",
            "base_url": "https://mercury.dev.dream-ai.com/api",
            "headers": {
                "X-API-Key": api_key,
                "Content-Type": "application/json"
            }
        },
        {
            "name": "Mercury API (Alternative Header)",
            "base_url": "https://mercury.dev.dream-ai.com/api", 
            "headers": {
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            }
        },
        {
            "name": "Hedra API (Web App Public)",
            "base_url": "https://api.hedra.com/web-app/public",
            "headers": {
                "x-api-key": api_key,
                "Content-Type": "application/json"
            }
        },
        {
            "name": "Hedra API (Direct)",
            "base_url": "https://api.hedra.com",
            "headers": {
                "X-API-Key": api_key,
                "Content-Type": "application/json"
            }
        }
    ]
    
    # Test each configuration
    for i, config in enumerate(test_configs, 1):
        print(f"\n🧪 TEST {i}: {config['name']}")
        print("-" * 40)
        
        # Test voices endpoint
        success, result = test_api_endpoint(
            config["base_url"], 
            config["headers"], 
            "/v1/voices",
            timeout=15
        )
        
        if success:
            print("✅ SUCCESS! This configuration works!")
            print(f"Found {len(result.get('supported_voices', []))} voices")
            break
        else:
            print(f"❌ Failed: {result}")
            
        print()
    
    # Additional diagnostic tests
    print("\n🔧 DIAGNOSTIC TESTS")
    print("-" * 30)
    
    # Test basic connectivity
    try:
        print("Testing basic connectivity to mercury.dev.dream-ai.com...")
        response = requests.get("https://mercury.dev.dream-ai.com", timeout=10)
        print(f"✅ Basic connectivity: {response.status_code}")
    except Exception as e:
        print(f"❌ Basic connectivity failed: {e}")
    
    # Test ping endpoints
    for base_url in ["https://mercury.dev.dream-ai.com/api", "https://api.hedra.com"]:
        try:
            print(f"Testing ping endpoint: {base_url}/ping")
            response = requests.get(f"{base_url}/ping", timeout=10)
            print(f"✅ Ping {base_url}: {response.status_code}")
        except Exception as e:
            print(f"❌ Ping {base_url} failed: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 TESTING COMPLETE")
    print("\nIf all tests failed, possible issues:")
    print("1. API key may not be activated for API access")
    print("2. Account may need to be upgraded to paid plan")
    print("3. API key may be for web app only, not API")
    print("4. Network connectivity issues")
    print("5. API endpoints may have changed")
    print("\n💡 Contact Hedra support if issues persist")

if __name__ == "__main__":
    main()
