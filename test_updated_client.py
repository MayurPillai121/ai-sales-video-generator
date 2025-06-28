#!/usr/bin/env python3
"""
Test the updated Synthesia client with comprehensive error handling
"""
import os
from dotenv import load_dotenv
from synthesia_client import SynthesiaClient

load_dotenv()

def test_updated_client():
    print("🧪 Testing Updated Synthesia Client")
    print("=" * 60)
    
    try:
        # Initialize client
        print("1. Initializing Synthesia client...")
        client = SynthesiaClient()
        print(f"   ✅ Client initialized")
        print(f"   API Key: {client.api_key[:10]}...{client.api_key[-4:]}")
        print(f"   Base URL: {client.base_url}")
        
        # Test connection
        print(f"\n2. Testing API connection...")
        connection_result = client.test_connection()
        
        if connection_result["success"]:
            print(f"   ✅ Connection successful!")
            print(f"   Auth method: {connection_result['auth_method']}")
            print(f"   Working endpoint: {connection_result['endpoint']}")
            
            # Test avatar retrieval
            print(f"\n3. Testing avatar retrieval...")
            avatars_result = client.get_avatars()
            
            if avatars_result["success"]:
                print(f"   ✅ {avatars_result['message']}")
                
                # Check for user's specific avatar
                avatars = avatars_result["data"].get("avatars", [])
                user_avatar = "02e3638f-2e2b-4f41-93dd-6dea6fdf2565"
                
                for avatar in avatars:
                    if avatar.get("id") == user_avatar:
                        print(f"   ✅ Your avatar found: {avatar.get('name', 'Custom Avatar')}")
                        break
                else:
                    print(f"   ⚠️  Your specific avatar not found")
                    print(f"   Available avatars (first 3):")
                    for i, avatar in enumerate(avatars[:3]):
                        print(f"     {i+1}. {avatar.get('id')} - {avatar.get('name', 'Unnamed')}")
                
                print(f"\n🎉 SUCCESS! Synthesia API is working correctly!")
                print(f"✅ Ready to create videos")
                
            else:
                print(f"   ❌ Avatar retrieval failed: {avatars_result['error']}")
                
        else:
            print(f"   ❌ Connection failed: {connection_result['error']}")
            print(f"\n🔧 Troubleshooting steps:")
            for step in connection_result.get("troubleshooting", []):
                print(f"   - {step}")
        
    except Exception as e:
        print(f"❌ Client initialization failed: {str(e)}")
        print(f"\n🔧 Check:")
        print(f"   - .env file exists with SYNTHESIA_API_KEY")
        print(f"   - API key is correct format")
        print(f"   - All dependencies are installed")

def main():
    test_updated_client()
    
    print(f"\n📋 Summary:")
    print(f"The Synthesia client has been updated with:")
    print(f"✅ Correct Bearer token authentication format")
    print(f"✅ Alternative X-API-KEY authentication method")
    print(f"✅ Comprehensive error handling and reporting")
    print(f"✅ Detailed troubleshooting guidance")
    print(f"✅ Proper API endpoint structure")
    
    print(f"\n🚀 Next Steps:")
    print(f"1. If connection succeeds: Ready to use in your app!")
    print(f"2. If connection fails: Follow troubleshooting steps")
    print(f"3. Contact Synthesia support if issues persist")

if __name__ == "__main__":
    main()
