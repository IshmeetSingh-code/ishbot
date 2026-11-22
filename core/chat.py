from google.genai import types
from core.client import get_client
from core.tools import calculate
from config import MODEL, TEMPERATURE, MAX_OUTPUT_TOKENS


def create_session(persona_instruction: str):
    client = get_client()
    return client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=persona_instruction,
            tools=[calculate],
            temperature=TEMPERATURE,
            max_output_tokens=MAX_OUTPUT_TOKENS,
        ),
    )


def stream(session, message: str):
    for chunk in session.send_message_stream(message):
        if chunk.text:
            yield chunk.text
