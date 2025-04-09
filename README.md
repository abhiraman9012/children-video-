# AI-Powered Children's Story Video Generator

## Overview

This project is a comprehensive automated system that uses Google's Gemini AI models to generate complete children's stories with matching images, converts the text to speech, and compiles everything into a professional-quality video with effects and transitions. The generated videos include YouTube-ready metadata (titles, descriptions, and tags) and can be automatically uploaded to Google Drive.

## Table of Contents

- [System Architecture](#system-architecture)
- [Code Structure](#code-structure)
- [Data Flow](#data-flow)
- [Module Details](#module-details)
- [Installation and Requirements](#installation-and-requirements)
- [Usage](#usage)
- [Technical Highlights](#technical-highlights)

## System Architecture

The system employs a modular architecture with specific components handling different aspects of the generation pipeline:

1. **AI Content Generation Layer**: Uses Google's Gemini models to generate story text and images
2. **Media Processing Layer**: Handles text-to-speech conversion and image optimization
3. **Video Production Layer**: Combines audio and images with professional effects
4. **Storage & Distribution Layer**: Uploads content to Google Drive with metadata

Each component is designed to function both independently and as part of the complete pipeline, with robust error handling and retry mechanisms throughout.

## Code Structure

The codebase is organized into multiple Python modules, each handling specific functionality:

```
divided_code/
├── setup.py                  # Library installations and imports
├── api_config.py             # API key configuration and safety settings
├── google_drive_utils.py     # Google Drive API integration utilities
├── prompt_generation.py      # Story prompt generation using Gemini models
├── retry_mechanisms.py       # Robust retry logic for API calls and generation
├── collect_story.py          # Story text processing and cleaning
├── generate_part1.py         # Main generation initialization
├── generate_part2.py         # Stream processing for Gemini responses
├── generate_part3.py         # Text-to-speech generation
├── generate_part4.py         # Video preparation code
├── generate_part5.py         # Video effects and transitions
├── generate_part6.py         # Video processing execution
├── google_drive_upload.py    # Google Drive upload functionality
├── direct_download.py        # Local download options
├── seo_metadata.py           # YouTube metadata generation
├── thumbnail_generation.py   # Video thumbnail creation
└── main.py                   # Main entry point coordinating all modules
```

## Data Flow

```
┌────────────────────┐    ┌────────────────────┐    ┌────────────────────┐
│   Input & Config   │    │  Content Generation │    │  Media Processing  │
│                    │    │                    │    │                    │
│ - API Keys         │───►│ - Story Generation │───►│ - Text-to-Speech   │
│ - Safety Settings  │    │ - Image Generation │    │ - Image Resizing   │
│ - Prompt Templates │    │ - Content Cleaning │    │ - Audio Processing │
└────────────────────┘    └────────────────────┘    └─────────┬──────────┘
                                                                │
                                                                ▼
┌────────────────────┐    ┌────────────────────┐    ┌────────────────────┐
│   Final Delivery   │    │  Content Packaging │    │  Video Production  │
│                    │◄───│                    │◄───│                    │
│ - Google Drive     │    │ - SEO Metadata     │    │ - FFmpeg Effects   │
│   Upload           │    │ - Thumbnail        │    │ - Transitions      │
│ - Direct Download  │    │ - YouTube Ready    │    │ - Video Rendering  │
└────────────────────┘    └────────────────────┘    └────────────────────┘
```

## Module Details

### setup.py
- Contains necessary library installations (Google Generative AI, Pillow, Kokoro, etc.)
- Imports required modules for image/audio processing

### api_config.py
- Manages API keys for Gemini models (selects randomly from available keys)
- Defines safety settings for content generation
- Tests API connectivity

### google_drive_utils.py
- Provides Google Drive file download functionality
- Tests Google Drive API connectivity
- Validates credentials

### prompt_generation.py
- Uses `gemini-2.0-flash-thinking-exp-01-21` model to create story prompts
- Ensures prompts have consistent structure for reliable results
- Includes formatting validation and correction mechanisms

### retry_mechanisms.py
- Implements robust error handling and retry logic for API calls
- Persistent story generation retry functionality
- Monitors generation quality and completeness

### collect_story.py
- Extracts and cleans story text from AI-generated content
- Uses multiple parsing strategies for reliable extraction
- Handles various text formats and structures

### generate_part1.py through generate_part6.py
- The core generation pipeline split into manageable components:
  - Part1: Initialization and prompt setup
  - Part2: API streaming interface and content collection
  - Part3: Text-to-speech conversion
  - Part4: Video preparation with image processing
  - Part5: Video effects and transitions definition
  - Part6: Video processing execution

### google_drive_upload.py
- Manages the upload of generated content to Google Drive
- Creates organized folder structure
- Uploads videos, thumbnails, and metadata

### direct_download.py
- Provides fallback for local downloads when Google Drive is unavailable

### seo_metadata.py
- Generates YouTube-optimized titles, descriptions, and tags
- Uses AI analysis of story content
- Includes fallback mechanisms

### thumbnail_generation.py
- Creates professional YouTube thumbnails
- Adds title overlays and graphics
- Optimizes images for YouTube

### main.py
- Coordinates the entire generation pipeline
- Imports and organizes all modules
- Entry point for the application

## Data Processing Pipeline

1. **Story Prompt Generation**
   - Input: Basic instructions
   - Process: Enhanced by Gemini AI model
   - Output: Structured story prompt

2. **Story & Image Generation**
   - Input: Enhanced prompt
   - Process: Gemini API generates text and images simultaneously
   - Output: Raw story text and image data

3. **Content Processing**
   - Input: Raw story text and images
   - Process: Text cleaning, segment extraction, image saving
   - Output: Clean story segments and optimized images

4. **Audio Generation**
   - Input: Clean story text
   - Process: Kokoro TTS converts text to natural speech
   - Output: High-quality audio file

5. **Video Production**
   - Input: Images and audio
   - Process: FFmpeg processing with effects and transitions
   - Output: Complete video file

6. **Metadata Generation**
   - Input: Story content
   - Process: AI-powered SEO analysis
   - Output: YouTube-optimized title, description, and tags

7. **Delivery**
   - Input: Video file and metadata
   - Process: Google Drive upload or direct download
   - Output: Accessible content

## Technical Highlights

### AI Model Integration
- Primary story/image generation: `gemini-2.0-flash-exp-image-generation`
- Prompt enhancement: `gemini-2.0-flash-thinking-exp-01-21`
- Safety settings customized for child-friendly content

### Robust Error Handling
- Multiple fallback mechanisms for API failures
- Persistent retries with exponential backoff
- Comprehensive API error monitoring

### Video Production Quality
- Professional Ken Burns-style effects
- Dynamic transitions based on story position
- High-quality encoding parameters

### Content Optimization
- SEO-optimized metadata generation
- Professional thumbnail generation
- Proper YouTube aspect ratios (16:9)

## Installation and Requirements

### Installation with pip

You can install all required Python dependencies using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Required Libraries

The requirements.txt file includes the following dependencies:

```python
# Core libraries
google-generativeai>=0.6.0
IPython>=8.10.0
Pillow>=10.0.0

# Google Drive integration
google-auth>=2.28.0
google-auth-oauthlib>=1.2.0
google-auth-httplib2>=0.1.1
google-api-python-client>=2.120.0

# Audio processing
kokoro>=0.9.2
soundfile>=0.12.1
numpy>=1.24.0

# Media processing
matplotlib>=3.7.0
requests>=2.28.2
```

### System Dependencies

You will also need to install the following system dependencies:

```
# System dependencies
ffmpeg (system installation required)
espeak-ng (for speech synthesis)
```

## Google Colab Notebook

You can run this project directly in Google Colab using the following notebook code. Copy this code into a new Colab notebook to get started:

```python
# AI-Powered Children's Story Video Generator - Google Colab Notebook

# Clone the repository
!git clone https://github.com/abhiraman9012/children-video-.git
%cd children-video-

# Install required dependencies
!pip install google-generativeai
!pip install IPython pillow
!pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
!pip install kokoro>=0.9.2 soundfile

# Install system dependencies
!apt-get update
!apt-get install -y ffmpeg
!apt-get install -y espeak-ng

# Note: This code already includes Google Drive API functionality through google_drive_upload.py
# No additional drive mounting is needed

# Create a folder for outputs
!mkdir -p /content/outputs

# Import necessary modules from the project
import os
import sys

# Set up your API key
import os
os.environ["GEMINI_API_KEY"] = "YOUR_GEMINI_API_KEY"  # Replace with your actual Gemini API key

# Run the application
print("Setting up modules...")

# Execute the main file with all modules imported
exec(open("setup.py").read())
exec(open("api_config.py").read())
exec(open("google_drive_utils.py").read())
exec(open("prompt_generation.py").read())
exec(open("retry_mechanisms.py").read())
exec(open("collect_story.py").read())
exec(open("generate_part1.py").read())
exec(open("generate_part2.py").read())
exec(open("generate_part3.py").read())
exec(open("generate_part4.py").read())
exec(open("generate_part5.py").read())
exec(open("generate_part6.py").read())
exec(open("google_drive_upload.py").read())
exec(open("direct_download.py").read())
exec(open("seo_metadata.py").read())
exec(open("thumbnail_generation.py").read())

print("Starting story generation...")
# Call the main story generation function
retry_story_generation(use_prompt_generator=True)
print("Story generation complete!")
```

### Using the Colab Notebook

1. Create a new notebook in Google Colab
2. Copy and paste the code above
3. Replace `YOUR_GEMINI_API_KEY` with your actual Gemini API key
4. Run each cell in sequence
5. The code will use its built-in Google Drive API functionality (in google_drive_upload.py) to handle uploads
6. The generated video will be displayed in the notebook and can also be downloaded directly

### Troubleshooting Colab Issues

- If you encounter memory errors, try using a Colab Pro subscription for more resources
- For TTS issues, you may need to restart the runtime after installing dependencies
- If Google Drive API uploads fail, check your API credentials or use the direct download option

## Usage

### Basic Usage

1. Install all required dependencies
2. Configure Google API keys in `api_config.py`
3. Run `main.py`

### Customization Options

- Modify prompt templates in `prompt_generation.py`
- Adjust safety settings in `api_config.py`
- Change video effects in `generate_part5.py`

## Implementation Notes

### Streaming API Usage
- The code prioritizes streaming API for better performance
- Includes fallback to non-streaming when JSON errors occur

### Memory Management
- Temporary files are used for large media storage
- Cleanup operations included after processing

### Security Considerations
- API keys are randomly selected from a pool
- Google Drive credentials stored securely

---

## Performance Optimization

The system includes several optimizations for reliability and quality:

1. **Adaptive Retry Logic**: Intelligent retry mechanisms detect specific failure modes and adjust accordingly

2. **Quality Validation**: Checks for minimum story segment count and image quality

3. **Resource Efficiency**: Uses streaming APIs where possible to minimize memory usage

4. **Parallel Processing**: Leverages parallel processing for intensive operations

5. **Format Compatibility**: Ensures output is compatible with YouTube and other platforms

---

This project represents a complete end-to-end solution for AI-powered content creation, combining Google's Gemini models with professional media processing to generate high-quality children's story videos automatically.
