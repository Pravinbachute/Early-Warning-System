@echo off
echo.
echo ================================================
echo    ENTERPRISE RISK INTELLIGENCE PLATFORM
echo           Professional Edition v3.0
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo After installation, restart Command Prompt and try again.
    pause
    exit /b 1
)

REM Display Python version
echo [INFO] Python version:
python --version
echo.

REM Check if app.py exists
if not exist "app.py" (
    echo [ERROR] app.py not found in current directory!
    echo.
    echo Please make sure you are in the correct folder containing:
    echo - app.py
    echo - requirements.txt
    echo - launch.bat
    pause
    exit /b 1
)

REM Install requirements
echo [INFO] Installing required packages...
echo.
pip install -r requirements.txt

echo.
echo [SUCCESS] All packages installed!
echo.

REM Clear Streamlit cache
echo [INFO] Clearing application cache...
streamlit cache clear --force >nul 2>&1

echo.
echo ================================================
echo          STARTING APPLICATION...
echo ================================================
echo.
echo [INFO] Launching Enterprise Dashboard...
echo [URL] http://localhost:8501
echo.
echo [NOTE] The application will open in your default browser.
echo        If it doesn't open automatically, copy the URL above.
echo.

timeout /t 3 /nobreak >nul

REM Launch the application
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

pause