import requests
import json
import logging
import re
from app.core.config import settings
from typing import Dict, Any, Optional

# 提示词模板
PROMPT_TEMPLATE = """
你是一个专业的情感分析和语音合成参数调整专家。我将给你一段文本及其详细的情感分析结果，你需要根据这些情感分析结果，为Azure Text-to-Speech服务推荐最合适的语音合成参数。

分析结果包含以下信息:
- overall_sentiment: 整体情感倾向 (positive/negative/neutral)
- confidence_scores: 各情感类型的置信度
- detailed_emotions: 详细情感分类及其强度
- emotion_intensity: 情感强度 (0-100)
- sentence_sentiments: 句子级情感分析

请你根据这些信息，推荐以下语音合成参数:
1. voice: 语音模型，例如:
   - 中文模型: zh-CN-XiaoxiaoNeural(女声), zh-CN-YunyangNeural(男声)等
   - 英文模型: en-US-AriaNeural(女声), en-US-GuyNeural(男声)等
2. style: 语音风格，如cheerful, sad, angry, calm等
3. rate: 语速调整，范围从"-30%"到"+30%"
4. pitch: 音调调整，范围从"-12st"到"+12st"
5. role: (可选)角色，如YoungAdultFemale, OlderAdultMale等
6. styledegree: 风格强度，范围从"0.5"到"2.0"

必须返回一个有效的JSON对象，包含以上参数。

文本内容: {text}
情感分析结果: {emotion_data}
"""

async def analyze_with_wenxin(text: str, emotion_data: Dict[str, Any]) -> Dict[str, Any]:
    """使用百度文心分析情感结果并推荐TTS参数"""
    # 确保API密钥已配置
    if not settings.BAIDU_WENXIN_API_KEY:
        logging.warning("Baidu Wenxin API not configured, falling back to rule-based params")
        return None
    
    try:
        # 准备API请求 - 使用v2 API
        url = "https://qianfan.baidubce.com/v2/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.BAIDU_WENXIN_API_KEY}"
        }
        
        # 准备提示词
        prompt = PROMPT_TEMPLATE.format(
            text=text,
            emotion_data=json.dumps(emotion_data, ensure_ascii=False)
        )
        
        # 构建请求参数
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": "ernie-4.0-8k",
            "temperature": 0.1,
            "top_p": 0.95,
        }
        
        # 发送API请求
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            logging.error(f"Error response from Baidu Wenxin API: Status code {response.status_code}")
            return None
            
        result = response.json()
        
        # 处理v2 API响应格式
        content = ""
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0].get('message', {}).get('content', '')
        
        if content:
            # 尝试从响应文本中提取JSON
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                json_text = json_match.group(0)
                
                # 提取TTS参数
                try:
                    tts_params = json.loads(json_text)
                    
                    # 检查和清理参数
                    required_keys = ['voice', 'style', 'rate', 'pitch']
                    for key in required_keys:
                        if key not in tts_params:
                            logging.warning(f"Missing required key {key} in response")
                            return None
                            
                    # 移除可能存在的无效字段
                    cleaned_params = {}
                    for key, value in tts_params.items():
                        if key in ['voice', 'style', 'rate', 'pitch', 'role', 'styledegree']:
                            cleaned_params[key] = value
                            
                    return cleaned_params
                    
                except json.JSONDecodeError:
                    return None
            else:
                return None
        else:
            return None
            
    except Exception as e:
        logging.error(f"Error using Baidu Wenxin API: {str(e)}")
        return None 