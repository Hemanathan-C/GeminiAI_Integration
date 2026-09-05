# LLM Experiments

A personal playground of small, independent scripts exploring different ways of working with LLMs: multi-provider chat, a tool-calling agent, image captioning, a PDF RAG pipeline, and a voice assistant. Each folder/script is standalone — pick the one you want and run it.

## Contents

| Path | What it does |
|---|---|
| [gemini_integration.py](gemini_integration.py) | Terminal chatbot using Google's Gemini API, keeps conversation context. |
| [agent.py](agent.py) | An agent that plans over START/PLAN/TOOL/OUTPUT steps (via Gemini's OpenAI-compatible endpoint) and can call a weather-lookup tool or run shell commands. |
| [image/main.py](image/main.py) | Sends a public image URL to GPT-4o and prints a generated caption. |
| [rag/index.py](rag/index.py) + [rag/chat.py](rag/chat.py) | RAG pipeline: chunks a PDF, embeds it into a Qdrant vector store, then answers questions with page-number citations from retrieved chunks. |
| [voice_agent/main.py](voice_agent/main.py) | Voice assistant: listens via microphone, transcribes with Google Speech Recognition, replies with GPT-4o-mini, and speaks the answer back with OpenAI TTS. |

## Prerequisites

- Python 3.7+
- API keys for the providers you want to use: Gemini, OpenAI, and/or Groq
- Docker (only needed for the RAG pipeline, to run Qdrant)
- A working microphone (only needed for the voice agent)

## Setup

1. **Clone this repository:**
   ```sh
   git clone https://github.com/YOUR-USERNAME/GeminiAI_Integration.git
   cd GeminiAI_Integration
   ```

2. **Create `env.py` in the project root** with the keys you need (only used by the root-level and `image/` scripts):
   ```python
   GEMINI_API_KEY = "your_gemini_api_key_here"
   GROQ_API_KEY = "your_groq_api_key_here"
   OPEN_API_KEY = "your_openai_api_key_here"
   ```
   `env.py` is already in `.gitignore` and will not be tracked by Git. **Never commit real API keys.**

   The `rag/` and `voice_agent/` scripts instead read from a `.env` file (via `python-dotenv`) with standard variable names, e.g.:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Install dependencies** for the script(s) you want to run:
   ```sh
   # Gemini chat
   pip install google-genai

   # agent.py (Gemini via OpenAI-compatible API + tool calling)
   pip install openai pydantic requests

   # image captioning
   pip install openai

   # RAG pipeline
   pip install python-dotenv langchain-openai langchain-qdrant langchain-community langchain-text-splitters openai

   # voice agent
   pip install python-dotenv SpeechRecognition openai pyaudio
   ```

## Usage

**Gemini chat:**
```sh
python gemini_integration.py
```
Type your message and press Enter. Type `exit`, `quit`, or `stop` to end.

**Agent with tools:**
```sh
python agent.py
```
Ask it something like "what's the weather in Delhi?" and watch it plan, call the tool, and respond.

**Image captioning:**
```sh
python image/main.py
```
Paste a public image URL when prompted.

**RAG pipeline:**
```sh
# 1. Start the vector database
cd rag
docker compose up -d

# 2. Place your PDF as rag/nodejs.pdf, then index it
python index.py

# 3. Ask questions against the indexed content
python chat.py
```

**Voice agent:**
```sh
python voice_agent/main.py
```
Speak into your microphone; the assistant transcribes, responds, and speaks back.

## Notes

- These are exploratory scripts, not a production system — expect minimal error handling and hardcoded values (e.g. `rag/index.py` expects a PDF named `nodejs.pdf`).
- Provider SDKs change quickly; API calls here may need updates if the underlying SDKs change their interfaces.
