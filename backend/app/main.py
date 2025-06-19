import logging
from fastapi import FastAPI
from app.api.routes import router

# 创建 FastAPI 应用
app = FastAPI(title="EmotionSpeak API", version="1.0.0")

# 注册路由
app.include_router(router, prefix="/api/v1")

# 启动日志
logging.info("EmotionSpeak API 服务启动") 