@echo off
chcp 65001 >nul
echo ========================================
echo   Music Format Converter - Launch Script
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Error: Virtual environment not found!
    echo Please run first: uv venv
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
.venv\Scripts\python -c "import PyQt6, pydub" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Error: Dependencies not installed!
    echo Please run first: uv pip install -r requirements.txt
    pause
    exit /b 1
)

echo [OK] Environment check passed!
echo.
echo Starting program...
echo.

REM Start program
.venv\Scripts\python main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Program failed to start!
    echo Please check the error message.
    pause
    exit /b 1
)

echo.
echo Program exited.
pause
