from abc import ABC, abstractmethod
from typing import BinaryIO

class AudioToTextPort(ABC):
    @abstractmethod
    def transcribe_audio(self, file: BinaryIO, filename: str) -> str:
        pass
    
    @abstractmethod
    async def transcribe_audio_local(self, file: BinaryIO, filename: str) -> str:
        pass
    
    @abstractmethod
    async def analyze_transcription(self, transcribed_text: str) -> str:
        pass