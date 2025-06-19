import requests
import json
import logging
import re
from app.core.config import settings
from app.services.voice_catalog import get_all_voices, get_voice_info
from typing import Dict, Any

def build_voice_catalog_prompt():
    voices = get_all_voices()
    prompt = """
【可选语音模型及参数】
"""
    for lang, vdict in voices.items():
        prompt += f"\n{('中文' if lang=='chinese' else '英文')}语音模型:"
        for vid, vinfo in vdict.items():
            prompt += f"\n- {vid}（{vinfo['name']}，{vinfo['description']}，性别:{'女' if vinfo['gender']=='female' else '男'}）"
            prompt += f"\n  支持角色: {', '.join(vinfo['roles'])}"
            prompt += f"\n  支持风格: {', '.join(vinfo['styles'])}"
    prompt += "\n【注意】voice、role、style必须严格选择上表可用项，role必须在voice支持的角色列表中，style必须在voice支持的风格列表中。"
    return prompt

PROMPT_TEMPLATE = """
你是一个专业的语音合成参数推荐专家。请根据下方文本和情感分析结果，为Azure TTS推荐最合适的参数，只需返回一个标准JSON对象，字段如下：
- voice: 语音模型ID（必须是官方支持的ID）
- style: 语音风格（字符串）
- rate: 语速（如+10%）
- pitch: 音调（如+2st）
- role: 角色（可为null或官方支持的角色）
- styledegree: 风格强度（如1.0）

{voice_catalog}

只需返回一个JSON对象，不要多余解释。

文本: {text}
情感分析: {emotion_data}
"""

def analyze_with_wenxin(text: str, emotion_data: Dict[str, Any]) -> Dict[str, Any]:
    if not settings.BAIDU_WENXIN_API_KEY:
        raise RuntimeError("Baidu Wenxin API not configured")
    try:
        url = "https://qianfan.baidubce.com/v2/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.BAIDU_WENXIN_API_KEY}"
        }
        voice_catalog = build_voice_catalog_prompt()
        prompt = PROMPT_TEMPLATE.format(
            text=text,
            emotion_data=json.dumps(emotion_data, ensure_ascii=False, indent=2),
            voice_catalog=voice_catalog
        )
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": "ernie-4.0-8k",
            "temperature": 0.1,
            "top_p": 0.95,
        }
        logging.info(f"Wenxin请求: {prompt[:200]}...")
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise RuntimeError(f"Wenxin API error: {response.status_code}")
        result = response.json()
        content = ''
        if 'choices' in result and result['choices']:
            content = result['choices'][0].get('message', {}).get('content', '')
        logging.info(f"Wenxin返回: {content[:200]}...")
        # 提取JSON
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if not json_match:
            raise ValueError("Wenxin未返回有效JSON")
        tts_params = json.loads(json_match.group(0))
        # 校验voice/role
        all_voices = get_all_voices()
        all_voice_ids = list(all_voices['chinese'].keys()) + list(all_voices['english'].keys())
        if tts_params.get('voice') not in all_voice_ids:
            raise ValueError(f"Wenxin返回的voice不在官方列表: {tts_params.get('voice')}")
        voice_info = get_voice_info(tts_params['voice'])
        if tts_params.get('role') and voice_info:
            if tts_params['role'] not in voice_info.get('roles', []):
                raise ValueError(f"Wenxin返回的role不在voice支持列表: {tts_params['role']}")
        # 其它字段简单校验
        for k in ['style', 'rate', 'pitch']:
            if k not in tts_params or not isinstance(tts_params[k], str):
                raise ValueError(f"Wenxin返回的{k}字段无效")
        # styledegree允许float或str，最终转为str
        if 'styledegree' not in tts_params or not isinstance(tts_params['styledegree'], (str, float, int)):
            raise ValueError("Wenxin返回的styledegree字段无效")
        tts_params['styledegree'] = str(tts_params['styledegree'])
        return tts_params
    except Exception as e:
        logging.error(f"Wenxin分析失败: {str(e)}")
        raise 