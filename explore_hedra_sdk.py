#!/usr/bin/env python3
"""
Explore Hedra SDK structure
"""

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("HEDRA_API_KEY")

try:
    from hedra import Hedra
    print("✅ Hedra SDK imported successfully")
    
    # Try different initialization approaches
    print("\n🔧 Testing SDK initialization...")
    
    try:
        # Method 1: Simple initialization
        client = Hedra(api_key=api_key)
        print("✅ Method 1 successful: Hedra(api_key=api_key)")
    except Exception as e:
        print(f"❌ Method 1 failed: {e}")
        
        try:
            # Method 2: Just API key
            client = Hedra(api_key)
            print("✅ Method 2 successful: Hedra(api_key)")
        except Exception as e2:
            print(f"❌ Method 2 failed: {e2}")
            
            try:
                # Method 3: No arguments
                client = Hedra()
                print("✅ Method 3 successful: Hedra()")
            except Exception as e3:
                print(f"❌ Method 3 failed: {e3}")
    
    # Explore client structure
    if 'client' in locals():
        print(f"\n📋 Client attributes:")
        for attr in dir(client):
            if not attr.startswith('_'):
                print(f"   • {attr}")
        
        # Check for characters and projects
        if hasattr(client, 'characters'):
            print(f"\n🎭 Characters methods:")
            for method in dir(client.characters):
                if not method.startswith('_'):
                    print(f"   • characters.{method}")
        
        if hasattr(client, 'projects'):
            print(f"\n📁 Projects methods:")
            for method in dir(client.projects):
                if not method.startswith('_'):
                    print(f"   • projects.{method}")

except ImportError as e:
    print(f"❌ Failed to import Hedra SDK: {e}")
except Exception as e:
    print(f"❌ Error exploring SDK: {e}")
