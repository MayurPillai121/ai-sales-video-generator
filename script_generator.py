import openai
import os
from typing import Dict, Any, Optional

class ScriptGenerator:
    """
    AI-powered script generator for sales videos using OpenAI
    """
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        # Set the API key for the openai module
        openai.api_key = api_key
        
        # Initialize client with minimal parameters
        try:
            self.client = openai.OpenAI()
        except Exception as e:
            # Fallback: try with just the API key
            try:
                self.client = openai.OpenAI(api_key=api_key)
            except Exception as e2:
                raise ValueError(f"Failed to initialize OpenAI client: {str(e2)}")
    
    def generate_sales_script(self,
                            company_name: str,
                            contact_name: str,
                            product_service: str,
                            key_benefits: str,
                            call_to_action: str,
                            tone: str = "professional",
                            duration: str = "60-90 seconds") -> str:
        """
        Generate a personalized sales script using OpenAI
        
        Args:
            company_name: Name of the target company
            contact_name: Name of the contact person
            product_service: Description of the product/service
            key_benefits: Key benefits to highlight
            call_to_action: Desired action from the prospect
            tone: Tone of the script (professional, friendly, casual)
            duration: Target duration of the video
        
        Returns:
            Generated sales script as a string
        """
        
        prompt = f"""
        Create a personalized sales video script with the following details:
        
        Target Company: {company_name}
        Contact Person: {contact_name}
        Product/Service: {product_service}
        Key Benefits: {key_benefits}
        Call to Action: {call_to_action}
        Tone: {tone}
        Duration: {duration}
        
        Requirements:
        1. Start with a personalized greeting using the contact's name and company
        2. Quickly establish credibility and relevance
        3. Present the product/service in a compelling way
        4. Highlight the key benefits specifically for their company
        5. Include a clear and compelling call to action
        6. Keep it conversational and engaging
        7. Ensure the script is appropriate for a {duration} video
        8. Use a {tone} tone throughout
        
        Format the script as natural speech that would work well for an AI avatar.
        Avoid overly complex sentences and include natural pauses.
        
        Script:
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert sales copywriter specializing in creating compelling, personalized video scripts for B2B sales outreach. Your scripts are known for being engaging, concise, and highly effective at generating responses."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error generating script: {str(e)}"
    
    def generate_follow_up_script(self,
                                company_name: str,
                                contact_name: str,
                                original_script: str,
                                response_type: str = "no_response") -> str:
        """
        Generate a follow-up script based on the original outreach
        
        Args:
            company_name: Name of the target company
            contact_name: Name of the contact person
            original_script: The original script that was sent
            response_type: Type of response received (no_response, interested, not_interested)
        
        Returns:
            Generated follow-up script
        """
        
        prompt = f"""
        Create a follow-up sales video script based on the previous outreach:
        
        Target Company: {company_name}
        Contact Person: {contact_name}
        Response Type: {response_type}
        
        Original Script:
        {original_script}
        
        Requirements for follow-up:
        1. Reference the previous message appropriately
        2. Provide additional value or information
        3. Address potential concerns based on the response type
        4. Include a softer, more consultative approach
        5. Keep it shorter than the original (30-45 seconds)
        6. End with a low-pressure call to action
        
        Script:
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at creating follow-up sales messages that are helpful, non-pushy, and focused on providing value to the prospect."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=600,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error generating follow-up script: {str(e)}"
    
    def optimize_script_for_avatar(self, script: str, avatar_style: str = "professional") -> str:
        """
        Optimize a script for better delivery by an AI avatar
        
        Args:
            script: The original script
            avatar_style: Style of the avatar (professional, friendly, casual)
        
        Returns:
            Optimized script with better pacing and delivery cues
        """
        
        prompt = f"""
        Optimize this sales script for delivery by an AI avatar with a {avatar_style} style:
        
        Original Script:
        {script}
        
        Optimization requirements:
        1. Add natural pauses where appropriate (indicate with [pause])
        2. Break up long sentences into shorter, more natural phrases
        3. Ensure pronunciation-friendly words
        4. Add emphasis markers where needed (indicate with *emphasis*)
        5. Make it sound more conversational and natural
        6. Maintain the original message and call to action
        7. Ensure smooth flow for AI voice synthesis
        
        Optimized Script:
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in optimizing scripts for AI avatar delivery, ensuring natural speech patterns and effective communication."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=600,
                temperature=0.5
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error optimizing script: {str(e)}"
    
    def generate_script_variations(self,
                                 base_script: str,
                                 num_variations: int = 3) -> list:
        """
        Generate multiple variations of a script for A/B testing
        
        Args:
            base_script: The base script to create variations from
            num_variations: Number of variations to generate
        
        Returns:
            List of script variations
        """
        
        variations = []
        
        for i in range(num_variations):
            prompt = f"""
            Create a variation of this sales script while maintaining the core message:
            
            Base Script:
            {base_script}
            
            Variation #{i+1} requirements:
            1. Keep the same key points and call to action
            2. Change the opening approach
            3. Vary the language and phrasing
            4. Maintain the same approximate length
            5. Make it feel fresh and different from the original
            
            Variation:
            """
            
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a creative copywriter skilled at creating fresh variations of sales messages while maintaining their effectiveness."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=600,
                    temperature=0.8
                )
                
                variations.append(response.choices[0].message.content.strip())
                
            except Exception as e:
                variations.append(f"Error generating variation {i+1}: {str(e)}")
        
        return variations
