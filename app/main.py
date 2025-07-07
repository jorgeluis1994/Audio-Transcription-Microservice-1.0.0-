from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Audio Transcription Microservice",
    description="Convierte audio en texto usando OpenAI Whisper",
    version="1.0.0",
    contact={
        "name": "Tu Nombre",
        "email": "tu@email.com",
    },
)

app.include_router(router, prefix="/api")
