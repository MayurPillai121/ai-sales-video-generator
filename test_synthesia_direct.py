#!/usr/bin/env python3
"""
Direct Synthesia API test with correct endpoints
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_synthesia_direct():
    api_key = os.getenv("SYNTHESIA_API_KEY")
    
    print("🧪 Direct Synthesia API Test")
    print("=" * 50)
    print(f"API Key: {api_key[:10]}...{api_key[-4:]}")
    
    # Correct Synthesia API endpoints and format
    base_urls = [
        "https://api.synthesia.io/v2",
        "https://api.synthesia.io/v1",
        "https://api.synthesia.io"
    ]
    
    headers = {
        "Authorization": api_key,  # Direct API key (most common for Synthesia)
        "Content-Type": "application/json"
    }
    
    for base_url in base_urls:
        print(f"\nTesting base URL: {base_url}")
        
        # Test avatars endpoint
        try:
            response = requests.get(
                f"{base_url}/avatars",
                headers=headers,
                timeout=10
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Success!")
                data = response.json()
                avatars = data.get("avatars", [])
                print(f"Found {len(avatars)} avatars")
                
                # Check for user's avatar
                user_avatar = "02e3638f-2e2b-4f41-93dd-6dea6fdf2565"
                for avatar in avatars:
                    if avatar.get("id") == user_avatar:
                        print(f"✅ Your avatar found: {avatar.get('name', 'Custom Avatar')}")
                        break
                else:
                    print(f"⚠️  Avatar {user_avatar} not found")
                    print("Available avatars:")
                    for i, avatar in enumerate(avatars[:3]):
                        print(f"  {avatar.get('id')} - {avatar.get('name', 'Unnamed')}")
                
                return base_url, headers
                
            elif response.status_code == 401:
                print("❌ Unauthorized - Check API key")
            elif response.status_code == 403:
                print("❌ Forbidden - Check API permissions")
            elif response.status_code == 404:
                print("❌ Not Found - Wrong endpoint")
            else:
                print(f"❌ HTTP {response.status_code}")
                print(f"Response: {response.text[:200]}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {str(e)}")
    
    print("\n❌ No working endpoint found")
    return None, None

def test_video_creation(base_url, headers):
    """Test video creation with minimal payload"""
    print(f"\n🎥 Testing Video Creation...")
    
    payload = {
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
    
    try:
        response = requests.post(
            f"{base_url}/videos",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Video creation successful!")
            data = response.json()
            return data.get("id")
        else:
            print("❌ Video creation failed")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    base_url, headers = test_synthesia_direct()
    
    if base_url and headers:
        print(f"\n✅ Working configuration found!")
        print(f"Base URL: {base_url}")
        print(f"Headers: {headers}")
        
        # Optionally test video creation (commented out to avoid charges)
        # test_video_creation(base_url, headers)
    else:
        print("\n🔧 Troubleshooting Tips:")
        print("1. Verify your API key is correct")
        print("2. Check your Synthesia account has API access")
        print("3. Ensure your account is active")
        print("4. Try regenerating your API key")
