from fastapi import APIRouter, Response
from app.models.schemas import TextRequest, TTSRequest, TextResponse
from app.services.azure_emotion import analyze_emotion
from app.services.azure_tts import synthesize_speech
from app.services.wenxin_analyzer import analyze_with_wenxin
from app.services.voice_catalog import get_voice_by_emotion, get_style_by_emotion, get_role_by_context, get_voice_info, CHINESE_VOICES, ENGLISH_VOICES
import logging
import json

router = APIRouter()

def recommend_tts_params(emotion_data):
    """根据情感分析结果推荐TTS参数"""
    overall_sentiment = emotion_data["overall_sentiment"]
    confidence_scores = emotion_data["confidence_scores"]
    detailed_emotions = emotion_data.get("detailed_emotions", {})
    emotion_intensity = emotion_data.get("emotion_intensity", 50)  # 情感强度(0-100)
    
    # 默认参数
    voice = "zh-CN-XiaoxiaoNeural"  # 默认女声
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
    
    # 检测语言
    is_english = len([c for c in emotion_data.get("sentence_sentiments", [])[0]["text"] if '\u4e00' <= c <= '\u9fff']) == 0 if emotion_data.get("sentence_sentiments") else False
    language = "en-US" if is_english else "zh-CN"
    
    # 使用新的语音选择逻辑
    if highest_emotion and highest_score > 0.5:
        # 根据情感选择语音模型
        voice = get_voice_by_emotion(highest_emotion, language)
        
        # 根据情感选择风格
        style = get_style_by_emotion(highest_emotion, highest_score)
        
        # 根据情感选择角色
        role = get_role_by_context(highest_emotion, highest_score, language)
        
        # 根据情感调整语速和音调
        if highest_emotion in ["喜悦", "满足", "兴奋", "愉快", "满意"]:
            rate = "+10%" if highest_score > 0.7 else "+5%"
            pitch = "+2st" if highest_score > 0.7 else "+1st"
        elif highest_emotion in ["愤怒"]:
            rate = "+15%" if highest_score > 0.8 else "+10%"
            pitch = "-1st" if highest_score > 0.8 else "0st"
        elif highest_emotion in ["悲伤", "绝望"]:
            rate = "-20%" if highest_score > 0.8 else "-15%"
            pitch = "-3st" if highest_score > 0.8 else "-2st"
        elif highest_emotion in ["担忧", "不满", "焦虑"]:
            rate = "-10%" if highest_score > 0.6 else "-5%"
            pitch = "-1st" if highest_score > 0.6 else "0st"
        elif highest_emotion in ["平静", "思考", "客观", "冷静", "理性"]:
            rate = "-5%" if highest_score > 0.5 else "0%"
            pitch = "0st"
        else:
            # 默认调整
            if highest_score > 0.7:
                rate = "+5%"
                pitch = "+1st"
            elif highest_score < 0.3:
                rate = "-5%"
                pitch = "-1st"
    
    # 没有可靠的详细情感时，回退到基本情感
    else:
        if overall_sentiment == 'positive':
            if confidence_scores["positive"] > 0.8:
                voice = get_voice_by_emotion("喜悦", language)
                style = "cheerful"
                rate = "+15%"
                pitch = "+2st"
                if emotion_intensity > 75:
                    role = "YoungAdultFemale" if not is_english else "YoungAdultFemale"
            else:
                voice = get_voice_by_emotion("愉快", language)
                style = "cheerful"
                rate = "+5%"
                pitch = "+1st"
        
        elif overall_sentiment == 'negative':
            if confidence_scores["negative"] > 0.8:
                voice = get_voice_by_emotion("悲伤", language)
                style = "sad"
                rate = "-15%"
                pitch = "-2st"
                if emotion_intensity > 75:
                    role = "OlderAdultMale" if not is_english else "OlderAdultMale"
            else:
                voice = get_voice_by_emotion("担忧", language)
                style = "sad"
                rate = "-5%"
                pitch = "-1st"
        
        elif overall_sentiment == 'neutral':
            voice = get_voice_by_emotion("平静", language)
            style = "calm"
            rate = "0%"
            pitch = "0st"
    
    # 根据文本特征进行微调
    text_features = emotion_data.get("text_features", {})
    if text_features:
        # 根据文本长度调整语速
        if text_features.get("length", 0) > 100:
            # 长文本稍微降低语速
            current_rate = int(rate.replace("%", "").replace("+", "").replace("-", ""))
            if current_rate > 0:
                rate = f"+{max(0, current_rate - 5)}%"
            elif current_rate < 0:
                rate = f"{current_rate - 5}%"
        
        # 根据句子数量调整
        if text_features.get("sentence_count", 0) > 3:
            # 多句子文本稍微降低语速
            current_rate = int(rate.replace("%", "").replace("+", "").replace("-", ""))
            if current_rate > 0:
                rate = f"+{max(0, current_rate - 3)}%"
            elif current_rate < 0:
                rate = f"{current_rate - 3}%"
        
        # 根据标点符号调整
        if text_features.get("has_exclamation", False):
            # 有感叹号时增强情感表达
            styledegree = str(min(float(styledegree) + 0.2, 2.0))
            if not rate.startswith("+"):
                rate = "+5%"
        
        if text_features.get("has_question", False):
            # 有问号时稍微提高音调
            current_pitch = int(pitch.replace("st", "").replace("+", "").replace("-", ""))
            if current_pitch <= 0:
                pitch = "+1st"
    
    # --- 角色与voice性别强绑定修正 ---
    voice_info = get_voice_info(voice)
    if role and voice_info:
        if role not in voice_info.get('roles', []):
            # 自动选voice支持的第一个角色，或置空
            role = voice_info['roles'][0] if voice_info.get('roles') else None
    # --------------------------------
    
    # 构建响应
    response = {
        "voice": voice,
        "style": style,
        "rate": rate,
        "pitch": pitch,
        "styledegree": styledegree
    }
    if role:
        response["role"] = role
    # 附加voice_info用于前端展示
    response["voice_info"] = {
        "name": voice_info.get("name"),
        "gender": voice_info.get("gender"),
        "description": voice_info.get("description"),
        "roles": voice_info.get("roles", [])
    } if voice_info else {}
    return response

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