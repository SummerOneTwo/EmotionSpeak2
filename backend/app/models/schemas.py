from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class TextRequest(BaseModel):
    text: str

class SentenceSentiment(BaseModel):
    text: str
    sentiment: str
    confidence_scores: Dict[str, float]

class TTSParams(BaseModel):
    voice: str
    style: str
    rate: str
    pitch: str

class TextResponse(BaseModel):
    overall_sentiment: str
    confidence_scores: Dict[str, float]
    detailed_emotions: Dict[str, float]
    emotion_intensity: int
    sentence_sentiments: List[Dict[str, Any]]
    tts_params: Dict[str, Any]

class TTSRequest(BaseModel):
    text: str
    voice: str
    style: str = "general"
    rate: str = "0%"
    pitch: str = "0st"
    role: Optional[str] = None
    styledegree: Optional[str] = "1.0" 