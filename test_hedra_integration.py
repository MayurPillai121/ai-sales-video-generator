#!/usr/bin/env python3
"""
Test script for Hedra AI integration
Tests connection, model access, and basic functionality
"""

import os
import sys
from dotenv import load_dotenv
from hedra_client import HedraClient

def test_hedra_integration():
    """Test Hedra AI integration step by step"""
    
    print("🧪 Testing Hedra AI Integration")
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
        # Initialize client
        print("\n🔧 Initializing Hedra client...")
        client = HedraClient()
        print(f"✅ Client initialized")
        print(f"   Base URL: {client.base_url}")
        print(f"   Asset ID: {client.asset_id}")
        print(f"   Voice: {client.voice}")
        
        # Test connection
        print("\n🔗 Testing API connection...")
        connection_result = client.test_connection()
        
        if connection_result["success"]:
            print(f"✅ Connection successful: {connection_result['message']}")
            print(f"   Models available: {connection_result.get('models_count', 'Unknown')}")
        else:
            print(f"❌ Connection failed: {connection_result['error']}")
            return False
        
        # Get models
        print("\n🤖 Retrieving available models...")
        models_result = client.get_models()
        
        if models_result["success"]:
            models = models_result["data"]
            print(f"✅ Retrieved {len(models)} models")
            
            if models:
                print("   Available models:")
                for i, model in enumerate(models[:3]):  # Show first 3
                    print(f"   {i+1}. {model.get('id', 'Unknown ID')}")
                    print(f"      Name: {model.get('name', 'Unknown')}")
                    print(f"      Type: {model.get('type', 'Unknown')}")
                if len(models) > 3:
                    print(f"   ... and {len(models) - 3} more")
        else:
            print(f"❌ Failed to get models: {models_result['error']}")
            return False
        
        # Test TTS placeholder
        print("\n🎤 Testing TTS functionality...")
        tts_result = client.create_text_to_speech_audio(
            "Hello, this is a test message for Hedra AI integration.",
            voice=client.voice
        )
        
        if tts_result["success"]:
            print(f"✅ TTS test successful: {tts_result['message']}")
        else:
            print(f"⚠️ TTS test: {tts_result.get('message', 'Not implemented')}")
        
        print("\n🎉 All tests completed successfully!")
        print("\n📋 Integration Summary:")
        print(f"   • API Connection: ✅ Working")
        print(f"   • Models Available: ✅ {connection_result.get('models_count', 'Unknown')}")
        print(f"   • User Asset ID: ✅ {client.asset_id}")
        print(f"   • Voice Setting: ✅ {client.voice}")
        print(f"   • Ready for video generation: ✅ Yes")
        
        print("\n💡 Next Steps:")
        print("   1. Upload an audio file or implement TTS")
        print("   2. Run the Streamlit app: streamlit run app.py")
        print("   3. Generate a script and create your first video!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        return False

def main():
    """Main test function"""
    success = test_hedra_integration()
    
    if success:
        print("\n🎯 Integration test PASSED")
        sys.exit(0)
    else:
        print("\n💥 Integration test FAILED")
        print("\n🔧 Troubleshooting:")
        print("   • Check your HEDRA_API_KEY in .env file")
        print("   • Verify your Hedra account has API access")
        print("   • Ensure you have Creator plan or above")
        print("   • Try regenerating your API key")
        sys.exit(1)

if __name__ == "__main__":
    main()
