from app.domain.ports import AudioToTextPort
from typing import BinaryIO

class TranscribeAudioUseCase:
    def __init__(self, transcriber: AudioToTextPort):
        self.transcriber = transcriber

    def execute(self, file: BinaryIO, filename: str) -> str:
        return self.transcriber.transcribe_audio(file, filename)