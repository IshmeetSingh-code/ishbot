# 🤖 IshBot

AI assistant powered by Google Gemini with multi-persona support, calculator, Python REPL, and web search.

## Quick Start

```bash
cp .env.example .env
# Add your Gemini API key to .env
docker compose up --build
```

Open [http://localhost:8501](http://localhost:8501)

## Features

- **Multi-Persona** — Switch between IshBot, Coder, Creative, Scientist, and Tutor
- **Calculator** — Safe AST-based math evaluation (sqrt, sin, cos, log, pi, e)
- **Python REPL** — Gemini-powered code execution sandbox
- **Web Search** — Real-time Google Search grounding
- **Streaming** — Real-time token streaming for chat responses
- **Smart Routing** — Automatic intent classification routes to the right tool

## Architecture

```
User → Streamlit UI → Intent Router → ┬─ Chat Mode (calculator tool)
                                       ├─ Code Mode (Gemini code_execution)
                                       └─ Search Mode (Google Search grounding)
```

## Personas

| Persona | Style |
|---------|-------|
| 🤖 IshBot | Sharp, concise, slightly witty |
| 👨‍💻 Coder | Expert programmer, code-first |
| 🎨 Creative | Imaginative storyteller |
| 🔬 Scientist | Analytical, data-driven |
| 📚 Tutor | Patient teacher, step-by-step |

## Local Development

```bash
pip install -r requirements.txt
export GEMINI_API_KEY=your_key
streamlit run app.py
```

## Tech Stack

- **Frontend**: Streamlit
- **LLM**: Google Gemini 2.0 Flash-Lite (free tier)
- **SDK**: google-genai
- **Container**: Docker (python:3.12-slim)

## Project Structure

```
ishbot/
├── app.py              # Streamlit UI
├── config.py           # Configuration and personas
├── core/
│   ├── client.py       # Gemini client
│   ├── router.py       # Intent classifier
│   ├── chat.py         # Chat mode + calculator
│   ├── code.py         # Code execution mode
│   ├── search.py       # Web search mode
│   └── tools.py        # Calculator (AST-safe)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

Built by **Ishmeet Singh**
