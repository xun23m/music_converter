@echo off
chcp 65001 >nul
echo ========================================
echo   音乐格式转换器 - 启动脚本
echo ========================================
echo.

REM 检查虚拟环境是否存在
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] 错误：虚拟环境未找到！
    echo 请先运行: uv venv
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查依赖包...
.venv\Scripts\python -c "import PyQt6, pydub" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] 错误：依赖包未安装！
    echo 请先运行: uv pip install -r requirements.txt
    pause
    exit /b 1
)

echo [OK] 环境检查通过！
echo.
echo 正在启动程序...
echo.

REM 启动程序
.venv\Scripts\python main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] 程序启动失败！
    echo 请检查错误信息。
    pause
    exit /b 1
)

echo.
echo 程序已退出。
pause
