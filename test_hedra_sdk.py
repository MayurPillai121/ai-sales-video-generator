#!/usr/bin/env python3
"""
Test script for Hedra Python SDK integration
"""

import os
import sys
from dotenv import load_dotenv
from hedra_client import HedraClient

def test_hedra_sdk():
    """Test Hedra SDK integration"""
    
    print("🚀 Testing Hedra Python SDK Integration")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Check API key
    api_key = os.getenv("HEDRA_API_KEY")
    if not api_key:
        print("❌ HEDRA_API_KEY not found in environment")
        return False
    
    print(f"✅ API Key loaded: {api_key[:20]}...")
    
    try:
        # Initialize client with SDK
        print("\n🔧 Initializing Hedra SDK client...")
        client = HedraClient()
        print(f"✅ SDK client initialized")
        print(f"   Video Asset ID: {client.video_asset_id}")
        print(f"   Voice ID: {client.voice_id}")
        
        # Test connection
        print("\n🔗 Testing SDK connection...")
        connection_result = client.test_connection()
        
        if connection_result["success"]:
            print(f"✅ Connection successful: {connection_result['message']}")
        else:
            print(f"❌ Connection failed: {connection_result['error']}")
            return False
        
        # Test simple video generation
        test_script = "Hello, this is a test of our AI video system using the official Hedra SDK."
        
        print(f"\n🎬 Testing video generation with SDK...")
        print(f"Script: {test_script}")
        print(f"Voice: {client.voice_id}")
        print(f"Asset: {client.video_asset_id}")
        
        # Create video generation job using SDK
        creation_result = client.create_video_generation(
            audio_text=test_script,
            aspect_ratio="16:9",
            voice_id="tara"
        )
        
        if creation_result["success"]:
            job_id = creation_result["job_id"]
            print(f"✅ Video generation job created with SDK!")
            print(f"   Job ID: {job_id}")
            print(f"   Message: {creation_result['message']}")
            
            # Test status check
            print(f"\n📊 Testing job status with SDK...")
            status_result = client.get_job_status(job_id)
            
            if status_result["success"]:
                status = status_result["status"]
                print(f"✅ Status check successful: {status}")
                
                print(f"\n🎯 Hedra SDK Test Results:")
                print(f"   • SDK Initialization: ✅ Working")
                print(f"   • Video Generation: ✅ Job created")
                print(f"   • Job ID: ✅ {job_id}")
                print(f"   • Status Monitoring: ✅ Working")
                print(f"   • Current Status: ✅ {status}")
                
                print(f"\n💡 Next Steps:")
                print(f"   1. Job will process automatically")
                print(f"   2. When complete, video will be available for download")
                print(f"   3. Hedra SDK integration is working!")
                
                return True
            else:
                print(f"⚠️ Status check failed: {status_result['error']}")
                return False
                
        else:
            print(f"❌ Video generation failed: {creation_result['error']}")
            return False
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        return False

def main():
    """Main test function"""
    success = test_hedra_sdk()
    
    if success:
        print(f"\n🎉 Hedra SDK test PASSED")
        print(f"🚀 Ready for production use!")
        sys.exit(0)
    else:
        print(f"\n💥 Hedra SDK test FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()
