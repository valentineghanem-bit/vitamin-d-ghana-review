@echo off
REM Windows launcher -- Vitamin D Ghana Dashboard
cd /d "%~dp0"
echo Starting Vitamin D Ghana Dashboard...
echo Open http://127.0.0.1:8050 in your browser
start "" "http://127.0.0.1:8050"
timeout /t 1 /nobreak >nul
python app.py
pause
