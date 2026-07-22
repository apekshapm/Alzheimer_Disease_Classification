@echo off
REM Alzheimer's Disease Classification - Setup and Run Script for Windows

echo 🧠 Alzheimer's Disease Classification Setup
echo ===========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ %PYTHON_VERSION% found
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 📥 Installing dependencies from requirements.txt...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ✅ Setup complete!
echo.
echo 📝 Next steps:
echo 1. Place your 'alzheimers_disease_data.csv' in the repository root directory
echo 2. Run the app with: streamlit run app.py
echo.
echo 🚀 To run the app:
echo    streamlit run app.py
echo.
pause