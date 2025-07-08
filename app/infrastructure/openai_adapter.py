import asyncio
from io import BytesIO
import logging
from shutil import which
import tempfile
from fastapi import HTTPException
from faster_whisper import WhisperModel
import openai
from typing import BinaryIO
from dotenv import load_dotenv
import os
import tiktoken
from pydub import AudioSegment
from mutagen import File as MutagenFile
from app.domain.ports import AudioToTextPort
AudioSegment.converter = which("ffmpeg")  # ahora debería resolver sin problema
from openai import OpenAI
# print(f"FFmpeg path: {AudioSegment.converter}")

logger = logging.getLogger(__name__)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

class OpenAIWhisperAdapter(AudioToTextPort):
    
    def __init__(self):
        # Puedes ajustar el modelo y device aquí
        # self.model = WhisperModel("base", device="cpu", compute_type="int8")
        self.model = WhisperModel("small", device="cpu", compute_type="int8")

        
    async def transcribe_audio_local(self, file: BinaryIO, filename: str) -> str:
            loop = asyncio.get_running_loop()

            # Crear archivo temporal sin borrar automáticamente
            temp_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            try:
                temp_audio.write(file.read())
                temp_audio.close()  # Importante cerrar antes de usarlo en otra librería

                # Ejecutar la transcripción en executor pasándole la ruta del archivo
                segments, info = await loop.run_in_executor(None, self.model.transcribe, temp_audio.name)

                # Procesar resultado
                text = " ".join(segment.text for segment in segments)
                return text

            finally:
                # Borrar el archivo temporal manualmente
                os.remove(temp_audio.name)

    async def analyze_transcription(self, transcribed_text: str) -> str:
        # Aquí podrías llamar a openai o hacer análisis
        return transcribed_text
    
    def transcribe_audio(self, file: BinaryIO, filename: str) -> str:
        try:
            duration_seconds = self.get_audio_duration(file)
            logger.info(f"Duración del audio (mutagen): {duration_seconds} segundos")
            
            # Transcripción     
            response = openai.audio.transcriptions.create(
                file=(filename, file, "audio/mpeg"),
                model="whisper-1",
                response_format="text"  # devuelve un str directamente
            )

            logger.info(f"Texto transcrito: {response}")

            return response  # ya es str
        
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


    async def analyze_transcription(self, transcribed_text: str) -> str:
        try:
            token_count = self.count_tokens(transcribed_text, model="gpt-4")
            logger.info(f"Transcribed text token count: {token_count}")

            response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Informe médico básico, conciso y claro."},
                        {"role": "user", "content": f"Transcripción de la consulta: {transcribed_text}"}
                    ],
                    max_tokens=300  # Limita la respuesta a 300 tokens
                )
            logger.info(f"Response from GPT-4: {response}")


            gpt_response = response.choices[0].message.content
            logger.info(f"GPT response token count: {len(tiktoken.encoding_for_model('gpt-4').encode(gpt_response))}")

            return gpt_response

        except Exception as e:
            logger.error(f"Error al analizar la transcripción: {e}")
            raise HTTPException(status_code=500, detail="Error al analizar la transcripción")

    
    def count_tokens(self, text: str, model: str = "gpt-4") -> int:
        encoding = tiktoken.encoding_for_model(model)
        tokens = encoding.encode(text)
        return len(tokens)

    
    def get_audio_duration(self, file_like: BinaryIO) -> float:
        file_like.seek(0)
        audio = MutagenFile(file_like)
        if audio is None or not hasattr(audio, "info"):
            return 0.0
        duration = audio.info.length
        file_like.seek(0)
        return duration

