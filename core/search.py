from google.genai import types
from core.client import get_client
from config import MODEL, TEMPERATURE, MAX_OUTPUT_TOKENS


def query(message: str, persona_instruction: str) -> str:
    client = get_client()
    response = client.models.generate_content(
        model=MODEL,
        contents=message,
        config=types.GenerateContentConfig(
            system_instruction=persona_instruction,
            tools=[types.Tool(google_search=types.GoogleSearch())],
            temperature=TEMPERATURE,
            max_output_tokens=MAX_OUTPUT_TOKENS,
        ),
    )
    return response.text or "No results found."
