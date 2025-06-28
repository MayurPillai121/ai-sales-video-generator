#!/usr/bin/env python3
"""
Test mercury API with correct endpoints
"""

import os
from dotenv import load_dotenv
from hedra_client import HedraClient

def test_mercury_api():
    """Test mercury API video generation"""
    
    load_dotenv()
    
    try:
        print("🎬 Testing Mercury API Video Generation...")
        print("=" * 50)
        
        client = HedraClient()
        print(f"✅ Client initialized")
        print(f"   Base URL: {client.base_url}")
        print(f"   Voice ID: {client.voice_id}")
        
        # Test video generation
        test_text = "Hello! This is a test of the mercury API video generation system."
        print(f"\n🎥 Creating video with text: {test_text}")
        
        result = client.create_video_generation(
            audio_text=test_text,
            aspect_ratio="16:9",
            voice_id="tara"
        )
        
        if result["success"]:
            print(f"✅ Video generation started successfully!")
            print(f"   Job ID: {result['job_id']}")
            print(f"   Message: {result['message']}")
            
            # Check status
            print(f"\n⏳ Checking job status...")
            status_result = client.check_job_status(result['job_id'])
            
            if status_result["success"]:
                print(f"✅ Status check successful!")
                print(f"   Status: {status_result['status']}")
                print(f"   Progress: {status_result.get('progress', 0)*100:.1f}%")
                if status_result.get('video_url'):
                    print(f"   Video URL: {status_result['video_url']}")
            else:
                print(f"❌ Status check failed: {status_result['error']}")
            
            return True
            
        else:
            print(f"❌ Video generation failed: {result['error']}")
            if "status_code" in result:
                print(f"   Status Code: {result['status_code']}")
            return False
            
    except Exception as e:
        print(f"💥 Test failed with exception: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_mercury_api()
    if success:
        print(f"\n🎉 MERCURY API TEST PASSED!")
    else:
        print(f"\n❌ MERCURY API TEST FAILED!")
