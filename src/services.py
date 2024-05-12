import tempfile

from gtts import gTTS

from src.gemini import GEMINI
from src.settings import GEMINI_TOPIC_LENGTH_LIMIT, GEMINI_TOPIC_VALIDATION_SAMPLES


class TopicNotAllowed(Exception):
    """The topic is invalid"""


def text_to_speech(text: str) -> tempfile._TemporaryFileWrapper:
    # PEP 333 -> Do not need to use context manager with file
    speech = gTTS(text, lang="pt", slow=False)
    tmp = tempfile.NamedTemporaryFile(suffix=".mp3")
    for idx, decoded in enumerate(speech.stream()):
        tmp.write(decoded)
    tmp.seek(0)
    return tmp


def validate_topic(topic: str) -> str:
    if len(topic) > GEMINI_TOPIC_LENGTH_LIMIT:
        raise TopicNotAllowed

    response = GEMINI.generate_content(
        GEMINI_TOPIC_VALIDATION_SAMPLES
        + f"Responda só sim ou não sem pontuação. Existe o nome de uma pessoa nesse texto: {topic}."
    )

    if "sim" in response.text.lower().strip():
        raise TopicNotAllowed


def generate_joke(topic: str) -> str:
    prompt = f"Hoje o seu show é sobre {topic}."
    response = GEMINI.generate_content(prompt)
    return response.text
