# EmotionSpeak

基于 FastAPI + Azure AI 的情感分析与语音合成应用

## 项目简介
EmotionSpeak 是一个结合了文本情感分析与语音合成的 Web 应用。用户输入文本后，系统会分析其情感（积极/消极/中性），并根据情感动态调整语音参数进行朗读。前端界面美观，后端基于 FastAPI，调用 Azure 认知服务。

## 目录结构
```
EmotionSpeak2/
├── backend/           # 后端 FastAPI 服务
│   ├── main.py        # FastAPI 入口
│   ├── requirements.txt
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

### 2. 配置 Azure 密钥
后端依赖 Azure 认知服务，请在 `backend/` 目录下新建 `.env` 文件，内容参考：
```ini
AZURE_TEXT_ANALYTICS_KEY=your_text_analytics_key
AZURE_TEXT_ANALYTICS_ENDPOINT=https://your-text-analytics-endpoint.cognitiveservices.azure.com/
AZURE_TTS_KEY=your_tts_key
AZURE_TTS_ENDPOINT=https://your-tts-endpoint.cognitiveservices.azure.com/
```

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
- **语音合成**：调用 Azure TTS，情感驱动语速、音量、音调变化。
- **前端可视化**：使用 Chart.js 展示情感置信度饼图，界面美观简洁。

## 依赖
- 后端：FastAPI, Uvicorn, python-dotenv, azure-ai-textanalytics, azure-cognitiveservices-speech
- 前端：原生 HTML/CSS/JS, Chart.js（CDN）

## 许可证
MIT

---
如有问题欢迎提 issue 或 PR！ 