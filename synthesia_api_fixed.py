#!/usr/bin/env python3
"""
Fixed Synthesia API client based on official documentation
"""
import os
import requests
import time
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class SynthesiaAPIFixed:
    """
    Fixed Synthesia API client with correct endpoints and authentication
    """
    
    def __init__(self):
        self.api_key = os.getenv("SYNTHESIA_API_KEY")
        # Based on Synthesia documentation, the correct base URL is:
        self.base_url = "https://api.synthesia.io/v2"
        
        # Correct authentication header format
        self.headers = {
            "Authorization": self.api_key,  # Direct API key without Bearer
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def test_api_access(self):
        """Test API access with different methods"""
        print("🔧 Testing Synthesia API Access...")
        
        # Test different authentication formats
        auth_formats = [
            ("Direct API Key", {"Authorization": self.api_key}),
            ("Bearer Token", {"Authorization": f"Bearer {self.api_key}"}),
            ("X-API-Key Header", {"X-API-Key": self.api_key}),
        ]
        
        # Test different endpoints
        endpoints = [
            "/avatars",
            "/videos", 
            "/templates",
            "/account"
        ]
        
        for auth_name, auth_header in auth_formats:
            print(f"\nTesting {auth_name}:")
            headers = {
                **auth_header,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            for endpoint in endpoints:
                try:
                    url = f"{self.base_url}{endpoint}"
                    print(f"  Trying: {url}")
                    
                    response = requests.get(url, headers=headers, timeout=10)
                    
                    print(f"    Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        print(f"    ✅ SUCCESS with {auth_name} on {endpoint}")
                        self.headers = headers  # Save working headers
                        return {"success": True, "auth": auth_name, "endpoint": endpoint}
                    elif response.status_code == 401:
                        print(f"    ❌ Unauthorized")
                    elif response.status_code == 403:
                        print(f"    ❌ Forbidden")
                    elif response.status_code == 404:
                        print(f"    ❌ Not Found")
                    else:
                        print(f"    ❌ HTTP {response.status_code}")
                        
                except requests.exceptions.RequestException as e:
                    print(f"    ❌ Connection error: {str(e)}")
        
        return {"success": False, "error": "No working authentication method found"}
    
    def get_account_info(self):
        """Get account information to verify API access"""
        try:
            response = requests.get(
                f"{self.base_url}/account",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {
                    "success": False, 
                    "status_code": response.status_code,
                    "error": response.text
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_simple_video(self, script: str, avatar_id: str):
        """Create a video with minimal required parameters"""
        payload = {
            "title": "Test Video",
            "scenes": [
                {
                    "elements": [
                        {
                            "type": "avatar",
                            "avatar_id": avatar_id,
                            "script": {
                                "type": "text",
                                "text": script
                            }
                        }
                    ]
                }
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/videos",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            return {
                "success": response.status_code == 201,
                "status_code": response.status_code,
                "response": response.text,
                "data": response.json() if response.status_code == 201 else None
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

def main():
    print("🧪 Synthesia API Fixed Test")
    print("=" * 60)
    
    api = SynthesiaAPIFixed()
    
    # Test 1: API Access
    access_result = api.test_api_access()
    
    if access_result.get("success"):
        print(f"\n✅ API Access Working!")
        print(f"   Authentication: {access_result.get('auth')}")
        print(f"   Working Endpoint: {access_result.get('endpoint')}")
        
        # Test 2: Account Info
        print(f"\n📋 Getting Account Info...")
        account_result = api.get_account_info()
        
        if account_result.get("success"):
            account_data = account_result.get("data", {})
            print(f"✅ Account verified!")
            print(f"   Plan: {account_data.get('plan', 'Unknown')}")
            print(f"   Credits: {account_data.get('credits', 'Unknown')}")
        else:
            print(f"❌ Account info failed: {account_result.get('error')}")
        
        # Test 3: Video Creation (optional)
        print(f"\n🎥 Testing Video Creation...")
        print("This will create an actual video and may use credits.")
        
        # For safety, we'll just show what would be sent
        print("Payload that would be sent:")
        test_payload = {
            "title": "Test Video",
            "scenes": [
                {
                    "elements": [
                        {
                            "type": "avatar",
                            "avatar_id": "02e3638f-2e2b-4f41-93dd-6dea6fdf2565",
                            "script": {
                                "type": "text",
                                "text": "Hello, this is a test video."
                            }
                        }
                    ]
                }
            ]
        }
        print(f"   {test_payload}")
        
    else:
        print(f"\n❌ API Access Failed!")
        print(f"   Error: {access_result.get('error')}")
        
        print(f"\n🔧 Troubleshooting:")
        print(f"1. Check if your API key is correct: {api.api_key[:10]}...{api.api_key[-4:]}")
        print(f"2. Verify your Synthesia account has API access")
        print(f"3. Check if your account is active and in good standing")
        print(f"4. Try regenerating your API key from Synthesia dashboard")

if __name__ == "__main__":
    main()
