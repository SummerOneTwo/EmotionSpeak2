import logging
from app.core.config import LOG_DIR, LOG_FILE
import os
from fastapi import FastAPI
from app.api.routes import router

# 日志初始化
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# 创建 FastAPI 应用
app = FastAPI(title="EmotionSpeak API", version="1.0.0")

# 注册路由
app.include_router(router, prefix="/api/v1")

# 启动日志
logging.info("EmotionSpeak API 服务启动") 