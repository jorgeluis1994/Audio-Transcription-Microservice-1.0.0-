from fastapi import APIRouter, UploadFile, File, HTTPException
from app.application.use_cases import TranscribeAudioUseCase
from app.infrastructure.openai_adapter import OpenAIWhisperAdapter

router = APIRouter()
use_case = TranscribeAudioUseCase(OpenAIWhisperAdapter())

@router.post(
    "/transcribe/audio",
    summary="Transcribe un archivo de audio a texto",
    description="Recibe un archivo .mp3 o .wav y devuelve el texto transcrito.",
    response_description="Texto transcrito del audio.",
)
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        content = await file.read()
        transcription = use_case.execute(file=content, filename=file.filename)
        return {"text": transcription}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))