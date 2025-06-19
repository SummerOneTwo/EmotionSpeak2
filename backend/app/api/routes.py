from fastapi import APIRouter, Response
from app.models.schemas import TextRequest, TTSRequest
from app.services.azure_emotion import analyze_emotion
from app.services.azure_tts import synthesize_speech
from app.services.wenxin_analyzer import analyze_with_wenxin
import logging
import json

router = APIRouter()

@router.post("/analyze")
async def analyze(request: TextRequest):
    logging.info(f"/analyze 输入: {request.text[:100]}...")
    emotion = analyze_emotion(request.text)
    logging.info(f"情感分析结果: {json.dumps(emotion, ensure_ascii=False)}")
    tts_params = analyze_with_wenxin(request.text, emotion)
    logging.info(f"Wenxin推荐TTS参数: {tts_params}")
    return {"emotion": emotion, "tts_params": tts_params}

@router.post("/tts")
def tts(request: TTSRequest):
    logging.info(f"/tts 输入: {request.dict()}")
    try:
        audio = synthesize_speech(
            request.text,
            request.voice,
            request.style,
            request.rate,
            request.pitch,
            request.role,
            request.styledegree
        )
        logging.info(f"TTS合成成功: voice={request.voice}, role={request.role}, style={request.style}, rate={request.rate}, pitch={request.pitch}, styledegree={request.styledegree}")
        return Response(content=audio, media_type="audio/mpeg")
    except Exception as e:
        logging.error(f"TTS error: {str(e)}")
        raise 