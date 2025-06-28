#!/usr/bin/env python3
"""
Test script to verify API keys and configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_configuration():
    print("🔧 Testing AI Sales Video Generator Configuration...")
    print("=" * 50)
    
    # Check OpenAI API Key
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and len(openai_key) > 20:
        print("✅ OpenAI API Key: Configured")
        print(f"   Key starts with: {openai_key[:10]}...")
    else:
        print("❌ OpenAI API Key: Not configured or invalid")
    
    # Check Synthesia API Key
    synthesia_key = os.getenv("SYNTHESIA_API_KEY")
    if synthesia_key and len(synthesia_key) > 20:
        print("✅ Synthesia API Key: Configured")
        print(f"   Key: {synthesia_key[:10]}...")
    else:
        print("❌ Synthesia API Key: Not configured or invalid")
    
    print("\n🎯 Configuration Summary:")
    if openai_key and synthesia_key:
        print("✅ All API keys are configured!")
        print("✅ Ready to generate AI sales videos!")
        print("\n🚀 Run the app with: python -m streamlit run app.py")
    else:
        print("❌ Some API keys are missing. Please check your .env file.")
    
    print("=" * 50)

if __name__ == "__main__":
    test_configuration()
