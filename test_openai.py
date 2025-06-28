#!/usr/bin/env python3
"""
Test script to verify OpenAI client initialization and basic functionality
"""
import os
from dotenv import load_dotenv
from script_generator import ScriptGenerator

# Load environment variables
load_dotenv()

def test_openai_client():
    print("🧪 Testing OpenAI Client...")
    print("=" * 50)
    
    try:
        # Test ScriptGenerator initialization
        print("1. Testing ScriptGenerator initialization...")
        script_gen = ScriptGenerator()
        print("✅ ScriptGenerator initialized successfully!")
        
        # Test script generation with sample data
        print("\n2. Testing script generation...")
        test_script = script_gen.generate_sales_script(
            company_name="Test Company",
            contact_name="John Doe",
            product_service="AI Video Generator",
            key_benefits="Save time, increase engagement, professional videos",
            call_to_action="Schedule a demo call"
        )
        
        if test_script and not test_script.startswith("Error"):
            print("✅ Script generation successful!")
            print(f"Generated script preview: {test_script[:100]}...")
        else:
            print(f"❌ Script generation failed: {test_script}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n🔧 Troubleshooting tips:")
        print("- Check your OpenAI API key in .env file")
        print("- Ensure you have sufficient OpenAI credits")
        print("- Verify your internet connection")
    
    print("=" * 50)

if __name__ == "__main__":
    test_openai_client()
