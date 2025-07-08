from app.domain.ports import AudioToTextPort
from typing import BinaryIO

class TranscribeAudioUseCase:
    def __init__(self, transcriber: AudioToTextPort):
        self.transcriber = transcriber

    async def execute(self, file: BinaryIO, filename: str) -> str:
        # 1. Transcribir audio
        texto = self.transcriber.transcribe_audio(file, filename)

        # 2. Analizar texto (llamado síncrono)
        resultado =  await self.transcriber.analyze_transcription(texto)

        return resultado

