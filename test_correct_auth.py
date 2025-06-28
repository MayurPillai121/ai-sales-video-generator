#!/usr/bin/env python3
"""
Test correct Synthesia API authentication format
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_correct_auth():
    api_key = "30b81de224c745457d4f561ff623abab"
    
    print("🔍 Testing Correct Synthesia API Authentication Format")
    print("=" * 70)
    
    # Based on the error message about "missing equal-sign", 
    # Synthesia might expect a different auth format
    auth_formats = [
        # Standard Bearer token
        ("Bearer Token", {"Authorization": f"Bearer {api_key}"}),
        
        # API Key with equals sign format
        ("API Key=Value", {"Authorization": f"api_key={api_key}"}),
        ("Token=Value", {"Authorization": f"token={api_key}"}),
        ("Key=Value", {"Authorization": f"key={api_key}"}),
        
        # X-API-KEY header
        ("X-API-KEY", {"X-API-KEY": api_key}),
        
        # Basic auth format
        ("Basic Auth", {"Authorization": f"Basic {api_key}"}),
        
        # Custom formats
        ("Direct Key", {"Authorization": api_key}),
        ("API-Key Header", {"API-Key": api_key}),
    ]
    
    test_url = "https://api.synthesia.io/v2/avatars"
    
    print(f"Testing endpoint: {test_url}")
    
    for auth_name, auth_header in auth_formats:
        print(f"\n🔐 Testing {auth_name}:")
        print(f"   Header: {auth_header}")
        
        headers = {
            **auth_header,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            response = requests.get(test_url, headers=headers, timeout=10)
            status = response.status_code
            
            print(f"   Status: {status}")
            
            if status == 200:
                print(f"   ✅ SUCCESS!")
                try:
                    data = response.json()
                    avatars = data.get("avatars", [])
                    print(f"   Found {len(avatars)} avatars")
                    
                    # Check for user's avatar
                    user_avatar = "02e3638f-2e2b-4f41-93dd-6dea6fdf2565"
                    for avatar in avatars:
                        if avatar.get("id") == user_avatar:
                            print(f"   ✅ Your avatar found: {avatar.get('name', 'Custom')}")
                            break
                    
                    print(f"   🎉 WORKING CONFIGURATION FOUND!")
                    return auth_name, headers
                    
                except Exception as e:
                    print(f"   Response parsing error: {e}")
                    print(f"   Raw response: {response.text[:200]}...")
                    
            elif status == 401:
                print(f"   🔑 Unauthorized")
            elif status == 403:
                print(f"   🚫 Forbidden: {response.text[:100]}...")
            elif status == 404:
                print(f"   ❌ Not Found")
            else:
                print(f"   ⚠️  HTTP {status}")
                print(f"   Response: {response.text[:150]}...")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print(f"\n❌ No working authentication format found")
    return None, None

def test_video_creation(auth_name, headers):
    """Test video creation with working auth"""
    print(f"\n🎥 Testing Video Creation with {auth_name}...")
    
    payload = {
        "title": "Test Video - Authentication Success",
        "scenes": [
            {
                "elements": [
                    {
                        "type": "avatar",
                        "avatar_id": "02e3638f-2e2b-4f41-93dd-6dea6fdf2565",
                        "script": {
                            "type": "text",
                            "text": "Hello! This test confirms that the Synthesia API authentication is working correctly."
                        }
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(
            "https://api.synthesia.io/v2/videos",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print(f"   ✅ Video creation successful!")
            data = response.json()
            video_id = data.get("id")
            print(f"   Video ID: {video_id}")
            return True
        else:
            print(f"   ❌ Video creation failed")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def main():
    auth_name, headers = test_correct_auth()
    
    if auth_name and headers:
        print(f"\n🎉 SUCCESS! Working Authentication Found:")
        print(f"   Method: {auth_name}")
        print(f"   Headers: {headers}")
        
        # Test video creation (optional)
        print(f"\n⚠️  Would you like to test video creation?")
        print(f"   This will create an actual video and may use API credits.")
        print(f"   Skipping for now - you can test manually.")
        
        print(f"\n✅ Ready to update synthesia_client.py!")
        
    else:
        print(f"\n❌ Authentication still failing")
        print(f"\n🔧 Final troubleshooting steps:")
        print(f"1. Verify API key is exactly: {api_key}")
        print(f"2. Check Synthesia account dashboard for API status")
        print(f"3. Ensure account has active API access")
        print(f"4. Try regenerating the API key")
        print(f"5. Contact Synthesia support with these test results")

if __name__ == "__main__":
    main()
