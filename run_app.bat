@echo off
title ATS Resume Builder - Streamlit App
echo ==========================================
echo Starting ATS Resume Builder...
echo ==========================================
cd /d "%~dp0"

:: Check if python is available
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python is not installed or not in your system PATH.
    echo Please install Python from https://www.python.org/ and make sure to check
    echo "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: Try to import streamlit, if it fails, install requirements
python -c "import streamlit" >nul 2>nul
if %errorlevel% neq 0 (
    echo Streamlit not found. Installing dependencies from requirements.txt...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Failed to install dependencies.
        echo Please make sure you have internet access and run 'pip install -r requirements.txt' manually.
        echo.
        pause
        exit /b 1
    )
)

echo Running from: "%~dp0"
python -m streamlit run "%~dp0app.py"
pause
