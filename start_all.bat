@echo off
chcp 65001
REM 一键启动 EmotionSpeak 后端和前端开发环境（.bat 版，含虚拟环境）

REM 启动后端
cd backend

REM 检查并创建虚拟环境
if not exist venv (
    echo [后端] 创建 Python 虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

echo [后端] 安装依赖...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo [后端] 启动 FastAPI...
start cmd /k "chcp 65001 && call venv\Scripts\activate.bat && uvicorn main:app --reload"
cd ..

REM 检查 frontend/index.html 是否存在
if exist frontend\index.html (
    echo [前端] 检测到 index.html，直接用浏览器打开 frontend\index.html 即可，无需 npm。
    start frontend\index.html
)

echo 后端和前端已分别在新命令行窗口启动。
echo 如需关闭，请手动关闭对应的命令行窗口。 