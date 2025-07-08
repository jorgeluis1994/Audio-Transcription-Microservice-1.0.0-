✅ Contenido del requirements.txt
txt
Copy
Edit
# Core FastAPI + servidor
fastapi
uvicorn

# Procesamiento de audio
pydub
mutagen
noisereduce
librosa
soundfile

# Transcripción con modelos locales (Faster Whisper)
faster-whisper

# OpenAI (nuevo cliente y legacy)
openai
tiktoken

# Carga de variables de entorno
python-dotenv

# Logging asincrónico / helpers
aiofiles

# Otros
httpx  # Necesario para openai client en algunos entornos
⚠️ Además, necesitas instalar herramientas del sistema:
Estas no van en el requirements.txt, pero deben estar instaladas en tu entorno (máquina local, servidor o contenedor):

bash
Copy
Edit
# FFmpeg (usado por pydub y librosa)
sudo apt install ffmpeg
# o en Mac:
brew install ffmpeg
También asegúrate de que ffmpeg esté en tu PATH. Puedes verificar con:

bash
Copy
Edit
which ffmpeg
💡 Si quieres un requirements.txt congelado (con versiones exactas):
Puedes generarlo después de instalar todo con:

bash
Copy
Edit
pip freeze > requirements.txt
