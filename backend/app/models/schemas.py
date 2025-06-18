from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str

class TTSRequest(BaseModel):
    text: str
    speed: float = 1.0
    volume: str = "+0dB"
    pitch: str = "default"
    voice: str = "zh-CN-XiaoxiaoNeural" 