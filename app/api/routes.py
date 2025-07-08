from io import BytesIO
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.application.use_cases import TranscribeAudioUseCase
from app.infrastructure.openai_adapter import OpenAIWhisperAdapter

# Configuración básica del logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

router = APIRouter()
use_case = TranscribeAudioUseCase(OpenAIWhisperAdapter())

ALLOWED_EXTENSIONS = {"mp3", "wav", "m4a"}
ALLOWED_MIME_TYPES = {"audio/mpeg", "audio/wav", "audio/x-wav", "audio/mp4", "audio/aac","audio/x-m4a"}

@router.post(
    "/transcribe/audio",
    summary="Transcribe un archivo de audio a texto",
    description="Recibe un archivo .mp3, .wav o .m4a y devuelve el texto transcrito.",
    response_description="Texto transcrito del audio.",
)
async def transcribe_audio(file: UploadFile = File(...)):
    logger.info(f"Recibido archivo: {file.filename} con tipo MIME: {file.content_type}")

    # Validar extensión
    extension = file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        logger.warning(f"Archivo rechazado por extensión: {file.filename}")
        raise HTTPException(
            status_code=400,
            detail="Archivo no soportado. Solo se permiten .mp3, .wav y .m4a"
        )

    # Validar MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        logger.warning(f"Archivo rechazado por tipo MIME: {file.content_type}")
        raise HTTPException(
            status_code=400,
            detail="Tipo de archivo no válido. Debe ser un archivo de audio."
        )

    try:
        content = await file.read()
        file_like = BytesIO(content)
        
        transcription = await use_case.execute(file=file_like, filename=file.filename)
        
        logger.info(f"Transcripción exitosa para archivo: {file.filename}")
        return {"text": transcription}
    except Exception as e:
        logger.error(f"Error durante la transcripción: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    

