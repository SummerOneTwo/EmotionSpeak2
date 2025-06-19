"""
Azure TTS Neural语音模型目录
基于Azure Cognitive Services Speech SDK官方文档
"""

# 中文语音模型
CHINESE_VOICES = {
    # 女声模型
    "zh-CN-XiaoxiaoNeural": {
        "name": "晓晓",
        "gender": "female",
        "description": "年轻女声，自然流畅",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["Girl", "YoungAdultFemale", "OlderAdultFemale", "SeniorFemale"],
        "emotion_suitability": {
            "positive": ["cheerful", "gentle", "affectionate", "hopeful"],
            "negative": ["sad", "angry", "fearful", "disgruntled", "terrified"],
            "neutral": ["calm", "serious", "soft"]
        }
    },
    "zh-CN-XiaoyiNeural": {
        "name": "晓伊",
        "gender": "female", 
        "description": "温柔女声，适合客服场景",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["YoungAdultFemale", "OlderAdultFemale"],
        "emotion_suitability": {
            "positive": ["cheerful", "gentle", "affectionate", "hopeful"],
            "negative": ["sad", "angry", "fearful", "disgruntled"],
            "neutral": ["calm", "serious", "soft"]
        }
    },
    "zh-CN-XiaomoNeural": {
        "name": "晓墨",
        "gender": "female",
        "description": "成熟女声，知性优雅",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["OlderAdultFemale", "SeniorFemale"],
        "emotion_suitability": {
            "positive": ["gentle", "affectionate", "calm"],
            "negative": ["sad", "serious", "disgruntled"],
            "neutral": ["calm", "serious", "soft"]
        }
    },
    "zh-CN-XiaoruiNeural": {
        "name": "晓睿",
        "gender": "female",
        "description": "专业女声，适合新闻播报",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["YoungAdultFemale", "OlderAdultFemale"],
        "emotion_suitability": {
            "positive": ["cheerful", "gentle"],
            "negative": ["serious", "disgruntled"],
            "neutral": ["calm", "serious"]
        }
    },
    "zh-CN-XiaohanNeural": {
        "name": "晓涵",
        "gender": "female",
        "description": "活泼女声，适合儿童内容",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["Girl", "YoungAdultFemale"],
        "emotion_suitability": {
            "positive": ["cheerful", "gentle", "affectionate", "hopeful"],
            "negative": ["sad", "fearful", "embarrassed"],
            "neutral": ["calm", "soft"]
        }
    },
    "zh-CN-XiaoxuanNeural": {
        "name": "晓萱",
        "gender": "female",
        "description": "温柔女声，适合情感表达",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["YoungAdultFemale", "OlderAdultFemale"],
        "emotion_suitability": {
            "positive": ["gentle", "affectionate", "calm", "hopeful"],
            "negative": ["sad", "fearful", "embarrassed"],
            "neutral": ["calm", "soft", "serious"]
        }
    },
    
    # 男声模型
    "zh-CN-YunxiNeural": {
        "name": "云希",
        "gender": "male",
        "description": "年轻男声，活力充沛",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["Boy", "YoungAdultMale"],
        "emotion_suitability": {
            "positive": ["cheerful", "gentle", "affectionate", "hopeful"],
            "negative": ["angry", "fearful", "disgruntled", "terrified"],
            "neutral": ["calm", "serious"]
        }
    },
    "zh-CN-YunyangNeural": {
        "name": "云扬",
        "gender": "male",
        "description": "成熟男声，权威专业",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["YoungAdultMale", "OlderAdultMale", "SeniorMale"],
        "emotion_suitability": {
            "positive": ["cheerful", "serious", "calm"],
            "negative": ["angry", "serious", "disgruntled"],
            "neutral": ["calm", "serious", "soft"]
        }
    },
    "zh-CN-YunyeNeural": {
        "name": "云野",
        "gender": "male",
        "description": "深沉男声，适合叙事",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["OlderAdultMale", "SeniorMale"],
        "emotion_suitability": {
            "positive": ["gentle", "calm", "serious"],
            "negative": ["sad", "serious", "disgruntled"],
            "neutral": ["calm", "serious", "soft"]
        }
    },
    "zh-CN-YunjianNeural": {
        "name": "云健",
        "gender": "male",
        "description": "稳重男声，适合商务场景",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["YoungAdultMale", "OlderAdultMale"],
        "emotion_suitability": {
            "positive": ["cheerful", "serious", "calm"],
            "negative": ["serious", "disgruntled"],
            "neutral": ["calm", "serious"]
        }
    }
}

# 英文语音模型
ENGLISH_VOICES = {
    # 女声模型
    "en-US-AriaNeural": {
        "name": "Aria",
        "gender": "female",
        "description": "自然女声，适合多种场景",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["YoungAdultFemale", "OlderAdultFemale"],
        "emotion_suitability": {
            "positive": ["cheerful", "gentle", "affectionate", "hopeful"],
            "negative": ["sad", "angry", "fearful", "disgruntled"],
            "neutral": ["calm", "serious", "soft"]
        }
    },
    "en-US-JennyNeural": {
        "name": "Jenny",
        "gender": "female",
        "description": "友好女声，适合客服",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["YoungAdultFemale"],
        "emotion_suitability": {
            "positive": ["cheerful", "gentle", "affectionate"],
            "negative": ["sad", "serious"],
            "neutral": ["calm", "serious", "soft"]
        }
    },
    "en-US-EmmaNeural": {
        "name": "Emma",
        "gender": "female",
        "description": "专业女声，适合商务",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["YoungAdultFemale", "OlderAdultFemale"],
        "emotion_suitability": {
            "positive": ["cheerful", "serious", "calm"],
            "negative": ["serious", "disgruntled"],
            "neutral": ["calm", "serious"]
        }
    },
    "en-US-SaraNeural": {
        "name": "Sara",
        "gender": "female",
        "description": "助手女声，适合AI对话",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["YoungAdultFemale"],
        "emotion_suitability": {
            "positive": ["cheerful", "gentle", "calm"],
            "negative": ["serious"],
            "neutral": ["calm", "serious", "soft"]
        }
    },
    "en-US-MichelleNeural": {
        "name": "Michelle",
        "gender": "female",
        "description": "温暖女声，适合情感表达",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["YoungAdultFemale", "OlderAdultFemale"],
        "emotion_suitability": {
            "positive": ["gentle", "affectionate", "calm", "hopeful"],
            "negative": ["sad", "fearful", "embarrassed"],
            "neutral": ["calm", "soft", "serious"]
        }
    },
    
    # 男声模型
    "en-US-GuyNeural": {
        "name": "Guy",
        "gender": "male",
        "description": "自然男声，适合多种场景",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["YoungAdultMale", "OlderAdultMale"],
        "emotion_suitability": {
            "positive": ["cheerful", "gentle", "affectionate", "hopeful"],
            "negative": ["angry", "fearful", "disgruntled", "terrified"],
            "neutral": ["calm", "serious"]
        }
    },
    "en-US-DavisNeural": {
        "name": "Davis",
        "gender": "male",
        "description": "活力男声，适合年轻内容",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["YoungAdultMale"],
        "emotion_suitability": {
            "positive": ["cheerful", "gentle", "affectionate", "hopeful"],
            "negative": ["angry", "fearful", "disgruntled"],
            "neutral": ["calm", "serious"]
        }
    },
    "en-US-TonyNeural": {
        "name": "Tony",
        "gender": "male",
        "description": "成熟男声，适合商务",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["OlderAdultMale", "SeniorMale"],
        "emotion_suitability": {
            "positive": ["cheerful", "serious", "calm"],
            "negative": ["sad", "serious", "disgruntled"],
            "neutral": ["calm", "serious", "soft"]
        }
    },
    "en-US-BrianNeural": {
        "name": "Brian",
        "gender": "male",
        "description": "友好男声，适合客服",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["YoungAdultMale", "OlderAdultMale"],
        "emotion_suitability": {
            "positive": ["cheerful", "gentle", "affectionate"],
            "negative": ["serious"],
            "neutral": ["calm", "serious", "soft"]
        }
    },
    "en-US-RogerNeural": {
        "name": "Roger",
        "gender": "male",
        "description": "深沉男声，适合叙事",
        "styles": ["cheerful", "sad", "angry", "fearful", "disgruntled", "serious", "gentle", "affectionate", "embarrassed", "calm", "soft", "shouting", "terrified", "unfriendly", "whispering", "hopeful"],
        "roles": ["OlderAdultMale", "SeniorMale"],
        "emotion_suitability": {
            "positive": ["gentle", "calm", "serious"],
            "negative": ["sad", "serious", "disgruntled"],
            "neutral": ["calm", "serious", "soft"]
        }
    }
}

# 语音风格映射
VOICE_STYLES = {
    "cheerful": "愉快",
    "sad": "悲伤", 
    "angry": "愤怒",
    "fearful": "恐惧",
    "disgruntled": "不满",
    "serious": "严肃",
    "gentle": "温柔",
    "affectionate": "亲切",
    "embarrassed": "尴尬",
    "calm": "平静",
    "soft": "柔和",
    "shouting": "喊叫",
    "terrified": "恐慌",
    "unfriendly": "不友好",
    "whispering": "耳语",
    "hopeful": "希望"
}

# 角色映射
VOICE_ROLES = {
    "Girl": "女孩",
    "Boy": "男孩", 
    "YoungAdultFemale": "年轻女性",
    "YoungAdultMale": "年轻男性",
    "OlderAdultFemale": "年长女性",
    "OlderAdultMale": "年长男性",
    "SeniorFemale": "老年女性",
    "SeniorMale": "老年男性"
}

def get_voice_by_emotion(emotion: str, language: str = "zh-CN", gender: str = None) -> str:
    """根据情感和语言选择合适的语音模型"""
    voices = CHINESE_VOICES if language == "zh-CN" else ENGLISH_VOICES
    
    # 过滤符合条件的语音
    suitable_voices = []
    for voice_id, voice_info in voices.items():
        if gender and voice_info["gender"] != gender:
            continue
            
        # 检查情感适配性
        emotion_suitability = voice_info["emotion_suitability"]
        if emotion in emotion_suitability:
            suitable_voices.append((voice_id, voice_info))
    
    if not suitable_voices:
        # 如果没有找到完全匹配的，返回默认语音
        return "zh-CN-XiaoxiaoNeural" if language == "zh-CN" else "en-US-AriaNeural"
    
    # 返回第一个匹配的语音
    return suitable_voices[0][0]

def get_style_by_emotion(emotion: str, intensity: float) -> str:
    """根据情感和强度选择合适的语音风格"""
    style_mapping = {
        "喜悦": "cheerful",
        "满足": "gentle", 
        "兴奋": "cheerful",
        "愉快": "cheerful",
        "满意": "gentle",
        "轻微积极": "calm",
        "愤怒": "angry",
        "悲伤": "sad",
        "绝望": "sad",
        "担忧": "fearful",
        "不满": "disgruntled",
        "焦虑": "fearful",
        "轻微不适": "soft",
        "困惑": "embarrassed",
        "平静": "calm",
        "思考": "serious",
        "客观": "serious",
        "冷静": "calm",
        "理性": "serious"
    }
    
    base_style = style_mapping.get(emotion, "calm")
    
    # 根据强度调整风格
    if intensity > 0.8:
        if base_style == "cheerful":
            return "shouting"
        elif base_style == "sad":
            return "terrified"
        elif base_style == "angry":
            return "shouting"
    
    return base_style

def get_role_by_context(emotion: str, intensity: float, language: str = "zh-CN") -> str:
    """根据情感和上下文选择合适的角色"""
    if intensity < 0.3:
        return None  # 低强度情感不需要特定角色
    
    role_mapping = {
        "喜悦": "YoungAdultFemale" if language == "zh-CN" else "YoungAdultFemale",
        "兴奋": "YoungAdultFemale" if language == "zh-CN" else "YoungAdultFemale", 
        "愤怒": "OlderAdultMale" if language == "zh-CN" else "OlderAdultMale",
        "悲伤": "OlderAdultFemale" if language == "zh-CN" else "OlderAdultFemale",
        "绝望": "SeniorFemale" if language == "zh-CN" else "SeniorFemale",
        "思考": "OlderAdultMale" if language == "zh-CN" else "OlderAdultMale",
        "客观": "OlderAdultMale" if language == "zh-CN" else "OlderAdultMale"
    }
    
    return role_mapping.get(emotion)

def get_all_voices() -> dict:
    """获取所有可用的语音模型"""
    return {
        "chinese": CHINESE_VOICES,
        "english": ENGLISH_VOICES
    }

def get_voice_info(voice_id: str) -> dict:
    """获取特定语音模型的详细信息"""
    all_voices = {**CHINESE_VOICES, **ENGLISH_VOICES}
    return all_voices.get(voice_id, {}) 