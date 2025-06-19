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
        detailed["兴奋"] = confidence_scores["positive"] * 0.9
    elif confidence_scores.get("positive", 0) > 0.3:
        detailed["愉快"] = confidence_scores["positive"] * 0.9
        detailed["满意"] = confidence_scores["positive"] * 0.7
    elif confidence_scores.get("positive", 0) > 0.1:
        detailed["轻微积极"] = confidence_scores["positive"] * 0.8
    
    # 负面情感细分
    if confidence_scores.get("negative", 0) > 0.7:
        detailed["愤怒"] = confidence_scores["negative"] * 0.8
        detailed["悲伤"] = confidence_scores["negative"] * 0.9
        detailed["绝望"] = confidence_scores["negative"] * 0.7
    elif confidence_scores.get("negative", 0) > 0.4:
        detailed["担忧"] = confidence_scores["negative"] * 0.7
        detailed["不满"] = confidence_scores["negative"] * 0.8
        detailed["焦虑"] = confidence_scores["negative"] * 0.6
    elif confidence_scores.get("negative", 0) > 0.2:
        detailed["轻微不适"] = confidence_scores["negative"] * 0.6
        detailed["困惑"] = confidence_scores["negative"] * 0.5
    
    # 中性情感细分
    if confidence_scores.get("neutral", 0) > 0.6:
        detailed["平静"] = confidence_scores["neutral"] * 0.9
        detailed["思考"] = confidence_scores["neutral"] * 0.7
        detailed["客观"] = confidence_scores["neutral"] * 0.8
    elif confidence_scores.get("neutral", 0) > 0.3:
        detailed["冷静"] = confidence_scores["neutral"] * 0.6
        detailed["理性"] = confidence_scores["neutral"] * 0.7
    
    return detailed

def extract_opinion_mining_data(response) -> Dict[str, Any]:
    """提取opinion mining的详细信息"""
    opinion_data = {
        "aspects": [],
        "opinions": [],
        "sentiment_indicators": []
    }
    
    if hasattr(response, 'mined_opinions') and response.mined_opinions:
        for opinion in response.mined_opinions:
            for aspect in opinion.aspects:
                aspect_info = {
                    "text": aspect.text,
                    "sentiment": aspect.sentiment,
                    "confidence_scores": {
                        "positive": aspect.confidence_scores.positive,
                        "negative": aspect.confidence_scores.negative,
                        "neutral": aspect.confidence_scores.neutral
                    },
                    "is_negated": aspect.is_negated if hasattr(aspect, 'is_negated') else False,
                    "offset": aspect.offset if hasattr(aspect, 'offset') else None,
                    "length": aspect.length if hasattr(aspect, 'length') else None
                }
                opinion_data["aspects"].append(aspect_info)
                
                # 提取相关观点
                for opinion_text in opinion.opinions:
                    opinion_info = {
                        "text": opinion_text.text,
                        "sentiment": opinion_text.sentiment,
                        "confidence_scores": {
                            "positive": opinion_text.confidence_scores.positive,
                            "negative": opinion_text.confidence_scores.negative,
                            "neutral": opinion_text.confidence_scores.neutral
                        },
                        "is_negated": opinion_text.is_negated if hasattr(opinion_text, 'is_negated') else False,
                        "offset": opinion_text.offset if hasattr(opinion_text, 'offset') else None,
                        "length": opinion_text.length if hasattr(opinion_text, 'length') else None,
                        "related_aspect": aspect.text
                    }
                    opinion_data["opinions"].append(opinion_info)
    
    return opinion_data

def analyze_emotion_intensity(confidence_scores: Dict[str, float], opinion_data: Dict[str, Any]) -> Dict[str, Any]:
    """分析情感强度和相关指标"""
    # 基础情感强度
    max_confidence = max(confidence_scores.values())
    emotion_intensity = int(max_confidence * 100)
    
    # 情感波动性（基于不同情感的差异）
    sorted_scores = sorted(confidence_scores.values(), reverse=True)
    emotion_volatility = int((sorted_scores[0] - sorted_scores[1]) * 100) if len(sorted_scores) > 1 else 0
    
    # 情感确定性（最高置信度）
    emotion_certainty = int(max_confidence * 100)
    
    # 情感复杂度（基于opinion mining中的aspects数量）
    complexity_score = min(len(opinion_data.get("aspects", [])), 10) * 10
    
    # 情感极性强度
    positive_intensity = int(confidence_scores.get("positive", 0) * 100)
    negative_intensity = int(confidence_scores.get("negative", 0) * 100)
    neutral_intensity = int(confidence_scores.get("neutral", 0) * 100)
    
    return {
        "overall_intensity": emotion_intensity,
        "volatility": emotion_volatility,
        "certainty": emotion_certainty,
        "complexity": complexity_score,
        "positive_intensity": positive_intensity,
        "negative_intensity": negative_intensity,
        "neutral_intensity": neutral_intensity,
        "dominant_emotion": max(confidence_scores.items(), key=lambda x: x[1])[0] if confidence_scores else "neutral"
    }

def analyze_emotion(text: str) -> Dict[str, Any]:
    """分析文本情感，返回详细情感分析结果"""
    # 预处理文本
    processed_text = preprocess_text(text)
    
    client = TextAnalyticsClient(
        endpoint=settings.AZURE_TEXT_ANALYTICS_ENDPOINT,
        credential=AzureKeyCredential(settings.AZURE_TEXT_ANALYTICS_KEY)
    )
    
    # 使用opinion mining获取更详细的分析
    response = client.analyze_sentiment([processed_text], show_opinion_mining=True)[0]
    
    # 句子级情感分析
    sentence_sentiments = []
    for sent in response.sentences:
        sentence_data = {
            "text": sent.text,
            "sentiment": sent.sentiment,
            "confidence_scores": {
                "positive": sent.confidence_scores.positive,
                "negative": sent.confidence_scores.negative,
                "neutral": sent.confidence_scores.neutral
            },
            "offset": sent.offset if hasattr(sent, 'offset') else None,
            "length": sent.length if hasattr(sent, 'length') else None
        }
        sentence_sentiments.append(sentence_data)
    
    # 获取详细情感分析
    detailed_emotions = map_to_detailed_emotions(response.confidence_scores)
    
    # 提取opinion mining数据
    opinion_data = extract_opinion_mining_data(response)
    
    # 分析情感强度
    intensity_analysis = analyze_emotion_intensity(response.confidence_scores, opinion_data)
    
    # 文本特征分析
    text_features = {
        "length": len(processed_text),
        "sentence_count": len(sentence_sentiments),
        "has_exclamation": "!" in processed_text,
        "has_question": "?" in processed_text,
        "has_ellipsis": "..." in processed_text,
        "capitalization_ratio": sum(1 for c in processed_text if c.isupper()) / len(processed_text) if processed_text else 0
    }
    
    # 情感关键词提取（基于opinion mining）
    sentiment_keywords = []
    if opinion_data["aspects"]:
        for aspect in opinion_data["aspects"]:
            if aspect["confidence_scores"][aspect["sentiment"]] > 0.6:
                sentiment_keywords.append({
                    "word": aspect["text"],
                    "sentiment": aspect["sentiment"],
                    "confidence": aspect["confidence_scores"][aspect["sentiment"]],
                    "is_negated": aspect["is_negated"]
                })
    
    return {
        "overall_sentiment": response.sentiment,
        "confidence_scores": {
            "positive": response.confidence_scores.positive,
            "negative": response.confidence_scores.negative,
            "neutral": response.confidence_scores.neutral
        },
        "detailed_emotions": detailed_emotions,
        "sentence_sentiments": sentence_sentiments,
        "opinion_mining": opinion_data,
        "intensity_analysis": intensity_analysis,
        "text_features": text_features,
        "sentiment_keywords": sentiment_keywords,
        # 保持向后兼容
        "emotion_intensity": intensity_analysis["overall_intensity"]
    } 