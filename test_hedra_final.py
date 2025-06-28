#!/usr/bin/env python3
"""
Test script for FINAL Hedra API integration using Official OpenAPI Spec
"""

import os
import sys
from dotenv import load_dotenv
from hedra_client import HedraClient

def main():
    print("🎬 Testing FINAL Hedra API Integration (Official OpenAPI Spec)")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    try:
        # Initialize client
        print("🔑 Initializing Hedra client...")
        hedra_client = HedraClient()
        print(f"✅ Client initialized with API: {hedra_client.base_url}")
        print(f"✅ Headers: X-API-Key configured")
        
        # Test 1: Get available voices
        print("\n🎤 Fetching available voices...")
        voices = hedra_client.get_available_voices()
        if voices:
            print(f"✅ Found {len(voices)} voices:")
            for voice in voices[:3]:  # Show first 3
                voice_id = voice.get("voice_id", voice.get("id", "unknown"))
                name = voice.get("name", "Unknown")
                print(f"   - {voice_id}: {name}")
            
            # Use first available voice
            voice_id = voices[0].get("voice_id", voices[0].get("id", "default"))
            print(f"🎯 Using voice: {voice_id}")
        else:
            voice_id = "default"
            print("⚠️  No voices found, using default")
        
        # Test 2: Create video with TTS + AI avatar
        print(f"\n🎬 Creating video with official OpenAPI spec...")
        test_script = """
        Hello! This is a test of the Hedra API integration using the official OpenAPI specification.
        
        We're testing the complete workflow:
        - Text-to-speech audio generation
        - AI-generated avatar creation
        - Video synthesis and rendering
        
        If you can see this video, the integration is working perfectly!
        """
        
        print(f"📝 Script length: {len(test_script)} characters")
        print(f"🎤 Voice ID: {voice_id}")
        print(f"📐 Aspect ratio: 16:9")
        
        # Create video using official workflow
        result = hedra_client.create_video_complete(
            script_text=test_script.strip(),
            voice_id=voice_id,
            aspect_ratio="16:9"
        )
        
        # Display results
        print("\n" + "=" * 60)
        if result["success"]:
            print("🎉 SUCCESS! Video generation completed!")
            print(f"✅ Video URL: {result['video_url']}")
            print(f"✅ Job ID: {result['job_id']}")
            print(f"✅ Status: {result['status']}")
            print(f"✅ Message: {result['message']}")
            
            # Optional: Download video
            print(f"\n💾 Downloading video...")
            download_result = hedra_client.download_video(
                result['video_url'], 
                "test_hedra_final.mp4"
            )
            
            if download_result["success"]:
                print(f"✅ Video downloaded: {download_result['video_path']}")
            else:
                print(f"⚠️  Download failed: {download_result['error']}")
                
        else:
            print("❌ FAILED! Video generation failed!")
            print(f"❌ Error: {result['error']}")
            if 'status_code' in result:
                print(f"❌ Status Code: {result['status_code']}")
            if 'response' in result:
                print(f"❌ Response: {result['response']}")
        
        print("\n" + "=" * 60)
        print("🏁 Test completed!")
        
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
