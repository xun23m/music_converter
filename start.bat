@echo off
chcp 65001 >nul
echo.
echo [音乐格式转换器] 启动中...
echo.

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [错误] 虚拟环境未找到，请先运行: uv venv
    pause
    exit /b 1
)

.venv\Scripts\python main.py
pause
