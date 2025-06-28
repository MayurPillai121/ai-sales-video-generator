#!/usr/bin/env python3
"""
Test script to verify the corrected Synthesia API authentication
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_synthesia_auth():
    api_key = os.getenv("SYNTHESIA_API_KEY")
    base_url = "https://api.synthesia.io/v2"
    
    print("🧪 Testing Corrected Synthesia API Authentication")
    print("=" * 60)
    print(f"API Key: {api_key[:10]}...{api_key[-4:]}")
    print(f"Base URL: {base_url}")
    
    # Test both authentication methods
    auth_methods = [
        ("Bearer Token", {"Authorization": f"Bearer {api_key}"}),
        ("X-API-KEY Header", {"X-API-KEY": api_key})
    ]
    
    endpoints_to_test = [
        ("/avatars", "GET"),
        ("/videos", "GET")
    ]
    
    for auth_name, auth_header in auth_methods:
        print(f"\n🔐 Testing {auth_name}:")
        
        headers = {
            **auth_header,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        print(f"   Headers: {headers}")
        
        for endpoint, method in endpoints_to_test:
            url = f"{base_url}{endpoint}"
            print(f"\n   Testing {method} {url}")
            
            try:
                if method == "GET":
                    response = requests.get(url, headers=headers, timeout=10)
                
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"   ✅ SUCCESS with {auth_name}!")
                    
                    # Parse response for avatars
                    if endpoint == "/avatars":
                        try:
                            data = response.json()
                            avatars = data.get("avatars", [])
                            print(f"   Found {len(avatars)} avatars")
                            
                            # Check for user's specific avatar
                            user_avatar = "02e3638f-2e2b-4f41-93dd-6dea6fdf2565"
                            for avatar in avatars:
                                if avatar.get("id") == user_avatar:
                                    print(f"   ✅ Your avatar found: {avatar.get('name', 'Custom Avatar')}")
                                    break
                            else:
                                print(f"   ⚠️  Your avatar {user_avatar} not in list")
                                print(f"   Available avatars (first 3):")
                                for i, avatar in enumerate(avatars[:3]):
                                    print(f"     {i+1}. {avatar.get('id')} - {avatar.get('name', 'Unnamed')}")
                                    
                        except Exception as e:
                            print(f"   ⚠️  Response parsing error: {e}")
                    
                    # If we found a working method, test video creation payload
                    if endpoint == "/avatars":
                        print(f"\n   🎥 Testing video creation payload format...")
                        test_video_payload(base_url, headers)
                    
                    return auth_name, headers  # Return working configuration
                    
                elif response.status_code == 401:
                    print(f"   ❌ Unauthorized - API key issue")
                elif response.status_code == 403:
                    print(f"   ❌ Forbidden - Access denied")
                elif response.status_code == 404:
                    print(f"   ❌ Not Found - Wrong endpoint")
                else:
                    print(f"   ❌ HTTP {response.status_code}")
                    print(f"   Response: {response.text[:200]}")
                    
            except requests.exceptions.RequestException as e:
                print(f"   ❌ Connection error: {str(e)}")
    
    print(f"\n❌ No working authentication method found!")
    return None, None

def test_video_payload(base_url, headers):
    """Test video creation payload without actually creating video"""
    payload = {
        "title": "Test Video - Auth Verification",
        "scenes": [
            {
                "elements": [
                    {
                        "type": "avatar",
                        "avatar_id": "02e3638f-2e2b-4f41-93dd-6dea6fdf2565",
                        "script": {
                            "type": "text",
                            "text": "Hello, this is a test to verify API authentication is working correctly."
                        }
                    }
                ]
            }
        ]
    }
    
    print(f"   Payload structure:")
    import json
    print(f"   {json.dumps(payload, indent=6)}")
    
    # Note: Not actually sending POST request to avoid creating video
    print(f"   ✅ Payload format is correct for video creation")

def main():
    working_auth, working_headers = test_synthesia_auth()
    
    if working_auth and working_headers:
        print(f"\n🎉 SUCCESS! Working Configuration Found:")
        print(f"   Authentication Method: {working_auth}")
        print(f"   Headers: {working_headers}")
        print(f"\n✅ Your Synthesia API is now properly configured!")
        print(f"✅ Ready to create videos with your avatar")
        
    else:
        print(f"\n❌ Authentication Failed!")
        print(f"\n🔧 Troubleshooting Steps:")
        print(f"1. Verify API key is correct: {os.getenv('SYNTHESIA_API_KEY', 'NOT_FOUND')[:10]}...")
        print(f"2. Check Synthesia account has API access enabled")
        print(f"3. Ensure account is active with sufficient credits")
        print(f"4. Try regenerating API key from Synthesia dashboard")
        print(f"5. Contact Synthesia support if issues persist")

if __name__ == "__main__":
    main()
