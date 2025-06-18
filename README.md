# EmotionSpeak

基于 FastAPI + Azure AI 的情感分析与语音合成应用

## 项目简介
EmotionSpeak 是一个结合了文本情感分析与语音合成的 Web 应用。用户输入文本后，系统会分析其情感（积极/消极/中性），并根据情感动态调整语音参数进行朗读。前端界面美观，后端基于 FastAPI，调用 Azure 认知服务和百度文心大模型进行高级语音参数推荐。

## 目录结构
```
EmotionSpeak2/
├── backend/           # 后端 FastAPI 服务
│   ├── main.py        # FastAPI 入口
│   ├── requirements.txt
│   ├── WENXIN_SETUP.md # 百度文心集成指南
│   ├── app/
│   │   ├── core/      # 配置与环境变量
│   │   ├── services/  # Azure 相关服务
│   │   ├── models/    # 数据模型
│   │   └── api/       # 路由
│   └── venv/          # Python 虚拟环境（已忽略）
├── frontend/          # 前端静态页面
│   ├── index.html
│   ├── main.js
│   └── style.css
└── start_all.bat      # 一键启动脚本（适用于 Windows）
```

## 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/yourname/EmotionSpeak2.git
cd EmotionSpeak2
```

### 2. 配置 API 密钥（**必须**）
**你必须在 `backend/` 目录下创建 `.env` 文件，否则后端无法正常启动。**

你可以参考 `backend/.env.example` 文件进行配置。内容如下：
```ini
# Azure认知服务配置（必需）
AZURE_TEXT_ANALYTICS_KEY=your_text_analytics_key
AZURE_TEXT_ANALYTICS_ENDPOINT=https://your-text-analytics-endpoint.cognitiveservices.azure.com/
AZURE_TTS_KEY=your_tts_key
AZURE_TTS_ENDPOINT=https://your-tts-endpoint.cognitiveservices.azure.com/

# 百度文心大模型API配置（可选但推荐，国内可直接使用）
# API Key格式示例: bce-v3/ALTAK-xxxxxxxx/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
BAIDU_WENXIN_API_KEY=your_wenxin_api_key
```

> 没有`.env`文件或密钥配置错误会导致服务启动失败。

关于百度文心API的详细设置，请参阅：
- [百度文心集成指南](backend/WENXIN_SETUP.md)

### 3. 一键启动（推荐 Windows 用户）
```bash
start_all.bat
```
脚本会自动创建虚拟环境、安装依赖并分别启动后端和前端。

### 4. 手动启动（适用于其他平台）
#### 后端
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
#### 前端
直接用浏览器打开 `frontend/index.html` 即可。

## 功能说明
- **情感分析**：调用 Azure Text Analytics API，支持中文文本，返回积极/消极/中性及置信度。
- **高级语音参数**：使用百度文心大模型，通过 AI 深度理解情感并生成更准确的语音参数。
- **语音合成**：调用 Azure TTS，情感驱动语速、音量、音调变化。
- **前端可视化**：使用 Chart.js 展示情感置信度饼图，界面美观简洁。

## 依赖
- 后端：FastAPI, Uvicorn, python-dotenv, azure-ai-textanalytics, azure-cognitiveservices-speech, requests
- 前端：原生 HTML/CSS/JS, Chart.js（CDN）

## 许可证
MIT

---
如有问题欢迎提 issue 或 PR！ 