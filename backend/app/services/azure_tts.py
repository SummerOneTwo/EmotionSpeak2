import azure.cognitiveservices.speech as speechsdk
from app.core.config import settings

def synthesize_speech(text: str, speed: float, volume: str, pitch: str, voice: str):
    speech_config = speechsdk.SpeechConfig(
        subscription=settings.AZURE_TTS_KEY,
        endpoint=settings.AZURE_TTS_ENDPOINT
    )
    # 设置语音
    speech_config.speech_synthesis_voice_name = voice
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        print("Error details: {}".format(cancellation_details.error_details))
        raise Exception(f"Speech synthesis canceled: {cancellation_details.reason}, details: {cancellation_details.error_details}")
    else:
        raise Exception(f"Speech synthesis failed: {result.reason}") 