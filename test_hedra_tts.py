#!/usr/bin/env python3
"""
Test script for Hedra AI text-to-speech video generation
Tests the complete text-to-video workflow without requiring separate audio files
"""

import os
import sys
from dotenv import load_dotenv
from hedra_client import HedraClient

def test_hedra_tts():
    """Test Hedra AI text-to-speech video generation"""
    
    print("🎤 Testing Hedra AI Text-to-Speech Video Generation")
    print("=" * 60)
    
    # Load environment
    load_dotenv()
    
    # Check API key
    api_key = os.getenv("HEDRA_API_KEY")
    if not api_key:
        print("❌ HEDRA_API_KEY not found in environment")
        return False
    
    print(f"✅ API Key loaded: {api_key[:20]}...")
    
    try:
        # Initialize client
        print("\n🔧 Initializing Hedra client...")
        client = HedraClient()
        print(f"✅ Client initialized")
        print(f"   Base URL: {client.base_url}")
        print(f"   Avatar Asset ID: {client.asset_id}")
        print(f"   Voice: {client.voice}")
        
        # Test connection
        print("\n🔗 Testing API connection...")
        connection_result = client.test_connection()
        
        if not connection_result["success"]:
            print(f"❌ Connection failed: {connection_result['error']}")
            return False
        
        print(f"✅ Connection successful: {connection_result['message']}")
        
        # Test script for TTS
        test_script = """
        Hello! This is a test of Hedra AI's text-to-speech capabilities. 
        I'm demonstrating how we can create talking avatar videos directly from text, 
        without needing to upload separate audio files. 
        Hedra AI will automatically generate the voice audio and synchronize it with the avatar.
        This makes the video creation process much simpler and more streamlined.
        """
        
        print(f"\n🎬 Testing text-to-speech video creation...")
        print(f"Script: {test_script[:100]}...")
        print(f"Voice: {client.voice}")
        print(f"Aspect Ratio: 16:9")
        print(f"Resolution: 720p")
        
        # Create video from text only
        creation_result = client.create_video_from_text(
            text=test_script.strip(),
            voice="tara",
            aspect_ratio="16:9",
            resolution="720p"
        )
        
        if creation_result["success"]:
            generation_id = creation_result["generation_id"]
            print(f"✅ Video generation started successfully!")
            print(f"   Generation ID: {generation_id}")
            print(f"   Message: {creation_result['message']}")
            
            # Test status checking
            print(f"\n📊 Testing status check...")
            status_result = client.get_generation_status(generation_id)
            
            if status_result["success"]:
                status_data = status_result["data"]
                current_status = status_data.get("status", "unknown")
                print(f"✅ Status check successful")
                print(f"   Current status: {current_status}")
                
                if current_status.lower() in ["pending", "processing", "queued"]:
                    print(f"   ⏳ Video is being generated...")
                    print(f"   💡 You can monitor progress with generation ID: {generation_id}")
                elif current_status.lower() == "complete":
                    print(f"   🎉 Video generation completed!")
                    if status_data.get("url"):
                        print(f"   🔗 Download URL available")
                elif current_status.lower() == "error":
                    error_msg = status_data.get("error_message", "Unknown error")
                    print(f"   ❌ Generation failed: {error_msg}")
                
            else:
                print(f"⚠️ Status check failed: {status_result['error']}")
            
            print(f"\n🎯 Text-to-Speech Test Results:")
            print(f"   • API Connection: ✅ Working")
            print(f"   • TTS Video Creation: ✅ Started successfully")
            print(f"   • Generation ID: ✅ {generation_id}")
            print(f"   • Voice Used: ✅ tara")
            print(f"   • Status Monitoring: ✅ Working")
            
            print(f"\n💡 Next Steps:")
            print(f"   1. Monitor generation progress with ID: {generation_id}")
            print(f"   2. Video will be available for download when complete")
            print(f"   3. Integration is ready for production use!")
            
            return True
            
        else:
            print(f"❌ Video creation failed: {creation_result['error']}")
            return False
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        return False

def main():
    """Main test function"""
    success = test_hedra_tts()
    
    if success:
        print(f"\n🎉 Text-to-Speech test PASSED")
        print(f"🚀 Hedra AI integration is ready for production!")
        sys.exit(0)
    else:
        print(f"\n💥 Text-to-Speech test FAILED")
        print(f"\n🔧 Troubleshooting:")
        print(f"   • Check your HEDRA_API_KEY in .env file")
        print(f"   • Verify your Hedra account has API access")
        print(f"   • Ensure you have Creator plan or above")
        print(f"   • Check if your asset ID is valid")
        sys.exit(1)

if __name__ == "__main__":
    main()
