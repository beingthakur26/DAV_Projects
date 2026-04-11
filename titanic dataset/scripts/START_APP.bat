@echo off
REM ========================================
REM Titanic Survival Predictor - Start Script
REM ========================================

echo.
echo 🚢 Titanic Survival Predictor - Starting...
echo ========================================
echo.

REM Get the current directory
set SCRIPT_DIR=%~dp0

REM Start Backend API
echo 📍 Starting Flask API...
start cmd /k "cd /d %SCRIPT_DIR% && python app.py"

REM Wait a bit for the backend to start
timeout /t 3 /nobreak

REM Start Frontend
echo 📍 Starting React Frontend...
start cmd /k "cd /d %SCRIPT_DIR%titanic-frontend && npm run dev"

echo.
echo ✅ Both servers are starting!
echo.
echo 🔗 Frontend: http://localhost:5173
echo 🔗 API: https://titanic-survival-api-ef66.onrender.com
echo.
echo 💡 Tip: Open frontend URL in your browser
echo.
pause
