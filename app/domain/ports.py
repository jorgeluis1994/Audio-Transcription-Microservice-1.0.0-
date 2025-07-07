from abc import ABC, abstractmethod
from typing import BinaryIO

class AudioToTextPort(ABC):
    @abstractmethod
    def transcribe_audio(self, file: BinaryIO, filename: str) -> str:
        pass