# Gemini AI Integration

This file demonstrates a simple command-line interface for interacting with Google's Gemini AI model using Python.

## Features

- Chat with Gemini AI in your terminal
- Maintains conversation context
- Exits gracefully on command

## Prerequisites

- Python 3.7+
- A valid Gemini API key
- The `google-genai` Python package

## Setup

1. **Clone this repository:**
   ```sh
   git clone https://github.com/YOUR-USERNAME/GeminiAI_Integration.git
   cd GeminiAI_Integration
   ```

2. **Install dependencies:**
   ```sh
   pip install google-genai
   ```

3. **Set up your API key:**
   - Create a file named `env.py` in the project directory:
     ```python
     GEMINI_API_KEY = "your_actual_gemini_api_key_here"
     ```
   - **Do not share your API key.**  
   - `env.py` is already in `.gitignore` and will not be tracked by Git.

## Usage

Run the script:

```sh
python gemini_integration.py
```

You will see a prompt to chat with Gemini AI.  
Type your message and press Enter.  
Type `exit`, `quit`, or `stop` to end the conversation.

## Notes

- This script uses a simple conversation list. For production use, consider more robust conversation management and error handling.
- The Gemini API usage in this script may need to be updated if the `google-genai` SDK changes.
