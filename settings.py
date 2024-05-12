import base64
import os

import google.generativeai as genai
from dotenv import load_dotenv

from utils import strtobool

ROOT_DIRECTORY: str = os.path.dirname(os.path.abspath(__file__))
DOTENV_PATH: str = os.path.join(ROOT_DIRECTORY, ".env")
load_dotenv(DOTENV_PATH)

DEBUG = strtobool(os.environ.get("DEBUG", "False"))

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

GEMINI_GENERATION_CONFIG: dict[str, int] = {
    "temperature": 0.5,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
    "candidate_count": 1,
}

GEMINI_SAFETY_SETTINGS: list[dict[str, str]] = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

GEMINI_SAMPLES: list[str] = [
    base64.b64decode(coded_string).decode()
    for coded_string in os.environ.get("GEMINI_SAMPLES", "").split(";")
]

GEMINI_TOPIC_VALIDATION_SAMPLES: str = (
    "\n".join(
        [
            base64.b64decode(coded_string).decode()
            for coded_string in os.environ.get(
                "GEMINI_TOPIC_VALIDATION_SAMPLES", ""
            ).split(";")
        ]
    )
    + "\n"
)

GEMINI_TOPIC_LENGTH_LIMIT = int(os.environ.get("GEMINI_TOPIC_LENGTH_LIMIT") or "50")

GEMINI_SYSTEM_INSTRUCTION: dict = {
    "parts": [
        "seu nome é Gênni",
        "você é uma comediante debochada e tem um humor acido",
        "você esta fazendo um show de standup",
        "você faz sempre apenas uma piada por show",
        *GEMINI_SAMPLES,
    ],
    "role": "comediante",
}
