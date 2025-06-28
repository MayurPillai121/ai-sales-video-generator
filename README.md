# 🎬 AI Sales Video Generator

A powerful Streamlit application that generates personalized sales videos using OpenAI for script generation and Hedra AI for professional AI avatar video creation.

## Features

- 🤖 **AI-Powered Script Generation**: Uses OpenAI GPT-4 to create personalized sales scripts
- 🎥 **Video Creation**: Integrates with Hedra AI Mercury API for professional AI avatar videos
- 🎭 **AI Avatar Generation**: Dynamic AI avatars created from text prompts
- 🗣️ **Text-to-Speech**: Multiple professional voices available
- 📝 **Customizable Scripts**: Edit generated scripts before video creation
- 🎯 **Personalization**: Tailored content for specific companies and contacts
- 📊 **User-Friendly Interface**: Modern Streamlit interface with comprehensive error handling
- 🔧 **Professional Error Handling**: Built-in troubleshooting and support guidance

## Project Structure

```
ai_sales_video_generator/
├── app.py                      # Main Streamlit application
├── hedra_client.py            # Hedra AI Mercury API client
├── openai_client.py           # OpenAI script generation
├── synthesia_client.py        # Legacy Synthesia client (backup)
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (API keys)
├── hedra_api_tester.py        # Comprehensive API testing tool
├── test_hedra_final.py        # Integration testing
├── hedra_support_response.md  # Technical documentation for support
├── README_HEDRA_FIX.md        # Detailed implementation guide
└── README.md                  # This file
```

## Installation

1. **Navigate to the project directory**:
   ```bash
   cd D:\ai_sales_video_generator
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API Keys**:
   - Create a `.env` file and add your API keys:
   ```
   OPENAI_API_KEY=your_actual_openai_key
   HEDRA_API_KEY=your_actual_hedra_key
   ```

## API Keys Setup

### OpenAI API Key
1. Go to [OpenAI API](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key to your `.env` file

### Hedra AI API Key
1. Sign up at [Hedra AI](https://app.hedra.com)
2. Go to your account settings → API
3. Generate an API key
4. Copy the key to your `.env` file
5. **Note**: API access may require account activation - contact support@hedra.com if needed

## Usage

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```

2. **Fill in the video details**:
   - Company Name
   - Contact Name
   - Product/Service Description
   - Key Benefits
   - Call to Action

3. **Generate Script**:
   - Click "Generate Script" to create an AI-powered sales script
   - Review and edit the script as needed

4. **Create Video**:
   - Select an avatar
   - Click "Create Video" to generate your sales video
   - Wait for processing (may take a few minutes)

## Features Overview

### Script Generation
- Personalized greetings using contact and company names
- Professional tone and structure
- Optimized for AI avatar delivery
- Editable before video creation

### Video Creation
- AI-generated avatars from text prompts
- Professional text-to-speech voices
- High-quality video generation (16:9, 9:16, 1:1 aspect ratios)
- Automatic job status polling and completion tracking
- Direct video download links

### AI Avatar Features
- Dynamic avatar generation from prompts
- Professional business personas
- Customizable appearance and style
- Multiple voice options available

## File Descriptions

### `app.py`
Main Streamlit application with user interface for:
- Input forms for video details
- Script generation interface
- Video creation controls
- API key validation

### `hedra_client.py`
Hedra AI Mercury API client providing:
- Official OpenAPI specification implementation
- Character video generation with TTS
- Job status polling and completion tracking
- Video download functionality
- Comprehensive error handling

### `openai_client.py`
OpenAI integration for:
- Personalized script generation
- Professional sales copy creation
- Script optimization for AI avatars
- Business-focused content generation

## Dependencies

- **streamlit**: Modern web application framework
- **openai**: OpenAI API client for script generation
- **requests**: HTTP library for API calls
- **python-dotenv**: Environment variable management
- **time**: For polling and timeout handling

## Troubleshooting

### Common Issues

1. **Hedra API Authentication (403 Error)**:
   - **Most Common Issue**: API access not enabled on account
   - **Solution**: Contact support@hedra.com to activate API access
   - Ensure you have a paid Hedra subscription
   - Verify API key format: `sk_hedra_[64-character string]`

2. **OpenAI API Issues**:
   - Check your OpenAI API key and credits
   - Ensure all input fields are filled
   - Verify account has GPT-4 access

3. **Video Generation Issues**:
   - Hedra videos take 2-5 minutes to process
   - Check internet connection stability
   - Use the built-in troubleshooting guide in the app

4. **Network Connectivity**:
   - Run `python hedra_api_tester.py` for comprehensive diagnostics
   - Check firewall settings if requests timeout

## Future Enhancements

- [ ] Bulk video generation from CSV
- [ ] Custom avatar training
- [ ] Video analytics and tracking
- [ ] Integration with CRM systems
- [ ] Advanced script templates
- [ ] Multi-language support

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your API keys and account status
3. Review the Synthesia and OpenAI documentation

## License

This project is for educational and commercial use. Please ensure compliance with OpenAI and Synthesia terms of service.

---

## 🎯 Current Status

✅ **Fully Functional Features:**
- AI script generation (OpenAI integration)
- Beautiful Streamlit interface
- Professional error handling and user guidance
- Comprehensive API testing and diagnostics

🔧 **Hedra Integration:**
- Complete implementation following official OpenAPI spec
- Ready to work once API access is activated
- Professional troubleshooting and support documentation

## 📞 Support

For Hedra API access issues:
- **Email**: support@hedra.com
- **Subject**: "API Access Request - Mercury API Integration"
- **Include**: Your API key (first 20 characters) and account details

For general issues:
1. Check the built-in troubleshooting guide in the app
2. Run `python hedra_api_tester.py` for diagnostics
3. Review the comprehensive documentation in `README_HEDRA_FIX.md`

---

**Built with ❤️ using Streamlit, OpenAI, and Hedra AI**
