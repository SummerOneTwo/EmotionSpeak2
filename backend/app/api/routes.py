from fastapi import APIRouter, Response
from app.models.schemas import TextRequest, TTSRequest
from app.services.azure_emotion import analyze_emotion
from app.services.azure_tts import synthesize_speech

router = APIRouter()

@router.post("/analyze")
def analyze(request: TextRequest):
    return analyze_emotion(request.text)

@router.post("/tts")
def tts(request: TTSRequest):
    audio = synthesize_speech(
        request.text,
        request.speed,
        request.volume,
        request.pitch,
        request.voice
    )
    return Response(content=audio, media_type="audio/mpeg") 