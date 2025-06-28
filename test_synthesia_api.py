#!/usr/bin/env python3
"""
Comprehensive test script for Synthesia API
Tests API connectivity, authentication, and request formats
"""
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SynthesiaAPITester:
    def __init__(self):
        self.api_key = os.getenv("SYNTHESIA_API_KEY")
        self.base_url = "https://api.synthesia.io/v2"
        
        # Test different header formats
        self.headers_v1 = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        self.headers_v2 = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }
        
        self.headers_v3 = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

    def test_api_key_format(self):
        """Test if API key is properly formatted"""
        print("🔑 Testing API Key Format...")
        print(f"API Key: {self.api_key[:10]}...{self.api_key[-4:]}")
        print(f"Length: {len(self.api_key) if self.api_key else 0}")
        
        if not self.api_key:
            print("❌ No API key found!")
            return False
        elif len(self.api_key) != 32:
            print("⚠️  API key length unusual (expected 32 chars)")
        else:
            print("✅ API key format looks correct")
        return True

    def test_basic_connectivity(self):
        """Test basic API connectivity"""
        print("\n🌐 Testing Basic Connectivity...")
        
        # Test different header formats
        header_formats = [
            ("Bearer Token", self.headers_v1),
            ("Token Auth", self.headers_v2),
            ("X-API-KEY", self.headers_v3)
        ]
        
        for name, headers in header_formats:
            print(f"\nTesting {name} format:")
            try:
                response = requests.get(
                    f"{self.base_url}/avatars",
                    headers=headers,
                    timeout=10
                )
                
                print(f"Status Code: {response.status_code}")
                print(f"Response Headers: {dict(response.headers)}")
                
                if response.status_code == 200:
                    print(f"✅ {name} format works!")
                    data = response.json()
                    print(f"Found {len(data.get('avatars', []))} avatars")
                    return headers
                elif response.status_code == 401:
                    print(f"❌ {name}: Unauthorized - API key issue")
                elif response.status_code == 403:
                    print(f"❌ {name}: Forbidden - Access denied")
                else:
                    print(f"❌ {name}: HTTP {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ {name}: Connection error - {str(e)}")
        
        return None

    def test_avatars_endpoint(self, headers):
        """Test avatars endpoint specifically"""
        print("\n👤 Testing Avatars Endpoint...")
        
        try:
            response = requests.get(
                f"{self.base_url}/avatars",
                headers=headers,
                timeout=10
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                avatars = data.get('avatars', [])
                print(f"✅ Found {len(avatars)} avatars")
                
                # Show first few avatars
                for i, avatar in enumerate(avatars[:3]):
                    print(f"  {i+1}. {avatar.get('id', 'N/A')} - {avatar.get('name', 'Unnamed')}")
                
                return True
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

    def test_video_creation_payload(self, headers):
        """Test video creation with minimal payload"""
        print("\n🎥 Testing Video Creation Payload...")
        
        # Test with minimal required payload
        minimal_payload = {
            "title": "API Test Video",
            "scenes": [
                {
                    "elements": [
                        {
                            "type": "avatar",
                            "avatar_id": "02e3638f-2e2b-4f41-93dd-6dea6fdf2565",
                            "script": {
                                "type": "text",
                                "text": "Hello, this is a test message."
                            }
                        }
                    ]
                }
            ]
        }
        
        print("Testing minimal payload...")
        print(json.dumps(minimal_payload, indent=2))
        
        try:
            response = requests.post(
                f"{self.base_url}/videos",
                headers=headers,
                json=minimal_payload,
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 201:
                print("✅ Video creation request successful!")
                data = response.json()
                video_id = data.get('id')
                print(f"Video ID: {video_id}")
                return video_id
            elif response.status_code == 400:
                print("❌ Bad Request - Payload format issue")
            elif response.status_code == 403:
                print("❌ Forbidden - Check API permissions")
            else:
                print(f"❌ Failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        return None

    def run_full_test(self):
        """Run comprehensive API test"""
        print("🧪 Synthesia API Comprehensive Test")
        print("=" * 50)
        
        # Test 1: API Key Format
        if not self.test_api_key_format():
            return
        
        # Test 2: Basic Connectivity
        working_headers = self.test_basic_connectivity()
        if not working_headers:
            print("\n❌ No working authentication method found!")
            print("\n🔧 Troubleshooting Tips:")
            print("1. Verify your API key is correct")
            print("2. Check if your Synthesia plan includes API access")
            print("3. Ensure your account is active and in good standing")
            print("4. Try regenerating your API key")
            return
        
        print(f"\n✅ Found working authentication method!")
        
        # Test 3: Avatars Endpoint
        if not self.test_avatars_endpoint(working_headers):
            return
        
        # Test 4: Video Creation (optional - creates actual video)
        print("\n⚠️  Video creation test will create an actual video.")
        print("This may consume API credits. Continue? (y/n): ", end="")
        
        # For automated testing, skip video creation
        print("Skipping video creation test for safety.")
        
        print("\n🎉 API Tests Complete!")
        print("✅ Authentication working")
        print("✅ Avatars endpoint accessible")
        print("✅ Ready for video creation")

if __name__ == "__main__":
    tester = SynthesiaAPITester()
    tester.run_full_test()
