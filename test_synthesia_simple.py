#!/usr/bin/env python3
"""
Simple Synthesia API test
"""
import os
from dotenv import load_dotenv
from synthesia_client import SynthesiaClient

# Load environment variables
load_dotenv()

def test_synthesia_connection():
    print("🧪 Testing Synthesia API Connection...")
    print("=" * 50)
    
    try:
        # Initialize client
        client = SynthesiaClient()
        
        # Test connection
        print("1. Testing API connection...")
        result = client.test_connection()
        
        if result.get("success"):
            print("✅ Connection successful!")
            print(f"   Method: {result.get('message')}")
            print(f"   Endpoint: {result.get('endpoint')}")
            
            # Test avatars
            print("\n2. Testing avatars endpoint...")
            avatars_result = client.get_avatars()
            
            if avatars_result.get("success"):
                print("✅ Avatars retrieved successfully!")
                avatars = avatars_result.get("data", {}).get("avatars", [])
                print(f"   Found {len(avatars)} avatars")
                
                # Show user's avatar if found
                user_avatar = "02e3638f-2e2b-4f41-93dd-6dea6fdf2565"
                found_user_avatar = False
                for avatar in avatars:
                    if avatar.get("id") == user_avatar:
                        print(f"✅ Your avatar found: {avatar.get('name', 'Unnamed')}")
                        found_user_avatar = True
                        break
                
                if not found_user_avatar:
                    print(f"⚠️  Your avatar ID ({user_avatar}) not found in available avatars")
                    print("   Available avatars:")
                    for i, avatar in enumerate(avatars[:5]):
                        print(f"   {i+1}. {avatar.get('id')} - {avatar.get('name', 'Unnamed')}")
                
            else:
                print(f"❌ Avatars failed: {avatars_result.get('error')}")
                
        else:
            print("❌ Connection failed!")
            print(f"   Error: {result.get('error')}")
            if result.get('status_code'):
                print(f"   Status Code: {result.get('status_code')}")
            if result.get('auth_method'):
                print(f"   Auth Method: {result.get('auth_method')}")
                
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
    
    print("=" * 50)

if __name__ == "__main__":
    test_synthesia_connection()
