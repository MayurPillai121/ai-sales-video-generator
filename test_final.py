#!/usr/bin/env python3
"""
Final comprehensive test of the updated Synthesia client
"""
import os
from dotenv import load_dotenv
from synthesia_client import SynthesiaClient

load_dotenv()

def main():
    print("🧪 Final Synthesia API Test")
    print("=" * 60)
    
    try:
        # Initialize client (this will auto-detect working configuration)
        print("1. Initializing Synthesia client...")
        client = SynthesiaClient()
        print(f"   ✅ Client initialized")
        print(f"   Base URL: {client.base_url}")
        
        # Test connection
        print("\n2. Testing API connection...")
        connection_result = client.test_connection()
        
        if connection_result.get("success"):
            print("   ✅ Connection successful!")
            print(f"   Status Code: {connection_result.get('status_code')}")
        else:
            print("   ❌ Connection failed!")
            print(f"   Error: {connection_result.get('error')}")
            print(f"   Status Code: {connection_result.get('status_code')}")
            print(f"   Response: {connection_result.get('response', '')[:200]}")
        
        # Test avatars endpoint
        print("\n3. Testing avatars endpoint...")
        avatars_result = client.get_avatars()
        
        if avatars_result.get("success"):
            print("   ✅ Avatars retrieved successfully!")
            avatars_data = avatars_result.get("data", {})
            avatars = avatars_data.get("avatars", [])
            print(f"   Found {len(avatars)} avatars")
            
            # Check for user's specific avatar
            user_avatar_id = "02e3638f-2e2b-4f41-93dd-6dea6fdf2565"
            user_avatar_found = False
            
            for avatar in avatars:
                if avatar.get("id") == user_avatar_id:
                    print(f"   ✅ Your avatar found: {avatar.get('name', 'Custom Avatar')}")
                    user_avatar_found = True
                    break
            
            if not user_avatar_found:
                print(f"   ⚠️  Your avatar ID ({user_avatar_id}) not found")
                print("   Available avatars (first 5):")
                for i, avatar in enumerate(avatars[:5]):
                    print(f"     {i+1}. {avatar.get('id')} - {avatar.get('name', 'Unnamed')}")
        else:
            print("   ❌ Avatars request failed!")
            print(f"   Error: {avatars_result.get('error')}")
            print(f"   Status Code: {avatars_result.get('status_code')}")
            print(f"   Message: {avatars_result.get('message', '')}")
        
        # Test video creation payload (without actually creating)
        print("\n4. Testing video creation payload format...")
        test_script = "Hello, this is a test message for the Synthesia API."
        test_avatar = "02e3638f-2e2b-4f41-93dd-6dea6fdf2565"
        
        print("   Payload that would be sent:")
        payload = {
            "title": "AI Generated Sales Video",
            "scenes": [
                {
                    "elements": [
                        {
                            "type": "avatar",
                            "avatar_id": test_avatar,
                            "script": {
                                "type": "text",
                                "text": test_script
                            }
                        }
                    ]
                }
            ]
        }
        
        import json
        print(f"   {json.dumps(payload, indent=6)}")
        
        print("\n5. Summary:")
        if connection_result.get("success") and avatars_result.get("success"):
            print("   ✅ API is working correctly!")
            print("   ✅ Authentication successful")
            print("   ✅ Avatars endpoint accessible")
            print("   ✅ Ready for video creation")
            
            print(f"\n   🎯 Recommended next steps:")
            print(f"   1. Use the working configuration in your main app")
            print(f"   2. Test video creation with a small script")
            print(f"   3. Monitor API usage and credits")
            
        else:
            print("   ❌ API issues detected")
            print(f"\n   🔧 Troubleshooting recommendations:")
            print(f"   1. Verify API key: {client.api_key[:10]}...{client.api_key[-4:]}")
            print(f"   2. Check Synthesia account status and API access")
            print(f"   3. Verify account has sufficient credits")
            print(f"   4. Contact Synthesia support if issues persist")
        
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        print(f"\n🔧 This suggests:")
        print(f"1. API key might be missing from .env file")
        print(f"2. Network connectivity issues")
        print(f"3. Synthesia API might be temporarily unavailable")

if __name__ == "__main__":
    main()
