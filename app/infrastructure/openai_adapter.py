import openai
from app.domain.ports import AudioToTextPort
from typing import BinaryIO
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIWhisperAdapter(AudioToTextPort):
    def transcribe_audio(self, file: BinaryIO, filename: str) -> str:
        try:
            response = openai.audio.transcriptions.create(
                file=(filename, file, "audio/mpeg"),
                model="whisper-1",
                response_format="text"
            )
            return response.text
        except openai.RateLimitError as e:
            logger.error(f"Rate limit excedido: {e}")
            raise Exception("Se ha excedido el límite de uso de la API de OpenAI.")
        except openai.AuthenticationError as e:
            logger.error(f"Error de autenticación con OpenAI: {e}")
            raise Exception("Error de autenticación con OpenAI. Verifica tu API Key.")
        except openai.BadRequestError as e:
            logger.error(f"Solicitud incorrecta a OpenAI: {e}")
            raise Exception("Solicitud malformada a la API de OpenAI.")
        except openai.APIConnectionError as e:
            logger.error(f"Error de conexión con OpenAI: {e}")
            raise Exception("No se pudo conectar con la API de OpenAI.")
        except openai.APIError as e:
            logger.error(f"Error general de OpenAI: {e}")
            raise Exception("Error inesperado de OpenAI.")
        except Exception as e:
            logger.error(f"Error inesperado durante la transcripción: {e}")
            raise Exception("Ocurrió un error inesperado durante la transcripción.")
