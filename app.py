import streamlit as st
import os
from dotenv import load_dotenv
from hedra_client import HedraClient
from script_generator import ScriptGenerator
from openai_client import OpenAIClient
import time

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="AI Sales Video Generator",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 AI Sales Video Generator")
st.markdown("Generate personalized sales videos with AI-powered scripts and talking avatars using **Hedra AI**")

# Sidebar for API configuration
st.sidebar.header("🔧 Configuration")

# Check API keys
openai_key = os.getenv("OPENAI_API_KEY")
hedra_key = os.getenv("HEDRA_API_KEY")

if openai_key:
    st.sidebar.success("✅ OpenAI API key configured")
else:
    st.sidebar.error("❌ OpenAI API key missing")
    st.sidebar.info("Add OPENAI_API_KEY to your .env file")

if hedra_key:
    st.sidebar.success("✅ Hedra API key configured")
else:
    st.sidebar.error("❌ Hedra API key missing")
    st.sidebar.info("Add HEDRA_API_KEY to your .env file")

# Test API connections
st.subheader("🔗 API Connection Status")

# Initialize clients
try:
    openai_client = OpenAIClient()
    hedra_client = HedraClient()
    
    # Test OpenAI connection
    with st.spinner("Testing OpenAI connection..."):
        openai_test = openai_client.test_connection()
        
    if openai_test["success"]:
        st.success("✅ OpenAI API: Connected successfully")
    else:
        st.error(f"❌ OpenAI API: {openai_test['error']}")
        st.info("💡 Check your OpenAI API key in the .env file")
    
    # Show Hedra connection status
    if hedra_key:
        st.success("✅ Hedra AI: API key configured")
        st.info(f"🔗 API Endpoint: {hedra_client.base_url}")
        st.info("🎤 Voice: Will use first available voice from API")
    else:
        st.error("❌ Hedra AI: API key missing")
        st.info("💡 Add HEDRA_API_KEY to your .env file")
        
except Exception as e:
    st.error(f"❌ Initialization Error: {str(e)}")
    st.info("💡 Check your .env file and API keys")

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Video Details")
    
    # Input fields
    company_name = st.text_input("Company Name", placeholder="Enter target company name")
    contact_name = st.text_input("Contact Name", placeholder="Enter contact person's name")
    product_service = st.text_area("Product/Service Description", 
                                 placeholder="Describe your product or service")
    key_benefits = st.text_area("Key Benefits", 
                              placeholder="List the main benefits for the prospect")
    call_to_action = st.text_input("Call to Action", 
                                 placeholder="What action do you want them to take?")
    
    # Avatar selection
    st.subheader("🎭 Avatar Configuration")
    st.info("Using your configured Hedra avatar and voice settings")
    
    # Video settings
    st.subheader("🎥 Video Settings")
    aspect_ratio = st.selectbox("Aspect Ratio", ["16:9", "9:16", "1:1"], index=0)
    
    # Generate script button
    if st.button("🤖 Generate Script", type="primary"):
        if all([company_name, contact_name, product_service, key_benefits, call_to_action]):
            with st.spinner("Generating personalized script..."):
                try:
                    script_gen = ScriptGenerator()
                    script = script_gen.generate_sales_script(
                        company_name=company_name,
                        contact_name=contact_name,
                        product_service=product_service,
                        key_benefits=key_benefits,
                        call_to_action=call_to_action
                    )
                    st.session_state.generated_script = script
                    st.success("✅ Script generated successfully!")
                except Exception as e:
                    st.error(f"❌ Error generating script: {str(e)}")
                    st.info("Please check your OpenAI API key in the .env file")
        else:
            st.error("Please fill in all fields to generate a script")

with col2:
    st.header("🎬 Video Generation")
    
    # Display generated script
    if 'generated_script' in st.session_state:
        st.subheader("Generated Script")
        script_text = st.text_area("Script (editable)", 
                                 value=st.session_state.generated_script, 
                                 height=200)
        
        # Voice configuration
        st.subheader("🎤 Voice Configuration")
        st.info("✅ Using Hedra AI voice: **tara** (built-in text-to-speech)")
        st.markdown("*Hedra will automatically generate audio from your script text*")
        
        # Video generation
        if st.button("🎥 Create Video", type="primary"):
            if openai_key and hedra_key:
                with st.spinner("🎬 Creating video with Hedra AI..."):
                    try:
                        # Use the new create_video_complete method
                        result = hedra_client.create_video_complete(
                            script_text=script_text,
                            aspect_ratio=aspect_ratio,
                            voice_id="default"  # Will use first available voice
                        )
                        
                        if result["success"]:
                            st.success(f"✅ {result['message']}")
                            
                            # Display video URL
                            video_url = result["video_url"]
                            st.subheader("🎬 Your Generated Video")
                            st.video(video_url)
                            
                            # Download button
                            st.markdown(f"**Video URL:** {video_url}")
                            st.markdown("*Right-click the video above and select 'Save video as...' to download*")
                            
                            # Show job details
                            with st.expander("📋 Generation Details"):
                                st.json({
                                    "job_id": result["job_id"],
                                    "status": result["status"],
                                    "video_url": video_url
                                })
                                
                        else:
                            error_msg = result.get('error', 'Unknown error')
                            st.error(f"❌ Video generation failed: {error_msg}")
                            
                            # Provide specific guidance based on error
                            if "authenticate" in error_msg.lower() or "403" in str(result.get('status_code', '')):
                                st.warning("🔑 **API Key Authentication Issue**")
                                st.info("""
                                **Possible Solutions:**
                                1. **Verify API Key**: Check if your API key is correct
                                2. **Account Upgrade**: Ensure you have a paid Hedra subscription
                                3. **API Access**: Enable API access in your Hedra dashboard
                                4. **Contact Support**: Reach out to Hedra support for API activation
                                """)
                                
                                with st.expander("🔧 Troubleshooting Steps"):
                                    st.markdown("""
                                    **Step 1: Check Your Hedra Account**
                                    - Log into [Hedra Dashboard](https://app.hedra.com)
                                    - Verify you have a paid subscription
                                    - Look for API access settings
                                    
                                    **Step 2: Verify API Key**
                                    - Go to API settings in your dashboard
                                    - Regenerate your API key if needed
                                    - Update your .env file with the new key
                                    
                                    **Step 3: Contact Support**
                                    - Email: support@hedra.com
                                    - Request API access activation
                                    - Mention you're using the mercury API endpoint
                                    """)
                            
                            # Show debug details
                            with st.expander("🔍 Debug Details"):
                                st.json(result)
                                
                    except Exception as e:
                        st.error(f"❌ Unexpected error: {str(e)}")
                        st.info("Please check your API configuration and try again")
                        
            else:
                st.error("Please configure your API keys in the .env file first")
                
                # Show setup instructions
                with st.expander("📝 Setup Instructions"):
                    st.markdown("""
                    **1. Create .env file** in your project directory with:
                    ```
                    OPENAI_API_KEY=your_openai_key_here
                    HEDRA_API_KEY=your_hedra_key_here
                    ```
                    
                    **2. Get API Keys:**
                    - **OpenAI**: [platform.openai.com](https://platform.openai.com/api-keys)
                    - **Hedra**: [app.hedra.com](https://app.hedra.com) → API Settings
                    
                    **3. Restart the app** after adding keys
                    """)
    else:
        st.info("👆 Generate a script first to create your video")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, OpenAI, and Hedra AI")
