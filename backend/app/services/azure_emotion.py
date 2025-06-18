from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from app.core.config import settings
import re
from typing import Dict, List, Any

def preprocess_text(text: str) -> str:
    """对输入文本进行预处理，提高情感分析准确性"""
    # 去除多余空格
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def map_to_detailed_emotions(confidence_scores: Dict[str, float]) -> Dict[str, float]:
    """将基本情感得分映射到更详细的情感类别"""
    detailed = {}
    
    # 正面情感细分
    if confidence_scores.get("positive", 0) > 0.6:
        detailed["喜悦"] = min(confidence_scores["positive"] * 1.2, 1.0)
        detailed["满足"] = confidence_scores["positive"] * 0.8
    elif confidence_scores.get("positive", 0) > 0.3:
        detailed["愉快"] = confidence_scores["positive"] * 0.9
    
    # 负面情感细分
    if confidence_scores.get("negative", 0) > 0.7:
        detailed["愤怒"] = confidence_scores["negative"] * 0.8
        detailed["悲伤"] = confidence_scores["negative"] * 0.9
    elif confidence_scores.get("negative", 0) > 0.4:
        detailed["担忧"] = confidence_scores["negative"] * 0.7
        detailed["不满"] = confidence_scores["negative"] * 0.8
    elif confidence_scores.get("negative", 0) > 0.2:
        detailed["轻微不适"] = confidence_scores["negative"] * 0.6
    
    # 中性情感细分
    if confidence_scores.get("neutral", 0) > 0.6:
        detailed["平静"] = confidence_scores["neutral"] * 0.9
        detailed["思考"] = confidence_scores["neutral"] * 0.7
    
    return detailed

def analyze_emotion(text: str) -> Dict[str, Any]:
    """分析文本情感，返回详细情感分析结果"""
    # 预处理文本
    processed_text = preprocess_text(text)
    
    client = TextAnalyticsClient(
        endpoint=settings.AZURE_TEXT_ANALYTICS_ENDPOINT,
        credential=AzureKeyCredential(settings.AZURE_TEXT_ANALYTICS_KEY)
    )
    
    response = client.analyze_sentiment([processed_text], show_opinion_mining=True)[0]
    
    # 句子级情感
    sentence_sentiments = []
    for sent in response.sentences:
        sentence_sentiments.append({
            "text": sent.text,
            "sentiment": sent.sentiment,
            "confidence_scores": {
                "positive": sent.confidence_scores.positive,
                "negative": sent.confidence_scores.negative,
                "neutral": sent.confidence_scores.neutral
            }
        })
    
    # 获取详细情感分析
    detailed_emotions = map_to_detailed_emotions(response.confidence_scores)
    
    # 从opinion mining中提取额外信息
    if hasattr(response, 'mined_opinions') and response.mined_opinions:
        for op in response.mined_opinions:
            for aspect in op.aspects:
                detailed_emotions[aspect.text] = aspect.sentiment
    
    # 情感强度指标 (0-100)
    emotion_intensity = int(max(
        response.confidence_scores.positive,
        response.confidence_scores.negative,
        response.confidence_scores.neutral
    ) * 100)
    
    return {
        "overall_sentiment": response.sentiment,
        "emotion_intensity": emotion_intensity,
        "confidence_scores": {
            "positive": response.confidence_scores.positive,
            "negative": response.confidence_scores.negative,
            "neutral": response.confidence_scores.neutral
        },
        "detailed_emotions": detailed_emotions,
        "sentence_sentiments": sentence_sentiments
    } 