from fastapi import APIRouter, Response
from app.models.schemas import TextRequest, TTSRequest, TextResponse
from app.services.azure_emotion import analyze_emotion
from app.services.azure_tts import synthesize_speech
<<<<<<< Updated upstream
=======
from app.services.wenxin_analyzer import analyze_with_wenxin
>>>>>>> Stashed changes
import logging

router = APIRouter()

def recommend_tts_params(emotion_data):
    """根据情感分析结果推荐TTS参数"""
    overall_sentiment = emotion_data["overall_sentiment"]
    confidence_scores = emotion_data["confidence_scores"]
    detailed_emotions = emotion_data.get("detailed_emotions", {})
    emotion_intensity = emotion_data.get("emotion_intensity", 50)  # 情感强度(0-100)
    
    # 默认参数
    voice = "zh-CN-XiaoyiNeural"  # 默认女声
    style = "general"
    rate = "0%"
    pitch = "0st"
    role = None
    styledegree = "1.0"  # 默认样式强度
    
    # 根据详细情感细化TTS参数
    highest_emotion = None
    highest_score = 0
    
    # 找出最强烈的详细情感
    if detailed_emotions:
        for emotion, score in detailed_emotions.items():
            if score > highest_score:
                highest_score = score
                highest_emotion = emotion
    
    # 根据情感强度计算样式强度
    intensity_factor = emotion_intensity / 50
    styledegree = str(min(max(intensity_factor, 0.5), 2.0))
    
    # 中文语音模型匹配
    zh_voices = {
        "cheerful_female": "zh-CN-XiaoxiaoNeural",
        "cheerful_male": "zh-CN-YunxiNeural",
        "serious_male": "zh-CN-YunyangNeural",
        "calm_female": "zh-CN-XiaomoNeural",
        "calm_male": "zh-CN-YunyeNeural",
        "angry_male": "zh-CN-YunxiNeural",
        "sad_female": "zh-CN-XiaomoNeural",
        "customer_service": "zh-CN-XiaoruiNeural"
    }
    
    # 英文语音模型匹配
    en_voices = {
        "cheerful_female": "en-US-AriaNeural",
        "cheerful_male": "en-US-DavisNeural",
        "angry_male": "en-US-GuyNeural",
        "sad_female": "en-US-JennyNeural",
        "sad_male": "en-US-TonyNeural",
        "friendly_female": "en-US-EmmaNeural",
        "friendly_male": "en-US-BrianNeural",
        "assistant": "en-US-SaraNeural"
    }
    
    # 是英文文本则使用英文语音模型
    is_english = len([c for c in emotion_data.get("sentence_sentiments", [])[0]["text"] if '\u4e00' <= c <= '\u9fff']) == 0 if emotion_data.get("sentence_sentiments") else False
    
    # 如果详细情感可信度高，则根据详细情感设置TTS参数
    if highest_emotion and highest_score > 0.5:
        if highest_emotion in ["喜悦", "满足"]:
            if is_english:
                voice = en_voices["cheerful_female"]
                style = "cheerful"
            else:
                voice = zh_voices["cheerful_female"]
                style = "cheerful"
            rate = "+10%"
            pitch = "+2st"
            
        elif highest_emotion in ["愉快"]:
            if is_english:
                voice = en_voices["friendly_female"]
                style = "cheerful"
            else:
                voice = zh_voices["cheerful_female"] 
                style = "cheerful"
            rate = "+5%"
            pitch = "+1st"
            
        elif highest_emotion in ["愤怒"]:
            if is_english:
                voice = en_voices["angry_male"]
                style = "angry"
            else:
                voice = zh_voices["angry_male"]
                style = "angry" 
            rate = "+10%"
            pitch = "-1st"
            
        elif highest_emotion in ["悲伤"]:
            if is_english:
                voice = en_voices["sad_female"]
                style = "sad"
            else:
                voice = zh_voices["sad_female"]
                style = "sad"
            rate = "-15%"
            pitch = "-2st"
            
        elif highest_emotion in ["担忧", "不满"]:
            if is_english:
                voice = en_voices["sad_male"]
                style = "serious" if not is_english else "sad"
            else:
                voice = zh_voices["serious_male"]
                style = "serious"
            rate = "-5%"
            pitch = "-1st"
            
        elif highest_emotion in ["平静", "思考"]:
            if is_english:
                voice = en_voices["friendly_male"]
                style = "calm" if not is_english else "assistant" 
            else:
                voice = zh_voices["calm_male"]
                style = "calm"
            rate = "-5%"
            pitch = "0st"
    
    # 没有可靠的详细情感时，回退到基本情感
    else:
        if overall_sentiment == 'positive':
            if confidence_scores["positive"] > 0.8:
                if is_english:
                    voice = en_voices["cheerful_female"]
                    style = "cheerful" 
                else:
                    voice = zh_voices["cheerful_female"]
                    style = "cheerful"
                rate = "+15%"
                pitch = "+2st"
                # 情感强烈时使用特定角色
                if emotion_intensity > 75:
                    role = "YoungAdultFemale"
            else:
                if is_english:
                    voice = en_voices["friendly_female"]
                    style = "cheerful"
                else:
                    voice = zh_voices["cheerful_female"]
                    style = "cheerful"
                rate = "+5%"
                pitch = "+1st"
        
        elif overall_sentiment == 'negative':
            if confidence_scores["negative"] > 0.8:
                if is_english:
                    voice = en_voices["sad_male"]
                    style = "sad"
                else:
                    voice = zh_voices["sad_female"]
                    style = "sad"
                rate = "-15%"
                pitch = "-2st"
                # 情感强烈时对应特定角色
                if emotion_intensity > 75:
                    role = "OlderAdultMale" if not is_english else None
            else:
                if is_english:
                    voice = en_voices["sad_female"]
                    style = "sad"
                else:
                    voice = zh_voices["calm_male"]
                    style = "sad"
                rate = "-5%"
                pitch = "-1st"
        
        elif overall_sentiment == 'neutral':
            # 中性情感的处理
            if is_english:
                voice = en_voices["assistant"]
                style = "assistant"
            else:
                voice = zh_voices["customer_service"]
                style = "calm" if not is_english else "assistant"
            rate = "0%"
            pitch = "0st"
    
    # 构建响应
    response = {
        "voice": voice,
        "style": style,
        "rate": rate,
        "pitch": pitch,
        "styledegree": styledegree
    }
    
    # 仅在有角色设置时添加
    if role:
        response["role"] = role
        
    return response

@router.post("/analyze", response_model=TextResponse)
def analyze(request: TextRequest):
    emotion = analyze_emotion(request.text)
<<<<<<< Updated upstream
    tts_params = recommend_tts_params(emotion)
=======
    
    try:
        # 尝试使用百度文心API
        wenxin_tts_params = await analyze_with_wenxin(request.text, emotion)
        if wenxin_tts_params:
            logging.info("Using Baidu Wenxin-generated TTS parameters")
            tts_params = wenxin_tts_params
            return {
                **emotion,
                "tts_params": tts_params
            }
        
        # 如果文心失败，使用规则型推荐
        logging.info("Falling back to rule-based TTS parameters")
        tts_params = recommend_tts_params(emotion)
    except Exception as e:
        # 异常情况下回退到规则型推荐
        logging.error(f"Error using AI services: {str(e)}, falling back to rule-based parameters")
        tts_params = recommend_tts_params(emotion)
    
>>>>>>> Stashed changes
    return {
        **emotion,
        "tts_params": tts_params
    }

@router.post("/tts")
def tts(request: TTSRequest):
    # 正确处理可选参数
    role = request.role if hasattr(request, 'role') and request.role is not None else None
    styledegree = request.styledegree if hasattr(request, 'styledegree') and request.styledegree is not None else "1.0"
    
    try:
        audio = synthesize_speech(
            request.text,
            request.voice,
            request.style,
            request.rate,
            request.pitch,
            role,
            styledegree
        )
        return Response(content=audio, media_type="audio/mpeg")
    except Exception as e:
        logging.error(f"TTS error: {str(e)}")
        raise 