@echo off
REM AegisAI Launcher for Windows
REM Double-click this file to start AegisAI

echo ========================================
echo    AegisAI Emergency Detection System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    echo.
    pause
    exit /b 1
)

REM Check if in virtual environment
if not defined VIRTUAL_ENV (
    echo Checking for virtual environment...
    if exist "aegis_env\Scripts\activate.bat" (
        echo Activating virtual environment...
        call aegis_env\Scripts\activate.bat
    ) else (
        echo.
        echo WARNING: Virtual environment not found
        echo It's recommended to create one:
        echo    python -m venv aegis_env
        echo    aegis_env\Scripts\activate
        echo    pip install -r requirements.txt
        echo.
        set /p continue="Continue without virtual environment? (Y/N): "
        if /i not "%continue%"=="Y" exit /b 1
    )
)

echo.
echo Starting AegisAI...
echo.

REM Try to run enhanced version first, then basic version
if exist "aegis_ai_enhanced.py" (
    python aegis_ai_enhanced.py
) else if exist "aegis_ai_main.py" (
    python aegis_ai_main.py
) else (
    echo ERROR: Cannot find main application files
    echo Please ensure aegis_ai_enhanced.py or aegis_ai_main.py exists
    echo.
    pause
    exit /b 1
)

echo.
echo AegisAI stopped
pause