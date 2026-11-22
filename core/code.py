from google.genai import types
from core.client import get_client
from config import MODEL, TEMPERATURE, MAX_OUTPUT_TOKENS


def execute(message: str, persona_instruction: str) -> dict:
    client = get_client()
    response = client.models.generate_content(
        model=MODEL,
        contents=message,
        config=types.GenerateContentConfig(
            system_instruction=persona_instruction,
            tools=[types.Tool(code_execution=types.ToolCodeExecution())],
            temperature=TEMPERATURE,
            max_output_tokens=MAX_OUTPUT_TOKENS,
        ),
    )
    result = {"text": "", "code": "", "output": ""}
    if not response.candidates or not response.candidates[0].content.parts:
        result["text"] = "No response generated."
        return result
    for part in response.candidates[0].content.parts:
        if part.text:
            result["text"] += part.text
        if part.executable_code:
            result["code"] = part.executable_code.code
        if part.code_execution_result:
            result["output"] = part.code_execution_result.output
    return result
