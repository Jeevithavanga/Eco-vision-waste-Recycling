@echo off
setlocal
cd /d "%~dp0"
echo EcoVision AI startup
if not exist "backend\app.py" (echo ERROR: backend\app.py is missing. Run this script from the complete project folder.& pause & exit /b 1)
if not exist "frontend\package.json" (echo ERROR: frontend\package.json is missing.& pause & exit /b 1)
if not exist ".venv\Scripts\python.exe" (echo Python virtual environment not found. Create it and install backend requirements first.& echo   py -m venv .venv& echo   .venv\Scripts\python -m pip install -r backend\requirements.txt& pause & exit /b 1)
where node >nul 2>nul
if errorlevel 1 (echo ERROR: Node.js is not installed or is not on PATH. Install Node.js LTS and reopen this window.& pause & exit /b 1)
if not exist "frontend\node_modules" (echo Frontend packages not found. Install them first with: cd frontend ^&^& npm install& pause & exit /b 1)
start "EcoVision AI Backend" /D "%~dp0" cmd /k ".venv\Scripts\python backend\app.py"
start "EcoVision AI Frontend" /D "%~dp0frontend" cmd /k "npm run dev"
echo Backend: http://localhost:5000/api/health
echo Frontend: http://localhost:5173
echo Keep both terminal windows open while demonstrating.
endlocal
