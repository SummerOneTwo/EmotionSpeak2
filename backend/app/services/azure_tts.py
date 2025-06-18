import azure.cognitiveservices.speech as speechsdk
from app.core.config import settings
import html
import logging

def synthesize_speech(text: str, voice: str, style: str, rate: str, pitch: str, role: str = None, styledegree: str = "1.0"):
    speech_config = speechsdk.SpeechConfig(
        subscription=settings.AZURE_TTS_KEY,
        endpoint=settings.AZURE_TTS_ENDPOINT
    )
    
    # 设置输出格式
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio24Khz160KBitRateMonoMp3)
    
    # 转义文本中的特殊字符
    escaped_text = html.escape(text)
    
    # 获取语言代码
    lang_code = 'zh-CN'
    if voice.startswith('en-'):
        lang_code = 'en-US'
    
    try:
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
        
        # 构建SSML
        ssml = f"""<speak version='1.0' xml:lang='{lang_code}'>
<voice name='{voice}'>
<prosody rate='{rate}' pitch='{pitch}'>
{escaped_text}
</prosody>
</voice>
</speak>"""
        
        result = synthesizer.speak_ssml_async(ssml).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return result.audio_data
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            logging.error(f"Speech synthesis canceled: {cancellation_details.reason}")
            
            # 如果SSML失败，尝试纯文本
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return result.audio_data
            
            raise Exception(f"Speech synthesis canceled: {cancellation_details.reason}")
        else:
            raise Exception(f"Speech synthesis failed: {result.reason}")
    except Exception as e:
        logging.error(f"Error in synthesize_speech: {str(e)}")
        raise Exception(f"Speech synthesis error: {str(e)}") 