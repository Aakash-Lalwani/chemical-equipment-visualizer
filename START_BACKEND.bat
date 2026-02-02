@echo off
echo Starting Django Backend Server...
echo.
cd /d "%~dp0backend"
.venv\Scripts\python.exe manage.py runserver
