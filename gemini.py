import google.generativeai as genai

from settings import (
    GEMINI_GENERATION_CONFIG,
    GEMINI_SAFETY_SETTINGS,
    GEMINI_SYSTEM_INSTRUCTION,
)

GEMINI = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=GEMINI_GENERATION_CONFIG,
    safety_settings=GEMINI_SAFETY_SETTINGS,
    system_instruction=GEMINI_SYSTEM_INSTRUCTION,
)
