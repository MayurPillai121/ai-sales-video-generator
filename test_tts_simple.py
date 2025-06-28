#!/usr/bin/env python3
"""
Simple test for TTS generation
"""

import os
from dotenv import load_dotenv
from hedra_client import HedraClient

def test_tts():
    """Test TTS generation"""
    
    load_dotenv()
    
    try:
        print("🎤 Testing TTS Generation...")
        print("=" * 50)
        
        client = HedraClient()
        print(f"✅ Client initialized")
        print(f"   Base URL: {client.base_url}")
        print(f"   Voice ID: {client.voice_id}")
        
        # Test TTS generation
        test_text = "Hello, this is a test of text to speech generation."
        print(f"\n🔊 Generating TTS for: {test_text}")
        
        result = client.create_text_to_speech_asset(test_text)
        
        if result["success"]:
            print(f"✅ TTS generation started successfully!")
            print(f"   Audio Asset ID: {result['audio_asset_id']}")
            print(f"   Generation ID: {result['generation_id']}")
            print(f"   Message: {result['message']}")
            
            # Check status
            print(f"\n⏳ Checking generation status...")
            status_result = client.check_job_status(result['generation_id'])
            
            if status_result["success"]:
                print(f"✅ Status check successful!")
                print(f"   Status: {status_result['status']}")
                print(f"   Progress: {status_result.get('progress', 0)*100:.1f}%")
            else:
                print(f"❌ Status check failed: {status_result['error']}")
            
            return True
            
        else:
            print(f"❌ TTS generation failed: {result['error']}")
            if "status_code" in result:
                print(f"   Status Code: {result['status_code']}")
            return False
            
    except Exception as e:
        print(f"💥 Test failed with exception: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_tts()
    if success:
        print(f"\n🎉 TTS TEST PASSED!")
    else:
        print(f"\n❌ TTS TEST FAILED!")
