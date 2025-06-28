#!/usr/bin/env python3
"""
Hedra API Client - FINAL VERSION using Official OpenAPI Spec
"""

import os
import time
import requests
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class HedraClient:
    def __init__(self, api_key: str = None):
        """Initialize Hedra client with official OpenAPI spec configuration"""
        self.api_key = api_key or os.getenv("HEDRA_API_KEY")
        if not self.api_key:
            raise ValueError("HEDRA_API_KEY not found in environment variables")
        
        # OFFICIAL OpenAPI spec configuration
        self.base_url = "https://mercury.dev.dream-ai.com/api"
        self.headers = {
            "X-API-Key": self.api_key,  # CORRECT: X-API-Key (case-sensitive!)
            "Content-Type": "application/json"
        }
        
        logger.info(f"Initialized Hedra client with API: {self.base_url}")
    
    def get_available_voices(self) -> list:
        """Get list of available voices from /v1/voices"""
        try:
            response = requests.get(
                f"{self.base_url}/v1/voices",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                voices_data = response.json()
                return voices_data.get("supported_voices", [])
            else:
                logger.warning(f"Could not fetch voices: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching voices: {e}")
            return []
    
    def create_video_complete(self, script_text: str, voice_id: str = "default", aspect_ratio: str = "16:9") -> Dict[str, Any]:
        """
        Generate video using TTS and AI-generated avatar - OFFICIAL OpenAPI spec
        No file uploads needed - everything in one call!
        """
        try:
            logger.info(f"Creating video with script length: {len(script_text)} characters")
            
            # OFFICIAL payload structure from OpenAPI spec
            payload = {
                "text": script_text,
                "audioSource": "tts",  # Use built-in TTS
                "voiceId": voice_id,
                "aspectRatio": aspect_ratio,
                "avatarImageInput": {
                    "seed": 42,
                    "prompt": "Professional business person presenting, confident smile, business attire, clean background"
                }
            }
            
            logger.info("Submitting to /v1/characters endpoint...")
            response = requests.post(
                f"{self.base_url}/v1/characters",
                json=payload,
                headers=self.headers,
                timeout=60
            )
            
            if response.status_code == 200:
                job_data = response.json()
                job_id = job_data.get("jobId")
                
                if job_id:
                    logger.info(f"Video generation started! Job ID: {job_id}")
                    
                    # Wait for completion and return result
                    return self.wait_for_completion(job_id)
                else:
                    return {
                        "success": False,
                        "error": "No jobId returned from API",
                        "response": job_data
                    }
            else:
                return {
                    "success": False,
                    "error": f"Video generation failed: {response.text}",
                    "status_code": response.status_code
                }
                
        except Exception as e:
            logger.error(f"Video generation error: {str(e)}")
            return {
                "success": False,
                "error": f"Video generation error: {str(e)}"
            }
    
    def wait_for_completion(self, job_id: str, max_wait_time: int = 300) -> Dict[str, Any]:
        """
        Wait for video generation to complete using /v1/projects/{jobId}
        Official status values: Queued, InProgress, Completed, Failed
        """
        start_time = time.time()
        logger.info(f"Waiting for job {job_id} to complete...")
        
        while time.time() - start_time < max_wait_time:
            try:
                # Check status using OFFICIAL endpoint
                response = requests.get(
                    f"{self.base_url}/v1/projects/{job_id}",
                    headers=self.headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    project = response.json()
                    status = project.get("status")
                    progress = project.get("progress", 0)
                    
                    logger.info(f"Job {job_id} status: {status} ({progress}% complete)")
                    
                    if status == "Completed":
                        video_url = project.get("videoUrl")
                        if video_url:
                            return {
                                "success": True,
                                "video_url": video_url,
                                "job_id": job_id,
                                "status": status,
                                "message": "Video generation completed successfully!"
                            }
                        else:
                            return {
                                "success": False,
                                "error": "Video completed but no videoUrl found",
                                "job_id": job_id,
                                "data": project
                            }
                            
                    elif status == "Failed":
                        return {
                            "success": False,
                            "error": project.get("errorMessage", "Video generation failed"),
                            "job_id": job_id,
                            "status": status
                        }
                        
                    elif status in ["Queued", "InProgress"]:
                        # Still processing - wait and continue
                        time.sleep(10)
                        continue
                    else:
                        logger.warning(f"Unknown status: {status}")
                        time.sleep(10)
                        continue
                        
                else:
                    logger.error(f"Status check failed: {response.status_code} - {response.text}")
                    time.sleep(10)
                    continue
                    
            except Exception as e:
                logger.error(f"Status check error: {e}")
                time.sleep(10)
                continue
                
        return {
            "success": False,
            "error": f"Video generation timed out after {max_wait_time} seconds",
            "job_id": job_id
        }
    
    def download_video(self, video_url: str, output_filename: str = "hedra_video.mp4") -> Dict[str, Any]:
        """Download video from URL"""
        try:
            logger.info(f"Downloading video from: {video_url}")
            
            response = requests.get(video_url, stream=True, timeout=60)
            response.raise_for_status()
            
            with open(output_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Video downloaded successfully: {output_filename}")
            return {
                "success": True,
                "video_path": output_filename,
                "message": f"Video downloaded: {output_filename}"
            }
            
        except Exception as e:
            logger.error(f"Download error: {str(e)}")
            return {
                "success": False,
                "error": f"Download error: {str(e)}"
            }
    
    # Alias for backward compatibility
    def create_video(self, audio_text: str, aspect_ratio: str = "16:9", voice_id: str = "default", **kwargs) -> Dict[str, Any]:
        """Alias for create_video_complete"""
        return self.create_video_complete(audio_text, voice_id, aspect_ratio)
