@echo off
chcp 65001 >nul
echo.
echo [Music Format Converter] Starting...
echo.

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found, please run first: uv venv
    pause
    exit /b 1
)

.venv\Scripts\python main.py
pause
