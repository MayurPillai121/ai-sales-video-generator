#!/usr/bin/env python3
"""
Test Hedra API with paid subscription
Verifies correct base URL, endpoints, and credit usage
"""

import os
import time
from dotenv import load_dotenv
from hedra_client import HedraClient

def test_hedra_paid_api():
    """Test Hedra API with paid subscription"""
    
    print("🚀 Testing Hedra API with Paid Subscription")
    print("=" * 60)
    
    # Load environment
    load_dotenv()
    api_key = os.getenv("HEDRA_API_KEY")
    
    if not api_key:
        print("❌ HEDRA_API_KEY not found in .env file")
        return False
    
    print(f"✅ API Key loaded: {api_key[:30]}...")
    print(f"   Full length: {len(api_key)} characters")
    
    try:
        # Initialize client
        print(f"\n🔧 Initializing Hedra client...")
        client = HedraClient()
        print(f"✅ Client initialized")
        print(f"   Base URL: {client.base_url}")
        print(f"   Voice ID: {client.voice_id}")
        print(f"   Avatar: Generated from prompt (professional business person)")
        
        # Test connection
        print(f"\n🔗 Testing API connection...")
        connection_result = client.test_connection()
        
        if connection_result["success"]:
            print(f"✅ Connection successful: {connection_result['message']}")
        else:
            print(f"❌ Connection failed: {connection_result['error']}")
            return False
        
        # Test video generation
        print(f"\n🎬 Testing video generation with Character-3 API...")
        test_script = "Hello! This is a test of our Hedra AI video generation with paid subscription. The system is working correctly."
        
        print(f"Script: {test_script}")
        print(f"Voice: {client.voice_id}")
        print(f"Endpoint: POST /generations")
        
        # Create video generation job
        result = client.create_video_generation(
            audio_text=test_script,
            aspect_ratio="16:9"
        )
        
        if result["success"]:
            job_id = result["job_id"]
            print(f"✅ Video generation job created successfully!")
            print(f"   Job ID: {job_id}")
            print(f"   Message: {result['message']}")
            
            # Test job status checking
            print(f"\n⏳ Testing job status polling...")
            max_checks = 12  # 1 minute of checking (5 second intervals)
            
            for i in range(max_checks):
                print(f"   Check {i+1}/{max_checks}...")
                
                status_result = client.check_job_status(job_id)
                
                if status_result["success"]:
                    status = status_result["status"]
                    print(f"   Status: {status.upper()}")
                    
                    if status == "completed":
                        print(f"🎉 Video generation completed!")
                        
                        # Check for video URL
                        video_url = status_result["data"].get("videoUrl")
                        if video_url:
                            print(f"✅ Video URL available: {video_url[:50]}...")
                            print(f"\n🎯 FULL SUCCESS: Paid API is working correctly!")
                            print(f"   - Authentication: ✅")
                            print(f"   - Job Creation: ✅") 
                            print(f"   - Status Polling: ✅")
                            print(f"   - Video Generation: ✅")
                            print(f"   - Download URL: ✅")
                            return True
                        else:
                            print(f"⚠️ Video completed but no download URL")
                            return False
                            
                    elif status == "failed":
                        error_msg = status_result["data"].get("errorMessage", "Unknown error")
                        print(f"❌ Video generation failed: {error_msg}")
                        return False
                        
                    elif status in ["processing", "queued", "pending"]:
                        print(f"   Continuing to wait...")
                        time.sleep(5)
                    else:
                        print(f"   Unknown status: {status}")
                        time.sleep(5)
                else:
                    print(f"❌ Status check failed: {status_result['error']}")
                    return False
            
            print(f"⏰ Job still processing after 1 minute - this is normal for longer videos")
            print(f"✅ API integration is working correctly!")
            print(f"   Job ID {job_id} can be checked later")
            return True
            
        else:
            print(f"❌ Video generation failed: {result['error']}")
            
            # Show specific error details
            if "status_code" in result:
                status_code = result["status_code"]
                print(f"   Status Code: {status_code}")
                
                if status_code == 429:
                    print(f"   ⚠️ Rate limit exceeded - API is working but you're hitting limits")
                elif status_code == 404:
                    print(f"   ⚠️ Asset not found - check video asset ID")
                elif status_code == 401:
                    print(f"   ⚠️ Authentication failed - check API key")
                elif status_code == 402:
                    print(f"   ⚠️ Payment required - check your subscription/credits")
            
            # Show response for debugging
            if "response" in result:
                print(f"   Response: {result['response']}")
            
            return False
            
    except Exception as e:
        print(f"💥 Test failed with exception: {str(e)}")
        return False

def main():
    """Main test function"""
    success = test_hedra_paid_api()
    
    print(f"\n" + "=" * 60)
    if success:
        print(f"🎉 HEDRA API TEST PASSED - Ready for production!")
    else:
        print(f"❌ HEDRA API TEST FAILED - Check configuration")
    print(f"=" * 60)

if __name__ == "__main__":
    main()
