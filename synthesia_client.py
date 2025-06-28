import requests
import os
import time
from typing import Dict, Any, Optional

class SynthesiaClient:
    """
    Synthesia API client for creating AI-generated videos
    Updated with correct authentication format based on API testing
    """
    
    def __init__(self):
        self.api_key = os.getenv("SYNTHESIA_API_KEY")
        if not self.api_key:
            raise ValueError("SYNTHESIA_API_KEY not found in environment variables")
        
        # Correct Synthesia API base URL (confirmed from documentation)
        self.base_url = "https://api.synthesia.io/v2"
        
        # Set up authentication headers with correct format
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Alternative authentication method
        self.headers_alt = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test API connection with comprehensive error reporting
        """
        print("🔍 Testing Synthesia API connection...")
        
        # Test both authentication methods
        auth_methods = [
            ("Bearer Token", self.headers),
            ("X-API-KEY", self.headers_alt)
        ]
        
        test_endpoints = ["/avatars", "/videos", "/account"]
        
        for auth_name, headers in auth_methods:
            print(f"   Trying {auth_name}...")
            
            for endpoint in test_endpoints:
                try:
                    url = f"{self.base_url}{endpoint}"
                    response = requests.get(url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        print(f"   ✅ Success with {auth_name} on {endpoint}")
                        self.headers = headers  # Use working headers
                        return {
                            "success": True,
                            "auth_method": auth_name,
                            "endpoint": endpoint,
                            "message": f"Connected successfully using {auth_name}"
                        }
                    elif response.status_code == 401:
                        print(f"   🔑 Unauthorized with {auth_name}")
                    elif response.status_code == 403:
                        print(f"   🚫 Forbidden with {auth_name}: {response.text[:100]}")
                    elif response.status_code == 404:
                        print(f"   ❌ Not Found: {endpoint}")
                    else:
                        print(f"   ⚠️  HTTP {response.status_code}: {response.text[:100]}")
                        
                except requests.exceptions.RequestException as e:
                    print(f"   ❌ Connection error: {str(e)}")
        
        return {
            "success": False,
            "error": "Unable to authenticate with Synthesia API",
            "troubleshooting": [
                "Verify API key is correct and active",
                "Check if account has API access enabled", 
                "Ensure account has sufficient credits",
                "Try regenerating API key from Synthesia dashboard",
                "Contact Synthesia support if issues persist"
            ]
        }
    
    def get_avatars(self) -> Dict[str, Any]:
        """Get list of available avatars with error handling"""
        try:
            response = requests.get(
                f"{self.base_url}/avatars",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True, 
                    "data": data,
                    "message": f"Retrieved {len(data.get('avatars', []))} avatars"
                }
            elif response.status_code == 401:
                return {
                    "success": False,
                    "error": "Unauthorized - API key invalid or expired",
                    "status_code": 401
                }
            elif response.status_code == 403:
                return {
                    "success": False,
                    "error": "Forbidden - Account may not have API access",
                    "status_code": 403
                }
            elif response.status_code == 404:
                return {
                    "success": False,
                    "error": "Avatars endpoint not found - API structure may have changed",
                    "status_code": 404
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "status_code": response.status_code
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Network error: {str(e)}",
                "troubleshooting": "Check internet connection and try again"
            }
    
    def create_video(self, 
                    script: str, 
                    avatar_id: str = "02e3638f-2e2b-4f41-93dd-6dea6fdf2565",
                    title: str = "AI Generated Sales Video") -> Dict[str, Any]:
        """
        Create a video using Synthesia API with proper error handling
        """
        if not script or not avatar_id:
            return {
                "success": False,
                "error": "Script and avatar_id are required"
            }
        
        # Correct payload format for Synthesia API
        payload = {
            "title": title,
            "scenes": [
                {
                    "elements": [
                        {
                            "type": "avatar",
                            "avatar_id": avatar_id,
                            "script": {
                                "type": "text",
                                "text": script
                            }
                        }
                    ]
                }
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/videos",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code in [200, 201]:
                try:
                    data = response.json()
                    return {
                        "success": True,
                        "video_id": data.get("id"),
                        "data": data,
                        "message": "Video creation started successfully"
                    }
                except:
                    return {
                        "success": True,
                        "message": "Video created but response parsing failed",
                        "raw_response": response.text
                    }
            elif response.status_code == 401:
                return {
                    "success": False,
                    "error": "Unauthorized - Check API key",
                    "status_code": 401
                }
            elif response.status_code == 403:
                return {
                    "success": False,
                    "error": "Forbidden - Account may lack permissions or credits",
                    "status_code": 403
                }
            elif response.status_code == 400:
                return {
                    "success": False,
                    "error": f"Bad Request - Invalid payload: {response.text}",
                    "status_code": 400,
                    "payload_sent": payload
                }
            elif response.status_code == 404:
                return {
                    "success": False,
                    "error": "Videos endpoint not found - API structure may have changed",
                    "status_code": 404
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "status_code": response.status_code,
                    "payload_sent": payload
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Network error: {str(e)}",
                "payload_sent": payload
            }
    
    def get_video_status(self, video_id: str) -> Dict[str, Any]:
        """Get video status with error handling"""
        if not video_id:
            return {"success": False, "error": "Video ID is required"}
        
        try:
            response = requests.get(
                f"{self.base_url}/videos/{video_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Network error: {str(e)}"}
    
    def wait_for_video_completion(self, video_id: str, max_wait_time: int = 600) -> Dict[str, Any]:
        """Wait for video to complete processing"""
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            status_result = self.get_video_status(video_id)
            
            if not status_result.get("success"):
                return status_result
            
            video_data = status_result["data"]
            status = video_data.get("status", "").lower()
            
            if status == "complete":
                return {
                    "success": True,
                    "status": "complete",
                    "download_url": video_data.get("download"),
                    "data": video_data
                }
            elif status in ["failed", "error"]:
                return {
                    "success": False,
                    "status": status,
                    "error": video_data.get("error", "Video generation failed")
                }
            
            # Wait before next check
            time.sleep(15)
        
        return {
            "success": False,
            "status": "timeout",
            "error": f"Video generation timed out after {max_wait_time} seconds"
        }
