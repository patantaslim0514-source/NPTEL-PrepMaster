@echo off
title NPTEL PrepMaster AI
echo ========================================================
echo   Launching NPTEL PrepMaster AI Exam Preparation Hub
echo ========================================================
echo.
echo Starting FastAPI Web Server at http://127.0.0.1:8000 ...
echo.

start "" http://127.0.0.1:8000
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload

pause
