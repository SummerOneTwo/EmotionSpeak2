import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    AZURE_TEXT_ANALYTICS_KEY = os.getenv("AZURE_TEXT_ANALYTICS_KEY")
    AZURE_TEXT_ANALYTICS_ENDPOINT = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT")
    AZURE_TTS_KEY = os.getenv("AZURE_TTS_KEY")
    AZURE_TTS_ENDPOINT = os.getenv("AZURE_TTS_ENDPOINT")
    
    BAIDU_WENXIN_API_KEY = os.getenv("BAIDU_WENXIN_API_KEY")

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../logs')
LOG_FILE = os.path.join(LOG_DIR, 'emotion_speak.log')

settings = Settings() 