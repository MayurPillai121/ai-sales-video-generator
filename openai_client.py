import os
import openai
from typing import Dict, Any

class OpenAIClient:
    """
    OpenAI API client for script generation
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        openai.api_key = self.api_key
    
    def test_connection(self) -> Dict[str, Any]:
        """Test OpenAI API connection"""
        try:
            # Simple test with minimal token usage
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            
            return {
                "success": True,
                "message": "OpenAI API connected successfully"
            }
            
        except Exception as e:
            if "authentication" in str(e).lower() or "api key" in str(e).lower():
                return {
                    "success": False,
                    "error": "Invalid OpenAI API key. Please check your API key in the .env file."
                }
            elif "rate limit" in str(e).lower() or "quota" in str(e).lower():
                return {
                    "success": False,
                    "error": "OpenAI rate limit exceeded. Please try again later or upgrade your plan."
                }
            else:
                return {
                    "success": False,
                    "error": f"Connection failed: {str(e)}"
                }
