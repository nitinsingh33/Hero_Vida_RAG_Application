@echo off
echo Starting Hero Vida RAG Backend Server...
cd backend
call venv\Scripts\activate
echo.
echo ===============================================
echo Hero Vida RAG Backend Server Starting...
echo API will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo ===============================================
echo.
python main.py
pause
