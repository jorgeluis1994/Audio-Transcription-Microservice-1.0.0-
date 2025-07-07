import openai
from app.domain.ports import AudioToTextPort
from typing import BinaryIO
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIWhisperAdapter(AudioToTextPort):
    def transcribe_audio(self, file: BinaryIO, filename: str) -> str:
        response = openai.audio.transcriptions.create(
            file=(filename, file, "audio/mpeg"),
            model="whisper-1",
            response_format="text"
        )
        return response.text