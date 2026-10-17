@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    py -m venv .venv
    if errorlevel 1 (
        echo Failed to create virtual environment. Ensure Python is installed.
        pause
        exit /b 1
    )
)

echo Activating environment and running program...
.venv\Scripts\python.exe Voice_Snake.py
pause
