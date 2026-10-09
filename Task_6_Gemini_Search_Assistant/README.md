# Task 6 — Gemini Assistant with Conversation Memory and Google Search

## Objective

Integrate Google Gemini in Python, preserve previous conversation turns, and use Google Search grounding for current information such as prices, weather, news, or other time-sensitive questions.

## Why this implementation

This project uses Google's current `google-genai` Python SDK and the Gemini Interactions API. The Interactions API supports multi-turn state using `previous_interaction_id`. Current Gemini documentation also supports a `google_search` tool that automatically performs web searches and returns citations for grounded answers.

## Requirements

- Python 3.10+
- A Gemini API key from Google AI Studio
- Internet connection while using Task 6

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your key:

```text
GEMINI_API_KEY=your_api_key_here
```

## Run

```bash
python assistant.py
```

### Suggested demo

```text
You: My name is Atharva and I am a computer engineering student.
Assistant: ...

You: What did I tell you my name was?
Assistant: ...

You: What is the current price of Bitcoin in USD?
Assistant: ... (grounded with Google Search when search is selected)
```

The assistant also accepts:

- `/search on` — enable Google Search grounding for the next turns
- `/search off` — disable Google Search grounding
- `/reset` — start a fresh conversation
- `/help` — show commands
- `/exit` — close the program

## Notes on API and privacy

The API key is loaded from `.env` and is not stored in source code. Do not commit `.env` to Git.

Google Search grounding is an API feature of Gemini that can retrieve current public web information and expose citations in the response metadata. Search-enabled requests may incur usage charges depending on the model/account configuration.
