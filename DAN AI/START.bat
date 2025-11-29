@echo off
echo.
echo ======================================
echo   AI AGENT - Advanced Web Interface
echo ======================================
echo.
echo Features:
echo   * Web Search (Safe/Unrestricted)
echo   * Persistent Memory Storage
echo   * Real Tool Implementations
echo   * Advanced Command System
echo   * Beautiful Modern UI
echo.

echo Installing dependencies...
pip install -r requirements.txt -q

echo.
echo Starting Advanced Agent...
echo.
echo Open your browser to: http://localhost:5000
echo.
echo Commands: /help /tools /memory /policy /search_mode /status
echo.
echo Press CTRL+C to stop
echo.

python app.py
pause
