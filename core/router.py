from google.genai import types
from core.client import get_client
from config import ROUTER_MODEL, ROUTER_TEMPERATURE

_PROMPT = (
    "Classify the user message into exactly one category. "
    "Reply with ONLY the category name, nothing else.\n\n"
    "Categories:\n"
    "- chat: general conversation, greetings, opinions, explanations, creative writing\n"
    "- code: requests to write, run, debug, or execute Python code, or complex multi-step computations\n"
    "- search: questions about current events, real-time data, recent news, live scores, weather today, stock prices\n\n"
    "User message: {message}"
)


def classify(message: str) -> str:
    client = get_client()
    response = client.models.generate_content(
        model=ROUTER_MODEL,
        contents=_PROMPT.format(message=message),
        config=types.GenerateContentConfig(
            temperature=ROUTER_TEMPERATURE,
            max_output_tokens=10,
        ),
    )
    text = response.text
    if not text:
        return "chat"
    result = text.strip().lower()
    if result in ("chat", "code", "search"):
        return result
    return "chat"
