from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class TextRequest(BaseModel):
    text: str

class TTSRequest(BaseModel):
    text: str
    voice: str
    style: str
    rate: str
    pitch: str
    role: Optional[str] = None
    styledegree: Optional[str] = "1.0"

class SentenceSentiment(BaseModel):
    text: str
    sentiment: str
    confidence_scores: Dict[str, float]
    offset: Optional[int] = None
    length: Optional[int] = None

class AspectInfo(BaseModel):
    text: str
    sentiment: str
    confidence_scores: Dict[str, float]
    is_negated: bool
    offset: Optional[int] = None
    length: Optional[int] = None

class OpinionInfo(BaseModel):
    text: str
    sentiment: str
    confidence_scores: Dict[str, float]
    is_negated: bool
    offset: Optional[int] = None
    length: Optional[int] = None
    related_aspect: str

class OpinionMiningData(BaseModel):
    aspects: List[AspectInfo]
    opinions: List[OpinionInfo]
    sentiment_indicators: List[Dict[str, Any]]

class IntensityAnalysis(BaseModel):
    overall_intensity: int
    volatility: int
    certainty: int
    complexity: int
    positive_intensity: int
    negative_intensity: int
    neutral_intensity: int
    dominant_emotion: str

class TextFeatures(BaseModel):
    length: int
    sentence_count: int
    has_exclamation: bool
    has_question: bool
    has_ellipsis: bool
    capitalization_ratio: float

class SentimentKeyword(BaseModel):
    word: str
    sentiment: str
    confidence: float
    is_negated: bool

class TextResponse(BaseModel):
    overall_sentiment: str
    confidence_scores: Dict[str, float]
    detailed_emotions: Dict[str, float]
    emotion_intensity: int
    sentence_sentiments: List[SentenceSentiment]
    opinion_mining: OpinionMiningData
    intensity_analysis: IntensityAnalysis
    text_features: TextFeatures
    sentiment_keywords: List[SentimentKeyword]
    tts_params: Dict[str, Any] 